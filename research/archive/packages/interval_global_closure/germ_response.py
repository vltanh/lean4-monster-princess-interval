#!/usr/bin/env python3
"""Exact unrestricted responses to finite rational epsilon path families.

Arithmetic is in QQ(epsilon), ordered at epsilon=0+. Every comparison records
an explicit positive rational radius on which its answer is valid. The finite
ordered capture-order theorem then makes a completed search an all-monster
response theorem on that common radius, not merely a fixed-epsilon test.

The input mixture weights are reconstructed rationally from a discovery JSON;
this module does not claim that those weights solve its discovery LP exactly.
"""
from __future__ import annotations

import argparse
from bisect import bisect_left, bisect_right
from collections import defaultdict
from fractions import Fraction as Q
from functools import total_ordering
import json
from pathlib import Path as FilePath
import sys
import time

from sympy.polys.domains import QQ
from sympy.polys.fields import field

FIELD, EPS = field('eps', QQ)
RADIUS = Q(1, 4)
COMPARISONS = 0
MAX_DEGREE = 0


def _fraction(value):
    return Q(int(value.numerator), int(value.denominator))


def _poly_sign(poly):
    """Leading sign and an elementary, conservative root-free radius."""
    global RADIUS, MAX_DEGREE
    terms = poly.to_dict()
    if not terms:
        return 0
    degrees = sorted(terms)
    MAX_DEGREE = max(MAX_DEGREE, degrees[-1][0])
    lead = _fraction(terms[degrees[0]])
    remainder = sum(abs(_fraction(terms[k])) for k in degrees[1:])
    if remainder:
        RADIUS = min(RADIUS, abs(lead)/(2*remainder), Q(1))
    return 1 if lead > 0 else -1


@total_ordering
class Germ:
    __slots__ = ('value',)

    def __init__(self, value=0):
        self.value = value.value if isinstance(value, Germ) else FIELD(value)

    def __add__(self, other):
        return Germ(self.value + Germ(other).value)

    __radd__ = __add__

    def __neg__(self):
        return Germ(-self.value)

    def __sub__(self, other):
        return self + -Germ(other)

    def __rsub__(self, other):
        return Germ(other) + -self

    def __mul__(self, other):
        return Germ(self.value * Germ(other).value)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Germ(other)
        if not other.value:
            raise ZeroDivisionError
        # A division is only interpreted on a nonzero denominator interval.
        _poly_sign(other.value.numer)
        _poly_sign(other.value.denom)
        return Germ(self.value / other.value)

    def __rtruediv__(self, other):
        return Germ(other) / self

    def __pow__(self, exponent):
        assert isinstance(exponent, int) and exponent >= 0
        return Germ(self.value ** exponent)

    def __eq__(self, other):
        global COMPARISONS
        COMPARISONS += 1
        difference = self.value-Germ(other).value
        if not difference:
            return True
        # A nonidentity equality can change at a positive root. Equality-only
        # branches (initial ties, coincident captures, simplification) need
        # the same radius protection as strict inequalities.
        _poly_sign(difference.numer)
        _poly_sign(difference.denom)
        return False

    def __lt__(self, other):
        global COMPARISONS
        COMPARISONS += 1
        difference = self.value - Germ(other).value
        return _poly_sign(difference.numer) * _poly_sign(difference.denom) < 0

    def __hash__(self):
        return hash(self.value)

    def __abs__(self):
        return -self if self < 0 else self

    def __repr__(self):
        return str(self.value)

    def evaluate(self, epsilon):
        epsilon = Q(epsilon)
        def val(poly):
            return sum(_fraction(c) * epsilon**power[0]
                       for power, c in poly.to_dict().items())
        return val(self.value.numer) / val(self.value.denom)

    def limit(self):
        numerator, denominator = self.value.numer.to_dict(), self.value.denom.to_dict()
        if not numerator:
            return Q(0)
        ni, di = min(numerator)[0], min(denominator)[0]
        if ni < di:
            raise ValueError('Infinite germ limit')
        if ni > di:
            return Q(0)
        return _fraction(numerator[(ni,)]) / _fraction(denominator[(di,)])

    def data(self):
        def encode(poly):
            return {str(k[0]): str(_fraction(v)) for k, v in sorted(poly.to_dict().items())}
        return {'numerator': encode(self.value.numer), 'denominator': encode(self.value.denom)}


E = Germ(EPS)


