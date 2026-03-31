# -----------------------------------------------
# Project - Def-HIDE, Defensive Framework for HID Explitation
# Version - v1.1
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


def on_run_shortcut():
    global alert_pending
    with alert_lock:
        if alert_pending:
            return
        alert_pending = True
    event_queue.put("show_dialog")


def open_run_dialog():
    subprocess.Popen(["explorer.exe", "shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}"])


def show_radio_dialog(root):
    result = {"action": "open"}

    # Use a standalone toplevel so it can show even when root is withdrawn.
    dialog = tk.Toplevel()
    dialog.title("Hotkey Alert")
    dialog.resizable(False, False)
    dialog.attributes("-topmost", True)
    dialog.grab_set()

    action_var = tk.StringVar(value="skip")

    frame = tk.Frame(dialog, padx=16, pady=12)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Win + R detected. Choose what to do:").pack(anchor="w", pady=(0, 8))

    tk.Radiobutton(frame, text="Open Run dialog", variable=action_var, value="open").pack(anchor="w")
    tk.Radiobutton(frame, text="Do not open Run dialog", variable=action_var, value="skip").pack(anchor="w")

    button_row = tk.Frame(frame)
    button_row.pack(fill="x", pady=(12, 0))

    def on_ok():
        result["action"] = action_var.get()
        dialog.destroy()

    def on_close():
        result["action"] = "skip"
        dialog.destroy()

    dialog.protocol("WM_DELETE_WINDOW", on_close)

    tk.Button(button_row, text="OK", width=10, command=on_ok).pack(side="right")

    dialog.update_idletasks()
    width = dialog.winfo_reqwidth()
    height = dialog.winfo_reqheight()
    x = root.winfo_screenwidth() // 2 - width // 2
    y = root.winfo_screenheight() // 2 - height // 2
    dialog.geometry(f"{width}x{height}+{x}+{y}")
    dialog.lift()
    dialog.focus_force()

    dialog.wait_window()
    return result["action"] == "open"


def process_events(root):
    global alert_pending
    while not event_queue.empty():
        event = event_queue.get_nowait()
        if event == "show_dialog":
            print("Win+R intercepted. Showing dialog...")
            try:
                should_open_run = show_radio_dialog(root)
                if should_open_run:
                    open_run_dialog()
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
    print("Listening for Win + R... Press ESC to stop.")

    root = tk.Tk()
    root.withdraw()

    try:
        keyboard.add_hotkey('windows+r', on_run_shortcut, suppress=True)
        print("Registered hotkey: Win+R (suppressed).")
    except Exception as exc:
        print(f"Win+R suppress failed ({exc}). Falling back to non-suppressed hotkey.")
        keyboard.add_hotkey('windows+r', on_run_shortcut, suppress=False)
        print("Registered hotkey: Win+R (non-suppressed).")

    keyboard.add_hotkey('esc', lambda: stop_app(root))

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
