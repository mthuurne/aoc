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
    width = max(x for x, y in obstacles) + 1
    height = max(y for x, y in obstacles) + 1

    def simulate(obstacles):
        """Return positions visited, or None if guard loops."""
        guard = (*start, 0, -1)
        visited = set()
        while guard not in visited:
            visited.add(guard)
            x, y, dx, dy = guard
            nx = x + dx
            ny = y + dy
            if (nx, ny) in obstacles:
                guard = (x, y, -dy, dx)
            elif 0 <= nx < width and 0 <= ny < height:
                guard = (nx, ny, dx, dy)
            else:
                return visited
        return None

    visited = {(x, y) for x, y, dx, dy in simulate(obstacles)}
    print(f"part 1: {len(visited)}")

    num_options = sum(
        simulate(obstacles | {new_obstacle}) is None
        for new_obstacle in visited - {start}
    )
    print(f"part 2: {num_options}")



if __name__ == "__main__":
    solve(*read_input())
