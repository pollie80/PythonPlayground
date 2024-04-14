import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from FaceDetection.video.UI import FaceDetectionApp

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


# Create a window and pass it to the FaceDetectionApp class
FaceDetectionApp(tk.Tk(), "Face Detection App")
