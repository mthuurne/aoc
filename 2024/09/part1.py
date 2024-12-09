import fileinput


def read_input():
    for line in fileinput.input():
        for idx, ch in enumerate(line.strip()):
            file_id = -1 if idx & 1 else idx // 2
            for _ in range(int(ch)):
                yield file_id


def solve(disk):
    i = 0
    j = len(disk) - 1
    while i < j:
        if disk[i] == -1:
            if disk[j] != -1:
                disk[i] = disk[j]
                disk[j] = -1
                i += 1
            j -= 1
        else:
            i += 1
    print(sum(idx * file_id for idx, file_id in enumerate(disk) if file_id != -1))


if __name__ == "__main__":
    solve(list(read_input()))
