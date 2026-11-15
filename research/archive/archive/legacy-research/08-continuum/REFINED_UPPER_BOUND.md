# An exact upper bound from the archived 32-grid discovery

## Result and scope

The supplied symmetric mixture of 134 monster paths guarantees

    V <= 36563170811/25600000000
       = 1.4282488598046875.

This improves the previously certified upper bound `5717477/4000000` by
exactly `28681989/25600000000`. Together with the existing unrestricted
princess certificate, it gives

    36290299773897097/25600000000000000
        <= V <= 36563170811/25600000000.

The remaining gap is positive. This is an improved bound, not a matching
saddle pair or a determination of the exact value.

The starting numerical weights were already present in
`packages/interval_uniform_reduction/research/upper_continuum_32.json`.
The new work converts them to a rational strategy and checks the guarantee
entirely by integer arithmetic. The floating optimizer and the archived
numerical response calculation are not assumptions of this certificate.

## 1. Explicit rational strategy

`packages/interval_refined_upper/strategy.json` specifies 67 reflection
pairs. A record `(kind,x,w)` chooses the corresponding path with total
probability `w/10^9`, split equally between it and its reflection:

    M1(x): (0,x) -> (1-x,1) -> (3-x,-1), then constant;
    M2(x): (0,x) -> ((1-x)/2,(1+x)/2) -> (2,-1) -> (4,1).

All weights are positive integers and their sum is `10^9`. Every path is
1-Lipschitz, stays in `[-1,1]`, and visits both endpoints by time four.
Consequently it captures every continuous princess path by time four.

The verifier uses spatial and temporal scale `S=128`, so every supplied
vertex, first pairwise intersection, and first endpoint visit has integer
coordinates. Every division in this geometric calculation is checked for
exact divisibility. Let `D=10^9` and `scale=2DS`. Each actual reflected or
unreflected path has mass `w/(2D)`.

## 2. Necessary capture constraints

Fix a princess starting point y that differs from all monster starts.
Let B be the monsters starting below y, and A those starting above it.
For a monster i let `d_i` be its first visit to the endpoint opposite its
initial side of the princess. For `i in B,j in A`, let `c_ij` be their
first meeting time, when they meet before time four.

For any continuous princess path, its first capture times satisfy

    0 <= r_i <= d_i,
    min(r_i,r_j) <= c_ij.

The first condition follows because a path cannot pass from one side of
the princess to the opposite endpoint without meeting her. For the second,
if neither capture had occurred before the monsters' first meeting, the
princess would have to remain strictly between two paths that have become
equal, which is impossible.

These are only necessary conditions in the upper-bound proof. The converse
deadline-envelope theorem is therefore not needed for this certificate's
upper inequality.

## 3. Per-path event compression

For each i, form its own event list `E_i` from zero, four, `d_i`, and all
`c_ij` involving i in the preceding opposite-side pairs. Round each feasible
`r_i` upward to the next event in `E_i`, obtaining `r'_i`.

This preserves every constraint: an endpoint deadline is in its own list,
and if `r_i<=c_ij`, then `r'_i<=c_ij` because the pair event is in `E_i`.
The rounded weighted objective can only increase. Thus a network with
different event lists for different monsters remains an upper relaxation
of every princess response. No common global time grid is required.

The rounded survival variables are one on the intervals before `r'_i` and
zero on subsequent intervals. If i is in B, represent these variables by
membership in the source side of a cut. If i is in A, represent them by
membership in the sink side. This opposite convention turns each forbidden
simultaneous survival into a directed cut implication.

## 4. Integer flow certificate

For every interval `(a,b)` of `E_i`, give its node an objective arc of
capacity `w_i*(b-a)`, where a and b are integer times at scale S. The arc
goes from the source for i in B, and to the sink for i in A. Consecutive
nodes have implication arcs enforcing decreasing survival. Endpoint
deadlines force survival to zero, and a pair meeting contributes the
implication arc from i's node at that time to j's node at that time.

All implication capacities are `4*scale+1`, larger than the total capacity
of all objective arcs, which is `4*scale`. Hence a minimum cut never cuts
an implication arc. For any feasible rounded deadline vector, the
associated cut has capacity

    scale * (4 - sum_i w_i r'_i / (2D)),

with `r'_i` now written in real time units. If F is the value of any
feasible source-to-sink flow, weak flow-cut duality gives

    E T(M,p) <= sum_i w_i r'_i/(2D) <= 4-F/scale.

The verifier computes integer flows, then checks their capacities and
conservation independently of the flow algorithm's internal state. It
also extracts the cut deadlines, checks every endpoint and pair constraint,
and checks equality between the deadline objective and `4-F/scale`.
Thus its arithmetic assertions validate both a feasible flow and a matching
feasible cut for every chamber.

## 5. All initial positions, including starting atoms

The network depends only on the partition A/B, so one calculation covers
an entire open chamber between consecutive distinct monster starts.
Reflection symmetry allows positive chambers to cover their negative
reflections. The verifier checks all 27 positive chambers using the full
interval walls `-1` and `+1`; it makes no assumption that the princess stays
nonnegative after starting.

At a starting atom, every coincident monster has capture time zero. Put
all coincident monsters on either side as in an adjacent open chamber.
Their zero deadlines satisfy every constraint in that chamber, while the
classification and constraints for all other monsters are unchanged.
The chamber upper bound therefore also covers the atom. The same argument
covers the endpoints; zero lies in the closure of the first chamber and
has no coincident monster in this strategy.

The largest of the 27 exact bounds is
`36563170811/25600000000`. The resulting inequality applies to every pure
princess path and hence, by integration, to every mixed princess strategy.

## 6. Reproduction

Run from the repository root:

    python packages/interval_refined_upper/verify.py

The package requires only Python's standard library. It constructs 282,194
arcs across the 27 networks, with at most 14,457 arcs in one network. The
saved `verification_output.txt` lists every chamber value and the exact
improvement. The verifier fixes the expected final rational value and
rejects any mismatch.

This result still leaves the all-monster lower-certificate gap. Neither
rounding the strategy weights nor solving these response networks proves
global optimality of M1/M2 or of this 134-path support.
