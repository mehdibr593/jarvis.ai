#!/usr/bin/env python3
"""Desktop notification helper for J.A.R.V.I.S"""
import subprocess
import platform

_OS = platform.system()

def notify(title: str, message: str, icon: str = "dialog-information"):
    """Send a desktop notification."""
    try:
        if _OS == "Linux":
            subprocess.Popen([
                "notify-send",
                "-i", icon,
                "-a", "J.A.R.V.I.S",
                title, message
            ])
        elif _OS == "Windows":
            try:
                from win10toast import ToastNotifier
                ToastNotifier().show_toast(title, message, duration=5)
            except ImportError:
                import ctypes
                ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)
        elif _OS == "Darwin":
            subprocess.Popen([
                "osascript", "-e",
                f'display notification "{message}" with title "{title}"' 
            ])
    except Exception as e:
        print(f"[Notify] Failed: {e}")

def notify_jarvis_online():
    notify("J.A.R.V.I.S Online", "Welcome back, Master Mehdi. All systems ready.", "dialog-information")

def notify_jarvis_offline():
    notify("J.A.R.V.I.S Offline", "Shutting down. Goodbye, Master Mehdi.", "dialog-warning")
