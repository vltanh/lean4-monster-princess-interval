# Current unrestricted lower and upper certificates

Research checkpoint, 2026-11-14. The exact game remains open. The intermediate
interval width below `1e-4` has not been attained.

The retained [incoming-front Princess certificate](../../packages/interval_discovery_certificates/princess_front_n512/README.md)
and the CI-discovered physical Monster law give

\[
\boxed{
\frac{36409808231}{25600000000}
\le V\le
\frac{291849329389899}{204800000000000}.
}
\]

The endpoints are respectively **1.4222581340234375** and
**1.4250455536616162109375**. Their difference is exactly
`570863541899/204800000000000`, or **0.0027874196381787109375**.
Neither certificate is a claim that its strategy is globally optimal. The separately preserved [B=1536 lattice certificate](INTEGER_LATTICE_VALUE_LOWER_CERTIFICATE.md) gives the weaker, independently obtained lower 3050023091/2147483648. Its complete input and replay remain available.

## 1. Current n512 lower and its mathematical dependencies

The [retained refinement packet](../../packages/interval_discovery_certificates/princess_front_n512/README.md)
contains a complete rational Qout profile on the `n=512` physical grid,
with denominator `1600000000` and 1,049,088 stored positive radial nodes.
It is the exact full-width refinement of the front-two n256 profile,
whose SHA256 is `a8e1d84d67e66e08d6d1eeb02f18c6e5121108cb4368ededd9db2e792a97189e`.
The new field's SHA256 is
`a4fe152dbf70f5896c256d3a329f6ac2ab31028421795ae74a3163b399c28e10`.

The unchanged original C++ engine and the exact compressed center engine
both compute

\[
 c=\frac{4663655453568}{3276800000000}
   =\frac{36434808231}{25600000000}.
\]

Independent BigInt target verification proves the same lower over the
whole normalized physical bank. It does not require an optimum of the
field-synthesis LP. The argument is:

1. [Common left-floor atomization](LEFT_FLOOR_CLOCK_ATOMIZATION.md)
   identifies the exact unrestricted-response value of the finite
   unit-speed Monster bank with its causal vertex-clock game.
2. [Bank/profile normalization](NORMALIZED_GRID_BANK_PRICING.md)
   permits branching until the first endpoint or time two. The supplied
   Qout profile is feasible for that full bank. The
   [center phase proof](DISCRETE_CENTER_BALANCE_PRICING.md) and
   [incoming-front theorem](GLOBAL_INCOMING_FRONT_COMPLETION.md)
   preserve its exact record minimum under the compressed oracle.
3. The [quantitative transfer](EFFECTIVE_FINITE_UPPER_REDUCTION.md)
   gives `V>=U_512-1/1024`. Feasibility and the complete pricing lower
   imply `U_512>=c`, hence

\[
 \boxed{V\ge c-\frac1{1024}
            =\frac{36409808231}{25600000000}.}
\]

The original native replay examined 2,609,003,114 retained states and
5,117,238,127 transitions. The compressed center minimum examined
508,713,709 states; the independent BigInt target replay examined
507,231,825 states and 893,765,461 transitions. The two center-based
searches differ in target pruning and implementation, so matching their
state counts is not an asserted invariant. All pruning uses proved
integer inequalities, with no beam or state budget in the certificate.

