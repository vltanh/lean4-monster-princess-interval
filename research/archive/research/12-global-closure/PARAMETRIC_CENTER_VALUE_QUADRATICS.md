# An exact finite quadratic envelope for the center value

Fix a rational normalized nodal Princess profile and a rational common
threshold width `epsilon > 0`. Its continuous interior CDF is denoted by
`F`. The paths are symmetric, ordered, stopped at their first endpoint,
and outward after time two. The field, rather than the globally optimal
Princess law, is fixed throughout this note.

The finite response theorem in **FINITE_POSTCENTER_RESPONSE.md** implies
that its exact value after a center visit has a finite description:

\[
 Q_F(t,L,R)=\min_{i:\,(t,L,R)\in D_i}q_i(t,L,R),              \tag{1}
\]

where each `D_i` is a rational polyhedron and each `q_i` is a rational
quadratic. The domains in (1) describe when a candidate is feasible.
The regions where it wins the minimum can have curved quadratic
boundaries; no polyhedral partition into winners is asserted.

The construction is exact and finite. Its size need not be small. It
does not bound the portion of a response before the first center visit,
or give a finite-dimensional class containing a globally optimal field.

## 1. The state and the finite response class

Let

\[
 \Theta=\{(t,L,R):0\le t\le2,\ 0\le L,R\le1/2\}.
\]

The Monster starts at the center at absolute time `t`, with remaining
left and right rank masses `L,R`. Its remaining cost is the integral of
the two surviving records. Away from actual endpoint capture they are
running minima of `F` and `1-F`. At the corresponding endpoint that
record is reset to zero. Define `Q_F` as the infimum of this remaining
cost over all legal continuations, including paths with infinitely many
turns.

Suppose `F` has `m` central affine time bands in the sense of
**FINITE_POSTCENTER_RESPONSE.md**. That theorem gives, from every state
in `Theta`, a response of no greater cost consisting of at most

\[
 K=2m+1\quad\text{returning center triangles}
\]

followed by one direct two-endpoint tour. Every proper triangle has
height less than one. Every return before the final tour is no later
than time three, and both endpoints are completed by time six. Equally,
there is a bound

\[
                       N=2K+2=4m+4                         \tag{2}
\]

on unit-speed physical legs. For full-width interpolation `m=2n`, so
`N=8n+4`; for positive narrower width `m<=6n`, so `N<=24n+4`.

The theorem applies to arbitrary incoming `L,R<=1/2`. It is therefore
available inside a dynamic recurrence, not only for records obtained
from one particular earlier route. Endpoint visits before the center
are already covered by a direct remaining sweep or a zero record.

## 2. Quadratic charts for a finite route word

One construction enumerates unit-speed sign words of length at most
`N`, allowing zero durations. Use their durations and, when convenient,
their cell-crossing times as variables `z`. All times and positions
are affine in `(z,t)`. Impose nonnegative durations, arena containment,
the prescribed physical endpoint events, and completion by time six.
These are rational affine constraints. The duration variables lie in
a fixed compact box.

The field has a finite rational P1 subdivision of the relevant compact
time-position domain. Subdivide a route word by the field cells it
visits and by its record comparisons. Each unit-speed segment is a
straight line and meets each convex field cell in an interval. A
nonparallel cell crossing solves an affine equation with a fixed
rational coefficient, so its time is affine in the word variables.
Parallel and face-contained cases are separate weak-inequality
branches. They require no division by a vanishing coefficient.

On each such segment the CDF is affine in time with a fixed rational
slope. The incoming record on a record-order branch is an affine
function of `(z,t,L,R)`. A record crossing therefore also has an affine
time, unless its slope is zero, in which case the two constant-order
branches suffice. Integrating the affine or constant survival record
between affine times gives a rational quadratic. Summing these terms
and including every specified actual endpoint reset gives a branch
objective of the form

\[
 q(z,\theta)=z^T H z+\ell(\theta)^Tz+q_0(\theta),
 \qquad \theta=(t,L,R),                                    \tag{3}
\]

where `H` is constant rational symmetric, `ell` is rational affine,
and `q0` is rational quadratic. Its feasibility conditions have form

\[
 A z\le b+B\theta,\qquad E z=f+G\theta.                    \tag{4}
\]

There are finitely many words, field-cell sequences, record orders,
and endpoint cases. All their data are rational.

## 3. Closing branches without losing endpoint capture

Actual capture at an endpoint can be strictly earlier than a formula
using the interior endpoint trace would suggest. In particular, the
interior formula for a returning triangle at height `h=1` need not
equal its physical capture cost: the outbound leg has already reached
an endpoint and reset one record to zero.

