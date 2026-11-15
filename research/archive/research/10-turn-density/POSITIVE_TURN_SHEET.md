# Positive-start turn sheets in the lower radial CDF

This note gives exact capture identities for a positive-start monster,
including the negative-characteristic flux that is absent from an ordinary
one-wave lower law. It then solves a capped, indifferent positive-turn
sheet locally. It does **not** construct a globally matched lower law or
prove an unrestricted lower bound.

The independent rational verifier is
[`verify_positive_cdf_sheet.py`](../../packages/interval_turn_density/verify_positive_cdf_sheet.py).
The corresponding upper-density construction is in
[`TWO_SIDED_LATE_RESPONSE.md`](TWO_SIDED_LATE_RESPONSE.md); its separate
verifier concerns the upper response comparison.

## 1. Paths, traces, and the monster route

Let `q` be uniform on `[0,1]`, and let `p_q(t)` be an ordered family of
nonnegative, 1-Lipschitz paths with `p_q(t)=1` for `t>=2`. Give each path
an independent fair reflection. Ordering means that `p_q(t)` is
nondecreasing in `q` at every time. The following identities also apply
to a finite weighted ordered family.

Use light coordinates

\[
 U=t+r,\qquad V=t-r,\qquad
 R_{<}(U,V)=\Pr\{p_q((U+V)/2)<(U-V)/2\},
\]

and define `R_le` with `<=` in place of `<`. Both traces are needed for
atomic laws. Write

\[
 A(z)=\Pr\{p_q(0)<z\}.
\]

Thus an initial-position atom at `a=z` is excluded from `A`. It is
captured at time zero and belongs in the outward first-inverse term
below. For a continuous initial distribution this distinction disappears.

Fix `0<z<1` and `z<=s<=2-z`. The positive-start monster follows

\[
 (0,z),\quad ((s-z)/2,(s+z)/2),\quad (s+1,-1),\quad(s+3,1).
\]

Call its expected capture time `C_+(s,z)`. The first turn lies on `U=s`.
The line strategy is `C_g(z)=C_+(1,z)`. The endpoint strategy is
`C_f(z)=C_+(2-z,z)`; its final leg is unnecessary, because all paths
have already been caught.

For this fixed `z`, abbreviate `A=A(z)` and set

\[
\begin{aligned}
 B(s,z)&=R_{\le}(s,-z),\\
 I(s,z)&=\int_z^s R_{\le}(U,-z)\,dU,\\
 F(s,A)&=\int_{-z}^s (A-R_{<}(s,V))_+\,dV,\\
 H(s)&=\int_s^{s+2}R_{\le}(U,s)\,dU.
\end{aligned}
\]

The horizontal integral `F` uses the **strict** radial trace. The turn
value `B`, the vertical integral `I`, and the outgoing integral `H` use
the **closed** trace. In particular, at the endpoint turn `s=2-z`,
`B=1`, even when the interior limit of that CDF is smaller.

## 2. Exact positive-turn capture formula

For every law above,

\[
\boxed{\quad
4C_+(s,z)=(4+2A)s+8-(6+s+z)B(s,z)-I(s,z)-F(s,A)-H(s).
\quad} \tag{1}
\]

Here is a direct first-capture derivation. Let

\[
 \alpha_q(s)=\inf\{t:t+p_q(t)\ge s\},\qquad
 \beta_q(v)=\inf\{t:t-p_q(t)\ge v\}.
\]

For the positive reflection, the ranks below `A` are caught on the
return leg at `alpha_q(s)`. The ranks from `A` through `B` are caught
on the first outward leg at `beta_q(-z)`. The remaining ranks are
caught at time `s+3`. Monotonicity of the two light coordinates gives

\[
\begin{aligned}
 \int_0^A\alpha_q(s)\,dq&=sA-\tfrac12F(s,A),\\
 \int_A^B\beta_q(-z)\,dq&=\tfrac12(s-z)B-\tfrac12I(s,z).
\end{aligned}
\]

The negative reflection is caught at `beta_q(s)`, with

\[
 \int_0^1\beta_q(s)\,dq=s+1-\tfrac12H(s).
\]

Adding these contributions and dividing by two proves (1). Strictness
in `F` records the **first** contact with a horizontal incoming plateau
`U=s`; using a closed trace there would retain that rank until the end
of the plateau.

