# Exact quadratic endpoint-tail charts

This is a finite, exact component of the actual-record Bellman certificate. It does not by itself provide a Princess security bound.

Let `F` be the continuous interior CDF of the symmetric ordered Princess law used by the certificate. For the implemented family, `F` is the common-threshold interpolation of a rational nodal Qout profile, with a symmetric threshold interval `[1/2-epsilon,1/2+epsilon]`, where `0<epsilon<=1/2`. The profile is extended exactly outward after time 2. Endpoint atoms are allowed.

After a first positive-endpoint contact at time `t`, let `L` be the remaining lower survival record. Its exact optimal continuation cost is

\[
B(t,L)=\int_0^2\min\{L,F(t+u,1-u)\}\,du.
\]

The direct sweep is optimal because its current CDF value is nonincreasing in `u` and no larger than the corresponding CDF value on any other legal continuation at that same time. It therefore bounds every competing running minimum from below. At the negative endpoint the reflected guard is `B(t,R)`.

The chart domain is **`0<=t<=2`, `0<=L<=1`**. A first positive endpoint can be visited before the center, and an initial endpoint start is possible, so the upper bound `L<=1/2` is insufficient for this guard. At the final opposite-endpoint contact the record is reset to zero; that single terminal time contributes no area to the integral.

## 1. Finite rational sweep geometry

Use light coordinates `U=time+position`, `W=time-position`. On the sweep,

\[
U=t+1,\qquad W=t-1+2u.
\]

For a fixed time band, the first coordinate stays inside one light-grid cell and one of the three threshold-clamping regions. The second coordinate crosses finitely many grid lines, threshold-clamping lines, and the common-threshold main or antidiagonal.

All sweep breakpoints have the form `u=a+b*t` with rational `a,b`. Their ordering can change only when the fixed coordinate crosses a grid or threshold-clamping knot. Splitting there gives finitely many time bands on which the ordered sweep pieces have affine endpoints

\[
a_i(t)\le u\le b_i(t)
\]

and an affine trace

\[
F(t+u,1-u)=q_i(t)+C_i u,
\qquad q_i(t)=A_i+B_i t,\quad C_i\le0.
\]

The last inequality follows from CDF transport, and the builder checks it exactly. At band boundaries pieces may have zero length; the closed formulas remain valid by continuity. Same-orientation and opposite-orientation cells are both included. No no-reentry theorem for physical paths is used.

## 2. A single record crossing

The trace is continuous and nonincreasing along the entire sweep. For a given `L`, there are three possibilities.

* Below the final trace: the record stays at `L`, and `B=2L`.
* Above the initial trace: every trace value is at most `L`, and `B` is the integral of the whole trace.
* A crossing in a nonflat piece: `C_i<0` and

  \[
  q_i(t)+C_i b_i(t)\le L\le q_i(t)+C_i a_i(t).
  \]

Each crossing condition is a pair of rational affine inequalities in `(t,L)`. The crossing point is

\[
u_*=(L-q_i(t))/C_i.
\]

Write `S_{i+1}(t)` for the exact integral of all later pieces. Then

\[
\boxed{
B(t,L)=S_{i+1}(t)+q_i(t)b_i(t)
 +\frac{C_i}{2}b_i(t)^2
 +\frac{(L-q_i(t))^2}{2C_i}.
}
\]

This includes the entire earlier contribution `L*u_*`; it does not omit the part before the selected cell. Each term is rational quadratic in `(t,L)`. The negative coefficient of `L^2` agrees with concavity of `B` in the survival record.

A flat piece needs no division by zero. If its level equals `L`, either neighboring closed crossing chart gives the same result; the below/above charts cover a wholly constant trace. The ordered continuous trace and the two exterior charts therefore cover every record value in `[0,1]` for every time in the band.

## 3. Interface and exact construction

`build_endpoint_tail_charts.py` uses only Python's standard library and `Fraction`. It accepts a complete radial table, an existing Princess extraction artifact, or the compact Qout field encoding. It validates the pre-two nodal table, bounds, cone order, and sticky endpoint trace. The output explicitly uses the exact outward extension after two, regardless of unused later entries in an older input artifact. Its interpolation width is an explicit argument; changing it constructs a different field and inherits no earlier security guarantee.

The output format is `endpoint-tail-charts-v1`. Each chart contains:

* its closed time interval;
* rational inequalities `[A,B,C]` meaning `A*t+B*L<=C`;
* its exact rational polygon vertices;
* polynomial coefficients in the order `[1,t,L,t^2,t*L,L^2]`;
* the crossing-piece index, or an exterior-branch label.

The file also retains the complete affine sweep partition for each band. Polygon clipping and polynomial integration are exact. A potential verifier intersects these chart inequalities with its endpoint state face and checks the resulting quadratic guard over the entire polytope.

## 4. Independent chronological replay

The optional direct replay evaluates the field through a separate common-threshold averaging calculation. At each rational query it partitions the threshold interval, evaluates the corresponding nodal CDF exactly, then integrates the chronological running record along an independently subdivided sweep. It does not evaluate the chart polynomial to obtain its comparison value.

Every chart vertex, edge midpoint, and vertex centroid is checked. For a triangular two-dimensional chart, the vertices and edge midpoints are the six unisolvent P2 nodes. The finite affine decomposition and crossing inequalities above establish the piecewise-quadratic form over the whole region; the independent values check the implemented coefficients. Degenerate line and point charts are retained and checked as well.

For the initial prototypes, full-width `n=1` gives 2 time bands and 10 charts; full-width `n=2` gives 4 bands and 18 charts. The same code handles `n=2`, `epsilon=1/4`, with 12 bands and 44 charts. These are exact tail components for the stated fields, not new global value bounds.
