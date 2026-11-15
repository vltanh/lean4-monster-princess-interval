# Complete atomic response with germ Monster coordinates

## Scope

The input is a finite symmetric paired Monster law. Each path has rational
functions of a positive parameter \(\epsilon\) as its light-coordinate vertices.
For all sufficiently small \(\epsilon>0\), it starts at time zero, stays in
\([-1,1]\), follows unit-speed legs, and visits both endpoints. Coordinates have
finite limits. Probabilities are nonnegative rational germs summing exactly
to one.

The output is the exact limiting UNRESTRICTED Princess response to this
supplied law. It is not an equilibrium certificate and does not restrict the
Princess to a time grid or fixed number of waves.

## Two separate infinitesimal roles

Monster coordinates live in \(\mathbb Q(\epsilon)\). The existing three labels
at each event level mean a value just below, exactly at, or just above that
level. Their side is a second, subordinate infinitesimal \(\delta\), smaller
than every positive arrangement gap in the Monster geometry.

Thus two Monster levels with the same constant term but different powers of
\(\epsilon\) remain distinct. Their label thresholds and physical strip
constraints are never collapsed merely because their limits agree.

The existing schema is unchanged:

- query_v: canonical rational-germ strings;
- base_levels: canonical rational-germ strings;
- label index \(k=3j+\sigma+1\), with \(\sigma\in\{-1,0,1\}\).

For a physical realization one may choose a sufficiently large integer \(K\)
and set \(\delta=\epsilon^K\), with exact comparison checks. The upper response
theorem itself may also use the original fixed-\(\epsilon\), then
\(\delta\downarrow0\), supremum argument. It does not identify the two scales.

## Stable finite event graph

The atomic survival-cut theorem is applied at every sufficiently small
positive \(\epsilon\). There are only finitely many comparisons of rational
germs in the event construction. Recording their polynomial sign radii gives
one interval on which all of the following remain fixed:

1. query and level order, including exact ties;
2. virtual and physical strip bounds;
3. strict initial-side and first-contact predicates;
4. threshold implications and positive survival clauses.

Every reward is a nonnegative germ \(r_j(\epsilon)\). The graph keeps ALL
event/order constraints, even when the corresponding reward has zero limit.

The implementation is a narrow lift of the existing rational module. Exact
arithmetic replaces coordinate arithmetic; the coefficient sign gate uses
eventual sign instead of inspecting a rational numerator. All event, capture,
and bound comparisons remain exact. Number conversions occur only in the
optional floating discovery coefficients and final row limits. Exact germ
rewards are retained per atom.

## Exact limiting maximum closure

Let \(\mathcal C\) be the finite family of feasible cuts of the stabilized
graph, and let \(b_j(C)\in\{0,1\}\) indicate whether reward \(j\) is activated.
The complete response at fixed \(\epsilon\) is

\[
V(\epsilon)=\frac14
 \max_{C\in\mathcal C}\sum_j r_j(\epsilon)b_j(C).
\]

The factor \(1/4\) is the unit-leg light-coordinate factor \(1/2\) and the
symmetric-pair averaging factor \(1/2\).

Since the feasible family is finite,

\[
\lim_{\epsilon\downarrow0}V(\epsilon)
=
\frac14\max_{C\in\mathcal C}
 \sum_j r_j(0)b_j(C).
\]

Every \(r_j(0)\) is a nonnegative rational. A common denominator therefore
turns this limiting maximum closure into an exact integer max-flow problem.
The returned flow is checked for capacity constraints, conservation, and
equality of cut capacity and total flow. Both extremal optimal cuts are also
rescored through the independent first-contact formula.

A uniform bound avoids enumerating the feasible cuts. Define

\[
E(\epsilon)=\frac14\sum_j |r_j(\epsilon)-r_j(0)|.
\]

Then \(E(\epsilon)\to0\) and

\[
|V(\epsilon)-V(0)|\le E(\epsilon)
\]

on the common comparison interval. The certificate retains every nonzero
error term as an exact positive germ. This bounds the full response
supremum, including Princess paths that depend arbitrarily on \(\epsilon\).

Zero-leading rewards can be zero in the limiting objective. Their geometric
order constraints remain present. Removing those events before compiling
the graph would be a different and generally invalid operation.

## API

The CommonJS factory exports createGermAtomic(E,G), where E is the preserved
atomic survival engine and G is the validated rational-germ oracle.

Its result contains:

- Model(atoms): compiles exact Monster geometry. Each atom has exact_light,
  an array of two-coordinate germ strings. Endpoint completion is required
  by default.