For `s>1`, the endpoint-by-two assumption forces `H(s)=0`. At `s=1`,
`H(1)` can be positive: a path may already follow the outgoing line
`V=1` before time two. This term must be retained for such an atomic
fixture. A law with no positive mass following `V=1` has `H(1)=0`.

At the endpoint turn, (1) therefore reduces to

\[
 \boxed{\quad
 4C_f(z)=8-4z+2(2-z)A-I(2-z,z)-F(2-z,A).
 \quad} \tag{2}
\]

The restriction `z<1` matters when taking endpoint limits. One must
not replace the exact start `z=1` by a limit without checking initial
and outgoing atoms.

## 3. The missing negative-row flux in `C_f-C_g`

Put

\[
 E(z)=1-R_{\le}(1,-z),\qquad s_*=2-z,
\]

and define the two nonnegative flux moments

\[
\begin{aligned}
 Q_{\rm low}(z)
   &=(s_*-1)A-[F(s_*,A)-F(1,A)],\\
 Q_{\rm neg}(z)
   &=\int_1^{s_*}[R_{\le}(U,-z)-R_{\le}(1,-z)]\,dU.
\end{aligned} \tag{3}
\]

The first definition is valid with atoms and first-inverse plateaus.
Equivalently, for `V_q(U)=2 alpha_q(U)-U`,

\[
 Q_{\rm low}(z)=\int_0^{A(z)}[V_q(2-z)-V_q(1)]\,dq.
\]

Subtracting (1) at `s=1` from (2) gives the exact identity

\[
\boxed{\quad
4(C_f-C_g)=(1-z)(A+2)-(6+2z)E
                 +Q_{\rm low}-Q_{\rm neg}+H(1).
\quad} \tag{4}
\]

The sign of `Q_neg` is **negative**. A post-`U=1` incoming wave on a
negative `V` row changes this identity even if its ranks lie above
`A(z)` and therefore contribute nothing to `Q_low(z)`. Omitting this
term gives an incorrect activation boundary for that extra-wave phase.

For a continuous field with no incoming atom on the sampled row, put

\[
 J_+(s,A)=\int_{-z}^s
       \mathbf 1_{\{R(s,V)<A\}}R_U(s,V)\,dV.
\]

On the interior `1<s<2-z`, differentiating the first-inverse formula
gives `F_s=A-J_+`, and hence

\[
 \boxed{\quad
 4\partial_sC_+=4+A-2R(s,-z)-(6+s+z)R_U(s,-z)+J_+(s,A).
 \quad} \tag{5}
\]

In this smooth setting, `Q_low=integral_1^(2-z) J_+(s,A) ds`.
The exact finite-trace definition (3) should be used when a smooth
derivative does not exist.

### Early turns retain the center and outgoing-row terms

Formula (1) also holds for `z<=s<1`. Its early derivative is different
from (5). Put `Z(s)=R(s,s)` and keep the integral defining `J_+` above.
The moving upper limit in `F` gives

\[
 F_s=(A-Z(s))_+-J_+(s,A).
\]

Consequently, with
`J_total(s,A)=min(A,Z(s))+J_+(s,A)`, the exact smooth early derivative is

\[
 4\partial_sC_+=4+A+J_{\rm total}(s,A)-2B
       -(6+s+z)B_s-H'(s). \tag{5a}
\]

In particular, omitting `H` or the center term does not give the turn
indifference equation of the complete early field. If the early row is
indifferent and is anchored by its value `B(1,z)`, write
`L0=7+z`, `W=6+s+z`, and
`K_+=(2+A/2-B(1,z))L0^2`. Integrating (5a) gives

\[
\begin{aligned}
 B(s)=2+\frac A2-\frac{1}{W^2}\bigg[&K_+-L_0H(1)+WH(s)
       +\int_s^1H(r)\,dr\\
       &+\int_s^1(6+r+z)J_{\rm total}(r,A)\,dr\bigg].
 \tag{5b}
\end{aligned}
\]

The term `-L0 H(1)` preserves the anchor even when a literal outgoing
`V=1` atom is present. This is an implicit source equation coupled to
the rest of the field, not a proof that every early turn is active or
that the resulting row has a legal transport cone.

## 4. A positive-start indifferent sheet on negative `V`

