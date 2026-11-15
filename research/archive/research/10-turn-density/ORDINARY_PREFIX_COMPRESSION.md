# Pointwise compression of an ordinary capped-wave prefix

## 1. Result and scope

This fills the initial-prefix normalization used in
`CENTER_BELLMAN_CERTIFICATE.md`. It also gives a finite interface into a
later curved region: the prefix may end at a prescribed interior point,
rather than at the center or an endpoint. The result concerns capture
records, not monotonicity of the raw CDF trace.

Let an ordered positive princess family have paths

    p_q(t)=min(1,max(0,min(a_q+t,u_q-t),t-c_q)),

where `a_q,u_q` are nondecreasing, `c_q` is nonincreasing, and

    0<=a_q<=u_q<=2-a_q,       -a_q<=c_q<=1.             (1)

Use its fair reflection for the symmetric game. In addition, assume the
following separation across distinct initial positions:

    a_q<a_r  implies  u_q<u_r and c_q>c_r.              (2)

The continuous strictly ordered family in the center certificate satisfies
(2). This slightly weaker formulation also allows initial atoms, repeated
identical paths, and characteristic atoms confined to one initial-position
class. It does not permit an incoming or outgoing coalescence shared by
paths on opposite sides of the monster's starting point.

Start a monster at `a in (0,1)`. Consider any 1-Lipschitz prefix ending at
`(T,x)`, where `0<=x<=1`, with no center or endpoint visit before `T`.
There is another legal prefix joining the same point at the same time
which captures every princess captured by the original prefix no later.
It has the following form:

    inward; one outward capture block; inward; final outward joining leg.

It therefore has at most three interior turns. When a proposed inward
leg would cross the center, replace that part by an earlier center visit
and a center wait. If `x=0`, the last outward joining leg disappears, and
the replacement returns to center at some `e<=T` and waits there. It then
has at most two interior turns before its first center visit.

The comparison is pathwise, for both reflected copies. After `(T,x)`, the
replacement may copy the original monster exactly. Thus it also dominates
the complete capture-time vector. There is no restriction on the number
of original turns or on its intermediate speeds.

This is not a reduction for an arbitrary curved incoming CDF. It applies
when the initial attachment has the specified ordinary wave, including
its outgoing cap. No matching law or game value is asserted here.

## 2. Traces, initial atoms, and first-contact classification

Write `U=t+m(t)` and `V=t-m(t)`. Both are continuous nondecreasing
functions along every legal monster path. For an interior radial point,

    R(U,V)=min(C_ge(V),max(A_le(-V),I_le(U))),            (3)

where the notation means

    A_le(z)=Pr(a_q<=z),  I_le(z)=Pr(u_q<=z),
    C_ge(z)=Pr(c_q>=z).

The strict interior trace is

    R_strict(U,V)
      =min(Pr(c_q>V),max(Pr(a_q<-V),Pr(u_q<U))).          (4)

Neither formula should be substituted for a boundary trace at radius zero
or one. The proof below uses individual first contacts and thereby retains
those boundary captures automatically.

Partition the paths at the initial point into

    L={q:a_q<a},    E={q:a_q=a},    H={q:a_q>a}.          (5)

Every path in `E` is captured at time zero. Thus the higher initial ranks
begin above the closed initial CDF, while the lower initial ranks end below
the strict initial CDF. An atom at `a` must not be assigned a later inverse
time.

Before the first boundary visit, an initially higher path can first be
captured only on its incoming characteristic:

    U=u_q,       V<=c_q.                                (6)

It cannot first be caught on its initial unit outward leg, because the
monster begins below it and `V` cannot decrease. It cannot first be caught
on its final unit outward leg from above, because that would require a
previous crossing. An initially higher path missed in the interior may
instead first be caught at the endpoint itself.

An initially lower path first caught in the interior has one of two forms:

    early: V=-a_q,  U<=u_q;
    late:  V=c_q,   U>=u_q.                             (7)

