# A finite exact attack set for any finite bang-bang Princess law

**Status: complete all-\(\mathcal B_1\) response theorem for a supplied
finite Princess law.** This does not claim that finite Princess support
attains \(W_1\), or that a particular supplied law separates \(W_1\)
from the unrestricted upper. It gives a finite, exact way to decide
the continuous one-turn security of such a law.

The inputs are actual legal trajectories with rational vertices.
Formal traces, infinitesimal contact labels, and limiting response
profiles are not interchangeable with these inputs.

## 1. Hypotheses and parameter domain

Let \(p_1,\ldots,p_N\) be continuous Princess trajectories in
\([-1,1]\), with finitely many rational vertices on \([0,6]\).
Every nonconstant segment has slope \(+1\) or \(-1\); stationary
segments are permitted at the endpoints. Each path is extended
legally beyond six, which cannot affect capture against the Monster
class considered below. No ordering between the Princess paths is
assumed. Let \(w_i\ge0\) be rational weights summing to one.

For the arrangement, include every Princess vertex \((t,x)\)
and its reflection \((t,-x)\), even if the law itself is not
reflection symmetric. For each of these vertices put
\[
 U=t+x,\qquad W=t-x.
\tag{1}
\]
Define the finite level sets
\[
 A=\{-1,1\}\cup\{-W:\text{Princess vertices}\},
\]
\[
 B=\{-1,3\}\cup
   \{U,\ W-2:\text{Princess vertices}\}.
\tag{2}
\]
Discard levels outside the possible parameter ranges
\(a\in[-1,1]\), \(b\in[-1,3]\).

The complete oriented one-turn domain is
\[
 D'=\{(a,b):-1\le a\le1,\quad a\le b\le2-a\}.
\tag{3}
\]
Its Monster vertices are
\[
 (0,a),\quad
 ((b-a)/2,(a+b)/2),\quad
 (b+1,-1),\quad(b+3,1).
\tag{4}
\]
As proved in
[ONE_TURN_COMPLETE_DOMAIN.md](ONE_TURN_COMPLETE_DOMAIN.md), adding
the harmless \(a=-1\) face does not change the minimum over genuine
\(\mathcal B_1\) paths: its extra routes are pathwise dominated by
the immediate endpoint sweep. Both orientations are included.

Draw every vertical line \(a=\alpha\), \(\alpha\in A\), and every
horizontal line \(b=\beta\), \(\beta\in B\), clipped to (3). Include
the domain edges \(a=-1\), \(b=a\), and \(a+b=2\).
Let \(\mathcal V\) be all vertices of this finite arrangement,
including intersections with the domain edges.

**Finite attack theorem.**
\[
 \boxed{
 \inf_{m\in\mathcal B_1}
       \sum_iw_iT(m,p_i)
 =
 \min_{\substack{(a,b)\in\mathcal V\\s\in\{-1,1\}}}
       \sum_iw_iT(s\,m_{a,b},p_i).}
\tag{5}
\]
All terms on the right are actual chronological first captures,
including time-zero contact, endpoint contact, and tangencies.
For a reflection-symmetric Princess law one orientation suffices.

Thus a finite rational matrix, independent of the chosen weights,
prices the whole continuous canonical one-turn class. If every
matrix column has weighted payoff at least \(c\), the supplied
actual Princess mixture secures \(c\) against all of
\(\mathcal B_1\).

## 2. Why the rectangle arrangement is complete

In light coordinates the three Monster legs are
\[
 W=-a,\quad U:a\longrightarrow b;
\]
\[
 U=b,\quad W:-a\longrightarrow b+2;
\]
\[
 W=b+2,\quad U:b\longrightarrow b+4.
\tag{6}
\]
Every nonstationary Princess leg is horizontal or vertical.
The incidence pattern can change only when a vertex meets a
segment, when an intersection reaches a Monster turn or endpoint,
or when parallel legs become coincident.

A Princess vertex lies on the supporting line of a Monster leg
precisely at
\[
 a=-W,\qquad b=U,\qquad\text{or}\qquad b=W-2,
\tag{7}
\]
respectively. These are exactly the levels in (2).

The Monster turning point has coordinates \((U,W)=(b,-a)\).
Lying on a vertical Princess segment fixes \(b=U\); lying on a
horizontal Princess segment fixes \(a=-W\). Its contact with a
stationary endpoint segment requires \(a+b=2\) or \(a+b=-2\).
The first is already a domain edge; the second is only the
domain corner \((-1,-1)\).

