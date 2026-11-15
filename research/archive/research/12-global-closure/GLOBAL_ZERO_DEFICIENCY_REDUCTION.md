# Global reduction to fully matched physical pressure


**Attainment update:** the later [protected-tail theorem](GLOBAL_ZERO_DEFICIENCY_ATTAINMENT.md)
strengthens the infimum below to an attained minimum within the same
center-3/completion-9 class, without a positive-sweep-mass assumption.
This note supplies the localization and physical completion operations
used by that proof. The game value itself is not evaluated.

Global theorem, independently reviewed, 2026-11-13.

Let \(V\) be the unrestricted interval Princess--Monster value. For a
symmetric physical Monster law \(\nu\), let
\(M(\nu)=\mathbb E_\nu\tau_-\) be its endpoint baseline. A physical
causal-clock certificate with all positive pressure matched has
deficiency zero; write \(D=0\) for this property.

The exact active-clock dual and pressure-matching theorem identify the
worst Princess payoff with the minimum certificate value \(M+d\).
The stationary fair endpoint Princess law attains \(M\) against every
symmetric Monster law. Hence a law with a full matching has actual
worst payoff exactly \(M\).

The result proved here is

\[
 \boxed{V=\inf\{M(\nu):
       \nu\text{ admits physical causal clocks and a full pressure matching}\}.}
\]

Moreover, if any globally optimal law has positive probability on the
fair fastest endpoint-sweep pair, then a globally optimal law with
deficiency zero exists. The infimum identity does not assume this
positive-mass condition and does not assert zero-deficiency attainment.

The infimum may be restricted to fully matched laws that visit the
center by time \(3\) and complete both endpoints by time \(9\).
The original exact horizon \(7\) is not claimed to be preserved by
the boundary-turn modification.

All constructions use actual physical paths and causal selected-history
resources. No detached Eulerian occupation relaxation is used.

## 1. Normalized physical pairs and localized residual

Use universal first-endpoint tail dominance to normalize every physical
path: after its first endpoint visit it moves at unit speed to the
opposite endpoint. A symmetric law may then be represented by a
probability measure \(\mu\) on path-pair representatives \(m\) that hit
\(+1\) first. If that visit is at time \(\sigma\), then

\[
 \tau_+(m)=\sigma,\qquad \tau_-(m)=\sigma+2.
\]

The active scoring resources of the two equally weighted orientations
are

\[
 \frac12\,dt\quad(0\le t<\sigma+2)\text{ on }m,
 \qquad
 \frac12\,dt\quad(0\le t<\sigma)\text{ on }-m.
\]

Their endpoint baseline is \(1+\sigma\).

Apply [POST_FIRST_ENDPOINT_PRESSURE_LOCALIZATION.md](POST_FIRST_ENDPOINT_PRESSURE_LOCALIZATION.md). Canonical current
clocks are retained on the fastest endpoint-start sweep. All remaining
unmatched positive resources are supported on the initial front

\[
 z_t=(t,1-t),\qquad 0<t<1.
\]

Their measure \(\rho\) has no atom at zero. Let \(q\) be the probability
of the fair fastest sweep pair. The total deficiency and its resource
decomposition are

\[
 d=d_{\mathrm{sweep}}+d_{\mathrm{int}},\qquad
 d_{\mathrm{sweep}}\le q/2.
\]

For every interior-start representative define the first light-coordinate
crossing

\[
 h(m)=\inf\{s:s+m(s)\ge1\}.
\]

Every residual-carrying interior pair has \(0<h<\min(1,\sigma)\).
There is a measurable \(r(m)\in[0,1/2]\), zero on other pairs, such that

\[
 \rho_{\mathrm{int}}=\int r(m)\delta_{h(m)}\,\mu(dm),
 \qquad d_{\mathrm{int}}=\int r(m)\,\mu(dm).
\]

The bound \(r\le1/2\) follows from the scoring-time lift before the
final retiming: the unmatched units occupy at most one unit of time on
the orientation of probability \(1/2\) that survives the first endpoint.

## 2. Completion of an arbitrary front measure

### Lemma

Suppose a normalized physical certificate has a front residual
\(\rho\) on \((0,1)\), of total mass \(d\), and has current-clock
fastest sweep probability \(q\ge d/2\). Then another physical law
admits a full matching and has endpoint baseline exactly \(M+d\).
No density bound on \(\rho\) is required.

### The physical replacement

For \(0<h<1/2\), use the fair reflection pair of

\[
 B_h:(0,-1+2h)\longrightarrow(h,-1+h)
       \longrightarrow(2,1)\longrightarrow(4,-1).
\]

All legs have unit speed. This pair has baseline \(3\), whereas the
fast sweep pair has baseline \(1\).

