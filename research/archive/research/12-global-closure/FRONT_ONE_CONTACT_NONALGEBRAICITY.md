# Front-one contacts and a nonalgebraic endpoint trace

This is a conditional obstruction to an algebraic phase ansatz. Assume
the Princess field is completed outward on `t+|x|=1`, and that the
endpoint sweep, positive-start principal turn, and positive-start
endpoint-first families all have one common cost on a neighborhood of
the positive endpoint. Then its initial CDF cannot be an algebraic
function there. In fact it cannot have a convergent Puiseux expansion
with any fixed exponent denominator.

The front-one restriction and these simultaneous contact hypotheses
have **not** been established for the unrestricted equilibrium. This
does not exclude algebraic game values, algebraic strategies with a
different contact pattern, a finite description by nonalgebraic
functions, or a uniformly certified approaching family. It identifies
a concrete obstruction within one candidate phase model.

There is also a response-family exclusion that needs no flat-contact
assumption: within the front-one class at a specified security floor,
positive endpoint-first S rows sufficiently near the center are strictly
dominated by principal P rows. Conversely an all-positive-start common
P/S contact model has an explicit sweep upper below the certified game
lower. These conclusions do not exclude a common phase confined near
the endpoint.

## 1. Field and physical conventions

Use the regular symmetric ordered CDF conventions of
`BULK_CONTACT_AND_CUSP_EQUATIONS.md`. Endpoints are sticky; actual
endpoint capture resets its survivor clock. Set

\[
 \mathcal F(U,W)=F((U+W)/2,(U-W)/2),\quad
 f(a)=F(0,a),\quad K(W)=\mathcal F(1,W),\quad k(a)=K(-a).
\]

Assume maximal outward continuation after the incoming front one,
without an atom lingering at that front. On the positive half-arena,
for `U>=1`, this gives `mathcal F(U,W)=K(W)` when `W<=1`, and
`F=1/2` when `W>=1`. Signed reflection determines the negative side.
In particular every interior point in the late central cone has CDF
one-half. This assertion concerns interior traces; actual endpoint
values continue to use the stopping convention.

For `0<a<1`, let `P(a,1)` start at `a`, turn right-to-left on `U=1`,
then visit `-1` at time two and `+1` at time four. Let `S(a)` go
directly to `+1` at time `1-a`, then to `-1`. Write

\[
 I(a,b)=\frac12\int_a^b\mathcal F(U,-a)\,dU,\qquad
 H_b(s)=\int_0^{b+1}\min\{s,F(t,b-t)\}\,dt,\quad H=H_1.
\tag{1}
\]

The exterior part of the auxiliary moment uses `F=1`, as in the bulk
note. Its exact physical identities are

\[
 C_P(a,1)=4-I(a,1)-\frac{7+a}{2}k(a)+H(f(a)),
\]
\[
 C_S(a)=1-a-I(a,2-a)+H_{2-a}(f(a)).
\tag{2}
\]

## 2. An exact positive-start contact relation

Put `sigma=1-a`. Outward completion gives

\[
 I(a,2-a)=I(a,1)+\frac{\sigma}{2}k(a).
\tag{3}
\]

The moment for the later descending front has an exterior contribution
`sigma*f(a)`. On the physical sweep it uses `K(W)` up to `W=1`, and
one-half afterwards. In the original front moment, the omitted initial
interval `-1<=W<=-a` has `K(W)>=k(a)>=f(a)` by transport. Therefore

\[
 H_{2-a}(f(a))-H(f(a))
             =\frac{\sigma}{2}f(a)+\frac{\sigma}{4}.
\tag{4}
\]

Subtraction in (2) proves, for every interior positive start,

\[
 \boxed{C_S(a)-C_P(a,1)
 =-4+\frac54(1-a)+(3+a)k(a)+\frac{1-a}{2}f(a).}
\tag{5}
\]

No equal-cost hypothesis was used in (5). If both families have the
same cost, it becomes the exact trace relation

\[
 \boxed{k(a)=\frac{11+5a-2(1-a)f(a)}{4(3+a)}.}
\tag{6}
\]

As a separate check, for `-1<a<0` one has `f(a)<=1/2`,
`H(f(a))=2f(a)` and `H_{2-a}(f(a))=(3-a)f(a)`. The corresponding
identity is

\[
 C_S(a)-C_P(a,1)=-(3+a)+(3+a)k(a)+(1-a)f(a).
\tag{7}
\]

