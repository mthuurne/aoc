import fileinput


def read_input():
    for line in fileinput.input():
        target_str, *value_strs = line.split()
        assert target_str.endswith(":")
        target = int(target_str[:-1])
        values = tuple(int(s) for s in value_strs)
        yield target, values


def can_match(target, values):
    num_values = len(values)

    def rec(idx, total):
        if idx == num_values:
            return total == target
        if total > target:
            # Our operators can only increase the total, so we can't match from here.
            return False
        value = values[idx]
        return rec(idx + 1, total * value) or rec(idx + 1, total + value)

    return rec(1, values[0])


def solve(equations):
    total = sum(target for target, values in equations if can_match(target, values))
    print(total)


if __name__ == "__main__":
    solve(tuple(read_input()))
