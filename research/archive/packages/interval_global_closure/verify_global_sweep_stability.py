"""Exact Fraction regression for unrestricted sweep-completion stability.

Analytic theorem applies to ALL speed-one Lipschitz Monster trajectories
completing both endpoints. These finite fixtures check the identities
independently, but do not mechanically prove the continuum theorem.
"""
from fractions import Fraction as Q

z = Q(0)
half = Q(1, 2)
one = Q(1)
two = Q(2)
six = Q(6)
grid = [-one, -half, z, half, one]
N = 8
Eps = [Q(1, 32), Q(1, 16), Q(1, 8), Q(1, 7),
       Q(1, 4), Q(1, 2), Q(3, 4)]


def pieceval(path, t):
    if t >= path[-1][0]:
        return path[-1][1]
    for (a, x), (b, y) in zip(path, path[1:]):
        if a <= t <= b:
            return x + (y - x) * (t - a) / (b - a)
    raise ValueError(("missing", t, path))


def hit(monster, princess):
    """Exact chronological first equality, including vertex contacts."""
    knots = sorted({a for a, _ in monster} |
                   {a for a, _ in princess})
    for t, u in zip(knots, knots[1:]):
        a = pieceval(monster, t) - pieceval(princess, t)
        b = pieceval(monster, u) - pieceval(princess, u)
        if a == 0:
            return t
        if a * b < 0 or b == 0:
            return t + (u - t) * (-a) / (b - a)
    if pieceval(monster, knots[-1]) == pieceval(princess, knots[-1]):
        return knots[-1]
    raise ValueError(("no hit", monster, princess))


def positions(prefix):
    return [(half * i, x) for i, x in enumerate(prefix)]


def endpoint_data(path):
    visits = [(t, x) for t, x in path if abs(x) == one]
    if not visits:
        return None
    sigma, first = visits[0]
    others = [(t, x) for t, x in visits if x == -first]
    if not others:
        return None
    tau = others[0][0]
    if tau <= sigma:
        return None
    return sigma, tau, first


def check(path):
    info = endpoint_data(path)
    if info is None:
        return 0
    sigma, tau, first = info
    complete = [(t, x) for t, x in path if t <= tau]
    complete.append((six, -first))
    sweep = [(z, first), (two, -first), (six, -first)]
    delay = tau - two
    assert sigma >= 0 and delay >= sigma
    for t in sorted({t for t, _ in complete} |
                    {t for t, _ in sweep}):
        assert abs(pieceval(complete, t) - pieceval(sweep, t)) <= delay, (
            path, t, delay
        )
    direction = -first
    backward = z
    idle = z
    for (a, x), (b, y) in zip(complete, complete[1:]):
        if b <= sigma or a >= tau:
            continue
        u, v = max(a, sigma), min(b, tau)
        dx = direction * (pieceval(complete, v) -
                          pieceval(complete, u))
        backward += max(z, -dx)
        idle += (v - u) - abs(dx)
    energy = (sigma + tau - two) / 2
    assert tau - sigma == two + 2 * backward + idle
    assert energy == sigma + backward + idle / 2
    for eps in Eps:
        p = [(z, -one + eps), (two - eps, one), (six, one)]
        reflected = [(t, -x) for t, x in p]
        first_hit, second_hit = hit(complete, p), hit(complete, reflected)
        score = (first_hit + second_hit) / 2
        assert score >= (one - eps) / 2, (path, eps, score, "floor")
        assert score >= Q(3, 2) - eps / 4 - (
            one / eps + Q(1, 4)
        ) * delay, (path, eps, score, "global")
        if delay < eps:
            assert score >= Q(3, 2) - eps / 4 - Q(3, 4) * delay, (
                path, eps, score, "near-sweep"
            )
    return 1


count = 0


def walk(xs, remaining):
    global count
    if remaining == 0:
        count += check(positions(xs))
        return
    x = xs[-1]
    for y in [x - half, x, x + half]:
        if -one <= y <= one:
            walk(xs + [y], remaining - 1)


for start in grid:
    walk([start], N)

assert count == 1050, count
print("PASS:", count, "complete rational Monster trajectories,",
      len(Eps), "runner offsets; all exact physical/energy inequalities")


# Independent symbolic-Fraction integration of the continuum Princess
# offset response FLOOR. Finite epsilon samples are not treated as
# exhaustive for the continuum theorem.
def uniform_response_floor(A, delta):
    if delta >= A:
        return Q(1, 2) - A / 4
    # Integral of 1/2-e/2 over [0,delta], then of
    # 3/2-e/4-3delta/4 over [delta,A].
    low = delta / 2 - delta * delta / 4
    high = (Q(3, 2) * (A - delta)
            - (A * A - delta * delta) / 8
            - Q(3, 4) * delta * (A - delta))
    return (low + high) / A


def uniform_closed_form(A, delta):
    if delta >= A:
        return Q(1, 2) - A / 4
    return (Q(3, 2) - A / 8
            - (1 / A + Q(3, 4)) * delta
            + 5 * delta * delta / (8 * A))


for A in [Q(1, 8), Q(1, 4), Q(4, 15), Q(1, 3),
          Q(1, 2), Q(3, 4)]:
    for delay in [z, Q(1, 1000), Q(9, 1000),
                  A / 2, A, 2 * A, Q(3, 2)]:
        assert uniform_response_floor(A, delay) == uniform_closed_form(A, delay)
        assert uniform_closed_form(A, delay) >= (
            Q(3, 2) - A / 8 - (1 / A + Q(3, 4)) * delay
        )

Ubest = Q(57045188913812444387410009,
          40000000000000000000000000)
A = Q(4, 15)
delay = Q(181, 20000)
assert (uniform_closed_form(A, delay) - Ubest
        == Q(468336687666837769973,
             120000000000000000000000000) > 0)
print("PASS: continuum-offset exact integrals, convex lower envelope,",
      "and mean-delay >181/20000 certificate")
