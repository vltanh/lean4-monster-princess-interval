> This folder holds only the files that the bounds in [`research/`](../../README.md) need. The description below is the original one; files it mentions that are not here are in [the archive](../../archive/packages/interval_center_pricing).

# Exact center compression for complete response pricing

This package accelerates the complete normalized integer Monster-response
bank for a supplied legal Qout CDF. It does not restrict the Princess
geometry, change the physical bank minimum, or reduce the continuum
transfer error. The unchanged native and BigInt implementations remain
independent references.

The [proof](../../archive/research/12-global-closure/DISCRETE_CENTER_BALANCE_PRICING.md)
uses maximal returning triangles, attack of a heavier surviving record,
and the balance condition at a returned peak. Each guard is applied after
charging the current center or peak sample. Before the first center visit,
all original unit directions are retained. Endpoint resets and both legal
time-two tours are unchanged. Non-Qout fields are rejected.

There is an important dominance issue: componentwise smaller records need
not permit the same balance-guarded path. The proof instead establishes
monotonicity of each phase's *value*. An unbalanced outward return can be
merged with the optimal next same-side excursion without changing its
fixed past. This justifies Pareto pruning within a phase; inward and
outward states must have separate frontiers.

`price_center.cpp` has five policies:

| Policy | Exact search |
|---|---|
| 0 | Original unrestricted normalized branching, as a control |
| 1 | Center triangles and heavier-side orientation |
| 2 | Also require balance before an inward return; supports witnesses |
| 3 | Also sum the deterministic inward return in one step; minimum only |
| 4 | Also use the incoming-front terminal guard, after checking all front-two identities |

Policies 3 and 4 schedule the destination center with its exact accumulated
integer cost. If time two comes first, it uses the original two endpoint
tails there. It requires witness count zero, because its scheduled states
do not retain a packed path prefix. Policy 2 has the original input/output
interface and can return physical violating routes for discovery.

```bash
python3 packages/interval_center_pricing/test_center_pricing.py /tmp/center-regression.json
python3 packages/interval_center_pricing/verify.py packages/interval_clock_grid/lower_n256_field.json --output /tmp/center-retained-replay.json
g++ -O3 -std=c++17 packages/interval_center_pricing/price_center.cpp -o /tmp/price_center
# Input is the existing little-endian integer pricing format.
/tmp/price_center /tmp/pricing.input.bin 0 3
```

The regression compares 91 exact legal fields against the unchanged native
oracle under all four policies. Its small cases independently enumerate
14,724 physical paths with Fraction arithmetic, and it chronologically
replays 765 returned routes. It also checks rejection of a field outside
the Qout hypotheses. These are implementation checks; the universal
equivalence uses the proof above.

On the rejected coarse-search candidate refined to n=256, all policies
returned exactly 582942762027/409600000000. The unchanged native run took
47.2 seconds locally; policy 2 took 23.8 seconds and policy 3 took 9.5
seconds. Policy 3 retained 62,616,982 states, including 48,185,851 before
the center. This diagnostic is a performance measurement, not a new game
bound. It identifies the still-unrestricted precenter phase as the next
dominant cost.

The incoming-front theorem permits policy 4 to finish a postcenter state
as soon as `j+abs(k)>=4*n`. Both endpoint tours scan the front node before
charging, including a new record at that first contact. The additional
regression projects all 91 fields and compares this policy with the
unchanged full oracle; 29,448 independently enumerated Fraction paths now
cover the source and projected cases together. On the retained projected
n256 field the exact minimum stays unchanged; policy 4 retains 43,195,355
states and took 9.7 seconds locally including compilation/decoding.

`refine.py` prepares a finer field without assembling an LP. It uses the
exact integer common-threshold interpolation weights. If the resulting
denominator fits uint32, every refined nodal value is preserved exactly;
otherwise it explicitly floors legal values at the selected denominator.
The compact input is independently decoded before pricing. `--classic`
also replays the unchanged full native engine on the identical binary.

```bash
python3 packages/interval_center_pricing/refine.py --source packages/interval_global_closure/lower_n256_front2_field.json --n 512 --policy 4 --classic --output /tmp/front-refinement
```

The native minimum proves the finite-bank value only. Apply the existing
1/(2n) transfer explicitly for a game-value lower. A security claim for a
particular continuous Princess CDF requires its separate extraction or
continuous-response theorem. No Lean kernel certification is claimed.

## Proved affine-cell transitions, not yet enabled

[DISCRETE_AFFINE_CELL_TWO_RUNS.md](../../archive/research/12-global-closure/DISCRETE_AFFINE_CELL_TWO_RUNS.md)
proves that, between fixed fine-grid entry and exit nodes in one legal
affine coordinate box, the complete discrete left-clock cost is minimized
by one of the two corner orders. The proof includes the whole concave
physical continuation and deliberately allows the two exit records to
change. Exact ceiling-level sums handle partial record crossings; no
continuous quadrature approximation is used.

This permits a future implementation to enumerate both corner orders for
each fine exit-edge node, retaining states at coarse affine-cell
boundaries. It does not justify resetting a remembered run at an arbitrary
shared edge, crossing a spatial kink, leaving the arena, or erasing a
required center visit. Macro transitions with explicit entry and exit
nodes are the intended safe formulation. Precenter boxes should lie
entirely in one open spatial half, or a new center contact must be
processed explicitly. No current pricing policy uses this additional
reduction.

