# Full ordered-CDF optimization and a stronger unrestricted upper certificate

Date: 2026-11-13. **This improves the unrestricted Monster upper bound.
It does not solve the game or provide a matching Princess lower law.**

## 1. Exact statement

The rational symmetric Monster law in
[`full_order_upper_exact.json`](../../packages/interval_global_closure/full_order_upper_exact.json)
has 241 reflected trajectory pairs and guarantees

\[
\boxed{
V\le U_{\mathrm{order}}
=\frac{1140799301969009059644426513}
       {800000000000000000000000000}
=1.4259991274612613\ldots .}
\]

Each listed pair has probability `weight_numerator / 1000000000000`;
the two reflected paths within a pair are equiprobable. A vertex `[U,V]`
means physical time `(U+V)/2` and position `(U-V)/2`. Consecutive vertices
are joined at unit speed, and the path remains at its final endpoint
after its last vertex. Every route visits both endpoints by
`4062499999999999/1000000000000000`, which is less than 7.

The improvement over the previously retained tight common-warp upper is

\[
\frac{104476307239828103773667}
     {800000000000000000000000000}
=0.0001305953840498\ldots .
\]

The existing lower certificate remains unchanged. The certified interval
is therefore

\[
\frac{36290299773897097}{25600000000000000}
\le V\le U_{\mathrm{order}},
\]

with exact width

\[
\frac{6727434034724778394426513}
     {800000000000000000000000000}
=0.008409292543406\ldots .
\]

## 2. What the numerical discovery optimized

The physical geometry came from the previous 280-pair warped law. On
that complete event geometry, the Princess variables were the marginal
probabilities of all 19,234 priced order thresholds. The optimization
retained every implication in the order polytope and every reward
conjunction for all 280 Monster rows.

Each conjunction contains literals of one sign only. For a common
uniform threshold coupling, its probability is the minimum of the
corresponding marginals. Thus the resulting concave row objectives
describe the whole ordered-CDF response on this event geometry, rather
than a preselected Princess path mixture. An auxiliary-free cutting-plane
solve reached numerical row minimum `1.4259991262833078` and relaxation
upper `1.4259991262891067`.

Those floating-point numbers are discovery results. They are not used
as proof. The Monster dual weights were rounded to denominator
`1000000000000`, normalized exactly, and all zero weights removed. The
resulting 241-pair physical law was then passed to the exact unrestricted
Princess oracle from scratch. That exact calculation, and not the
numerical LP objective, gives the rational value in Section 1.

## 3. Why the certificate covers every Princess path

The existing finite-event inverse-curve theorem applies to every finite
unit-speed Monster law. It represents a radial Princess trajectory by
monotone inverse labels, retains strict and closed first-contact sides,
and bounds the unrestricted supremum by a finite maximum-closure problem.
Conversely its optimal labels have legal approaching physical
realizations. Reflection reduces the general Princess oracle to that
radial problem without a turn-count assumption. See
[`GERM_RESPONSE.md`](GERM_RESPONSE.md),
[`GENERALIZED_GERM_REALIZATION.md`](GENERALIZED_GERM_REALIZATION.md),
and the previously audited exact response engine
[`atomic_survival_v8.cjs`](../../packages/interval_turn_density/atomic_survival_v8.cjs).

For this law the exact graph has 75,268 nodes and 191,435 directed arcs.
Its integer maximum flow and a matching minimum cut yield exactly
`U_order`. The verifier checks flow capacities and conservation, then
rebuilds the graph and replays the positive-flow witness on that separate
construction. It also compares the directly evaluated extreme optimal
label rows with the flow value. No sampled Princess bank enters this
upper verification.

The probability, physical speed, arena, starting-time and endpoint
completion checks are independent of the flow calculation. In total the
241 representative routes have 750 unit-speed legs.

## 4. Endpoint baseline and the remaining defect

The fair stationary-endpoint Princess has payoff

\[
M=\frac{356499183697229725947074931}
        {250000000000000000000000000}
=1.4259967347889189\ldots .
\]

Consequently the exact unrestricted response exceeds that baseline by

\[
D=U_{\mathrm{order}}-M
=\frac{9570689369683068933669}
       {4000000000000000000000000000}
=0.000002392672342420767\ldots .
\]

This is the minimum clock/matching deficiency for this fixed physical
law under the established causal-pressure duality. The subsequent
[finite clock homogenization](FINITE_BANK_CLOCK_HOMOGENIZATION.md)
has now recovered actual physical clocks and an exact matching at this
same value. A standalone integer replay verifies that the entire residue
is a submeasure of the continuous sweep front. The
[explicit continuum completion](ENDPOINT_FRONT_DEFICIENCY_COMPLETION.md)
therefore produces a zero-deficiency Monster law with exact worst-case
payoff `U_order`, attained by each stationary endpoint Princess. This
is a second unrestricted upper proof; it does not prove global optimality
or give a Princess security guarantee of `U_order`.

## 5. Reproduction and remaining goal

From the repository root run:

```sh
node --stack-size=16384 packages/interval_global_closure/verify_full_order_upper.cjs
```

The only inputs are the committed rational law and the existing response
engine. The verifier regenerates and checks the exact flow; no numerical
solver, saved LP basis, or uncommitted discovery file is needed. Its native
run passed all checks, including 83,601 positive-flow entries.

To solve the original game, an unrestricted Princess lower certificate
must meet an unrestricted Monster upper certificate at the same constant.
The newly discovered ordered CDF is being tested against free Monster
starts and turns outside the old geometry. Its finite-bank minimum is
not an unrestricted lower bound. No Lean compilation or formal kernel
verification is claimed.
