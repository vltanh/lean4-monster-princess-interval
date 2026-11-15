# Adaptive sparse-event Princess search

This searches the **full legal Qout nodal field** at the chosen physical mesh.
It does not freeze the seed's cone equalities or restrict the Princess to a
coarser profile. Only coordinates currently touched by causal calendar cuts
are explicit LP variables. `interval_sparse_upper/master.py` supplies the
exact projected order; new complete responses introduce new coordinates and
calendar inequalities. Its persistent basis is retained.

## Exact extension of a sparse event assignment

Let the full Qout order be `a <= b`, meaning the field must satisfy
`g(a) <= g(b)`. For consistent selected values `v(e)`, define

\[
 L(x)=\max(\{0\}\cup\{v(e):e\le x\}),\qquad
 U(x)=\min(\{1\}\cup\{v(e):x\le e\}).
\]

Both envelopes are isotone, `L <= U`, and both equal `v` at selected events.
For a legal incumbent `g0`, the extension

\[
                 g(x)=\max\{L(x),\min\{g_0(x),U(x)\}\}
\]

is isotone because pointwise min and max preserve order. It agrees with every
selected value. Every legal extension lies between the two envelopes, so
this construction is simultaneously closest to the incumbent at each node.
It therefore minimizes every separable displacement penalty whose minimum
is at the incumbent. This claim concerns extension with **fixed selected
values**, not optimality of the outer security search.

If each selected value is within `delta` of the incumbent, monotonicity of
`g0` gives `L(x) <= g0(x)+delta` and `U(x) >= g0(x)-delta`. Thus the full
extension also stays within the same trust box. The selected-node LP is
exactly the projection of the full-grid trust-box LP.

The implementation floors floating selected values and applies exact integer
order closure first. It builds the upper envelope from these repaired selected
integers, records the correction, and independently checks every cone and
sticky-endpoint inequality. Forward closure means increasing radius then
backward endpoint time. Reverse closure means forward endpoint time then
decreasing radius. Post-time-two values use the original outward extension.

## Search and validation

```bash
python packages/interval_sparse_lower/test_sparse_lower.py
python packages/interval_sparse_lower/search.py \
  --n 256 --component-prox --radius .001 --keep 32 \
  --initial-routes 128 --seconds 2400 --iterations 300 --lp-seconds 180 \
  --output /tmp/sparse-princess
```

`--component-prox` here stabilizes **event coordinates** at an intermediate
security level. It adds variables only when a new event appears; it does not
freeze transport components. Omit it for direct trust-box maximization. The
entrypoint supplies `--profile-grid=n`; a genuinely coarser profile is rejected.
The existing bundle driver handles exact pricing, reproducible checkpoints,
hashes, rejected trials and budget stops. `--resume` restores physical causal
calendars and the exact incumbent; the sparse LP basis is reconstructed.

The initial LP receives only the lowest `--initial-routes` cached responses;
**all** supplied physical routes remain in the exact cached separator. Each
path initially contributes its earliest-record calendar. These support-plane
choices keep long flat traces from populating the LP with needless latest-tie
vertices. Newly violating paths and their current calendars are still added,
and the complete native oracle remains mandatory. Importing all 4,100 pilot
routes with both tie choices produced 90,355 events and a 90-second cold-solve
timeout; sparse seeding addresses that observed bottleneck.

Cached responses only separate cuts. Every accepted lower requires the
unchanged **complete native response oracle**, followed by the unchanged
`1/(2n)` transfer. The same interpolated CDF is not assigned that game-value
lower. Independent BigInt verification remains the promotion gate. Sparse
projection reduces LP cost; it does not remove continuum error or prove a
finite equilibrium classification.

The regression independently compares projected reachability with the full
order's transitive closure, both envelope sweeps with a direct all-node
definition, and dynamically enlarged sparse trust LPs with independent full
nodal LPs. It also runs real complete tiny-bank response searches.
