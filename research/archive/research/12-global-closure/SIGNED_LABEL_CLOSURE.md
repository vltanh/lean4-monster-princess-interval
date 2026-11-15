# Signed unary rewards on ordered labels

This module is an exact maximum-closure backend. It is not, by itself, a physical response theorem: a caller must prove its label domain, strict-contact conventions, and interval-fill reduction.

## API

Load the existing `atomic_survival_v8.cjs` engine as `E`, then call
\[
S=\mathrm{createSignedLabelClosure}(E).
\]

`S.maximize({labels,rowBounds,unaryValues,mode:"exact",retainGraph:false})`
maximizes
\[
\sum_i f_i(k_i),\qquad
\ell_i\le k_i\le h_i,\qquad k_i\le k_{i+1}.
\]

- `labels` is the common ordered label list. Its entries are metadata; order is determined by array index.
- `rowBounds[i]=[lo,hi]` is inclusive.
- `unaryValues[i]` may have the full label-list length or only the original bounded length `hi-lo+1`.
- Every unary may have either sign and any shape. Rational strings are parsed using the engine's ordinary exact `Q` class. JavaScript number inputs denote their exact Float64 dyadic values.
- `mode:"exact"` is the default. It scales threshold weights to a common integer denominator and uses `E.BigFlow.BigFlow`.
- `mode:"float"` uses `E.Cut.Flow`; it reports the independently recomputed witness error and does not claim exact optimality.
- `retainGraph:true` additionally returns the residual graph and source/sink information in memory.

The output includes the value, exact rational scores of both returned label rows, and the componentwise smallest and largest optimal labels. An inconsistent ordered bound system returns `status:"infeasible"`.

The V8 factory can be loaded by replacing its single `module.exports=` with `return ` and evaluating the source as a function body.

## Reduction

First propagate lower bounds forward and upper bounds backward. These are exact order consequences. After propagation, both bound sequences are nondecreasing.

For each nonforced threshold, introduce
\[
b_{i,k}=1_{\{k_i\ge k\}},\qquad \ell_i<k\le h_i.
\]
Its unary weight is \(f_i(k)-f_i(k-1)\), with constant term \(\sum_i f_i(\ell_i)\). Add implications
\[
b_{i,k+1}\Longrightarrow b_{i,k},\qquad
b_{i,k}\Longrightarrow b_{i+1,k}
\]
whenever the destination is not already forced true.

A positive threshold weight is a source arc; a negative weight is a sink arc. Every implication gets capacity one integer unit larger than the sum of all finite absolute capacities. An implication-free cut is feasible, so a minimum cut never cuts an implication. This gives precisely the desired nondecreasing labels.

The exact value is the constant term plus all positive weights minus the minimum cut capacity. The source-reachable residual cut gives the smallest optimum, and the complement of the sink-reachable residual set gives the largest optimum. Both are independently rescored from the original unary tables. Exact mode also replays the returned cut capacity using the original integer capacities.

## Verification

`verify_signed_label_closure.cjs` passes 180 games against all 3,430 feasible exhaustive assignments. It checks:

- 288 exact value/encoding comparisons;
- 288 optimal-face extremum comparisons;
- 28 independent Float64 replays;
- 36 infeasible ordered-bound systems; and
- an entirely flat optimal face.

These tests cover arbitrary signed, nonconcave unary tables, forced ranges, rational denominators, and both full and bounded-row encodings. The algorithmic proof above supplies correctness beyond the fixtures.
