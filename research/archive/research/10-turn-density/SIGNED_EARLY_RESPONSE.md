# Positive early turns and the full signed-prefix response

This extends the global upper response construction to early M2 turns
from both signs of starting position. It supplies a computable response
envelope and equality corridor, not a matched equilibrium or a game value.
The rest of the law and the post-one sheets are those of
`SEPARATED_SHEETS_RESPONSE.md` and `TWO_SIDED_LATE_RESPONSE.md`.

## 1. The additional density and its two prefix prices

Write `p=f+g`, where g remains the **total** positive-M2 start marginal.
Choose a positive early start band `[lP,bP]` and a turn threshold `sP`
with `bP<sP<1`. All early and late start bands lie below both early
turn thresholds; in particular none starts inside either turning band.
Assume f, p, and k are nonnegative and nondecreasing and require

    k(sP)>=p(z)              for lP<z<bP.

Put

    jE(z,s)=[k(sP)-p(z)]/(sP+6+z)
                 +integral_sP^s dk(r)/(r+6+z),
          lP<z<bP, sP<s<1.                              (1)

The first term is an ordinary nonzero lower-edge density, not an atom.
For step k the integral is the sum over upward jumps strictly above sP.
Retain the total normalization `w0+integral(p+k)=1`. The positive line
residual is now

    g0(z)=g(z)-integral jE(z,s)ds-integral jL(z,s)ds>=0.   (2)

The negative line residual and both late-density nonnegativity tests
remain necessary. Let

    J_a(s)=integral_(z>a) jE(z,s)dz,
    betaP(s)=integral jE(z,s)dz.                         (3)

Here J_a is an alpha capture price for the positive reflection when
the princess starts below the monster. The reflected beta price betaP
is present for every princess initial position. Both functions vanish
below sP, have nonnegative lower-edge traces, and are nondecreasing
above sP. If a>=bP then J_a=0.

## 2. Negative-prefix first variation

Let the negative prefix inverse be phi(V), with `-a<V<min(c,0)`.
Use z=-V. For fixed a, its four-payoff derivative in an inverse value
U<1 is

    q_U(z,U)=p(z)-k(U)-J_a(U)                  outside [lP,bP],
    q_U(z,U)=p(z)-k(U)                        inside, U<sP,
    q_U(z,U)=-J_a(U)                          inside, U>sP. (4)

The last identity follows from (1):

    (U+6+z)jE(z,U)-integral_sP^U jE(z,s)ds=k(U)-p(z).

An upward jump in q_U at sP is allowed. It does not create a positive
derivative in the sheet or in the rows to its right once U>=sP.

## 3. A global constant-inverse compression

Split the negative V interval into the part with z>bP, the sheet band,
and the part with z<lP. Call the first part the left interval in the
order of increasing V.

On the left interval the score is concave in U and its linear beta
coefficient p(z) decreases as V increases. Jensen and opposite
Chebyshev therefore replace that entire part by one constant inverse,
with any imposed upper bound at its right endpoint. The replacement
does not exceed the old terminal inverse of that part.

On the sheet and on all rows to its right, every score is nonincreasing
for U>=sP. On the sheet this is `-J_a<=0`. On the right it follows from
`p(z)<=p(bP)<=k(sP)<=k(U)` in (4).

Let r be the inverse at the end of the left interval.

* If r<=sP, cap every later inverse at sP. This improves those scores
  and preserves monotonicity. The entire negative prefix is then below
  sP, where the original concavity and opposite coefficient order apply;
  one constant inverse improves it.
* If r>sP, optimize the left interval to a constant uL<=r. If uL>=sP,
  replace the entire remaining negative prefix by uL; its scores improve
  by their nonincrease above sP. The result is one constant inverse.
  If uL<sP, replace that remainder by sP and apply the preceding
  all-below-sP argument.
* If the left interval is empty, a<=bP<sP. Capping at sP is feasible
  from the start, and the first case applies directly. If the whole
  negative prefix ends before the sheet, the ordinary concavity argument
  already proves the result.

Consequently the full negative prefix can still be compressed to

    phi(V)=u,                  a<=u<=1.                  (5)

This is a global comparison. It does not assume that each threshold
score is globally concave across its lower-edge jump. If a>=bP, (4)
also gives a genuine flat equality corridor on the sheet above sP.
Ordered incoming paths may spread there while retaining the scalar
payoff. That equality freedom is relevant to a matching lower field.

