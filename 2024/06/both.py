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

    def simulate(obstacles):
        """Return positions visited, or None if guard loops."""
        x, y = start
        dx, dy = 0, -1
        visited = set()
        while 0 <= x < width and 0 <= y < height:
            guard = (x, y, dx, dy)
            if guard in visited:
                return None
            visited.add(guard)
            nx = x + dx
            ny = y + dy
            if (nx, ny) in obstacles:
                dx, dy = -dy, dx
            else:
                x = nx
                y = ny
        return visited

    visited = {(x, y) for x, y, dx, dy in simulate(obstacles)}
    print(f"part 1: {len(visited)}")

    num_options = sum(
        simulate(obstacles | {new_obstacle}) is None
        for new_obstacle in visited - {start}
    )
    print(f"part 2: {num_options}")



if __name__ == "__main__":
    solve(*read_input())
