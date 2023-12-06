import fileinput
import re

data: list[list[int]] = []

for line in fileinput.input():
    data.append(list(map(int, re.findall(r"(\d+)", line))))

margin = 1
for time, dist in zip(data[0], data[1]):
    wins = 0
    for t in range(time):
        d = (time - t) * (t)
        if d > dist:
            wins += 1
    margin *= wins

print(margin)
