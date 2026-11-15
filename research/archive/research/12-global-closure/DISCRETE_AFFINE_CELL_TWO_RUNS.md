# Two corner orders for the exact discrete affine-cell cost

This is a value-preserving local reduction for the **left-clock lattice
objective**, not an appeal to the continuous-cell theorem or an approximate
quadrature estimate. It includes the whole fixed continuation, which is
concave in the captured record extents. It does not preserve those extents.

The physical coordinate box used by a replacement must stay inside one
affine region and inside the arena. In particular, the result cannot be
applied across an unhandled spatial kink or a physical boundary half-cell
whose coordinate box leaves the arena. Its immediate application is to
the unrestricted precenter part of fine pricing on a coarser affine field.

## 1. Scalar statement and node conventions

Let a scalar walk start at zero. Each step is either `+alpha` or `-beta`,
with `alpha,beta>0`. Fix `m` upward and `n` downward steps, and put

\[
 N=m+n,\qquad A=\alpha m,\qquad C=\beta n,
 \qquad f=A-C.
\]

The incoming record interval is `[-a,b]`, with `a,b>=0`. At node `i`,
including `i=0`, update the record interval to `[-B_i,H_i]`. Define

\[
 \mathcal A=\sum_{i=0}^{N-1}(B_i+H_i),\qquad
 J=K-\mathcal A+g(B_N,H_N),                              \tag{1}
\]

where `K` is the same constant for every ordering and `g` is finite,
concave, and nonincreasing in both arguments. The final node is included
in the exit records but is not charged again in the local sum.

**Theorem.** One of the two words `U^m D^n` and `D^n U^m` has cost no
greater than any other ordering with these step counts.

In physical pricing, subtract the CDF at the entry node to obtain this
scalar coordinate. The two records are captured extents below and above
that value; a fixed physical future has exactly the required concavity
and monotonicity, by the sum of its running minimum/maximum formulas.
Endpoint jumps in that future are included in those formulas. The
constant `K` and the common step-duration factor do not affect the
comparison.

## 2. It suffices to remove a three-run block

Consider the word

\[
                   U^p D^n U^{m-p},\qquad 0\le p\le m,
                                                               \tag{2}
\]

and write `X=alpha*p`. Its final extents are

\[
 B(p)=\max(a,C-X),\qquad H(p)=\max(b,X,f).                 \tag{3}
\]

Both are convex functions of the real parameter `p`. Therefore
`g(B(p),H(p))` is concave: monotonicity of `g` first compares its value
at the componentwise smaller convex-function midpoint with its value
at the affine average, and concavity of `g` then compares that average
with the average of the two endpoint values.

We will prove that the discrete area in (1) is convex in `p` up to the
first point where the lower record is old. This makes the complete
cost concave there. The boundary where the lower record becomes old
is dominated directly by `U^m D^n`.

After proving this three-run statement, apply it to any three consecutive
runs of a longer word, taking its entire unchanged future as `g`.
Reflection handles a block `D^p U^n D^{m-p}`. Each replacement reduces
the number of runs, preserves time and final position, and cannot raise
the complete cost. Iteration leaves at most two runs, proving the theorem.

## 3. Exact lower-record area

Put `q=C-a`. If `q<=0`, no word in (2) creates a new lower record, and
`U^m D^n` directly dominates by reaching every upper level as early as
possible. Hence suppose `q>0`.

A new lower level `-z`, with `a<z<C-X`, is first reached by word (2)
at integer node

\[
                    p+\left\lceil\frac{X+z}{\beta}\right\rceil.
\]

Its contribution to the sum of lower extents is the number of remaining
charged nodes. Integrating over the levels gives the exact identity

\[
 \sum_{i=0}^{N-1}B_i=Na+\Phi(X),                          \tag{4}
\]

where, for `0<=X<q`,

\[
 \Phi(X)=\int_{a+X}^{C}
             \left[N-\left\lceil\frac z\beta\right\rceil\right]dz
                  -\frac{X(q-X)}\alpha,                 \tag{5}
\]

and `Phi(X)=0` for `X>=q`. Formula (5) is used on `0<=X<=A`.
The integrand after subtracting `p=X/alpha` is nonnegative there,
since `ceil(z/beta)<=n` and `p<=m`. Level equalities are null sets
in these exact area integrals; the original node comparison includes
the equalities and has exactly the same area.

On the open active interval `(0,q)`, the second derivative of `Phi`
as a measure is at least `2/alpha` times Lebesgue measure. Indeed,
differentiating (5) gives

\[
 \Phi'(X)=-N+\left\lceil\frac{a+X}{\beta}\right\rceil
                         -\frac q\alpha+\frac{2X}\alpha,
                                                               \tag{6}
\]

away from the ceiling jumps, and all jumps in this derivative are
nonnegative. If `q<A`, the extension by zero adds at `q` the
nonnegative derivative jump

\[
                 0-\Phi'(q-)=\frac{A-q}\alpha.            \tag{7}
\]

For every integer `1<=p<m` with `X=alpha*p<q`, these facts imply

\[
 \Phi(X+\alpha)-2\Phi(X)+\Phi(X-\alpha)\ge2\alpha.        \tag{8}
\]

If `q>=X+alpha`, integrate the derivative measure against the triangular
kernel `alpha-|s-X|`; its area is `alpha^2`. If `X<q<X+alpha`, put
`d=q-X`. The density contribution up to `q` is at least

\[
                     \alpha+2d-d^2/\alpha.
\]

Since `X+alpha<=A`, the jump (7) contributes at least

\[
 (\alpha-d)\frac{A-q}\alpha
                   \ge\frac{(\alpha-d)^2}\alpha.
\]

