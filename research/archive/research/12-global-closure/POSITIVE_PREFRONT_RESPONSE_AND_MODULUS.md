# Positive prefront response and a continuous center modulus

This extends two supplied-field reductions. A center record gap only
needs a uniform continuity modulus, not a bounded density. The curved
three-run exchange also applies on the whole positive precenter
decision region, with its physical center, endpoint, and incoming
front as stopping boundaries.

The curvature hypothesis is imposed on the entire region in this
second theorem. No optimality-preserving replacement into that class,
no equilibrium phase existence, and no uniform turn count across
approaching Princess laws is proved here.

There is also a sharp scope obstruction: monotonicity of `F_U` in
both light coordinates throughout the inner region already forces
an endpoint-sweep upper below the certified game lower once that
region extends to `U=41/40`. No front-completion assumption is needed
for that exclusion. Thus the whole-front-two curvature class is
excluded; a competitive phase construction needs a different inner
phase. The front-one case is not excluded by this argument.

Use the regular symmetric ordered signed CDF conventions of
`CURVED_INITIAL_PHASE_RESPONSE.md` and
`FRONT_CONTINUATION_GAPS_AND_ZENO.md`. There is no center atom;
interior traces are jointly continuous, endpoints are sticky, and
actual endpoint visits reset the appropriate surviving record.
Fix an incoming front `1<=C<=2` and maximal outward completion there.

## 1. A modulus is enough for the positive-gap center bound

Choose any fixed `0<r_0<1`. On the compact center strip define

\[
 \omega(h)=\sup_{\substack{0\le s\le C\\0\le x\le h}}
                    \bigl(F(s,x)-\tfrac12\bigr),
                    \qquad0\le h\le r_0.
\tag{1}
\]

Joint continuity and `F(s,0)=1/2` give `omega(h)->0` as `h->0`.
The strip avoids physical endpoints, so endpoint atoms are irrelevant
to this uniform continuity statement.

Suppose a center state at time `t<C` has

\[
                 \min(l,r)\le\tfrac12-\delta,
                 \qquad\delta>0.
\tag{2}
\]

Choose any `h_delta` with

\[
           0<h_\delta<r_0,\qquad \omega(h_\delta)<\delta.
\tag{3}
\]

In productive heavier-first balanced normal form, every proper
return must lower its affected record to at most its opposite record,
which is at most `1/2-delta`. Its peak consequently satisfies

\[
                        F(s+h,h)\ge\tfrac12+\delta.
\tag{4}
\]

If `h<=h_delta`, (1)--(3) contradict (4). Thus every such return has
height strictly greater than `h_delta`, and lasts more than
`2h_delta`. Front shortening makes all returned triangles finish
by time `C`. A safe count is therefore

\[
\boxed{\qquad
 N=\left\lfloor\frac{C-t}{2h_\delta}\right\rfloor.
\qquad}
\tag{5}
\]

Unproductive balanced returns are deleted or absorbed before using
(4), exactly as in Section 2 of the cited continuation note. Center
holds are absorbed into neighboring tents or the final tour. Prove
the bound in every finite triangle budget, then use the same compact
fixed-budget minima and payoff approximation argument. This produces
an attained continuation with at most `N` proper returns without
assuming a finite unrestricted optimizer beforehand.

Consequently **every center state other than `(1/2,1/2)` has a finite
optimal continuation for each such continuous fixed field**. The
explicit power-law Zeno example begins at the exceptional fully
uncaught pair and does not contradict this statement. The density
condition `F(s,x)-1/2<=Mx` is a convenient quantitative special case,
not a necessary regularity assumption for a fixed-field finite count.

### Uniformity over dangerous states

The center-slack estimate remains

\[
           J\ge b-(C+3)d,
\tag{6}
\]

for an early first-center state `(1/2,1/2-d)` whenever the initial
center value is at least `b`. If `b>c`, every response below target
`c` has the common positive gap `(b-c)/(C+3)`. One choice of
`h_delta` in (3) then works for all such states, so (5) is uniform
over dangerous responses of that one field. Late-center and
endpoint-first branches are handled by the exact incoming-front
terminal, not discarded by an unstated threshold assumption.

In particular, the endpoint-doping construction in the continuation
note gives finite dangerous postcenter complexity for every jointly
continuous base field to which its security and front hypotheses
apply. A bounded central density is unnecessary. For the globally
value-dense construction, continue to use the justified front `C=2`.
Both the modulus and the resulting count may deteriorate along the
approaching sequence.

## 2. The whole positive precenter domain

Use `U=t+x`, `W=t-x`, and in the following sections write `F(U,W)`
for the field in light coordinates. Its closed positive prefront region is

\[
 \mathcal D_C=\{0\le U\le C,\ -U\le W\le U,
                                      U-W\le2\}.
\tag{7}
\]

