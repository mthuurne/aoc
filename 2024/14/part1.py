import fileinput
import re
from math import prod
from pathlib import Path


re_line = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

def read_input():
    for line in fileinput.input():
        m = re_line.match(line.strip())
        assert m is not None, line.strip()
        yield tuple(int(n) for n in m.groups())


def solve(robots, size):
    width, height = size

    steps = 100
    locations = []
    for px, py, vx, vy in robots:
        nx = (px + vx * steps) % width
        ny = (py + vy * steps) % height
        locations.append((nx, ny))

    quadrant_counts = [0] * 4
    mx = width // 2
    my = height // 2
    for nx, ny in locations:
        if nx == mx or ny == my:
            continue
        qx = nx > mx
        qy = ny > my
        quadrant = qy * 2 + qx
        quadrant_counts[quadrant] += 1
    print(quadrant_counts)
    checksum = prod(quadrant_counts)
    print(checksum)


def get_size(path):
    return (11, 7) if path.name == "example.txt" else (101, 103)

if __name__ == "__main__":
    solve(tuple(read_input()), get_size(Path(fileinput.filename())))
