import fileinput
import re


def read_input():
    # Be careful: the input contains newlines.
    return "".join(line.strip() for line in fileinput.input())


re_mul = re.compile(r"(mul)\(([0-9]{1,3}),([0-9]{1,3})\)|(do)\(\)|(don't)\(\)")


def solve(data):
    total = 0
    enabled = True
    for found in re_mul.finditer(data):
        match found.groups():
            case ("mul", s1, s2, _, _):
                if enabled:
                    total += int(s1) * int(s2)
            case (_, _, _, "do", _):
                enabled = True
            case (_, _, _, _, "don't"):
                enabled = False
            case _:
                assert False, found
    print(total)


if __name__ == "__main__":
    solve(read_input())