```bash
python3 packages/interval_center_pricing/test_affine_cell.py
```

The Fraction regression checks 2,264 independently summed ceiling-area
identities, 1,132 explicit three-run mixture certificates, and all 4,952
words in its small complete banks. Their two corner triples admit a
rational mixture with at least the original captured area and both exit
extents, which tests every concave nonincreasing continuation on those
fixtures. Additional nonlinear continuation checks exercise the Jensen
step directly. The universal result is the linked proof.

Section 7 of the [center proof](../../archive/research/12-global-closure/DISCRETE_CENTER_BALANCE_PRICING.md)
also gives the exact earlier-front projection inequality
`v(Gamma_c g)>=min(v(g),(c+1)/2)` for aligned `1<=c<=2`, with a conditional
late-center search guard. That extension is distinct from policy 4's
currently implemented front-two guard; the README does not claim an
earlier-front computation has run.

## Independent compact BigInt replay

`verify_bigint.cjs` independently decodes and validates the compact nodal
field, checks the transport and sticky endpoint inequalities, and performs
target-bound response pricing with BigInt accumulated costs and pursuit
sums. It constructs neither the full event table nor the original large
discount map. Precenter directions remain unrestricted; after the center
it uses the proved heavier-side, balanced-return, and deterministic-return
normal forms. Exact front-two identities enable the additional terminal
guard automatically. A report establishes a lower target, without claiming
that its pruning search found an attaining path or the exact minimum.

```bash
python3 packages/interval_center_pricing/test_refinement.py
python3 packages/interval_center_pricing/test_bigint.py
node --max-old-space-size=6000 packages/interval_center_pricing/verify_bigint.cjs FIELD.json --progress 128 > independent.replay.json
node packages/interval_center_pricing/test_strategy.cjs
node --max-old-space-size=6000 packages/interval_center_pricing/verify_strategy.cjs FIELD.json PRINCESS.json --progress 128 > strategy.replay.json
```

The independent regression compares 30 fields with the unchanged native
engine and rejects each claimed minimum plus one integer unit. Eighteen
cases also agree with the original BigInt implementation; 4,908 small-grid
paths are independently summed with Fraction arithmetic. Disabling Pareto,
pursuit, and front pruning provides additional exact controls. Malformed
field hashes, cone violations, sticky-boundary violations, and an invalid
forced front are rejected.

The separate `compact-fine-replay.yml` workflow binds a previously completed
native discovery artifact by exact source and field hashes, independently
replays its lower target, and then uses the existing extractor to construct
a new explicit Princess law. It does not infer unrestricted security from a
continuous attack screen. Fine-field promotion requires the observed replay
result, not merely the presence of this workflow.

`verify_strategy.cjs` combines one compact BigInt target replay with the
unchanged `extract_normalized_princess.cjs` generator and exact strategy
comparison. This checks the saved explicit law without a second bank
search. Its report distinguishes the finite-bank lower, the transfer loss
including the selected positive interpolation width, and that fixed law's
all-Monster guarantee. It snapshots the executing verifier and extractor
source hashes before the search. Corruptions of the guarantee, source,
target, quantile rule, or interpolation width are rejected by the retained
integration regression.

### Proof obligations in the compact replay

| Code component | Mathematical or arithmetic obligation |
|---|---|
| `decode` | The compact row index matches nodal parity; range, both transport directions, and sticky endpoint traces are checked. Post-two values are the format's explicit outward extension. Front termination is enabled only after all front identities pass. |
| `key`, `pair`, record IDs | Prices up to `2D` are exactly representable Numbers because `D<2^32`. Sorted IDs preserve every price comparison. Numeric composite keys are used only within the safe-integer bound; otherwise distinct integer tuples are stored as strings. Costs, pursuit sums, targets, and rational numerators use BigInt. |
| Ordinary and pending layers | Every ordinary nonzero postcenter state is outward: inward paths jump directly to the center or terminal time. Hence the key cannot merge inward and outward phases. Every nonterminal pending state has position zero, so its time-local pair key is sufficient. |
| `pareto` | Dominance uses the proved monotonicity of the center or outward **value**, including the balanced-return phase lemma. It does not assume that the same guarded future is admissible from smaller records. |
| `lower` | Each endpoint clock independently pursues its own endpoint. The remaining endpoint-tour costs are affine in the reachable position, so their minima occur at the appropriate two interval extremes. A branch is discarded only when this valid lower already reaches the target. The target need not be an attained incumbent. |
| `terminal` | An actual endpoint deactivates its own clock and prices the other by direct pursuit. At time two or a verified postcenter front, both records are updated at the current node before the two exact linear endpoint-tour costs are evaluated. |
| Exhaustion and output | All nonnegative initial grid positions are included and reflection supplies the others. No beam, resource cutoff, or partial-search success exit exists. The output is a bank lower target; subtracting `2D` in denominator `4nD` applies the established `1/(2n)` transfer. Exact-minimum and fixed-CDF security claims require their separate certificates. |

The current CLI reads its verifier-source hash when producing the final
report. Its source must remain unchanged during a local replay; the CI
workflow uses an immutable checkout. An optional `attainment_checked`
flag records equality encountered during complete-path checks, but lower
verification does not require that flag because valid target pruning can
remove every attaining branch before a terminal check.
