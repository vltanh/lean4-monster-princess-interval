# Explicit Princess extraction from a feasible normalized dual

Research proof and implementation note, 2026-11-13.

The constructive extraction does not require an optimal finite-game solution
or a primal certificate. An exact feasible lower on every grid clock plane is
enough. This note records that specialization and its compact implementation.
It does not identify the exact value of the unrestricted game.

## 1. The feasible-dual theorem

Fix an integer `n >= 1`, put `h = 1/n`, and let `g` be a rational radial
nodal profile in the polytope `Qout` of
`NORMALIZED_GRID_BANK_PRICING.md`. In physical indices the nodes are

\[
t=\frac{j}{2n},\qquad r=\frac{k}{2n},\qquad
0\le k\le2n,\quad j\equiv k\pmod2.
\]

The profile is between zero and one, is zero at the center, is isotone under
radial light-interval containment, and satisfies the sticky endpoint and
outward-after-two constraints. Suppose exact normalized record pricing proves

\[
\min_{\alpha\text{ an admissible grid clock law}}R(\alpha,g)\ge c.
\tag{1}
\]

For `Qout`, the first-endpoint and time-two continuation results in
`NORMALIZED_GRID_BANK_PRICING.md` make this a lower on the full bounded grid
bank, not only its normalized subset. No assumption that `c` is the optimal
finite value is made.

For any rational `0 < epsilon <= 1/2`, the common-threshold construction in
`CONSTRUCTIVE_PRINCESS_GRID_DUAL.md` gives a legal symmetric ordered Princess
law whose security against every Monster is at least

\[
\boxed{c-\frac{1+\varepsilon}{2n}.}
\tag{2}
\]

Here is the precise change to that proof. Replace the optimal-profile lower
`U_n` in its equation (7) by (1). For a fixed continuous Monster, fix its
minimizing clocks before drawing the common threshold `Z`. Every repaired
and rounded clock plane is at least `c`. The symmetric initial clock buffer
has expected cost

\[
\mathbb E\,h\max(Z,1-Z)
=\frac{1+\varepsilon}{2n},
\qquad Z\sim\operatorname{Uniform}
\left[\frac12-\varepsilon,\frac12+\varepsilon\right].
\]

The same fixed-clock pushforward identity and nonnegative truncation argument
therefore prove (2) for the bounded continuous Monster class. The all-Monster
extension is unchanged. In particular `c <= U_n`, so the proposed lower is
at most `U_n - 1/(2n) <= V < 3/2`; the opposite uncaptured half handles a
Monster that has not reached the center by time two. Neither saddle-point
attainment nor an optimal primal solution enters this argument.

## 2. Exact strategy and the endpoint convention

Use the integer light-coordinate cell orientation

\[
\sigma(i)=+
\quad\text{when }0\le i\bmod 2n<n,
\qquad \sigma(i)=-\text{ otherwise}.
\]

For one common `Z`, use threshold `Z` in positive-orientation cells and
`1-Z` in negative-orientation cells. The resulting monotone odd period-two
rounding map `T_Z` fixes the lattice. On a rounded node define

\[
f_{j,k}=\frac{1+\operatorname{sgn}(k)g_{j,|k|}}2,
\qquad f_{j,0}=\frac12.
\]

The continuous interior trace is

\[
F_{\rm int}(t,x)
=\mathbb E_Z f\bigl(T_Z(t+x),T_Z(t-x)\bigr).
\tag{3}
\]

For each evaluation there are only two switching thresholds in `Z`.
Splitting its interval at those thresholds and adding rational interval
lengths evaluates (3) exactly.

Validated `Qout` constraints make additional endpoint stopping unnecessary.
At `x=1` the rounded endpoint time is `1 + T_Z(t-1)`, which is nondecreasing
in `t`; the nodal endpoint trace is nonincreasing along those times. The
interpolated endpoint trace is therefore already sticky. For `t >= 2`,
periodicity and oddness give `T_Z(4-L)=4-T_Z(L)`, where `L=t-r`. If `L >= 2`
the radial trace is zero. If `1 <= L < 2`, the nodal outward identity reduces
it to the time-two footpoint `2-L`. Consequently

\[
G(t,r)=
\begin{cases}
2F_{\rm int}(t,r)-1,&t\le2,\ 0\le r<1,\\
0,&t>2,\ r\le t-2,\\
G(2,r-t+2),&t>2,\ t-2<r<1,
\end{cases}
\qquad G(t,1)=1.
\tag{4}
\]

The jump at radius one is an endpoint atom. The signed **strict** CDF is
zero at `x=-1`, while at `x=1` it is the positive interior trace. The compact
evaluator preserves that distinction.

The strategy samples one rank `u` uniformly in `[0,1)` and one independent
fair sign `s`, both fixed for the entire path, then follows

\[
p(t)=s\,r(t,u),\qquad
r(t,u)=\inf\{a\in[0,1]:G(t,a)>u\}.
\tag{5}
\]

The threshold `Z` defines the averaged CDF; it is not an additional path
parameter sampled independently at each time. The common quantile rule (5)
is the actual Princess law. Its speed bound follows from the CDF transport
inequalities, and it is absorbed at an endpoint by time three.

