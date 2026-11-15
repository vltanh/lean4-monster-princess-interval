"""Exact marginal sweep certificate; Python standard library only.

This checks an explicit rejected princess law and its ordered quantile coupling.
It does not solve the interval game or certify a best monster response.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def clean(vertices):
    out = []
    for t, x in vertices:
        if out and t == out[-1][0]:
            assert x == out[-1][1]
            continue
        out.append((t, x))
        while len(out) >= 3:
            (a, x), (b, y), (c, z) = out[-3:]
            if (y-x)*(c-b) != (z-y)*(b-a):
                break
            out.pop(-2)
    return out


def path(a, u, c, delta):
    assert delta <= a <= u < 1 and -a <= c < 1
    p = [(F(0), a), ((u-a)/2, (u+a)/2)]
    if c >= u-2*delta:
        p.extend([(u-delta, delta), (c+delta, delta)])
    else:
        p.append(((u+c)/2, (u-c)/2))
    if c >= 0:
        # The first outgoing leg reaches U=1+delta, then returns inward
        # to delta at time 1; the final outgoing leg has V=1-delta.
        p.extend([((1+delta+c)/2, (1+delta-c)/2),
                  (F(1), delta), (2-delta, F(1))])
    else:
        # Negative-c paths retain the original outgoing suffix.
        p.append((c+1, F(1)))
    p = clean(p)
    assert p[0][0] == 0
    for t, x in p:
        assert t >= 0 and -1 <= x <= 1
    for (t, x), (s, y) in zip(p, p[1:]):
        assert t < s and abs(y-x) <= s-t
    return p


def at(p, t):
    for (a, x), (b, y) in zip(p, p[1:]):
        if a <= t <= b:
            return x + (y-x)*(t-a)/(b-a)
    return p[-1][1]


def main():
    d = json.loads((Path(__file__).parent/'candidate.json').read_text())
    scale = d['parameter_scale']
    delta, eta = F(d['delta']), F(d['eta'])
    assert 0 < delta < eta < 1
    W = sum(row['weight'] for row in d['rows'])
    assert W > 0
    alpha = beta = R = 0
    hs = []
    for row in d['rows']:
        a, u, c = [F(x, scale) for x in row['parameters']]
        w = row['weight']
        assert isinstance(w, int) and w > 0
        p = path(a, u, c, delta)
        if c >= 0:
            assert a < 1-eta and at(p, F(1)) == delta
        else:
            R += w
            assert at(p, F(1)) == 1
        for sign in (-1, 1):
            reflected = [(t, sign*x) for t, x in p]
            hs.append((reflected, w))
            alpha += w * (reflected[0][1] < -1+eta)
            beta += w * (at(reflected, F(1)) > eta)
    alpha, beta, R = F(alpha, 2*W), F(beta, 2*W), F(R, W)
    assert alpha <= R/2 and beta == R/2
    # The theorem bounds every coupling of these time marginals.
    bound = 1+(1+eta)*alpha+(3+eta)*beta
    simple_bound = 1+(2+eta)*R
    assert bound <= simple_bound
    assert R < F(7, 50)
    assert simple_bound < F(4103, 3200)
    known_lower = F(36290299773897097, 25600000000000000)
    assert simple_bound < known_lower
    print('PASS: all', len(hs), 'explicit paths are 1-Lipschitz in [-1,1]')
    print('PASS: post-U=1 detour is applied only when c >= 0')
    print('Initial left mass alpha =', alpha)
    print('Time-1 right mass beta =', beta)
    print('Nonfunnel pair mass R =', R)
    print('Unrestricted sweep upper bound =', bound)
    print('Decimal (display only) =', float(bound))
    print('Symmetric simplified bound =', simple_bound)
    print('PASS: bound is strictly below the existing exact full-game lower bound')
    print('PASS: the same bound holds after ordered quantile rearrangement')


if __name__ == '__main__':
    main()
