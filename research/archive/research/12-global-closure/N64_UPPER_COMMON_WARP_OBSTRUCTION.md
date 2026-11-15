# An exact obstruction for common deformations of the retained n64 Monster law

## Statement and scope

Let `upper_n64_physical.json.gz` be the retained n64 Monster certificate, with
736 calendar plans, 703 distinct reflected physical path pairs, and fixed
probability denominator \(10^{12}\). Apply one common map to every path in
light coordinates:

\[
(U,V)\longmapsto(\psi(U),\psi(V)),\qquad
\psi(-s)=-\psi(s),\qquad \psi(s+2)=\psi(s)+2,
\]

where \(\psi\) is continuous and strictly increasing. The pair probabilities
remain fixed. For **every** such deformation, its worst Princess response is
at least

\[
c_{\rm warp}=
\frac{2850080016475247253999527}{2000000000000000000000000}
=1.4250400082376236269997635.
\tag{1}
\]

This is a lower bound on the best upper strategy available **inside this
specified family of Monster laws**. It is not a lower bound on the unrestricted
game value. It does not cover changing the Monster probabilities, adding
routes, or deforming different routes independently.

The retained n64 upper is
\(U=364842628535291/256000000000000\). Consequently this family can improve it
by at most

\[
U-c_{\rm warp}=
\frac{253018956713683500473}{2000000000000000000000000}
=0.0001265094783568417502365.
\tag{2}
\]

The independently retained n=128 law has since improved the unrestricted
upper to \(145925593551091/102400000000000\). Even relative to that newer
upper, no map in the present n=64 family can gain more than
\(29232569498839750473/(2\cdot10^{24})=0.0000146162847494198752365\).
That is less than 0.425 percent of the remaining unrestricted interval width.
The unrestricted bounds themselves are unchanged by this obstruction.

## Why arbitrary continuous warps reduce to finitely many coordinates

