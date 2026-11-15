# Reachable-defect attachment for center continuation

**Scope.** This is a lower-potential construction for the exact center
renewal of an ordered, fairly reflected princess law. It is not a claim
that the saved field is an equilibrium, that the resulting potential is
the exact center value, or that the unrestricted interval game has been
solved. The complete-game attachment before the first center visit
remains separate.

The field used in the concrete computation is
`packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json`,
Git blob `5c45d042ee9948faebc03354c3e1e2ee3cbec1a5`.
Its known pure-monster deficits are not removed by this computation.

## 1. Center renewal and the reachable relaxation

Use the notation of `CENTER_IMBALANCE_RENEWAL.md`. At center time \(t\),
both surviving radial tails start above the balanced captured rank
\(n\ge Z(t)\). Put
\[
 T_t(q)=\int_0^q\beta_t(r)\,dr.
\]
A productive triangle returning at \(e\) reaches
\(N=\max\{n,R(e,t)\}\) and has exact immediate cost
\[
 K(t,e;n)=\frac12\int_n^N[\beta_t(q)+\beta_e(q)]\,dq.
\tag{1}
\]
A wait uses its running center record, with its exact first-capture
moment. Closed capture traces are retained at center and endpoint
faces.

Fix a center barrier \(b\). Let \(E(t,n)\) be a valid immediate-exit
envelope: an infimum over a specified class of exit routes, followed
by a certified boundary continuation. Every continuation that leaves
the internal center region must be represented by one of these exit
options, or be pointwise dominated by one. In particular, center waits
and the closed endpoint jump must not be omitted merely because an
interior-turn formula has a convenient limit.

Suppose \(V_0\) verifies every internal triangle and wait:
\[
 V_0(t,n)\le K(t,e;n)+V_0(e,N),
\tag{2}
\]
and the corresponding wait inequality. Define
\[
 {\cal S}(t,n)=
 \{(s,m):t\le s\le b,\quad
 m\ge n,\quad m\ge Z(s),\quad
 m\le\max(n,R(s,t))\}.
\tag{3}
\]
The past-center floor \(m\ge H(s)\) may be added when
\(n\ge H(t)\); it preserves the argument below.

For any internal successor \((e,N)\),
\[
 {\cal S}(e,N)\subseteq{\cal S}(t,n).
\tag{4}
\]
Indeed \(N\ge n\), \(R(s,e)\le R(s,t)\), and
\(N\le\max(n,R(e,t))\le\max(n,R(s,t))\).
For a wait, the last bound follows because every center trace between
\(t\) and \(e\) is at most \(R(e,t)\).

## 2. Attachment theorem

Set
\[
 D(t,n)=\inf_{(s,m)\in{\cal S}(t,n)}
             [E(s,m)-V_0(s,m)],\qquad
 \widehat V=V_0+D.
\tag{5}
\]
Then \(D(t,n)\le D(e,N)\) along every internal action. Adding this
inequality to (2) proves the internal subsolution inequality for
\(\widehat V\). The current state belongs to \({\cal S}(t,n)\), so
\[
 \widehat V(t,n)\le E(t,n).
\tag{6}
\]
Thus \(\widehat V\) is attached to every exit option. It is a lower
potential for the complete center continuation represented by the
renewal and exit normal form.

For the compact continuous-field setting used here, take \(V_0\)
continuous and the exit defect lower semicontinuous. Along an
accumulating history, the reachable sets are nested compact sets
whose intersection is the reachable set of the limiting state.
Their defect infima increase to the limiting infimum: choose
minimizers, pass to a convergent subsequence, and use lower
semicontinuity. This prevents a loss at an accumulation of returns.
The bounded-horizon quantile approximation in
`CENTER_IMBALANCE_RENEWAL.md` supplies the passage from finite
canonical routes to unrestricted center continuations. For a more
general atomic field, these trace and limit hypotheses must be
verified rather than inferred from a sampled CDF.

An added constant in \(V_0\) cancels from (5). The construction does
not assert attainment. Equality requires a minimizing exit state
reachable through actions whose \(V_0\)-residuals vanish, followed by
an attaining exit. A rank cap or an inverse-cell assumption cannot be
dropped when making such an attainment claim.

## 3. Earliest-single-capture base

Every capture of either reflected copy of rank \(q\), starting from
center \(t\), occurs no earlier than \(\beta_t(q)\). Therefore
\[
 L(t,n)=T_t(1)-T_t(n)
\tag{7}
\]
is a universal balanced-tail lower potential.

For any fixed continuation \(\pi\), and \(n_1<n_2\),
\[
 C_\pi(t,n_2)-C_\pi(t,n_1)
 =-\frac12\int_{n_1}^{n_2}
       [\tau_{\pi,+}(q)+\tau_{\pi,-}(q)]\,dq
 \le-\int_{n_1}^{n_2}\beta_t(q)\,dq.
\tag{8}
\]
Consequently \(C_\pi-L\), and hence \(E-L\), is nonincreasing in the
rank. The rank minimization in (5) collapses exactly to
\[
 N_s=\max(n,R(s,t)),
\]
which already dominates every intervening center trace. Thus
\[
 \widehat V_L(t,n)=L(t,n)+
 \inf_{t\le s\le b}[E(s,N_s)-L(s,N_s)].
\tag{9}
\]
The exit family must be the same physical route class at every rank.
An equivalent useful-crossing formula may omit nonproductive turns
only after proving their domination by an included wait or endpoint
option.

For the saved field, all interior traces with \(V\ge1\) vanish.
With endpoint completion after time two, a center return at or after
one leaves only endpoint captures. Hence \(b=1\) is a global center
barrier. Its immediate exits are:

1. a triangle with return \(e\in[1,s+2)\), followed by the optimal
   endpoint continuation;
