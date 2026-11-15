# Four directional legs suffice inside an affine CDF cell

Analytic proof independently reviewed, 2026-11-13. Exact rational
regressions accompany the formulas; no Lean compilation is claimed.

Consider a scalar path \(Y\) with

\[
 -\beta\le Y'(t)\le\alpha,\qquad \alpha,\beta>0,
\]

on a fixed time interval \([0,T]\), with \(Y(0)=0\) and \(Y(T)=f\).
Suppose its entry record interval is \([-a,b]\), where \(a,b\ge0\),
and its prescribed exit record interval is \([-B,H]\), where
\(B\ge a\), \(H\ge b\), and \(-B\le f\le H\).

The running record range is

\[
 \mathcal R_Y(t)=
 \max\bigl(b,\sup_{s\le t}Y(s)\bigr)
 -\min\bigl(-a,\inf_{s\le t}Y(s)\bigr).
\]

**Theorem.** Every admissible \(Y\) is weakly dominated, for the
objective \(\int_0^T\mathcal R_Y(t)\,dt\), by a path with the same
initial and final values, duration, and exit record interval, using
at most four constant-speed directional legs, of speeds \(\alpha\)
or \(-\beta\), followed by one constant-\(Y\) holding leg.

Four legs can be necessary. A three-leg statement, even with an
additional constant-\(Y\) holding leg, is false.

## 1. Reduce the objective to a uniform first-visit cost

Assume first that both exit records are new:
\(B>a\) and \(H>b\). They must then be attained by the path.
For every newly discovered level, let \(\tau_z\) be its first visit.
Fubini's theorem gives

\[
 \int_0^T\mathcal R_Y(t)\,dt
  =T(B+H)
    -\left[\int_b^H\tau_z\,dz+\int_a^B\tau_{-z}\,dz\right].
\]

Thus it suffices to minimize the bracketed uniform first-visit cost,
subject to the terminal time and position.

For a finite piecewise-linear path, remove holds before all new levels
have been visited and move that time to the end. Replace each monotone
movement by its maximal directional speed. All first visits become
earlier and the final position and duration can be preserved by a
final hold.

A reversal at an already visited record level is unnecessary. The
excursion from one frontier to an old opposite frontier and back
discovers no new level on that opposite side. Replacing it by direct
movement toward the next new record advances all affected first visits.

After the first global extreme is reached, move directly to the other
global extreme and then directly to \(f\). There is no remaining new
level on the already completed side that could justify a return.

Consequently it suffices to study finite tours whose turns alternate
between strictly expanding right and left records. Their last two
record turns are the global extremes \(H,-B\) in one order. The
remaining travel to \(f\) is direct, and any unused time is held at
the end.

## 2. Exact first-visit algebra

Write

\[
 \kappa=\frac1\alpha+\frac1\beta.
\]

Consider a tour starting to the right, with successive positive turn
levels \(R_1,R_2,\ldots\) and negative turn depths \(L_1,L_2,\ldots\).
They obey

\[
 b\le R_1\le R_2\le\cdots\le H,\qquad
 a\le L_1\le L_2\le\cdots\le B.
\]

Equalities are permitted when optimizing the closed feasible polytope;
the corresponding nonexpanding turns can be removed afterward.

The first-visit cost is exactly

\[
 C_{\mathrm{direct}}+\kappa E,
 \qquad
 C_{\mathrm{direct}}
 =\frac{H^2-b^2}{2\alpha}+\frac{B^2-a^2}{2\beta},
\]

where

\[
 \boxed{
 E=R_1(B-a)
   +\sum_{\text{left legs }R_i\to-L_i}
          (R_i+L_i)(H-R_i)
   +\sum_{\text{right legs }-L_{i-1}\to R_i,\ i\ge2}
          (L_{i-1}+R_i)(B-L_{i-1}).}
\]

Here is a direct accounting proof. For a newly visited positive
level \(z\), the elapsed time is

\[
 \tau_z=\frac z\alpha+\kappa
       \bigl(\text{total downward variation before its first visit}\bigr).
\]

Each leftward leg of length \(R_i+L_i\) delays all still-unvisited
positive levels, whose total length is \(H-R_i\), by \(\kappa\)
times that leg length. Summing gives the first displayed sum.

Similarly,

\[
 \tau_{-z}=\frac z\beta+\kappa
       \bigl(\text{total upward variation before its first visit}\bigr).
\]

The initial rightward leg of length \(R_1\) delays all \(B-a\)
new negative levels. Each later rightward leg of length
\(L_{i-1}+R_i\) delays the \(B-L_{i-1}\) negative levels still
unvisited. This gives the remaining terms.

The formula holds even with repeated record turns, since the
corresponding newly visited interval has length zero.

## 3. Joint concavity in every partial turn

