# A two-dimensional upper-certificate problem for M1/M2 mixtures

## Scope

This note develops the separable functional in `CHARACTERISTIC_RESPONSE.md`
into an explicit control problem and an upper-certificate theorem. It uses
that note's exact capture formulas, including the end of the `U=1` plateau.
It does not prove that an optimal unrestricted monster law belongs to M1/M2,
and supplies no matching unrestricted princess guarantee.

Let `mu_1,mu_2` be the nonnegative parameter measures of a symmetric M1/M2
monster mixture; their combined mass is one. By symmetry and uncrossing, its
princess response supremum can be taken over paths in `[0,1]`. Use

    a=p(0),  U=t+p(t),  V=t-p(t),
    e=inf{t:U(t)>1},  b=1-2e.

The allowed parameters satisfy

    0<=a<=1,      (1-a)/2 <= e <= 1.

The corresponding initial and transition points in characteristic space are

    S=(a,-a),       P=(1,2e-1).

The geometric path is coordinatewise nondecreasing and stays in the strip
`0<=U-V<=2`. Its time parametrization is fixed by `t=(U+V)/2`.

## 1. Survival requires only one frozen threshold

The following formulas give the surviving mass in an **unreflected**
parameter family before dividing by two for the reflection choice. They are
exact, including atoms. Set differences and interval endpoints are literal.

For M1, the surviving mass at time `t` is

    mu_1({x:x<-V(t)}) + mu_1({x:a<x<2-U(t)}).

For its reflection it is

    mu_1({x:x<-U(t)}) + mu_1({x:-a<x<2-V(t)}).

For M2, the surviving mass has three modes:

| Current characteristic | Surviving unreflected M2 mass |
| --- | --- |
| `U<1` | `mu_2({x:x<-V}) + mu_2({x:x>a})` |
| `U=1` | `mu_2({x:x<-V})` |
| `U>1` | `mu_2([-1,b)) * 1_{V<3}` |

On the plateau `U=1`, an initial right-moving monster whose turn occurs on
that plateau meets the princess at its turn, if it has not already met her.
Consequently its cutoff continues to move while the plateau lasts. It freezes
only when `U` leaves one, at `b=-V(e)`. Freezing at the first time `U=1`
instead gives the wrong capture times.

The reflected M2 mass is always

    mu_2({x:x<-U}) + mu_2({x:x>-a}) * 1_{V<1}.

There is no second delayed tail in the nonnegative half-interval: by the time
`V` reaches one, `U>=V` has already reached one. Every reflected M2 path has
then been captured. Thus only the scalar `b` needs to be retained from the
earlier trajectory.

These formulas follow either by checking which first inverses in
`CHARACTERISTIC_RESPONSE.md`, Section 2, are still ahead of the current time,
or directly from the three unit-speed segments of M2. In particular, the
inequalities are strict at a capture threshold. A path starting at the
princess's initial position has already been captured at time zero.

## 2. Two monotone-path pieces with separable cost

For fixed `(a,e)`, take the threshold measures `alpha,beta` defined in
`CHARACTERISTIC_RESPONSE.md`, Section 4, and put

    f(u)=alpha((u,infinity)),
    g(v)=beta((v,infinity)).

The exact payoff is

    J(p) = (1/4) integral_gamma (f(u)+g(v)) (du+dv).        (1)

The factor is one quarter: reflection contributes one half, and
`dt=(du+dv)/2` contributes the other. This is a line integral along the
characteristic path, not an assertion of path independence.

Every monster in the mixture completes its sweep by time four, so the
integrand is zero thereafter. At time four the nonnegative princess satisfies

    4<=U(4)<=5,      3<=V(4)<=4.

Extend the characteristic path monotonically inside the strip to the fixed
point `Q=(5,5)`. For example, first raise `V` to `U(4)`, then raise both
coordinates equally to five. Both tails are zero on this added part. Hence
the endpoint in (1) may be fixed at Q without changing the payoff.

There are now just two geometric pieces: `S -> P` and `P -> Q`. The prefix
has `U<=1`. The actual suffix has `U>1` at every time strictly after `e`.
Retaining the latter condition preserves the exact cutoff; omitting it is
permitted for an **upper relaxation**, but must not be silently identified
with an attaining princess.

This reduces a proposed M1/M2 upper bound to a two-parameter family of
separable monotone-path inequalities. It does not yet bound the number of
turns of an optimizing path.

