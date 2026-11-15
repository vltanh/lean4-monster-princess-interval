# Finite exact response after a stationary piecewise constant tail

## Statement

Fix a time h, Monster position x, and the finite measure mu of targets still
uncaptured at h. Suppose that from h onward every target is stationary in
[-1,1], and mu is the sum of a bounded piecewise constant nonnegative density
and finitely many atoms. Its total mass need not be one.

Let D contain -1, 1, every density-cell endpoint, and every atom position,
after duplicates are removed, and let K=|D|. Then the unrestricted optimal
continuation is attained by a finite unit-speed route whose productive turns
belong to D. Each productive turn strictly enlarges the visited spatial
interval, so no point of D is productive twice. A harmless final endpoint
completion gives the explicit common horizon

\[
 h+2(K+1).
\]

The deliberately loose bound includes the terminal leg and zero-mass arena
completion. This statement concerns the stationary tail from a fixed state.
It does not bound the number of productive turns before h.

## Productive-route normalization

For static targets, speeding each straight piece up to unit speed and deleting
waits never delays any first capture. Once a route has visited an interval
[l,r], an excursion that turns without enlarging that interval captures
nothing new on its outward part. Delete that excursion and continue directly
to its next new frontier. This catches every remaining static target no later.

Thus a finite route can be reduced to alternating left and right turns, each
strictly extending the previous same-side record, until both endpoints have
been visited. Captures at an already visited boundary are included: an atom
there was caught on the previous visit, so a repeated visit is unproductive.

## Local turning-point concavity

Consider one productive right turn y. Keep the preceding left turn a, the
next left turn b, and the subsequent spatial route fixed. Let r be the old
right record and r2 the next right record in the fixed tail. There is a next
right record because the completed route eventually visits +1. Vary y within

\[
 r\le y\le r2.
\]

Also restrict y to one open density cell containing no atom, of signed
surviving density beta. The arrival time at the preceding left turn a is
fixed. Targets first caught on the excursion from a to y have capture times
independent of y. Every target not caught there has its later capture time
shifted by 2*dy.

A target at position y would, if omitted from the present excursion, be
caught on the next rightward pass from b toward r2. Its extra delay is

\[
 D(y)=2(y-b).
\]

If M(y) is the surviving mass not caught on the present excursion, endpoint
differentiation gives

\[
 C'(y)=2M(y)-\beta D(y),\qquad
 C''(y)=-4\beta\le0.
\]

Here C is the unnormalized integral of absolute first-capture time against
the signed measure mu. If beta instead denotes radial density before a fair
reflection, the corresponding contribution is `C''=-2*beta`. The same proof
applies to a left turn after reflection.

Existing atoms elsewhere contribute only affine functions while their
capture branch is unchanged. At an atom boundary, reaching the atom exactly
captures it on the earlier excursion. The closed-contact payoff is therefore
no larger than either relevant one-sided limiting payoff. For a right turn
reaching an atom of mass w at q, the downward jump from the unvisited side is
exactly `2*w*(q-b)`.

## Pushing a turn to a boundary

Intersect `[r,r2]` with the closure of the current density cell. Concavity
implies that at least one endpoint has no larger cost than the current
interior turn, using the closed-contact value at an atom. There are three
possibilities.

1. The endpoint belongs to D. That turn is now fixed at a density or atom
   boundary.
2. It equals the old record r. The current excursion has become unproductive
   and can be deleted.
3. It equals the later record r2. That later excursion has become unproductive
   and can be deleted.

Repeat. A move to D reduces the number of free turns. A collision reduces the
number of turns. This lexicographic progress terminates for every finite
route, without increasing its cost. Every remaining productive turn lies in
D, and each expands the visited interval, so there are at most K of them.
The route has at most K+1 unit legs of length at most 2, proving the displayed
horizon bound.

Only a finite set of such boundary-turn routes exists from the fixed initial
position x. The minimum over that set is attained. The next section proves
that allowing arbitrary histories, including infinitely many turns, does not
lower it.

## Arbitrary histories and the correct approximation direction

Take any continuation of finite expected remaining latency. Truncate it at
relative time T and append a unit endpoint tour of length at most 4. The cost
increases by at most

\[
 4\,\mu\{\tau>T\},
\]

which tends to zero. This gives a bounded-horizon continuous route, but it
could still have infinitely many turns before T.

Approximate that route uniformly by a piecewise linear interpolation through
a fine time partition. Include as interpolation vertices the first-hit times
of every atom and the appended endpoint visits. Interpolation preserves the
speed bound. Every atom is therefore caught no later than before. For the
density part, the captured spatial set at each time is exactly the interval
between the running minimum and maximum of the Monster position. If the
uniform path error is eta and the density is bounded by B, the captured
continuous mass changes by at most `2*B*eta`. On the bounded horizon the
latency error is at most `2*B*eta*(T+4)`, which tends to zero.

