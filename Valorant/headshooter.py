import cv2
import numpy as np
import pyautogui
import mss

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to move the mouse to the specified (x, y) coordinate instantly
def move_mouse_instantly(x, y):
    print(f"Moving mouse to ({x}, {y})")
    screenWidth, screenHeight = pyautogui.size()
    pyautogui.moveTo(x, y)

# Main loop to continuously capture the screen and detect faces
with mss.mss() as sct:
    while True:
        # Capture the screen
        screenshot = sct.shot(output="fullscreen.png")

        screen = cv2.imread("fullscreen.png", cv2.IMREAD_COLOR)  # Load the screenshot in color

        # Detect faces in the captured screen
        faces = face_cascade.detectMultiScale(screen, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces and move the mouse to the first detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(screen, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a green rectangle around the face
            center_x = x + w // 2
            center_y = y + h // 2
            move_mouse_instantly(center_x, center_y)

        # Save the output image with rectangles drawn around detected faces
        cv2.imwrite("output.png", screen)

        # Display the output image with rectangles
        cv2.imshow("Detected Faces", screen)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cv2.destroyAllWindows()