A Monster starting at an interior positive position first leaves
the open decision region by reaching one of

* the center, `U=W`;
* the positive physical endpoint, `U-W=2`;
* the incoming front, `U=C`.

The initial time boundary `U+W=0` is not an outgoing boundary:
physical time increases. Actual endpoint and center starts are
separate cases from the outset.

Assume the curved response conditions on the smooth positive-time
interior of this **whole** region:

\[
 F_U>0,\qquad F_{UU}\ge0,\qquad F_{UW}\ge0,
                    (\log F_U)_{UW}\le0.
\tag{8}
\]

The equivalent inverse/transition-map conditions from the curved
phase theorem are sufficient instead. They are required only on
the physical rectangles that occur below: the inverse bottom-edge
map is increasing concave, and every vertical transition is
increasing concave with slope at least one. Continuous singular
boundary traces are permitted as in that theorem. The strict
horizontal condition is imposed on intervals that are inverted;
no unproved inference from an undifferentiated boundary asymptotic
is used.

**Theorem.** Every complete Monster response with an interior positive
start is weakly dominated by one whose prefix to its first outgoing
boundary of (7) has at most three unit-speed runs. If three occur,
their order is left-right-left. A first front or first positive-
endpoint prefix has at most two runs, left-right, with a zero first
run allowed. A first-center prefix has at most three. Reflection
gives the negative-start statement.

After that exit use the exact center continuation, the exact
one-parameter precenter-front terminal, or the direct opposite
sweep, respectively. The statement concerns a whole response with
both records; it does not claim that a prefix replacement preserves
its two exit records.

## 3. The feasible peak interval keeps every comparison physical

Isolate a right-left-right triple with entry `(U_0,W_0)` and exit
`(U_1,W_1)`. Its variable middle light coordinate is `u`:

\[
 (U_0,W_0)\longrightarrow(u,W_0)
 \longrightarrow(u,W_1)\longrightarrow(U_1,W_1).
\tag{9}
\]

The exact physical feasible interval is

\[
\boxed{
 u_-:=\max\{U_0,W_1\}\le u\le
 u_+:=\min\{U_1,W_0+2\}.}
\tag{10}
\]

The old triple lies in this interval. The first edge is below the
positive endpoint precisely when `u<=W_0+2`, and the entire middle
edge stays nonnegative precisely when `u>=W_1`. The final edge is
legal because its prescribed exit is legal. All times remain
nonnegative, and all `U` values are at most `U_1<=C`.
In particular the rectangle
`[u_-,u_+] x [W_0,W_1]` lies in the physical positive arena.
The bottom and top integration edges outside this smaller rectangle
also remain inside the arena. No CDF extension beyond an endpoint
or through a negative spatial half is used.

Let the incoming scalar record interval be `[ell,h]`, so the two
surviving masses are `(ell,1-h)`. Put

\[
 s=F(u,W_0),\qquad u=\chi(s),\qquad g(s)=F(u,W_1).
\]

On the productive interval `s>h`, `g(s)<ell`, the exact integrated
prefix-plus-future cost is concave in `s`, by the proof in
`CURVED_INITIAL_PHASE_RESPONSE.md`. Use the **actual fixed complete
old suffix** as the continuation. Its cost is increasing and concave
in both incoming records. The smaller physical interval (10) changes
none of that calculation.

A concave minimum occurs at a physical endpoint of (10) or at one
of the record boundaries `s=h`, `g=ell`. The latter boundaries can
also be pushed to a physical endpoint, by the next comparisons.

### An unproductive first right leg

If `s<=h`, decrease `u` toward `u_-`. Until the old final right edge
is rejoined, the new Monster is pointwise no farther right than the
old one, so its lower record only improves. The old field never
exceeded `h` before that rejoining: its first right peak was at
most `h`, its left leg decreased the CDF, and the new extra part
of the final edge has values at most `g<=s<=h`. Thus no upper
capture is delayed. After rejoining, the physical path is identical.
The record costs and the fixed future cannot increase.

### An unproductive middle left leg

If `g>=ell`, increase `u` toward `u_+`. The new Monster is pointwise
no farther left until rejoining the old final edge, so its upper
record only improves. Every old field value on the triple was at
least `ell`; every new value before rejoining is no smaller. The
lower record remains `ell`. Again the complete cost cannot increase.

These arguments stay inside (10). They do not silently replace the
triple by an illegal full left-right or right-left corner of a box.
They cover the record-boundary minima and initially unproductive
triples alike. Hence a weakly improving replacement always reaches
`u_-` or `u_+`.

## 4. Boundary contacts terminate the precenter prefix

At the physical endpoints of (10), one of the following happens.