A Monster initial point can coincide with a Princess only at
time zero, where \(a=p_i(0)=-W_i(0)\). A first negative endpoint
contact with a Princess endpoint arrival occurs at
\(b=t-1=U\). A final positive endpoint contact occurs at
\(b=t-3=W-2\). Stationary endpoint intervals introduce only the
same beginning/end thresholds and the existing domain edges.

The apparent additional third-leg endpoint line \(b=U_i-4\)
is redundant. An intersection at the Monster's final \(+1\)
endpoint can occur on a Princess vertical unit leg only at that
leg's \(+1\) endpoint vertex. There \(U_i-W_i=2\), so
\(U_i-4=W_i-2\), which is already included.

These observations also cover coincident parallel legs.
For example, a coincident second leg has \(b=U\); its first
contact is the later of its own start \((b-a)/2\) and a Princess
segment start \(t_i\). The change between these two affine
expressions occurs at \(a=b-2t_i=-W_i\), already in the
arrangement. The other coincident-leg cases are analogous.

It follows that, on every relatively open arrangement cell,
including its lower-dimensional strata, the first intersecting
Princess segment and Monster leg have fixed incidence type.
The first intersection time is affine in \((a,b)\). For
nonparallel unit legs the possible formulas have the forms
\[
 \frac{U_i-a}{2},\qquad
 \frac{b+W_i}{2},\qquad
 \frac{U_i+b+2}{2}.
\tag{8}
\]
Endpoint contacts and coincident-leg starts are affine as well.
Chronology decides which segment is first: different Princess
segments already have ordered time intervals, as do the Monster
legs. No unlisted crossing of two candidate time formulas can
change their chronological order while both remain valid.

Consequently
\[
 C_s(a,b)=\sum_iw_iT(s\,m_{a,b},p_i)
\tag{9}
\]
is affine on each relatively open arrangement cell. The reflected
Monster may equivalently be priced against the reflected Princess
paths. To use one shared arrangement for both orientations,
include the vertices of both \(p_i\) and \(-p_i\) in (2), unless
the original Princess support is already reflection closed.

## 3. Why actual vertices suffice despite discontinuities

First coincidence is lower semicontinuous in the Monster
parameters. Indeed the physical paths (4), completed constantly
after their final endpoint, depend continuously on \((a,b)\) in
uniform norm on \([0,6]\). If a sequence of capture times has a
finite limit, the corresponding limiting equality of positions
is still a coincidence. Therefore
\[
 T(m_{a,b},p)\le
 \liminf_n T(m_{a_n,b_n},p).
\tag{10}
\]
Every path (4) captures every Princess by six, and finite
nonnegative weighted sums preserve this lower semicontinuity.

Take any parameter point in a relatively open cell. The affine
extension of (9) to that cell's compact polygonal closure has a
minimum at one of its vertices \(v\). By (10), the **actual**
capture payoff at \(v\) is no larger than the affine limiting
value there. It is therefore no larger than the payoff at the
original point. The same argument applies to line cells and
point cells.

Every parameter point is thus dominated by an actual arrangement
vertex. Together with the complete-domain theorem, this proves
(5). No one-sided limit is substituted for an actual contact.
Contact jumps work in the direction required by the proof:
a boundary coincidence can lower the Monster's payoff, so it
must be checked rather than discarded.

## 4. The third-leg levels cannot be omitted

Consider the positive Princess path with vertices
\[
 (0,1/2),\ (1/2,0),\ (1,1/2),\
 (3/2,0),\ (2,1/2),\ (5/2,1),
\tag{11}
\]
then stopped at one. Fix the Monster start \(a=-3/4\).
For \(b\) on either side of \(-1/2\), sufficiently close to it,
direct first capture gives
\[
 T(m_{a,b},p)=
 \begin{cases}
 7/4+b/2,&b\le-1/2,\\
 b+3,&b>-1/2.
 \end{cases}
\tag{12}
\]
At \(b=-1/2\) the two paths meet at the center at time \(3/2\).
On the strict upper side the Princess escapes along an equal-speed
outward leg and is caught only at the positive endpoint.

The jump occurs at \(b=-1/2=W_{\rm vertex}-2\).
Every \(U\)-coordinate of a vertex in (11) is positive, so an
arrangement containing only \(a=-W\) and \(b=U\) misses this
essential contact change. Formula (2) retains it.

