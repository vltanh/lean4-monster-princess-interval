# A shared travel-budget bound for arbitrary same-side prefixes

## Scope

This concerns the fixed complete radial CDF in
`packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json`
(Git blob `5c45d042ee9948faebc03354c3e1e2ee3cbec1a5`). It is a local
all-path exclusion, not a global game value or a matching strategy.

The center-arrival interval is

\[
 t_0=\frac78,\qquad
 t_L=\frac{9321277864605}{10363024948016}
       \simeq0.8994746139629393.
\]

The center analysis in `CENTER_RANK_REMOVAL_AND_EXTERIOR.md` supplies an
increasing threshold \(N(t)=n_{\rm crit}(t)\), an exact exterior value
\(E_W(t,n)\), and the following facts on this entire interval:

\[
 Z(t)<N(t)<I(t):=R(t,0),\qquad
 W(t,n)=E_W(t,n)\quad\text{for }n\ge N(t).
\tag{1}
\]

The front lower bound used to prove (1) remains valid beyond its interval
of exact equality. Consequently this argument does not assume an exact
front formula on the small interval between the Zeno threshold and
\(t_L\).

The exact certificate proves that **every positive prefix whose
first center visit is at \(t\in[t_0,t_L]\) and whose upper captured rank
is \(n\le N(t)\) has total optimally continued cost at least**

\[
 \frac{7131}{5000}=1.4262.
\tag{2}
\]

The finite rational certificate for (2) is recorded in
`shared_prefix_budget_certificate.json`; its independent replay is
`verify_shared_prefix_budget.cjs`. No bound
on the number of turns, no unit-speed restriction, and no prescribed
final-turn direction is imposed on the prefix.

## 1. Prefix records and the common state

Let the monster start at \(+a\), remain strictly positive before its first
center visit at time \(t\), and have arbitrary speed at most one. Write

\[
 U_s=s+m(s),\qquad V_s=s-m(s).
\]

Both coordinates are nondecreasing. Before the first center visit,

\[
 a\le U_s\le t,\qquad -a\le V_s<U_s,\qquad U_s+V_s=2s.
\tag{3}
\]

Let \(M_s,L_s\) be the running closed upper and strict lower radial rank
records. The positive-copy ranks already captured form the interval
\([L_s,M_s]\). At the center put \(n=M_t\), and set the lower record to
zero, including the center atom. The unweighted positive-copy capture
moment is exactly

\[
 \mathcal M=\int_0^n\tau_q^+\,dq
 =tn-\int_0^t(M_s-L_s)\,ds.
\tag{4}
\]

The optimized full cost after this prescribed prefix is

\[
 G=W(t,n)+\frac12\mathcal M.
\tag{5}
\]

Equation (5) includes the first-center captures of negative copies. Their
contribution cancels the center transformation term; it must not be
added a second time.

Monotonicity of the radial CDF gives, at every pre-center state,

\[
 M_s\le\min\{n,R(U_s,-a)\},\qquad
 L_s\ge
 \begin{cases}
 R_{\rm strict}(a,V_s),&V_s<a,\\
 0,&V_s\ge a.
 \end{cases}
\tag{6}
\]

The two records in (6) share the **same** \((U_s,V_s)\). Optimizing their
bounds independently would incorrectly combine the fastest inward and
outward rays from the initial position. That weaker relaxation does not
clear the required threshold near the end of the interval.

## 2. One enclosure for an entire interval of initial positions

Fix \(0\le l\le a\le h<1\). The frozen field has a continuous initial
CDF \(A\) and a continuous radial CDF at positive interior positions.
Define

\[
 F_h(U)=
 \begin{cases}
 A(h),&l\le U<h,\\
 R(U,-h),&h\le U\le1,
 \end{cases}
\]

and

\[
 G_l(V)=
 \begin{cases}
 A(l),&-h\le V<-l,\\
 R(l,V),&-l\le V<l,\\
 0,&l\le V\le1.
 \end{cases}
\tag{7}
\]

The left trace at \(V=l\) is retained as a separate trace in the
piecewise-linear calculation. Setting the right side to zero relaxes
lower-record information; it does not assert that the monster actually
visited the center there.

