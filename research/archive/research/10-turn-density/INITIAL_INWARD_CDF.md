# Initial-inward responses and their moving support boundary

## 1. Exact first-contact identity

Let `p_q` be ordered nonnegative princess paths, with uniform rank `q`,
and reflect the law fairly. Assume that `beta_q(1)=2` and `beta_q(3)=4`
almost surely. This holds, for example, for endpoint-absorbed paths whose
final outgoing characteristic is strictly less than one. Define first
inverses

    alpha_q(U)=inf{t:t+p_q(t)>=U},
    beta_q(V)=inf{t:t-p_q(t)>=V}.

Use the initial-inward route `I(a,v)` from
`INWARD_INITIAL_OBSTRUCTION.md`, with `-a<=v<a`. Write

    A=A(a)=Pr(p_q(0)<=a),
    r=R_<(a,v),              B=R(1,v),
    c_1(q)=2 alpha_q(1)-1,   J(r)=integral_0^r c_1(q)dq.

Here `R_<` is the strict radial CDF and `R` the closed radial CDF, in
characteristics `U=t+x,V=t-x`. Then the exact four-score is

    4CI(a,v)=12-8A
       +integral_-a^v R_<(a,w)dw
       +(1-a-v)r+J(r)
       -(7-v)(B-A)_+
       -integral_a^1 (R(U,v)-A)_+dU.                     (1)

The initial row and its turn trace must be strict. The initial CDF, middle
column, and `U=1` trace must be closed. This distinction retains capture at
time zero and on a shared incoming characteristic. Defining `c_1` through
the first inverse also allows an incoming `U=1` atom; identifying it with
the final outgoing characteristic requires excluding such an atom.

For the boundary turn `v=a`, subtract

    2(2-a) Pr(p_q(a)=0)                                 (2)

from (1). The reflected route then touches the center at time `a` and
captures its waiting atom before the nominal `beta(1)=2` capture. A
two-dimensional inward density gives this boundary zero mass, but a pure
response comparison cannot discard the correction.

### Derivation

On the unreflected side, ranks below `r` first meet `U=1`; ranks in
`(r,A]` meet the initial inward segment at `alpha(a)`; ranks in
`(A,B]`, if that interval is nonempty, meet the middle outward leg at
`beta(v)`; all other ranks are captured at time four. The reflected copy
is captured at time two when `v<a`.

Layer cake gives

    integral_r^A 2alpha_q(a)dq
      =integral_-a^v R_<(a,w)dw-(a+v)r,

    integral_0^r 2alpha_q(1)dq=r+J(r),

    integral_(q>A) capture_middle_or_final(q)dq
      =4(1-A)-[(7-v)(B-A)_+
                 +integral_a^1(R(U,v)-A)_+dU]/2.

Adding the reflected contribution proves (1). For exact CDF integration,
the moment can also be written without recovering individual quantiles:

    J(r)=integral_-1^1 min(r,R_<(1,w))dw-r.              (3)

## 2. The turn derivative and a necessary support boundary

At smooth interior points, (1) yields

    4 partial_v CI
      =[1+c_1(r)-a-v]R_V(a,v)
       -(7-v)1_(B>A)B'(v)+(B-A)_+
       -integral_a^1 1_(R(U,v)>A)R_V(U,v)dU.            (4)

If `B<=A`, transport implies `R(U,v)<=A` for every `U<=1`.
The last three terms vanish. The remaining coefficient is
`2[alpha_r(1)-alpha_r(a)]>=1-a>0`, so

    B<=A and R_V(a,v)<0  =>  partial_v^+ CI<0.          (5)

At `B=A`, use the right derivative, since increasing `v` makes `B`
nonincreasing. A two-sided derivative at that positive-part boundary
need not exist. With `B<A`, the ordinary derivative suffices.

Thus an active open inward-density patch cannot occupy such a region.
It must either lie on a transport plateau `R_V=0`, or satisfy the rank
ordering `R(1,v)>A(a)`. In a genuinely varying negative outgoing tail,
this is a moving support boundary. A density positive on an entire fixed
triangle `d<a<1,-a<v<-d` is consequently an upper-strategy experiment,
not automatically a matching terminal support.

## 3. A conditional Volterra equation for the curved initial phase

Suppose the first `U=1` characteristic agrees with the final outgoing
characteristic on the branch in question. Introduce deficits

    x=1-U,        y=1+V,
    r(x)=1-A(1-x),
    e(y)=1-R(1,-1+y),
    D(x,y)=1-R(1-x,-1+y),       w=e^{-1}.

On any specified smooth active inward patch with `e(y)<r(x)`, equation
`partial_v CI=0` becomes

    [w(D)+x-y]D_y(x,y)
      =(8-y)e'(y)+r(x)-e(y)
         +integral_0^x 1_(D(t,y)<r(x))D_y(t,y)dt.       (6)

Its integral source uses only smaller `x`, so this is a backward Volterra
equation in the original `U` coordinate. Transport requires `D_x,D_y>=0`.
The actual initial and row-one traces are

    D(x,x)=r(x),        D(0,y)=e(y).                    (7)

The active patch has not been proved to fill the wedge between those
traces. Its lower free boundary, attachment conditions, and positivity
must be solved rather than assumed. If the diagonal is differentiable,
the initial princess speed is

    velocity=2 D_y(x,x)/r'(x)-1.                       (8)

A positive-length initial unit run is ruled out by
`INWARD_INITIAL_OBSTRUCTION.md` wherever `Cg` is active. A unit tangent
with immediate curvature is still possible. Equation (6) is a candidate
construction equation, not an existence or equilibrium theorem.

## 4. Verification and scope

Run

```sh
python -B packages/interval_turn_sheet/verify_initial_inward_cdf.py
```

The rational fixtures compare (1)-(3), including the center correction,
with complete capture-record integration for one-, two-, and three-wave
ordered laws. They also check the strict initial trace using actual atomic
paths and the finite ordinary-prefix attacks. No path mesh or numerical
optimization is used in those checks.

The exact unrestricted minimax value remains open. The new results exclude
an incompatible tail and identify the initial field and moving boundary
that a replacement must address.