This is an explicit upper approximation of the cost; it does not invoke
lower semicontinuity in the wrong direction. Unitize the finite polygonal
route and apply the turning-point reduction. Consequently the finite D-route
minimum is no larger than any arbitrary continuation. The reverse inequality
holds because the finite routes are admissible. This proves exact equality
and attainment for the unrestricted static tail.

## Consequences for uniform translation fans

A finite collection of clipped translation fans is stationary after the last
base-path vertex. Its spatial marginal is piecewise constant density with
endpoint atoms. For the ordered quantile law, a pre-h history removes one
captured rank interval. At the stationary time, the surviving law consists of
the two outer spatial tails, with at most two additional cut locations.
Partial endpoint or coalesced atoms remain atoms at existing locations.

If the complete stationary marginal has K0 density/atom/arena boundaries,
every reachable ordered history therefore has a tail boundary set of size
at most `K0+2`. The uniform tail horizon is

\[
 h+2(K0+3).
\]

For an unsorted raw mixture of N fairly reflected fan components, every
orientation has one captured translation interval. Deleting it introduces
at most two spatial cuts per orientation, giving the conservative bound
`K<=K0+4*N`. The static theorem applies there as well.

The new boundary locations depend on the actual previous records. They must
be retained as state variables in a full dynamic program; this theorem does
not replace them by a fixed grid or show that the earlier phase is solved.

The theorem is pointwise valid for every sufficiently small specialization of
a germ law. A common sign radius fixes the finite ordering of its density and
atom boundaries. No endpoint-by-two condition is used.

## Independent exact fixtures

`verify_static_tail_turns.mjs` compares two implementations. The first
integrates each newly visited spatial record band against a piecewise
constant measure. The second splits each density interval at all Monster
turning positions, evaluates its affine first-hit function by chronological
segment intersection at the midpoint, and integrates it exactly. Atoms are
scored by independent direct first contact.

The fixtures include asymmetric step densities, overlapping uniform bands,
interior and endpoint atoms, atom-only laws, both turn orientations, old-record
collisions, later-record collisions, and exact one-sided germ turns at atoms.
Second differences check `C''=-4*beta` on every tested open cell. Separate
closed-trace checks verify the exact atom jump.

A countercheck prevents the earlier unsafe direct-tour shortcut. Starting at
0, place mass `499999/1000000` at each of +/-99/100 and mass `1/1000000` at each
endpoint. The route `0 -> -99/100 -> 1 -> -1` costs `495001/250000`, while the
direct left/right endpoint tour costs `99500001/50000000`. The former finishes
at `249/50>4`. Stationarity alone does not justify discarding interior turns;
the finite density-boundary theorem is the required reduction.


## Constructive exact dynamic program

The theorem has an O(K^2) implementation in static_tail_dp.cjs.
Insert the current position into D. A state (l,r,side) has visited interval
[D_l,D_r], current position at the named endpoint, and remaining mass

\[
 M=F_{<}(D_l)+\mu([-1,1])-F_{\le}(D_r).
\]

Move to the adjacent unvisited boundary y on either side. Let Delta be the
width of the newly searched cell and beta its signed constant density. The
exact additional latency is

\[
 M\,|y-x_{\rm current}|-\beta\,\Delta^2/2.
\]

An atom at y remains in M during travel and is removed in the successor state;
it is therefore priced correctly. Every move expands the visited interval,
so the recursion is acyclic. Consecutive moves in one direction are allowed
and collapse to one physical leg. The minimum gives the unrestricted static
value by the preceding theorem.

Factory createStaticTailDP(G) returns:

- solve({cells,atoms},start,{absoluteTime,completeEndpoints,maxPoints}):
  exact relative latency, absolute moment, a physical boundary route, and a
  finite-horizon witness.
- fromFans(rows,{normalize:true}): exact stationary density and clipping atoms
  for immutable fans with specified tail positions and translation intervals.
- removeRankBand(measure,lower,upper): exact ordered survivor measure after
  removing a captured rank interval, retaining partial atoms.
- compile(measure,extraPoints): density cells, atom masses, strict/closed
  prefix masses, and total mass.

The optional point cap is an explicit resource guard; exceeding it throws
instead of returning an approximate result. All arithmetic and decisions can
be rational or Q(epsilon). The relative route starts at time 0; the returned
absolute route is shifted by the supplied absoluteTime.

The verifier verify_static_tail_dp.mjs passes 24 fixed-state problems against
164 exhaustive boundary routes scored by independent physical segment
intersection and exact spatial integration. It additionally checks 36 fan
marginal traces and 156 ordered survivor-rank traces, including vanishing
widths and partial endpoint atoms. The common radius is 39747/680680 and the
maximum degree is 2. These are complete checks of the small supplied instances;
the general unrestricted-tail claim rests on the proof above.
