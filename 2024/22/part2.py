import fileinput
from itertools import pairwise, product


def read_input():
    for line in fileinput.input():
        yield int(line.strip())


def rng_step(state):
    state ^= state << 6
    state &= (1 << 24) - 1
    state ^= state >> 5
    state ^= state << 11
    state &= (1 << 24) - 1
    return state


def iter_prices(seed):
    state = seed
    yield state % 10
    for _ in range(2000):
        state = rng_step(state)
        yield state % 10


def solve(seeds):
    buyers_prices = [list(iter_prices(seed)) for seed in seeds]
    buyers_bytes = [
        bytes(10 + curr_digit - prev_digit for prev_digit, curr_digit in pairwise(prices))
        for prices in buyers_prices
    ]

    best_bananas = 0
    for pattern in product(range(-9, 10), repeat=4):
        pattern_bytes = bytes(n + 10 for n in pattern)
        bananas = 0
        for prices, delta_bytes in zip(buyers_prices, buyers_bytes, strict=True):
            if (idx := delta_bytes.find(pattern_bytes)) != -1:
                bananas += prices[idx + 4]
        print(pattern, bananas)
        best_bananas = max(best_bananas, bananas)
    print(best_bananas)

if __name__ == "__main__":
    solve(tuple(read_input()))