The sum is `2*alpha`. Thus (8) also covers the final grid interval
that crosses the old-record boundary; no fractional run is inserted.

## 4. Exact upper-record area

For a positive level `z` with `0<z<=A`, its charged holding times after
first capture in the two corner words are

\[
 w_U(z)=N-\left\lceil\frac z\alpha\right\rceil,\qquad
 w_D(z)=\max\left(0,m-
                         \left\lceil\frac{C+z}\alpha\right\rceil\right).
\]

Set `d(z)=w_U(z)-w_D(z)>=0`. In (2), levels at most `X` are caught
on the initial upward run at their `U` capture times. Any higher
positive level that is caught is reached on the final upward run,
at exactly its `D` capture time. Therefore

\[
 \sum_{i=0}^{N-1}H_i=\mathcal H_D+\Psi(X),\qquad
 \Psi(X)=\int_0^X 1_{\{z>b\}}d(z)\,dz,                  \tag{9}
\]

where `H_D` is the upper-record area of `D^n U^m`.

Whenever `0<z<z+alpha<=A`, increasing `z` by `alpha` decreases
`w_U` by exactly one and decreases `w_D` by either zero or one.
Consequently

\[
                  d(z+\alpha)-d(z)\in\{-1,0\}.           \tag{10}
\]

Multiplication by the cutoff `1_{z>b}` preserves the lower bound
`-1`: crossing the cutoff only adds a nonnegative value. Integrating
this shift inequality over `[X-alpha,X]` proves

\[
 \Psi(X+\alpha)-2\Psi(X)+\Psi(X-\alpha)\ge-\alpha.        \tag{11}
\]

Combining (4), (8), (9), and (11) yields

\[
             \mathcal A(p+1)-2\mathcal A(p)
                        +\mathcal A(p-1)\ge\alpha>0       \tag{12}
\]

whenever `1<=p<m` and `alpha*p<q`.

## 5. Finish the three-run comparison

Let

\[
                 P=\min\left(m,\left\lceil q/\alpha\right\rceil\right).
\]

Equations (3) and (12) show that the complete sequence `J(p)` is
concave on the integer interval `0<=p<=P`. Its minimum occurs at
`p=0` or `p=P`.

If `P=m`, these are exactly the two corner orders. Otherwise every
`p>=P` has `C-alpha*p<=a`. Its lower record remains old throughout.
The pure `U` corner also has no new lower record, since
`C-alpha*m<=a`, and it reaches every new upper level as early as
possible. It therefore has pointwise at least the captured area of
each such word, no smaller upper exit extent, and the same lower
extent. Its local cost plus `g` is no greater. In particular it
dominates `p=P`, and the three-run comparison follows.

There is also an explicit continuation-independent mixture certificate.
For `0<=p<P`, use the corner `U^m D^n` with probability `p/P` and
the corner `D^n U^m` with probability `1-p/P`. Convexity of the area
sequence and of both extents first shows that the corresponding mixture
of the `p=0` and `p=P` triples dominates the original triple in all
three coordinates. Replacing the `p=P` triple by its dominating pure
`U` triple preserves this comparison. For `p>=P`, use pure `U`.
When `q<=0`, pure `U` also suffices. Jensen's inequality for any
concave nonincreasing `g` then gives the cost comparison directly.
This makes the local reduction independent of which physical future
will eventually be selected.

If one scalar step size is zero, put the strictly capturing direction
first; its scalar record is monotone and all old levels are reached
at their earliest possible nodes. If both step sizes are zero, all
records and costs are constant. These cases require no division.

## 6. Physical and implementation scope

An affine field in light coordinates has the form

\[
                 F(U,W)=F_0+bU-cW,\qquad b,c\ge0.
\]

One fine unit physical step changes exactly one light coordinate by
the fine light spacing. Its scalar increments are the constant values
`alpha` and `-beta` used above. For fixed physical entry and exit
nodes, the two retained paths turn at the corresponding two coordinate
corners. They have the exact original duration and node parity, and
their full left-clock objective is covered by the proof.

Apply the result only when the whole coordinate box is affine and
legal. An affine coordinate rectangle or an affine time-diagonal
triangle has this containment property. A spatially split square
need not have it. A boundary half-cell need not have it. An earlier
actual endpoint contact must be processed by the original endpoint
reset and first-endpoint sweep rules, not by extrapolating an affine
CDF outside its physical cell.

No continuous constant-CDF leg is needed for this discrete local
minimum. The comparison deliberately changes the exit records and
uses concavity of the complete future; it is not the stronger
record-preserving four-leg statement. Similarly, independently
proved phase restrictions should not be combined by assuming an old
guarded continuation remains admissible after records change.
A safe first application is compression before the first center of
affine boxes contained entirely in one **open spatial half-arena**,
with the complete center value as the eventual future cost. Positive
entry and exit positions alone do not imply this box condition. The
unrestricted precenter prefix and the proved optimal center value then
keep their original meaning.

The box also must not silently erase a required historical event. For
example, a replacement across a cell containing the center need not
preserve the old first center visit. Split at that visit or keep the
original treatment of such cells; physical entry and exit coordinates
alone do not encode the center flag. The same care applies to a
separately imposed decision front or endpoint event.

This is an exact local algorithmic permission, not a completed new
pricing implementation or an improved unrestricted game bound.

The standard-library regression
`packages/interval_center_pricing/test_affine_cell.py` compares direct
node sums with (5) and (9), including fractional old-record boundaries.
For complete small word banks it independently finds a rational mixture
of the two corner triples whose area and both exit extents dominate the
original triple. That checks the conclusion simultaneously for every
concave nonincreasing continuation on those fixtures. Additional explicit
nonlinear continuation checks exercise the Jensen step. These finite
regressions test conventions; the universal assertion is proved above.