The hypotheses below only use positive starts. Endpoint-start and
interior endpoint-limit rows must remain distinct when endpoint atoms
are present.

### A quantitative restriction on possible contact starts

The endpoint sweep has cost `C_E=H(1)`. Its front CDF is at most one
before time `(1-a)/2`, at most `k(a)` between that time and one, and
exactly one-half between times one and two. Thus

\[
 C_E\le1-\frac a2+\frac{1+a}{2}k(a).
\tag{7a}
\]

If `C_S(a)<=C_P(a,1)`, (5) and `f(a)>=1/2` give

\[
 k(a)\le\frac{5+3a}{2(3+a)},\qquad
 C_E\le B(a):=\frac{a^2+6a+17}{4(a+3)}.
\tag{7b}
\]

Here `B` is strictly increasing, since
`B'(a)=(a^2+6a+1)/(4(a+3)^2)>0`. More generally, if `C_E>=c`,
substitution of the lower bound on `k(a)` from (7a) into (5) proves

\[
 \boxed{C_S(a)-C_P(a,1)
       \ge\frac{2(3+a)}{1+a}\,[c-B(a)].}
\tag{7c}
\]

Consequently, for any front-one candidate with sweep cost at least
`c>219/154`, all S rows with `0<a<=1/7` are strictly dominated by
their P rows, because `B(1/7)=219/154`. It is enough to impose the
sweep floor and the corresponding P lower constraints when discarding
these S rows; a full security theorem is not assumed to derive (7c).

If `C_S(a_j)<=C_P(a_j,1)` along a sequence `a_j` decreasing to zero,
(7b) gives `C_E<=17/12`. This is already below the certified global
lower. In particular, simultaneous flat P/S contacts on **all** positive
starts cannot describe an unrestricted optimal Princess, even if one
allows arbitrary nonalgebraic initial fields.

For a whole interval of such comparisons, `a_0<=a<1`, integration of
the stronger pointwise front bound in (7b) yields

\[
 \boxed{C_E\le1+\frac2{3+a_0}
                         -\log\frac4{3+a_0}.}
\tag{7d}
\]

Indeed, integrate `k(a)<=3/2-2/(3+a)` on `[a_0,1]` for the first
part of the front and use its value at `a_0` for the remaining part.
If the comparison holds for every positive start, its limiting upper
is `5/3-log(4/3)`. The single-start rational bound (7b) applies under
weaker hypotheses and is sufficient for the stated support exclusion.

For a concrete tail-phase exclusion, taking `a_0=1/3` in (7d) gives

\[
 C_E\le\frac85+\log\frac56
 \le\frac85-\frac16-\frac1{72}
 =\frac{511}{360}.
\tag{7e}
\]

The middle inequality is `log(1-u)<=-u-u^2/2` at `u=1/6`.
This rational upper is below even the retained n256 global lower.
Therefore a common P/S contact interval reaching the endpoint cannot
extend throughout `(1/3,1)` in a globally optimal front-one candidate.
Its left endpoint must be larger than one-third, or it must contain
an inactive gap. This is distinct from the weaker-hypothesis single-start
exclusion (7c).

## 3. The endpoint slope is fixed

Assume for all sufficiently small `x>0` that

\[
 C_P(1-x,1)=C_S(1-x)=C_E=V_0.
\tag{8}
\]

Here `V_0` denotes the common row cost, not a claim about the unrestricted
game value. Define

\[
 r(x)=1-f(1-x),\qquad
 A(t)=F(t,1-t)=K(2t-1),\qquad \delta(t)=1-A(t).
\]

The endpoint jump in the bulk identity, or the endpoint contact
argument in `ENDPOINT_SQUARE_ROOT_CONTACT.md`, implies no initial
positive endpoint atom under (8); thus `r(x)->0`. Equations (6) and (8)
give the exact functional relation

\[
 \boxed{\delta(t)=\frac{t[3-2r(2t)]}{8-4t}.}
\tag{9}
\]

Consequently

\[
 \delta(t)=\lambda t+o(t),\qquad \lambda=\frac38.
\tag{10}
\]

The reviewed endpoint theorem, applied to the sweep/principal contacts,
then yields

\[
 \boxed{r(x)\sim c\sqrt{x},\qquad c=2\lambda=\frac34.}
\tag{11}
\]

