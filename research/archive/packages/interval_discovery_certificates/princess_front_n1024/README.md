# Retained incoming-front field refined to n = 1024

This package records the exact computation behind the game-value lower bound

\[
V\ge \frac{9322984150699}{6553600000000}=1.4225744858854674 .
\]

It is the field of [princess_front_n512](../princess_front_n512/README.md) refined once more. The
bound is a statement about the value of the game. It is not a security certificate for the full-width
interpolant of `field.json`, and no explicit continuous Princess strategy is extracted here.

## What was verified

`field.json` has `n = 1024`, denominator `3200000000` and 4,195,328 stored radial nodes. It was written
by the unchanged [refine.py](../../interval_center_pricing/refine.py) from the n512 `field.json`
(SHA-256 `a4fe152d…28e10`). The refinement is the full-width common-threshold interpolation; with a
factor 2 the denominator doubles and every value is exact (`exact_fullwidth_refinement: true`).

The complete normalized-bank minimum is

\[
\frac{18652368301398}{13107200000000}=\frac{9326184150699}{6553600000000}=1.4230627671354674,
\]

and the game-value loss is `1/2048`. Three exact integer runs on the same binary input (SHA-256
`085285a8…dcd80`, the table that the repository's decoder rebuilds from `field.json`) return this
minimum:

| Engine | Time | Memory | Retained states | Record |
| --- | ---: | ---: | ---: | --- |
| `price_center.cpp`, policy 4 | 1,458 s | 6.3 GB | 6,711,010,516 | `center.replay.json` (written by `refine.py`) |
| `price_center.cpp`, policy 3 | 1,535 s | 8.6 GB | 7,366,755,383 | `center_policy3.replay.json` |
| `price_normalized.cpp` | 17,862 s | 16.2 GB | 36,178,048,329 | `original.replay.json` |

The run of `price_normalized.cpp` was made before `refine.py` wrote `field.json`, on a table built by an
independent implementation of the same refinement,
[refine_retained_field.py](../../interval_lightcone/refine_retained_field.py). The two tables are
identical byte for byte, which is why its result is recorded here. `manifest.json` is the file written
by `refine.py`; its flag `independent_original_replay: false` describes that run of `refine.py` alone.

**Not done:** the independent BigInt target replay
([verify_bigint.cjs](../../interval_center_pricing/verify_bigint.cjs)) that the n512 package has. It
re-verifies the n512 field in 1,029 s on the same machine; for this field it was started on 2026-11-15
and stopped after about 15 minutes. It has not been completed.

The proof dependencies are those of the n512 package: the
[normalized-bank response theorem](../../../research/12-global-closure/NORMALIZED_GRID_BANK_PRICING.md),
the transfer `V >= U_n - 1/(2n)`, and the center/incoming-front normal forms used by `price_center.cpp`
([proof](../../../research/12-global-closure/DISCRETE_CENTER_BALANCE_PRICING.md)). These are analytical
proofs with exact computational certificates, not a Lean formalization.

## Reproduce

```sh
python3 packages/interval_center_pricing/refine.py \
  --source packages/interval_discovery_certificates/princess_front_n512/field.json \
  --n 1024 --policy 4 --output /tmp/front_n1024          # 25 minutes, 6.3 GB; add --classic for the 5-hour engine
cmp /tmp/front_n1024/field.json packages/interval_discovery_certificates/princess_front_n1024/field.json
```

Context and the behaviour of the bank minimum under refinement:
[REFINED_N1024_LOWER.md](../../../research/14-light-cone-lattice/REFINED_N1024_LOWER.md).
