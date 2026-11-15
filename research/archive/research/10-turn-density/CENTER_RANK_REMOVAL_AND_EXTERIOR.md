# Center rank removal and the exact exterior region

## Scope

This note extends the conditional center certificate in
[AFFINE_CENTER_ZENO_ATTACHMENT.md](AFFINE_CENTER_ZENO_ATTACHMENT.md).
It does not establish a value for the unrestricted interval game. The saved
field still has independent initial-sweep and fixed-turn attacks.

There are two distinct results.

1. A general rank-removal comparison converts a lower bound on the center
   front into a lower bound for every continuation whose first productive
   center action occurs before a fixed barrier.
2. For the specified saved field, an exact algebraic audit identifies a
   two-dimensional region on which the full unrestricted center value equals
   the immediate exterior envelope. No bound on subsequent turns is imposed.

The new verifier repeats the complete attachment audit on the larger source
region beginning at \((7/8,0)\). It does not infer that extension from a finite
sample of center states.

## 1. Definitions and the barrier

Let \(p_q\), \(0<q<1\), be ordered nonnegative, continuous, speed-at-most-one
princess paths, reflected fairly about the center. Write
\[
 R(U,V)=\Pr\left(p_q((U+V)/2)\le (U-V)/2\right),\qquad
 Z(t)=R(t,t).
\]
Boundary and first-contact integrals use the strict/closed conventions of
CENTER_IMBALANCE_FACTORIZATION.md. Statements about rank intervals are
unchanged by null sets of ranks. Closed endpoint capture is kept separate
from an interior spatial trace.

Let \(\beta_t(q)\) be the first meeting time of \(p_q\) with the outward
unit-speed ray beginning at the center at time \(t\), and put
\[
 T_t(n)=\int_0^n\beta_t(q)\,dq.
\]
Thus \(t\le\beta_t(q)\le t+1\). Let \(V(t,n)\) be the remaining absolute
capture-time contribution when both reflected copies of ranks at most \(n\)
have already been captured and the monster is at the center at time \(t\).
Use the transformed value
\[
 W(t,n)=V(t,n)+\tfrac12T_t(n).
\]

Assume a barrier time \(b\), with \(q_b=Z(b)\), such that
\[
 R(U,V)\le q_b
 \quad\text{at every future interior point with }V\ge b.                 \tag{1}
\]
This is a future-envelope condition, not merely a condition on one outgoing
row. In particular, every rank \(q\le q_b\) is at the center at time \(b\).
For \(e\le b\),
\[
 \beta_e(q)\le b\quad(q\le q_b),
 \qquad \beta_e(q)\le b+1\quad(q>q_b).                                  \tag{2}
\]
For \(e\ge b\), a rank \(q>q_b\) can only be caught at an endpoint along
the outgoing ray, so \(\beta_e(q)=e+1\). Condition (1) forces that rank
to have reached the endpoint by that time. Consequently
\[
 V(e,N)=(e+2)(1-N),\qquad e\ge b,\quad N\ge q_b.                          \tag{3}
\]
The fair reflected endpoint tails have equal mass; visiting the two endpoints
at \(e+1,e+3\) is optimal.

The center-renewal and finite-quantile approximation hypotheses of
CENTER_IMBALANCE_FACTORIZATION.md are retained. They include a common bounded
endpoint-completion horizon. They allow arbitrary speed, arbitrary later
turns, and limiting chains of center returns.

## 2. Rank removal before the barrier

Suppose
\[
 B(t)\le W(t,Z(t)).
\]
For \(n\ge z:=Z(t)\), define
\[
 L_B(t,n)=B(t)-\tfrac12\left[b(n-z)+(n-q_b)_+\right].                    \tag{4}
\]

**Early-productivity comparison.** Every continuation whose first productive
center action relative to the surviving ranks \(q>n\) occurs by time \(b\)
has transformed cost at least \(L_B(t,n)\).

A productive tent returning at \(u\le b\) reaches
\(N=R(u,t)\ge n\). Compare the same tent and the same later continuation,
first from rank \(n\), then from the front rank \(z\). The added band
\((z,n]\) contributes
\[
 \tfrac12\int_z^n[\beta_t(q)+\beta_u(q)]\,dq.
\]
After the \(T_t/2\) transformation, the difference is just
\(\tfrac12\int_z^n\beta_u(q)\,dq\), which is bounded by (2). The later
continuation is unrestricted.

