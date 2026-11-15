# The complete one-turn response domain

**Status:** Gate 1 is closed by the theorem below. This is a complete
response reduction for the specified canonical Monster class
`B1`, not a proof of strict separation or of its exact minimax value.
No speed/waiting normalization beyond the definition of `B1` is asserted.

The previous bulk formula required a nonnegative turn and an outward
tail. The three-integral formula here has neither restriction. It
includes endpoint atoms, interior atoms, time-zero captures, negative
turns, late returns, and all first-contact equalities.

## 1. Princess conventions

Let `F(t,x)` be a probability CDF supported on `[-1,1]` satisfying the
exact transport inequalities

\[
 F(s,x-(t-s))\le F(t,x)\le F(s,x+(t-s)),\qquad s\le t.
\tag{1}
\]

Write `F⁺(t,x)=F(t,x)` and `F⁻(t,x)=Pr(P(t)<x)`. Use the common-quantile
law

\[
 Q(t,r)=\inf\{x:F(t,x)\ge r\},\qquad 0<r<1,
\]

with one uniform rank for the whole trajectory. Equation (1) makes
every quantile trajectory 1-Lipschitz. These assertions and the exact
record identity are proved in
[GLOBAL_CDF_TRANSPORT_LP.md](../12-global-closure/GLOBAL_CDF_TRANSPORT_LP.md).
For clarity, the identity used here is

\[
 \Pr(T(m,Q)>t)=1+
 \inf_{0\le s\le t}F^-(s,m(s))-
 \sup_{0\le s\le t}F^+(s,m(s)).
\tag{2}
\]

Rank-boundary conventions do not affect its Lebesgue probability.
The strict lower trace and closed upper trace are essential: the whole
mass at an initial contact or a turning contact is captured.
For a law with the same marginals but a different temporal coupling,
(2) is generally only an upper bound; our theorem concerns the legal
ordered law just defined.

Along any unit-speed rightward leg both traces are nondecreasing;
along any unit-speed leftward leg both are nonincreasing. One direct
proof is that `Q(t,r)-m(t)` is respectively nonincreasing or
nondecreasing for every rank. Thus both sets `{Q<m}` and `{Q≤m}` have
the asserted nesting. No differentiation or density is required.

## 2. Exhaustion and a harmless compact boundary

Set

\[
 D=\{(a,h):-1\le a\le1,\quad 0\le h\le1-a\},\quad
 b=a+2h,\quad H=1+b.
\tag{3}
\]

For `(a,h)∈D`, let `m_{a,h}` follow the vertices

\[
 (0,a),\quad (h,a+h),\quad(H,-1),\quad(H+2,1),
\tag{4}
\]

deleting zero-length legs, then remain at `1`. All three legs have
speed one, remain in the arena, and finish by time six. A convenient
all-time formula, also showing continuous dependence on `(a,h)`, is

\[
 m_{a,h}(t)=a+t-2(t-h)_++2(t-H)_+-(t-H-2)_+.
\tag{5}
\]

Here `B1` consists of arbitrary starts, at most one interior reversal
before the first endpoint, and then a direct sweep to the opposite
endpoint, as in
[ONE_TURN_SUBGAME_BRACKET.md](ONE_TURN_SUBGAME_BRACKET.md).
After both endpoints have been visited, every Princess has already
been captured; subsequent continuation is immaterial.

**Exhaustion theorem.** Against any Princess law,

\[
 \inf_{m\in B1}\mathbb E T(m,P)
 =\min_{(a,h)\in D,\ \epsilon\in\{-1,1\}}
       \mathbb E T(\epsilon m_{a,h},P).
\tag{6}
\]

For a reflection-symmetric Princess law the two orientations have
equal costs, so only `D` is needed.

**Proof of exhaustion.** An interior-start path with a genuine
interior turn can be reflected so that its first leg moves right.
Its turn time is exactly some `0<h<1-a`; its turn is `a+h`, which
may be negative. Its next endpoint must be `-1`, reached at
`h+(a+h+1)=H`; its direct sweep then reaches `1` at `H+2`.
This is (4). An interior-start path with no interior turn either
goes left first (`h=0`) or goes right first (`h=1-a`). In the latter
case the first endpoint is `1` at time `h`, and the opposite endpoint
is `-1` at time `H=h+2`; the extra last leg in (4) occurs after all
captures. Endpoint starts reduce to immediate endpoint sweeps,
represented by `(-1,0)` and `(1,0)`. Thus every genuine `B1` payoff
occurs on the right-hand side of (6).

