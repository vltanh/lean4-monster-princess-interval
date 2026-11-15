# Exact response calculation and elimination of earlier candidate values

## Status

**This is not a solution of the unrestricted interval game.** It gives an explicit finite princess distribution and proves the exact value of its unrestricted monster-response problem:

    inf over all admissible monster paths m of E_mu T(m,P)
      = 56305800187 / 40000000000
      = 1.407645004675.

Consequently neither 11/8 nor a value near 1.373 can be the unrestricted game's value, under the rules stated below. This conclusion is a mathematical/computational result of the supplied certificate, not a claim that a new literature record has been established. No matching upper saddle inequality has been proved.

The computation was checked using two implementations: Python integer arithmetic and C++ GMP rational arithmetic. A separate Fraction-based intersection routine checked every capture time of an attaining monster. Forty small regression cases agree with the previous unpruned Fraction oracle. These are reproducibility checks, not a Lean formalization or independent external review.

## 1. Rules

The arena is [-1,1]. Each player independently selects a hidden path. Both paths have Lipschitz constant at most one. Initial positions are chosen by the players, not prescribed or sampled by an external rule. Capture is the first equality of positions, including time zero. The monster minimizes and the princess maximizes expected capture time.

The displayed princess strategy is also admissible when the princess is allowed arbitrary continuous motion. The certificate restricts neither the monster's initial position nor its number of turns a priori.

## 2. Explicit princess distribution

Set epsilon = 1/100000. For a table row (a,b,u), except the endpoint row a=1, put

    A = max(a, 2 epsilon),
    B = min(A, max(b, epsilon)),
    U = max(A, u-epsilon).

The positive princess path has vertices

    (0,A), (U-A,A), (U-B,B), (U+1-2B,1),

and then stays at +1. Repeated identical vertices are removed. The first coordinate is time. Thus the princess waits, moves left at speed one, turns, moves right at speed one, and stays at the endpoint. The different values of u are essential: these are not the old family with a common departure timing.

For a=1, the positive path stays at +1 from time zero. Select a row with probability n/100000 and then select its displayed path or its reflection with probability 1/2. Equivalently each of the sixty actual paths has probability n/200000. All entries in the last column are positive and their sum is 100000.

| Row | a | b | u | n |
|---:|---:|---:|---:|---:|
| 1 | 0 | 0 | 1 | 2585 |
| 2 | 1/16 | 0 | 1 | 1742 |
| 3 | 1/8 | 0 | 1 | 1765 |
| 4 | 3/16 | 0 | 15/16 | 1820 |
| 5 | 1/4 | 0 | 15/16 | 3964 |
| 6 | 5/16 | 0 | 15/16 | 1926 |
| 7 | 3/8 | 0 | 15/16 | 3517 |
| 8 | 7/16 | 0 | 15/16 | 2051 |
| 9 | 1/2 | 0 | 15/16 | 6734 |
| 10 | 9/16 | 0 | 15/16 | 2404 |
| 11 | 5/8 | 0 | 11/16 | 3454 |
| 12 | 5/8 | 0 | 7/8 | 2960 |
| 13 | 5/8 | 0 | 15/16 | 2956 |
| 14 | 11/16 | 0 | 3/4 | 3710 |
| 15 | 11/16 | 0 | 13/16 | 648 |
| 16 | 11/16 | 0 | 7/8 | 3334 |
| 17 | 11/16 | 0 | 1 | 1594 |
| 18 | 3/4 | 0 | 13/16 | 9973 |
| 19 | 13/16 | 0 | 7/8 | 9602 |
| 20 | 7/8 | 0 | 15/16 | 9708 |
| 21 | 7/8 | 3/16 | 15/16 | 114 |
| 22 | 15/16 | 0 | 1 | 864 |
| 23 | 15/16 | 3/16 | 1 | 4459 |
| 24 | 15/16 | 1/4 | 1 | 2880 |
| 25 | 15/16 | 5/16 | 1 | 943 |
| 26 | 15/16 | 3/8 | 1 | 1269 |
| 27 | 15/16 | 3/4 | 1 | 1113 |
| 28 | 15/16 | 13/16 | 1 | 1741 |
| 29 | 15/16 | 7/8 | 1 | 3121 |
| 30 | 1 | 1 | 1 | 7049 |