We use closed polyhedral branches, with the following convention.

* Include branches with the actual first endpoint event and its
  subsequent direct sweep. A required endpoint reset is used only
  where the physical position is that endpoint.
* On a closure where an additional, earlier endpoint event appears,
  a nominal branch may keep using its former interior record until
  its specified reset. This branch then **overestimates** the cost
  of its represented physical route.

Indeed, its nominal record starts correctly and is updated by the same
interior minima. An accidental earlier endpoint contact only lowers
the actual record to zero. Later interior minima cannot reverse the
inequality between the actual and nominal records. Field-cell ties
and ordinary record ties cause no discrepancy, since the interior
field and the minimum operation are continuous.

Consequently every closed feasible branch value is at least the
actual cost of a legal route, and hence at least `Q_F(theta)`. The
finite-response theorem supplies an exact proper branch for every
dominating normal-form route, with its actual endpoint events. Thus
the minimum over the closed branches is no greater than every
epsilon-optimal response cost. Letting epsilon decrease to zero shows
that the closed-branch minimum is exactly `Q_F(theta)`.

This argument does not assume in advance that a best response is
attained. Each branch has a compact fiber, and the exact finite
minimum below subsequently supplies attainment. It also explains why
an interior-trace closure cannot introduce a spuriously low value.

## 4. Parametric active-face elimination in arbitrary finite dimension

Consider any one branch (3)--(4). First row-reduce the constant matrix
`E`. A dependent zero row may leave a nonzero affine expression on the
right. Keep its equation in `theta` as an explicit consistency
condition. The retained equality rows are independent. This step is
essential when an equality is consistent only on a lower-dimensional
parameter set.

For each subset of inequality rows extending those equality normals
to an independent matrix `C`, form the constant KKT matrix

\[
 \begin{pmatrix}2H&C^T\\ C&0\end{pmatrix}.
                                                               \tag{5}
\]

If it is nonsingular, solve

\[
 \begin{pmatrix}2H&C^T\\ C&0\end{pmatrix}
 \binom{z}{\lambda}
 =\binom{-\ell(\theta)}{d+D\theta}.                         \tag{6}
\]

The solution `z_i(theta)` is rational affine. Its eligibility domain
consists of `Theta`, all equality consistency conditions, and every
original constraint after this substitution. It is a rational
polyhedron, possibly empty or lower-dimensional. Substitution in (3)
gives a rational quadratic candidate `q_i(theta)`.

Full-rank point faces are included: if `C` has as many independent
rows as there are variables, (5) is nonsingular regardless of `H`.
Multiplier sign tests are unnecessary. Every retained candidate is
feasible, so retaining a saddle or maximum cannot lower the envelope
below the true minimum of the branch.

### Why singular systems may be skipped

Fix a parameter with a nonempty compact fiber, and choose a global
minimizer `z*`. Let `C` be an independent basis of the equality and
active inequality normals at `z*`. In the relative interior of this
face, stationarity gives a multiplier solving (6).

If (5) is singular, take a nonzero null pair `(v,mu)`. Independence
of the rows of `C` ensures `v!=0`. The null equations give

\[
 Cv=0,\qquad 2Hv+C^T\mu=0,
 \qquad v^THv=0.
\]

Stationarity also gives `gradient(q)(z*) dot v=0`. Thus the objective
is constant on the whole line `z*+s v`. Move along this line inside
the current face until another inequality becomes tight. Such an
endpoint exists by compactness. Its normal is independent of the
current face normals, because a dependent normal would be constant
on the line and could not change from slack to tight.

The new point is still a global minimizer, on a strictly smaller
face. Repeat. In finitely many steps one reaches a nonsingular KKT
face or a point face. Hence one of the enumerated affine candidates
attains every nonempty fiber minimum. No nondegeneracy, positive
definiteness, or full-dimensional parameter-domain assumption is
used.

Taking the finite union over route branches proves (1). The argument
works in every finite dimension. The current implementation
`exact_quadratic_polytope.py` has a dimension-at-most-four interface;
that implementation limit is not a limit on this mathematical
active-face argument, nor an implementation of the entire route
enumeration.

## 5. A bounded-depth construction using only scalar elimination

The center-triangle normal form gives an alternative explicit
construction closer to the implemented scalar eliminator.
Use the exact charts from **CENTER_EXCURSION_QUADRATIC_CHARTS.md**:

