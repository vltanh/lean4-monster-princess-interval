# Finite global certificate synthesis after the exact horizon reduction

Date: 2026-11-13. **Every declared finite polynomial certificate template
can be checked against the full unrestricted game by a finite real-algebraic
problem.** The exact horizon and physical-clock lift theorems remove the
previous conditional absorption and physical-feasibility gaps. They do not
supply a uniform degree, partition or chart bound, nor an explicit matching
certificate pair. A completed finite-dimensional minimax reduction is not
claimed.

Inputs: [exact horizon reduction](GLOBAL_EXACT_HORIZON_REDUCTION.md),
[exact physical-clock lift](FINITE_STATE_PHYSICAL_CLOCK_LIFT.md),
[signed Bellman actions](../10-turn-density/GLOBAL_CDF_BELLMAN.md), and
[pressure matching](GLOBAL_CAUSAL_PRESSURE_MATCHING.md).

## 1. Input from the horizon theorem

Use a symmetric ordered Princess law on [-1,1]. Its negative-rank half
stays nonpositive and its positive-rank half stays nonnegative. Retain its
paths through time H=3; thereafter send each rank toward its signed
endpoint at unit speed. This modification preserves the full security
value: Monsters visiting zero by H cannot capture a previously surviving
rank earlier after the modification, and Monsters avoiding zero through
H have expected capture time at least H/2=3/2. The known upper bound is
strictly smaller than 3/2.

For a Monster that has visited zero by H, every survivor at H belongs to
one of the two outer rank tails. Its future unit-speed outward motion
cannot be caught from behind before its endpoint. Thus the remaining
problem is exactly a weighted two-endpoint tour. A best response can
complete by time H+4=7.

This is an exact reduction to a compact-time *function* problem. It is
not yet a finite-dimensional parameterization of the unknown functions.

## 2. A full-game lower certificate with no extra center flag

**Theorem 1 (global lower certificate).** A legal symmetric ordered CDF
and potential satisfying (B), (I), and (T) below, with c<=3/2, guarantee c
against every Monster path. The potential need not assume a Monster turn
bound, finite Princess support, or endpoint absorption before time three.

Let F- and F+ be the strict and closed traces of the supplied legal CDF
on 0<=t<=3. For rank records l,h use the state domain

    0 <= l <= F-(t,x) <= F+(t,x) <= h <= 1.

Let Q(t,x,l,h) represent a certified lower bound for the absolute capture
time contribution of the surviving ranks. It may be any explicitly
defined finite piecewise polynomial; record concavity is optional.

