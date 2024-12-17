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


def solve(reg, program):

    def combo(operand):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4 | 5 | 6:
                return reg[operand - 4]
            case _:
                assert False

    output = []
    ip = 0
    while ip < len(program):
        print(f"{reg} {program[:ip]} >{program[ip:ip+2]} {program[ip + 2:]}")
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
                print(f"OUT: {value}")
                output.append(value)
            case Instruction.BDV:
                reg[1] = reg[0] >> combo(operand)
            case Instruction.CDV:
                reg[2] = reg[0] >> combo(operand)
            case _:
                assert False

    print()
    print(",".join(str(value) for value in output))


if __name__ == "__main__":
    solve(*read_input())
