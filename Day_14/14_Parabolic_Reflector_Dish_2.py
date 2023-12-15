import fileinput
import pprint
import sys
from collections import OrderedDict
from functools import cache, lru_cache
from typing import TypeAlias

Point: TypeAlias = tuple[int, int]


class Platform:
    def __init__(self, round_rocks: set[Point], cube_rocks: set[Point], height: int, width: int):
        self.round_rocks = round_rocks
        self.cube_rocks = cube_rocks
        self.height = height
        self.width = width

    def calc_load(self) -> int:
        total_load = 0
        for rock in self.round_rocks:
            load = self.height - rock[0]
            total_load += load
        return total_load

    @cache
    def north(self):
        new_round_rocks: set[Point] = set()

        for rock in sorted(self.round_rocks):
            new_r = rock[0]
            for r in range(rock[0] - 1, -1, -1):
                if (r, rock[1]) not in self.cube_rocks and (r, rock[1]) not in new_round_rocks:
                    new_r = r
                else:
                    break

            new_round_rocks.add((new_r, rock[1]))

        return new_round_rocks

    @cache
    def south(self):
        new_round_rocks: set[Point] = set()

        for rock in sorted(self.round_rocks, reverse=True):
            new_r = rock[0]
            for r in range(rock[0] + 1, self.height):
                if (r, rock[1]) not in self.cube_rocks and (r, rock[1]) not in new_round_rocks:
                    new_r = r
                else:
                    break

            new_round_rocks.add((new_r, rock[1]))

        return new_round_rocks

    @cache
    def west(self):
        new_round_rocks: set[Point] = set()

        for rock in sorted(self.round_rocks, key=lambda x: x[1]):
            new_c = rock[1]
            for c in range(rock[1] - 1, -1, -1):
                if (rock[0], c) not in self.cube_rocks and (rock[0], c) not in new_round_rocks:
                    new_c = c
                else:
                    break

            new_round_rocks.add((rock[0], new_c))

        return new_round_rocks

    @cache
    def east(self):
        new_round_rocks: set[Point] = set()

        for rock in sorted(self.round_rocks, key=lambda x: x[1], reverse=True):
            new_c = rock[1]
            for c in range(rock[1] + 1, self.width):
                if (rock[0], c) not in self.cube_rocks and (rock[0], c) not in new_round_rocks:
                    new_c = c
                else:
                    break

            new_round_rocks.add((rock[0], new_c))

        return new_round_rocks

    def cycle(self):
        self.round_rocks = self.north()
        self.round_rocks = self.west()
        self.round_rocks = self.south()
        self.round_rocks = self.east()

    def __eq__(self, other):
        return self.round_rocks == other.round_rocks

    def __hash__(self):
        return hash(frozenset(sorted(self.round_rocks)))

    def toGrid(self):
        grid = []
        for r in range(self.height):
            grid.append([])
            for c in range(self.width):
                p = (r, c)
                grid[r].append("#" if p in self.cube_rocks else ("O" if p in self.round_rocks else "."))
        return grid

    def printGrid(self):
        grid = self.toGrid()
        for r in grid:
            print(" ".join(r))
        print("")


def main():
    round_rocks: set[Point] = set()
    cube_rocks: set[Point] = set()
    height = 0
    width = 0
    for r, line in enumerate(fileinput.input()):
        line = line.strip()
        for c, val in enumerate(line):
            if val == ".":
                continue
            elif val == "O":
                round_rocks.add((r, c))
            elif val == "#":
                cube_rocks.add((r, c))
            else:
                assert False
        height = r + 1
        width = len(line)
    del r, line, c, val
    plat = Platform(round_rocks, cube_rocks, height, width)
    del round_rocks, cube_rocks, height

    CYCLES = 1_000_000_000
    hashes: OrderedDict[int, int] = OrderedDict()

    offset = None
    interval = None
    for i in range(CYCLES):
        plat.cycle()
        h = hash(plat)
        # print(h)
        if h in hashes:
            if not offset:
                offset = list(hashes).index(h)
                interval = i - offset

            # print(hashes.values())
            # print(plat.calc_load())
            m = (CYCLES - 1 - offset) % (interval)
            print(list(hashes.values())[m + offset])
            sys.exit()
        else:
            hashes[h] = plat.calc_load()


if __name__ == "__main__":
    main()
