import fileinput
from itertools import combinations


def read_input():
    inp = fileinput.input()

    ordering = []
    for line in inp:
        line = line.strip()
        if not line:
            break
        ordering.append(tuple(int(s) for s in line.split("|")))

    books = []
    for line in inp:
        line = line.strip()
        books.append(tuple(int(s) for s in line.split(",")))

    return ordering, books


def successors(graph, start):
    done = set()
    new = {start}
    while new:
        page = new.pop()
        done.add(page)
        for succ in graph.get(page, ()):
            if succ not in done:
                new.add(succ)
    return done


def is_correct(graph, book):
    return all(
        p1 not in successors(graph, p2)
        for p1, p2 in combinations(book, 2)
    )


def filter_graph(full_graph, book):
    present_pages = set(book)
    graph = {}
    for page, successors in full_graph.items():
        if page in present_pages:
            for succ in successors:
                if succ in present_pages:
                    graph.setdefault(page, set()).add(succ)
    return graph


def solve(ordering, books):
    full_graph = {}
    for a, b in ordering:
        full_graph.setdefault(a, set()).add(b)

    print(", ".join(f"{a} <  {b}" for a, b in ordering))
    score = 0
    for book in books:
        graph = filter_graph(full_graph, book)
        print(book)
        if is_correct(graph, book):
            middle = book[len(book) // 2]
            score += middle
            print("right order, middle page is", middle)
        else:
            print("wrong order")
    print(f"{score=}")


if __name__ == "__main__":
    solve(*read_input())
