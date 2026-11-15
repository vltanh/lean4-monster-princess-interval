# A two-turn response that reaches the last incoming wave

Use the ordered five-leg law and notation of
`FIRST_WAVE_TWO_TURN_RESPONSE.md`. Assume the first wave is separated from
zero, the peak inequalities exclude early absorption, and `C2<=1`.

Choose

```text
0 <= x < min(1,inf A2),       -x <= v <= x,
s >= max(1,sup A2),          s-v < 2.
```

The monster vertices are again

```text
(0,x), ((x+v)/2,(x-v)/2), ((s+v)/2,(s-v)/2),
(s+1,-1), (s+3,+1).
```

Write `D1(z)=Pr(C1>=z)` and `D2(z)=Pr(C2>=z)`, and define

```text
r=A(x),        b=B1(x),       d1=D1(v),       d2=D2(v),
l=max(A(-v),min(b,d1)),       m=max(l,b),
h1=max(r,d1),                h2=max(r,d2).
```

The order hypotheses imply `l<=m<=r<=h1<=h2<=1`. In particular,
`A(-v)<=D1(v)` follows from `C1>=-a`, and `B1(x)<=A(x)` follows from
`A1>=a`.

**Exact formula.** For the continuous symmetric part of the princess law,

```text
4J = 2(s+1)
     + integral_0^l    (s+C2(q)) dq
     + integral_l^m    (x+C1(q)) dq
     + integral_m^r    (x-a(q)) dq
     + integral_r^h1   (A1(q)+v) dq
     + integral_h1^h2  (A2(q)+v) dq
     + 2(s+3)(1-h2).                                  (1)
```

A stationary endpoint pair has payoff `s+2`; thus a total endpoint mass
lambda changes J to `(1-lambda)J+lambda(s+2)`.

## Capture classes

The initial leftward monster leg keeps U=x. Its radial CDF decreases from
r to l. Since `x<inf A2`, the second incoming wave has not yet contributed
to this trace. Ranks between l and m are caught on the first return
outward, at `(x+C1)/2`. Ranks between m and r are caught on the initial
outward leg, at `(x-a)/2`.

The short rightward monster leg keeps V=v and raises U from x to s.
For previously uncaptured ranks above r, those below d1 can be caught on
the first incoming wave, at `(A1+v)/2`. Those above d1 but below d2 have
already passed that wave and are caught on the second incoming wave, at
`(A2+v)/2`. This gives the intervals `(r,h1)` and `(h1,h2)`.

The remaining low ranks below l are caught on the final outward leg when
the monster next moves left: their capture time is `(s+C2)/2`. The high
ranks above h2 stay above that descending monster and are caught at the
final positive endpoint, at `s+3`.

Every negative rank is captured at the first negative endpoint, at `s+1`.
The argument is the same as in the first-wave note: `s>=1>=C2` prevents
an earlier crossing after the monster reaches the negative half, and
strict rank monotonicity removes positive-mass equality cases. Averaging
these capture classes proves (1).

All displayed rank endpoints can coincide; empty integrals then vanish.
The strict prefix-peak inequality `s-v<2` matters for the endpoint atom.
At equality, the positive endpoint is visited earlier and its payoff must
be recomputed rather than taken from the generic formula.

## What the bounded negative-C1 test found

A negative outer C1 branch escaped the simple first-wave attack, but the
fitted law was defeated by this last-wave version. The effective attack
used `s=sup A2`, with V close to the minimum C2. Its short outward leg
therefore intercepted both incoming waves, including the ranks protected
by the negative C1 branch.

This identifies a structural problem with keeping all second incoming
characteristics in the narrow strip
`A2(q)=1+1/1000+q/1000000`: the monster can traverse the entire last wave
with very little additional travel. The bounded local fits do not prove
that every law in this class is suboptimal. They also do not identify a
matching candidate. Their role is to reveal the missing all-monster
constraints before attempting equilibrium equations.

For a fixed rational law and s, (1) is piecewise quadratic in x,v on a
finite rational polygonal subdivision. Four exact fixtures in the
continuous-rank package exercise first-wave catches, second-wave catches,
missed high ranks, and both definitions of the lower captured front.
