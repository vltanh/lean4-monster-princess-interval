# A linear program for moving physical one-turn geometry and its upper flow

**Status: a certificate-synthesis reduction.** The later [continuum countercertificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) closes the frozen separation comparison negatively. The atomic law synthesized here is an earlier, weaker upper.
For fixed probabilities and a fixed ordered event pattern, the physical
Monster coordinates and a global Princess-response flow can be optimized
together by one finite linear program. This removes a nested numerical
response search. It does not assert that the fixed probabilities or event
pattern suffice for the optimum of the one-turn game.

The independently replayed law in
[the projected upper note](ONE_TURN_PROJECTED_PHYSICAL_UPPER.md) was obtained
by applying this construction after a complete physical-response weight
optimization. Its physical paths, rational probabilities and exact flow are
the certificate; the floating optimization is not a proof input.

## 1. One common light-coordinate map preserves the physical class

Choose a strictly increasing continuous function \(\phi:\mathbb R\to
\mathbb R\) satisfying

\[
\phi(-z)=-\phi(z),\qquad \phi(z+2)=\phi(z)+2,
\qquad \phi(0)=0,\quad\phi(1)=1.
\]

Apply the same map to both light coordinates:

\[
(U,W)\longmapsto(\phi(U),\phi(W)),\qquad
t=(U+W)/2,\quad x=(U-W)/2.
\]

Monotone light-coordinate curves remain monotone, so their physical paths
remain 1-Lipschitz. A horizontal or vertical light segment remains a
horizontal or vertical segment, with positive duration. Therefore a unit
speed Monster leg remains a unit speed leg. The arena boundaries
\(U=W+2\) and \(U=W-2\), the center \(U=W\), and the initial line
\(U=-W\) are preserved. Reflection exchanges the light coordinates and
commutes with the map.

In particular, the canonical parameter path

\[
(a,-a),\quad(b,-a),\quad(b,b+2),\quad(b+4,b+2)
\]

is sent to the same canonical form with parameters
\((\phi(a),\phi(b))\). The inequality
\(a\le b\le2-a\) is preserved because
\(\phi(2-a)=2-\phi(a)\). Endpoint-first faces and the direct opposite
endpoint sweep are preserved too. Thus this transformation remains inside
the precise canonical one-turn class. It does not introduce waiting,
variable Monster speed, or a second interior reversal.

Strict monotonicity also preserves every order and equality among event
coordinates, including the strict/closed first-contact comparisons. The
physical finite-event response construction therefore uses the same
thresholds, clauses and sound order implications throughout this family.

## 2. Every survival coefficient is linear in the map

Let

\[
0=z_0<z_1<\cdots<z_K=1
\]

contain the folds of all query and base coordinates of a supplied rational
finite Monster law, under oddness and translation by two. Write
\(q_i=\phi(z_i)\). These variables satisfy

\[
q_0=0,\qquad q_K=1,\qquad q_{i+1}>q_i.
\]

Split every survival interval at integer boundaries before folding it into
\([0,1]\). Its transformed length is a sum of terms
\(q_h-q_l\), with \(l<h\). Fixed nonnegative rational probabilities
therefore make the coefficient of each response clause

\[
c_j(q)=\sum_{(l,h)}\gamma_{jlh}(q_h-q_l),
\qquad \gamma_{jlh}\ge0,
\]

a rational linear function which is nonnegative on the ordered knot
polytope. No sampled Princess path or differentiability of capture time is
used in this statement. It follows from the exact survival lengths in the
finite-event construction.

Let \(y_i\) be its Boolean ordered thresholds. Each reward is either
\(c_j(q)\prod_{i\in A_j}y_i\) or
\(c_j(q)\prod_{i\in A_j}(1-y_i)\). Empty clauses contribute their
coefficient directly. This one-sign property is essential: arbitrary
mixed-sign Boolean clauses would not have the same closure construction.

## 3. Optimize the map and a flow simultaneously

Keep one auxiliary closure node for each nonsingleton nonempty clause.
For a positive clause, require that its auxiliary implies every literal
and add a source arc of capacity \(c_j(q)\). For an all-false clause,
require each literal to imply its auxiliary and add a sink arc of that
capacity. Single-literal clauses use the threshold node directly. All
threshold order implications are retained as hard arcs.

It is useful here to leave positive and negative terminal contributions
as separate arcs even when they use the same node. This avoids selecting
the sign of a coefficient which changes with \(q\).

Let \(f_e\ge0\) be an arc flow. Enforce conservation at each ordinary
node and, for each terminal arc associated with clause \(j\), enforce

\[
f_e\le c_j(q).
\]

Hard arcs may be uncapacitated. Equivalently, for completed canonical
one-turn routes, capacity 49 suffices: the sum of all clause coefficients
is at most 48, since a route completes by time six, each physical time
length contributes at most two survivor terms, there are two reflected
orientations, and light length is twice physical time. A maximum flow
can be chosen without circulations and has total source flow at most 48.

Write \(F=\sum_{e\text{ out of the source}} f_e\). The finite LP is

\[
\boxed{\quad
\min_{q,f}\ \frac{\sum_j c_j(q)-F}{4}
\quad}
\]

subject to these flow constraints and the knot order constraints. The
factor four accounts for physical time and the fair reflected pair.
Every coefficient and constraint is linear. The objective includes each
empty clause once; for every other clause it is the usual constant plus
source-capacity term of the closure construction.

For any feasible strict map and feasible flow, weak flow/cut duality
proves the displayed objective is an upper bound on every legal Princess
payoff against the transformed physical law. Sound order implications
suffice for this upper direction. Omitting a valid implication merely
weakens the bound; completeness of a supplied projected order graph is
not assumed here.

Thus optimizing the flow jointly with the coordinates is legitimate. It
is not an interchange of a Princess maximum with a nonlinear coordinate
minimum, and it does not treat a formal threshold label as an actual
finite Princess lower witness.

## 4. Collapsed knots and rational physical delivery

Numerical discovery may replace strict inequalities by
\(q_{i+1}\ge q_i\). This is a closed relaxation. A collapsed knot is not
silently accepted as a positive-duration physical leg.

For any relaxed feasible pair, mix its knot vector with the identity:

\[
q_i^{\varepsilon}=(1-\varepsilon)q_i+\varepsilon z_i,
\qquad 0<\varepsilon<1.
\]

The map is now strict. Mixing its flow with the zero flow at the identity
preserves every capacity and conservation constraint. The resulting
objective tends to the relaxed objective as \(\varepsilon\downarrow0\).
This supplies a controlled family of legal physical upper laws, rather
than an unsupported assertion about captures at collapsed coordinates.
Rational knot values and probabilities give rational physical vertices.

For the retained concrete law, discovery knots were rounded to strictly
positive increments with denominator \(2^{26}\), and the probabilities
were rounded and normalized to denominator \(10^{10}\). The final law
was rebuilt from those physical vertices. A fresh integer flow was then
checked independently with Python, including all probabilities, canonical
membership, strict/closed rewards, capacities, balances and cut equality.
The floating flow, its residuals, and the optimizer's objective are not
used by the retained proof.

The portable command is unchanged:

```sh
python3 packages/interval_one_turn/rebuild_projected_upper.py \
  --output /tmp/one-turn-projected
```

The exact countercertificate gate remains
`--require-counterexample`. It passes only if the resulting all-Princess
upper is at most the frozen unrestricted benchmark. The retained law does
not pass that gate. Neither the exact restricted value nor the sign of
\(W_1-U_*\) is determined by this synthesis reduction.
