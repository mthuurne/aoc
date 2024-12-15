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


def solve(machines, offset=10000000000000):
    total_cost = 0

    for (ax, ay), (bx, by), (px, py) in machines:
        px += offset
        py += offset

        if by * ax == bx * ay:
            # The vectors are parallel.
            # We have to push the button that is cheapest per distance travelled
            # as many times as possible without overshooting the target and then
            # the other button zero or more times to reach the target.
            # However, this case does not occur in our input and therefore
            # we do not handle it.
            assert False

        nb = (py * ax - ay * px) // (by * ax - bx * ay)
        na = (px - bx * nb) // ax
        if na < 0 or nb < 0:
            # Both vectors point below or above the target, so we cannot reach it.
            # This doesn't occur in our input either, but is trivial to handle.
            continue
        if ax * na + bx * nb == px and ay * na + by * nb == py:
            # A single integer solution exists.
            total_cost += 3 * na + nb

    print(total_cost)


if __name__ == "__main__":
    solve(tuple(read_input()))
