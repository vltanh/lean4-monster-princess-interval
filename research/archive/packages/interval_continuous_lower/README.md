# Continuous geometry search with an exact bank floor

This optimizer keeps two quantities separate:

1. A **fixed exact normalized-bank floor**, checked against the complete
   physical response bank before accepting a field.
2. The minimum exact cost among a changing finite bank of **continuous
   physical attacking paths**, which is an upper screen on the fixed
   full-width field's security. It is never a Princess lower certificate.

Native causal-calendar inequalities enforce the fixed floor and contain no
continuous-objective variable. Exact continuous supporting-clock planes
bound a separate objective. The sparse event LP therefore never equates the
sampled bank value with the full-width CDF's continuous security.

## New transport geometry

Every full nodal Qout variable is available. Only currently charged nodes are
explicit in the LP. Exact projected cone order and closest-seed envelope
clamping come from `interval_sparse_lower`; no seed equality component or
coarse-profile restriction is imposed. The optimizer minimizes event L1
displacement at an intermediate continuous objective level, then checks the
repaired integer field.

Cached physical paths separate bank-floor violations. Exact rescoring of each
continuous path separates its new active clocks. When both screens clear,
the complete integer oracle decides whether the bank floor really holds.
The lowest native witness is also integrated as a continuous physical attack.
Seeded floating searches in several additional path families discover new
rational attacks; their scores and supporting planes are recomputed exactly
before entering the objective. Finite attack families supply no lower bound.

The default bank allowance is explicitly `1/10000000` below the completely
priced seed. The floating discovery LP uses a small additional strengthening
buffer, while the exact acceptance comparison uses the declared rational
floor without numerical tolerance. A successful geometry update may improve
the continuous attack screen without improving the certified game lower.

```bash
python packages/interval_continuous_lower/test_continuous_lower.py
python packages/interval_continuous_lower/search.py \
  --n 256 --oracle center --radius .002 --seconds 2400 \
  --iterations 100 --lp-seconds 180 --keep 16 --cached-keep 128 \
  --attack-seconds 40 --attack-starts 4 --new-attacks 2 \
  --output /tmp/continuous-princess
```

The center oracle uses the independently reviewed discrete normal form and
records its own source hash and policy. `--oracle classic` uses the original
complete oracle. A prospective new global lower from the accelerated engine
requires the original exact verifier and independent BigInt replay before
promotion. The retained seed's existing exact report can be reused only when
its field bytes and verifier hash match; no inherited certificate is assigned
to a different field or mesh.

`incumbent.field.json` includes a complete bank certificate. Every exact
trial is now saved immediately after the model returns it, before cached
response screening, as
`trials/trial_<iteration>_<full-JSON-SHA256>.field.json.gz`. Its history row
binds the relative path, compressed-file SHA-256, JSON SHA-256 and decoded
nodal SHA-256. Trial files contain no security certificate. Exclusive atomic
creation preserves an earlier candidate even if a stale checkpoint retries
the same iteration with a different field; matching content is reused and
conflicting content fails explicitly.

Exact continuous clock planes, newly generated rational routes, randomized
search reports and checkpoints are retained as well. `--resume` checks the
incumbent, seed and retained-trial hashes and restores the exact floor, all
discovery rows and the attack bank. Older checkpoints without trial references
remain readable. The same full-width CDF is not assigned the game-value
transfer bound; its continuous screen remains an upper attack value.

The strict regression compares the sparse two-objective LP against an
independent full-grid LP, checks old supporting planes on different exact
fields, and runs complete tiny-bank integer searches. These tests verify the
implementation's scope distinctions; they do not establish an equilibrium
or a width below `1e-4`.

## Hybrid continuous records

`hybrid_lp.py` implements the conservative continuous-route secant
hypograph from [the proof](../../research/12-global-closure/CONTINUOUS_RECORD_HYPOGRAPHS.md).
It keeps ordinary cached-calendar rows and promotes only explicitly selected
physical paths to exact discrete running records. The same persistent main
and proximal LPs accommodate both these records and the continuous route
charges, including noncontiguous variable appends. Increasing stretches,
zero slopes, initial endpoint capture and interior endpoint traces are
handled separately. Waiting legs are rejected.

