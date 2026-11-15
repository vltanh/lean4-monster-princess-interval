# Center imbalance factorization and a two-state renewal certificate

## Preservation and scope

This note was reconstructed in the tool runtime after the native executor
became unavailable on 2026-11-11. The mathematical factorization and renewal
algebra were independently audited by the parent and global-equilibrium
agents. Before the outage, the first direct polygonal fixture run completed
successfully; its precise evidence is recorded in Section 9. A second native run adding the renewal-kernel fixture was launched, but
its completion was not observed. A subsequent pure-V8 port was executed
successfully in the tool runtime: it reproduced all 19,362 confirmed physical
checks and added 360 exact renewal-kernel checks. That independent execution,
not the unobserved native run, supplies the additional evidence.

The standalone portable verifier is verify_center_factorization.cjs; it
uses only the rational scalar helpers from the embedded exact runtime,
not its CDF or Bellman routines. Its report is center_factorization_checks.json.

The result is an exact response reduction for every center record state of
an ordered reflected princess law. It does not impose a finite monster turn
bound, supply an equilibrium law, or claim a game value. It identifies a
two-variable renewal potential whose construction and initial attachment
remain open.

## 1. Ordered law, records, and moments

Let the nonnegative paths \(p_q(s)\), \(0<q<1\), be ordered nondecreasingly
in \(q\), take values in \([0,1]\), and be 1-Lipschitz. Assign \(p_q\) and
\(-p_q\) probability \(dq/2\). Assume they are absorbed at their signed
endpoints by time two. Earlier endpoint visits followed by departure are
allowed. Absorption supplies a common finite completion horizon.

Write
\[
 R(U,V)=\Pr\!\left(p_q((U+V)/2)\le (U-V)/2\right),
 \qquad Z(t)=R(t,t).
\]
The actual closed endpoint value is \(R(t+2,t)=1\); an endpoint-interior
limit must not replace it.

At a center visit at time \(t\), let the captured positive and negative
ranks be the prefixes \([0,r]\) and \([0,n]\), with \(r,n\ge Z(t)\).
Define \(J(t,r,n)\) as the infimum of the absolute first-capture contribution
of the still-uncaught paths over all future legal monster curves from the
center. Previously caught paths contribute zero.

The earliest possible capture time of rank \(q\), on either chosen sign, is
the direct outward-ray time
\[
 \beta_t(q)=\inf\{s\ge t:s-p_q(s)\ge t\},
 \qquad t\le\beta_t(q)\le t+1.
\]
A path at center initially has \(\beta_t(q)=t\), but its rank is already
below both frontiers. Put
\[
 T_t(q)=\int_0^q\beta_t(x)\,dx,\qquad V(t,n)=J(t,n,n).
 \tag{1}
\]
Thus \(V(t,n)\) is the balanced-tail value for the two signed copies of
ranks \(q>n\).

## 2. Exact imbalance factorization

**Theorem.** For \(Z(t)\le r\le n\le1\),
\[
 \boxed{J(t,r,n)=\frac12\int_r^n\beta_t(q)\,dq+V(t,n).}
 \tag{2}
\]
Interchange the two frontiers for the other order. This is an equality of
infima and does not assume an attained optimizer or first positive-mass
capture event.

The lower inequality is immediate. The unmatched positive band \((r,n]\)
cannot be caught before its direct-ray times. The restriction of any route
to the balanced tail \(q>n\) costs at least \(V(t,n)\). Their contributions
add.

For the converse first consider a finite canonical center route for the
balanced tail: center waits, maximal same-half tents, and endpoint
completion. Choose its first action which captures an upper-tail rank.
All preceding actions are empty for that tail.

### First productive triangle

Suppose this triangle returns to center at \(e\). Reflect the continuation
if necessary to orient its chosen side toward the unmatched positive band.
Replace its preceding empty prefix and the triangle by the capped maximal
bridge
\[
 m(s)=\min(s-t,e-s,1),\qquad t\le s\le e.                 \tag{3}
\]
The cap is essential when a long empty prefix makes \(e-t>2\).
This bridge is pointwise above the old chosen-side excursion, so every
chosen-side upper-tail capture is no later. The opposite upper tail had
no capture at the removed junctions; its return contact at \(e\) and its
subsequent continuation are retained.

