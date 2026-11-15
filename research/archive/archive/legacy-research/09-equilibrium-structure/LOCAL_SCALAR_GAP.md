# An exact local exclusion for the rationalized signed-density candidate

This note supplies the finite scalar obligation in section 6 of
[`NEGATIVE_M2_SHIFT.md`](NEGATIVE_M2_SHIFT.md). It proves that one explicit
signed M1/M2 law is strictly improvable against **all** princess paths.
It does not identify the game value or claim an equilibrium.

The inputs and a standard-library-only rational checker are
[`local_gap_certificate.json`](../../packages/interval_signed_densities/local_gap_certificate.json)
and [`verify_local_gap.py`](../../packages/interval_signed_densities/verify_local_gap.py).
Run from the repository root:

```sh
python -B packages/interval_signed_densities/verify_local_gap.py
```

## 1. A fixed exact monster law

Round each density and the endpoint mass in `discovery.json` to the
nearest multiple of `1/1000000`, then normalize the entire law by one
common factor. The following integers, multiplied by `64/64000047`,
are the resulting densities. The endpoint mass is
`w0 = 42164416/64000047`.

| Interval | f | g | h | ell |
| --- | ---: | ---: | ---: | ---: |
| [0, 1/8] | 0 | 0 | 0 | 0 |
| [1/8, 1/4] | 0 | 130914 | 68785 | 0 |
| [1/4, 3/8] | 0 | 176271 | 92091 | 0 |
| [3/8, 1/2] | 0 | 181702 | 92091 | 0 |
| [1/2, 5/8] | 100362 | 81340 | 103225 | 0 |
| [5/8, 3/4] | 114123 | 80958 | 106153 | 0 |
| [3/4, 7/8] | 131539 | 81221 | 110668 | 0 |
| [7/8, 15/16] | 181542 | 81151 | 110356 | 11651 |
| [15/16, 31/32] | 1256903 | 74975 | 0 | 386184 |
| [31/32, 63/64] | 1311840 | 79865 | 0 | 386184 |
| [63/64, 1] | 1403706 | 81384 | 0 | 386184 |

Values on the finitely many interval endpoints do not affect the law.
All coefficients are nonnegative. The density sums integrate to
`1-w0`, and `f`, `f+g`, and `h+ell` are nondecreasing. In particular,
rounding did not destroy any of the hypotheses of the global scalar
response theorem. The checker verifies these facts using fractions.

Write `K(a,u,c,y)` for the continuous **limiting scalar payoff** in
[`SIGNED_M1_FUNCTIONAL.md`](SIGNED_M1_FUNCTIONAL.md), on the closed domain

    0 <= a <= u <= 1,       -a <= c <= y <= 1.

This includes one-sided payoff limits at endpoint or capture-coincidence
parameters; it does not silently substitute a smaller exact-boundary
path payoff. Let `S` be the supremum response to this fixed monster law.
The global response theorem identifies `S` with the supremum of `K`.
The argument below does not compute `S`.

## 2. The exact local gap

Set

    l = 31/32,     r = 63/64,     I = [l,r],
    lambda = 1/16.

The legal scalar tuple `(l,l,3/4,15/16)` gives the comparison value

    W = 631234171/442811136 <= S.

The exact maxima on the two closed bad regions are:

| Additional restriction, with a in I | Exact maximum of K | One maximizing tuple (a,u,c,y) |
| --- | --- | --- |
| c <= 0 | 543669789287969/381780248369664 | (63/64,63/64,-1/2,329021/372832) |
| y-c <= 1/16 | 7782693893/5461337344 | (31/32,31/32,7/8,15/16) |

The second maximum is larger. Write it as `B`. Then

    W-B = 947831/2048001504 > 0.

Consequently the rational threshold

    d0 = 947831/4096003008

has the required property: if `a in I` and `K >= S-d0`, then

    c > 0,       y-c > 1/16,       c < 15/16.

Indeed `S-d0 >= W-d0 > B`. Thus the local theorem can use
`kappa=lambda=1/16`, including all one-sided boundary limits.

## 3. Why the finite calculation covers every tuple

### First eliminate u

Put `k=h+ell`. It is constant throughout `[l,1]`. For fixed `a,c,y`
with `a in I`, the derivatives in `SIGNED_M1_FUNCTIONAL.md` show that
`K` is affine in `u` on `[a,1]`.

For `c<0` this follows directly from the formula for `K_u`, since its
only dependence on `u` is through `k(u)`. For `c>=0`, write
`v=min(u,c)`. The expression `K0(v)-v*k(u)` is constant when `v=u`,
because then `u>=l`; it is independent of `u` when `v=c`. The expressions
agree at `u=c`. Therefore only `u=a` and `u=1` need be considered.

### Then eliminate a except on one feasibility boundary

