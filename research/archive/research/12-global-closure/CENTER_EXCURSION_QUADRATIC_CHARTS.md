# Exact partial outward integrals for center renewal

This note describes a finite exact component for a center-renewal Bellman certificate. No successful security value follows from the component alone.

For the symmetric continuous interior CDF `F`, define

\[
I(t,h,r)=\int_0^h\min\{r,1-F(t+s,s)\}\,ds
       =\int_0^h\min\{r,F(t+s,-s)\}\,ds.
\]

The implemented domain is the full box

\[
0\le t\le2,\qquad0\le h\le1,\qquad0\le r\le\tfrac12.
\]

For returning excursions, the useful peak restriction `h<=2-t` can be intersected later. Keeping the full box also supplies the direct endpoint-tour guard through `I(t,1,r)`, including tours whose endpoint time exceeds 2.

The interior record after the outward leg is

\[
r'=\min\{r,F(t+h,-h)\}.
\]

At `h=1`, this is explicitly an **interior-limit** record. Actual endpoint contact resets the corresponding record to zero. The direct-tour guard uses the integral `I(t,1,r)` and the exact opposite-endpoint tail; it must not use this interior record as an uncaptured endpoint mass after contact. Closed renewal charts at `h=1` describe the limiting interior branch, while physical endpoint paths have their separate guard.

## 1. Finite decreasing-ray partition

Along the negative outward ray,

\[
U=t,\qquad W=t+2s.
\]

For a common-threshold interpolated rational Qout field, split `t` at the fixed-coordinate grid and threshold-clamping knots. On each resulting band, the ordered ray pieces have rational affine endpoints

\[
a_i(t)\le s\le b_i(t)
\]

and affine trace

\[
f_i(t,s)=q_i(t)+C_i s,
\qquad q_i(t)=A_i+B_i t,\quad C_i\le0.
\]

The center value is always `F(t,0)=1/2`. The entire trace is continuous and nonincreasing. The same exact field parser, nodal validation, and narrow/full-width interpolation rules as the endpoint-tail builder are used.

## 2. Ending and crossing pieces

Choose the piece `j` containing the excursion height:

\[
a_j(t)\le h\le b_j(t).
\]

These are affine inequalities in `(t,h,r)`. If `r<=f_j(t,h)`, the record never falls during the outward leg. The exact chart is

\[
I=hr,\qquad r'=r.
\]

Otherwise there is a crossing in a nonflat piece `i<=j`, with

\[
f_i(t,b_i(t))\le r\le f_i(t,a_i(t)),
\qquad r\ge f_j(t,h).
\]

The crossing location is

\[
s_*=(r-q_i(t))/C_i.
\]

If `i=j`, the whole integral is

\[
I=q_i(t)h+\frac{C_i}{2}h^2
       +\frac{(r-q_i(t))^2}{2C_i}.
\]

If `i<j`, take the same expression with `h` replaced by `b_i(t)`, add the exact full integrals of pieces `i+1,...,j-1`, and add

\[
q_j(t)(h-a_j(t))
+\frac{C_j}{2}\bigl(h^2-a_j(t)^2\bigr).
\]

In every crossing case,

\[
r'=q_j(t)+C_jh.
\]

Thus `I` is rational quadratic and `r'` is rational affine on each chart. All defining inequalities are affine. Flat pieces require no division: their equality levels are covered by the no-drop chart or adjacent closed crossing charts.

These charts cover the whole box. For any `(t,h,r)`, choose an ending piece. Either `r` is below its final trace, or continuity and monotonicity give a first crossing between the center value `1/2>=r` and that final trace. If the trace truly drops below `r`, some nonflat piece realizes such a crossing. Ties, zero-height excursions, collapsed pieces at time-band boundaries, and flat intervals are included by the closed inequalities.

## 3. Composition with a center potential

For a positive triangle of height `h<1`, starting from center records `(L,R)`, its cost and new records are

\[
C_+=2hL+I(t,h,R)+hR',\qquad (L,R').
\]

The return time is `t+2h`. If a center potential is P2, then

\[
C_+ + Q(t+2h,L,R')-Q(t,L,R)
\]

is rational quadratic in `(t,h,L,R)` after selecting the initial and final potential cells. Their membership conditions are affine because `R'` is affine on the chart. The reflected excursion is identical with `L,R` exchanged.

For returns after time 2, the exact two-endpoint tour replaces `Q`, with its two branches checked separately. Direct endpoint tours cost `3L+I(t,1,R)` and its reflection. The separate center-renewal theorem must justify those guards and arbitrary countable excursion decompositions; this chart builder supplies their exact finite algebra.

## 4. Operational representation and replay

`build_center_excursion_charts.py` imports the validated field parser from `build_endpoint_tail_charts.py`. Its format is `center-excursion-charts-v1`:

* inequalities `[A,B,C,D]` mean `A*t+B*h+C*r<=D`;
* quadratic coefficients use `[1,t,h,r,t^2,t*h,t*r,h^2,h*r,r^2]`;
* the affine `record_update` uses `[1,t,h,r]`;
* each chart records its ending and crossing pieces and all exact rational vertices.

Every chart is bounded by the explicit box. Its vertices are enumerated by exact intersections of triples of boundary planes, with all inequalities checked. This also includes implicit lower-dimensional charts.

The optional independent replay averages the field directly over the common threshold, independently subdivides the actual outward ray, and integrates its chronological minimum. It checks both the integral and record update at every vertex, every pairwise vertex midpoint, and the vertex centroid. These include an unisolvent P2 set on the affine hull of every nonempty chart. The algebra and coverage argument establish the polynomial branch throughout; the independent values check the implemented coefficients.

The full-width initial prototypes produce 19 charts for `n=1` and 81 for `n=2`. They are exact components, not new game-value certificates.
