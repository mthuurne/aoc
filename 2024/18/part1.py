import fileinput
from heapq import heappop, heappush
from pathlib import Path


def read_input():
    for line in fileinput.input():
        yield tuple(int(n) for n in line.strip().split(","))


def shortest_path(get_edges, start, start_cost=0):
    """
    Compute the lowest-cost paths from the start node to every other node
    in a graph, using a variation of Dijkstra's algorithm.

    A node can be any hashable type.

    Cost is typically distance, but could be any other value that we want
    to minimize. Typically this is an `int` or `float`, but any type that
    supports `+` and `<` should work.

    The `get_edges` function is called with a node and must return/yield
    a series of edges, where each edge is a pair containing a neighbouring
    node and the cost to travel to that node from the given node. The travel
    cost cannot be negative: when added to a total cost T the result must
    never be smaller than T.

    If your graph is stored in a dictionary that maps nodes to a sequence of
    (successor node, cost) pairs, you can pass `__getitem__` for `get_edge`.

    Returns a dictionary that maps each node N to a pair containing the
    previous node on the shortest path and the total cost to reach N.
    For the start points, the previous node is `None`.
    """

    # Note: id() is used as a tie-breaker on equal costs, since we don't
    #       require nodes to be ordered. If your nodes are ordered though,
    #       you can remove the tie breaker mechanism.
    tie_breaker = id

    new = []
    heappush(new, (start_cost, tie_breaker(start), start, None))
    min_costs = {}

    while new:
        total_cost, _, node, prev = heappop(new)
        if node not in min_costs:
            min_costs[node] = (prev, total_cost)
            # Note: If you only care about reaching one from a small set of
            #       end nodes, you can exit here if an end node is found.
            for succ, cost in get_edges(node):
                if succ not in min_costs:
                    new_cost = total_cost + cost
                    heappush(new, (new_cost, tie_breaker(succ), succ, node))

    return min_costs


def solve(incoming, size):
    width, height, steps = size

    accessible = [[True] * width for _ in range(height)]
    for x, y in incoming[:steps]:
        accessible[y][x] = False

    def neighbours(x, y):
        if x > 0:
            yield x - 1, y
        if y > 0:
            yield x, y - 1
        if x + 1 < width:
            yield x + 1, y
        if y + 1 < height:
            yield x, y + 1

    def get_edges(node):
        for neighbour in neighbours(*node):
            if accessible[neighbour[1]][neighbour[0]]:
                yield neighbour, 1

    min_costs = shortest_path(get_edges, (0, 0))
    print(min_costs[(width - 1, height - 1)][1])


def get_size(path):
    return (7, 7, 12) if path.name == "example.txt" else (71, 71, 1024)

if __name__ == "__main__":
    solve(tuple(read_input()), get_size(Path(fileinput.filename())))
