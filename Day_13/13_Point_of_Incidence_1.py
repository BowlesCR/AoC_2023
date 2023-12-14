import fileinput


def main():
    grid: list[list[str]] = []
    total_left = 0
    total_top = 0
    for line in fileinput.input():
        if line.strip() == "":
            left, top = solve(grid)
            print(left, top)
            total_left += left
            total_top += top
            grid = []
            continue
        grid.append(list(line.strip()))
    if grid:
        left, top = solve(grid)
        print(left, top)
        total_left += left
        total_top += top

    print(total_left + 100 * total_top)


def solve(grid: list[list[str]]):
    for r in range(len(grid) - 1):
        if all([pair[0] == pair[1] for pair in zip(grid[r::-1], grid[r + 1 :])]):
            return (0, r + 1)

    for c in range(len(grid[0]) - 1):
        fail = False
        for r in range(len(grid)):
            if any([pair[0] != pair[1] for pair in zip(grid[r][c::-1], grid[r][c + 1 :])]):
                fail = True
                break
        if not fail:
            return (c + 1, 0)

    assert False


if __name__ == "__main__":
    main()