The optimized secant score is an inner approximation to the specified-route
objective; its optimum is **not an upper bound** on exact continuous-route
optimization. The old search objective cap of three is removed because a
specified inefficient physical route can have mean capture time above three.
Exact rational rescoring and complete response pricing remain necessary.

```bash
python3 -B packages/interval_continuous_lower/test_hybrid_lp.py
```

The differential regression checks 90 fixed-field LP scores against exact
secant evaluation and chronological integration, 12 independent full-node
LPs for promoted discrete routes, 12 changed-field/incremental-append cases,
six endpoint-atom fields, and five rejected invalid routes. These checks
verify the implementation; they supply no new unrestricted bound.

`search.py` and `front_search.py` accept `--bank-model hybrid`,
`--continuous-secants K`, and `--promotion-after N`. Every continuous
route scored by the driver also gets its conservative secant hypograph;
ordinary supporting clock planes remain valid additional constraints.
An optional `--route-bank FILE` supplies a JSON list (or a `routes` member)
of additional physical routes. These routes can have either initial sign
and arbitrary legal turn times; no positive-start or time-one restriction
is imposed.

Every repeated cached violation still adds its new calendar when available.
At the declared repetition threshold its entire discrete history is
promoted to exact records. Checkpoints retain the promoted paths, violation
counts, continuous routes, and secant count. Resume rejects a changed bank
model or secant count. All exact candidates are retained before screening,
and the existing complete response oracle still controls acceptance.

```bash
python3 -B packages/interval_continuous_lower/test_hybrid_search.py
python3 -B packages/interval_continuous_lower/front_search.py \
  --bank-model hybrid --continuous-secants 8 --promotion-after 3 \
  --n 256 --oracle center --initial-routes 1292 --initial-attacks 0 \
  --route-bank packages/interval_quantile_certificate/earlier_front_probe.json \
  --radius .004 --bank-slack 1/20000 --seconds 420 --iterations 24 \
  --lp-seconds 90 --cached-keep 256 --keep 16 --attack-seconds 0 \
  --output /tmp/pr1-hybrid-front-pilot
```

The driver regression runs both ordinary and front-two tiny searches,
resumes each checkpoint, verifies eight retained trial fields and their
exact cached scores, and rejects a changed secant count. The reported LP
secant objective is explicitly labeled as an inner model value, never an
upper bound on exact optimization or a lower security certificate.

## Globally sufficient incoming-front variant

`front_search.py` imposes the proved incoming-front `U=t+radius=2`
identities. It maps every native-calendar and continuous-plane coefficient
to the canonical front coordinate with the same `W=t-radius`, or to zero
when `W>=2`. The exact full-grid clamp is then projected by the same map.
The sparse LP is exactly the front-two nodal subpolytope, with no additional
coarse-profile restriction. This removes 65,536 independent variables from
the n256 pre-two domain before sparse event selection.

The default seed is the committed exact projection of the retained n256
field. Its source field, source verifier replay, lower fraction and complete
projection are checked exactly. The inherited bank lower is recorded as a
lower bound with `minimum_is_exact=false`; it is never presented as a new
computed minimum or given an attaining witness. A subsequently completely
priced accepted candidate receives its actual exact minimum. Existing
complete certificates and the projection's per-path record monotonicity
justify the inherited floor.

```bash
python packages/interval_continuous_lower/test_front_model.py
python packages/interval_continuous_lower/front_search.py \
  --n 256 --oracle center --radius .01 --bank-slack 1/20000 \
  --seconds 2400 --iterations 100 --lp-seconds 180 \
  --keep 16 --cached-keep 128 --attack-seconds 40 --new-attacks 2 \
  --output /tmp/continuous-front-princess
```

