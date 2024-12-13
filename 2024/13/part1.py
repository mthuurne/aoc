import fileinput


def read_input():
    buf = []
    for line in fileinput.input():
        line = line.strip()
        if not line:
            assert not buf
            continue
        _, spec = line.split(":")
        buf.append(tuple(s.strip() for s in spec.split(",")))
        if len(buf) == 3:
            a, b, p = buf
            buf.clear()
            assert a[0].startswith("X+")
            assert a[1].startswith("Y+")
            a_offset = (int(a[0][2:]), int(a[1][2:]))
            assert b[0].startswith("X+")
            assert b[1].startswith("Y+")
            b_offset = (int(b[0][2:]), int(b[1][2:]))
            assert p[0].startswith("X=")
            assert p[1].startswith("Y=")
            prize = (int(p[0][2:]), int(p[1][2:]))
            yield a_offset, b_offset, prize


def solve(machines):
    total_cost = 0
    for ao, bo, prize in machines:
        min_cost = None
        for na in range(min(prize[0] // ao[0], prize[1] // ao[1]) + 1):
            x = na * ao[0]
            y = na * ao[1]
            dy = prize[0] - y
            nbx = (prize[0] - x) // bo[0]
            nby = (prize[1] - y) // bo[1]
            if nbx == nby and (x + bo[0] * nbx, y + bo[1] * nby) == prize:
                cost = 3 * na + 1 * nbx
                min_cost = cost if min_cost is None else min(min_cost, cost)
        print(ao, bo, prize, min_cost)
        if min_cost is not None:
            total_cost += min_cost
    print(total_cost)


if __name__ == "__main__":
    solve(tuple(read_input()))
