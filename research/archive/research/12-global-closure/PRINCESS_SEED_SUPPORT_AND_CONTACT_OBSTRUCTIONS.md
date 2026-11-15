# The 338-path seed: support ceiling and two contact barriers

**Scope.** This note reproduces the original 338-path unrestricted Princess lower
certificate, proves a ceiling for *every reweighting of its exact path
support*, and isolates why ordinary mesh snapping destroys its security.
It does not identify the unrestricted equilibrium or exclude continuous
Princess CDFs. All finite assertions below are replayed with rational
arithmetic by

```sh
python packages/interval_princess_geometry/verify_geometry.py
```

The geometry replay file is
`packages/interval_princess_geometry/geometry_certificate.json`.
The existing exhaustive capture-order oracle supplies the two unrestricted
response minima. A separate polygon-intersection implementation checks
every direct-route payoff and the support upper certificate.

## 1. Reweighting this support cannot materially improve the lower bound

Let \(p_1,\ldots,p_{169}\) be the positive paths in
`packages/interval_uniform_reduction/princess_strategy.json`, and include
their reflections. Their present weighted law has exact unrestricted
security

\[
L=\frac{36290299773897097}{25600000000000000}.
\]

Here \(L\) denotes the original 338-path value. Section 6 retains a tiny,
exactly verified improvement as a constructive regression.

Consider the **legal** symmetric Monster law in
`packages/interval_uniform_reduction/rejected_dual.json`: it contains 164
reflected pairs, with positive integer pair weights totaling \(10^9\).
This law was correctly rejected as a matching unrestricted upper: another
Princess path attains about 1.635 against it. That does not invalidate its
use as an opponent of the specified 338-path support.

For each \(p_i\), compute every first coincidence with these 328 oriented
Monster paths, including equality at vertices and the beginning of any
coincident segment. The largest expected payoff among the 338 paths is
exactly

\[
C_{\rm support}
=\frac{362903002466223591}{256000000000000000}
=1.417589853383686\ldots .
\]

The Monster law is symmetric, so \(p_i\) and \(-p_i\) have the same
expected payoff. Linearity proves the following statement without any
assumption on the Princess weights:

> **Fixed-support obstruction.** Every probability distribution supported
> on these 338 exact paths, including asymmetric distributions, has
> unrestricted security at most \(C_{\rm support}\).

The remaining room for reweighting is therefore at most

\[
C_{\rm support}-L
=\frac{4727252621}{256000000000000000}
=0.00000001846583055078125.
\]

This is a certificate for an entire optimization class, not an LP discovery
number. The verifier records all 169 distinct column payoffs and checks the
Monster paths, weights and contact equalities. It rules out a useful gain
from further reweighting of this support. It does **not** constrain new
Princess paths, new time-dependent CDF transport, or a quantile coupling
that uses additional marginals.

## 2. The geometry is concentrated near two characteristic contact fronts

The seed has 125 distinct positive initial positions. Every positive path
stays strictly positive, and all are absorbed at \(+1\) by time 2. Its
initial stationary atom has mass \(0.045330635\) at each endpoint. The
conditional positive half-law has inward-moving mass \(0.79632761\) at
time \(1/4\); later it evacuates outward. Thus its structure includes
substantial inward travel followed by carefully placed outward departures.

There is a particularly informative test Monster:

\[
m_\uparrow(t)=\min\{1,-1+t\}.
\]

Against the original law, **every positive Princess is first captured at
time 2**. For a positive radial path \(r\), the two reflected capture
conditions are

\[
 t-r(t)=1\quad\text{and}\quad t+r(t)=1.
\]

These are precisely the outgoing and incoming characteristic fronts.
Before reaching the endpoint, every positive seed path has
\(t-r(t)<1\); the smallest outgoing lead is \(3/100000\).
The inward portions similarly distinguish being just short of
\(t+r(t)=1\) from lying exactly on it. A long shared segment on that
line is captured at its first equality, even if its duration is arbitrarily
small in a later perturbation.

