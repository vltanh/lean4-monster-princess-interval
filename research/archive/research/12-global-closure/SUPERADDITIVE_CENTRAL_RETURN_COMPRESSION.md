# Return compression from superadditive central CDF excess

This is a sufficient phase criterion for reducing Monster turns. It
preserves the terminal center time and permits the original future or
its reflection, with the same future turn count. It is not a claim that an unrestricted optimal Princess
has this phase structure, or that its number of phases is bounded.

## 1. Statement and physical hypotheses

Let `F` be the regular signed CDF of a symmetric ordered Princess law.
On the positive half-arena, define its excess over the center value by

\[
 w(U,W)=F((U+W)/2,(U-W)/2)-\frac12.
\]

Thus `w>=0`, it is nondecreasing in `U` and nonincreasing in `W`, and
`w(u,u)=0`. Assume the following interval superadditivity in the region
used below:

\[
 \boxed{w(D,A)\ge w(B,A)+w(D,B)\qquad(A\le B\le D).}       \tag{1}
\]

Every queried interval must lie in the legal arena and the specified
region. This is an additional structural hypothesis on a legal field;
it does not follow from the two transport inequalities alone.

Start at the center at time `t` with surviving negative and positive
records `l,r` in `[0,1/2]`. Consider a positive returning triangle of
height `a>0`, followed by a negative returning triangle of height `b>0`.
Put

\[
 H=a+b<1,\qquad v=2a+b,\qquad T=t+2H.
\]

All legs of these two triangles and of the enlarged positive triangle
of height `H` must remain in the specified region. In particular there
is no endpoint contact. For this pair, (1) is needed with
`A=t,B=t+2a,D=t+2a+2u` for every `0<=u<=b`.
Assume both original peaks actually update their respective records.
With

\[
 w_1=w(t+2a,t),\quad
 w_2=w(T,t+2a),\quad
 w_E=w(T,t),
\]

this means

\[
 r_1=\frac12-w_1<r,\qquad
 l_2=\frac12-w_2<l.                                     \tag{2}
\]

The old exit state at time `T` is `(l_2,r_1)`. The enlarged positive
triangle has the same exit time and center position, and its exit
records are

\[
                     (l,q),\qquad q=\frac12-w_E.          \tag{3}
\]

**Theorem.** Replacing the two original triangles by this one enlarged
triangle, then choosing the cheaper of the old suffix and its reflection
at the terminal center, reduces the whole cost by at least `a w_2>0`.
The future turn count is unchanged, so the prefix has one fewer proper
return. The same
inequality holds for any symmetric increasing concave continuation
function of the two exit records. The theorem does not claim that one
prescribed asymmetric suffix always works without the reflection option.

In particular, the statement applies to equal entry records `l=r=1/2`,
to every equal entry `l=r=s<=1/2` satisfying (2), and to the ordered
heavier-first/balanced states in CENTER_HEAVIER_FIRST_BALANCE.md. The
proof below in fact needs neither an initial order between `l,r` nor
the return-balance inequalities, once both actual updates (2) hold.

## 2. The complete exit-state comparison

The superadditivity hypothesis at the two original center intervals gives

\[
                         w_E\ge w_1+w_2.                 \tag{4}
\]

The new record is consequently no larger than either old record, and
the new total record is no larger than the old total:

\[
 q\le\min\{l_2,r_1\},\qquad
 q+l\le l_2+r_1.                                        \tag{5}
\]

For the second inequality, its exact slack is

\[
 (l_2+r_1)-(q+l)=\frac12-l+w_E-w_1-w_2\ge0.
\]

Here `q>=0` follows from legality of the enlarged peak, and `q<l`
follows from (2) and (4). If `Q` is symmetric, increasing and concave,
choose

\[
                   \lambda=\frac{l_2-q}{l-q}\in[0,1].
\]

The mixture of `(l,q)` and its reflection `(q,l)` with weight `lambda`
on the first vector has mean `(l_2,q+l-l_2)`, whose second coordinate
is at most `r_1`. Thus

\[
 \begin{aligned}
 Q(l,q)
 &=\lambda Q(l,q)+(1-\lambda)Q(q,l)\\
 &\le Q(l_2,q+l-l_2)\\
 &\le Q(l_2,r_1).
 \end{aligned}                                           \tag{6}
\]

The actual center value has these properties: each fixed future path
has a concave increasing running-record cost, the infimum of those
costs remains concave and increasing, and reflection makes it symmetric.
The same argument works with an infimum and near-minimizing futures if
one has not separately invoked response attainment.

### Keeping the old future turn count

