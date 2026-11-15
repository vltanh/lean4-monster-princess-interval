# Strict exclusion of the previous exact-value target

## Status

This is **not a solution of the unrestricted Princess and Monster interval game**.
It rules out the specific value c = 56305800187/40000000000, by showing that the
previous 60-path princess mixture is strictly improvable. No new numerical
interval is presented as a substitute for the exact value.

Rules: both players select independent hidden 1-Lipschitz paths in [-1,1],
including their initial positions. Capture is first equality, including time zero.
The monster minimizes expected capture time. The princess maximizes it.

## 1. The specified distribution and its response problem

Let mu be the distribution in princess_strategy.json. All 60 weights are positive,
all path pieces have slopes 0,+1,-1, and all vertex times and positions have
 denominators dividing 100000. The distribution is invariant under reflection.
The file is unchanged from the earlier response certificate.

For this input, unrestricted monster best responses admit the finite capture-order
reduction: start on a hider at time zero; run at speed one; reverse only at a first
meeting with a previously uncaptured hider. There are finitely many such paths.
The reduction does not fix a small number of turns: each segment captures at least
one new hider, so at most 59 positive-time segments are required.

Source for the reduction: S. Alpern, R. Fokkink, R. Lindelauf and G. J. Olsder,
The "Princess and Monster" Game on an Interval, SIAM Journal on Control and
Optimization 47(3), 1178-1190 (2008), DOI 10.1137/060672054, Proposition 5.

It applies to every positive reweighting of this same support.

## 2. ALL minimizing capture-order paths

The new enumeration uses exact integer arithmetic. It discards a branch only
when its independent-target lower bound is STRICTLY greater than the current
incumbent. It does not discard a branch with equal lower bound and does not use
any dominance pruning. Thus it retains every minimizing path, rather than only
one minimizing response.

The enumeration visits 751782 states and makes 375887 strict lower-bound prunes.
There are 34 distinct possible initial positions. Five completed routes are
encountered as the incumbent improves; exactly two attain the final minimum c.
After removal of collinear intermediate vertices, they are m and its reflection:

    (time, position)
    (0, -5/16)
    (131249/200000, 68749/200000)
    (199999/100000, -1)
    (399999/100000, +1).

Behavior after all 60 hiders are captured is immaterial.

The lower-bound pruning rule at state (captured set, time, position, incurred
weighted cost) adds, for each uncaptured target independently, its weight times
its earliest possible interception time. Any actual continuation is at least
this costly. This argument only needs that targets have speed at most one.
The verifier explores both directions at every remaining first-capture event.

## 3. Endpoint test

Let eta choose the stationary hider +1 or -1 with equal probabilities. Each of
m and its reflection first reaches one endpoint at 2-1/100000 and the other at
4-1/100000. Hence

    E_eta T(m,P) = E_eta T(-m,P) = b = 299999/100000.

Every mixture of these two response paths has the same payoff b against eta.
In particular, these paths cannot supply a matching monster-side guarantee c.

The next section proves the stronger statement V > c without relying on any
attainment theorem for the unrestricted game.

## 4. A finite-support perturbation proves strict exclusion

The canonical response family depends on the hider paths, not their positive
weights. Every canonical response has its event times in (1/200000) Z.
To see this, write u=t+x and v=t-x. Initially u,v belong to (1/100000) Z.
A speed-one monster ray holds one coordinate fixed. At an encounter with an
oppositely moving hider, the other coordinate equals a hider piece's line
intercept, also in (1/100000) Z. At a stationary hider x=a, u-v=2a gives the same
conclusion. Thus t=(u+v)/2 belongs to (1/200000) Z at every event.

The old hider probabilities have denominator dividing 200000. Therefore the
old payoff of EVERY canonical response is an integer multiple of

    d = 1/40000000000.

Since the enumeration found all minimizers, any other canonical response has
old payoff at least c+d.

Set theta=1/1000000000000 and let

    mu_theta = (1-theta) mu + theta eta.

The two endpoint hiders already belong to the support of mu, so mu_theta has
exactly the same path support, with positive weights. The same canonical response
family therefore suffices.

For each old minimizer its new payoff is

    c_theta = (1-theta)c + theta b.

For any other canonical response its new payoff is at least

    (1-theta)(c+d),

because capture times against eta are nonnegative. Exact rational arithmetic
checks

    (1-theta)d > theta b.

Thus every other canonical response is strictly more expensive than c_theta.
The two old minimizers remain the minimizing canonical responses to mu_theta.
The capture-order reduction gives the exact unrestricted response value

    inf_m E_mu_theta T(m,P) = c_theta > c.

Consequently V > c. This excludes c as the full-game value. The tiny increase
is used only to certify strict exclusion, not presented as an exact solution or
as a new numerical target.

## 5. Scope of the computation

This result does NOT identify the unrestricted value V. It does NOT establish a
bounded family containing an equilibrium. It does NOT show that every finite
princess mixture is suboptimal, only that this particular one is.

The accompanying proof uses a published structural reduction plus exact
exhaustive computation. It is not a Lean formalization or an external review.

## 6. Reproduce

Run, from this directory:

    python verify_target.py

Only Python's standard library is used. The command repeats the full exact
all-minimizer enumeration, checks the two paths, checks their endpoint capture
times, and verifies the strict perturbation inequalities. The saved JSON output
is a reproducibility record, not a substitute for running the verifier.