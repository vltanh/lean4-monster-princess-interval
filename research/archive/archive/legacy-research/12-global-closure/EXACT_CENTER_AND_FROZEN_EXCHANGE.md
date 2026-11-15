# Exact center continuation and frozen physical strategy exchange

Date: 2026-11-12 UTC.

The unrestricted interval game remains open. This checkpoint proves an exact
conditional continuation value for the supplied Princess field, rejects a
proposed lower law by a complete all-start sweep calculation, and supplies
the physical strategy interfaces needed for a coupled search. It does not
replace the missing matching global inequalities with a finite-table value.

## 1. A closed conditional continuation

Use the frozen field in
[endpoint_joint_i1_field.json](../../packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json).
On its affine terminal slab put
\[
a=7/8,\quad b=15/16,\quad
k=655898601421/62500000000,\quad
\ell=820954217/12500000000,\quad
d=k-\ell,\quad c=-7d/8.
\]
The center CDF is \(Z(t)=dt+c\). Define
\[
D=1-8\ell/k,\qquad
\theta=\frac{1-\sqrt D}{1+\sqrt D},\qquad
\tau=b-\frac{3\theta}{1-\theta},
\]
and
\[
C_*=(b+2)(1-Z(b))+\frac{db^2}{2}-\frac94\ell\theta.
\]
Then, for \(57/64\le t\le\tau\), the unrestricted balanced-tail continuation
value from center rank \(Z(t)\) is exactly
\[
V(t,Z(t))=C_*-\frac{dt^2}{2}.
\]
This is a remaining absolute capture contribution at a specified state,
not the value of the original game.

The lower certificate is the large-root quadratic potential on the full
stated reachable inverse domain. Every direct, rank-boundary, endpoint,
and post-slab exit is included. The exact arithmetic is in
\(\mathbb Q(\sqrt{623060432741/655898601421})\). The independent root replay
of the complete verifier reproduced its full report, including 140 direct
regions, 5,886 rank-boundary regions and 103,840 Bernstein coefficient pairs.

The matching continuation waits to \(\tau\), then makes a continuous
sequence of growing center-return tents with durations
\(\ldots,3\theta^3,3\theta^2,3\theta\), followed by the specified endpoint
tour. The infinitely many early turns accumulate at the departure time.
Finite truncations have the exact energy correction
\(-9\ell\theta(1-\theta^{2m})/4\). Their costs converge by a shrinking
affected-rank argument. No continuity of first hitting time is assumed.

The transformed front potential \(W=V+T_t/2\) is strictly larger than \(3/2\)
throughout this interval. Consequently this particular on-front arrival
branch is slack for the current global target. The off-front extension,
where the captured rank exceeds \(Z(t)\), is the relevant next gate.

See [the exact algebraic attachment](../10-turn-density/AFFINE_CENTER_ZENO_ATTACHMENT.md),
[the preceding rational subsolution](../10-turn-density/AFFINE_CENTER_ATTACHED_SUBSOLUTION.md),
and [the off-front transfer identities](../10-turn-density/AFFINE_CENTER_OFFFRONT_TRANSFER.md).
The off-front packet retains all short-return hinges and uses the actual
exterior field. Forcing a final return at \(b\) is not an admissible
substitute for minimizing over that exterior.

## 2. The retained 159-path candidate is rejected

The former full-bank master had a finite-table value near 1.425924.
Its 159 positive response profiles can be realized as legal avoided-center
paths, but that does not make their dual mixture a lower certificate.

For the frozen clipped realization the complete M1 separation checks every
actual initial atom and both endpoint-sweep directions. There are 62 distinct
positive initial germs, although only 45 limiting initial radii; collapsing
them loses attacks. The resulting 252 routes cover all starts, not a sampled
grid: inside each gap in the actual initial support, the left-first payoff
is nondecreasing and the right-first payoff is nonincreasing. Exact initial
coincidences supply the boundary trace.

The worst route starts at \(15/16-\epsilon\), visits the left endpoint,
then the right endpoint. Its limiting cost is exactly
\[
\frac{4115606858452227030094659793}
     {3276799999999999976930082816}
=1.2559835383460167\ldots.
\]
All 252 costs were independently matched by record and inverse-moment
calculations. The first leg already captures approximately 0.88241 of the
mass. Even an ideal remaining continuation with this prefix cannot exceed
\[
\frac{1397113958465290679188261275}
     {1092266666666666658976694272}
=1.2790960313097754\ldots.
\]
Thus changing only its later center behavior cannot repair this candidate.