The coordinate change sends legal physical paths to legal physical paths
after the new time parametrization
\(t'=(\psi(U)+\psi(V))/2\). Both new coordinates are nondecreasing, so
\(|\Delta x'|\le\Delta t'\). Strict increase makes time strictly increasing;
periodicity makes it unbounded. Oddness preserves time zero and reflection,
and \(U\le V+2\) implies \(\psi(U)\le\psi(V)+2\), preserving the arena.

The change is a homeomorphism of the light-coordinate plane. It preserves
the intersection points of any two path traces and their chronological order.
Therefore it maps their first contact to the corresponding first contact,
including an initial equality. No differentiability or Lipschitz assumption
on \(\psi\) is needed.

Every Monster leg in this certificate is a unit-speed leg. Its light trace is
horizontal or vertical, and its image is the entire corresponding horizontal
or vertical segment between the image vertices. Thus the transformed physical
law depends only on \(\psi\) at the finitely many vertex coordinates. For the
present arrangement, folding by oddness and period two gives the knots

\[
r_k=k/64,\qquad 0\le k\le64.
\]

Set \(d_k=\psi(r_{k+1})-\psi(r_k)>0\). Then
\(\sum_{k=0}^{63}d_k=1\). A piecewise-linear map with the same knot values
gives the identical Monster law. The finite certificate consequently covers
all the continuous strictly increasing maps in the statement, not merely
piecewise-linear maps. An actually collapsed non-strict map is not asserted
to have the same first-contact behavior.

## Forty-one realizable response profiles

The certificate contains 41 legal ordered finite query profiles and positive
rational weights with sum one. Its arrangement has 209 query coordinates and
273 base levels. A label \(3k+\sigma+1\), with
\(\sigma\in\{-1,0,1\}\), specifies a queried U-coordinate
\(b_k+\sigma e\), subject to the physical strip bounds.

The independent verifier builds an actual radial path for each profile over
polynomial germs in \(e>0\):

1. Join successive queries by monotone light-coordinate segments, with the
   last U advance at V-distance \(e^2\) before the next query. Use the center
   and endpoint diagonals whenever the strip requires them.
2. Trim the negative-time portion and clip the radius to
   \([e^6,1-e^6]\). Clipping preserves the speed bound. All resulting pieces
   are unit-speed legs or stationary intervals.
3. Compute the first intersection with every oriented Monster route, in
   chronological Monster-leg order. Comparisons use the first nonzero
   polynomial coefficient and therefore hold for all sufficiently small
   positive \(e\).

The finite collection of comparisons has a common sufficiently small radius.
It defines actual legal Princess paths, rather than just formal labels. In
particular, side-zero entries, endpoint limits, and center limits are checked
by physical intersection; they are not assumed harmless.

All **57,646** oriented first captures
\((41\cdot703\cdot2)\) have exactly the coordinate limits claimed by the
certificate. There are no instances where only a weaker, later limit was
obtained. Applying any fixed \(\psi\) to each of these realizing sequences
preserves first contacts. Continuity of \(\psi\), followed by the finite
weighted sum, gives the corresponding limiting capture payoff. This justifies
using each profile as a lower bound on the worst response even when its
limiting unperturbed path would suffer an earlier coincidence.

## Exact finite certificate

Fold any capture coordinate \(q\) as

\[
\psi(q)=a+s\psi(r),\qquad
a\in2\mathbb Z,\quad s\in\{-1,1\},\quad r\in[0,1].
\]

Every folded limiting capture coordinate is a knot \(r_k\). For profile i,
the mean of the two reflected capture times, weighted by the Monster law,
therefore has the exact form

\[
J_i(\psi)=\sum_{k=0}^{63}
  \frac{N_{ik}}{4\cdot10^{12}}d_k,
\qquad N_{ik}\in\mathbb Z.
\tag{3}
\]

The factor four accounts for time \((U+V)/2\) and fair reflection. Constant
terms are absorbed using \(\sum_kd_k=1\). The verifier independently recovers
every integer \(N_{ik}\) from the chronological captures; it does not import
the discovery closure graph or its floating optimizer.

Let \(w_i/10^{12}\) be the saved positive Princess mixture weights. They sum
to one, and the verifier computes all 64 rational column coefficients

\[
C_k=\frac{\sum_iw_iN_{ik}}{4\cdot10^{24}}.
\]

Every \(C_k\ge c_{\rm warp}\), with equality at zero-based column 37.
Hence, for every admissible \(\psi\),

\[
\sup_p\mathbb E_{m\sim\nu_\psi}T(m,p)
\ \ge\ \sum_i\frac{w_i}{10^{12}}J_i(\psi)
\ =\ \sum_kC_kd_k
\ \ge\ c_{\rm warp}.
\]

This proves (1) without trusting any floating-point LP optimality claim.
The discovery LP was used only to find the finite profiles and mixture.

## Independent replay

Run from the repository root:

```sh
python packages/interval_global_closure/verify_common_warp_family.py \
  --physical-certificate packages/interval_clock_grid/upper_n64_physical.json.gz \
  --family-certificate packages/interval_global_closure/n64_upper_common_warp_obstruction.json.gz \
  --report /tmp/common_warp_family_replay.json
```

The verifier uses only Python's standard library and exact rational arithmetic.
It checks the source law's SHA-256
`2a09355539fa015a0b281843a9db108c4a619243118eb0d57d14144cab20d89a`,
all physical route and profile constraints, the polynomial-germ realizations,
every first capture, all feature integers, the probability normalization, and
the final minimum column. It does not certify a new unrestricted lower or
upper bound.

The [endpoint-gap calculation](BOUNDARY_LAYER_KERNEL_AND_GAP.md) identifies a
different obstruction for this same law. Together the two results direct the
next search toward changing the support or probabilities and attaching a
continuum endpoint layer to the bulk strategy.
