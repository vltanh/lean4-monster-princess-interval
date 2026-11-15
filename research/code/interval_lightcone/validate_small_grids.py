"""Regression: the unrestricted half-offset lattice value L_n plus 1/(4n) reproduces the exact
clock-grid optima U_n already certified in research/code/interval_clock_grid (n = 1, 2, 3, 4, 6)."""
import json, os, sys
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice_game import solve

here = os.path.dirname(os.path.abspath(__file__))
ok = True
for n in (1, 2, 3, 4, 6):
    cert = json.load(open(os.path.join(here, "..", "interval_clock_grid", f"grid_n{n}_certificate.json")))
    exact = Fraction(cert["exact_value"])
    out = solve(n, iters=5000, verbose=False)
    got = out["value_lp"] + 1 / (4 * n)
    err = abs(got - float(exact))
    ok &= err < 1e-10
    print(f"n={n}: exact U_n = {exact} = {float(exact):.15f}   lattice value + 1/(4n) = {got:.15f}   |diff| = {err:.1e}")
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
