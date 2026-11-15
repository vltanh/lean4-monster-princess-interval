# Physical mixture discovery through exact Qout cuts

This is an alternative to a large cold LP over every CDF order variable.
The numerical master has one variable per admitted physical/calendar plan,
one normalization equality, and one inequality per observed binary Qout cut
or supplied feasible field.
An integer maximum-flow oracle supplies an unrestricted upper for every
proposed rational physical mixture and separates another maximizing cut.
The LP dual mixes the admitted cuts into a feasible nodal field for discovering
additional physical paths and running-record calendars.

The retained feasible CDF field enters directly as one response row. Its
information is not reduced to finitely sampled quantile thresholds; those
threshold cuts are additional exploration rows. All supplied fields are
checked against the full Qout order before admission.

The restricted-cut LP objective is a discovery estimate for this calendar
bank. **It is not a lower bound on the unrestricted game.** A Qout cut
maximizes a supplied clock plane; it need not describe an actual Princess
best response to the physical law. The upper certificate remains valid
because every actual Princess payoff lies below that clock plane, and the
integer closure calculation bounds its maximum over all legal Princesses.

## Exact acceptance and active-cut sampling

`closure_server.cjs` retains the charged-event geometry between queries.
It accepts integer probability numerators, independently reconstructs physical
paths and causal clocks, solves the sparse integer closure, and replays the
flow and matching cut before reporting an upper. Saved certificates contain
the complete physical law, rational probabilities, individually checked
Qout order inequalities, positive flow entries, and the cut. No LP status or
floating objective enters that verification.

One residual flow graph supplies additional equally maximizing cuts without
another maximum-flow solve. A minimum source side is residual-reachable from
the source. A maximum side excludes every vertex that can reach the sink.
Starting from the minimum side, the forward closure of any set of vertices
outside the latter sink basin gives another minimum cut. The server samples
such closed sets deterministically from the recorded seed and checks each
cut capacity against the exact maximum flow. Python then extends every cut
to a full binary Qout field and verifies that its exact weighted objective
equals the oracle value. This explores the active face of the clock-plane
optimization; it does not assume the corresponding physical Princess paths
attain that value.

The default level step chooses a mixture close to the retained certified
law while requiring improvement in the restricted cut model. This reduces
oscillation among extreme probability vectors. Its acceptance still depends
on fresh exact closure. The unregularized small LP remains the source of
the reported restricted-cut estimate and of the pricing field.

## Native discovery with unchanged certificate verification

`--native-flow` uses the optimizer adapter in `interval_integer_flow`.
Only the integer maximum-flow search changes. Capacities, conservation, and
flow/cut equality are rechecked with BigInt, then the unchanged existing
server replays physical paths, causal clocks, geometric Qout edges, and the
complete exact witness before accepting a certificate. Source hashes and the
compiled optimizer hash are saved. The pure BigInt optimizer remains the
default when the flag is omitted.

The native adapter reduced an actual 99,188-event refined-clock closure
from 137.13 seconds to about 15.4 seconds including its independent checks.
Those are local measurements from `interval_integer_flow`, not a prediction
of this campaign's runtime. Joint-search logs report each actual closure time.

## Reject physical proposals that already lose to an explicit loop

The current retained n256 law has upper
`291849329389899/204800000000000`. Its exact endpoint-loop response lower is
`729623323469031/512000000000000`. Consequently changing **only its clocks**
can improve its upper by at most `11433/1024000000000000`, about `1.12e-11`.
This campaign changes physical probabilities and discovers new routes.