Suppose all post-`U=1` incoming ranks in the patch lie above `A(z)`.
Then `J_+=0` there. If the positive-turn cost is independent of `s`,
(5) becomes

\[
 (6+s+z)R_U(s,-z)+2R(s,-z)=4+A(z).
\]

Anchoring at `R(1,-z)=1-E(z)` gives

\[
\boxed{\quad
R(s,-z)=2+\frac{A(z)}2
 -\frac{K_+(z)}{(6+s+z)^2},\qquad
K_+(z)=\left(1+\frac{A(z)}2+E(z)\right)(7+z)^2.
\quad} \tag{6}
\]

This is a local incoming CDF, not a prescription to put all returning
ranks on one light line. A common second incoming line would create an
atomic capture advantage for a monster that moves its turn to that line.

### Transport and the exact cone test

Write `B(s,z)=R(s,-z)`, `rho=A'(z)`, `W0=7+z`, `W=6+s+z`, and
`Dp=1+A/2+E`. Then

\[
\begin{aligned}
 B_s&=\frac{2D_pW_0^2}{W^3}>0,\\
 B_z&=\frac{\rho}{2}\left(1-\frac{W_0^2}{W^2}\right)
       -E'\frac{W_0^2}{W^2}
       -\frac{2D_pW_0(s-1)}{W^3}.
\end{aligned} \tag{7}
\]

The light-coordinate cone is `R_U>=0, R_V<=0`; on this negative row
it is exactly `B_s>=0, B_z>=0`. Along a nondegenerate quantile, these
inequalities give a path speed between `-1` and `1`.

A sufficient condition is

\[
 E'\le0,\qquad \rho/2\ge D_p/(7+z).
\]

It is not necessary. An exact test over a whole sheet interval follows
from `K=Dp W0^2`:

\[
 W^3B_z=\frac{\rho}{2}W^3-K'W+2K. \tag{8}
\]

For `rho>=0`, the right side is convex as a function of positive `W`.
Check the two endpoints and, when it lies inside the interval, the
stationary point `W=sqrt(2K'/(3rho))`. If `rho=0`, the expression is
linear. This retains the actual transport condition instead of imposing
an unnecessary lower bound on the initial density.

## 5. Capping the sheet and matching the endpoint turn

Let `d>=0` be the mass of the ordinary terminal negative-outgoing tail.
Assume, on a start band under consideration, that the sheet reaches
the constant interior cap

\[
 P=1-d
\]

at `s=v(z)` and then remains at that cap until the endpoint turn
`s_*=2-z`. Thus the extra returning rank mass on this row is `E-d`.
Set

\[
 L=1+A/2+d,\qquad D_p=L+E-d.
\]

The cap equation in (6) gives

\[
 v=1+(7+z)\left(\sqrt{D_p/L}-1\right). \tag{9}
\]

When `v<=2-z`, the exact negative-row moment is

\[
\begin{aligned}
 Q_{\rm neg}
  &=\frac{D_p(v-1)^2}{6+v+z}+(E-d)(2-z-v)\\
  &=(E-d)(1-z)-(7+z)(\sqrt{D_p}-\sqrt L)^2.
\end{aligned} \tag{10}
\]

More generally, if the endpoint is reached before the cap, replace `v`
in the first fraction by `min(v,2-z)` and replace the second factor
`2-z-v` by its positive part.

Assume now `Q_low=H(1)=0` for these starts. Equality of the positive
line and endpoint strategies is (4) with zero left side. Define

\[
 S=\frac{(1-z)(A+2+d)}{7+z}.
\]

Substitution of (10) reduces the equality to

\[
 2\sqrt L\left(\sqrt{L+E-d}-\sqrt L\right)=S-d.
\]

Consequently the positive branch is explicit:

\[
\boxed{\quad
 E=S+\frac{(S-d)^2}{4L},\qquad
 v=1+\frac{(7+z)(S-d)}{2L}
   =2-z-\frac{8d}{A+2+2d}.
\quad} \tag{11}
\]

The branch condition is

\[
 0\le d\le\frac{(1-z)(A+2)}{6+2z},
\]

equivalently `S>=d`. The initial-rank separation also requires
`E<=1-A`. If `d>0`, (11) puts the exit strictly before the endpoint;
if `d=0`, the sheet reaches the endpoint.

This solves the whole one-turn cost comparison for the fixed start:

