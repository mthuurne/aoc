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
    score = 0
    for book in books:
        # Use the fact that the input compares every page combination.
        freqs = {page: 0 for page in book}
        for p1, p2 in rules:
            if p1 in freqs and p2 in freqs:
                freqs[p1] += 1
        correct = tuple(sorted(freqs, key=freqs.__getitem__, reverse=True))
        print(book)
        print(correct)
        if book == correct:
            middle = book[len(book) // 2]
            score += middle
            print("right order, middle page is", middle)
        else:
            print("wrong order")
    print(f"{score=}")


if __name__ == "__main__":
    solve(*read_input())
