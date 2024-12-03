import fileinput
import re


def read_input():
    # Be careful: the input contains newlines.
    return "".join(line.strip() for line in fileinput.input())


re_mul = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")


def solve(data):
    total = 0
    for found in re_mul.finditer(data):
        x1, x2 = (int(x) for x in found.groups())
        total += x1 * x2
    print(total)


if __name__ == "__main__":
    solve(read_input())
