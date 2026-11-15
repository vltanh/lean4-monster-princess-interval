# Avoided center bounces and the distinction between a response face and a lower law

## Scope

This note gives an exact discontinuity for legal reflected princess laws, including
an all-monster lower proof. It also records a uniform attack on the particular
residual face of a rounded upper law. Neither construction is a matching lower
strategy for the interval game.

The two uses of epsilon are distinct. The elementary example below uses a radial
lift. An actual response-face realization must preserve its recorded one-sided
inverse labels. A radial lift of a limiting face path can change its initial
capture order and is not asserted to realize that face.

## 1. A sharp avoided-bounce example

Fix \(0<\tau<1\) and \(0<\varepsilon<1\). Choose the two paths
\[
 \pm p_\varepsilon(t),\qquad
 p_\varepsilon(t)=\min\{1,\varepsilon+(1-\varepsilon)|t-\tau|\}
\]
with equal probability. Put
\[
 a_\varepsilon=p_\varepsilon(0)
 =\varepsilon+(1-\varepsilon)\tau.
\]
Both paths are legal, remain strictly on their respective sides of the center,
and absorb at their endpoints at time \(1+\tau<2\).

Their unrestricted monster value is exactly
\[
 \boxed{V_\varepsilon=\frac{1+a_\varepsilon}{2}.}
\]

For the lower bound, write \(U(t)=t+p_\varepsilon(t)\) and
\(V(t)=t-p_\varepsilon(t)\). Speed at most one gives \(U(t)\ge a_\varepsilon\).
Before absorption, \(V(t)\le\tau<a_\varepsilon\). If a monster meets one sign at
\(t_1\) and then the other at \(t_2\), its speed bound gives
\(V(t_2)\ge U(t_1)\). Thus the second meeting is after absorption and
\(t_2-1\ge a_\varepsilon\). At least one of the two captures occurs no earlier than
\(1+a_\varepsilon\), so their average is at least the boxed quantity. Starting at
\(+a_\varepsilon\) and moving left attains it: the positive path is captured at
zero and the negative endpoint at \(1+a_\varepsilon\).

The literal limiting law \(p_0(t)=\min(1,|t-\tau|)\) has value \(\tau/2\).
Indeed the same light-coordinate comparison gives second capture time at least
\(\tau\), and the sweep from \(+\tau\) captures the two signs at zero and \(\tau\).
Consequently
\[
 \lim_{\varepsilon\downarrow0}V_\varepsilon
 =\frac{1+\tau}{2},\qquad V_0=\frac{\tau}{2}.
\]
The gap is exactly \(1/2\). This proof allows an arbitrary epsilon-dependent
monster; it is not a comparison against only fixed limiting routes. Its value
is at most one, so the example does not reach the current game target.

## 2. The effect does not require an initial atom

Let \(\tau\) have any atomless distribution supported on
\([\tau_0-\delta,\tau_0+\delta]\), and choose the sign independently and fairly.
Use the same path formula at each \(\tau\). Define
\(a_{\min}=\varepsilon+(1-\varepsilon)(\tau_0-\delta)\) and \(a_{\max}\)
analogously. If \(a_{\min}>\tau_0+\delta\), a monster cannot meet a positive
and a negative member of the family before \(1+a_{\min}\): the preceding
light-coordinate argument works for two different parameters. Therefore
\[
 V_{\varepsilon,\delta}\ge(1+a_{\min})/2.
\]
The sweep from \(a_{\max}\) catches every positive path before its inward turn
in at most \(2\delta/\varepsilon\), provided this is less than
\(\tau_0-\delta\). Every negative capture is at its endpoint by
\(1+a_{\max}\). Hence
\[
 V_{\varepsilon,\delta}\le(1+a_{\max})/2+\delta/\varepsilon.
\]
Taking \(\delta=o(\varepsilon)\), for example a sufficiently small constant
times \(\varepsilon^2\), gives the same limit \((1+\tau_0)/2\).
These are analytic bounds for the continuous family. The accompanying
three-parameter fixtures are checks of the calculation, not a replacement
for that argument.

## 3. What the concrete upper face does and does not imply

The exact upper certificate has two extremal residual cuts. Its face anatomy
is stored in blob
`61db8ab94e396c4bf5423e69e47e3aa64321d93a`; the strict warped upper certificate
is `07c65a9a017864c97a5433e0a721a682aadee96b`, using query coordinates and base
labels from `188b8b43fad7c69cafb42195d69d045cb44e8f23`.

Both residual cuts require isolated avoided center bounces at reference
\(5/8,11/16,3/4,13/16,7/8,15/16,2047/2048\).
A priced incoming trace requires \(\alpha(b)=b\) in the limit while a priced
outgoing trace requires \(\beta(b)>b\). A literal path through the center at
\(b\) cannot satisfy both first-contact requirements. This is a genuine
one-sided trace issue, not just a choice of interpolation between queries.

However, that exact residual face cannot itself support a useful lower law.
Let \(\psi\) be the certificate's common warp and put
\(A=\psi(15/32)\), \(X=\psi(1/2)\), \(T=\psi(5/8)\).
Direct extraction from the two exact extremal label arrays gives:

| Reference query \(V\) | Minimum label | Maximum label |
| --- | --- | --- |
| \(-1/2\) | \((0,0)\) | \((1/2,-)\) |
| \(-15/32\) | \((4823449/8388608,-)\) | the same |
| \(1/2\) | \((5/8,-)\) | the same |

The lattice envelope contains every residual maximum cut, so these priced
traces imply an initial radius at most \(X\),
\(\alpha(X)\le(X-A)/2\), and \(\beta(X)\le(X+T)/2\), in the limiting
one-sided sense. No assumption about canonical filling of unpriced intervals
is used. The straight-left monster from \(+X\) therefore has limiting pair
cost at most
\[
 \frac{2X+T-A}{4}
 =\frac{578124999999997}{2000000000000000}
 =0.2890624999999985.
\]
For the supplied actual epsilon realization, independent exact segment
intersection gives \(0.2890624999999976\). This attack occurs before the center
bounce sequence matters.

The certificate's atom weights were rounded. Its exact residual face can
therefore be much smaller than its nearly optimal response family. The right
input for a lower construction is the retained broad master-dual or
near-optimal family, including its trace labels and weights, not only these
two exact extremal profiles.

## 4. Symbolic realization and verification route

The existing `germ_response.py` works over \(\mathbb Q(\varepsilon)\), orders
comparisons at \(\varepsilon=0+\), and records a common positive rational
radius on which all branch decisions are valid. It reuses the finite ordered
capture-order theorem and independently checks the returned route by segment
intersection. A completed search certifies the supplied finite approaching
law only; a node-limited search does not.

Use its stored one-sided labels, epsilon-squared connectors, and strict
epsilon-sixth shrink for actual face data. Do not substitute a center-zero
CDF or assume that a uniform radial lift preserves an upper face's initial
contact labels.

The accompanying JavaScript verifier reuses the committed exact finite
response oracle. It completes fifteen pair searches (including literal
zero-epsilon limits), three six-path jitter fixtures, independently captures
the supplied three face profiles, and extracts the three trace gates from
the exact certificate arrays. It checks a finite model where applicable and
does not claim a minimax solution.