The only extra, potentially noncanonical paths in the closed
triangle are `a=-1, 0<h<2`: they start at an endpoint but turn
before completing the compulsory sweep. They cannot lower the
infimum. Indeed the immediate right sweep `e(t)=-1+t`, `0≤t≤2`,
is at least as far right as every speed-at-most-one path starting
at `-1`. If such a path meets `P` at time `s≤2`, then
`e(0)≤P(0)` and `e(s)≥P(s)`, so the intermediate value theorem
gives `T(e,P)≤s`. If `s>2`, the complete sweep already captured
`P` by time two. Thus

\[
 T(m_{-1,0},P)\le T(m_{-1,h},P)
 \quad\text{for every Princess path and every }h\in[0,2].
\tag{7}
\]

The same applies after reflection. Every added payoff is therefore
dominated by a genuine member, proving equality of the infima.

Finally, the family (5) is compact in uniform convergence on `[0,6]`.
For a fixed continuous `P`, first coincidence on this family is
lower semicontinuous: along any convergent sequence of paths and
capture times, a subsequential limiting capture is still a
coincidence for the limit path. Since every member captures by six,
Fatou's lemma makes the expected payoff lower semicontinuous as
well. It attains its minimum on compact `D` and the finite
orientation set. If the minimizer is an extra endpoint-face path,
(7) supplies a genuine endpoint sweep attaining no larger value.
This proves (6), including attainment. QED.

There is no claim that the payoff is continuous. An actual endpoint
hit or a turning tangency can strictly lower the first-capture time.
The minimum in (6) uses the exact boundary paths, not interior limits.

## 3. Exact cost on the entire closed triangle

Put

\[
 A=F^-(0,a),\qquad B=F^+(h,a+h).
\tag{8}
\]

**Three-integral theorem.** The ordered-law expectation of (4) is

\[
\boxed{\begin{aligned}
 C_F(a,h)={}&
 \int_0^h\bigl[1+A-F^+(t,a+t)\bigr]\,dt\\
 &+\int_h^H\bigl[1-B+\min\{A,F^-(t,b-t)\}\bigr]\,dt\\
 &+\int_H^{H+2}\bigl[1-\max\{B,F^+(t,t-H-1)\}\bigr]\,dt.
\end{aligned}}\tag{9}
\]

This formula applies to every `(a,h)∈D`. It requires neither
symmetry, an outward tail, sticky endpoints, absence of atoms, nor
`b≥0` or `a+h≥0`.

**Proof.** On the right first leg, characteristic monotonicity fixes
the lower record at `A` and the upper record at the current `F⁺`.
On the left second leg, the upper record is the turn value `B` and
the lower record is the smaller of `A` and the current `F⁻`.
At the endpoint `-1`, the lower record becomes exactly zero,
including any mass at that endpoint. During the right final leg it
stays zero, while the upper record is the larger of `B` and the
current `F⁺`. Substitution in (2) gives the three integrands.
After the final endpoint the upper record is one, so no survivors
remain. Integrating the survival probability proves (9). Endpoint
times themselves have zero integration measure, but their exact
trace values set the subsequent records and therefore cannot be
replaced by one-sided limits. QED.

### Boundary faces, stated explicitly

| Parameter face | Physical meaning | Exact record rule |
|---|---|---|
| `-1<a<1`, `0<h<1-a` | One genuine interior turn; negative, zero and positive turn locations all allowed | `A=F⁻(0,a)`, `B=F⁺(h,a+h)` |
| `h=0`, `-1<a<1` | Left endpoint first, then right sweep | Initial contact uses both traces: `A=F⁻(0,a)`, `B=F⁺(0,a)` |
| `h=1-a`, `-1<a<1` | Right endpoint first, then left sweep | `B=F⁺(h,1)=1`; the third integral is zero |
| `a=-1` | Immediate right sweep at `h=0`; remaining face dominated by that sweep | `A=F⁻(0,-1)=0`; retain the atom in `F⁺(0,-1)` |
| `(a,h)=(1,0)` | Immediate left sweep | `B=F⁺(0,1)=1`; retain the atom in `F⁻(0,1)` |
| `a+h=0` or `b=0` | Center/characteristic tie, with no new domain restriction | Formula (9) is unchanged |
| Any CDF atom or persistent equal-speed coincidence | Genuine first capture, including a tangency at the turn | Always use the strict lower and closed upper traces in (9) |

The separate endpoint-sweep costs are consequently

