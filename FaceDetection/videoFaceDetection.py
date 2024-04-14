import cv2
import tkinter as tk
from PIL import Image, ImageTk

# Load the pre-trained Haar Cascade face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# Function to detect faces in the image
def detect_faces(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return frame


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


# Create a window and pass it to the FaceDetectionApp class
FaceDetectionApp(tk.Tk(), "Face Detection App")
