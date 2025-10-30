import psutil
import tkinter as tk
import win32con
import win32gui

REFRESH_INTERVAL_MS = 1000  # 1 second

KNOWN_CAMERA_APPS = {
    "chrome.exe", "msedge.exe", "teams.exe", "zoom.exe",
    "obs64.exe", "discord.exe", "skype.exe", "vlc.exe"
}

def get_camera_processes():
    result = []
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info.get('name')
                if not name:
                    continue
                if name.lower() in KNOWN_CAMERA_APPS:
                    result.append(f"{name} (PID: {proc.info['pid']})")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        result = [f"Error: {e}"]

    return result or ["No active camera processes found."]

def update_process_list(text_widget):
    processes = get_camera_processes()
    text_widget.configure(state='normal')
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, "\n".join(processes))
    text_widget.configure(state='disabled')
    text_widget.after(REFRESH_INTERVAL_MS, update_process_list, text_widget)

def ensure_always_on_top(root):
    try:
        root.update_idletasks()
        root.update()
        hwnd = root.winfo_id()
        if hwnd:
            win32gui.SetWindowPos(
                hwnd,
                win32con.HWND_TOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )
    except Exception:
        # ignore any errors (e.g. window closed) — nothing fatal
        pass
    # re-run periodically to keep it topmost if needed
    try:
        root.after(2000, ensure_always_on_top, root)
    except Exception:
        pass

def show_popup():
    root = tk.Tk()
    root.title("Camera Monitor")
    root.geometry("420x260")
    # basic Tk native topmost attribute too (helps without Win32)
    root.wm_attributes("-topmost", True)

    label = tk.Label(root, text="Apps using your camera:", font=('Segoe UI', 12, 'bold'))
    label.pack(pady=8)

    text_box = tk.Text(root, wrap='word', height=9, width=52)
    text_box.pack(padx=10)
    text_box.configure(state='disabled')

    btn = tk.Button(root, text="Close", command=root.destroy)
    btn.pack(pady=8)

    # ensure SetWindowPos runs after window exists
    root.after(100, ensure_always_on_top, root)
    update_process_list(text_box)
    root.mainloop()

if __name__ == "__main__":
    show_popup()
