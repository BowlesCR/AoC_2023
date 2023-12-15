import fileinput

type Point = tuple[int, int]

round_rocks: dict[Point, str] = {}
cube_rocks: dict[Point, str] = {}
height = 0

for r, line in enumerate(fileinput.input()):
    for c, val in enumerate(line.strip()):
        if val == ".":
            continue
        elif val == "O":
            round_rocks[(r, c)] = val
        elif val == "#":
            cube_rocks[(r, c)] = val
        else:
            assert False
    height = r + 1
del r, line, c, val

for rock in round_rocks:
    new_r = rock[0]
    for r in range(rock[0] - 1, -1, -1):
        if (r, rock[1]) not in cube_rocks:
            new_r = r
        else:
            break

    cube_rocks[(new_r, rock[1])] = "O"

print(sum([height - rock[0] for rock in cube_rocks if cube_rocks[rock] == "O"]))
