import fileinput


def read_input():
    for line in fileinput.input():
        yield line.strip()


def solve(data):
    print(data)


if __name__ == "__main__":
    solve(tuple(read_input()))
