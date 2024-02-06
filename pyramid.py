import math

width = 5

for i in range(0, width):
    front_and_back = " " * math.floor((width - i) / 2)
    middle = "*" * (i + 1)
    print(front_and_back, middle, front_and_back)