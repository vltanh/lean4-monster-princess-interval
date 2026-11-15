# An exhaustive integer lattice certificate for the unrestricted value

Verified implementation and independent rational regression, 2026-11-13.

**Certified result:**

\[
\boxed{V\ge\frac{3050023091}{2147483648}
=1.4202776788733899593353271484375.}
\]

This converts a completed fixed-CDF lattice search into an **unrestricted
game-value lower bound**. The exact frozen input, integer minimum, source
hashes and resulting fraction are recorded in
[the certificate manifest](../../packages/interval_global_closure/lattice_lower/h3_lattice_certificate.json).
The implementation uses no beam or unresolved search frontier. Its independent
checks use Python integers and `Fraction`.

The scope matters: this proves a lower bound for **V** through the global
quantization theorem. It does not assert that the same supplied CDF secures
that number against every continuous Monster path. It neither identifies the
exact equilibrium nor replaces the missing sharp all-Monster Bellman potential.

## 1. Transfer from the entire lattice bank to the unrestricted game

Let B be a positive even integer, n=B/2, h=1/n=2/B and Delta=1/B.
The [common light-coordinate quantization theorem](EFFECTIVE_FINITE_UPPER_REDUCTION.md)
provides a finite rational clock/matching LP with optimum U_n and

    U_n - 1/B <= V <= U_n.

Its bank contains **every** unit-speed lattice Monster that starts on the
h-grid, visits the center by time 2, and visits both endpoints by time 8.
A lattice move has duration Delta and displacement plus or minus Delta.

Fix any legal symmetric ordered Princess CDF F. If c is a verified lower
bound on its payoff against every member of this entire bank, it is also a
lower bound against every mixture of bank paths. Every feasible clock/matching
certificate dominates that physical payoff. Therefore c <= U_n, and

    V >= c - 1/B.

This argument is not a finite sampled-bank optimum promoted to a global bound:
the complete bank is searched, and the explicit 1/B loss is indispensable.
The quantization theorem handles arbitrary original starts, waiting, contacts
at equalities, reversals and infinitely many turns. It uses monotone light
coordinates and preserves causal clocks; it does not assume a finite-turn
optimal Monster or continuity of first-contact time under path perturbations.

## 2. A frozen integer table defines its own legal Princess law

The binary input contains integer entries f[n,j], with 0 <= n <= 6B,
0 <= j <= 2B and positive even D. Entries with n+j even prescribe
F(n/B,(j-B)/B)=f[n,j]/D. The other checkerboard is auxiliary and need not equal
the interpolant at those intermediate points. Endpoint values on the defining
checkerboard are **interior traces**: mass at an endpoint is handled separately
when that endpoint is hit.
The C++ verifier and an independent streaming Python checker verify exactly:

* 0 <= f <= D, reflection f[n,j]+f[n,2B-j]=D, and center value D/2;
* f[n+1,j-1] <= f[n,j] <= f[n+1,j+1], wherever defined;
* positive and negative outward characteristic equalities after a declared
  cutoff a in {1,2};
* f=D/2 from time a+1 onward, meaning all Princess mass is at the endpoints.

Only nodes with n+j even are traversed by the Monster bank. In light coordinates
U=t+x=2i/B and W=t-x=2k/B, these nodes form a rectangular lattice. Triangulate
its physical strip so that time boundaries 0,a,a+1 and spatial boundaries
0,+1,-1 are triangle faces. This is possible because B is even. A time boundary
cuts a cell on its anti-diagonal only when the lower-left index sum is odd;
a spatial boundary cuts a cell on its main diagonal only when the index
difference is even. Sum and difference have the same parity, so the two
requirements never conflict in a cell. Choose the remaining diagonals in a
reflection-symmetric way.

For either diagonal, each triangle has one edge in each characteristic
direction. The checked edge orders give F_U >= 0 and F_W <= 0 throughout it.
They imply monotonicity in x and the two speed-cone transport inequalities.
The signed CDF is continuous in the interior; missing endpoint mass gives
legal endpoint atoms. Its common quantiles are 1-Lipschitz Princess paths.
Reflection is exact. The outward equalities imply F_U=0 on the positive side
and F_W=0 on the negative side after a. The aligned time faces give the claimed
outward motion and endpoint absorption throughout the continuum, not only at
sample points.

Consequently the certificate does not trust floating-point interpolation of
an earlier discovery field. The frozen integer table itself is the definition
of a legal rational characteristic-P1 CDF. The compact input stores only
positive-half horizontal differences through time 2; reflection and the
checked outward shift reconstruct the full table. Its expanded SHA-256 is
fixed in the manifest, and a byte-for-byte round trip was checked.

## 3. First endpoint and the general time-two continuation

