# Characteristic first-capture verification

Run `python verify.py` with Python's standard library.

The exact formulas in
`../../research/08-continuum/CHARACTERISTIC_RESPONSE.md` are checked against
an independent direct piecewise-linear intersection routine. The input
includes explicit plateau and equality fixtures, plus 200 reproducible
bounded random paths. Every calculation uses exact fractions.

This checks capture formulas; it does not certify an equilibrium or an
optimal response-shape reduction.
