# Uniform all-count single-return dominance outside a narrow front strip

Date: 2026-11-12. **New exact terminal-center theorem, not an unrestricted game value or an equilibrium CDF.**

## Result and scope

Consider the saved terminal affine wedge in LOW_SURPLUS_ALL_HINGES_EXCLUSION.md:

\[
R(U,V)=kU-\ell V+c,\quad Z(t)=(k-\ell)t+c,
\quad k=\frac{655898601421}{62500000000},
\quad\ell=\frac{820954217}{12500000000},
\quad d=k-\ell,\quad b=15/16.
\]

Let \(H=b-t\in(0,1/16]\). Start from a balanced center captured-rank
state \(n=Z(t)+y\), where \(0\le y<kH\), within the certified affine
inverse/exterior gates. Fix the **last return exactly at \(b\)** and
exclude initial waiting, earlier front resets, and competing exterior
exits from this component, exactly as in the existing productive-chain
energy theorem.

**Theorem (all-count one-return strip).** If
\[
\boxed{\frac25H\le y<kH,}
\]
the single maximal center tent of duration \(H\), returning at \(b\),
strictly beats every *finite productive chain with at least two returns*
ending at \(b\). The same comparison holds against terminal-Zeno
sequences of returns accumulating at \(b\), subject to the existing
rank-band limit assumptions. **No turn-count cutoff is imposed.**

The preceding high-surplus theorem required \(y\ge 3kH/8\), i.e.
\(y/H\ge3.935391608526\). The new threshold is \(y/H=0.4\), improving
the proved one-return strip by a factor of about 9.84 in its threshold.
For each eligible \(H\), **more than 96.18% of the nominal productive
surplus interval** \(0\le y<kH\) is now covered; only
\(0\le y<2H/5\) can require a multi-return comparison in this
prescribed-terminal no-initial-wait sector.

The proof combines the previously established strict short-hinge deletion
with a new all-count Green lower bound and a four-corner rational
certificate. It does not claim that initial waiting or alternative exits
are dominated, that the saved affine law is an equilibrium, or that the
global Princess–Monster value is improved.

## 1. Delete the short hinges

By LOW_SURPLUS_ALL_HINGES_EXCLUSION.md, every finite productive fixed-\(b\)
chain is strictly improved by a shorter legal policy whenever it has a
strict initial, interior, or terminal short hinge. Repeatedly delete such
hinges. A remaining chain either has one return or is hinge-free.
In particular, with
\[
A=k/8-\ell/2,\qquad
dh_1\ge y,\quad dh_j\ge\ell h_{j-1},\quad
h_j\ge0,\quad\sum_{j=1}^m h_j=H,
\]
its full excess energy for \(m\ge2\) is
\[
E_y(h)=A\sum_jh_j^2-\frac\ell2\sum_{j<m}h_jh_{j+1}
-\frac{3\ell}{2}h_m-\frac y2h_1-\frac{y^2}{8k}.       \tag{1}
\]
For the single return, if \(y\le dH\), the exact formula is
\[
E_y(H)=AH^2-\frac{3\ell}{2}H-\frac y2H-\frac{y^2}{8k}.
                                                               \tag{2}
\]
The case \(y>dH\) is covered directly by the previous high-surplus
all-hinge theorem.

## 2. A uniform two-source Green lower bound

Define the algebraic number and constants
\[
r=\ell/k,\quad
\theta=\frac{1-\sqrt{1-8r}}{1+\sqrt{1-8r}}\in(0,1),\quad
C_0=\frac{\ell}{4\theta},\quad
\alpha=\frac{\theta y}{\ell},\quad\gamma=3\theta.
\]
As in INFINITE_TURN_RENEWAL.md, the \(h\)-dependent part of (1) is
\[
C_0\left(h^{\mathsf T}K_mh-2\alpha h_1-2\gamma h_m\right),
\]
where \(K_m\) has diagonal \(1+\theta^2\) and neighboring
off-diagonal entries \(-\theta\). It is strictly positive definite.

For every \(m\ge2\), completing the square without enforcing any
duration/productivity constraints gives
\[
h^{\mathsf T}K_mh-2(\alpha e_1+\gamma e_m)^{\mathsf T}h
\ge-(\alpha e_1+\gamma e_m)^{\mathsf T}
K_m^{-1}(\alpha e_1+\gamma e_m).
\]
The exact inverse boundary entries are
\[
(K_m^{-1})_{11}=(K_m^{-1})_{mm}
=u_m=\frac{1-\theta^{2m}}{1-\theta^{2m+2}}<1,
\]
\[
(K_m^{-1})_{1m}
=v_m=\frac{\theta^{m-1}(1-\theta^2)}
           {1-\theta^{2m+2}}<\theta
\quad(m\ge2).
\]
Both source coefficients are nonnegative. Therefore every hinge-free
multi-return chain, regardless of count or active duration interfaces,
satisfies
\[
\boxed{
E_y(h)\ge
-\frac{9\ell\theta}{4}
-\frac{3\theta^2y}{2}
-\frac{\theta y^2}{4\ell}
-\frac{y^2}{8k}.}                                      \tag{3}
\]

