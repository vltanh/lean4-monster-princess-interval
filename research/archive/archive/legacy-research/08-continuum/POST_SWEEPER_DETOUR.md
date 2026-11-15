# A necessary second inward leg in the continuum candidate

## Scope

The numerical density calculation suggested a three-parameter princess
family consisting of an initial outward leg, an inward leg, an optional
wait at the centre, and a final outward leg. This note proves that an
active path in that family can be strictly improved under the proposed
monster support. The result is an exact path comparison, including atoms;
it is not evidence from discretization.

Consequently, indifference equations for the three-parameter family alone
cannot certify the proposed continuum equilibrium. The missing phase is
an inward leg immediately **after** crossing the monster characteristic
`U=t+p=1`. This timing preserves the late M2 capture branch.

## 1. Candidate support and path family

Consider a symmetric monster law whose unreflected parameter measures have
the following support:

* M1 has an atom of mass `w0` at parameter `-1`, and an arbitrary finite
  nonnegative measure `mu` on `[0,1]`;
* M2 has an arbitrary finite nonnegative measure on `[-1,1]`.

As usual, each displayed path and its reflection have equal probability.
No density, continuity, or monotonicity assumption is needed in this note.

Choose

    0 <= a <= u < 1,      0 <= c < 1.

Define `P(a,u,c)` by its path in characteristic coordinates `(U,V)`:

    (a,-a) -> (u,-a) -> (u,min(u,c)).

If `c>=u`, continue along the diagonal to `(c,c)`; otherwise this diagonal
piece is absent. Then increase U at fixed `V=c` until reaching the endpoint
boundary `U-V=2`, and remain at `p=1` thereafter. Thus the path crosses
`U=1` at `(1,c)`, at time `(1+c)/2`, without a plateau there. The geometric
rules `t=(U+V)/2` and `p=(U-V)/2` make this a legal 1-Lipschitz path.

## 2. An exact improvement

Choose `0<epsilon<1-c`. Follow `P(a,u,c)` until `(U,V)=(1+epsilon,c)`.
Replace the rest of its outward leg by

    (1+epsilon,c)
       -> (1+epsilon,1-epsilon)
       -> (3-epsilon,1-epsilon),

then remain at `p=1`. Call the resulting princess path `Q_epsilon`.
The first added leg moves inward at speed one and ends at
`(t,p)=(1,epsilon)`; the second moves outward at speed one and reaches
`p=1` at time `2-epsilon`. Both paths have exactly the same initial point,
the same crossing of `U=1`, and the same cutoff `b=-c` for the unreflected
M2 family.

**Theorem.** Under the stated monster law,

    E T(M,Q_epsilon) - E T(M,P(a,u,c))
      = (1-epsilon-c)/4 * mu((a,1-epsilon)).              (1)

In particular, the comparison is nonnegative. It is strict whenever the
open interval `(a,1-epsilon)` has positive M1 mass.

**Proof.** Write `A,B` for the first characteristic inverses of P and
`A_epsilon,B_epsilon` for those of Q. The paths agree through `U=1+epsilon`.
They also have the following inverse agreements:

    A_epsilon(z)=A(z)                    for z<=1+epsilon,
    B_epsilon(z)=B(z)                    for z<=c,
    B_epsilon(z)=B(z)=z+1                for z>=1.

For thresholds `1+epsilon<z<=2`, P reaches U=z at time `(z+c)/2`, whereas
Q reaches it at time `(z+1-epsilon)/2`. Thus

    A_epsilon(z)-A(z)=(1-epsilon-c)/2.                    (2)

For an unreflected positive-parameter M1 path with `x<a`, the relevant
inverse is `B(-x)`, whose threshold is nonpositive and hence at most c.
Initial equality `x=a` captures at zero for both paths. For `x>a`, the
inverse is `A(2-x)`: it changes by (2) exactly when `x<1-epsilon`, and is
otherwise unchanged. At `x=1-epsilon`, the first inverse is attained
before the extra inward leg, so equality does not belong to the changed
branch. All reflected positive-parameter M1 captures use `B(2-x)` with
threshold at least one, and are unchanged. The endpoint M1 pair uses
`A(1)` and `B(1)`, also unchanged.

The M2 cutoff stays `b=-c`. The unreflected early branch has `-x<=c` and
uses an unchanged B inverse; the other branches use `A(1)`, `B(3)`, or
initial capture. Reflected M2 captures use `A(-x)` with threshold at most
one, `B(1)`, or initial capture. Thus all M2 capture times agree, including
the exact cutoff and starting-equality cases.

Only the specified unreflected M1 captures change. Integrating their delay
and multiplying by the reflection probability one half proves (1).

## 3. Consequences for a continuum density calculation

If `mu(dx)=f(x) dx`, dominated convergence in (1) gives the limiting gain

    lim_(epsilon->0+) [J(Q_epsilon)-J(P(a,u,c))]
      = (1-c)/4 * integral_a^1 f(x) dx.                  (3)

Whenever `c<1` and `f` has positive mass above a, the original
three-parameter path is therefore not a best response. In particular, a
candidate calculation with active paths approaching `u=1` and `c<1`
must include this extra phase before its indifference equations can be
used for a global upper bound. Letting `u` approach one does not remove
the gain in (3) if a remains below the top of the M1 support.

This also explains why replacing the strict transition condition by a
plateau at `U=1` is unsafe. The added inward leg must have `U>1`, so that
the early/late M2 cutoff remains frozen at c. An inward leg at exactly
`U=1` instead changes that cutoff and generally has a different payoff.

The theorem does not assert that adding this phase completes the response
family. It does not cover negative c, where extra inward movement can
accelerate some unreflected M1 captures with negative B thresholds. A
complete unrestricted upper proof still needs the characteristic
potential inequalities or another globally sufficient argument.

## 4. Exact verification

`packages/interval_post_sweeper_detour/verify.py` checks the individual
capture-time comparison by direct rational intersection of the actual
piecewise-linear paths. It covers zero-length initial legs, both regimes
`c<u` and `c>=u`, starting coincidences, the M2 cutoff, and the
`x=1-epsilon` boundary. The algebraic argument above proves (1) for all
parameters and measures; the finite checks serve as regression tests for
the construction and boundary conventions.
