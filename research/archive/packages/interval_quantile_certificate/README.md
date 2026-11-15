# Exact quantile laws, continuum attacks, and center-balance pruning

This package supplies three tools for the requested narrow unrestricted
enclosure: exact finite-quantile extraction, exact continuous physical
attacks with supporting CDF planes, and a validated center-balance
restriction for the finite-quantile response oracle. It has **not** produced
a new global lower or a width below `1/10000`.

## A genuine deficit in the retained full-width CDF

Let `F` be the **full-width** common-threshold interpolation of
`../interval_clock_grid/lower_n256_field.json`, source SHA-256
`81483589b60c14d823d2bb467015a321d77cf555076fe8d69a36d63cd829d7d5`.
This field is exactly the full-width interpolation of its coarse n=64
samples; all 262,400 fine nodal identities are checked before coarsening.

The rational Monster route in `current_fullwidth_attack.json` is

| Time | Position |
|---|---|
| `0` | `31/32` |
| `63/32` | `-1` |
| `127/32` | `1` |

Every leg has speed one. Its first endpoint is reached at time
`1.96875`, before two. Direct chronological integration, including
every field boundary, record crossing and endpoint reset, gives

\[
 J_F(m)=\frac{36421298289}{25600000000}
       =1.4227069644140625.
\]

Thus this full-width field's unrestricted security is **at most** that
number. Removing its numerical transfer allowance cannot raise its actual
security to approximately `1.425`. This is an obstruction for this supplied
field, not a global game upper and not an assertion about the saved
narrow-width `lower_n256_princess.json` law.

The saved replay verifies every affine interval with two chronological
implementations. It also freezes the minimizing continuous clocks along
this route and integrates their exact full-width nodal coefficients.

```bash
python packages/interval_quantile_certificate/score_continuous_attack.py \
  packages/interval_clock_grid/lower_n256_field.json \
  packages/interval_quantile_certificate/current_fullwidth_attack.json \
  --output /tmp/current_fullwidth_attack_replay.json
```

The `constant` and `[j,k,coefficient]` rows form a supporting **upper** plane
for the actual route payoff over all full-width Qout fields on `contour_n`.
They are useful exact separation cuts during Princess optimization. A
future CDF's minimum record cost cannot exceed the cost of these fixed
causal clocks. The continuous clock intervals and historical atoms are
retained explicitly. Trapezoidal nodal coefficients integrate the fixed P1
basis; they are **not** presented as a causal atomic clock at the later
endpoint of each scoring interval, nor as an all-Princess Monster upper.

### Finding additional continuous attacks

`search_continuous_attacks.py` supplies five independently parameterized
physical path families: an initial outward turn, an initial inward turn,
two turns, two turns with first endpoint at time two, and a precenter
inward-then-outward loop. The bounded parameters always produce legal
unit-speed paths. Exploration uses a vectorized floating implementation
of the exact full-width P1 trace and its capped affine integrals. The best
parameters are snapped to rationals; all arrival times are then rebuilt
from exact distances, preserving speed and endpoint validity.

```bash
python packages/interval_quantile_certificate/search_continuous_attacks.py \
  packages/interval_clock_grid/lower_n256_field.json \
  --output /tmp/continuous_attacks --starts 6 --seed 1701 \
  --seconds 120 --exact-top 5
```

The `.search.json` report separates exploratory scores from the exact
`.plane*.json` outputs. Each exact plane is replayed by the two rational
chronological implementations and binds the source hash and interpolation
class. They are candidate optimization cuts; even a large bank of these
attacks does not establish a Princess lower. The helper exposes `FastField`,
`positions`, `snap_route`, and `search` for repeated optimization against
changing fields. Families can discover the same path, so callers may
deduplicate exact coefficient vectors before adding cuts.

## Exact finite quantile extraction

`extract_quantiles.py` traces quantile level sets through the full-width
triangulation using rational arithmetic. For radial rank count `K` and
field denominator `D`, it chooses

\[
 u_k=\frac{(2k+1)(D+1)+1}{2K(D+1)},\qquad 0\le k<K.
\]

No rank equals a nodal value: its numerator is one modulo `D+1`, which
is coprime to `D`. Consequently a level set cannot pass through a mesh
vertex or branch along a constant-valued edge. Its intersections with all
triangulation edges give the complete polygonal quantile path. The
transport inequalities make its speed at most one. The path stops at an
endpoint and moves maximally outward after time two. Reflection and equal
rank weights give an explicit finite ordered symmetric law; duplicate
endpoint paths are merged.

This is a **new finite Princess law**. A certificate for its unrestricted
Monster-response problem is directly a lower for the game; no physical-grid
transfer is needed. Conversely, extracting finitely many ranks and merely
testing some attackers does not certify that lower. The finite-initial-
support nonattainment theorem continues to exclude an exact attained
equilibrium of this form, but does not exclude an approaching family.

```bash
python packages/interval_quantile_certificate/extract_quantiles.py \
  packages/interval_clock_grid/lower_n256_field.json \
  --ranks 256 --output /tmp/current_256 --check-points
g++ -O3 -std=c++17 \
  packages/interval_quantile_certificate/center_balanced_response.cpp \
  -lgmpxx -lgmp -o /tmp/center_balanced_response
QUANTILE_CENTER_BALANCE=1 /tmp/center_balanced_response \
  /tmp/current_256.paths.txt 1000000
```