- pack(model): serializes query levels, labels, constraints, and exact germ
  rewards.
- integerLimitCut(model,weights): accepts exact probability germs, verifies
  their sum, and returns the rational limiting response, both extremal label
  rows, exact capture germs, a replayable integer flow certificate, and
  uniform error terms.
- model.solve(numericalWeights): the inherited floating discovery solver
  uses limiting reward coefficients only. Its result is not an exact
  certificate until integer replay.

The lower germ oracle and this upper oracle use the same physical field but
serve different roles. A matched limiting upper and lower certificate would
be needed to close the game.

## Regression and a noncommuting corner

Six finite laws were tested at three exact rational values of \(\epsilon\).
All609 reward, topology, capture, and envelope checks agree with the original
rational integer oracle after specialization. Every limiting flow additionally
passes exact conservation and cut replay.

The fixtures include endpoint sweeps, perturbed M1 starts, split M2 turns,
split initial positions, a general initial-inward route, and nested powers
near an initial corner.

The nested fixture mixes the endpoint sweep with weight one half and an
initial-inward route with

\[
a=1-\epsilon,\qquad
v=-1+\epsilon+\epsilon^3,\qquad
s=1+\epsilon^2
\]

with weight one half, followed by endpoint completion. Its exact limiting
unrestricted response is \(2\). Collapsing its vanishing initial legs first
would instead give the ordinary endpoint law, whose response is \(3/2\).
The finite germ graph preserves this contact layer correctly.

These are verification fixtures, not proposed near-equilibrium laws.


## Retaining a growing event universe

Model accepts optional extraQueries and extraBases. This retains exact germ
coordinates belonging to earlier saved controls when the physical atom bank
grows. extend(shape,atoms,options) unions the saved query/base universe with
the new atom geometry and recompiles all physical rewards.

restore(shape,atoms) checks event order, physical bounds, offsets, and the
presence of every Monster query and nonnegative level. By default it also
recompiles the physical rewards. A discovery caller may skip that last step
with auditRewards:false, but integerLimitCut automatically recompiles before
certifying any such restored model. Cached rewards alone are never trusted
for an exact certificate.

lift(small,labels,full) requires the smaller query and level universes to be
contained in the larger one. It retains the same label side at every old
query and inserts a legal minimal graph at new queries. The optional
tail:"absorb" fills newly added queries beyond the old final query along
the endpoint boundary instead. Old atom capture germs are preserved.

A lifted abstract control is not asserted to be the same already-specialized
physical path. If new Monster events require a smaller common subordinate
scale, its legal realization changes accordingly. This can change capture
against the new atoms while retaining the old iterated-limit response row.

Six extension fixtures checked both extremal old controls after adding a
Monster with an epsilon^5 start perturbation and extra epsilon^6/epsilon^7
profile levels. All old capture germs were preserved exactly, and restored
integer responses agreed. The main specialization suite remains unchanged.


## Physical exchange rows and a constant-coordinate fast path

An exchange master must retain each previously specialized physical Princess
germ path. When a new Monster is added, that same path is rescored by exact
first capture. Re-lifting an old abstract profile and selecting a new
subordinate scale creates a NEW legal candidate; it is not preservation of
the old physical row and must not replace it silently.

The abstract label rows returned by the cut are iterated \(\delta\)-limit
capture germs. They guide construction of new physical rows. The eventual
lower certificate must test the actual chosen realizations against all
Monster paths using the germ capture-order oracle.

sparseSolve(full,numericalWeights) compiles only strictly positive Monster
support, then returns both extremal label candidates and their limiting
discovery rows. It applies no probability clipping threshold. It also returns
the sparse model and labels, so a new physical response can be realized on
that small universe and then scored against every bank atom. Old physical
rows remain unchanged.

Constant coordinates use direct exact rational operations as a performance
optimization. Every genuinely epsilon-dependent operation still uses the
validated germ field. This preserves the complete serialized event graph
and exact reward germs.

The existing280-pair rational law was independently replayed through this
lift. All77,939 reward coefficients agreed with the original rational
compiler, and the archived integer certificate replayed117,051 positive
flows on105,783 nodes and268,928 arcs. Both extremal responses were exactly

\[
957063215727541539/671088640000000000.
\]

The constant-coordinate fast path produces byte-identical graph/reward
serialization and reduced compilation from59.5 seconds to1.92 seconds in
the portable V8 runtime. This is a verification of an existing law, not a
new bound optimization.