There is a separate obstruction for the different 676-pair plain seed:
all three fixed-marginal jobs in
[run 43546004339](https://github.com/vltanh/lean4-monster-princess/actions/runs/43546004339)
stopped on exact all-calendar family floors above the retained global upper,
including n512 floor `145931157143161/102400000000000`. This obstructs those
nodal clock families at the specified fixed physical probabilities. It is
not an obstruction to their actual continuous law or to changing probabilities.
The seed and independent family-verification tools are in
`interval_fixed_marginal`.

`--loop-screen` performs a cheap exact check before each proposal's costly
closure query. Let `M` be its mean first-endpoint baseline, `q` its mass on
direct endpoint-start sweeps, and `delta` the gap between the endpoint and
its nearest interior initial position. For every `0 < epsilon < h < delta`,
the explicit radial Princess loop

\[
 r(0)=1-\epsilon,\qquad
 r(t)=1-\epsilon-t\quad\left(t\le\frac{h-\epsilon}{2}\right),\qquad
 r(t)=\min(1,1-h+t)\quad\left(t\ge\frac{h-\epsilon}{2}\right)
\]

has actual expected capture time `M + q*h/4`. Every interior-start Monster
misses this loop before its endpoint arrival and pays its first-endpoint
time. A direct endpoint-start sweep contributes `1+h/4`. These are actual
chronological contacts, not a value inferred from a finite response bank.

If the supremum `M + q*delta/4` exceeds the incumbent by more than `1e-8`,
the screen chooses an explicit rational `h` and `epsilon` whose physical
payoff still exceeds that threshold. It builds the binary nodal field using
**strict radial traces**, checks every Qout order inequality, and checks the
proposal's exact clock-plane value against the physical witness. Strict
traces matter: closing an interior atom while keeping the endpoint trace
open can violate the cone edge into actual endpoint arrival.

The resulting feasible field becomes another cut in the small LP. If this
is a new cut, the proposal is rejected without solving maximum flow; path
discovery still runs on its scheduled rounds. Unsupported endpoint-start
paths simply bypass this optional screen. The record contains the rejected
rational weights, model hash, explicit loop parameters, and exact witness.
**This rejects one proposed physical mixture. It never rejects a support
family with variable probabilities and never supplies a game lower bound.**

### Complete separation of the one-turn loop field family

The nearest-start gap can shrink when a tiny amount of new support is added,
making the preceding physical lower witness weak. The second stage of
`--loop-screen` therefore separates **every** nodal field of a legal radial
one-turn endpoint loop in quadratic time. It includes the long loops that
touch the center, as well as short endpoint-layer loops.

Let `0 < epsilon <= h` and `epsilon+h <= 2`. At time and radius indices
`(j,k)/(2n)`, set

\[
u=(j+k)/2,\qquad v=(k-j)/2.
\]

Before endpoint absorption the radial path is
`max(1-epsilon-t, 1-h+t)`. Its strict-trace binary field is therefore

\[
G(j,k)=1\{u\ge a,\ v\ge b\},\qquad
a=\lfloor n(1-\epsilon)\rfloor+1,\quad
b=\lfloor n(1-h)\rfloor+1.
\]

The exact admissible integer domain is
`1 <= a <= n`, `1-a <= b <= a`: it contains `n(n+1)` fields. Conversely each
rectangle is realized by the explicit shifted parameters

\[
\epsilon=\frac{2n-2a+1}{2n},\qquad
h=\frac{2n-2b+1}{2n}.
\]

These offsets are material. The starting radius and endpoint time are odd
in physical grid units; using unshifted integers would change strict traces
and contact ties. The `h<1` subfamily is `b>=1` and has `n(n+1)/2` fields.

For rational proposed weights, aggregate the signed clock pressure at
`(u,v)` and take two-dimensional suffix sums. Every rectangle cost is then
one exact integer lookup plus the constant clock mass. A checked absolute
mass bound prevents signed 64-bit overflow. The selected maximum is checked
again against its direct full-field weighted clock sum before admission.

If a new rectangle cut exceeds the incumbent, its proposed **calendar
mixture** is rejected without max-flow. The driver separately computes the
actual first-contact payoff of the shifted physical Princess loop. Contacts
before endpoint arrival occur at half-grid times, and later contacts use
the actual first endpoint visit. Only when that independently scored physical
payoff also exceeds the incumbent is the rejection labeled
`physical_mixture`; otherwise it is labeled `calendar_mixture`. The latter
does not exclude improving the same physical law with different clocks.

This is a complete finite classification of one specified nodal field
family. It is not an equilibrium-sufficient classification, and it does not
replace the all-Princess oracle used to certify an upper.

Every proposal also records exact probability total variation from the
seed, probability mass on genuinely new physical routes, and whether only
clocks changed. Physical routes are identified up to fair reflection and
irrelevant suffixes after both endpoints have already been visited. Merely
adding another calendar or dead suffix therefore does not count as new
physical geometry.

## Search and replay

```sh
python packages/interval_mixture_cut/test_search.py
python -u packages/interval_mixture_cut/search.py \
  --native-flow --loop-screen --n 256 \
  --initial-law packages/interval_discovery_certificates/monster_boundary_n256.physical.json.gz \
  --iterations 80 --seconds 1200 --lp-seconds 60 \
  --boundary-points 48 --pricing-paths 256 --price-every 3 \
  --mutation-count 256 --alternative-cuts 16 --level-fraction 0.8 \
  --seed 173205 --output results/joint-native-256
```

The physical reservoir comes from `interval_monster_boundary`: both boundary
fronts and initial deficits vary independently, and bulk paths can mutate.
Probabilities and causal calendars are optimized jointly. `--full-every 4`
also invokes complete native Monster pricing every fourth pricing round;
without it, reservoir pricing makes no claim of completeness or security.
Every complete native output is retained in the compact pre-two field format
described below, with the separate continuum transfer. Cached route minima
are never passed to this retention gate.

This is a bounded joint-support experiment, not a continuation of clock-only
optimization. Inspect certified improvement, exact loop rejections, new-path
mass, and the remaining separation gap before allocating another run. A
second `--n 512` experiment can resolve the endpoint layer more finely; its
seed physical paths are lifted exactly, while additional routes and weights
remain free. No monotone improvement or equilibrium is assumed.

Resume with `--resume results/joint-native-256/checkpoint.json`. The checkpoint
binds a compressed binary-cut archive, calendar bank, random state, and
history. The previous best exact law is replayed on restart. Seed and best
certificates survive solver budget stops. Artifacts include source and input
hashes, run metadata, solver logs, exact certificates and replays, the
endpoint-loop diagnostic, and a hash manifest.

An improved sparse certificate can be independently rebuilt on the complete
grid without changing its rational probabilities:

```sh
node --stack-size=16384 packages/interval_mixture_cut/dense_replay.cjs \
  results/mixture-cut-256/best.sparse.json results/mixture-cut-256/dense-check
node packages/interval_clock_grid/qout_primal_certificate.cjs \
  results/mixture-cut-256/dense-check.physical.json
```

The small-grid regression compares native and BigInt cut/mixture optimization with the
complete order LP, checks every returned binary field and its dual mixture,
rejects invalid probability vectors, reproduces the exact upper through the
independent full-grid verifier, and exercises checkpoint resumption. It also
checks the explicit loop through independent chronological affine
intersections, its feasible strict-trace field, exact probability changes
versus genuinely new routes, and bypass of unsupported endpoint loops.
All 40 rectangles on grids n=1,2,3,4 are compared with direct full-field
weighted sums, and 618 independent chronological contacts check the shifted
physical representatives, including center and endpoint contacts.
These checks support the computation, not an equilibrium claim.

## Retaining every completely priced Princess field

An upper search can discover a useful Princess field even when it does not
improve its physical Monster mixture. Each `--full-every` pricing call now
retains a separate capsule under
`complete_princess/candidates/nN-roundRRRRRR-HASH/`. Each capsule contains:

* `field.json`: exact uint32 pre-two Qout values, compressed with zlib; its
  deterministic outward extension reconstructs the complete priced input.
* `native_report.json.gz`: the entire returned native result, including its
  witnesses and search counters, serialized as canonical JSON and compressed
  with a zero gzip timestamp. These are reserialized result bytes, not the
  original stdout stream.
* `manifest.json`: SHA256 bindings for both files, the uncompressed report,
  the complete raw binary pricing input, the native executable and relevant
  source files, plus an immutable copy of the discovery metadata.

Before retention, the compact field is decoded by the existing independent
Python decoder and hashed in the native input format. That hash must match
the exact binary input consumed by the completed pricing call. The input
header, full row-major table, report scale, and field scale must agree.
This is a byte and arithmetic check; it does not repeat the exhaustive search.

`best_complete_bank.json` points to the candidate with the largest **exact**
bank value `c`, retaining an earlier winner when a later field is weaker.
`last_complete_bank.json` identifies the latest retained field, and
`complete_princess/index.json` lists all candidates. The unrestricted value
lower saved with each field is `c - 1/(2n)`. The field itself is not claimed
to have this security against every continuous Monster; obtaining an
explicit Princess law requires the separately proved extraction step.
Floating cut-LP estimates and cached response minima remain unqualified
discovery quantities.

Candidate names bind the exact input, result, source hashes, run provenance,
and pricing round. Same-directory and different-directory resume preserve
all earlier capsules byte for byte, including when a pricing-round number
is reused. An inconsistent best pointer or altered candidate bytes stops
resume rather than silently discarding evidence. Full-horizon radial-node
JSON and duplicate master checkpoints are no longer emitted on every
pricing call; the ordinary joint checkpoint remains the resumable search
state.

Run the small independent replay and retention regression with:

```sh
python packages/interval_mixture_cut/test_princess_retention.py
```

It performs a fresh native complete search and an independent BigInt target
replay, checks exact input reconstruction, preserves a stronger earlier
field through both resume modes, and rejects incomplete cached results,
changed raw inputs, altered field bytes, and a weakened best pointer. The
joint driver regression also exercises complete pricing and resumed compact
retention end to end. A promising retained field can be passed directly to
the established native and BigInt field verifiers; those expensive replays
are reserved for candidates that warrant certification.

## Completed joint CI campaign

[Run 43548450417](https://github.com/vltanh/lean4-monster-princess/actions/runs/43548450417)
completed all three families: 111 proposals, 22 exact physical upper checks,
and 19 complete native Princess pricing calls. It tried genuinely new
physical paths and probabilities but improved neither current unrestricted
bound. The retained n256 fields changed their known continuous attack
ceilings by only about 2e-5; no larger refinement was warranted. The n512
family used cached pricing only, which certifies no Princess lower.

[ci_joint_campaign.json](ci_joint_campaign.json) binds the downloaded artifact
ZIPs, internal manifests, exact objectives and continuous diagnostics. It also
records the historical overwrite of an earlier best native-priced field.
The complete-field archive above fixes that issue for subsequent runs.

The explicit `campaign.json` switch is currently false. Set `run_on_push` to
true in an intentional research commit to launch via the verified push path,
or use the workflow's manual search input. Routine source and retention
updates still run exact regressions without repeating these completed
experiments.
