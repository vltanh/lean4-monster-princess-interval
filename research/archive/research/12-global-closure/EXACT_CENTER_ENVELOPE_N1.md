# Operational exact center value for the first light grid

This is an exact center-continuation computation for one fixed Princess
field. It is not a new value bound for the unrestricted game and does not
solve its precenter response problem.

The full-width \(n=1\) normalized field has radial CDF denominator \(8\)
and the following positive-radius nodes before time \(2\). Physical
coordinates are \((t,r)=(j,k)/2\).

| \(j\) | \(k\) | Radial CDF numerator |
|---:|---:|---:|
| 0 | 2 | 8 |
| 1 | 1 | 7 |
| 2 | 2 | 8 |
| 3 | 1 | 0 |
| 4 | 2 | 8 |

The radial value at the center is zero. After time \(2\), use the
outward-characteristic extension. The signed interior CDF is
\(F(t,x)=(1+\operatorname{sgn}(x)g(t,|x|))/2\).
The input is the existing **grid_n1_princess.json** profile, with the
interpolation width explicitly set to \(1/2\).

The exact remaining value from the center, with records
\(L,R\in[0,1/2]\), is represented by **48 rational quadratic candidates
on rational polyhedral eligibility domains**. In particular,

\[
                         Q_F(0,1/2,1/2)=\frac{79}{64}.       \tag{1}
\]

One attaining physical path is

\[
 (0,0)\longrightarrow(1/2,1/2)\longrightarrow(1,0)
 \longrightarrow(2,-1)\longrightarrow(4,1).
\]

The middle two consecutive left-moving pieces can be merged. The
uncorrected direct-tour minimum from the same center state is \(53/32\),
so the renewal step matters.

## 1. Why the finite depth is complete

**FINITE_POSTCENTER_RESPONSE.md** gives \(m=2\) central affine bands
for this field. Every center continuation is dominated by at most

\[
                         K=2m+1=5
\]

returning center triangles followed by one direct two-endpoint tour.
This applies to arbitrary incoming records, not only to one path's
reachable records.

Let

\[
 I(t,h,r)=\int_0^h\min\{r,1-F(t+s,s)\}\,ds,\qquad
 r'=\min\{r,1-F(t+h,h)\}.
\]

The chart builder gives exact quadratic formulas for \(I\), affine
formulas for \(r'\), and rational polyhedral domains. The direct-tour
envelope is

\[
 Q_0(t,L,R)=\min\{3L+I(t,1,R),\,3R+I(t,1,L)\}
\]

for \(t\le2\). For \(2\le t\le3\), every depth uses the exact value

\[
                         G(L,R)=\min(3L+R,L+3R).
\]

A positive renewal appends the cost

\[
 2hL+I(t,h,R)+hR'+Q_{k-1}(t+2h,L,R'),                       \tag{2}
\]

and a negative renewal interchanges \(L,R\).
The implementation uses

\[
                 0\le h\le\min(1,2-t),\qquad 0\le t\le2.
\]

