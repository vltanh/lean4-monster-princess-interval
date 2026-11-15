# Exact continuum completion of an endpoint-front matching deficit

Date: 2026-11-13. A constructive theorem with an explicit verified
application to the new 241-pair upper strategy. The density hypothesis
is verified for that supplied law. The later
[global full-matching reduction](GLOBAL_ZERO_DEFICIENCY_REDUCTION.md)
localizes arbitrary residual measures to the same front and removes the
density hypothesis: positive sweep probability suffices after a physical
boundary-turn modification. The older uniform-density construction below
remains the explicit realization of the supplied numerical certificate.

## 1. Physical input and the hypothesis

Let a symmetric legal Monster law and causal clocks produce an active
pressure measure \(\alpha\), of mass \(M=\mathbb E\tau_-\).
Write \(\mu_+,\mu_-\) for its positive and negative radial pressures.
Suppose the law contains the fair fastest endpoint-sweep pair with total
probability \(q>0\), and its clock on the active descending sweep is current
time. Its pressure is

\[
 \alpha_{\rm sw}=\frac q2\int_0^2\delta_{(t,1-t)}\,dt.
\]

Suppose a partial causal-order matching of \(\mu_+\) to \(\mu_-\)
covers every positive source except a submeasure

\[
 \rho\le \frac q2\,\mathbf1_{(0,1)}(t)\,dt
 \quad\text{on the front }z_t=(t,1-t).
\]

Let \(d=\rho((0,1))\). The matching need not be maximal; the certificate
already gives the upper bound \(M+d\). Necessarily \(0\le d\le q/2\).

**Theorem.** There is an explicitly described symmetric legal Monster law
with causal clocks and a full positive-pressure matching, whose active
mass is exactly \(M+d\). Thus it has zero matching deficiency and the
same upper certificate. Its stationary-endpoint Princess payoff is
exactly \(M+d\), so this is also its exact unrestricted worst-case value.

In particular, if the original input is a global optimal dual and its
unmatched pressure can be localized to this front, then a global optimal
dual with zero deficiency exists.

## 2. The physical replacement family

Assume \(d>0\), and put \(b=d/q\le1/2\). For \(0<h<b\), define a
reflection pair \(B_h\) by the representative vertices

\[
 (0,-1+2h),\qquad(h,-1+h),\qquad(2,1),\qquad(4,-1).
\]

Every leg has speed one. The first endpoint is \(+1\) at time \(2\);
the reflected path first hits \(-1\) at time \(2\).
Thus this pair's active mass is \(3\), compared with mass \(1\) for
the fast-sweep pair.

Replace probability \(d/2\) of the existing sweep pair by the continuum
of pairs \(B_h\) with unnormalized density

\[
 \lambda(dh)=\frac q2\,\mathbf1_{(0,b)}(h)\,dh.
\]

Its total probability is \(qb/2=d/2\), so probability is preserved.
The remaining sweep-pair weight is \(q-d/2\ge3q/4>0\).
All added paths are completed by time four. The new active mass is

\[
 M_{\rm new}=M+2\lambda((0,b))=M+d.
\]

For the negative-start representative use the backward clock
\(s(t)=\min(t,h)\) for \(0\le t<4\).
For its reflection use \(s(t)=0\) for \(0\le t<2h\) and
\(s(t)=t\) for \(2h\le t<2\).
Both clocks are causal and nondecreasing.

## 3. Exact pressure accounting for one pair

The representative contributes negative prefix pressure

\[
 \frac12\int_0^h\delta_{(t,\,1-2h+t)}\,dt
\]

and negative frozen-turn pressure

\[
 \frac{4-h}{2}\,\delta_{(h,\,1-h)}.
\]

The reflected path contributes a positive atom of mass \(h\) at
\((0,1-2h)\), positive front pressure
\(\tfrac12\,dt\) on \(2h<t<1\), and negative pressure
\(\tfrac12\,dt\) on \((t,t-1)\), \(1<t<2\).
This last negative pressure is exactly that of the replaced sweep pair.

Every negative prefix point causally dominates the positive atom:

\[
 1-2h+t=(1-2h)+|t-0|.
\]

Match \(h/2\) of the positive atom with the entire prefix pressure,
and its remaining \(h/2\) with the frozen turn. The latter matching is
also on equality, because

\[
 1-h=(1-2h)+|h-0|.
\]