Productivity implies that the bridge's outward capture frontier exceeds
\(n\), or that it reaches the endpoint. Consequently every rank in
\((r,n]\) is met on the initial unit ray at its exact \(\beta_t(q)\).
An earlier endpoint hit may instead be completed by a direct opposite
sweep, but the capped bridge itself is already a legal comparison.

### First productive center wait

Let \(\tau\) be its first upper-tail center contact and set
\[
 \chi=\inf\{U\in[t,t+2]:R(U,t)\ge n\}.                    \tag{4}
\]
Use the essential left rank limit at \(n\) if necessary; the unmatched
band is half open and a single rank has no effect on its integral.
A closed overshoot at \(\chi\) can only help.

If \(\tau\le t+2\), transport gives \(R(\tau,t)\ge Z(\tau)>n\), so
\(\chi\le\tau\). If \(\tau>t+2\), this follows from \(\chi\le t+2\).
Run the positive balancing tent from \(t\) to \(\chi\), wait at center
until \(\tau\), and follow the old continuation. The unmatched band is
caught at \(\beta_t\); every upper-tail contact due at \(\tau\) is retained,
and no prior upper-tail capture is lost.

For \(n=1\), there is no balanced tail and a direct outward sweep attains
the integral in (2). For \(r=n\), that integral is empty.

### Infimum and exact-contact justification

For a fixed route starting at center, each sign's future first-capture
time is nondecreasing in radial rank: reaching an upper ordered path
requires crossing every lower path that started on the same side of the
center. On a common bounded horizon this gives a route-independent
uniform-quantile quadrature error tending to zero.

Take a near-minimizing balanced-tail route and finitely many ordered tail
quantiles. The fixed-start capture-order construction, followed by maximal
tents between center visits, gives a finite canonical route preserving the
sampled capture deadlines. Endpoint absorption permits completion within
a common horizon (time six suffices when \(t\le2\)).

Use the first productive action for that finite sample in the repair above.
A productive sampled rank is strictly greater than \(n\), so the entire
continuum unmatched band is still caught at its exact earliest times.
No sampled upper-tail capture is later. Uniform quantile discrepancy bounds
the change in the full balanced-tail contribution. Let the sample size
increase and the near-optimality error decrease.

This proves (2) without postulating an attained first positive-measure event,
and covers Zeno histories and characteristic contacts. Center mass present
at \(t\) is already below both frontiers. No continuity of individual capture
times under uniform perturbations of monster paths is invoked.

## 3. The lagging-side sign lemma

At \(r\le n\), consider a triangle departing at \(t\) and returning at \(e\).
Let
\[
 \rho=R(e,t),\quad z=Z(e),\quad \rho\ge z,\qquad
 c=\max(r,\min(n,\rho)),\quad d=\max(r,\min(n,z)).
\]
The lagging-side and leading-side updates are respectively
\[
 (\max(r,\rho),\max(n,z)),\qquad
 (\max(r,z),\max(n,\rho)).
\]
Their immediate cost difference is
\[
 K_{\rm lag}-K_{\rm lead}
   =\frac12\int_r^c\beta_t(q)\,dq-\frac e2(d-r).           \tag{5}
\]
Keep the same continuation orientation if \(\rho\le n\), and reflect it
if \(\rho>n\). After that common ordering, the lagging terminal state has
increased one frontier by \(c-d\). For any symmetric future potential with
one-coordinate slopes at most \(-e/2\), its change is at most
\(-e(c-d)/2\). Thus total lagging-minus-leading cost is at most
\[
 \frac12\int_r^c(\beta_t(q)-e)\,dq\le0.                   \tag{6}
\]
The band is empty for \(\rho\le r\). No concavity is needed for this lemma.

For actual routes, compare paired ranks directly: above \(n\) the paired
capture times agree after the indicated reflection. The unmatched ranks
are caught by time \(e\) on the lagging outward leg instead of at or after
the return. The lemma holds for a general curved ordered law, without an
ordinary-wave CDF factorization.

## 4. Exact balanced renewal actions

