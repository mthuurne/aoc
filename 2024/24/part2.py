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
        # As all our operations are symmetrical, we can order labels alphabetically.
        if label1 > label2:
            label1, label2 = label2, label1
        rules[label3] = (label1, label2, oper)

    return initial, rules


class SwapError(Exception):
    "Raised when swapped outputs are detected."


def attempt_solve(rules, num_bits):

    def find_rule(find1, find2, find_op):
        if find1 > find2:
            find1, find2 = find2, find1
        # print(f"find {find1} {find_op.__name__} {find2}")
        for label3, (label1, label2, oper) in rules.items():
            if oper is find_op:
                if label1 == find1 and label2 == find2:
                    return label3
        else:
            raise KeyError

    input_xors = [None] * num_bits
    input_ands = [None] * num_bits
    for label3, (label1, label2, oper) in rules.items():
        if label1[0] == "x" and label2[0] == "y":
            bit1 = int(label1[1:])
            bit2 = int(label2[1:])
            assert bit1 == bit2
            if oper is operator.__xor__:
                assert input_xors[bit1] is None
                input_xors[bit1] = label3
            elif oper is operator.__and__:
                assert input_ands[bit1] is None
                input_ands[bit1] = label3
    for label in input_xors:
        assert label is not None
    for label in input_ands:
        assert label is not None

    carry = None
    for bit, (input_xor, input_and) in enumerate(zip(input_xors, input_ands, strict=True)):
        print(f"{bit:02} - {input_xor=} {input_and=} {carry=}")
        label3 = f"z{bit:02}"
        label1, label2, oper = rules[label3]
        if oper is not operator.__xor__:
            print(f"     operator for {label3} is {oper.__name__}")
            output = find_rule(carry, input_xor, operator.__xor__)
            print(f"     swapping with {output}")
            raise SwapError(label3, output)
        if bit == 0:
            carry = find_rule("x00", "y00", operator.__and__)
        else:
            assert input_xor != carry
            expected = {input_xor, carry}
            actual = {label1, label2}
            if expected != actual:
                print(f"     expected operants {expected}, got {actual}")
                found = expected & actual
                assert found
                diff = expected.symmetric_difference(actual)
                print(f"     swapping {diff}")
                raise SwapError(*diff)
            forwarded_carry = find_rule(input_xor, carry, operator.__and__)
            carry = find_rule(forwarded_carry, input_and, operator.__or__)

def solve(initial, rules):
    num_x = sum(label[0] == "x" for label in initial)
    num_y = sum(label[0] == "y" for label in initial)
    assert num_x == num_y
    num_bits = num_x
    print(f"adding two {num_bits}-bit numbers")

    swapped = []
    def swap(label1, label2):
        swapped.append(label1)
        swapped.append(label2)
        rules[label1], rules[label2] = rules[label2], rules[label1]

    while True:
        try:
            attempt_solve(rules, num_bits)
        except SwapError as err:
            swap(*err.args)
        else:
            break

    print()
    print(",".join(sorted(swapped)))
    assert len(swapped) == 8


if __name__ == "__main__":
    solve(*read_input())
