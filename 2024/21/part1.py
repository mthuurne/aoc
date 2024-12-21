import fileinput


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


def iter_moves(grid, grid_map, start, code):
    if code:
        sx, sy = grid_map[start]
        ex, ey = grid_map[code[0]]
        dx = ex - sx
        dy = ey - sy
        hmoves = horizontal_moves(dx)
        vmoves = vertical_moves(dy)
        # Horizontal first.
        if grid[sy][ex] != " ":
            for moves in iter_moves(grid, grid_map, code[0], code[1:]):
                yield f"{hmoves}{vmoves}A{moves}"
        # Vertical first.
        if grid[ey][sx] != " " and dx != 0 and dy != 0:
            for moves in iter_moves(grid, grid_map, code[0], code[1:]):
                yield f"{vmoves}{hmoves}A{moves}"
    else:
        yield ""


def iter_moves_rec(level, code):
    if level == 0:
        yield from iter_moves(grid0, grid0_map, "A", code)
    else:
        for uplevel_moves in iter_moves_rec(level - 1, code):
            yield from iter_moves(grid1, grid1_map, "A", uplevel_moves)


def calc_min_steps(code):
    min_steps = None
    for moves in iter_moves_rec(2, code):
        print(f"  {moves}")
        min_steps = len(moves) if min_steps is None else min(min_steps, len(moves))
    return min_steps


def solve(codes):
    checksum = 0
    for code in codes:
        steps = calc_min_steps(code)
        print(code, steps)
        checksum += steps * int(code[:-1])
    print(checksum)


if __name__ == "__main__":
    solve(tuple(read_input()))