Only \(V(t,n)\) remains unknown. For a triangle from the balanced state
\((n,n)\), put
\[
 N=\max(n,R(e,t)),\qquad r_1=\max(n,Z(e)).
\]
Its immediate cost is
\[
 \frac12\int_n^N\beta_t(q)\,dq+\frac e2(r_1-n).
\]
At the return the frontiers are \((r_1,N)\). Apply (2), and use
\(\beta_e(q)=e\) for ranks at center at time \(e\). The action followed by
optimal continuation is exactly
\[
 \boxed{\frac12\int_n^N[\beta_t(q)+\beta_e(q)]\,dq+V(e,N).}
 \tag{7}
\]
It remains valid when \(R(e,t)\le n\), with an empty integral. At the
actual endpoint turn \(e=t+2\), use the closed \(N=1\). Formula (7) is
then the direct endpoint-tour cost, not an interior-limit cost.

For a center wait on \([t,e]\), define
\[
 H_t(s)=\sup_{t\le v\le s}Z(v),\qquad N=\max(n,H_t(e)).
\]
Its balanced immediate contribution is
\[
 W_{\rm wait}(t,e;n)
  =e(N-n)-\int_t^e(H_t(s)-n)_+\,ds,                      \tag{8}
\]
followed by \(V(e,N)\). The running center record in (8) is essential.

A bounded potential below the physical terminal values, satisfying the
triangle inequalities (7) and wait inequalities (8), bounds every balanced
continuation from below. The actual value satisfies the same inequalities,
so it is the largest such verification potential. This follows by
telescoping finite canonical routes and applying the quantile argument.
The identity action \(e=t\) does not remove the terminal obligations or
select a unique fixed point on its own.

If \(N=n\), a triangle captures no balanced-tail rank. Since
\(R(e,t)\ge H_t(e)\), waiting to \(e\) also captures none and has the same
state. Every productive triangle has \(N>n\), and productive waits also
increase \(n\). Thus the nontrivial problem is a forward renewal in captured
rank. Arbitrarily small increases remain possible: this is not a finite
turn theorem or a uniform-contraction claim.

## 5. Transformed potential and shape

Set
\[
 \mathcal W(t,n)=V(t,n)+\frac12T_t(n).
\]
The full center value becomes
\[
 J(t,r,n)
   =\mathcal W(t,\max(r,n))-\frac12T_t(\min(r,n)).         \tag{9}
\]
The triangle verification inequality has the short form
\[
 \boxed{2\mathcal W(t,n)
 \le2\mathcal W(e,N)+T_t(N)-T_e(n).}                     \tag{10}
\]
The wait inequality is
\[
 \mathcal W(t,n)\le\mathcal W(e,N)+W_{\rm wait}(t,e;n)
                    +\frac12[T_t(n)-T_e(N)].            \tag{11}
\]
An explicit wait check is retained: replacing a long wait by one final
tent may delay opposite captures at intermediate center peaks.

The true \(\mathcal W(t,\cdot)\) is concave. Fix the smaller frontier at
\(Z(t)\) in (9) and use joint concavity of the remaining-cost value in its
two frontiers. Moreover,
\[
 \mathcal W(t,n_2)-\mathcal W(t,n_1)
 \le-\frac12\int_{n_1}^{n_2}\beta_t(q)\,dq
 \quad(n_1\le n_2).                                    \tag{12}
\]
To prove this, deleting the balanced band from a near-optimal route reduces
its cost by at least \(\int_{n_1}^{n_2}\beta_t\), since both signs' first
captures are no earlier than their direct-ray times. Add half the \(T_t\)
difference.

Conversely a concave candidate satisfying (12) has a jointly concave
symmetric lift. Indeed the lift is
\[
 \min\{\mathcal W(t,r)-T_t(n)/2,\;
        \mathcal W(t,n)-T_t(r)/2\},                      \tag{13}
\]
because \(\mathcal W(t,q)+T_t(q)/2\) is nonincreasing. Each branch is
concave, and all one-coordinate slopes are at most \(-t/2\).

For a fixed affine triangular field, \(T_t(n)\) is piecewise quadratic
after the finite row/inverse arrangement is split. A piecewise-quadratic
\(\mathcal W\) makes (10) a rational quadratic on polyhedral cells in
\((t,e,n)\), because \(N\) is either \(n\) or the affine \(R(e,t)\).
This permits exact whole-cell verification using the existing
quadratic-polytope tools. It represents a proof potential, not a replacement
of the princess continuum by finitely many rank paths.

## 6. Reachable domain and terminal sweep region

