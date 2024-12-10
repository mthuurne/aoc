import fileinput


def read_input():
    for line in fileinput.input():
        yield tuple(int(x) for x in line.strip())


def solve(grid):
    height = len(grid)
    width = len(grid[0])

    def neighbours(x, y):
        if x > 0:
            yield x - 1, y
        if y > 0:
            yield x, y - 1
        if x + 1 < width:
            yield x + 1, y
        if y + 1 < height:
            yield x, y + 1

    score = [[0] * width for _ in range(height)]

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 9:
                score[y][x] = 1

    for elevation in range(8, -1, -1):
        print(f"{elevation=}")
        for row in score:
            print("".join(f"{v:3}" for v in row))

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == elevation:
                    score[y][x] = sum(
                        score[ny][nx]
                        for nx, ny in neighbours(x, y)
                        if grid[ny][nx] == elevation + 1
                    )

    total = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 0:
                head_score = score[y][x]
                total += head_score
                # print(head_score)
    print(f"{total=}")


if __name__ == "__main__":
    solve(tuple(read_input()))
