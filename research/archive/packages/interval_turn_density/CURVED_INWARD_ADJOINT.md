# The general initial-inward adjoint and its terminal balance

This note gives exact upper-response identities for an arbitrary physical
initial-inward density. It also records a conditional endpoint balance which
differs from the excluded ordinary initial-outward tail. The identities are
verified independently below. The active region and a matched normalized law
have **not** been constructed.

## 1. General density and first-touch-safe score

Use the symmetric routes `I(z,v)` from
`research/10-turn-density/UNIFORM_INWARD_UPPER.md`. Their density is

    i(z,v)>=0,             0<z<1, -z<v<z.

It is additional probability mass. Define

    m(z)=integral_-z^z i(z,v)dv,       M=integral_0^1 m(z)dz,
    T_z(V)=integral_V^z i(z,v)dv,
    j_a(V)=integral_-V^a i(z,V)dz,     -a<=V<0.

The formulas here concern a negative outgoing characteristic `-a<c<0`.
The princess inverse `U=phi(V)` runs from `V=-a` to `V=c`, is nondecreasing,
and satisfies `a<=phi<=1`. Write `u=phi(c-)`, and let `psi` denote its
inverse in the U direction, including initial and terminal outward
connectors. The last point on `U=1` has characteristic c.

The relaxed four-score of this component is

    F_I=4M+(1+c) integral_a^1 m(z)dz+8 integral_0^a m(z)dz
          +integral_a^1 (z-1)T_z(c)dz
          +integral_-a^c q_I(a,c,V,phi(V))dV,              (1)

where

    q_I(a,c,V,U)
      =j_a(V)(V+U-8)
       -integral_a^U [T_z(V)+(1+c-z-V)i(z,V)]dz.          (2)

This is an upper ceiling for an arbitrary nonnegative princess. It uses
`alpha(1)<=(1+c)/2`, `beta(1)<=2`, and `beta(3)<=4`, exactly as the
uniform-density proof. For the canonical prefix and an outgoing suffix,
the joint epsilon convention approaches it. In particular, replacing a
first inverse by its last-U=1 representative is a relaxation, not an
identity for a path with a U=1 plateau.

To derive (2), put

    G(z,V)=(z+V-1-c)T_z(V).

Then `G_V=T_z(V)+(1+c-z-V)i(z,V)`. The alpha capture region
`psi(z)<=V` is `z<=phi(V)`, apart from density-null boundary sets.
Integrating this derivative gives the second term of (2). The first term
is the direct outward-capture contribution from starts below a.

The local derivative is therefore

    (q_I)_U=j_a(V)-T_U(V)-(1+c-U-V)i(U,V).              (3)

For an old-law negative prefix outside its compact M3 start band, the
total derivative of four times the score is

    F=p(-V)-k(U)+j_a(V)-T_U(V)-(1+c-U-V)i(U,V),         (4)

where `p=f+g` and k is the total negative alpha marginal. Formula (4)
does not itself assert concavity or a four-scalar response theorem for
arbitrary i.

## 2. Exact a and c variations

Assume the density and graph are regular at the displayed traces, so that
the one-sided variations agree. Let `u0=phi(-a+)`. Holding the interior
graph fixed, its initial-coordinate variation is

    (F_I)_a
       = integral_-a^c [phi(V)+V]i(a,V)dV
          +8T_a(c)+q_I(a,c,-a,u0).                     (5)

For an immediately curved initial path, `u0=a`, and the final term is
zero. For an initial outward connector it must be retained. Varying a
while clamping the graph below by the new a gives the same first
variation at a continuous initial tangent; the additional area is of
higher order.

The last-characteristic variation is

    (F_I)_c
       = integral_u^1 m(z)dz
          +integral_a^u integral_-z^psi(z) i(z,v)dv dz
          +integral_u^1 (1-z)i(z,c)dz
          +(c+u-8)j_a(c).                              (6)

The third term is a genuine edge term. For starts above u the first
inverse lies on the final outward connector, so changing c moves both
the capture time and the first-turn capture boundary. Omitting this term
already fails for a constant uniform density.

For example, at `a=4/5,u=9/10,c=-2/5` with `i=1`, the first two terms
of (6) are `39/200`, the edge is `1/200`, and the last term is `-3`.
The correct derivative is `-14/5`, not `-561/200`.