## 5. Exact arithmetic and scope extensions

Suppose all Princess vertex times and positions have denominator
dividing \(D_0\). All arrangement coordinates in (2)–(3) then have
denominator dividing \(D_0\), and Monster vertices have denominator
dividing \(2D_0\). Intersections of slopes \(-1,0,1\) have times
with denominator dividing \(4D_0\).

Thus scale all positions and vertex times by \(2D_0\). Every
slope is an integer in \(\{-1,0,1\}\); computing **twice** the
first-intersection time uses only integers. If the Princess
weights have common denominator \(W_0\), every matrix payoff has
common denominator \(4D_0W_0\). This avoids floating comparisons
and need not use a rational-arithmetic object inside each
physical intersection.

### Complete extension to arbitrary rational piecewise-affine paths

Allow each fixed Princess segment to have any rational slope
\(|v|\le1\), including stationary interior segments. Start with
the vertex-incidence lines (2) and the domain edges. For every
segment \(p(t)=vt+c\), and for its reflection, add the line
\[
 (1+v)a+(1-v)b=2c.
\tag{13}
\]
A stationary interior segment introduces \(a+b=2c\).
Let \(\mathcal V_{\mathrm{PL}}\) be all vertices of this augmented
finite rational line arrangement clipped to (3).

**General finite attack theorem.** Formula (5) remains valid with
\(\mathcal V_{\mathrm{PL}}\) in place of \(\mathcal V\).
Indeed (13) is exactly the condition that the Monster turning
point lies on the indicated Princess segment. Every other
vertex/segment incidence is one of (7), an initial contact, or
an endpoint contact already listed in Section 2. Nonparallel
intersection times solve a linear equation with fixed nonzero
denominator \(1-v\) or \(1+v\), so are affine on each incidence
stratum. Parallel unit-speed cases have already been handled.
The compactness/lower-semicontinuity proof in Section 3 applies
unchanged. This proves the augmented arrangement is exhaustive,
including arbitrary rational subunit speeds and interior waits.

The default checker uses the faster rectangle construction and
rejects interior waits and subunit legs. Its explicit general
mode uses all lines (13), not the rectangle approximation.

### A simpler exact first-capture oracle

For any legal Princess path define the two first-level inverses
\[
 L(c)=\inf\{t:p(t)-t\le c\},\qquad
 R(c)=\inf\{t:p(t)+t\ge c\}.
\tag{13a}
\]
Both underlying light coordinates are monotone. Earliest contact
on a constant-level plateau is included. Put \(h=(b-a)/2\).
The exact capture time against (4) is
\[
 \boxed{
 T(m_{a,b},p)=
 \begin{cases}
 0,&p(0)=a,\\
 R(b),&p(0)<a,\\
 L(a),&p(0)>a\ \text{and }L(a)\le h,\\
 L(-b-2),&p(0)>a\ \text{and }L(a)>h.
 \end{cases}}
\tag{13b}
\]
If the Princess starts below the Monster, she cannot meet its
first rightward leg; at the turn her \(U\)-coordinate is still
strictly below \(b\), and the second-leg meeting is precisely
the first \(U=b\) contact. It occurs by the negative endpoint.
If she starts above, the first-leg meeting is the first
\(W=-a\) contact. When that has not occurred by the turn,
monotonicity prevents a second-leg meeting. The final rightward
leg meets her at the first \(W=b+2\) contact. The arena bounds
place this contact between the negative and positive endpoints.
This proves every branch of (13b), including its equality cases.

For rational polygonal paths, the first-level inverse is affine
between vertex levels and may jump at a constant-coordinate
plateau. Binary search with the earliest-level convention computes
it exactly. The implementation checks this inverse oracle against
an independent chronological segment-intersection routine on
every arrangement vertex of a rational-subunit fixture.

A formal infinitesimal path is not an input to this theorem.
First choose a positive rational perturbation and construct its
actual vertices. Uniform approximation of its contact payoffs
over Monster starts is not automatic: the Monster may start at
one of the new exact Princess positions. The exact finite attack
set checks those time-zero equalities too.

## 6. A strict finite-law certificate yields continuous Princess laws