2. the closed endpoint action at \(e=s+2\);
3. a center wait until one, with its complete running-center-record
   capture cost, followed by the endpoint tour.

For a useful interior exit, write \(m=N_s\),
\(N=R(e,s)\ge m\),
\(I(s,e)=\int_s^eR(U,s)\,dU\), and
\(H(s)=\int_s^{s+2}R(U,s)\,dU\). Its defect is
\[
\begin{split}
4(E_e-L)(s,m)={}&4e+4-4s
 -(e+6-s)N-I(s,e)\\
&-2(e+1)m+2T_s(m)+2H(s).
\end{split}
\tag{10}
\]
The endpoint defect is
\[
 \frac12[(s+3)(1-m)-T_s(1)+T_s(m)].
\tag{11}
\]
Both formulas retain absolute capture times.

## 4. Exact reflected-pair base

For one radial path, let
\[
 u_t(q)=2\beta_t(q)-t.
\]
The exact center-start value of that reflected pair is
\[
 p(t,q)=\frac12[\beta_t(q)+\beta_{u_t(q)}(q)].
\tag{12}
\]
The first hit cannot precede \(\beta_t(q)\). Its outgoing
characteristic is at least \(u_t(q)\), because \(t+p_q(t)\) is
nondecreasing. The other copy therefore cannot be hit before
\(\beta_{u_t(q)}(q)\). Moving outward until the first hit and reversing
immediately attains these two times.

It follows that
\[
 P(t,n)=\int_n^1p(t,q)\,dq
\tag{13}
\]
is a universal balanced-tail lower bound and internal subsolution.
The characteristic \(u_t(q)\) is nondecreasing in \(t\). For ranks
captured by a triangle to \(e\), \(u_t(q)\le e\), so the second term
in (1) is no smaller than the second term in (12); the remaining
ranks have \(p(e,q)\ge p(t,q)\). Wait inequalities follow from the
same earliest-capture argument.

The fixed-route argument also makes \(E-P\) nonincreasing in rank.
However, at the global barrier,
\[
 P(1,m)=E(1,m)=3(1-m).
\]
Since \(P\) is already a pointwise pairwise lower bound, \(E-P\ge0\).
Every reachable set contains a state at \(s=1\), so its attached
defect is identically zero. Repeating the two-dimensional attachment
optimization for \(P\) cannot strengthen \(P\).

Maxima of separately certified lower potentials remain lower
potentials by monotonicity of the renewal operator. Thus \(P\), (9),
and locally attached affine potentials can be combined without
identifying any of them with the exact value.

## 5. Finite exact evaluation on a piecewise affine field

For a fixed rational state \((t,n)\), the source
\(m(s)=\max(n,R(s,t))\) is piecewise affine. Split at:

- characteristic-edge intersections of this source;
- its intersections with the affine inverse-cell images defining
  \(T_s(m(s))\);
- changes in the running center-record inverse;
- the ordinary field edges for \(R(e,s)\).

Equation (10) is then quadratic in \((s,e)\) on rational polygons.
The endpoint and wait defects are quadratic in \(s\). Their exact
minima occur among polygon vertices, stationary edge points, and
interior stationary points. Singular stationary directions reach a
lower-dimensional face, so the same finite list is complete.

The verifier generates this arrangement; it does not sample a
return-time grid. Extra quarter-point and full-moment identities
check the implementation. The degree statement follows from
integrating an affine CDF between affine characteristic boundaries,
not from the number of interpolation checks.

For (13), a first inverse \(u_t(q)\) is affine on each rank segment.
Intersect its graph \((u_t(q),q)\) with the second inverse-cell
arrangement. The composed inverse, hence \(p(t,q)\), is affine on
each resulting segment. Its exact rank integral is rational.
Endpoint rank intervals are included with their closed capture
times.

## 6. Completed computation and its limitation

At
\[
 t=57/64,\qquad n=10184278599/62500000000=Z(t),
\]
the exact single-capture base is
\[
 L=\frac{17353761934125903079}{16777216000000000000}.
\]
The entire global exit-defect minimum is
\[
 D_L=\frac{231472701107}{800000000000},
\]
attained at future center \(s=1\) with endpoint continuation. Thus
\[
 \widehat V_L=
 \frac{22208096314845375719}{16777216000000000000}
 \simeq1.32370569198402.
\]
The calculation covers 63 source pieces, 1,920 crossing-row pieces,
3,135 quadratic polygons, 12,651 feasible extremum candidates, and
7,479 additional exact primitive checks.

The exact reflected-pair integral is retained in the JSON report;
numerically,
\[
 P(t,n)\simeq1.35273608564425.
\]
It uses 31 first-inverse segments and 62 composed-inverse segments,
with 372 exact contact and affine identities. The separate terminal
fixture gives \(P(1,3/5)=6/5\). All 204 saved-field future-cone vertex
checks at \(V\ge1\) vanish exactly.

These are conditional future-capture costs for one center state.
The available affine-slab continuations there cost about 1.46, so
the two universal bases are materially loose. This computation
therefore directs the remaining proof toward the affine renewal and
its exterior attachment. It does not improve or certify an interval
game bound.

## 7. Affine-domain warning

For an affine wedge ending at \(b\), the internal inverse domain is
\[
 n\le R(b,t),\qquad
 n-Z(t)\le k(b-t).
\]
A productive return \(e<b\) stays in that domain precisely when
\[
 \ell(e-t)\le k(b-e).
\]
A potential based on the affine inverse must either check the actual
inverse correction beyond this boundary or treat the crossing as
an exit action. Restricting reachable states to this domain preserves
nesting, but the exit envelope must then include a boundary-crossing
triangle followed by the exact exterior continuation. Passing only
the direct exits does not certify this last branch.
