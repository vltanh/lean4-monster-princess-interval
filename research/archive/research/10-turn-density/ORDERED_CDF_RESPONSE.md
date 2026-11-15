# Ordered-CDF responses, a transport obstacle, and separated turn support

## 1. Scope

This note supplies three tools for constructing a matching lower law:

1. an exact response formula for a monster with one interior turn, including
   the strict trace required at an incoming atom;
2. a contracting obstacle map that enforces every early response of this
   form, without guessing which of those responses is active;
3. an uncrossing inequality that rules out certain chains of active turns
   and motivates a separated start/turn geometry.

The last section gives elementary functions satisfying joint start and turn
indifference on a separated rectangle. The boundary attachment, the other
monster responses, and a matching upper law are not solved. In particular,
neither the obstacle fixed point nor the rectangle is an unrestricted saddle
certificate.

The exact finite fixtures in
`packages/interval_turn_sheet/verify_general_response.py` and
`packages/interval_turn_sheet/verify_uncrossing.py` independently check the
response and uncrossing identities by direct segment intersections. They do
not certify an equilibrium or the infinite-dimensional obstacle construction.

## 2. Definitions and the exact one-turn response

Choose an ordered law of nonnegative princess paths `p_q`, with uniform
`q in (0,1)`, and then reflect it with probability one half. For this section
assume that every positive path has reached `+1` by time two and remains there.
Write

    A(z) = Pr(p_q(0) <= z),
    B_q(v) = inf{t : t-p_q(t) >= v}.

For characteristic coordinates `U=t+x`, `V=t-x`, define the closed and
strict radial CDFs by

    R(U,V)  = Pr(p_q((U+V)/2) <= (U-V)/2),
    R_<(U,V)= Pr(p_q((U+V)/2) <  (U-V)/2).

The domain is `U>=V`, `U+V>=0`, `U-V<=2`. At an interior positive position,
transport admissibility is the order condition that `R` increases in `U`
and decreases in `V`. Where derivatives exist it is `R_U>=0`, `R_V<=0`.
Central and endpoint atoms are allowed.

Let `M2(z,s)` start at `-z`, move right to the event

    (time,position)=((s+z)/2,(s-z)/2),

then visit `-1` and `+1` at times `s+1` and `s+3`. In the formula below
`0<=z<=1` and `z<=s<=z+2`. Let `C2(z,s)` be its expected capture time
against the symmetric princess law. Put

    N(z) = integral_(-z)^z R_<(z,V) dV,
    I(s,z) = integral_z^s R(U,z) dU,
    G(s,a) = integral_s^(s+2) (R(U,s)-a)_+ dU,
    W = 6+s-z.

Then the exact identity is

    4 C2(z,s)
      = N(z)+4s+8-2(s+1)A(z)
        -W R(s,z)-I(s,z)-G(s,A(z)).                    (1)

### Derivation

Negative princesses whose initial radial position is at most `z` are either
captured initially or captured on the first rightward leg. Their total
first-capture contribution, before the reflection factor, is `N(z)/2`.
The strict CDF is required because a first inverse of `t+p_q(t)` has already
ended at equality. In particular an initial atom at `z` costs zero; an entire
incoming segment on `U=z` must not be charged as still uncaptured.

The remaining negative princesses are captured on the leftward leg at
`B_q(s)`. Layer cake gives

    integral_(q>A(z)) B_q(s) dq
      =(1-A(z))(s+1)-G(s,A(z))/2.                      (2)

The positive princesses captured before the first turn have total mass
`R(s,z)`. Their capture-time moment is

    ((s+z)R(s,z)-I(s,z))/2.

Every other positive princess is captured on the final sweep at `s+3`.
Here endpoint absorption by time two is used: the relevant first inverse
is `B_q(s+2)=s+3`. Adding these contributions and multiplying by the
reflection factor proves (1).

