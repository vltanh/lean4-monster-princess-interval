# Joint free CDF field and moving atoms: implementation design

Status: design recorded after the execution environment became unavailable on
2026-11-11. It is not a completed solver, a tested implementation, or a new
strategy certificate. A local draft named
`continuum_atomic_separator.mjs` had been written, but its bytes and the outcome
of its first fixture test were not recoverable in the remaining tool context.
This document is newly written from the mathematical design; it is not a
reconstruction of the lost source.

## Purpose and scope

The completed continuum search varies a whole continuous, symmetric CDF field,
with a possible center atom and endpoint absorption by a chosen horizon. The
global upper response supplies legal Princess paths with moving interior atoms.
Varying the full field jointly with the weights of those paths is a coherent
enlargement of the Princess strategy class. Mixing a fixed field with these
paths, which previously put zero weight on all added columns, does not settle
this enlarged problem.

Every candidate produced by the proposed finite route master remains a
candidate. A minimum over a configured Monster bank is not an unrestricted
lower guarantee. Neither the prior field search nor this design closes G5.

## The law and its legality

Let R be the radial CDF field used by `ExtendedFieldMesh`, and let its symmetric
probability law have CDF F_R. Let p_j be actual legal paths, retained with their
exact rational vertices. Use their fair reflection pairs. For nonnegative
masses m_0,w_1,...,w_k summing to one, define

    F(t,x) = m_0 F_R(t,x)
             + sum_j w_j [1{p_j(t)<=x}+1{-p_j(t)<=x}]/2.

The strict CDF F^-(t,x) uses strict inequalities in all atomic terms and the
strict CDF of the field. This is an aggregate marginal CDF. The Princess
strategy is the common-quantile coupling of these marginals, not a random
choice between the original path components.

Each component satisfies the speed-one transport inequalities between times.
Convex mixtures preserve those inequalities, so common quantiles admit
speed-one paths. The aggregate quantile law is therefore legal. This remains
true with moving interior atoms, center atoms, endpoint atoms, and crossings
between the original path columns.

For a continuous Monster path m, define

    A(t) = inf_{0<=s<=t} F^-(s,m(s)),
    B(t) = sup_{0<=s<=t} F(s,m(s)).

Up to rank endpoints of measure zero, the surviving quantiles are
(0,A(t)) union (B(t),1). Hence the expected first capture time is

    J_m(F) = integral_0^infinity [A(t)+1-B(t)] dt.

If the Monster has visited both distinct endpoints by T, all legal Princess
paths have been captured by T and the integral stops at T. These formulas
handle contact atoms through the separate strict and closed CDFs. Marginals
must be aggregated before either running record is taken.

## Linear joint variables

Use scaled field values y_i=m_0 R_i. The variable vector is

    z=(y_0,...,y_{N-1},m_0,w_1,...,w_k).

The radial field is piecewise affine on the existing characteristic mesh.
All legality constraints are linear in z:

- the same homogeneous directional inequalities y_U>=0 and y_V<=0;
- 0<=y_i<=m_0;
- y=0 on the existing origin and terminal radial faces;
- y=m_0 at the initial endpoint;
- m_0+sum_j w_j=1 and all masses nonnegative.

The last equality can be represented by two inequalities with right sides
1 and -1. The current persistent FieldMaster needs an explicit structural RHS
argument rather than assuming every structural inequality has right side zero.

Every strict or closed CDF evaluation is a sparse linear form in z. For
example, away from the center and endpoints, the field contribution is
m_0/2 plus or minus half of a barycentric interpolation of y. Each atomic
contribution has coefficient 0, 1/2, or 1 on its path-pair weight. At the center,
use the appropriate two CDF sides of the field, and at the endpoints include
the actual field and path atoms rather than replacing both sides by 0 or 1.

## Concavity and master cuts

For a fixed complete Monster path, infima of linear CDF forms are concave and
negative suprema of linear CDF forms are concave. Consequently J_m(z) is a
concave, positively homogeneous function on the nonnegative cone of legal
scaled marginal laws. On the probability section, the finite-bank optimization

    maximize c subject to c<=J_m(z) for every configured m

is a convex optimization problem.

At an evaluated point z*, choose active forms for the running minimum and
maximum, splitting integration intervals wherever the active record changes.
Integrating their coefficients gives a supergradient g_m such that

    J_m(z) <= J_m(z*) + g_m . (z-z*).

Positive homogeneity gives J_m(z*)=g_m.z* for a consistently chosen active
supergradient. Thus the linear master cut is c<=g_m.z. Retain the affine
intercept explicitly in floating arithmetic and verify it is numerically
consistent; do not silently turn floating error into an exact certificate.

The baseline integral over a complete route ending at T is
T*(m_0+sum w_j). The remaining contributions come from the two CDF records.
There is no extra baseline coefficient on the scaled field nodes.

## Exact route arrangement

Construct each Monster route from exact light coordinates or original exact
physical vertices. For (u,v), use t=(u+v)/2 and x=(u-v)/2. Never independently
round physical turn times and positions: shared contact alignments can change
the global response discontinuously.

For each Monster leg, take the exact union of:

1. its endpoints and any center crossing;
2. crossings of all field triangle boundaries and the field absorption face;
3. all relevant path-column vertex times;
4. all intersections with p_j and -p_j, including endpoints and intervals of
   coincidence.

