# Full-width common-threshold interpolation commutes with integer refinement

This is a fixed-field identity. It does not improve the universal transfer error, prove that a finite grid is optimal for the unrestricted game, or identify a continuous response with a grid response.

## 1. Statement

Let `n` be a positive integer and put `h=1/n`. Use light coordinates

\[
 U=t+x,\qquad W=t-x.
\]

Let `f` be a signed nodal field on the common light lattice `h Z × h Z`, restricted to the physical strip when appropriate. In a light-coordinate cell with integer index `k`, use the positive threshold orientation when `k mod 2n < n`, and the negative orientation otherwise. Equivalently, the orientation is positive on every interval `[2a,2a+1]` and negative on `[2a+1,2a+2]`. Endpoint conventions at knots have no effect on the interpolation.

Let `I_n f` be the full-width interpolation: sample one common `Z` uniformly from `[0,1]`, round each coordinate up when its fractional coordinate exceeds `Z` in a positive cell, or exceeds `1-Z` in a negative cell, and average the nodal field at the resulting lattice point.

If `m` is a positive integer, sample `I_n f` at the refined lattice with spacing `h/m`. Then

\[
 I_{mn}\bigl((I_n f)|_{(h/m)\mathbb Z^2}\bigr)=I_n f. \tag{1}
\]

The statement is pointwise on every region where the coarse nodal field is defined at the needed corners. In the Princess construction, it holds on the entire physical strip through the retained time horizon.

If the original radial profile belongs to `Qout`, the raw interpolated field is already symmetric, legal, sticky at its first endpoint, and maximally outward after time 2. The stopping and outward-normalization operations therefore introduce no additional pieces, so (1) applies to the final Princess law as well.

## 2. The exact local interpolation rule

Normalize a coarse light square to `[0,1]^2`, with coordinates `(u,w)`. For two positive orientations, the four corner probabilities are

\[
 p_{11}=\min(u,w),\quad p_{10}=(u-w)_+,\quad
 p_{01}=(w-u)_+,\quad p_{00}=1-\max(u,w).
\]

For two negative orientations the same probabilities result, by replacing `Z` with `1-Z` simultaneously. Thus the interpolation is affine on each side of the main diagonal `u=w`.

For opposite orientations, they are

\[
 p_{11}=(u+w-1)_+,\quad p_{00}=(1-u-w)_+,\quad
 p_{10}=\min(u,1-w),\quad p_{01}=\min(w,1-u).
\]

Thus the interpolation is affine on each side of the antidiagonal `u+w=1`. Reversing both orientation labels again leaves these probabilities unchanged.

Each formula is a convex combination of the four nodal values. It reproduces every affine function exactly, since each coordinate is rounded without bias. Independence of the two rounded coordinates is neither used nor true.

## 3. Refinement proof

Every fine cell lies inside one coarse cell and inherits its two orientation labels: the changes of orientation occur only at integer light coordinates, which are already coarse grid knots.

Suppose first that the coarse cell uses the main diagonal. Its diagonal can cross the interior of a fine cell only when that fine cell has equal local horizontal and vertical indices. In such a fine cell it is exactly the fine main diagonal. Every fine triangle is therefore contained in one of the two coarse triangles.

For an antidiagonal, an interior crossing occurs only for fine indices whose sum is `m-1`, and the crossing is exactly the fine antidiagonal. Again every fine triangle lies in one coarse affine piece.

On each fine triangle, the coarse field is affine. The fine interpolation has the same triangle type and agrees with that affine function at its three vertices. Hence it agrees throughout the triangle. The pieces agree on their common boundaries, proving (1).

This argument also covers coarse cells cut by the arena boundary, the center, or time zero: restrict the identity to the relevant part of the square. The center diagonal lies in a same-orientation cell. The time-2 diagonal lies in opposite-orientation cells except at grid vertices. These are already the diagonals selected above.

## 4. Relation to exact refined pricing

Suppose a validated `Qout` field on grid `n` is interpolated at full width and then sampled on grid `mn`. An exact normalized-bank oracle applied to the sampled profile computes a lower bound on the finite-bank dual for that same continuous field. Extracting the full-width Princess field again from the refined profile gives exactly the original field, not a second approximation.

In particular, any previously proved constructive transfer estimate can be used at the refined mesh size. If `c` is an exact lower bound on every refined atomic clock plane, the full-width extraction theorem gives security at least

\[
 c-\frac{3}{4mn}.
\]

The independent global value estimate remains

\[
 V\ge c-\frac{1}{2mn}.
\]

No estimate with `1/(4mn)` for arbitrary continuous Monster responses is asserted here. The trapezoidal record estimate gives that smaller error against physical **grid** responses; extending it to all responses requires a further argument.

Narrow-width re-extraction is generally a different field. The refined profile can still be used to construct such a new law, and its existing guarantee is

\[
 c-\frac{1}{2mn}-\frac{\varepsilon}{2mn}
 \qquad(0<\varepsilon\le1/2).
\]

## 5. Exact local regression

`verify_full_width_refinement.py` checks the complete local interpolation operator, not merely a few chosen nodal fields. It represents each value as its four rational coefficients on the coarse corner values. For all four orientation pairs and refinement factors 1 through 7, it compares direct coarse interpolation with fine interpolation of the sampled coefficients at a rational set covering every fine cell and both diagonal sides. It also verifies partition of unity and unbiased coordinate marginals.

The script includes a narrow-width countercheck: with threshold range `[1/4,3/4]`, coarse interpolation of the one-dimensional nodal values `0,1` is zero at `1/4`, while reinterpolating its values at `0,1/2,1` gives `1/4` there. Full width is therefore an essential hypothesis of (1).

The regression supports the finite affine calculation in Sections 2–3; the proof itself covers every point and every nodal field.
