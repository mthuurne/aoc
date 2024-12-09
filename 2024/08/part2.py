import fileinput
from collections import defaultdict
from itertools import combinations


def read_input():
    antennas = defaultdict(set)
    height = 0
    width = 0
    for y, line in enumerate(fileinput.input()):
        height += 1
        for x, ch in enumerate(line.strip()):
            width = max(width, x + 1)
            if ch != ".":
                antennas[ch].add((x, y))
    return width, height, antennas


def solve(width, height, antennas):
    antinodes = set()

    def add_antinodes(x, y, dx, dy):
        while 0 <= x < width and 0 <= y < height:
            antinodes.add((x, y))
            x += dx
            y += dy

    for locations in antennas.values():
        for (x1, y1), (x2, y2) in combinations(locations, 2):
            dx = x2 - x1
            dy = y2 - y1
            add_antinodes(x1, y1, -dx, -dy)
            add_antinodes(x2, y2, dx, dy)

    print(len(antinodes))


if __name__ == "__main__":
    solve(*read_input())
