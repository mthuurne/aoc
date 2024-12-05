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
        freqs = {page: 0 for page in book}
        for p1, p2 in rules:
            if p1 in freqs and p2 in freqs:
                freqs[p2] += 1
        correct = tuple(sorted(freqs, key=freqs.__getitem__))
        print(book)
        print(correct)
        middle = correct[len(book) // 2]
        if book == correct:
            print("right order, middle page is", middle)
            score1 += middle
        else:
            print("wrong order, middle page should be", middle)
            score2 += middle
        print()
    print(f"{score1=}")
    print(f"{score2=}")


if __name__ == "__main__":
    solve(*read_input())
