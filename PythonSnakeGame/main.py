import sys
import random
import os
import time
import keyboard

os.environ['TERM'] = 'xterm'


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_board():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            position = (x, y)
            if position == food:
                print("F", end=" ")
            elif position in snake:
                if position == snake[0]:
                    print("H", end=" ")
                else:
                    print("S", end=" ")
            else:
                print(".", end=" ")
        print()


def new_food_position():
    global food
    while True:
        x = random.randint(0, WIDTH - 1)
        y = random.randint(0, HEIGHT - 1)
        position = (x, y)
        if position not in snake:
            food = position
            return food


def move_snake():
    global snake
    head_x, head_y = snake[0]

    if direction == 'up':
        new_head = (head_x, head_y - 1)
    elif direction == 'down':
        new_head = (head_x, head_y + 1)
    elif direction == 'left':
        new_head = (head_x - 1, head_y)
    elif direction == 'right':
        new_head = (head_x + 1, head_y)

    snake.insert(0, new_head)


def change_direction(key_event):
    global direction
    key = key_event.name

    if key == 'up' and direction != 'down':
        direction = 'up'
    elif key == 'down' and direction != 'up':
        direction = 'down'
    elif key == 'left' and direction != 'right':
        direction = 'left'
    elif key == 'right' and direction != 'left':
        direction = 'right'


def game_over():
    head_x, head_y = snake[0]
    return (
        head_x < 0 or head_x >= WIDTH or
        head_y < 0 or head_y >= HEIGHT or
        snake[0] in snake[1:]
    )


def restart_game():
    global snake, direction, food, game_is_over, WIDTH, HEIGHT
    WIDTH, HEIGHT = 10, 10
    snake = [(1, 3), (1, 2), (1, 1)]
    direction = 'down'
    food = None
    food = new_food_position()
    game_is_over = False


if __name__ == '__main__':
    restart_game()

    keyboard.on_press_key("up", change_direction)
    keyboard.on_press_key("down", change_direction)
    keyboard.on_press_key("left", change_direction)
    keyboard.on_press_key("right", change_direction)
    keyboard.on_press_key("r", lambda e: restart_game())

    food = new_food_position()

    while True:
        clear_screen()
        print_board()

        if game_is_over:
            print("Game over! Press 'R' to restart or Ctrl+C to exit.")
            time.sleep(0.1)
            continue

        move_snake()

        if food == snake[0]:
            food = new_food_position()
        else:
            snake.pop()

        game_is_over = game_over()
        time.sleep(1)

