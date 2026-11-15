# The narrow common-threshold interpolation loss can approach one half-step

Date: 2026-11-13.

There is an optimal \(n=1\) sticky/outward-after-two nodal dual profile,
with exact finite-bank value \(47/32\), whose common-threshold
interpolants have an explicit continuous Monster response of payoff

\[
 \frac{31}{32}+\frac{\varepsilon}{2},
 \qquad 0<\varepsilon\le\frac12.
\]

The loss from the finite value is

\[
 \boxed{\frac12-\frac{\varepsilon}{2}\longrightarrow\frac12.}
\]

Thus a universal \(1/(4n)\) transfer bound cannot hold for the entire
positive-width interpolation family. The limiting \(1/(2n)\) constant
in the existing construction cannot be improved for this profile as
the width tends to zero.

This example does **not** disprove a special \(1/(4n)\) theorem for
the full-width unbiased interpolation \(\varepsilon=1/2\), does not
give the field's exact global security, and does not establish
sharpness of the game-value enclosure \(U_n-V\). It concerns the
specified explicit Princess extraction from an optimal nodal dual.

## 1. A self-contained optimal \(n=1\) profile

Here \(h=1\), physical step \(\Delta=1/2\), and nodes have
\(t=j/2,r=k/2\), with \(0\le j\le16\), \(0\le k\le2\), and
\(j\equiv k\pmod2\).

The radial nodal profile is:

| Radius | Times | Value \(g(t,r)\) |
|---|---|---:|
| \(0\) | all integer times \(0,\ldots,8\) | \(0\) |
| \(1/2\) | \(t=1/2\) | \(7/8\) |
| \(1/2\) | \(t=3/2,5/2,\ldots,15/2\) | \(0\) |
| \(1\) | \(t=0,1,2\) | \(1\) |
| \(1\) | \(t=3,4,\ldots,8\) | \(0\) |

It satisfies every radial interval-containment inequality, the
nonincreasing endpoint-trace condition, and the outward-after-two
nodal identities. Its signed interior-trace value is

\[
 f(t,x)=\frac{1+\operatorname{sgn}(x)g(t,|x|)}2,
 \qquad f(t,0)=\frac12.
\]

For completeness, a physical upper certificate uses the following
two fair reflected Monster pairs:

* weight \(7/8\): start at \(+1\), move left directly to \(-1\);
* weight \(1/8\): start at zero, move to
  \((1/2,1/2)\), then to \((2,-1)\), then to \((4,+1)\).

In units of \(\Delta\), the first path's negative-endpoint clock
puts one selected unit at each node \(j=0,1,2,3\); its other clock
is initially inactive. The second path's negative-endpoint clock
puts three units at \(j=0\) and one at \(j=3\); its
positive-endpoint clock puts one unit at \(j=0\) and seven at
\(j=1\).

After fair reflection and weight normalization, all selected masses
are integer multiples of \(1/32\). Their total mass is \(40/32\),
positive pressure is \(14/32\), and a match of mass \(7/32\)
joins the positive and negative events of radius \(1/2\) at
time \(1/2\). Thus the upper objective is

\[
 \frac{40+14-7}{32}=\frac{47}{32}.
\]

The accompanying exact verifier independently enumerates every
unit-grid physical path through the full horizon, using both running
record prices. The minimum nodal plane for the displayed profile is
also \(47/32\). This gives an exact finite primal/dual certificate;
left-floor atomization identifies it with the true physical-bank
value \(U_1\).

## 2. The legal continuous Princess field

Fix \(0<\varepsilon\le1/2\), and put

\[
 b=\frac12-\varepsilon,\qquad
 a=\frac12+\varepsilon.
\]

Let \(Z\) be uniform on \((b,a)\). In every even unit-coordinate cell,
round at fractional threshold \(Z\); in every odd cell, round at
threshold \(1-Z\). Fix the integer knots and use reflected tie
conventions. The resulting map \(T_Z\) is nondecreasing, odd, and
period two.

Define the continuous interior CDF by the common-coordinate average

\[
 F_\varepsilon(t,x)=
 \mathbb E_Z f\!\left(T_Z(t+x),T_Z(t-x)\right),
\]

where \(f\) on the right is evaluated in light coordinates.
The nodal transport inequalities imply legality. The atom-free
threshold law makes this a continuous piecewise affine field with
no center atom. Reflection gives signed symmetry.