Thus `A`, the turn value, `I`, and `G` use closed CDFs, while `N` uses the
strict CDF. Replacing the latter by the closed CDF is incorrect for atomic
incoming characteristics. For continuous interior CDFs the distinction
disappears except on integral-null central boundary points.

For `s>1`, endpoint absorption makes `G(s,a)=0`; (1) reduces to the simpler
late-turn formula. For `s<1`, omitting `G` discards new negative captures on
the return leg and is generally wrong.

## 3. A contracting obstacle for every early one-turn response

Work on the prefix triangle

    D = {(s,z): 0<=z<=s<=1}.

Fix the initial CDF `A`, a continuous candidate upper-boundary CDF `C(z)`,
the characteristic strip with `V<0`, and the field with `U>1`. Assume these
fixed pieces have values in `[0,1]`. In this construction the unknown
interior CDF is continuous; atomic boundary attachments need their separate
first-touch checks from Section 2.

For a proposed guarantee `c`, define

    F_c[R](s,z)
      =[N(z)+4s+8-2(s+1)A(z)-4c-I(s,z)-G(s,A(z))]
        /(6+s-z).                                     (3)

Equation (1) says exactly that

    C2(z,s)>=c  if and only if  R(s,z)<=F_c[R](s,z).     (4)

The unknown prefix contributions in `N`, `I`, and `G` have lengths `z`,
`s-z`, and `1-s`, respectively. Positive part is 1-Lipschitz. Consequently

    ||F_c[R]-F_c[S]||_infinity <= (1/6)||R-S||_infinity. (5)

This estimate includes changes in the running rank cut `A(z)` only through
the fixed initial data; `A` is not an additional variable in this bound.

### Transport projection

For a continuous function `f` on `D`, put

    (M f)(s,z) = inf {f(u,v): u>=s, 0<=v<=z}.           (6)

The set is the rectangle `[s,1] x [0,z]`, which lies in `D`. The function
`M f` is the greatest function below `f` that increases in its first
coordinate and decreases in its second. It is continuous and nonexpansive
in the uniform norm. The direction of the infimum is essential.

Define

    T[R] = M min{A(s), C(z), F_c[R](s,z)}.              (7)

The minimum and `M` are nonexpansive, so `T` is a contraction with constant
at most `1/6`. It also preserves values in `[0,1]` when `0<=c<=3/2`.
Indeed `N>=0`, `I<=s-z`, and `G(s,A)<=2(1-A)` imply

    numerator of F_c[R] >= s+z+6-4c >=0.               (8)

The other two obstacles bound the result above by one. Thus Banach iteration
gives a unique continuous fixed point `R_*` in this space. An exact uniform
residual bound gives the error estimate

    ||R-R_*||_infinity <= (6/5)||R-T[R]||_infinity.     (9)

A residual checked only at numerical mesh points is not an exact uniform
residual bound.

At the fixed point, `R_*<=F_c[R_*]`, so every early `M2(z,s)` response in
`D` satisfies (4), provided the field attaches to the fixed pieces with the
specified CDF traces. This construction chooses active and inactive early
turns through the obstacle; it does not assume all of them are indifferent.

### Limits of this conclusion

The fixed point is not asserted to be the greatest feasible CDF. The map
`F_c` contains terms with both signs and need not preserve the pointwise
order of input fields; contraction uniqueness is not an optimization
statement.

Boundary attachment is also a genuine obligation. The fixed-point trace
at `U=1` or `V=0` can fall below the prescribed `C` or strip trace. A jump
may describe admissible characteristic atoms, but a monster touching that
characteristic captures the atom. Its cost must use the prescribed closed
CDF, and may be smaller than the interior limit. Such a jump cannot be
silently accepted as a matching boundary certificate.

Finally, (7) checks one-turn monsters. Repeated interior turns and the
initial motion within one half-interval remain outside this certificate.

## 4. The indifference equation and its Volterra form

For smooth data, differentiating (1) in the turning characteristic gives

    W R_U(s,z)+2R(s,z)
      =2(2-A(z))-partial_s G(s,A(z))                  (10)