The additional regression compares this event model with an independent
full-node LP containing explicit front equalities, verifies exact coefficient
substitution on changed fields, and checks complete tiny-bank prices before
and after projection. The larger bank allowance above is an explicit
`5e-5` exploration tradeoff, not an unchanged-security assertion.

## Enforce every calendar for each selected physical path

The optional `--bank-model records` replaces successive active-calendar cuts
with an exact running-record hypograph for each admitted physical path.
For a fixed field, each active endpoint clock has variables `r_j` bounded
above by its previous record and its current price `1+g` or `1-g`.
The path floor is `sum(weight_j*r_j)/(4*n) >= floor`. Every feasible auxiliary
record is at most the actual running minimum; the actual running minima
themselves are feasible. Consequently this existential LP constraint is
equivalent to **every causal calendar for that physical path** costing at
least the floor. A finite physical bank still gives no complete security
claim: exhaustive response pricing remains mandatory before acceptance.

The implementation omits copies on increasing-price stretches and, strictly
after the first center sample, caps on the opposite side whose prices remain
at least one. It processes the time-two entry sample and then aggregates
the constant record through that clock's actual first endpoint time. For
front-two fields the same aggregation starts at the first postcenter front
contact, after its entry sample. Endpoint clocks stop before their own first
endpoint sample, including endpoint starts. The other clock still sees the
interior endpoint trace. No fixed physical path is shortened by this model.

Identical record-prefix histories share auxiliary variables across paths.
All actual maximal records are simultaneously feasible, so this sharing
preserves the projected feasible set of CDFs. Physical paths are deduplicated
by their entire route, not by one currently active calendar. The proximal
model penalizes only CDF movement and leaves record variables unpenalized.

```bash
python packages/interval_continuous_lower/test_record_lp.py
python packages/interval_continuous_lower/front_search.py \
  --bank-model records --n 256 --oracle center \
  --initial-routes 32 --cached-keep 16 --keep 16 \
  --radius .002 --bank-slack 1/10000000 \
  --seconds 2400 --iterations 100 --lp-seconds 180 \
  --output /tmp/continuous-front-records
```

An initial 128-path cold model exhausted a 90-second LP budget. With 32 initial
paths, shared histories, and the exact front aggregation, a bounded n256
pilot completed three iterations in about 50 seconds: the first main/prox
solves took 7.5/15.3 seconds and subsequent solves took 2.3--3.5 seconds.
Each iteration exposed 16 additional physical paths from the held-out cache;
none produced an accepted field or a new lower bound. This establishes a
workable model size, not convergence or mathematical improvement.

The differential regression checks 84 fixed-field costs against exact cached
pricing and auxiliary LP optima, then compares 12 sparse compressed models
with independent full-node LPs containing every clock tick. Endpoint starts,
first center exactly at time two, post-two tours, front projection, and
dynamic variable appends are included.

## Completed record-model CI campaign

