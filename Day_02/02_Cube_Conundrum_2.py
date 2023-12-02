import fileinput
import re
from math import prod

re_game = re.compile(r"^Game (\d+): (.+)\n$")
re_cube = re.compile(r"(\d+) (red|blue|green)")

sum_ = 0

for line in fileinput.input():
    gamenum, gamestr = re_game.match(line).groups()
    rounds = gamestr.split(";")

    counts = {"red": 0, "green": 0, "blue": 0}

    for r in rounds:
        for cube in re_cube.findall(r):
            count, color = cube
            counts[color] = max(counts[color], int(count))

    power = prod(counts.values())
    print(power)
    sum_ += power

print(sum_)