A useful equivalent derivation of (6) starts from

    integral_a^1 m
      -integral_a^u T_z(c)dz
      -integral_-a^c integral_a^phi(V) i(z,V)dz dV
      +integral_u^1(1-z)i(z,c)dz+(c+u-8)j_a(c).

Fubini combines its first three terms into the first two terms of (6).
Thus the missed first-leg mass, terminal edge, and early-capture jump are
separate quantities.

## 3. The full terminal upper equations

Consider a negative-c no-extra branch with an immediately curved initial
tangent. Assume its other attached monster components have compact start
support below this branch and have constant score there. Put

    x=1-a,       d=1+c,       h=1-u,
    Pbar(a)=integral_a^1 p(z)dz,       Kbar(u)=integral_u^1 k(z)dz.

Assume also `k=ell` in this terminal start interval. This is a restriction
of the specified attached family, not a consequence of negative-M2 slack
for every possible monster law. Extra negative-M2 mass cannot simply be
used there to repair an adjoint imbalance: its endpoint limit has a
strictly larger cost than the endpoint sweeper under the stated lower-law
trace assumptions. Any proposed extra multi-turn family must have its
own score and free-start variation included.

With `I_a=(F_I)_a` and `I_c=(F_I)_c`, exact a and c stationarity are

    0=-(d+x)p(a)+x g(a)+(8-2x)ell(a)+I_a,              (7)

    0=w0+Pbar(a)+Kbar(u)
        -(d+h)p(-c)-(8-2d)g(-c)+I_c.                  (8)

These replace the old ordinary-prefix equations. They are linear in the
upper densities when the lower graph is supplied.

On every genuinely increasing interior portion of that supplied inverse,
equation (4) must vanish pointwise. On a constant incoming block it is
instead an ordered variational condition: the total integral of F over
the block is zero and every initial partial integral is nonnegative,
when no endpoint constraint binds. It is not valid to impose a pointwise
equation throughout a unit-speed incoming block. The old single Ku
equation is consequently only one special block condition.

## 4. A support cap and an exact column-mass gate

The following is an explicit additional hypothesis, not a conclusion
from the local initial germ:

    c(a) is decreasing, and i(a,v)=0 for v>c(a).        (9)

In an ordered lower law, `B(v)=R(1,v)=A(c^{-1}(v))` on a smooth ordinary
outgoing phase. Condition (9) keeps the density on the necessary
`B(v)>A(a)` side of the support boundary. The exact route comparison in
`research/10-turn-density/INWARD_TURN_DOMINANCE.md` supersedes the earlier
derivative-only gate: it excludes `B<=A` even on transport plateaus and,
under its endpoint hypotheses, excludes a quantitative strip next to
that boundary. Thus (9) is a valid weaker cap for a matching fixed-second-
U=1 density under those hypotheses. The actual active region may be
strictly smaller. This statement does not apply without alteration to
the moving-second-turn family discussed below.

Under (9), `T_a(c(a))=0` and the edge term in (6) is zero. Its two
nonnegative remaining mass terms are bounded by `integral_a^1 m`.
Using the complete normalization

    w0+integral_0^1 p+integral_0^1 k+M=1,

equation (8) gives the necessary bound

    (8-c-u)j_a(c)+(2+c-u)p(-c)+(6-2c)g(-c)<=1.         (10)

In particular the relevant inward column masses remain bounded as
`a,u->1` and `c->-1`. This conclusion does not discard a possible edge
concentration without (9); that concentration appears explicitly in (6).

## 5. Conditional endpoint exponent selection

Here are the uniform hypotheses needed to turn (10) into an exponent
test. Suppose `d(x)~D x^r` and `p(1-y)~B y^(-s)`, with `B,D>0`.
For each small y, suppose there is an active curved-I strip of width at
least a fixed positive multiple of y in the start coordinate U, lying
between `1-theta_1 y` and `1-theta_0 y`, for fixed
`0<theta_0<theta_1<1`. On that strip require:

* The princess rank in (4) has initial deficit at most y, so its
  coefficient `1+c-U-V` is at most a constant times `y^r`.
* `k(U)+T_U(-1+y)<=theta p(1-y)` uniformly for some `theta<1`.
* The strip lies inside the column integrated in (10) for the princess
  whose final characteristic is `-1+y`.

Then (4), with `j_a>=0`, yields

    i(U,-1+y)>=constant*y^(-s-r),
    j_(c^-1(-1+y))(-1+y)>=constant*y^(1-s-r).

