# A physical lattice certificate yields a new explicit all-Monster Princess law

**Result.** The existing complete physical lattice certificate supplies a
previously unused feasible nodal-clock lower. Constructive common-threshold
interpolation of those nodal values therefore gives a **new** explicit legal
Princess distribution with unrestricted security

\[
\boxed{S(\widetilde\mu)\ge
\frac{27450199627}{19327352832}
=1.420277255018138223224216037326388888\ldots.}
\tag{1}
\]

This improves the previously retained fixed-law guarantee
`726775425061/512000000000 = 1.419483252072265625`. The unrestricted
**game-value** interval is unchanged. In particular, (1) is not a claim that
the original frozen characteristic-P1 CDF has this continuous security. The
new law uses a specified positive-width common-threshold interpolation.

The result depends on the already completed `B=1536` exhaustive search.
The extractor checks and binds that dependency; it does not rerun it or claim
that an independent normalized-bank search has been performed. This note is
an analytical proof with exact regression checks, not a Lean formalization.

## 1. The physical-to-clock implication

Use `B=2n`, physical time step `Delta=1/B`, and initial-position step
`h=2/B=1/n`. Let `B_n` be the entire physical lattice Monster bank in
[the lattice certificate](INTEGER_LATTICE_VALUE_LOWER_CERTIFICATE.md): all
legal lattice paths starting on the `h`-grid, visiting the center by time
two, and visiting both endpoints by time eight. No prefix-turn restriction
is part of this bank.

Let `F` be a legal symmetric ordered Princess CDF, continuous in the
interior, and let `f` be its signed interior-trace values on the defining
lattice checkerboard. Suppose a completed calculation proves

\[
J(F,m)\ge c\qquad(m\in\mathcal B_n).                     \tag{2}
\]

For a physical path `m`, write `tau_-` for its first visit to the negative
endpoint. A causal active negative clock is a nonnegative measure `eta`
supported on historical path points strictly before `tau_-`, with total
mass `tau_-` and prefix mass at least elapsed time. Its selected time can
be coupled to a scoring time `u` uniformly distributed over
`[0,tau_-)` so that the selected time `s` satisfies `s<=u`. Therefore

\[
\int F^-(s,m(s))\,d\eta(s)
\ \ge\ \int_0^{\tau_-}\inf_{0\le s\le u}
                 F^-(s,m(s))\,du.                         \tag{3}
\]

The right side is the time integral of the surviving lower-rank mass.
The reflected positive clock gives the surviving upper-rank mass. Adding
the two inequalities gives the actual ordered first-contact payoff as a
lower bound for **every** admissible clock plane. This is a one-way
inequality; it does not require a clock plane to attain the physical cost.

For a clock supported on grid vertices, its values on the left of (3) are
exactly the sampled nodal values `f`. Endpoint conventions are essential:

* A clock never selects its own first endpoint: its active interval ends
  there. If the Monster starts at that endpoint, that clock has zero mass.
* At the opposite endpoint, the interior trace equals the strict CDF used
  by that clock. The opposite endpoint atom has already been captured.
* Interior continuity makes the defining center value `1/2` correct.

Thus, for any pair of admissible vertex clocks on any path in the full
bank, (2) and (3) imply

\[
R(m,\eta_-,\eta_+;f)\ge J(F,m)\ge c.                     \tag{4}
\]

The reflection-pair formulation used in the clock-grid code is equivalent:
symmetry identifies the positive clock with the reflected negative clock;
the factor of two in that code cancels the fair reflection weight.
Mixtures preserve (4). If `P_n` is the complete physical/vertex-clock
polytope, and `g=2f-1` on the positive half, then

\[
\boxed{\min_{\alpha\in P_n}R(\alpha,g)\ge c.}             \tag{5}
\]

This is stronger information than merely `c<=U_n`. It is a feasible
**specific-field** nodal lower, even though the original continuous field's
unrestricted security need not be `c-1/B`.

The exhaustive physical proof may normalize a bank path after its first
endpoint or an appropriate terminal time. That is harmless here only
because the source proof establishes (2) for the **entire original bank**.
A lower checked on a finite sample of physical paths would not imply (5).

## 2. Construct a different continuous law

The proof of [constructive Princess extraction](CONSTRUCTIVE_PRINCESS_GRID_DUAL.md)
uses its optimal value `U_n` only through the inequality that every feasible
nodal plane is at least that level. Replace that inequality by (5). Every
other step is unchanged.

For any rational `0<epsilon<=1/2`, let `Z` be uniform on

\[
\left(\frac12-\varepsilon,\frac12+\varepsilon\right).
\]

In each light-coordinate cell `[kh,(k+1)h]`, use threshold `Z` when
`k modulo 2n` lies in `[0,n)`, and threshold `1-Z` otherwise. The same
`Z` rounds both `U=t+x` and `W=t-x`. Use the reflected tie convention
from the extraction theorem; grid points are fixed. The rounding map is
nondecreasing, odd, and periodic up to translation by two.

Define the new interior trace by

\[
\widetilde F_{\rm int}(t,x)
 =\mathbb E_Z f\bigl(T_Z(t+x),T_Z(t-x)\bigr).              \tag{6}
\]

This is a continuous rational piecewise-affine legal CDF. Its radial CDF
is `2 F_int(t,r)-1` for `r<1`, completed by the endpoint value one.
Choose one uniform radial rank and one independent fair sign for the
entire path. The resulting quantile trajectory is 1-Lipschitz; the sign
is not resampled in time.

