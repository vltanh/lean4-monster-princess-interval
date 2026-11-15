# A localized initial-inward triangle tied to a density ramp

## 1. The added basis direction

Fix `d>r`, where `r=1/4` is the first-turn floor of the existing small-start
signed-M3 attachment. The intended first construction uses `d=7/8`, at the
existing outer negative-start boundary. Add the initial-inward density

    i(a,v)=eta 1_(d<a<1, -a<v<-d),                     (1)

using the routes `I(a,v)` in `UNIFORM_INWARD_UPPER.md`. Simultaneously add

    k_ramp(U)=ell_ramp(U)=eta(U-d)_+.                   (2)

The ramp is inserted into the **complete existing density construction**:
its signed-M3 and early-M2 redistributions and the corresponding line
subtractions must all be included. It is not enough to add the bare
negative-M1 density and leave the calibrated sheets unchanged.

The I triangle has mass `eta(1-d)^2/2`. The complete ramp direction adds
the same total mass through `k`; `ell` is already part of that marginal
and must not be counted again. Therefore the combined normalization column
is

    eta(1-d)^2.                                        (3)

Some induced line-density changes are negative. This is an affine strategy
parameter direction, not a separately nonnegative old-law component.
Admissibility of the resulting complete law requires the usual residual
line inequalities. The new I density itself is nonnegative when `eta>=0`.

## 2. Exact I-only frozen feature

Use princess initial position `b`, the last `U=1` characteristic `c`, and
the inverse graph `U=phi(V)` from the uniform-I note. Work first at unit
amplitude. Put

    M=(1-d)^2/2,       m=(b-d)_+^2/2.

The first-touch-safe four-score of the I component is

    F_T=4M+(1+c)(M-m)+8m
        -(-d-c)_+(1-b)^2/2
        +integral_-b^min(c,-d) q_T(b,c,V,phi(V))dV,     (4)

where the integral is zero for `b<=d`, and

    q_T(b,c,V,U)
      =(b+V)(V+U-8)
       -(1+c-d-2V)(U-b)+(U^2-b^2)/2.                  (5)

Outside `V<-d`, this additional local score is zero. The feature is an
upper ceiling for every princess path, and its slack consists of exactly
the same three nonnegative first-touch relaxations as in the uniform-I
case: `beta(1)<=2`, `beta(3)<=4`, and
`alpha(1)<=(1+c)/2`.

To derive (4), for `a<b` the redistributed beta-threshold density is

    j_b(V)=(b+V)1_(-b<V<-d).

For `a>b`, the first-inward tail mass is `(-d-psi(a))_+`. Its correction
has derivative in `V`

    (-d-V)+(1+c-a-V)=1+c-d-a-2V

on `V<-d`. Integrating in `a` from `b` to `U` gives (5); evaluating the
boundary term at `V=c` gives the negative term in (4). If `b<=d`, every I
start lies above the princess and the first inward turn misses; the whole
feature reduces to `M(5+c)`, with no dependence on the inverse graph.

For a frozen affine graph segment, (5) is a quadratic polynomial in `V`.
Its integral is exact by Simpson's rule, after cutting at `V=-d`. No new
density coordinates or numerical princess ranks are introduced.

## 3. Cancellation and complete negative-prefix control

Let the original monotone negative marginal be `k0`, so that the new one
is `k=k0+eta(U-d)_+`. Denote the small signed-M3 start-band edge by `bP=1/8`.
For `b>d`, every allowed negative-prefix inverse has `U>=b>d>r`; hence all
small-M3 starts lie below the initial princess rank.

On the localized band,

    partial_U q_T=U+b+d+3V-1-c.                        (6)

The ramp contributes `-eta(U-d)` to the old negative-prefix derivative.
Thus the `U` terms cancel exactly. The complete derivative is

    V<-d:
        p(-V)-k0(U)+eta[b+2d+3V-1-c];

    -d<V<-bP:
        p(-V)-k0(U)-eta(U-d);

    -bP<V<=0:
        0.                                             (7)

The last line uses the actual calibrated signed-M3 flat band. It must not
be replaced by the uncalibrated expression `p-k`. Every expression in (7)
is nonincreasing in `U`. No monotonicity assumption on `p=f+g` is needed.

### Nested tail maximizers

Fix the four outer response parameters, including the common bound `u`
between the negative and positive inverse portions. On
`V in [-b,min(c,0)]`, write the local score by layer cake:

    q(V,phi(V))=q(V,b)
       +integral_b^u partial_U q(V,s) 1_(phi(V)>=s)ds.  (8)

For a nondecreasing inverse, each superlevel set is a tail interval
`[t(s),min(c,0)]`. For fixed `s`, maximize its tail gain

    T_s(t)=integral_t^min(c,0) partial_U q(V,s)dV.        (9)

Since the derivative in (7) is nonincreasing in `s`, `T_s(t)` has
increasing differences in `(s,t)`. Its smallest maximizing threshold is
nondecreasing in `s`. Indeed, if smaller `s` chose a strictly larger
smallest maximizer, the cross inequality and the two optimality
inequalities would make the smaller threshold optimal for both, a
contradiction. Consequently the independently optimal tails nest and
define a legal inverse. Integrating their gains in (8) attains the global
negative-prefix maximum.

