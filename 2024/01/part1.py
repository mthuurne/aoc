import fileinput


def read_input():
    for line in fileinput.input():
        yield tuple(int(x) for x in line.strip().split())


def solve(data):
    l1 = sorted(x1 for x1, x2 in data)
    l2 = sorted(x2 for x1, x2 in data)
    print(sum(abs(x1 - x2) for x1, x2 in zip(l1, l2, strict=True)))


if __name__ == "__main__":
    solve(tuple(read_input()))
