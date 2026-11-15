#!/usr/bin/env python3
"""Cross-check discovery integration against independent rational integrals.

NumPy, SciPy, and Numba are optional discovery dependencies. The actual
functional identity verifier, verify.py, uses only the standard library.
"""

from fractions import Fraction as Q

import numpy as np

from discover import features
from verify import evaluate


def main():
    knots = np.array([0,1/8,1/4,3/8,1/2,5/8,3/4,7/8,
                      15/16,31/32,63/64,1.])
    widths = np.diff(knots)
    # This unnormalized measure is intentional: it checks linearity of
    # every signed component, not the value of a probability strategy.
    weights = np.r_[1/7, widths,2*widths,3*widths,4*widths]
    cases = [(2,6,1,3),(2,6,3,5),(2,6,7,8),
             (5,7,2,8),(5,7,6,8),(5,7,-4,-2),
             (5,7,-4,2),(5,7,-1,8),(6,7,-5,-1)]
    checked = 0
    for denominator in (8,9,11):
        for case in cases:
            parameters = tuple(Q(x,denominator) for x in case)
            exact = evaluate(parameters,(1,),(2,),(3,),(4,))/4
            computed = float(features(np.array([float(x) for x in parameters]),
                                      knots)@weights)
            assert abs(computed-float(exact)) < 1e-12, (parameters,computed,exact)
            checked += 1
    print(f"PASS: {checked} independent constant-density integral comparisons")
    print("Scope: discovery-feature arithmetic; no equilibrium or value bound")


if __name__ == "__main__":
    main()
