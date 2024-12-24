import fileinput
import operator


def read_input():
    lines = fileinput.input()

    initial = {}
    for line in lines:
        line = line.strip()
        if not line:
            break
        label, value_str = line.split(":")
        value = int(value_str)
        initial[label] = value
        assert label[0] != "z"

    rules = {}
    for line in lines:
        label1, oper_str, label2, arrow, label3 = line.strip().split()
        assert arrow == "->"
        oper = {
            "AND": operator.__and__,
            "OR": operator.__or__,
            "XOR": operator.__xor__,
        }[oper_str]
        assert label3 not in rules
        rules[label3] = (label1, label2, oper)

    return initial, rules


def solve(initial, rules):
    print(initial)
    print(rules)

    known = dict(initial)
    missing = {label for label in rules if label[0] == "z"}
    while missing:
        for label3, (label1, label2, oper) in rules.items():
            if label3 not in known and label1 in known and label2 in known:
                known[label3] = oper(known[label1], known[label2])
                missing.discard(label3)

    result = 0
    for label, value in known.items():
        if label[0] == "z":
            bit = int(label[1:])
            result |= value << bit
    print(result)


if __name__ == "__main__":
    solve(*read_input())
