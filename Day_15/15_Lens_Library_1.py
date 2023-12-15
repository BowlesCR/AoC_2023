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

    print(sum([hash_1a(step) for step in line.split(",")]))
