import fileinput
import re

points = 0
for line in fileinput.input():
    halves = line.split(":")[1].split("|")
    winning: set[int] = set(map(int, re.findall(r"(\d+)", halves[0])))
    have: set[int] = set(map(int, re.findall(r"(\d+)", halves[1])))

    matches = have.intersection(winning)
    if matches:
        points += 2 ** (len(matches) - 1)

print(points)
