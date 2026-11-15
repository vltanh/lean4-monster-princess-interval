# Endpoint inward turns and the curved initial field

An inward route whose second turn is the positive endpoint is a separate
response face. Monotonicity of an interior turn does not control its
closed endpoint capture. This note gives its exact initial-band kernel,
a derivative-free field obstacle, and a strict finite consequence for
ordinary initial runs. All post-one first inverses are retained. No
complete matching law is asserted.

## 1. Coalescence with positive M1

Fix `0<b<=a<=1`, and write

    v=-b, S=2-b, t0=(a-b)/2.

The endpoint inward route `I_end(a,-b)` starts at +a, moves inward to
`(U,V)=(a,-b)`, moves outward to the positive endpoint, and then sweeps
the two endpoints. Positive M1 `f(b)` starts at +b and moves outward to
the positive endpoint before the same final sweeps.

At time t0 both monsters occupy `(a+b)/2`. Their subsequent trajectories
coincide exactly. The two prefixes are positive, so the negative
princess copy has identical first capture under both routes. A positive
path initially below b stays below both prefixes until coalescence; a
path initially above a stays above both. Only initial positions in
`[b,a]` can have different capture times.

Let `alpha_q(U)` and `beta_q(V)` be the true first inverses of `t+p_q(t)`
and `t-p_q(t)`. Put

    A0=Pr(p(0)<b), A=Pr(p(0)<=a), L=R_<(a,-b).

Then `A0<=L<=A`. First inward captures are exactly the ranks between L
and A, with closed first contact at the turn. The other ranks in the
initial band are captured after the endpoint turn. Consequently

    4[CI_end(a,-b)-Cf(b)]
      =2 integral_A0^L [alpha_q(S)-beta_q(-b)]dq
       +2 integral_L^A [alpha_q(a)-beta_q(-b)]dq.       (1)

The strict lower initial boundary and closed upper initial boundary
retain initial atoms correctly. A path at the first turn is assigned
using the strict radial trace; its actual first inverse, rather than an
arbitrary point on a characteristic plateau, must be used.

## 2. Positive-M1 activity also excludes an initial unit-outward run

Assume `Pr(p(0)=b)=0`. Suppose the positive-mass initial band
`b<xi<=a=b+delta` moves at speed +1 until its incoming coordinate reaches
`u(xi)>a`. The replacement endpoint
I catches each of these paths at

    t_new=(a-xi)/2<t0.

Positive M1 from b cannot catch it before `(u(xi)-b)/2`: the gap stays
constant during the initial +1 run, and even the fastest subsequent
approach closes it at relative speed at most two. Thus

    4[CI_end(a,-b)-Cf(b)]
      <=integral_(b,a] [a+b-xi-u(xi)]dA(xi)<0.        (2)

Equality in the first comparison holds when the old capture is on the
first incoming leg. If it is later, including capture at the endpoint,
the inequality is stronger. The paths outside this initial band have
identical first captures by the coalescence argument. The no-atom
condition at b is essential here: a path initially exactly at b is
captured by f(b) at time zero but can be delayed by the endpoint-I
replacement. An atom at the upper start a is included in `(b,a]` and is
captured by the replacement at time zero. The general identity (1)
retains both kinds of atoms without these extra assumptions.

Hence an active positive M1 start b with no initial atom there cannot
face a positive-mass ordinary initial +1 band with a positive run length
past b. This is independent
of positive-M2 activity. Making g inactive does not rescue the ordinary
initial tail considered in `DETACHED_INWARD_CORNERS.md`.

The result does not prohibit an initial unit tangent followed by
immediate curvature. It identifies an actual initial-motion obligation,
not merely a missing correction to a later incoming moment.

## 3. Full field form of the endpoint obstacle

Use deficits

    x=1-a, y=1-b,      0<=x<=y<1,
    D0=1-R_<(1-x,-1+y),
    r_x=Pr(p(0)>1-x), r_y=Pr(p(0)>=1-y).

For continuous initial laws, both r values are the same initial-deficit
function evaluated at x and y. Define the **full post-one** alpha moment

    Aplus_y(d)=2 integral_0^d alpha_(1-q)(1+y)dq.       (3)

It can be read directly from the strict radial row:

    Aplus_y(d)=2y d
       +integral_(-1+y)^(1+y)
                     [R_<(1+y,V)-(1-d)]_+dV.         (4)

The first term accounts for the physical endpoint edge before that row
enters the interval. Formula (4) retains post-one incoming motion,
reversals, and endpoint atoms. It is not a final-outgoing-characteristic
substitution.

The exact deficit-field identity is

    4[CI_end-Cf(b)]
      =Aplus_y(r_y)-Aplus_y(D0)+(y-x)D0
       -integral_x^y D_<(x,t)dt
       -integral_b^(1+y) [1-R(U,-b)-r_x]_+dU,         (5)

where `D_<(x,t)=1-R_<(1-x,-1+t)`. The first integral is strict in its
horizontal row; the last uses the closed radial CDF. At `U=1+y` the
monster is at +1 and uses closed endpoint capture. An endpoint value
does not alter the integral, but it is essential to the preceding
capture partition.