* On `1<=s<=v`, (6) makes `C_+(s,z)=C_g(z)`.
* On `v<s<2-z`, `4 partial_s C_+=2+A+2d>0`.
* At `s=2-z`, the closed CDF jumps from `1-d` to `1`, decreasing
  the four-cost by `8d`.

The excess just before that jump is

\[
 (2+A+2d)(2-z-v)=8d,
\]

so the endpoint strategy returns to exactly the line value. This is
an exact local response validation; it does not compare monsters with
additional turns or establish a common value across different starts.

For constant `d`, differentiating the cap identity gives

\[
 v'=-1+\frac{8d\rho}{(A+2+2d)^2},\qquad
 B_z(v,z)=-B_s(v,z)v'.
\]

Thus the upper-edge cone test is `d rho<=(A+2+2d)^2/8`; the lower-edge
test is `-E'>=0`. An interior minimum in (8) must still be checked.

### A varying cap with flux from the other sheet

The cap need not have the same rank at every start. Write `d=d(z)` and
let `J(s)=J_+(s,A(z))` retain all other incoming flux below the initial
rank, including flux inside the active positive-turn interval. For each
fixed start define

\[
 L_0=7+z,\quad W=6+s+z,\quad
 D=1+A/2+E,\quad L=1+A/2+d,\quad T=2L,
 \qquad T_J(s)=\int_1^s(6+r+z)J(r)\,dr.
\]

Equation (5) gives the exact indifferent row

\[
 B(s)=2+\frac A2-\frac{D L_0^2-T_J(s)}{W^2}.
 \tag{11a}
\]

If this row reaches the interior cap `1-d` at `v`, the cap relation is
`D L0^2=L(6+v+z)^2+T_J(v)`. On the remaining interval before the
endpoint turn, the four-cost derivative is `T+J(s)`. The closed endpoint
jump still removes `8d`. Therefore cap-to-endpoint indifference is
equivalent to the scalar equation

\[
 \boxed{\displaystyle
 T(2-z-v)+\int_v^{2-z}J(r)\,dr=8d.}
 \tag{11b}
\]

For nonnegative flux its left side has derivative `-T-J(v)<0`, so there
is at most one exit. An exit in `[1,2-z]` exists exactly when
`T(1-z)+integral_1^(2-z) J>=8d`. Once that exit is chosen,

\[
 \boxed{\displaystyle
 E=d+L\left[\left(\frac{6+v+z}{L_0}\right)^2-1\right]
       +\frac{T_J(v)}{L_0^2}.}
 \tag{11c}
\]

These identities are pointwise in `z` and permit a varying final cap.
They do not assume that the other sheet's flux occurs only after the
active interval. Direct integration of (11a), followed by the constant
cap, gives the useful check

\[
 Q_{\rm neg}=2L(6+v+z)-2D L_0+8(D-L)+\int_1^v J(r)\,dr.
 \tag{11d}
\]

Substituting this expression into (4), with
`Q_low=integral_1^(2-z) J` and `H(1)=0`, reproduces (11b).
The conditions `0<=E<=1-A`, monotonicity of the cap, the full transport
cone, attachments, and equality with the other monster families remain
separate requirements. A flux and cap that satisfy this local algebra
are not by themselves a completed ordered CDF.

## 6. Corrected boundary and mass closure for the extra branch

Suppose the positive sheet occupies starts `z` in `[b,beta]`. The
ordinary terminal tail has mass `d` and first outgoing coordinates
`c<=-beta`. An extra-wave branch supplies the ranks whose first
outgoing coordinates run through `[-beta,-b]`. Its total mass is

\[
 m_{\rm extra}=E(b)-d.
\]

At the upper edge,

\[
 E(\beta)=d,\quad v(\beta)=1,\quad
 d=\frac{(1-\beta)(A(\beta)+2)}{6+2\beta}. \tag{12}
\]

At the lower edge, `E(b)` is given by (11), not by the ordinary-wave
formula `(1-b)(A(b)+2)/(6+2b)`. If there are no further first-outgoing
coordinates in `(-b,0)`, `E` is constant below `b`; this is the value
that must be used while solving a preceding positive-`g`-only branch.
The two free boundaries `b` and `beta` have different roles and should
not be identified.

There is also an explicit low-branch differential equation. Regard
`d` as constant and differentiate (11) with respect to `A` and `z`:

