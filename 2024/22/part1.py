import fileinput


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


def solve(seeds):
    checksum = 0
    for seed in seeds:
        state = seed
        for _ in range(2000):
            state = rng_step(state)
        print(seed, state)
        checksum += state
    print(checksum)


if __name__ == "__main__":
    solve(tuple(read_input()))
