# Repeated inward and outward turns before the first center crossing

This note gives an exact capture-record comparison for

    +a -> inward V=v1 -> outward U=s1
       -> inward V=v2 -> outward U=s2 -> -1 -> +1.

It is not the crossed-center negative-M3 family. The second inward leg
can capture lower positive ranks missed earlier, before a second outward
leg captures higher survivors. The formulas identify precisely when this
mechanism is possible. They do not assert that a repeated route is active
in the game, or that every such route reduces to one I route.

## 1. Route and capture records

Assume

    0<a<=s1<=s2<=1,       -a<=v1<=v2<=0.

Every displayed turn is on the positive half of the interval. Its
space-time vertices are

    (0,a), ((a+v1)/2,(a-v1)/2), ((s1+v1)/2,(s1-v1)/2),
    ((s1+v2)/2,(s1-v2)/2), ((s2+v2)/2,(s2-v2)/2),
    (s2+1,-1), (s2+3,+1).

Let `A=Pr(p(0)<=a)` and use strict radial CDFs for inward first contacts
and closed CDFs for outward last contacts. Define deficit records

    r0=1-A,
    d1=1-R_<(a,v1),
    d=max(d1,1-R_<(s1,v2)),
    m1=min(r0,1-R(s1,v1)),
    m2=min(m1,1-R(s2,v2)),
    m0=min(r0,1-R(s2,v1)).

Transport and the ordering of the route imply

    m0<=m2<=m1<=r0<=d1<=d.                            (1)

The new lower-positive ranks captured by the second inward leg have
deficits in `(d1,d]`. The new upper-positive ranks caught by the final
outward leg have deficits in `[m2,m1)`. These rank intervals are separate.

## 2. Exact deletion cost

For a deficit q define the row and column primitives

    A_s(q)=integral_-s^s [R_<(s,V)-(1-q)]_+ dV,
    B_v(q)=integral_-v^1 [R(U,v)-(1-q)]_+ dU.          (2)

The first is `2 integral_0^q alpha_(1-r)(s)dr`. Differences of the second
encode the outgoing first-inverse moment; its constant below the first
capturable rank cancels in every expression below.

Let Cloop be the repeated route's payoff, and let Cfirst be the payoff
of the route that keeps the original first turn but merges the two
outward legs: `I_{s2}(a,v1)`. Put

    HighLoss=(v2-v1)(m1-m2)+(2s2+5-v1)(m2-m0)
       -B_v2(m1)+B_v2(m2)+B_v1(m1)-B_v1(m0),

    LowGain=A_s2(d)-A_s2(d1)-A_s1(d)+A_s1(d1).

Then the exact identity is

    4(Cloop-Cfirst)=HighLoss-LowGain.                 (3)

The two high terms have a direct capture interpretation. Ranks between
m2 and m1 are caught on the later outward characteristic v2 instead of
v1. Ranks between m0 and m2 are caught at the final positive endpoint
instead of on that earlier outward leg. The lower gain is the earlier
capture of `(d1,d]` on U=s1 instead of U=s2. All later negative-copy
captures coincide between the two routes, so they cancel exactly.

### Both outward turns may pass U=1

The restriction `s2<=1` is unnecessary for the capture kernel. Suppose
instead `a<=s1<=s2<=2+v1`, so the merged comparison route remains inside
the interval, and the paths are absorbed at their signed endpoints by
time two. Choose a common anchor `K>=s2` with `K<=2+v1`, for example
`K=max(1,s2)`, and replace the column primitive by

    B_(v,K)(q)=integral_-v^K [R(U,v)-(1-q)]_+ dU.

In HighLoss replace `2s2+5-v1` by `2s2+6-K-v1` and use that same anchor
in all four column terms. The other terms and every deletion gate stay
unchanged. For `s>1`, the row primitive has the physical-boundary form

    A_s(q)=2(s-1)q
           +integral_(s-2)^s [R_<(s,V)-(1-q)]_+dV.

The first term is the time needed to reach the spatial endpoint edge
from the formal U=s inward characteristic. Equivalently, extend R by 1
on its portion outside the interval. This extension retains all post-one
incoming and extra-wave captures; it assumes no ordinary incoming cap
and no outgoing plateau at U=1. The verifier includes cases with both
outward turns strictly after U=1.

## 3. Pointwise deletions and a necessary interlacing rectangle