The exact `radiusAt(t,u)` implementation inverts finitely many rational
affine pieces. For fixed `t <= 2`, the complete breakpoint list consists of
light-coordinate cell boundaries, points where a normalized coordinate is
`1/2-epsilon` or `1/2+epsilon`, and `r=k/(2n)`. The last family covers equality
of the two switching thresholds when their orientations agree. With opposite
orientations that equality depends only on time, so it introduces no extra
radius breakpoint. Binary search finds the first breakpoint whose CDF is
strictly greater than `u`, including the correct treatment of plateaus, and
rational linear inversion finishes the calculation. For `t > 2`, (5) is
`min(1,r(2,u)+t-2)`.

## 3. Compact representation and exact checks

`packages/interval_clock_grid/extract_normalized_princess.cjs` stores only
the `n(4n+1)` noncenter radial values at `j=0,...,4n`, as exact unsigned
32-bit integers with a common denominator. The values are in increasing
`j`, then increasing positive `k` of the matching parity. Its table index is

\[
j n+\left\lfloor\frac{k-1}{2}\right\rfloor.
\]

The getter uses center value zero. For `j > 4n`, it replaces `k` by
`k-j+4n` and `j` by `4n`, returning zero if that footpoint is nonpositive.
The footpoint has even parity, so it is an actual node of the time-two row.
This supplies the full profile through time eight without allocating it.

Loading the strategy checks the decoded byte length and checksum, every
stored value, every pre-two immediate cone inequality, and every pre-two
sticky endpoint inequality. Those constraints imply the same inequalities
for the outward extension. Loading an uncompressed full nodal input also
checks every post-two value against that extension before compression.

The `generate` command requires an exact pricing report whose input-file
SHA256, `n`, integer lower, objective denominator, and rational lower agree
with the source field. It validates and binds that report; it does not rerun
pricing. The `verify` command independently calls the BigInt target-bound
pricer on the source field and regenerates the strategy. Regeneration checks
literal decoded-buffer equality as well as the complete strategy metadata.
Different valid zlib streams containing the same exact nodes are accepted.

The `createEvaluator` API checks the law and guarantee arithmetic; a saved
claim about its security still requires the exact pricing replay. A positive
report produced by an arbitrary external program is not self-authenticating.

## 4. Commands

From the repository root, construct a strategy using an independently saved
pricing report:

```sh
node packages/interval_clock_grid/extract_normalized_princess.cjs generate \
  packages/interval_clock_grid/lower_n256_field.json \
  packages/interval_clock_grid/lower_n256_independent_replay.json \
  1/512 packages/interval_clock_grid/lower_n256_princess.json
```

Independently reprice the complete finite bank and regenerate the strategy:

```sh
node --max-old-space-size=8192 packages/interval_clock_grid/extract_normalized_princess.cjs verify \
  packages/interval_clock_grid/lower_n256_field.json \
  packages/interval_clock_grid/lower_n256_princess.json
```

The large replay is intentionally separate from cheap exact evaluation:

```sh
node packages/interval_clock_grid/extract_normalized_princess.cjs cdf \
  packages/interval_clock_grid/lower_n256_princess.json 1/2 1/3
node packages/interval_clock_grid/extract_normalized_princess.cjs radius \
  packages/interval_clock_grid/lower_n256_princess.json 1/2 3/4
node packages/interval_clock_grid/test_normalized_princess.cjs
```

Source fields and strategy files may be gzip-compressed. The source hash is
the SHA256 of the exact input file bytes, so a report for the JSON file must
be used with that JSON file; a separate gzip byte stream has a different
input hash.

## 5. Concrete arithmetic and regression scope

For the n256 feasible dual with

\[
c=\frac{583091421641}{409600000000},\qquad
\varepsilon=\frac1{512},
\]

the explicit security given by (2) is

\[
\begin{aligned}
c-\frac1{512}-\frac1{262144}
&=\frac{582289859141}{409600000000}\\
&=1.42160610141845703125.
\end{aligned}
\]

Its compact input has SHA256
`81483589b60c14d823d2bb467015a321d77cf555076fe8d69a36d63cd829d7d5`.
There are 262,400 stored values, occupying 1,049,600 decoded bytes;
validation checks 523,264 cone inequalities and 512 endpoint inequalities.
The security statement uses the exact target-bound pricing report for this
input, not the decimal approximation and not finite optimality.

The standalone exact regression covers a constant endpoint law, a stationary
radial uniform mixture with an endpoint atom, and a nonoptimal native n6
profile. Eight extractions at full and narrow interpolation widths pass
4,172 exact-node recoveries, 7,052 comparisons with the existing expanded
CDF evaluator, 1,384 fixed-time affine-piece checks, 3,196 symmetry checks,
6,064 transport checks, 540 outward checks, 820 exact quantile inversions,
780 quantile speed checks, and 37 malformed-input rejections. Each extraction
also regenerates after independent BigInt target-bound pricing.

These finite regressions validate the implementation. The continuous
legality and all-Monster security assertions follow from the mathematical
extraction and normalization proofs; they are not inferred from sampling.
