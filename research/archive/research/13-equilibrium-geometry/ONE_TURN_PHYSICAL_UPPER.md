# An independently certified physical one-turn upper

> **Superseded upper, retained for reproduction.** The later [continuum countercertificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) proves W_1≤142472349375511/100000000000003<U_* and closes the frozen separation target negatively. This note's earlier physical certificate remains valid.

**Status: valid historical upper certificate.** The frozen separation
comparison is now closed negatively by the continuum result above; the exact
one-turn value remains open. This note concerns the canonical class \(\mathcal B_1\)
defined in [ONE_TURN_SUBGAME_BRACKET.md](ONE_TURN_SUBGAME_BRACKET.md):
unit-speed straight legs, at most one interior reversal before the
first endpoint, and then a direct sweep to the opposite endpoint.
The endpoint reversal is not an interior reversal. The Princess has
arbitrary initial position and an arbitrary 1-Lipschitz path.

**Later improvement:** the [projected physical certificate](ONE_TURN_PROJECTED_PHYSICAL_UPPER.md) gives the stronger exact upper `478205958821456999/335544320000000000`. The law, clocks, and endpoint baseline in this note remain a valid earlier certificate and the fixed reference for the endpoint-component obstruction.

## 1. The concrete theorem

There is a rational probability law \(\nu_1\) on \(\mathcal B_1\) such
that, for **every** legal Princess path \(p\),

\[
 \mathbb E_{m\sim\nu_1}T(m,p)
 \le B_1:=
 \frac{1459511091170171}{1024000000000000}
 =1.4253037999708701171875.
\tag{1}
\]

Consequently the restricted minimax value satisfies

\[
 \boxed{\frac{36409808231}{25600000000}
 \le W_1\le
 \frac{1459511091170171}{1024000000000000}.}
\tag{2}
\]

The lower endpoint in (2) is the existing unrestricted game lower;
no new Princess lower certificate is asserted here.
The law and clocks are stored compactly in
[one_turn_upper.json.gz](../../packages/interval_one_turn/one_turn_upper.json.gz).
They specify 413 rationally weighted physical/calendar plans over
326 distinct reflected physical path pairs. A calendar is proof data
attached to a physical path; different calendars on the same path do
not require different physical Monster behavior.

Each plan is used together with its reflection, with equal conditional
probability. The physical mesh is \(1/512\), and the plan weights have
common denominator \(10^{12}\). Every positive-weight path visits the
center by time two, belongs to \(\mathcal B_1\), and completes its
two-endpoint tour by time \(65/16\).

| Physical class | Exact probability |
|---|---|
| Endpoint start, immediate sweep | \(158373491249/250000000000\) |
| Interior start, endpoint first, no interior reversal | \(190419854979/10^{12}\) |
| One interior reversal, then the endpoint tour | \(7043447201/40000000000\) |

These three probabilities sum to one.

### Relation to the historical separation target

The frozen unrestricted upper remains
\[
 U_*=\frac{291849329389899}{204800000000000}.
\]
This earlier one-turn upper is **above** the frozen benchmark by exactly
\[
 B_1-U_*=
 \frac{66111055169}{256000000000000}
 =0.00025824630925390625.
\tag{3}
\]

Thus (1) neither proves \(W_1>U_*\) nor supplies the opposing
certificate \(W_1\le U_*\). It significantly strengthens the previous
one-turn upper \(1458323028259559/1017696260809728\), but does not
improve the already smaller unrestricted upper. It does not identify
the optimal one-turn distribution, prove \(W_1=V\), or solve the
restricted saddle problem. The complete response-domain theorem in
[ONE_TURN_COMPLETE_DOMAIN.md](ONE_TURN_COMPLETE_DOMAIN.md) and the
certificate in this note address different sides of that problem.

## 2. Why the Princess remains unrestricted

The upper proof uses a normalization valid for this **fixed**
reflection-symmetric physical Monster law. It does not infer a global
upper from a finite set of Princess tests.

