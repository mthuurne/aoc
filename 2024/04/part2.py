import fileinput


def read_input():
    for line in fileinput.input():
        yield line.strip()


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
    yield from bidirectional(scan_diag_backslash(width, height))
    yield from bidirectional(scan_diag_slash(width, height))


def find_centers(data, scanner):
    centers = set()
    for scan in scanner:
        coords = list(scan)
        line = "".join(data[y][x] for x, y in coords)
        start = 0
        while (idx := line.find("MAS", start)) != -1:
            centers.add(coords[idx + 1])
            start = idx + 3
    return centers


def solve(data):
    height = len(data)
    width = len(data[0])
    backslash_centers = find_centers(data, bidirectional(scan_diag_backslash(width, height)))
    slash_centers = find_centers(data, bidirectional(scan_diag_slash(width, height)))
    centers = backslash_centers & slash_centers
    # print(centers)
    print(len(centers))


if __name__ == "__main__":
    solve(tuple(read_input()))
