# Removing unproductive inward-response turns

The second outward turn of an initial-inward monster must be free. An
active route cannot continue outward across a positive-length interval
that captures no additional initial ranks. This observation gives an
exact finite attack against an ordinary incoming completion, even after
its initial outward run has been replaced by a curved arc.

The results below concern ordered nonnegative princess paths and their
fair reflection. The pointwise comparisons do not require ordinary
princess waves, smooth CDFs, or a bound on the princess's number of turns.
The stronger quantitative comparisons state their endpoint hypotheses
separately. They do not supply a matching law or the game's value.

## 1. The free-second-turn route

Write `alpha_q(U)` and `beta_q(V)` for the first inverses of `t+p_q(t)`
and `t-p_q(t)`. For

\[
0<a<1,\qquad -a\le v<a,\qquad a\le s\le v+2,
\]

let `I_s(a,v)` have vertices

\[
(0,a),\quad ((a+v)/2,(a-v)/2),\quad
((s+v)/2,(s-v)/2),\quad(s+1,-1),\quad(s+3,1).
\]

Its cost is `CI_s(a,v)`. Set

\[
A=\Pr(p_q(0)\le a),\quad L=R_<(a,v),\quad
M_s=\max\{A,R_{\le}(s,v)\}.
\]

The positive ranks split into four capture groups: ranks below `L`
are caught at `alpha_q(s)`; ranks from `L` through `A` at
`alpha_q(a)`; ranks from `A` through `M_s` at `beta_q(v)`; and
ranks above `M_s` at `beta_q(s+2)`. Initial equality is capture at zero
and must be retained in the second group. Every negative reflected path
is caught at `beta_q(s)`. The condition `v<a` keeps the initial inward
turn strictly above the center; it prevents an unrecorded center-atom
capture on that first leg.

These are individual first contacts, so the partition also handles
incoming atoms and coincidence intervals with the stated strict/closed
traces. An initial equality atom contributes the same zero to both routes
in every comparison below.

## 2. Exact deletion of a final outward plateau

Take `a<=s0<s1<=v+2`. Suppose

\[
M_{s_0}=M_{s_1}=M.                                      \tag{1}
\]

Then `I_s0` captures every princess path no later than `I_s1`.
The groups captured at `alpha(a)` and `beta(v)` are unchanged.
All other capture times decrease by monotonicity of their first inverse.
The exact mean difference is

\[
\begin{aligned}
2(CI_{s_1}-CI_{s_0})
={}&\int_0^L[\alpha_q(s_1)-\alpha_q(s_0)]\,dq\\
 &+\int_0^1[\beta_q(s_1)-\beta_q(s_0)]\,dq\\
 &+\int_M^1[\beta_q(s_1+2)-\beta_q(s_0+2)]\,dq .       \tag{2}
\end{aligned}
\]

Both characteristics are 2-Lipschitz. Increasing either inverse threshold
by `s1-s0` therefore increases its first hitting time by at least
`(s1-s0)/2`. Consequently

\[
CI_{s_1}-CI_{s_0}\ge
{(s_1-s_0)(L+2-M)\over4}>0.                          \tag{3}
\]

No endpoint-absorption assumption is needed for this strict improvement.

For the fixed-second-turn face `s1=1`, suppose additionally that
`beta_q(1)=2` almost surely and that every princess stays at `+1` after
time two. Then `beta_q(s0)<=1+s0` and
`beta_q(s+2)=s+3` for `s>=0`. Dropping the nonnegative first integral
in (2) gives the stronger bound

\[
CI_1-CI_{s_0}\ge{(1-s_0)(2-M)\over2}>0.              \tag{4}
\]

### Consequence for an ordinary incoming completion

An ordinary incoming characteristic followed by a final unit outward leg
produces a column plateau once its last middle-capturable rank has turned
outward. If that transition is strictly before `U=1`, choose `s0<1`
inside the plateau. Condition (1) then holds, and (4) is a legal strict
finite attack on the proposed fixed-`U=1` response.

Thus changing only the initial arc cannot make that completed law match
an active `I_1` or positive-M2 `I_1(a,-a)` component. Either its incoming
field must continue to vary up to the turn, or its active second turn must
move earlier. A small positive plateau is still excluded; its size changes
the attack's amount, not its strictness. This statement does not exclude
all curved incoming fields or all free-second-turn laws.

## 3. Direct-left domination and a quantitative support gap

Let `Cell(a)` be the route starting at `+a`, visiting `-1`, and then
`+1` directly. This is `I_a(a,v)` after removing its zero outward leg,
independently of `v`.

