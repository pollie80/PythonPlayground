import cv2
import tkinter as tk
from tkinter import filedialog
import pygetwindow as gw

# Load the pre-trained Haar Cascade face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
acceptable_file_types = [
    ('Image files', '*.png;*.jpg;*.jpeg'),
    ('PNG files', '*.png'),
    ('JPEG files', '*.jpg;*.jpeg')
]

# Load the image
root = tk.Tk()
root.withdraw()  # Hide the main window
image_path = filedialog.askopenfilename(title='Select an Image File', filetypes=acceptable_file_types)
if not image_path:
    print('No file selected.')
image = cv2.imread(image_path)

# Convert the image to grayscale (required for face detection)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangles around the detected faces
print(f"detected {len(faces)} faces")
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

# Display the image with detected faces - windows are acting weird
window_title = 'Detected Faces'
cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
cv2.imshow(window_title, image)
try:
    win = gw.getWindowsWithTitle(window_title)[0]  # Find the window
    if win:
        win.activate()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except Exception as e:
    print("Failed to bring window to the foreground:", e)

print("fin")