There is a more concrete version which does not choose a new optimizing
suffix. Let `H_old(L,R)` be the cost of the actual old future from the
center at time `T`, as a function of its entry records. This function is
concave and increasing, though it need not be symmetric. The same `lambda`
and the same mean-vector comparison give

\[
 \lambda H_{\rm old}(l,q)+(1-\lambda)H_{\rm old}(q,l)
       \le H_{\rm old}(l_2,r_1).                         \tag{6a}
\]

By symmetry of the Princess field, following the reflected old suffix
from `(l,q)` costs `H_old(q,l)`. Thus one of the old suffix and its
reflection, both keeping their original clock times and number of
returns, costs no more than the old continuation. This proves the
physical replacement statement directly, without response attainment.
For the globally normalized responses the suffix already completes its
endpoint tour in a bounded time, so all these record-cost functions are
finite. The optimal-continuation version (6) follows as well.

## 3. Prefix saving when the two entry records are one-half

First take `l=r=1/2`. Define the outgoing captured-rank amounts

\[
 w_0(u)=w(t+2u,t),\qquad
 w_{\rm late}(u)=w(t+2a+2u,t+2a).
\]

They are nondecreasing by transport, and are frozen at their peak values
on their respective returns.

Let `D_0` denote old prefix cost minus enlarged prefix cost. Direct
integration of those captured amounts gives the linear functional

\[
 D_0=\int_a^H w_0(u)\,du-\int_0^b w_{\rm late}(u)\,du
          +Hw_E-(a+2b)w_1-bw_2.                         \tag{7}
\]

Superadditivity gives, for every `0<=u<=b`,

\[
                w_0(a+u)\ge w_1+w_{\rm late}(u).
\]

Together with `w_E>=w_1+w_2`, substitution into (7) yields

\[
 \boxed{D_0\ge bw_1+H(w_1+w_2)-(a+2b)w_1-bw_2
                    =a w_2\ge0.}                       \tag{8}
\]

This accounts for the whole prefix cost, not only its exit records.

## 4. Equal or unequal smaller entry records

Put

\[
                   d_r=\frac12-r,\qquad d_l=\frac12-l.
\]

The captured amount for a clock whose untruncated captured-rank amount
is `z` is `(z-d)_+=z-min(z,d)`. Let `w_E(u)` and `w_1(u)` now denote the
untruncated enlarged and old first-clock histories throughout the prefix.
They agree up to time `a`. Afterward both are at least
`w_1(a)>d_r`: the old first record stays at its peak, and transport
makes the enlarged outgoing record improve further. Hence

\[
                 \min(w_E(u),d_r)=\min(w_1(u),d_r)
                         \quad(0\le u\le2H).             \tag{9}
\]

The first-clock clipping terms cancel **pointwise**. The only remaining
correction to (7) clips the old second clock. Its outgoing amount is
`w_late(u)`, and its peak exceeds `d_l` by (2). Thus the exact saving is

\[
 \boxed{D_{d_r,d_l}
   =D_0+\int_0^b\min\{d_l,w_{\rm late}(u)\}\,du+b d_l
   \ge D_0+b d_l\ge a w_2+b d_l>0.}                      \tag{10}
\]

This proves the prefix comparison for arbitrary entry `l,r` satisfying
(2), not only for equal one-half records. Combining (10) with (6) proves
the theorem. The equal-entry extension therefore needs no new numerical
fixtures or additional shape hypothesis.

## 5. Sufficient field structures

### A nonpositive mixed characteristic derivative

For a smooth field, `w_UW<=0` is sufficient. Indeed, using `w(B,B)=0`,

\[
 \begin{aligned}
 w(D,A)-w(B,A)-w(D,B)
   &=\int_B^D\int_A^B(-w_{UW})(u,v)\,dv\,du\\
   &\ge0.
 \end{aligned}
\]

The same conclusion holds for a continuous field with nonpositive
distributional mixed derivative: apply the rectangle inequality to
interior mollifications and pass to the continuous traces. Since
`4w_UW=F_tt-F_xx`, a sufficient physical-coordinate condition is

\[
                              F_{tt}-F_{xx}\le0.
\]

This wave inequality is additional to transport. A legal CDF is not
assumed to satisfy it automatically.

### Additive characteristic excess

Any legal field with

\[
                         w(U,W)=A(U)-A(W)
\]

satisfies (1) with equality. Here `A` is nondecreasing and all required
CDF range and endpoint constraints must still be satisfied. This class
can be nonlinear in the physical spatial coordinate; spatial affinity
is not required by the theorem.

### Spatially linear density concave in time

Suppose instead

