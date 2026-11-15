# Center-wait / principal one-turn exact subgame

This small, standalone Fraction regression audits the *physical first-contact*
formulas in [the exact subgame proof](../../research/13-equilibrium-geometry/CENTER_WAIT_PRINCIPAL_ONE_TURN_EXACT.md).

Run `python3 packages/interval_center_wait_principal/verify.py` from the repository root.

The analytic game value is `3/2 - exp(-1/2)/2`. The Monster uses
a `exp(-1/2)` atom at initial position zero and continuous density
`exp((a-1)/2)/2` on positive starts; fair reflection is applied.
The Princess's uniformly approaching strategy has a continuous radius density
and center departure times strictly below one.

**Scope:** every Princess pure path must move inward to the *exact center*
at unit speed, wait there, then move outward at unit speed to an endpoint.
The Monster is restricted to the principal turn level `t+x=1`, together
with its reflections. The theorem supplies an **upper bound**, not an exact
value, when the Monster is allowed *all* one-interior-turn routes.
This is not an unrestricted-game solution.

The regression does **not** verify the analytic proof or certify the larger
project's numerical game bounds.
