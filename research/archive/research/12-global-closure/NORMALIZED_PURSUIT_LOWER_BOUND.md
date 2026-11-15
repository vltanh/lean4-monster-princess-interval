# Exact pursuit lower bounds for normalized record pricing

Research proof, 2026-11-13.

This note justifies the additional pruning in the native normalized-bank
oracle. It concerns exact finite path pricing. The unrestricted conclusion
still uses [clock atomization](LEFT_FLOOR_CLOCK_ATOMIZATION.md),
[physical-bank normalization](NORMALIZED_GRID_BANK_PRICING.md), and the
[quantitative transfer](EFFECTIVE_FINITE_UPPER_REDUCTION.md).

Use integer physical coordinates: arena endpoints are `−R,+R`, where
`R=2n`, and time two is `C=4n`. One tick has physical duration `1/(2n)`.
Let `p(j,k)=1+sgn(k)g(j,abs(k))`, with center price one. Multiply all prices
by a common positive integer denominator in the implementation.

At a nonterminal prefix `(j,k)`, let `l,r` be the two history minima before
including the current vertex. Both clocks are still alive: the oracle
finishes a deterministic sweep as soon as either endpoint has been visited.

## 1. One clock: direct pursuit is an exact relaxation

For the negative-endpoint clock, compare any continuation with the direct
left sweep `x(s)=k−s`, until it reaches `−R`. At every common time, the
direct sweep is no farther right than the competing continuation. Its
nodal price is therefore no larger by spatial monotonicity.

Moreover, along the direct left sweep the signed price is nonincreasing:
one light coordinate is fixed and the other increases. Consequently its
price at elapsed time `s` is no larger than **every earlier price** of the
competing continuation after the prefix, not just the price at time `s`.
After taking the minimum with the entry record `l`, its running record is
no larger than the competitor's record. It also reaches its endpoint no
later. Its integrated record cost is thus a lower bound for the remaining
cost of this one clock. The right-endpoint clock is the reflection.

Adding the two independently minimized pursuit costs remains a lower bound.
The two relaxed clocks are allowed to use different physical continuations;
this enlarges the feasible set only for the lower-bound calculation.

This basic bound requires only the nodal cone inequalities. It does not
require outward-after-two or sticky endpoint constraints.

## 2. A stronger bound for outward-after-two profiles

Assume the exact outward identity of `Qout`. Put `d=C−j`. For each clock,
price its direct pursuit only up to time `C` or its own endpoint, whichever
comes first. Denote the sum of these two independent prefix costs by `A`.
The scoring intervals included here end strictly before time `C`.

The following are lower bounds on the actual two records at time `C`,
where an inactive clock is assigned record zero:

\[
\ell_0=
\begin{cases}
0,&k+R\le d,\\
\min(\ell,p(C,k-d)),&k+R>d,
\end{cases}
\]

\[
r_0=
\begin{cases}
0,&R-k\le d,\\
\min(r,p(C,-k-d)),&R-k>d.
\end{cases}
\]

If an endpoint is reachable **by** time `C`, including equality, zero is
a valid lower bound whether or not the actual continuation uses that option.
Otherwise the clock is necessarily alive at `C`; Section 1 compares its
whole history with the direct pursuit's price at `C`. The time-`C` node is
included in this record bound, but not in the preceding scoring sum `A`.

For a center-by-two path, the exact `Qout` identities freeze both actual
records after time two until their respective endpoints. With records
`a,b` and time-two position `y`, the least remaining raw tick cost is

\[
G(y,a,b)=\min\left\{
(R-y)b+(3R-y)a,
\ (R+y)a+(3R+y)b
\right\}.
\]

This formula remains valid with inactive records set to zero. It is
coordinatewise nondecreasing in `a,b`, since every endpoint time coefficient
is nonnegative. Replacing the actual records by `ell_0,r_0` therefore gives
a lower bound.

The time-two position lies in the ordinary reachable interval

\[
I=[\max(-R,k-d),\min(R,k+d)].
\]

If the center has not yet been visited, a feasible continuation must first
reach it. When `abs(k)>d` the state is infeasible. Otherwise the stronger
interval is

\[
I=[\max(-R,-(d-|k|)),\min(R,d-|k|)].
\]

For fixed records, `G` is the minimum of two affine functions of `y`, hence
is concave. Its minimum over the interval `I=[u,v]` is attained at one of
the endpoints. The final admissible remaining-cost bound is therefore

\[
\boxed{B=A+\min\{G(u,\ell_0,r_0),G(v,\ell_0,r_0)\}.}
\]

The two terms price disjoint time intervals. Although their separate
minimizers need not agree, each term is a lower bound for the corresponding
part of every actual continuation, so they can be added.

## 3. Exact evaluation and pruning

All direct-left prices on a characteristic `j+k=constant` form a
nonincreasing sequence. The implementation precomputes its exact cumulative
sums. A binary search finds the single crossing of an entry record, so
`sum min(record,price)` on any segment takes logarithmic time. The reflected
clock uses the same characteristic arrays. There are only quadratically
many stored prices in the grid parameter.

The oracle checks the outward identities exactly before using Section 2.
If they fail, it uses only the basic independent-pursuit bound of Section 1.
Thus an arbitrary isotone input is never silently treated as an outward
profile.

Every incumbent is the exact price of a complete legal normalized physical
path. Initial direct endpoint tours supply such incumbents before branching.
If accumulated prefix cost plus `B` is at least the incumbent, that state
cannot improve the minimum. When several output paths are retained, the
comparison uses the largest retained complete-path price once the requested
number of slots is full; this still preserves the exact minimum. Equal-cost
alternative paths need not all be listed.

No floating comparisons or rounding enter the bound. Integer range checks
precede the search. The supplied independent regression compares the result
with exhaustive Fraction enumeration on 72 small profiles, including 16
nontrivial outward profiles, and a separate record DP on known certificates
through `n=6`. It enumerates 29,448 normalized paths and independently checks
1,006 returned routes. A larger `n=128` example also agrees exactly with the
previous computation without this pruning. These are implementation checks;
the inequalities above justify pruning every legal continuation.
