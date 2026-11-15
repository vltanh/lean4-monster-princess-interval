# Global Bellman-potential experiment: design, not executed

The physical-node and adaptive-record engines were executed. No interpolated
potential residual scan or certificate was executed before the executor
outage. The intended target was `continuum_h5_candidate_08.json`, SHA256
`fe6329176f03f76be08e97b22e8cb9beab0b01a8cfdb327e431511a2234b1c68`.
Its adaptive physical-node audit used 187 shared record knots and 234,360,892
states; the floating guide and an exactly rescored three-interior-turn route
both gave approximately 1.421488834258294. This is not an unrestricted
Monster lower certificate. The complete late field/report bytes were not
in the last pushed checkpoint and are unavailable while the executor is down.

## 1. State and nodal candidate

Use remaining masses a,b, with survival S=a+b. Feasible post-contact states
satisfy a<=F^-(t,x), b<=1-F^+(t,x). At node i let A_i=F^-_i and B_i=1-F^+_i.
Convert the node DP's absolute future capture moment Q_i to remaining duration

    W_i=Q_i-t_i(a+b).

Rationalized table entries define a candidate function; their numerical
provenance does not certify it. Interpolate each nodal table piecewise
bilinearly in records and extend it by zero-cost immediate clipping:

    Wbar_i(a,b)=W_i(min(a,A_i),min(b,B_i)).

Use a physical triangulation containing x=0, x=+-1, t=0 and t=H as faces.
On each triangle define phi=sum_i lambda_i Wbar_i. Shared edge traces agree.
The finite polynomial partition contains the common record knots and every
incident node-specific A_i/B_i breakpoint. This physical interpolation is
affine in (t,x) and bilinear in (a,b), hence piecewise cubic.

## 2. Enforce center resets before computing a differential defect

Raw physical interpolation need not respect moving center caps between time
nodes. Put

    g(t)=(1-R(t,t))/2,
    phi0(t,a,b)=phi(t,0,a,b),
    C(t,a,b)=phi0(t,min(a,g(t)),min(b,g(t))),
    V(t,x,a,b)=phi(t,x,a,b)-(1-|x|)*(phi0(t,a,b)-C(t,a,b)).

Then V(t,0,a,b)=C(t,a,b), and C is unchanged by the center reset
a->min(a,g), b->min(b,g). Both incoming traces therefore equal the
post-reset value.

At x=+-1 the correction vanishes. Nodal clipping makes the +1 trace
independent of b and the -1 trace independent of a, so endpoint resets also
have zero potential jump. The moving surviving endpoint cap still matters
for waiting at an endpoint and must not be omitted.

At t=0 and H, the actual center cap equals its center-node cap, so phi0 is
already flat beyond it and the correction is zero. Initial and terminal
values are preserved.

Refine at center-time knots, the planes a=g(t), b=g(t), and crossings of g
with record knots. The corrected candidate is continuous and piecewise
polynomial of degree at most four, with no moving denominators. This
construction received internal mathematical review. It does not
automatically preserve monotonicity in the surviving records.

## 3. Global differential obligations

On an open half-interval, the signed CDF F is affine on each field cell.
For Monster speed v, set d=F_t+v F_x and

    adot=min(d,0) if a=F, otherwise 0,
    bdot=min(-d,0) if b=1-F, otherwise 0.

The remaining-duration residual is

    R_v=V_t+v V_x+V_a adot+V_b bdot+a+b.

Check all four active/inactive record cases, with their appropriate closures
and every incident potential/field piece. The residual is piecewise affine
in v. Its critical speeds are -1, +1 and v_track=-F_t/F_x when F_x>0.
The transport inequalities put v_track in [-1,1]. If F_x=0 then F_t=0 and
the two unit speeds suffice. Tracking speed cannot be discarded unless
V_a,V_b>=0 have been established separately.

