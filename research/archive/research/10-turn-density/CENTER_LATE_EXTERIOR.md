# Exact late center continuation by last-two deletion

## What this closes

For the immutable ordered field with Git blob
5c45d042ee9948faebc03354c3e1e2ee3cbec1a5, this note proves an exact
unrestricted center continuation value on the entire late slab
\[
 t_L\le t\le b=\frac{15}{16},\qquad Z(t)\le n\le1,
\]
where
\[
 t_L=\frac{9321277864605}{10363024948016}
 \simeq0.8994746139629393.                                               \tag{1}
\]
Here \(n\) is the captured radial prefix on both reflected sides. The value
equals the immediate exterior envelope: one useful return after \(b\),
followed by endpoint sweeps, or a direct endpoint tour. Arbitrarily many
earlier center returns, center waits, and accumulated return chains do not
improve it.

This is a conditional result for the specified field, not a value of the
whole interval game. Its initial-prefix constraints remain separate. The
source field has independent global attacks.

The proof uses the exact center factorization and first-center conventions
in CENTER_IMBALANCE_FACTORIZATION.md and
CENTER_RANK_REMOVAL_AND_EXTERIOR.md. The new ingredients are a complete
front exterior comparison, an exact last-two comparison, and a rank
monotonicity argument that removes the initial record from that comparison.

## 1. Notation and previously audited exterior gates

On
\[
 a=\frac78\le V\le U\le b=\frac{15}{16},
\qquad R(U,V)=kU-\ell V+c,\qquad Z(t)=dt+c,\quad d=k-\ell,
\]
the constants are
\[
 k=\frac{655898601421}{62500000000},\quad
 \ell=\frac{820954217}{12500000000},\quad
 c=-\frac{71289950193}{7812500000},\quad
 q_b=Z(b)=\frac{10184278599}{15625000000}.                                \tag{2}
\]
Let
\[
 A=\frac{k}{8}-\frac{\ell}{2},\qquad
 C_{\rm front}=(b+2)(1-q_b)+\frac d2b^2.
\]
The outgoing first-inverse moment is
\(T_t(n)=\int_0^n\beta_t(q)\,dq\). Use
\(W(t,n)=V(t,n)+T_t(n)/2\), where \(V\) is the absolute remaining
capture-time contribution of the balanced surviving rank tail.

The audited future barrier is
\[
 R(U,V)\le q_b\quad(V\ge b,\ \text{interior}),
\]
and all rows \(V\in[a,b]\) are flat once \(U\ge17/16\). The row at \(V=b\)
is constant in the interior. The comparison with the global affine inverse
model includes the closed endpoint jump; it is not inferred solely from
interior CDF domination.

For \(e\ge b\) and \(N\ge q_b\), the remaining balanced tail is endpoint-only:
\[
 V(e,N)=(e+2)(1-N).
\]
For an interior immediate return, put \(N=\max(n,R(e,t))\) and define
\[
 E_e(t,n)=\frac12[T_t(N)+T_e(N)-T_e(n)]+(e+2)(1-N).                       \tag{3}
\]
The direct endpoint action is
\[
 E_{\rm end}(t,n)=\frac12[T_t(1)+(t+3)(1-n)].                             \tag{4}
\]
Their lower envelope is \(E_W(t,n)\). Useful interior returns need only
\(b\le e\le17/16\); beyond that cutoff no new rank is added and all
remaining inverse and endpoint times are nondecreasing. The endpoint
action (4) is kept separately closed.

An exterior return with \(R(e,t)<n\) is empty for the balanced state. Its
endpoint-only remaining tail makes it no better than an endpoint tour.
It may therefore be omitted from the oracle, but it is not an uncovered
case in the response theorem.

## 2. The immediate front envelope

On the front \(n=Z(t)\), the action returning directly at \(b\) has
\[
 W_b(t,Z(t))
 =C_{\rm front}+\frac c2t+A(b-t)^2-\frac{3\ell}{2}(b-t).                  \tag{5}
\]
This follows from the actual rank primitive:
\(T_b(n)=bn\) below \(q_b\), whereas
\(T_b(n)=bn+n-q_b\) above \(q_b\). The linear endpoint contribution in
the latter formula is essential.

The complete exact geometric audit proves
\[
 \boxed{E_W(t,Z(t))=W_b(t,Z(t)),\qquad a\le t\le b.}                     \tag{6}
\]
It compares (5) with every actual crossing return and the endpoint
action. The source partitions the full \((t,e,n)\) geometry, imposes the
affine equality \(n=Z(t)\), and minimizes the resulting quadratic on every
rational polytope. It checks all vertices and all relevant stationary
faces.

