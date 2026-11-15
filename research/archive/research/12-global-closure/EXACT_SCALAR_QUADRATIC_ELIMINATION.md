# Exact elimination of a bounded scalar decision

This algebraic component implements one renewal step for a finite quadratic
center-value envelope. It is not an independent game-value certificate.

Let the parameters be theta and the scalar decision be h. Suppose the
objective is a rational quadratic

\[
q(\theta,h)=c+\ell\cdot(\theta,h)+(\theta,h)^T H(\theta,h),
\]

where H is a fixed rational symmetric matrix. Impose finitely many rational
affine inequalities and a fixed finite rational interval a <= h <= b.
Every nonempty fiber in h is a compact interval, possibly a singleton.

## Finite candidate construction

Each inequality with a nonzero h coefficient gives an affine boundary
candidate h=h_i(theta). Substitute that candidate into every original
inequality and the interval bounds. The resulting eligibility domain is a
rational polyhedron in theta. Substitution into q gives a rational quadratic
q_i(theta). Every eligible candidate is a feasible actual decision.

The coefficient alpha=H_hh is constant. If alpha is positive, also include
the unique stationary candidate

\[
h_*(\theta)=-\frac{\ell_h+2H_{h,\theta}\theta}{2\alpha}.
\]

Its eligibility domain is obtained by the same substitution. If alpha is
zero or negative, the minimum of the affine or concave fiber quadratic is
at a fiber endpoint, so no stationary candidate is needed. A constant fiber
objective is covered by its endpoints as well.

Each endpoint of a nonempty bounded fiber makes at least one inequality
with nonzero h coefficient an equality. Hence the list includes both
endpoints. The elementary one-variable quadratic minimum theorem proves

\[
\min_{h\text{ feasible}}q(\theta,h)
 =\min_{i:\,\theta\in D_i}q_i(\theta).
\]

The right side has no eligible candidate exactly when the fiber is empty.
Equalities can be expressed as pairs of weak inequalities; degenerate
parameter faces and singleton h-fibers require no generic-position rule.

This describes a finite lower envelope with polyhedral *eligibility*
domains. The regions where candidates actually win can have quadratic
boundaries; the construction neither needs nor claims a polyhedral winner
partition. In a center recurrence, the original field charts and the
continuation candidate's eligibility inequalities supply the affine rows.
Each recurrence step remains in the same finite-envelope class. A separate
finite response theorem must justify how many steps suffice.

## Implementation and independent checks

`packages/interval_global_closure/record_bellman/eliminate_quadratic_interval.py`
implements this construction using only rational arithmetic. It retains
all nontrivially eligible domains; it does not silently discard a candidate
because numerical sampling failed to find a point. False constant domains
are rejected exactly. Positive multiples and tautological inequalities are
removed without changing a domain.

The independent regression fixes rational parameter values, computes the
feasible h interval directly, solves its scalar quadratic, and compares the
answer with the generated envelope. It also evaluates the original
polynomial at every eligible candidate, independently of the coefficient
substitution. Tests include convex, concave, affine and constant h behavior,
zero parameters, lower-dimensional domains, empty and singleton fibers,
and malformed rational inputs.

```sh
python packages/interval_global_closure/record_bellman/test_eliminate_quadratic_interval.py
```