Let
\[
 H(t)=\sup_{0\le v\le t}Z(v),\qquad
 Y_{\rm tail}(t)=\sup_{V\ge t,\;V\le U<V+2}R(U,V).
\]
The center-memory lemma gives \(\max(r,n)\ge H(t)\) for any reachable
center state, independently of the initial monster start. Thus the
balanced potential needed for reachable histories has domain
\[
 H(t)\le n\le1.                                        \tag{14}
\]
It is invariant: for every \(v\in[t,e]\),
\(R(e,t)\ge Z(v)\), so \(N=\max(n,R(e,t))\ge H(e)\).
Waits have the same property.

When \(n\ge Y_{\rm tail}(t)\), all remaining balanced ranks are endpoint
only. The exact transformed value is
\[
 \boxed{\mathcal W(t,n)
   =\frac{T_t(1)+(t+3)(1-n)}2.}                         \tag{15}
\]
It is affine in \(n\) on that region. A field with the memory barrier
\(H(s_0)\ge Y_{\rm tail}(s_0)\) therefore has (15) as the exact terminal
condition for every reachable center state at and after \(s_0\).
The saved candidate uses \(s_0=15/16\); its field-specific barrier audit
must be retained separately.

Without an earlier barrier, absorption and the no-\(V=1\)-atom condition
give \(V(e,n)=(e+2)(1-n)\) for \(e\ge1\). A general atomic version can
instead use center horizon two. Neither terminal convention is needed
for factorization (2) itself.

## 7. Relation to the unresolved lower construction

The imbalance part is explicit, and the late center boundary is known.
The remaining task is to construct \(\mathcal W\) on the earlier domain,
verify (10)-(12), and attach arbitrary initial prefixes or their independent
record potential. Existing cost deficits in the saved law do not disappear.

The exact alternative to a turn cap is now a one-rank renewal/free-boundary
system on \((t,n)\), with center-record waits and a known terminal region.
No solution of that system at a proposed equilibrium cost is asserted.

## 8. Independent audits

The parent and global-equilibrium agents independently checked the
factorization construction, the lagging-side comparison, the transformed
renewal algebra, and the reachable memory domain. The long-prefix bridge
is explicitly capped at one.

## 9. Confirmed physical fixture evidence

The first native Python fixture run completed before the environment outage.
It used three ordered weighted polygonal laws, including slow motion,
multiple waves, exact center contacts, stationary endpoint mass, a path
leaving an earlier endpoint, and a final \(V=1\) characteristic. Direct
rational segment intersections supplied every capture time.

Recorded semantic checks:
- 26 ordering checks;
- 1,276 legality checks;
- 1,260 repaired-upper-tail cost comparisons;
- 7,350 exact earliest-unmatched capture equalities;
- 4,410 full-cost decomposition comparisons;
- 5,040 lagging-versus-leading sign comparisons.

Total: **19,362 recorded exact checks**.

The 1,260 repairs comprise 814 first-productive-triangle cases (578 using
a capped long bridge), 96 productive-center-wait cases, 210 no-upper-tail
cases, and 140 empty-unmatched-band cases. These are case classifications,
not additional independent checks.

The pure-V8 port subsequently reproduced every count above and passed an
additional 360 direct physical renewal-kernel identities. Its total is
**19,722 recorded exact checks**. The kernel check compares direct captures
on a triangle plus the explicit imbalance integral at its return against
(7), retaining center and endpoint contacts. The matching native rerun
remains unconfirmed and is not used as evidence.


## 10. An analytic patch on a constant incoming cone

Suppose \(R(U,V)=\lambda U\) on \(0\le V\le U\le b\), with
\(\lambda>0\). For \(\lambda t\le n\le\lambda b\),
\[
 T_t(n)=nt/2+n^2/(4\lambda)+\lambda t^2/4.
\]
For an arbitrary constant \(C\), define
\[
 \mathcal W_C(t,n)=C+(tn-n^2/\lambda)/2,
\]
or equivalently
\[
 V_C(t,n)=C-\frac{5n^2}{8\lambda}
               +\frac{nt}{4}-\frac{\lambda t^2}{8}.     \tag{16}
\]
This candidate satisfies every within-cone triangle and center-wait
verification inequality.