The source nodal profile is exactly sticky and outward after time two.
The extractor verifies all its transport and sticky endpoint inequalities.
Common rounding preserves those conditions, as proved in
[normalized-bank pricing](NORMALIZED_GRID_BANK_PRICING.md). Hence no
additional endpoint-stopping modification is needed. For completeness,
the exported evaluator uses the outward-after-two continuation explicitly;
all quantiles are at endpoints by time three. The source's stronger
outward-after-one property is also checked, but the security theorem does
not need a global assertion that cutoff one suffices at equilibrium.

Fix any continuous Monster that visits the center by time two and completes
both endpoints by time eight. Choose its minimizing continuous record clocks
against **the new field** (6) before sampling `Z`. Push these same clocks
through the common rounding. A buffer of

\[
b(Z)=h\max(Z,1-Z)
\]

at time zero restores causality; truncating to the required active clock
mass removes only nonnegative cost. The reflected buffer has plane cost
exactly `b(Z)`. The defining expectation in (6) makes the expected
unrepaired pushed cost equal to the original new-field payoff. Applying
(5) to every repaired grid clock therefore gives

\[
J(\widetilde F,m)\ge c-\mathbb E b(Z)
 =c-\frac{1+\varepsilon}{B}.                            \tag{7}
\]

The extraction theorem's endpoint-tour argument covers every continuous
Monster that visits zero by time two. A Monster that does not visit zero
by then pays more than `3/2` against any symmetric law outward after two,
so it cannot violate (7) when the displayed target is at most `3/2`.
The concrete target below satisfies that inequality exactly. Arbitrary
initial positions, waiting, contact equalities, and infinitely many turns
are included in this argument.

Consequently the reusable implication is

\[
\boxed{
\text{full physical-bank lower }c
\quad\Longrightarrow\quad
\text{explicit new law with security }
c-\frac{1+\varepsilon}{B}.}
\tag{8}
\]

The interpolated field is not asserted equal to the source characteristic
field. In particular, full-width interpolation identities do not identify
the narrow-width law in (6) with the frozen source.

## 3. Exact current instance

The frozen source certificate has

\[
B=1536,\quad D=16384,\quad P=256,\quad
K=18308527154,\quad C=2DBP=12884901888,
\]

and proves

\[
c=K/C=9154263577/6442450944.
\]

Set `epsilon=1/1536`. Formula (7) becomes

\[
S(\widetilde\mu)\ge
\frac{9154263577}{6442450944}
-\frac{1537}{2359296}
=\frac{27450199627}{19327352832}.
\]

This is exactly `L_lattice-1/1536^2`. Its improvement over the previously
saved explicit law is

\[
\frac{29972607586967}{37748736000000000}
=0.000794002945872598224216\ldots.
\]

The gap between this **fixed-law security guarantee** and the already
certified **game-value lower** is only `1/2359296`, about `4.24e-7`.
Varying positive `epsilon` produces an explicitly described approaching
family. It does not produce a legal zero-width limiting law, prove
attainment of the game-value lower, or improve the whole-game lower.

The portable descriptor is
`packages/interval_princess_lift/lattice_b1536_princess.json`. It contains a
losslessly compressed, self-contained nodal profile and the exact
interpolation/quantile prescription. Its radial denominator is `D*P`,
and its nodal integer is `(2*f-D)*P`. Thus the existing evaluator's
denominator `4*n*(D*P)` equals the physical source cost scale `C`.
This rescaling does not change any nodal CDF value.

## 4. Reproduction and independent checks

From the repository root:

```bash
python packages/interval_princess_lift/test_lattice_princess_lift.py
python packages/interval_princess_lift/extract_lattice_princess.py verify
node packages/interval_clock_grid/extract_normalized_princess.cjs cdf packages/interval_princess_lift/lattice_b1536_princess.json 0 1/3
node packages/interval_clock_grid/extract_normalized_princess.cjs radius packages/interval_princess_lift/lattice_b1536_princess.json 1/2 1/2
```

The last two exact evaluations return `9129/16384` and
`4671739/12976128`, respectively. Evaluation alone is not a security check.

The extractor checks the source manifest/result agreement, source hashes,
empty final frontier and zero beam truncations, exact scale and fraction,
2,360,064 generated nodal values, 4,715,520 cone inequalities, 1,536 sticky
endpoint inequalities, and 1,180,416 inherited outward-one equalities.
It regenerates the strategy and compares all mathematical metadata and the
decoded nodal bytes. Equivalent zlib encodings are allowed.

The separate standard-library Fraction regression enumerates 4,090 small
physical paths for ten legal fields. It checks 41,544 causal clock planes,
including 15,400 exhaustive short-history clocks and 1,730 partial-record
crossings. Endpoint-start paths and strict physical/clock inequalities are
included. Continuous edge integration is reconstructed by splitting at
exact record intersections; the test imports neither the native edge
formula nor its pruning logic.

The full source search is separately replayed by

```bash
python packages/interval_global_closure/lattice_lower/replay_h3_lattice.py
```

The lift's `verify` command intentionally does not duplicate that
1.84-billion-transition computation. Its report says this explicitly and
does not label the bridge as normalized native or BigInt repricing.

## 5. What this closes and what it leaves open

This closes the gap between the current game-value certificate and the
best retained explicitly evaluable Princess law, up to an arbitrarily
small specified interpolation allowance. It also means any improved
**complete physical lattice** discovery can be lifted to a concrete
all-Monster strategy by the same argument.

It does not establish a free-boundary equation, prove outward-after-one
equilibrium sufficiency, identify the optimal Monster law, or yield a
terminating finite classification. The remaining decisive condition is
still a matching physical all-Princess upper and all-Monster Princess
lower, or a proven sufficient equilibrium class. Fine-grid discovery
remains useful for identifying that class; grid convergence alone cannot
prove exact termination.
