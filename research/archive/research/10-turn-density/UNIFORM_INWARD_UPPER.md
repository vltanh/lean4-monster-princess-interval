# A controlled upper density with an initial inward turn

## 1. Actual monster law and normalization

For `0<a<1` and `-a<v<a`, let `I(a,v)` have vertices

    (0,a), ((a+v)/2,(a-v)/2), ((1+v)/2,(1-v)/2),
    (2,-1), (4,+1).                                    (1)

It first moves inward without reaching center, reverses outward to `U=1`,
and then visits both endpoints. Reflect this route with probability one
half. The additional, unnormalized monster density studied here is

    i(a,v)=h(a),       -a<v<a,                           (2)

where `h>=0`. Its total mass is

    M=integral_0^1 2a h(a)da.                           (3)

For step density `h_j` on `[d_j,d_(j+1)]`, this is the linear expression

    M=sum_j h_j (d_(j+1)^2-d_j^2).                     (4)

This is **additional mass**, not a replacement for an existing positive-M2
line. The complete upper law must include (4) in its normalization.
Replacing positive-M2 density instead requires subtracting that family's
score and mass explicitly. All scores below are four times unnormalized
expected capture time.

The formulas hold for arbitrary nonnegative 1-Lipschitz princess paths.
The existing absolute-value reduction for a symmetric monster law then
gives the unrestricted upper ceiling. No endpoint-by-two assumption is
imposed on the tested princess in this derivation.

## 2. Exact single-route first contacts

Let the positive princess start at `b` and write

    alpha(s)=inf{t:t+p(t)>=s},
    beta(v)=inf{t:t-p(t)>=v},
    psi(s)=2alpha(s)-s,     phi(v)=2beta(v)-v.

The reflected princess is first caught at `beta(1)`: the first two monster
legs remain positive, and the third has `U=1`. The positive princess is
caught as follows:

    if b<=a:
        alpha(a), if psi(a)<=v;
        alpha(1), otherwise;

    if b>a:
        beta(v), if phi(v)<=1;
        beta(3), otherwise.                            (5)

The route's symmetric expected cost is half the sum of this time and
`beta(1)`. All inequalities in (5) include equality. In particular, when
`b=a`, `alpha(a)=0` and `psi(a)=-a<=v`, so initial capture is retained.
The boundary `v=-a` is the positive-M2 route with no first inward leg.
The boundary `v=a` reaches center earlier and is outside (1).

For `b<a`, the positive path begins below the monster. If the first inward
leg misses it, the following outward leg cannot catch it; its first
remaining contact is on `U=1`. For `b>a`, the first inward leg cannot catch
the path. If the outward leg also misses, the path is caught on the final
`V=3` sweep. This proves (5) without smoothness or inverse-limit assumptions.

## 3. First-touch-safe inverse graph

Let `c` be the **last** `V` on the princess characteristic `U=1`:

    (1+c)/2 = sup{t:t+p(t)=1}.                          (6)

Since `p>=0` and `p<=1`, `-b<=c<=1`, and

    alpha(1)<=(1+c)/2,       beta(1)<=2,       beta(3)<=4. (7)

The inverse graph `U=phi(V)` on `-b<V<c` is nondecreasing and satisfies

    max(b,V)<=phi(V)<=1.                                (8)

Initial or intermediate outward unit segments can give jumps of this
inverse graph. Incoming unit segments give constant-U portions. A plateau
on `U=1` is included up to its last point; it is not replaced by the first
inverse `alpha(1)`.

For higher initial paths, the early-capture condition `phi(V)<=1` holds
exactly up to this cutoff `c`, apart from immaterial endpoint conventions
for a density in `V`. Replacing the three times in (7) by their upper
values raises the cost in (5). In the first case of (5), the replacement
of `alpha(1)` affects only paths missed by the first inward leg, whose
coefficient is nonnegative. Thus the construction is an upper relaxation
even at incoming atoms and at exact center contact at time one.

Define

    H(x)=integral_0^x h(a)da,
    M_<(b)=integral_0^b 2a h(a)da,   M_>(b)=M-M_<(b),
    j_b(V)=(H(b)-H(abs(V)))_+,
    w(V,c)=1+c-2V,
    D(b,c)=integral_max(b,c)^1 (a-1)(a-c)h(a)da.         (9)

The positive part in `j_b` is valid because `h>=0`. On the relevant graph,
`w>=0`.

The relaxed four-score is

    F_I(b,c,phi)=4M+(1+c)M_>(b)+8M_<(b)+D(b,c)
       +integral_-b^c q_I(b,c,V,phi(V))dV,              (10)

where

    q_I(b,c,V,U)
      =j_b(V)(V+U-8)
       -w(V,c)[H(U)-H(max(b,V))].                      (11)

For every princess path,

    4 J_I(p) <= F_I(b,c,phi).                           (12)

### Derivation of the alpha/beta cancellation

For initial monster radii `a<b`, integrate the early `beta(v)` term in (5)
first in `a`. Its density at `V` is exactly `j_b(V)`, producing the first
term in (11). The corresponding late baseline is `8M_<(b)`.

For `a>b`, the mass caught by the initial inward leg is
`(a-psi(a))h(a)`. Relative to the late baseline `(1+c)M_>(b)`, its
four-score correction is

    integral_b^1 (a+psi(a)-1-c)(a-psi(a))h(a)da.         (13)

