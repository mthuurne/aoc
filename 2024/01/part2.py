import fileinput
from collections import defaultdict


def read_input():
    for line in fileinput.input():
        yield tuple(int(x) for x in line.strip().split())


def solve(data):
    freqs = defaultdict(int)
    for _, x in data:
        freqs[x] += 1
    print(sum(x * freqs[x] for x, _ in data))


if __name__ == "__main__":
    solve(tuple(read_input()))