\[
 C_{E_-}=\int_0^2[1-F^+(t,-1+t)]\,dt,
 \qquad C_{E_+}=\int_0^2F^-(t,1-t)\,dt.
\tag{10}
\]

As an elementary jump test, take a stationary Princess at each
endpoint with probability one-half, and `a=0`. For `0<h<1`, (9)
gives `C=2+2h`; at `h=1` the actual endpoint-first path has `C=2`,
not its interior limit `4`. The lost two units are exactly the
four-unit earlier capture of the half-mass at the positive endpoint.

The required negative-start/late-turn regression `a=-7/8`,
`b=67/64` corresponds to `h=123/128`, `a+h=11/128`, and
`H=131/64`. It lies strictly inside the complete domain.

## 4. A finite exact certificate for a fixed piecewise-affine field

The following proposition is specific to the stated representation.
It does not assert that arbitrary piecewise-rational or algebraic
CDFs have quadratic response costs.

**Finite quadratic partition proposition.** Suppose the CDF is
continuous on the open spatial strip `0≤t≤6`, `-1<x<1`, and is
affine with rational coefficients on each member of a fixed finite
rational polygonal subdivision of that strip. Its one-sided
endpoint traces must have finite rational piecewise-affine
subdivisions as well; endpoint atoms are allowed. Then the interior
of `D`, and each of its exact boundary strata, have a finite rational
polygonal partition on which (9) is a rational polynomial of degree
at most two. Lower-dimensional cells and all one-sided limits are
included in a complete certificate.

**Proof and construction.** First split parameter space according to
the CDF cell containing `(0,a)` and the one containing `(h,a+h)`.
On a resulting region `A` and `B` are affine rational functions of
`(a,h)`; exact endpoint values are prescribed separately on the
boundary. Within any CDF cell, each of the three pulled-back fields
has the form

\[
 F(t,m_{a,h}(t))=\kappa t+\ell(a,h),
\tag{11}
\]

where `κ` is a fixed rational constant and `ℓ` is affine rational.
A ray crosses a mesh edge `u t+v x+w=0` at an affine rational time,
unless the constant time coefficient after substitution is zero.
That case is either no crossing or an entire coincident edge,
distinguished by an affine parameter equation. Continuity makes
either adjacent formula agree on a coincident interior edge.

The clipping equations on the later legs are `F=A` and `F=B`.
When `κ≠0`, (11) makes their crossing times affine rational too.
When `κ=0`, an affine parameter sign determines which expression is
selected, or the two expressions tie throughout the interval.
Add all these affine sign splits, together with comparisons of
every relevant crossing time and the leg endpoints `0,h,H,H+2`.
There are only finitely many rational lines. Their arrangement
partitions `D` into rational convex polygons, segments and points.
One may refine more than necessary; infeasible activity orders
contribute empty cells.

On each remaining open cell, each integral is a fixed sum of
affine-in-time expressions between affine parameter-dependent
limits. Integrating (11) produces
`κ(v²-u²)/2+ℓ(v-u)`, of degree at most two. Constants `A` and `B`
give the same degree bound. This proves the proposition.
Exact boundary records must be recomputed; an interior polynomial
limit is not substituted for an endpoint-turn payoff. QED.

This gives a finite proof of `C_F≥c` for a *supplied* rational field:
publish the arrangement, a coverage proof, every polynomial and
its face conventions, then minimize the corresponding quadratics.
For a quadratic on a compact rational polygon it suffices to
check vertices, edge stationary points, and feasible interior
solutions of its affine gradient equations. Singular stationary
sets are harmless: the quadratic is constant on such a set, and
one rational feasible representative suffices. Include segment
and point cells, and polynomial limits from all open cells.
This is a finite test for each fixed CDF, not an equilibrium-
sufficiency theorem for a finite family of CDFs.

## 5. Independent exact fixtures

Run from the repository root:

```sh
python3 packages/interval_one_turn/verify_domain.py
```

The standard-library checker compares (9), integrated from exact
CDF traces and their crossing partitions, with direct rational
first-intersection times of ordered polygonal Princess paths.
It includes random ordered atomic laws, stationary atoms, moving
coincidences, negative turns, both endpoint-first faces, endpoint
starts, initial/turn ties, and the late-turn witness. It separately
checks the added `a=-1` face domination and the endpoint jump.
These fixtures audit the formulas; the exhaustion, atomic record
argument, compactness and finite-partition results are established
by the proofs above, not by finite testing. No Lean compilation or
CI proof is claimed.
