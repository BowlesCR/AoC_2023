import fileinput
import itertools

type Point = tuple[int, int]

galaxies: set[Point] = set()

emptyRows: set[int] = set()
emptyCols: set[int] | None = None

for r, line in enumerate(fileinput.input()):
    if emptyCols is None:
        emptyCols = set(range(len(line.strip())))

    cols = [c for c in range(len(line)) if line[c] == "#"]
    emptyCols = emptyCols.difference(cols)

    galaxies.update((r, c) for c in cols)

    if not cols:
        emptyRows.add(r)
del cols

for row in sorted(emptyRows, reverse=True):
    newgalaxies: set[Point] = set()
    while galaxies:
        g = galaxies.pop()
        if g[0] > row:
            g = (g[0] + 1, g[1])
        newgalaxies.add(g)
    galaxies = newgalaxies
del row, newgalaxies, g
del emptyRows

for col in sorted(emptyCols, reverse=True):
    newgalaxies: set[Point] = set()
    while galaxies:
        g = galaxies.pop()
        if g[1] > col:
            g = (g[0], g[1] + 1)
        newgalaxies.add(g)
    galaxies = newgalaxies
del col, newgalaxies, g
del emptyCols

total = 0
for pair in itertools.combinations(galaxies, 2):
    mdist = abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
    total += mdist

print(total)
