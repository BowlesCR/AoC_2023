import fileinput
import sys
from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue
from typing import TypeAlias

Point: TypeAlias = tuple[int, int]


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3

    def __lt__(self, other):
        return self.value < other.value


@dataclass(order=True)
class PrioritizedItem:
    cost: int
    pos: Point = field(compare=False)
    dir: Direction = field(compare=False)
    straight_count: int = field(compare=False)

    def fields(self):
        return self.cost, self.pos, self.dir, self.straight_count


class Map:
    def __init__(self, grid: list[list[int]]):
        self.grid: list[list[int]] = grid
        self.target: Point = (len(grid) - 1, len(grid[0]) - 1)
        self.q: PriorityQueue = PriorityQueue()
        self.mincost: int = sys.maxsize

        self.seen: set[tuple[Point, dir]] = set()

    def cost(self, cost: int, pos: Point, dir: Direction, straight_count: int):
        if (pos, dir) in self.seen:
            return
        else:
            self.seen.add((pos, dir))

        if cost > self.mincost:
            return

        if pos == self.target:
            self.mincost = min(self.mincost, cost)
            print(f"Mincost: {self.mincost}")
            return

        r, c = pos
        if r < 0 or r >= len(self.grid) or c < 0 or c >= len(self.grid[0]):
            return

        cost += self.grid[r][c]

        match dir:
            case Direction.NORTH:
                if straight_count < 3:
                    self.q.put(PrioritizedItem(cost, (r - 1, c), Direction.NORTH, straight_count + 1))
                self.q.put(PrioritizedItem(cost, (r, c - 1), Direction.WEST, 1))
                self.q.put(PrioritizedItem(cost, (r, c + 1), Direction.EAST, 1))

            case Direction.SOUTH:
                if straight_count < 3:
                    self.q.put(PrioritizedItem(cost, (r + 1, c), Direction.SOUTH, straight_count + 1))
                self.q.put(PrioritizedItem(cost, (r, c - 1), Direction.WEST, 1))
                self.q.put(PrioritizedItem(cost, (r, c + 1), Direction.EAST, 1))

            case Direction.WEST:
                self.q.put(PrioritizedItem(cost, (r - 1, c), Direction.NORTH, 1))
                self.q.put(PrioritizedItem(cost, (r + 1, c), Direction.SOUTH, 1))
                if straight_count < 3:
                    self.q.put(PrioritizedItem(cost, (r, c - 1), Direction.WEST, straight_count + 1))

            case Direction.EAST:
                self.q.put(PrioritizedItem(cost, (r - 1, c), Direction.NORTH, 1))
                self.q.put(PrioritizedItem(cost, (r + 1, c), Direction.SOUTH, 1))
                if straight_count < 3:
                    self.q.put(PrioritizedItem(cost, (r, c + 1), Direction.EAST, straight_count + 1))

    def go(self):
        while self.q.not_empty:
            n = self.q.get()
            self.cost(*n.fields())


def main():
    grid: list[list[int]] = []
    for line in fileinput.input():
        grid.append(list(map(int, line.strip())))

    m = Map(grid)
    m.q.put(PrioritizedItem(-grid[0][0], (0, 0), Direction.SOUTH, 0))
    m.go()
    print(m.mincost)


if __name__ == "__main__":
    main()
