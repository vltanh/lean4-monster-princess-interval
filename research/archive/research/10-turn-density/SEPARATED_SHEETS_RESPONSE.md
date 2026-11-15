# A computable global response theorem for separated early and late turns

## 1. The support geometry

Choose

    0<=l<b<=s0<1.

The early negative-M2 sheet has starts `-z`, `l<z<b`, and turning
characteristics `s0<s<1`. The late sheet has the same permitted start
band, or a different start band lying below s0, and turns
`1<s<v(z)<=2`. The remaining negative-M2 component is a
density `h0(z)` on the line `s=1`. Positive M1, positive M2, negative M1,
and the endpoint M1 atom retain the notation `f,g,ell,w0`.

Use as an independent variable the **total negative alpha density**

    k(z)=ell(z)+h0(z)+H_E(z)+H_L(z),                         (1)

where `H_E,H_L` are the two sheet marginals. Assume that `f,f+g,k` are
nondecreasing and that `k` is constant, equal to `Klow`, on `[l,s0)`.
Section 8 removes this last restriction by permitting a nonzero early
density at the lower turn boundary.

For an absolutely continuous k, define the early joint density by

    E(z,s)=integral_s0^s k'(r)/(r+6-z) dr,
             l<z<b, s0<s<1.                               (2)

It vanishes outside that rectangle. Monotone k makes E nonnegative.
For step k, with upward jumps `Delta k_i` at turns `r_i>=s0`, this is

    E(z,s)=sum_(r_i<s) Delta k_i/(r_i+6-z),
    H_E(z)=sum_i (1-r_i)Delta k_i/(r_i+6-z).                 (3)

The late sheet is constructed as in `UPPER_EQUALITY_CORRIDOR.md`, with
upper boundary `v(z)=1` off `(l,b)`:

    L(z,s)=[f(2-v(z))-ell(z)]/[v(z)+6-z]
               +integral_s^v(z) f'(2-r)/(r+6-z) dr.          (4)

Require `f(2-v)>=ell` wherever `v>1`. Put `H_L=integral L` and
`M_L=integral(s-1)L`. Finally define the line density by the residual

    h0(z)=k(z)-ell(z)-H_E(z)-H_L(z)>=0.                     (5)

One can impose `ell=k` above b; then no negative-M2 path starts in its
early turning band. This is compatible with the separated support
geometry suggested by the capture-order uncrossing calculation.

The total mass is particularly simple:

    w0+integral_0^1(f+g+k)=1.                               (6)

As before, each reflected pair is split fairly. The functions in (1)-(5)
are ordinary densities; derivative jumps are interpreted through (3).

## 2. Reflected early captures create an initial-position-dependent price

For a nonnegative princess starting at a, define

    beta_a(z)=integral_l^min(a,b) E(r,z) dr,                 (7)

with an empty integral equal to zero. This is the density of reflected
early-sheet captures at the beta threshold z. It vanishes below s0 and
is nondecreasing above s0, because `partial_s E>=0`.

For step k, it is an explicit sum of logarithms:

    beta_a(z)=sum_(r_i<z) Delta k_i
                 log[(r_i+6-l)/(r_i+6-min(a,b))],           (8)

again zero when `a<=l`.

This term is essential. An early turn's reflected capture is `B(s)`,
not the endpoint value `s+1`. It is also the mechanism that changes
the optimal high-V prefix, rather than merely adding another old wave.

## 3. Exact prefix first variation

Fix the initial a and the right-end `U=1` cutoff c. For a beta threshold
z crossed in the prefix, write `phi(z)=U(B(z))`. Its legal domain is

    max(a,z)<=phi(z)<=1,

and the inverse graph is nondecreasing. The cap and atom conventions of
the preceding response theorem are retained: captures at the first
inverse `A(1)` are bounded by the right endpoint of the plateau, and
the corresponding bound is approached with the prefix below one.

Let q denote four times the per-threshold score after expressing alpha
capture delays as integrals in phi. For `a<u<1`, its derivative is

    q'_a(z,u)
      =-k(u)+ell(z)+beta_a(z)
         +Htail(z,u)+(u+6-z)E(z,u),                       (9)

