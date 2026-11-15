# Exact initial-start separation for ordered interval fans

This note upgrades the raw-mixture constructions in CONTINUOUS_FAN_INITIAL_STARTS.md to the actual ordered common-quantile law. Paths, translation windows and normalized constant rational row weights remain immutable throughout a separation call. The output is an exact minimum over a specified continuous Monster family, not an unrestricted response or a game-value certificate.

The ordered supplied-route provider is ordered_fan_cost.cjs, source blob b843ced722089b742ce15ce908220c48d46e64d5. Its constructor takes the fan MODULE, not an already constructed fan instance:

    const O=createOrderedFanTools(G,fanModule);
    const B=O.prepareBasis(rows);
    const law=O.law(B,weights);

The source normalizes the nonnegative constant weights and keeps exact strict/closed endpoint traces.

## 1. Why an additional arrangement is needed

For a unit Monster leg the signed CDF F(t,m(t)) is monotone. The previously captured ordered quantiles form an interval [L,H]. A rightward leg contributes survival

    1-H+L - (F-H)_+,

and a leftward leg contributes

    1-H+L - (L-F)_+.

At an actual endpoint visit the appropriate closed record is updated after integrating the interior trace.

Every component CDF is piecewise affine in time and the initial-position parameter. A raw mixture integrates component capture moments separately; the ordered law first sums the CDFs and then compares that sum with a running rank. Therefore component geometry alone does not fix the ordered hinge branches. One must add equalities of summed CDF values and summed record values.

Inside a completed geometric cell write

    F(t;a)=A*t+B*a+C,   record(a)=D*a+E.

If A is nonzero, its crossing time with the record is affine in a. If A is zero, the entire time interval is on one side of the record, or contributes a zero hinge. Integrating over affine time endpoints gives a quadratic in a in either case. This is the reason an exact finite quadratic arrangement still exists.

## 2. Efficient fixed-tail refinement

Use the oriented fixed-tail coordinates from the raw note. The first leg moves right from b. Its first turn is

    t1=(c-b)/2,   y1=(c+b)/2.

After that turn every Monster leg lies on a fixed space-time ray; only the start of the first inward ray varies. Define the two moving record values

    l(b)=F_strict(0,b),
    h(b)=F_closed(t1,y1).

Both are nondecreasing in b. For each component, the first-turn relative position is affine on a Princess phase with derivative (1+sigma*v)/2>=0; the initial relative position has derivative 1. Their clipped CDF sums are consequently nondecreasing.

### Geometric cells

The implementation inserts:

- the two legal start-domain endpoints;
- every first-turn phase boundary b=c-2*t_i;
- every equality of a first-leg translation-window edge with the relative position at a fixed Princess vertex;
- every equality of a first-turn relative position with a translation-window edge on its Princess phase.

These cuts make the first-leg cost quadratic and make l,h affine. There is no running-record hinge on the first leg: its CDF immediately advances the appropriate initial record, so its survival integral is linear in the component CDFs.

### Rank cells

For the complete fixed suffix, collect:

- every interior CDF value at a ray's piecewise affine time break;
- both strict and closed CDF values at every fixed suffix vertex;
- 0 and 1.

The first inward ray is traced over its whole physically legal time interval, from max(0,c-1) to the first fixed vertex. This contains the variable starting point for every allowed b.

Later upper records are maxima of h(b) and fixed closed endpoint values. Later lower records are minima of l(b) and fixed strict endpoint values. Refining at every equality of l or h with a collected fixed rank therefore fixes both the record source and every activation branch on every later leg.

The monotonicity of l,h allows the implementation to find only target ranks between their endpoint values. Each target can be crossed at most once by each record across the full domain. This avoids a cross-component time-line arrangement for the fixed suffix.

The code verifies that l,h are affine at an additional exact midpoint. It evaluates each final quadratic at two additional rational parameters and fails if either identity is false.

## 3. Complete ordered M1 refinement

By fair reflection consider

    (0,a), (1+a,-1), (3+a,+1),   -1<=a<=1.

Let

    M(a)=F_closed(0,a),
    N(a)=integral from 0 to 1+a of F_strict(t,a-t) dt.

The exact ordered cost is

    C(a)=N(a)+(3+a)*(1-M(a))
         - integral from 1+a to 3+a of (F(t,t-a-2)-M(a))_+ dt.

The raw M1 geometric arrangement already makes N quadratic and M affine on each open cell. Only the last integral requires new rank geometry.

### Time-event lines on the second ray

On a Princess phase p(t)=beta+v*t and orientation sigma, the second Monster ray is m(t)=t-a-2. For a translation edge z, a component CDF changes affine branch at

    (1-sigma*v)*t = a+2+sigma*beta+z.

If 1-sigma*v>0, this is an affine time-event line t=s*a+b. It is kept only while it lies in both the Princess phase and the Monster leg:

    t_i <= t <= t_(i+1),
    a+1 <= t <= a+3.

All these conditions are linear inequalities in a, so each event has one closed validity interval. The final constant Princess tail has no upper phase bound.

