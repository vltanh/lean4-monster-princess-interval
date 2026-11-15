# Probes of the missing endpoint and turn geometry

This package records a fixed structural experiment and exact characteristic
checks. Its floating LP outputs are **not** rational certificates or new
claims about the unrestricted value. The experiment changes the available
path families; it does not run a sequence of finer game grids.

## Exact checks

`verify_characteristics.py` uses only the Python standard library. It
compares general two-turn first-capture formulas with independent direct
segment intersection, including initial equalities, turn equalities, and
plateaus. The general path starts at x, turns on characteristic U=b,
visits -1 at b+1, and then +1 at b+3, on the full domain
`-1<=x<=1`, `|x|<=b<=2-x`. Turns before `U=1` are included. When the
princess starts above b, its unreflected capture is always late; the
zero-length-first-leg case cannot be assigned to a generic cutoff
equality branch.

It also checks the free-strip replacement used by
`research/09-equilibrium-structure/SUFFIX_GAP_EXCLUSION.md` against atomic
positive M1 measures. The replacement preserves every tested M2 capture
and delays the stated positive-M1 captures by at least the quantitative
bound.

```sh
python packages/interval_turn_curve_discovery/verify_characteristics.py
```

The recorded run passes 9,440 general free-turn captures, 440 fixed-time
turn captures, and 142 atomic free-strip exchanges. These are arithmetic
and boundary checks of the proof formulas, not a replacement for the
arbitrary-path arguments in the manuscript.

## One fixed support, three geometric comparisons

`probe_turn_curve.py` uses the existing floating direct-flow LP. The base
support has both M1 and M2 at the fixed start positions k/8. The added
parameter list is fixed at

`eta = 1/64, 1/32, 1/16, 1/8, 1/4, 1/2, 3/4, 1`.

The three probes are:

- `--families q`: add Q_eta, which starts at -1+eta, turns at time one at
  eta, and then visits -1,+1. These paths receive zero weight in this
  particular optimum.
- `--families fq`: also add F_eta=M1(1-eta). Q paths now receive positive
  total mass, about 0.00796. Endpoint probing on both sides of the response
  constraint matters.
- `--families flq`: additionally add L_eta=M1(-1+eta). Negative M1 paths
  receive about 0.02476 total mass, concentrated on the three new start
  positions nearest -1. Most of the Q mass disappears; about 0.000444
  remains in this fixed support.

The last observation supports the analytical exclusion: forbidding
interior negative M1 starts omits useful responses. On the natural top
bins, the negative M1 weights suggest a roughly constant density, while
the positive M1 density has a much higher terminal branch. These are
shape observations for candidate discovery, not proofs of an optimal
density or of optimal support boundaries.

The source uses NumPy and SciPy through the existing direct-flow module;
its deadline oracle also uses the project's optional numerical
dependencies. Each probe solves its prescribed LP once, then independently
evaluates the resulting weights with the deadline response oracle. The
JSON and logs preserve the floating objectives and active weights. No
rationalization, new bound verification, mesh-refinement loop, or Lean/CI
run was performed.

## Independent negative-M2 turning offsets

`probe_free_turn.py` keeps the preceding signed/endpoint support and adds
one prescribed list of negative M2 starts and independent turning offsets:

`z = 1/8, 2/8, ..., 7/8`,
`b-1 = 1/128, 1/32, 1/8, 1/4, 1/2`.

The completed floating LP assigns positive extra weight only at `b=33/32`,
with starts `-5/8`, `-3/4`, and `-7/8`, totaling about 0.002018. The
original `b=1` component remains much larger. This is evidence for a
secondary turning characteristic in this fixed support, not a proof of a
continuum support curve. The source, complete output JSON, and log are
saved alongside the other probes. No parameter-refinement loop or new
rational game-bound claim is attached to this experiment.
