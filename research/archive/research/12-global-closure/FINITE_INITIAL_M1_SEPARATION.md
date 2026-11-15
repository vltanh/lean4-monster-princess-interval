# Complete M1 separation at the finite initial support

## Pointwise reduction, including initial atoms

Let a princess path p be 1-Lipschitz in [-1,1]. Write
\[
\alpha_p(u)=\inf\{t:t+p(t)=u\},\qquad
\beta_p(v)=\inf\{t:t-p(t)=v\}.
\]
First contact, including equality at time zero, is always used.

A Monster starting at a, moving left to -1 and then right to +1, catches p at
\[
\tau_p^-(a)=
\begin{cases}
\alpha_p(a),&p(0)\le a,\\
\beta_p(a+2),&p(0)>a.
\end{cases}
\]
The first branch is the earliest possible left contact. In the second branch, the first left leg cannot catch p because \(p(t)-(a-t)\) is nondecreasing and initially positive. The second leg has constant characteristic \(t-x=a+2\). The interval bound ensures its first inverse lies between \(1+a\) and \(3+a\).

For a right-first sweep the formula is
\[
\tau_p^+(a)=
\begin{cases}
\beta_p(-a),&p(0)\ge a,\\
\alpha_p(2-a),&p(0)<a.
\end{cases}
\]

Suppose the initial law is supported on a finite set S. On a gap in S, the classification in each formula stays fixed. Both left-first inverse targets increase with a, so its cost is nondecreasing. Both right-first targets decrease with a, so its cost is nonincreasing.

At an initial-support endpoint, the coincident atom is captured at time zero. Thus a left-first sweep inside a gap is pointwise dominated by the sweep at its left support endpoint; a right-first sweep is pointwise dominated by the sweep at its right endpoint. Add -1 and +1 for the exterior gaps. Consequently
\[
\inf_{a\in[-1,1],\,d=\pm1} C_{M1}(a,d)
=\min_{a\in S\cup\{-1,1\},\,d=\pm1} C_{M1}(a,d).
\]

This statement does not require finite support in the whole path space, endpoint absorption, smooth densities, or any temporal coupling assumption. Finite initial support is enough. Quantile ordering preserves the initial marginal, so the same complete separator applies to the ordered law.

## Rational-germ version

For a finite collection of physical paths over \(\mathbb Q(\epsilon)\), keep distinct ACTUAL initial germs even when their limits agree. On a common sufficiently small positive interval their order is fixed. The pointwise argument above holds for every epsilon in that interval and every real Monster start, including starts depending arbitrarily on epsilon. It reduces the entire M1 family to the finite list of exact initial-germ routes.

Each retained route is physically frozen. A later subordinate re-realization of an abstract query profile is a new Princess row, not a replacement for an old row after a Monster has learned its initial position.

## Fast ordered-law first-moment formula

Consider a left-first sweep from a. Let I_i indicate \(p_i(0)\le a\), let
\[
A_i=\alpha_{p_i}(a),\qquad B_i=\beta_{p_i}(a+2),
\qquad m=\sum_i w_i I_i.
\]
Set (A_i=0) when (I_i=0), so no inverse below the initial value is used. The first-leg moment is \(\sum_i w_i I_iA_i\), independently of the temporal coupling. Under the comonotone coupling, the second-leg surviving rank interval has mass \(1-m\) and consists of the largest \(B_i\)'s, with weighted partial groups at the cutoff. Therefore the exact ordered cost is the first moment plus that weighted upper-tail moment.

The same construction applies to a right-first sweep, using its first inverse and the upper tail of \(\alpha_i(2-a)\). The implementation retains strict/closed initial contact and exact equality times.

For normalized weights, the weighted upper-tail identity is
\[
C(w)=\min_\theta\sum_i w_i\left[
 I_i A_i+(1-I_i)\theta+(B_i-\theta)_+
\right].
\]
At a selected cutoff theta the displayed coefficient vector is an exact supergradient in the weights. It gives a supporting linear upper plane for every other nonnegative weight vector. No running-record branch needs to be approximated.

The continuation-independent ceiling is
\[
K(w)=\sum_iw_i\bigl[I_i A_i+(1-I_i)(3+a)\bigr].
\]
It is linear in the fixed prefix law. Holding that prefix fixed, no later modification can exceed K against this Monster.

## Rejected159-row example

The frozen clipped dictionary is blob fe415d4ca2938a8503bedf0bfea432f540ce4569. Its weights are the exact recorded decimal rationals, normalized. It has45 distinct limiting positive radii but62 distinct actual positive initial germs. The complete list has126 signed starts and252 M1 routes.

The minimum is attained by the reflected pair of routes whose positive start is
\[
a_\epsilon=15/16-\epsilon,
\]
followed by the left endpoint at \(31/16-\epsilon\) and the right endpoint at \(63/16-\epsilon\). Its exact limiting ordered cost is
\[
\frac{4115606858452227030094659793}
{3276799999999999976930082816}
\simeq1.2559835383460167.
\]
The first leg captures mass
\[
\frac{88240967097144535002781}
{99999999999999999295962}
\simeq0.88240967.
\]
Even an ideal remaining tail cannot exceed
\[
\frac{1397113958465290679188261275}
{1092266666666666658976694272}
\simeq1.2790960313097754.
\]
Thus this candidate requires an early/initial-law correction. A microscopic connector change or tail replacement alone cannot repair it.

## Verification and replay

All252 first-inverse costs were compared exactly with the independent strict/closed running-record scorer. Every supporting plane reproduces the original weighted score. The complete comparison has common radius \(1/320000000000000000\).

Six smaller fixtures additionally check66 record identities,66 direct segment-capture identities,54 gap-dominance inequalities, and132 supergradient inequalities under changed weights. They retain initial ties, distinct germs with the same limit, rational speeds, and path crossings.

```sh
node packages/interval_global_closure/verify_m1_germs.mjs \
  packages/interval_global_closure/germ_v8_fixture_inputs.json \
  m1_fixture_report.json

node packages/interval_global_closure/audit_m1_germs.mjs \
  clipped159_dictionary.json m1_report.json SHARED_HYDRATOR.cjs \
  m1_record_report.json
```

The shared hydrator is blob1ba70ffcb1bd571675eae9894a7f7d325b304a87. The optional final argument is the independently generated record report, blob7ee2af6f3720c98d8176461392f76cc9cafd4181. The constructor uses actual physical vertices throughout. Complete M1 separation is not an all-monster lower certificate.
