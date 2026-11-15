# Independent exact replay of a projected physical upper

`verify_projected_upper.py` verifies a result emitted by the discovery helper
`solve_projected_upper.cjs`. It uses only the Python standard library. The numerical
optimizer, JavaScript response engine, saved model geometry, and formal
Princess labels are not imported or trusted by the replay.

A successful replay proves an all-Princess upper bound for the supplied
fair-reflected canonical one-turn Monster law. It does not establish a
Princess lower bound, an equilibrium, or a comparison with a benchmark unless
the resulting exact upper actually makes that comparison.

## Reproduction

The retained 375-pair law can be rebuilt without numerical discovery:

```sh
python3 packages/interval_one_turn/rebuild_projected_upper.py --output /tmp/one-turn-projected
```

The law and executed replay are packaged as `one_turn_projected_upper.json.gz`
and `one_turn_projected_upper_replay.json`. From the repository root, pass
the generated or another complete projected result JSON:

```sh
python3 packages/interval_one_turn/verify_projected_upper.py \
  path/to/projected_result.json --output projected_python_replay.json
```

A gzip-compressed input ending in `.gz` is also accepted. The replay reports
the exact rational upper, physical class masses, independently reconstructed
graph sizes, integer flow and cut values, and the input file's SHA-256 hash.
No optimization is performed. The input contains the physical law and the
finite flow witness needed for the replay.

To require a counterexample to the frozen strict-separation target, add the
explicit comparison gate:

```sh
python3 packages/interval_one_turn/verify_projected_upper.py \
  path/to/projected_result.json --require-counterexample
```

This command fails unless the independently verified exact upper is at most
`291849329389899/204800000000000`. Every ordinary replay also reports the
signed exact difference `upper - frozen_benchmark`; a passing upper-certificate
replay alone does not imply that this additional comparison gate passes.

Run the embedded independent fixtures and corruption checks with:

```sh
python3 packages/interval_one_turn/verify_projected_upper.py --self-test
```

The self-tests include exact uppers `3/2`, `5/2`, and `41/15`, coordinates with
LCM scale 15, both signs of auxiliary reward clauses, zero-probability rows,
and an explicitly irrelevant continuation after a complete endpoint sweep.
They reject 17 corrupted certificates. A deliberately omitted sound order
edge is accepted: completeness of the projected implication graph is not
needed for the upper direction.

## 1. Physical law and canonical membership

The trusted candidate data are the rational `atoms[].exact_light` vertices
and integer `weight_numerator` values, interpreted with the common positive
`weights_denominator`. Every atom represents its listed path and its spatial
reflection with equal probabilities.

At a light-coordinate vertex `[U,V]`, physical time and position are
`t=(U+V)/2` and `x=(U-V)/2`. The verifier independently requires:

- nonnegative integer weights with exactly the stated total;
- time-zero starts and positions in `[-1,1]`;
- strictly positive-duration unit-speed legs, so exactly one of `U,V`
  increases on each leg;
- visits to both endpoints;
- at most one interior direction reversal before the first endpoint;
- a direct unit-speed sweep from the first endpoint to the opposite endpoint.

If further unit-speed arena legs are supplied after that complete sweep, the
report explicitly counts them as irrelevant continuation. This is justified
pathwise: at the first endpoint the Monster is on one side of every Princess,
and at the opposite endpoint it is on the other side, so every continuous
Princess was captured during that sweep. The canonical representative stops
at its second endpoint. The extra supplied vertices are still retained when
reconstructing the response graph, so no unexplained change of certificate
indices is made.

The canonical class and its endpoint conventions are proved in
[the complete-domain note](../../research/13-equilibrium-geometry/ONE_TURN_COMPLETE_DOMAIN.md).

## 2. Independent integer geometry and survival rewards

The verifier takes the LCM `S` of all rational light-coordinate denominators
and does the complete reconstruction in integer coordinates. This is not a
dyadic-grid restriction. All query coordinates, base levels, triple contact
labels, physical label bounds, and unprojected threshold indices are rebuilt
from the physical paths and their reflections.

In scaled coordinates, the radial inverse curve obeys

\[
 \max(V,0)\le U\le V+2S,
\]