Fix the order of the two final global record turns. List the earlier
partial-turn magnitudes in chronological order as
\(z_1,\ldots,z_m\). Each \(z_i\) is a right level or a left depth
according to its parity.

Expanding the preceding formula shows that the entire quadratic part
in these variables is

\[
 -\sum_{i=1}^m z_i^2-\sum_{i=1}^{m-1}z_i z_{i+1}.
\]

Everything else is affine in them or constant. Indeed every partial
turn contributes its square through the next opposite-direction leg,
and the only products of two partial turns couple adjacent turns.
The two global turns are fixed and contribute only affine terms.

For \(m\ge1\), the negative quadratic part can be written

\[
 -\frac12\left[
      z_1^2+z_m^2+\sum_{i=1}^{m-1}(z_i+z_{i+1})^2
     \right].
\]

Thus the first-visit cost is jointly concave in all partial-turn
coordinates. Separate one-coordinate concavity alone would not
justify the argument; the displayed joint form does.

A tour starting to the left is obtained by replacing \(Y\) by
\(-Y\) and exchanging the corresponding rates and record bounds.
The same joint concavity holds.

## 4. The time constraint is one linear inequality

Let the last global record be \(H\). The fastest complete tour,
including direct travel to \(f\), has duration

\[
 \kappa\left(H+B+\sum_{i=1}^m z_i\right)-\frac f\beta.
\]

If the last global record is \(-B\), its duration is

\[
 \kappa\left(H+B+\sum_{i=1}^m z_i\right)+\frac f\alpha.
\]

These identities follow by adding upward and downward travel distances.
Every turn magnitude occurs once in the upward total and once in the
downward total; the final displacement supplies the indicated last
term.

Hence, for the chosen final-record order, feasibility is precisely:

- the two bounded monotone-chain constraints for the right and left
  partial extrema;
- one additional inequality \(\sum_i z_i\le S\), where \(S\) is
  determined by \(T\), the fixed global records, the rates, and \(f\).

The unused time is filled by the final constant-\(Y\) hold.
The original tour makes this finite polytope nonempty.

## 5. A vertex has at most one genuinely partial record

A concave function on a nonempty compact polytope has a minimum at
a vertex. Apply this to the exact capture-cost polynomial.

Within either ordered chain, group equal coordinates strictly between
that chain's lower and upper bounds into maximal blocks. Each such
block can be shifted slightly as a unit while preserving all strict
inequalities to neighboring blocks and bounds.

If the total-time inequality is inactive, any interior block gives a
two-sided feasible perturbation, so the point is not a vertex.
If the total-time inequality is active and two interior blocks exist,
shift them by opposite amounts weighted by their block lengths. Their
total sum remains fixed and the perturbation is again two-sided.

Therefore a vertex has at most one interior block in the two chains
together. All other coordinates equal an entry-record bound or a
global exit-record bound.

Remove the nonexpanding turns from the vertex tour. A turn at an
entry-record bound discovers nothing. Repeated visits to the one
interior block discover nothing after its first visit. Repeated
global-record visits also discover nothing. Their removal cannot
increase any first-visit time.

At most one partial record excursion remains, followed by the two
global records in some order. There are therefore at most three
record-turn locations and at most four directional legs after the
final travel to \(f\) is included.

This new tour has no larger first-visit cost and fits within time
\(T\). Add the remaining constant-\(Y\) hold at the end. Its final
records and terminal position agree with the original ones.

## 6. Arbitrary admissible scalar paths

For a general Lipschitz path, choose polygonal interpolants through
the initial and final times, through times attaining both prescribed
global extrema, and through a mesh of times whose spacing tends
to zero. They retain the exact terminal value and exact exit record
interval, satisfy the same derivative bounds, and converge uniformly.

Running maximum and minimum are \(1\)-Lipschitz functionals of a
path in the uniform norm. The integrated record ranges therefore
converge to that of the original path.

Apply the finite-tour result to each interpolant after its speed/hold
normalization. The class of paths with at most four directional legs
and a final hold is a finite union of compact duration-parameter sets.
The endpoint and record constraints are closed, and the integrated
record range is continuous on those sets.

Passing to a subsequence gives a four-leg path that dominates the
original path exactly.

If only one exit record is new, visit that extreme directly, travel
directly to \(f\), and hold the unused time. This takes at most two
directional legs and advances all new-level visits. If no record is
new, one direct directional leg to \(f\) and a hold suffice.

If one scalar speed is zero, the scalar path is monotone and the
corresponding one-direction statement applies. If both are zero,
the scalar value is constant throughout.

## 7. Three legs are insufficient

Use \(\alpha=\beta=1\), entry value \(0\), entry records
\([-19/100,0]\), final value \(1/200\), exit records
\([-1/5,1/100]\), and duration \(T=417/1000\).

The four directional legs are

