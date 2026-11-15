# Microscopic connectors at isolated center bounces

## Scope

The inverse-label data of a finite upper response problem does not determine a
lower approaching law. This note gives two legal rational epsilon realizations
with the same priced trace data and different unrestricted response limits.
It also verifies the new connector on four controls from the actual 159-row
probability-master dual. The full 159-control lower feasibility problem remains
open; its finite-master value is not asserted to be its physical value.

The implementation extends, rather than replaces, the existing
\`germ_response.py\` and \`germ_response_v8.cjs\` conventions.

## 1. The minimum-fill pause

Let consecutive inverse queries have next coordinate \(V=b\). Suppose the
previous label is \(U=b-\varepsilon\) and the next label has limiting value
strictly greater than \(b\). The standard realizer places the outgoing jump
at \(V=b-\varepsilon^2\). Before that jump it follows the center diagonal
from \(U=V=b-\varepsilon\) to \(U=V=b-\varepsilon^2\).

After the standard strict radial shrink
\[
 p\longmapsto(1-2\eta)p+\eta,\qquad\eta=\varepsilon^6,
\]
this is a pause at radius \(\eta\), lasting
\(\varepsilon-\varepsilon^2\). A monster can traverse from \(+\eta\) to
\(-\eta\) during that pause. Strict positivity alone therefore does not make
this a robust avoided bounce.

This is a property of that interpolation, not a consequence of the priced
labels.

## 2. A legal avoided connector with the same labels

Instead place the jump at
\[
 V_{\rm jump}=b-2\varepsilon.
\]
The incoming characteristic remains \(U=b-\varepsilon\). Their junction has
\[
 t=b-\frac32\varepsilon,\qquad p=\frac{\varepsilon}{2}.
\]
The next query at \(V=b\) still receives its original target label.

The implementation uses the more general rule
\[
 V_{\rm jump}=\min\{v-\delta,\ U_{\rm previous}-\varepsilon\},
 \qquad
 \delta=\min\{\varepsilon^2,(v-v_{\rm previous})/3\},
\]
only when the previous label's limiting \(U\) equals \(v\) and the next
limiting \(U\) is greater than \(v\). It verifies
\(V_{\rm jump}>v_{\rm previous}\). Fixed positive query spacing guarantees
this for sufficiently small epsilon; the arithmetic records an explicit
common radius.

At each new junction, \(U-V\ge\varepsilon\). The old endpoint clipping
\(U\le V+2\) is retained. Both light coordinates are nondecreasing, so the
curve is legal. After the strict shrink the corner radius is at least
\[
 \frac{(1-2\eta)\varepsilon}{2}+\eta,
\]
and there is no inserted center pause at that isolated bounce.

If the previous limiting \(U\) is strictly less than \(v\), the limiting
center-wait interval is genuine. This implementation leaves it explicit;
it does not silently erase a macroscopic interval or change its priced
alpha inverses.

Every pre-shrink query has exactly its original first and last \(U\) value.
Nonzero label sides are also checked after the final shrink. A zero label
need not remain literal equality under the shrink, so the verifier records
and compares the entire post-shrink sign signature of the two realizations.
The actual tests below check the fixed physical payoffs as well.

## 3. A complete all-monster comparison

For \(0<\tau<1\), use queries
\[
 (-1,-\tau,\tau,\tau+2)
\]
and target labels
\[
 (0,0),\quad(\tau,-),\quad(\tau+2,-),\quad(\tau+4,-).
\]
Pair the realized positive path with its reflection. Put
\[
 \eta=\varepsilon^6,\qquad
 a=(1-2\eta)(\tau-\varepsilon)+\eta.
\]
For sufficiently small epsilon, the standard minimum-fill realization has
unrestricted value
\[
 V_{\rm fill}=(a+\eta)/2,
\]
whereas the avoided realization has
\[
 V_{\rm avoid}=(a+1-\eta)/2.
\]
Their difference is \(1/2-\eta\), and their limits are respectively
\(\tau/2\) and \((1+\tau)/2\).

These formulas follow directly from the two-path light-coordinate comparison.
Every first capture has \(U\ge a\). For the fill realization, \(p\ge\eta\)
implies the opposite capture is no earlier than \(a+\eta\); the long near-center
pause attains that time. For the avoided realization, \(V<a\) until the first
near-endpoint pause, where \(p=1-\eta\); the earliest opposite capture is
\(a+1-\eta\). Sweeping left from the positive initial position attains both
bounds. The later part of the queried paths is irrelevant to these attaining
tours.

The exact germ oracle independently completes all six searches at
\(\tau=1/4,1/2,3/4\), using eight vertices per positive path. All query traces
agree. This is an unrestricted adaptive-monster comparison, not just agreement
against a fixed finite bank.

## 4. Checks on the actual master dual

The actual input is
\`efficient_checkpoint.json\`, Git blob
\`6cac47a4b2227fa1469bb463d35ed37ffb3af1b6\`.
It has 159 retained princess controls, 408 inverse queries, and 1,086 physical
unit-route atoms. Its floating probability-master weights remain only
finite-bank information.

Rows 0, 79, 158, and the largest-weight row 85 were checked:

| Row | Original vertices | Avoided vertices | Isolated corners replaced |
| --- | ---: | ---: | ---: |
| 0 | 256 | 234 | 23 |
| 79 | 427 | 427 | 0 |
| 158 | 159 | 158 | 1 |
| 85 | 295 | 294 | 1 |

The checks include 3,264 pre-query first/last trace pairs, 2,010 nonzero
post-shrink sign checks, and 1,632 complete old/new post-sign comparisons.
The original-mode path agrees exactly with the existing realizer after
collinearity compression. All legal light-coordinate and speed conditions
pass. The common recorded radius is
\[
 0<\varepsilon<1/959999999999999998.
\]

For each of these four controls, all 1,086 physical monster-pair payoffs have
exactly the same limiting value under the two realizations: 4,344 comparisons
in total. The verifier uses exact first-hit ray times and running strict/closed
rank records. Equality of these fixed-bank limits does not imply equality of
the two adaptive response values; Section 3 proves the contrary in a small
complete example.

The reported forced-center intervals include virtual negative-time and late
extensions; their mere count is not a count of physical pre-two center waits.

## 5. Faster diagnostic variants

Setting \`shrink:false\` leaves legal unit/wait pieces and often turns capture
times into polynomials. It is a separate candidate, not an equivalent
implementation. Initial center contacts and side-zero labels can change:
a path starting literally at the center is caught there, while a positive
epsilon displacement may avoid that capture for a macroscopic time.

A common increasing light-coordinate warp cannot resolve this distinction,
because it preserves every contact and maps \(U=V\) to \(U'=V'\).
Pointwise clipping to a small positive radius is another possible
unit/wait realization, but it also needs its own trace and physical-response
audit.

## Reproduction

Run

\`\`\`sh
node packages/interval_global_closure/verify_avoided_realizer.mjs \
  efficient_checkpoint.json avoided_realizer_verification.json
\`\`\`

Add \`--skip-bank\` to omit the 4,344 fixed-bank payoff comparisons while
retaining the complete toy searches and actual legality/trace checks.
The inputs and rational function conventions are pinned by the source blobs
above. No node-limited run is presented as an all-monster certificate.