For clarity the exact moment identity needed below is also recorded.
Let `D(y)=H(1)-H(1-y)` and `I_x=I(1-x,1)`. Then

\[
 D(r(x))=4\delta(x/2)+\frac{x}{2}A(x/2)-I_x,
\quad
 0\le\frac{x}{2}A(x/2)-I_x\le\frac{x}{2}r(x).
\tag{12}
\]

Inserting (9) and (11) gives

\[
                  D(r(x))=2\lambda x+O(x^{3/2}).
\tag{13}
\]

Thus all terms of order below `x^(3/2)` in this identity are independent
of the unresolved two-dimensional initial attachment.

## 4. No fixed-denominator Puiseux trace

Suppose, for contradiction, that `r` has a convergent Puiseux series
near zero with one fixed denominator. In view of (11), its derivative
satisfies `r'(x)=O(x^(-1/2))`. Differentiating (9) gives
`delta'(t)=lambda+O(sqrt(t))>0` on a sufficiently small interval. Write
`tau` for its local inverse. The front is nonincreasing everywhere by
transport, so for small `y>0` the front moment has exactly the layer-cake
representation

\[
                       D(y)=\int_0^y\tau(s)\,ds.
\tag{14}
\]

Expanding only to the order that will be used,

\[
 \delta(t)=\lambda t-\frac{t}{4}r(2t)+O(t^2).
\]

First `tau(s)=s/lambda+O(s^(3/2))`. The derivative bound on `r`
therefore permits replacing `r(2tau(s))` by `r(2s/lambda)` with
error `O(s)`. Substitution in the inverse equation proves

\[
 \tau(s)=\frac{s}{\lambda}
      +\frac{s}{4\lambda^2}r(2s/\lambda)+O(s^2),
\]
\[
 D(y)=\frac{y^2}{2\lambda}
       +\frac1{4\lambda^2}\int_0^y s\,r(2s/\lambda)\,ds
       +O(y^3).
\tag{15}
\]

Since the integral is `O(y^(5/2))`, equations (13) and (15) first
improve (11) to

\[
                     r(x)=c\sqrt{x}+O(x^{3/4}).
\tag{16}
\]

Let `E` be the finite set of exponents below one with nonzero
coefficients in the alleged Puiseux expansion. It contains `1/2`,
with coefficient `c_(1/2)=3/4`, and by (16) has no exponent strictly
between `1/2` and `3/4`. Thus

\[
 r(x)=\sum_{\alpha\in E}c_\alpha x^\alpha+O(x).
\tag{17}
\]

All products of two corrections in (16) are `O(x^(3/2))`. Replacing
the upper limit `r(x)` in the integral of (15) by `c*sqrt(x)` also
changes it by only `O(x^(3/2))`: its integrand is `O(x^(3/4))` there
and the change of limit is `O(x^(3/4))`. Consequently (13) reduces to

\[
 2\sum_{\beta\in E\setminus\{1/2\}}c_\beta x^{\beta+1/2}
 +\sum_{\alpha\in E}\frac{4^\alpha c_\alpha}{2+\alpha}
                         x^{1+\alpha/2}
                         =O(x^{3/2}).
\tag{18}
\]

Every displayed exponent is strictly below `3/2`, so its combined
coefficient must vanish. Choose the largest exponent `alpha_*` in
the finite nonempty set `E`. Its second-sum term in (18) has nonzero
coefficient. The only possible first-sum cancellation would require

\[
                  \beta=\frac{1+\alpha_*}{2}>\alpha_*,
\]

which is absent from `E`. No other second-sum exponent is equal to
it. This contradiction proves the claim.

The same coefficient identity displays the forced chain, if one tries
to maintain the contact equations by successive fractional powers:

\[
 \alpha_0=\frac12,\quad c_0=\frac34,\qquad
 \alpha_{j+1}=\frac{1+\alpha_j}{2},\quad
 c_{j+1}=-\frac{4^{\alpha_j}}{2(2+\alpha_j)}c_j.
\tag{19}
\]

All these coefficients are nonzero, and
`alpha_j=1-2^(-j-1)` accumulates at one. The first three forced terms
are

\[
 \frac34x^{1/2}-\frac3{10}x^{3/4}
                   +\frac{6\sqrt2}{55}x^{7/8}.
\tag{20}
\]

This is a coefficient obstruction, not a claim that the infinite
series in (19) converges to a legal Princess law or exhausts its
asymptotic terms. Existence and the global continuation are separate.

