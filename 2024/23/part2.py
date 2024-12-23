import fileinput
from collections import defaultdict
from itertools import combinations


def read_input():
    for line in fileinput.input():
        yield line.strip().split("-")


def subsets(sequence):
    for mask in range(1 << len(sequence)):
        yield [
            elem
            for bit, elem in enumerate(sequence)
            if (mask >> bit) & 1
        ]


def solve(connections):
    connected_to = defaultdict(set)
    for c1, c2 in connections:
        connected_to[c1].add(c2)
        connected_to[c2].add(c1)

    def is_complete(graph):
        return all(c2 in connected_to[c1] for c1, c2 in combinations(graph, 2))

    max_complete_graph = None
    target_size = 1
    for cmin in sorted(connected_to):
        # Form subgraphs starting from the minimum node in the subgraph.
        # This avoids retrying the same subgraphs many times for different initial nodes.
        nodes = sorted(c for c in connected_to[cmin] if c > cmin)
        while target_size <= len(nodes):
            for subgraph in combinations(nodes, target_size):
                if is_complete(subgraph):
                    max_complete_graph = (cmin,) + subgraph
                    target_size += 1
                    # Look for an even larger subgraph.
                    break
            else:
                # There won't be a larger subgraph using these nodes, as such a subgraph
                # would include multiple subgraphs of the target size.
                break

    print(",".join(max_complete_graph))


if __name__ == "__main__":
    solve(tuple(read_input()))