Use the ordered quantile coupling. A state records time, position, surviving
left rank mass l, surviving right rank mass r, and whether the center has been
visited. Its instantaneous survival mass is l+r. Moving left or right updates
the appropriate running minima of the two CDF traces. At an endpoint, the
corresponding outside rank mass is zero, including contact at time zero.

After a Monster first reaches an endpoint, its immediate unit-speed sweep
to the opposite endpoint captures every survivor no later than any other
continuation. This preserves the center deadline. Thus it is an exact exit.

For a field outward after time 2, a bank path that has not reached an endpoint
by then has already visited the center. Hence l,r <= 1/2. The surviving left
quantiles flee toward -1 and the surviving right quantiles toward +1 at unit
speed. Their first possible capture is at their respective endpoints. From
(2,x), the exact remaining payoff is

    min((l+r)*(1-x)+2*l, (l+r)*(1+x)+2*r).

These are the two shortest endpoint tours; completion is by time 6. Before
its first center visit, a reflected Monster has x>0 and must satisfy t+x<=2.
The implementation keeps this flag and never assigns the centered terminal
formula to an uncentered time-two state.

## 4. Exact earlier closure for fields outward after time one

The frozen CDF used here satisfies the stronger outward-after-one condition.
This is checked on the full table; it is not assumed from the source field's
name or from a numerical derivative. Such a field is absorbed by time 2.

For a centered state at time 1, the same endpoint-tour formula is exact.
For an uncentered interior state (1,x), x>0, one instead has l>=1/2 and r<=1/2.
A center-by-two Monster cannot visit +1 before its first center: that itinerary
would reach the center no earlier than 3-x>2. Every surviving positive
Princess below x must therefore be crossed before that first center visit.
The immediate leftward unit-speed path intercepts each of those ranks at
its earliest physically possible time.

All negative mass 1/2 remains uncaptured until -1, and surviving right mass r
cannot be caught before +1. At the first center time c>=1+x, exactly these two
rank groups remain. A left-first tour costs 1/2+3r from the center, whereas a
right-first tour costs 3/2+r. The former is no larger because r<=1/2. Delaying
c adds (1/2+r) times the delay. Thus the immediate sweep to -1 and then +1 is
an exact optimal continuation for every uncentered time-one state.

This proof covers waiting and arbitrarily many reversals before the center.
The resulting normalized paths finish by time 5. The optional cutoff-one
search stops at time 1, uses this uncentered exit and the centered tour exit,
and retains the original center deadline 2 in every prefix test.

Normalization minimizes **true physical cost**. It need not preserve the
minimum of an artificially edge-rounded longer-path search. The conclusion
needed here is that the minimum rounded cost of the normalized paths is a
lower bound for the minimum true cost over the entire original bank. The
independent early-exit regression checks precisely that direction.

## 5. Exact edge floors with independent probability and cost precision

Let P be a positive integer cost-precision factor, independent of D. Use

    C = 2*D*B*P

as the cost denominator. Records are exact CDF numerators. On a single grid
edge F is affine. If A and Z are its starting and ending CDF numerators and
R is the old record, first replace R by min(R,A). The exact floor of the
one-clock edge integral in units C is

    2*R*P                                  if Z>=R;
    (A+Z)*P                                if A<=R;
    2*R*P-ceil(P*(R-Z)^2/(A-Z))             otherwise.

The new record is min(R,Z). The other clock uses D-A,D-Z. These formulas are
integers; the squared product and ceiling division use unsigned 128-bit
arithmetic. The input bound 32DBP <= UINT64_MAX/2 keeps all accumulated costs
within unsigned 64-bit arithmetic and the squared numerator below 128 bits.
The verifier requires 1 <= P < 2^32.

Each clock integral is floored separately, losing less than one cost unit.
Every normalized path has at most 6B edges, so its total loss is less than
12B cost units. Increasing P improves integration precision without enlarging
the CDF record alphabet. All pursuit suffixes, rollouts, endpoint excesses
and terminal tours use this same scale. The error budget remains 12B, rather
than 12BP.

## 6. Exhaustive Pareto search and safe pruning

At each time and position, the search retains (left record, right record,
cost, center flag). Smaller records and smaller cost dominate larger ones.
The exact floor is nondecreasing in its input record, and both record updates
and all exits are monotone. A centered state may dominate an uncentered one,
since its remaining deadline constraint is weaker; the reverse is forbidden.
Integer Fenwick minima implement this comparison. No beam, state-count cap,
heuristic deletion or unfinished frontier is accepted as a certificate.
For small D, the CDF numerator itself indexes the record alphabet; this is
an order-preserving implementation change only.

Independent direct pursuits to the left and right give a true continuation
lower bound G_l+G_r, ignoring the incompatibility of moving in both directions.
Along each pursuit the relevant CDF trace is nonincreasing, so there is at
most one partial record crossing. Integer trapezoid suffixes and one ceiling
division evaluate the floor of each pursuit cost exactly.

