# Full-record continuation at the center and after U = 1

## Status and scope

This note supplies the continuation boundaries for the high-start record
Bellman argument. It retains the lower and upper capture records from the
entire monster history. Its center argument applies to arbitrary speeds
and arbitrarily many turns. Its post-one inequalities are sufficient
conditions on an ordered princess CDF, and are verified over every relevant
affine cell of the saved field below.

The exact input is `snapshots/endpoint_joint_i1_field.json`, Git blob
`5c45d042ee9948faebc03354c3e1e2ee3cbec1a5`. The standalone verifier is
`verify_record_bellman_boundary.cjs`; its report is
`snapshots/record_bellman_boundary.json`. The embedded rational field reader
is the source with blob `5714f57ada458f38ef8b46adb32be2472a009622`.

This is a response-geometry result. It supplies no lower cost level for
the remaining initial one-I family, no matching upper law, and no game
value. The saved field has known pure-monster cost deficits. Replacing its
nodal values requires rechecking the stated gates; it does not inherit the
million-cell pre-one certificate automatically.

## 1. State and conventions

Let the nonnegative ordered quantile paths be `p_q`, with a fair reflection.
They are legal, reach their endpoint by time two, and stay there afterward.
Write `R(U,V)` for the radial CDF at
`t=(U+V)/2`, `x=(U-V)/2`. On a spatial endpoint, `R` below denotes the
interior trace; the closed CDF at the positive endpoint is one. On the
center, the strict radial CDF is zero. Interior CDF traces are continuous
for the field being certified.

Until its first center visit, a positive monster has caught one positive
rank interval `[L,M]` and has caught no negative copy. Its state satisfies

\[
 L\le R(U,V)\le M,
 \qquad \sigma=(2+L-M)/2.
\]

Fix an initial-start cutoff `a_0` and put `m_0=A(a_0)`. For every history
starting at `a>=a_0`,

\[
 M\ge m_0,
 \qquad L\ge B_0(V):=R_<\bigl(\max(a_0,-V),V\bigr).       \tag{1}
\]

For `V<-a_0`, the right side is the strict initial CDF `A_<(-V)`.
For the remaining values it is the fixed row `R_<(a_0,V)`.
Indeed every earlier light coordinate has `U'>=a>=a_0` and `V'<=V`;
also the actual initial position obeys `a>=-V`. Transport bounds every
past lower trace below by the right side of (1), so it bounds their running
minimum. The function `B_0` is nonincreasing. No record is reset at `U=1`.

Use the actual first inverses `alpha_q(s)` of `t+p_q(t)` and `beta_q(w)`
of `t-p_q(t)`. The absence of a `V=1` plateau and endpoint absorption imply

\[
 \beta_q(s)=s+1\quad(s\ge1)                              \tag{2}
\]

for almost every rank. Before time two, legality and `p_q(2)=1` give
`t-p_q(t)<=1`; equality is precisely the excluded `V=1` case when `s=1`.
After time two the path is at one. This proves (2) with the first-contact
convention.

The record envelope is the one in `PREONE_RECORD_BELLMAN.md`: go inward
to `V=w`, outward to `U=s`, then sweep the negative and positive endpoints.
It includes the direct-inward and immediate-outward boundary plans.
Here `V<=w<U<=s<=2+w`; a plan is truncated at its first endpoint.

## 2. A center boundary with full records

**Endpoint-block lemma.** Suppose that, from every center time
`tau>=a_0`, every radial interior point reachable afterward has

\[
 R\le r_*<m_0.                                          \tag{3}
\]

Then after the first center visit of any monster starting at `a>=a_0`,
the direct negative-first endpoint tour is optimal among all legal
continuations.

At the first center visit every previously missed lower positive rank has
been caught, by continuity; center ranks are caught at the visit itself.
Thus the remaining positive ranks are exactly `q>M`, with probability
`P=(1-M)/2`. By (3) they can be caught only at the positive endpoint.
The entire negative block `q>r_*`, of probability `H=(1-r_*)/2`, is still
uncaught and can be caught only at the negative endpoint. Hence `H>P`.

The direct left unit ray catches each surviving negative path at its
earliest possible time. Before reaching `-1` it is pointwise no larger
than any other legal monster continuation from the center. If another
curve meets a negative target at a time in this interval, the ray has
already crossed it by the intermediate value theorem. By the time the
ray reaches `-1`, it has crossed every surviving negative target.

If a competitor reaches `-1` before `+1`, the direct tour is no later on
any negative target and reaches `+1` no later. If the competitor reaches
`+1` first, it can gain at most two time units on each positive survivor,
for a gain of at most `2P`. It reaches `-1` at least two units later than
the direct tour, losing at least `2H` on the negative endpoint-only block.
All other negative captures are no earlier than for the direct ray.
Since `H>P`, this cannot improve the expected cost. A continuation which
never reaches a required endpoint has infinite cost on a positive block.
This proves the lemma without a turn-count or waiting restriction.

A sufficient CDF test for (3) is

