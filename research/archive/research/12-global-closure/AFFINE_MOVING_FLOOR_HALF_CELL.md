# Affine moving-floor half-cell: four directional legs

Research proof independently reviewed by both the audit and verification agents,
2026-11-14.

Consider the affine scalar field

\[
 Y(t,x)=at+bx,\qquad b\ge a\ge0,
\]

on the half-plane `x>=0`, with fixed physical entry and exit states and
times. The application here is an interior half of a merged light square;
the entry/exit coordinate box intersected with `x>=0` must stay within the
physical arena. The scalar theorem also applies to an affine physical
boundary half-cell under this same containment condition; actual endpoint
resets are then accounted for separately in the global corollary.

**Claim.** Every admissible segment is weakly dominated for integrated
captured record range by one with the same physical endpoints, duration,
and both exit scalar records, with at most four unit-speed directional legs
and one final constant-`Y` leg. The latter has physical velocity `-a/b`.

This is the half-cell whose scalar state constraint is a moving lower
bound `Y>=at`. It does not assert the corresponding result for the moving
upper bound `Y<=at`.

## 1. Acceleration preserves this half-plane

First take `b>a`, write

\[
 \alpha=b+a,\qquad \beta=b-a,\qquad
 \kappa=\frac1\alpha+\frac1\beta,
\]

and subtract the initial scalar value `s=bx(0)` from `Y`. The scalar path
starts at zero, ends at a fixed value `f`, and has rates in
`[-beta,alpha]`. Its physical constraint is

\[
 s+Y(t)\ge at.
 \tag{1}
\]

Use the first-visit normalization from
`FOUR_LEG_AFFINE_RECORD_RESPONSE.md`: accelerate monotone travel to its
maximum scalar rate, remove reversals at old record levels, then visit
the two global new records directly in their original order and travel
directly to `f`. Put unused time in a final constant-scalar hold.

Every retained record event occurs no later than the corresponding old
first visit. If a scalar value `y` was feasible at an old time `t`, it is
feasible at every earlier time because `a>=0`. Hence each accelerated turn
vertex satisfies (1). Physical position is affine on each maximal-speed
leg, so feasibility at the vertices implies feasibility throughout it.

The final direct scalar trip reaches `f` by some time `t_f<=T`. Its final
constant-scalar hold has physical position `(s+f-at)/b`, which is
nonincreasing and ends at the prescribed nonnegative physical endpoint.
It also stays in the half-plane. Thus the acceleration and hold
normalization is valid here, not merely in the unrestricted scalar line.

## 2. The global minimum is the only new half-plane inequality

Assume both exit records are new, so the normalized tour visits scalar
levels `-B` and `H`. List its genuinely partial record-turn magnitudes,
before the two global records, as `z_1,...,z_m`.

Every partial lower turn has scalar level at least `-B` and occurs before
the first visit to `-B`. Therefore, if the global-minimum event satisfies
(1), every partial lower turn does too. All physical local minima before
the final hold are these lower turns or a physical endpoint. The fixed
terminal endpoint and the initial endpoint are already feasible. Hence
the entire normalized tour is in the half-plane if and only if its global
minimum event is feasible.

The first visit time to the global scalar minimum is

\[
 \tau_{-B}=\begin{cases}
 \kappa\sum_i z_i+B/\beta,
    &\text{if `-B` is the first of the two global records},\\[3pt]
 \kappa\left(H+\sum_i z_i\right)+B/\beta,
    &\text{if `-B` is the second global record}.
 \end{cases}
 \tag{2}
\]

Indeed, the first-visit identity is
`tau_(-B)=B/beta+kappa*(total prior upward variation)`. That upward
variation is respectively `sum z_i` or `H+sum z_i`.

For `a>0`, the extra constraint `s-B>=a*tau_(-B)` is consequently just
another upper bound on `sum z_i`. For `a=0`, it is the fixed condition
`s-B>=0`, which the original path already satisfies.

The fixed terminal time in the unrestricted four-leg proof is also one
upper bound on the same sum. Replacing these two upper bounds by their
minimum leaves exactly the same polytope geometry as in that proof:
two bounded monotone chains and one sum inequality.

## 3. Apply the existing concave vertex reduction

The exact uniform first-visit cost has quadratic part

\[
 -\kappa\left(\sum_i z_i^2+
       \sum_{i=1}^{m-1}z_i z_{i+1}\right),
\]

which is jointly concave. A minimum on the constrained turn polytope can
therefore be chosen at a vertex. The usual equal-coordinate-block argument
leaves at most one genuinely partial record turn. Removing nonexpanding
turns only advances the remaining first visits, so it again preserves
the moving-floor constraint.

There are at most one partial turn, two global record turns, and travel
to the final state: four directional legs, plus the final scalar hold.
This preserves both exit records and improves the integrated range.

If only one record is new, its direct fastest visit followed by direct
travel to the endpoint and a final scalar hold suffices. Every retained
extreme event is earlier than before, so the same feasibility argument
applies. With no new record, direct scalar travel and the final hold
suffice.

## 4. Limits and containment

Polygonal approximation through the original extrema and endpoint states
preserves the half-plane, the speed bound, and the prescribed records.
The running-record functionals are continuous in the uniform norm. The
bounded five-piece duration parameterization is compact, so the conclusion
passes to arbitrary Lipschitz paths.

When `b=a>0`, the scalar trajectory is nondecreasing. Accelerate its new
upper levels and put the remaining time into the final constant-scalar
leg; the same physical endpoint argument gives feasibility. If `a=b=0`,
all records are constant and any feasible two-run physical path suffices.

Every replacement retains physical endpoints and duration and has speed
at most one. Its light coordinates remain in the coordinatewise box
between those endpoints. Together with the proved half-plane constraint,
this keeps it in the original half-square and, under the stated
intersection containment, inside the physical arena. No scalar field is
extended outside that legal half-square.
