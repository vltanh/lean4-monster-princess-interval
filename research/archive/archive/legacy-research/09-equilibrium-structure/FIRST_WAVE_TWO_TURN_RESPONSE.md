# A two-turn response that captures both fronts of the first wave

Consider a continuous ordered five-leg law with parameters
`a(q), A1(q), C1(q), A2(q), C2(q)`, uniform rank q, and equal reflection
probabilities. Use the no-early-peak hypotheses of the continuous-rank
engine and the first-wave separation `inf A1>=sup C1`. The hypotheses
below also separate the second incoming wave from C2, so there is no
positive-mass atom at zero. Write

```text
A(z)=Pr(a<=z),      B1(z)=Pr(A1<=z).
```

An optional stationary endpoint pair has total mass lambda; all expectations
below first refer to the continuous part, before that atom is added.

## 1. A finite response family with an explicit payoff

Choose x,v,s satisfying

```text
0 <= x < 1,       -x <= v <= min(x, inf C1),
max(1,sup A1) <= s < inf A2,       s-v < 2.
```

The monster has vertices

```text
(0,x),
((x+v)/2,(x-v)/2),
((s+v)/2,(s-v)/2),
(s+1,-1),
(s+3,+1).
```

It first moves left, briefly right, then left to minus one and finally
right to plus one. Its initial characteristic route is

```text
(U,V)=(x,-x) -> (x,v) -> (s,v).
```

Put `r=A(x)` and `l=max(A(-v),B1(x))`. The inequalities `A1>=a` and
`-v<=x` imply `0<=l<=r<=1`.

**Exact formula.** Its continuous symmetric payoff J satisfies

```text
4J = 2(s+1)
     + integral_0^l   (s+C1(q)) dq
     + integral_l^r   (x-a(q)) dq
     + integral_r^1   (A1(q)+v) dq.                    (1)
```

The formula is independent of C2. Adding stationary endpoint-pair mass
lambda changes the payoff to `(1-lambda)J+lambda(s+2)`.

### Capture proof

For ranks `l<q<r`, we have `a(q)<x`, `A1(q)>x`, and `a(q)>-v`.
Their first outward leg meets the monster's initial leftward leg at
`(x-a(q))/2`, before the monster's first turn.

For ranks `q>r`, the princess starts above the monster and remains above
it on that first leftward leg. The short outward monster leg then catches
her first incoming leg at `(A1(q)+v)/2`. This time lies on that monster
leg because `x<A1(q)<=s`. The inequality `C1(q)>=v` ensures that the
princess's next outward leg has not passed above the encounter. The second
incoming wave cannot interfere, because `A2(q)>s`.

For ranks `q<l`, either `A1(q)<x` or `a(q)<-v` prevents capture on the
first leftward leg. They stay below the monster on its short outward leg.
On the following leftward leg, whose U characteristic equals s, they are
caught on the first return outward at `(s+C1(q))/2`. Again `A2(q)>s`
prevents the later wave from changing this encounter, and `C2>=C1`
makes the final outward leaf no higher.

Every negative princess is captured at time `s+1`, apart from null
boundary ranks. Before the monster crosses zero its position is positive.
Afterward its position is `s-t`; since `C2<=1<=s`, a negative princess is
strictly below this line until the endpoint, or is already waiting there.
The strict decrease of C2 makes any equality `C2=s=1` a null rank.

These four capture classes give (1). All quantile-boundary equalities have
zero probability because the parameter functions are strictly monotone.
The stationary positive endpoint is not visited during the two-turn prefix,
because `s-v<2`; hence the endpoint-pair capture times are `s+1,s+3`.

## 2. A particularly effective choice

Suppose additionally

```text
inf A1 < 1,
inf C1 >= -inf a,
max(1,sup A1) < inf A2.
```

Choose

```text
x=inf A1,       v=-inf a,       s=max(1,sup A1).
```

The usual peak inequality `a+A1<=2` ensures that the prefix stays inside
the arena; a strict peak is needed if endpoint mass is present. Both
`A(-v)` and `B1(x)` are zero, so l=0. **Every positive rank is captured
during the first two legs**, before the second incoming wave can help:

```text
T_+(q) = (x-a(q))/2       if a(q)<=x,
         (A1(q)-inf a)/2  if a(q)>x.
```

This is a useful exact constraint for candidate fitting. A generic floating
search over turn positions can miss it when `sup A1` and `inf A2` are
separated by a very narrow strip. The explicit parameters land in the
required strip without a spatial or temporal grid.

The bounded fixed-wave experiment produced local laws with nearly equal
C1 and C2 and a positive outer C1 value. All were strongly defeated by this
response. Those numerical fits do not exclude the whole five-leg class.
They identify the first-wave issue that final-suffix changes alone cannot
repair. An outer branch with `inf C1 < -inf a` escapes this particularly
simple all-positive capture argument; its actual response must still be
checked.

## 3. Stationarity when the lower missed front moves

Within a smooth regime where `l=A(-v)>B1(x)`, differentiate (1) with
respect to v. Since `a(l)=-v`, the stationary equation is

```text
1-A(x) = A'(-v) [s-x+C1(l)-v].                        (2)
```

When `l=B1(x)>A(-v)`, the derivative of `4J` with respect to v is simply
`1-A(x)>=0`. Thus a candidate can be tested at the boundary where the
lower missed front first changes, rather than relying only on a generic
multivariate optimizer.

For piecewise-affine parameter functions, (1) is piecewise quadratic in
(x,v) on a finite rational polygonal arrangement when the law and s are
rational. This is a small explicit instance of the general finite-quadratic
response theorem. The engine's exact tests check (1) on both choices of
the lower-front branch.
