import fileinput


def read_input():
    inp = fileinput.input()

    rules = []
    for line in inp:
        line = line.strip()
        if not line:
            break
        rules.append(tuple(int(s) for s in line.split("|")))

    books = []
    for line in inp:
        line = line.strip()
        books.append(tuple(int(s) for s in line.split(",")))

    return rules, books


def solve(rules, books):
    score1 = 0
    score2 = 0
    for book in books:
        # Use the fact that the input compares every page combination.
        # The number of times each page occurs in the right hand side of
        # a comparison rule is equal to its position in the correct order.
        freqs = {page: 0 for page in book}
        for p1, p2 in rules:
            if p1 in freqs and p2 in freqs:
                freqs[p2] += 1
        middle, = (p for p, c in freqs.items() if c == len(book) // 2)
        if all(p == book[c] for p, c in freqs.items()):
            print("right order, middle page is", middle)
            score1 += middle
        else:
            print("wrong order, middle page should be", middle)
            score2 += middle
    print(f"{score1=}")
    print(f"{score2=}")


if __name__ == "__main__":
    solve(*read_input())