A first productive wait requires a separate argument. Before its first
productive time \(\rho\le b\), no surviving positive-measure rank band has
been caught. Let \(\chi\) be the first tent-return characteristic with
\(R(\chi,t)\ge n\); it satisfies \(\chi\le\rho\). Insert the maximal tent
from \(t\) to \(\chi\), oriented toward either reflected copy, and then wait
until \(\rho\). The added chosen-side band \((z,n]\) is caught at its earliest
times \(\beta_t(q)\); its opposite copy is caught no later than \(\rho\).
No previously captured surviving band is delayed, and any closed overshoot
at \(\chi\) helps. This gives the same bound (4).

This proof is first made for finite canonical near-optimizers. Uniform
quantile discrepancy for monotone capture-rank functions, together with
the common completion horizon, transfers the comparison to arbitrary
routes. Thus it does not assume that an arbitrary infinite route has an
attained first positive-measure productive event. A later finite-time
accumulation is simply part of the unchanged continuation; it is not
discarded or replaced by an assumed finite number of turns.

## 3. Late first productivity and the exterior envelope

If the first productive tent returns at \(e\ge b\), then
\[
 N=\max(n,R(e,t))\ge q_b,
\]
and its continuation is exactly (3). All preceding empty waits and
excursions can be absorbed into that first tent. A first productive center
wait cannot occur strictly after \(b\): if \(n<q_b\), the center visit at
\(b\) is already productive; if \(n\ge q_b\), (1) forbids such productivity.

For an interior return \(e\ge b\), define the actual feasible action
\[
 W_e(t,n)=
 \tfrac12\left[T_t(N)+T_e(N)-T_e(n)\right]+(e+2)(1-N),
 \quad N=\max(n,R(e,t)).                                                \tag{5}
\]
The direct endpoint tour has
\[
 W_{\rm end}(t,n)=\tfrac12\left[T_t(1)+(t+3)(1-n)\right].                 \tag{6}
\]
Let \(E_W(t,n)\) be the infimum of these immediate late-return and endpoint
actions. Nonproductive late tents can be retained in the definition; they
are dominated by the direct endpoint alternative when relevant.

The full unrestricted center value satisfies
\[
 \boxed{\quad
 \min\{E_W(t,n),L_B(t,n)\}\le W(t,n)\le E_W(t,n).
 \quad}                                                               \tag{7}
\]
In particular, wherever \(E_W\le L_B\),
\[
 \boxed{W(t,n)=E_W(t,n).}                                               \tag{8}
\]

The difference \(E_W-L_B\) is nonincreasing in rank. For a useful fixed
return \(e\), the derivative of (5) is \(-\beta_e(n)/2\), which is at most
\(-b/2\) below \(q_b\) and at most \(-(b+1)/2\) above it. These are the
two slopes of (4). Once the same tent is nonproductive, \(n\ge R(e,t)\ge
q_b\), its derivative is
\[
 -(e+2)+\beta_t(n)/2\le -(b+1)/2.
\]
The endpoint slope is \(-(t+3)/2\), also sufficiently negative on the
stated time domain. Taking an infimum preserves nonincrease. This
argument includes the rank boundary of a useful tent, so it does not
silently drop higher-rank states from (8).

## 4. The saved affine wedge

The reference data are
packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json,
Git blob 5c45d042ee9948faebc03354c3e1e2ee3cbec1a5.

On \(a=7/8\le V\le U\le b=15/16\),
\[
 R(U,V)=kU-\ell V+c,\qquad Z(t)=dt+c,\quad d=k-\ell,
\]
where
\[
 k=\frac{655898601421}{62500000000},\quad
 \ell=\frac{820954217}{12500000000},\quad
 d=\frac{10184278599}{976562500},\quad
 c=-\frac{71289950193}{7812500000},\quad
 q_b=\frac{10184278599}{15625000000}.                                    \tag{9}
\]
Put
\[
 D=\frac{623060432741}{655898601421},\quad
 \theta=\frac{1-\sqrt D}{1+\sqrt D},\quad
 B_+=\frac2{(1-\sqrt D)^2},
\]
\[
 C_*=-\frac{149534660791}{10^{12}}
       +\frac{5903087412789}{10^{12}}\sqrt D,\qquad
 \tau=\frac{39}{16}-\frac{1967695804263}{1246120865482}\sqrt D.            \tag{10}
\]
Here \(\tau\) is approximately \(0.8984790728300504\).