The additional peak constraint is exact: after physical time \(2\),
the affected record is constant on an outward ray. If \(h>2-t\),
shorten to \(2-t\); both returns occur after time \(2\), their
continuation is the same \(G\), and the removed positive-excursion
cost is exactly \(2(h-(2-t))(L+R')\). This can only improve the path
and does not increase its triangle count.

Every proper triangle has \(h<1\). At the closed boundary \(h=1\),
the nominal renewal uses the interior trace and can overestimate
the actual endpoint capture. It cannot underestimate it: the
physical endpoint only resets a record earlier to zero.
The actual direct endpoint tour is included separately. Thus the
closed recurrence supplies no spuriously low branch, while the
finite normal form supplies exact proper branches. Consequently
depth \(5\) equals the unrestricted center-continuation value.
This is the endpoint-closure argument in
**PARAMETRIC_CENTER_VALUE_QUADRATICS.md**.

## 2. Exact scalar elimination

On one integral chart and one successor eligibility domain, (2)
is a rational quadratic in \((t,L,R,h)\), subject to rational
affine inequalities. All composed successor maps are affine.

The separately checked **eliminate_quadratic_interval.py**
enumerates every affine constraint boundary for \(h\), and the
affine stationary value when the constant \(h^2\) coefficient is
positive. Each candidate retains all substituted eligibility
inequalities. Singleton fibers, zero slopes, parameter faces,
and empty constant domains are included.

No winner regions are approximated. Each layer remains a finite
minimum of quadratics on their own eligibility polyhedra, which
may overlap or have lower dimension.

## 3. Pruning is proved, not sampled

The generator uses only integers and Python Fractions for its
mathematical calculations. Floating-point elapsed times are
diagnostic and are excluded from the regeneration comparison.

Every eligibility polyhedron is explicitly inside the compact
box \(0\le t\le3,\ 0\le L,R\le1/2\). The program enumerates all
triples of constraint normals with nonzero determinant and
checks their intersection points against every inequality.
Thus it obtains every vertex, including vertices of
lower-dimensional polyhedra. A nonempty compact polyhedron has
a vertex, so no vertices means the domain is empty.

Rows strict at every vertex may be removed. A compact polyhedron
is the intersection of its supporting active rows; this does
not enlarge its domain.

A candidate \(A\) is discarded in favor of \(B\) only after
proving both:

1. Every vertex of \(D_A\) lies in \(D_B\), hence
   \(D_A\subseteq D_B\).
2. The quadratic \(q_A-q_B\) is nonnegative on \(D_A\).

The fixture proves the second condition by checking every
quadratic polar coefficient

\[
 p(v,w)=2q((v+w)/2)-\frac{q(v)+q(w)}2
\]

for vertices \(v,w\) of \(D_A\), including \(v=w\).
If \(x=\sum_i\lambda_i v_i\), then

\[
                   q(x)=\sum_{i,j}\lambda_i\lambda_jp(v_i,v_j).
\]

Thus nonnegative coefficients prove nonnegativity on the entire
polyhedron. This sufficient test may keep redundant pieces,
but cannot remove a needed one. The optional exact quadratic
minimum fallback is not used in the saved fixture.

The completed layers are:

| Allowed returning triangles | Retained candidates | Nonempty candidates generated | Proved empty candidate domains |
|---:|---:|---:|---:|
| 0 | 12 | 34 | 6 |
| 1 | 32 | 1,542 | 1,326 |
| 2 | 42 | 3,316 | 5,482 |
| 3 | 44 | 3,674 | 8,086 |
| 4 | 46 | 3,714 | 8,748 |
| 5 | 48 | 3,760 | 9,478 |

The retained count is a representation size, not a claim that
all 48 candidates are needed or that their winning regions
are polyhedral.

## 4. Portable artifact and complete regeneration

**center_envelope_n1_exact.json.gz** is a losslessly compressed
certificate. It contains every retained quadratic, its complete
eligibility inequalities and vertices, its affine-height route
witness, all six layer summaries, and a digest of every layer's
full generated-candidate and pruning history.

The digest is only a compact comparison target. The verifier
actually regenerates every candidate and every exact pruning
calculation; it does not infer mathematical validity from a
hash alone.

Place the generator, path replay, scalar eliminator, and the
two chart-builder modules together in the **record_bellman**
package. From that directory, the complete sequence is:

    python build_center_excursion_charts.py \
      ../../interval_clock_grid/grid_n1_princess.json \
      /tmp/center_n1_charts.json --epsilon 1/2 --direct-replay

Byte-compare this regenerated JSON with the decompressed
**center_excursion_n1_fullwidth.json.gz**. This binds the
quadratic chart data to the independently evaluated field.
The saved chart has 19 pieces and passes 261 direct integral
and record-update comparisons.

    python exact_center_renewal_envelope.py \
      center_excursion_n1_fullwidth.json.gz \
      center_envelope_n1_exact.json.gz --depth 5 --verify \
      --history-output /tmp/center_n1_history.json.gz

This replays all six layers, including every feasibility and
domination calculation. A full standard-library run took
approximately 54 seconds in the development workspace.
Run time is not part of the mathematical certificate.

    python replay_center_renewal_paths.py \
      center_envelope_n1_exact.json.gz \
      ../../interval_clock_grid/grid_n1_princess.json \
      /tmp/center_n1_path_replay.json \
      --raw-history /tmp/center_n1_history.json.gz

The last replay reconstructs minimizing physical paths from
the affine-height witnesses. It computes the CDF by direct
threshold averaging and integrates the chronological running
records, splitting every field and record crossing. It does
not use the quadratic integral charts to calculate those
physical costs.

The saved independent replay passes:

* 297 exact reconstructed physical-path checks;
* 3,886 exact affine field-interval checks;
* 120 raw-versus-pruned envelope comparisons across all layers;
* the exact initial-center equality (1).

These sampled path comparisons are a regression of physical
accounting, not a substitute for the finite-depth normal form
or the complete exact enumeration.

## 5. Scope

This fixture establishes an exact, operational continuum
center-value calculation with a finite termination depth.
It avoids a fitted queue or record potential for this
portion of the response.

The precenter portion of a response is still unrestricted.
The fixture is for the specified \(n=1\) field and does not
claim its Princess law is globally optimal, that a fine
field will have only 48 candidates, or that the remaining
unrestricted game-value gap has been closed.
