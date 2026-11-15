# A delay bound after an outward turn at U=1

This is a response comparison for an ordered reflected princess law.
It excludes some additional same-half excursions under explicit geometric
gates. It does not by itself reduce every monster path to an endpoint I
or a fixed-turn I.

## 1. Assumptions and statement

Let the positive radial paths be continuous, have speed at most one, and
be absorbed at +1 by time two. Give each path and its reflection equal
probability. Fix a monster prefix which starts at +a, moves inward along
U=a to V=v, then outward along V=v to U=1. Assume this prefix stays on
the positive half. Write

    A=Pr(p(0)<=a),     B=R_closed(1,v),
    m=1-max(A,B).

The number m is the mass of positive ranks above the upper capture record
at the end of the shared prefix; the reflected law gives those ranks
total probability m/2. Initial contact uses the closed initial CDF, and
the outward contact uses the closed spatial CDF.

Let C1 be the payoff obtained by immediately continuing inward along U=1
to -1 and then sweeping to +1. Let Cdet be a route which instead makes
any finite number of further excursions on the **strictly positive**
half, then follows U=S inward to -1 and sweeps to +1, where S>1. The
excursions may include endpoint contact, but they may not touch the
center before this final inward leg. Then

    2(Cdet-C1) >= (S-1)-4m.                         (1)

In particular, if S-1>=4m, deleting all those excursions is no worse.
The conclusion includes center and outgoing characteristic atoms in the
princess law. It does not assume that every radial path first reaches
V=1 at time two.

## 2. Capture proof

The two routes have the same history through the U=1 outward turn.
Partition the surviving positive ranks by the lower and upper records
there.

Every still-lower positive rank is caught no earlier after inserting the
excursions. Indeed U=t+m(t) cannot decrease along a speed-one monster
path. The direct inward continuation uses the smallest possible incoming
coordinate U=1; any later inward contact has U>=1. Equivalently, direct
inward motion is pointwise at least as far toward those lower ranks at
each elapsed time. Captures already made on the common prefix remain
unchanged.

Only the m surviving upper positive ranks can benefit. Under C1 they are
all caught by time four. Under Cdet their capture times are nonnegative,
so their integrated gain is at most 4m before multiplying by the
reflection probability one half. This estimate is deliberately coarse;
it does not assume a particular extra-wave shape or the number of added
turns.

No reflected path is caught during the added positive-half excursions.
On the final inward leg its capture time is the first inverse beta_q(S)
of V_q(t)=t-p_q(t). Endpoint absorption by time two gives

    beta_q(1)<=2,     beta_q(S)=S+1 for S>1.

The second identity follows because V_q(2)=1 and V_q is nondecreasing,
while p_q(t)=1 for t>=2. Thus every reflected capture is delayed by at
least S-1. The reflected mass is one half. Adding these three rank
contributions proves (1).

If a princess path has an outgoing-time-one atom, beta_q(1) can be
strictly smaller than two. Its reflected delay is then larger than the
bound used here. The closed upper record in m also includes any atom
captured exactly at the shared outward turn.

## 3. Conditional short-wave application

Suppose a separate field analysis establishes all of the following for
a terminal first-turn column with deficit y:

* its surviving upper mass is at most C*y;
* any nondeletable additional excursion must first reach an outward
  characteristic whose deficit is at least c*sqrt(y);
* after that new lower capture, any new upper capture requires the
  positive endpoint, so the final incoming coordinate satisfies
  S-1>=c*sqrt(y).

Then (1) excludes that entire finite-detour class whenever

    c*sqrt(y) >= 4C*y,

for example y<=(c/(4C))^2. These three geometric gates are hypotheses,
not conclusions of the delay lemma. A short post-one wave alone does
not prove them, and a center-touching detour requires a different
comparison because it can capture reflected center mass early.

## 4. Independent exact checks

Run

```sh
python -B packages/interval_turn_density/verify_postone_same_half_delay.py
```

The verifier uses direct rational intersections of physical princess
and monster paths. It checks 288 routes with one added excursion and
288 with two added excursions. Ninety-six additional checks flag cases
with an outgoing-time-one atom. All 672 checks pass. The fixtures
exercise the inequality; the arbitrary finite number of excursions is
handled by the capture partition in Section 2.
