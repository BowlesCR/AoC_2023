import fileinput
import math
import re

data: list[list[int]] = []

for line in fileinput.input():
    line = line.replace(" ", "")
    data.append(list(map(int, re.findall(r"(\d+)", line))))

margin = 1
for time, dist in zip(data[0], data[1]):
    wins = 0

    disc = time**2 - 4 * -1 * (-1 * dist)
    min_t = (-time + math.sqrt(disc)) / -2
    max_t = (-time - math.sqrt(disc)) / -2

    if min_t % 1 == 0:
        min_t += 1

    if max_t % 1 == 0:
        max_t -= 1

    wins = math.floor(max_t) - math.ceil(min_t) + 1
    print(wins)
    margin *= wins

print(margin)