\[
                    F(s,x)=\frac12+\rho(s)x,              \tag{11}
\]

where `rho` is nonnegative, continuous and concave on the required time
interval. The actual field must be legal. In a differentiable part,
transport says `|rho'(s)x|<=rho(s)`.

For adjacent characteristic intervals `[A,B]` and `[B,D]`, their
midpoints have weighted mean `(A+D)/2` with weights proportional to
the interval lengths. Jensen's inequality for `rho` gives

\[
 \frac{D-A}{2}\rho\left(\frac{A+D}{2}\right)
 \ge\frac{B-A}{2}\rho\left(\frac{A+B}{2}\right)
    +\frac{D-B}{2}\rho\left(\frac{B+D}{2}\right).
\]

This is exactly (1). The return-compression theorem therefore applies
throughout every such central-density phase, including arbitrary
unequal entry records satisfying the actual-update conditions.

## 6. An independent kernel proof for the concave-density corollary

The preceding superadditivity proof is sufficient. The following exact
kernel calculation independently checks its concave-density specialization.
Translate the initial time to zero and retain `H=a+b,v=2a+b`. Equation
(7) becomes

\[
\begin{aligned}
 D_0(\rho)={}&\int_a^H u\rho(u)\,du
       -\int_0^b u\rho(2a+u)\,du\\
 &+H^2\rho(H)-(a^2+2ab)\rho(a)-b^2\rho(v).
\end{aligned}                                           \tag{12}
\]

For affine `rho`, direct algebra gives `D_0=ab rho(v)`.

Use the zero-endpoint Green tents on `[0,v]`,

\[
                 G_s(u)=\min\{u,s\}-\frac{us}{v}.
\]

For `K(s)=D_0(G_s)`, exact substitution into (12) gives

\[
 K(s)=0\qquad(0\le s\le a),                              \tag{13}
\]

\[
 K(s)=aH(s-a)+\int_0^b u(2a+u-s)_+\,du
                    -\int_s^H u(u-s)\,du
                    \quad(a\le s\le H),                 \tag{14}
\]

\[
 K(s)=bH(v-s)+\int_0^b u(2a+u-s)_+\,du
                    \quad(H\le s\le v).                 \tag{15}
\]

The last expression is nonnegative. In the middle interval, `K(a)=0`
and

\[
 K'(s)=\frac{3a^2+4ab-s^2+(s-2a)_+^2}{2}>0.             \tag{16}
\]

If `b<=a`, then `H<=2a`, and the numerator at its smallest point
`s=H` is `2a^2+2ab-b^2>0`. If `b>a`, split at `s=2a`; on the second
part the minimum is `3a^2/2` for `K'`, attained at `s=H`, and the first
part has a larger lower bound. Equations (13)--(16) prove `K>=0`.

A continuous concave density is its affine endpoint interpolant plus
a nonnegative superposition of these tents. Equivalently, using the
nonnegative distributional measure `-rho''`,

\[
       D_0(\rho)=ab\rho(v)+\int_0^v K(s)(-\rho''(ds))
                    \ge0.                               \tag{17}
\]

One may avoid any endpoint derivative convention by first proving this
for concave polygonal densities and then using their uniform convergence
to `rho`. The finite evaluation and integral functional (12) is continuous
under that convergence. No smoothness or strict concavity is required.

## 7. Structural scope and the remaining equilibrium question

No exact best response can contain an eligible pair of opposite
record-setting triangles entirely inside such a phase, when the
enlarged triangle also stays in the phase: (2) gives `w_2>d_l>=0`, so
the quantitative saving in (10) is strictly positive. This conclusion
does not require selecting a minimum-count best response. Equation (6a)
also keeps the old suffix or its reflection, hence its exact future
return count, while removing one prefix return. The replacement preserves the terminal
center time, so it does not advance later characteristic contacts. The
future contacts may be reflected. This is the feature missing from a
naive deletion and time advance of the full suffix.

The condition is substantive. In the retained full-width n256 field,
the first two small triangles of the recorded three-return example
have `w_1+w_2>w_E`; the exit-state inequality (4) fails. Its direct
front-preserving compression happens to improve that particular future,
but the universal continuation argument above cannot justify it. Exact
values are recorded in INITIAL_PREFIX_COMPRESSION_DIAGNOSTIC.md.

No assertion here forces an optimal Princess field to satisfy (1), or
its density to be concave in time or linear in space. Nor is a finite
number of suitable regions proved. The theorem supplies a uniform
turn-compression rule **within** an identified region; turning it into
an equilibrium-sufficient finite family still requires that missing
field structure and its attachments.