on an active turn sheet. This is equivalent to the first-inverse formula
`W R_U+2R=2+2 partial_s integral_(q>A(z)) B_q(s)dq`.

Let `C(z)=R(1,z)`, `L=7-z`, and

    K(z)=[2-A(z)-C(z)]L^2.

Integration by parts eliminates all derivatives of `G`:

    R(s,z)=2-A(z)
      -[K(z)-L G(1,A(z))+W G(s,A(z))
          +integral_s^1 G(r,A(z))dr]/W^2.             (11)

Each `G(s,.)` uses the future row `V=s`, so this is a backward Volterra
construction. For fixed `A`, `C`, and exterior field, its map on the
unknown prefix triangle has uniform contraction constant at most

    (1-s)/W+(1-s)^2/(2W^2) <= 13/72.                  (12)

Start indifference can likewise be imposed by the exact boundary equation

    4c=N(z)+12-4A(z)-G(1,A(z))-L C(z)
         -integral_z^1 R(U,z)dU.                      (13)

Eliminating `C` between (11) and (13) yields a joint start/turn map with
contraction constant at most `7/36+13/72=3/8`, for fixed `A`, `c`, the
negative-V strip, and the post-prefix field. Its boundary trace must still
match that exterior field, and its result must still satisfy the transport
and probability constraints.

These indifference constructions should be used only on a proposed active
region. For example, with `A(0)=0`, the monster at `(z,s)=(0,0)` has cost
`3/2+E B_q(0)/2>=3/2`; it cannot be active at the target value below `3/2`.
The obstacle formulation avoids forcing that false equality.

## 5. An exact uncrossing inequality for two successive turn choices

This section no longer requires endpoint absorption. It applies to any
ordered nonnegative 1-Lipschitz princess law, using the exact first inverses
`B_q(v)` throughout.

For `0<=z<=s<=1` and `s<=t<=s+2`, define:

* `M2(z,s)` as above;
* `M1(s)`: start at `-s`, visit `+1`, then `-1`;
* `M3(z,s,t)`: start at `-z`, turn right-to-left at `U=s`, turn
  left-to-right at `V=t`, then visit `+1` and `-1`.

Let their symmetric expected costs be `C2`, `C1`, and `C3`. Write

    r=R(s,z), q=R(t,s), A0=A(z), As=A(s).

The speed cone gives `r<=As`. Direct capture partitioning yields

    2[C3(z,s,t)+C1(s)-C2(z,s)-C2(s,t)]
      = integral_r^As [B_u(t)-B_u(s+2)]du
        -integral_q^max(A0,q) [B_u(t+2)-B_u(s)]du.     (14)

The first integrand is nonpositive and the second is nonnegative. Therefore

    C3(z,s,t)+C1(s) <= C2(z,s)+C2(s,t).                (15)

For a pure nonnegative princess the same calculation uses indicator ranks.
Hence the inequality holds pointwise for every such princess, and not just
for one selected lower law. The absolute-value response theorem for a
symmetric monster law then shows that replacing equal masses of these two
M2 pairs by the M3 and M1 pairs cannot increase the unrestricted response
ceiling, even with other symmetric monster components held fixed. This is
a statement about response ceilings; the absolute-value argument alone does
not establish pointwise domination for sign-changing princess paths.

For endpoint-absorbed lower laws, (14) has the quantitative bound

    2[C3+C1-C2(z,s)-C2(s,t)]
      <= -(As-r)(s+2-t)-(A0-q)_+(t-s+2).               (16)

Indeed `B_u(s+2)=s+3`, `B_u(t+2)=t+3`, and `B_u(v)<=v+1`.
Without endpoint absorption, the two lower bounds on inverse increments
from the 2-Lipschitz function `t-p_q(t)` give half these coefficients.

### Consequence for active support

