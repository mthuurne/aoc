import fileinput


def read_input():
    for line in fileinput.input():
        yield line.strip()


def scan_horizontal(width, height):
    for y in range(height):
        yield ((x, y) for x in range(width))


def scan_vertical(width, height):
    for x in range(width):
        yield ((x, y) for y in range(height))


def scan_diag_backslash(width, height):
    for x in range(width):
        yield ((x + d, d) for d in range(min(width - x, height)))
    for y in range(1, height):
        yield ((d, y + d) for d in range(min(width, height - y)))


def scan_diag_slash(width, height):
    for x in range(width):
        yield ((x + d, height - 1 - d) for d in range(min(width - x, height)))
    for y in range(height - 1):
        yield ((d, y - d) for d in range(min(width, y + 1)))


def bidirectional(scanner):
    for scan in scanner:
        coords = list(scan)
        yield iter(coords)
        yield reversed(coords)


def scan_grid(width, height):
    yield from bidirectional(scan_horizontal(width, height))
    yield from bidirectional(scan_vertical(width, height))
    yield from bidirectional(scan_diag_backslash(width, height))
    yield from bidirectional(scan_diag_slash(width, height))


def solve(data):
    height = len(data)
    width = len(data[0])
    count = 0
    # for coords in scan_grid(width, height):
    #     print(" ".join(repr(coord) for coord in coords))
    for coords in scan_grid(width, height):
        line = "".join(data[y][x] for x, y in coords)
        count += line.count("XMAS")
    print(count)


if __name__ == "__main__":
    solve(tuple(read_input()))
