import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab

# Define the range of purple color in HSV format
purple_lower = np.array([120, 50, 50])
purple_upper = np.array([160, 255, 255])

# Function to find the center of the detected figure
def find_center(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (cX, cY)
    else:
        return None

while True:
    # Capture the screen
    screenshot = np.array(ImageGrab.grab())

    # Convert the screenshot to HSV color space
    hsv_frame = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

    # Create a mask to identify purple color
    mask = cv2.inRange(hsv_frame, purple_lower, purple_upper)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Find the center of the detected figure
        center = find_center(contour)
        if center:
            # Move the mouse to the center of the figure's head
            x, y = center
            pyautogui.moveTo(x, y)

    # Display the original frame with the purple outline
    cv2.imshow("Purple Figures Detection", screenshot)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