For the row term, the first-inverse identity is

    2 integral_L^A alpha_q(a)dq
       =(y-x)D0-integral_x^yD_<(x,t)dt.

For the whole initial band's outward time,

    2 integral_A0^A beta_q(-b)dq
       =integral_b^(1+y)[1-R(U,-b)-r_x]_+dU.

Substituting these two identities into (1) proves (5).

## 4. Increasing scalar inverse and an initial-rank barrier

For fixed x,y define

    Phi_(x,y)(d)=Aplus_y(d)-(y-x)d.

Almost everywhere in rank,

    Phi'(d)=2alpha_(1-d)(1+y)-(y-x)>=x+y.             (6)

The inequality uses `alpha(1+y)>=y`, since the princess position is at
most one. Thus the endpoint equality determines at most one local
deficit D0 once its row and column moments and the post-one inverse are
given. At continuous diagonal points x=y, the identity gives D0=r(y).

A stronger lower barrier comes from the actual positive-M1 costs.
Formally put D0=r_x, or L=A(a), while retaining the input row and column
integrals. Replacing the initial-row moment N by its upper bound
`delta A(a)`, where `delta=a-b=y-x`, gives a delayed positive-M1 payoff:
the lower positive ranks use `alpha(2-b)` instead of `alpha(2-a)`, the
higher positive ranks use `beta(-b)` instead of `beta(-a)`, and the
reflected copy uses the later endpoint tour.

Each positive first inverse increases by at least delta/2. The reflected
capture increases by at least delta. In four times expected capture this
is a gain of at least `3delta`. Restoring the actual N loses at most
`delta A(a)`. Therefore the formal endpoint four-cost satisfies

    RawCost(D0=r_x)
       >=4Cf(a)+(3-A(a))(y-x)
       >=4Cf(a)+2(y-x).                               (7)

If every relevant positive-M1 cost is at least a proposed value V, a
root of the endpoint-I equality at V cannot fall below r_x. This is an
invariant of the endpoint obstacle. It does not rely on an ordinary
incoming cap or on fixed positive-M2 indifference.

## 5. Positive M2 needs slack at an active endpoint inward column

Let `CI1=CI(a,-b,1)` and `Cg(b)` be the positive M2 with second turn U=1.
Set `B1=R(1,-b)` and `M=max(A,B1)`. The exact cross comparison is

    2{(CI_end-CI1)-(Cf(b)-Cg(b))}
      =integral_A0^L [alpha_q(2-b)-alpha_q(1)]dq
       +integral_B1^M [beta_q(3)-beta_q(-b)]dq
      >=(1-b)(L-A0)/2+(3+b)(M-B1)>=0.                (8)

The first term accounts for initially lower ranks missed by the first
inward leg. The second accounts for upper ranks missed by the U=1
outward turn. All negative-copy terms cancel. The identity remains true
with post-one high-rank motion.

If Cf(b) and the endpoint I both equal V, but fixed-turn g(b) also equals
V and either band on the right is nonempty, (8) gives CI1<V. Thus a
nondegenerate active endpoint-I column requires sufficient positive-M2
slack. The old equality update

    (8-2y)e(y)=y(3-r(y))+Q(y)

cannot be imposed merely because positive M1 and endpoint I are active.
The post-one field and its U=1 trace must be matched through the correct
remaining equations and inequalities.

## 6. A conditional contraction estimate and its interface limitation

The exact obstacle does not itself prove existence. One useful local
estimate is available when the prescribed post-one inverse has the box

    Aplus_y'(d)>=kappa d,       r(y)>=Dlo sqrt(y).

At `d=theta r(y)`, the two subtractive moments in (5) are bounded by
`3y r(y)`. Hence the raw gap above Cf(b) is at least

    (kappa/2)(1-theta^2)r(y)^2-3y r(y).

For sufficiently small Y this is positive throughout `0<y<=Y`; an
active root lies above theta r(y). Its inverse derivative is then at
least `kappa theta Dlo sqrt(y)-y`. With fixed r and post-one data, the
unknown pre-one row and column lengths total at most `2y-x`. The scalar
root map consequently has the uniform-norm Lipschitz bound

    2 sqrt(Y)/(kappa theta Dlo-sqrt(Y)),              (9)

provided the denominator is positive and the displayed invariant box
holds. This is a conditional initial-patch estimate, not a joint
equilibrium theorem.

In particular, the active root can be of order sqrt(y) as x approaches
zero, while the required U=1 trace can be of order y. The active initial
patch must therefore attach to an independently determined incoming
region. Extending the root throughout the entire pre-one triangle would
create an unverified U=1 jump. The incoming interface, transport
projection, positive- and negative-M1 moments, post-one field, and all
other monster inequalities remain part of the construction problem.

## 7. Independent exact verification

Run

```sh
python -B packages/interval_turn_density/verify_endpoint_inward_comparison.py
```

The verifier compares the initial-band kernel and full obstacle against
independent physical first intersections, including initial atoms,
strict first-turn traces, and post-one first inverses. It also checks the
formal lower barrier, the increasing inverse bound, the cross comparison
(8), and strict finite attacks on ordinary initial runs using the
continuous-rank capture engine. No sampled route minimum is promoted to
an unrestricted value or matching strategy.
