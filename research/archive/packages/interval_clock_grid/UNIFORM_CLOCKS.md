# Exact clocks on vertices and open legs

This implementation checks the enlarged clock model from [POLYNOMIAL_UNIFORM_LEG_CLOCK_LP.md](../../research/12-global-closure/POLYNOMIAL_UNIFORM_LEG_CLOCK_LP.md). Every active clock may select atoms at physical grid vertices and mass uniformly distributed over open physical unit legs. The physical path bank still has free grid starts, a center visit by time 2, and both endpoints visited by time 8.

The first three exact optima agree with the vertex-only model:

| Grid | Exact optimum | Physical/calendar plans | Exact record states |
|---|---:|---:|---:|
| 1 | 47/32 | 2 | 177 |
| 2 | 4893/3376 | 4 | 1,531 |
| 3 | 3153038167/2187120435 | 10 | 8,861 |

The first two certificates also pass an independent full planning-DAG verifier. Its graphs have 9,431 nodes and 25,829 arcs for n=1, and 192,047 nodes and 584,151 arcs for n=2. The n=3 certificate was checked by the exact physical-record verifier.

## Reproduce

```sh
node packages/interval_clock_grid/solve_uniform_grid.cjs 1 /tmp/uniform_n1
node packages/interval_clock_grid/uniform_certificate.cjs packages/interval_clock_grid/uniform_n1_certificate.json
node packages/interval_clock_grid/uniform_planning_replay.cjs packages/interval_clock_grid/uniform_n1_certificate.json
```

Replace n1 by n2 or n3 as needed. The solver uses floating-point column generation only for discovery. It reconstructs both the positive Monster weights and the dual profile by exact integer linear systems, constructs a BigInt matching witness, and refuses success unless the exact all-path dual equals the exact primal.

## Coordinates and calendars

Physical paths retain integer indices with time and position unit 1/(2n). A vertex pressure type has doubled coordinates `(2j,2k)`. An open-leg type from physical index `(j,k)` in direction d has doubled midpoint coordinates `(2j+1,2k+d)`. Pressure coordinates therefore have unit 1/(4n). A midpoint denotes an entire uniform open-leg type; it is not a point-mass approximation.

Each path has `minus_charges`, `plus_charges`, `minus_uniform`, and `plus_uniform` arrays. An item `[j,a]` places a integer clock units at the indicated vertex or uniformly on that open leg. Each unit has physical selected mass 1/(4n), after fair reflection of the pair.

At the end of every active leg j, cumulative selected mass must be at least j+1. Its final value is exactly the active endpoint index. Real credit on a leg is linear between its two nonnegative endpoint credits. Matching is checked by containment of the doubled type intervals. A common uniform parameter within equal light-coordinate bands lifts every finite matching edge to an actual causal coupling.

The independent record verifier includes the current leg's uniform item before pricing that scoring interval. A unit of current-leg mass is feasible from zero previous credit: selected and scoring times can be coupled identically. The planning verifier implements this differently through separate ordinary and direction-planning states, with rank `4j + q_minus + q_plus + phase`.

## Why agreement is expected

For unit-speed grid paths, common left-flooring of the two light coordinates maps every selected event on an open leg to that leg's own left physical vertex. The physical path stays fixed and every selected time moves earlier, so the clock remains causal with the same total mass. The common monotone floor preserves matching interval containment. Signs may collapse to the center, but a surviving positive image cannot have a center-collapsed matched target. The matching loss is therefore at most the positive mass removed, and deficiency cannot increase.

Consequently arbitrary continuous clocks on this physical bank can be replaced by vertex clocks without increasing the upper objective. The two clock models have the same exact optimum. The expanded implementation provides an independent check of the current-leg pricing and continuous matching bookkeeping; it does not improve the value by itself.

These finite values remain global upper bounds, with the already proved global lower enclosure obtained by subtracting 1/(2n). None of these coarse-grid values is asserted to equal the unrestricted game's value.
