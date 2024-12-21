import fileinput
from functools import cache
from itertools import pairwise


def read_input():
    for line in fileinput.input():
        yield line.strip()


def horizontal_moves(dx):
    match dx:
        case -2:
            return "<<"
        case -1:
            return "<"
        case 0:
            return ""
        case 1:
            return ">"
        case 2:
            return ">>"
        case _:
            assert False, dx


def vertical_moves(dy):
    match dy:
        case -3:
            return "^^^"
        case -2:
            return "^^"
        case -1:
            return "^"
        case 0:
            return ""
        case 1:
            return "v"
        case 2:
            return "vv"
        case 3:
            return "vvv"
        case _:
            assert False, dy


def map_grid(grid):
    return {
        button: (x, y)
        for y, row in enumerate(grid)
        for x, button in enumerate(row)
    }


grid0 = (
    "789",
    "456",
    "123",
    " 0A",
)
grid1 = (
    " ^A",
    "<v>",
)

grid0_map = map_grid(grid0)
grid1_map = map_grid(grid1)


def iter_moves_button(grid, grid_map, start, end):
    sx, sy = grid_map[start]
    ex, ey = grid_map[end]
    dx = ex - sx
    dy = ey - sy
    hmoves = horizontal_moves(dx)
    vmoves = vertical_moves(dy)
    # Horizontal first.
    if grid[sy][ex] != " ":
        yield f"{hmoves}{vmoves}A"
    # Vertical first.
    if grid[ey][sx] != " " and hmoves and vmoves:
        yield f"{vmoves}{hmoves}A"


@cache
def calc_min_steps(code, level):
    grid = grid0 if level == 0 else grid1
    grid_map = grid0_map if level == 0 else grid1_map
    total_steps = 0
    for start, end in pairwise(f"A{code}"):
        # print(f"  {start} -> {end}")
        min_steps = None
        for moves in iter_moves_button(grid, grid_map, start, end):
            # print(f"    {moves}")
            if level == 25:
                steps = len(moves)
            else:
                steps = calc_min_steps(moves, level + 1)
            min_steps = steps if min_steps is None else min(min_steps, steps)
        total_steps += min_steps
    return total_steps


def solve(codes):
    checksum = 0
    for code in codes:
        steps = calc_min_steps(code, 0)
        print(code, steps)
        checksum += steps * int(code[:-1])
    print(checksum)


if __name__ == "__main__":
    solve(tuple(read_input()))