If 1-sigma*v=0, the clipping change is a vertical initial-parameter boundary. The implementation inserts that boundary directly instead of dividing by zero.

The event list also contains the Monster leg endpoints and the fixed Princess vertex times. Identical affine event lines are merged over overlapping validity intervals.

Insert every intersection of two unequal event lines inside their common validity range. Between consecutive resulting parameter cuts:

- every active event stays in the same Princess phases;
- every component is on the same clipping branch at every event;
- the order of the time events is fixed;
- the summed CDF at each event is affine in a.

### Initial-rank crossings

On each such interval, insert every equality

    F(t_event(a), t_event(a)-a-2) = M(a).

This fixes the unique activation interval of the monotone second-ray CDF. Consequently the hinge integral and the entire M1 cost are quadratic on every final parameter cell.

An exact midpoint check verifies each claimed affine event-rank function before its zero is inserted. Exact checks at two more rational parameters verify every resulting payoff quadratic.

The event-intersection algorithm is finite but can be expensive for a large basis. Explicit maxEvents, maxPairTests and maxCells guards abort rather than returning partial coverage. No current 349-row performance claim is part of this packet.

## 4. Closed events and global minima

All physical parameter boundaries are scored with the actual route, including initial endpoint overlap, zero-length first legs and first turns that reach an endpoint exactly. The inside-polynomial value is never substituted for a closed endpoint capture.

The compactness/lower-semicontinuity argument from the raw note also applies to the ordered law. A closed breakpoint value cannot exceed a lower one-sided limiting cost. Thus the minimum over the full closed family occurs at a physical breakpoint or an interior stationary point of a convex quadratic piece.

For each piece the implementation reconstructs the exact quadratic from three interior rational values, checks two further values, and tests its stationary point when present. Completeness follows from the event/rank arrangement proof; the sampled identities are independent guards against implementation errors.

For germ inputs the finite comparison and division decisions retain one common positive epsilon radius. The laws and Monsters are evaluated at their actual germ coordinates; an interior turn whose limit is an endpoint remains an interior turn.

## 5. Independent first-contact verifier

The independent helper physicalOrderedFanScore computes the signed CDF directly from each effective translation interval. It does not call the ordered provider, its survival-area routine, the raw inverse-band primitive, or its gradient.

It splits a unit Monster leg at all Princess vertex times and all crossings of translated interval edges. On each open interval the signed CDF is affine. Each newly captured rank band is integrated against its affine first-contact inverse. Endpoint record jumps add the actual endpoint time times the newly captured mass. Initial endpoint mass contributes time zero. At completion the captured quantile interval must have mass one.

This is a second exact evaluation of the physical ordered law: first-contact rank moments are compared with the provider's survival integrals.

### Completed verification

Ordered M1:

- 8 supplied laws, 101 complete parameter cells;
- 413 independent rank-moment route scores;
- 202 independent payoff-polynomial checks;
- 5,246 affine CDF time pieces;
- common radius 1/56, maximum arithmetic degree 2.

The subunit asymmetric fixture needs 14 time-event intersection cuts and 6 additional rank cuts. This is a concrete check that merely reusing the raw cells would omit necessary geometry.

Ordered fixed tails:

- 19 complete fixed-tail families, 140 parameter cells;
- 579 independent rank-moment route scores;
- 280 independent payoff-polynomial checks and 280 closed-boundary checks;
- 9,425 affine CDF time pieces;
- common radius 3/160, maximum arithmetic degree 4.

The two-outward-wave fixture with first opposite characteristic c=1 has raw minimum 291/320 and ordered minimum 977/960. The verifier therefore tests an actual rearrangement improvement, rather than a family on which the two couplings accidentally coincide.

As in the raw fixture packet, these particular tests contain no interior convex stationary minimizer. The exact stationary branch is included by the proof and evaluated whenever present; the report does not count an untested physical stationary witness.

## 6. APIs and replay

    const M=createOrderedFanM1Separator(
      G,fanModule,orderedModule,rawM1Module,entries
    );
    const result=M.separate({keepCells:true});

    const F=createOrderedFanFixedTailSeparator(
      G,fanModule,orderedModule,rawTailModule,entries,
      {firstDirection:1,tail:[["2","-1"],["4","1"]]}
    );
    const result2=F.separate({keepCells:true});

Each entry is {row:preparedIntervalFan,weight:constantRational,id}. The fixed-tail result uses oriented start b and additionally returns physical_start=firstDirection*b. Both providers expose the exact supplied ordered law, route and score.

    node packages/interval_global_closure/verify_ordered_fan_fixed_tail_separator.mjs FIXED_REPORT.json
    node packages/interval_global_closure/verify_ordered_fan_m1_separator.mjs M1_REPORT.json

The M1 verifier imports only the independent helper from the fixed-tail verifier; importing that module does not run its command-line entry point.

This packet is specific to clipped interval fans. Endpoint-reflected fans proposed later are new physical rows with different CDF event lines; they are not silently substituted into these providers.