The negative-start orientation selects current time until \(h\) and
then freezes at \(h\) until its active lifetime ends at \(4\).
The reflected orientation selects time zero until scoring time \(2h\)
and then selects current time until its active lifetime ends at \(2\).
These are causal clocks.

Their pressure consists of:

- negative prefix density \(ds/2\) at
  \((s,1-2h+s)\), \(0<s<h\);
- negative front mass \((4-h)/2\) at \(z_h\);
- positive atom of mass \(h\) at \((0,1-2h)\);
- positive front density \(dt/2\) on \(2h<t<1\);
- the unchanged negative sweep pressure of density \(dt/2\) on \(1<t<2\).

The positive atom is matched internally using the negative prefix,
of mass \(h/2\), and \(h/2\) of the front atom. Every prefix point
dominates the positive atom in interval containment, and so does \(z_h\).
The usable new negative front mass is therefore \(2-h\).

Relative to the replaced fast sweep, this operation removes positive
front density \(dt/2\) on \(0<t<2h\), retains all old negative sweep
pressure, and supplies the usable negative atom \((2-h)\delta_h\).

Choose the pair-replacement measure

\[
 \lambda=\frac12\,(t\mapsto t/2)_\#\rho.
\]

Its total mass is \(d/2\le q\), so this amount of the existing sweep
pair can be replaced without changing total probability. Atoms of
\(\rho\) at positive times simply give atoms of \(\lambda\); every
new path remains strictly interior-starting.

Let \(R\) be the removed positive front measure and \(\Gamma\) the
usable new negative front measure. Their combined cumulative mass is

\[
 K(a):=R([0,a])+\Gamma([0,a])
 =\int\left[
       \frac12\min(a,2h)+(2-h)\mathbf1_{\{h\le a\}}
      \right]\lambda(dh).
\]

For \(a\ge2h\), the bracket is exactly \(2\). It is nonnegative
everywhere. Therefore

\[
 K(a)\ge2\lambda((0,a/2])=\rho((0,a]),
 \qquad K(1)=d.
\]

The removed density is bounded by
\(\lambda((0,1/2))/2=d/4\le q/2\), so \(R\) really is a submeasure
of the fast-sweep positive pressure.

### Preserve old off-front matches and complete on the front

Retain every old off-front matching edge. For the negative resource
fractions used by front matches, retime their selections to their
path's first crossing of \(s-m(s)=1\). This time is earlier than the
old selected time and hence is causal. It remains a negative selected
position and still dominates the original positive front point:
the negative interval now has right endpoint \(1\), while its left
endpoint has decreased. Only the fractions assigned to front matches
are retimed, so other matches are untouched.

Let \(A\) be all original positive front pressure, and \(C\) the
resulting negative front capacity used by its old matching. A negative
front point indexed by \(s\) dominates a positive front point indexed
by \(t\) exactly when \(s\le t\). Thus the old matching gives

\[
 C([0,a])\ge(A-\rho)([0,a]).
\]

After the replacement the positive front demand is \(A-R\), and
the available negative front capacity is \(C+\Gamma\). The preceding
cumulative inequalities give

\[
 (C+\Gamma)([0,a])\ge(A-R)([0,a]).
\]

Their total masses agree, since \(R((0,1))+\Gamma((0,1))=d\).
The one-dimensional monotone coupling, or its quantile construction,
therefore gives a full front matching.

The preserved negative sweep pressure supports every old matching that
used it; the new internal matches use disjoint resource fractions.
The resulting certificate is fully matched.

Replacing probability \(d/2\) of baseline-\(1\) pairs by baseline-\(3\)
pairs increases the baseline by exactly \(d\). This proves the lemma.

## 3. A boundary turn reduces the remaining deficiency at no added bound

We now remove the condition \(q\ge d/2\) whenever \(q>0\). The
construction also produces arbitrarily small residual when \(q=0\).

Fix an integer \(n\ge2\). On every interior pair with \(r(m)>0\), set

\[
 \eta(m)=\min\left(\frac1n,\frac{\sigma(m)-h(m)}2\right),
 \qquad a=\sigma-\eta,
 \qquad \varepsilon=1-m(a).
\]

These choices are measurable, and

\[
 h<a<\sigma,\qquad
 0<\varepsilon\le\eta\le1/n.
\]

The last inequality follows from the unit speed bound and
\(m(\sigma)=1\). In particular the turn is at a positive position
\(m(a)=1-\varepsilon\).

Replace the fraction

\[
 \gamma(m)=r(m)/2\le1/4
\]

