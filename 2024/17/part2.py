import fileinput
from enum import IntEnum


def read_input():
    lines = fileinput.input()

    reg = [None] * 3
    for line in lines:
        parts = line.strip().split()
        if not parts:
            break
        keyword, reg_str, value_str = parts
        assert keyword == "Register", parts
        idx = ord(reg_str[0]) - ord("A")
        value = int(value_str)
        reg[idx] = value

    program = []
    for line in lines:
        parts = line.strip().split()
        assert parts[0] == "Program:"
        for instr_str in parts[1].split(","):
            program.append(int(instr_str))

    return reg, program


class Instruction(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


def check(reg, program):

    def combo(operand):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4 | 5 | 6:
                return reg[operand - 4]
            case _:
                assert False

    out_idx = 0
    ip = 0
    while ip < len(program):
        instr = program[ip]
        operand = program[ip + 1]
        ip += 2
        match instr:
            case Instruction.ADV:
                reg[0] >>= combo(operand)
            case Instruction.BXL:
                reg[1] ^= operand
            case Instruction.BST:
                reg[1] = combo(operand) & 7
            case Instruction.JNZ:
                if reg[0] != 0:
                    ip = operand
            case Instruction.BXC:
                reg[1] ^= reg[2]
            case Instruction.OUT:
                value = combo(operand) & 7
                if value == program[out_idx]:
                    out_idx += 1
                else:
                    return False
            case Instruction.BDV:
                reg[1] = reg[0] >> combo(operand)
            case Instruction.CDV:
                reg[2] = reg[0] >> combo(operand)
            case _:
                assert False

    return out_idx == len(program)


def brute_force(reg, program):
    """This is too slow."""
    a_val = 0
    while True:
        if a_val % 1000000 == 0:
            print(a_val)
        reg[0] = a_val
        if check(reg, program):
            return a_val
        a_val += 1


def solve(reg, program):
    """
    My input disassembles into this program:

    do {
        X := A[:3] ^ 5
        output A[X:X + 3] ^ A[:3] ^ 3
        A := A[3:]
    } until A == 0

    Since the output looks forward in the value of A, we work backwards in
    searching for the right value, so we already know higher bits of A.
    """

    def search(idx, a_val):
        if idx == 0:
            yield a_val
        else:
            idx -= 1
            output = program[idx]
            for v_new in range(8):
                a_new = (a_val << 3) | v_new
                if v_new == output ^ 3 ^ ((a_new >> (v_new ^ 5)) & 7):
                    yield from search(idx, a_new)

    solutions = []
    for a_val in search(len(program), 0):
        print(a_val)
        reg[0] = a_val
        assert check(reg, program)
        solutions.append(a_val)
    print()
    print(min(solutions))


if __name__ == "__main__":
    solve(*read_input())