\[
 \sup_{U\ge1,\,V\ge0}R(U,V)\le r_*<m_0.                 \tag{4}
\]

A future point reachable from the center at `tau` has `V>=tau>=a_0`.
For `U<1`, transport gives `R(U,V)<=R(1,V)`, so (4) also bounds the
pre-one part of that cone. For `V>1` the endpoint-by-two extension has
zero interior CDF. Thus (4) covers the entire future cone, not just the
single outgoing row at the center visit.

## 3. Four sufficient post-one gates

Choose constants `C<1/2` and `1<Ubar<2`. In addition to (4), assume on
the physical interior:

\[
 -R_V(U,V)\le C\qquad(U\ge1,\ V\le0).                  \tag{5}
\]

\[
 4+B_0(V)-2R(U,V)-(U+6-V)R_U(U,V)\ge0
 \qquad(U\ge1,\ V\le0).                                \tag{6}
\]

\[
 R(U,V)<m_0\qquad(U\ge\overline U).                     \tag{7}
\]

\[
 2(2-\overline U)-(\overline U+6)(1-m_0)>0.              \tag{8}
\]

For a continuous piecewise-affine field these are whole-cell inequalities
with one-sided slopes. They imply the outward record Bellman inequality
after `U=1`, for every reachable high-start record state. The following
argument treats interior second turns and closed endpoint turns separately.

## 4. Interior second turns after one

After a first inward leg to `w`, its remaining lower record is

\[
 l=\min(L,R_<(U,w)).
\]

For `w<=0`, (1) and transport give `l>=B_0(w)`.
Fix this first leg and vary the second turn `s`, strictly before its
endpoint. Put `m(s)=max(M,R(s,w))`.

When `m(s)>M`, differentiating direct first-capture moments gives

\[
 4\frac{dC}{ds}
 =2\frac{d}{ds}\int_0^l\alpha_q(s)dq
   +4-2R(s,w)-(s+6-w)R_U(s,w).                          \tag{9}
\]

First-inverse speed gives
`alpha_q(s+h)-alpha_q(s)>=h/2` for `s>=1`, hence the first term in (9)
is at least `l`. Equations (1) and (6) make (9) nonnegative. If the old
upper record dominates, then `m(s)=M` and the derivative is at least
`4-2M+l>=2`. At inverse-rank regime boundaries the same statement follows
from direct moments; first inverses cannot jump downward.

For `w>=0`, (4) gives `R(s,w)<m_0<=M`, so there is no new interior upper
capture and the latter case applies. Therefore every interior `s>U>=1`
is no better than reducing `s` to `U`. That limit is the direct-inward
continuation. The endpoint capture jump is not included in (9).

## 5. Delayed endpoint turns

Only the nonautomatic outward Bellman case needs a further check:

\[
 M=R(U,V),\quad l=R(U,w)<L\le M,\quad w>V.
\]

If the old upper record is strictly above the current CDF, or the first
inward leg adds no lower capture, the existing automatic or finite-prepending
arguments apply.

### 5.1 First turn w <= 0

For the delayed endpoint `s=2+w`, compare immediate outward motion to the
earlier endpoint `sbar=2+V`. In the notation of the record Bellman note,
twice the delayed cost minus comparator cost is `H-K(L)`, and `K` increases
with `L`. First-inverse speed and `0<=alpha_sbar<=sbar` give

\[
 H-K(L)\ge H-K(M)
 \ge (1+l/2)(w-V)-(2+V)(M-l).                           \tag{10}
\]

The whole reflected-copy delay supplies `H>=w-V`. Equation (5), along
the fixed current row, gives `M-l<=C(w-V)`. Since `V<=w<=0`, (10) is at
least

\[
 (1-2C)(w-V)>0.                                        \tag{11}
\]

Thus every genuinely delayed endpoint plan in this case is strictly
dominated for every admissible lower record `L`.

### 5.2 First turn w >= 0

Compare the delayed plan directly to inward motion from the current `U`.
Let `Delta=s-U` and `m=max(M,R_closed(s,w))`. Direct capture partition and
first-inverse speed give

\[
 4(C_{\rm delayed}-C_{\rm inward})
 \ge \Delta(4+l-2m)-(U+6-w)(m-M)
 \ge \Delta(2+l)-(U+6-w)(1-M).                         \tag{12}
\]

At the endpoint, `s=2+w`. Since the nonautomatic case has
`R(U,V)=M>=m_0`, (7) forces `U<Ubar`. With `w>=0`, the last expression
in (12) is bounded below by the strictly positive constant in (8).
This excludes the remaining endpoint plans. It does not rely on declaring
flat incoming pieces to stay flat under future field perturbations.

## 6. Endpoint and terminal-time boundaries

At a positive endpoint, the direct left unit sweep catches every remaining
target no later than any other continuation. It is the pointwise smallest
legal curve until it reaches `-1`; by that time, which is at least time two,
all targets are at their endpoints. The intermediate value theorem therefore
also covers targets that were still interior when the sweep began.