Every path lies in the interval and has speed 0 or 1. Epsilon is the specified positive rational number, not a limit or an unverified small-parameter approximation. `princess_strategy.json` lists all actual rational vertices and probabilities.

## 3. An attaining monster

Let x=-5/16 and tau=(1-x-epsilon)/2. Use the monster path

    m(t)=x+t                 for 0 <= t <= tau;
    m(t)=1-epsilon-t         for tau <= t <= 2-epsilon;
    m(t)=t-3+epsilon         for 2-epsilon <= t <= 4-epsilon.

It can remain at +1 afterward. Its vertices are

    (0,-5/16),
    (131249/200000,68749/200000),
    (199999/100000,-1),
    (399999/100000,1).

Intersecting this path with each of the sixty princess paths gives a weighted capture-time sum exactly equal to 56305800187/40000000000. The full capture vector is in `attaining_monster.json`. This proves the response value is AT MOST that number. The next sections establish the other inequality against every monster path.

## 4. Why the monster-response search is exhaustive

For a finitely supported princess distribution, an optimal response can be chosen to start at one of the princess initial positions and run at maximum speed, changing direction only upon a first encounter with a previously uncaptured princess path. This is the capture-order reduction in Proposition 5 of Alpern, Fokkink, Lindelauf and Olsder, *The “Princess and Monster” Game on an Interval* (SIAM J. Control Optim. 47(3), 1178–1190, 2008; DOI 10.1137/060672054). The accessible 2006 preprint gives the same proposition.

For completeness, the initial capture can be moved to time zero by starting at that princess's initial point and shadowing her until the original capture time. This cannot delay any original capture. Between successive new captures, move directly at speed one toward the next target. The target has speed at most one, so it cannot escape across or behind this ray before being met. This reaches it no later than the original route did. Shadowing until the original meeting time would allow the original continuation, so earlier arrival cannot hurt. Repeating the exchange removes waits and reversals between new captures. Incidental extra captures only help.

At each event there are just two directions. A speed-one ray cannot be overtaken by an uncaught target that is strictly behind it. In a chosen direction, the next event is the first meeting with any currently uncaught path ahead. Every positive-time step captures at least one new path. With n paths there are at most n-1 such steps after an initial capture. Paths that never catch a positive-probability target have infinite expectation and cannot improve on the displayed finite response.

For this input there are sixty target paths and thirty-four distinct starting positions. The algorithm explores the resulting capture-order tree, using the two exact pruning lemmas below.

### 4.1 Independent-target lower-bound pruning

At state (S,t,x,C), S is the captured set, (t,x) the current event, and C the sum of weighted capture times already incurred. For each remaining target j, let h_j be the earliest possible meeting time from (t,x), found by moving directly toward its current position at speed one.

Every continuation has total payoff at least

    C + sum_{j not in S} w_j h_j.

The earliest meetings need not be mutually achievable; that only makes this a weaker lower bound. If this bound is at least the payoff of an already known complete route, the state cannot improve the incumbent and is safely discarded. All comparisons are exact.

### 4.2 Dominance pruning

A capture-event state includes an anchor target j with current monster position p_j(t). Suppose the same captured set S and same anchor j have previously been reached at t' <= t with already-incurred cost C' <= C.

The earlier monster can shadow target j until time t, then follow any proposed continuation of the later state. It incurs no greater cost for S. Any additional targets met during shadowing are caught earlier, which only helps. Thus the later state is dominated. The verifier keeps all non-dominated pairs (time,cost), not just the earliest time or cheapest cost separately.

Neither pruning rule assumes a specific number of reversals, a preselected monster family, or a numerical tolerance.