For \(U<h\), the upper bound follows from
\(R(U,-a)\le A(U)\le A(h)\). For \(U\ge h\), it follows from
\(R(U,-a)\le R(U,-h)\). The lower bound in (7) also holds throughout the
past history. In particular, while \(V<-l\), ranks initially below
\(l\) cannot yet have crossed the monster: their own nondecreasing
\(V\)-coordinates start above \(-l\). For \(-l\le V<l\), use the lower
initial coordinate \(l\) and CDF monotonicity. Thus

\[
 M_s-L_s\le\min\{n,F_h(U_s)\}-G_l(V_s).
\tag{8}
\]

For any auxiliary rank \(r\in[0,1]\), set

\[
 e_{l,h,r}(s)=\max\left(0,
 \max_{\substack{l\le U\le1,\;-h\le V\le U\\U+V=2s}}
 [\min\{r,F_h(U)\}-G_l(V)]\right),
\]

\[
 J_{l,h}(r)=r-\int_0^1e_{l,h,r}(s)\,ds.
\tag{9}
\]

The upper horizon one in (9) is an auxiliary coordinate bound. It is not
an assumption that the original monster stops moving at time one.
For the actual prefix, (3) lies inside its feasible set.

At the actual arrival time, \(F_h(t)\ge n\) and \(l\le a\le t\).
For every \(s\in[t,1]\), the diagonal state \(U=V=s\) therefore gives
\(e_{l,h,n}(s)=n\). Consequently (4), (8), and (9) imply

\[
 \boxed{\mathcal M\ge J_{l,h}(n).}
\tag{10}
\]

This is an inequality for every continuous admissible prefix, including
arbitrary slow motion and accumulating turns. The finite arrangement
below evaluates a relaxation of its records; it is not a canonical-path
claim.

## 3. Lifting a low rank to the known center boundary

For fixed \(s\), the function \(r\mapsto e_{l,h,r}(s)\) is nondecreasing
and one-Lipschitz. Hence \(J_{l,h}\) is nondecreasing.

If \(n\le N=N(t)\), then (1) gives
\(F_h(t)\ge I(t)>N\). Both rank envelopes equal their full ranks for
\(s\ge t\). Thus

\[
 J_{l,h}(N)-J_{l,h}(n)
 =t(N-n)-\int_0^t[e_{l,h,N}(s)-e_{l,h,n}(s)]\,ds
 \le t(N-n).
\tag{11}
\]

The general center rank-removal inequality is

\[
 W(t,n)\ge W(t,N)+\frac12\int_n^N\beta_t(q)\,dq.
\]

Every first inverse \(\beta_t(q)\ge t\). Combining this with
(5), (10), and (11) proves

\[
 \boxed{G\ge E_W(t,N(t))+\frac12J_{l,h}(N(t)).}
\tag{12}
\]

The argument never differentiates an envelope switch. It also never
uses the early-productivity comparison as an unconditional lower bound
on all center continuations.

## 4. Monotonicity of the complete exterior envelope

For this field the proved exterior truncation retains the common return
interval \(e\in[b,17/16]\), where \(b=15/16\), together with direct
endpoints. Every retained tent is feasible for every arrival time under
consideration; longer nonendpoint returns are already dominated. For a
fixed retained return, let
\(N_i=\max\{n,R(e,t_i)\}\) for \(t_1<t_2\). Then \(N_1\ge N_2\).
Retain nonproductive returns in this comparison. With
\(T_t(r)=\int_0^r\beta_t(q)\,dq\), the action is

\[
 W_e(t,n)=\frac12[T_t(N)+T_e(N)-T_e(n)]+(e+2)(1-N).
\]

Subtracting its two values gives

\[
 W_e(t_2,n)-W_e(t_1,n)
 =\frac12[T_{t_2}(N_2)-T_{t_1}(N_2)]
 +\frac12\int_{N_2}^{N_1}
 [2e+4-\beta_{t_1}(q)-\beta_e(q)]\,dq\ge0.
\tag{13}
\]

The first term is nonnegative by inverse monotonicity. If the integral
is nonempty, \(N_1=R(e,t_1)\), so
\(\beta_{t_1}(q)\le(e+t_1)/2\), while \(\beta_e(q)\le e+1\).
The integrand is therefore at least \(3+(e-t_1)/2>0\).
The direct endpoint alternative is also nondecreasing in \(t\).
Taking the common action envelope shows that \(E_W(t,n)\) is
nondecreasing in time and nonincreasing in rank.

