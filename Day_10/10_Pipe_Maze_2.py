import fileinput
import sys
from collections import defaultdict, deque

type Point = tuple[int, int]


class Maze:
    start_pos: Point | None = None

    def __init__(self, grid: list[list[str]]):
        self.grid: list[list[str]] = grid
        self.adj: defaultdict[Point, set[Point]] = defaultdict(set)
        self._calc_adj()
        self.dist: defaultdict[Point, int] = defaultdict(lambda: sys.maxsize)
        self.dist[self.start_pos] = 0

        self._dijk()

    def width(self):
        return len(self.grid[0])

    def height(self):
        return len(self.grid)

    def _calc_adj(self):
        for r in range(len(self.grid)):
            for c in range(len(self.grid[0])):
                self._set_adj(r, c)

        paths: set[tuple[int, int]] = {p for p in self.adj if self.start_pos in self.adj[p]}
        assert len(paths) == 2
        dirs = set()
        for p in paths:
            if p[0] - self.start_pos[0] == -1:
                dirs.add('N')
            elif p[0] - self.start_pos[0] == 1:
                dirs.add('S')
            elif p[1] - self.start_pos[1] == -1:
                dirs.add('W')
            elif p[1] - self.start_pos[1] == 1:
                dirs.add('E')

        if dirs == {'N', 'S'}:
            self.grid[self.start_pos[0]][self.start_pos[1]] = '|'
        elif dirs == {'E', 'W'}:
            self.grid[self.start_pos[0]][self.start_pos[1]] = '-'
        elif dirs == {'N', 'E'}:
            self.grid[self.start_pos[0]][self.start_pos[1]] = 'L'
        elif dirs == {'N', 'W'}:
            self.grid[self.start_pos[0]][self.start_pos[1]] = 'J'
        elif dirs == {'S', 'W'}:
            self.grid[self.start_pos[0]][self.start_pos[1]] = '7'
        elif dirs == {'S', 'E'}:
            self.grid[self.start_pos[0]][self.start_pos[1]] = 'F'
        else:
            assert False

        self._set_adj(*self.start_pos)

    def _set_adj(self, r: int, c: int):
        match self.grid[r][c]:
            case "|":  # North, South
                self._add_adj_north(r, c)
                self._add_adj_south(r, c)
            case "-":  # East, West
                self._add_adj_east(r, c)
                self._add_adj_west(r, c)
            case "L":  # North, East
                self._add_adj_north(r, c)
                self._add_adj_east(r, c)
            case "J":  # North, West
                self._add_adj_north(r, c)
                self._add_adj_west(r, c)
            case "7":  # South, West
                self._add_adj_south(r, c)
                self._add_adj_west(r, c)
            case "F":  # South, East
                self._add_adj_south(r, c)
                self._add_adj_east(r, c)
            case ".":  # No pipe
                pass
            case "S":
                # Starting pos, don't know the shape yet, but note the coords
                self.start_pos = (r, c)

            case _:
                assert False

    def _add_adj_north(self, r, c):
        if self._is_valid_coord(r - 1, c):
            self.adj[(r, c)].add((r - 1, c))
            # self.adj[(r - 1, c)].add((r, c))

    def _add_adj_south(self, r, c):
        if self._is_valid_coord(r + 1, c):
            self.adj[(r, c)].add((r + 1, c))
            # self.adj[(r + 1, c)].add((r, c))

    def _add_adj_east(self, r, c):
        if self._is_valid_coord(r, c + 1):
            self.adj[(r, c)].add((r, c + 1))
            # self.adj[(r, c + 1)].add((r, c))

    def _add_adj_west(self, r, c):
        if self._is_valid_coord(r, c - 1):
            self.adj[(r, c)].add((r, c - 1))
            # self.adj[(r, c - 1)].add((r, c))

    def _is_valid_coord(self, r, c):
        return (0 <= r < self.height()) and (0 <= c <= self.width())

    def _dijk(self):
        # modified dijkstras -- weights are all 1, graph is not fully connected
        candidates: deque[tuple[Point, Point]] = deque([(self.start_pos, a) for a in self.adj[self.start_pos]])
        while candidates:
            c = candidates.popleft()
            d = self.dist[c[0]] + 1
            if d < self.dist[c[1]]:
                self.dist[c[1]] = d
                candidates.extend([(c[1], a) for a in self.adj[c[1]] if a != c[0]])

    def count_inside(self) -> int:
        # https://www.reddit.com/r/adventofcode/comments/18fgddy/2023_day_10_part_2_using_a_rendering_algorithm_to/
        count = 0
        for r in range(self.height()):
            inside = False
            for c in range(self.width()):
                if (r, c) in self.dist:
                    if self.grid[r][c] in "|LJ":
                        inside = not inside
                elif inside:
                    count += 1
        return count


def main():
    grid: list[list[str]] = []

    for line in fileinput.input():
        grid.append(list(line.strip()))
    maze: Maze = Maze(grid)
    del grid

    print(max(*maze.dist.values()))
    print(maze.count_inside())


if __name__ == "__main__":
    main()
