import pyautogui
import keyboard
import sys

# Define agent information
agent_block_size = 85
lock_coordinate = (955, 725)
first_agent_coordinate = (615, 845)
selected_agent = "Yoru"
agents_positions = [
    ["Astra", "Breach", "Brimstone", "Chamber", "Cypher", "Deadlock", "Fade", "Gekko", "Harbour"],
    ["Iso", "Jett", "KAY/O", "Killjoy", "Neon", "Omen", "Phoenix", "Raze", "Reyna"],
    ["Sage", "Skye", "Sova", "Viper", "Yoru"]
]


def find_agent_coordinates(selected_agent):
    agent_row = -1
    agent_col = -1

    for row_idx, row in enumerate(agents_positions):
        if selected_agent in row:
            agent_row = row_idx
            agent_col = row.index(selected_agent)
            break

    if agent_row != -1 and agent_col != -1:
        selected_agent_coordinate = (
            first_agent_coordinate[0] + agent_col * agent_block_size,
            first_agent_coordinate[1] + agent_row * agent_block_size
        )
        print(f"Coordinates for {selected_agent}: {selected_agent_coordinate}")
        return selected_agent_coordinate
    else:
        print(f"{selected_agent} not found in the agents_positions list.")
        return None


def click_agent(selected_agent_coordinate):
    if selected_agent_coordinate is not None:
        pyautogui.moveTo(selected_agent_coordinate)
        pyautogui.click()
        pyautogui.moveTo(lock_coordinate)
        pyautogui.click()


def on_hotkey_pressed(agent_name):
    selected_agent_coordinate = find_agent_coordinates(agent_name)
    click_agent(selected_agent_coordinate)


# Add hotkey listeners for each agent
for row in agents_positions:
    for agent_name in row:
        hotkey = agent_name[0]
        keyboard.add_hotkey(hotkey, lambda agent_name=agent_name: on_hotkey_pressed(agent_name))

keyboard.wait("esc")
