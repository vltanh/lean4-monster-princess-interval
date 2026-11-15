# Early-cone attachment and a finite middle-return bound

## Scope and notation

This is a parameter-level attachment theorem, followed by exact gates for
the immutable field
packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json
(Git blob 5c45d042ee9948faebc03354c3e1e2ee3cbec1a5).

Use the ordered, fairly reflected path law, first-contact conventions,
and center factorization of CENTER_IMBALANCE_FACTORIZATION.md. Write
\(T_t(n)=\int_0^n\beta_t(q)\,dq\) and
\(W(t,n)=V(t,n)+T_t(n)/2\), with \(n\) the balanced captured prefix.
A productive return adds a positive-measure rank band above \(n\).
All statements refer to the normalized center renewal, not to an
unproved finite-turn restriction on an arbitrary initial same-side prefix.

The outside continuation remains an explicit input. In particular this
note does not assume that the center-front value is constant.

## 1. A constant incoming cone

Assume
\[
 R(U,V)=\lambda U,\qquad 0\le V\le U\le h,\qquad
 \lambda>0,\quad \lambda h\le1.                                        \tag{1}
\]
Thus \(Z(t)=\lambda t\) in this cone. Let \(X(t,n)\) denote the immediate
first-exit envelope: one maximal tent returning at \(e\ge h\), followed
by the actual outside continuation, or the closed endpoint alternative.
For an interior return put \(N=\max(n,R(e,t))\); its transformed cost is
\[
 W(e,N)+\frac12[T_t(N)-T_e(n)].                                         \tag{2}
\]
The boundary \(e=h\) is included. A return reaching an endpoint uses the
closed rank one, not an extrapolation of (1).

The first-exit envelope uses the full outside field and its continuation
value. It is not determined by \(\lambda,h\) alone.

### Front states

A front triangle \(t\to e\le h\) has terminal rank \(\lambda e\).
Compared with waiting at the center to \(e\), it costs exactly
\[
 \frac{\lambda}{8}(e-t)^2.                                             \tag{3}
\]
The continuation state is identical. Thus all internal front triangles
can be replaced by waits, and
\[
 \boxed{
 B(t):=W(t,\lambda t)
 =\inf_{s\in[t,h]}X(s,\lambda s).
 }                                                                     \tag{4}
\]
The front is a future running minimum of the exit data. A constant \(B\)
is a possible attachment outcome, not a premise of the theorem.

### Off-front states

For \(\lambda t\le n\le\lambda h\), any productive return wholly inside
the cone lands exactly on a front, since its new rank is \(\lambda e\).
After that return only front waits are needed before the first exit.
An empty prefix before the first productive action can be absorbed into
that tent. A first productive wait is included by taking the limiting
empty return \(e=n/\lambda\).

The exact formula is
\[
 \boxed{
 W(t,n)=\min\left\{
 X(t,n),\
 \inf_{e\in[n/\lambda,h]}
 \left[B(e)+\frac{\lambda}{8}(e-t)^2
             -\frac e2(n-\lambda t)\right]
 \right\}.
 }                                                                     \tag{5}
\]
Indeed
\[
 T_t(\lambda e)=\lambda te+\frac{\lambda}{4}(e-t)^2,\qquad
 T_e(n)=en,
\]
so (5) is exactly (2) at that first internal return.

If \(n\ge\lambda h\), every internal action is empty and
\[
 \boxed{W(t,n)=X(t,n).}                                                 \tag{6}
\]
Empty center waits and empty excursions are absorbed into the first exit.
The maximal tent catches its chosen-side ranks no later, and no surviving
opposite-side rank had been caught during the empty prefix.

These arguments are first made for finite canonical center routes.
Uniform quantile/CDF approximation with a common completion horizon
transfers them to arbitrary histories and possible accumulating returns.
They do not assume an attained first productive event in every
continuous route.

### Consequences for attachment

Equations (4)--(6) remove all within-cone return counts. They leave a
one-dimensional running minimum and one scalar return minimization,
coupled to the actual outside envelope.