After this internal matching, the additional usable negative pressure
is

\[
 (2-h)\,\delta_{z_h},
 \qquad z_h=(h,1-h).
\]

Relative to the replaced sweep, positive front pressure
\(\tfrac12\,dt\) on \(0<t<2h\) has been removed.
All other original pressures and matches can be retained.

## 4. The remaining matching is one-dimensional

Along the front, \(z_t\preceq z_s\) exactly when \(s\le t\).
More generally, a negative point \(w=(T,u)\) that can match any
front source has \(T+u\ge1\), and its eligible source parameters are

\[
 t\in[k(w),1],\qquad k(w)=\frac{1+T-u}{2}.
\]

The original matching restricted to front sources can therefore be
viewed as a one-dimensional matching from source time \(t\) to capacity
time \(k\le t\). Keep all matches of off-front sources fixed.
A full front matching exists precisely when cumulative available
capacity through every \(a\) is at least cumulative source mass
through \(a\), with the total-mass condition.

The new removed-positive front measure \(R\) and usable negative
front measure \(\Gamma\) satisfy

\[
 R([0,a])=\frac q4\int_0^b\min(a,2h)\,dh,\qquad
 \Gamma([0,a])=\frac q2\int_0^{\min(a,b)}(2-h)\,dh.
\]

Set \(K(a)=R([0,a])+\Gamma([0,a])\).
For \(0\le a\le2b\), with \(m=\min(a,b)\),

\[
 K(a)=\frac q2
 \left(\frac{ab}{2}-\frac{a^2}{8}+2m-\frac{m^2}{2}\right),
\]

and \(K(a)=qb=d\) for \(a\ge2b\).

On \([0,b]\),

\[
 K(a)=\frac q2\,a\left(2+\frac b2-\frac{5a}{8}\right)
 \ge\frac q2\,a.
\]

On \([b,2b]\), \(K\) is concave, \(K(b)\ge qb/2\), and
\(K(2b)=qb\). Consequently

\[
 \boxed{K(a)\ge \min(qa/2,d)\ge\rho([0,a])
 \quad(0\le a\le1).}
\]

The new source removal and capacity addition therefore cover the entire
old unmatched deficit at every cumulative threshold.
Their total combined mass is exactly \(d\).
The one-dimensional cumulative matching criterion supplies a full
matching of all remaining front sources, using the original front
partners and \(\Gamma\). Together with the retained off-front matches
and the internal matches from Section 3, this is a full causal-order
matching of the new positive pressure.

The all-Princess upper value is at most \(M+d\); the stationary
endpoint pair has physical payoff \(M_{\rm new}=M+d\), proving
the claimed exact supplied-law value.

## 5. Canonicalizing an old sweep clock preserves localization

The hypothesis does not require that an initial computed clock already
be current time on its sweep component. Suppose an arbitrary causal
sweep clock selects \(s\le t\).

If \(s,t<1\), replacing \(s\) by \(t\) moves the positive source
downward in the causal order along the front:
\(z_t\preceq z_s\).
If \(1<s\le t\), the negative point moves upward along the reflected
front \((t,t-1)\).
If \(s<1\le t\), a positive source is removed and new negative pressure
is created. Center selections create no positive source.

Disintegrate an existing matching over the sweep's scoring times.
Move surviving positive sources downward and surviving negative
partners upward; remove matches whose source disappears.
The order relation is preserved by transitivity. Every off-front
positive source remains covered, and the only uncovered new positive
sources are a submeasure of the continuous current-clock front.

Thus front localization in a finite clock computation survives the
analytic replacement of rounded sweep clocks by continuous current
clocks. The precise remaining mass \(d\) can decrease in this step.

## 6. General first-crossing retiming

The same geometry gives a useful normal form for every matching edge.
For a physical Monster path write

\[
 U_m(s)=s+m(s),\qquad V_m(s)=s-m(s).
\]

Both are nondecreasing. A positive source \(z=(t,u)\), with
\(c=t+u\) and \(e=t-u\), can match a negative selected history \(s\)
exactly when

\[
 V_m(s)\ge c,\qquad U_m(s)\le e.
\]

Retiming this negative selected history to

\[
 h_m(c)=\inf\{v\ge0:V_m(v)\ge c\}
\]

