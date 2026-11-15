# First-antipodal clock matching and a finite-support normal form

**Status: a global physical-clock reduction, conditional finite-support
reduction, and a simultaneous Princess speed reduction. No exact game
value or finite optimal support is asserted.**

The pressure matching in
[GLOBAL_CAUSAL_PRESSURE_MATCHING.md](GLOBAL_CAUSAL_PRESSURE_MATCHING.md)
can be moved back along the actual sampled Monster histories. After this
operation, every positive-time matching edge joins exactly antipodal
positions at the same selected time. Only selected time zero needs a
strict radial inequality. This is an exact physical reduction, not a
relaxation of the Monster/history lift.

For a fully matched law on N oriented Monster paths, the same construction
gives atomic clocks and a symmetric polygonal law with at most N+2 knots
per path. The bound depends only on support cardinality, even when the
original paths have infinitely many turns. Existence of a finite optimal
fully matched support remains unproved.

The final section gives a separate, stronger pathwise fact: every
continuous Princess trajectory, regardless of its speed, is dominated
against all unit-speed-bounded Monsters simultaneously by one legal
1-Lipschitz Princess trajectory.

## 1. Physical resources and lifted matching

Let nu be a symmetric probability law on complete legal Monster paths.
Write tau_-(m) for the first visit to -1 and assume

\[
 M=\int\tau_-(m)\,\nu(dm)<\infty.
\]

A scoring resource is (m,a), where 0 <= a < tau_-(m), with measure

\[
 \lambda(dm,da)=\nu(dm)\,da.
\]

Temporarily allow a causal selected-time kernel K(m,a,dt), supported on
0 <= t <= a. Its extended resource measure is

\[
 \Lambda(dm,da,dt)=\lambda(dm,da)K(m,a,dt).
\]

The selected pressure event is (t,m(t)). Split Lambda into the disjoint
positive, negative and zero resource classes P, N and Z according to the
sign of m(t). This is a split of resource slots, not merely of paths.

Lift a partial pressure matching to a measure Pi on P times N by
disintegrating the positive and negative resource measures over their
pressure events. Its marginals satisfy

\[
 \Pi_1\le\Lambda|_P,\qquad \Pi_2\le\Lambda|_N.
\]

For a matched pair

\[
 e=(m,a,t),\qquad f=(n,b,s),
\]

put u=m(t)>0 and v=-n(s)>0. The original causal-cone relation is

\[
 v\ge u+|t-s|.                                      \tag{1}
\]

These disintegrations exist on the standard Borel path/resource spaces.
They allow a resource fraction to split among several partners. No
purification or single-partner assertion is needed.

## 2. Retiming to the first antipodal event

Set q=min(t,s). The Monster speed bounds imply

\[
 m(q)+n(q)\le0.                                      \tag{2}
\]

Indeed, if t <= s, then
n(t) <= n(s)+(s-t) <= -u. If s < t, then
m(s) <= m(t)+(t-s) <= v. Define

\[
 h(m,n)=\inf\{r\ge0:m(r)+n(r)\le0\}.                 \tag{3}
\]

Equation (2) ensures h <= q on every matched resource pair. Crucially,
h depends only on the two entire physical paths; it does not depend on
the scoring or selected times of the particular resource slots.

Retiming both slots to h is causal because
h <= t <= a and h <= s <= b. If h>0, continuity gives

\[
 m(h)+n(h)=0.                                        \tag{4}
\]

Thus the two new events are either strictly antipodal or both at zero.
The positive member may be the old negative resource: orientation is
assigned again after retiming. If h=0, their sum is nonpositive. They
are then both nonpositive, or the negative radius is at least the
positive radius. Pair the new positive event with its negative partner
whenever one exists. Otherwise discard the matching edge, while keeping
both clock-resource units.

The hitting map (3) is Borel. For example, on a compact time interval,
the condition h <= c is equivalent to
min_{0<=r<=c}(m(r)+n(r)) <= 0; the minimum is continuous in the two
paths for uniform convergence on that interval. Applying this to all
rational c gives the required measurability. The selected times are
bounded above by the original finite resource times.