On any time box \([t_-,t_+]\), choose rational bounds

\[
 r_-\le N(t_-),\qquad r_+\ge N(t_+).
\]

Equations (12), (13), and rank monotonicity give the entire-box bound

\[
 \boxed{G\ge E_W(t_-,r_+)+\frac12J_{l,h}(r_-).}
\tag{14}
\]

The threshold polynomial is increasing on the whole interval. Its
reachability margin \(I-N\) is a concave quadratic, so checking its two
endpoints certifies positivity. Also \(A(81/100)>N(t_L)\); the initial
cover \(0\le a\le81/100\) contains every low-record prefix.

## 5. Exact finite envelope verification

For fixed rational \((l,h,r)\), both functions in (7) are piecewise
linear. Insert the crossings \(F_h(U)=r\). On every resulting rectangle
in \((U,V)\), the reward in (9) is affine. Its maximum on a fixed
\(U+V=2s\) slice is attained at an edge of that rectangle clipped by
\(U\ge V\).

It is therefore enough to retain these complete edge families:

1. Every vertical line through a breakpoint of \(\min(r,F_h)\).
2. Every horizontal line through a breakpoint of \(G_l\), retaining both
   traces at its jump.
3. The physical diagonal \(U=V\).
4. The zero reward.

Every edge gives an affine function of \(s\) on an exact rational
interval. The implementation constructs a piecewise-affine upper
envelope. A separate static check compares every candidate to that
envelope at both endpoints of each positive-length overlap, and checks
nonnegativity and coverage. Isolated endpoint values do not affect the
area; the verifier does not demand that an interval's one-sided trace
majorize an unrelated trace at a single shared endpoint.

All areas are then integrated as rational numbers. The exterior oracle
uses the already-audited complete last-crossing arrangement, including
quadratic stationary points and endpoint alternatives. Adaptive boxes
are used solely to verify the explicit two-variable inequality (14).
They add no monster/princess support and impose no discretization on
admissible paths.

The saved certificate lists every accepted time/initial-position box,
its rank bounds, exact exterior value, exact moment bound, and rational
comparison with (2). A replay must also verify that these boxes and the
explicitly infeasible boxes cover the initial rectangle.

## 6. What this resolves

The recorded finite certificate passes. All low-record first-center
arrivals in \([7/8,t_L]\) are strictly slack relative to the current
certified upper ceiling. At higher records the unrestricted center
continuation is exactly the exterior envelope by (1); at times
\(t\ge t_L\), `CENTER_LATE_EXTERIOR.md` supplies all-record
exterior equality through \(b=15/16\).

The dependencies are therefore explicit: the rank-removal/exterior
threshold theorem supplies (1) through \(t_L\); this prefix certificate
excludes low-record **first** arrivals there; the late exterior theorem
covers all records from \(t_L\) onward. This does not declare low-record
intermediate center states slack, because they do not have the initial
prefix moment used in (5).

This closes the low-record same-side-prefix gap in this slab. It does
not make the frozen field a global lower strategy, prove a matching
saddle, or cover first-center arrivals outside the stated interval.


## 7. Reproduction and replay result

With the repository dependencies present, run:

```sh
node packages/interval_turn_sheet/verify_shared_prefix_budget.cjs
```

The CLI accepts explicit field, certificate, exterior-oracle, and area-module
paths after its optional repository root argument. The exported
`verifySharedPrefix(fieldData, certificate, oracleModule, areaModule)`
function also supports a direct in-memory replay.

The saved replay passes:

- 874 accepted boxes, with no discarded region and 22 distinct time slabs
  in the independent coverage sweep.
- 12,385 logical, transport, rank-enclosure, and coverage checks.
- 3,061,252 exact candidate/envelope endpoint comparisons.
- 7,542 complete-exterior primitive and quadratic identities.
- 108 independent physical-prefix moment comparisons, including direct
  outward/inward paths and prefixes with additional same-side turns.

The smallest recorded rational enclosure is

\[
\frac{16385201286137840537456238199878549282378183289053}
{11488705337148601898000000000000000000000000000000}
\simeq1.4262008472927297>\frac{7131}{5000}.
\]

This number is a verification margin for the fixed-field exclusion; it
is not an optimized game value or a new lower bound for the whole game.
