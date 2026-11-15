#!/usr/bin/env python3
"""Exact checks of free-turn characteristics and the free-strip exchange.

All reference capture times come from direct segment intersection. These
checks supplement the written proofs; no grid-game optimality is claimed.
"""

import importlib.util
from fractions import Fraction as F
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "characteristic_reference", ROOT / "packages/interval_characteristic_response/verify.py")
REF = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REF)
at, clean, inverse, capture = REF.at, REF.clean, REF.inverse, REF.direct_capture


def free_turn(x, b):
    assert -1 <= x <= 1 and abs(x) <= b <= 2-x
    return clean([(0, x), ((b-x)/2, (b+x)/2), (b+1, -1), (b+3, 1)])


def reflected(path):
    return [(t, -x) for t, x in path]


def predicted(path, x, b, reflection):
    a = path[0][1]
    A = lambda v: inverse(path, v, 1)
    B = lambda v: inverse(path, v, -1)
    if reflection:
        return A(-x) if x < -a else (F(0) if x == -a else B(b))
    if x == a:
        return F(0)
    if x > a:
        return A(b)
    if a > b:
        # U starts strictly above the turning characteristic. Even at
        # x=b (a zero-length first leg), there is no early capture.
        return B(b+2)
    cutoff = b-2*inverse(path, b, 1, strict=True)
    return B(b+2) if x < cutoff else B(-x)


def clamp(path, delta, eta):
    u0, r = 1+eta, 1-delta/2
    entrance = inverse(path, u0, 1)
    exit_time = inverse(path, r, -1)
    corner = ((u0+r)/2, (u0-r)/2)
    result = [(t, x) for t, x in path if t < entrance]
    result += [(entrance, at(path, entrance)), corner,
               (exit_time, at(path, exit_time))]
    result += [(t, x) for t, x in path if t > exit_time]
    result = clean(result)
    assert all(0 <= x <= 1 for t, x in result)
    assert all(abs(y-x) <= s-t for (t, x), (s, y) in zip(result, result[1:]))
    return result


def main():
    rng = Random(20261111)
    paths = [clean([(0, 0), (6, 0)]), clean([(0, 1), (6, 1)]),
             clean([(0, F(1, 2)), (F(1, 2), F(1, 2)), (1, 0), (6, 0)]),
             clean([(0, 0), (1, 1), (2, 0), (3, 1), (6, 1)])]
    for _ in range(40):
        x = rng.randrange(9)
        p = [(F(0), F(x, 8))]
        for k in range(1, 49):
            x = rng.choice([x+d for d in (-1, 0, 1) if 0 <= x+d <= 8])
            p.append((F(k, 8), F(x, 8)))
        paths.append(p)

    free_cases = q_cases = exchanges = 0
    for p in paths:
        a, d = p[0][1], at(p, F(1))
        for b in [F(0), F(1, 4), F(1, 2), F(7, 8), F(15, 16),
                  F(1), F(5, 4), F(3, 2), F(2), F(5, 2), F(3)]:
            cutoff = b-2*inverse(p, b, 1, strict=True)
            starts = {F(j, 8) for j in range(-8, 9)} | {a, -a, cutoff, 2-b, b, -b}
            for x in starts:
                if not (-1 <= x <= 1 and abs(x) <= b <= 2-x):
                    continue
                m = free_turn(x, b)
                for reflection in (False, True):
                    route = reflected(m) if reflection else m
                    assert capture(route, p) == predicted(p, x, b, reflection)
                    free_cases += 1
        for zeta in [F(1, 16), F(1, 8), F(1, 4), F(1, 2), F(1)]:
            m = free_turn(-1+zeta, 1+zeta)
            t = inverse(p, 1-zeta if d <= zeta else 3+zeta, -1)
            assert capture(m, p) == t
            expected = (inverse(p, 1-zeta, 1) if a < 1-zeta
                        else F(0) if a == 1-zeta else inverse(p, 1+zeta, -1))
            assert capture(reflected(m), p) == expected
            q_cases += 2

        for delta in [F(1, 4), F(1, 2), F(3, 4)]:
            if not a <= 1-delta or not d >= delta:
                continue
            for eta in [F(1, 16), F(1, 8)]:
                entrance = inverse(p, 1+eta, 1)
                for beta in [F(0), F(1, 4), F(1, 2)]:
                    if entrance < (1+eta-beta)/2:
                        continue
                    q = clamp(p, delta, eta)
                    e = inverse(p, 1, 1, strict=True)
                    starts = {F(j, 8) for j in range(-8, 9)} | {a, -a, 1-2*e}
                    for x in starts:
                        m = REF.monster_path(2, x)
                        for route in (m, reflected(m)):
                            assert capture(route, p) == capture(route, q)
                    sweep = REF.monster_path(1, F(-1))
                    for route in (sweep, reflected(sweep)):
                        assert capture(route, p) == capture(route, q)
                    # An atomic positive-M1 measure tests the lemma without
                    # relying on continuity of parameter densities.
                    xs = [F(j, 16) for j in range(17) if F(j, 16) >= beta]
                    improvement = F(0)
                    for x in xs:
                        m = REF.monster_path(1, x)
                        for route in (m, reflected(m)):
                            improvement += (capture(route, q)-capture(route, p))/(2*len(xs))
                    mass = F(sum(1-delta < x < 1-eta for x in xs), len(xs))
                    assert improvement >= delta*mass/8
                    exchanges += 1

    assert exchanges > 50
    print(f"PASS: {free_cases} free-turn and {q_cases} fixed-time-turn exact captures.")
    print(f"PASS: {exchanges} atomic free-strip exchanges preserve M2 and attain the gain bound.")


if __name__ == "__main__":
    main()