* If `u_-=U_0`, the first right run disappears.
* If `u_+=U_1`, the final right run disappears.
* If `u_-=W_1`, the middle left run reaches the actual center.
* If `u_+=W_0+2`, the first right run reaches the actual positive
  endpoint.
* If `u_+=U_1=C`, the first right run reaches the incoming front,
  possibly earlier than the old exit time.

Several equalities can hold at once; any earlier outgoing contact
is a valid stopping event. At an actual endpoint contact use the
one-sided limit of the nominal interior-trace calculation. Joint
continuity of an endpoint trace is not inferred from interior
continuity alone. Physical capture is lower semicontinuous under
uniform path limits, and the actual endpoint reset is favorable,
so the limiting physical path has no greater cost than this
one-sided nominal limit.
Every compared path itself is still inside the arena. Retaining
its remainder as a physical path and then taking the direct sweep
can only improve the comparison. The same first-exit logic uses
the exact center or incoming-front value at the other two boundaries.

In a finite alternating word, always process the **earliest**
right-left-right triple. It occupies runs one through three if
the word begins right, and runs two through four if the word begins
left. If a new boundary is reached in that triple, the prefix to
the new first exit therefore has at most three runs. Otherwise
one of its runs disappears, strictly decreasing the finite word
length. Repeat until a boundary terminates the prefix or there
is no right-left-right triple. The latter alternating word has
at most three runs and can only have left-right-left order.

A first front or positive-endpoint contact requires a last right
run. A left-right-left replacement that touches that boundary
on its middle right run is stopped there, leaving at most two
runs. This proves the sharper assertions in the theorem.

## 5. Arbitrary paths and certified boundary lower bounds

The established center, front, and endpoint normalizations allow
every compared complete future to finish by absolute time `C+3`.
This gives a common finite record-cost bound and a compact family
of complete physical continuations.

For an arbitrary legal precenter path, trim a shrinking time window
before its first outgoing boundary. On the compact remaining open
prefix, sufficiently fine axis-staircase approximations stay inside
the physical region. In the final window, join its exact old exit
by the appropriate two directional legs: right then left for a
center exit, left then right for an endpoint exit, and either legal
order for an interior front exit. The window is small enough that
no unintended opposite boundary is reached. Simultaneous front/
center or front/endpoint exits use the same corresponding order.

This gives uniform path approximations preserving the old exit
state and time. Record histories converge on compact interior
prefixes. At an endpoint exit, any old capture in the final window
that is missed by the approximation but not captured by its shared
actual endpoint arrival belongs to a Princess lying in a shrinking
punctured endpoint neighborhood at that arrival time. Its mass tends
to zero; an actual endpoint atom is captured by both paths. Bounded
completion time therefore makes the resulting payoff error tend
to zero, without assuming endpoint-trace continuity. The fixed
complete suffix has continuous record cost. Apply the finite-word
replacement and take subsequences of the at most three run lengths
and the bounded complete physical continuations.
Limits at actual endpoint contacts use lower semicontinuity of
capture; an earlier endpoint hit is a favorable reset. Front and
center exit limits follow from the continuous field and their
actual legal continuations. The result has no larger complete
cost. There is no finite-switch or non-Zeno premise.

Here is a useful global certificate form. At each outgoing boundary
let `P` be **any** valid lower bound on all legal remaining
continuations from its actual state and both updated records.
It must include continuations that travel along that boundary.
If every at-most-three-run **first-exit** prefix has

\[
                  \hbox{prefix cost}+P(\hbox{exit})\ge c,
\tag{11}
\]

and the separate initial center and endpoint cases are covered,
then every unrestricted response costs at least `c`.

For this whole-response inference, `P` itself need not be concave.
Run every exchange with the actual fixed old suffix as its concave
continuation. After obtaining the short prefix, truncate it at its
first outgoing contact. Its remainder together with the old suffix
is one actual legal continuation, whose cost is at least `P` there.
Thus the old cost is at least the new actual cost, which is at least
the left side of (11). This does not modify the earlier fixed-exit
theorem for an abstract concave terminal `Q`; it is a different way
to use that theorem in a global lower certificate.

Equivalently, if an arbitrary complete path strictly violated `c`,
take a finite prefix approximation whose complete physical cost still
violates `c`, then apply the finite-word exchange and the first-exit
guard. This gives a contradiction without taking any limit through
`P`. No monotonicity or continuity of `P` is needed either. Its
concavity can still be useful for convex synthesis in unknown field
variables; the soundness statement above does not assert such
convexity for an arbitrary boundary function.

## 6. The inner monotonicity class is excluded beyond a short front-one range

For this section, `C` denotes only the extent of the inner shape
hypothesis, with `1<C<=2`. **No outward completion at `C` is assumed.**
Suppose

\[
 g(U,W):=F_U(U,W)
\]