## 3. An exact two-dimensional potential certificate

The following sufficient condition proves an unrestricted upper guarantee
for a specified M1/M2 mixture.

**Theorem.** For every admissible `(a,e)`, suppose there are continuously
differentiable potentials `Phi^-` and `Phi^+`, defined on neighborhoods of
the respective closed strip rectangles from S to P and P to Q, such that

    Phi^-_u(u,v) >= f(u)+g(v),
    Phi^-_v(u,v) >= f(u)+g(v),

on the prefix region, and the same two inequalities hold for `Phi^+` on the
suffix region. Suppose also

    Phi^-(P)-Phi^-(S) + Phi^+(Q)-Phi^+(P) <= 4c            (2)

for every `(a,e)`. Then the symmetric monster mixture guarantees

    E T(M,p) <= c

against every admissible princess path, and hence against every princess
mixture.

**Proof.** Along a coordinatewise nondecreasing characteristic path, both
coordinate increments are nonnegative. The two derivative inequalities
therefore give

    d Phi >= (f(u)+g(v))(du+dv).

Integrate on the two pieces, add them, and use (1) and (2). This proves the
claim for nonnegative princess paths. Symmetry and uncrossing then prove it
for arbitrary princess paths. The continuum deadline theorem also shows the
same upper guarantee against arbitrary continuous princess motion. No bound
on the princess's number of turns is used.

The potentials may depend on `(a,e)`; no derivatives with respect to these
parameters are required. The inequalities are checked at all states,
including atom thresholds where the tails have their specified open-cut
values. Continuously differentiable potentials are a sufficient certificate
class, not a claim that a sharp potential must be smooth. A piecewise smooth
version needs explicit directional conditions at its interfaces.

An attaining path, if present and if the certificate is sharp, can move in a
coordinate direction only where its corresponding derivative inequality is
an equality. This gives concrete complementary-slackness equations for
discovering a candidate law and its response curves.

## 4. A one-dimensional form within a smooth region

Suppose a monotone path piece goes from `(u_0,v_0)` to `(u_1,v_1)` and `f` is
absolutely continuous on `[u_0,u_1]`. Represent the path by a nondecreasing
graph `v=z(u)`, allowing jumps for vertical segments; its values at individual
jumps do not matter to integrals in `du`. The strip imposes

    max(v_0,u-2) <= z(u) <= min(v_1,u).

Integration by parts gives the exact identity

    integral_gamma (f+g)(du+dv)
      = C + integral_{u_0}^{u_1} [g(z(u))-z(u)f'(u)] du,    (3)

where the path-independent part is

    C = integral_{u_0}^{u_1} f(u) du
        + integral_{v_0}^{v_1} g(v) dv
        + f(u_1)v_1-f(u_0)v_0.

Indeed, the only cross term needing manipulation is

    integral_gamma f(u) dv
      = f(u_1)v_1-f(u_0)v_0 - integral_{u_0}^{u_1} z(u)f'(u) du.

If alpha has a density `A(u)`, then `f'=-A` almost everywhere, and the
variable part of (3) is

    integral [g(z(u)) + A(u)z(u)] du.

Thus, away from atoms and the transition, the response is a monotone scalar
optimization with explicit lower and upper obstacles. Where beta has a
density `B(v)`, a freely varying interior maximizing curve must satisfy

    A(u)=B(z(u)),

subject to the monotonicity constraint. This equation is only a necessary
stationarity condition; the maximum may instead occur on an obstacle or use
a pooled constant segment. It cannot be substituted for a global
inequality such as the potential certificate.

For a small rectangle on which both orderings stay inside the strip, (3)
agrees with the exact exchange identity

    J(U then V)-J(V then U)
      = [Delta_u * beta((v_0,v_1])
         - Delta_v * alpha((u_0,u_1])] / 4.

This ties the proposed density calculation directly to the original
capture-time objective. In particular, a claimed simple response shape
requires inequalities comparing the appropriate density averages; it does
not follow merely from symmetry or from using M1/M2 paths.

## 5. Remaining equilibrium step

The theorem in Section 3 replaces an unrestricted princess upper-bound
problem by explicit inequalities in two state coordinates and two parameters.
To close the game by this route, one still needs a specific exact pair of
measures, potentials verifying a constant c, and a princess law giving the
same lower guarantee against every monster. The formulas above impose no
unproved M1/M2 restriction on that lower inequality.
