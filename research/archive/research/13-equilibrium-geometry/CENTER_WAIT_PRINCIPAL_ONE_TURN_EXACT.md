# An exactly solved center-wait / principal one-turn subgame

**Theorem, 2026-11-15.** This is an exact saddle-value computation for the explicitly stated *restricted* strategy classes, **not** an exact value for the unrestricted Princess–Monster game or for the full one-interior-turn Monster class. The Princess has free initial radius and a free center-wait duration; the Monster's interior reversal is restricted to the principal characteristic \(\,t+x=1\,\).

## 1. Legal physical strategy classes

Both players move in \([-1,1]\) with speed at most one, and capture occurs on **first coincidence**, including time zero.

**Center-in/wait/out Princess family \(\mathcal C\).** For \(0\le r\le1,\ d\ge r,\ \eta\in\{-1,+1\}\), and an initial side \(\sigma\in\{-1,+1\}\), the Princess
- starts at \(p(0)=\sigma r\);
- moves inward at unit speed, reaching zero at \(t=r\);
- stays at zero through \(t=d\);
- moves outward at unit speed to the endpoint \(\sigma\eta\), then stays there.

Here \(\eta=+1\) means return toward the starting side; \(\eta=-1\) means exit through the opposite endpoint. Arbitrary probability laws on these paths are allowed. No common departure time, finite support, or independence of \(r,d,\eta\) is assumed.

**Principal one-turn Monster family \(\mathcal P^+\).** For \(a\in[0,1]\), its right-oriented physical path \(m_a\) has successive vertices
\[
(0,a),\quad \left(\frac{1-a}{2},\frac{1+a}{2}\right),
\quad(2,-1),\quad(4,1).
\tag{1}
\]
After reaching \(+1\), it stays there. This is the \(P(a,1)\) family from [bulk contact equations](../12-global-closure/BULK_CONTACT_AND_CUSP_EQUATIONS.md); at \(a=1\), the first leg has zero length and it is the leftward endpoint sweep. The Monster may choose any mixed law on the \(m_a\) and their reflected paths \(-m_a\), with arbitrary orientation probabilities. Its only interior reversal is at \(t=(1-a)/2\), before the mandatory reversal at its first endpoint.

Let \(W_{\mathcal C,\mathcal P^+}\) be this mixed minimax game. We use the fair-reflection convention only in the explicitly constructed certificates: the lower construction handles either Monster orientation separately, and the upper construction handles either Princess orientation separately.

## 2. Exact value

\[
\boxed{\displaystyle
W_{\mathcal C,\mathcal P^+}
 = \frac32-\frac{e^{-1/2}}2
 =1.1967346701436832881981002325\ldots .}
\tag{2}
\]

The Monster optimum is attained by a very simple law: choose \(a\) from
\[
\boxed{\Pr(a=0)=e^{-1/2},\qquad
  \frac{d\Pr(a\in da)}{da}
   =\frac12e^{(a-1)/2}\quad(0<a<1)}
\tag{3}
\]
and independently choose fair reflection. The atom plus density have total probability one.

The Princess has an explicit uniformly approaching family below. No law supported on the center-in/wait/out family **attains** (2): the Monster law (3) makes the payoff of every single such path strictly less than (2), and therefore does so for every probability mixture of them.

## 3. Physical capture table — first coincidence, not a clock relaxation

For \(0<r\le d<1\), average the payoff of \(m_a\) against a Princess trajectory and its reflection. This equals the payoff against the fair-reflected Monster law for a fixed Princess orientation. For \(\eta=+1\), at \(a\ne r\),
\[
J_+(a;r,d)=
 \begin{cases}
 1+(r-a)/4,&0\le a<r,\\
 1+(1+d)/4,&r<a\le1.
 \end{cases}
\tag{4}
\]
At the **equality** \(a=r>0\), one Princess starts at the Monster's exact initial position, so its first contact is at time zero and \(J_+(r;r,d)=1\). The equality is essential and cannot be obtained as either one-sided limit.

For \(\eta=-1\), the corresponding exact table is
\[
J_-(a;r,d)=
 \begin{cases}
 (r-a+1+d)/4,&a<r,\\
 (1+d)/4,&a=r,\\
 1+(1+d)/4,&a>r.
 \end{cases}
\tag{5}
\]
In particular, \(J_-\le J_+\) pointwise. If \(r=0\), the case \(a=0\) has time-zero capture; all \(a>0\) have payoff \(1+(1+d)/4\) for either exit. If \(d\ge1\), every Princess is at zero at time one, when every path (1) passes through zero; thus both capture times are at most one. These cases are strictly inferior for the upper certificate.

