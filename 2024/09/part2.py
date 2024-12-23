import fileinput


def read_input():
    files = []
    gaps = []
    block_idx = 0
    for line in fileinput.input():
        for seq_idx, ch in enumerate(line.strip()):
            num_blocks = int(ch)
            if seq_idx & 1:
                gaps.append((block_idx, num_blocks))
            else:
                files.append((block_idx, num_blocks))
            block_idx += num_blocks
    return files, gaps


def solve(files, gaps):
    disk_size = sum(s for _, s in files) + sum(s for _, s in gaps)

    for file_idx in reversed(range(len(files))):
        from_block, file_size = files[file_idx]
        for gap_idx, (to_block, gap_size) in enumerate(gaps):
            if to_block > from_block:
                break
            if gap_size >= file_size:
                # Update file location.
                files[file_idx] = (to_block, file_size)
                # Update destination gap.
                gaps[gap_idx] = (to_block + file_size, gap_size - file_size)
                # We don't need to update the source gap, as we'll never use it:
                # files are only moved to the left and we're processing files right-to-left.
                break

    # print(files)
    # print(gaps)
    # layout = ["."] * disk_size
    # for file_idx, (block_idx, file_size) in enumerate(files):
    #     for i in range(file_size):
    #         layout[block_idx + i] = str(file_idx)
    # print("".join(layout))

    print(sum(
        sum((block_idx + i) * file_id for i in range(file_size))
        for file_id, (block_idx, file_size) in enumerate(files)
    ))


if __name__ == "__main__":
    solve(*read_input())
