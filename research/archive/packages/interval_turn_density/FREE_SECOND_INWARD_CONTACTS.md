# Free second inward turns: contacts and the common-graph obstruction

These exact identities enlarge the physical monster family and exclude
one proposed attachment. They do not construct a matched law or give a
new game-value bound. Ongoing start-dependent surface work is separate.

## 1. Physical route and exact first contacts

For `0<z<=s<=1` and `-z<=v<z`, let `I(z,v,s)` have vertices

    (0,z), ((z+v)/2,(z-v)/2), ((s+v)/2,(s-v)/2),
    (1+s,-1), (3+s,+1).                                (1)

Reflect the route fairly. Its second turn is `U=s`; the previously
studied inward family has `s=1`. The boundary `s=z` is negative M1,
because the middle outward segment has zero length. The larger physical
range is `s<=2+v`, but the pre-one range is the focus here.

For a nonnegative princess starting at a, define exact first inverses

    alpha(U)=inf{t:t+p(t)>=U},
    beta(V)=inf{t:t-p(t)>=V},
    psi(U)=2alpha(U)-U,       phi(V)=2beta(V)-V.

The reflected princess is first caught at `beta(s)`. The positive
princess is first caught at

    a<=z: alpha(z) if psi(z)<=v, and alpha(s) otherwise;
    a>z:  beta(v) if phi(v)<=s, and beta(s+2) otherwise. (2)

The symmetric expected time is half the sum of these two contacts.
Every equality in (2) is closed, retaining initial capture at `a=z` and
capture on a turn. The excluded boundary `v=z` can touch a waiting
center atom and requires its separate first-contact correction.

For `a<=z`, if the first inward leg misses, the following outward leg
cannot catch the princess; the next available contact is `alpha(s)`.
For `a>z`, the first inward leg cannot catch the princess. The middle
outward leg catches it precisely when its first inverse lies before the
second turn; otherwise the third inward leg has also already been
crossed, and the last sweep catches it. The reflected copy cannot meet
the first two positive-half legs, so its contact is `beta(s)`. This
proves (2) without a wave-count or endpoint-time assumption.

Replacing only `beta(s+2)` by its upper bound `s+3` gives an upper
relaxation. This is exact for a canonical path already at the endpoint
when those positive outgoing thresholds are reached. The alpha terms
must remain first inverses. A distribution of second turns can put mass
at an incoming U plateau, where first and last inverses differ.

## 2. A common decreasing second-turn graph

Suppose all initial starts with first-turn V=v share the second turn
`s=S(v)`, with S continuously decreasing locally. Give the physical
surface a nonnegative density `h(z,v) dz dv`, supported where
`-z<v<z` and `z<=S(v)<=1`.

Consider a canonical negative-c princess prefix whose incoming inverse
is the constant u near its end, followed by an outward connector to
`U=1` and then the endpoint. Its initial prefix may itself be curved.
Fix a and u, and vary the last characteristic c. Suppose

    S(c0)=u,             -a<c0<0,
    j_a(c0)=integral_-c0^a h(z,c0)dz>0.                (3)

The low-start I early-capture condition on the final incoming portion
is exactly

    v<=min(c,S^{-1}(u)).                               (4)

Below the cutoff, its unreflected four-score is `v+u`; above the cutoff
it is `2S(v)+6`. Thus its c derivative jumps **upward** at c0 by

    (u+6-c0)j_a(c0)>0.                                (5)

The high-start alpha contribution has a continuous first derivative at
c0. Its additional start interval `u<z<S(v)` collapses, and the
capture-time difference has the vanishing factor `S(v)-z`. The
reflected beta contribution does not depend on c for these negative
outgoing paths. Consequently no differentiable remaining component
can cancel (5).

More concretely, for sufficiently small positive epsilon, the complete
four-score has the finite midpoint gain

    F(c0+epsilon)+F(c0-epsilon)-2F(c0)
       =(u+6-c0)j_a(c0)epsilon+o(epsilon)>0.            (6)

Both modified princess paths are legal. At least one has a strictly
larger payoff. Hence the graph law cannot have this proposed ordinary
incoming/outgoing junction as an upper best response when the column
is positive and all other components have differentiable scores there.

This is a complementarity obstruction. Finding a lower monster minimum
on `s=S(v)` alone does not yield a saddle. A surface `s=S(z,v)` depending
on the initial start, a zero column, or an explicitly opposing
nondifferentiable contribution requires a different analysis. No claim
is made that this excludes those possibilities.

## 3. Exact physical verification

Run `verify_free_second_inward.py`. It passes 1,576 rational checks:

* 448 first-contact identities, including initial equality, zero middle
  legs, and second turn s=1;
* 52 complete physical integrals over moving second-turn surfaces,
  partitioned into 1,068 independent capture cells;
* four exact one-sided derivative jumps and four strict finite midpoint
  gains, for constant and nonconstant positive densities, and for both
  curved and unit-outward initial prefixes.

The physical reference computes actual segment intersections and
integrates them on independently partitioned rational polygons. The
derivative calculation is exact polynomial interpolation, not a small
floating difference. The test graph S is affine decreasing to allow
rational integration; the local proof of (5)-(6) does not assume a
globally affine graph.
