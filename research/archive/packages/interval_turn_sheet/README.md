# Ordered-CDF response identities and center verification

These tools support the research in
[`research/10-turn-density`](../../research/10-turn-density/). They do not
contain a matching equilibrium or a certificate of the unrestricted game
value.

## Exact independent checks

Run from the repository root:

```sh
python packages/interval_turn_sheet/verify_general_response.py
python packages/interval_turn_sheet/verify_uncrossing.py
python packages/interval_turn_sheet/verify_initial_wave.py
python packages/interval_turn_sheet/verify_terminal_integrals.py
python packages/interval_turn_sheet/verify_center_bellman.py
```

The first three audit the general negative-M2 CDF formula, the two-turn
uncrossing identity, and independent initial/incoming-wave derivatives.
They are separate from the numerical density searches in this directory.

The terminal verifier checks 328 exact cost-residual identities, including
the positive outgoing-front Volterra correction, and 60 independent
endpoint traces. It retains the first-contact dips from center and incoming
atoms. Those identities are valid for supplied laws; they are not claims
that a matching law solves the endpoint equations.

The center verifier performs **756 exact Fraction checks** against the
independent continuous running-CDF capture engine:

| Identity or comparison | Exact checks |
|---|---:|
| Initial prefixes ending at center | 180 |
| Complete prefixes reaching an endpoint first | 360 |
| Direct center endpoint sweeps | 27 |
| Center waits and early return triangles | 27 |
| Terminal triangles crossing the center peak | 81 |
| Lagging-side versus leading-side terminal choice | 81 |

Fixtures include initial positions different from incoming characteristics,
negative outgoing characteristics, center waiting, a start at an endpoint,
incoming characteristics above one, and terminal returns above one. The
formulas integrate inverse characteristics over a continuous rank law. The
reference engine instead integrates the running capture records along the
actual monster route; it does not use the asserted action formulas.

## All-monster criterion

[`CENTER_BELLMAN_CERTIFICATE.md`](../../research/10-turn-density/CENTER_BELLMAN_CERTIFICATE.md)
gives the theorem. For an ordinary ordered three-leg law, the center state
is the time `t` and one captured frontier `M`; the other frontier is the
known incoming CDF `I(t)`. Exact triangle, wait, and terminal inequalities
certify every center continuation without a guessed turn count. Explicit
initial-prefix inequalities attach the free monster start.

A concave potential that is piecewise affine in `M`, with slopes at most
`-t/2`, needs its Bellman inequalities checked only at its frontier knots.
The remaining continuous variables are the current time and next return
time. No candidate potential satisfying all the required initial
inequalities at a matching upper value has yet been established.

`center_bellman.py` implements the exact action and prefix formulas. It
accepts an ordinary `RankLaw` with no separate stationary endpoint atom and
with `a+u<=2`. It does allow `u>1`. Curved incoming sheets and multi-wave
laws are outside this implementation's scope.

## Continuous response discovery

`probe_center_bellman.py` searches the complete reduced monster family for
a piecewise-affine ordinary `RankLaw`, using continuous turn parameters:

```sh
python packages/interval_turn_sheet/probe_center_bellman.py \
  --iterations 80 --population 7 --output /tmp/center-response.json
```

Without `--law`, it uses the legal three-knot fixture built into the tool.
A supplied JSON file has this shape:

```json
{
  "q": [0, 0.4, 1],
  "a": [0.1, 0.45, 0.7],
  "u": [0.2, 0.7, 1.2],
  "c": [0.95, 0.3, -0.6]
}
```

The loader also accepts this object under `law`, or as the last `law` in a
`history` list. The rank knots specify the actual continuum law; the probe
does not form princess sample rows or a finite capture matrix.

The fixed breakpoints of its piecewise-constant incoming density supply
the exhaustive number of early return triangles. The default search
includes that count and all smaller counts. `--triangle-cap` is available
for exploratory runs; if it is too small, the output explicitly marks the
structural family incomplete. Every reported route is recomputed by the
independent capture-record engine and checked against the action objective.