If `B=R(1,v)<=A`, then `M_a=M_1=A`. Section 2 proves pointwise
domination by `Cell(a)`. Thus this entire region is inactive in a matched
inward sheet once the negative-M1 inequality is controlled. A transport
plateau does not provide an exception.

Under the endpoint hypotheses of (4), there is a stronger necessary
condition even when `B>A`. Put

\[
t_1=(a+v)/2,\qquad \Delta=(B-A)_+.
\]

The negative reflected copy is captured at time two under `I_1` and
by time `1+a` under `Cell`, a loss of at least `1-a`. Every initially
lower positive path is captured earliest by direct left travel, so it
cannot offset that loss. The initially higher positive ranks missed by
the middle segment lose exactly `1-a` on the final right sweep. Only
the `Delta` ranks caught on the middle segment can improve; their gain
is at most `3+a-t1` each. Hence

\[
CI_1-Cell\ge
{(1-a)(2-A)-(4-t_1)\Delta\over2}.                    \tag{5}
\]

An equality `CI_1=Cell` therefore requires

\[
B-A\ge{(1-a)(2-A)\over4-(a+v)/2}>0.                 \tag{6}
\]

In deficit coordinates `x=1-a`, `y=1+v`, `r(x)=1-A(a)`,
`e(y)=1-R(1,v)`, this is

\[
r(x)-e(y)\ge{2x[1+r(x)]\over8+x-y}.                 \tag{7}
\]

It supplies a nonzero inactive strip before the rank boundary `B=A`.
The first-turn corner bound in `CURVED_TERMINAL_SOURCES.md` uses an
additional row equality and can be sharper there. Neither bound asserts
that every point beyond the strip is active.

## 4. A negative M3 return that captures no new rank

Consider the opposite-half two-turn route from
`TWO_INTERIOR_TURN_CDF.md`, starting at `-z`, first turning at `U=s`
and then at `V=t`, with `z<=s<=t`. Write

\[
A=A(z),\quad B=R(s,z),\quad D=R(t,s).
\]

If `D<=A`, its leftward excursion catches no new negative rank. The
direct negative-M1 route from `-z` then dominates it pointwise.
The exact cost difference is

\[
\begin{aligned}
2(C_3(-z;s,t)-Cell(z))
={}&\int_B^1[\beta_q(t)-\beta_q(z)]\,dq\\
 &+\int_A^1[\beta_q(t+2)-\beta_q(z+2)]\,dq\ge0 .      \tag{8}
\end{aligned}
\]

Reflection makes the direct-M1 cost equal to the notation `Cell(z)`
used above. Formula (8) retains exact endpoint values in `B,D`; an
endpoint turn cannot be tested using an interior CDF limit.

This rules out the proposed early negative-M3 corner `z,s,t -> 1` for
the current endpoint-absorbed class. Indeed, `beta_q(1)=2` implies
`p_q(1)>0` almost surely. For `z<=s<=t<=1`, the speed bound gives

\[
R(t,s)\le\Pr\{p_q(1)\le1-s\}\longrightarrow0
\quad\text{uniformly as }z\uparrow1.
\]

If `A(1-)>0`, then `D<A(z)` throughout a sufficiently small such
corner. Every genuine return there is therefore dominated by M1.
The zero-duration reversal at `s=t=z` is merely an M1 duplicate.

With the stronger hypothesis of endpoint arrival at `sigma_q<2` almost
surely, the same conclusion extends to arbitrary interior return turns
with `V>=z` near one, since

\[
R(U,V)\le\Pr\{\sigma_q\ge1+z\}\longrightarrow0
\quad(V\ge z,\ U-V<2).
\]

This uses the Lipschitz lower bound
`p_q(time)>=1-(sigma_q-time)>time-z` before absorption. The strict
arrival assumption is stated explicitly; mere absorption *by* time two
does not imply it.

The surviving route enlargement is consequently the **same-half**
initial-inward family with a free second turn. It is not a
center-crossing negative-M3 corner disguised by a limit.

## 5. Independent exact checks

Run

```sh
python -B packages/interval_turn_sheet/verify_inward_dominance.py
```

The verifier passes **12,513 exact Fraction checks**, including 288
quantitative support-gap comparisons, 288 strict earlier-second-turn
attacks, 120 strict inactive-rank costs, and 81 negative-M3 empty-return
comparisons. The other checks use direct polygon intersections to compare
capture times individually on both signs. Fixtures include initial speeds
`1/3`, `2/3`, and `1`, with actual center waits and negative outgoing
characteristics. Thus the turn attack is tested after non-unit initial
motion has already replaced the ordinary unit run.

These checks establish the finite comparisons and validate their capture
classes. They do not instantiate the full free-second-turn field or an
unrestricted saddle certificate.