## 4. Positive-prefix optimizer and suffix

Let betaN_a be the reflected price from the negative early sheet.
Outside the negative early start band the positive-prefix derivative is

    -k(U)-J_a(U)+k(V)+betaN_a(V)+betaP(V).              (6)

Both its alpha price `k+J_a` and its threshold target
`k+betaN_a+betaP` are nondecreasing. The first crossing of these prices,
clipped to `U>=max(u,V)` and `U<=1`, is therefore an ordered optimizing
inverse. Below the turning bands the minimum legal inverse optimizes
the score, including on the negative early start band. On that band's
old equality corridor the additional derivative is `-J_a<=0`; taking
the minimum legal inverse remains maximizing. When J_a=0, its old
equality freedom remains.

The added alpha price in (3) has support below one, so the post-one
alpha reward is unchanged. The new betaP term changes the positive
suffix price by `(1+V)betaP(V)`. Thus the effective Gamma is

    Gamma(V)-(1+V)[betaN_a(V)+betaP(V)].                 (7)

It is nonincreasing under the previous Gamma hypothesis. The positive
late-sheet alpha source retains its earlier support bound `U<=2-a`.
The same endpoint comparison and one-exit suffix proof consequently
apply.

Under all the stated nonnegativity, separation, and monotonicity
conditions, the unrestricted princess response is therefore still the
supremum over `0<=a<=u<=1, -a<=c<=y<=1`, with (5), the positive-prefix
optimizer (6), and the same one-exit suffix. Boundary values mean legal
one-sided path limits. The cap and time-five argument extend as before;
an integrable unbounded k gives an integrable jE by (1).

## 5. Exact fixed-prefix features

For a rectangular component

    jE(z,s)=C(z)/(r+6+z),         r<s<1,

set `z0=max(0,-c)` and define

    AP(r)=-(1-r)^2/2-integral_(-a)^c (phi(V)-r)_+ dV,
    BP(r)=integral_r^1 [s+phi(s)-4]ds.

Its replacement of positive line mass changes four times the payoff by

    (u-r)_+ integral_max(lP,z0)^min(bP,a) C(z)dz
      -(1-r)^2 integral_lP^min(bP,a,z0) C(z)/(r+6+z)dz
      +AP(r) integral_max(lP,a)^bP C(z)/(r+6+z)dz
      +BP(r) integral_lP^bP C(z)/(r+6+z)dz.             (8)

The first two terms split starts below a according to whether their
negative threshold is crossed in the prefix. The third is the alpha
capture change for starts above a. The fourth is the reflected beta
capture change for every start. The area identity for AP uses exact
first inverses; equality at an individual threshold has zero density
measure in this expression.

For the lower-edge term use `r=sP, C(z)=k(sP)-p(z)`. For an upward k
jump at r>sP use its constant jump size as C(z). These formulas are
linear in the density coefficients for a frozen prefix. The implementation
is `packages/interval_turn_density/positive_early_oracle.py`; it also
provides the optimizer (6) and the positive-sheet marginal rows.

This extension removes a missing upper-support family. It does not show
that the current numerical lower field satisfies equality in every
compression step, that a normalized matching law has been found, or
that every unrestricted monster is controlled.

The implementation's independent checks pass six direct first-capture
comparisons of legal epsilon paths, with maximum extrapolated difference
`1.0843e-18`. `verify_signed_prefix_compression.py` separately optimizes
all monotone inverse sequences on each of its finite fixtures by dynamic
programming: all **2,112 exact rational comparisons** agree with the best
constant inverse, including **1,324** lower-edge-jump cases. The finite
checks support the stated formulas and compression mechanism; the
continuous comparison is the argument in Section 3.

## 6. A moving zero-density lower edge

A finite-band alternative sets

    u0(z)=first{U:k(U)>=p(z)},
    jE(z,s)=integral_u0(z)^s dk(r)/(r+6+z),
                    lP<z<bP, u0(z)<s<1,                (9)

with the continuous-density convention `k(u0(z))=p(z)`. Require
`p(z)>=k(z)` so that every turn is legal. For discontinuous k, the first
crossing jump is included only to the extent exceeding p(z); this gives
the corresponding nonnegative edge term. At fixed lower-edge geometry
the density is still linear in k and p.

