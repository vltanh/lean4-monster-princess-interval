# Exact CDF costs for two interior monster turns

This note adds a response family that is not controlled merely by making
all one-interior-turn costs large. It gives full-field capture formulas
and exact rational checks. It does not assert that the current numerical
field is a matching law or that this family contains every best response.

Use the ordered radial endpoint-by-two model and strict/closed trace
conventions of [POSITIVE_TURN_SHEET.md](POSITIVE_TURN_SHEET.md). Paths
may have multiple waves, stationary phases, or non-unit speeds. Let
`R(U,V)` denote the closed radial CDF except where a strict trace is
explicitly requested.

## 1. Route and notation

For initial monster position `x`, first positive turn `U=s`, and second
negative turn `V=t`, use the route

\[
 (0,x),\quad
 ((s-x)/2,(s+x)/2),\quad
 ((s+t)/2,(s-t)/2),\quad
 (t+1,1),\quad(t+3,-1).
\]

Its legal parameter range is

\[
 |x|\le s\le2-x,\qquad s\le t\le s+2.
\]

Write its expected capture time as `C3(x;s,t)`. Center and endpoint
equality faces are included. When `t=s+2`, the second turn is the left
endpoint, and the route reduces to the corresponding one-interior-turn
strategy; the final extra sweep is then irrelevant.

For any threshold `q`, define

\[
 G(v;q)=\int_v^{v+2}(R(U,v)-q)_+\,dU.
\]

This is a closed-trace first-inverse integral. At a genuine endpoint
turn, the point value of `R` is one, even if the interior endpoint trace
is smaller. The point value does not change a vertical integral, but it
does change a turn-capture coefficient.

## 2. Positive initial position

Let `x=z>0`, and put

\[
\begin{aligned}
 A&=\Pr\{p_q(0)<z\},&
 B&=R(s,-z),& D&=R(t,s),\\
 I&=\int_z^sR(U,-z)\,dU,&
 J&=\int_s^tR(U,s)\,dU,\\
 F&=\int_{-z}^s(A-R_{<}(s,V))_+\,dV.
\end{aligned}
\]

Then

\[
\boxed{\begin{aligned}
4C_3(z;s,t)={}&4t+8+2sA
 -(2t+2+z-s)B-(t+6-s)D\\
 &-I-F-J-G(t;B).
\end{aligned}} \tag{1}
\]

The strict initial CDF is necessary: an initial-position atom at `a=z`
was already caught at time zero and belongs to the first outward-capture
group, not the return-capture group.

To prove (1), let `alpha_q(s)` and `beta_q(v)` be the first inverses of
`tau+p_q(tau)` and `tau-p_q(tau)`. The positive reflected component is
partitioned into three disjoint capture groups:

* ranks below `A` are caught at `alpha_q(s)` on the first return;
* ranks from `A` through `B` are caught at `beta_q(-z)` on the initial
  outward leg;
* ranks above `B` are caught at `beta_q(t)` on the final rightward sweep.

For the negative reflected component, ranks through `D` are caught at
`beta_q(s)` before the second turn, and ranks above `D` are caught at the
final left endpoint at time `t+3`. The first-inverse identities are

\[
\begin{aligned}
 \int_0^A\alpha_q(s)\,dq&=sA-F/2,\\
 \int_A^B\beta_q(-z)\,dq&=(s-z)B/2-I/2,\\
 \int_B^1\beta_q(t)\,dq&=(t+1)(1-B)-G(t;B)/2,\\
 \int_0^D\beta_q(s)\,dq&=(s+t)D/2-J/2.
\end{aligned}
\]

Summing the two reflections and dividing by two yields (1).

## 3. Negative initial position

Let `x=-z<0`. Here use the **closed** initial CDF

\[
 A=\Pr\{p_q(0)\le z\},
\]

because the initial `a=z` atom belongs to the already-caught negative
component. Set

\[
\begin{aligned}
 N&=\int_{-z}^zR_{<}(z,V)\,dV,&
 B&=R(s,z),&D&=R(t,s),\\
 I&=\int_z^sR(U,z)\,dU,&
 G_{s,t}(A)&=\int_s^t(R(U,s)-A)_+\,dU.
\end{aligned}
\]

The exact formula is

\[
\boxed{\begin{aligned}
4C_3(-z;s,t)={}&N+4t+8-2(t+3)A
 +(s+z-2t-2)B\\
 &-(t+6-s)(D-A)_+-I-G_{s,t}(A)-G(t;B).
\end{aligned}} \tag{2}
\]

The negative component's ranks through `A` are caught on the first leg,
with total first-inverse integral `N/2`. The second, leftward excursion
adds only ranks from `A` through `D` when `D>A`; otherwise it adds none.
Those new capture times sum to

