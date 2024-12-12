import fileinput
from collections import defaultdict


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

    def count_sides(region, borders):
        sides = 0
        i = 0
        num_borders = len(borders)
        while i < num_borders:
            sides += 1
            inside = borders[i] in region
            a, b = borders[i]
            b += 1
            i += 1
            while i < num_borders and borders[i] == (a, b) and (borders[i] in region) == inside:
                b += 1
                i += 1
        # print(sides, borders)
        return sides

    def calc_sides(region):
        hborder_freqs = defaultdict(int)
        vborder_freqs = defaultdict(int)
        for x, y in region:
            hborder_freqs[(x, y)] += 1
            hborder_freqs[(x, y + 1)] += 1
            vborder_freqs[(x, y)] += 1
            vborder_freqs[(x + 1, y)] += 1
        hborders = sorted((y, x) for (x, y), freq in hborder_freqs.items() if freq == 1)
        vborders = sorted(plot for plot, freq in vborder_freqs.items() if freq == 1)
        return count_sides({(y, x) for x, y in region}, hborders) + count_sides(region, vborders)

    done = set()
    total_cost = 0
    for y in range(height):
        for x in range(width):
            plot = (x, y)
            if plot not in done:
                plant, region = calc_region(*plot)
                area = len(region)
                sides = calc_sides(region)
                cost = area * sides
                print(f"{plant}: {area=} x {sides=} = {cost=}")
                total_cost += cost
                done |= region
    print(f"{total_cost=}")


if __name__ == "__main__":
    solve(tuple(read_input()))
