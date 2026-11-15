"""Exact first-inverse support gate for a free inward second turn.

The gate is a necessary condition for CI_s <= Cell(s).  It does not
identify an equilibrium support, or presume that Cell(s) is active.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_free_second_inward_field import (
    Law, Princess, direct_route, finite_fixtures, initial_inward_route,
)


def main():
    counts = Counter()
    def ordinary(a,u,c):
        return Princess([(Q(0),a), ((u-a)/2,(u+a)/2),
                         ((u+c)/2,(u-c)/2), (1+c,Q(1)), (Q(2),Q(1))])
    # In these laws some initial ranks lie above the free second turn but
    # reach the terminal row at the same V.  Thus A(s)>=R(1,v) really fails.
    extra = [Law([(Q(1,2),ordinary(Q(3,10),Q(7,20),Q(1,5))),
                  (Q(1,2),ordinary(Q(4,5),Q(9,10),Q(0)))])]
    for original in list(finite_fixtures()) + extra:
        law = Law([(w, Princess(list(p.knots)+[(Q(8), Q(1))]))
                   for w, p in original.paths])
        starts = {Q(1,10), Q(1,4), Q(1,2), Q(3,4), Q(9,10)}
        starts.update(p.value(Q(0)) for _, p in law.paths
                      if 0 < p.value(Q(0)) < 1)
        for a in sorted(starts):
            A = sum((w for w,p in law.paths if p.value(Q(0)) <= a), Q(0))
            x = 1-a
            for v in [-a, -a/2, Q(0), a/2]:
                y = 1+v
                L = law.radial(a,v,strict=True)
                d = 1-L
                for s in sorted({a, (3*a+1)/4, (a+1)/2, (a+3)/4, Q(1)}):
                    B = law.radial(s,v)
                    if B <= A:
                        continue
                    k = 1-s
                    rk = sum((w for w,p in law.paths
                              if p.value(Q(0)) > s), Q(0))
                    rx, Dk = 1-A, 1-B
                    first = law.integrate(s,-s,s,horizontal=True,strict=True,
                        transform=lambda rank:max(Q(0),rank-L))
                    bound = ((8-k-y)*(Dk-rk)-(y-k)*rk
                             +(y-x)*rx-first)
                    ci = direct_route(law,initial_inward_route(a,v,s))
                    cell = direct_route(law,[(Q(0),s),(s+1,Q(-1)),(s+3,Q(1))])
                    actual = 4*(ci-cell)
                    assert actual >= bound, (a,v,s,actual,bound)
                    counts['bound versus direct physical captures'] += 1
                    if ci <= cell:
                        assert ((8-k-y)*(Dk-rk)
                                <= first+(y-k)*rk-(y-x)*rx)
                        counts['necessary support gate'] += 1
                    if bound > 0:
                        assert ci > cell
                        counts['strictly excluded inward responses'] += 1
                    if rk > 1-law.radial(Q(1),v):
                        counts['future-row gate-failing turns covered'] += 1
                    if law.radial(a,v) != L:
                        counts['strict initial-turn witnesses'] += 1
    print('PASS:',sum(counts.values()),'exact free-inward support-gate checks')
    for label,count in counts.items():
        print(' ',label+':',count)
    print('Scope: necessary active-support bound; no equilibrium claim')


if __name__ == '__main__':
    main()