The complete exact attachment replay from source \((a,0)\) proves
\[
 W(t,Z(t))\ge B(t):=C_*+\frac c2t
 \quad(a\le t\le b),                                                   \tag{11}
\]
with equality throughout
\[
 a\le t\le\tau.                                                        \tag{12}
\]
The attaining path waits to \(\tau\), then takes the growing alternating
tent chain already proved in AFFINE_CENTER_ZENO_ATTACHMENT.md, ending
at \(b\), and finally tours the endpoints.

The extension from \(57/64\) to \(7/8\) is independently checked by the new
source-domain attachment, including crossing, endpoint, wait, and
rank-boundary exits. It is not an extrapolation of the front formula.

The field audit also proves (1), verifies the closed endpoint comparison
for the dominating affine inverse model, and proves that rows
\(V\in[a,b]\) are flat for \(U\ge17/16\). Monotonicity of the inverse
moments then makes all longer nonendpoint returns no better than
\(17/16\). Thus \(E_W\) reduces to useful returns
\(e\in[b,17/16]\) and the separately closed endpoint tour. There is genuine
post-\(b\) incoming mass before \(17/16\); returning at \(b\) is not assumed
optimal.

## 5. An explicit unrestricted off-front region

For the saved field, \(Z(1)=0\), there is no outgoing \(V=1\) plateau, and
\(\beta_1(q)=2\) almost everywhere. The useful return at \(e=1\) has
\[
 W_1(t,n)=J(t)-n,\qquad
 J(t)=\frac{12-(7-t)R(1,t)-\int_t^1R(U,t)\,dU}{4}.                       \tag{13}
\]
On \([a,\tau]\), its exact polynomial coefficients are
\[
 J(t)=
 \frac{1499993496472898751}{2097152000000000000}
 +\frac{33250875365717409}{65536000000000000}\,t
 +\frac{7559351910113219}{8192000000000000}\,t^2.                         \tag{14}
\]
Set
\[
 n_{\rm crit}(t)=
 \frac{J(t)-C_*-[ct+bZ(t)]/2}{1-b/2}.                                  \tag{15}
\]
The exact interval audit proves
\[
 Z(t)<n_{\rm crit}(t)<q_b,\qquad
 I(t):=R(t,0)>n_{\rm crit}(t),\qquad a\le t\le\tau.                      \tag{16}
\]
At \(n=n_{\rm crit}\), (13) equals (4). Therefore \(E_W\le L_B\) there.
The rank monotonicity in Section 3 extends this inequality through rank one.

**Exact unrestricted region.**
\[
 \boxed{
 W(t,n)=E_W(t,n),\qquad
 \frac78\le t\le\tau,\quad n_{\rm crit}(t)\le n\le1.
 }                                                                     \tag{17}
\]
The threshold is about \(0.4782136041\) at \(7/8\), \(0.5314707007\) at
\(57/64\), and \(0.5585612589\) at \(\tau\). These decimal displays are not
used in the proof.

The polynomial
\[
 I(t)=-\frac{713310167489}{500000000000}
       +\frac{1735432447}{781250000}\,t
\]
has exact minimum \(I-n_{\rm crit}>0.0106580681\) on this interval.
Consequently a first-center prefix with a final outward turn
\((U,V)=(t,w)\), \(w\le0\), has \(n\ge R(t,w)\ge I(t)\) and falls in
(17). The conclusion also holds for limiting prefixes with that closed
record property. It does not assert that every arbitrary prefix has such
a last turn.

The front is slack for any proposed game value at most \(3/2\):
\[
 \min_{[a,\tau]}B(t)=B(\tau)>3/2.
\]
Thus the exact front branch itself is not an active global matching
constraint for this field. Off-front arrivals are materially different.

