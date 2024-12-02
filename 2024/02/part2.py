import fileinput
from itertools import pairwise


def read_input():
    for line in fileinput.input():
        yield tuple(int(x) for x in line.strip().split())


def is_slow_increase(report):
    return all(1 <= x2 - x1 <= 3 for x1, x2 in pairwise(report))


def is_safe_increase(report):
    return is_slow_increase(report) or any(
        is_slow_increase(report[:idx] + report[idx + 1:]) for idx in range(len(report))
    )


def solve(reports):
    num_safe = sum(
        is_safe_increase(report) or is_safe_increase(tuple(reversed(report)))
        for report in reports
    )
    print(num_safe)


if __name__ == "__main__":
    solve(tuple(read_input()))
