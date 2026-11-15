# A pointwise two-extrema envelope before the first center

## Scope

This is a sufficient capture-moment bound for an arbitrary same-side
prefix. It does **not** assert that a single one-reversal path attains the
pointwise envelope at all times, or that every optimal whole prefix has
one reversal.

Assume an ordered law of radial 1-Lipschitz paths. A monster starts at
positive position a, stays positive before its first center visit at
time t<1, and has final upper captured rank n. No speed or turn-count
restriction is imposed. The implementation presently accepts continuous
piecewise-affine initial and interior radial CDFs. Center atoms are
retained with their strict/closed traces.

Write A=A(a). At time s≤t let L_s,M_s be the running lower and upper
positive-rank records. Then L_s≤A≤M_s≤n.

## 1. Domination for two extreme targets

Fix an interior rank below A that was caught by s and an interior rank
above A that was caught by s. Follow their actual capture order.

If the lower target was caught first, move left at unit speed until its
first contact, then right at unit speed until contact with the upper
target. The first contact is no later than under the original prefix.
At the original first-contact time, the new right-moving segment is at
least as far right as the first target, by that target's speed bound.
It therefore meets the upper target no later than the original prefix.
The reverse-order argument is identical with directions reversed.

Every accelerated contact remains reachable to center by time t. If the
original target was caught at time r and position p_q(r), then
p_q(r)≤t−r. At an earlier contact r'≤r,

\[
 p_q(r')\le p_q(r)+(r-r')\le t-r'.
\]

In particular these auxiliary routes cannot visit +1: such a contact
could not return to center by t<1. They may touch the center early. That
is an intentional relaxation, and its strict lower rank must be zero.

Letting the two selected ranks approach L_s and M_s proves the following
pointwise width bound, including histories with accumulating turns.
Only two target contacts are compressed; the rest of the original
history is not replaced.

## 2. The two explicit families

For a left-first route, let u be its first-turn time and put

\[
 0\le u\le\min(a,s),\qquad V=2u-a,
\]
\[
 \tau=\min\left(s,\frac{t-a}{2}+u\right),
 \qquad U=a+2(\tau-u).
\]

The latest allowed second contact maximizes the captured width, giving

\[
 C_L(s)=\max_u\left[
 \max\{A,\min(n,R(U,V))\}-R_{\rm strict}(a,V)
 \right].
\tag{1}
\]

At V=a the first turn is at center, so its strict lower trace is zero.
Using closed R(a,a)=Z(a) at that endpoint would miss an allowed branch
of this relaxation.

For a right-first route,

\[
 0\le u\le\min\left(s,\frac{t-a}{2}\right),\qquad U=a+2u,
\]
\[
 \tau=\min(s,U),\qquad V=2(\tau-u)-a,
\]

and

\[
 C_R(s)=\max_u\left[
 \min(n,R(U,-a))-\min\{A,R_{\rm strict}(U,V)\}
 \right].
\tag{2}
\]

Again R_strict(U,U)=0. Set C_2(s)=max(0,C_L(s),C_R(s)). Then every
original prefix satisfies

\[
 \boxed{M_s-L_s\le C_2(s).}
\tag{3}
\]

If initial atoms are allowed, replace the initial upper A in (1) by
A(a), and the initial lower A in (2) by A(a−). The current numerical
adapter uses a continuous initial CDF, so these are equal.

## 3. Moment and rank lifting

The unweighted positive capture moment obeys

\[
 \int_0^n\tau_q^+dq\ge
 J_2(a,t,n):=tn-\int_0^tC_2(s;a,t,n)ds.
\tag{4}
\]

For ranks at least A, C_2 is nondecreasing and one-Lipschitz in n.
Therefore J_2 is nondecreasing, and

\[
 J_2(a,t,N)-J_2(a,t,n)\le t(N-n).
\tag{5}
\]

Combine (5) with the general center rank-removal comparison. For every
N≥n,