Replace the two Pi marginals in Lambda by these retimed marginals,
leaving the unmatched resource fractions untouched. The projection onto
(m,a) is unchanged. Original positive and negative resource slots were
disjoint, so an orientation reversal creates no conflict or double use.
Every new positive unit arising from a retimed pair is covered by its
own partner. The only possibly unmatched positive units are the old
unmatched positive resources. In fact, the unmatched positive mass of
the constructed matching equals that of the supplied matching Pi.
Taking Pi to be an old maximizing matching, whose attainment is part of
the imported pressure-matching theorem, gives the optimized deficiency
comparison

\[
 M_{\rm new}=M,\qquad D_{\rm new}\le D_{\rm old}.       \tag{5}
\]

An additional matching could improve the new certificate further. In
particular, full matching is preserved, and an arbitrary supplied partial
matching retains its own unmatched-mass bound without an optimality
assumption.

No selected -1 event is introduced. Each selected time is no later than
its resource's scoring time, which is strictly before that same path's
first -1 visit. This also handles paths starting at -1: their active
resource measure is zero.

Finally restore deterministic nondecreasing clocks if desired. For each
path, the new selected-time marginal eta_m has mass tau_-(m), and

\[
 \eta_m([0,c])\ge\min(c,\tau_-(m)),                   \tag{6}
\]

because every scoring resource a <= c selected a time no later than a.
The existing generalized-quantile clock construction therefore realizes
eta_m by a nondecreasing causal clock. This changes neither the pressure
occupation nor its matching. Compression is done after the resource
retiming, not during it.

**Theorem 1.** Every physical clock certificate admits, on the same
physical Monster law and with no larger deficiency, a matching whose
positive-time edges have equal selected time and equal radius. Its
time-zero edges satisfy ordinary radial dominance. The selected positive-
time edge is a first antipodal event of its original two path histories.

In particular, the attained fully matched optimum supplied by
[GLOBAL_ZERO_DEFICIENCY_ATTAINMENT.md](GLOBAL_ZERO_DEFICIENCY_ATTAINMENT.md)
can be chosen in this form. Its existing physical horizon and center
deadline remain unchanged because this theorem changes only clocks.

## 3. What matching constraints remain

Let mu_+ and mu_- denote positive and negative pressure on selected
time/radius space. Full matching by equal-time/equal-radius edges at
positive times and radial-dominance edges at time zero is equivalent to

\[
 \mu_+|_{\{t>0\}}\le\mu_-|_{\{t>0\}}                \tag{7}
\]

as measures on the SAME time/radius space, together with

\[
 \mu_+(\{0\}\times(c,1])
 \le \mu_-(\{0\}\times(c,1])
 \quad(0\le c<1).                                   \tag{8}
\]

All c may be replaced by rational c and monotone limits. Equation (7)
uses identity matching. Equation (8), including total mass at c=0,
is exactly the one-dimensional partial stochastic-dominance condition;
a monotone quantile coupling gives its radial matching. Closed-tail
inequalities follow by limits, so atoms and equal-radius edges are
included. These measure inequalities characterize the retained matching
geometry; the first-hit status additionally comes from its physical
resource construction in Section 2.

For comparison, equal selected times WITHOUT the first-antipodal
tightening would require

\[
 \mu_+(A\times(c,1])\le\mu_-(A\times(c,1])             \tag{9}
\]

for every Borel time set A and rational c. Disintegrating both measures
over a common time marginal turns (9) into conditional radial dominance
at almost every time. Equations (7)-(8) are the stronger normal form
obtained above.

For a fully matched certificate and any measurable radius function r
with values in [0,1], the resulting clock plane is at most M. A pair at
(t,+u),(t,-u) contributes at most two
resource units, and an unused nonpositive event contributes at most one.
At time zero, (8) supplies the same inequality. Strict equality contacts
only reduce the plane. This observation does not authorize jumps by the
physical Princess; Section 5 treats continuous paths directly.

The joint physical clock lift is still essential. The fake occupations
in [EULERIAN_RELAXATION_GAP.md](EULERIAN_RELAXATION_GAP.md) already satisfy
diagonal matching. Thus (7)-(8), even together with bare Eulerian
conservation laws, do not supply missing physical histories.