For fixed `a`, set

    F(a,V)=(a+V-1-c)(a-V)_+ h(a).

Away from its harmless corner at `V=a`,

    partial_V F(a,V)=w(V,c)h(a) 1_(V<a).                (14)

Integrate (14) from `psi(a)` to `c`, then interchange the integrals. The
region `psi(a)<=V` is `a<=phi(V)` up to null boundary sets. This changes
(13) into

    D(b,c)-integral_-b^c w(V,c)
                        integral_max(b,V)^phi(V) h(a)da dV.

This proves (10)-(11). It also explains why uniform density in the first
turn characteristic is useful: the derivative (14) has no remaining `a`
factor.

### Exact amount of relaxation

The slack in (12) can itself be written exactly. Put

    Lmiss=integral_b^1 2alpha(a)h(a)da,
    Hmiss=integral_0^b (a-max(-a,c))_+ h(a)da.

Then

    F_I-4J_I
      =2M(2-beta(1))
       +2[(1+c)/2-alpha(1)] Lmiss
       +2(4-beta(3)) Hmiss.                            (15)

Every term is nonnegative. This distinguishes a valid upper ceiling from
an attained payoff for a path containing an exact first-touch plateau.

For a canonical prefix graph and a one-exit suffix, the envelope is
approached by the usual epsilon paths. Keep `U<1` until the selected
crossing, avoid a center contact at time one, and end on an outgoing
characteristic `y<1`. Then all three equalities in (7) hold. A concrete
standalone regularization scales the prefix `(U,V)` by `1-epsilon`, adds
an outward segment from `U=1-epsilon` to `U=1`, and maps the suffix to

    U_new=epsilon+(1-epsilon)U,
    V_new=(1-epsilon)V,

extending its last outward leg to the endpoint. For bounded step `h`,
dominated convergence gives (10). A joint upper law must still use its
established epsilon convention at any other fixed turn atoms; uniform I
adds only the requirements in (7).

## 4. Control by a nondecreasing density

The local derivative contributed by uniform I is particularly simple:

    partial_U q_I=j_b(V)-w(V,c)h(U).                   (16)

Suppose `h` is nondecreasing. For every legal `U>=max(b,V)`,

    j_b(V)<=(b-abs(V))_+ h(U).

Together with `c>=V` and `b<=1`, this gives

    partial_U q_I <=0.                                 (17)

Thus the added family does not spoil a pre-existing improvement obtained
by capping an overly large incoming inverse. In particular, the small
positive-M3 band can retain its cap at its fixed edge even though the
previously flat part of its score becomes decreasing.

On positive `V`, within a density cell,

    partial_V partial_U q_I
       =2h(U)-h(V)1_(V<b) >=0.                         (18)

This preserves the ordered first-crossing rule when added to a base
positive-prefix score with that property.

If the base negative-prefix derivative is `p(-V)-k(U)`, the new one is

    p(-V)+j_b(V)-k(U)-w(V,c)h(U).                       (19)

The special choice `h=lambda k` gives a weighted isotonic problem with
positive weight `1+lambda w`. It is not necessary to impose this tie:
independent nonnegative nondecreasing step heights for `h` give a broader
linear fitting class and retain (17)-(18).

For fixed step `k,h`, the score is affine in `U` between their knots and
the existing special edges. Therefore a maximizing inverse can choose
those knots and its boundary states. For two fixed states `U1,U2`, the new
score difference is

    j_b(V)(U1-U2)-w(V,c)[H(U1)-H(U2)],                  (20)

which is affine in `V` on each density cell. The common quadratic part of
the score cancels. Adding all pairwise crossing points to those cells gives
a finite ordered-switch arrangement for the negative-prefix dynamic
program. The complete score, rather than just its differences, must still
be integrated when evaluating the selected response.

## 5. Implementation and exact physical checks

`packages/interval_turn_sheet/uniform_inward.py` implements exact rational
mass, constants, graph integrands, derivatives, and piecewise-polynomial
integration. An inverse graph is a list of `(V,U)` vertices; vertical jumps
are allowed.

`uniform_inward_features.py` exports

    uniform_inward_feature_row(knots,b,c,segments)

with rows of `segments` equal to `(V_left,V_right,alpha,beta)`, meaning
`U(V)=alpha*V+beta`. It returns the linear four-score coefficients for the
step heights `h`. Vertical jumps contribute zero. The routine is compatible
with Numba and has a plain-Python fallback when Numba is absent. Its mass
coefficients are `knots[1:]**2-knots[:-1]**2`.

Run the independent audit with:

```sh
python packages/interval_turn_sheet/verify_uniform_inward.py
```

It passes 483 reported checks: 172 single-route first-contact identities,
16 complete two-dimensional density integrals, 247 rational affine capture
cells, 16 exact slack identities (15), and 16 comparisons with the fast
feature row. Six physical examples attain the feature exactly; ten retain
the explicitly measured ceiling slack. Physical density integration uses
direct segment intersections on rational polygons in `(a,v)`, not the
inverse-graph feature formula.

The density is an admissible additional upper-strategy component, with
global response control available through the stated prefix construction.
No optimized law using it, matching lower law, or exact game value is
claimed by these checks.