The exact endpoint-sweep payoff is

\[
J(m_\uparrow)=
\frac{18145150023847037}{12800000000000000}
=1.4175898456130498\ldots,
\]

only about \(1.07\times10^{-8}\) above the certified worst response.
Thus these fronts occur in an almost active global constraint.

## 3. An exact mesh-collapse experiment

Round every time and position coordinate of every Princess vertex to the
nearest multiple of \(1/128\), using exact round-half-to-even, remove
repeated vertices, and retain the weights. In this particular input all
resulting paths are still legal, ordered and reflection symmetric.

The maximum uniform distance between any original path and its rounded
counterpart is exactly

\[
\max_i\sup_{t\ge0}|p_i(t)-\widehat p_i(t)|=\frac3{100000}.
\]

This is checked at the joint breakpoint set, which suffices for the
difference of two piecewise-affine paths. Nevertheless, the exhaustive
unrestricted response of the rounded law is

\[
\widehat L=\frac{3977106327}{3200000000}=1.2428457271875.
\]

The plain endpoint sweep attains this value, and independent direct
intersections verify it. The security loss is exactly

\[
L-\widehat L
=\frac{4473449157897097}{25600000000000000}
=0.1747441077303553515625.
\]

The endpoint-sweep loss has two distinct geometric sources:

| Part of the symmetric law | Original conditional mean capture | Rounded conditional mean capture | Loss in the total expected payoff |
| --- | ---: | ---: | ---: |
| Positive half: outgoing front | \(2\) | \(1.78102268\) | \(0.10948866\) |
| Negative half: incoming front | \(0.8351796912260995\ldots\) | \(0.704668774375\) | \(0.0652554584255497\ldots\) |

For the positive half, exactly \(0.21897732\) of the conditional mass
now reaches zero at time 1. The upward sweep captures it at time 1 instead
of time 2. For the negative half, \(0.61673595\) of the conditional mass
loses more than \(1/100\) in capture time when nearly shared inward
fronts become exact contact fronts.

This example rules out transferring the seed certificate by small uniform
path error or by simply deleting its microscopic offsets. It does not rule
out the existing characteristic-CDF approximation hierarchy: that hierarchy
uses CDF control and one-sided contact conventions, not a uniform path-error
claim. It also does not prove that arbitrarily fine snapping of this fixed
rational law fails; a mesh containing its exact vertices preserves it.

## 4. A global constraint on center atoms and outgoing-front mass

The following simple inequality applies to **every** legal Princess law;
it does not require symmetry, ordering, piecewise linearity, or finitely
many paths. Let the Monster choose with equal probability the two endpoint
sweeps \(m_\uparrow(t)=\min(1,-1+t)\) and
\(m_\downarrow(t)=\max(-1,1-t)\).

If a path has \(p(1)=r>0\), the descending sweep captures it no later
than \(1-r/2\): at that time, the Lipschitz bound gives
\(p(1-r/2)\ge r/2=m_\downarrow(1-r/2)\), while the sweep starts weakly
above the Princess. The ascending sweep captures by time 2. Reflection
handles \(r<0\). If \(r=0\), both sweeps capture by time 1.

Consequently, writing \(S(\mu)\) for the unrestricted security of a
Princess law \(\mu\),

\[
\boxed{S(\mu)\le
\frac32-\frac14\mathbb E_\mu|P(1)|
-\frac12\Pr_\mu\{P(1)=0\}.}
\]

In particular, a center atom of mass at least

\[
3-2L=\frac{2109700226102903}{12800000000000000}
=0.164820330164289296875
\]

already prevents a law from exceeding \(L\), even before using the
nonnegative moment penalty. The snapped law has center mass
\(0.21897732\); its full right-hand side is
\(34239665513/25600000000=1.3374869341015625<L\).
The direct sweep evaluation from Section 3 is still stronger.

There is a version along the entire outgoing light cone. For
\(1\le t\le2\), define

\[
h_t(r)=
\begin{cases}
(t+1)/2,& |r|\le t-1,\\
(t+5-|r|)/4,& |r|>t-1.
\end{cases}
\]