## 4. Finite fully matched support implies a finite polygonal template

Assume nu has N distinct oriented paths of positive weight, includes
their reflections, and all have finite first endpoint times. Start with
a full matching and apply Theorem 1.

Unmatched nonpositive resources can also be retimed. If their path starts
nonpositive, select time zero. Otherwise select its first center visit;
this visit precedes every old nonpositive selection. Their selected event
remains nonpositive. These fractions support no matching edges, so the
operation loses no used capacity.

Consequently every clock is atomic on time zero, its path's first center,
and the pair events h(m_i,m_j). For h>0, this is the first meeting of
m_i with the reflected path -m_j, which is another path in the oriented
bank. There is at most one first meeting with each other oriented path.
The first center is the first meeting with the path's own reflection.

For path i, take time zero, all such first-meeting times before its second
endpoint, and both its first endpoint times. There are at most

\[
                         N+2                       \tag{10}
\]

distinct knot times. This knot set is already reflection-invariant:
reflection permutes the oriented bank, preserves every first-meeting
time, and swaps the two endpoint labels.

Linearly interpolate m_i between its retained knots and hold it after
its second endpoint. Each new segment has speed at most one. Every
selected pressure event is unchanged, as are both first endpoint times.
For example, all vertices preceding the old first +1 visit lie strictly
below +1, so their affine interpolants cannot reach +1 earlier. The same
argument preserves the first center: before it all vertices have the
strict initial sign. Reflection symmetry and all old horizon/deadline
requirements are preserved.

Keep the atomic selected-time measures on the new paths. Their masses,
prefix inequalities (6), pressure events, full matching and endpoint
baseline are identical. A new polygonal interpolation may create an
earlier meeting of two paths with different knot sets. No assertion is
made that the retained contact times remain FIRST meetings afterward;
their preserved contact values are sufficient for the certificate.

**Theorem 2.** Every fully matched symmetric physical law supported on N
oriented paths has a fully matched symmetric polygonal replacement,
with the same baseline, at most N+2 knots per oriented path, atomic
causal clocks, and the same first center and endpoint times.

There is also an explicit finite algebraic feasibility problem for each
fixed N. Use path weights, the bounded lists of knot times and positions,
weighted clock-atom masses, and matching masses aggregated by unordered
path pair. Each original pair uses only its one retained event, so
O(N^2) event/matching variables suffice. Remaining nonpositive clock mass
on a path uses its one safe initial/center event. For fixed combinatorial
orders and sign cases, physical legality, reflections, endpoint labels,
equal-time antipodality and initial radial dominance are polynomial
equalities and inequalities. Atomic clock causality is checked at the
left limits of the ordered atom times; in weighted units, the cumulative
previous mass is at least the path weight times the next atom time.
Total clock mass is the path weight times its first -1 time.

Taking the finite disjunction over these combinatorial cases gives a
semialgebraic template with rational constants at any fixed rational
horizon; the known globally attained zero-deficiency class permits the
fixed horizon eight. Its feasibility for baseline at most a given rational number
is decidable by real quantifier elimination. This is a completeness
statement for the fixed-N FULLY MATCHED class, not merely for a selected
polygonal ansatz.

The missing global gate is now precise: no finite N is known to contain
a fully matched global optimum. An arbitrary finite optimal Monster law
would not by itself close this gate, since the known conversion of a
positive-sweep-mass law to deficiency zero can introduce a continuum of
boundary-turn paths. None of these statements rules out a finite formula
with continuous support.

There is a useful explicit obstruction within the finite-start class.
Let q>0 be the total endpoint-start probability, and suppose every
interior start is at distance at least delta>0 from both endpoints,
with delta<=1. Every +1-start scoring resource a<delta/2 selects a time
t<=a and a position u>=1-t>0. An interior-start negative query at time s
has radius v<=1-delta+s. The cone matching condition would force

\[
 1-\delta+s\ge1-t+|s-t|,
 \quad\hbox{hence}\quad \delta\le2\min(s,t)<\delta,
\]

