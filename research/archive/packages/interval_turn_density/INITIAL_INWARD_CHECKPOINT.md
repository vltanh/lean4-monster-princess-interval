# Initial-inward components and released line support

This is a structural checkpoint, not a game-value bound. The experiments use
the same eleven outer density intervals. They construct and check full
normalized monster laws, but they do not construct a matching unrestricted
princess law or close the equilibrium proof.

## What was added and tested

The uniform initial-inward law adds density `i(a,v)=h(a)` on `-a<v<a`.
Its extra mass is `integral 2a h(a) da`. The exact four-score feature is in
`interval_turn_sheet/uniform_inward_features.py`; its independent verifier
passed 483 checks, including complete physical integrations. The apparent
first-touch slack disappears along the joint canonical epsilon construction,
so this supplies a response supremum, not an unattainable extra allowance.

`inward_attached_law.py` initially required independent nonnegative,
nondecreasing h. The full fit chose h identically zero. A second model,
`inward_curvature_law.py`, allowed h to decrease above 7/8, subject to three
explicit sets of sufficient conditions:

* k and k+2h remain nondecreasing, preserving the positive-prefix U ordering.
* The full signed-M3 beta curvature controls each possible h decrease in the
  positive V direction.
* Integral gates preserve the actual calibrated flat regions: `H<=7h/8`
  below the early-M2 turn floor and `H<=h/2` above it, where `H(U)=integral_0^U h`.

The last gates are essential; checking the raw target-minus-alpha formula
alone would miss the local cancellations in those regions. The relaxed fit
also chose h=0. Every added gate and support-equality multiplier was zero.
Against its frozen response dual, all eleven unit uniform-v density columns
have average cost above the LP level, with a minimum difference about .01020
per unit probability mass. Thus this finite response pool rejects the entire
tested uniform-v addition, rather than merely its monotonicity restriction.
That conclusion concerns the finite pool and the stated family.

The localized law instead puts unit density on
`D<a<1, -a<v<-D`, with `D=7/8`. Its mass is `(1-D)^2/2`. The independent
physical verifier passed 260 checks, including 22 full triangle-density
integrations and 81 tied-ramp cancellations.

The first localized experiment tied this density to `k=ell=eta*(U-D)+`.
Every induced negative-early-M2 and signed-M3 density was included. Because
`D<s0`, the early sheet has the nonzero lower edge `s0-D`; its generator is
not obtained by integrating blindly from D. The combined mass is
`eta*(1-D)^2`. The resulting fit chose eta=0.

The next version removes the tied ramp. For the existing step k, the added
negative-prefix score is convex inside each U interval. Common-threshold
rounding preserves the order of an inverse graph, so the full optimizer uses
finitely many U levels and an exact crossing arrangement. The positive-prefix
optimizer is the existing one because this localized I component has no
positive-V inverse term. No extra density-shape condition is needed.

## An optional support restriction was removed

The old equality `k=ell` above 7/8 was an optional geometry restriction, not a
hypothesis of the bounded response theorem. The negative M2 line at `U=1`
can start anywhere up to 1. Releasing those four equalities preserves the
prefix first variation, suffix envelope, and physical residual tests.
The driver exposes this as `--negative-start-bound 1`.

The resulting `independent_full_start_discovery.json` has normalization 1
and minimum structural slack approximately `-1.6e-15`. It uses new negative
M2 line mass `.00242995483`, entirely on starts `[.875,.9375]`, with density
`.0388792773`. The line residual vanishes above `.9375`, so the new mass does
not overlap the interior of the early turn range. The independent localized
I amplitude remains zero.

The numerical response was `1.42509540702`; the finite response LP objective
was `1.42509539679`. These report a discovery calculation and its separation
gap, not a new rigorous interval. The remaining genuine shape normal is k
monotonicity at `.984375`, about `.00008972`. The three upper line residuals
have physical nonnegativity multipliers about `.00418,.00418,.00585`. The
nonzero f-join multiplier is degenerate at two zero f values.

The frozen dual puts about `.13654` weight on negative-c no-extra rows, but
all those rows have initial coordinate exactly 1 in the limiting feature
representation. It has **not** produced a continuous ordinary terminal
phase. A small negative-c extra row remains. Neither the frozen multipliers
nor the boundary-limit paths are asserted to be a valid matching lower law.

## Verification and numerical trace correction

The complete induced ramp column passed five independent reconstructions
from capture-checked step generators, with maximum absolute error
`2.61e-17`, and 33 independent density-kernel checks, with maximum error
`1.83e-17`. The combined localized-law verifier now passes 60 zero-component
whole-oracle comparisons exactly, supplies a feasible normalized eta=.2 law,
and passes 960 positive-prefix competitors. The tied negative optimizer
passed 3,840 complete-feature competitors; the independent-I optimizer passed
3,840 competitors including independently integrated affine inverse graphs.

A finite-knot probe was corrected after the first tied fit. `bin_at` snaps
within `1e-13` to the right bin; a `nextafter` left probe therefore read the
wrong trace and created spurious slopes near `1e-12`. Divided primitive
expressions amplified these to score noise around `2.1e-8`. The bounded ramp
oracle now uses the original explicit left/right probes. The singular-tail
oracle's finite-knot left probe was corrected too, while retaining its true
infinite endpoint price. Frozen feature identities were unaffected.

## Stable entry points

* `discover_inward_attached.py`: uniform h and the separately labelled
  curvature/corridor relaxation.
* `discover_localized_inward.py`: localized I plus its tied ramp.
* `discover_independent_inward.py`: localized I alone; use
  `--negative-start-bound 1` for the released-support result.
* `verify_inward_positive.py`, `verify_localized_law.py`, and
  `verify_localized_ramp.py`: the additional full-law checks owned here.

The remaining work is joint support and density selection, including a
continuous terminal attachment and a legal lower strategy against every
monster path. Further fitting of the same fixed triangle is not a substitute
for those obligations.
