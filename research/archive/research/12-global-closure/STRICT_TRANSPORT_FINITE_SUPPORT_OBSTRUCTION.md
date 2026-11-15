# A strict-transport obstruction to a finite-support saddle

Research proposition independently reviewed by the root and audit agents;
the initial-density corollary was also reviewed by the verification agent,
2026-11-14.

This is a necessary equilibrium condition, not a new numerical bound and
not a proof that every optimal Monster law is nonatomic. It distinguishes
a finite response certificate from a finite **saddle** certificate.

## 1. Statement

Let `F` be a legal symmetric ordered Princess interior CDF, locally
Lipschitz in `(t,x)`, with continuous interior traces, sticky endpoints,
and the outward-after-two normalization. Let `ν` be a finite mixture of
Monster paths of positive weights, completed within a common finite
horizon. We may take `ν` to be reflection symmetric.

Let `D` be an open patch contained in `0<t<2`, away from the center and
physical endpoints, on which the transport inequalities have a uniform
strict margin locally:

\[
             F_U>0,\qquad F_W<0,
 \qquad U=t+x,\quad W=t-x.
 \tag{1}
\]

Precisely, every point under consideration has a neighborhood on which
`F_U>=η` and `-F_W>=η` almost everywhere for some `η>0`, and on which
`0<F<1`. A strict affine cell is the principal example. The condition may
also hold across a P1 interface if both adjacent pieces have a common
positive margin.

For a supported Monster path `m_i`, let `L_i(t)` and `H_i(t)` be its actual
running lower and upper capture records, including endpoint resets. Then:

**Proposition.** If `F` is a best Princess response to `ν`, each supported
path captures no positive amount of rank mass while its graph lies in
`D`. In particular,

\[
 L_i'(t)=H_i'(t)=0
 \quad\text{for almost every }t\text{ with }(t,m_i(t))\in D.
 \tag{2}
\]

If either record changes on a set of positive measure in such a patch,
there is a legal symmetric local perturbation of `F` that weakly improves
the payoff against every supported path and strictly improves the payoff
against at least one of them. Hence `F,ν` cannot be a saddle.

## 2. Opposite record events cannot cover a descending record arc

Write

\[
 f_i(t)=F(t,m_i(t)).
\]

Suppose the set