\[
 \frac{s+t}{2}(D-A)_+-\frac12G_{s,t}(A).
\]

The remaining negative mass is `1-A-(D-A)_+` and is caught at time
`t+3`. The positive component is partitioned at `B`: its first-leg
capture integral is `(s+z)B/2-I/2`, and its later capture integral is
`(t+1)(1-B)-G(t;B)/2`. These groups give (2), including the case
`D<A`, which must not be replaced by an uncapped difference.

At `z=0`, the two formulas agree for a law without an initial center
atom. An initial center atom requires its immediate-capture rule; the
current continuous-field construction excludes that atom.

## 4. Endpoint collapse and the useful `t=1` face

At `t=s+2`, closed endpoint contact gives `D=1`, while the endpoint-by-two
condition gives `G(t;B)=0`. Substitution in (1) and (2) recovers the
corresponding exact M2 formula. Thus these identities include the older
one-turn family as an equality face.

If there is no outgoing `V=1` atom, then `G(1;B)=0`. For a positive
initial position, (1) on this face becomes

\[
\begin{aligned}
4C_3(z;s,1)={}&12+2sA-(4+z-s)R(s,-z)\\
 &-(7-s)R(1,s)-I-F-\int_s^1R(U,s)\,dU.
\end{aligned} \tag{3}
\]

This face is relevant to the observed attacks: an early positive turn
can be followed by a negative excursion whose return characteristic is
arbitrarily close to one. The term involving `R(1,s)` is not controlled
by checking the first turn in isolation.

For `t>1`, `G(t;B)=0` under the endpoint-by-two assumption. In a smooth
row, differentiating (1) in its second-turn coordinate gives

\[
 4\partial_tC_3
 =4-2B-2R(t,s)-(t+6-s)R_U(t,s). \tag{4}
\]

The first-turn capture rank satisfies `B=R(s,-z)<=A(s)`. Consequently
the sufficient post-one inequality

\[
 (t+6-s)R_U(t,s)+2R(t,s)\le4-2A(s)
\]

makes this interior second-turn cost nondecreasing. Endpoint jumps must
still be checked separately. This explains the role of the labelled
post-one sufficient condition in the full-field experiment; it is not
a substitute for early second-turn constraints.

## 5. Convex full-field feasibility

For fixed `(z,s,t)`, all named point values and plain integrals are
linear in the full radial CDF. The remaining terms in (1) are negative
integrals of positive parts of linear functions. Formula (2) has the
same form and one additional negative positive-part point term, whose
coefficient `t+6-s` is positive.

Therefore both costs are concave in the CDF. A lower constraint
`C3>=value` is convex and can join the same transport-constrained field
solve as the M1/M2 inequalities. No initial, prefix, or outgoing front
needs to be frozen when adding this family.

On a triangular affine field, the plain integrals are linear forms, and
each positive-part integral is evaluated exactly by splitting at its
affine zero. This avoids time-step quadrature and avoids weak generic
record selections on flat transport faces. Generic running records
remain an independent evaluator and handle additional turn patterns.

## 6. The two same-half orientations

### A positive start whose second turn stays positive

Keep the route of Section 1, but take
`0<z<1`, `z<=s<=2-z`, and
`-z<=t<s`, `s<=t+2`, `t<=1`. Both interior turns now occur on the
positive half. Use the strict initial `A=Pr(a<z)` and set

\[
\begin{aligned}
 B&=R_{\le}(s,-z),&D&=R_{<}(s,t),&L&=\min(A,D),\\
 I&=\int_z^sR_{\le}(U,-z)\,dU,&
 F_t&=\int_{-z}^t(A-R_{<}(s,V))_+\,dV,\\
 G_t&=\int_{|t|}^{t+2}(R_{\le}(U,t)-B)_+\,dU.
\end{aligned}
\]

Then the exact four-cost is

\[
\boxed{\begin{aligned}
4C={}&4t+8+(s+t)A-(2t+2+z-s)B-I-F_t-G_t\\
    &+(2+t-s)L+\int_t^1\min(L,R_{<}(t+2,V))\,dV.
\end{aligned}} \tag{5}
\]

The positive component's initial ranks `A..B` are caught on its first
outward leg. Ranks `L..A` are caught on the first return, while `0..L`
are still below the second turn and are caught after the right endpoint
visit. All negative copies are caught at the final negative endpoint.
The three positive first-inverse moments are

\[
 \frac{(s-z)B-I}{2},\qquad
 \frac{(s+t)(A-L)-F_t}{2},\qquad
 (t+1)L+\frac12\int_t^1\min(L,R_{<}(t+2,V))\,dV.
\]

The remaining positive tail has moment
`(t+1)(1-B)-G_t/2`. Their sum proves (5). The second turn's strict trace
is essential: a path exactly at that turn has already been caught.
The strict inequality `t<s` also matters for a center atom; the exact
center-turn face is instead covered by (1).

