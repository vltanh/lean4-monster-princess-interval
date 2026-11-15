# Princess field search with bounded updates

This discovery package maximizes security over legal nodal CDF profiles. It
starts with the retained `lower_n256_field.json` and a bank of 1,292 legal
physical Monster paths. The bank includes new responses found by a complete
oracle during the initial bounded-update pilot. It has no probability weights
and supplies no lower certificate.

The LP uses an initial interior-point solve with crossover, then retains that
basis for sparse new calendar rows. A box around the best completely priced
field replaces the large L1 auxiliary model. An unsuccessful complete pricing
step shrinks the box and preserves the incumbent. Closing a box's restricted
gap expands it. These are discovery choices, not approximation theorems.

`--contract-tight-cones` additionally keeps every connected component of exact
seed cone equalities equal. This is an explicitly restricted transport family.
For the retained seed, profile128 has 65,664 nodal variables but only 6,139
components. The exact seed is feasible in that family. The code repairs
component values in a proved topological order, expands them to the original
physical table, and sends that table to the unchanged complete integer oracle.
No equilibrium sufficiency of these fixed equalities is claimed.

```bash
python packages/interval_lower_bundle/test_search.py
python packages/interval_lower_bundle/search.py \
  --n 256 --profile-grid 128 --contract-tight-cones \
  --component-prox --radius .001 --keep 32 --seconds 2400 --iterations 300 \
  --lp-seconds 90 --output /tmp/lower-bundle
```

Omit `--contract-tight-cones` to search the full finer nodal profile. Increase
`--lp-seconds` for that larger model. Add `--resume` with the same output
directory and profile family to restore every discovered causal calendar and
the exact incumbent. The certified integer table is loaded directly; restart
does not silently round it through floating point. Additional JSON or gzipped
physical banks/checkpoints can be supplied using repeatable `--response-bank`.

`--component-prox` minimizes L1 displacement from the certified incumbent at
a target security level halfway to the restricted box optimum. The target
fraction is adjustable with `--level-fraction`. This stabilizes optimization
of security; it does not minimize temporal variation. Its persistent model
uses the same trust bounds, and a complete integer response is still required
before acceptance. The saved profile is the actual repaired proximal field,
not the different unrestricted master maximizer.

`best.dual.json` is updated only by complete native pricing.
`state.json.gz` retains the discovery state, `priced_trials/` retains every
completely priced trial including rejected ones, and `manifest.json` records
hashes, the exact finite-bank fraction, and the unchanged transfer penalty
`1/(2n)`. Causal calendars from cached paths are valid separating inequalities;
clearing them does not certify the field. No restricted-master number is a
global upper, and no transferred bound is assigned as the security of the
same frozen common-threshold law.

The `--seconds` deadline is checked between completed solver/oracle calls.
An external job deadline should allow one additional oracle call and upload
the saved state even after cancellation. High-resolution searches need an
independent BigInt replay before promotion to the authoritative bracket.

The initial uncontracted n128/profile64 pilot did **not** improve the seed.
Its first candidate cleared 1,004 cached physical routes at about 1.4241373,
then complete pricing found 1.3772895. The rejected field therefore supplied
new response geometry rather than a bound. Warm LP updates took roughly
0.24–2.4 seconds after a 30.7-second initial solve. The finer component pilot
is a new search, not a claim that more computation alone reaches a width of
`1e-4`: the n256 transfer allowance alone is `0.001953125`, so a much sharper
continuous certificate or substantially finer exact bank is still required.