[Run 43547653603](https://github.com/vltanh/lean4-monster-princess/actions/runs/43547653603),
commit `f79b812c4b2362934c568880027fc0201d657078`, completed all three
discovery jobs and the exact regressions. **No candidate was accepted and
no unrestricted bound improved.** Each job ended with `LP_BUDGET_STOPPED`
when a main LP reached its declared 180-second solve limit.

| Family | Radius / bank allowance | Completed iterations | Retained physical paths | Last exact floor violation | Elapsed seconds |
| --- | --- | ---: | ---: | ---: | ---: |
| full-strict | `.004` / `1e-7` | 12 | 224 | `0.004997290223388672` | 814.06 |
| front-strict | `.004` / `1e-7` | 10 | 192 | `0.00702276013671875` | 821.36 |
| front-flexible | `.02` / `5e-5` | 7 | 144 | `0.027958454860839844` | 669.83 |

Every completed iteration failed the exact cached-bank floor and added 16
new physical paths to its LP. All those paths were already in the supplied
1,292-path cache. No trial reached continuous rescoring or complete response
pricing; the final incumbents' decoded nodal hashes equal their seeds.
Thus these failures diagnose incomplete physical-constraint coverage and
the cost of its exact auxiliary representation. They do not demonstrate
infeasibility of an improving CDF or a ceiling for the whole front class.
The observed violations greatly exceed rounding tolerances.

The last successful main LPs contained respectively **506,954**, **322,776**,
and **234,023** rows, including **190,029**, **116,800**, and **81,696**
record variables. They took 146.0, 148.2, and 156.0 seconds. Reconstructing
the next models from the retained path constraints, without solving them,
gives 538,558, 345,482, and 262,745 rows. The record formulation removed
calendar ambiguity for admitted paths, but this campaign did not reach
enough of the physical bank before LP cost became limiting. Additional
continuous-clock machinery would not alone resolve this observed gate.

The artifacts preserve seeds, source hashes, exact rejection values,
selected paths, initial continuous planes, solver statistics, and resumable
checkpoints:

- [full-strict, artifact 14094598300](https://github.com/vltanh/lean4-monster-princess/actions/runs/43547653603/artifacts/14094598300), ZIP SHA-256 `c503083f471f941084fa769cd5b9f93bb948c3211b6c409d25b63224010e94bb`.
- [front-strict, artifact 14095686629](https://github.com/vltanh/lean4-monster-princess/actions/runs/43547653603/artifacts/14095686629), ZIP SHA-256 `c63c6bb9902eba93fdfa3e64001a8e6fce083dbaec51051b0aa5da7f0eef25d7`.
- [front-flexible, artifact 14094892253](https://github.com/vltanh/lean4-monster-princess/actions/runs/43547653603/artifacts/14094892253), ZIP SHA-256 `58d430dfc122790581f8f49c7a3df77d1dfba8730ce3658a70fa219c4527595b`.

All three archive digests and their manifest file hashes were checked after
download. Those historical artifacts did not save cached-rejected trial
field arrays; their recorded exact costs cannot be replayed from the fields
alone. The retention change described above fixes that gap for future runs;
it does not reconstruct the missing historical candidates.

The targeted regression exercises actual cached-floor rejection with two
prescribed legal fields, replays both saved fields' exact cached costs, and
simulates a stale-checkpoint restart at the same iteration. It also checks
idempotent reuse and rejection of corrupt existing bytes, without numerical
optimization or a large response search:

```bash
python packages/interval_continuous_lower/test_trial_retention.py
```

## Earlier incoming-front probe

The aligned projection `Gamma_(237/128)` is allowed by
[the discrete front theorem, section 7](../../research/12-global-closure/DISCRETE_CENTER_BALANCE_PRICING.md).
On the retained n256 source it changes **8,028** values relative to the
front-two field, while preserving an inherited bank lower. Exact rescoring
leaves all nine saved continuous route costs unchanged. One retained
five-run physical path costs `291545780947/204800000000`, only
`140253/409600000000` (about `3.42415e-7`) above the inherited bank lower.
This is a one-path upper on this particular n256 bank minimum, not a new
minimum or a game upper bound.

The dyadic two-turn attack still costs
`14570592687/10240000000 = 1.42290944208984375`. Its nonincreasing survival
function also bounds every compatible exact full-width refinement's
standard `bank_minimum - 1/(2N)` certificate by that same number. The earlier
projection therefore leaves the existing fixed-geometry refinement ceiling
in place. A separately extracted narrow Princess law is a different law;
no security upper for it is asserted here.

The compact [probe and fixture](../interval_quantile_certificate/earlier_front_probe.py)
bind both source hashes, regenerate the projected nodes, replay the nine
continuous attacks and the one native path, and check the refinement
inequality at N=256,512,1024:

```bash
python packages/interval_quantile_certificate/earlier_front_probe.py
```

This targeted check passed in about 17 seconds with 1,572,864 transport
inequalities checked. It constructs no full fine-grid field and runs no
complete response oracle. No further pricing was justified by this probe.