Suppose both `C2(z,s)` and `C2(s,t)` equal a proposed saddle value `c`,
while every monster must cost at least `c`. Then `C1(s)>=c`, and (16)
is incompatible with `R(s,z)<A(s)` and `t<s+2`. Thus a spread incoming
field cannot support such a chain of two active M2 choices.

A full triangular active M2 sheet is therefore the wrong support geometry
for a genuinely spread prefix. This does not exclude the obstacle field,
whose inactive responses can be strictly more costly. It motivates a sheet
whose start coordinates and turn characteristics are separated.

### Exact-start atoms cannot be hidden in one-sided parameter limits

Let `Cf(x)` be the positive-M1 pair cost and `Cell(x)` the negative-M1 pair
cost, and write `A_q(v)=inf{t:t+p_q(t)>=v}`. At an interior initial position
`a`, the first-inverse capture formulas give

    Cf(a+) = Cf(a)
               +(1/2) integral_(p_q(0)=a) A_q(2-a)dq,  (16e)

    Cell(a-) = Cell(a)
               +(1/2) integral_(p_q(0)=a) B_q(a+2)dq.  (16f)

Every other capture term converges to its exact value in the indicated
direction: the inverse threshold approaches from below, and first inverses
of continuous nondecreasing characteristics are left-continuous. The sweep
deadlines permit dominated convergence.

Since `A_q(2-a)>=1-a`, an interior initial atom produces a strict dip in
`Cf` at its exact starting position. Therefore, if positive-M1 support
accumulates from the right at `a` with common cost `c`, an attained lower
law guaranteeing `c` cannot put an initial atom there. No opposite jump in
another capture branch repairs the exact-start dip.

Formula (16f) also applies at `a=1` from the left. For endpoint-absorbed
paths its extra term is twice the total initial endpoint mass. Thus an
attained matching law has no initial endpoint atom when negative-M1 support
is active arbitrarily close to one. This restriction does not itself
exclude an approaching family of nonatomic laws: its shrinking layers
must be checked uniformly against monsters, rather than replaced by their
singular limit.

## 6. A concrete separated-sheet branch

### Independent initial and incoming distributions

A completed candidate should not identify its initial-position CDF with its
incoming-characteristic CDF without proof. For an ordinary first wave write

    A(z)=Pr(a<=z), I0(z)=Pr(u<=z), C(z)=Pr(c>=z),
    R(U,V)=min(max(A(-V),I0(U)),C(V)),

where `0<=a(q)<=u(q)<1` permits a genuine initial outward leg and
`-a(q)<=c(q)<=1`. Initial endpoint components are handled separately by
their traces. At regular fronts put

    alpha=A^{-1}(I0(z)), beta=I0^{-1}(C(z)),
    gamma=C^{-1}(I0(z)).

For the monster with turn `U=1`, exact differentiation of (1) gives

    4 C2_z(z,1)
      = A+2I0+C+(alpha+z)I0'-4A'-(8-z-beta)C'
          if C>I0,

    4 C2_z(z,1)
      = A+3C+(alpha+gamma)I0'-4A'-(8-2z)C'
          if C<I0.                                    (16a)

The second formula also allows `gamma<0`. Admissibility gives
`alpha+gamma>=0`, and the first-leg moment in that regime is

    N(z)=integral_gamma^z C(V)dV+(alpha+gamma)I0(z)
           +integral_alpha^z A(x)dx.

Its derivative is `A+C+(alpha+gamma)I0'`, so no assumption
`I0(z)<=C(0)` is needed.

The negative-C branch can include moving paths, not just endpoint starts.
Let `E(z)=Pr(c<-z)` and `alpha_minus=A^{-1}(1-E(z))`. For nonendpoint
fronts define

    u0=I0^{-1}(A(z)), uminus=I0^{-1}(1-E(z)),
    d=V-coordinate of rank A(z) at U=2-z,
    c0=V-coordinate of rank A(z) at the U=1 cutoff,
    J=integral_0^A(z) partial_U V_q(2-z)dq.

