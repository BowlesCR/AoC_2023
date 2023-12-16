import copy
from collections import deque
import fileinput
import functools
import sys
from enum import Enum

type Point = tuple[int, int]


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3


class Floor:
    def __init__(self, grid: list[list[str]]):
        self.grid: list[list[str]] = grid
        self.energized: set[Point] = set()
        self.q: deque = deque()

    @functools.cache
    def beam(self, p: Point, dir: Direction) -> None:
        r, c = p
        if r < 0 or r >= len(self.grid) or c < 0 or c >= len(self.grid[0]):
            return

        self.energized.add(p)

        match dir:
            case Direction.NORTH:
                match self.grid[r][c]:
                    case ".":
                        self.q.append(((r - 1, c), dir))
                    case "/":
                        self.q.append(((r, c + 1), Direction.EAST))
                    case "\\":
                        self.q.append(((r, c - 1), Direction.WEST))
                    case "|":
                        self.q.append(((r - 1, c), dir))
                    case "-":
                        self.q.append(((r, c - 1), Direction.WEST))
                        self.q.append(((r, c + 1), Direction.EAST))
                    case _:
                        assert False
            case Direction.SOUTH:
                match self.grid[r][c]:
                    case ".":
                        self.q.append(((r + 1, c), dir))
                    case "/":
                        self.q.append(((r, c - 1), Direction.WEST))
                    case "\\":
                        self.q.append(((r, c + 1), Direction.EAST))
                    case "|":
                        self.q.append(((r + 1, c), dir))
                    case "-":
                        self.q.append(((r, c - 1), Direction.WEST))
                        self.q.append(((r, c + 1), Direction.EAST))
                    case _:
                        assert False
            case Direction.WEST:
                match self.grid[r][c]:
                    case ".":
                        self.q.append(((r, c - 1), dir))
                    case "/":
                        self.q.append(((r + 1, c), Direction.SOUTH))
                    case "\\":
                        self.q.append(((r - 1, c), Direction.NORTH))
                    case "|":
                        self.q.append(((r - 1, c), Direction.NORTH))
                        self.q.append(((r + 1, c), Direction.SOUTH))
                    case "-":
                        self.q.append(((r, c - 1), dir))
                    case _:
                        assert False
            case Direction.EAST:
                match self.grid[r][c]:
                    case ".":
                        self.q.append(((r, c + 1), dir))
                    case "/":
                        self.q.append(((r - 1, c), Direction.NORTH))
                    case "\\":
                        self.q.append(((r + 1, c), Direction.SOUTH))
                    case "|":
                        self.q.append(((r - 1, c), Direction.NORTH))
                        self.q.append(((r + 1, c), Direction.SOUTH))
                    case "-":
                        self.q.append(((r, c + 1), dir))
                    case _:
                        assert False
            case _:
                assert False

    def all_the_beams(self, p: Point, dir: Direction):
        self.q.append((p, dir))

        while self.q:
            b = self.q.pop()
            self.beam(*b)

    def count_energized(self):
        return len(self.energized)


def main():
    grid: list[list[str]] = []
    for r, line in enumerate(fileinput.input()):
        grid.append([])
        for val in line.strip():
            grid[r].append(val)

    m = 0

    for r in range(len(grid)):
        floor = Floor(grid)
        floor.all_the_beams((r, 0), Direction.EAST)
        m = max(m, floor.count_energized())

        floor = Floor(grid)
        floor.all_the_beams((r, len(grid[0]) - 1), Direction.WEST)
        m = max(m, floor.count_energized())

    for c in range(len(grid[0])):
        floor = Floor(grid)
        floor.all_the_beams((0, c), Direction.SOUTH)
        m = max(m, floor.count_energized())

        floor = Floor(grid)
        floor.all_the_beams((len(grid) - 1, c), Direction.NORTH)
        m = max(m, floor.count_energized())

    print(m)


if __name__ == "__main__":
    main()