For a productive triangle \(e\ge n/\lambda\), the residual in (10) is
\[
 \frac{[\lambda(e+t)-2n]^2}{4\lambda}\ge0.               \tag{17}
\]
Equality occurs at \(e_*=2n/\lambda-t\). For a nonproductive triangle
\(t\le e\le n/\lambda\), the residual is
\[
 (e-t)[2n-\lambda(e+t)]/4\ge0.                          \tag{18}
\]
For a center wait the actual-value residual is
\[
 \begin{cases}
 (e-t)[2n-\lambda(e+t)]/8,& e\le n/\lambda,\\
 (n-\lambda t)^2/(8\lambda),& e\ge n/\lambda.
 \end{cases}                                          \tag{19}
\]
The potential is concave in \(n\) and satisfies the slope bound (12).

If the front has constant total cost along waits,
\(V(e,\lambda e)=C-\lambda e^2/2\), and \(e_*\le b\), the action at \(e_*\)
attains (16). This is a conditional within-cone value statement. For a
verification potential, the square identities are valid without asserting
front equality, but the crossing actions, outer boundary data, and initial
attachment must still be checked.

The triangular patch
\[
 \lambda t\le n\le\lambda(t+b)/2
\]
is invariant under within-cone actions and has \(e_*\le b\).
For the saved field, a pure-V8 exact audit of all 81 triangles in
\(0\le V\le U\le1/2\) gives
\(\lambda=3521265547/12500000000\), with no coefficient failure.

There is also a finite prefix interpretation. For an initial balanced
frontier \(n\), put \(u_0=n/\lambda\). A wholly-cone productive triangle
from \(t\) to \(e\) has excess over waiting to the same return
\[
 \lambda(e-u_0)(e+2t-3u_0)/8.
\]
After the first productive triangle or productive wait, the balanced state
is on the front \(n=\lambda t\). Every further wholly-cone triangle then
has nonnegative excess \(\lambda(e-t)^2/8\) and can be replaced by a wait.
Any empty wait before a productive triangle can be removed by extending
that triangle backward to the initial departure. Thus before leaving the
constant cone, at most one immediate productive triangle is needed,
followed by a wait and the crossing action. This does not bound the later
renewal count in the curved middle region.

For a general pure-incoming cone \(R(U,V)=F(U)\), differentiating the same
triangle-versus-front-wait expression gives the stationary return equation
\[
 2(F(e)-n)=(e-t)F'(e).
\]
No global minimum or shape claim follows from this stationarity equation
alone.


## 11. A diagonal affine cell and an exact accumulating-return solution

Suppose that all characteristic segments and outgoing first inverses used
below lie in one affine region
\[
 R(U,V)=kU-\ell V+c,\qquad k>0,\quad
 0\le r:=\ell/k<1/8.
\]
Put \(d=k-\ell\), \(z(t)=dt+c\), and \(y=n-z(t)\ge0\). The local
outgoing inverse and its primitive are
\[
 \beta_t(q)=t+\frac{(q-z(t))_+}{2k},
 \qquad T_t(q)=tq+\frac{(q-z(t))_+^2}{4k}.              \tag{20}
\]
As elsewhere, the center ranks below \(z(t)\) have already been captured.
Formula (20) is used only while its indicated inverse remains in the
affine region.

Let
\[
 w=\sqrt{1-8r},\quad
 B=\frac{2}{(1+w)^2},\quad b=\frac Bk,\quad
 a=b+\frac1{8k}.
\]
For an arbitrary constant \(C\), define
\[
 V_C(t,n)=C-\frac{dt^2}{2}-ty-ay^2,\qquad
 \mathcal W_C(t,n)=C+\frac{ct}{2}-\frac{ty}{2}-by^2.
                                                               \tag{21}
\]
These formulas agree with \(\mathcal W=V+T/2\). They prescribe constant
total cost along front waits:
\(V_C(t,z(t))=C-dt^2/2\).

