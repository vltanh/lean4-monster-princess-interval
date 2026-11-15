# Continuation checkpoint: exact global response and whole-region constraints

The exact unrestricted interval game remains open. This checkpoint does
not change the established rigorous value interval and does not assert
a saddle point. Its purpose is to replace sampled response checks with
global response formulas and exact geometric constraints.

## Completed mathematical components

1. A finite symmetric unit-leg monster law has an unrestricted princess
   response supremum given by one finite lexicographic survival cut.
   Arbitrary princess starts, speeds, turns, and completion times are
   included. The full optimal residual face is retained. This theorem
   is for a supplied law; it does not identify the optimal law.

2. The frozen endpoint_joint_i1 field fails both signed fixed-U=1 M2
   families and an early two-turn family. Exact continuous-start
   minimization and independent physical capture integration locate
   those failures. The original endpoint reference is not a lower
   guarantee for that field.

3. On the existing affine geometry, whole M1/M2 and early-M3 response
   cells have exact quadratic descriptions with coefficients affine in
   the CDF values. Tetrahedral nonnegativity has an exact order-four
   copositive/semidefinite representation. The finite geometry is
   constructed once; it does not refine a response sampling grid.

4. General initial inward/outward routes have a free-second-turn
   formula with two explicit rank cutoffs. Their center-first-turn
   face has a different capture identity, including both reflected
   center masses. Both identities agree with exact physical capture
   checks, including endpoint second turns and turns after U=1.

5. Before the first center visit, a record Bellman envelope reduces
   unrestricted speed/turn verification to an outward inequality and
   explicit boundary continuations. The corrected derivative includes
   a moving-rank flux missed by pointwise inverse differentiation.
   The entire remaining region has not been certified.

## Executed checks

The independent exact BigInt implementation in
packages/interval_cdf_discovery/exact_response_audit.mjs reproduced:

- 119 fixed-U=1 quadratic regions and 238 independent physical comparisons;
- 12 early-M3 source identities, 112 tetrahedral quadratic identities,
  and 224 independent capture/lift comparisons;
- 9 simplex fixtures including singular and nonconvex quadratics;
- 120 general-I physical comparisons and 24 exact cutoff minimizations;
- 35 center-first-turn physical comparisons and 7 fixed-second-one lifts.

The separate exact geometry verifier covers 39,304 negative early-M3
tetrahedra, 117,912 positive early-M3 tetrahedra, 3,468 triangles for each
positive M1/M2 family, 34 intervals for each negative M1/M2 family, and
1,156 center-first/fixed-second-one triangles. It checks the complete
projected triangle containment, primitive knot intervals, and total
volumes. This verifies the decomposition, not payoff nonnegativity.

The Python survival-cut verifier completed its 1,335 nonlex checks before
the outage. Its expanded lex run was interrupted. A separate V8 port has
checked small dyadic lex instances and is being used for discovery;
numerical cut/LP solves are not rational game certificates.

## Reconstruction status

The original executor disconnected during this continuation. The exact
V8 computations above were run independently against the committed field
blob 5c45d042ee9948faebc03354c3e1e2ee3cbec1a5.

Several Python files and manuscripts in this checkpoint were reconstructed
from the reviewed source/formulas. They are not claimed to be byte-identical
copies of the inaccessible working tree. The reconstructed Python files
were not executed during the outage. Their mathematical computations were
checked in V8 where explicitly reported.

The earlier 13,092 Bellman-moment and 3,396 outward-preservation fixture
counts refer to completed pre-outage runs. Their original verifier source
files were not recovered in this checkpoint. The full analytic notes are
preserved, as is the independently reconstructed exact flux witness.
No claim is made that every uncommitted pre-outage file has been backed up.

No Lean compilation or CI was run.

## Work still needed for closure

A complete proof must supply the same exact constant and matching
unrestricted upper and lower strategies. The remaining tasks are to
construct a normalized global upper law, construct a field satisfying
all initial and continuation inequalities, prove the remaining Bellman
regions and boundary gates, and establish equality of the two guarantees.
Neither a finite-support numerical optimum nor exact verification of
the response formulas alone closes the game.
