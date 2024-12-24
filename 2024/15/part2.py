import fileinput


def double_line(line):
    line = line.replace("#", "##")
    line = line.replace("O", "[]")
    line = line.replace(".", "..")
    line = line.replace("@", "@.")
    return line


def read_input():
    lines = fileinput.input()

    warehouse = []
    start = None
    for y, line in enumerate(lines):
        line = list(double_line(line.strip()))
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

    def dump(rx, ry):
        for y, row in enumerate(warehouse):
            line = "".join(row)
            if y == ry:
                # assert line[rx] == "."
                line = line[:rx] + "@" + line[rx + 1:]
            print(line)
        print()

    def can_move(x, y, dx, dy):
        nx, ny = x + dx, y + dy
        match warehouse[ny][nx]:
            case "#":
                return False
            case ".":
                return True
            case "[":
                pass
            case "]":
                nx -= 1
            case _ as unknown:
                assert False, unknown
        assert warehouse[ny][nx:nx + 2] == ["[", "]"]
        return (
            dx == 1 or can_move(nx, ny, dx, dy)
        ) and (
            dx == -1 or can_move(nx + 1, ny, dx, dy)
        )

    def do_move(x, y, dx, dy):
        match warehouse[y][x]:
            case "#":
                assert False
            case ".":
                return
            case "[":
                pass
            case "]":
                x -= 1
            case _ as unknown:
                assert False, unknown
        assert warehouse[y][x:x + 2] == ["[", "]"]
        nx, ny = x + dx, y + dy
        if dx != 1:
            do_move(nx, ny, dx, dy)
        if dx != -1:
            do_move(nx + 1, ny, dx, dy)
        print(f"moving box from ({x}, {y}) to ({nx}, {ny})")
        warehouse[y][x:x + 2] = [".", "."]
        warehouse[ny][nx:nx + 2] = ["[", "]"]

    x, y = start
    for dx, dy in moves:
        dump(x, y)
        print("move:", dx, dy)
        if can_move(x, y, dx, dy):
            print("can move")
            x, y = x + dx, y + dy
            do_move(x, y, dx, dy)
        else:
            print("blocked")
    print("final:")
    dump(x, y)

    checksum = sum(
        100 * y + x
        for y, row in enumerate(warehouse)
        for x, cell in enumerate(row)
        if cell == "["
    )
    print(checksum)


if __name__ == "__main__":
    solve(*read_input())