Therefore (10) forces

    s+r<=1.                                            (11)

The old `s=2/3,r=1/2` tail is incompatible with these *uniform active-strip*
hypotheses. A fixed-a golden-ratio expansion does not supply them: the
size of the active region must still be established from the lower field.

Under (9), equation (7) also gives

    ell(1-x)<=(d(x)+x)p(1-x)/(8-2x).                    (12)

If ell stays bounded below by a positive constant, (12) forces `s>=r`.
This holds, for example, in a nontrivial matched law retaining a
nondecreasing k with `k=ell` near one. Thus for the provisional lower
exponent `r=1/2`, assumptions (9)-(12) select the critical exponent

    p(1-x)~B/sqrt(x).                                   (13)

They do not prove that the provisional lower exponent, the support cap,
or a full active strip actually occurs.

## 6. The a/c leading balance and its incoming obstruction

Retain the provisional lower maps `d(x)~4sqrt(x)` and `h(x)~x^2/16`.
Assume the critical I field has the uniform column and row-moment limits

    i(U,-1+y)~B/(4y) on almost all its width-y active column,
    j_(c^-1(-1+y))(-1+y)->B/4,
    integral_-a^c [phi(V)+V]i(a,V)dV=o(1).              (14)

The first assertion is motivated by (4) when the initial rank deficit is
`y(1+o(1))` and its other prices are lower order. It is a further uniform
matching requirement, not a consequence of the fixed-a germ. More
generally one can replace the column limit `B/4` by an unknown finite J.

Equations (7)-(8), integrability of the upper law, and (9) then give

    ell(1-)=k(1-)=B/2,
    g(1-)=w0/8-J.                                      (15)

For the column limit in (14), this becomes

    g(1-)=(w0-2B)/8,       0<B<=w0/2.                  (16)

This is a nonnegative, integrable balance of the a and c equations only.
It does not satisfy the remaining incoming variation automatically. The I mass in a
turn-deficit interval of length t is `Jt+o(t)`, even though its density
is of order `1/y`. It differs substantially from the old power-log tail.
In particular, (16) also gives the conditional endpoint ceiling
`ell(1-)<=w0/4`.

Keeping only a start-independent turn density is not enough to construct
this balance. A subleading start dependence in its **value** can contribute
at leading order to its start derivative. Dropping that derivative gave
the misleading coefficient `k~3B/2*x^(-1/6)` when the old exponent 2/3 was
temporarily retained. Equations (7)-(8) show why that coefficient cannot
be patched into the old law.

There is a concrete incoming obstruction to treating (13)-(16) as a valid
tail. Under (9), at a terminal inverse `u>a`, the I row above `c(u)` is
empty. A small upward variation near `V=c(a)>c(u)` therefore requires

    k(u)>=p(-c)+j_a(c)>=p(-c).                         (16a)

For provisional powers `d(x)~D x^r`, `1-u(x)~H x^q`, and
`p(1-x)~B x^(-s)`, the a-equation bound (12) and (16a) require

    s>=q r/(q-r),             q>r.                    (16b)

The old `r=1/2,q=2` attachment requires `s>=2/3`, which conflicts with
the uniform active-strip gate (11). A finite limiting k also directly
fails (16a) when p diverges. This is a restriction of the capped,
fixed-second-U=1 family and the stated lower attachment. Moving the
second turn of I below one changes the alpha price and is not covered
by these equations.

## 7. The local adjoint germ at the initial diagonal

At a fixed interior initial coordinate a, put `d(a)=1+c(a)` and suppose

    i(a,-a+tau)=i0(a)+i1(a)tau+i_phi(a)tau^phi+o(tau^phi),
    phi=(1+sqrt(5))/2,

