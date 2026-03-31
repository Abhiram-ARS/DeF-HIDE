# 🛡️ DeF-HIDE
### Defensive Framework for HID Exploits

---

## 📌 Overview

**DeF-HIDE** is a lightweight cybersecurity tool designed to detect and control suspicious keyboard activity caused by **HID (Human Interface Device) attacks**.

It focuses on preventing unauthorized command execution by intercepting the **Win + R (Run Dialog)** shortcut and asking for user confirmation.

---

## 🚨 Problem

Malicious devices can act as keyboards and automatically execute harmful commands by simulating keystrokes.

Example:

* Open Run dialog (`Win + R`)
* Execute PowerShell commands
* Download malware

---

## 💡 Solution

DeF-HIDE:

* Monitors keyboard input in real-time
* Detects `Win + R` usage
* Displays a confirmation dialog
* Allows or blocks execution based on user choice

---

## ⚙️ Features

* ✅ Detects `Win + R` shortcut
* ✅ Optional key suppression
* ✅ Simple popup alert using Tkinter
* ✅ Thread-safe event handling
* ✅ Easy to use and lightweight

---

## ▶️ How to Run

```bash
python main.pyw
```

---

## 🎯 Purpose

This project is built for:

* Cybersecurity learning
* Demonstrating HID attack prevention
* Academic projects and competitions

---

## 👨‍💻 Author

*[Abhiram S](https://github.com/Abhiram-ARS)*

## 📜 License
This Project is licensed under [MIT Liscense](https://github.com/Abhiram-ARS/DeF-HIDE/blob/main/LICENSE).
This project is for educational and ethical use only.

