# Effective finite upper reduction by common light-coordinate quantization

Research proof for independent review, 2026-11-13.

There is a concrete sequence of finite rational linear programs with values
\(U_n\) satisfying

\[
 \boxed{U_n-\frac1{2n}\ \le\ V\ \le\ U_n.}
\]

Every feasible point supplies an actual finite law on rational unit-speed
Monster paths and an atomic causal-clock/pressure-matching upper certificate.
Rational feasible points have rational mixture and clock weights.
The error estimate follows from an explicit physical quantization and a
small clock buffer. It does not assume upper-semicontinuity of the
Princess supremum under weak approximation of Monster laws.

The input global result is the attained full-matching optimal law:
some symmetric Monster law visits the center by time \(2\), completes
both endpoints by time \(8\), and has a causal active clock of mass
\(M=V\) whose positive pressure is fully matched. The general
quantization lemma below also allows an initial deficiency.

## 1. Clock and pressure conventions

For an oriented physical Monster path \(m\), let

\[
 \tau(m)=\inf\{t:m(t)=-1\}.
\]

A causal active clock can be represented by a measure \(\eta_m\) on
selected history times, with

\[
 \eta_m([0,\tau(m)))=\tau(m),\qquad
 \eta_m([0,s])\ge s\quad(0\le s<\tau(m)).
\]

The prefix condition is equivalent to realizing its selected-time law
by a causal selector, or by the monotone quantile clock. Its selected
spacetime event measure, averaged over a symmetric Monster law \(\nu\),
is denoted by \(\alpha\), and has total mass

\[
 M=\mathbb E_\nu\tau.
\]

For a radial Princess path \(r\), the one-clock plane has integrand

\[
 \Phi(r(t),x)=
 \begin{cases}
 1+\mathbf1_{\{r(t)<x\}},&x>0,\\
 \mathbf1_{\{r(t)>0\}},&x=0,\\
 \mathbf1_{\{r(t)>-x\}},&x<0.
 \end{cases}
\]

It lies in \([0,2]\). The actual symmetric capture payoff is bounded
above by this plane for every fixed clock.

A positive event \(z=(t,x)\), \(x>0\), can be matched to a negative
event \(w=(s,-y)\), \(y>0\), when

\[
 [t-x,t+x]\subseteq[s-y,s+y],
 \quad\text{equivalently}\quad
 y\ge x+|s-t|.
\]

For every legal radial \(r\), the two equal-mass matched contributions
have sum at most \(2\). Center events have contribution at most \(1\);
unmatched negative events also have contribution at most \(1\).
Consequently a matching leaving positive mass \(d\) uncovered gives
the upper bound \(M+d\).

## 2. One common nearest-grid map

Fix \(n\ge1\), and put

\[
 h=\frac1n,\qquad \delta=\frac h2.
\]

Define

\[
 T_h(z)=h\,\operatorname{round}_{\rm even}(z/h),
\]

where half-integers are rounded to the nearest even integer.
Then \(T_h\) is nondecreasing and satisfies

\[
 T_h(-z)=-T_h(z),\qquad
 T_h(z+2)=T_h(z)+2,\qquad
 |T_h(z)-z|\le\delta.
\]

The translation identity uses that \(2/h=2n\) is even.
An arbitrary tie convention, such as rounding away from zero, would
not give this identity at every tie.

The same map is applied to every physical path, every selected event,
and both ends of every pressure-matching edge.

## 3. Physical lift to a finite unit-speed lattice path

Write the original light coordinates as

\[
 U(s)=s+m(s),\qquad W(s)=s-m(s).
\]

They are nondecreasing. Their quantized image

\[
 \bigl(T_h(U(s)),T_h(W(s))\bigr)
\]

is a finite coordinatewise ordered chain of lattice nodes over a
bounded time interval. All its nodes satisfy

\[
 |T_h(U)-T_h(W)|\le2.
\]

Indeed \(U\le W+2\) and \(W\le U+2\), so monotonicity and the
translation identity preserve both inequalities.

Connect consecutive image nodes by positive coordinate-axis steps of
length \(h\), staying in this strip. Parameterize each step by physical
time \((U+W)/2\). These are physical unit-speed Monster moves.

At a simultaneous crossing of two rounding thresholds, include the
actual ties-to-even image node as well as the before/after nodes.
If the tie image is one intermediate corner, it fixes the order of
the two steps. If it is the before or after node, either legal order
can be used. At a strip boundary choose the inward step first when
necessary. Thus every exact \(T_h\)-image event is present on the
new physical path.

