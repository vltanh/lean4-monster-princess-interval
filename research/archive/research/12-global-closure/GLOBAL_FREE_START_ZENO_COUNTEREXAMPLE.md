# An attained infinite-turn response with a free initial position

This gives one explicit legal Princess law for which **every globally
optimal Monster response changes sign arbitrarily close to time zero**.
The Monster's initial position is free. Thus no exact finite-turn best-
response theorem can hold for all legal Princess laws.

This is not an equilibrium law or a new game bound. Its security is at
most one-third in the concrete example below. The example has a center
atom and unbounded density near the center; it lies outside the continuous
center-trace hypotheses of the finite fixed-field response theorems.
It does not exclude a finite equilibrium-sufficient class, a finite
description that allows infinite-turn paths, or regular approaching laws.

## 1. A completely specified static law

Fix

\[
                   \tfrac12<q<1,\qquad0<p<1.
\tag{1}
\]

With probability `q`, the Princess stays at zero forever. With the
remaining probability, choose an independent fair sign and an initial
radius with CDF `G(r)=r^p`, `0<=r<=1`, and stay at that signed position
forever. All Princess paths are legal and stationary.

For a Monster path `m`, let

\[
 T_y(m)=\inf\{t\ge0:m(t)=y\},
\]

with the value infinity if the target is never reached. Its expected
capture cost is the actual physical first-hit integral

\[
 J(m)=qT_0(m)+\frac{1-q}{2}
       \int_0^1[T_r(m)+T_{-r}(m)]p r^{p-1}\,dr.
\tag{2}
\]

No interior-CDF convention is used to price the center atom: a Monster
starting at zero captures it at time zero.

For example, choose `q=3/4`, `p=1/2`. The initial position law is

\[
 \mu=\frac34\delta_0+
      \frac{\mathbf 1_{\{0<|x|<1\}}}{16\sqrt{|x|}}\,dx.
\tag{3}
\]

The Monster path `0 -> +1 -> -1` has cost

\[
 (1-q)\left(1+\frac{p}{p+1}\right)=\frac13.
\tag{4}
\]

In particular the minimum is finite. The proof below in fact shows
that this finite-turn competitor is not optimal.

## 2. Every globally optimal response starts at zero

Take a finite-cost Monster path starting at `x!=0`, and put `a=|x|`.
Construct a new path that starts at zero, travels directly to `x`
in time `a`, and then follows the complete old path delayed by `a`.
The concatenation is legal.

Every noncentral target is static. It is therefore caught by the new
path no later than its old capture time plus `a`; the added initial
segment may catch it earlier. The center atom is now captured at
time zero, whereas the old path cannot reach it before time `a`.
Consequently

\[
 J(m_{\rm new})-J(m)
 \le(1-q)a-qT_0(m)
 \le(1-2q)a<0.
\tag{5}
\]

An old path of infinite cost is already worse than (4). Thus every
global minimizer starts at zero. This is a direct free-start comparison,
not an imposed starting condition or an averaging argument.

## 3. No one-sided initial interval can occur in an optimum

Suppose now that `m(0)=0`, `J(m)<infinity`, and for some `tau>0`
the path remains nonnegative on `[0,tau]`. Choose a small
`0<epsilon<1`. Prepend a negative triangle: travel from zero to
`-epsilon` and back to zero in time `2epsilon`, then follow the
**entire** old path delayed by `2epsilon`.

Every residual static target has new capture time at most its old
capture time plus `2epsilon`. The selected negative targets of
radii `0<r<=epsilon` have total residual probability `epsilon^p/2`.
The old path did not catch any of them before `tau`, whereas the
new triangle catches each at time `r`. Relative to the delayed old
path, each selected target gains at least `tau`: indeed

\[
           T_{-r}(m)+2\epsilon-r\ge\tau.
\]

The center atom remains captured at time zero in both paths. It
follows that

\[
\boxed{
 J(m_{\rm new})-J(m)
 \le(1-q)\left(2\epsilon-
                       \frac{\tau}{2}\epsilon^p\right)<0
}
\tag{6}
\]

whenever `epsilon^(1-p)<tau/4`. This choice is possible because
`p<1`. Reflection proves the same result for a path remaining
nonpositive on an initial interval.

This argument requires no finite-turn normalization, finite completion
horizon, endpoint visits, density bound, or regularity of the old
path beyond its legal speed bound. Delaying a finite-cost path adds
at most a constant to each residual capture time, so the comparison
remains a finite-cost one even if the old completion horizon is
unbounded.

Therefore every globally optimal path has **both positive and negative
positions in every interval `(0,tau)`**. Continuity forces infinitely
many center crossings and directional reversals accumulating at zero.
In particular it cannot be a finite concatenation of monotone pieces
or unit-speed runs.

## 4. A minimizer exists

The set of all 1-Lipschitz paths from `[0,infinity)` to `[-1,1]`,
with their initial positions free, is compact in the topology of
uniform convergence on compact time intervals. This follows from
Arzela-Ascoli on each finite interval and a diagonal subsequence.

For each fixed target `y`, the first-hit function `T_y` is lower
semicontinuous in this topology. If a convergent sequence of paths
has a bounded sequence of first-hit times, pass to a convergent
subsequence of those times; uniform convergence on the corresponding
compact time interval makes the limiting path hit `y` at the limiting
time. If the lower limit of the times is infinite there is nothing
to prove.

Fatou's lemma applied to (2) makes `J` lower semicontinuous. The
finite competitor (4) then ensures that its minimum is attained
and finite. By (5)--(6), every attaining path starts at zero and
has infinitely many initial directional reversals.

