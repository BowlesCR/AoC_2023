import fileinput
import functools
from collections import deque
from enum import Enum

type Point = tuple[int, int]


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3


class Floor:
    def __init__(self):
        self.grid: list[list[str]] = []
        self.energized: set[Point] = set()
        self.q: deque = deque()

    @functools.cache
    def beam(self, p: Point, direction: Direction) -> None:
        r, c = p
        if r < 0 or r >= len(self.grid) or c < 0 or c >= len(self.grid[0]):
            return

        self.energized.add(p)

        match direction:
            case Direction.NORTH:
                match self.grid[r][c]:
                    case ".":
                        self.q.append(((r - 1, c), direction))
                    case "/":
                        self.q.append(((r, c + 1), Direction.EAST))
                    case "\\":
                        self.q.append(((r, c - 1), Direction.WEST))
                    case "|":
                        self.q.append(((r - 1, c), direction))
                    case "-":
                        self.q.append(((r, c - 1), Direction.WEST))
                        self.q.append(((r, c + 1), Direction.EAST))
                    case _:
                        assert False
            case Direction.SOUTH:
                match self.grid[r][c]:
                    case ".":
                        self.q.append(((r + 1, c), direction))
                    case "/":
                        self.q.append(((r, c - 1), Direction.WEST))
                    case "\\":
                        self.q.append(((r, c + 1), Direction.EAST))
                    case "|":
                        self.q.append(((r + 1, c), direction))
                    case "-":
                        self.q.append(((r, c - 1), Direction.WEST))
                        self.q.append(((r, c + 1), Direction.EAST))
                    case _:
                        assert False
            case Direction.WEST:
                match self.grid[r][c]:
                    case ".":
                        self.q.append(((r, c - 1), direction))
                    case "/":
                        self.q.append(((r + 1, c), Direction.SOUTH))
                    case "\\":
                        self.q.append(((r - 1, c), Direction.NORTH))
                    case "|":
                        self.q.append(((r - 1, c), Direction.NORTH))
                        self.q.append(((r + 1, c), Direction.SOUTH))
                    case "-":
                        self.q.append(((r, c - 1), direction))
                    case _:
                        assert False
            case Direction.EAST:
                match self.grid[r][c]:
                    case ".":
                        self.q.append(((r, c + 1), direction))
                    case "/":
                        self.q.append(((r - 1, c), Direction.NORTH))
                    case "\\":
                        self.q.append(((r + 1, c), Direction.SOUTH))
                    case "|":
                        self.q.append(((r - 1, c), Direction.NORTH))
                        self.q.append(((r + 1, c), Direction.SOUTH))
                    case "-":
                        self.q.append(((r, c + 1), direction))
                    case _:
                        assert False
            case _:
                assert False

    def all_the_beams(self, p: Point, direction: Direction):
        self.q.append((p, direction))

        while self.q:
            b = self.q.pop()
            self.beam(*b)


def main():
    floor = Floor()
    for r, line in enumerate(fileinput.input()):
        floor.grid.append([])
        for val in line.strip():
            floor.grid[r].append(val)

    floor.all_the_beams((0, 0), Direction.EAST)

    print(len(floor.energized))


if __name__ == "__main__":
    main()