The original and compressed C++ runs completed in
[43545082756](https://github.com/vltanh/lean4-monster-princess/actions/runs/43545082756).
Independent BigInt verification and strategy extraction completed
successfully in
[43546803161](https://github.com/vltanh/lean4-monster-princess/actions/runs/43546803161),
job `132300097087`, artifact `14095016913`.
Their input, verifier-source and extraction-source hashes are retained.
The manuscript normalization and transfer are not claimed as Lean
kernel checks.

## 2. Current explicit law and retained predecessors

The [feasible-dual extraction theorem](NORMALIZED_PRINCESS_EXTRACTION.md)
constructs a legal symmetric ordered Princess law for every rational
`0<epsilon<=1/2`, with security at least

\[
                    c-\frac{1+\varepsilon}{1024}.
\]

The saved `interval_discovery_certificates/princess_front_n512/princess.json` uses
`epsilon=1/1024`. It guarantees

\[
 \boxed{c-\frac{1025}{1048576}
       =\frac{582556541071}{409600000000}
       =1.42225718034912109375.}
\]

Letting the positive width tend to zero gives the slightly larger
value lower in Section 1. Do not assign that larger lower to this one
fixed strategy. The actual law chooses a single uniform quantile rank
and an independent fair sign, fixed for the whole path; exact CDF
inversion supplies its legal 1-Lipschitz motion and sticky endpoints.

Exact full-width refinement preserves the continuous full-width CDF
used to prepare the nodes. It does not identify the new narrow-width
saved law with either that full-width CDF or the previous n256 narrow
law. The upper on a fixed full-width CDF's actual security is also not
a game-value upper. [The fixed-field refinement ceiling](FROZEN_FIELD_REFINEMENT_CEILING.md)
explains why changing only the mesh cannot close the remaining game gap.

The original n256 field, its original explicit strategy and its
front-two projected strategy are all preserved unchanged. Their complete
bank lower is `583091421641/409600000000`; the original half-mesh transfer
gives value lower `582291421641/409600000000`, and their saved narrow
law guarantee is `582289859141/409600000000`. Its original native and
BigInt reports remain valid. The separate B=1536 lattice construction
is another preserved, weaker lower certificate.

## 3. The physical Monster upper

`packages/interval_discovery_certificates/monster_boundary_n256.physical.json.gz`
contains a rational mixture of 770 physical path/calendar plans on 752
distinct reflected physical pairs. It was discovered in Actions run
43541622377, experiment `upper-boundary-256`, seed 577215. Every path is
legal, visits the center by time two, and reaches both endpoints within
the permitted horizon. Its calendars satisfy every causal prefix
inequality and have exactly the correct active mass.

The experiment completed one improving iteration, then stopped at the
next solve's LP budget. Its retained exact certificate is valid
independently of convergence or the unfinished LP. The former n=128
768-pair law and n=64 703-pair law remain preserved seeds and regressions.
The improvement over the n=128 upper is exactly
`1857712283/204800000000000`.

For each fixed symmetric center-by-two physical law, Princess ordering,
endpoint stopping and outward-after-two normalization preserve the
Princess supremum. A fixed admissible clock plane upper-bounds the actual
payoff of every normalized Princess. Maximizing this plane over `Qout`
thus gives a global upper for the supplied physical Monster law. This
law-specific argument is proved in
[the normalized-bank note](NORMALIZED_GRID_BANK_PRICING.md).

The resulting finite maximum-closure graph has 262,402 nodes and 558,630
arcs. Its supplied integral flow and source-side cut both have value
`265930716799554`. Exact capacity, conservation and cut checks prove the
maximum and hence

\[
V\le \frac{291849329389899}{204800000000000}.
\]

The [primal certificate documentation](../../packages/interval_clock_grid/QOUT_PRIMAL_CERTIFICATES.md)
gives the baseline, signed coefficients, scaling and closure construction.
The [retained discovery manifest](../../packages/interval_discovery_certificates/monster_boundary_n256_manifest.json)
binds the exact original CI bytes, seed, artifact ZIP, verifier sources
and replay. Its compressed and uncompressed SHA256 hashes are respectively
`80580dae8551c2838172d7f419861a3a9774793a8d039bdad087e21d24526f39`
and `5c736b0c6ef59b418cce0e2e2ef24b0a8dbe4d017a6eca7578d9e1c79616b31d`.
A separate Python implementation checks 2,301,592 causal-clock prefixes
and reconstructs the integer closure graph, flow and cut; the existing
Node implementation agrees. Both passed in
[run 43544245486](https://github.com/vltanh/lean4-monster-princess/actions/runs/43544245486),
and a subsequent local replay of the hash-bound retained packet agrees.
This certificate does not depend on a floating optimizer or on an upper
for a different physical law.

The endpoint-loop limit for this fixed physical law lies only
`11433/1024000000000000` below its certified upper. This is a diagnostic
of that law's response geometry, not a new unrestricted Princess lower.

## 4. Portable exact data and replay

The new lower package contains the field, explicit Princess law, both native
reports, independent BigInt report, extraction report, and a hash-bound
[manifest](../../packages/interval_discovery_certificates/princess_front_n512/manifest.json).
Its input stores 1,049,088 radial nodes as little-endian uint32 integers;
the decoded data occupies 4,196,352 bytes. Center and later outward values
are reconstructed exactly. The field SHA256 is

```
a4fe152dbf70f5896c256d3a329f6ac2ab31028421795ae74a3163b399c28e10
```

The saved explicit strategy SHA256 is

```
b7ac0c124dfcf6d3d00fbfaa6fbf2872e04878572d0f5221e7f7de0b05a257d7
```

The native discovery is [run 43545082756, artifact 14093139934](https://github.com/vltanh/lean4-monster-princess/actions/runs/43545082756/artifacts/14093139934).
The completed independent replay is [run 43546803161, artifact 14095016913](https://github.com/vltanh/lean4-monster-princess/actions/runs/43546803161/artifacts/14095016913).
Both downloaded archive digests and identical source members were verified.
The retained reports preserve the actual historical verifier source hashes;
a later provenance-only change is not substituted into their reports.

The strengthened cheap check also binds seven implementation sources and nine reviewed proof sources, retains the historical BigInt verifier bytes, reconstructs the archive members, and checks 262,144 front identities. It does not rerun the complete response search or certify the manuscript theorems in Lean.

From the repository root, the inexpensive retention check and a deliberately
requested complete replay are separate commands:

```sh
# Hashes, report bindings, exact fractions, nodal transport and strategy identity.
# This does not recompute the complete response search.
node packages/interval_discovery_certificates/princess_front_n512/check.cjs

# Complete independent bank search, followed by exact strategy comparison.
node --max-old-space-size=6000 packages/interval_center_pricing/verify_strategy.cjs \
  packages/interval_discovery_certificates/princess_front_n512/field.json \
  packages/interval_discovery_certificates/princess_front_n512/princess.json --progress 128

# Original native engine, independent of the center/front search reductions.
python packages/interval_clock_grid/normalized_native/verify_native_field.py \
  packages/interval_discovery_certificates/princess_front_n512/field.json

# Independent physical upper reconstruction and existing Node replay.
python packages/interval_discovery_certificates/verify_manifest.py \
  packages/interval_discovery_certificates/monster_boundary_n256_manifest.json
```

Do not repeat all large pricing commands during each floating discovery step.
The n256 source field, its weaker explicit law, and their original replays
remain at their existing paths for reproducibility.

## 5. What remains unsolved

The lower and upper do not meet. There is no proved equilibrium-sufficient
finite mesh, degree bound or physical support class, and no completed Lean
formalization. Increasing the grid remains an approximation hierarchy.

Two exact counterexamples prevent an unjustified shortcut: the
[narrow-width interpolation loss](SHARP_NARROW_INTERPOLATION_LOSS.md) can
approach the original half-mesh allowance, and even at full width a legal
`n=2` profile violates a universal quarter-mesh transfer by `1/3136`; see
[the full-width counterexample](FULL_WIDTH_TRANSFER_COUNTEREXAMPLE.md).
These do not disprove a sharper theorem for specially characterized
optimal profiles. They require any such characterization to be proved.

The current lower does not depend on the fixed-field finite-response
theorem. The [complete common-threshold response construction](COMMON_THRESHOLD_FIXED_CDF_RESPONSE.md)
now covers the formerly unresolved off-center spatial diagonals and supplies
a finite rational-quadratic exact response algorithm for each supplied
positive-width field. It has not been evaluated on the large discovery
field, and it does not bound the complexity of an optimal Princess law.
The [heavier-first rank-balance recurrence](CENTER_HEAVIER_FIRST_BALANCE.md)
further reduces the center search without supplying that outer optimization.


A further [frozen-field ceiling](FROZEN_FIELD_REFINEMENT_CEILING.md) proves
that every compatible exact refinement of the current full-width front-two
source has standard transferred lower at most
`14570592687/10240000000 = 1.42290944208984375`. The proof uses one exact
continuous Monster route and the monotone edge quadrature error. With the
current upper held fixed this leaves at least `0.0021361115717724609375`,
so refining that same field cannot deliver width below `1e-4`. This ceiling
is neither an upper bound on V nor a bound on the separate saved narrow-width
Princess law. New CDF geometry, a sharper justified certificate, or a
substantially improved physical Monster law is necessary.
