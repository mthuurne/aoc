import fileinput
import re


re_line = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

def read_input():
    for line in fileinput.input():
        m = re_line.match(line.strip())
        assert m is not None, line.strip()
        yield tuple(int(n) for n in m.groups())


def solve(robots):
    width, height = 101, 103

    # Generate all iterations as ASCII art.
    # To find the relevant one, you don't manually scan them all.
    # There is a horizontal convergence every 'width' steps and a vertical
    # convergence every 'height' steps.
    # The step contained in both convergence sequences is the solution.
    # For my input:
    #      set(72 + 101 * i for i in range(103))
    #    & set(134 + 103 * i for i in range(101))
    #   == {7344}
    for steps in range(width * height):
        grid = [[0] * width for _ in range(height)]
        for px, py, vx, vy in robots:
            nx = (px + vx * steps) % width
            ny = (py + vy * steps) % height
            grid[ny][nx] += 1

        print(f"{steps=}")
        for row in grid:
            print("".join("*" if c else "." for c in row))


if __name__ == "__main__":
    solve(tuple(read_input()))