preserves causality and the matching relation. Indeed
\(h_m(c)\le s\), \(U_m(h_m(c))\le e<c\), and
\(V_m(h_m(c))\ge c\), so the new location remains negative.
Unless \(V_m(0)>c\), the new partner lies exactly on \(V=c\).

The map is Borel: for \(r\ge0\),
\(h_m(c)\le r\) iff \(V_m(r)\ge c\).
Lift a matching to its physical path/scoring-time provenance by
disintegration, perform this retiming, and leave unmatched clock mass
unchanged. The resulting kernels remain causal. The existing
conditional quantile clock compression then restores nondecreasing
deterministic clocks without changing the pathwise selected-history
measure.

This yields monotone crossing fronts
\(f_m(c)=U_m(h_m(c))\), with a matching condition \(f_m(c)\le e\).
It is a structural reduction of matching edges, not a finite
parameterization of all possible Monster fronts.

## 7. Remaining global issue

No proof is supplied that every optimal dual, or even one optimal dual,
has a matching whose unmatched positive sources lie solely on its
endpoint-sweep component. No proof that optimal sweep weight \(q\)
is positive is supplied either.

Those are the exact missing hypotheses for using this construction to
establish a global zero-deficiency optimum. The construction itself
is explicit, physical, and preserves the certified upper value.

## 8. An explicit verified continuum Monster strategy

The localization hypothesis has now been verified exactly for the
241-pair reweighted finite Monster law in
[reweighted_physical_clock_certificate.json.gz](../../packages/interval_global_closure/reweighted_physical_clock_certificate.json.gz).
Its complete physical path law, clocks, and interval-containment matching
are included in that file. The proof of the exact finite clock templates
and the independently replayed checks are in
[FINITE_BANK_CLOCK_HOMOGENIZATION.md](FINITE_BANK_CLOCK_HOMOGENIZATION.md).

For this law,

\[
 q=\frac{125454990007}{200000000000},\qquad
 d=\frac{9570689369683068933669}
         {4000000000000000000000000000},
\]

\[
 b=\frac dq=
 \frac{9570689369683068933669}
      {2509099800140000000000000000}
 \approx 3.8143916671425563\cdot10^{-6}.
\]

The exact completed strategy is therefore:

1. Keep every nonsweep reflection pair in the certificate at its listed
   probability.
2. Use the fastest endpoint-sweep reflection pair with probability
   \(q-d/2\).
3. With probability \(d/2\), draw \(h\) uniformly from \((0,b)\),
   use the \(B_h\) route from Section 2, and choose its reflection
   independently with probability one half.

The third component has probability

\[
 \frac d2=
 \frac{9570689369683068933669}
      {8000000000000000000000000000}
 \approx1.1963361712103836\cdot10^{-6}.
\]

Equivalently, its unnormalized pair density is
\(q/2=125454990007/400000000000\) on \((0,b)\).
The remaining sweep probability is

\[
 q-\frac d2=
 \frac{5018190029590630316931066331}
      {8000000000000000000000000000}.
\]

Every added route hits the center at time one and visits both endpoints
by time four. Its clocks and internal matching are the explicit ones
from Sections 2 and 3. The full matching follows from Section 4 and the
replayed front-density domination.

The resulting actual continuum law has zero deficiency and exact
unrestricted Princess-response value

\[
 \boxed{
 \sup_{p\ {\rm legal}}\mathbb E T(M,p)
 =
 \frac{1140799301969009059644426513}
      {800000000000000000000000000}
 \approx1.4259991274612613.}
\]

This supremum is attained by each stationary endpoint Princess:
symmetry makes its endpoint-hitting mean equal to the new active mass,
and the full matching bounds every legal Princess by that same mass.
Thus this is an exact worst-response computation for a compactly
described continuum Monster law, including all continuous Princess
paths and all contact atoms.

The construction preserves the upper value of its finite seed.
It does not prove that this number is the unrestricted game value:
a matching global Princess lower strategy is still missing, and
global optimal front localization has not been proved.

The following standard-library command verifies the physical finite
seed and all numerical hypotheses of the analytic continuum
completion:

    python packages/interval_global_closure/replay_continuum_clock_certificate.py packages/interval_global_closure/reweighted_physical_clock_certificate.json.gz

The compressed physical certificate has SHA256

    37175c842b97bb5f3774815be076450f5852ddb51d530e4956d7b9a71b7fc652

It contains the full seed law and can be replayed without any external
optimizer state.
