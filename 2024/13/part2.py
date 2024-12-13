import fileinput
from math import gcd


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


def extended_euclid(a, b):
    """Return (g, x, y) such that g = gcd(a, b) and a * x + b * y = g."""
    ro, r = a, b
    so, s = 1, 0
    to, t = 0, 1
    while True:
        q, m = divmod(ro, r)
        if m == 0:
            return r, s, t
        ro, r = r, m
        so, s = s, so - q * s
        to, t = t, to - q * t


def solve1d(a, b, n):
    """
    Given positive integers a, b, n, return factors x and y and steps i and j,
    such that a(x - ki) + b(y + kj) = n.
    If no solution exists, None is returned.
    """

    # Remove common dividers shared by a, b and n.
    g = gcd(a, b, n)
    a //= g
    b //= g
    n //= g

    g, x1, y1 = extended_euclid(a, b)
    if g != 1:
        # As a and b have a common divider, every ax + by will have that divider,
        # but n does not have it, so there is no solution.
        return None

    # Since x1 * a + y1 * b = 1, multiply both factors by n to get n as a result.
    return x1 * n, y1 * n, b, a


# def solve(machines, offset=0):
def solve(machines, offset=10000000000000):
    total_cost = 0

    for (ax, ay), (bx, by), (px, py) in machines:
        px += offset
        py += offset
        sx = solve1d(ax, bx, px)
        sy = solve1d(ay, by, py)
        if sx is None or sy is None:
            continue
        nax, nbx, iax, ibx = sx
        nay, nby, iay, iby = sy

        # ax * (nax - r * iax) + bx * (nbx + r * ibx) == px
        # ay * (nay - s * iay) + by * (nby + s * iby) == py
        # na == nax - r * iax == nay - s * iay
        # nb == nbx + r * ibx == nby + s * iby

        na = nax % iax
        nb = (px - ax * na) // bx
        assert ax * na + bx * nb == px
        while nb >= 0:
            s, t = divmod(nay - na, iay)
            if t == 0:
                assert na == nay - s * iay
                if nby + s * iby == nb:
                    break
            na += iax
            nb -= ibx
            assert ax * na + bx * nb == px
        else:
            continue

        assert ax * na + bx * nb == px
        assert ay * na + by * nb == py
        cost = 3 * na + 1 * nb
        total_cost += cost

    print(total_cost)


if __name__ == "__main__":
    solve(tuple(read_input()))