Suppose an actual finite law \(\mu\) has certified security
\(c>U_*\) against \(\mathcal B_1\). Draw one independent
\(Z\sim\operatorname{Uniform}[-1,1]\) for the entire path and set
\[
 p_\varepsilon(t)=(1-\varepsilon)p(t)+\varepsilon Z,
 \qquad 0<\varepsilon<1.
\tag{14}
\]
These paths remain in the arena, have speed at most
\(1-\varepsilon\), and differ uniformly from their original
paths by at most \(2\varepsilon\). Every one-time marginal has
a density bounded by \(1/(2\varepsilon)\). A reflection-symmetric
input law stays symmetric, and common-quantile reordering of
these marginals can only improve security.

Let \(J_\varepsilon(a,b,s)\) denote the physical capture
expectation of the regularized law. Then
\[
 \liminf_{\varepsilon\downarrow0}
   \inf_{(a,b)\in D',\ s=\pm1}J_\varepsilon(a,b,s)
 \ \ge\
   \inf_{(a,b)\in D',\ s=\pm1}J_0(a,b,s)=c.
\tag{15}
\]
To prove this, choose any sequence of perturbation widths tending
to zero and approximate minimizing Monster parameters. Compactness
of \(D'\) and the finite orientation set supplies a convergent
subsequence. Couple all perturbed Princess paths with the same
original path and the same \(Z\). Uniform convergence of both
players' paths and joint lower semicontinuity of first coincidence
give the required pointwise lower limit. Capture is bounded by six
for every Monster in the parameter family, so Fatou's lemma gives
the same inequality for expected capture. The limiting Monster
has original-law payoff at least \(c\), proving (15).

Consequently all sufficiently small positive widths yield a legal
continuous law with security greater than \(U_*\); for example its
security is eventually at least \((c+U_*)/2\). This is a uniform
existence statement over the full Monster class. It does not
provide a numerical smoothing-width threshold, and does not apply
to a formal germ profile that has never been realized as an actual
law satisfying the finite attack certificate.

For a finite actual law the regularized CDF is explicit:
\[
 F_\varepsilon(t,x)=
 \sum_iw_i
 \left[\frac{x-(1-\varepsilon)p_i(t)+\varepsilon}
              {2\varepsilon}\right]_0^1,
 \qquad [y]_0^1=\min\{1,\max\{0,y\}\}.
\tag{16}
\]
For rational \(\varepsilon\) and rational polygonal inputs this
is a rational continuous piecewise-affine CDF. Its common-quantile
realization is legal and has at least the security of the raw
regularized mixture. Thus a successful finite-law certificate also
provides a concrete piecewise-affine candidate for the exact
three-integral verification machinery, if a specific positive
smoothing width is subsequently desired.

## 7. Replay and reusable checker

Run the exact examples and independent physical comparisons:

~~~sh
python3 packages/interval_one_turn/verify_finite_princess.py
~~~

The checker also accepts an actual finite law in the following
format (this elementary example has exact security one):

~~~json
{
  "format": "one-turn-finite-princess-v1",
  "paths": [
    {"weight": "1/2", "vertices": [["0", "-1"], ["6", "-1"]]},
    {"weight": "1/2", "vertices": [["0", "1"], ["6", "1"]]}
  ],
  "claim_lower": "1"
}
~~~

Run:

~~~sh
python3 packages/interval_one_turn/verify_finite_princess.py --law actual_princess_law.json
~~~

Add `--general` for rational subunit slopes or interior waits.
Add `--require-separation` to reject any actual law whose exact full-domain
security is not strictly above the frozen unrestricted upper U_*.
The elementary fixtures deliberately do not pass this strict target gate.

For actual rational piecewise-affine paths with subunit speeds or
interior waits, use the complete augmented arrangement:

~~~sh
python3 packages/interval_one_turn/verify_finite_princess.py --general --law actual_princess_law.json
~~~

Paths are inspected only through time six. A listed path ending
earlier is held at its last position; the unit-leg mode permits
this only at an endpoint, while general mode allows an interior
stationary tail. A path listed beyond six is truncated exactly
at six. These conventions specify actual trajectories and agree
with the capture horizon of the complete Monster family.

It constructs the complete attack set, checks every physical
intersection with exact arithmetic, and reports the exact
all-\(\mathcal B_1\) lower attained at a supplied attack. Rational
weights and coordinates are strings such as "1/2".
The finite fixture comparisons audit the implementation; the
continuum reduction is proved in Sections 2–3. No positive
separation from \(U_*\) is asserted without a successful actual
law and its replay.