with the row coefficients sufficiently smooth in a. Diagonal equality
and a critical initial tangent in (4) require exactly

    p=k+m+d i0,
    d i1=(2+c')i0-p'.                                  (17)

For `U=a+zeta,V=-a+delta`, these give

    F=(1-c')i0 delta-d i_phi zeta^phi
         +o(delta+zeta^phi).                            (18)

The independently audited lower germ has

    V+a~kappa(a)((U-a)/2)^phi,
    kappa(a)^phi=2^(phi+1)/(phi*d(a)).

Matching it in (18) fixes the positive coefficient

    i_phi/i0=(1-c') phi^(-1/phi) d^(-phi).              (19)

For `i0>0,c'<1`, the density is positive on a sufficiently small local
neighborhood. At fixed a it may be finite and continuously differentiable;
the fractional singularity is in its second derivative. Its endpoint
dependence may still be unbounded. This local positive germ does not
determine its row mass, its free support edge, or its continuation over
the entire incoming arc.

## 8. A positive adjoint solve on a supplied active patch

There is a local construction of the I density once its lower field and
active patch are supplied. It removes the arbitrary density function
from that conditional problem, but does not choose the patch or enforce
the a/c and block conditions.

Use `eta=1-U`, `y=1+V` on a measurable patch
`P subset {0<eta<=y<=Y}`. Let `x(eta,y)` be the initial deficit of the
lower rank at that point, so `eta<=x<=y`. Prescribe the lower c front
and put

    Dcoef(eta,y)=d(x(eta,y))+eta-y.

Assume `c0 sqrt(y)<=Dcoef<=C0 sqrt(y)` for positive constants c0,C0.
Extend the unknown density I by zero outside P at turn deficits below
Y. Any density at larger turn deficits is fixed exterior data, whose
row tail is `E(eta)>=0`. Equation (4) is exactly the affine map

    T[I](eta,y) = [p(1-y)-k(1-eta)-E(eta)
          +integral_x(eta,y)^y I(s,y)ds
          -integral_y^Y I(eta,t)dt]/Dcoef(eta,y).       (20)

In the weighted norm `||I||=ess sup_P y|I(eta,y)|`, its linear part has
norm at most

    kappa=(1+2/exp(1))*sqrt(Y)/c0.                    (21)

The column integral is at most `||I||`, and the row integral is at most
`||I|| log(Y/y)`. Multiplication by `y/Dcoef` and
`sup_(0<y<=Y) sqrt(y)log(Y/y)=2sqrt(Y)/exp(1)` prove (21).
This is a complete integral operator on the patch, not a discretized
incoming path.

Suppose the weighted source S in (20) lies between positive constants
`s_min,s_max`. If

    kappa<1,
    H=s_max/(1-kappa),       L=s_min-kappa H>0,        (22)

then (20) preserves the box `L/y<=I<=H/y` and is a strict contraction.
It therefore constructs a unique positive density by Picard iteration.
Its physical mass is at most `H Y`, so the singularity is integrable.
After two successive iterates differ by epsilon in the weighted norm,
the remaining error is at most `epsilon*kappa/(1-kappa)`.

For example, source bounds follow from

    B_min<=sqrt(y)p(1-y)<=B_max,
    0<=k(1-eta)+E(eta)<=K,

with `s_min=(B_min-K sqrt(Y))/C0` and `s_max=B_max/c0`.
Taking Y sufficiently small supplies (22). These are checkable data
requirements; no actual matching lower patch is asserted here.

Where the supplied rank field is smooth, the resulting equality also
encodes the correct local ordering. Along `a=a(U,V)`, differentiate (4)
with `c=c(a)`. Its parameter derivative is

    F_a=i(a,V)-c'(a)i(U,V).

For nonnegative density and `c'<=0`, one has `F_a>=0`. It is strictly
positive if `i(a,V)>0`, or if `c'<0` and `i(U,V)>0`; positivity only at
the latter point is insufficient when `c'=0`. Consequently
`F_U=-F_a a_U<=0` and `F_V=-F_a a_V>=0` on the active patch of a legal
ordered lower field. This does not control a jump to an inactive region
or a bound incoming block; those remain global variational checks.

## 9. Independent verification and remaining construction

Run `verify_general_inward_adjoint.py`. It passes 693 exact checks:
18 complete physical two-dimensional integrations, 549 independent
capture cells, 36 a variations, 36 c variations, 36 nonzero edge-term
checks, and 18 inverse-gradient identities. All arithmetic is rational.
The physical integration partitions the monster parameter domain and
computes actual segment intersections; it does not evaluate (1)-(6) as
its capture oracle. The derivative checks use exact polynomial
interpolation, not a small floating finite difference.

To obtain an equilibrium one must still construct the lower active field
and its transport, solve (4), (7), and (8) with the block and boundary
conditions, prove nonnegative densities and residual line masses, and
attach the other phases at a common score. The actual generalized I law
also needs its unrestricted ordered-prefix optimization; the existing
uniform and localized finite-state oracles do not establish that result
for an arbitrary i. No new value bound or matched strategy is claimed.
