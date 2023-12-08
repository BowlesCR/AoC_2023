import fileinput
import itertools
import re

steps: list[str] = []
nodes: dict[str, tuple[str, str]] = {}

for line in fileinput.input():
    if len(steps) == 0:
        steps = list(line.strip())
    elif line.strip() == "":
        continue
    else:
        start, left, right = re.findall(r"\w{3}", line)
        nodes[start] = (left, right)

pos = "AAA"
count = 0
for step in itertools.cycle(steps):
    if step == "L":
        pos = nodes[pos][0]
    elif step == "R":
        pos = nodes[pos][1]
    else:
        assert False
    count += 1

    if pos == "ZZZ":
        break

print(count)