The construction can be chosen as a Borel kernel invariant under
reflection: for example use a uniform choice among the finitely many
legal fills of the image chain. Reflection swaps the two coordinates
and bijects these fills. A randomized tie choice is necessary for a
self-reflected simultaneous center jump; a deterministic
reflection-equivariant fill need not exist.

Denote a resulting physical path by \(m'\). Each old selected time
\(s\) has its image at the new physical time

\[
 r_m(s)=\frac{T_h(s+m(s))+T_h(s-m(s))}{2},
 \qquad |r_m(s)-s|\le\delta.
\]

Its physical position is the corresponding half-difference.
Oddness gives \(r_m(0)=0\), so the initial time is unchanged.

If \(m(s)=-1\), the image position is exactly \(-1\), and similarly
for \(+1\). Hence, writing \(\tau'=\tau(m')\),

\[
 \tau'\le r_m(\tau)\le\tau+\delta.
\]

The new path may hit an endpoint earlier, which is permitted.

Suppose both old endpoints have been visited by an integer time \(D\).
Hold the original path at its last endpoint after its second endpoint
visit. For an endpoint visit at time \(s\le D\), the image time is
\(1+T_h(s-1)\le1+T_h(D-1)=D\).
Thus the quantized path also completes both endpoints by \(D\).
If a center visit occurred by an integer time \(C\), its image is a
center visit at \(T_h(s)\le C\). In particular center-by-\(2\) and
completion-by-\(8\) are preserved.

## 4. Repair the scoring clock with a buffer of mass \(\delta\)

