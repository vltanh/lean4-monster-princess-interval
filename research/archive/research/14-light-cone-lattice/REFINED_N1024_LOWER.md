# The retained field refined to n = 1024: V ≥ 1.4225745

**2026-11-15.** The retained \(n=512\) Princess field, refined once more by the repository's own
rule and priced by the repository's exact engine, gives

\[
 V\;\ge\;\frac{9322984150699}{6553600000000}=1.4225744858854674
 \;>\;\frac{36409808231}{25600000000}=1.4222581340234375 .                         \tag{1}
\]

The gain is \(3.16\cdot10^{-4}\). With the upper bound of
[ATOMIC_TWO_TURN_UPPER.md](ATOMIC_TWO_TURN_UPPER.md) the bracket is

\[
 1.4225744858\ldots\;\le\;V\;\le\;1.4240199074\ldots,\qquad\text{width }0.0014454215\ldots
\]

Status: an exact integer computation with unchanged engines and existing theorems. The two native engines
of the repository, `price_normalized.cpp` and `price_center.cpp` (policies 3 and 4), return the same
minimum. The \(n=512\) certificate also had an independent BigInt replay; for this one that replay was
started and stopped after about 15 minutes, and has not been completed. The files are in
[princess_front_n1024](../../packages/interval_discovery_certificates/princess_front_n1024/README.md),
written by the repository's own `refine.py`.

## 1. What was computed

The source is `field.json` of
[princess_front_n512](../../packages/interval_discovery_certificates/princess_front_n512/README.md)
(\(n=512\), denominator \(D=1.6\cdot10^9\), SHA-256 `a4fe152d…28e10`).

1. **Refinement.** The field is interpolated to \(n=1024\) by the common-threshold rule of
   `solve_normalized.Master.interpolate_seed`. With a factor 2 every fine node is a coarse node or the
   midpoint of two coarse nodes, so the interpolant is exact over the denominator \(2D=3.2\cdot10^9\) and no
   flooring is needed. [refine_retained_field.py](../../packages/interval_lightcone/refine_retained_field.py)
   does this in integers; its self-test compares it with a literal port of the rule in exact fractions.
   The repository's own tool, `packages/interval_center_pricing/refine.py`, produces the same table byte
   for byte.
2. **Closure and extension.** The order closure of `Master.repair` changes no node. Beyond \(t=2\) the table
   follows the outward rule. The table has SHA-256 `9bda9142…35e08`.
3. **Pricing.** `price_normalized.cpp` (SHA-256 `9fe59dd9…f9bd`, unchanged) accepts the table and returns the
   complete normalized-bank minimum

\[
 K=18652368301398\ \text{ in units of }\frac1{4nD}=\frac1{13107200000000},\qquad
 \frac{K}{4nD}=\frac{9326184150699}{6553600000000}=1.4230627671\ldots
\]

   It retained 36,178,048,329 states and generated 71,614,961,981 transitions, in 17,862 s and 16.2 GB.
4. **Second engine.** `price_center.cpp` of
   [interval_center_pricing](../../packages/interval_center_pricing/README.md), on the same binary table,
   returns the same \(K\) with policy 4 (1,515 s, 6.3 GB, \(6.7\cdot10^9\) states) and with policy 3
   (1,535 s, 8.6 GB). On the retained \(n=512\) field both policies return the certified minimum in about
   145 s.

The record is
[refined_n1024_lower_replay.json](../../packages/interval_lightcone/refined_n1024_lower_replay.json).
The binary was byte-identical to a fresh `g++ -O3 -std=c++17` build of the repository source, and the same
binary returns the certified \(n=512\) minimum 4663655453568 for the retained field (938 s). The bytes that
were priced were compared with the table that the script rebuilds.

## 2. Why this bounds the value

This is the statement of
[normalized_native/README.md](../../packages/interval_clock_grid/normalized_native/README.md) for any
profile the engine accepts: the minimum over the normalized bank of a feasible nodal dual is at most the
clock-grid optimum \(U_n\)
([NORMALIZED_GRID_BANK_PRICING.md](../12-global-closure/NORMALIZED_GRID_BANK_PRICING.md),
[LEFT_FLOOR_CLOCK_ATOMIZATION.md](../12-global-closure/LEFT_FLOOR_CLOCK_ATOMIZATION.md)), and
\(V\ge U_n-1/(2n)\). Hence