## 5. Why integer arithmetic is exact here

All princess vertices have rational times and positions with denominators dividing D=100000. Every princess piece has slope -1, 0 or +1. For each speed-one monster segment, one of the coordinates

    u=t+x,  v=t-x

is constant. At the initial point both coordinates are multiples of 1/D. When the monster meets an oppositely moving princess piece, the other coordinate is that piece's rational line intercept, also a multiple of 1/D. When it meets a stationary piece at position a, the coordinates differ by 2a, again a multiple of 1/D. The same-velocity case cannot cause a new encounter from a positive separation.

It follows inductively that every capture-order candidate has all its event times and positions in (1/(2D)) Z. Therefore scaling times and positions by 200000 loses no candidate in the finite reduction. This is not an imposed numerical time mesh on the unrestricted game: it is an exact consequence of the specified hider paths and the capture-order theorem.

Each actual path probability has denominator dividing 200000. Weighted objective numerators are consequently integers over the common denominator 40000000000. The integer verifier uses Python's arbitrary-precision integers. It checks divisibility whenever an intersection is formed; it never rounds a capture time.

## 6. Completed exact checks

The Python integer search returns:

    value                    56305800187/40000000000
    visited states           27677
    complete routes reached  4
    lower-bound prunes       8390
    dominance prunes         5446
    memo keys                6366
    distinct initial points  34

The four complete routes are the leaves that remain after valid exact pruning. They are not an assertion that the unpruned game has only four cases.

The C++ rational search returns the same exact minimum. It visits 27769 states because its tie-breaking order is different. Its arithmetic is GMP rational arithmetic rather than the integer-lattice specialization. A separate Fraction intersection implementation verified all sixty capture times of the attaining route. Forty deterministic-seed small test instances agree with the previous unpruned Fraction response solver.

Together, exhaustive search with valid pruning proves every monster response costs at least the reported value, while the displayed route attains it. This establishes the equality in the status statement.

## 7. Verification

With Python 3 and no third-party packages:

    python verify.py princess_strategy.json --expect 56305800187/40000000000
    python tests.py

The first command performs the exact unrestricted response search afresh. The second checks the explicit attaining route and the forty small regression instances, including comparison with the unpruned reference implementation.

Optional second implementation (requires a C++ compiler, GMP, and Boost headers):

    g++ -O3 -std=c++17 verify_gmp.cpp -lgmpxx -lgmp -o verify_gmp
    ./verify_gmp princess_strategy_gmp.txt

The binary is intentionally not included. The discovery optimizers are not needed for either verification.

## 8. An exact rejection of a candidate monster distribution

The fixed-hider optimization also produced a candidate monster mixture. Rationalizing that candidate does not make it a saddle strategy. The file `rejected_monster_candidate.json` specifies sixty monster paths with rational weights and an explicit admissible princess response starting at 29/32.

Direct exact intersection gives that princess an expected payoff

    20281364461051 / 12000000000000 = 1.69011370508758... .

This is much greater than the fixed-hider value L. The file contains the actual princess vertices and all sixty capture times; `tests.py` checks them. This is an explicit counterexample to that particular attempted monster certificate, not an assertion that every monster mixture fails at L.

## 9. What remains unsolved

Let mu denote the explicit princess distribution above and L its exact response value. The result is

    inf_m E_mu T(m,P) = L.

It does not imply

    inf_nu sup_p E_nu T(M,p) = L.

No monster distribution with worst-case performance L has been found or certified. Nor has a higher matching saddle value been established. Numerical optimization over richer finite families and noncrossing rearrangements produced additional candidates, but their unrestricted responses did not close a saddle-point equality. Those exploratory decimal values are not promoted to theorems here.

The previously supplied deadline theorem still applies to specified finite monster mixtures. The work in this package uses the complementary response reduction to make a decisive test of previously suggested values. It does not prove that an unrestricted equilibrium belongs to a bounded finite family.