This argument is also the pointwise increasing-differences theorem in the
inverse representation `V=psi(U)`. It adds no outer response scalar.

### Finite arrangement for step `k0,p`

Within a fixed `k0` cell, candidates for `t` are the `V` density boundaries,
the special edges `-d,-bP`, and roots in the left region of

    p(-V)+eta[b+2d+3V-1-c]=k0.                         (10)

Those roots are constant in `s` inside the chosen `k0` cell. The right
region is constant in `V` on each density cell, so it adds no other
interior candidate. Every candidate tail gain is affine in `s` on this
cell. Their pairwise crossings therefore give a finite arrangement, with
piecewise-constant optimal thresholds. The nested thresholds reconstruct
a finite inverse graph, and all frozen features can then be evaluated on
that graph. Rational input data produce a rational arrangement.

For `b<=d`, the I score has no graph term. The existing two-case negative
PAVA reduction applies with the monotone total marginal
`k0+eta(U-d)_+`; its inverse levels inside a ramp cell are linear roots.

The added I term vanishes on every positive-V prefix. The complete ramp
construction retains the old positive-prefix crossing and calibrated
corridor rules. In particular, this localized component avoids the
additional corridor condition that is needed for a nonmonotone full
uniform-I density.

## 4. All induced ramp densities

The following identities describe the complete ramp direction and also
provide independent checks for its implementation. Write `sigma=+1` or
`-1` for the two small-start M3 signs. Since `d>r`, the ramp has no
lower-edge generator at `r`; its contribution is the Stieltjes integral
of unit jump generators for thresholds in `[d,1]`.

The added M3 density is

    delta m_sigma(z,s)
      =eta 1_(s>d) [(s-d)/(4+sigma z-s)
                    +(s-d)^2/(2(4+sigma z-s)^2)].       (11)

Its total mass at start `z` is

    delta M_sigma(z)=eta(1-d)^2/[2(3+sigma z)].          (12)

The full added beta price `B_d(s)` is the sum of the start integrals of
(11). Its primitives contain only rational terms and logarithms. For the
negative early-M2 sheet with turn floor `s0`, the added density is

    delta E(z,s)/eta
      =[(s0-d)_+-(z-d)_+-B_d(z)]/(s0+6-z)
       +1_(s>max(s0,d))
          log[(s+6-z)/(max(s0,d)+6-z)],                (13)

where `B_d` in (13) is understood at unit ramp amplitude. This includes
the full signed-M3 beta-price subtraction at the early edge.

For the intended `d=7/8`, early starts satisfy `z<=1/2<d<s0=15/16`.
Therefore `B_d(z)=0`, `(z-d)_+=0`, and the added early mass is

    delta H_E(z)/eta
      =(1-s0)(s0-d)/(s0+6-z)
       +(7-z)log[(7-z)/(s0+6-z)]-(1-s0).               (14)

It increases in `z`, preserving the old endpoint choice for the line
residual checks. The positive and negative M3 line subtractions use (12).
The high-start difference `k-ell` is unchanged. Both late-sheet densities
are unchanged at this cutoff: the negative late profile is one above `d`,
and the positive late sheet depends on the unchanged `f`. On that outer
region the suffix boundary function gains

    -eta(z+1)(z-d),                                    (15)

which is nonincreasing. The physical line residuals, rather than the
separate signed columns, must be nonnegative in the fitted law.

### Complete frozen feature as a bounded Stieltjes integral

Let `F_old[P;k,ell]` denote the complete old four-score, with the signed-M3
and early-sheet edge corrections included. Its dependence on `k,ell` is
linear for a frozen princess response `P`. If `S_r(U)=1_(U>=r)`, the full
unit-amplitude added column is exactly

    G_d(P)=F_T(P)
       +integral_d^1 F_old[P; k=S_r, ell=S_r]dr,         (16)

with every other old coefficient set to zero in the integrand. Formula
(16) includes the line changes and all induced generators; omitting any
one of them gives a different law. The old generator formulas have bounded
denominators on this compact range, so the integral is finite. Its pieces
are polynomial, rational, and logarithmic. A numerical quadrature of this
column remains a discovery calculation until its error or primitive is
certified.

## 5. Implemented I feature and verification

`packages/interval_turn_sheet/localized_inward.py` supplies exact rational
mass and I-only feature (4). `localized_inward_features.py` exports

    localized_inward_feature(d,b,c,segments)

for the same affine inverse-segment format as the uniform-I feature. It
returns the unit-amplitude four-score. Divide by four when using expected
capture-time LP columns; add the complete old-law ramp column separately.

The independent audit is

```sh
python packages/interval_turn_sheet/verify_localized_inward.py
```

It passes 260 reported checks, including 22 physical two-dimensional
triangle-density integrations by direct polygonal intersections, 22 exact
first-touch slack identities, 22 fast-feature comparisons, and 81 exact
gradient cancellations. The fixtures include high initial positions with
`c<-d` and incoming levels exactly one. Twelve physical examples attain
the envelope; ten retain its stated ceiling slack.

These checks establish the new I feature and its local cancellation. The
complete fitted law must also pass the ramp-density and global response
audits described above. No matching lower law or exact game value is
claimed here.