\[
 V\ \ge\ \frac{K-2D}{4nD}\qquad(n=1024,\ D=3.2\cdot10^9).
\]

`refine_dual.py` of the same package reports exactly this quantity for a refined seed. As there, it is a
bound on the value of the game. It is not a security certificate for one explicit Princess law.

## 3. What refinement can still give

| \(n\) | bank minimum | lower bound | engine |
| ---: | --- | --- | --- |
| 256 | 583091421641/409600000000 = 1.4235630 | 1.4216099 | |
| 512 | 36434808231/25600000000 = 1.4232347 | 1.4222581 | 938 s, 2.3 GB, \(2.6\cdot10^9\) states |
| 1024 | 9326184150699/6553600000000 = 1.4230628 | 1.4225745 | 17,862 s, 16.2 GB, \(3.6\cdot10^{10}\) states; center engine 1,515 s, 6.3 GB |

The bank minimum of the same continuous field falls as the Monster's grid gets finer, by \(3.3\cdot10^{-4}\)
and then \(1.7\cdot10^{-4}\) (the first step also contains the incoming-front projection), while the
transfer loss \(1/(2n)\) halves. If the fall halves again, \(n=2048\) would give about 1.42273 and the
limit for this field is about 1.4229. From 512 to 1024 the time of `price_normalized.cpp` grew by a factor
19 and its memory by a factor 7, so \(n=2048\) would need about four days and about 110 GB with it. With
the center engine (factors 10.6 and 6.6) it would need about 4.5 hours and about 42 GB. It was not
attempted. A lower bound above 1.423 needs a better field, not a finer grid.

## 4. What a finer profile would give

The retained field is the full-width interpolant of a profile on the grid \(1/64\). The repository's
optimizer, `solve_normalized.py n --profile-grid k`, runs on this machine and converges quickly when it is
seeded from the next coarser solution (`--seed`, `--profile-seed`): 143 s for \(k=16\) at \(n=32\) from
scratch, 98 s for \(k=32\) at \(n=64\), 18 minutes for \(k=64\) at \(n=128\) down to a gap of
\(7\cdot10^{-6}\). Each optimum was then refined by factors of 2 with the rule of Section 1 and priced
exactly by `price_center.cpp` (policy 3). Bank minima:

| profile | optimized at | \(n=32\) | 64 | 128 | 256 | 512 | 1024 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| \(k=16\) | \(n=32\) | 1.4246923 | 1.4217905 | 1.4204372 | 1.4197595 | 1.4194182 | |
| \(k=32\) | \(n=64\) | | 1.4243495 | 1.4229441 | 1.4222568 | 1.4219089 | |
| \(k=64\) | \(n=128\) | | | 1.4241504 | 1.4234482 | 1.4230955 | |
| \(k=64\), retained | \(n=256\) | | | | 1.4235630 | 1.4232347 | 1.4230628 |

Every entry is the exact minimum of an explicit field, so entry minus \(1/(2n)\) is a valid lower bound on
\(V\); none of them beats (1). Two regularities stand out. The bank minimum of a fixed field falls by half
as much at each doubling of \(n\), so it exceeds its limit by about \(0.18/n\) for every profile. And the
limits, about 1.41908, 1.42156, 1.42274 (1.42289 for the retained field), rise by \(2.5\cdot10^{-3}\) and
then \(1.2\cdot10^{-3}\): the best grid-\(k\) profile is worth about \(0.078/k\) less than the value
1.42397 estimated from the Monster's side. A grid-128 profile should therefore be worth about 1.4234 in the
limit and certify about 1.4231 when priced at \(n=1024\); a grid-256 profile about 1.4234. The grid-128
stage (65,664 variables) needs a longer LP time limit than the 120 s built into `persistent_highs.py`; its
first solve takes 6.5 minutes.

## 5. Reproduce

```sh
python3 packages/interval_lightcone/refine_retained_field.py --selftest    # refinement rule against a literal port
python3 packages/interval_lightcone/refine_retained_field.py --price       # about 5 hours, 16 GB; rewrites the record
```