The equality cases include first contact at a princess turn and tangency
along a unit-speed characteristic. Initial equality is already handled by
`E`. For a lower path, a first tangency on `U=u_q` can begin only at its
initial outward turn, so it is included in the early case.

By (2), every early lower capture occurs before every higher incoming
capture: its `U` is at most `u_q`, which is strictly smaller than the
incoming characteristic of each higher path. Likewise, every late lower
capture occurs after every higher incoming capture: its `V=c_q` is strictly
larger than the outgoing deadline of each higher path. These are the three
useful capture phases:

    early lower captures; higher captures; late lower captures. (8)

The raw trace may oscillate within or between these phases. Only new
records relative to the initial rank split are constrained by (8).

## 3. Construction and pathwise comparison

Let `S` be the initially higher paths caught by (6) before the final cut.
For a center cut, a contact at the final center on `U=u_q` may also be
included. At an endpoint cut, keep captures occurring only on that endpoint
outside `S`. If `S` is nonempty, let

    v = V at the first such capture,
    e = sup{u_q:q in S}.                               (9)

For a nonattained first capture, take the limit at the infimum of the
capture times. The monster path is continuous, so this defines `v`
unambiguously. Supremum and infimum are used directly; no ambiguous
generalized-inverse value is selected inside a distributional jump or gap.

Put `U_b=T+x` and `V_b=T-x`. The replacement makes the following moves.

1. Move inward at unit speed until `V=v`. If `v>a`, first reach center at
   time `a` and wait there until time `v` instead.
2. Move outward on `V=v` until `U=e`.
3. Move inward on `U=e` until `V=V_b`. If `V_b>e`, reach center at time `e`
   and wait until time `V_b` instead.
4. Move outward on `V=V_b` to the prescribed endpoint `(T,x)`.

Zero-length moves are omitted. At a center cut, step 3 is return and wait
and step 4 has zero length. At an endpoint cut, step 4 ends at that endpoint
at its original time.

### Legality

Monotonicity of the original characteristics gives `v<=e<=U_b` and
`v<=V_b`. Every originally captured higher rank has

    u_q<=2-a_q<2-a<=2+v.

Thus the first outward block cannot leave the interval. Its limiting
endpoint has the same property. The final outward leg ends at `x<=1`.
The two explicit center waits handle the only possible violations of
`V<=U`. All other segments have speed one, and all waits have speed zero.

### Initially higher paths

For `q in S`, the new outward block reaches `U=u_q` at

    time=(u_q+v)/2.

The original capture used the same `U` and a value of `V` no smaller than
`v`. Its outgoing deadline is still satisfied because `v<=V_original<=c_q`.
Consequently the new capture is no later. If the construction already
captured the path at an earlier center visit, that only improves the
comparison.

At a center cut, any additional higher path first caught at that center is
also caught during the replacement's center wait by time `T`. At an
endpoint cut, every higher path first caught exactly on the endpoint is
caught by the replacement no later than the same endpoint time. At an
interior cut all higher first contacts have already been included in `S`.

### Initially lower paths

An early lower capture has `V=-a_q<=v`. The new initial inward leg reaches
that characteristic with the smallest possible `U=a`, hence at time

    (a-a_q)/2 <= (U_original-a_q)/2.

The condition for the initial princess leg remains valid, since
`a<=U_original<=u_q`. If the construction visits center earlier, direct
inward travel already catches every initially lower path no later than
any other route from the same start could.

A late lower capture has `V=c_q` and occurs after every higher incoming
capture. Therefore `U_original>=e`. The new second inward leg reaches
`V=c_q` on `U=e`, at a no-later time. If `c_q>e`, the replacement reaches
center at time `e` instead: since `u_q<e<c_q`, that lower path is waiting
there and is captured even earlier. A lower path first caught at the final
center is covered in the same way.

Paths in `E` remain captured at time zero. The original prefix catches no
negative reflected path before its center boundary. Any earlier center
visit made by the replacement can only add negative captures. At a final
center, it catches every negative copy the original catches there. This
proves the full pathwise comparison.

