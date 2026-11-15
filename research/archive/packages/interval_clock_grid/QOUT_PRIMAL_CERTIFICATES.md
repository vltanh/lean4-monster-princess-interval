# Physical upper certificates from the normalized CDF order

`qout_primal_certificate.cjs` turns a native-master physical plan mixture into an exact global Monster upper certificate. It verifies the physical paths and causal clocks, then solves and replays a small integer maximum-closure problem. It does not require a dense positive-to-negative pressure graph.

The mathematical justification is law-specific Princess normalization. For any fair reflected Monster law whose paths visit the center by time 2, the Princess supremum is unchanged by common-quantile ordering, endpoint stopping, and maximal outward motion after time 2. Regularized laws in this class have radial nodal profiles in the closed polytope Qout. Every fixed admissible clock plane upper-bounds their actual capture payoff. Hence the maximum of that plane over Qout bounds the unrestricted Princess response to the supplied physical law. See [NORMALIZED_GRID_BANK_PRICING.md](../../research/12-global-closure/NORMALIZED_GRID_BANK_PRICING.md).

This differs from the unrestricted pressure-matching certificate: the additional CDF constraints are justified by normalizing the Princess against this fixed centered Monster law. It is still a global upper bound for a concrete physical Monster law.

## Build and replay

```sh
node packages/interval_clock_grid/qout_primal_certificate.cjs --make path/to/native.checkpoint.json /tmp/physical_upper
node packages/interval_clock_grid/qout_primal_certificate.cjs /tmp/physical_upper.physical.json
```

The maker rounds nonnegative plan weights to a common denominator of 10^12 by largest remainders. Numerical weights are only discovery input. Every accepted upper is calculated exactly from the resulting rational law. The replay also accepts gzip-compressed certificates.

The physical verifier checks every initial position and unit-speed move, the center-by-two and endpoint-by-eight conditions, exact probability normalization, and both active-clock calendars. The clocks must satisfy every left-limit causal prefix and have exactly their active endpoint's mass. Every listed path is used together with its reflection with equal probabilities.

## Closure graph

Field variables are the positive radial parity nodes through time 2. Every selected event contributes its signed clock mass to that node. A later event is substituted along the exact outward characteristic to time 2; a nonpositive footpoint has field value zero. Center events contribute only to the endpoint baseline.

Let c be the resulting integer coefficient vector and M the integer baseline. The remaining objective is

```
M + max { sum(c_i * g_i) : 0 <= g <= 1, g respects Qout order }.
```

The graph has source capacities c_i for positive coefficients, sink capacities -c_i for negative coefficients, hard inner-to-outer transport edges, and hard edges enforcing the nonincreasing endpoint trace. The outward identities have already been eliminated by substitution.

If P is the sum of positive coefficients and F the maximum flow, the exact objective is M+P-F. Dividing by 4n times the path-weight denominator gives the global upper. The supplied witness contains nonzero integer arc flows and a source-side cut. Replay checks all capacities, exact conservation, and equality of flow value with cut capacity. The hard capacity P+1 ensures that a minimum cut respects every order constraint.

## Validation

Applying this closure to the existing exact physical laws for n=1,2,3,4,6 reproduces their previously certified optima exactly. Their closure graphs have respectively 7,20,41,70,152 nodes. These comparisons test the normalization substitution and scaling against the independent full-bank certificates.

The saved n=32 native-checkpoint law has 385 physical/calendar plans representing 309 distinct fair physical pairs. Its exact certificate gives

```
global upper = 91282277722011 / 64000000000000
             = 1.426285589406421875.
```

Its graph has 4,130 nodes and 9,780 arcs. The supplied flow and cut both have integer value 10457015449292. This coarse-grid upper does not improve the tighter separately certified warped-law upper; it demonstrates an operational exact primal certificate for the sparse normalized master.
# Improved n=64 physical certificate

`upper_n64_physical.json.gz` is a self-contained exact law and closure-flow certificate giving

\[
V\le \frac{364842628535291}{256000000000000}
 =1.42516651771598046875.
\]

It contains 736 causal calendar plans on 703 distinct reflected physical path pairs. The exact Qout closure has 16,450 nodes and 40,760 arcs; its flow and cut both equal 23,926,115,635,762. Independent replay checks the unit-speed paths, center deadline, endpoint completion, all causal calendar prefixes, capacities, conservation, and equality of flow and cut:

```sh
node packages/interval_clock_grid/qout_primal_certificate.cjs packages/interval_clock_grid/upper_n64_physical.json.gz
```

The associated `upper_n64_physical_replay.json` includes hashes of both the gzip artifact and its uncompressed exact certificate. Numerical discovery and the rounding of weights are not trusted by this replay.

