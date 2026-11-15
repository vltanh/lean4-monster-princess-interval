> This folder holds only the files that the bounds in [`research/`](../../README.md) need. The description below is the original one; files it mentions that are not here are in [the archive](../../archive/packages/interval_discovery_certificates).

# Retained discovery certificates

The current independently certified bracket is

\[
\frac{36409808231}{25600000000}\le V\le
\frac{291849329389899}{204800000000000}.
\]

Its width is **0.0027874196381787109375**; the requested width below 1e-4
remains open. The [front512 Princess package](princess_front_n512/README.md)
preserves the complete native and independent BigInt results, both original
artifact digests, and the explicit continuous Princess law guaranteeing
**582556541071/409600000000**. Its cheap `check.cjs` binds saved evidence and
regenerates the strategy; it does not repeat all-bank pricing.


The current retained physical law gives the unrestricted upper

\[
V\le\frac{291849329389899}{204800000000000}
=1.4250455536616162109375.
\]

`monster_boundary_n256.physical.json.gz` contains **770 causal calendar
plans on 752 reflected physical path pairs**. It was discovered by the
`upper-boundary-256` experiment in
[run 43541622377](https://github.com/vltanh/lean4-monster-princess/actions/runs/43541622377),
commit `317d1d8d0164c0f1ff9996398c113135f7e8d33e`, seed `577215`.
The original strategy, solver logs and restart checkpoint are retained in
[artifact 14092179160](https://github.com/vltanh/lean4-monster-princess/actions/runs/43541622377/artifacts/14092179160).
The artifact ZIP SHA-256 is
`d356d204e73ab82e20aa3a47955afc830f9fe941b35fc785883fa6159838a1a8`.

The archive preserves the original JSON bytes inside deterministic gzip.
Its SHA-256 is
`80580dae8551c2838172d7f419861a3a9774793a8d039bdad087e21d24526f39`.
The accompanying manifest binds the original artifact, exact probabilities,
source hashes, replay and structural diagnostic.

## Exact all-Princess replay

From the repository root:

```bash
python3 packages/interval_discovery_certificates/verify_manifest.py packages/interval_discovery_certificates/monster_boundary_n256_manifest.json
```

The independent Python implementation reconstructs the physical paths,
**2,301,592 causal-clock prefixes**, and the complete Qout closure graph.
It then checks exact capacities, conservation and the matching source-side
cut. The existing Node verifier is replayed independently as well:

```bash
node packages/interval_clock_grid/qout_primal_certificate.cjs packages/interval_discovery_certificates/monster_boundary_n256.physical.json.gz
```

The closure has **262,402 nodes and 558,630 arcs**, with **83,592** positive
flow entries. Integral flow and cut both equal **265,930,716,799,554**.
Both implementations passed in
[verification run 43544245486](https://github.com/vltanh/lean4-monster-princess/actions/runs/43544245486).
No floating optimization result enters this exact acceptance gate.

The all-Princess scope follows from
[normalized-bank pricing](../../archive/research/12-global-closure/NORMALIZED_GRID_BANK_PRICING.md)
and the [physical Qout certificate theorem](../../archive/packages/interval_clock_grid/QOUT_PRIMAL_CERTIFICATES.md).
These are analytical proofs with exact computational certificates; a complete
Lean formalization is not claimed.

## What this discovery establishes

The search completed one optimization iteration before its next LP reached
the declared 600-second solve limit. The retained upper improves the earlier
768-pair law by exactly `1857712283/204800000000000`, approximately
`0.000009070860756835938`. The certificate remains valid independently of
convergence or that later budget stop.

This law has endpoint-sweep mass `629535049023/1000000000000` and initial gap
`1/128`. Its exact endpoint-loop response supremum is at least
`729623323469031/512000000000000`. The certified upper exceeds that
fixed-law witness by only `11433/1024000000000000`, approximately
`1.12e-11`. Improving causal clocks while leaving these physical probabilities
unchanged therefore has almost no remaining room. Stronger uppers require
changing the physical law. This is a statement about this supplied Monster
mixture, not a lower bound on the unrestricted game.

The [fixed-marginal experiments](../../archive/packages/interval_fixed_marginal/README.md) examine
a different retained law. Their exact all-calendar obstructions concern a
specified grid's clock-certificate family; they do not exclude every
continuous certificate for that physical law. The distinction is preserved
in their independent reports.

## Earlier retained discovery

`monster_mutations_n128.physical.json.gz` remains a valid weaker certificate:
809 calendars on 768 reflected pairs, with upper
`145925593551091/102400000000000`. Its independent Python and Node replays
check flow and cut `93007371780317` on 65,666 nodes and 151,953 arcs.

```bash
python3 packages/interval_discovery_certificates/verify_manifest.py packages/interval_discovery_certificates/monster_mutations_n128_manifest.json
```

It came from
[run 43532597339](https://github.com/vltanh/lean4-monster-princess/actions/runs/43532597339),
seed `161803`,
[artifact 14088158597](https://github.com/vltanh/lean4-monster-princess/actions/runs/43532597339/artifacts/14088158597).
The manifest preserves its full provenance and original bytes. Its 111 new
physical paths and supported late center returns remain useful diagnostics;
they do not justify a universal time-one or finite-support restriction.
The original 703-pair law also remains a seed and regression.

See the [current bound note](../../archive/research/12-global-closure/NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md)
for the strongest independently replayed Princess lower and its distinct
explicit-strategy guarantee. No retained numerical mixture is asserted to be
an unrestricted saddle.
