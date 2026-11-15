#!/usr/bin/env python3
"""Exact physical regression for the positive-prefront boundary extension.

The Princess has a uniform initial radial component: radius q stays fixed
until time 2-q, then moves outward at speed one and sticks at the endpoint.
A stationary endpoint pair carries the remaining probability. This is a
legal front-two field, affine before the front, with actual endpoint atoms.
For uniform mass m its radial endpoint probability is
1-m+m*clamp((t-1)/2,0,1), hence nondecreasing. Before the positive front,
F(U,W)=1/2+m*(U-W)/4, so all required curvature signs hold exactly.

The first-contact oracle integrates over initial radii independently of the
chronological CDF/record integrator. Neither uses the RLR cost formula.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse
import json

from verify_curved_initial_phase import clipped_integral


def clip(rows):
    lo, hi = Q(0), Q(1)
    for a, b in rows:
        a, b = Q(a), Q(b)
        if not a:
            if b < 0:
                return None
        elif a > 0:
            hi = min(hi, b/a)
        else:
            lo = max(lo, b/a)
    return (lo, hi) if lo < hi else None


def clean(path):
    answer = []
    for t, x in path:
        t, x = Q(t), Q(x)
        assert -1 <= x <= 1
        if answer and t == answer[-1][0]:
            assert x == answer[-1][1]
            continue
        if answer:
            a, y = answer[-1]
            assert t > a and abs(x-y) == t-a
        answer.append((t, x))
    return answer


def physical_score(path, mass):
    """Integrate earliest actual contacts of the three physical rank pieces."""
    uniform, branches_seen = Q(0), 0
    for sign in (-1, 1):
        # Position ar*q+bt*t+c; each guard is a*q+b*t<=k.
        pieces = [
            (Q(sign), Q(0), Q(0), [(0, -1, 0), (1, 1, 2)]),
            (Q(2*sign), Q(sign), Q(-2*sign),
             [(-1, -1, -2), (2, 1, 3)]),
            (Q(0), Q(0), Q(sign), [(-2, -1, -3)]),
        ]
        branches = []
        for (start, x), (end, y) in zip(path, path[1:]):
            v = (y-x)/(end-start)
            offset = x-v*start
            for ar, bt, c, guards in pieces:
                if v == bt:
                    assert ar != 0  # at most one uniform rank, of zero mass
                    continue
                slope, intercept = ar/(v-bt), (c-offset)/(v-bt)
                rows = [(-slope, intercept-start), (slope, end-intercept)]
                rows += [(Q(a)+Q(b)*slope, Q(k)-Q(b)*intercept)
                         for a, b, k in guards]
                domain = clip(rows)
                if domain is not None:
                    branches.append((*domain, slope, intercept))
        cuts = {Q(0), Q(1)}
        for lo, hi, _, _ in branches:
            cuts.update((lo, hi))
        for p, q in combinations(branches, 2):
            lo, hi = max(p[0], q[0]), min(p[1], q[1])
            if p[2] != q[2]:
                at = (q[3]-p[3])/(p[2]-q[2])
                if lo < at < hi:
                    cuts.add(at)
        cuts = sorted(cuts)
        for lo, hi in zip(cuts, cuts[1:]):
            rank = (lo+hi)/2
            possible = [p for p in branches if p[0] <= rank <= p[1]]
            assert possible, (path, sign, lo, hi)
            first = min(possible, key=lambda p: p[2]*rank+p[3])
            uniform += (first[2]*(hi*hi-lo*lo)/2+first[3]*(hi-lo))/2
        branches_seen += len(branches)
    endpoint = Q(0)
    for side in (-1, 1):
        hits = [t for t, x in path if x == side]
        assert hits
        endpoint += min(hits)/2
    return mass*uniform+(1-mass)*endpoint, branches_seen


def cdf(t, x, mass):
    """Interior trace, including one-sided traces at the two endpoints."""
    radius = max(Q(0), min(abs(x), (2-t+abs(x))/2))
    return Q(1, 2)+(mass*radius/2 if x > 0 else
                     -mass*radius/2 if x < 0 else 0)


def record_score(path, mass, skip_positive_reset=None):
    low = cdf(*path[0], mass)
    right = 1-low
    cost = Q(0)
    intervals = 0
    for (start, x), (end, y) in zip(path, path[1:]):
        if x == -1:
            low = Q(0)
        if x == 1 and start != skip_positive_reset:
            right = Q(0)
        v, offset = (y-x)/(end-start), x-(y-x)*start/(end-start)
        cuts = {start, end}
        # Center and the two characteristic seams of the explicit field.
        for slope, intercept in ((v, offset), (1+v, offset-2),
                                 (1-v, -offset-2)):
            if slope:
                at = -intercept/slope
                if start < at < end:
                    cuts.add(at)
        cuts = sorted(cuts)
        for lo, hi in zip(cuts, cuts[1:]):
            a, b = (3*lo+hi)/4, (lo+3*hi)/4
            fa, fb = cdf(a, v*a+offset, mass), cdf(b, v*b+offset, mass)
            slope = (fb-fa)/(b-a)
            intercept = fa-slope*a
            assert cdf((lo+hi)/2, v*(lo+hi)/2+offset, mass) == slope*(lo+hi)/2+intercept
            assert slope*v >= 0
            low = min(low, slope*lo+intercept)
            right = min(right, 1-slope*lo-intercept)
            if v > 0:
                cost += low*(hi-lo)+clipped_integral(
                    (Q(0), -slope, 1-intercept), lo, hi, right, 'min')
                right = min(right, 1-slope*hi-intercept)
            else:
                cost += right*(hi-lo)+clipped_integral(
                    (Q(0), slope, intercept), lo, hi, low, 'min')
                low = min(low, slope*hi+intercept)
            intervals += 1
        if y == -1:
            low = Q(0)
        if y == 1 and end != skip_positive_reset:
            right = Q(0)
    return cost, low, right, intervals


def light_to_physical(path):
    return clean([((u+w)/2, (u-w)/2) for u, w in path])


def first_exit(path):
    for index, ((start,x),(end,y)) in enumerate(zip(path,path[1:]),1):
        velocity = (y-x)/(end-start)
        offset = x-velocity*start
        events = []
        for kind, slope, intercept in (
                ('center',velocity,offset),
                ('endpoint',velocity,offset-1),
                ('front',1+velocity,offset-2)):
            if slope:
                at = -intercept/slope
                if start <= at <= end:
                    events.append((at,kind))
            elif not intercept:
                events.append((start,kind))
        if events:
            at,kind = min(events)
            return kind,index,at
    return None,None,None


def runs_before(path, stop):
    runs, previous = 0, None
    for (a,x),(b,y) in zip(path,path[1:]):
        if a >= stop:
            break
        direction = (y-x)/(b-a)
        if direction != previous:
            runs += 1
            previous = direction
    return runs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    fixtures = [
        ('center_truncation', [(Q(1, 4), Q(-1, 4)), (Q(3, 4), Q(-1, 4))],
         Q(7, 4), Q(1)),
        ('endpoint_truncation', [(Q(1, 2), Q(-1, 2)), (Q(3, 4), Q(-1, 2))],
         Q(7, 4), Q(1, 2)),
        ('front_or_center_truncation', [(Q(3, 4), Q(-3, 4)), (Q(3, 4), Q(1, 4))],
         Q(2), Q(3, 2)),
        ('both_physical_truncations', [(Q(1, 2), Q(-1, 2))],
         Q(7, 4), Q(3, 4)),
        ('unproductive_right_center_minimum',
         [(Q(19, 20), Q(-19, 20)), (Q(19, 20), Q(1, 2))],
         Q(2), Q(3, 2)),
    ]
    counts = {'exact_physical_record_agreements': 0, 'physical_capture_branches': 0,
              'chronological_affine_intervals': 0, 'endpoint_minimum_comparisons': 0,
              'productive_triples': 0, 'first_right_unproductive': 0,
              'middle_left_unproductive': 0, 'actual_endpoint_atom_resets': 0,
              'early_boundary_prefix_run_checks': 0,
              'center_endpoint_is_minimizer': 0,
              'front_endpoint_is_minimizer': 0,
              'first_right_run_erased': 0, 'last_right_run_erased': 0,
              'center_boundary_paths': 0, 'endpoint_boundary_paths': 0,
              'front_boundary_paths': 0}
    rows = []
    for name, prefix, u1, w1 in fixtures:
        u0, w0 = prefix[-1]
        lower, upper = max(u0, w1), min(u1, w0+2)
        assert lower < upper
        # Every path has exactly this same physical suffix after (u1,w1).
        suffix = [(u1, u1+2), (u1+4, u1+2)]
        for mass in (Q(1), Q(2, 3), Q(1, 3)):
            prefix_path = light_to_physical(prefix)
            if len(prefix_path) == 1:
                low = cdf(*prefix_path[0], mass)
                high = low
            else:
                _, low, right, _ = record_score(prefix_path, mass)
                high = 1-right
            scores, paths = [], []
            for i in range(9):
                u = lower+(upper-lower)*Q(i, 8)
                path = light_to_physical(prefix+[(u,w0),(u,w1),(u1,w1)]+suffix)
                physical, branches = physical_score(path, mass)
                recorded, left, right, intervals = record_score(path, mass)
                assert physical == recorded and left == right == 0
                counts['exact_physical_record_agreements'] += 1
                counts['physical_capture_branches'] += branches
                counts['chronological_affine_intervals'] += intervals
                f = cdf((u+w0)/2, (u-w0)/2, mass)
                g = cdf((u+w1)/2, (u-w1)/2, mass)
                counts['productive_triples'] += int(f > high and g < low)
                counts['first_right_unproductive'] += int(f <= high)
                counts['middle_left_unproductive'] += int(g >= low)
                scores.append(physical)
                paths.append(path)
            for score in scores:
                assert min(scores[0], scores[-1]) <= score
                counts['endpoint_minimum_comparisons'] += 1
            boundaries = []
            for path, score in ((paths[0],scores[0]),(paths[-1],scores[-1])):
                kind, index, at = first_exit(path)
                assert kind in ('center','endpoint','front')
                counts[kind+'_boundary_paths'] += 1
                if at <= (u1+w1)/2:
                    assert runs_before(path,at) <= (3 if kind == 'center' else 2)
                    counts['early_boundary_prefix_run_checks'] += 1
                if score == min(scores) and kind in ('center','front'):
                    counts[kind+'_endpoint_is_minimizer'] += 1
                boundaries.append({'first_exit':kind,'exit_time':str(at),
                                   'score':str(score)})
                if kind == 'endpoint' and mass < 1:
                    t = at
                    nominal = record_score(path, mass, skip_positive_reset=t)[0]
                    assert nominal > score
                    later = min(s for s,x in path if x == 1 and s > t)
                    assert nominal-score == (1-mass)*(later-t)/2
                    counts['actual_endpoint_atom_resets'] += 1
            counts['first_right_run_erased'] += int(lower == u0)
            counts['last_right_run_erased'] += int(upper == u1)
            rows.append({'fixture':name,'uniform_radial_mass':str(mass),
                         'feasible_peak_interval':[str(lower),str(upper)],
                         'incoming_records':[str(low),str(1-high)],
                         'endpoint_scores':boundaries,
                         'minimum_sample_score':str(min(scores))})
    assert all(counts[key] > 0 for key in counts)
    report = {'status':'PASS','scope':'Exact supplied-field boundary regression, not equilibrium or phase-existence evidence.',
              'law':'Uniform initial radial mass remains stationary until t+r=2, then moves outward and sticks; remaining mass is a stationary endpoint pair.',
              'checks':counts,'fixtures':rows}
    text = json.dumps(report, indent=2)+'\n'
    args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
