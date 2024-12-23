import fileinput
from collections import defaultdict


def read_input():
    for line in fileinput.input():
        yield line.strip().split("-")


def solve(connections):
    print(connections)

    connected_to = defaultdict(set)
    for c1, c2 in connections:
        connected_to[c1].add(c2)
        connected_to[c2].add(c1)

    triples = set()
    for c1, c2 in connections:
        for c3 in connected_to[c1] & connected_to[c2]:
            if c3 not in (c1, c2):
                triples.add(tuple(sorted((c1, c2, c3))))

    count = sum(
        c1[0] == "t" or c2[0] == "t" or c3[0] == "t"
        for c1, c2, c3 in triples
    )
    print(count)


if __name__ == "__main__":
    solve(tuple(read_input()))