If \(B(e)=C\) on the relevant interval, the unconstrained stationary return
is \(e_*=2n/\lambda-t\), and the interior value is
\[
 W(t,n)=C+\frac12(tn-n^2/\lambda),
\]
provided its first-exit competitors and interval gates are satisfied.
This is only the constant-boundary specialization of (5).

For a piecewise quadratic \(B\), each branch in (5) is quadratic in the
return parameter. Branch endpoints and admissible stationary points
give a finite exact transfer. A proved lower outside continuation can
also be substituted to obtain a lower certificate; equality requires
the actual outside value.

## 2. Exact early gate for the saved field

The immutable field satisfies (1) with
\[
 h=\frac12,\qquad
 \lambda=\frac{3521265547}{12500000000},\qquad
 H:=\lambda h=\frac{3521265547}{25000000000}.                             \tag{7}
\]
Every one of the 81 positive-cone triangles has exactly the coefficients
\((R_U,R_V,c)=(\lambda,0,0)\). No unresolved triangle crosses the cutoff.
The verifier also checks 288 off-front action identities, 288
triangle-versus-wait identities, and 48 constant-boundary stationary
identities by direct piecewise-affine first-inverse integration.

The field outside this cone is not declared canonical and is not
replaced by a fitted incoming curve.

## 3. A strict productive-duration gap in the middle strip

At every center visit after \(h=1/2\), the larger captured frontier is at
least \(H\): every radial rank that visited the center by time \(h\) has
at least one reflected copy captured before the monster's current
center visit. The center imbalance factorization therefore starts its
balanced tail at some \(n\ge H\).

For the saved field,
\[
 Z(t)\le H,\qquad \frac12\le t\le a:=\frac78.                            \tag{8}
\]
Thus there are no productive center waits for that balanced tail.

The exact polygon audit proves
\[
 R(e,t)>H,\quad \frac12\le t\le e\le\frac78
 \quad\Longrightarrow\quad
 e-t>\eta,\qquad
 \eta=\frac{3521265547}{358964317046}.                                   \tag{9}
\]
The displayed strict inequality follows because the minimum is on the
closed level \(R=H\); the non-strict duration bound is already sufficient
for the finite count.

To compute the gap, intersect every actual CDF triangle with the middle
cone. Discard triangles whose maximum rank is at most \(H\). On the
remaining triangles impose \(R\ge H\) and minimize the affine form
\(U-V\) at every clipped polygon vertex. The exact minimizer is on
triangle 336 at
\[
 V=\frac9{16},\qquad
 U=\frac{1643509551083}{2871714536368},\qquad R(U,V)=H.
\]
The audit uses 120 clipped triangles, of which 102 have a rank above
\(H\). No numerical rank or coordinate sampling enters (9).

The duration bound implies
\[
 \boxed{\text{at most 38 productive returns wholly inside }
        [1/2,7/8].}                                                    \tag{10}
\]
Their disjoint durations sum to at most \(3/8\), and
\(\lfloor(3/8)/\eta\rfloor=38\). Empty waits and excursions can be
absorbed into the next productive or exit action. In particular there
is no productive Zeno accumulation inside this middle strip.

This is a uniform finite bound for the saved field's normalized center
renewal. It is not a claim that 38 returns are needed or optimal.

## 4. Remaining dependencies

The center problem now separates as follows.

- Before \(1/2\), (4)--(6) are exact in terms of the first-exit data.
- Inside \([1/2,7/8]\), at most 38 productive returns are needed, followed
  by an exit. There are no productive balanced waits there.
- On \([7/8,t_L]\), CENTER_LATE_EXTERIOR.md gives an exact exterior value
  for records above \(n_{\rm crit}(t)\). Below that threshold, the attached
  Riccati/rank-removal expressions remain valid lower boundaries; an exact
  arbitrary-intermediate-state value is not asserted.
- On \([t_L,15/16]\), the exterior continuation is exact for every record.
  Later reachable center states lie above the audited endpoint-tail barrier.

The first-center low-record cost exclusion is an initial-prefix theorem.
It must not be used as a value for a low-record state reached after
earlier center visits.

Thus the saved field has a genuinely finite middle-return optimization
with explicit outside data. Turning this into a sharp global lower
certificate still requires the outside low-record attachment and
arbitrary first-center prefix inequalities. No new interval-game bound
is claimed here.