where Htail includes the early turns above u, the line h0, and the
entire late sheet. This follows directly from the early/late first
capture test `phi(z)<=s`; it remains valid when the princess starts
above the monster's turning characteristic.

### Inside the early start band

If `l<z<b`, then `beta_a(z)=0`, since the early turn band lies above b.
For `z<=u<s0`, (9) is zero because k is constant there. For `s0<u<1`,
equation (2) gives

    (u+6-z)E(z,u)-integral_s0^u E(z,r)dr=k(u)-Klow.

Substituting (1) into (9) again gives zero. Thus

    q'_a(z,u)=0            for max(a,z)<=u<1.               (10)

The entire admissible prefix inverse interval is an equality corridor.
No common characteristic is forced on these ranks.

### Outside the early start band

Here E and its marginal vanish, so (9) becomes

    q'_a(z,u)=k(z)+beta_a(z)-k(u).                          (11)

It is nonincreasing in u. A maximizing u is the first point at which
`k(u)>=k(z)+beta_a(z)`, clipped to the current lower bound and one.
Below s0, beta is zero and the smallest legal u already maximizes it.
Above s0, both `k(z)` and `beta_a(z)` are nondecreasing. The selected
maximizers are therefore nondecreasing in z and constitute a legal
characteristic graph. This turns the pointwise sign test into a global
prefix optimization, not just a stationarity condition.

## 4. Only one scalar is needed for the negative-V prefix

On the negative threshold interval `[-a,min(c,0)]`, the alpha potential
is concave in u because k is nondecreasing. Its beta coefficient is
`(f+g)(-z)`, a nonincreasing function of z. For a nondecreasing inverse
graph phi, opposite Chebyshev bounds the beta cross term by the one
using the mean of phi, and Jensen bounds the concave alpha term by the
same constant graph. Thus the entire negative interval can be replaced
by one constant inverse

    phi(z)=u,              a<=u<=1.                         (12)

The mean is no larger than the old terminal inverse, so this replacement
does not make the subsequent positive interval less feasible.

For fixed a,u,c, a canonical maximizing positive prefix is therefore

    phi(z)=max(u,z),                         0<z<min(c,s0),

    phi(z)=max(u, first{k>=k(z)+beta_a(z)}), s0<z<c,         (13)

with the latter value clipped to one and to the spatial lower bound z.
The first line is also a maximizing choice within the early-sheet
equality corridor; arbitrary monotone choices there may be useful for
the matching lower law.

For step k, (13) consists of finitely many constant or diagonal inverse
segments. Its breakpoints and values are determined by a,u,c and the
fixed density knots. The number of segments is bounded by the number
of k bins; no unrestricted wave search is hidden in this construction.

## 5. The post-one suffix still has one exit

Define

    Gamma(z)=F(2-v(z))-ell(z)(z+2-v(z)),

and require Gamma to be nonincreasing. Off the late start band, `v=1`.
The late sheet's equality corridor is unchanged because beta vanishes
on its start band. Outside that band there is no late sheet, and the
ordinary beta cost is `ell(z)+beta_a(z)`.

The exact positive suffix envelope is consequently

    q_a(z,u)<=max{Gamma_a(z)-F(a),0},
    Gamma_a(z)=Gamma(z)-(1+z)beta_a(z).                     (14)

Gamma_a is nonincreasing for every a. Thus one immediate inward leg,
ending at a scalar y, controls every suffix. The old negative-c
argument also applies: if any positive-threshold contribution is
positive, all preceding negative inverses lie below `2-a` and are
improved by moving them to `U=1+`; otherwise the negative-only
Chebyshev reduction suffices.

**Global response theorem.** Under the displayed nonnegativity,
monotonicity, separation, and normalization conditions, the unrestricted
princess response supremum equals optimization over

    0<=a<=u<=1,        -a<=c<=y<=1,                         (15)

using prefix (12)-(13), followed by `phi=1+` up to y and the endpoint
inverse `phi(z)=z+2` thereafter. Boundary parameters mean legal
one-sided payoff limits. The absolute-value comparison covers arbitrary
signed princesses. Every monster captures by time five, so the cap and
boundary limiting arguments have a common finite horizon.

## 6. Analytic features used by the implementation

