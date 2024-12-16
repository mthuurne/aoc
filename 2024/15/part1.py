import fileinput


def read_input():
    lines = fileinput.input()

    warehouse = []
    start = None
    for y, line in enumerate(lines):
        line = list(line.strip())
        if not line:
            break
        try:
            x = line.index("@")
        except ValueError:
            pass
        else:
            assert start is None
            start = (x, y)
            line[x] = "."
        warehouse.append(line)
    assert start is not None

    deltas = {
        "^": (0, -1),
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0),
    }
    moves = []
    for line in lines:
        for instr in line.strip():
            moves.append(deltas[instr])

    return warehouse, start, moves


def solve(warehouse, start, moves):
    x, y = start
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        ex, ey = nx, ny
        while warehouse[ey][ex] == "O":
            ex += dx
            ey += dy
        if warehouse[ey][ex] == ".":
            # Move robot.
            x, y = nx, ny
            # Move boxes.
            if warehouse[ny][nx] == "O":
                warehouse[ny][nx] = "."
                warehouse[ey][ex] = "O"
        else:
            # Move is blocked by a wall.
            assert warehouse[ey][ex] == "#"

    checksum = sum(
        100 * y + x
        for y, row in enumerate(warehouse)
        for x, cell in enumerate(row)
        if cell == "O"
    )
    print(checksum)


if __name__ == "__main__":
    solve(*read_input())
