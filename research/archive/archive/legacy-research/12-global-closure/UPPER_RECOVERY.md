# Upper-strategy recovery and exact resume point

Date: 2026-11-11.

This note preserves two source changes after the execution environment became unavailable. The parent checkpoint is `cc81521e146f2999ead1b56f47a6e81afd6d8a37` (tree `0c6959daf82698a0610cfa4eb9641e4d5b9405cf`). The original recovery commit was unreferenced; its reviewed contents are now preserved in the PR with the recovered separator kept separate from the tested default.

## Verification status

The two implementations were executed in the unavailable working copy before the outage, with the observations below. Their present text was reconstructed from recorded source and edits. No working-copy hash was recorded for either original file, so byte identity with the executed files is unverified. The recovered JavaScript parses successfully; neither recovered program has been rerun against repository data. The recovered Python has not been executed or syntax-checked.

`efficient_recovery_manifest.json` hashes the recovered text, not the unavailable working copy. The existing `efficient_separator.cjs` remains the tested default, and `efficient_manifest.json` still matches that pinned version. The recovered optimization is saved separately as `efficient_separator_recovered.cjs`; validate it directly before selecting it in the master.

## Preserved source changes

### Lightweight full-bank separator

`efficient_separator_recovered.cjs` retains the complete bank's event geometry and physical payoff rows without compiling reward auxiliaries for all bank columns. Each global separation still compiles the complete maximum-closure problem for every positive-weight Monster pair in the proposed law. Thus sparse support changes construction cost without restricting the Princess response.

The common-quantile completion evaluates every threshold interval by the existing physical row evaluator. It collects distinct marginal probabilities with a set and uses binary search for each query label. It returns the requested profiles but accumulates costs over the entire completed mixture. This preserves the whole-bank coarea construction; it does not select only the heaviest components.

Recorded execution on the frozen 1,086-pair bank:

- Separator startup: about 0.149 seconds, previously about 10--15 seconds.
- Complete coarea mixture: 807 components in about 0.423 seconds.
- Component weights summed to one.
- Minimum completed-mixture bank payoff: `1.4259240849269774`, against primary-master value `1.4259240849269847`.
- Unrestricted Princess response to the retained Monster law: `1.4261353247507313`, unchanged.

These are numerical development observations, not additional exact certificates. Repeat the comparison before relying on the recovered optimization in a new run.

### Semantic dual reconstruction

`efficient_semantic_dual.py` builds an explicit rational physical Monster law from named M1/M2/M3/I controls and saved attack-route provenance. Native light-coordinate parameters define shared contact equalities directly. External routes are matched back to exact rational source records when available. The output records the reconstruction mode; floating-only inferences are explicit.

The code also recognizes exact-decimal unit routes and monotone wall sweeps, completes routes to both endpoints, removes redundant vertices, and replaces center waits by the already proved closed unit excursions. Generic floating-only light-run inference is available but was not used in the final recorded H3 replay.

Recorded reconstruction of `continuum_complete_h3_duals.json`: 718 controls, comprising 681 named light-parameter controls, 31 exact source routes, two recognized M1 controls, and four exact-decimal unit routes. Eight shared-phase or boundary interpretations were recorded; zero controls required generic light-run inference. Weights were normalized to one.

The resulting actual law had 249 query coordinates, 322 base levels and 71,010 threshold nodes. Its global numerical Princess response was `1.4350536067275825`, with dual flow value `1.4350536067413018`, in about 9.095 seconds. This rejects that constructed law as a matching upper strategy. It does not prove a statement about an unspecified idealization of the floating CDF dual.

Recreate and globally evaluate the law from the repository root:

```sh
python packages/interval_global_closure/efficient_semantic_dual.py packages/interval_global_closure/continuum_complete_h3_duals.json packages/interval_global_closure/efficient_semantic_h3
node packages/interval_global_closure/efficient_test_continuum.cjs packages/interval_global_closure/efficient_semantic_h3
```

The source dual can refer to saved attack banks and original source JSON. Restore those referenced files before reconstruction; a missing source must not be replaced by independent physical-vertex rounding.

## Durable mathematical checkpoint

The frozen `efficient_checkpoint.json` and `efficient_checkpoint_bank.json` remain unchanged. They supply the parent checkpoint's exact 280-pair upper certificate after the shared order-preserving light-coordinate map and exact replay:

```text
V <= 957063215727541539 / 671088640000000000
  = 1.426135325025828985869...
```

The map preserves the required order and contact equalities by commuting with reflection and integer translation. Independent physical turn-position rounding is unsuitable here: an earlier actual rounded law had response about 1.434503 despite perturbations of order 1e-7. Every altered law requires its own unrestricted response check.

All finite-bank lower values in the optimizer are lower bounds only for the corresponding restricted Monster game. They are not unrestricted Princess guarantees. Canonical physical representatives of query-profile mixtures were previously defeated by valid Monster routes and must not be relabeled as lower strategies.

## Interrupted experiment

A new union combined the previous extended bank, all 1,473 uniformly sampled density-seed pairs, and the semantically reconstructed H3 controls. Physical deduplication left 3,058 reflected pairs. It had 1,101 query coordinates and 4,281 labels, with about 1,365,108 compressed threshold variables in its full geometry.

Lightweight geometry setup completed in about 0.39 seconds, and 1,189 seed profiles took about 17.8 seconds. After two coarea steps the sampled-row master value was only `1.4116556323794451`; a new proposal's global response was `1.5271652814987262`, so the earlier incumbent was retained. The recorded incumbent `1.4261262705813273` belonged to an unpublished floating checkpoint. It was not exact-certified, and no completed new union solve survived.

Do not report the interrupted union as a converged minimax result, an improved exact bound, or a matching strategy. Its full bank can be rebuilt as a new explicit union from the durable checkpoint, `efficient_density128.bank.json`, the recovered semantic reconstructor, and chosen exact attack sources. Byte-identical recovery of the lost 3,058-pair bank is not claimed.

## Resume priorities

1. Rerun the recovered separator on the frozen 1,086-pair checkpoint and repeat the complete coarea and global-response comparisons above. Preserve the exact query geometry stored with every profile.
2. Reconstruct the semantic H3 law and repeat its unrestricted numerical response. Keep all inference/provenance counts in the resulting diagnostic.
3. Build one explicit union with the published uniform-density bank and exact new attack routes. Keep the published incumbent in the bank and retain its exact certificate as the current bound.
4. Improve initial Princess rows using actual legal finite Princess laws from the whole-CDF search, then apply common-quantile completion and primary-master reoptimization. Mapping those physical paths to query profiles still needs implementation and independent physical payoff comparison.
5. Run one substantial optimization at a time. The lost session also had a large finite-law Monster search and a whole-CDF LP active; memory pressure is a possible cause of the outage, not a confirmed diagnosis.
6. Stop only when the proposed law has actually been separated, retain the best normalized law separately from the latest master proposal, and save compact self-contained checkpoints. Avoid persisting regenerable large response pools.

The unrestricted optimal strategies and matching game value remain open.
