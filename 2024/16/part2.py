import fileinput
from heapq import heappop, heappush


def read_input():
    for line in fileinput.input():
        yield line.strip()


def shortest_path(get_edges, start, start_cost=0):
    # Modified to return multiple preceding nodes.
    # Modified to put total cost first in output pairs.

    # Note: id() is used as a tie-breaker on equal costs, since we don't
    #       require nodes to be ordered. If your nodes are ordered though,
    #       you can remove the tie breaker mechanism.
    tie_breaker = id

    new = []
    heappush(new, (start_cost, tie_breaker(start), start, None))
    min_costs = {}

    while new:
        total_cost, _, node, prev = heappop(new)

        if (min_cost := min_costs.get(node)) is not None:
            if min_cost[0] == total_cost:
                min_cost[1].add(prev)
            else:
                continue
        else:
            min_costs[node] = (total_cost, {prev})

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
    min_cost = min(min_costs[end + (d,)][0] for d in range(4))

    visited = set()
    def visit(node):
        if node not in visited:
            visited.add(node)
            for prev_node in min_costs[node][1]:
                if prev_node is not None:
                    visit(prev_node)

    for d in range(4):
        end_node = end + (d,)
        if min_costs[end_node][0] == min_cost:
            visit(end_node)

    print(len({(x, y) for x, y, d in visited}))


if __name__ == "__main__":
    solve(tuple(read_input()))