On active positive-M1 and positive-M2 parameter intervals the corresponding
lower indifference equations are

    (2+d-u0)A'=3+E-(2-z-uminus)E'+J,
    (1+z+c0-u0)A'=1-A-E-(8+z-uminus)E'.                (16b)

These follow from the moving negative-C corrections
`integral_(c<-z)(2-z-u(q))dq` and
`integral_(c<-z)(8+z-u(q))dq`, respectively. The earlier endpoint-only
equations are the special case `uminus=1`. A first-inverse plateau at
`U=1` needs the same first-touch convention as Section 2; these are smooth
front equations, not rules for replacing a plateau by its later endpoint.

The exact fixtures in `verify_initial_wave.py` test the ordinary-wave
derivatives with `a` different from `u`, including both front orderings and
support gaps. Equations (16a)-(16b), together with the upper free-`u`
condition, are the appropriate general candidate system. The simpler
explicit branch below is only one attachment within it.

There is a useful first integral when both positive families are active.
Put

    Qlate(z)=integral_0^A(z) [V_q(2-z)-V_q(1)]dq.

Since `Qlate'=(d-c0)A'-J`, subtracting (16b) gives

    (1-z)A(z)-2(3+z)E(z)+Qlate(z)-2z = constant.       (16c)

If the active interval reaches one and `E(1-)=e1`, then

    E(z)=[(1-z)(A(z)+2)+Qlate(z)+8e1]/[2(3+z)].        (16d)

For a wave completed by `U=1`, `Qlate=0`. Thus the moving negative-C
distribution is not an additional freely fitted function on this branch.

### An elementary attachment

Use three distinct cutoffs

    b < d < s0,

where negative-M2 starts satisfy `z in [l,b]`, every positive princess has
final outgoing characteristic at most `d`, and active monster turns have
`U>=s0`. Then `B_q(s)=s+1` on the active turn region: the return threshold
is beyond every final outgoing characteristic. Consequently `G=0` there,
and (10) integrates to

    R(s,z)=2-A(z)-K(z)/(6+s-z)^2.                      (17)

Suppose a simple pre-sheet attachment has

    R(s0,z)=Q=A(s0)             for l<=z<=b,

and, before that boundary, the relevant cone has `R(U,V)=A(U)`. This is the
canonical incoming cone with enough central/outgoing threshold separation;
it is an attachment hypothesis to verify for the completed law.

Start indifference at `U=s0` is then

    2(s0+1-z)A'(z)=3A(z)+Q.                            (18)

It has the explicit solution

    A(z)=k/(s0+1-z)^(3/2)-Q/3,
    k=[A(l)+Q/3](s0+1-l)^(3/2),                        (19)

and

    K(z)=[2-A(z)-Q](6+s0-z)^2.                        (20)

Thus (17)-(20) solve both start and turn indifference on an entire
two-dimensional rectangle; no fitted incoming density is left on that
branch. Their common cost is

    4c=4s0+8-2(s0+1-l)A(l)-(6+s0-l)Q
          -integral_l^s0 A(u)du.                      (21)

The integral depends on the still-to-be-specified initial-CDF attachment
between `b` and `s0`.

### Transport and inward motion

Let `D(z)=2-A(z)-Q`, `W0=6+s0-z`, and let `v(z)` be the upper turn boundary.
For `s0<=s<=v(z)`, a sufficient transport condition is

    A'(z)>=D(z)/W0.                                   (22)

Every quantile in this patch moves inward or stays fixed if also

    A'(z) <= 2D(z)W0/[(6+v(z)-z)^2-W0^2].              (23)

This follows from `R_t=R_U+R_V=-A'-K'/(6+s-z)^2`.
The usual transport inequalities already imply speed at most one. The two
conditions are compatible when the patch is sufficiently narrow.

Matching the lower-V edge `V=l` to a canonical incoming strip would require

    A(U)=2-A(l)-K(l)/(6+U-l)^2                         (24)