The four densities are constant on the interior of `I`. For fixed
`c,y`, the second derivatives of the two endpoint functions are

    4 d^2 K(a,1,c,y)/da^2 = -g+h+3ell > 0,
    4 d^2 K(a,a,c,y)/da^2 = 2f+g-h+ell > 0.

The formulas remain valid across `a=c`, because `k` is constant on
the whole terminal interval. The functions and their first derivatives
match there. At the two endpoints of `I`, use continuity of `K`.

The feasible `a` interval, with `c,y` held fixed, is
`[max(l,-c),r]`. Convexity therefore leaves these five two-dimensional
slices:

* `a=l,u=l`, with `-l<=c<=y<=1`;
* `a=l,u=1`, with `-l<=c<=y<=1`;
* `a=r,u=r`, with `-r<=c<=y<=1`;
* `a=r,u=1`, with `-r<=c<=y<=1`;
* `a=-c,u=1`, with `-r<=c<=-l` and `c<=y<=1`.

At `c=-a`, the derivative `K_u` is identically zero, so the last slice
also covers its `u=a` version. Both bad-region restrictions depend only
on `c,y`, so these maximizations preserve the restrictions.

### Exact quadratic maximization on closed polygons

On each slice, split `c` and `y` at every signed density knot; add `c=u`
as a split when `u` is fixed. The limiting capture integrals give a
polynomial of total degree at most two on each resulting rectangle:
integrating a constant density against an affine capture time gives a
quadratic expression with affine endpoints. On the moving slice
`a=-c`, the initial coordinate stays within one density bin.

Intersect the rectangles with `c<=y`, and then with either `c<=0` or
`y-c<=1/16`. Every intersection is a closed rational polygon, possibly
a segment or a point. The checker retains these degenerate cells.

For each nondegenerate cell it reconstructs the quadratic from its
values at six rational points on an inscribed triangle. These values
are calculated from the exact integral formula, using fraction
arithmetic. Polynomial degree follows from the preceding integral
argument; an additional centroid check detects implementation mistakes
in choosing the cells or recovering the coefficients.

A quadratic on a compact polygon attains its maximum at a vertex, an
edge stationary point, or an interior stationary point. The latter is
obtained by a rational linear system. If the stationary Hessian is
singular and an interior maximum exists, the same value extends along
a null direction to the boundary, so the edge checks suffice. Segments
are checked by their two endpoints and their one-variable stationary
point; points are evaluated directly.

This proves both maxima above. The calculation visits 678 closed
negative-c cells and 268 closed short-suffix cells. It uses no numerical
optimization and no parameter sampling as an upper-bound argument.

The separate `verify_local_capture.py` checker obtains the reference and
both maximizing payoffs from actual legal epsilon paths and direct segment
intersections, integrated exactly over this law's continuous densities.
Five exact one-sided limits agree with the scalar functional, including
additional central-wait and negative-suffix cases. This checks the capture
integral implementation independently of the quadratic maximizer; the
finite reductions above supply the exhaustive inequality.

## 4. Explicit constants for the arbitrary-path exclusion

Take the left half

    J = [31/32,125/128],
    d = 1/128,
    w = integral_J f = 218640/21333349.

The initial-mass forcing constant in `NEGATIVE_M2_SHIFT.md` is

    rho_star = d/(6+d) = 1/769.

The required positive suffix score is

    m = ess_inf_[l,1] f - ess_sup_[0,1] ell
      = 19747328/21333349 > 0.

The remaining exact density constants are

    H(1) = 1675176/21333349,
    ||h||_infinity = 7082752/64000047.

With `D=d/2`, `E=3+D`, `L0=w0*lambda/7` and
`omega=L0/(2E)`, choose

    eta = 1/65536.

The checker verifies `eta<1-r` and `eta*H(1)<omega*D`. The coefficient
from the explicit mixture theorem is

    Cstar = max(4/7+4||h||_infinity/(m*eta), L0/d0, 2omega/w)
          = 25385045996/809949.

Use the following unnormalized weights, with total `Z=1+Cstar/2`:

| Law | Coefficient |
| --- | --- |
| M | Cstar/2-omega/w |
| M_rest | omega(1-w)/w |
| F_r | omega |
| M_eta | 1 |

Here `M_rest` removes the positive-M1 submixture on `J` from `M` and
renormalizes, `F_r` is the symmetric M1 pair starting at `r`, and
`M_eta` shifts the negative-M2 turn characteristic from `1` to
`1+eta`, as defined in `NEGATIVE_M2_SHIFT.md`. All coefficients are
nonnegative, and the checker prints their exact normalized values.

The arbitrary-path theorem gives this explicit mixture response ceiling

    S - 285894191351167/1705889882370552363474944,

strictly below the original law's response supremum `S`. The decrease
is not an estimate of the distance to the game value. Its role is to
certify that this rational signed M1/M2 candidate cannot be an optimal
monster strategy, even though no-extra scalar responses remain active
at other initial positions.
