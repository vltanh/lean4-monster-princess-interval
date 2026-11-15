# Center waiting followed by two triangles

This is an exact response identity for an ordered radial law with a
constant incoming-density cone. It supplies a convex lower-field
constraint that includes waiting, which is absent from a pool containing
only unit-speed M1/M2/M3 prefixes. It does not establish an unrestricted
guarantee or a matching equilibrium.

## 1. Geometry and assumptions

Use the strict/closed radial CDF conventions of
[POSITIVE_TURN_SHEET.md](POSITIVE_TURN_SHEET.md). All princess paths are
at their signed endpoints by time two. Assume an exact early cone

\[
 R(U,V)=\lambda U,\qquad 0\le V\le U\le\tau,
 \qquad \lambda\ge0.
\]

Choose `0<=s<=tau`, `s<=t<=e`, `e>=1`, with both triangle widths below
two. The monster waits at the center until `s`, makes a negative triangle
returning at `t`, makes a positive triangle returning at `e`, then visits
both endpoints. Its vertices before the endpoint tour are

\[
 (0,0),(s,0),\left(\frac{s+t}{2},\frac{s-t}{2}\right),(t,0),
 \left(\frac{t+e}{2},\frac{e-t}{2}\right),(e,0).
\]

Put

\[
\begin{aligned}
 q&=\lambda s,& B&=R(t,s),&D&=R(e,t),\\
 J_1&=\int_s^t R(U,s)\,dU,&
 J_2&=\int_t^e(R(U,t)-q)_+\,dU.
\end{aligned}
\]

Here `q` is the radial rank caught on both signs during the center wait.
Transport gives `B>=q`. The wait's absolute capture-time contribution is
`lambda*s^2/2=s*q/2`. Both turn CDF values are closed traces. Initially
assume there is no center atom at time one; a correction is given below.

## 2. Exact cost and concavity

If the negative endpoint is visited first, then

\[
\boxed{\begin{aligned}
4C_-={}&4e+8-(2e+2-s-t)B-(2e+6)q\\
       &-(e+6-t)(D-q)_+-J_1-J_2.
\end{aligned}} \tag{1}
\]

If the positive endpoint is visited first, replace the three coefficients
`2e+2-s-t`, `2e+6`, and `e+6-t` by
`2e+6-s-t`, `2e+2`, and `e+2-t`, respectively. Thus

\[
\boxed{\begin{aligned}
4C_+={}&4e+8-(2e+6-s-t)B-(2e+2)q\\
       &-(e+2-t)(D-q)_+-J_1-J_2.
\end{aligned}} \tag{2}
\]

All nonlinear terms are negative positive parts with nonnegative
coefficients. Both costs are concave in the full CDF and can join the
same convex feasibility problem as the other fixed-route costs.

For the first order, an equivalent expression is

\[
\begin{aligned}
4C_-={}&4e+8-(2e+2-s-t)B-(e+6-t)\max(D,q)-2tq\\
       &-\int_s^tR(U,s)\,dU-\int_t^e\max(R(U,t),q)\,dU.
\end{aligned} \tag{3}
\]

This form makes the two outgoing rows explicit. Setting `e=1` gives
the currently used structured response family on the existing CDF mesh.
Neither formula says that all optimal final return times are one.

## 3. Direct capture derivation and the time-one atom

For a more general center-wait prefix, let `q` be the total radial rank
that has visited the center by time `s`, and let `P` be the absolute
capture-time moment of that rank. Define

\[
 X=(B-q)_+,\quad Y=(D-q)_+,\quad b=q+X,\quad c=q+Y,
\]

and use clipped row integrals

\[
 K_1=\int_s^t(R(U,s)-q)_+\,dU,\qquad K_2=J_2.
\]

The first triangle's new negative capture moment is
`[(s+t)X-K1]/2`. The second triangle's new positive capture moment is
`[(t+e)Y-K2]/2`, including immediate center contact at its departure.
The remaining signs have captured ranks `b,c`. Since `e>=1`, every
uncaught endpoint copy is at its endpoint by the first endpoint visit.
The general four-cost before the final center correction is therefore

\[
 4P+(s+t)X+(t+e)Y-K_1-K_2
 +2(e+1)(1-b)+2(e+3)(1-c) \tag{4}
\]

for the negative endpoint first. Reverse `b,c` in the final two terms
for the other endpoint order.

If a center atom at the final return has rank `Z(e)>b`, the negative
copies in that additional rank are caught at time `e`. Formula (4)
then needs the correction

\[
 -2(Z(e)-b)_+
\]

for the negative endpoint first, or `-6(Z(e)-b)_+` when it is second.
The endpoint-by-two condition makes `Z(e)=0` for `e>1`; the explicit
correction is needed at `e=1` if a literal outgoing time-one atom is
allowed. The saved CDF construction sets that atom to zero.

On the exact constant cone, `P=s*q/2` and `B>=q`. Substituting these
facts into (4), and eliminating `K1=J1-(t-s)q`, gives (1) and (2).

## 4. Validation and constructive scope

Run

```bash
python packages/interval_turn_density/verify_wait_two_triangles.py
```

It performs **814 exact Fraction checks**: 360 independent direct
capture comparisons, 22 witnesses requiring the time-one center
correction, and 432 coefficient-elimination checks. The finite fixtures
include multiwave paths, non-unit speeds, and center/endpoint atoms.
The current mesh formula also agreed with generic running signed records
on 64 continuous-parameter routes within `1.8e-12`.

The constant cone has one useful exact consequence: for a balanced
center state, a triangle contained wholly in the cone has excess cost
`lambda*(e-s)^2/8>=0` over center waiting. Such triangles may be
removed. Initial asymmetry, triangles crossing the cone boundary, and
the subsequent curved field remain separate response questions; the
fixed pool in this note does not close them.
