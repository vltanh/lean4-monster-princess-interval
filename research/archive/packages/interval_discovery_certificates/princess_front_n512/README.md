# Retained incoming-front Princess certificate at n = 512

This package preserves the exact CI artifact bytes proving the unrestricted
game-value lower bound

\[
V\ge \frac{36409808231}{25600000000}=1.4222581340234375.
\]

The supplied **explicit continuous Princess strategy**, stored separately in
`princess.json`, guarantees

\[
\frac{582556541071}{409600000000}=1.42225718034912109375
\]

against every legal Monster path. These are distinct statements. The game-value
transfer does not claim that the full-width interpolant of `field.json`
attains the first number.

## What was verified

The compact field has `n=512`, denominator `1600000000`, and 1,049,088 stored
radial nodes. Both native response engines found the complete normalized-bank
minimum

\[
\frac{4663655453568}{3276800000000}
=\frac{36434808231}{25600000000}.
\]

The independent BigInt implementation checked the same target lower in
[run 43546803161, job 132300097087](https://github.com/vltanh/lean4-monster-princess/actions/runs/43546803161/job/132300097087).
It completed successfully after 780.246 seconds, retaining 507,231,825 states
and generating 893,765,461 transitions. The exact game-value loss is `1/1024`.
The common-threshold construction with `epsilon=1/1024` gives the explicit
strategy loss `1025/1048576`.

The proof dependencies are the
[normalized-bank response theorem](../../../research/12-global-closure/NORMALIZED_GRID_BANK_PRICING.md),
the [constructive Princess transfer](../../../research/12-global-closure/CONSTRUCTIVE_PRINCESS_GRID_DUAL.md),
and the center/incoming-front normal forms documented with the
[independent compact verifier](../../interval_center_pricing/README.md).
These are analytical proofs with exact computational certificates; this is
not a completed Lean formalization or an unrestricted equilibrium.

## Provenance and retained files

The source field is an exact full-width refinement of the incoming-front
projection of the retained n256 field. It was priced in
[discovery run 43545082756](https://github.com/vltanh/lean4-monster-princess/actions/runs/43545082756),
commit `43ecfa2140c22ce31b0d2469a8ae2862320bc7fe`,
[artifact 14093139934](https://github.com/vltanh/lean4-monster-princess/actions/runs/43545082756/artifacts/14093139934).
Its downloaded ZIP SHA-256 was checked as
`d0a518a73fc8d3bc23aee8519ff9395a3faa2db8d6dbd346f52bb44e2b7205d9`.

The completed independent replay and extraction are from commit
`4503f3ea3eb360978b0d2632461ca748cd714899`,
[artifact 14095016913](https://github.com/vltanh/lean4-monster-princess/actions/runs/43546803161/artifacts/14095016913).
Its downloaded ZIP SHA-256 was checked as
`ff3c36fe107a6c739b63ab77bacd41ae1816018c76f2182cca77c972aad240cc`.
The source members in both downloads match byte for byte.

| File | Meaning |
| --- | --- |
| `field.json` | Exact compact n512 nodal field, SHA-256 `a4fe152dbf70f5896c256d3a329f6ac2ab31028421795ae74a3163b399c28e10` |
| `princess.json` | Exact saved CI continuous strategy, SHA-256 `b7ac0c124dfcf6d3d00fbfaa6fbf2872e04878572d0f5221e7f7de0b05a257d7` |
| `original.replay.json` | Complete original native response minimum |
| `center.replay.json` | Complete native minimum with proved center/front reductions |
| `independent.replay.json` | Independent BigInt complete-bank target check |
| `extraction.replay.json` | Exact strategy construction and transfer arithmetic |
| `manifest.json` | Artifact, source, report, and file hashes |
| `provenance.json` | Successful-job metadata, exact archive-member bindings, and reviewed source/proof commitments |
| `provenance/verify_bigint_4503f3e.cjs` | Byte-exact historical BigInt verifier used by the completed independent CI report |

The old `independent_bigint_replay: false` in the byte-exact native report
describes its earlier stage. The separate successful independent report now
supplies that verification. Its historical verifier hash remains
`3ca39089073633d89e12a7ebec1b46257ee037d3ff4ed71d58614f5f6aa73092`.
The later `9ff33b8b0cfe3afcd04829aade627e7465264f641246cc2a795c96609b4d2b97`
version only snapshots its own source hash before a long verification; it is
not relabeled as the source of the completed CI report.

## Cheap retention check

From the repository root:

```bash
node packages/interval_discovery_certificates/princess_front_n512/check.cjs
```

This checks the six saved files against their hashes and byte counts, binds
the completed reports to their actual source files and successful CI jobs,
checks every exact fraction, revalidates all 2,095,104 pre-time-two transport
inequalities and 1,024 sticky-endpoint inequalities, and directly checks all
262,144 incoming-front nodal identities. It calls `makeStrategy`,
`assertSameStrategy`, and `createEvaluator` to compare the deterministic
extraction with the saved CI Princess. Seven current source dependencies,
nine reviewed proof sources, and the separately preserved historical BigInt
source are hash-bound. A later source or proof edit requires an explicit
reviewed update to these commitments.

All eleven members of the independent artifact are byte-recoverable. Four
small original metadata files are embedded verbatim in `provenance.json`;
the prepared field is reconstructed with its original compact serialization
by dropping only the recorded pricing metadata. This avoids duplicating the
nodal payload. The provenance checker verifies every reconstructed member
against its original SHA-256 and byte count, as well as the earlier discovery
manifest's file commitments. The historical `false` flags remain unchanged.

The cheap check **does not rerun all-bank pricing** and does not redownload
or recompute the two archive ZIP digests. Those download digests were checked
when retaining the artifacts, and the metadata records that provenance.
The completed reports remain the computational evidence for the exhaustive
search. `check.replay.json` records the cheap retention check, while
`test_check.cjs` rejects altered source/receipt bindings and omitted transfer
allowances without importing a complete-bank pricer:

```bash
node packages/interval_discovery_certificates/princess_front_n512/test_check.cjs
```

A new independent target replay, when deliberately required, can be run with:

```bash
node --max-old-space-size=6000 packages/interval_center_pricing/verify_bigint.cjs packages/interval_discovery_certificates/princess_front_n512/field.json --front --progress 128
```

That command performs the substantial response search. No additional full
search was run merely to assemble or check this retention package.

For a deliberately requested combined pricing and saved-strategy replay:

```bash
node --max-old-space-size=6000 packages/interval_center_pricing/verify_strategy.cjs packages/interval_discovery_certificates/princess_front_n512/field.json packages/interval_discovery_certificates/princess_front_n512/princess.json --progress 128
```

The current independent upper is a separate certificate. Combining its exact
value `291849329389899/204800000000000` with this packet's game lower gives
the remaining gap `570863541899/204800000000000`; this packet does not replay
that upper or claim the gap is closed.
