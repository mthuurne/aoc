import fileinput


def read_input():
    lines = fileinput.input()

    supply = []
    for line in lines:
        line = line.strip()
        if not line:
            break
        for pattern in line.split(","):
            supply.append(pattern.strip())

    designs = []
    for line in lines:
        designs.append(line.strip())

    return supply, designs


class Node:
    def __init__(self):
        self.leaf = False
        self.children = {}

    def __repr__(self):
        child_repr = ", ".join(
            f"{color}: {node!r}"
            for color, node in self.children.items()
        )
        return f"[{child_repr}]" if self.leaf else f"({child_repr})"

    def add_pattern(self, pattern):
        if pattern:
            color = pattern[0]
            if (child := self.children.get(color)) is None:
                child = Node()
                self.children[color] = child
            child.add_pattern(pattern[1:])
        else:
            self.leaf = True

    def iter_prefix_lengths(self, design):
        if self.leaf:
            yield 0
        if design:
            color = design[0]
            child = self.children.get(color)
            if (child := self.children.get(color)) is not None:
                for length in child.iter_prefix_lengths(design[1:]):
                    yield length + 1


def count_possible(tree, design):
    full = len(design) + 1
    reachable = [0] * full
    reachable[0] = 1
    for idx in range(len(design)):
        if reachable[idx]:
            for length in tree.iter_prefix_lengths(design[idx:]):
                if (end := idx + length) < full:
                    reachable[end] += reachable[idx]
    return reachable[-1]


def solve(supply, designs):
    tree = Node()
    for pattern in supply:
        tree.add_pattern(pattern)

    num_possible = sum(count_possible(tree, design) for design in designs)
    print(num_possible)


if __name__ == "__main__":
    solve(*read_input())
