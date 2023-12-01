import fileinput
import re

checksum = 0

for line in fileinput.input():
    matches = re.findall(r"\d", line)
    checksum += int(f"{matches[0]}{matches[-1]}")

print(checksum)