\[
 \operatorname{up}\frac1{1000},\quad
 \operatorname{down}\frac{201}{1000},\quad
 \operatorname{up}\frac{21}{100},\quad
 \operatorname{down}\frac1{200}.
\]

They have integrated record range

\[
 \frac{20483}{250000}=0.081932.
\]

Any three-directional-leg path preserving both new extreme records
must use its two turns at those extremes. The low-first order takes
\(415/1000\); filling the remaining \(2/1000\) at the full record
range gives only

\[
 \frac{8157}{100000}=0.081570.
\]

The high-first order needs \(425/1000>T\). Hence three directional
legs plus any constant-\(Y\) hold cannot attain the four-leg value.
The strict gap is \(181/500000\).

The example fits an affine legal CDF after a common positive shift
and scaling; it is not caused by an endpoint atom or an illegal scalar
range.

## 8. An explicit envelope of four quadratic candidates

When both exit records are new, the local response can be computed
without retaining a free partial-turn coordinate. Put

\[
 C_0=\frac{H^2-b^2}{2\alpha}+\frac{B^2-a^2}{2\beta},
 \qquad
 T_{LH}=\kappa(B+H)-\frac f\beta,\qquad
 T_{HL}=\kappa(B+H)+\frac f\alpha.
\]

The minimum first-visit cost is the minimum of the following feasible
candidates.

| Tour | Feasibility | First-visit cost |
|---|---|---|
| \(-B,H,f\) | \(T\ge T_{LH}\) | \(C_0+\kappa B(H-b)\) |
| \(H,-B,f\) | \(T\ge T_{HL}\) | \(C_0+\kappa H(B-a)\) |
| \(r,-B,H,f\) | \(r=(T-T_{LH})/\kappa,\ b\le r\le H\) | \(C_0+\kappa[BH+r(H-a)-r^2]\) |
| \(-l,H,-B,f\) | \(l=(T-T_{HL})/\kappa,\ a\le l\le B\) | \(C_0+\kappa[BH+l(B-b)-l^2]\) |

The first two candidates use a final hold for any unused time.
The two partial-excursion candidates use all their available time.
Candidate equalities at an old or final record are harmless and may
be included in the closed branches.

To prove this, a remaining initial partial right excursion can vary
over

\[
 b\le r\le\min\left(H,\frac{T-T_{LH}}\kappa\right).
\]

Its displayed cost is concave in \(r\), so its minimum is at an
endpoint. At \(r=b\), the initial excursion discovers no new level;
the direct low-first tour is better by
\(\kappa b[(B-a)+(H-b)]\). At \(r=H\), its cost is already exactly
the high-first tour's cost, and that shorter tour is feasible.
Only the available-time endpoint strictly between these two records
can supply an additional candidate. The left case is symmetric.

For a prescribed feasible exit record state, the integrated maximum
range is \(T(B+H)\) minus this minimum cost.

If only the upper exit record is new, the direct tour \(H,f\) is
optimal and its first-visit cost is \((H^2-b^2)/(2\alpha)\). If only
the lower exit record is new, use \(-B,f\) and the reflected cost.
If neither is new, the range is constant throughout the cell.

All candidate feasibility conditions are linear in the entry and
exit state and record variables. All displayed costs are rational
quadratics when the fixed rates are rational.

## 9. Interpretation on an affine characteristic cell

Suppose the signed interior CDF is

\[
 F(t,x)=A+bU-cV,\qquad U=t+x,\quad V=t-x,
 \qquad b,c\ge0.
\]

Along a physical Monster path, \(U',V'\ge0\) and \(U'+V'=2\).
Thus \(Y=F(t,m(t))\) has scalar rates
\(\alpha=2b\) and \(\beta=2c\).

When \(b+c>0\), any admissible scalar replacement reconstructs

\[
 U'=\frac{Y'+2c}{b+c},\qquad
 V'=\frac{2b-Y'}{b+c}.
\]

The fixed duration and scalar endpoint imply exactly the original
total \(U\) and \(V\) increments. Both coordinates remain nondecreasing.
If the cell contains the entire coordinatewise box between its
entry and exit points, the reconstructed physical path stays in
the cell.

This box condition holds for rectangles and for characteristic
triangles bounded by two coordinate lines and a line \(U+V=\text{constant}\).
The four directional scalar legs are physical speed-\(1\) legs.
The final constant-\(Y\) leg has the fixed physical velocity

\[
 m'=\frac{c-b}{b+c}.
\]

The theorem preserves both exit records, so the same physical
continuation after the cell has exactly the same record state.
Since capture survival in the continuous interior CDF is one minus
the record range, the replacement does not increase capture payoff.

Physical boundary half-cells require the separate strict-trace
projection argument in BOUNDARY_CELL_RECORD_PROJECTION.md.
