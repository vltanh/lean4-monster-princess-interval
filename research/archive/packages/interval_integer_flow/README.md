# Native integer maximum-flow discovery

This is an **untrusted optimizer**, introduced to accelerate repeated exact
Qout separation during discovery. It does not replace any certificate
verification. A n512 refined-clock pilot spent 64.8 seconds in its first
BigInt closure query; its small probability LP was cheap.

On the actual second n512 candidate (99,188 event nodes, 314,877 closure
arcs), native optimization plus an independent BigInt network replay took
14.30 seconds. Rebuilding the physical graph and repeating the full physical
certificate replay took another 1.10 seconds. The original complete BigInt
query took 137.13 seconds and produced the identical exact upper
`364876917217859/256000000000000`. These are local timings, not CI timings.

The C++ helper uses iterative Dinic search and integer residual capacities.
Every capacity and source-capacity sum must fit below `2^63`; malformed
integers, overflow, inconsistent edge counts, and wrong source bounds are
rejected. An iterative augmenting-path traversal avoids recursion depth
limits on long order chains. Input and output use decimal integer strings.

`native_server.cjs` explicitly replaces only the exported maximum-flow
optimizer before loading the existing cut-discovery server. It checks the
native output's exact graph size, capacity inequalities, conservation, and
flow/cut equality again using JavaScript BigInt. The original server then
performs its mandatory **unchanged** sparse physical certificate replay:
physical paths, causal calendar prefixes, every supplied geometric Qout
edge, integer flow conservation, and equality with the cut. A native bug can
therefore fail or delay a search, but cannot turn an unchecked optimizer
answer into an accepted upper certificate.

From the repository root:

```sh
python packages/interval_integer_flow/test_flow.py
python packages/interval_fixed_marginal/search.py \
  --native-flow --n 512 --iterations 100 --seconds 1200 \
  --lp-seconds 60 --pricing-rounds 2 --level-fraction 0.8 \
  --price-every 3 --alternative-cuts 4 --seed 223606 \
  --output results/fixed-plain-512
```

The regression compares 100 independent integer graphs with the original
BigInt optimizer, includes capacities above exact binary64 range and a
20,000-node chain, rejects malformed inputs and corrupted witnesses, and
replays the retained 676-pair physical seed through the unchanged BigInt
certificate verifier. Discovery metadata binds both the helper source and
the actual compiled binary hash. No native binary is committed.