class Path:
    def __init__(self, vertices, weight=Q(1)):
        vertices = [(Germ(t), Germ(x)) for t, x in vertices]
        assert vertices and vertices[0][0] == 0
        simplified = []
        for t, x in vertices:
            assert t >= 0 and -1 <= x <= 1
            if simplified and t == simplified[-1][0]:
                assert x == simplified[-1][1]
                continue
            if simplified:
                assert t > simplified[-1][0]
                assert abs(x - simplified[-1][1]) <= t - simplified[-1][0]
            simplified.append((t, x))
            while len(simplified) >= 3:
                (a, u), (b, v), (c, w) = simplified[-3:]
                if (v-u)*(c-b) == (w-v)*(b-a):
                    simplified.pop(-2)
                else:
                    break
        self.t = [t for t, x in simplified]
        self.x = [x for t, x in simplified]
        self.slopes = [(v-u)/(b-a) for (a,u),(b,v) in zip(simplified,simplified[1:])]
        self.seq = ([t+x for t,x in simplified], [t-x for t,x in simplified])
        self.weight = Q(weight)
        assert self.weight > 0

    @property
    def vertices(self):
        return list(zip(self.t, self.x))

    def at(self, t):
        t = Germ(t)
        k = bisect_right(self.t, t) - 1
        assert k >= 0
        return self.x[k] if k+1 == len(self.t) else self.x[k]+self.slopes[k]*(t-self.t[k])

    def hit(self, t, x, direction):
        q = t-direction*x
        sequence = self.seq[(direction+1)//2]
        k = bisect_left(sequence, q)
        if k == len(sequence):
            result = self.t[-1]+q-sequence[-1]
        elif k == 0:
            result = t
        else:
            denominator = 1-direction*self.slopes[k-1]
            assert denominator > 0
            result = self.t[k-1]+(q-sequence[k-1])/denominator
        assert result >= t
        assert self.at(result) == x+direction*(result-t)
        return result

    def reflected(self):
        return Path([(t,-x) for t,x in self.vertices], self.weight)


def realize(query_v, event_labels, indices):
    """Symbolic counterpart of SurvivalCut.realize with its strict shrink."""
    vv = [Germ(Q(v)) for v in query_v]
    labels = [(Q(q), int(side)) for q, side in event_labels]
    values = [Germ(labels[k][0])+labels[k][1]*E for k in indices]
    points = [(Germ(0), Germ(-1))]
    def add(u, v):
        u, v = Germ(u), Germ(v)
        if (u,v) == points[-1]:
            return
        assert u >= points[-1][0] and v >= points[-1][1]
        assert 0 <= u-v <= 2
        points.append((u,v))
    for j in range(1,len(vv)):
        v, previous, target = vv[j], values[j-1], values[j]
        delta = min(E**2, (v-vv[j-1])/3)
        before = v-delta
        add(previous,min(before,previous))
        if before > previous:
            add(before,before)
        add(min(target,before+2),before)
        if target > before+2:
            add(target,target-2)
        add(target,v)
    path = []
    for (u0,v0),(u1,v1) in zip(points,points[1:]):
        t0,t1 = (u0+v0)/2,(u1+v1)/2
        if t1 < 0:
            continue
        x0,x1 = (u0-v0)/2,(u1-v1)/2
        if not path:
            assert t0 <= 0
            path.append((Germ(0),x0+(x1-x0)*(-t0)/(t1-t0)))
        if t1 > path[-1][0]:
            path.append((t1,x1))
    eta = E**6
    return Path([(t,(1-2*eta)*x+eta) for t,x in path])


def validate_order(paths):
    for p,q in zip(paths,paths[1:]):
        for t in sorted(set(p.t+q.t)):
            assert p.at(t) <= q.at(t), ('Crossing paths',t,p.at(t),q.at(t))


def solve(paths, node_limit=1000000, use_pruning=True, symmetry=False):
    """Complete ordered capture-order minimization with exact germ pruning."""
    validate_order(paths)
    n = len(paths)
    total = sum(p.weight for p in paths)
    assert total == 1
    zero, left = Germ(0), Germ(-1)
    best = sum((p.weight*p.hit(zero,left,1) for p in paths), Germ(0))
    best_route = [(zero,left),(Germ(2),Germ(1))]
    current = []
    memo = defaultdict(list)
    stats = dict(nodes=0, leaves=0, dominated=0, bounded=0)
    if symmetry:
        for p,q in zip(paths,paths[::-1]):
            assert p.weight == q.weight
            assert all(p.at(t) == -q.at(t) for t in sorted(set(p.t+q.t)))
    def walk(l,r,anchor,t,x,cost):
        nonlocal best,best_route
        stats['nodes'] += 1
        if stats['nodes'] > node_limit:
            raise RuntimeError('Node limit reached; no completed all-monster certificate')
        while l > 0 and paths[l-1].at(t) == x:
            l -= 1
            cost += paths[l].weight*t
        while r+1 < n and paths[r+1].at(t) == x:
            r += 1
            cost += paths[r].weight*t
        if l == 0 and r == n-1:
            stats['leaves'] += 1
            if cost < best:
                best,best_route = cost,list(current)
            return
        if use_pruning:
            key = l,r,anchor
            previous = memo[key]
            if any(a <= t and c <= cost for a,c in previous):
                stats['dominated'] += 1
                return
            memo[key] = [(a,c) for a,c in previous if not(t <= a and cost <= c)]+[(t,cost)]
            lower = cost
            lower += sum((paths[j].weight*paths[j].hit(t,x,-1) for j in range(l)),Germ(0))
            lower += sum((paths[j].weight*paths[j].hit(t,x,1) for j in range(r+1,n)),Germ(0))
            if lower >= best:
                stats['bounded'] += 1
                return
        choices = []
        if l > 0:
            choices.append((paths[l-1].hit(t,x,-1),l-1,-1))
        if r+1 < n:
            choices.append((paths[r+1].hit(t,x,1),r+1,1))
        choices.sort(key=lambda z:(z[0],-z[2]))
        for nt,j,direction in choices:
            nx = x+direction*(nt-t)
            current.append((nt,nx))
            walk(min(l,j),max(r,j),j,nt,nx,cost+paths[j].weight*nt)
            current.pop()
    for i,p in enumerate(paths):
        if i and p.x[0] == paths[i-1].x[0]:
            continue
        if symmetry and p.x[0] < 0:
            continue
        current[:] = [(zero,p.x[0])]
        walk(i,i,i,zero,p.x[0],Germ(0))
    return best,best_route,stats


def direct_capture(monster, princess):
    """Separate segment intersection check, without generalized inverses."""
    monster = Path(monster)
    times = sorted(set(monster.t+princess.t))
    previous = None
    for t in times:
        difference = monster.at(t)-princess.at(t)
        if difference == 0:
            return t
        if previous:
            a,old = previous
            if (old < 0) != (difference < 0):
                return a+(t-a)*old/(old-difference)
        previous = t,difference
    raise ValueError('No capture')


def load_discovery(data, denominator=10**8):
    exact = 'princess_components' in data
    components = data['princess_components'] if exact else data['princess_mixture']
    weights = [Q(str(row['weight'])) if exact else
               Q(str(row['weight'])).limit_denominator(denominator)
               for row in components]
    total = sum(weights)
    if exact:
        assert total == 1
    positives = []
    for row,weight in zip(components,weights):
        path = realize(data['query_v'],data['event_labels'],row['labels'])
        path.weight = weight/(2*total)
        positives.append(path)
    # Threshold decomposition orders its query graphs from high to low.
    # That induces the same temporal ordering of the physical paths.
    positives.reverse()
    validate_order(positives)
    return [p.reflected() for p in positives[::-1]]+positives,weights,total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--output')
    parser.add_argument('--node-limit',type=int,default=1000000)
    parser.add_argument('--weight-denominator',type=int,default=10**8)
    parser.add_argument('--rightmost-left-attack',action='store_true',
                        help='Check only the straight-left attack from the rightmost initial path; no minimization claim.')
    args = parser.parse_args()
    started = time.time()
    data = json.loads(FilePath(args.input).read_text())
    paths,weights,total = load_discovery(data,args.weight_denominator)
    print('GERM MODEL',dict(paths=len(paths),vertices=sum(len(p.t) for p in paths),
                            radius=str(RADIUS)),flush=True)
    if args.rightmost_left_attack:
        initial=paths[-1].x[0]
        route=[(Germ(0),initial),(1+initial,Germ(-1))]
        value=sum((p.weight*p.hit(Germ(0),initial,-1)for p in paths),Germ(0))
        stats=None
    else:
        value,route,stats = solve(paths,args.node_limit,symmetry=True)
    direct = sum((p.weight*direct_capture(route,p) for p in paths),Germ(0))
    assert direct == value
    limit = value.limit()
    scope=('Exact specified straight-left attack on this supplied rational epsilon family; '
           'not an exhaustive response calculation or a game bound.' if args.rightmost_left_attack else
           'Exact all-monster response for this supplied rational epsilon family; '
           'not a full-game equilibrium certificate.')
    out = dict(scope=scope,
               input=str(FilePath(args.input).name),value=value.data(),limit=str(limit),
               limit_decimal=float(limit),valid_epsilon_radius=str(RADIUS),
               weights_before_normalization=list(map(str,weights)),weight_sum=str(total),
               route=[dict(time=t.data(),position=x.data()) for t,x in route],
               stats=stats,comparisons=COMPARISONS,max_polynomial_degree=MAX_DEGREE,
               seconds=time.time()-started)
    target = FilePath(args.output) if args.output else FilePath(args.input).with_suffix('.germ.json')
    target.write_text(json.dumps(out,indent=2)+'\n')
    print('GERM RESULT',dict(limit=str(limit),decimal=float(limit),radius=str(RADIUS),
                             stats=stats,seconds=time.time()-started),flush=True)
    print('OUTPUT',target,flush=True)


if __name__ == '__main__':
    main()
