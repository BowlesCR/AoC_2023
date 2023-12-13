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


def distinct_permutations(iterable, r=None):
    # https://more-itertools.readthedocs.io/en/stable/_modules/more_itertools/more.html#distinct_permutations

    def _full(A):
        while True:
            # Yield the permutation we have
            yield tuple(A)

            # Find the largest index i such that A[i] < A[i + 1]
            for i in range(size - 2, -1, -1):
                if A[i] < A[i + 1]:
                    break
            #  If no such index exists, this permutation is the last one
            else:
                return

            # Find the largest index j greater than j such that A[i] < A[j]
            for j in range(size - 1, i, -1):
                if A[i] < A[j]:
                    break

            # Swap the value of A[i] with that of A[j], then reverse the
            # sequence from A[i + 1] to form the new permutation
            A[i], A[j] = A[j], A[i]
            A[i + 1 :] = A[: i - size : -1]  # A[i + 1:][::-1]

    # Algorithm: modified from the above
    def _partial(A, r):
        # Split A into the first r items and the last r items
        head, tail = A[:r], A[r:]
        right_head_indexes = range(r - 1, -1, -1)
        left_tail_indexes = range(len(tail))

        while True:
            # Yield the permutation we have
            yield tuple(head)

            # Starting from the right, find the first index of the head with
            # value smaller than the maximum value of the tail - call it i.
            pivot = tail[-1]
            for i in right_head_indexes:
                if head[i] < pivot:
                    break
                pivot = head[i]
            else:
                return

            # Starting from the left, find the first value of the tail
            # with a value greater than head[i] and swap.
            for j in left_tail_indexes:
                if tail[j] > head[i]:
                    head[i], tail[j] = tail[j], head[i]
                    break
            # If we didn't find one, start from the right and find the first
            # index of the head with a value greater than head[i] and swap.
            else:
                for j in right_head_indexes:
                    if head[j] > head[i]:
                        head[i], head[j] = head[j], head[i]
                        break

            # Reverse head[i + 1:] and swap it with tail[:r - (i + 1)]
            tail += head[: i - r : -1]  # head[i + 1:][::-1]
            i += 1
            head[i:], tail[:] = tail[: r - i], tail[r - i :]

    items = sorted(iterable)

    size = len(items)
    if r is None:
        r = size

    if 0 < r <= size:
        return _full(items) if (r == size) else _partial(items, r)

    return iter(() if r else ((),))

def main():
    solutions = 0
    for line in fileinput.input():
        springs: str
        springs, groups = line.strip().split(" ")
        springs = "?".join([springs]*5)
        groups = list(map(int, groups.split(",")))
        groups *= 5
        del line

        b_count = sum(map(len, re_broken.findall(springs)))
        unk_count = springs.count("?")
        unk_broken = sum(groups) - b_count
        del b_count

        inp = ["#"] * unk_broken + ["."] * (unk_count-unk_broken)

        for p in distinct_permutations(inp, unk_count):
            p = list(p)
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
    print(solutions)

if __name__ == "__main__":
    main()
