# A full-width counterexample to the universal `1/(4n)` transfer claim

The full-width common-threshold interpolation does **not** satisfy

\[
 \operatorname{security}(F)\ge c-\frac1{4n}
 \tag{1}
\]

for every feasible `Qout` nodal profile whose exact grid-clock price is `c`.

The counterexample below has `n=2`, a profile with denominator 49, an exact grid lower `c=429/392`, and a legal one-turn attack of cost `3039/3136`. Consequently

\[
 c-J=\frac{393}{3136}
     =\frac18+\frac1{3136}
     >\frac1{4n}.
\]

This does not refute the existing `1/(2n)` game-value transfer or the constructive randomized-interpolation estimate. It also does not exclude a strengthening that uses additional optimality or slack properties of a particular nodal profile. The profile here is feasible, and is **not** claimed to maximize the finite-grid dual.

## 1. Complete rational profile

The physical nodal coordinates are `(t,r)=(j/4,k/4)`, with `j+k` even. Let `g(t,r)` be the radial interior CDF at these nodes. It is zero at the center. Its complete pre-time-2 values are:

| Integer time `j` | First radial node and value | Second radial node and value |
|---:|---|---|
| 0 | `r=1/2`, `g=2/7` | `r=1`, `g=1` |
| 1 | `r=1/4`, `g=12/49` | `r=3/4`, `g=1` |
| 2 | `r=1/2`, `g=1` | `r=1`, `g=1` |
| 3 | `r=1/4`, `g=48/49` | `r=3/4`, `g=1` |
| 4 | `r=1/2`, `g=48/49` | `r=1`, `g=1` |
| 5 | `r=1/4`, `g=0` | `r=3/4`, `g=48/49` |
| 6 | `r=1/2`, `g=0` | `r=1`, `g=1` |
| 7 | `r=1/4`, `g=0` | `r=3/4`, `g=1` |
| 8 | `r=1/2`, `g=0` | `r=1`, `g=1` |

For `j>8`, extend by the outward rule

\[
 g_{j,k}=\begin{cases}
 g_{8,k-j+8},&k-j+8>0,\\
 0,&k-j+8\le0.
 \end{cases}
\]

Every radial value lies in `[0,1]`; every interval-containment inequality holds; the endpoint interior trace is nonincreasing; and the outward-after-two identities hold. The standalone verifier checks all 558 containment comparisons among the 83 radial nodes through time 8, in addition to these explicit normalization conditions.

## 2. The legal full-width field

Use the common light-coordinate grid of spacing `h=1/2`. On each light cell, round with one common `Z` uniform on `[0,1]`, with positive threshold orientation on `[2a,2a+1]` and negative orientation on `[2a+1,2a+2]`. Apply the same map to `U=t+x` and `W=t-x`, and average the signed nodal interior CDF

\[
 f(t,x)=\frac{1+\operatorname{sgn}(x)g(t,|x|)}2.
\]

This is exactly the full-width construction in `CONSTRUCTIVE_PRINCESS_GRID_DUAL.md`. The nodal order gives the transport inequalities. The atom-free threshold distribution gives continuity through the interior and to the endpoint traces, including center trace `1/2`. Thus the resulting field is a legal symmetric ordered Princess law with no center atom. Since the profile belongs to `Qout`, the raw interpolation is already sticky and outward after time 2; no further stopping or forcing changes it.

## 3. Exact grid-clock minimum

The atomic grid-clock price of this profile is

\[
 c=\frac{429}{392}.
\]

Here is a fully finite way to verify the assertion. Work in integer positions `k=-4,...,4`, integer times `j=0,...,32`, and integer signed prices

\[
 P(j,k)=49+\operatorname{sgn}(k)\,49g_{j,|k|}.
\]

Initialize all five legal starts `k=-4,-2,0,2,4`. Keep a state consisting of current position, the two endpoint-visited flags, the center-visited flag, and the two surviving running minimum prices. At each time, update an active minimum with the current signed price, add both active minima to the accumulated integer cost, and take each legal unit move. Require a center visit by integer time 8 and both endpoints by time 32. For an identical state, retain the smallest accumulated cost.

This enumerates every physical lattice walk in the full bank and its exact optimal atomic calendar. The minimum terminal integer cost is 429, and the physical normalization is `4nD=392`. The replay uses 2,499 states and 4,606 transitions. It neither prunes with an unproved bound nor calls a numerical optimizer.

An independent run of `normalized_record_pricing.cjs`, with both Pareto and pursuit pruning disabled, gives the same `429/392` and an attaining calendar. The complete radial field for this replay is `fullwidth_counterexample_field.json`; its output is `fullwidth_counterexample_independent_pricer.json`.

## 4. A strictly cheaper continuous attack

Take the legal physical path

\[
 (0,1/4)\longrightarrow(5/8,-3/8)
 \longrightarrow(2,1)\longrightarrow(4,-1).
\]

It visits the center by time `1/4`, reaches its first endpoint at time 2, and then uses the direct opposite sweep. Its initial position is not a legal start of the `n=2` bank.

Write `Y(t)=F(t,m(t))` for the signed interior CDF along this path, and let

\[
 L(t)=\min_{s\le t}Y(s),\qquad
 R(t)=\min_{s\le t}(1-Y(s)),
\]

with the corresponding record set to zero at its own endpoint. The expected capture time is the integral of `L+R`.

On the first descending leg, `Y` is affine between the following values:

| Time | `Y(t)` |
|---:|---:|
| 0 | `4/7` |
| `1/8` | `55/98` |
| `1/4` | `1/2` |
| `3/8` | `43/98` |
| `1/2` | `19/98` |
| `5/8` | `1/196` |

It is nonincreasing there, so `L=Y`. After the turn, `L` remains `1/196` until the negative endpoint at time 4. Trapezoidal integration gives

\[
 \int_0^{5/8}Y(t)\,dt=\frac{111}{448},
 \qquad
 \int_0^4L(t)\,dt
 =\frac{111}{448}+\frac{4-5/8}{196}
 =\frac{831}{3136}.
\]

The right record initially equals `3/7`. It stays there until `43/28`. On `[3/2,7/4]`, the field grows affinely from `1/2` to 1, so after the crossing at `43/28` the right record decreases with slope `-2` to zero at `7/4`. Hence

\[
 \int_0^4R(t)\,dt
 =\frac37\frac{43}{28}
  +\frac12\frac37\left(\frac74-\frac{43}{28}\right)
 =\frac{69}{98}.
\]

Therefore

\[
 J=\frac{831}{3136}+\frac{69}{98}
   =\frac{3039}{3136}
   <\frac{3040}{3136}
   =\frac{429}{392}-\frac18.
\]

The standalone verifier separately reconstructs the field by exact threshold integration, checks every affine piece, and integrates the running records including their interior crossings. Its result is the same fraction above. It does not assume that this attack is the field's globally best response.

## 5. What remains valid

For a physical **grid** path, each leg sees an affine field. Its running record is concave on that leg, so the continuous integral dominates its trapezoid. The resulting telescoping estimate bounds left-node overcharging by `h/4` after the fair-sign normalization.

The path in Section 4 is outside that bank. This counterexample isolates why the grid-path estimate alone does not prove (1). A useful stronger transfer theorem would need an additional argument or finite conditions controlling off-grid starts and turns; a record telescoping estimate along grid legs is insufficient.
