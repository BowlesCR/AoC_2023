import fileinput
import itertools
import math
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

pos = [p for p in nodes if p.endswith("A")]
count = 0
factors = [0] * len(pos)
for step in itertools.cycle(steps):
    count += 1
    for i, p in enumerate(pos):
        pos[i] = nodes[p][0 if step == "L" else 1]
        if pos[i].endswith("Z") and factors[i] == 0:
            factors[i] = count

    if all(factors):
        break

print(math.lcm(*factors))