First symmetrize any Princess law. This preserves its expected payoff
against a reflection-symmetric Monster law. Next couple its one-time
marginal CDFs by a common uniform quantile. The resulting trajectories
are legal: the speed bound on the original law implies the CDF
transport inequalities, which imply the same speed bound for each
quantile.

This ordering cannot decrease capture time in expectation against
any fixed Monster route. Indeed an uncaptured continuous Princess
trajectory must remain strictly on one side of the Monster.
The probability of staying below is at most the minimum of the
strict marginal CDF values along the route; the probability of
staying above is at most one minus the maximum closed CDF value.
For common quantiles these two tail bounds are attained, up to
rank-boundaries of measure zero. Integrating the survivor
probabilities proves the assertion. This argument includes atoms
and time-zero contacts.

A symmetric ordered law can be represented by a fair fixed sign
and a nonnegative ordered radius \(R(t)\). Stop each radius at its
first endpoint contact. This cannot make capture earlier: if the
Monster later reaches that endpoint, continuity forces it to have
met the original trajectory no later. The stopped paths remain
legal and ordered.

Finally impose maximal outward motion after time two:
\[
 R^{\mathrm{out}}(t)=\min\{1,R(2)+t-2\},\qquad t\ge2.
\tag{4}
\]
Every Monster in the supplied law has visited zero by time two.
Every positive Princess surviving to time two is therefore to the
right of the Monster, and every surviving negative Princess is to
its left. The outward modification stays at least as far outward
as the original legal path. If the Monster meets the modified
survivor, continuity forces a meeting with the original survivor
no later. Thus (4) also cannot decrease the Princess payoff,
simultaneously against every path in the law.

It follows that bounding symmetric ordered, endpoint-stopped,
outward-after-two laws from above bounds **all** Princess laws.
The argument uses neither a turn restriction on the Princess nor
a minimax exchange or an assumed Princess best response.
The center deadline is essential to this proof and is checked in
the certificate.

### Atoms and passage to regular CDFs

It is enough to establish a uniform upper for regular normalized
laws with continuous interior CDFs and no center atom.
Here is an explicit approximation argument.

For a normalized radius \(R\), draw an independent
\(Z\sim\operatorname{Uniform}[0,1]\) and, for \(0\le t\le2\), set
\[
 R_\varepsilon(t)=(1-\varepsilon)R(t)+\varepsilon Z.
\tag{5}
\]
After time two, apply (4) to \(R_\varepsilon(2)\). Before time two
the speed is at most \(1-\varepsilon\), and afterwards it is at
most one. Almost surely the radius does not hit either boundary
before two; after two it stops at one. It is within
\(\varepsilon\) of the original radius throughout the relevant
horizon. The pre-two radial distributions have bounded densities;
the outward continuation gives continuous interior CDFs and
continuous endpoint traces. Reorder this mixture by common
quantiles, which can only improve its payoff.

For continuous paths, first coincidence is lower semicontinuous
under uniform convergence: any limit of earlier coincidence times
would itself be a coincidence of the limiting paths. All Monster
paths here complete an endpoint sweep by \(65/16\), so capture
times are uniformly bounded. Fatou's lemma therefore gives the
original payoff at most the lower limit of the approximating
payoffs. A common upper for the regular ordered approximations
passes to the original law. Endpoint atoms and center atoms are
therefore included in theorem (1).

## 3. Admissible calendars give continuous-path upper planes

For a regular normalized radial law, write \(g(t,r)\) for its radial
CDF, using the interior trace at \(r=1\) and \(g(t,0)=0\).
Fix a physical Monster path \(m\). Its two clock lifetimes
\(\tau_-\) and \(\tau_+\) are its first visits to \(-1\) and \(1\).
Before the respective endpoint, define
\[
 p_-(s)=1+\operatorname{sgn}(m(s))g(s,|m(s)|),
 \qquad
 p_+(s)=1-\operatorname{sgn}(m(s))g(s,|m(s)|).
\tag{6}
\]
At a center event both prices are one. A clock is deactivated at
its **own** endpoint, so that endpoint is not a selected event for
that clock. The other endpoint uses the interior trace in (6).