Because `2+t-s>=0`, the two positive terms involving `L` are concave
minima of linear CDF forms. The other nonlinear terms are negative
positive parts. Thus (5) is again concave in the complete field.

### An initial inward turn followed by an outward turn

Start at `a>0` and use

\[
 (0,a),\quad ((a+v)/2,(a-v)/2),\quad
 ((s+v)/2,(s-v)/2),\quad(s+1,-1),\quad(s+3,1),
\]

where `-a<=v<a` and `a<=s<=v+2`. This is the other same-half
orientation. Define the closed initial `A=Pr(a_q<=a)` and

\[
\begin{aligned}
 L&=R_{<}(a,v),&M&=\max(A,R_{\le}(s,v)),\\
 N_v&=\int_{-a}^vR_{<}(a,V)\,dV,&
 F&=\int_v^s(L-R_{<}(s,V))_+\,dV,\\
 I_A&=\int_a^s(R_{\le}(U,v)-A)_+\,dU,&
 H(s)&=\int_s^{s+2}R_{\le}(U,s)\,dU.
\end{aligned}
\]

The exact identity is

\[
\boxed{\begin{aligned}
4C={}&4s+8+N_v+(2s-a-v)L-(s+6-v)M\\
    &-(s+v)A-F-I_A-H(s).
\end{aligned}} \tag{6}
\]

The positive ranks `L..A`, `0..L`, and `A..M` contribute the moments
`[N_v-(a+v)L]/2`, `sL-F/2`, and
`[(s+v)(M-A)-I_A]/2`. The positive tail has endpoint moment
`(s+3)(1-M)`. The negative component contributes
`s+1-H(s)/2`. This proves (6), including early outward turns. At
`v=-a`, the first inward leg has zero duration and (6) reduces to the
positive M2 identity with its appropriate initial-atom convention.
All nonlinear terms in (6) have the concave signs.

### Post-one second turns in the initial-inward family

For fixed `a,v`, consider the second outward turn `s>1` before its
endpoint face. In a continuous field set

\[
 J_L(s)=\int_v^s\mathbf1_{\{R(s,V)<L\}}R_U(s,V)\,dV\ge0.
\]

The endpoint-by-two condition gives `H(s)=0` and `Z(s)=0`. Differentiating
(6), using `F_s=L-J_L` and `(I_A)_s=M-A`, yields

\[
 4C_s=4+L-2M-(s+6-v)M_s+J_L. \tag{7}
\]

Where `M=A`, this derivative is at least two. Where `M=R(s,v)`, the
following full-field inequalities are sufficient for nonnegativity:

\[
\begin{cases}
 (s+6-v)R_U(s,v)+2R(s,v)\le4-2A(v),&v\ge0,\\
 (s+6-v)R_U(s,v)+2R(s,v)\le4+A(-v),&v<0.
\end{cases} \tag{8}
\]

For the negative row, transport gives `L>=A(-v)`; in an atomic initial
law this comparison uses the **strict** initial CDF at `-v`, as does the
positive-start late inequality. For a continuous initial field there is
no distinction. Thus (7) is nonnegative almost everywhere, and continuity
makes the interior cost nondecreasing in `s`.

Consequently, under exact (8), every post-one interior second turn in
this family is dominated by its turn at `s=1`. The actual endpoint turn
`s=v+2` has its own closed-contact gain and must be checked separately.
This is a conditional response reduction, not a claim that the early
initial-inward family has been minimized. The separately rationally
repaired discovery field satisfies (8) exactly; the unrepaired snapshot
has the explicitly reported small violations.

These formulas are structural tools. The saved full M3 mesh pool covers
the opposite-half parameter domain of Section 1; it does not silently
claim that both additional same-half domains have been exhaustively
collocated.

## 7. Exact validation and scope

Run

```bash
python packages/interval_turn_density/verify_two_interior_cdf.py
```

The verifier performs **4,512 exact Fraction checks**:

* 1,014 direct-capture comparisons for each initial sign;
* 312 second-turn endpoint collapses;
* 309 initial/center equality-face checks;
* 464 initial-atom start checks;
* 503 positive same-half direct-capture comparisons, including 201
  negative return characteristics and 95 strict-turn witnesses;
* 480 initial-inward direct-capture comparisons and 120 zero-leg
  collapses to positive M2.

The fixtures include multiple-wave paths, non-unit speeds, a center-wait
component ending on `V=1`, and an endpoint component. Direct segment
intersections are independent of formulas (1) and (2).

The corresponding floating field implementation was also compared with
generic running signed records on 112 routes, agreeing within `1.6e-14`.
These results establish the identities and their implementation. The
full game still requires an admissible complete CDF, every relevant
monster inequality, and a matching upper response construction.
