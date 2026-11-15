# An explicit approximate saddle pair and both responses

Date: 2026-11-11. The exact unrestricted game value remains open.
This checkpoint combines two actual independently certified strategies,
computes their cross payoff exactly, and quantifies every unilateral
improvement. It does not infer global optimality from a finite payoff table.

## 1. The two strategies

The Princess law P_* is the archived ordered, symmetric law in
[`princess_strategy.json`](../../packages/interval_uniform_reduction/princess_strategy.json).
Its 169 displayed paths have integer time and position coordinates divided
by `S=256000000`. Choose displayed index i with probability
`weights_h[i]/100000000`, then independently choose its displayed path or
spatial reflection with probability one half. Interpolate each segment
linearly and remain at the final position afterwards. This gives 338 listed
legal paths, with speeds in {-1,0,1}.

The Monster law M_* is the new law in
[`upper_dyadic_exact.json`](../../packages/interval_global_closure/upper_dyadic_exact.json).
Choose one of its 280 reflected pairs with probability
`weight_numerator/10000000000`, then choose either orientation fairly.
Convert each light vertex (U,V) to ((U+V)/2,(U-V)/2), and interpolate linearly.
All legs have unit speed and every route visits both endpoints.

Write T(M,P) for expected first-capture time. The existing unrestricted
response certificates give, for every legal randomized strategy M or P,

    T(M,P_*) >= L = 36290299773897097/25600000000000000,
    T(M_*,P) <= U = 957063215727541539/671088640000000000.

The first constant is attained by an explicit Monster route. The second
is the Princess-response supremum, with an actual rational response within
1.907889187625e-8. Randomized opponents are included because averaging
preserves the pure-path inequalities.

These are audited mathematical reductions plus exact computation, not Lean
kernel certificates. The global response searches are imported from their
saved certificates here; the new cross-play computation does not rerun them.

## 2. Exact cross payoff and unilateral gains

The new calculation gives

    J = T(M_*,P_*)
      = 74616624991393892648392565953/52428800000000000000000000000
      = 1.423199176624181607215... .

Consequently the maximum Monster improvement is attained and equals

    J-L = 294091054452637992392565953/52428800000000000000000000000
        = 0.005609341706326255653... .

The supremum of possible Princess improvements is

    U-J = 153938737320290085982434047/52428800000000000000000000000
        = 0.002936148401647378654... .

Thus (M_*,P_*) is an explicit epsilon-Nash pair, also called an approximate
saddle pair, for the unrestricted game, with

    epsilon = 294091054452637992392565953/52428800000000000000000000000
            = 0.005609341706326255653... .

The asymmetric statement is sharper: no Monster deviation can lower the
pair's payoff by more than J-L, and no Princess deviation can raise it by
more than U-J. This follows directly from

    T(M_*,P) <= J+(U-J),
    T(M,P_*) >= J-(J-L).

It does not require assuming that the full game has an attained equilibrium.
The sum of the two regrets is exactly U-L, so this construction does not
improve either global game-value bound. It makes the two supplied laws and
their individual incentives explicit.

## 3. Best response to the Princess law

One unrestricted optimal Monster response to P_* has the following vertices:

| Time | Position |
| --- | --- |
| 0 | 11/16 |
| 107999999/128000000 | -19999999/128000000 |
| 127999999/64000000 | 1 |
| 255999999/64000000 | -1 |

Travel at unit speed on each segment, and remain at -1 after the last
vertex. Its reflection has the same payoff. The exact old capture-order
search covered every unrestricted Monster response to this specified
ordered law and recorded 48,228 visited states. The current computation
independently replays all 338 captures of the displayed route and obtains
L exactly. Replaying this route verifies attainment; the exhaustive
capture-order certificate supplies the separate optimality statement.

## 4. Best response to the Monster law

[`upper_dyadic_princess_response.json`](../../packages/interval_global_closure/upper_dyadic_princess_response.json)
contains 158 exact rational vertices of an actual Princess path, together
with every oriented first capture. Its expected payoff is within
1.907889187625e-8 of U. Therefore it improves on P_* against M_* by

    0.0029361293227555024...

and approaches the full Princess gain stated above. The supremum language
matters: no claim of an exactly attaining Princess path is made.

This response is effective against M_*. It is not a new Princess maximin
law. Likewise the Monster route above is optimal against P_*; it is not an
optimal universal Monster strategy.

## 5. New exact computation

[`paired_strategy_regret.cjs`](../../packages/interval_global_closure/paired_strategy_regret.cjs)
puts both supplied laws on the common integer coordinate scale

    D = 524288000000.

All slopes are -1, 0 or 1, so doubled first-capture times are integers in
that scale. The program checks safe-integer bounds before using exact
integer JavaScript arithmetic for geometry; weighted sums and rational
reductions use BigInt.

For every one of the 280 representative Monster routes, it computes
captures against each of the 169 displayed Princess paths and its
reflection. Two separate implementations are compared on all 94,640 such
encounters:

- segment-by-segment relative-velocity intersections;
- independently merged vertex times, zero/sign-change detection, and
  BigInt interpolation across the crossing interval.

Princess symmetry makes each reflected Monster route's weighted payoff
identical, so this accounts for all 189,280 encounters in the full pair.
The 338 captures against the archived attaining Monster are checked again
by both routines. Weight normalization, path legality, endpoint completion,
and L <= J <= U are also checked. The output retains all 280 exact
representative row payoffs.

[`paired_strategy_regret.json`](../../packages/interval_global_closure/paired_strategy_regret.json)
is the exact result.
[`paired_strategy_regret_manifest.json`](../../packages/interval_global_closure/paired_strategy_regret_manifest.json)
pins the source and input hashes.

The calculation was executed in the still-available V8 runtime after
the general executor became unavailable. The Node filesystem wrapper below
was packaged but not itself invoked during the outage:

```sh
node packages/interval_global_closure/paired_strategy_regret.cjs /tmp/paired_strategy_regret.json
```

To replay the separate unrestricted response certificates in a working
environment:

```sh
python packages/interval_uniform_reduction/exact_response.py packages/interval_uniform_reduction/princess_strategy.json
node --stack-size=16384 packages/interval_global_closure/certify_upper_candidate.cjs --verify packages/interval_global_closure/upper_dyadic_exact.json
python packages/interval_global_closure/verify_upper_candidate.py packages/interval_global_closure/upper_dyadic_exact.json /tmp/upper_dyadic_princess_response.json
```

No Lean compilation or CI was run. A matching global pair is still missing.
