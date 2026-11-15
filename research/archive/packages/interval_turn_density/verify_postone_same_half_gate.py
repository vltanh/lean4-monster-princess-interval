#!/usr/bin/env python3
"""Exact capture audit of the post-U1 CDF gate and finite-loop merge."""
from collections import Counter
from fractions import Fraction as Q

from verify_positive_cdf_sheet import Law, Path, first_capture
from verify_curved_terminal_sources import inward_cost
from verify_repeated_same_half import cost


def single_route(a, v, s):
    return [(Q(0), a), ((a+v)/2, (a-v)/2),
            ((s+v)/2, (s-v)/2), (s+1, Q(-1)), (s+3, Q(1))]


def multi_route(a, v, turns):
    route = [(Q(0), a), ((a+v)/2, (a-v)/2),
             ((1+v)/2, (1-v)/2)]
    old_s = Q(1)
    for new_v, new_s in turns:
        assert v <= new_v < old_s <= new_s <= 2+new_v
        route.extend([((old_s+new_v)/2, (old_s-new_v)/2),
                      ((new_s+new_v)/2, (new_s-new_v)/2)])
        v, old_s = new_v, new_s
    return route+[(old_s+1, Q(-1)), (old_s+3, Q(1))]


def laws():
    low = Path([(0,Q(7,10)),(Q(7,10),0),(Q(9,10),0),
                (Q(19,10),1),(6,1)])
    curved = Path([(0,Q(7,10)),(Q(3,10),Q(1,2)),
                   (Q(3,5),Q(1,5)),(Q(4,5),0),
                   (Q(9,10),0),(Q(19,10),1),(6,1)])
    mid = Path([(0,Q(9,10)),(Q(9,10),0),(Q(19,10),1),(6,1)])
    post = Path([(0,Q(9,10)),(Q(3,5),Q(3,10)),
                 (Q(27,40),Q(3,8)),(Q(39,40),Q(3,40)),
                 (Q(19,10),1),(6,1)])
    high = Path([(0,1),(6,1)])
    return [Law([(Q(9,10), p), (Q(9,100), m), (Q(1,100), high)])
            for p, m in [(low,mid),(curved,mid),(low,post),(curved,post)]]


def main():
    counts = Counter()
    for law_index, law in enumerate(laws()):
        for a in [Q(3,4),Q(4,5),Q(19,20),Q(99,100)]:
            for v in [-a,-a+Q(1,10)]:
                initial = sum((w for w,p in law.paths if p.value(Q(0)) <= a),Q(0))
                lower = law.radial(a,v,strict=True)
                upper = max(initial,law.radial(Q(1),v))
                d1, m = 1-lower, 1-upper
                assert m == Q(1,100)
                full_cuts = law.line_cuts(Q(1), v, Q(1), horizontal=True)
                first = None
                for index, w in enumerate(full_cuts):
                    here = 1-law.radial(Q(1),w,strict=True)
                    next_value = (1-law.radial(Q(1),(w+full_cuts[index+1])/2,strict=True)
                                  if index+1 < len(full_cuts) else here)
                    if max(here,next_value) > d1:
                        first = w
                        break
                assert first is not None
                ystar = 1+first
                assert ystar > 4*m
                cuts = law.line_cuts(Q(1), v, ystar-1, horizontal=True)
                probes = cuts[:-1]+[(x+y)/2 for x,y in zip(cuts,cuts[1:])]
                assert all(1-law.radial(Q(1),w,strict=True) <= d1 for w in probes)
                assert 1-law.radial(1+4*m,ystar-1) >= m
                counts['full first-lower gate with strict traces'] += 1
                for v2 in [Q(-1,5),Q(1,2),Q(89,100),Q(9,10),Q(19,20)]:
                    for delta in [Q(1,1000),Q(1,50),Q(39,1000),Q(1,25),Q(2,25)]:
                        s2 = 1+delta
                        choices = [[(v2,s2)]]
                        if s2 < 1+4*m:
                            for v3 in [(v2+s2)/2, max(v2,Q(19,20))]:
                                if v3 < s2:
                                    choices.append([(v2,s2),(v3,(s2+1+4*m)/2)])
                        for turns in choices:
                            route = multi_route(a,v,turns)
                            final_s = turns[-1][1]
                            if final_s >= 1+4*m:
                                assert cost(law,route) >= inward_cost(law,a,v)
                                counts['long final turn: delay comparison'] += 1
                                continue
                            old_s, merge_s = Q(1), final_s
                            first_lower = False
                            for vv,ss in turns:
                                if law.radial(old_s,vv,strict=True) < lower:
                                    merge_s, first_lower = old_s, True
                                    break
                                old_s = ss
                            merge_s = min(merge_s,2+v)
                            replacement = single_route(a,v,merge_s)
                            for _, path in law.paths:
                                for reflection in [-1,1]:
                                    assert first_capture(path,replacement,reflection) <= first_capture(path,route,reflection)
                            counts['short final turn: pointwise one-I merge'] += 1
                            if first_lower:
                                counts['new lower capture before deletion'] += 1
                            if merge_s == 2+v:
                                counts['merge stops at physical endpoint'] += 1
                            if law_index >= 2:
                                counts['actual post-one wave fixtures'] += 1
    print('PASS:',sum(counts.values()),'exact post-one finite-return gate checks')
    for name, value in counts.items():
        print(' ',name+':',value)
    print('Scope: stated CDF gate plus unit-speed same-half finite returns; no global game claim')


if __name__ == '__main__':
    main()