There are 207 nonempty crossing regions, 513 vertices, 210 independent
primitive/source comparisons including the endpoint check, and no negative
residual. This statement concerns the immediate envelope only. Before the
late interval (1), repeated returns can beat this envelope; the exact
growing-chain front value is an example.

## 3. The last-two identity and elimination of the initial rank

Consider a productive internal return \(t\to u<b\), then a useful
exterior return \(u\to e\), with
\[
 n\le N_1:=R(u,t)\le N_2:=R(e,u),\qquad e\ge b.
\]
The transformed two-step cost is
\[
 Q(t,u,e;n)=E_e(u,N_1)
            +\frac12[T_t(N_1)-T_u(n)].                                 \tag{7}
\]
All subsequent endpoint captures are included in \(E_e\).

For comparison with a merged tent, let
\(\widehat N=R(e,t)\) at an interior merged return. The exact identity is
\[
\begin{split}
 2\bigl(E_e(t,n)-Q(t,u,e;n)\bigr)
 ={}&(e+3)(N_2-\widehat N)
 +T_t(\widehat N)-T_t(N_1)\\
 &+T_e(N_1)-T_e(n)-T_u(N_2)+T_u(n).                                   \tag{8}
\end{split}
\]
At a merged endpoint use the closed value \(\widehat N=1\); beyond it,
a capped tent is legal but a direct endpoint action can be better.

A blanket same-exterior merge is false for this field. An independent
physical-capture regression exhibits positive values of (8). The proof
uses the direct-\(b\) comparator instead.

For fixed \(t,u,e\), differentiate the difference between the direct-\(b\)
action and (7) with respect to \(n\):
\[
 \frac{\partial}{\partial n}
 [E_b(t,n)-Q(t,u,e;n)]
 =\frac12[\beta_u(n)-\beta_b(n)]\le0.                                   \tag{9}
\]
The direct-\(b\) action remains useful because
\(R(b,t)\ge R(u,t)=N_1\). First-inverse jumps cause no problem: the finite
increment version of (9) is the integral of the same nonpositive
difference. Therefore the worst initial rank is the front \(n=Z(t)\).

For an endpoint as the second action, replace \(E_e(u,N_1)\) in (7) by
\(E_{\rm end}(u,N_1)\). The rank derivative is still
\(-\beta_u(n)/2\), so the same reduction applies.

## 4. Complete late front comparison

Define
\[
 H_1=\frac{6\ell}{k-2\ell}
     =\frac{24628626510}{647689059251},
 \qquad t_L=b-H_1.                                                     \tag{10}
\]
The exact source proves
\[
 Q(t,u,e;Z(t))\ge W_b(t,Z(t))                                          \tag{11}
\]
on the full region
\[
 t_L\le t\le u\le b,\qquad
 b\le e\le17/16,\qquad R(e,u)\ge R(u,t).
\]
The second endpoint action is included in a separate exact comparison.

The field inverse at the exterior return is retained. In particular,
\(T_e(R(u,t))\) is evaluated on its actual center, incoming, or endpoint
piece. Neither an affine extrapolation of that moment nor a claim that
the field is flat immediately after \(b\) is used.

The audit uses 130 nonempty crossing regions, 582 vertices, 133
independent primitive/source comparisons including the endpoint case,
and all exact quadratic stationary faces. The minimum is zero on
degenerate equality faces and there are no negative residuals.

Combining (9) and (11) gives
\[
 E_W(t,n)\le E_b(t,n)\le Q(t,u,e;n)                                    \tag{12}
\]
for every \(Z(t)\le n\le R(u,t)\). Thus every productive internal
triangle followed by an exterior action is dominated by an immediate
exterior action. The comparison is uniform over the initial record;
it is not only a front-state theorem.

If the proposed second exterior return has \(R(e,u)<N_1\), it is empty
for the balanced state at \(u\), and the endpoint alternative dominates
it. It is therefore covered by the separately checked endpoint case,
not silently excluded by the last inequality in (11).

## 5. Waiting, empty actions, and unbounded return counts

### Productive front waits