On each open cell, the field CDF is affine in time and each atomic comparison
is constant unless paths coincide. Preserve four distinct pieces of
information: strict and closed values at the cell endpoints, and the incoming
and outgoing open-cell traces. An isolated contact can change a running record
permanently, even though it has zero integration length. Endpoint-only
evaluation, or treating a tiny positive-duration connector as zero duration,
can therefore give the wrong answer.

The lost draft used exact rational geometry and sampled the open affine trace
at the one-third and two-third interior points. Those samples determine its
linear coefficient forms without conflating an endpoint contact with an open
trace. The arrangement is independent of the optimized weights, but record
switching times within the arrangement depend on those weights.

For floating optimization, store each linear form as sparse index/coefficient
pairs and intern repeated forms. Store route cells using form IDs and
durations, rather than a dense array with one entry per field node. A hash
collision must be checked by comparing the full packed sparse form.

For exact replay, rationalize a complete legal candidate and evaluate the
same route using rational record comparisons and rational switching times.
The exact scorer should be implemented independently enough to catch a
contact-side error in the floating separator.

The exported path columns can move after the field horizon and can finish at
stationary interior points such as 1-epsilon. Consequently the existing
endpoint-absorbed terminal Bellman formula cannot automatically be used for
the hybrid law. One coherent construction is to append an explicit legal
endpoint-completion leg to every column and declare a common later absorption
horizon. This creates a new, fully specified legal candidate and requires
rescoring; no payoff is transferred merely because the appended displacement
is small. Alternatively, a hybrid global response oracle must explicitly
handle its surviving stationary interior atoms.

If a hybrid law is absorbed at the endpoints by a common horizon H, an optimal
Monster response can be chosen to finish visiting both endpoints by H+4:
after H only the two endpoint targets remain, and replacing its eventual
endpoint itinerary by the earliest such itinerary cannot delay capture.
A common-quantile N-point midpoint discretization then has uniform CDF error
at most 1/(2N), so the expected capture payoff differs by at most (H+4)/N,
uniformly over this complete response class. This gives a rigorous route from
an exact finite-quantile response to a continuous-law lower estimate, although
the required rank count may be computationally impractical. It does not
justify replacing the hybrid endpoint geometry by the old field horizon.

## Stable optimization

The existing retained-model whole-field search successfully preserves the
complete route pool, all cuts, and the LP basis. A later simplex vertex,
however, exhibited a poor new global attack. Preserve the best exactly legal
field after rescoring it on every newly added route.

For the joint problem, use a persistent level projection rather than repeatedly
selecting an arbitrary vertex of the master optimum. If U is the finite-master
upper estimate and L is the current bank minimum, a proposed level is

    ell = L + theta*(U-L), with 0<theta<1.

Minimize a weighted L1 distance from the incumbent subject to all current cuts,
the physical constraints, and c>=ell. This is a secondary LP; its added
absolute-value variables and changed level RHS can retain their own basis.
Keep U from the primary master. Do not report the level-projection objective
as a bound on the game.

Rationalize the masses while keeping their sum exactly one. If m_0>0,
normalize R_i=y_i/m_0, enforce the fixed faces and repair the field transport
inequalities as in the existing exact field pipeline. Then rescale y_i.
If m_0=0, the unused field can be any fixed legal field. Record the size of
all repairs and recompute route payoffs afterward.

## Route pools and reporting

The latest proposed common Monster bank was
`efficient_joint_bank.json`: 3,058 distinct fair reflection pairs with exact
vertices in `atoms[].exact_light`. It contained the prior union, the complete
density-128 bank, and the semantically reconstructed H3 support. This file was
local at the environment interruption; durable availability must be checked.

Add native-family and exact physical-DP attacks, including all distinct prefix
completions, without treating them as part of the common-bank comparison.
Report separately:

- the achieved minimum on the 3,058 common rows;
- the minimum over all additional configured routes;
- the best actual Monster response found by a declared global search;
- the current finite-master upper estimate for the chosen Princess class.

The final frozen H5 field's adaptive native-node audit found an actual attack
of approximately 1.421488834258294, below its saved configured-bank score.
The report was named `continuous_response_grid_h5_08_adaptive.json`, with
source field SHA256
`fe6329176f03f76be08e97b22e8cb9beab0b01a8cfdb327e431511a2234b1c68`.
These exact attacks should be imported before any continuation. Availability
of the local report must be verified after the environment returns.

## Required first tests

No result of the draft's first fixture test was recovered. Before using a
rebuilt implementation:

1. On a small legal field, set m_0=1 and all w_j=0. Compare every route payoff
   against ExtendedExactField, including positive and negative starts, center
   waits, endpoint atoms, and horizons beyond two.
2. Set m_0=0 and give one path pair full mass. Compare the quantile law against
   direct exact first intersections of the ordered reflected pair. For several
   crossing path columns, compare against an independently extracted ordered
   quantile family; raw path-mixture capture times are not an equivalent test.
3. Check g.z=J(z) and the global supergradient inequality on many feasible
   pairs of joint laws, including zero masses and ties between active records.
4. Include a Monster/Princess coincidence interval, an isolated tangency,
   an incoming endpoint contact, a center atom, and a sub-double positive
   connector interval. Compute all geometry rationally.
5. Recompute the worst floating routes using the independent exact scorer after
   every output repair, and validate all actual path-column speeds and ranges.
6. Check that checkpoint/restart preserves all existing cuts, all route
   identities, both LP models' bases where applicable, and incumbent scores.

These tests would make the proposed implementation reviewable. They would not
by themselves establish an unrestricted saddle point.