The implementation uses variables `w0,f_j,g_j,k_j,ell_j`. First evaluate
the old negative-M2-line functional with line density `k-ell`, but with
the actual prefix (13). Replacing the appropriate line mass by each
sheet adds linear features.

For an early derivative jump `Delta k` at turn r, its entire correction
to four times payoff is Delta k multiplied by

    (u-r)_+ length([l,min(b,c)])
      -(1-r)^2 integral_max(l,c)^b dz/(r+6-z)
      +[integral_l^min(a,b) dz/(r+6-z)]
          *[integral_r^1 (s+phi(s)-4)ds].                  (16)

The first term is the change from early to late unreflected capture
before the common cutoff. Its apparent rational denominator cancels
exactly when the turn parameter is integrated. The second changes an
old late capture at four to an earlier late capture at `s+3`. The
third is the reflected `B(s)` correction, including the actual optimized
prefix at high beta thresholds.

The late-sheet correction remains

    2 integral_0^a M_L
      +2 integral_max(0,y)^1 M_L
      -integral_max(0,c)^max(0,y) (7-z)H_L(z)dz.             (17)

Every coefficient in (16)-(17) is integrated by affine primitives and
the two logarithmic primitives in `UPPER_EQUALITY_CORRIDOR.md`.
The residual h0 is a constant minus sums of positive `C/(A-z)` on
each bin. Its minimum is at the right endpoint, so nonnegativity has
finitely many linear checks when profiles and knots are fixed.

The files are:

* `packages/interval_turn_density/separated_oracle.py`: analytic features,
  optimal prefix construction, and residual density rows;
* `packages/interval_turn_density/discover_separated.py`: fixed-profile
  density LP with numerical separation of the four remaining scalars;
* `packages/interval_turn_density/verify_separated.py`: an independent
  direct segment-intersection check on legal epsilon paths.

LP rows freeze their full prefix segments. Recomputing their prefix after
changing k would not be a linear program; the code instead adds a new
row when the updated oracle finds a better prefix.

The numerical optimizer is a discovery tool. It does not certify the
four-scalar maximum exactly and its constraint multipliers are not a
princess lower strategy. The global reduction (15) identifies precisely
what an eventual exact upper certificate must check.

For an affine boundary `v(z)=v0+v1*z`, the late moments are integrated
after splitting where `2-v(z)` crosses an f knot. On each resulting
cell, the new numerators have degree at most two and the denominator
is the affine function `v(z)+6-z`. Polynomial division and one
logarithm integrate them exactly. `features_affine` implements this
case; it does not replace the affine boundary by a step approximation.

## 7. Optional endpoint-time cap

Suppose no negative-M2 paths start above b and ell is nondecreasing
there. For any `d>=b`, the sufficient condition

    2ell(d)-integral_d^1ell >= w0+F(1)+G(1)                 (18)

allows all positive beta advance to stop at d before the final endpoint
wait. Indeed for `z>d` and a prefix inverse `z<=u<=1`, the per-threshold
score is at most

    Fbar(a)+w0+Gbar(a)+integral_u^1ell
                           -ell(z)(z+2-u)
      <=w0+F(1)+G(1)+integral_z^1ell-2ell(z)<=0.

The omitted beta_a cost only strengthens the inequality. The suffix
score is also at most zero under (18). Replacing every inverse above d
by `z+2` is monotone and feasible, and improves the payoff. This yields
responses with `c,y<=d` and endpoint arrival by `1+d`.

Condition (18) is sufficient and can be too restrictive for an optimum.
The first fixed-profile numerical experiment with this condition gave
a much worse objective; that is a diagnostic for this constrained
class, not an exclusion of other ways to obtain the same lower-path
completion geometry.

## 8. Nonzero lower-edge density removes the flat-k restriction

The flat-k assumption in Section 1 is a sufficient special case. For
arbitrary nondecreasing k, use instead

    E(z,s)=[k(s0)-k(z)]/(s0+6-z)
                   +integral_s0^s k'(r)/(r+6-z)dr,
             l<z<b, s0<s<1.                              (19)

