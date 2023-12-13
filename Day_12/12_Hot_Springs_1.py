import fileinput
import re

re_broken = re.compile(r"(#+)")


def bit_count(i: int) -> int:
    # Kernighan's method
    count = 0
    while i:
        i &= i - 1
        count += 1
    return count


def main():
    solutions = 0
    for line in fileinput.input():
        springs: str
        springs, groups = line.strip().split(" ")
        groups = list(map(int, groups.split(",")))
        del line

        b_count = sum(map(len, re_broken.findall(springs)))
        unk_count = springs.count("?")
        unk_broken = sum(groups) - b_count
        del b_count

        for perm in (x for x in range(2 ** unk_count) if bit_count(x) == unk_broken):
            p = format(perm, "b").zfill(unk_count)
            p = list(map(lambda x: '#' if x == "1" else ".", p))
            del perm

            s = list(springs)
            p.reverse()  # Reverse so we can pop-left more efficiently
            for i in range(len(springs)):
                if s[i] == "?":
                    s[i] = p.pop()

            s = "".join(s)
            matches = re_broken.findall(s)
            lens = list(map(len, matches))
            if lens == groups:
                solutions += 1
    print(solutions)


if __name__ == "__main__":
    main()
