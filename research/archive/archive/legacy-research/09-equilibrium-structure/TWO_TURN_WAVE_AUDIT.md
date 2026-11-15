# Independent audit of the first- and last-wave capture formulas

## Outcome

The formulas in `FIRST_WAVE_TWO_TURN_RESPONSE.md` and
`LAST_WAVE_TWO_TURN_RESPONSE.md` are correct under their stated order,
separation, peak, and endpoint assumptions. The continuous-rank verifier
passes. A separate exact segment-intersection audit also agrees with both
formulas, including a capture term not exercised by the original fixtures.

This audit concerns the fixed-law response identities. It makes no claim
that their two-turn monster family is globally sufficient or that the
tested laws approach an equilibrium.

## 1. First-wave formula

On the initial leftward leg U=x, the radial CDF decreases from A(x) to

    max(A(-v),B1(x)).

The hypothesis v<=inf C1 removes the outgoing cap from this expression,
and x<inf A2 excludes the second incoming wave. The captured ranks are
therefore exactly the initial-outward class between the two fronts.

On the following rightward leg V=v, the first incoming CDF rises to one
because s>=sup A1, while the second wave remains absent because s<inf A2.
This captures every remaining high rank. The next leftward leg U=s
captures the low missed ranks on the first return outward, at
`(s+C1(q))/2`. Its feasibility follows from C1(q)>=v on those ranks and
the strict monster peak inequality s-v<2.

The negative ranks are all captured at s+1. The assumption C2<=1<=s
prevents a prior crossing after the monster enters the negative half;
strict parameter order makes the possible equality at s=C2=1 null.
These observations give every term and coefficient in the first-wave
formula, including the endpoint-pair payoff s+2.

Differentiating the lower-front case l=A(-v)>B1(x) gives exactly

    1-A(x)=A'(-v)[s-x+C1(l)-v].

The derivative is 1-A(x) when the other lower-front branch is fixed.

## 2. Last-wave formula

On U=x the second incoming wave is absent. The remaining radial front is

    l=max(A(-v),min(B1(x),D1(v))).

Writing b=B1(x), the captured interval (l,A(x)) splits at
`m=max(l,b)`. Ranks (l,m) meet the first return outward, and ranks
(m,A(x)) meet the initial outward leg. This is the source of the
otherwise easily missed term involving C1.

On V=v, the outward monster reaches every A2 characteristic because
s>=sup A2. Among ranks above the old upper front, those below D1(v)
meet the first incoming wave; those between D1(v) and D2(v) meet the
second incoming wave. This yields the two upper fronts h1 and h2.

The third leg U=s sees radial CDF D2(V). It captures exactly the low
missed ranks on the final outward leg. High ranks above h2 stay above
the monster until the final positive endpoint. Negative ranks again
capture at s+1. Thus every term of the last-wave formula has the stated
first-capture interpretation.

The inequalities l<=m<=r<=h1<=h2 follow from A1>=a, C1>=-a, and
C2>=C1. They are not additional unverified numerical conditions.

## 3. What the original fixtures covered

The existing first-wave fixtures exercise both definitions of the lower
front. The four last-wave fixtures exercise first-incoming captures,
second-incoming captures, missed high ranks, and the two lower-front
definitions.

However, in all four last-wave fixtures l=m. Thus the first-return
integral over (l,m) was always empty. This is a coverage gap rather than
an error in the formula. At the same x and s, choosing v=29/50 or v=4/5
makes that interval nonempty.

## 4. Independent exact verification

The separate script

    packages/interval_continuous_rank/research/audit_two_turn_formulas.py

does not compute payoffs using a radial CDF or running rank records.
It constructs the affine princess segments on each quantile piece,
enumerates every valid monster/princess segment intersection, splits
quantile space at all validity and candidate-order boundaries, and
integrates the earliest valid capture time exactly with rational arithmetic.

It passes:

* 22 last-wave comparisons, including five cases with a nonempty
  first-return interval;
* 20 first-wave comparisons;
* comparison with the continuous-rank engine including its stationary
  endpoint mixture, where applicable.

The companion script

    packages/interval_continuous_rank/research/audit_last_wave_stationarity.py

uses the same independent segment method to check the exact C_s, C_z,
and mixed derivative formulas in four fixed front chambers. Centered
differences there are exact identities because the payoff is quadratic
on each chamber. Its cases include both moving-front corrections, the
first-wave separation gap, and A(z)+B2(s)>1. It also checks the rational
joins, density signs, and derivative identities of the finite-last-wave
counterexample.

The hand arguments establish the general identities; these exact checks
verify the independent implementation and the additional fixture regimes.
