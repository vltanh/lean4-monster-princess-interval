# Causal preservation under an incoming-field change

The corrected incoming-band construction has a stronger preservation
property than a one-turn calculation: it cannot improve **any** monster
path whose absolute starting position is sufficiently large. Arbitrary
speeds, waits, returns, and center crossings are included. The statement
compares two supplied laws; it does not assert that either law is already
an equilibrium or satisfies every monster inequality.

## 1. A general high-start comparison

Let `p_old(q,t)` and `p_new(q,t)` be ordered radial quantile paths for two
reflected princess laws, coupled by rank q. Suppose the following hold,
outside one common null set of ranks:

1. Initial positions agree, and `p_new(q,t)<=p_old(q,t)` for every t.
2. There is qhi such that every rank q>qhi has its entire path unchanged.
3. For some a0, all possibly changed ranks start at or below a0:
   `A(a0)>=qhi`, where A is the common closed initial CDF.
4. The full radial fields agree throughout the outgoing cone
   `V=t-radius>=a0`, including the applicable endpoint and center traces.

Then, for **every** continuous monster path m with speed at most one and
`m(0)>=a0`,

    E[tau_new(m)] >= E[tau_old(m)].                  (1)

The same holds for `m(0)<=-a0` by reflection. There is no restriction on
the number or location of turns and no assumption that the monster law
or the tested path is active.

### Positive-copy proof

Every possibly changed positive path starts below the monster. If it
starts exactly at the monster, both first captures occur at time zero.
Otherwise, before its old first capture, continuity gives

    m(t)>p_old(q,t)>=p_new(q,t).

Thus the new positive copy cannot be captured earlier. This argument
holds for an arbitrary fixed monster curve, even after it changes
direction. The unchanged higher ranks need no comparison.

### Reflected-copy proof

At any possible reflected contact,

    m(t)=-p(q,t),       V_p=t-p(q,t)=t+m(t)>=m(0)>=a0, (2)

where the inequality is the monster speed bound. Thus the monster can
meet a reflected path only inside the unchanged outgoing cone.

The first-capture sets really are the same there. At fixed t, put
`c=t-a0`. The radial CDFs agree for radii at most c. Their quantiles
therefore agree whenever either quantile lies in that interval: if a
new quantile were smaller than the old one inside it, equality of the
CDFs at that smaller radius would give the opposite quantile inequality.
The reverse implication is identical. Equation (2) then proves that an
old reflected contact is a new contact at the same time, and conversely.
Their first capture times are exactly equal. Adding the two reflected
copies proves (1), including infinite expectations.

For CDF-defined laws, choose quantile versions on rational times and
discard the common exceptional rank set. The speed bounds extend the
quantile comparisons to every time by continuity. This avoids an
implicit convention at CDF plateaus.

## 2. The corrected rank-band construction satisfies the hypotheses

For a band `[qlo,qhi]`, define

    h(r)=min(max(r-qlo,0),qhi-qlo).

Let psi be increasing with `U<=psi(U)<=1` before U=1, and identity
afterward. Replace its CDF contribution by

    h(min(A(U),R_old(psi(U),V)))                     (3)

for U<1, using the unmodified contribution for U>=1. The initial-front
cap in (3) is essential on a bridge where A(U)<qhi. Every legal old
field satisfies `R_old(U,V)<=A(U)` on U<1. Consequently the replacement
is at least h(R_old(U,V)), is increasing in U and decreasing in V, and
equals the old initial contribution at V=-U. Summing disjoint bands
therefore gives a legal ordered CDF with

    R_new>=R_old,       A_new=A_old.                 (4)

The resulting quantile paths satisfy `p_new<=p_old`. Independently moved
bands may cross and reorder lower ranks, so it is **not** correct to
say that only ranks in the named band intervals change. What is true is
that, if qhi is the largest upper band endpoint,

    R_new=R_old wherever R_old>=qhi,
    R_new<=qhi wherever R_old<=qhi.                  (5)