Because the nodal profile satisfies the normalized constraints,
the interpolated field is sticky and outward after time \(2\).
Its endpoint trace is one through time \(2\), so it has no endpoint
mass before that time. Its radial CDF at both time zero and time
two is the uniform CDF on \((b,a)\).

The common upper quantiles of this radial field, with an independent
fair sign, are the explicit Princess strategy. The strict CDF at
the negative endpoint is set to zero; elsewhere the continuous
interior trace has the usual interpretation.

## 3. The fast-sweep front integral

On the descending endpoint sweep, one light coordinate is \(U=1\).
At the five successive values \(W=-1,0,1,2,3\), its nodal signed
CDF values are

\[
 \left(1,\frac{15}{16},\frac12,\frac12,0\right).
\]

Inside a unit band of \(W\), the expected field interpolates the two
adjacent values. The threshold in either orientation has mean
\(1/2\). Hence the integral over that band is exactly the
trapezoidal average of its endpoint values, for every positive
\(\varepsilon\). Since \(dt=dW/2\), the complete fast-sweep payoff is

\[
 \begin{split}
 \int_0^2F_\varepsilon(t,1-t)\,dt
 &=
 \frac14\left(
 1+2\frac{15}{16}+2\frac12+2\frac12+0\right)\\
 &=\frac{39}{32}.
 \end{split}
\]

The field along a direct descending sweep is nonincreasing. All
Princesses start to its left, so this CDF is exactly the surviving
mass, not merely a clock upper plane.

## 4. An off-grid initial position gives the sharp limiting loss

Start the Monster at \(x=a\), then move left at speed one:

\[
 m(t)=a-t,\qquad 0\le t\le a+1.
\]

At time zero every Princess lies at or to its left, with equality
having probability zero. The sweep therefore catches every
Princess by its arrival at \(-1\); a subsequent sweep to \(+1\)
can be added to meet the physical endpoint-completion convention.

Along this attack, \(U=a\) is constant and \(W=2t-a\).
Since \(Z<a\) almost surely,

\[
 T_Z(a)=1.
\]

Thus the field on the attack is the same front function used in
Section 3, but integrated only over

\[
 -a\le W\le a+2.
\]

The omitted left interval is \([-1,-a]\). In the cell
\(W=-1+y\), its fractional coordinate satisfies \(0\le y\le b\).
The cell's threshold \(1-Z\) lies in \((b,a)\), so
\(T_Z(W)=-1\) almost surely and the field is identically one.
This omitted piece contributes

\[
 \frac{1-a}{2}=\frac14-\frac{\varepsilon}{2}.
\]

On the omitted right interval \([a+2,3]\), the fractional coordinate
in the cell \([2,3]\) is at least \(a\), so \(T_Z(W)=3\) almost
surely and the field is zero.

Consequently the exact attacking payoff is

\[
 \boxed{
 J_\varepsilon(m)
 =\frac{39}{32}
  -\left(\frac14-\frac{\varepsilon}{2}\right)
 =\frac{31}{32}+\frac{\varepsilon}{2}.}
\]

For example, \(\varepsilon=1/8\) gives the legal path

\[
 (0,5/8)\longrightarrow(13/8,-1)
 \longrightarrow(29/8,+1)
\]

with exact payoff \(33/32\), versus finite value \(47/32\).
Its loss \(7/16\) is strictly larger than \(1/4\).

The path visits zero before time \(2\), so the discrepancy is not
caused by the late-center class omitted by normalization.
It is also not caused by a defect in the atomic clock minimax:
the finite physical-bank value itself is exactly \(47/32\).
The continuous Monster is using an initial position absent from
the \(n=1\) bank.

## 5. Independent exact replay and remaining question

Run the standard-library verifier:

    python verify_sharp_interpolation_loss.py

It checks the physical primal calendars and matching, all nodal
transport and normalization conditions, and the full finite-bank
dual by exact record DP. It then evaluates the continuous field by
exact interval integration in the threshold parameter and verifies
the attacking-path integral for 90 rational widths.

The executed replay reports:

* 26 profile nodes and 83 cone comparisons;
* 16 physical clock prefix checks;
* 177 full-bank record states and 274 transitions;
* 1,966 exact affine integration pieces;
* 3,600 field identities.

The symbolic proof above covers every real width in \((0,1/2]\);
the rational replay checks the construction independently.

For full width \(\varepsilon=1/2\), this particular attack becomes
the endpoint sweep and its loss is exactly \(1/4\). Whether a
special full-width transfer theorem achieves that smaller constant
for arbitrary continuous Monster responses is a separate question.
Neither this example nor its replay settles it.