The two ordered survivor records give the exact identity
\[
 J(m)=\frac12\sum_{\sigma\in\{-,+\}}
 \int_0^{\tau_\sigma}
       \min_{0\le s\le t}p_\sigma(s)\,dt.
\tag{7}
\]
Now choose, independently of the Princess, an atomic selected-time
measure \(\eta_\sigma\) of total mass \(\tau_\sigma\) satisfying
\[
 \eta_\sigma([0,t])\ge t,\qquad 0\le t<\tau_\sigma,
\tag{8}
\]
with all selected times strictly before its own endpoint.
Its quantile map assigns each scoring time \(t\) a selected history
time \(s\le t\). Therefore each running minimum in (7) is at most
the selected price, and
\[
 J(m)\le
 \frac12\sum_{\sigma\in\{-,+\}}
       \int p_\sigma(s)\,d\eta_\sigma(s).
\tag{9}
\]
This is a genuine continuous-path inequality, not sampled capture
time. Any admissible calendars give it; they need not be optimal.

Let \(n=256\), \(\Delta=1/(2n)=1/512\). The supplied calendar at
node \(j\Delta\) has mass \(a_j\Delta\), where \(a_j\) is a
nonnegative integer. If the clock endpoint has index \(K\), the
verifier checks
\[
 \sum_{i=0}^{j}a_i\ge j+1\quad(0\le j<K),
 \qquad \sum_{i=0}^{K-1}a_i=K.
\tag{10}
\]
Between successive selected grid times the cumulative mass is
constant; (10) supplies (8) throughout each such interval, including
the relevant left limits. Thus the finite inequalities check the
full causal condition, not merely causality at sampled times.

Write the plan probability as \(q_i/W\), \(W=10^{12}\).
Summing the two clocks and the physical mixture turns (9) into
\[
 J(\nu_1)\le
 \frac{M+\sum_v c_vg_v}{4nW}.
\tag{11}
\]
Here \(M\) is the integer total selected mass, and \(c_v\) is the
integer signed pressure at a radial event. These integers are
reconstructed from the actual physical moves, exact plan weights,
and calendars by the independent verifier.

## 4. Sound Qout inequalities suffice

Legal normalized radial fields satisfy \(0\le g\le1\). The speed
bound gives the ordinary cone implication
\[
 g(t,r)\le g(s,a)\quad\text{when }a-r\ge|s-t|.
\tag{12}
\]
Endpoint stopping gives \(g(v,1)\le g(u,1)\) for \(u\le v\).
Outward motion after two gives
\[
 g(v,r)=
 \begin{cases}
 0,&r\le v-2,\\
 g(2,r-v+2),&r>v-2,
 \end{cases}
 \qquad v\ge2.
\tag{13}
\]
The endpoint values in these formulas are always interior traces.
Use (13) to eliminate every charged event after time two.

The remaining graph contains selected events \((t,r)\) with
\(0\le t\le2\), \(0<r\le1\). Each supplied order edge
\((t,r)\to(s,a)\) is independently checked against
\[
 a-r\ge|s-t|
 \quad\text{or}\quad
 \bigl[a=1,\quad s\le\min\{2,t+1-r\}\bigr].
\tag{14}
\]
The second alternative is sound because (12) reaches the endpoint
at time \(\min\{2,t+1-r\}\), after which endpoint stopping permits
an earlier endpoint time.

The full projection theorem and sparse construction are documented
in [SPARSE_CHARGED_EVENT_QOUT.md](../12-global-closure/SPARSE_CHARGED_EVENT_QOUT.md).
For this upper certificate, **completeness of the supplied graph is
not needed**. Missing a valid order inequality enlarges the class
being maximized over and can only weaken the upper. Every included
edge must be valid, and the replay checks (14) edge by edge.
No graph-generator correctness assertion is trusted.

## 5. Integer flow proves the upper