Derivation of (4): when \(a<r\), the right-oriented Monster meets the Princess starting at \(+r\) during its initial rightward leg, at time \((r-a)/2\); its reflected Princess escapes along the leftward leg until the Monster arrives at \(-1\) at time two. When \(a>r\), that first contact instead occurs on the descending leg at time \((1+d)/2\), and the reflected contact is still at time two. The other outbound sign exchanges the roles of the latter two captures as in (5). The equality case makes the first capture time exactly zero.

The standard-library [Fraction regression](../../packages/interval_center_wait_principal/verify.py) checks 3,380 exact chronological path intersections, including both exit signs, equal starts, time-one capture and endpoint completion. It is a *fixture check*, not a substitute for this analytic proof.

## 4. Matching all-Princess upper

Let \(\alpha=e^{-1/2}\). For the Monster law (3), denote its CDF on \([0,1]\) by
\[
  F_M(r)=e^{(r-1)/2},\qquad
  f_M(r)=\tfrac12 F_M(r)\quad(0<r<1).
\]
Its \(a=0\) atom has mass \(\alpha\). The opposite outbound side is dominated by \(\eta=+1\) by (4)–(5). For any \(0<r\le d<1\), (4) yields
\[
\begin{aligned}
\mathbb E J_+(a;r,d)
&\le \int_{[0,r)}\left(1+\frac{r-a}{4}\right)\,dF_M(a)
 +\frac32\Pr(a>r)\\
&=:B(r).
\end{aligned}
\tag{6}
\]
All possible equality atoms at \(a=r>0\) are absent because (3) is continuous away from zero. At \(r\in(0,1)\), differentiation gives
\[
  B'(r)=\tfrac14F_M(r)-\tfrac12f_M(r)=0.
\]
The right limit at zero is
\[
 B(0+)=\alpha\cdot1+(1-\alpha)\cdot\tfrac32
      =\tfrac32-\tfrac\alpha2.
\]
Thus **every** pure Princess in \(\mathcal C\) has payoff at most the value (2). At \(r=0\), the Monster atom at zero captures instantly and the remaining mass contributes at most \(3(1-\alpha)/2\), strictly below (2). At \(d\ge1\), the payoff is at most one, also strictly below (2). At any \(0<r\le d<1\), the inequality (6) is strict because \(d<1\) and \(\Pr(a>r)>0\); for the opposite outbound sign, (5) only decreases payoff. Consequently **every** mixed Princess law also has expected payoff strictly smaller than (2) against the fixed Monster strategy (3). This proves the upper and Princess nonattainment.

## 5. Matching uniformly approaching Princess lower

Fix \(0<\varepsilon<1\), put \(b=1-\varepsilon\), \(s=e^{-b/2}\), and choose a continuous random starting radius \(R\) with density
\[
 \pi_\varepsilon(r)=
 \begin{cases}
 \tfrac12e^{-r/2}, &0<r<b,\\
 s/\varepsilon,&b<r<1.
 \end{cases}
\tag{7}
\]
The total mass below \(b\) is \(1-s\) and the upper layer has mass \(s\). Independently choose a fair starting sign. For each radius, leave the center at
\[
 D(R)=\max\{R,b\}<1
\]
and run outward to the **same-side endpoint**. This is a legal \(\mathcal C\) law with no atoms in its initial radius.

For any fixed \(a\in[0,1]\), the first-capture table (4) and \(D\ge1-\varepsilon\) imply
\[
 \mathbb E J_+(a;R,D(R))
 \ge K_\varepsilon(a)-\frac{\varepsilon}{4},
\quad
 K_\varepsilon(a)
 :=1+\frac14\mathbb E[(R-a)_+]
       +\frac12\Pr(R<a).
\tag{8}
\]
The equality event \(R=a\) has probability zero, even if the Monster chooses a Dirac mass at \(a\). The same bound holds for either Monster reflection by the fair-reflected Princess law.

