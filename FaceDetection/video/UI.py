import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class FaceDetectionApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = None

        self.canvas = tk.Canvas(window, width=640, height=480)  # Adjust the dimensions as per your camera resolution
        self.canvas.pack()

        self.btn_start = tk.Button(window, text="Start", width=10, command=self.start)
        self.btn_start.pack(anchor=tk.CENTER, expand=True)

        self.btn_stop = tk.Button(window, text="Stop", width=10, command=self.stop)
        self.btn_stop.pack(anchor=tk.CENTER, expand=True)
        self.btn_stop['state'] = 'disabled'

        self.is_running = False

        self.window.mainloop()

    def start(self):
        if not self.is_running:
            self.vid = cv2.VideoCapture(self.video_source)
            self.is_running = True
            self.btn_start['state'] = 'disabled'
            self.btn_stop['state'] = 'normal'
            self.update()

    def stop(self):
        if self.is_running:
            self.vid.release()
            self.is_running = False
            self.btn_start['state'] = 'normal'
            self.btn_stop['state'] = 'disabled'

    def update(self):
        if self.is_running:
            ret, frame = self.vid.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = detect_faces(frame)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.window.after(10, self.update)