A center wait from front time \(t\) to front time \(u\) captures the
intervening ranks on both signs. Because \(Z(s)=ds+c\), its transformed
cost followed by the exterior envelope is
\[
 E_W(u,Z(u))-\frac c2(u-t).                                             \tag{13}
\]
By (5)--(6), put
\[
 C_E(t)=E_W(t,Z(t))-\frac c2t
       =C_{\rm front}+A(b-t)^2-\frac{3\ell}{2}(b-t).
\]
On \([t_L,b]\),
\[
 C_E'(t)=\frac{3\ell}{2}-2A(b-t)
 \ge\frac{3\ell^2}{k-2\ell}>0.                                         \tag{14}
\]
Thus an immediate exterior action is no more costly than a productive
front wait followed by the exterior envelope.

### Empty prefixes and off-front waits

If a wait or triangle captures no surviving rank, absorb it into the
first exterior tent that follows. Extending that tent back to the earlier
center time catches its chosen-side ranks no later. No opposite surviving
rank had been caught during the empty prefix, so none is lost. A capped
tent or the direct endpoint tour handles an endpoint-first action.

For an off-front productive wait, split it at the first time the increasing
front reaches the current record. The preceding wait is empty; the
remaining wait is a front wait governed by (13)--(14). This proves the
wait inequality for every record, not only \(n=Z(t)\).

### Arbitrary later histories

For a finite canonical center history, apply (12) to the final productive
internal triangle and its exterior continuation. Productive waits use
(13)--(14); empty pieces are handled above. Induction removes all internal
actions. This proves that \(E_W\) is a lower Bellman potential as well as
a feasible upper continuation.

For arbitrary speeds and accumulated return histories, use the established
uniform quantile approximation. A uniform error in an ordered CDF gives
a uniform error in each running capture record and hence a uniform payoff
error on the common endpoint-completion horizon. Finite capture-order
routes suffice for each finite quantile law. Taking the limit transfers
the inequality without assuming an attained first productive event or a
finite number of center returns. Lower semicontinuity alone is not used
to justify this passage.

Consequently,
\[
 \boxed{
 W(t,n)=E_W(t,n),\qquad
 t_L\le t\le b,\quad Z(t)\le n\le1.
 }                                                                     \tag{15}
\]

## 6. Joining the earlier high-record region

The earlier rank-removal certificate uses only the front lower bound
\(B(t)=C_*+ct/2\), which is valid on all \([a,b]\). Its use does not require
front equality. The same polynomial threshold
\[
 n_{\rm crit}(t)=
 \frac{J(t)-C_*-[ct+bZ(t)]/2}{1-b/2}
\]
therefore extends beyond the growing-chain equality time \(\tau\).

The combined verifier checks the whole interval \([a,t_L]\) and proves
\[
 Z(t)<n_{\rm crit}(t)<q_b,\qquad
 R(t,0)>n_{\rm crit}(t).
\]
The exact minimum margins are displayed approximately as
\(0.3067719812\), \(0.08978341108\), and \(0.009420356584\), respectively.
The threshold at \(t_L\) is approximately \(0.5620104193\). All decisions
use exact quadratic-field arithmetic.

It follows that
\[
 W(t,n)=E_W(t,n),\qquad
 a\le t\le t_L,\quad n_{\rm crit}(t)\le n\le1.                           \tag{16}
\]
Together, (15)--(16) cover all late records and all earlier high records.
They bypass the narrow front-count transition between \(\tau\) and \(t_L\).

The incidental bound \(B>3/2\), valid on the previous shorter interval,
does not extend: \(B(t_L)\simeq1.4999795810\). This has no role in
(15)--(16). Low-record first-center prefixes before \(t_L\) are being
checked by a separate shared-light-cone capture-moment certificate.

## 7. Replay and reusable hypotheses

The standalone source verify_center_late_exterior.cjs is both a native
CommonJS wrapper and a pure function body. It can be run as
\[
 \texttt{node verify\_center\_late\_exterior.cjs FIELD.json}
\]
or \(\texttt{Function(source)().verify(fieldData)}\).

The complete report contains:

- the full immediate-front exterior comparison;
- the full front-rank last-two comparison and its positive wait derivative;
- 36 independent signed-record two-tent capture identities, 24
  rank-monotonicity regressions, and 9 endpoint-second-action capture
  identities;
- the exact extended high-record margins through \(t_L\).

The independent physical engine begins with balanced signed records
\((1-n)/2,(1+n)/2\) and integrates actual first captures along each unit
leg. It does not call the renewal formula being checked.

For another candidate field, the reusable sufficient hypotheses are the
future endpoint-tail barrier, a complete immediate front envelope, the
rank-reduced last-two comparison, the front-wait inequality, and the
quantile approximation/trace assumptions. The rational coefficients and
polytope inequalities in this packet are specific to the immutable field.
No claim of robustness under arbitrary nodal perturbations is made.
