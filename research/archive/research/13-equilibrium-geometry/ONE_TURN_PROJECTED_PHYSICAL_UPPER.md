# Improved physical one-turn upper with independent projected replay

> **Superseded upper, retained for reproduction.** The later [continuum countercertificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) proves W_1≤142472349375511/100000000000003<U_* and closes the frozen separation target negatively. This note's earlier physical certificate remains valid.

**Status: valid historical all-Princess upper.** The frozen separation
comparison is now closed negatively by the continuum result above; the exact
restricted value remains open. The Monster class is the canonical
class of unit-speed paths with at most one interior reversal before the first
endpoint, followed by a direct sweep to the opposite endpoint. The Princess
is unrestricted.

## 1. The retained theorem

The rational law in
[one_turn_projected_upper.json.gz](../../packages/interval_one_turn/one_turn_projected_upper.json.gz)
satisfies, for every legal Princess path,

\[
 \mathbb E_\nu T(m,p)\le B_{\rm proj}
 :=\frac{478205958821456999}{335544320000000000}
 =1.425164815251401\ldots.
\]

Thus this earlier certificate gives the valid enclosure

\[
 \boxed{\frac{36409808231}{25600000000}\le W_1
 \le\frac{478205958821456999}{335544320000000000}.}
\]

The lower endpoint is inherited from the already certified unrestricted
game lower. This update supplies no new Princess lower certificate.

The upper improves the previous
[causal-clock certificate](ONE_TURN_PHYSICAL_UPPER.md) by exactly

\[
 \frac{1165888329615857}{8388608000000000000}
 =0.00013898471946905338\ldots.
\]

It exceeds the frozen unrestricted benchmark
\(U_*=291849329389899/204800000000000\) by exactly

\[
 \boxed{B_{\rm proj}-U_*
 =\frac{200087745232387}{1677721600000000000}
 =0.00011926158978485287\ldots>0.}
\]

This projected certificate alone does not decide the comparison with
\(U_*\). The later continuum certificate does decide it and improves
the unrestricted upper; the frozen benchmark and its provenance are retained.

## 2. Physical law

There are 375 positive-weight reflected pairs. A listed physical path and
its spatial reflection are used with equal conditional probability. The
integer pair weights have common denominator \(10^{10}\). All listed legs
have positive duration and unit speed; all starts are at time zero in
\([-1,1]\). Every path completes its direct endpoint-to-opposite-endpoint
sweep by time \(136314829/33554432\). No postcapture continuation is present.

| Physical class | Reflected pairs | Exact probability |
|---|---:|---|
| Endpoint start, immediate sweep | 1 | \(614170753/1000000000\) |
| Interior start, endpoint first | 51 | \(2105144763/10000000000\) |
| One interior reversal before the endpoint tour | 323 | \(1753147707/10000000000\) |

The probabilities sum to one. The stored vertices are rational light
coordinates \((U,V)=(t+x,t-x)\); their common coordinate denominator is
67,108,864. That denominator describes this certificate, not a restriction of
the continuous one-turn game.

The endpoint-component obstruction in
[ONE_TURN_ENDPOINT_REPAIR_OBSTRUCTION.md](ONE_TURN_ENDPOINT_REPAIR_OBSTRUCTION.md)
concerns the earlier fixed interior law. This improved law changes both
interior and endpoint weights, so its smaller upper does not contradict
that obstruction.

## 3. Why the certificate bounds every Princess

The existing finite-event inverse-curve response theorem gives a valid upper
for every Princess against a fixed reflection-symmetric physical Monster
law. Its normalization and strict/closed contact conventions include atoms
and initial coincidence. The finite algebra is an ordered-threshold closure
problem, with nonnegative physical survival lengths multiplying conjunctions
of true thresholds or conjunctions of false thresholds.

The independent verifier reconstructs these clauses directly from the
rational physical paths. It does not use the optimizer's value or the graph
builder's saved geometry, reward table, or formal Princess labels.
The [verification note](../../packages/interval_one_turn/PROJECTED_UPPER_VERIFICATION.md)
gives the complete reconstruction and its mathematical dependency.

Only sound order implications are admitted. Their completeness is
unnecessary for the upper direction: omitting an implication enlarges the
response set. Every priced threshold must still be included. Auxiliary
nodes convert the positive conjunction and negative disjunction rewards
into a linear closure objective.

Let \(S=67108864\) and \(W=10^{10}\). Independent integer reconstruction gives

\[
\begin{aligned}
 C&=2639222631148291316,\\
 P&=2505934516305978158,\\
 F&=1319509476882613482,\\
 C+P-F&=3825647670571655992.
\end{aligned}
\]

Here \(C\) is the constant reward, \(P\) the sum of positive signed
coefficients, and \(F\) the value of an integer flow whose capacity equals
the supplied cut. Consequently every physical Princess payoff is at most

\[
 \frac{C+P-F}{4SW}=B_{\rm proj}.
\]

| Independently reconstructed quantity | Result |
|---|---:|
| Full threshold nodes | 135,195 |
| Retained projected threshold nodes | 38,288 |
| Sound supplied threshold implications | 75,755 |
| Physical reward clauses | 103,776 |
| Auxiliary closure nodes | 74,314 |
| Graph nodes, including source and sink | 112,604 |
| Graph arcs | 328,157 |
| Positive flow entries checked | 203,621 |

Every capacity, probability, node balance, terminal total, and cut crossing
is checked with exact integers. An optimal formal label vector is not
asserted to be an actual finite-width Princess witness, and no such witness
is needed for the upper.

The coordinate discovery used the [joint common-warp and flow LP](ONE_TURN_COMMON_WARP_FLOW.md). The final bound comes from the separately rounded physical law and independent replay.

## 4. Reproduce from the compact law

From the repository root:

```sh
python3 packages/interval_one_turn/rebuild_projected_upper.py \
  --output /tmp/one-turn-projected
```

This validates canonical membership, compiles the existing C++17 flow
proposal helper, rebuilds the rational response graph with Node, checks the
proposed flow with JavaScript BigInt arithmetic, and independently replays
the physical construction with Python. It performs no numerical LP search.
Python's standard library, Node, and a C++17 compiler suffice.

The independent replay can also be run on the generated certificate:

```sh
python3 packages/interval_one_turn/verify_projected_upper.py \
  /tmp/one-turn-projected/one_turn_projected_upper.certificate.json
python3 packages/interval_one_turn/verify_projected_upper.py --self-test
```

The retained
[replay report](../../packages/interval_one_turn/one_turn_projected_upper_replay.json)
binds the exact law, generated certificate, reconstructed quantities, and
benchmark comparison with SHA-256 hashes. The self-tests include nondyadic
geometry, both auxiliary clause signs, endpoint continuation, zero weights,
and rejection of 17 corrupted certificates.

Both rebuild and replay accept `--require-counterexample`. The flag rejects
this law because its exact upper remains above \(U_*\). The later
continuum verifier passes the corresponding gate and disproves the
strict separation target. It does not identify \(W_1\), prove
\(W_1=V\), or establish optimality of the supplied measure.

No CI run or new Lean formalization is claimed.
