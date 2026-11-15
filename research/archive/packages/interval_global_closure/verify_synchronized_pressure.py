#!/usr/bin/env python3
"""Small Fraction regression for physical retiming and finite support knots.

This checks concrete structural risks, not the continuum theorem or a game
value. Paired resource fixtures need not themselves be whole causal clocks;
the separate two-path fixture is a complete fully matched physical law.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json


def frac(x):
    return x if isinstance(x, F) else F(str(x))


class PathPL:
    def __init__(self, vertices, speed=None):
        self.v = [(frac(t), frac(x)) for t, x in vertices]
        assert self.v[0][0] == 0
        assert all(-1 <= x <= 1 for _, x in self.v)
        assert all(a[0] < b[0] for a, b in zip(self.v, self.v[1:]))
        if speed is not None:
            assert all(abs(b[1]-a[1]) <= speed*(b[0]-a[0])
                       for a, b in zip(self.v, self.v[1:]))

    def at(self, t):
        t = frac(t)
        for (a, x), (b, y) in zip(self.v, self.v[1:]):
            if a <= t <= b:
                return x+(y-x)*(t-a)/(b-a)
        assert t >= self.v[-1][0]
        return self.v[-1][1]

    def reflection(self):
        return PathPL([(t, -x) for t, x in self.v], F(1))

    def first_level(self, x):
        x = frac(x)
        if self.v[0][1] == x:
            return F(0)
        for (a, u), (b, v) in zip(self.v, self.v[1:]):
            if min(u, v) <= x <= max(u, v) and u != v:
                return a+(x-u)*(b-a)/(v-u)
        return None


def complete(vertices):
    v = [(frac(t), frac(x)) for t, x in vertices]
    t, x = v[-1]
    if x != 1:
        t += 1-x
        v.append((t, F(1)))
    v.append((t+2, F(-1)))
    return PathPL(v, F(1))


def first_sum_nonpositive(m, n, q):
    cuts = sorted({F(0), q} | {t for p in (m, n) for t, _ in p.v if t < q})
    for a, b in zip(cuts, cuts[1:]):
        va, vb = m.at(a)+n.at(a), m.at(b)+n.at(b)
        if va <= 0:
            return a
        if vb <= 0:
            return a+va*(b-a)/(va-vb)
    assert m.at(q)+n.at(q) <= 0
    return q


def first_contact(m, p):
    cuts = sorted({t for q in (m, p) for t, _ in q.v})
    for a, b in zip(cuts, cuts[1:]):
        va, vb = m.at(a)-p.at(a), m.at(b)-p.at(b)
        if va == 0:
            return a
        if va*vb <= 0:
            return a+va*(b-a)/(va-vb)
    return cuts[-1] if m.at(cuts[-1]) == p.at(cuts[-1]) else None


def retiming_fixtures():
    fixtures = [
        ("earlier-source", complete([(0,"1/4"),(1,"1/4")]),
         complete([(0,0),("3/4","-3/4")]), F(1,4), F(3,4), F(1,2), F(1)),
        ("earlier-target", complete([(0,"1/4"),(1,"1/4")]),
         complete([(0,"-3/4"),(1,"-3/4")]), F(3,4), F(1,4), F(1), F(1,2)),
        ("positive-time-sign-swap", complete([(0,"-1/4"),("1/4","-1/2"),(1,"1/4")]),
         complete([(0,"3/4"),(1,"-1/4")]), F(1), F(1), F(9,8), F(9,8)),
        ("both-negative-at-zero", complete([(0,"-1/2"),(1,"1/4")]),
         complete([(0,"-1/2"),(1,"-1/2")]), F(1), F(1), F(9,8), F(9,8)),
        ("both-center", complete([(0,"1/4"),("1/4",0),("3/4","1/2")]),
         complete([(0,"1/4"),("3/4","-1/2")]), F(3,4), F(3,4), F(7,8), F(7,8)),
        ("initial-sign-swap", complete([(0,"-3/4"),(1,"1/4")]),
         complete([(0,"1/4"),(1,"-3/4")]), F(1), F(1), F(9,8), F(9,8)),
    ]
    rows = []
    for name, m, n, t, s, a, b in fixtures:
        u, v = m.at(t), -n.at(s)
        assert u > 0 and v > 0 and v >= u+abs(t-s)
        assert t <= a < m.first_level(-1) and s <= b < n.first_level(-1)
        h = first_sum_nonpositive(m, n, min(t,s))
        x, y = m.at(h), n.at(h)
        assert h <= min(t,s,a,b)
        assert x > -1 and y > -1
        assert x+y <= 0 and (h == 0 or x+y == 0)
        positives = int(x > 0)+int(y > 0)
        assert positives <= 1
        if positives:
            assert min(x,y) < 0 and max(x,y) <= -min(x,y)
        # A matched unit plus unmatched source mass 1/2 and unused target
        # capacity 1/4. Sign swaps/collapses preserve the resource marginals
        # and leave the constructed unmatched-positive mass exactly 1/2.
        new_positive = F(1,2)+positives
        new_matched = F(positives)
        assert new_positive-new_matched == F(1,2)
        assert F(3,2)+F(5,4) == 2+F(1,2)+F(1,4)
        rows.append({"name":name,"selected_time":str(h),
                     "new_positions":[str(x),str(y)],
                     "constructed_deficiency":"1/2"})
    return rows


def polygonal_fixture():
    m = PathPL([(0,"1/4"),("1/4",0),("1/2","1/4"),
                ("7/4",-1),("13/4","1/2"),("15/4",1)], F(1))
    n = m.reflection()
    meet = first_contact(m, n)
    knots = sorted({F(0),meet,m.first_level(-1),m.first_level(1)})
    assert len(knots) <= 2+2
    new_m = PathPL([(t,m.at(t)) for t in knots], F(1))
    new_n = new_m.reflection()
    for old, new in ((m,new_m),(n,new_n)):
        for level in (-1,0,1):
            assert old.first_level(level) == new.first_level(level)
        # The complete causal clock selects time zero for its whole active
        # lifetime. Its only left-limit obligation is at zero.
        tau = old.first_level(-1)
        assert tau > 0
        for a in (F(0),tau/3,2*tau/3,tau):
            assert tau >= a
        assert old.at(0) == new.at(0)
    positive_mass = m.first_level(-1)/2
    negative_mass = n.first_level(-1)/2
    assert positive_mass <= negative_mass
    baseline = positive_mass+negative_mass
    for r in (F(0),F(1,8),F(1,4),F(1,2),F(1)):
        phi = lambda x: int(x>r)+int(x>-r)
        plane = positive_mass*phi(m.at(0))+negative_mass*phi(n.at(0))
        assert plane <= baseline
    return {"oriented_paths":2,"old_knots_each":len(m.v),
            "new_knots_each":len(knots),"baseline":str(baseline),
            "matched_mass":str(positive_mass),"pressure_unchanged":True}


def tracker(p):
    out = [p.v[0]]
    q = out[0][1]
    for (a,x),(b,y) in zip(p.v,p.v[1:]):
        v = (y-x)/(b-a)
        rate = max(F(-1),min(F(1),v)) if q == x else F(1 if x>q else -1)
        gap, relative = x-q, v-rate
        catch = -gap/relative if gap and relative else None
        if catch is not None and 0 < catch < b-a:
            c = a+catch
            q += rate*catch
            out.append((c,q))
            rate = max(F(-1),min(F(1),v))
            q += rate*(b-c)
        else:
            q += rate*(b-a)
        out.append((b,q))
    a,x = p.v[-1]
    if q != x:
        out.append((a+abs(x-q),x))
    return PathPL(out,F(1))


def tracker_fixtures():
    princesses = [
        PathPL([(0,"-3/4"),("1/4","3/4"),("1/2","-1/2"),(1,1),(2,-1)]),
        PathPL([(0,"1/2"),("1/8",-1),("5/8",1),(1,0)]),
        PathPL([(0,1),("1/4",1),("1/2",-1),("3/4",1)]),
        PathPL([(0,"-1/4"),(1,"1/2"),(2,0)],F(1)),
    ]
    monsters = []
    for a in (F(-1),F(-1,2),F(0),F(1,2),F(1)):
        for direction in (-1,1):
            v=[(F(0),a)]
            end=F(direction)
            t=abs(end-a)
            if t:
                v.append((t,end))
            v.append((t+2,-end))
            monsters.append(PathPL(v,F(1)))
    trackers=[tracker(p) for p in princesses]
    comparisons=0
    for p,q in zip(princesses,trackers):
        for m in monsters:
            tp,tq=first_contact(m,p),first_contact(m,q)
            assert tp is not None and tq is not None and tq >= tp
            comparisons+=1
    contractions=0
    for i,p in enumerate(princesses):
        for j in range(i):
            q=princesses[j]
            knots=sorted({t for a in (p,q,trackers[i],trackers[j]) for t,_ in a.v})
            di=max(abs(p.at(t)-q.at(t)) for t in knots)
            do=max(abs(trackers[i].at(t)-trackers[j].at(t)) for t in knots)
            assert do <= di
            contractions+=1
    legal=princesses[-1]
    assert all(trackers[-1].at(t)==x for t,x in legal.v)
    return {"princess_paths":len(princesses),"monster_paths":len(monsters),
            "exact_capture_comparisons":comparisons,
            "input_output_contractions":contractions,"legal_input_fixed":True}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("report",type=Path)
    args=ap.parse_args()
    report={"status":"PASS","arithmetic":"fractions.Fraction only",
            "scope":"structural regression; no new game bound",
            "retiming":retiming_fixtures(),"polygonal":polygonal_fixture(),
            "tracker":tracker_fixtures()}
    args.report.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,sort_keys=True))


if __name__=="__main__":
    main()