## 6. Attachment to arbitrary first-center prefixes

Let a monster start at \(+a_0\), stay positive until its first center visit
\(\sigma\), and let \(L_s,M_s\) be its running strict lower and closed upper
radial records. Write \(n=M_\sigma\). Before \(\sigma\), only the positive
copy is captured, and its captured rank band is \([L_s,M_s]\). If
\(\tau_q^+\) denotes its first capture time, layer cake gives exactly
\[
 \int_0^n\tau_q^+\,dq
 =\sigma n-\int_0^\sigma(M_s-L_s)\,ds.                                  \tag{18}
\]
The negative copies meeting the monster at the first center contribute
\(\sigma Z(\sigma)/2\). The same term cancels in the center imbalance
factorization. Hence the optimized full cost after this arbitrary prefix is
\[
 \boxed{
 W(\sigma,n)+\frac12\int_0^n\tau_q^+\,dq
 =W(\sigma,n)+\frac12\left[\sigma n-\int_0^\sigma(M_s-L_s)\,ds\right].
 }                                                                     \tag{19}
\]
No count of pre-center turns, nor a unit-speed assumption on the original
prefix, is used.

For low records, a further general comparison is available. Removing both
copies of a rank band gives
\[
 W(t,n)\ge W(t,N)+\frac12\int_n^N\beta_t(q)\,dq,\qquad N\ge n.             \tag{20}
\]
For an arbitrary prefix from \(+a_0\), the positive capture moment is at
least the earliest-direction moment
\[
 M(a_0,n)=\frac12\int_{-a_0}^{a_0}R_{\rm strict}(a_0,V)\,dV
 +\frac12\int_{a_0}^{t}(n-R_{\rm closed}(U,-a_0))_+\,dU,                 \tag{21}
\]
provided \(A(a_0)\le n\le R(t,-a_0)\). The first inequality holds at a
first-center visit; the second follows from the light-cone bounds on all
earlier records. The moment in (21) is unweighted by reflection; its
contribution to (19) is \(M/2\).

If \(n\le N=n_{\rm crit}(t)\), then (16) gives
\(N<I(t)\le R(t,-a_0)\). On that band
\[
 \partial_n M(a_0,n)=\beta_{-a_0}(n)\le(t-a_0)/2\le\beta_t(n).
\]
Combining (19)--(21) and the exact boundary value (17) yields
\[
 \boxed{
 \text{full prefix cost}\ \ge
 E_W(t,n_{\rm crit}(t))+\tfrac12M(a_0,n_{\rm crit}(t)).
 }                                                                     \tag{22}
\]
There is even an additional nonnegative margin at least
\((t+a_0)[n_{\rm crit}(t)-n]/4\).

Equation (22) reduces all low-record prefixes in the time interval to a
two-variable field/hinge inequality in \((t,a_0)\). This note does not
assert that this remaining inequality clears a proposed game target.
The early-prefix worker is auditing that exact gate separately.

## 7. Reproduction and exact scope

Run the native wrapper with the immutable reference field:
\[
\texttt{node verify\_center\_rank\_removal.cjs endpoint\_joint\_i1\_field.json}.
\]
The source is also a pure function body:
\[
\texttt{Function(source)().verify(fieldData)}.
\]
All sign decisions occur in the exact quadratic field
\(\mathbb Q(\sqrt{623060432741/655898601421})\). Numeric conversions are
display-only.

The complete report records:

- 207 direct-crossing regions and 207 independent primitive checks;
- 5,886 rank-boundary exit regions, of which 5,885 pass Bernstein gates and
  one has a complete exact stationary fallback;
- 103,840 Bernstein pairs, 28,514 rank-boundary vertices, and 66 independent
  rank-boundary primitive checks;
- 674 quadratic-field arithmetic checks, 27,950 rational-geometry regression
  checks, and 42 exact finite-chain attainment checks;
- whole-interval exact margins for (16), the front slack, and the
  negative-\(V\) arrival condition.

The full native replay reproduces the assembled report. The report is a
conditional center certificate for one specified legal field. It is not
a globally matching lower strategy, an all-initial-state certificate, or
an improved interval-game bound.