\[
\begin{aligned}
 S_A&=(1-z)/(7+z),&
 S_z&=-8(A+2+d)/(7+z)^2,\\
 E_A&=S_A\left(1+\frac{S-d}{2L}\right)
                -\frac{(S-d)^2}{8L^2},&
 E_z&=S_z\left(1+\frac{S-d}{2L}\right).
\end{aligned} \tag{13}
\]

Assume the low initial rank `A(z)` has first incoming coordinate
`u_low=z` and first outgoing coordinate `c_low`. Let `u_T` be the
actual first incoming coordinate of the rank `1-E(z)`. Positive-line
start indifference is

\[
 (1+c_{\rm low})\rho=1-A-E-(8+z-u_T)E'.
\]

Writing `B0=8+z-u_T` and `Q0=1+c_low`, it becomes

\[
 \boxed{\quad
 \rho=\frac{1-A-E-B_0E_z}{Q_0+B_0E_A}.
 \quad} \tag{14}
\]

Equation (14) is a boundary-system component, not a closed solver by
itself. The upper response conditions and global quantile matching
must supply `c_low` and the extra branch's **actual** `u_T`. The mass
`E(b)` cannot be replaced by the ordinary terminal mass `d`, because
the extra ranks already contribute to the earlier line strategy.

## 7. Both post-incoming sheets feed the terminal tail

For an initial position `a` near one, the negative row `V=-a` lies
outside a finite positive-sheet start band, so `Q_neg(a)=0`. However,
`Q_low(a)` includes every post-`U=1` incoming rank below `A(a)`, on
both positive and negative `V`. If the relevant flux has a smooth
limit, write

\[
 Q_{\rm low}(1-\varepsilon)=J_0\varepsilon+q_2\varepsilon^2
                                  +o(\varepsilon^2).
\]

For patches whose ranks stay bounded away from one, their contributions
to `J0` are their right incoming fluxes integrated over `V`. In
particular, (6) contributes

\[
 J_0^{\rm positive\ start}
 =\int_b^\beta\frac{2(1+A(z)/2+E(z))}{7+z}\,dz.
\]

A negative-start late sheet
`R(U,z)=2-A(z)-K_-(z)/(6+U-z)^2`, anchored at `C(z)=R(1,z)`,
contributes

\[
 J_0^{\rm negative\ start}
 =\int_{\text{active positive-}V\text{ rows}}
       \frac{2(2-A(z)-C(z))}{7-z}\,dz.
\]

Other post-incoming patches must also be included. Their support and
the initial-rank cutoff must be checked before replacing the full
`J_+` integral by these expressions. The coefficient `q2` also includes
the motion of sheet exits; it is not determined by one pointwise row
derivative alone.

Under the additional terminal-branch hypotheses used in the ordinary
tail balance—simultaneous positive `f/g` and negative endpoint-strategy
indifference, no initial endpoint atom, and no late excursion of the
terminal ranks themselves—put

\[
 D(\varepsilon)=1-A(1-\varepsilon),\quad
 w(\varepsilon)=1+c(1-\varepsilon),\quad
 \eta(\varepsilon)=1-u(1-\varepsilon).
\]

The conditional leading balance is

\[
 D\sim D_0\sqrt\varepsilon,\quad
 D_0=(3+J_0)/2,\qquad
 w\sim4\sqrt\varepsilon,\qquad
 \eta\sim\varepsilon^2/16. \tag{15}
\]

For the incoming coefficient in (15), the full omitted correction in
the differentiated negative endpoint-strategy equation must also be
`o((1-z)^(-1/2))` at its delayed argument `z=u(1-epsilon)`. In
particular, if `Omega(z)` is the additive four-cost correction caused
by lower-rank curved prefixes, require
`Omega'(z)=o((1-z)^(-1/2))`, or require it to vanish on a terminal
interval. A lower-rank incoming flux that violates this condition can
change the leading incoming balance, even when the terminal ranks have
an ordinary suffix.

Thus a no-late terminal history with coefficient `3/2` cannot simply
be reused once a global post-incoming field is present.

For completeness, the formal normalized correction series below
relative order `sqrt(epsilon)` is unchanged. With
`theta_n=(1-2^(-n))/2`, `d_0=1`, its coefficients satisfy

\[
 d_n=-\frac{16^{\theta_n}}{4(1+\theta_n)}d_{n-1},\qquad
 k_n=-(1+2\theta_n)d_n.
\]

