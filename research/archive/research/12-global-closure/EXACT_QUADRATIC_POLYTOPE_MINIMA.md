# Finite exact checking of quadratic boundary guards

This lemma supplies the boundary checker for an actual-record Bellman
certificate. It is a finite exact optimization result, not a claimed new
game value or a bound on the number of equilibrium pieces.

Let

\[
P=\{x\in\mathbb R^d:Ax\le b,\ Ex=f\},\qquad
q(x)=c+\ell^Tx+x^THx,
\]

where all data are rational, `H` is symmetric, and `P` is compact. For the
application `d <= 4`, and boundary guards normally have dimension at most
three. The minimum can be obtained with rational linear algebra alone.

## 1. Candidate list

Reduce `Ex=f` to an equivalent independent system, first checking
consistency. For every subset of inequality rows whose combined rank with
`E` can be at most `d`, consider their equality face. Write its independent
equations as `Cx=h`. Its stationary system is

\[
\begin{pmatrix}2H&C^T\\ C&0\end{pmatrix}
\begin{pmatrix}x\\\lambda\end{pmatrix}
=\begin{pmatrix}-\ell\\h\end{pmatrix}.                 \tag{1}
\]

If this square system is nonsingular, solve it over the rationals and
retain `x` exactly when it lies in `P`. Include every vertex of `P`; these
can be enumerated directly by `d` independent active equations, including
the fixed equalities. Discard inconsistent or dependent equation choices.

The smallest retained objective value is the exact global minimum. There
is no requirement that the Hessian be positive semidefinite. Saddle or
maximum stationary points do not invalidate the test: every retained
point is feasible, and the complete list contains a global minimum.

## 2. Why singular stationary families can be skipped

Take a global minimizer `x` in the relative interior of its minimal face
`F`. Its gradient is orthogonal to every tangent of `F`, so (1) has a
solution for an independent defining system `C` of that face.

If the matrix in (1) is singular, choose a nonzero null vector `(z,mu)`.
It satisfies

\[
Cz=0,\qquad 2Hz+C^T\mu=0.
\]

Independence of the rows of `C` implies `z != 0`: if `z=0`, then
`C^T mu=0` would force `mu=0`. Moreover,

\[
\nabla q(x)^Tz=0,\qquad z^THz=0,
\]

so `q(x+t z)=q(x)` for every real `t`. Because `x` is in the relative
interior, a nontrivial interval of these points stays in `F`. Because `F`
is compact, that interval has a finite endpoint at which an additional
independent inequality becomes active. Move to that endpoint, preserving
the minimum value.

Repeat on the smaller minimal face. Its dimension decreases strictly each
time. In at most `d` such steps the minimizer has either a nonsingular
stationary system or is a vertex. Both types are in the candidate list.
Thus discarding singular systems is complete, including flat directions,
singular Hessians and lower-dimensional input polytopes.

In particular, some minimum point is rational and the minimum value is
rational. This does not assert that every minimizer is rational.

## 3. Feasibility and boundedness are checked

The implementation does not silently assume compactness. If vertex
enumeration has not supplied a feasible point, it applies the same
active-face method to `||x||^2`. That strictly convex coercive objective
has an attained minimum on every nonempty closed polyhedron, even an
unbounded one. Every independent equality-restricted stationary system is
nonsingular. Thus failure to find a feasible candidate certifies that the
input set is empty.

For a nonempty polyhedron, its recession cone is

\[
K=\{z:Az\le0,\ Ez=0\}.
\]

The polyhedron is bounded exactly when `K={0}`. Intersect `K` with the
unit coordinate box. Every nonzero recession direction has a nonzero
multiple in this box; a compact polytope containing a nonzero point must
have a nonzero vertex. Exact vertex enumeration therefore either proves
boundedness or returns a rational nonzero recession direction. In the
latter case the checker rejects the domain and returns that direction
with a feasible starting point. It does not report a finite minimum on
an unbounded domain, even if that particular objective happens to have
one.

## 4. Implementation and use

`packages/interval_global_closure/record_bellman/exact_quadratic_polytope.py`
uses only Python's standard library and `Fraction`. Floating coefficients
are rejected. Its interface is

```python
result = minimize_quadratic(
    inequalities, c, linear, hessian, equalities=()
)
```

Each constraint is `(coefficient_vector, rhs)`. A nonempty bounded domain
returns the exact value, an attaining rational point, and enumeration
counts. An empty domain returns `None`. An unbounded domain raises
`UnboundedPolytope` with exact feasibility and recession witnesses.

To certify `q >= 0` everywhere, check that the returned minimum is
nonnegative; an empty domain is vacuous. To certify `q <= 0`, negate the
objective. This accepts quadratic Bellman boundary guards without relying
on the stronger sufficient condition that every quadratic polar
coefficient be nonnegative.

The standalone regression compares 100 interval cases with independent
one-variable calculus, 160 rectangles and 80 oblique rational polygons
with separate edge/interior critical-point formulas, and manufactured
two-, three- and four-dimensional minima. It explicitly checks singular
stationary sets, equality faces, implicit point domains, empty domains,
unbounded recession witnesses, and malformed-input rejection.

```sh
python packages/interval_global_closure/record_bellman/test_exact_quadratic_polytope.py
```

This finite checker establishes a supplied guard inequality. The separate
Bellman theorem must still prove that all necessary guards and bulk
controls are present and that they imply the desired all-Monster bound.