\[
 G\ge W(t,N)+\tfrac12J_2(a,t,N).
\tag{6}
\]

The natural common upper record is N_max=R(t,−a): every original
prefix has n≤N_max. Thus any proved lower center boundary B(t,N) gives

\[
 \boxed{G\ge B(t,R(t,-a))+
 \tfrac12J_2(a,t,R(t,-a)).}
\tag{7}
\]

Where the unrestricted center value is the exterior envelope, substitute
B=E_W. Equation (7) removes the record variable from a sufficient
first-arrival verification gate. It is not automatically sharp.

## 4. Complete finite arrangement

For fixed rational (a,t,n), use endpoint light coordinates instead of u.
The left-first region is

\[
 a\le U\le t,\quad -a\le V\le a,\quad U+V\le2s.
\]

Its reward is max(A,min(n,R(U,V)))−R(a,V), together with the separate
strict-center edge V=a. The right-first region is

\[
 a\le U\le t,\quad -a\le V\le U,\quad U+V\le2s,
\]

with reward min(n,R(U,−a))−min(A,R(U,V)), and the strict-center edge U=V.

Split the field triangles at the relevant one-dimensional trace
breakpoints and the rank lines R=A,R=n. Each reward is affine on every
resulting polygon. Its maximum under U+V≤2s is attained either at a
polygon vertex or where U+V=2s meets an edge. A vertex supplies a constant
reward for every later s; an edge supplies an affine reward over its
exact time interval. Their upper envelope is complete.

All coefficients, intersections, and integrations are rational. The
implementation also verifies every candidate below the final envelope
on both endpoints of every positive-length overlap. No time, path, or
turn-count mesh is used.

For a piecewise-affine field, the moment is piecewise quadratic in the
outer parameters on a finite arrangement: polygon normals and reward
gradients are constant on each branch, so candidate time boundaries and
intercepts are affine in those parameters. This observation is useful
for a further finite inequality certificate; no such complete outer
certificate is claimed here.

## 5. Center-free laws and scope

If the ordered radial law has no center atom at any time, every positive
rank path stays strictly positive. Then the two accelerated positive-rank
contacts themselves avoid an early center; the explicit zero-rank
boundary remains harmless. Endpoint absorption is not required anywhere
in this prefix argument.

A center-free law alone does not prove that the entire optimal prefix
has one reversal. The pointwise maximizing order can change with s.
The finite envelope retains this distinction.

## 6. Verification

On the frozen complete CDF, the initial exact suite passes 27 prescribed
multi-turn prefixes, 3,141 pointwise and moment comparisons, and 289,040
candidate/envelope inequalities. It independently checks the actual
running-record function of each unit prefix and confirms that this
relaxation is at least as strong as the earlier shared-coordinate
rectangle bound. A plain rational-field adapter also agrees exactly
with the quadratic-field runtime on a nontrivial fixture.


## 7. An exact suffix compression inside the early constant cone

For the frozen field, R(U,V)=rho U on 0≤V≤U≤1/2. If the first
center time is t≤1/2, let (U0,0) be the first V=0 crossing of the
prefix, with current records L0,M0. Throughout its remaining positive-V
phase, R=rho U is nondecreasing along every admissible path. Therefore
the lower record stays L0 until center, and the upper record is
max(M0,rho U).

Replace that phase by moving outward at unit speed along V=0 to U=t,
then inward at unit speed along U=t to center. This maximizes U at every
intervening time, catches every new upper rank no later, leaves lower
captures unchanged until the same first-center time, and preserves the
final rank max(M0,rho t). Negative copies are unaffected before center.
Thus the replacement pointwise dominates the original completion of
this prefix phase.

This is an exact compression of the phase after V=0, not merely a
pointwise moment relaxation. The arbitrary initial negative-V phase
remains a separate obligation. The claim uses the stated constant-cone
identity and is not imported into a different CDF law without checking
that identity.
