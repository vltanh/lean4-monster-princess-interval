# Initial affine motion cannot support both boundary contact families

Research proposition independently reviewed by the root and verification
agents, 2026-11-14.

This is a conditional obstruction to an exact finite P1 equilibrium
template. It uses a local physical comparison and does not assume the
historical endpoint inverse identities `beta(1)=2`, `beta(3)=4`.

## 1. Two Monster routes with a common future

Let `g(s)=M2(s,1)` be the fair reflected pair whose positive member has
vertices

\[
 (0,s),\quad
 ((1-s)/2,(1+s)/2),\quad
 (2,-1),\quad(4,1),\qquad 0<s<1.
\]

Let `I(s+δ,-s)` be the fair pair that first moves left from `s+δ` to
`s+δ/2` at time `δ/2`, then follows exactly the same future as `g(s)`.
Require `0<δ<1-s`. These routes join at time `δ/2` and never separate
afterward.

Consider a fair signed ordered Princess law, parametrized locally by
initial positive radius `b` with initial CDF `A`. Assume no atom at the
old start `s`. Before the join, the speed bound alone shows that neither
route captures any positive Princess with `b<s` or `b>s+δ`. Such a
Princess stays respectively behind or ahead of both prefixes. Both
reflected prefixes remain negative, so they capture no positive Princess
before the join.

Therefore all payoff differences come from the initial-radius band
`(s,s+δ]`. If `T_old(b),T_new(b)` denote the positive-side capture times,
the exact expected-payoff difference is

\[
 2\,[C_I(s+\delta,-s)-C_g(s)]
   =\int_{(s,s+\delta]}
          [T_{\rm new}(b)-T_{\rm old}(b)]\,dA(b).
 \tag{1}
\]

An atom at `s` would create an additional term and cannot be discarded.
All statements below are on an atom-free initial band.

## 2. A uniform initial unit run gives a strict attack

Suppose the Princess paths with `b` in a neighborhood of `s` satisfy

\[
                   p_b(t)=b+t,\qquad 0\le t\le\tau,
 \tag{2}
\]

for one common `τ>0`. Shrink `τ` so that the old Monster is still on its
outward leg up to `τ`, and take `δ/2<τ`.

For every `b` in `(s,s+δ]`, the old path cannot catch her before `τ`,
whereas the new initial inward leg catches her at

\[
                  T_{\rm new}(b)=\frac{s+\delta-b}{2}
                                  \le\frac\delta2.
\]

If the band has positive mass, (1) gives

\[
 C_I(s+\delta,-s)-C_g(s)
 \le -\frac12\left(\tau-\frac\delta2\right)
               [A(s+\delta)-A(s)]<0.
 \tag{3}
\]

This needs no assumption about the Princess paths after `τ`, their later
turn fronts, or their endpoint arrival times. Thus `g(s)` cannot be an
active best Monster response to a claimed security level on such an
initial band.

## 3. A strictly slower affine initial velocity gives an inactive gap

Now assume instead that on an initial-radius interval the paths have the
common affine initial motion

\[
                   p_b(t)=b+vt,\qquad 0\le t\le\tau,
 \qquad -1\le v<1.
 \tag{4}
\]

Assume the initial density has bounds `0<m<=A'(b)<=M` there. Keep the old
Monster outward up to `τ`, and choose `δ/(1-v)<τ`.

Every Princess in `(s,s+δ]` is caught by the old prefix at

\[
               T_{\rm old}(b)=\frac{b-s}{1-v}
                                \le\frac\delta{1-v}.
 \tag{5}
\]

In the subband

\[
                 s<b<s+\frac{1-v}{4}\delta,
 \tag{6}
\]

the new Monster has not yet caught her at the join. At that time its
position exceeds hers by at least `(1-v)δ/4`, and afterward the common
outward Monster prefix moves faster than she does. Therefore
`T_new(b)>=τ` on (6). On the rest of the full band the crude bound
`T_new>=0` suffices.

Using (1), (5), and the density bounds gives the explicit estimate

\[
 \boxed{
 2[C_I(s+\delta,-s)-C_g(s)]
 \ge \frac{m\tau(1-v)}4\,\delta
       -\frac{M}{1-v}\,\delta^2.}
 \tag{7}
\]

It is strictly positive for all sufficiently small positive `δ`. This
also covers `v=-1`: then the new inward Monster cannot catch any initially
lower member of the band while both move left at the same speed.

If `C_g` is constant with value `c` on an open start interval, set
`s=z-δ` in (7). On any compact subinterval where (4) and the density bounds
hold uniformly, there is a uniform `δ_0>0` such that

\[
                  C_I(z,-z+\delta)>c,
       \qquad 0<\delta<\delta_0.
 \tag{8}
\]

Thus the initial-inward contact family has an actual inactive gap next
to its no-inward-turn boundary. It cannot be flat at `c` arbitrarily close
to that boundary throughout this initial interval.

## 4. Consequence for a finite P1 CDF

Let the initial spatial CDF have positive density on an interval, and let
the spacetime CDF be continuous and affine on finitely many rational or
real polygonal pieces near time zero. At any initial point away from the
finitely many initial mesh breakpoints, a smaller initial-radius interval
and a common positive time interval lie in one affine cell. There the
radial field is

\[
                    R(t,x)=\lambda t+\rho x+d,
                        \qquad\rho>0,
\]

so its ordered quantile trajectories have the common initial velocity

\[
                       v=-\lambda/\rho\in[-1,1].
\]

There are only two possibilities.

* If `v=1`, the strict attack (3) prevents the positive-start M2 family
  from being active at the claimed security value.
* If `v<1` and that M2 family is flat on the initial band, (8) forces an
  inactive initial-inward gap.

Consequently no such finite P1 field can simultaneously have, on a
positive-density open initial band, both a flat active positive-M2 family
and an active initial-inward sheet that reaches `v=-z` at every interior
start. The conclusion does not require a power-law expansion and does
not depend on the later endpoint-tail formulas.

## 5. Relation to the curved initial phase

An immediately curved path with initial tangent one has neither a
positive-length unit run nor a fixed positive slowdown `1-v` near zero.
It can therefore evade both estimates above. The conditional
golden-ratio power balance in `CURVED_INITIAL_POWER_PHASE.md` is consistent
with exactly this escape: under its additional regularity and active-sheet
hypotheses, it selects an initial power `(1+sqrt(5))/2`.

This note does not prove that those two contact families persist in the
unrestricted equilibrium. They may lose activity, acquire a gap, or fail
the stated positive-density assumptions. Accordingly it excludes a finite
P1 template only under the specified contact pattern; it does not exclude
all finite analytic descriptions or solve the global game by itself.