## 5. Consequence for algebraic ansatzes

The classical Newton–Puiseux theorem says that a local branch of an
algebraic function has a convergent fractional-power series with one
fixed denominator. See Flajolet and Sedgewick, *Analytic Combinatorics:
Complex Asymptotics*, Theorem VII.5, in the
[authors' text](https://algo.inria.fr/flajolet/Publications/ch4567.pdf).
Section 4 therefore rules out every algebraic initial trace satisfying
the stated candidate contacts, including a finite algebraic endpoint
phase. It rules out neither a nonalgebraic finite description nor a
different endpoint contact pattern. No finite sufficient class for the
unrestricted equilibrium follows from this obstruction.

## 6. Endpoint-return rows become redundant in this candidate phase

There is also a useful exact family reduction within the same front-one
model. Use the initial-patch notation from
`MOVING_FRONT_INITIAL_CONTACT.md`:

\[
 L(a,z)=\mathcal F(1-a,z-1),\quad \phi(a)=L(a,a),\quad
 k_z=K(z-1)=A(z/2),\qquad 0<a\le z<1.
\]

The principal initial-inward row `I(a,z)` and positive-endpoint-return
row `J(a,z)` have the same first inward leg and turn. The former then
turns again on front one and visits the negative endpoint first; the
latter proceeds to the positive endpoint first. Put `l=L(a,z)` and
`f=phi(a)`. Transport gives `1/2<=l<=k_z`. The outward-completed field
makes the two auxiliary moments exactly

\[
 H_{1+z}(l)=H(l)+\frac z2l+\frac z4,\qquad
 O_z(f)=\frac z2\max\{f,k_z\}.
\tag{21}
\]

Subtracting the independently proved physical I and J formulas yields

\[
 C_J(a,z)-C_I(a,z)
 =-4+\frac{5z}{4}+\frac z2L(a,z)
                       +(4-z)\max\{\phi(a),k_z\}.
\tag{22}
\]

Now subtract (5), with its positive start set to `1-z`:

\[
\begin{aligned}
 C_J(a,z)-C_I(a,z)
 ={}&C_S(1-z)-C_P(1-z,1)\\
 &+\frac z2[L(a,z)-\phi(z)]\\
 &+(4-z)[\max\{\phi(a),k_z\}-k_z].
\end{aligned}
\tag{23}
\]

Both terms on the last two lines are nonnegative. Hence wherever
`C_S(1-z)>=C_P(1-z,1)`, every positive-valley J row is dominated by
the corresponding I row. In particular J adds no response constraint
inside a simultaneous flat positive-P/S phase. The diagonal `a=z`
reduces to equality with the S/P difference. The actual endpoint-start
case `a=0` is handled separately: the fastest endpoint sweep dominates
every Monster route starting at that endpoint.

This is a genuine conditional elimination of one continuous response
family. It does not eliminate variable turning fronts, negative-start
responses or additional center excursions, and it does not prove that
the front-one phase is sufficient for the unrestricted game.

Combining (23) with (7c) also eliminates J rows with `6/7<=z<1` and
`0<a<=z` whenever the sweep floor is `c>219/154`. Their corresponding
positive comparison start `1-z` lies in `(0,1/7]`, so the first line
of (23) is already strictly positive. This exclusion needs no flat P/S
contact in that part of the candidate field.

## 7. Independent physical regression

`verify_front_one_contact_moments.py` independently intersects actual
Princess paths that start at a uniform radial position `r`, stay there
until time `1-r`, then move outward at unit speed until the endpoint.
It also mixes in genuine stationary endpoint mass. The test compares
the actual chronological captures to (5), (7), (21) and (23), including
the initial endpoint trace jumps. It does not assume this fixture has
flat contact costs and does not test the non-Puiseux theorem by merely
repeating its coefficient recurrence.

```sh
python -B packages/interval_global_closure/verify_front_one_contact_moments.py \
  packages/interval_global_closure/front_one_contact_moment_replay.json
```

The receipt records 90 P/S and 36 I/J physical path scores, 45 signed
S/P identities, 24 column and 24 moment extensions, 18 J/I identities,
36 outer moment/column identities, 18 initial endpoint trace jumps,
three sweep scores and 1,062 actual affine capture branches. The
continuous trace identities and the algebraicity obstruction are
analytic arguments above, independently reviewed by both peers.
