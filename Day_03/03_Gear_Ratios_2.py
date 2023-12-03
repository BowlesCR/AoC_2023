import fileinput
import re

grid: list[str] = []
for line in fileinput.input():
    grid.append(line.strip())
del line

sum_ = 0

matches: list[tuple[int, int, int, int]] = []

# Find part numbers
for r, row in enumerate(grid):
    for match in re.finditer(r"(\d+)", row):
        matches.append((r, match.start(), match.end(), int(match[0])))

# Find gears
for r, row in enumerate(grid):
    for match in re.finditer(r"\*", row):
        nums = [m for m in matches if (r - 1 <= m[0] <= r + 1) and (m[1] - 1 <= match.start() <= m[2])]
        if len(nums) == 2:
            sum_ += nums[0][3] * nums[1][3]

print(sum_)
