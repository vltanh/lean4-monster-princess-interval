# An endpoint sweep excludes an all-rank incoming strip above one

Consider positive paths of the three-leg form

```text
p_q(t)=min(1,max(min(a(q)+t,u(q)-t),t-C(q),0)),
```

and their reflections with equal probability. Assume

```text
0 <= a <= 1,   u >= a,   -a <= C <= 1,
u(q) >= U for every q,   1 <= U <= 2.
```

No ordering of these parameters is needed for the following obstruction.
Stationary endpoint-pair atoms may also be included.

**Proposition.** The monster starting at `x=2-U`, moving right to one and
then left to minus one, has expected payoff at most

```text
(U+1)/2 + (1/2) E[max(U-1,(U-a)/2)]
    <= 1/2 + 3U/4.                                    (1)
```

The expectation in the first expression is over the positive rank law.
It is an equality if the reflected princesses have no earlier capture;
this holds when `U>1`, and also when `U=1` with no positive mass at `C=1`.

The first endpoint visit is at time `delta=U-1`. Before that visit the
monster is at `2-U+t`; afterward it is at `U-t`, reaching minus one at
time `U+1`.

If `a<=2-U`, put `t_*=(U-a)/2`. Then `t_*>=delta`, and `u>=U` implies
that the initial outward leaf `a+t` remains below the inward leaf `u-t`
up to `t_*`. The inequality `C>=-a` makes the final outward leaf no larger
than `a+t` there. Thus this princess is caught on its initial outward leg
at `t_*`. Its position at the meeting is `(U+a)/2<=1`.

If `a>=2-U`, at time delta both `a+delta` and `u-delta` are at least one.
The princess is therefore at one when the monster first reaches it, and
is captured at delta. Hence the positive capture time in both cases is

```text
T_+(q)=max(U-1,(U-a(q))/2).                            (2)
```

Every negative princess is captured by the final endpoint time `U+1`.
More specifically, the descending monster has position `U-t`. Until time
`1+C`, a negative princess has position at most `C-t`, because the positive
path is at least `t-C` before endpoint clipping. From time `1+C` onward it
is at minus one. If `U>C`, neither case permits an earlier meeting.

Since `a>=0` and `U<=2`, both terms in the maximum in (2) are at most
`U/2`. Averaging the positive and negative capture times proves (1).
A stationary endpoint pair is caught at times `U-1` and `U+1`, with pair
average U, which is also at most the bound in (1).

## Consequence for the proposed singular family

The family

```text
u(q)=1+epsilon+epsilon^2 q,
C(q)<=1-epsilon
```

has `U=1+epsilon`. Its unrestricted lower guarantee is therefore at most
`5/4+3epsilon/4`, tending to `5/4` as epsilon tends to zero. This remains
true with arbitrary distributions of a and C, arbitrary endpoint-pair
mass, early endpoint visits, and either clipping or permanent absorption
at the first endpoint visit.

Thus synchronizing *all* incoming characteristics immediately above one
cannot explain the existing interval lower strategy. A viable ordered
three-leg candidate needs a substantial earlier incoming branch, or a
different path structure. This is an analytic structural exclusion, not a
numerical search failure or a tighter bound on the original game.
