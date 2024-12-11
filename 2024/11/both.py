import fileinput
from functools import cache


def read_input():
    for line in fileinput.input():
        for n in line.strip().split():
            yield int(n)


@cache
def simulate(stone, ticks):
    if ticks == 0:
        return 1
    if stone == 0:
        return simulate(1, ticks - 1)
    digits = 0
    value = stone
    while value > 0:
        value //= 10
        digits += 1
    if digits & 1:
        return simulate(stone * 2024, ticks - 1)
    else:
        stone1, stone2 = divmod(stone, 10 ** (digits >> 1))
        return simulate(stone1, ticks - 1) + simulate(stone2, ticks - 1)


def solve(stones):
    print("after 25 blinks:", sum(simulate(stone, 25) for stone in stones))
    print("after 75 blinks:", sum(simulate(stone, 75) for stone in stones))


if __name__ == "__main__":
    solve(tuple(read_input()))
