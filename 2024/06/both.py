import fileinput


def read_input():
    starts = set()
    obstacles = set()
    for y, line in enumerate(fileinput.input()):
        for x, cell in enumerate(line.strip()):
            match cell:
                case ".":
                    pass
                case "#":
                    obstacles.add((x, y))
                case "^":
                    starts.add((x, y))
                case _:
                    assert False, cell
    start, = starts
    return obstacles, start


def solve(obstacles, start):
    width = max(x + 1 for x, y in obstacles)
    height = max(y + 1 for x, y in obstacles)

    x, y = start
    dx, dy = 0, -1
    visited = set()
    while 0 <= x < width and 0 <= y < height:
        visited.add((x, y))
        nx = x + dx
        ny = y + dy
        if (nx, ny) in obstacles:
            dx, dy = -dy, dx
        else:
            x = nx
            y = ny
    print(f"part 1: {len(visited)}")

    def would_loop(obstacles):
        x, y = start
        dx, dy = 0, -1
        visited = set()
        while 0 <= x < width and 0 <= y < height:
            guard = (x, y, dx, dy)
            if guard in visited:
                return True
            visited.add(guard)
            nx = x + dx
            ny = y + dy
            if (nx, ny) in obstacles:
                dx, dy = -dy, dx
            else:
                x = nx
                y = ny
        return False

    num_options = sum(
        would_loop(obstacles | {new_obstacle})
        for new_obstacle in visited - {start}
    )
    print(f"part 2: {num_options}")



if __name__ == "__main__":
    solve(*read_input())
