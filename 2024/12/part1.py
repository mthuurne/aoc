import fileinput


def read_input():
    for line in fileinput.input():
        yield line.strip()


def solve(garden):
    height = len(garden)
    width = len(garden[0])

    def neighbours(x, y):
        if x > 0:
            yield x - 1, y
        if y > 0:
            yield x, y - 1
        if x + 1 < width:
            yield x + 1, y
        if y + 1 < height:
            yield x, y + 1

    def calc_region(sx, sy):
        plant = garden[sy][sx]
        done_plots = set()
        todo_plots = {(sx, sy)}
        while todo_plots:
            plot = todo_plots.pop()
            done_plots.add(plot)
            for neighbour in neighbours(*plot):
                if neighbour not in done_plots:
                    nx, ny = neighbour
                    if garden[ny][nx] == plant:
                        todo_plots.add(neighbour)
        return plant, done_plots

    def calc_perimeter(region):
        perimeter = 4 * len(region)
        for plot in region:
            for neighbour in neighbours(*plot):
                if neighbour in region:
                    perimeter -= 1
        return perimeter

    done = set()
    total_cost = 0
    for y in range(height):
        for x in range(width):
            plot = (x, y)
            if plot not in done:
                plant, region = calc_region(*plot)
                area = len(region)
                perimeter = calc_perimeter(region)
                cost = area * perimeter
                print(f"{plant}: {area=} x {perimeter=} = {cost=}")
                total_cost += cost
                done |= region
    print(f"{total_cost=}")


if __name__ == "__main__":
    solve(tuple(read_input()))