Let \(P=\sum_v\max(c_v,0)\). Attach a source edge of capacity \(c_v\)
to each positive-pressure event and a sink edge of capacity \(-c_v\)
from each negative-pressure event. Every supplied order edge has
capacity \(P+1\).

A feasible source-to-sink flow of value \(F\) matches positive
pressure to negative pressure through inequalities \(g_u\le g_v\).
Matched pressure contributes at most zero. Unmatched negative
pressure is nonpositive, and unmatched positive pressure contributes
at most its mass because \(g\le1\). Hence
\[
 \sum_v c_vg_v\le P-F
\tag{15}
\]
for every legal normalized field. Combining (11) and (15) proves an
all-Princess upper \((M+P-F)/(4nW)\). This argument needs only a
valid flow through sound edges. The supplied equal-value cut also
checks that this particular finite closure problem has been solved
exactly; it does not assert that the physical law or calendars are
globally optimal.

The independent integer reconstruction gives
\[
\begin{aligned}
 M&=1458244103230376,\\
 P&=305482442000336,\\
 F&=304215454060541,\\
 P-F&=1266987939795.
\end{aligned}
\tag{16}
\]
The flow and cut have the same integer value. Substitution in
(11) and (15) gives exactly (1).

| Verified item | Result |
|---|---|
| Physical/calendar plans | 413 |
| Distinct reflected physical pairs | 326 |
| Causal prefix inequalities checked | 1,204,680 |
| Closure graph nodes, including source and sink | 35,132 |
| Closure graph arcs | 139,253 |
| Exact flow and cut | \(304215454060541\) |
| Endpoint baseline | \(182280512903797/128000000000000\) |
| Closure excess | \(253397587959/204800000000000\) |
| Their sum | \(1459511091170171/1024000000000000\) |

The verifier also checks every physical unit-speed move, every
arena constraint, the center deadline, first-endpoint interior
turn count, direct post-endpoint sweep, exact probability
normalization, selected-event legality, flow capacities,
conservation, and cut equality.

## 6. Reproduce without numerical discovery

The retained input contains exact run-length encoded physical
moves and selected-clock charges, integer weights, and the expected
rational upper. No floating discovery checkpoint or LP solution is
needed to regenerate the certificate.

From the repository root:

~~~sh
python3 packages/interval_one_turn/rebuild_upper.py --output /tmp/one-turn-upper
~~~

This expands the exact law, builds a proposed sparse graph,
reconstructs an integer maximum flow, and runs both the existing
JavaScript BigInt replay and the independent Python integer replay.
The generated certificate is
/tmp/one-turn-upper/one_turn_upper.sparse.json; the directory also
contains the two replay reports.

The independent replay by itself uses only the Python standard
library:

~~~sh
python3 packages/interval_one_turn/verify_upper.py /tmp/one-turn-upper/one_turn_upper.sparse.json
~~~

Graph generation and native maximum flow are proposal steps.
Acceptance uses exact physical data, valid-edge checks, and integer
flow/cut replay; no floating tolerance is involved. Rebuilding uses
the repository's Python graph utilities, Node, and a C++ compiler;
the Python replay does not import those utilities or an optimizer.
No CI execution or Lean formalization is claimed.

The compact input for the result stated here has SHA-256

~~~text
compressed:   f560ed0593fd93b6c73ab287a3e2efa5e061df3ab4413c37e49fc85e7ea534cb
uncompressed: 66a3e4cef01902a4ec4a4a72ad0dcee6f0585569ecef98122a89efd07460c6bf
~~~

## 7. Resolved comparison and remaining exact-value problem

The [separation directive](ONE_TURN_SEPARATION_DIRECTIVE.md) originally
asked for either an all-one-turn Princess lower above \(U_*\), or an
all-Princess one-turn Monster upper at most \(U_*\). The later
[continuum countercertificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md)
proves the second alternative with a strict margin and excludes the first.

The certificate in this note remains a valid earlier upper above the
frozen target. The exact restricted value \(W_1\), its equality or strict
inequality with \(V\), and a matching unrestricted saddle remain open.
