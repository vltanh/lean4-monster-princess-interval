# Exact switch-time geometry audit

This package audits the earlier retained 752-pair law. Its exact ablations and pruning bounds remain valid historical results. The later [continuum one-turn certificate](../../research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) gives the stronger upper 142472349375511/100000000000003 and closes the frozen separation comparison negatively. Read [the switch-geometry note](../../research/13-equilibrium-geometry/SWITCH_TIME_DISTRIBUTIONS.md) for the scope of these earlier calculations.

```sh
python3 packages/interval_switch_geometry/audit_switch_geometry.py --output /tmp/switch-geometry.json
```

The standard-library verifier reads the retained 752-pair Monster certificate, binds its original uncompressed SHA256, merges physical duplicates, and proves the exact family counts. It checks a single legal waiting-then-running Princess against the original law and three precisely specified renormalized ablations, using two distinct chronological first-contact implementations. All 1,504 oriented comparisons agree. A separate set of 102 rational physical fixtures checks the discontinuous switch-time formula, including the equality boundary.

The three principal families carry 98.7707900672% of the mass. Deleting the remainder and renormalizing exposes an actual response of 1.4325924122184144, above the original certified upper. This is an exclusion of the particular fixed-proportion ablation, **not** all possible reweightings of those continuum families.

The script also inherits a weaker global upper of 1459246646949495/1023896293471232 for the 719-pair sublaw with at most two interior turns. This uses nonnegative-payoff deletion and the original already verified upper; the script does not rerun the max-flow certificate. There is no new best unrestricted bound, equilibrium claim, or Lean proof.

## Exact restricted-game upper, not an exact restricted value

See [the one-interior-turn theorem](../../research/13-equilibrium-geometry/ONE_TURN_SUBGAME_BRACKET.md). Run `python3 packages/interval_switch_geometry/verify_one_turn_subgame.py`. It preserves all original SHA256 and independent full-upper dependencies and proves, via the reflected-start lemma and exact rational pruning, the all-Princess upper **1.432964907524812...** for at most one interior reversal and **1.425178547805600...** for at most two. The first-endpoint reversal is not counted as an interior turn; neither restricted game is solved exactly.

