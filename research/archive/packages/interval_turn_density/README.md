# Separated early and late turning-density research

This package constructs genuine two-dimensional negative-M2 laws and
computes their response to **all princess paths** through an analytic
four-scalar reduction. It is a research bridge to an equilibrium, not a
claim that the game has been solved.

The proofs are in:

* `research/10-turn-density/UPPER_EQUALITY_CORRIDOR.md`;
* `research/10-turn-density/SEPARATED_SHEETS_RESPONSE.md`.

## Ordered prefixes and an attached analytic tail

`ORDERED_NEGATIVE_PREFIX.md` in the research directory removes monotonicity
of `p=f+g` from the signed-M3 construction. A complete adjacent-violator
calculation chooses ordered negative inverse blocks, while retaining the
same four free scalar parameters. The implementation and independent
checks are `negative_prefix_oracle.py` and `verify_negative_pava.py`.
The numerical law in `negative_prefix_discovery.json` has a response near
`1.42514378`; it is not an exact ceiling or a matching lower law.

`SINGULAR_TAIL_ATTACHMENT.md` records the complete continuous-tail law,
including every induced turning sheet and its residual conditions. It
uses one analytic density component and no new density optimization bins.
Its tested outer attachment fails to select the required ordinary branch.
The exact game proof remains open; the failed phase selection and its
binding structural conditions are preserved with the full law.

## Main implementation

`separated_oracle.py` takes fixed density knots and variables

    w0, f, g, k, ell,

where k is the total negative-start alpha density. The line density is
the residual `h0=k-ell-Hearly-Hlate`, and normalization is
`w0+integral(f+g+k)=1`.

The early sheet has separate start and turn bands. With `--edge-trace`,
it uses

    h_early(z,s)=[k(s0)-k(z)]/(s0+6-z)
                      +integral_s0^s k'(r)/(r+6-z)dr.

The nonzero trace at s0 removes the flat-k restriction of the first
construction. Its score decreases up to s0 and is flat above s0, so
high incoming prefixes can spread inside a real equality corridor.

The late sheet uses the explicit density that makes the positive suffix
score flat in `1<U<v(V)`. The upper boundary may be genuinely affine:

    v(z)=1+offset+slope*(z-late_left).

The oracle splits exactly where `2-v(z)` crosses an f knot. All feature
integrals are evaluated by polynomial and logarithmic primitives; the
affine curve is not discretized into constant turns.

For fixed densities, the canonical prefix is obtained by a monotone
inverse of `k(z)+beta_a(z)`, and the remaining optimization has only
`a,u,c,y`. A legal path can have additional equality-corridor freedom;
the canonical representative computes its common maximal payoff.

## Current concrete structural candidate

`split_edge_affine_discovery.json` is the latest, less restrictive
candidate:

* early starts: `[1/8,1/2]`;
* late starts: `[5/8,7/8]`;
* early turns: `[15/16,1]`;
* late upper boundary: `v(z)=1+1/32+(z-5/8)/64`;
* a nonzero early lower-edge density, with nonconstant k;
* no negative-M2 starts above `7/8`.

Its sampled LP objective is approximately `1.4254295168`, and the
numerical four-scalar separation found `1.4254295350`. These decimals
are **not an exact game bound**. The stored structural multipliers are
nonzero, and the LP dual is **not a matching princess lower law**.

Earlier JSON files record fixed-support structural comparisons, including
the overly restrictive endpoint-cap experiment. `affine_outer_search.json`
records a bounded two-parameter search with fixed bins. No density-bin
refinement was performed in that search.

## Reproduce the current candidate

The session's research dependencies are in `experiment_deps` next to
the checkout. From the repository root:

```sh
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_density/discover_separated.py --left 0.125 --right 0.5 --late-left 0.625 --late-right 0.875 --offset 0.03125 --slope 0.015625 --edge-trace --rounds 7 --output split_edge_affine_discovery.json
```

The fixed-profile density LP is linear. Each added row freezes its whole
prefix profile; changing the density later does not silently change old
LP constraints. The updated global scalar oracle produces new rows when
needed. Density inequalities and class-defining equality multipliers are
reported separately.

## Verification performed

`verify_corridor.py` uses only the Python standard library. It checks
the late-sheet capture integrals, effective prices, and pointwise
envelope with exact fractions, including step densities.

`verify_separated.py` uses the experiment dependencies. It checks:

* 80 zero-sheet regressions against the independently implemented signed
  scalar functional;
* four actual piecewise-linear princess paths against direct first
  segment intersections with all monster components;
* a genuinely affine late boundary;
* a nonconstant k and a positive lower-edge early-sheet trace.

The latter checks integrate the actual capture times independently of
the analytic feature assembly and extrapolate legal epsilon paths.
Observed discrepancies were below `9e-16`. Numerical quadrature here
is an implementation cross-check, not the proof of the global upper
response theorem or an exact equilibrium certificate.

No Lean compilation or CI was run.

## Continuous endpoint tail

`endpoint_tail.py` implements the independently audited logarithmic tail.
Write `eps=1-a`, `x=log(16/eps)`, and

    gamma=log(3/2)/log(4),
    H(x)=x^gamma sum_(n>=0) c_n/x^n,
    c_0=1,
    c_n=-12(gamma-n+1)c_(n-1)/(4^n-1).

The series converges for every positive x. Its coefficients after c_0 are
negative, its derivative is positive, and the implementation verifies
positivity on the stated density domain `x>=log(16)`. It satisfies

    12 H'(x)=H(x)-(3/2)H(x/4),
    H(x)=(1/2) integral_0^infinity exp(-r/3) H(x/4+r) dr.

