"""Exact physical capture + independent causal-record integral for two sweeps.

Tests a solved infinite-path Monster-restricted game, not the full value.
All arithmetic is Fraction; no floats or numerical quadrature.
"""
from fractions import Fraction as Q
from itertools import product

ZERO = Q(0)
ONE = Q(1)
TWO = Q(2)
THREE = Q(3)


def sweep(t, direction):
    return t - ONE if direction == +1 else ONE - t


def interpolation(a, x, b, y, t):
    return x + (y-x)*(t-a)/(b-a)


def hit(path, direction):
    """Chronological first physical equality against a speed-one sweep."""
    for (a, x), (b, y) in zip(path, path[1:]):
        da, db = sweep(a, direction)-x, sweep(b, direction)-y
        if da == 0:
            return a
        if (da < 0 <= db) or (da > 0 >= db):
            return a + (b-a)*(-da)/(db-da)
    raise AssertionError('Endpoint sweep must cross every legal path by t=2')


def selector_score(path):
    """Independent exact integral of the causal strict/closed CDF plane.

    The two active sweep selectors yield
      (1/2) int_0^2 (1 + 1[p(t)<1-t] - 1[p(t)<=t-1]) dt.
    Each affine segment is split at all sweep contacts. The midpoint
    sign on each resulting open cell is exact (including coincidences).
    """
    total = ZERO
    for (a, x), (b, y) in zip(path, path[1:]):
        cuts = {a, b}
        for direction in (+1, -1):
            da, db = sweep(a, direction)-x, sweep(b, direction)-y
            if da != db:
                root = a + (b-a)*(-da)/(db-da)
                if a < root < b:
                    cuts.add(root)
        ordered = sorted(cuts)
        for left, right in zip(ordered, ordered[1:]):
            mid = (left + right)/2
            p = interpolation(a, x, b, y, mid)
            survival_sum = (1 + int(p < sweep(mid, -1))
                              - int(p <= sweep(mid, +1)))
            assert 0 <= survival_sum <= 2
            total += (right-left)*survival_sum/2
    return total


def check(path):
    assert path[0][0] == 0 and path[-1][0] == 2
    assert all(-1 <= x <= 1 for _, x in path)
    assert all(b > a and abs(y-x) <= b-a
               for (a, x), (b, y) in zip(path, path[1:]))
    right, left = hit(path, +1), hit(path, -1)
    assert right + left < 3, (path, right, left)
    expected = (right + left)/2
    assert selector_score(path) == expected, path
    return right, left, expected


count = 0
best = ZERO
for xs in product([Q(v,4) for v in range(-4,5)], repeat=3):
    path = [(ZERO,xs[0]), (ONE,xs[1]), (TWO,xs[2])]
    if abs(xs[1]-xs[0]) <= 1 and abs(xs[2]-xs[1]) <= 1:
        _, _, score = check(path)
        best = max(best, score)
        count += 1
assert count == 429

for n in range(1,30):
    epsilon = Q(1, 2**n)
    path = [(ZERO,-ONE+epsilon), (TWO-epsilon,ONE), (TWO,ONE)]
    reflected = [(t,-x) for t,x in path]
    right, left, score = check(path)
    rright, rleft, rscore = check(reflected)
    assert right == rleft == 2
    assert left == rright == 1-epsilon/2
    assert score == rscore == Q(3,2)-epsilon/4
    assert (right+rright)/2 == (left+rleft)/2 == score

print(f'PASS: {count} polygonal legal paths and 29 epsilon/reflection families;'
      f' physical hits match independent strict/closed selector integrals;'
      f' grid max {best}, restricted game supremum 3/2 unattained')


def value_at(path, t):
    for (a, x), (b, y) in zip(path, path[1:]):
        if a <= t <= b:
            return interpolation(a,x,b,y,t)
    assert t >= path[-1][0]
    return path[-1][1]


def physical_capture(monster, target):
    """Independent chronological polygonal contact via merged time vertices."""
    horizon = max(monster[-1][0], target[-1][0])
    knots = sorted({ZERO, horizon} |
                   {t for t,_ in monster if t<=horizon} |
                   {t for t,_ in target if t<=horizon})
    for a,b in zip(knots,knots[1:]):
        da = value_at(monster,a)-value_at(target,a)
        db = value_at(monster,b)-value_at(target,b)
        if da == 0:
            return a
        if da*db < 0 or db==0:
            return a+(b-a)*(-da)/(db-da)
    raise AssertionError('Completed monster did not capture target')


positions = [Q(v,2) for v in range(-2,3)]
steps = [Q(v,2) for v in range(5)]
monsters = 0
for xs in product(positions, repeat=len(steps)):
    if any(abs(y-x)>Q(1,2) for x,y in zip(xs,xs[1:])):
        continue
    m = list(zip(steps,xs))
    # A legal completed endpoint tour after the arbitrary prefix.
    endpoint = ONE if xs[-1]>=0 else -ONE
    t1 = TWO+abs(endpoint-xs[-1])
    m += [(t1,endpoint),(t1+TWO,-endpoint),(Q(6),-endpoint)]
    for n in (1,2,3,4):
        eps=Q(1,2**n)
        a=ONE-eps
        p=[(ZERO,-a),(TWO-eps,ONE),(Q(6),ONE)]
        pref=[(t,-x) for t,x in p]
        first=physical_capture(m,p)
        second=physical_capture(m,pref)
        assert (first+second)/2 >= a/2, (m,eps,first,second)
    monsters+=1

for n in range(1,15):
    eps=Q(1,2**n)
    a=ONE-eps
    p=[(ZERO,-a),(TWO-eps,ONE),(Q(6),ONE)]
    pref=[(t,-x) for t,x in p]
    m=[(ZERO,-a),(a,ZERO),(a+ONE,ONE),(a+THREE,-ONE),(Q(6),-ONE)]
    assert physical_capture(m,p)==0
    assert physical_capture(m,pref)==a

print(f'PASS: {monsters} arbitrary completed Monster prefixes x 4 eps;'
      f' physical two-runner response >= (1-eps)/2;'
      f' 14 explicit attaining Monster responses')


# Exact archived 338-path versus the two endpoint sweeps. Execute this
# when running from a full repository checkout with the original JSON.
if __name__ == '__main__':
    import json
    from pathlib import Path
    source=(Path(__file__).resolve().parents[1]/
            'interval_uniform_reduction'/'princess_strategy.json')
    if source.exists():
        data=json.loads(source.read_text())
        S=Q(data['S'])
        b=ZERO
        for nums,weight in zip(data['paths_h'],data['weights_h']):
            path=[(Q(t)/S,Q(x)/S) for t,x in nums]
            i=next(i for i,(t,x) in enumerate(path) if t>=TWO)
            if path[i][0]>TWO:
                t1,x1=path[i-1]
                t2,x2=path[i]
                p2=interpolation(t1,x1,t2,x2,TWO)
                path=path[:i]+[(TWO,p2)]
            else:
                path=path[:i+1]
            r,l,_=check(path)
            b+=Q(weight,data['weight_total'])*(r+l)/2
        assert b == Q(18145150023847037,12800000000000000),b
        L=Q(36290299773897097,25600000000000000)
        assert b-L==Q(273796977,25600000000000000)
        print(f'PASS: archived {len(data["paths_h"])} weighted paths, exact symmetric sweep cross {b}')
