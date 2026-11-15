#!/usr/bin/env python3
"""Exact deletion cost for two inward/outward excursions on one side.

The first-capture engine is independent of the row/column moment formula.
This is a finite-route identity and a record-based deletion lemma, not an
all-monster certificate or an assertion about an equilibrium support.
"""
from collections import Counter
from fractions import Fraction as Q

from verify_positive_cdf_sheet import Law, Path, finite_fixtures, first_capture
from verify_curved_terminal_sources import fixture, inward_cost


def repeated_route(a, v1, s1, v2, s2):
    return [(Q(0), a), ((a+v1)/2, (a-v1)/2),
            ((s1+v1)/2, (s1-v1)/2),
            ((s1+v2)/2, (s1-v2)/2),
            ((s2+v2)/2, (s2-v2)/2),
            (s2+1, Q(-1)), (s2+3, Q(1))]


def cost(law, route):
    return sum((weight*(first_capture(path, route, 1)
                        +first_capture(path, route, -1))/2
                for weight, path in law.paths), Q(0))


def alpha_moment(law, s, deficit):
    """Two times integral_0^deficit alpha_(1-q)(s)dq."""
    lower=max(-s,s-2)
    outside=2*max(Q(0),s-1)*deficit
    return outside+law.integrate(s, lower, s, horizontal=True, strict=True,
                                  transform=lambda R: max(Q(0), R-(1-deficit)))


def beta_moment(law, v, deficit, anchor=Q(1)):
    """Column inverse moment at a common anchor >= both outward turns."""
    assert anchor<=2+v
    return law.integrate(v, -v, anchor, horizontal=False,
                         transform=lambda R: max(Q(0), R-(1-deficit)))


def four_deletion_difference(law, a, v1, s1, v2, s2):
    A = sum((weight for weight, path in law.paths
             if path.value(Q(0)) <= a), Q(0))
    initial = 1-A
    d1 = 1-law.radial(a, v1, strict=True)
    d = max(d1, 1-law.radial(s1, v2, strict=True))
    m1 = min(initial, 1-law.radial(s1, v1))
    m2 = min(m1, 1-law.radial(s2, v2))
    m0 = min(initial, 1-law.radial(s2, v1))
    assert m0 <= m2 <= m1 <= initial <= d1 <= d

    anchor=max(Q(1),s2)
    high_loss = ((v2-v1)*(m1-m2)+(2*s2+6-anchor-v1)*(m2-m0)
                 -beta_moment(law, v2, m1,anchor)+beta_moment(law, v2, m2,anchor)
                 +beta_moment(law, v1, m1,anchor)-beta_moment(law, v1, m0,anchor))
    low_gain = (alpha_moment(law, s2, d)-alpha_moment(law, s2, d1)
                -alpha_moment(law, s1, d)+alpha_moment(law, s1, d1))
    return high_loss-low_gain, dict(initial=initial, d1=d1, d=d,
                                    m1=m1, m2=m2, m0=m0)


def main():
    laws = finite_fixtures()
    law, _, _, _ = fixture(Q(1), [(Q(0), Q(0)), (Q(1, 2), Q(1, 4)),
                                (Q(1), Q(1))], Q(4))
    laws.append(law)
    counts = Counter()
    for law in laws:
        for a in [Q(3, 10), Q(3, 5), Q(4, 5), Q(19, 20)]:
            for f1 in [Q(0), Q(1, 5), Q(1, 2)]:
                v1 = -a+a*f1
                for g1 in [Q(1, 4), Q(3, 4)]:
                    s1 = a+(1-a)*g1
                    for f2 in [Q(1, 4), Q(3, 4)]:
                        v2 = v1+(-v1)*f2
                        for g2 in [Q(1, 3), Q(1)]:
                            s2 = s1+(1-s1)*g2
                            route = repeated_route(a, v1, s1, v2, s2)
                            repeated = cost(law, route)
                            simple = inward_cost(law, a, v1, s2)
                            predicted, records = four_deletion_difference(
                                law, a, v1, s1, v2, s2)
                            actual = 4*(repeated-simple)
                            assert predicted == actual, (a, v1, s1, v2, s2, actual, predicted)
                            counts['exact repeated-return deletion costs'] += 1
                            if records['d'] == records['d1']:
                                assert repeated >= simple
                                counts['no new lower ranks: merge outward legs'] += 1
                            if records['m2'] == records['m1']:
                                assert repeated >= inward_cost(law, a, v1, s1)
                                counts['no new upper ranks: delete last outward leg'] += 1
                            if records['m1'] == records['initial']:
                                assert repeated >= inward_cost(law, a, v2, s2)
                                counts['no first upper captures: delete first outward leg'] += 1
                            if (records['d'] > records['d1']
                                    and records['m2'] < records['m1']
                                    and records['m1'] < records['initial']):
                                counts['genuine interlacing record rectangles'] += 1

        # Both outward turns can lie after U=1; these are distinct from
        # an ordinary pre-one incoming cap and retain every post-one wave.
        for a in [Q(3,5),Q(4,5),Q(19,20)]:
            for v1 in [-a,-a/2]:
                s1=1+(1+v1)/5
                s2=1+2*(1+v1)/5
                v2=v1/2
                repeated=cost(law,repeated_route(a,v1,s1,v2,s2))
                simple=inward_cost(law,a,v1,s2)
                predicted,_=four_deletion_difference(law,a,v1,s1,v2,s2)
                assert 4*(repeated-simple)==predicted,(a,v1,s1,v2,s2)
                counts['both outward turns after U=1']+=1

    # A legal ordered field in which both new capture bands really occur.
    # This prevents the formula test from covering only deletable loops.
    low = Path([(0,Q(2,5)),(Q(3,10),Q(11,20)),(Q(1,2),Q(11,20)),
                (Q(19,20),1),(6,1)])
    middle = Path([(0,Q(31,50)),(Q(1,5),Q(57,100)),(Q(1,2),Q(57,100)),
                   (Q(93,100),1),(6,1)])
    high = Path([(0,Q(7,10)),(Q(1,5),Q(7,10)),(Q(2,5),Q(29,50)),
                 (Q(1,2),Q(29,50)),(Q(23,25),1),(6,1)])
    law = Law([(Q(7,20),low),(Q(9,20),middle),(Q(1,5),high)])
    a,v1,s1,v2,s2 = Q(3,5),-Q(2,5),Q(4,5),-Q(1,5),Q(1)
    actual = cost(law,repeated_route(a,v1,s1,v2,s2))
    predicted, records = four_deletion_difference(law,a,v1,s1,v2,s2)
    assert 4*(actual-inward_cost(law,a,v1,s2)) == predicted
    assert records['d'] > records['d1'] and records['m2'] < records['m1'] < records['initial']
    counts['genuine interlacing record rectangle'] += 1
    comparisons = [inward_cost(law,a,v1,s2), inward_cost(law,a,v1,s1),
                   inward_cost(law,a,v2,s2)]
    assert all(actual < value for value in comparisons), (actual,comparisons)
    counts['strict improvement over all three elementary deletions'] += 3
    print('PASS:', sum(counts.values()), 'exact repeated-same-half checks')
    for name, n in counts.items():
        print(' ', name+':', n)
    print('Scope: exact finite-route identity and deletion gates, no global claim')
    print('Interlacing witness cost:', actual)
    print('Its three elementary-deletion costs:', ', '.join(map(str,comparisons)))


if __name__ == '__main__':
    main()