of this fair pair by a new fair pair whose positive representative
\(m^a\) follows \(m\) until \(a\), then moves left at unit speed to
\(-1\), then moves right at unit speed to \(+1\).

The new first and second endpoint times are

\[
 T=a+2-\varepsilon
   =\sigma+2-\eta-\varepsilon,\qquad T+2.
\]

There was no endpoint visit before \(a\). Hence the new pair's
baseline is \(T+1\), and its increase over the old baseline
\(\sigma+1\) is exactly

\[
 2-\eta-\varepsilon.
\]

The path after its new first endpoint is again a direct unit sweep.

### Retain old resources whenever their pressure improves

For the original orientation, retain its old selected history time
for each scoring time \(0\le t<T\). The new physical history satisfies

\[
 m^a(s)\le m(s)\qquad(0\le s<T).
\]

Before \(a\) the histories agree. After \(a\), the new position is the
smallest position allowed by the unit speed constraint from \(m(a)\).
Thus every retained positive source becomes weaker or disappears, and
every retained negative partner becomes stronger. Existing matching
edges continue to hold whenever both endpoints are retained.

The deleted original-orientation scoring interval has length
\(\eta+\varepsilon\). Its probability-weighted resource mass is
\((\eta+\varepsilon)/2\).

For the reflected orientation, keep every old resource with scoring
time \(t<a\). These physical histories are unchanged. Discard its old
selected pressures on \(a\le t<\sigma\), whose weighted resource
mass is \(\eta/2\).

Deleting a positive source cannot increase unmatched positive mass.
Deleting a negative partner can expose at most its deleted mass.
Consequently the total possible loss of old matching capacity is at
most

\[
 \frac{\eta+\varepsilon}{2}+\frac\eta2
   =\eta+\frac\varepsilon2
\]

per replaced pair.

### Use all new reflected resources at the old negative front point

The new reflected active lifetime ends at \(T+2=a+4-\varepsilon\).
For all its scoring times

\[
 a\le t<a+4-\varepsilon
\]

select the old history time \(h\). This is causal because \(h<a\).
Its selected position is
\(-m(h)=-(1-h)<0\), so these resources give new negative front
capacity

\[
 2-\varepsilon/2
\]

at exactly the front point that carries the original pair's residual.

The original unmatched interior sources are all retained: their scoring
times were in \([\sigma,\sigma+1)\), while

\[
 T=\sigma+2-\eta-\varepsilon\ge\sigma+1.
\]

Their selected time \(h<a\) and selected position are unchanged.
After replacing the pair fraction \(\gamma=r/2\), the new negative
capacity assigned to these sources is
\(\gamma(2-\varepsilon/2)\). Their remaining original deficiency is
at most

\[
 r-\gamma(2-\varepsilon/2)
   =\gamma\varepsilon/2.
\]

This matching uses only previously unmatched source fractions and the
new reflected resource pool, which is disjoint from every retained old
negative resource.

Combining the leftover original residual with any matching capacity
lost during deletion gives the per-pair bound

\[
 \gamma\frac\varepsilon2
   +\gamma\left(\eta+\frac\varepsilon2\right)
   =\gamma(\eta+\varepsilon).
\]

The argument is valid for simultaneous modifications of all pairs.
Lift old matching edges to the retained or modified copies of their
resource endpoints; remove an edge only if its source disappears or
its target resource is deleted. Pressure dominance preserves all other
edges. Product disintegration of the endpoint copy kernels performs
this lifting for arbitrary measures.

### Exact integrated accounting

Put

\[
 A_n=\int \gamma(m)(\eta(m)+\varepsilon(m))\,\mu(dm).
\]

Then

\[
 0\le A_n\le\frac{d_{\mathrm{int}}}{n}.
\]

The modified physical law has baseline

\[
 \boxed{M_n=M+d_{\mathrm{int}}-A_n}
\]

and a causal matching certificate with deficiency

\[
 \boxed{d_n\le d_{\mathrm{sweep}}+A_n.}
\]

In particular

\[
 \boxed{M_n+d_n\le M+d.}
\]

This is an exact inequality for each \(n\), not merely a limiting
estimate. The new physical paths have finite active mass. The
fast-sweep probability \(q\) is unchanged because only interior-start
pairs were modified.

Apply global resource localization again to the remaining unmatched
units. This preserves \(M_n\), does not increase \(d_n\), and yields
a front residual with no atom at zero while preserving current
fast-sweep clocks. Perform clock compression only after the resource
matching constructions have been completed.

## 4. Positive sweep probability gives a full matching without loss

Suppose \(q>0\). Choose \(n\ge2\) so large that

\[
 \frac q2+\frac{d_{\mathrm{int}}}{n}\le2q.
\]

The preceding construction gives