Writing the particular relative-`sqrt(epsilon)` terms in `D` and `w`
as `d_*` and `k_*`, respectively, the formal equations give

\[
 3d_*-k_*=\frac1{10}+\frac{2q_2}{D_0},\qquad
 k_*+2d_*=\frac9{25},
\]

and therefore

\[
 d_*=\frac{23}{250}+\frac{2q_2}{5D_0},\qquad
 k_*=\frac{22}{125}-\frac{4q_2}{5D_0}.
\]

The incoming correction remains
`eta=(epsilon^2/16)(1+sqrt(epsilon)/15+...)` only when the omitted
terms in the negative endpoint-strategy balance are small enough at
the delayed incoming front. For example, a bounded remainder suffices;
the **full** omitted derivative correction, including any `C'(u)`
and curved-prefix `Omega'(u)` contributions, must be
`o((1-u)^(-1/4))` at this order, or must be retained explicitly.
These are conditional formal balances, not a uniqueness or convergence
theorem for a global tail. Homogeneous corrections at the accumulation
order and outer matching data remain possible.

## 8. Fixed-parameter audit of the earlier local continuation

The earlier local `C>0` continuation was constructed with an ordinary
no-extra terminal history and the old boundary equation without
`Q_neg`. It is a useful local attachment diagnostic, but it cannot be
turned into a global law merely by appending (6). Its saved boundary
data were

| Quantity | Fixed diagnostic value |
|---|---:|
| Positive-`f` activation `b` | 0.5 |
| Initial CDF `A(b)` | 0.14479760204237943 |
| End of the ordinary negative-outgoing branch `beta` | 0.5464834743541831 |
| Ordinary terminal mass `d` | 0.13569896898056544 |
| Old constant negative-row deficit `E(b)` | 0.1531998287175268 |

Holding these inputs fixed, (11) gives the corrected entry values

\[
\begin{aligned}
 E(b)&\simeq0.15208831632399608,\\
 E(b)-d&\simeq0.016389347343430644,\\
 v(b)&\simeq1.050702029752548,\\
 Q_{\rm neg}(b)&\simeq0.007780586753217245.
\end{aligned}
\]

There is a separate mass-closure failure at the upper edge. Equation
(12), with that same `beta` and `d`, forces

\[
 A(\beta)=\frac{(6+2\beta)d}{1-\beta}-2
          \simeq0.12232244587409635.
\]

This is smaller than `A(b)` by approximately `0.0224751562`, although
`beta>b`; it violates monotonicity of the initial CDF. Even before
integrating the new low-branch equation, a necessary condition at this
fixed `beta` is

\[
 d\ge\frac{(1-\beta)(A(b)+2)}{6+2\beta}
      \simeq0.1371360058104978.
\]

This audit concerns those fixed diagnostic inputs. It does not exclude
the sheet geometry, and the corrected entry values are not a refitted
candidate. A self-consistent construction must change the phase
parameters and terminal history together with both contributions to
`J0`, the low initial CDF, and the extra branch's incoming map. The
earlier local continuation should therefore remain labelled as a
no-extra diagnostic rather than a completed lower strategy.

## 9. What the exact verifier establishes

Run from the repository root:

```bash
python packages/interval_turn_density/verify_positive_cdf_sheet.py
```

It performs **4,895 exact Fraction checks**, including:

* 500 comparisons of (1), including 234 early turns, against direct intersections with reflected
  piecewise-linear paths, including multiple waves and non-unit speeds;
* 36 checks of (4), with seven cases having nonzero `Q_neg`;
* 52 cases where replacing the strict incoming trace changes the answer,
  28 where the closed endpoint trace is essential, and 13 where omitting
  `H(1)` changes the answer; another 173 early cases require the full `H(s)` term;
* exact cap and endpoint matching with nonzero affine flux from the other sheet;
* exact cap, exit, boundary, endpoint-jump, transport, and derivative
  identities for rational sheet parameters.

The algebraic sheet checks verify the formulas and local cone tests.
They do not prove that these local patches can all be attached to one
ordered global law. A completed candidate still requires consistent
initial and outgoing quantiles, both post-incoming sheets, the extra
branch's mass and incoming map, an absolute common capture value,
matching upper response conditions, and an unrestricted monster
verification.