### No higher incoming capture

If `S` is empty, move inward as far as `V=V_b`, using a center visit and
wait when `V_b>a`, and then move outward to `(T,x)`. Direct inward motion
catches every originally captured lower path no later. There are no
interior higher captures to preserve; center or endpoint contacts are kept
by the same endpoint argument. This is the zero-outward-block case.

## 4. Interface to a later curved field

The proof uses the ordinary representation only in the characteristic
rectangle traversed by the original and replacement prefixes. In particular,
if the law has this representation for `U<=s0`, stop the original prefix at
its first crossing of `U=s0`. The replacement stays in that region, ends at
exactly the same point, and has at most three interior turns before that
cut. Any subsequent curved continuation is unchanged.

If the replacement visits center sooner, its remaining portion is already
covered by the applicable center continuation certificate. If it has no
such visit, its finite interface parameters are the initial radius, the
first inward characteristic, the outward block characteristic, and the
final cut position. This supplies an initial-prefix reduction for a jointly
constructed ordinary attachment. It does not assert that the currently
collocated field has that attachment.

For the full ordinary family, taking the cut at the first boundary proves
the completeness of the center-prefix and endpoint-prefix families in
Section 4 of `CENTER_BELLMAN_CERTIFICATE.md`. The center-memory sweep theorem
or a verified center Bellman potential may then be attached at an earlier
center visit.

## 5. Why cross-initial characteristic atoms cannot be inserted by a limit

Take initial monster position `3/10` and three ordinary paths with

    (a,u,c)=(1/5,4/5,9/10), (2/5,4/5,4/5), (3/5,1,1/2).

The monster follows the vertices

    (0,3/10), (1/4,11/20), (3/10,1/2), (2/5,3/5), (1,0).

The higher incoming atom at `U=4/5` is caught at time `1/4`; following that
same characteristic inward then catches the lower path at time `3/10`.
After another outward leg, the highest path is caught at `2/5`. A single
outward capture block preserving the first higher capture must have
`V=-3/10`; preserving the last requires `U>=1`. It therefore catches the
lower path only at time at least `19/20`. This is a genuine failure of
pointwise compression without (2), not an inverse-convention discrepancy.

An outgoing-atom counterpart uses

    (a,u,c)=(1/5,3/10,3/5), (2/5,7/10,3/5), (3/5,9/10,3/5),

and monster vertices

    (0,3/10), (1/5,1/2), (13/20,1/20),
    (3/4,3/20), (9/10,0).

The lower path is caught at `13/20`. The proposed single outward block
would postpone it to `3/4`. Thus neither incoming nor outgoing positive-mass
coalescence across the initial split may be silently passed through this
normalization.

More general curved incoming fields can also alternate lower and higher
captures. For example, take a continuum of distinct initial positions
`a_q in [1/5,3/5]`, hold each until time one, and then move it outward at
unit speed to the endpoint. A monster starting at `3/10` may visit
`2/5`, then `1/5`, then `3/5` before time one. This captures new higher,
then lower, then higher ranks under a spatially atom-free ordered law.
Thus transport alone does not restore (8). A curved-prefix extension needs
an additional comparison or a capture-record potential.

## 6. Independent verification

`packages/interval_turn_sheet/verify_prefix_compression.py` constructs
ordinary princess polygons from the displayed max/min formula, independently
computes first captures by exact segment intersections, and compares them
with the normalized prefixes. The original monsters include arbitrary
piecewise speeds, waits, many turns, initial atoms, incoming levels above
one, negative outgoing characteristics, and cuts in the interior as well as
at both boundaries. The two counterfixtures above are explicitly rejected
by the hypothesis checker and confirm the stated capture-time failures.

Run:

```sh
python packages/interval_turn_sheet/verify_prefix_compression.py
```

These finite exact fixtures audit the construction and first-touch cases.
They do not instantiate a global game certificate or replace the proof.