Consequently the continuous densities

    f(1-eps)=B eps^(-2/3) H(log(16/eps)),
    ell(1-eps)=(B/2) eps^(-1/6) H(log(16/eps))

satisfy the dominant incoming identity exactly for the leading front maps
`delta(eps)=4 sqrt(eps)` and `eta(eps)=eps^2/16`. This removes all errors
that are inverse powers of the logarithm; finite-power corrections still
matter. These densities have finite integrals and no endpoint atoms.
The real H is a selected positive basis, not a uniqueness result: other
homogeneous oscillatory modes are not excluded by leading asymptotics.

`fit_endpoint_tail.py` goes further. It uses `p=f+g` as its primary density,
with primitive P, and solves the exact terminal a and c stationarity
equations through a scalar linear Volterra equation for the primitive
Lambda of ell. For `r=delta^{-1}` these equations are

    g(1-t)=[w0+P(r(t))+Lambda(eta(r(t)))
                -(t+eta(r(t)))p(1-t)]/(8-2t),
    ell(1-t)=[(delta(t)+eta(t))p(1-t)-t*g(1-t)
                +Lambda(t)-Lambda(eta(t))]/(8-2t).

The remaining incoming stationarity is

    P(delta(t))-P(t)=(delta(t)-t)ell(1-eta(t)).

This last equation is linear in p and w0. The script fits it with eight
analytic power/pantograph functions, using the corrected fractional
lower-history series and the particular term `(88/125)t` for delta, and
`eta=t^2/16*(1+sqrt(t)/15)`. The local result is stored
in `endpoint_tail_fit.json`. At the default cutoff `1e-5`, an off-sample
audit over eleven orders of magnitude gives relative a and incoming
residuals below `6e-8`, with positive f, g, and ell and increasing f and
ell on independent probes. Adaptive quadrature separately checks the
primitives. This is an actual continuous local candidate, but its lower
front data are still asymptotic, and it has not been attached to an outer
law or checked as a complete equilibrium.

Reproduce the boundary construction from the repository root:

```sh
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_density/endpoint_tail.py
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_density/fit_endpoint_tail.py
```

## Archived response dual seed

`extract_dual_seed.py` reconstructs the LP dual using the archived active
paths and their frozen prefix profiles. The resulting
`split_edge_affine_dual_seed.json` has 25 positive response weights,
summing to one, and reproduces the archived objective to `1.5e-14`.
Its structural multipliers are retained: it is a geometric seed for the
lower-law work, not a lower certificate. Future `discover_separated.py`
runs now store response weights directly, with the exact solved row set.

## Positive late turns and the joint attachment

`positive_sheet_oracle.py` adds a positive-start late-turn sheet to the
separated construction. Its analytic features retain the initial-position
alpha correction; the global four-scalar upper response reduction remains
valid under the hypotheses in
[`TWO_SIDED_LATE_RESPONSE.md`](../../research/10-turn-density/TWO_SIDED_LATE_RESPONSE.md).
`discover_two_sided.py` is a bounded structural smoke test. Its output is
not a certified bound or a matching lower strategy.

The lower-CDF calculation in
[`POSITIVE_TURN_SHEET.md`](../../research/10-turn-density/POSITIVE_TURN_SHEET.md)
retains the negative-row post-incoming flux and the endpoint first-contact
jump. It explicitly solves the local indifferent sheet's cap and exit.
The law still has to attach to the remaining field with ordered quantiles.

```sh
python packages/interval_turn_density/verify_positive_sheet.py
python packages/interval_turn_density/verify_positive_cdf_sheet.py
```

These standard-library checks perform 4,284 exact upper-envelope checks and
4,895 exact lower identities and transport checks. The latter includes
independent direct path-intersection comparisons and fixtures with
nonzero negative-row flux, incoming atoms, and endpoint capture jumps.

`TWO_SIDED_CHECKPOINT.md` records why the saved seed does not yet attach.
`outer_lower_input.json` freezes the numerical history used by
`reconstruct_outer_upper.py`; it is a diagnostic input, not an exact lower
law. Reconstructing two upper stationarity equations leaves the third
unsatisfied. `suffix_switch_splice.py` separately exposes a nonzero
suffix-switch gain. The positive-sheet response dual also fails the
required crossing-rank capacity. None of these fixed-seed failures excludes
all choices of free boundaries and densities.

## Signed early turns and a moving final exit

`positive_early_oracle.py` supplies the additional positive early sheet,
its alpha and beta prices, and the corrected residual and edge rows when
the signed bands overlap. The global response proof, including the
negative-prefix compression across the lower-edge derivative jump, is in
[`SIGNED_EARLY_RESPONSE.md`](../../research/10-turn-density/SIGNED_EARLY_RESPONSE.md).
`verify_signed_prefix_compression.py` performs 2,112 exact isotonic
comparisons. The independent capture integrations are numerical checks of
the feature implementation; they are not equilibrium certificates.

`negative_exit_phase.py` constructs the positive late row with a supplied
nonzero lower-rank flux. Its legal exit is the unique root of a strictly
decreasing scalar function. The elementary rational verification is
standard-library only and checks 4,400 identities. Numerical construction
of a row uses SciPy. The coupled phase and its remaining interface and
normalization equations are in
[`NEGATIVE_EXIT_PHASE.md`](../../research/10-turn-density/NEGATIVE_EXIT_PHASE.md).
No complete phase solution has been selected.

`verify_two_interior_cdf.py` independently checks the full CDF costs for
both signs of monster start and two interior turns. Its 3,113 exact checks
include initial atoms, center and endpoint equality faces, and collapse to
the one-interior-turn family. The proof is in
[`TWO_INTERIOR_TURN_CDF.md`](../../research/10-turn-density/TWO_INTERIOR_TURN_CDF.md).
Controlling this family alone does not control every monster.
