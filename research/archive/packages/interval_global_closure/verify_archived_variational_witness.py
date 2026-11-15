#!/usr/bin/env python3
"""Exact archived-response gap arithmetic; source capture engines are separate."""
import json
from fractions import Fraction
from pathlib import Path

root = Path(__file__).resolve().parents[2] / "packages" / "interval_global_closure"
pair = json.loads((root / "paired_strategy_regret.json").read_text())
response = json.loads((root / "upper_dyadic_princess_response.json").read_text())
assert pair["princess_paths"] == 338
assert pair["monster_reflected_pairs"] == 280
cross = Fraction(pair["cross_payoff"])
lower = Fraction(pair["lower_response"])
upper = Fraction(pair["upper_response"])
actual = Fraction(response["actual_princess_payoff"])
assert upper == Fraction(response["response_ceiling"])
assert upper - actual == Fraction(response["exact_best_response_gap"])
assert lower < cross < actual < upper
princess_defect = actual - cross
monster_defect = cross - lower
assert princess_defect > Fraction(29, 10000)
assert monster_defect > Fraction(56, 10000)
for n in (1, 2, 4, 8, 16, 100):
    lam = Fraction(1, n)
    assert (1-lam)*cross + lam*actual == cross + lam*princess_defect
print("Exact Princess CDF ascent lower bound:", princess_defect)
print("Exact Monster deviation gain:", monster_defect)
print("These are frozen-law defects, not new unrestricted value bounds.")