For every legal rightward unit leg from (t,x) to (e,y), with
y=x+e-t and 0<=t<=e<=3, define

    h' = max(h,F+(e,y)),  l'=l,
    G+ = e*(h'-h) - integral_t^e (F+(s,x+s-t)-h)_+ ds.

For every leftward unit leg use y=x-e+t and

    l' = min(l,F-(e,y)),  h'=h,
    G- = e*(l-l') - integral_t^e (l-F-(s,x-s+t))_+ ds.

Require the exact Bellman inequalities

    Q(t,x,l,h) <= Gv + Q(e,y,l',h')                 (B)

on the entire feasible state domain, in both directions. Require also

    Q(0,x,F-(0,x),F+(0,x)) >= c                    (I)

for every x, with c<=3/2. At time three impose only

    Q(3,x,l,h) <= min(
      l*(4+x)+(1-h)*(6+x),
      (1-h)*(4-x)+l*(6-x))                         (T)

on feasible states satisfying l<=1/2<=h. No terminal condition outside
this region is needed for the proof, because no-center histories are
handled by their independent 3/2 lower bound. A separate center flag is
therefore unnecessary.

### Why these conditions cover arbitrary Monster paths

For a finite unit-leg Monster that visits zero by three, telescope (B)
through time three, using first-contact record updates. A visit to zero
puts the median inside the captured interval permanently. The terminal
tour formula is therefore valid. Conditions (I) and (T) prove the bound.

For an arbitrary Monster visiting zero by three, replace its continuation
after three by the optimal endpoint tour; this cannot increase its
payoff and completes by seven. Choose n midpoint quantiles of the
Princess law and include the stationary path at zero as an additional
zero-weight target. All these targets remain ordered. The finite
capture-order domination theorem supplies a finite unit-leg canonical
Monster capturing each target no later. In particular it visits zero by
three. If its last selected capture occurs before three, extend it by
finitely many unit-speed endpoint bounces through time three, stopping
the final bounce at exactly three. All selected targets are already
captured, so this changes none of their capture times. Then append a
nearest-endpoint tour if needed. If the last selected capture occurs at
or after three, append that tour directly. The resulting route has
unit-speed legs throughout [0,3] and is complete by ten. Thus telescoping
(B) never silently applies it to a holding segment, and no continuity
assumption on Q is being used to fill that gap.

For any Monster the captured quantiles form an interval. Midpoint
discrepancy bounds the payoff difference between the n selected ranks
and the entire law by T/n on a common capture horizon T, including atoms
and tied captures. The canonical route therefore gives

    c <= J(original Monster) + 20/n.

Let n tend to infinity. Monsters avoiding zero through three already
cost at least 3/2. This proves the lower bound against every legal
Monster, including waits, non-unit speeds and Zeno paths. No convergence
of first-contact times under polygonal path approximation is invoked.

The zero-weight target is useful: merely canonicalizing the selected
quantiles need not preserve the original center visit, whereas adding
this target preserves it coordinatewise.

## 3. An exact finite real-algebraic problem for each declared template

**Theorem 2 (finite verification at fixed syntax).** Once the following
finite partition and degree bounds have been declared, feasibility of
Theorem 1 is a finite first-order sentence over the ordered real field.
It includes all real states and durations, strict contacts, moving atoms,
and degeneracies. No discretization of the opposing Monster is made.

Fix finite integers describing a candidate syntax:

* a finite sign-condition partition for the CDF, with a bound on the
  number and degree of its defining polynomials;
* a polynomial formula for each of F- and F+ on each piece, with a fixed
  degree bound;
* a finite piecewise polynomial formula for Q, with fixed degrees.

Coefficients, boundary coefficients when applicable, and c are finitely
many unknown real numbers. Partition coverage and compatibility are
first-order real formulas. CDF normalization, monotonicity, right/left
trace identities, symmetry, and the full transport inequalities

    F+(s,x-(t-s)) <= F+(t,x) <= F+(s,x+(t-s))

for 0<=s<=t<=3 are likewise finite first-order real formulas. Extending
the CDF by zero/one outside the arena makes these inequalities explicit
without endpoint ambiguity. Trace limits can either be supplied by
explicit pieces or expressed by the ordinary epsilon-delta formulas,
which still have finitely many real quantifiers.

The only apparent nonalgebraic operation in (B) is the positive-part
integral. For this *piecewise polynomial* syntax, its exact graph is
semialgebraic:

1. Substitute the unit ray (s,x+v*(s-t)), v in {-1,+1}, into every
   partition polynomial and every candidate branch polynomial.
2. Partition [t,e] at all real roots of the resulting polynomials and
   of each branch value minus the relevant rank record.
3. Each nonzero univariate polynomial contributes at most its degree
   roots. Polynomials identically zero on the ray are handled by the
   vanishing of all their coefficients; they do not create an unbounded
   number of intervals.
4. On each resulting open interval the applicable CDF branch and sign
   of the positive part are fixed. Integrate its polynomial by its
   polynomial primitive and evaluate at the algebraic breakpoints.
5. Quantify over the finitely many breakpoints, branch choices and
   order conditions. Repeated breakpoints and zero-length intervals
   accommodate all degeneracies. If the ray lies on an interface for
   an entire interval, use that interface's supplied strict/closed
   trace branch. Point values do not affect the integral but do affect
   the terminal record update, which is checked separately.

If the partition uses B polynomials of ray degree at most db and the
CDF has P branches of ray degree at most df, at most B*db+P*df distinct
interior roots are needed. A corresponding finite formula defines each
integral exactly. This statement is NOT the false general assertion
that integrals of all semialgebraic functions are semialgebraic; rational
or algebraic integrands can produce logarithms or other transcendental
values. The polynomial-in-the-integration-variable restriction matters.

Consequently (B), (I), and (T), together with legality, form a finite
sentence of the ordered real field for every fixed template. Exact
quantifier elimination decides that sentence in principle. It checks
all real starting positions, all real durations and all rank states;
it is not a mesh or a sampled path bank. Practical complexity may be
very large.

### Optional record-vertex reduction

If

    Q(t,x,l,h)=min_j [a_j(t,x)*l+b_j(t,x)*h+d_j(t,x)],
    a_j(t,x)>=t, b_j(t,x)<=-t,

the existing record-concavity argument reduces (B) to the vertices of
each current affine region in the record rectangle. For K planes,
each region is cut out by K-1 plane comparisons and four rectangle
faces. There are at most

    K * binomial(K+3,2)

candidate record-vertex families per physical piece. Invertible 2x2
systems give rational functions of (t,x); determinant-zero cases and
empty regions are handled by finite real-algebraic case splitting.
The terminal median restriction merely clips the rectangle further.
The remaining continuous variables are (t,x,e) for (B), plus one
initial x variable. This improves a verifier's size; it does not bound
K at the true game optimum.

## 4. Finite upper certificates without an explicit path bank

The exact physical-clock lift supplies seven nonnegative control fluxes
on a fixed seven-coordinate polytope, graph horizon 24, and three linear
registration guards. Its continuity equation is **necessary and
sufficient** for a physical Monster/clock law. Therefore a certified
finite description of these fluxes does not need to enumerate Monster
paths or separately guess how to lift an aggregate pressure field.

One concrete finite certificate syntax is a finite polyhedral complex
in graph-time/state space, carrying polynomial measure densities on its
faces. Include the initial and terminal measures, and require the
prescribed initial support, nonnegative control fluxes, total occupation
identity, all guard supports, and the continuity equation in the ambient
space. Singular face measures must be retained when present.

For a finite measure input it is convenient to set R=sum_i F_i on
[0,24] times the state polytope and require its graph-time marginal to
be ordinary Lebesgue measure. Check the ambient distributional identity

    partial_lambda R + div_z(sum_i v_i F_i)
      = delta_0 rho_initial - delta_24 rho_terminal.

Both boundary measures have total one. Disintegration of R gives
probability slices almost everywhere; bounded velocities and this weak
equation give their narrowly continuous representative. Thus no unknown
arbitrary time-indexed probability curve is left outside the supplied
measure certificate. The time-marginal check is itself an affine
projection/marginal identity of the finite chart data.

These distributional checks are finite in this syntax. On each affine
chart, integration by parts gives a polynomial bulk divergence and
polynomial boundary fluxes. Verify their coefficient identities, cancel
shared-face fluxes, and match the initial and terminal traces. A current
normal to a lower-dimensional chart would create a normal derivative
of its supporting delta measure; require its coefficient to vanish,
or explicitly cancel it with another current on that same chart.
Testing only the interiors of full-dimensional cells is insufficient.
Nonnegativity is a finite polynomial inequality problem on the supplied
polyhedra.

The affine pressure projection is

    alpha_bar = (1/2)*(t,x)_# F_minus_charge
              + (1/2)*(t,-x)_# F_plus_charge.

Its inert x=-1 part is removed exactly before applying the matching
formula. Split the projected charts at x=-1 and x=0 and retain boundary
mass explicitly. A polynomial density on a polytope has a finite
piecewise polynomial density under a linear projection, relative to the
appropriate image dimension: subdivide into finitely many chambers with
a fixed fiber-vertex description and integrate the polynomial over the
resulting simplices. Rational-affine coordinate chart measures avoid
unnecessary square-root normalization constants for lower-dimensional
Hausdorff measure.

Supply a partial matching measure pi in the same finite polyhedral
polynomial syntax on pairs (t,u;s,v). Check its two marginal domination
inequalities and its polyhedral support condition

    v >= u+abs(s-t).

The marginal integrations and total masses are finite exact polynomial
integrations over affine fibers. Thus the density domination conditions
and the cost inequality

    M + mu_plus(X) - pi(X cross X) <= c

are finite real-algebraic conditions. Superposition in the exact lift
theorem produces a genuine physical Monster law from the certified
fluxes. The pressure-matching theorem then bounds **every Princess**.

**Corollary (finite matched-template theorem).** A lower template passing
Theorem 2 and an upper finite flux/matching template passing the checks
above at the same c prove V=c. Neither template has to enumerate a
finite bank of the opponent's trajectories. Fixing a rational polyhedral
complex and piecewise constant nonnegative densities gives particularly
simple finite linear coefficient constraints; higher polynomial degrees
require nonnegativity certificates or exact real-algebraic verification.

The upper syntax is sufficient, not proved complete at the optimum.
The exact lift establishes sufficiency for **arbitrary** feasible
measures. It does not establish that an optimal such measure has a
finite polyhedral polynomial density representation. Curved or more
singular optimal support could require another finite certificate
language, or an approximation hierarchy with no finite exact endpoint.

## 5. The exact remaining completeness gap

The horizon theorem genuinely removes an unproved restriction. It fixes
the compact domain on which the unknown strategy and potential must be
found. It does not bound their number of pieces, polynomial degree,
number of free boundaries, or the dimension/number of Monster charts.
The space of Lipschitz paths on a fixed time interval remains infinite
dimensional, as does the feasible CDF space.

For each fixed syntax the preceding construction is finite. Taking

    there exists some finite number of pieces and some finite degree

is an unbounded union of such problems, not one finite first-order-real
problem. Quantifier elimination cannot quantify over an arbitrary
function or an arbitrary-length coefficient list. Compactness alone
does not replace those variables by finitely many coordinates; a
Caratheodory support argument would need a finite sufficient payoff
feature space, which has not been established.

An additional diagnostic is algebraicity. A fixed first-order-real
certificate template with rational input defines a semialgebraic set
of feasible c values. Its finite extremal values are algebraic. If
such a complete template exactly characterizes V, it consequently
proves V algebraic. No algebraicity theorem for this game's value is
currently available. This does not show that an exact template cannot
exist, but it exposes a nontrivial conclusion being assumed by any
claim of an automatic fixed semialgebraic reduction.

There are therefore two honest completion routes:

1. Construct one explicit finite pair of full-game certificates at the
   same c. Its verification proves V=c directly; no prior theorem that
   every equilibrium belongs to the chosen syntax is needed.
2. Prove an equilibrium-specific uniform complexity theorem giving
   actual finite bounds for a sufficient certificate syntax, then
   decide its finite feasibility problem.

Neither has yet been done. The exact bounded-horizon theorem is a
substantive unrestricted reduction, and the construction above is a
finite full-game verifier for each candidate. Neither alone supplies
the requested finite-dimensional minimax classification.