with monotone query labels. Each base level has a below, equal, and above
contact label. The strict and closed comparisons therefore remain distinct;
initial contacts are not replaced by limits from nearby starts.

For each oriented physical leg the verifier reconstructs its survival
integral as a sum of nonnegative exact lengths times clauses of one sign:
either all specified thresholds are true, or all are false. Forced physical
thresholds and redundant ordered literals are eliminated independently.
Identical clauses are combined and multiplied by the exact atom weights.

The supplied `geometry`, `defs`, `units`, `labels`, and floating-point `value`
are unused. Only independently computed integer coefficients enter the bound.
The mathematical basis is the existing finite-event inverse-curve response
theorem, as used by the repository's
[full ordered-CDF upper construction](../../research/12-global-closure/FULL_ORDER_CDF_UPPER_CERTIFICATE.md).
The present replay independently certifies its finite algebraic calculation;
it does not claim a new Lean formalization of that theorem.

## 3. Projection is checked as an upper relaxation

The supplied `projection.projection.old_nodes` is used only as a selection and
ordering of independently reconstructed threshold indices. Its indices must
be valid and distinct, and it must include every threshold occurring in any
physical reward clause.

For a threshold `B(i,k)=[label(i)>=k]`, an implication

\[
 B(i,k)\Longrightarrow B(j,l)
\]

is checked using the sufficient exact conditions `i<=j` and `k>=l`. Every
supplied hard edge must meet these conditions. Consequently all physical
inverse profiles satisfy the projected constraints. Missing valid implications
can only enlarge the feasible set and weaken the upper bound. No claimed
projection-completeness theorem, saved projected closure, or supplied row
threshold table is needed.

For a positive clause, a positive-weight auxiliary is constrained to imply
each literal; maximization realizes their conjunction. For an all-false
clause, the verifier writes its reward as a constant minus a negative-weight
auxiliary and requires each literal to imply that auxiliary. This realizes
one minus their disjunction. Empty and single-literal clauses are handled
directly.

## 4. Capacities and the exact witness

Let `C` be the reconstructed constant and `l_i` the signed linear coefficients.
The reconstructed graph has source arcs of capacity `l_i` for positive
coefficients, sink arcs of capacity `-l_i` for negative coefficients, and hard
arcs of capacity

\[
 I=1+\sum_i|l_i|.
\]

Every supplied arc and capacity must agree exactly with this separate
reconstruction. The verifier then checks each positive flow entry, duplicate
indices, capacity constraints, all node balances, source and sink totals, the
cut's terminal separation, and exact flow/cut equality.

Write `P=sum(max(l_i,0))` and let `F` be the certified integer flow. The exact
all-Princess upper is

\[
 \boxed{\frac{C+P-F}{4SW}},
\]

where `W` is the weight denominator. One factor two converts light length to
physical time; the other averages the two reflected Monster orientations.
The stated `exact_value` must equal this fraction exactly.

The upper remains valid without an actual Princess attaining the cut value.
In particular, equality of a formal-label row with the cut is not treated as
an actual finite-width Princess witness.

## 5. Retained certificate and independent replays

The packaged 375-pair law reconstructs 112,604 nodes and 328,157 arcs and gives
exactly `478205958821456999/335544320000000000`, approximately
`1.4251648152514012`. Its excess over the frozen benchmark is exactly
`200087745232387/1677721600000000000`. See the
[physical theorem](../../research/13-equilibrium-geometry/ONE_TURN_PROJECTED_PHYSICAL_UPPER.md)
for its class masses and integer flow totals.

Two additional workspace discovery outputs were independently replayed during
development. These filenames describe executed checks, not additional
packaged artifacts:

| Input | Reflected pairs | Rebuilt nodes | Rebuilt arcs | Exact upper |
|---|---:|---:|---:|---|
| `exact_physical_replay.json` | 326 | 77,304 | 226,379 | `364877772791201/256000000000000` |
| `union_quantized_exact.json` | 281 | 25,213 | 73,954 | `1462049715738029/1024000000000000` |

All three uppers remain above the benchmark. The independent reconstruction
closes a certification dependency; it does not close the one-turn comparison.
