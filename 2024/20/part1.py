import fileinput


def read_input():
    for line in fileinput.input():
        yield line.strip()


def solve(track):
    start = None
    end = None
    for y, row in enumerate(track):
        if (x := row.find("S")) != -1:
            start = (x, y)
        elif (x := row.find("E")) != -1:
            end = (x, y)
    assert start is not None
    assert end is not None

    height = len(track)
    width = len(track[0])

    def neighbours(x, y):
        if x > 0:
            yield x - 1, y
        if y > 0:
            yield x, y - 1
        if x + 1 < width:
            yield x + 1, y
        if y + 1 < height:
            yield x, y + 1

    def cheat_dest(x, y):
        done = {(x, y)}
        for step1 in neighbours(x, y):
            for step2 in neighbours(*step1):
                if step2 not in done:
                    done.add(step2)
                    yield step2

    def iter_race_pos():
        pos = start
        prev = None
        while True:
            yield pos
            if pos == end:
                break
            for nx, ny in neighbours(*pos):
                if track[ny][nx] != "#" and (nx, ny) != prev:
                    prev = pos
                    pos = (nx, ny)
                    break
            else:
                assert False

    race = [[None] * width for _ in range(height)]
    for t, (x, y) in enumerate(iter_race_pos()):
        race[y][x] = t

    num_big_cheats = 0
    for t, (x, y) in enumerate(iter_race_pos()):
        for cx, cy in cheat_dest(x, y):
            ct = race[cy][cx]
            if ct is None:
                continue
            saved = ct - t - 2
            if saved >= 100:
                print(f"({x}, {y}) => ({cx}, {cy}): {saved}")
                num_big_cheats += 1
    print(num_big_cheats)


if __name__ == "__main__":
    solve(tuple(read_input()))