Three cases admit direct deletions.

* If `d=d1`, the inserted inward leg captures no new lower ranks. Merge
  the outward legs to obtain `I_{s2}(a,v1)`; every first capture is at
  least as early.
* If `m2=m1`, the last outward leg captures no new upper ranks. Delete it
  and continue the preceding inward leg to the endpoints, obtaining
  `I_{s1}(a,v1)`.
* If `m1=r0`, the first outward leg captures no new upper ranks. Delete
  it and extend the initial inward leg to v2, obtaining `I_{s2}(a,v2)`.

Thus a nondeletable extra return requires all three strict inequalities

    d>d1,             m2<m1<r0.                     (4)

In terminal deficit coordinates

    x=1-a, yj=1+vj, zj=1-sj,
    D(z,y)=1-R(1-z,-1+y), e(y)=D(0,y),

the first and last requirements imply

    D(z1,y2)>D(x,y1),       e(y2)<m1.                (5)

If e is strictly increasing, a necessary gate is

    D(z1,e^{-1}(m1))>D(x,y1).                        (6)

For a general monotone e, replace the inverse by the supremum of the set
where `e(y)<m1`, with the appropriate one-sided trace. A numerical search
can screen (6) before evaluating the much more expensive capture costs.
Passing the gate only identifies a possible new capture mechanism; the
delay cost in (3) may still outweigh its gain.

## 4. Ordinary caps and a separated rounded outgoing turn

For the ordinary field

    D(z,y)=max(e(y),min(r(y),i(z))),

a useful first outward leg has `i(z1)<=m1<r0<=d1`. If a later outward leg
can capture anything new, `e(y2)<m1`; therefore

    D(z1,y2)<=max(e(y2),i(z1))<=m1<d1.

This contradicts the needed new lower captures. Hence these four-turn
same-half routes are pointwise reducible in an ordinary cap field,
without a concavity assumption on i.

For the rounded maximum `M_epsilon(I,e)` from
`FREE_SECOND_INWARD_FIELD.md`, suppose instead

    D=min(Z,M_epsilon(I,e)),       I(z1)<=(1-epsilon)d1. (7)

The homogeneous rounded maximum is increasing in both arguments, and
`M_epsilon(I(z1),d1)=d1`. Any y2 satisfying `e(y2)<m1<=d1` therefore has
`D(z1,y2)<=d1`. The same deletion conclusion follows. In particular, the
separated rounded outgoing-edge turn, with incoming scale much smaller
than the first inward deficit rank, cannot generate this additional
loop. A useful repeated route must use an earlier curved initial region
where the condition in (7) fails, or a different incoming topology.

## 5. The elementary deletions are not universal

There are legal ordered paths for which all three inequalities in (4)
hold and the repeated route beats each of the three elementary deletions.
An exact example uses the following positive paths, followed by an equal
reflection. Each listed path is linearly interpolated and stays at +1
after its last nonconstant knot.

| Mass | Space-time knots before the final constant segment |
|---|---|
| 7/20 | (0,2/5), (3/10,11/20), (1/2,11/20), (19/20,1) |
| 9/20 | (0,31/50), (1/5,57/100), (1/2,57/100), (93/100,1) |
| 1/5 | (0,7/10), (1/5,7/10), (2/5,29/50), (1/2,29/50), (23/25,1) |

Take

    a=3/5, v1=-2/5, s1=4/5, v2=-1/5, s2=1.

Direct first-intersection calculation gives

| Route | Exact expected capture time |
|---|---:|
| Repeated route | 67501/60000 |
| Merge outward legs, I_s2(a,v1) | 5723/5000 |
| Delete final outward leg, I_s1(a,v1) | 10247/7500 |
| Delete first outward leg, I_s2(a,v2) | 859/750 |

The first value is strictly smaller than each of the other three. This
does **not** prove that it beats every possible one-I route: an adjusted
first turn or initial start may still be better. Its purpose is to show
why the record gates, or a stronger cost inequality, are necessary in a
general curved field.

## 6. Verification and diagnostic scope

Run

```sh
python -B packages/interval_turn_density/verify_repeated_same_half.py
```

The verifier checks (3) against independent exact intersections of the
physical monster and princess paths, tests all three pointwise deletion
cases, and includes the genuine interlacing witness above. It does not
replace a global best-response theorem.