Differential evolution and local polishing are heuristic. Even with the
complete structural parameterization, the reported optimizer minimum is
**not** a certified global minimum. Each returned route is an actual
response that can expose an unsatisfied lower inequality. These searches
do not replace the Bellman and initial-prefix certificates.

## Curved-law and global signed certificates

`general_center_bellman.py` retains two captured radial frontiers for a
curved ordered law. The opposite frontier at a center return is updated
from the center CDF, not from the entire outward rank. This distinction
matters for slowly outgoing paths. Its theorem and exact triangle, wait,
and terminal formulas appear in
[`GENERAL_CENTER_BELLMAN.md`](../../research/10-turn-density/GENERAL_CENTER_BELLMAN.md).

`signed_bellman.py` uses the full signed CDF and the state `(t,x,l,h)`:
the captured quantile interval is `[l,h]`. Rightward legs use the closed
CDF, leftward legs use the strict CDF, and time-two endpoint sweeps give an
exact terminal cost. A bounded potential satisfying the displayed action,
terminal, and free-start inequalities certifies every monster path. This
includes the initial motion; no extra initial-prefix theorem is needed.
The theorem is in
[`GLOBAL_CDF_BELLMAN.md`](../../research/10-turn-density/GLOBAL_CDF_BELLMAN.md).

```sh
python packages/interval_turn_sheet/verify_general_center.py
python packages/interval_turn_sheet/verify_signed_bellman.py
```

The first command performs 1,056 exact Fraction checks; the second performs
1,189. Independent segment-capture fixtures include whole incoming
coincidence atoms, center waits, endpoint starts, and positive mass absorbed
exactly at time two. Concavity checks also exercise the finite record-cell
vertex reduction. These implementations and checks do not supply a
matching princess law or an instantiated verification potential.

## A concrete continuation value from center memory

[`CENTER_MEMORY_SWEEP.md`](../../research/10-turn-density/CENTER_MEMORY_SWEEP.md)
constructs an attained value on a useful region of the state space. At a
center return, let `H(t)` be the largest radial center mass seen so far,
and let `Y_tail(t)` be the largest rank capturable at any future interior
point reachable from that center state. If `H(t)>=Y_tail(t)`, every later
return excursion is dominated by a direct endpoint tour starting toward
the less-captured sign. This remains true for slow outward paths and does
not assume that every uncaught path is already at an endpoint.

`center_memory.py` checks the sufficient boundary condition exactly for a
saved triangular field. It uses the whole future endpoint-interior
envelope, which is essential for endpoint departures and characteristic
atoms. `verify_center_memory.py` performs 3,987 exact checks using direct
Fraction intersections. Transport admissibility and the costs before the
barrier must still be checked separately.

## Independent whole-field attack discovery

`probe_ordered_capture.py` searches capture orders of a finite ordered
polygonal law, with explicit node and time limits. `probe_cdf_field.py`
extracts quantile contours from a continuous triangular CDF, uses that
finite search to propose a route, and then evaluates it against the entire
CDF. Continuous route polishing also uses the entire field. The finite
sample's minimum is never reported as a lower guarantee for the field.

```sh
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_sheet/probe_cdf_field.py FIELD.json --quantiles 32 --nodes 600000 --seconds 20 --polish-seconds 20 --output ATTACK.json
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_sheet/verify_cdf_probe.py
```

The field format has `nodes` in `(U,V)` coordinates, triangle vertex
indices, and affine nodal `values`. Endpoint boundary values denote the
fixed-characteristic interior trace. Exact endpoint contact uses its
separate closed/strict spatial trace; in particular, a characteristic atom
arriving at time two is removed at that time. The optional integer
isotonic repair is an explicitly reported modification of discovery data,
not an exact certificate for the original solver output.

The regression checker compares 300 whole-field costs with independent
exact continuous-rank integrals and direct atomic captures. It also checks
the analytic uniform-outward sweep value `9/8`, quantile contours, and two
complete finite capture-order examples. A returned attacking route can
expose a proposed lower law's failure. A search that finds no attack, even
one complete on its finite sample, does not prove the continuous law.