\[
 I(t,h,r)=\int_0^h\min\{r,1-F(t+s,s)\}\,ds,
 \qquad r'=\min\{r,1-F(t+h,h)\}.                            \tag{7}
\]

On each chart, `I` is a rational quadratic and `r'` is rational
affine, with rational affine feasibility conditions. The charts
cover `0<=t<=2`, `0<=h<=1`, `0<=r<=1/2`. At `h=1`, (7) is the
interior trace; apply the convention of Section 3 when using it for
a nominal returning triangle.

Define the direct-tour cost

\[
 T(t,L,R)=\min\{3L+I(t,1,R),\ 3R+I(t,1,L)\},\quad t\le2,
                                                               \tag{8}
\]

and, at or after time two, the exact center value

\[
                  G(L,R)=\min\{3L+R,L+3R\}.                 \tag{9}
\]

In (8) the first endpoint is an actual capture event. The opposite
side survives the three-unit tour until its endpoint: the tour next
crosses the center at time `t+2>=2`, when its surviving paths move
outward. Thus (8) is an exact physical cost, including endpoint
starts of the second leg. Formula (9) follows from the same outward
motion and is valid for all later center times.

Set `Q_0=T` for `t<=2`, and `Q_k=G` for `2<=t<=3`, for every `k`.
For `t<=2`, form `Q_{k+1}` as the minimum of `T` and the two
triangle-continuation families. The positive family is

\[
 2hL+I(t,h,R)+hR'
       +Q_k(t+2h,L,R'),
 \qquad 0\le h\le1,\quad t+2h\le3,                         \tag{10}
\]

and the negative family is its reflection, interchanging `L,R`.
The initial upper bound one on `h` makes every scalar fiber compact.
The return-by-three constraint includes every normal-form route.
Zero-height triangles are harmless. At `h=1` a nominal branch can
overestimate its physical cost, exactly as in Section 3; the actual
direct-tour branch is retained separately.

The implementation may additionally impose `h<=2-t`. If the peak is
later than time two, the same-sign record is already constant from
height `2-t` onward. Both the original and shortened returns are at
or after two, and hence have the same continuation value (9).
Shortening by `delta` removes exactly `2*delta*(L+R')` in the
positive case, or its reflection. This is the peak-shortening lemma
in **CENTER_RECORD_RENEWAL_CERTIFICATE.md**. It preserves the number
of triangles and can only improve the cost. Together with `h<=1`
it already implies return by three.

Assume `Q_k` is represented by finitely many quadratic candidates on
polyhedral eligibility domains. Compose each candidate and its
eligibility rows with the affine successor in (10), separately on
each chart (7). The resulting objective is quadratic in
`(t,L,R,h)`, and its constraints are affine. Eliminate `h` by
**EXACT_SCALAR_QUADRATIC_ELIMINATION.md**: test its affine boundary
values and, when its constant `h^2` coefficient is positive, its
affine stationary value. The output is again a finite family of
rational quadratics on rational polyhedra. Empty and singleton
fibers, parameter faces, and zero slopes are included.

Every candidate so constructed is the cost of a nominal finite
physical route and is at least its actual capture cost. Conversely,
the finite response theorem supplies proper exact routes with at
most `K=2m+1` triangles. Consequently

\[
                            Q_K=Q_F.                       \tag{11}
\]

This is a finite algorithm for the complete centered response of
the fixed field. It can be large because each layer retains all
eligible branches. Neither sampling nor an unsupported bound on
the number of record changes is needed.

## 6. Consequences and the remaining obstruction

At rational `(t,L,R)`, all eligible candidate values in (1) are
rational. The minimum is rational and has a rational finite route
witness. For the active-face construction the route variables are
rational affine evaluations. If a winning closed branch ignored an
earlier endpoint, its actual route still has cost at most its branch
value; equality with the infimum forces that actual route to attain
the same value.

A precenter potential can use this value as an exact center guard.
For a quadratic precenter cell potential, its trace

\[
                  P_{\rm pre}(t,t,1/2,R)
\]

must be at most `Q_F(t,1/2,R)`. By (1), this is equivalent to being
at most **every eligible** `q_i(t,1/2,R)`. After intersecting with the
precenter cell and the candidate domain, each check is nonnegativity
of a rational quadratic on a rational polytope in the two variables
`(t,R)`. The existing exact quadratic-polytope checker covers that
dimension, once the complete candidate family has been generated.

The postcenter response is therefore finite and exactly eliminable
for each fixed rational interpolated field. The remaining precenter
response and the choice of a globally optimal Princess field are
separate obligations. This note proves neither a bounded global
equilibrium template nor a matching exact game value.