on the corresponding high-initial-position interval. Endpoint components
and any extension beyond `U=1` require their own matching equations.

That canonical matching is not forced. Write `J(U,l)` for the sheet's
lower-edge value and choose a larger high-initial CDF `A(U)>=J(U,l)`, with
`A(s0)=J(s0,l)=Q`. For an increasing function `theta` with `theta(0)=0`
and `theta(l)=1`, the unused strip can instead be attached by

    R(U,V)=(1-theta(V))A(U)+theta(V)J(U,l),
        U>=s0, 0<=V<=l.                               (24a)

Both terms increase in `U`, and `J(U,l)<=A(U)` makes this expression
decrease in `V`. It joins the canonical `R=A(U)` field at `U=s0` and
the sheet at `V=l` without an atom on the latter characteristic. This
allows more initial mass at high positions than (24).

For active starts `z in [l,b]`, the first-leg moment at `U=z<s0` and the
prefix row through `U=s0` are unchanged. If the remaining return/front
conditions are retained, the exact common cost (21) is therefore unchanged.
Other monsters can distinguish these attachments; their inequalities still
have to select a suitable `A` and `theta`. At the endpoint `U=1`, initial
atoms retain the separate trace obligations of Section 2.

For scale only, one may start discovery with
`l=1/10`, `b=7/10`, `s0=9/10`, `A(l)=1/10`, `Q` near `0.78`, and choose
`d` strictly between `b` and `s0`. Formula (19), followed by a monotone
attachment to `A(s0)=Q`, gives costs in the range relevant to the existing
game bounds, and (22)-(23) hold for sufficiently small turn width. These
numbers are a parameter seed, not a lower strategy certificate or a new
claimed bound.

The separation has a useful global implication: after one of its active
turns the monster returns to the center at time at least `s0>d`. From a
center visit at such a time, no remaining positive path can be caught at an
interior point by a same-side excursion; direct endpoint completion suffices.
The initial same-half prefix and turns below `s0` remain to be controlled.

### A weaker completion condition permits late central waiting

The restriction on every outgoing characteristic is stronger than necessary.
Suppose instead that, for a nonincreasing function `Y`,

    R(U,V)=Y(V)       whenever U>=V>=s0 and U-V<2.       (25)

This occurs if the inner ranks have completed their incoming motion by
`U=s0` and then only wait at zero or move outward, while all later curved
incoming ranks have final outgoing characteristic below some `b<s0`.

At a center visit at time `e>=s0`, both reflected prefixes through rank
`Y(e)` have been captured. Any subsequent same-half excursion before an
endpoint visit lies in the cone `U>=V>=e`. By (25), its radial rank is at
most `Y(V)<=Y(e)`, so it captures no new interior princess. This proves the
same endpoint-completion conclusion, even if some inner paths wait at zero
until time one.

Condition (25) does not alone remove the return-front term from the active
M2 payoff. It gives exactly

    G(s,A(z))=2(Y(s)-A(z))_+.                           (26)

A sufficient additional condition preserving the inverse-square formula is

    Y(s0)<=A(l).                                       (27)

Every remaining late central rank was then already captured on the first
leg, for every active start `z>=l`. If (27) fails, the turn-indifference
equation must retain the derivative of (26); one cannot reuse (17) merely
from the endpoint-completion observation.

## 7. Remaining full-game obligation

The obstacle map rigorously handles one specified infinite response family;
the uncrossing identity explains why naive triangular active support fails;
and the separated branch supplies actual elementary indifference functions.
None proves that all monster paths are controlled.

To close the game, a completed lower law must attach the initial, central,
sheet, outgoing, and endpoint pieces with correct capture traces, match a
specific normalized upper law at the same constant, and satisfy a global
monster certificate. The Bellman inequality in
`../08-continuum/QUANTILE_AND_TAIL.md` remains one route. A finite-response
reduction specific to the completed separated law would be another. No
universal turn bound is inferred from symmetry or CDF ordering.