is nondecreasing in both variables throughout
`0<=W<=U<=C`. This follows from the two signs `F_UU>=0` and
`F_UW>=0`; neither strict positivity nor the logarithmic curvature
condition is needed. Define

\[
                         b=\sup_{0\le w<1}g(1,w).
\tag{12}
\]

There is no assumption that the two derivatives have a common
center trace. Monotonicity instead gives `g(u,1)>=g(1,w)` for
every `1<u<C` and `0<=w<1`. Integrating in `u` proves

\[
 (C-1)b\le F(C,1)-\tfrac12\le\tfrac12,
\tag{13}
\]

so `b` is finite. Continuity of the field at the center justifies
the corresponding improper integrals if a derivative has a
singular one-sided trace.

The fastest endpoint sweep is the path `U=1`, `-1<=W<=3`. Its
actual expected capture cost is

\[
                   E=\frac12\int_{-1}^{3}F(1,W)\,dW.
\tag{14}
\]

Endpoint atoms are captured at their actual endpoints; they do
not add a spurious interior-trace jump to this integral. On the
positive inner portion,

\[
 F(1,w)-\tfrac12
       =\int_w^1g(u,w)\,du
       \le\min\{b(1-w),\tfrac12\},\qquad0\le w\le1.
\tag{15}
\]

On the negative portion, symmetry and monotonicity give

\[
 F(1,w)=1-F(w,1)
       \le\tfrac12-b(w-1),\qquad1\le w\le C.
\tag{16}
\]

For `C<=w<=3`, transport alone preserves the upper bound
`1/2-b(C-1)`. On `-1<=w<=0` use `F<=1`.
Putting `d=C-1` and `A=d-d^2/4` in (14) therefore gives

\[
 E\le\frac54+\frac12\int_0^1\min\{bu,\tfrac12\}\,du-Ab.
\tag{17}
\]

For `b<=1/2` this is `5/4+b(1/4-A)`. For `b>=1/2` it is
`3/2-1/(16b)-Ab`. If `A<=1/4`, the second expression is at most
`3/2-sqrt(A)/2` by the arithmetic-geometric mean inequality.
The maximum of the first expression is no greater: the difference
is `(sqrt(A)-1/2)^2/2`. If `A>=1/4`, both expressions are at most
`5/4`. Consequently

\[
\boxed{
 E\le
 \begin{cases}
 \displaystyle\frac32-\frac14\sqrt{(C-1)(5-C)},
                                  &1<C\le3-\sqrt3,\\[1mm]
 \displaystyle\frac54,           &3-\sqrt3\le C\le2.
 \end{cases}}
\tag{18}
\]

The bound is nonincreasing in `C`. Already at `C=41/40`,

\[
 E\le\frac32-\frac{\sqrt{159}}{160}
       <\frac{1137}{800}=1.42125,
\tag{19}
\]

because `sqrt(159)>63/5`. This is below the published certified
global lower; see the repository [proof status](../../README.md).
Every law with the displayed inner monotonicity through `41/40`
is therefore excluded from competitive security. In particular
the whole-positive-wedge condition for the globally sufficient
front two cannot be an equilibrium-sufficient field class.

This conclusion uses only the inner region `0<=W<=U<=41/40`.
It leaves the local curved initial-phase theorem intact and does
not rule out a front-one field or a finite construction with a
change of inner phase before that level. It supplies a concrete
location requirement for such a change, rather than an assertion
that all Princess laws have the required phase geometry.

## 7. What the combined gate proves

For a field satisfying the whole-region curvature hypothesis, the
precenter search is now a finite list of continuous parameter
families. A front exit uses the exact one-parameter terminal already
proved. A center exit uses the center recurrence with both records.
If the same field has a certified center slack above a target, the
uniform modulus supplies a finite triangle budget for every
potentially violating center branch.

Endpoint doping preserves the curvature conditions when the base
field has them: nonzero derivatives scale by a positive constant
and the logarithmic mixed derivative is unchanged. It can create
the center slack above an unrestricted game upper as in the cited
continuation note. These facts give a complete finite response
gate for that supplied curved class, including actual boundary
captures and arbitrary original turn counts.

They must not be confused with a global sufficient field class:
Section 6 excludes the whole-front-two curvature hypothesis itself.
The modulus and endpoint-doping result is value-dense without that
curvature assumption; the three-run precenter theorem is a separate
conditional simplification. A competitive use of both needs the
appropriate additional inner phase or a justified front-one model.

The remaining equilibrium question is whether a globally sufficient
approaching or attaining Princess class can be chosen with the
whole precenter curvature property, or with a finite one-way cover
to which an equally complete argument applies. Neither endpoint
doping nor the finite center count proves that field-structure
statement. No one triangle budget is claimed for an entire
approaching sequence.
