import fileinput
import re


def convert(number: str):
    words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    if number in words:
        return words[number]
    else:
        return int(number)


checksum = 0

for line in fileinput.input():
    matches = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)
    checksum += (convert(matches[0]) * 10) + convert(matches[-1])

print(checksum)
