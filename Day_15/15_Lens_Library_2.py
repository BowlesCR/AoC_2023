import re
from collections import deque, defaultdict
import fileinput


def hash_1a(line: str) -> int:
    val = 0
    for c in line:
        val += ord(c)
        val *= 17
        val %= 256
    return val


for line in fileinput.input():
    line = line.strip()

    boxes: defaultdict[int, deque[tuple[str, int]]] = defaultdict(deque)

    for step in line.split(","):
        m = re.match(r"^(\w+)([-=])(\d+)?$", step)

        label = m.group(1)
        box = hash_1a(label)
        op = m.group(2)
        if op == "=":
            focal = int(m.group(3))

        if op == "-":
            for lens in boxes[box]:
                if lens[0] == label:
                    boxes[box].remove(lens)
                    break
        elif op == "=":
            insert = True
            for lens in boxes[box]:
                if lens[0] == label:
                    i = boxes[box].index(lens)
                    boxes[box].remove(lens)
                    boxes[box].insert(i, (label, focal))
                    insert = False
                    break
            if insert:
                boxes[box].append((label, focal))

    sum_fp = 0
    for b in range(256):
        for i, lens in enumerate(boxes[b], start=1):
            fp = (b + 1) * i * lens[1]
            sum_fp += fp

    print(sum_fp)