In the band the negative-prefix derivative becomes

    q_U=[p(z)-k(U)]_+-J_a(U).                           (10)

Outside it the derivative remains `p(z)-k(U)-J_a(U)`. Put
`sMax=u0(bP)`. Below sMax these scores are concave in U and their
subgradients are ordered in z across both band interfaces. Applying a
supporting line at the mean inverse, followed by opposite Chebyshev,
gives the constant-inverse comparison. Above sMax the band and all rows
to its right are nonincreasing in U. The left-interval and cap argument
of Section 3 then proves the same global negative-prefix reduction.
This avoids imposing a rectangular lower edge.

Two restrictions matter when attaching (9). First, if its start band
extends all the way to one and the entire ordinary negative prefix lies
in that band, its interior incoming condition is `k(u)=p(a)`. The old
ordinary terminal powers would then force an incoming deficit of order
`(1-a)^4`, rather than `(1-a)^2`. The old terminal equations cannot be
carried through that different geometry without rederiving the lower
balance. A finite bP below the ordinary first-outgoing threshold avoids
this particular change.

Second, the separation assumptions in Sections 1-4 ensure betaP is zero
on both negative-M2 start bands. If those bands overlap the positive
early turn region, their cancellation prices change: the late negative
sheet uses `ell+betaP`, and a negative early edge uses
`k(sN)-k(z)-betaP(z)`. Nonnegativity, ordering, and any remaining alpha
price J_a must then be retained. The following section gives that extension;
it is enabled explicitly by `overlap=True` in the implementation.

## 7. The coupled construction when the signed bands overlap

The positive early density is constructed first. Its betaP is a known
linear function of p and k. Define the effective positive-threshold price

    ellEff(z)=ell(z)+betaP(z).

Replace the negative early and late densities by

    hE(z,s)=[k(sN)-k(z)-betaP(z)]/(sN+6-z)
                   +integral_sN^s dk(r)/(r+6-z),

    hL(z,s)=[f(2-v(z))-ellEff(z)]/(v(z)+6-z)
                   +integral_s^v(z) f'(2-r)/(r+6-z)dr.    (11)

Check both displayed edge numerators are nonnegative on their active
start bands, and set the negative line residual to
`k-ell-integral hE-integral hL>=0`. The **actual** negative M1 density
is still ell; betaP is a capture price, not extra monster mass.
Use

    Gamma(z)=F(2-v(z))-ellEff(z)(z+2-v(z))                (12)

in the suffix monotonicity hypothesis. The negative early and late start
bands still lie below sN, so betaN_a vanishes on their starts. They may
now overlap the positive early turn region.

The positive-prefix target remains
`m_a(z)=k(z)+betaP(z)+betaN_a(z)`, and its alpha price is `k(U)+J_a(U)`.
On the negative early start band, the derivative below sN is their
difference, and above sN it is `-J_a(U)`. The new edge condition gives
`k(z)+betaP(z)<=k(sN)`, so the first crossing of the increasing alpha
price with this target occurs no later than sN. Above that crossing
the score is nonincreasing, even through the lower-edge derivative jump.
Consequently the same first-crossing optimizer in Section 4 is valid.
Its targets are ordered across the start-band boundaries, so its
threshold-by-threshold maximizers form a legal nondecreasing inverse.

In the suffix the construction (11) absorbs betaP into the flat negative
late corridor. The remaining effective price is
`Gamma(z)-(1+z)betaN_a(z)`, which is nonincreasing. The negative-prefix
argument is unchanged. Thus the global four-scalar response reduction
extends to these overlapping signed bands under the modified edge,
residual, and Gamma conditions.

For a frozen prefix, the additional features are especially simple.
On each start bin betaP is constant for step densities. Subtract betaP
times the negative early rectangular-component feature at r=sN, and
subtract betaP times the negative late base feature at its upper edge
v(z). This decreases those sheet masses and returns the released mass
to the negative line, preserving k and normalization. Both corrections
are linear in the original densities. `overlap_features`,
`signed_negative_residual`, `signed_positive_residual`, and
`signed_negative_edge` implement the respective rows.

Three additional independent direct-capture comparisons check the
early and late overlap corrections. No optimized density law has been
constructed by these feature checks.