The response engine is derived from the existing exact GMP
`continuous_response_fast_search.cpp`. Its only new mathematical pruning
rule is described below and is opt-in. Its input, earliest contacts,
states, dominance comparisons, pursuit bounds and objective use exact
rationals. A stopped priority search reports an attained upper `value`
and a valid frontier `lower_bound`; it must not report the upper as the
law's guaranteed security unless the search is complete.

## Finite-atomic center-balance theorem

The opt-in rule requires a symmetric ordered finite law whose positive
paths stay **strictly positive**, whose negative paths stay strictly
negative, whose endpoints are sticky, and whose motion after time two is
maximally outward until absorption. The executable independently checks
these conditions. General center-atomic laws are rejected by this mode.

The cap exchange in
`research/12-global-closure/CENTER_HEAVIER_FIRST_BALANCE.md` remains valid
for these atomic laws. On a positive outward ray use `S=1-F^+`, the closed
capture trace. Its possible jumps do not affect the integral cap
inequalities, monotonicity, or the sorted-record comparison. At the center
both strict and closed traces equal `1/2`.

Thus an optimal center continuation can be chosen as heavier-first
alternating triangles, with every returned affected record at most the
opposite record. To use this inside a **capture-event** oracle requires a
joint normal form, not just two separate existence theorems:

1. Retain the precenter prefix of an optimal finite capture-event response.
   Normalize its center continuation to the heavier-first balanced form.
   At the first center, the untouched opposite fair half is a heavier
   side, so the first departure can align with the incoming unit leg.
   On a tie, reflect the whole center continuation to make that choice.
2. If a triangle's peak occurs after its last new outbound capture, trim
   the peak back to that capture. The Monster returns to the center
   earlier with exactly the same records; replacing the saved time by
   a center hold initially preserves cost exactly.
3. Absorb that hold into the **next opposite-side** maximal triangle,
   keeping its old return time. It pointwise dominates the hold and old
   triangle. It starts with the same heavier-side records and can only
   lower its affected outgoing record, preserving the next balance
   comparison. At height at least one, use the legal endpoint-tour
   replacement. Proceed forward so that previously trimmed peaks remain
   untouched. A no-new-capture triangle disappears by this procedure,
   contradicting the minimum-triangle choice.
4. For the final tour, if the opposite record `l>0` and its first endpoint
   turn captured no residual mass, its last same-side capture occurred
   at some height `a<1`. Turning there reaches the opposite endpoint
   `2(1-a)` earlier and strictly saves `2l(1-a)`. Therefore an optimal
   final first-endpoint turn is a new capture when both sides survive.
   If the opposite record is zero, the finite oracle terminates upon
   clearing the remaining targets; any endpoint padding is cost-free.

The resulting unit-speed route changes direction only at new finite-target
captures and satisfies the center balance rule. It is therefore contained
in the original complete capture-event tree.

At a capture state on the positive side **after a genuine center visit**,
turning toward a negative target reaches the center without changing either
surviving record. Such a turn need only be considered when the negative
surviving weight is at least the positive surviving weight. Apply the
reflected condition on the negative side. The executable establishes the
prior center visit conservatively by checking that the captured rank
interval already contains targets of both signs. It never applies this
test to the unrestricted precenter prefix.

The existing finite-law memo key retains the exact captured rank interval
and anchor; it does not compare different surviving masses. Its
earlier-time/lower-cost dominance can shadow the same strictly signed
anchor, preserving the balance comparisons. The phase-dependent
componentwise Pareto issue in a nodal-grid engine is a separate problem;
see `research/12-global-closure/DISCRETE_CENTER_BALANCE_PRICING.md` for the
required phase-value lemma there.

## Verification and measured limitation

```bash
python packages/interval_quantile_certificate/test_quantile_certificate.py
```

The regression compares both solver modes with an independent exhaustive
Python `Fraction` next-capture tree, without dominance or lower-bound
pruning. It independently replays every returned physical route, checks
that unsupported center/contact hypotheses are rejected, and tests the
frozen-clock supporting-plane inequality on other legal fields.

A local scaling pilot on the retained full-width field gave:

| Positive ranks | Signed paths | Result | Processed states | Time |
|---:|---:|---|---:|---:|
| 64 | 128 | Complete: `1.40020605605688` | 159,326 | 24.5 s |
| 64, balance enabled | 128 | Same exact rational optimum | 148,383 | 20.1 s |
| 256 | 512 | Incomplete: lower about `1.07627`, attack `1.42023` | 1,000,000 | 218.7 s |
| 1024, balance enabled | 2048 | Incomplete: lower about `0.74061`, attack `1.42236` | 100,000 | 39.7 s |

The 64-rank law's attaining route costs about `1.4228171991` against
the original continuous field, but only `1.4002060561` against the
finite law. The observed loss is about `1.4471/K`; that is one measured
example, not a convergence-rate theorem. The much denser pilots do not
certify useful lowers. Their unresolved precenter branching makes a
large uniform rank increase unjustified with the current engine.

The useful retained outputs are the exact contour extractor, the physical
attacker and its exact optimization cut, the verified finite-law balance
rule, and the scaling evidence. A stronger field and a substantially
sharper continuum or response certificate are still required for the
requested `1/10000` enclosure.
