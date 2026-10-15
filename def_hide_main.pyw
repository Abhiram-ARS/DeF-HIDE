# -----------------------------------------------
# Project - Def-HIDE, Defensive Framework for HID Explitation
# Version - v1.2
# Filename - def_hide_main.pyw
# Author - Abhiram S [https://github.com/Abhiram-ARS]
# Date - 31-03-2026
# -----------------------------------------------
import keyboard
import queue
import subprocess
import threading
import tkinter as tk


event_queue = queue.Queue()
alert_lock = threading.Lock()
alert_pending = False


def on_shortcut_detected(shortcut_name):
    global alert_pending

    with alert_lock:
        if alert_pending:
            return
        alert_pending = True

    event_queue.put(shortcut_name)


def open_run_dialog():
    subprocess.Popen([
        "explorer.exe",
        "shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}"
    ])


def show_radio_dialog(root, shortcut_name):
    result = {"action": "skip"}

    dialog = tk.Toplevel()
    dialog.title("⚠️ DeF-HIDE Alert ! ⚠️")
    dialog.resizable(False, False)
    dialog.attributes("-topmost", True)
    dialog.grab_set()

    action_var = tk.StringVar(value="skip")

    frame = tk.Frame(dialog, padx=16, pady=12)
    frame.pack(fill="both", expand=True)

    tk.Label(
        frame,
        text=f"{shortcut_name} detected. Choose what to do:"
    ).pack(anchor="w", pady=(0, 8))

    if shortcut_name == "Win + R":
        tk.Radiobutton(
            frame,
            text="✅ ALLOW",
            variable=action_var,
            value="open"
        ).pack(anchor="w")

        tk.Radiobutton(
            frame,
            text="❌ DENY",
            variable=action_var,
            value="skip"
        ).pack(anchor="w")

    elif shortcut_name == "Alt + F4":
        tk.Radiobutton(
            frame,
            text="✅ ALLOW",
            variable=action_var,
            value="allow"
        ).pack(anchor="w")

        tk.Radiobutton(
            frame,
            text="❌ DENY",
            variable=action_var,
            value="skip"
        ).pack(anchor="w")

    button_row = tk.Frame(frame)
    button_row.pack(fill="x", pady=(12, 0))

    def on_ok():
        result["action"] = action_var.get()
        dialog.destroy()

    def on_close():
        result["action"] = "skip"
        dialog.destroy()

    dialog.protocol("WM_DELETE_WINDOW", on_close)

    tk.Button(
        button_row,
        text="OK",
        width=10,
        command=on_ok
    ).pack(side="right")

    dialog.update_idletasks()

    width = dialog.winfo_reqwidth()
    height = dialog.winfo_reqheight()

    # Set a sensible default/minimum size while keeping the dialog centered
    target_width = max(width, 360)
    target_height = max(height, 160)

    x = root.winfo_screenwidth() // 2 - target_width // 2
    y = root.winfo_screenheight() // 2 - target_height // 2

    dialog.geometry(f"{target_width}x{target_height}+{x}+{y}")
    dialog.minsize(target_width, target_height)
    dialog.resizable(True, True)

    dialog.lift()
    dialog.focus_force()

    dialog.wait_window()

    return result["action"]


def trigger_alt_f4():
    keyboard.send("alt+f4")


def process_events(root):
    global alert_pending

    while not event_queue.empty():
        event = event_queue.get_nowait()

        try:
            if event == "Win + R":
                print("Win+R intercepted.")

                action = show_radio_dialog(root, "Win + R")

                if action == "open":
                    open_run_dialog()

            elif event == "Alt + F4":
                print("Alt+F4 intercepted.")

                action = show_radio_dialog(root, "Alt + F4")

                if action == "allow":
                    trigger_alt_f4()

        except Exception as exc:
            print(f"Dialog error: {exc}")

        finally:
            with alert_lock:
                alert_pending = False

    root.after(100, process_events, root)


def stop_app(root):
    keyboard.clear_all_hotkeys()

    try:
        root.after(0, root.quit)
    except tk.TclError:
        pass


def main():
    print("Listening for Win + R and Alt + F4...")
    print("Press ESC to stop.")

    root = tk.Tk()
    root.withdraw()

    # Win + R
    try:
        keyboard.add_hotkey(
            'windows+r',
            lambda: on_shortcut_detected("Win + R"),
            suppress=True
        )

        print("Registered Win+R (suppressed).")

    except Exception as exc:
        print(f"Win+R suppress failed ({exc}).")

        keyboard.add_hotkey(
            'windows+r',
            lambda: on_shortcut_detected("Win + R"),
            suppress=False
        )

    # Alt + F4
    try:
        keyboard.add_hotkey(
            'alt+f4',
            lambda: on_shortcut_detected("Alt + F4"),
            suppress=True
        )

        print("Registered Alt+F4 (suppressed).")

    except Exception as exc:
        print(f"Alt+F4 suppress failed ({exc}).")

        keyboard.add_hotkey(
            'alt+f4',
            lambda: on_shortcut_detected("Alt + F4"),
            suppress=False
        )

    # ESC to exit
    keyboard.add_hotkey(
        'esc',
        lambda: stop_app(root)
    )

    try:
        process_events(root)
        root.mainloop()

    except KeyboardInterrupt:
        print("\nCtrl+C detected. Exiting gracefully...")

    finally:
        keyboard.clear_all_hotkeys()

        try:
            root.destroy()
        except tk.TclError:
            pass


if __name__ == "__main__":
    main()
