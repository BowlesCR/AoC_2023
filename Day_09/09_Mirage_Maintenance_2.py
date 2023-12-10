import fileinput

sum_ = 0
for line in fileinput.input():
    hist: list[list[int]] = []
    hist.append(list(map(int, line.split(" ")))[::-1])
    del line
    while any((h != 0 for h in hist[-1])):
        s = []
        for i in range(len(hist[-1]) - 1):
            s.append(hist[-1][i + 1] - hist[-1][i])
        hist.append(s)

    for i in range(len(hist) - 1, -1, -1):
        if i == len(hist) - 1:
            hist[i].append(0)
            continue

        hist[i].append(hist[i][-1] + hist[i + 1][-1])

    sum_ += hist[0][-1]

print(sum_)