At time two, the remaining law is supported on the two endpoints. One of
the two direct endpoint orders is optimal. Both orders are included in the
one-I envelope by its immediate-outward and direct-inward boundary plans.
Thus time two may be used as a finite stopping boundary. Together with the
center lemma, these are the physical exits needed for the post-one argument.

## 7. From local gates to finite record inequalities

The pre-one certificates cover genuinely delayed plans `U<s<1` and
`s>=1`. Sections 3–5 cover the continuation region `U>=1`. Direct-inward
and immediate-outward plans are handled by finite prepending: prepend the
current short unit leg and merge it with the corresponding boundary leg.
This is preferable to assigning a sign to a standalone boundary derivative.

For the finite continuous affine field, direct inverse moments are
continuous piecewise-polynomial functions of their threshold and rank.
For example, with the physical constant extensions,

\[
 2P_s(q)=\int_{-s}^{s}\min(q,R_<(s,v))\,dv,
 \qquad
 2T_v(q)=\int_{-v}^{v+2}(q-R_\le(u,v))_+\,du.           \tag{13}
\]

Here the first extension is one below the positive endpoint boundary;
the second is zero below the center boundary when needed. Above time two,
the absorbed paths give the explicit affine moments. Formula (13), rather
than an integral of pointwise inverse derivatives, retains moving-rank flux.

Treat closed endpoint plans as a separate parameter branch from the
interior-endpoint limit. Each branch has continuous direct moments on a
compact parameter domain. At a limiting first-center turn, the actual
center contact can only lower the displayed limiting capture cost, and
the center lemma supplies a direct-inward plan with no greater cost.
Thus that limit does not lower the envelope below its valid boundary plan.

On a fixed outward current leg, the upper record is
`M(u)=max(M,R(u,V))`; the lower record is retained. The resulting envelope
is semialgebraic and has finitely many differentiable pieces. Interior
active branches satisfy the verified derivative inequalities. When a
minimizing branch enters through `s=U` or `w=V`, finite prepending supplies
the same inequality. Continuous direct moments, including the separate
closed endpoint branch, rule out an unaccounted downward jump.
Integration over the finite pieces proves the outward finite-increment
inequality. Prepending and merging inward legs proves the inward one.

These finite inequalities telescope along all finite unit-leg curves with
their actual records. The finite-contact/quantile approximation argument
in `PREONE_RECORD_BELLMAN.md` then extends them to arbitrary legal speeds
and arbitrary turn counts. The center and endpoint arguments above are
already unrestricted, so this extension does not assume a finite number
of turns after an artificial boundary.

Consequently, after combining the three gate certificates, minimizing
against this saved field over monsters with `|a|>=a_0` reduces to the
initial one-I family with its stated endpoint and direct-sweep boundary
plans. This is an equality of response infima on that starting-position
domain; it is not a lower cost bound for that family.

## 8. Exact saved-field audit and reusable conditions

For this field the verifier chooses

\[
 a_0=255/256,\quad m_0=17670484999841/19531250000000,
 \quad C=9/20,\quad \overline U=3/2.
\]

It reconstructs all 34 affine pieces of the history floor from triangle
intersections and the initial diagonal. It checks 1,156 negative post-one
triangles, 6,834 floor-split flux vertices, and 1,936 pieces beyond
`U=3/2`. Its exact bounds are:

| Quantity | Certified value |
|---|---:|
| Maximum negative-V spatial slope `-R_V` | `108238912/244140625` |
| Margin below `9/20` | `6497477/976562500` |
| Minimum post-turn flux (6) | `91472232581/1000000000000` |
| Positive-V rank bound `r_*` | `431776293429/500000000000` |
| Margin `m_0-r_*` | `12867576604331/312500000000000` |
| Maximum rank for `U>=3/2` | `107952655811/125000000000` |
| Margin below `m_0` there | `3211530117489/78125000000000` |
| Maximum U with `R>=m_0` | `58583102860647/45229875167500` |
| Wide endpoint four-cost margin (8) | `2230204999523/7812500000000` |
| Negative endpoint coefficient in (11) | `1/10` |

All 69 saved nodes on `V=1` have zero interior CDF. The cone and CDF range
checks pass exactly. Endpoint and center atoms retain their separate
strict/closed conventions.

The proofs in Sections 2–6 are reusable. On a fixed triangulation their
CDF tests are linear in nodal values: transport, the positive-V cap,
negative-V slope bound, floor-corrected flux, and the cap beyond `Ubar`.
The physical endpoint and no-`V=1` conditions are explicit structural
attachments. Their positive margins can be imposed in a joint corrected
field solver. The pre-one arrangement and its inverse-rank inequalities
remain field dependent and must be reverified for a new field.

Replay from the repository package directory:

```sh
node verify_record_bellman_boundary.cjs \
  --field snapshots/endpoint_joint_i1_field.json \
  --expected snapshots/record_bellman_boundary.json
```

For a distinct diagnostic field use `--allow-other-field` and `--report`;
the report records its actual blob hash and every failed gate. This does
not transfer the original pre-one proof or assert a game bound.