\[
 E=\{t:(t,m_i(t))\in D,\ L_i'(t)<0\}
\]

has positive Lebesgue measure. At almost every such time,
`f_i(t)=L_i(t)` and `f_i'(t)=L_i'(t)<0`.

For another supported path `m_j`, consider its upper-record contact set

\[
 C_j^+=\{(s,m_j(s)):f_j(s)=H_j(s)\}.
\]

Within a compact patch away from physical endpoints, this is closed.
Endpoint discontinuities occur outside the patch. On its time contact
set, absolute continuity gives `f_j'=H_j'>=0` almost everywhere.

If the two physical paths coincide at a set of times, then
`f_i=f_j` there. The derivative of the difference of two absolutely
continuous functions is zero almost everywhere on its zero set.
Consequently `f_i'=f_j'` almost everywhere on that coincidence set.
It follows that

\[
 \bigl|\{t\in E:(t,m_i(t))\in C_j^+\}\bigr|=0.
 \tag{3}
\]

There are only finitely many supported paths. Choose a density point of
`E` outside the union of the sets in (3). Since the finitely many
upper-contact graphs are closed locally, a sufficiently small open ball
around its spacetime point is disjoint from all of them. The ball still
contains a positive-measure subset of the descending-record events of
`m_i`.

This argument does not require the supported Monster paths themselves to
be polygonal. The finite-support assumption, local closedness, and absolute
continuity of the record processes are the relevant facts.

## 3. A legal bump improves the finite mixture

Choose a nonnegative smooth bump `φ`, supported in that ball and positive
on a smaller ball meeting the descending-record set in positive measure.
Raise `F` by `εφ` there, and impose the reflected opposite perturbation
on the reflected patch so that CDF reflection symmetry is retained.

For sufficiently small `ε>0`, the perturbed CDF remains legal. The strict
margin in (1) absorbs the bounded derivatives of the bump; the value
bounds, initial trace, center trace, endpoint traces, and outward extension
are unchanged outside the two patches. The characteristic monotonicity
conditions still give a legal ordered quantile family.

The positive bump is separated from every upper-record contact graph.
On the compact set of supported-path visits to its support, there is
therefore a positive gap between the current field value and the old
upper record. Taking `ε` smaller than this gap ensures that no upper
record of any supported path changes because of the positive bump.
Every lower record can only increase there, which helps the Princess.

By reflection symmetry of `ν`, the negative reflected bump is separated
from every lower-record contact graph. It therefore leaves lower records
unchanged there and can only decrease upper records, again helping the
Princess. Thus every supported path's capture cost weakly increases.

At almost every selected descending-record time `t`, the old minimizing
time for the lower record is unique. Indeed, if an earlier time had already
attained `L_i(t)`, the lower record would have been constant on an interval
ending at `t`, contradicting `L_i'(t)<0` at a differentiability point.
The bump is strictly positive at this unique minimizer. Use the actual
lower-semicontinuous strict-CDF trace on the compact past interval. Here
`L_i'<0` also excludes any earlier visit to `-1`; positive-endpoint strict
traces are continuous under the hypotheses. The perturbed minimum is
therefore attained and is strictly larger at each such time. The reflected
bump cannot create a new lower minimum by the uniform gap just established.
Local absolute continuity and contact-graph closedness near the selected
patch suffice; global endpoint jumps have not been treated as continuous.

The lower-record cost increases on a set of positive time measure. Its
integral strictly increases, so the positive-weight row `m_i` and the
finite mixture improve strictly. This contradicts best response to `ν`.

An increasing upper record is treated by reversing the sign of the bump
and exchanging upper and lower records. This proves (2).

## 4. Pressure and complementary slackness interpretation

For one fixed Monster path, the running-minimum formula can be written
as an infimum of linear clock planes. At a strictly descending active
lower record, the minimizing clock must select the current time, so it
puts positive clock pressure on that spacetime arc. Upper-clock pressure
has the opposite sign. The proof above says that a finite collection of
upper-record contact graphs cannot cancel that absolutely continuous
descending-record pressure in a strict transport patch.

At a true saddle, signed clock pressure must vanish on every patch where
the CDF transport and value constraints permit perturbations of both
signs. The local bump proof establishes the relevant consequence directly;
it does not assume a dual multiplier or measurable clock-selection theorem.

For a finite P1 field paired with a finite Monster law, continuous interior
capture must therefore occur in the closure of cells where at least one
transport inequality is saturated (or at the excluded physical boundaries).
In quantile language, those are the
regions in which Princess motion can have maximal inward or outward speed.
Endpoint atoms are not covered by this obstruction.

## 5. A conditional initial-density balance for a continuous Monster law

There is a complementary statement for a Monster law with initial-position
densities, rather than finite support. Consider a positive initial interval
`J` and a common time `tau>0`. Use the full early strip
`{0<t<tau, x-t in J, x+t in J}`, or its intersections with smaller initial
subintervals. Assume every supported path that can enter this strip retains
its initial unit direction up to `tau`; no already-turned path enters it. Let `p(s)` and `q(s)` be
the total positive-start densities for the initial inward and outward
families, respectively.

If the CDF has a strict transport margin in the strip, an initial inward
path `x=s-t` is setting its lower record there, and an initial outward path
`x=s+t` is setting its upper record. The opposite clock selects its time-zero
record and contributes no pressure in a perturbation supported away from
time zero. The directional first variation, up to the common positive
reflection factor, is therefore

\[
 \int [p(x+t)-q(x-t)]\,\phi(t,x)\,dt\,dx.
 \tag{4}
\]

Both signs of the local perturbation are legal. Best response forces

\[
                       p(x+t)=q(x-t)
 \quad\text{almost everywhere in the open strip}.          \tag{5}
\]

This is stronger than equality at time zero. In the variables
`u=x+t`, `v=x-t`, the strip contains open sets of pairs with `u>v`.
On any small product rectangle in such a set, (5) forces `p` to be
constant on its `u` interval and `q` to equal the same constant on its
`v` interval. Overlapping rectangles show that the two densities are
locally equal constants on every connected initial subband covered by
the hypotheses.

Consequently nonconstant or unequal initial directional densities require
at least one of the assumptions to fail: turns must enter arbitrarily
early, the CDF transport constraint must saturate, or additional contact
families must enter the strip. This does not identify those additional
families and does not by itself establish an active initial-inward sheet
up to its boundary.

## 6. Limits of the conclusion

The proposition does not forbid a finite P1 Princess field from being
globally optimal against an infinite or continuous Monster law. A continuum
of opposite record arcs can supply pressure densities on the same patch.
It also does not forbid a finite-support saddle whose active capture is
confined to transport-saturated regions and physical endpoints.

The test is pair-specific: finding strict-patch capture for a current
finite upper certificate and a current lower field proves that those two
strategies cannot already be an exact saddle. It does not identify the
optimal value or quantify their payoff gap by itself.
