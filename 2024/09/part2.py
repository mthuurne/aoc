import fileinput
from bisect import bisect
from operator import itemgetter


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
                # Update source gap.
                new_gap_idx = bisect(gaps, from_block, key=itemgetter(0))
                gaps.insert(new_gap_idx, (from_block, file_size))
                if new_gap_idx != 0:
                    prev_gap_block, prev_gap_size = gaps[new_gap_idx - 1]
                    if prev_gap_block + prev_gap_size == from_block:
                        # Merge with preceding gap.
                        gaps[new_gap_idx - 1] = (prev_gap_block, prev_gap_size + file_size)
                        del gaps[new_gap_idx]
                        new_gap_idx -= 1
                if new_gap_idx + 1 < len(gaps):
                    next_gap_block, next_gap_size = gaps[new_gap_idx + 1]
                    if next_gap_block == from_block + file_size:
                        # Merge with following gap.
                        gaps[new_gap_idx] = (
                            gaps[new_gap_idx][0], gaps[new_gap_idx][1] + next_gap_size
                        )
                        del gaps[new_gap_idx + 1]
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
