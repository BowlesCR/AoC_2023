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
        errors = 0
        for pair in zip(grid[r::-1], grid[r + 1 :]):
            if pair[0] == pair[1]:
                continue
            else:
                errors += [p[0] == p[1] for p in zip(pair[0], pair[1])].count(False)
                if errors > 1:
                    break

        if errors == 1:
            return (0, r + 1)

    for c in range(len(grid[0]) - 1):
        errors = 0
        for r in range(len(grid)):
            for pair in zip(grid[r][c::-1], grid[r][c + 1 :]):
                if pair[0] != pair[1]:
                    errors += 1
                    if errors > 1:
                        break
            if errors > 1:
                break
        if errors == 1:
            return (c + 1, 0)

    assert False


if __name__ == "__main__":
    main()