\[
 d_n\le d_{\mathrm{sweep}}+A_n
      \le\frac q2+\frac{d_{\mathrm{int}}}{n}
      \le2q.
\]

Section 2 therefore applies to its arbitrary front residual.
The completed physical law has a full pressure matching and baseline

\[
 \widetilde M=M_n+d_n\le M+d.
\]

Thus any finite-mass physical certificate with positive fast-sweep
probability can be converted to a fully matched physical law at no
larger certified bound.

If the original law and certificate are globally optimal, then
\(M+d=V\). Since no physical law can have worst payoff below \(V\),
the completed law must satisfy

\[
 \widetilde M=V,\qquad \widetilde D=0.
\]

## 5. The unconditional infimum identity

Let \(\mathcal Z\) be the class of symmetric physical laws admitting
causal clocks with a full pressure matching. Every law in
\(\mathcal Z\) has worst Princess payoff exactly its endpoint baseline.
Therefore

\[
 V\le\inf_{\nu\in\mathcal Z}M(\nu).
\]

For the reverse inequality, take any finite-mass physical certificate
of value \(U=M+d\) arbitrarily close to \(V\). Such certificates exist
by the exact horizon and active-clock reductions. For any
\(\delta\in(0,1)\), mix in probability \(\delta\) of the fair fastest
sweep pair with its current clocks. The sweep certificate has baseline
\(1\) and deficiency at most \(1/2\), so the mixed certificate has
value at most

\[
 U_\delta=(1-\delta)U+\frac32\delta.
\]

The mixture has positive fast-sweep probability. Section 4 converts
it to a fully matched physical law with baseline at most \(U_\delta\).
Let \(\delta\downarrow0\), then let \(U\downarrow V\), to obtain

\[
 \inf_{\nu\in\mathcal Z}M(\nu)\le V.
\]

This proves the asserted identity.

### A uniform completion horizon of nine

The exact horizon theorem supplies a globally optimal symmetric law
whose paths visit the center by time \(3\) and complete both endpoints
by time \(7\). Normalize its first-endpoint tails; the center visit
does not become later, and its first endpoint time satisfies
\(\sigma+2\le7\), hence \(\sigma\le5\).

Mixing in fast sweeps preserves these time bounds. Every boundary-turn
replacement in Section 3 completes its second endpoint at

\[
 T+2=\sigma+4-\eta-\varepsilon\le9.
\]

It also reaches the center no later than the original path. If the
center was reached before \(a\), that prefix is unchanged. Otherwise
the new path reaches the center at \(a+m(a)\), which is the earliest
time allowed by the unit speed bound from the positive position \(m(a)\).
Its reflected path has the same first center time.

The completion pairs \(B_h\) reach the center by time \(1\) and both
endpoints by time \(4\). Clock localization changes no physical path.
Thus every approximating fully matched law in the infimum argument
can satisfy simultaneously

\[
 \tau_0\le3,\qquad \max(\tau_+,\tau_-)\le9
 \quad\text{almost surely}.
\]

Consequently the stronger exact identity is

\[
 \boxed{
 V=\inf\{M(\nu):\nu\in\mathcal Z,\ 
              \tau_0\le3,\ \tau_+\le9,\ \tau_-\le9
              \text{ almost surely}\}.}
\]

If the initial optimal law in the horizon-seven class has \(q>0\),
the zero-deficiency optimizer supplied by Section 4 also obeys these
horizon-nine and center-three bounds. More generally the positive-\(q\)
attainment result remains true for any finite-mass optimum, but an
arbitrary such optimum need not initially have the horizon-seven bound.

The construction does not show that \(\mathcal Z\) is closed or that
its infimum is attained. In the boundary-turn limit, a path can first
touch an endpoint earlier than every approximating path, so active
clock resources can disappear. Compactness of physical path space
alone cannot remove this issue, even under the uniform horizon-nine
restriction.

## 6. Exact finite checks accompanying the measure proof

The standard-library verifier [verify_global_pressure_localization.py](../../packages/interval_global_closure/verify_global_pressure_localization.py)
checks a genuinely fractional alternating cycle with unused negative
capacity, including an unrelated closed cycle that carries no
deficiency. It verifies the simultaneous resource rerouting marginals
exactly with rational arithmetic.

It also checks arbitrary atomic front measures, including a case that
consumes the entire sweep probability, and verifies the cumulative
completion inequalities at every affine breakpoint and jump. A
physical multileg path fixture checks the boundary-turn geometry,
active resource lengths, pressure dominance, and the exact
baseline/deficiency accounting.

These finite checks guard the formulas and simultaneous accounting.
The arguments above supply the measure-level proof and do not rely
on sampling a path or measure class.