Subtracting the actual one-return energy (2) yields the sufficient
criterion
\[
E_y(h)-E_y(H)\ge-G(H,y),                                \tag{4}
\]
where
\[
\boxed{
G(H,y)=AH^2-\frac{3\ell H}{2}+\frac{9\ell\theta}{4}
+y\left(\frac{3\theta^2}{2}-\frac H2\right)
+\frac{\theta y^2}{4\ell}.}                            \tag{5}
\]
Thus \(G(H,y)<0\) rules out **all** \(m\ge2\) at once.

## 3. The four-corner exact certificate

Let \(H_1=6\ell/(k-2\ell)\), the exact one-return/second-return
threshold in FRONT_CHAIN_QUADRATIC_SOLUTION.md, and \(H_{\max}=1/16\).
For the saved constants,
\[
0<H_1<H_{\max},\quad
0<2/5<3k/8<d,\quad
\theta<\theta_+=321/25000.
\]
The last inequality is verified *rationally*: the function
\(q(x)=x/[2(1+x)^2]\) increases for \(0<x<1\), and
\[
q(321/25000)>\ell/k=q(\theta).
\]

Because every coefficient of the \(\theta\)-dependent terms of (5)
is nonnegative for \(y\ge0\), replacing \(\theta\) by the rational
upper bound \(\theta_+\) gives \(G(H,y)\le G_+(H,y)\).

On the band
\[
H_1\le H\le H_{\max},\qquad
(2/5)H\le y\le(3k/8)H,
\]
\(G_+\) is convex in \(y\). At either boundary \(y=cH\), it is the
quadratic polynomial
\[
G_+(H,cH)=
\left(A-\frac c2+\frac{\theta_+c^2}{4\ell}\right)H^2
+\left(-\frac{3\ell}{2}+\frac{3\theta_+^2c}{2}\right)H
+\frac{9\ell\theta_+}{4}.
\]
Its leading coefficient is positive for both
\(c=2/5\) and \(c=3k/8\); hence each boundary expression is convex
in \(H\) and cannot exceed the larger endpoint value.

All **four** rational endpoint checks satisfy the strict inequality
\[
\boxed{G_+(H,cH)<-1/125000}
\]
for \(H\in\{H_1,1/16\}\) and
\(c\in\{2/5,3k/8\}\).
There are no floating-point or sampled-domain steps here:
the exact inequalities and the two convexity coefficients are
verified with Python's standard-library Fraction arithmetic in
packages/interval_turn_sheet/verify_single_return_outer_strip.py.

The two nested convexity arguments therefore prove
\[
G(H,y)\le G_+(H,y)<-1/125000
\]
on the *entire* band, which gives a positive **uniform absolute energy
gap** between a no-hinge \(m\ge2\) chain and the one-return policy.

## 4. Complete the all-surplus partition

There are three cases.

* If \(0<H\le H_1\) and \(y\le dH\), the exact one-source front
  theorem gives \(Q_0(h)\ge Q_0(H)\) for every duration word of sum
  \(H\), across **all counts**. Adding the off-front source
  \(-yh_1/2\) can only favor the one-return policy because
  \(h_1\le H\). Formula (2) follows. If \(y>dH\), apply the
  previous high-surplus theorem instead.
* If \(H_1<H\le1/16\) and \(2H/5\le y\le3kH/8\),
  the strict four-corner argument above applies; note \(y<dH\),
  so (2) is exact.
* If \(y\ge3kH/8\), apply HIGH_SURPLUS_SINGLE_RETURN.md Theorem 1,
  which already includes all positive-count and hinge patterns.

The earlier short-hinge deletion covers all remaining finite productive
chains in the first two cases. Therefore a strictly better multi-return
chain cannot exist for any \(y\ge2H/5\).

For a countably infinite productive sequence accumulating only at \(b\),
collapse the tail after return \(t_N\) into a final maximal tent ending
at \(b\). Productivity of the old chain implies this replacement is
productive. The original rank-band estimate from
HIGH_SURPLUS_SINGLE_RETURN.md bounds the cost difference by
\((b+3)k(b-t_N)\to0\). Apply the finite-chain comparison to the collapsed
route, and pass to the limit. This covers terminal Zeno; it does **not**
cover an accumulation at an earlier front reset followed by a new phase.

## 5. Impact on the unrestricted game

This removes the all-count, no-initial-wait productive fixed-terminal
optimization for the entire outer strip \(y\ge2H/5\).
The only possible multi-return competition in this component is now
the very narrow front strip \(0\le y<2H/5\). At the widest
\(H=1/16\), that means \(0\le y<1/40\).

This is a genuine analytic reduction in the Monster response problem.
It **does not give either player's optimal mixed-strategy CDF**, because
initial center waits/front resets, earlier or later exterior exits,
other initial starts, and the matching global Princess law remain
unresolved. The unrestricted game's previously certified upper and
lower values are unchanged.

## Reproduction

Run: python packages/interval_turn_sheet/verify_single_return_outer_strip.py

All four endpoint signs, strict margin, required convexity coefficients,
and algebraic enclosure of \(\theta\) use exact Fractions. No Lean
compilation or CI is claimed.