At the center, waiting has v=0 and both records use cap g(t):
qdot=min(g'(t),0) on q=g(t), otherwise zero. Check

    C_t+C_a adot+C_b bdot+a+b.

At +1, b=0 and a follows the changing strict endpoint cap when active.
At -1, a=0 and b follows the changing complementary closed cap. Check these
waiting residuals as well as the inward controls. Do not assume endpoint
trace monotonicity unless it is imposed or proved for the supplied field.

## 4. Terminal and initial conditions

At absorption time H, the exact remaining endpoint-tour cost is

    T(x,a,b)=min((1+x)a+(3+x)b,(3-x)a+(1-x)b).

Assign terminal nodal record values by exact rational evaluation of T,
rounding downward if desired. For fixed x, T is concave in records, and for
fixed records it is concave in x. Record chords followed by physical boundary
interpolation therefore remain below T. Clipping only decreases T since it
is nondecreasing in a,b. The center correction vanishes at H, giving V_H<=T.
This boundary construction must not rely on a floating value accidentally
being rounded downward.

Compute

    c0=inf_x V(0,x,F^-(0,x),1-F^+(0,x)),

including endpoint starts. The present fields have a continuous piecewise
affine initial CDF. On an initial physical edge the left node clips a to
its own initial cap, while the right node clips b to its cap. After splitting
at record-knot crossings, the initial expression is quadratic in x.
Endpoints and any in-interval stationary point give an exact rational
minimum. Initial atoms would require their explicit strict/closed values.

## 5. Repair a verified global differential defect

If every differential residual, including center and endpoint waiting, is
rigorously at least -K with K>=0, define

    Vhat=V-K*(H-t).

Its residuals are nonnegative, reset equalities remain exact, and terminal
values are unchanged. It certifies c0-KH against every Monster, provided all
partition/interface and boundary obligations have been checked.

A piecewise constant time profile K(t) can instead be repaired by subtracting
integral_t^H K(s) ds. The initial loss is then integral_0^H K(s) ds.

A numerical worst-residual scan is diagnostic only. A certificate needs
exact polynomial bounds or outward-safe interval/Bernstein bounds on every
state cell and every control case. A negative residual witness or a weak
rigorous K would still be a useful result, but neither is a matching saddle.

## 6. Arbitrarily many center contacts

The existing interior-CDF gate needs an explicit extension at center atoms.
A finite-center-excursion approximation avoids a gap in applying the chain
rule to infinitely many resets.

For a legal Monster on a bounded complete horizon, replace every bounded
excursion away from zero of duration at most eta by the constant-zero path
on that interval. Leave the at-most-two boundary components unchanged.
The modified path is legal, has finitely many nonzero excursions, preserves
all endpoint visits for eta<1, and differs from the original by at most
delta=eta/2.

Let L bound the spatial slope of the interior radial CDF R near the center,
for example on 0<=r<=1/2, with constant continuation after H. Take eta<1,
so all removed excursions stay in this neighborhood. No global Lipschitz
bound across the endpoint atom is assumed. On a removed positive excursion, the strict CDF can only decrease and the
complementary closed CDF increases by at most L*delta/2. On a negative
excursion the roles reverse. Taking the two running minima gives

    S_modified(t)<=S_original(t)+L*delta.

Thus J_modified<=J_original+L*delta*T on the common complete horizon T=H+4.
The certificate applies to the modified path, which has finitely many
center resets and arbitrary Lipschitz motion within each open-sign excursion.
Letting eta tend to zero transfers the same lower bound to the original.
No turn-count bound or continuity of the first-capture functional is assumed.

Endpoint contact resets one remaining tail to zero at its first visit;
subsequent endpoint waiting uses the surviving cap obligation above.
These boundary traces must remain explicit in the implementation.

## 7. Implementation order after recovery

1. Export the completed node DP's remaining-duration table to a scratch
   binary and rationalize it to define the candidate. A smaller certification
   record grid may be sampled initially, retaining local caps.
2. Replace terminal values by the exact endpoint-tour values.
3. Implement the center correction and analytic derivatives; independently
   test reset identities and finite fixtures.
4. Scan the whole domain numerically to estimate the scale of K.
5. Certify K using exact or outward-safe arithmetic, then compute the
   corrected initial bound.

No table export, residual scan, K, or corrected initial guarantee was
produced before the outage. The closed numerical node objective is not a
substitute for these checks.