Randomization cannot repair a finite-turn restriction: the objective
against this fixed Princess law is linear in a Monster law. Any
optimal randomized response must be supported, up to a null set,
on pure minimizers, each of which has the stated infinite-turn
property.

## 5. What this rules out

This is a global free-start obstruction to a **universal finite-turn
best-response normal form over all legal Princess laws**. It is
stronger in that respect than a counterexample conditioned on a
prescribed center state.

Its scope is also deliberately limited. The center atom and static
law need not be retained by value-preserving Princess normalizations
for the unrestricted game. A supplied continuous P1 field can still
have the proved finite response reduction, and a suitable sufficient
equilibrium class could still admit one. The example does not identify
the unrestricted game value or any equilibrium strategy.

## 6. The atom-free front-one cusp behaves differently with a free start

For comparison, consider the different law in Section 3 of
`FRONT_CONTINUATION_GAPS_AND_ZENO.md`: the initial radial CDF is
`G(r)=r^p`, `0<p<1`, with a fair sign, and a radius `r` stays still
until `t=1-r`, then moves outward at unit speed and stops at its
endpoint. There is no center or endpoint atom initially. Write `Q_p`
for its minimum over Monster paths starting at the center, and `S_p`
for its minimum with a free initial position.

The fixed-center optimum has infinitely many excursions accumulating
at zero, as proved in that note. Nevertheless

\[
                         \boxed{S_p<Q_p.}
\tag{7}
\]

In fact a finite-turn off-center competitor already has cost strictly
less than `Q_p`. This does not assert that a globally optimal free-start
response has finitely many turns.

### A small record excursion and a finite continuation

Take an attaining centered response. The incoming-front and center
terminal reductions allow it to complete by time four. Its center
zeros accumulate at zero, and it is not identically zero on any
initial interval. Choose a sufficiently early center zero
`0<epsilon<1/3`. On `[0,epsilon]` the maximum absolute position is
some `A>0`. Choose a completed one-sided excursion containing a
point where that maximum is attained. By reflection assume that
excursion is positive, with center endpoints at times `s,t`.

Replace just this excursion by its pointwise maximal positive
triangle. Its height and peak time are

\[
              a=\frac{t-s}{2}\ge A,
              \qquad \tau=s+a\ge a,
              \qquad a\le\frac\epsilon2.
\tag{8}
\]

The replacement captures positive targets no later, leaves negative
targets untouched, and has the same physical center exit. Hence it
cannot increase cost; since the original response was optimal, the
modified response is also optimal. Every position before its peak
has absolute value at most `a`. The small-time choice ensures that
all radii it reaches during this early replacement are still static.

At the return time `t`, the surviving positive mass is
`1/2-a^p/2`; the negative surviving mass is at least this large,
because no earlier position had absolute value greater than `a`.
Replace the remainder by an optimal heavier-first balanced center
continuation with the minimum number of proper returns, so every
retained proper return is productive. Section 1 of
`POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md` makes this continuation
finite: its lighter incoming record has the strictly positive gap
`a^p/2` from one-half. This uses a finite positive-gap continuation
only after the selected excursion; it does not assume an infinite
initial balanced normalization.

The first action of that continuation is to the negative side, with
reflection resolving a tie of the two records. If the negative
record is strictly heavier and the action is a proper return,
balance requires its attacked record to fall to at most
`1/2-a^p/2`. Since every Princess radius is nondecreasing, a Monster
peak of height less than `a` cannot capture that much mass. If the
two records are equal, all negative initial radii at most `a` have
already been captured, so a peak below `a` would be unproductive.
In either case the negative triangle has height at least `a`. If instead
the continuation is a direct endpoint tour, its first negative
leg also reaches `-a`. Thus, after the selected peak `+a` at time
`tau`, this modified centered optimum travels straight to `-a`
over the next `2a` time units.

### Cut off the expensive initial history

Start a new Monster at `+a` at time zero and follow the complete
modified old path from its peak onward, advanced by `tau`.
The new path is legal and has finitely many turns.

Every target of initial radius `r>a` was uncaught before the old
peak: all earlier Monster positions had absolute value at most
`a`, and Princess radii never decrease. If its old capture time is
`T`, the new Monster at time `T-tau` is at that old capture position.
The target at this earlier time is no farther from the center.
At new time zero its relative order with the Monster is the opposite
one. The intermediate value theorem therefore gives a new capture
by `T-tau`, for either sign. Each such outer target gains at least
`tau`.

All targets of initial radius `r<=a` stay static through new time
`2a`, since `3a<1`. The new straight segment `+a -> -a` catches
all of them by that time. Their mass is `a^p`, whereas the outer
mass is `1-a^p`. Consequently

\[
\begin{aligned}
 J_{\rm new}-Q_p
 &\le 2a^{p+1}-\tau(1-a^p)\\
 &\le a(3a^p-1)<0
\end{aligned}
\tag{9}
\]

when the early zero was chosen small enough. This proves (7).

The two examples therefore have different conclusions. The static
majority-center law in Sections 1--4 forces global free-start Zeno.
The atom-free outward cusp forces Zeno only in the fixed-center
problem, and its centered optimum is strictly beaten by a finite
off-center competitor. Neither conclusion supplies a finite-turn
normal form for an equilibrium-sufficient class of Princess laws.

## Follow-up: finite global response for the atom-free cusp

The [compensated curvature theorem](COMPENSATED_CURVATURE_AND_CUSP_RESPONSE.md) now combines the strict comparison in Section 6 with a three-run prefront exchange and the positive-gap center continuation. It proves that this particular atom-free cusp admits an attained finite-turn global free-start optimizer. The stationary majority-center-atom example in Sections 1-5 still forces every optimizer to have infinitely many initial reversals. Neither example classifies an unrestricted equilibrium.
