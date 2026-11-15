#!/usr/bin/env python3
"""Exact local operator check for full-width shared-threshold interpolation.

Standard library only. This is a field-refinement regression, not a game-value
or best-response certificate.
"""
from fractions import Fraction as F
import json


def weights(u, v, su, sv, lo=F(0), hi=F(1)):
    assert 0 <= u <= 1 and 0 <= v <= 1 and lo < hi
    cuts = sorted({lo, hi} | {z for z in (u if su > 0 else 1-u,
                                          v if sv > 0 else 1-v)
                             if lo < z < hi})
    out = [F(0) for _ in range(4)]
    for a, b in zip(cuts, cuts[1:]):
        z = (a+b)/2
        i = int(u > (z if su > 0 else 1-z))
        j = int(v > (z if sv > 0 else 1-z))
        out[2*i+j] += (b-a)/(hi-lo)
    assert sum(out) == 1
    return out


def linear_combination(w, values):
    return [sum(w[i]*values[i][k] for i in range(4)) for k in range(4)]


def main():
    tests = marginals = local_formula = 0
    probes = [F(0), F(1, 5), F(1, 3), F(1, 2), F(2, 3), F(4, 5), F(1)]
    for su in (-1, 1):
        for sv in (-1, 1):
            for m in range(1, 8):
                nodes = {(i, j): weights(F(i, m), F(j, m), su, sv)
                         for i in range(m+1) for j in range(m+1)}
                for i in range(m):
                    for j in range(m):
                        corners = [nodes[i, j], nodes[i, j+1],
                                   nodes[i+1, j], nodes[i+1, j+1]]
                        for a in probes:
                            for b in probes:
                                u, v = (i+a)/m, (j+b)/m
                                direct = weights(u, v, su, sv)
                                refined = linear_combination(weights(a, b, su, sv), corners)
                                assert direct == refined, (su, sv, m, i, j, a, b, direct, refined)
                                assert direct[2]+direct[3] == u
                                assert direct[1]+direct[3] == v
                                marginals += 2
                                if su == sv:
                                    formula = [1-max(u, v), max(v-u, 0),
                                               max(u-v, 0), min(u, v)]
                                else:
                                    formula = [max(1-u-v, 0), min(v, 1-u),
                                               min(u, 1-v), max(u+v-1, 0)]
                                assert direct == formula
                                local_formula += 1
                                tests += 1
    # A non-idempotent narrow interpolation, included to check the theorem's scope.
    a, b = F(1, 4), F(3, 4)
    coarse = sum(w*x for w, x in zip(weights(F(1, 4), F(0), 1, 1, a, b), [0, 0, 1, 1]))
    fine = sum(w*x for w, x in zip(weights(F(1, 2), F(0), 1, 1, a, b), [0, 0, F(1, 2), F(1, 2)]))
    assert coarse == 0 and fine == F(1, 4)
    print(json.dumps({
        "status": "PASS",
        "scope": "exact local full-width interpolation/refinement identity; no game-value claim",
        "orientation_pairs": 4,
        "refinement_factors": list(range(1, 8)),
        "operator_equalities": tests,
        "coordinate_marginal_equalities": marginals,
        "closed_form_equalities": local_formula,
        "narrow_width_countercheck": {"coarse": str(coarse), "refined": str(fine)},
    }, indent=2))


if __name__ == "__main__":
    main()