Hence no quantile above qhi changes. This is exactly the rank restriction
needed in Section 1.

For the selected two-band field the bands are

    [1/2,17/20] and [17/20,113/125].

The exact initial gate at `a0=255/256` is

    A(a0)-113/125 = 14234999841/19531250000000 > 0.

The outgoing gate is `R_old(1,a0)<1/2`. Before U=1, any point with
V>=a0 has

    R_old(psi(U),V)<=R_old(1,V)<=R_old(1,a0)<1/2.

Both changed band contributions vanish there. The post-U=1 field is
unchanged by definition. Thus the entire outgoing cone in Section 1
agrees, not merely one prescribed second-turn row. The corrected
construction therefore preserves or raises every monster cost with
absolute initial position at least 255/256.

## 3. Free-second-turn and continuation consequences

In particular, all costs of the legal same-half initial-inward routes

    +a -> inward V=v -> outward U=s -> -1 -> +1,

with

    a>=255/256,       -a<=v<a,       a<=s<=2+v,

are nondecreasing. The second turn may be before U=1, at U=1, strictly
after it, or the positive endpoint. No ordinary incoming cap is used.
The reflected first inverses beta(s) remain unchanged because s>=a lies
in the unchanged outgoing cone; the general causal proof explains why
the conclusion extends much further than these particular routes.

The all-return gates in `POSTONE_SAME_HALF_GATE.md` are also preserved
throughout the larger terminal prefix domain `0<=x<=y<=1/128`. Indeed,
with the upper band endpoint 113/125,

    D_new>=min(D_old,12/125),
    r_new=r_old,       e_new=e_old.

The old certificate gives `D_old>=(19/10)min(r_old,e_old)`, while
`(19/10)e_old(1/128)<12/125`. Therefore the new field satisfies the same
rank gate at every point, including between the old mesh nodes. Its
post-boundary gates are unchanged. This is an analytic preservation
statement for the unmeshed field, not a claim based on a new mesh.

These comparisons preserve every previously proved lower inequality in
the stated regions. They do not manufacture a proof of the old
inequalities and do not cover smaller initial starts automatically.

## 4. The explicit lower-start coupling

For any fixed positive start `a<1`, the initial CDF is
unchanged, all U>=1 rows are unchanged, and the incoming changes are
confined to the pre-one part of its outward column. The exact positive
M1 and fixed-U=1 M2 formulas then give

    4(Cf_new(a)-Cf_old(a))
      =4(Cg_new(a)-Cg_old(a))
      =-integral_a^1 [R_new(U,-a)-R_old(U,-a)]dU.     (6)

Thus these costs can decrease. If a previously active column is
affected, the outer lower law must be adjusted jointly. This is the
concrete missing compatibility condition for the current local repair,
not a failure of its transport or high-start preservation.

The portable column audit records numerical integrals of (6), exact
base costs, and comparison with the selected field evaluator. Its
reported quadrature errors are numerical estimates, not certified
interval bounds. The local construction is not presented as a game
bound or a matching law.

There is a separate exact incompatibility certificate in
`packages/interval_cdf_discovery/verify_warp_outer_column.py`. It brackets
one algebraic inverse by rational B/T inequalities and obtains a positive
rectangular lower bound on the column integral at `a=5/8`. Exact base
fractions then put both corrected costs strictly below the endpoint
target. No quadrature estimate is needed for this strict conclusion.
For `a>=255/256`, the column change in (6) is zero: its old CDF is at
least A(a), which already exceeds the largest moved rank.

## 5. Independent exact capture fixtures

Run

```sh
python -B packages/interval_turn_density/verify_incoming_warp_preservation.py
```

The verifier compares direct rational first intersections for both
copies, retaining monster waits, endpoint turns, and repeated center
crossings. A second fixture actually reorders two lower paths after
moving one of them, so the test does not silently preserve invalid
rank-band labels. Every reflected first capture is unchanged and every
positive first capture is no earlier, in agreement with the continuous
proof above.
