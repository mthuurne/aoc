import fileinput
from heapq import heappop, heappush


def read_input():
    for line in fileinput.input():
        yield line.strip()


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

def solve(maze):
    # Find start and end point.
    start = None
    end = None
    for y, row in enumerate(maze):
        if (sx := row.find("S")) != -1:
            assert start is None
            start = (sx, y)
        if (ex := row.find("E")) != -1:
            assert end is None
            end = (ex, y)
    assert start is not None
    assert end is not None

    deltas = ((0, -1), (1, 0), (0, 1), (-1, 0))

    def get_edges(node):
        x, y, d = node
        # Turn.
        yield (x, y, (d + 1) % 4), 1000
        yield (x, y, (d - 1) % 4), 1000
        # Move.
        dx, dy = deltas[d]
        x += dx
        y += dy
        if maze[y][x] != "#":
            yield (x, y, d), 1

    # Start trip facing east.
    start_node = start + (1,)
    min_costs = shortest_path(get_edges, start_node)
    min_cost = min(min_costs[end + (d,)][1] for d in range(4))
    print(min_cost)


if __name__ == "__main__":
    solve(tuple(read_input()))