There is a useful additional incompatibility bound. Let e be any lower bound
for the endpoint trace F(s,-1) at all future times. The surviving masses
b_l=min(l,e) and b_r=min(r,e) then stay at their respective endpoints forever.
With distances d_l=1+x and d_r=1-x, independent pursuits count
b_l*d_l+b_r*d_r. A single physical path must visit the endpoints in some order,
so these groups alone force the extra cost

    min(2*b_r*d_l, 2*b_l*d_r).

Subtracting these groups' independent contributions leaves the independent
lower bound for every other rank intact. Write beta_l=D*b_l and beta_r=D*b_r
for their integer CDF numerators. In integer cost units the extra is

    min(4*beta_r*j, 4*beta_l*(2B-j))*P.

The code obtains a conservative e by taking the minimum of all endpoint
samples from the preceding time row onward. The preceding row protects a
current odd-time boundary point lying between two even-time mesh vertices;
linear boundary interpolation never falls below those samples. Extra unused
checkerboard samples can only weaken this bound. Endpoint mass need not grow
monotonically: the **future minimum** is essential.

Finally subtract 12B from this true-continuation lower bound and clip at zero.
The result is a valid lower bound for the remaining rounded continuation.
Pruning occurs only if accumulated rounded cost plus that bound is at least
a known feasible rounded tour cost. Initial and later incumbent tours obey
the center deadline. In particular an uncentered positive-first rollout is
permitted only when t<=x.

## 7. Certified fraction and independent verification

Let K be the completed minimum in cost units C. The preceding normalization,
downward rounding, dominance and safe pruning prove

    K/(2DBP) <= inf_{m in the whole lattice bank} J(F,m).

Section 1 therefore gives the unrestricted certificate

    V >= K/(2DBP) - 1/B = (K-2DP)/(2DBP).

For the frozen instance, B=1536, D=16384, P=256 and cutoff=1. The complete
search returns K=18308527154 and C=12884901888. Hence

\[
\frac{K}{C}=\frac{9154263577}{6442450944},\qquad
\frac{K}{C}-\frac1{1536}=\frac{3050023091}{2147483648}.
\]

It processes 1,841,162,324 transitions, accepts 920,580,394 states across all
1536 layers, and has maximum live layer 1,215,248. The final frontier is empty.
The separate checker validates 28,323,841 input entries. The expanded table
SHA-256 is
`dda8e0d186d68d1844b1a05c27d374729d48c540c1cd3733216185a9ff1d25c9`.

The saved report records every time-layer size, the final empty frontier,
zero beam truncations, state counts, B,D,P, the exact K and all source/input
hashes. The following checks accompany the full integer replay:

* A separate streaming Python checker verifies the entire frozen table and
  computes the final bound using `Fraction`.
* Independent Fraction polygon integration exhaustively enumerates small
  normalized path banks without dominance, pursuit pruning or the C++ edge
  formula. It covers inward-moving fields, partial record crossings and
  128-bit squared numerators.
* Endpoint-release tests include endpoint populations that first shrink,
  mixtures with delayed radial motion, and an adversarial unused checkerboard.
* The early-outward tests compare with the complete time-two lattice-prefix
  search in true physical costs, and check both centered and uncentered exits
  at P=1 and256.
* Invalid transport, reflection and outward tables are rejected. Incorrect
  claimed final fractions are rejected by the independent checker.

These are exact arithmetic checks of a computer-assisted analytical
certificate. They are not a complete Lean formalization or a claim that a
remote CI workflow has already run. Replay commands are in
[REPRODUCE.md](../../REPRODUCE.md).

## Compatibility with the retained sampler and normalized-bank work

The concurrent native sampler/wrapper regression is preserved. It was rerun
with this unchanged certificate verifier: all 27,666 entries across six legal
fields and 18 refinement cases matched independent Fraction evaluation, and
both complete wrapper fixtures passed. The old two-argument CLI remains
precision one and cutoff two. The optional
[test_native_sampler.py](../../packages/interval_global_closure/lattice_lower/test_native_sampler.py)
requires NumPy; the frozen certificate replay above does not. Earlier native
CI and sampler reports remain in `native_ci_replay.json` and
`native_sampler_replay.json` in the same package.

The normalized Qout construction independently supplies an explicit Princess
law with security 1.419483252072265625 and the current 703-pair Monster upper
1.42516651771598046875. The new lower combines with that upper, giving interval
width 0.0048888388425905094146728515625. The lattice proof does not invoke the
fixed-CDF no-reentry theorem and is therefore unaffected by the separately
recorded off-center-main-diagonal caveat for that theorem.