Let \(S_\varepsilon(a)=\Pr(R>a)\). At every density point,
\[
 K_\varepsilon'(a)
  =-\tfrac14S_\varepsilon(a)+\tfrac12\pi_\varepsilon(a).
\]
For \(0<a<b\), \(S_\varepsilon(a)=e^{-a/2}\), so the derivative is zero. For \(b<a<1\),
\[
 K_\varepsilon'(a)
  =\frac{s}{2\varepsilon}
     -\frac{s(1-a)}{4\varepsilon}
  \ge0.
\]
It follows that
\[
  \inf_{a\in[0,1]}K_\varepsilon(a)
  = K_\varepsilon(0)
  =1+\frac14\mathbb E R.
\tag{9}
\]
Compare (7) with the limiting radius law having density \(\tfrac12e^{-r/2}\) on \((0,1)\) and residual atom \(e^{-1/2}\) at \(r=1\). The two distributions agree on \((0,b)\); their remaining masses are both in \([b,1]\), so their means differ by at most \(\varepsilon\). The limiting mean is
\[
 \mathbb E R_{\rm lim}=2-2e^{-1/2}.
\]
Equations (8)–(9) therefore give **uniformly in every legal \(a\)**:
\[
 \boxed{\inf_{m\in\mathcal P^+}
    \mathbb E_{\mu_\varepsilon}T(m,P)
    \ge\frac32-\frac{e^{-1/2}}2-\frac{\varepsilon}{2}.}
\tag{10}
\]
Taking \(\varepsilon\downarrow0\) proves the reverse inequality and (2). The endpoint atom is only a *weak limit*: an actual Princess atom at \(r=1\) would create a time-zero attack. The continuous tail in (7) is necessary to preserve the first-capture semantics.

## 6. Why this does NOT solve the requested full one-turn game

The canonical all-one-interior-turn Monster class \(\mathcal B_1\) permits starts \(a<0\) and independently moving the turn level \(b\ne1\), including endpoint-first paths and actual endpoint hits. Our Monster law (3) lies inside \(\mathcal B_1\), so it **does** prove the rigorous, useful upper
\[
 \boxed{W_{\mathcal C,\mathcal B_1}\le
       \frac32-\frac1{2\sqrt e}\approx1.1967346701.}
\tag{11}
\]
But the approaching Princess law (7) need not protect against the larger Monster class. For example, a negative-start principal turn \(P(-c,1)\) has limiting payoff against (7), for fixed \(0<c<1\), of
\[
  N(c)=c+\left(\frac32-\frac c2\right)e^{-c/2}
                    -\frac12e^{-1/2}.
\tag{12}
\]
The minimum occurs at the unique positive \(c\) satisfying
\[
 (5-c)e^{-c/2}=4,\qquad c\approx0.3158010964,
\]
where \(N(c)\approx1.1586010634\), strictly below (2). Thus (7) is **not** a lower certificate for all signed one-turn paths. Off-front turns may also matter.

A broader interpretation of “one turn” that permits an initial stationary hold is even easier for the Monster: remain at zero through time one, then travel to one endpoint and sweep to the other (only the endpoint reversal). Every \(\mathcal C\) Princess reaches zero by time \(r\le1\), so she is captured by time one and the corresponding restricted value is at most **one**. This does not determine that larger restricted minimax value.

Therefore this theorem **refutes an all-center-pass Princess equilibrium** but does not solve \(W_{\mathcal C,\mathcal B_1}\), \(W_1\), or the unrestricted game value \(V\). A genuinely competitive Princess law must allow some trajectories not to reach the exact center before the Monster's vulnerable time window. The current numerical unrestricted law indeed includes initial outward motion and ranks skimming past the center.

## 7. Reproduction and relation to the larger program

Run:
```sh
python3 packages/interval_center_wait_principal/verify.py
```

The verifier performs exact rational first-contact calculations for 3,380 sampled configurations plus high-precision checks of the indifference derivative. It has no dependence on the prior 1.424 upper/lower certificates and does not modify their hashes or data. [The complete one-turn domain](ONE_TURN_COMPLETE_DOMAIN.md), [signed contact constraints](../12-global-closure/BULK_CONTACT_AND_CUSP_EQUATIONS.md), and [indifference equations](../14-light-cone-lattice/ONE_TURN_INDIFFERENCE_EQUATIONS.md) provide the context. This result is a **complete analytic solution of a genuinely infinite-dimensional subgame**, not merely a finite-grid fit.
