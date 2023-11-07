import pyautogui
import keyboard

# todo use listener
# todo use 3d array instead
selected_agent = "sova"
# where the agents are on screen
agents_positions = {
    "astra": (625, 840),
    "breach": (715, 840),
    "brim": (790, 840),
    "chamber": (790, 840),
    "cypher": (790, 840),
    "deadlock": (790, 840),
    "fade": (790, 840),
    "gekko": (790, 840),
    "harbour": (790, 840),
    "iso": (625, 915),
    "raze": (1215, 915)
}
lock_positions = (955, 725)

# Perform the mouse movement and clicking while F12 is held down
while True:
    if keyboard.is_pressed('F12'):
        pyautogui.moveTo(agents_positions[selected_agent])
        pyautogui.click()
        pyautogui.moveTo(lock_positions)
        pyautogui.click()
    # to get position
    # event = pyautogui.mouseInfo()
    # if event["left"]:
    #     x, y = pyautogui.position()
    #     print(f"Left Click at ({x}, {y})")