import psutil
import subprocess
import tkinter as tk
from tkinter import messagebox
import win32con
import win32gui

def get_camera_processes(camera_name=None):
    result = []
    try:
        # Run "handle.exe" from Sysinternals to check camera handles (if available)
        # fallback: scan for known camera-using processes
        known_camera_apps = [
            "chrome.exe", "msedge.exe", "teams.exe", "zoom.exe",
            "obs64.exe", "discord.exe", "skype.exe", "vlc.exe"
        ]
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() in known_camera_apps:
                    result.append(f"{proc.info['name']} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        result = [f"Error: {e}"]

    if not result:
        result = ["No active camera processes found."]
    return result

def show_popup(process_list):
    root = tk.Tk()
    root.title("Camera Monitor")
    root.attributes('-topmost', True)  # Always on top
    root.geometry("400x250")

    label = tk.Label(root, text="Apps using your camera:", font=('Segoe UI', 12, 'bold'))
    label.pack(pady=10)

    text_box = tk.Text(root, wrap='word', height=8, width=45)
    text_box.pack(padx=10)
    text_box.insert(tk.END, "\n".join(process_list))
    text_box.configure(state='disabled')

    btn = tk.Button(root, text="Close", command=root.destroy)
    btn.pack(pady=10)

    # Keep the window always on top even when focus changes
    hwnd = win32gui.FindWindow(None, "Camera Monitor")
    # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
    #                       win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    root.mainloop()

if __name__ == "__main__":
    camera_name = None  # or set your camera's friendly name here
    processes = get_camera_processes(camera_name)
    show_popup(processes)