See [finite initial M1 separation](FINITE_INITIAL_M1_SEPARATION.md) and
[the prefix ceiling](../../packages/interval_global_closure/INWARD_M1_PREFIX_CEILING.md).
These are candidate exclusions, not new upper bounds for the game.

## 3. Preserve the physical rows

A master row now means one actual path \(p_\epsilon\), paired with its
reflection. On adding a Monster attack, that same path is rescored.
Changing its subordinate scale or center connector creates a new row.

This distinction is essential. A Princess pair at \(\pm\epsilon\) can have
a different limiting payoff from a pair at \(\pm\epsilon^2\) against a
Monster whose start also depends on \(\epsilon\). Equal limiting coordinates
or equal old event labels do not determine the capture order.

The generalized realizer accepts rational-function query coordinates and
chooses a genuinely subordinate scale from all exact gap valuations.
It supports late, early, isolated-avoided and common-wave connectors.
The root independently replayed all 48 geometry cases, 24 realized
upper-germ maximizers and four legacy compatibilities. The nested
initial-layer fixture has limiting response 2; collapsing its Monster
geometry first changes that response to \(3/2\).

The frozen scorer uses exact characteristic inverses, shares caches across
both reflections, and retains their common valid sign radius. The independent
chronological-intersection audit checks 1,372 signed first contacts. The
initial 159-by-1,087 physical matrix has all 172,833 entries complete, with
zero disagreements against the old columns of the abstract table. The new
germ attack is an added column rather than a reason to re-realize old rows.

The native SciPy packing solve of this matrix gives approximately
1.4143104303035083, with 39 positive weights on each side and independently
rescored numerical duality gap below \(7\,10^{-16}\). This is only the
finite physical matrix. The already certified 169-pair Princess law is
being retained as a seed for further exchange.

See [frozen rows](FROZEN_GERM_ROWS.md),
[generalized realization](GENERALIZED_GERM_REALIZATION.md), and
[microscopic center connectors](MICROSCOPIC_CENTER_CONNECTORS.md).

## 4. Unrestricted upper response in germ geometry

The atomic survival-cut engine now accepts \(\mathbb Q(\epsilon)\) geometry.
For a fixed finite germ Monster law, all eventual event and cut comparisons
are exact. Limiting edge capacities are rational and are solved by integer
flow. A uniform sum of reward errors controls every cut simultaneously;
therefore the finite graph's maximum and the small-parameter limit commute.

Independent replay passes 609 specialization checks and 62 graph
extension/serialization checks. The ordinary 280-pair law also reproduces
its existing unwarped response exactly. These tests preserve the distinction
between an unrestricted response to a supplied Monster law and a minimax
certificate.

There is a useful separate simplification. Collapse all vertices and
probabilities of a finite germ Monster law to their ordinary limits, remove
zero-duration legs, and call the ordinary law \(\nu_0\). Then
\[
U(\nu_0)\le\liminf_{\epsilon\downarrow0}U(\nu_\epsilon).
\]
For every fixed Princess path, uniform Monster convergence gives lower
semicontinuity of its first capture time; take the finite weighted sum and
then the supremum over that fixed path. The companion receives its own
response calculation. It must never replace a column against a varying
Princess family. The helper has 462 exact checks and six independent
ordinary integer-flow replays.

See [the germ upper oracle](../../packages/interval_global_closure/GERM_ATOMIC_RESPONSE.md)
and [the collapsed companion](../../packages/interval_global_closure/COLLAPSED_COMPANION.md).

## 5. Global obligations still required

The preserved exact bounds are unchanged:
\[
\frac{36290299773897097}{25600000000000000}
\le V\le
\frac{57045189772271291487410009}{40000000000000000000000000}.
\]
Closing the full proof requires a common value and two matching unrestricted
inequalities. The remaining work is to construct a lower law whose initial
and early capture behavior survives all Monster routes, and match it with
an unrestricted upper law. A supplied-field Bellman certificate, completed
finite master, or completed M1 separator alone does not satisfy that goal.

No Lean compilation or CI was run.