Then \(S(\mu)\le\mathbb E_\mu h_t(P(t))\). To prove it, a path at
\(r\) at time \(t\) is captured by the descending sweep by
\((t+1-r)/2\) whenever \(r\ge1-t\), and by the ascending sweep by
\((t+1+r)/2\) whenever \(r\le t-1\). These times are within
\([0,t]\), and the same Lipschitz/continuity argument applies. Inside
the cone both bounds apply; outside it the remaining sweep is bounded
by 2. At \(|r|=t-1\), the **inside** formula is required because
coincidence counts as capture.

This is the relevant design constraint: an exact atom on the outgoing
front pays a discontinuous capture penalty relative to a nearby path
outside the front. A successful continuous CDF must preserve the required
one-sided mass geometry while spreading initial atoms; being visually
close to the seed paths is insufficient.

## 5. Resulting research direction

The two exclusions are complementary. Reweighting the existing paths has
less than \(1.85\times10^{-8}\) available gain, while a naive simplification
of their geometry destroys a large portion of the certified value. Future
Princess construction needs new transport geometry with explicit strict
and closed traces on the inward and outward fronts, followed by the
all-Monster certificate. No statement here upgrades a finite Monster bank
to an unrestricted lower proof or claims that the exact game is solved.

## 6. Constructive initial-atom regression: 588 legal paths

A small explicit initial-atom spread gives a strictly stronger certificate,
although the gain is far too small to count as meaningful numerical closure.
Its purpose is to instantiate the structural lesson: new initial transport
can help, and it must respect the existing near-contact geometry.

Set \(\delta=1/128000000\). Every path of the 338-path source is initially
constant for longer than \(\delta\), and distinct positive initial atoms
are separated by more than \(2\delta\). For each positive interior initial
atom at \(x\), divide its mass equally between the two prefixes

\[
x-(\delta-t),\qquad x+(\delta-t),\qquad 0\le t\le\delta.
\]

For the initial atom at \(1\), use \(1-(\delta-t)\) and \(1\), again
with equal mass. Reflect this prescription for the negative half-law.
At time \(\delta\), each pair rejoins its original starting point.
For every later time, keep the source law's marginal distribution exactly.

Use the ordered quantile coupling of these marginals. This is concretely
realized by cutting the source rank intervals at the midpoint of each
initial atom. The lower half uses the lower prefix and the upper half uses
the upper prefix; after \(\delta\), ranks follow their original tails.
Paths stay ordered because initial groups remain separated and each group
coalesces at its original position before any source path moves. All
prefixes have speeds \(0\) or \(\pm1\). Multiplying the source weights
by two makes every split an integer split, with no numerical rounding.

The deterministic construction yields 294 reflected pairs, with positive
half-law weights totaling \(200000000\). Its exact unrestricted response is

\[
L_{588}=\frac{9072574958621987}{6400000000000000}
=1.41758983728468546875.
\]

The certified gain is

\[
L_{588}-L
=\frac{60590851}{25600000000000000}
=0.0000000023668301171875.
\]

The all-Monster capture-order search visits 68,164 states and terminates
without reaching its node cap. A separate rational polygon-intersection
calculation verifies the returned attaining Monster's payoff. Replay:

```sh
python packages/interval_princess_geometry/verify_prefix_split.py
python packages/interval_uniform_reduction/exact_response.py packages/interval_princess_geometry/prefix_split_princess.json
```

The first command reconstructs the fixture deterministically from the
338-path source, checks its identity, and runs the unrestricted search and
independent payoff check. Its optional `--write` regenerates the compact
fixture. `prefix_split_replay.json` records exact output and source hashes.

This remains a **finite atomic** Princess CDF. It is neither an attaining
continuous CDF nor a literal instance of any separately defined mixed-law
construction in the nonattainment theorem. Its retained role is a concrete
strict-improvement regression; the main new milestones of this note are
the fixed-support ceiling and the contact-sensitive obstruction.