For a productive triangle of duration \(h=e-t\ge y/k\), the residual in
the transformed triangle inequality is
\[
\begin{split}
 \Delta={}&2\mathcal W_C(e,R(e,t))+T_t(R(e,t))
              -T_e(n)-2\mathcal W_C(t,n)\\
 ={}&k\left[
 (1/4-r-2Br^2)h^2-\frac yk h
 +2B\left(\frac yk\right)^2
 -\frac14\left(\frac yk-(1-r)h\right)_+^2
 \right].                                             \tag{22}
\end{split}
\]
The small Riccati root obeys
\[
 8B(1/4-r-2Br^2)=1.
\]
Consequently, when \(h\ge y/d\),
\[
 \Delta=\frac{k}{8B}\left(h-\frac{4By}{k}\right)^2.
                                                               \tag{23}
\]
On \(y/k\le h\le y/d\), the coefficient of \(h^2\) in (22) is
\(-k[r/2+r^2(1/4+2B)]\le0\). Its minimum on that interval is at an
endpoint, where the adjacent nonnegative formulas apply.

For a nonproductive triangle \(0\le h\le y/k\), put
\[
 A=4B(1-r)-(3+r)/2>0.
\]
The transformed residual is
\[
 \Delta=A h(y-dh/2)\ge0.                              \tag{24}
\]
A center wait has actual-value residual
\[
 \begin{cases}
  (A/2)h(y-dh/2),&h\le y/d,\\
  y^2(a-1/(2d)),&h\ge y/d.
 \end{cases}                                          \tag{25}
\]
Here \(a-1/(2d)=A/(4d)>0\). Also
\(\mathcal W_{nn}=-2b<0\) and
\(\mathcal W_n=-t/2-2by\le-\beta_t(n)/2\).
Thus (21) has the required concavity and finite rank-slope bound.

Equality in (23) occurs at
\[
 h_*=\frac{4By}{k}.
\]
The resulting balanced return state has new front gap
\[
 y'=\ell h_*=\theta y,\qquad
 \theta=4rB=\frac{1-w}{1+w}<1.
\]
Repeating equality actions gives a geometric sequence of tent lengths
and the finite accumulation time
\[
 t_\infty=t+\frac{4y}{kw(1+w)}.                       \tag{26}
\]
For \(r>0\) and \(y>0\), the individual gaps remain positive at every
finite step. The concatenated tents nevertheless define a continuous
unit-speed-bounded monster path: their heights tend to zero and the
path returns to center at \(t_\infty\). Each rank strictly below the
limiting captured frontier is caught during some finite tent; the one
limiting rank has zero rank measure. This justifies the accumulating
route directly. Equivalently, after \(N\) equality tents, a wait to the
same \(t_\infty\) leaves residual
\[
 [a-1/(2d)]y_N^2\longrightarrow0.                     \tag{27}
\]
This supplies a finite-route approximation without assuming continuity
of arbitrary hitting times.

If the whole characteristic wedge through \(t_\infty\) remains in the
affine region and its front continuation has the prescribed value in
(21), the equality chain supplies an actual local attainable solution.
The required outgoing inverse at a return lies before \(t_\infty\).
For a general tested triangle, however, the primitive \(T_e(n)\) may
leave the affine cell. Such a crossing must use the actual exterior
primitive. Nor is the state domain automatically invariant under every
return that happens to occur before the end of the cell: a productive
triangle can produce a rank above that cell's final center frontier.
Accordingly, (21) is a local verification component. Crossing actions,
front equality, and the outer attachment remain separate obligations.

This example explains why a blanket finite-return hypothesis would be
too restrictive for the center renewal problem. It does not assert that
the saved field has this exact cell shape, that an accumulating chain
is globally optimal in the game, or that every local affine cell
satisfies \(r<1/8\).

### Exact checks

The standalone pure-V8/CommonJS verifier
`verify_center_affine_renewal.cjs` uses six rational values of
\(w=\sqrt{1-8r}\), three \(k\)'s, two \(c\)'s, two departure times, and two
front gaps. It checks the Riccati, productive/nonproductive, wait,
slope, telescoping, and finite-truncation formulas with exact rational
arithmetic. Independently of those algebraic substitutions, it checks
direct rational line intersections for the legal local realization
\[
 p_q(s)=\max(0,(q-c-ds)/(k+\ell))
\]
before time one, followed by a common unit outward path to the endpoint
at time two. These physical checks include center contacts and triangle
peak equality.

The confirmed pure-V8 run passed **30,864 recorded checks**, including
16,320 direct capture intersections and 1,728 finite-truncation residual
checks. These are exact local formula and realization checks; they do
not certify a global continuation or a game value.
