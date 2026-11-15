# Frozen physical rows for rational-germ exchange

The probability master has two distinct operations.

1. A pure response row is a fixed physical path \(p_\epsilon\), paired with its reflection. Its payoff against a fixed Monster is linear in the row probabilities.
2. A lower candidate may then use the comonotone law with the same time marginals. Its payoff must be computed with ordered rank records; it is not the raw weighted average of the pure-row scores.

Changing a subordinate realization of the same abstract labels creates a NEW row. It never replaces the physical row against which an earlier Monster attack was found.

## Exact unit-Monster scoring

Before first capture, the sign of \(p(t)-m(t)\) is fixed by continuity. If it is positive, only a right-moving unit Monster leg can close the gap; if it is negative, only a left-moving unit leg can close it. Legs moving the other way cannot reach equality.

A unit leg of direction \(d\in\{-1,1\}\) has constant characteristic
\[
q=t-d\,m(t).
\]
For the reflected princess \(\sigma p\), its first possible contact is the first inverse of
\[
t-d\sigma p(t)=q.
\]
Thus the same two first-inverse caches for p serve both reflections. The algorithm checks only the closing legs and includes equality at their endpoints. An initial coincidence returns time zero. Before a successful closing leg, the inverse cannot lie before the leg start; the implementation asserts this invariant.

Each first inverse is found by exact binary search in the monotone characteristic sequence, followed by affine interpolation on the selected physical segment. A stationary continuation after the last stored vertex is explicit. Constant paths and constant targets use rational arithmetic directly; all other geometry comparisons remain in \(\mathbb Q(\epsilon)\). The rational limit returned for probability optimization is separate from the full first-hit germ.

The API rejects nonunit Monster legs. Such routes require the general physical segment scorer rather than silently passing through this specialization.

## Normalized ordered-law constructor

The constructor accepts immutable physical row objects
\[
\{\,\text{id},\text{path},\text{weight},\text{provenance}\,\}.
\]
Weights are nonnegative constant rationals. Zero weights are omitted; positive weights are normalized exactly as pair probabilities. IDs and provenance are retained.

The returned raw-marginal representation contains the positive paths and their reflections, integer copy weights, and the total integer mass. Its strict and closed CDF ranks define the common-quantile law. A quantile evaluator and a lossless coordinate dictionary are included.

For any two times s,t, every raw coordinate moves by at most \(|t-s|\). Monotonicity of weighted order statistics therefore gives the same bound for every fixed quantile. The resulting ordered paths are legal. Their initial marginal, including all distinct initial germs and atoms, is unchanged.

The dictionary is a generator of these marginals. Interpreting it as an unordered path mixture would use a different coupling. Feed its prepared representation to the ordered record scorer or to CaptureSearch in sorted mode.

## API

Load the module and use one canonical germ arithmetic instance G:
\[
F=\texttt{createFrozenLawTools(G)}.
\]

- \(\texttt{preparePath(raw)}\) accepts serialized physical vertices or an existing path from the same G.
- \(\texttt{prepareMonster(raw)}\) accepts physical vertices, an exact-light atom, or the archived PATH parameter format.
- \(\texttt{pairScore(p,m)}\) returns both first-hit germs and their exact rational limiting mean; \(\texttt{fullCost:true}\) also returns the full mean germ.
- \(\texttt{orderedLaw(rows)}\) returns normalized metadata, prepared marginals, strict/closed ranks, quantiles, and a dictionary.

Serialize paths when moving between different arithmetic instances. Physical vertices stay fixed; only inverse caches grow. Retain the minimum eventual-sign radius over the entire cache lifetime. Resetting arithmetic statistics while reusing old inverse caches does not erase the earlier branch restrictions.

## Verification

The package verifier checks716 signed first contacts against the independent general segment-intersection scorer. The cases include rational speeds, initial ties, equal-limit distinct germs, opposite-turn histories, endpoint contacts, constant-path fast cases, and all supplied upper-germ geometries.

It additionally matches all318 signed component captures of the clipped159 law against its strongest M1 attack, and checks20 strict/closed quantile and normalized-dictionary identities. The existing frozen paths are unchanged after construction.

A separate agent independently replayed1,372 signed contacts with a separately written chronological segment intersection implementation, including both inward-M1 attacks and24 realized upper-germ profiles. These are correctness checks for the interface, not a minimax certificate.

```sh
node packages/interval_global_closure/verify_frozen_law_tools.mjs \
  packages/interval_global_closure/germ_v8_fixture_inputs.json \
  packages/interval_global_closure/germ_atomic_fixture_labels.json \
  frozen_tools_report.json \
  clipped159_dictionary.json clipped159_all_m1_verification.json \
  SHARED_HYDRATOR.cjs
```

The optional last three arguments enable the full frozen159 and ordering tests. The shared hydrator is blob1ba70ffcb1bd571675eae9894a7f7d325b304a87.