The first term is nonnegative. For step k, use its right-continuous
value at s0 in that term, and sum only derivative jumps strictly above
s0 in the second term. A derivative jump at s0 is thereby counted
exactly once. The resulting early density has a permitted positive
one-sided trace at its lower turn boundary, not a measure atom there.

The residual (5), normalization (6), and late sheet (4) are unchanged.
The inside-band first variation is now

    q'_a(z,u)=k(z)-k(u)<=0,       max(a,z)<u<s0,
    q'_a(z,u)=0,                 s0<u<1.                   (20)

Indeed, above s0,

    (u+6-z)E(z,u)-integral_s0^u E(z,r)dr=k(u)-k(z),

which substitutes directly into (9). The score decreases until s0 and
is flat thereafter. Therefore choosing the smallest legal inverse is
still globally maximizing on this start band. If the incoming prefix
already has `u>=s0`, the entire remaining interval is an equality
corridor. Low incoming prefixes need not be spread across that corridor.

Outside the early start band, (11) still holds. The new beta_a has a
nonnegative jump at s0 and is nondecreasing thereafter, so its selected
maximizers remain ordered. The Jensen argument, suffix envelope, and
global four-scalar theorem are unchanged. In particular this extension
does not require k to be constant across either start band.

For each fixed start-density bin j inside `(l,b)`, the extra trace in
(19) is a rectangular component with turn range `[s0,1]` and coefficient
`k(s0)-k_j`. Its feature is exactly (16), with `r=s0` and the start
interval restricted to that bin. Thus all features and residual checks
remain linear in the variables `w0,f,g,k,ell`.

The implementation enables this extension with `--edge-trace`. The
fixed-bin density LP then drops its flat-k equalities. The early and
late start bands may also be specified independently with
`--left/--right` and `--late-left/--late-right`.

## 9. Integrable unbounded endpoint densities

The response reduction also permits integrable endpoint singularities.
Assume f, p=f+g, and k have nonnegative nondecreasing versions on `[0,1)`,
are locally bounded there, and have finite integrals. Retain all the
stated support, residual-density, and Gamma monotonicity assumptions.
The negative-M2 start bands must remain in a fixed compact subinterval
`[0,b]`, with `b<s0<1`; on the terminal interval take `k=ell`.
The conclusions concern the same legal path limits as before, not an
endpoint atom substituted for a continuous layer.

All cumulative primitives are then finite and continuous on `[0,1]`.
The early density in (19) obeys `E(z,s)<=C k(s)` uniformly over its
start band, for a constant depending only on b and s0. Hence its total
mass is finite. Integration by parts in the late density gives an
analogous bound by `C[f(2-s)+ell(z)]`, so its mass is finite as well.
The boundary terms vanish because a nondecreasing integrable function
q satisfies `(1-s)q(s)->0` as s tends to one.

The prefix proof uses the concavity of the finite primitive of k, rather
than a boundedness assumption on its derivative. Jensen and opposite
Chebyshev therefore apply unchanged. Every interior inverse threshold
has finite density values; the pointwise first-variation inequalities
integrate to the same finite score inequalities. Their endpoint values
follow by continuity of the primitives. The suffix proof likewise uses
the finite integral identities and the assumed monotonicity of Gamma.
Thus the four-scalar upper envelope extends directly to these densities.

For approximation or verification, use `f_n=min(f,n)`,
`p_n=min(p,n)`, `g_n=p_n-f_n>=0`, and `k_n=min(k,n)`, with the matching
terminal `ell_n=k_n`. For large n the values on the compact start bands
and at s0 are unchanged. Clipping decreases both early and late sheet
mass; putting the released mass on the line at U=1 preserves their
start marginals and nonnegativity of the residual. The densities converge
in L1, including the sheet components. Adding the vanishing missing
normalization mass to the endpoint pair gives legal probability laws.
This construction is used for convergence, not to silently assume every
clipped Gamma retains an original equality at a support interface.

Every component monster in this support captures by time five. Thus
the payoff error between two such laws is at most five times their L1
measure distance, uniformly over all princess paths. This justifies the
bounded approximations and the passage of legal near-maximizing paths
to the unbounded response envelope. A numerical tail splice still has
to check the density and monotonicity assumptions of this section; an
endpoint singularity alone does not establish a global bound.
