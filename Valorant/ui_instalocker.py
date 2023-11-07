import pyautogui
import keyboard
import tkinter as tk
import threading

# Define agent information
agent_block_size = 85
lock_coordinate = (955, 725)
first_agent_coordinate = (615, 845)
agents_positions = [
    ["Astra", "Breach", "Brimstone", "Chamber", "Cypher", "Deadlock", "Fade", "Gekko", "Harbour"],
    ["Iso", "Jett", "KAY/O", "Killjoy", "Neon", "Omen", "Phoenix", "Raze", "Reyna"],
    ["Sage", "Skye", "Sova", "Viper", "Yoru"]
]

# Create a function to find agent coordinates
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

# Create a function to click an agent and lock in
def click_agent(selected_agent_coordinate):
    if selected_agent_coordinate is not None:
        pyautogui.moveTo(selected_agent_coordinate)
        pyautogui.click()
        pyautogui.moveTo(lock_coordinate)
        pyautogui.click()

# Create a function to handle button click events
def on_agent_button_click(agent_name):
    selected_agent_coordinate = find_agent_coordinates(agent_name)
    while not keyboard.is_pressed("esc"):
        click_agent(selected_agent_coordinate)

# Create the main application window
app = tk.Tk()
app.title("Agent Selection")

# Create buttons for each agent
for row in agents_positions:
    for agent_name in row:
        agent_button = tk.Button(app, text=agent_name, command=lambda name=agent_name: on_agent_button_click(name))
        agent_button.pack()

# Create an exit button
exit_button = tk.Button(app, text="Exit", command=app.destroy)
exit_button.pack()

app.mainloop()