The selected-time pushforward \(r_{m\#}\eta_m\) is supported on
actual vertices of \(m'\), but its scoring prefixes need not be causal
for the changed physical time. Define

\[
 \zeta_m=r_{m\#}\eta_m+\delta\,\delta_0.
\]

For every \(0\le t<\tau'\), one has

\[
 \zeta_m([0,t])\ge t.
\]

For \(t<\delta\), the added atom proves this directly. Otherwise set
\(s=t-\delta\). The endpoint inequality above gives \(s<\tau\),
and every old selected time \(u\le s\) satisfies
\(r_m(u)\le u+\delta\le t\). Therefore

\[
 \zeta_m([0,t])
 \ge\delta+\eta_m([0,t-\delta])
 \ge\delta+(t-\delta)=t.
\]

Also \(\zeta_m\) has mass \(\tau+\delta\ge\tau'\).
Keep its earliest \(\tau'\) units of mass, taking a fraction of the
last retained atom if needed. Call the resulting measure \(\eta'_m\).
It has total mass \(\tau'\) and still obeys every causal prefix bound.
When \(\tau'=0\), this simply discards the entire raw clock and buffer.

Moreover all its selected times lie strictly before \(\tau'\).
Letting \(t\uparrow\tau'\) in the preceding prefix inequality gives
\(\zeta_m([0,\tau'))\ge\tau'\), so no atom at the first negative
endpoint needs to be retained.

Thus \(\eta'_m\) is an actual active causal clock on \(m'\), and

\[
 \eta'_m\le r_{m\#}\eta_m+\delta\,\delta_0
\]

as measures. Averaging over old paths and fill choices, then
conditioning on each resulting lattice path, gives admissible clocks
for the finite new Monster law.

## 5. The upper bound increases by at most \(h/2\)

A selected event with interval \([a,b]\) is sent to the event with
interval \([T_h(a),T_h(b)]\). Since \(T_h\) is nondecreasing,
every matching containment remains valid.

Positive and negative spatial signs can collapse to zero but cannot
reverse. If an image matching target has zero radius, its contained
source interval also has zero radius. Discard those collapsed
matching edges. Every remaining positive-radius source retains its
negative-radius partner. Thus pushing the old event measure through
\(T_h\) leaves at most the original uncovered positive mass \(d\).

The pushed measure has the same total mass \(M\), so its plane is
bounded by \(M+d\). This argument still permits raw pushed events
at the negative endpoint: there their actual integrand is zero, and
the matching estimate remains valid.

The time-zero buffer has total mass \(\delta\) after averaging over
the probability law. Its spatial distribution is symmetric: every
oriented path receives the same buffer, the old law is symmetric, and
\(T_h\) is odd. Each positive buffer event therefore matches its
reflected negative event at the same time and radius. Center buffer
mass has contribution at most its mass.

Equivalently, for \(x>0\),

\[
 \Phi(r,x)+\Phi(r,-x)=2-\mathbf1_{\{r=x\}}\le2,
\]

and \(\Phi(r,0)\le1\). Thus the symmetric buffer adds at most
\(\delta\), not \(2\delta\), to any Princess plane.
Chronological truncation removes only nonnegative integrand
contributions. Hence the new physical law with its repaired clocks
has the all-Princess upper bound

\[
 \boxed{M+d+\delta=M+d+\frac h2.}
\]

There is also a direct matching-objective accounting. Let \(R\) be the
total raw clock mass discarded in the truncation. The raw mass is
\(M+\delta\); its uncovered positive mass is at most \(d\), because
the buffer is itself fully matched.
Deleting positive capacity cannot increase deficiency, while deleting
negative capacity increases it by at most the deleted negative mass,
which is at most \(R\). The final certificate therefore satisfies

\[
 M'+d'
 \le(M+\delta-R)+(d+R)
 =M+d+\delta.
\]

This supplies an actual finite matching certificate after truncation,
not just a bound on an unimplemented clock plane.

## 6. An explicit rational finite linear program

Take \(D=8\). Let \(\mathcal B_n\) contain every unit-axis lattice
path with:

* initial position in \(\{-1,-1+h,\ldots,1\}\);
* physical step duration \(\Delta=h/2\);
* center visited by time \(2\);
* both endpoints visited by time \(8\).

One may represent every path through time \(8\), even after both
endpoints have been visited. There are at most

\[
 (2n+1)\,2^{16n}
\]

such binary step sequences before imposing strip and visit constraints.
The bank is finite, closed under reflection, and constructively enumerable.

For every oriented bank path \(m\), introduce its probability \(w_m\),
with \(\sum_mw_m=1\) and \(w_m=w_{-m}\).
If its first negative endpoint is at time \(k_m\Delta\), introduce
clock charges \(a_{m,j}\ge0\) at its vertices
\(j=0,\ldots,k_m-1\). Impose

\[
 \sum_{j=0}^{k_m-1}a_{m,j}=w_m k_m\Delta,\qquad
 \sum_{i=0}^{j}a_{m,i}\ge w_m(j+1)\Delta
 \quad(0\le j<k_m).
\]

These are the exact causal conditions for a clock supported on
left endpoints of the scoring intervals. The last prefix inequality
is the displayed total-mass equality.

Aggregate the positive and negative charges at each spacetime node.
Introduce nonnegative matching variables for every pair of nodes
whose intervals satisfy the containment condition. Their source
and target sums are bounded by the corresponding aggregate charges.
Minimize

\[
 \sum_m w_m k_m\Delta
 +\sum_{\text{positive nodes }z}a_z
 -\sum_{\text{matching edges }(z,w)}\pi_{zw}.
\]

All data and constraints are rational. The feasible set is nonempty
and bounded, and each feasible point represents a genuine physical
Monster law, causal clocks, and a pressure matching. Its objective
is therefore an unrestricted upper bound.

Let the exact optimum be \(U_n\). A rational optimal extreme point
exists, so the upper law and certificate may be taken rational.
No approximation of arbitrary real mixture weights is needed.

Apply Sections 2--5 to the attained fully matched optimal
center-by-\(2\), completed-by-\(8\) law, for which \(M=V,d=0\).
The resulting real feasible point of this finite LP has objective at
most \(V+\delta\). Consequently

\[
 V\le U_n\le V+\frac1{2n}.
\]

Thus solving one explicitly specified finite rational LP gives the
two-sided enclosure

\[
 \boxed{U_n-\frac1{2n}\le V\le U_n.}
\]

For dyadic \(n\), the banks and atomic clock times refine each other,
so \(U_{2n}\le U_n\). The construction is effective but not claimed to
be computationally economical: the naive path bank is exponential.

## 7. What the theorem does and does not assert

Finite rational unit-speed Monster laws with atomic causal clocks are
value-dense, with an explicit error \(1/(2n)\) for the common lattice
quantization. The finite programs are complete upper certificates,
and the quantization theorem turns each exact program value into a
global lower bound as well.

This is a quantitative sequence of finite reductions. It does not
assert that one fixed finite program has value exactly \(V\), that
the equilibrium is a finite rational law, or that the naive
exponential bank is practical at high precision.

Independent snapping of individual starts, turns, or paths is not
covered. The proof requires the same monotone map on every light
coordinate of every physical event and every pressure-matching edge,
followed by the explicit scoring-clock buffer and truncation.