a contradiction. A +1-start negative query has v<=s-1 instead, forcing
min(s,t)>=1, again impossible. A -1-start path has no active resources.
Thus all these positive scoring resources are unmatchable, and symmetry
gives

\[
                         D\ge q\delta/4>0.          \tag{10a}
\]

In particular, a finite-initial-support fully matched law cannot carry
endpoint-start mass. If there are no interior starts, one may take
delta=1. This rules out a finite D=0 support with a sweep atom; it does
not exclude a finite D=0 support whose starts are all interior.

## 5. Princess speed is irrelevant: simultaneous pathwise tracking

This is independent of clock matching and does not assume an optimal law.
Let p:[0,infinity) -> [-1,1] be ANY continuous Princess path. There is a
canonical 1-Lipschitz tracker q, with q(0)=p(0), characterized by

\[
 q'(t)=\operatorname{sign}(p(t)-q(t))
 \quad\hbox{whenever }p(t)\ne q(t),\qquad |q'|\le1.   \tag{11}
\]

For existence, solve

\[
 q_\varepsilon'
 =\operatorname{clamp}((p-q_\varepsilon)/\varepsilon,-1,1),
 \qquad q_\varepsilon(0)=p(0).
\]

The interval [-1,1] is invariant. Arzela--Ascoli on bounded intervals
gives a locally uniform limit. On every compact subinterval where
p-q is strictly positive or strictly negative, the approximating
derivatives are eventually exactly +1 or -1; hence the limit satisfies
(11). The scalar monotonicity comparison proves uniqueness: on a region
where two outputs for the same input are strictly ordered, their
difference cannot increase in the ordered direction. The same comparison
for two inputs proves

\[
 \sup_{0\le t\le H}|q_1(t)-q_2(t)|
 \le\sup_{0\le t\le H}|p_1(t)-p_2(t)|.               \tag{12}
\]

One can first prove (12) for the regularized tracking equations and then pass
to their unique limits. Thus the tracker is Borel, continuous on compact
time intervals, causal, and commutes with reflection.

Let m be any legal Monster. Before its first contact with p, continuity
forces m-p to keep one strict sign. Suppose, for example, m<p there.
Initially q-m>0 unless capture already occurs at zero. If the first
contact of m with q happened at a time tau strictly before contact with
p, then q(tau)=m(tau)<p(tau). On a neighborhood of tau, (11) gives q'=1.
Since m'<=1 almost everywhere, q-m is nondecreasing on that neighborhood,
contradicting its first arrival at zero from a positive value. The case
m>p follows by reflection. Therefore

\[
                  T(m,q)\ge T(m,p)
 \quad\hbox{for EVERY legal Monster }m.              \tag{13}
\]

The Borel tracker can be applied to a Princess law path by path. It weakly
improves every Monster payoff simultaneously and produces a legal
unit-speed-bounded law. Consequently the unrestricted game value, and
every fixed-law Monster upper oracle, are unchanged if the Princess is
initially allowed arbitrary continuous motion. Discontinuous jumps are
not covered: the strict-side argument uses continuity essentially.

This removes the Princess speed condition as a source of additional
optimal strategies. It does not prove a finite phase count, finite
initial support, or a finite optimal Monster law.

## 6. Focused exact structural replay

The standard-library Fraction script
[verify_synchronized_pressure.py](../../packages/interval_global_closure/verify_synchronized_pressure.py)
checks six matched-resource configurations, including positive-time and
time-zero orientation reversals, collapse to two negative events, and
collapse to the center. It checks causality, active-endpoint exclusion,
the retained radial capacity and an unchanged unmatched source fraction.

Its complete two-path D=0 fixture reduces six original knots to the
N+2=4 retained knots per path while preserving all first center/endpoint
times, atomic clocks, pressure and baseline 11/4. Four exact piecewise
affine Princess inputs, including speeds greater than one, provide 40
chronological capture comparisons against legal Monsters and six
input/output contraction checks for the tracker. The legal input is
fixed by tracking.

These finite checks audit the transformations and strict-contact
accounting. The continuum resource disintegration, global attainment
input and simultaneous pathwise comparison are the analytical proofs
above, not conclusions inferred from the fixture counts. No new game
bound is claimed.
