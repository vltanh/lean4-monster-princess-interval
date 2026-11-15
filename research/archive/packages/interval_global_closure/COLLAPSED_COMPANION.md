# A collapsed ordinary companion for a finite germ Monster law

## Statement and scope

Let a finite symmetric paired Monster law have paths m_i^epsilon and probabilities
w_i^epsilon, all defined for sufficiently small positive epsilon. The paths are
legal, start at time zero, and have a fixed finite list of piecewise-linear
vertices whose time and position coordinates have finite limits. Their
probabilities are nonnegative and sum exactly to one. Each positive-weight
path visits both endpoints by a common finite horizon H. The germ atomic
oracle's complete unit-leg inputs satisfy these hypotheses.

Collapse every vertex and probability jointly to its limit. Delete repeated
equal-time vertices, discard zero limiting weights, and optionally merge
collinear legs and reflection-equivalent paired atoms. The result is a legal,
normalized, ordinary Monster law nu_0. If U denotes unrestricted expected
capture time maximized over Princess paths, then

    U(nu_0) <= liminf_{epsilon -> 0+} U(nu_epsilon).

This constructs a SEPARATE ordinary upper strategy. It does not assert equality
of responses, equality of capture order, or preservation of payoffs against
a Princess strategy that varies with epsilon.

## Uniform convergence of the physical paths

Write the vertices as (t_j^epsilon,x_j^epsilon), and their limits as
(t_j^0,x_j^0). Legality gives

    |x_{j+1}^epsilon-x_j^epsilon|
       <= t_{j+1}^epsilon-t_j^epsilon.

The same inequality holds in the limit. Consequently, equal limiting times
have equal limiting positions. Deleting a zero-duration leg therefore removes
a repeated physical point, not a jump.

Let Delta_t and Delta_x be the largest vertex time and position errors.
Interpolate both vertex lists using the same polygonal parameter. Their
interpolated coordinates differ by at most Delta_t and Delta_x. The limiting
physical path is 1-Lipschitz, so, with constant extension past the last vertex,

    sup_t |m_i^epsilon(t)-m_i^0(t)| <= Delta_x + Delta_t.

This remains valid across collapsed legs. Endpoint visits survive: an exact
visit at an original vertex has the same limiting endpoint. A path that
visits both endpoints captures every continuous Princess path by the second
endpoint visit, by the intermediate value theorem. Thus the common finite
capture horizon is preserved.

For unit-leg inputs, any limiting leg of positive duration has slope exactly
+1 or -1. Deleting zero-duration legs cannot create a nonunit leg. A fixed
finite unit-leg list cannot average to a slower segment. Such averaging would
require an increasing number of turns, outside this finite-list construction.

The geometric collapse helper also accepts general legal piecewise-linear
inputs. Their limit can have nonunit segments, and the inequality still holds.
The ordinary atomic response adapter explicitly rejects those unsupported
segments instead of replacing them by unit legs.

## First capture and the supremum

Fix ONE Princess path p independently of epsilon. Write tau_epsilon for its
first capture by m_i^epsilon. Take any subsequence realizing liminf tau_epsilon.
The common horizon permits a further subsequence tau_epsilon -> t*. Uniform
convergence of the Monster paths and continuity of p imply

    m_i^0(t*) = p(t*).

Hence tau_0 <= t* = liminf tau_epsilon. Equivalently, before any time strictly
less than tau_0, the two limiting continuous paths have a positive separation
on the compact interval, which uniform convergence preserves.

Finite nonnegative probability convergence now gives

    J(nu_0,p) <= liminf J(nu_epsilon,p)
              <= liminf U(nu_epsilon).

Zero limiting weights contribute zero; the common horizon also makes their
entire expected contribution tend to zero. Taking the supremum over fixed
Princess paths p proves the result. There is no interchange of a supremum
and a limit: every fixed p has the same upper bound on the right.

The semicontinuity argument itself extends to locally uniform convergence
without a common finite horizon, using nonnegative extended capture times.
The implemented finite ordinary companion requires finite vertex limits and
endpoint completion, so it retains a finite, directly evaluable upper law.

## Why a varying Princess must not be substituted

Let the Princess law be the stationary pair p_epsilon=+epsilon and
p_epsilon=-epsilon. Let the Monster start at +epsilon, move left to -1,
then right to +1. The original pair cost is epsilon: the positive Princess is
caught initially and the negative one at time 2 epsilon.

The collapsed Monster starts at zero, moves left to -1, then right to +1.
Against the SAME varying Princess pair its cost is 1+epsilon. Thus even the
limiting payoff against a varying Princess law can increase, from 0 to 1,
under Monster collapse. This does not contradict the unrestricted upper
inequality, whose proof fixes p before passing to the limit.

In particular, a master must keep the original germ Monster columns and
already constructed physical Princess rows unchanged. The companion is a new
ordinary law, evaluated by its own complete upper oracle.

## Exact helper

The portable module collapsed_companion.cjs exports

    createCollapsedCompanion(E,G)

where E is atomic_survival_v8.cjs and G is the validated germ arithmetic/path
oracle. Its methods are:

- collapseRoute(atom, options): validate the eventual legal geometry, collapse
  exact light or physical coordinates, delete zero-duration legs, and report
  completeness and any nonunit limiting segments.
- collapseLaw(atoms, probabilities, options): collapse the finite normalized
  law, discard zero limiting weights, and merge identical/reflected paired
  routes. It returns exact rational probabilities and common integer
  numerators/denominator.
- standardResponse(law, options): run the independent ordinary rational
  atomic engine. The default is an exact integer maximum-flow certificate,
  followed by independent capacity/conservation/cut replay.
- companion(atoms, probabilities, options): perform both steps.

The optional exact:false mode returns a numerical ordinary response for
discovery, explicitly without a certificate. Neither mode silently modifies
a genuinely nonunit limit. Reflection merging assumes the symmetric paired-law
convention used by both atomic engines.

## Regression obligations

The verifier checks the six germ upper fixtures against their separate exact
ordinary companions, including integer-flow replay. Strict examples are

    shifted_M1:           7/4 -> 53/32
    general_inward:       9/4 -> 33/16
    nested_initial_layer: 2   -> 3/2.

The first two improvements do not require a zero-duration limiting leg;
coincident event levels alone can lower the response. Additional checks cover
zero limiting probabilities, reflection merging, repeated vertices, legal
nonunit limits, invalid instantaneous jumps, probability normalization,
fixed-Princess semicontinuity, the explicit varying-Princess counterexample,
and the uniform physical convergence estimate.

This is a structural comparison and an upper-law construction. It does not
produce a matching lower law or settle the unrestricted game.
