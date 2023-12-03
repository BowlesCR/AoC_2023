import fileinput
import re

grid: list[str] = []
for line in fileinput.input():
    grid.append(line.strip())
del line

sum_ = 0

for r, row in enumerate(grid):
    for match in re.finditer(r"(\d+)", row):
        check = row[max(0, match.start() - 1) : min(len(row), match.end() + 1)]
        if any([c != "." and not c.isdigit() for c in check]):
            sum_ += int(match[0])
            continue

        if r > 0:
            check = grid[r - 1][max(0, match.start() - 1) : min(len(row), match.end() + 1)]
            if any([c != "." and not c.isdigit() for c in check]):
                sum_ += int(match[0])
                continue

        if r < len(grid) - 1:
            check = grid[r + 1][max(0, match.start() - 1) : min(len(row), match.end() + 1)]
            if any([c != "." and not c.isdigit() for c in check]):
                sum_ += int(match[0])
                continue

print(sum_)
