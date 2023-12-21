import fileinput
import re
from typing import TypeAlias

Point: TypeAlias = tuple[int, int]

grid: dict[Point, str] = {}


r, c = 0, 0
for line in fileinput.input():
    m = re.match(r"^([UDLR]) (\d+) \(#(\w{6})\)$", line)
    dir, count, color = m.groups()
    count = int(count)
    match dir:
        case 'U':
            for r in range(r, r - count, -1):
                grid[(r, c)] = dir
        case 'D':
            for r in range(r, r + count):
                grid[(r, c)] = dir
        case 'L':
            for c in range(c, c - count, -1):
                grid[(r, c)] = dir
        case 'R':
            for c in range(c, c + count):
                grid[(r, c)] = dir
        case _:
            assert False