import pyautogui
import keyboard
import sys

agent_block_size = 85
lock_coordinate = (955, 725)
first_agent_coordinate = (615, 845)
selected_agent = "Yoru"
# agents orders
agents_positions = [
    ["Astra", "Breach", "Brimstone", "Chamber", "Cypher", "Deadlock", "Fade", "Gekko", "Harbour"],
    ["Iso", "Jett", "KAY/O", "Killjoy", "Neon", "Omen", "Phoenix", "Raze", "Reyna"],
    ["Sage", "Skye", "Sova", "Viper", "Yoru"]
]
agent_row = -1
agent_col = -1

for row_idx, row in enumerate(agents_positions):
    if selected_agent in row:
        agent_row = row_idx
        agent_col = row.index(selected_agent)
        break
# print(f"r,c {agent_row, agent_col}") # test correct position
if agent_row != -1 and agent_col != -1:
    selected_agent_coordinate = (
        first_agent_coordinate[0] + agent_col * agent_block_size,
        first_agent_coordinate[1] + agent_row * agent_block_size
    )
    print(f"Coordinates for {selected_agent}: {selected_agent_coordinate}")
else:
    print(f"{selected_agent} not found in the agents_positions list.")
    sys.exit()


def on_f12_pressed(e):
    if e.event_type == keyboard.KEY_DOWN:
        pyautogui.moveTo(selected_agent_coordinate)
        pyautogui.click()
        pyautogui.moveTo(lock_coordinate)
        pyautogui.click()


keyboard.on_press_key("F12", on_f12_pressed)
keyboard.wait("esc")

# Perform the mouse movement and clicking while F12 is held down
# while True:
    # # to get position
    # event = pyautogui.mouseInfo()
    # if event["left"]:
    #     x, y = pyautogui.position()
    #     print(f"Left Click at ({x}, {y})")