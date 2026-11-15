# Exact rank phases for ordered alternating-leg princess laws

## Scope

This note identifies a candidate class whose rank process has a fixed finite
number of monotonicity phases along **every** monster path. The class includes
ordered initial-outward / inward / outward paths and their five-leg extension.
The result is structural, not a numerical bound. It does not establish that an
optimal princess law belongs to the class, or by itself prove a bound on the
number of turns in an optimal monster response.

The finite rank-phase conclusion is the feature to use in an all-monster
response reduction. It is not justified for arbitrary ordered paths; the
stationary-shell counterexamples remain unaffected.

## 1. Ordered path parameters

Let the positive-half princess rank q be uniform on [0,1]. Fix an integer k.
Choose measurable functions

    a(q), A_1(q),...,A_k(q), C_1(q),...,C_k(q)

such that a and every A_j are nondecreasing in q, and every C_j is
nonincreasing in q. Assume pointwise

    0 <= a <= 1,
    a <= A_1 <= A_2 <= ... <= A_k,
    -a <= C_1 <= C_2 <= ... <= C_k.

Define, before clipping at zero or absorbing at the endpoint,

    z_0(t,q) = a(q)+t,
    z_j(t,q) = max(min(z_(j-1)(t,q), A_j(q)-t), t-C_j(q)).  (1)

Set b(t,q)=max(0,z_k(t,q)). Follow b until its first visit to one, and
remain at one afterward. Call this path p_q. The full symmetric law chooses
p_q or -p_q with equal probability.

Every leaf in (1) is 1-Lipschitz in t. Minimum, maximum, clipping, and
absorption preserve that property. The parameter inequalities give
p_q(0)=a(q). All paths stay in [0,1]. Every leaf is also nondecreasing in q,
so the paths are ordered in q at every time, including after absorption.

The alternating line intersections occur in their stated temporal order:
first at (A_1-a)/2, then (A_1+C_1)/2, then
(A_2+C_1)/2, then (A_2+C_2)/2, and so forth. Thus (1) is an ordered
2k+1-leg construction, allowing zero-length legs, zero-height waits, and
early endpoint absorption. If C_k is uniformly bounded above by Cmax,
every path is absorbed at one by time 1+Cmax.

## 2. The exact interior radial CDF

For x in [0,1), put U=t+x and V=t-x, and define the parameter distribution
functions

    D_0(V) = Pr(a <= -V),
    I_j(U) = Pr(A_j <= U),
    D_j(V) = Pr(C_j >= V).

The corresponding sets of q are initial intervals. Their lengths therefore
turn unions into maxima and intersections into minima. The parameter order
implies, at every U,V,

    D_0 <= D_1 <= ... <= D_k,
    I_1 >= I_2 >= ... >= I_k.                            (2)

In particular, a<=-V implies C_1>=-a>=V, proving the first comparison.

Let R_raw(t,x)=Pr(b(t,q)<=x). Translating (1) gives the recurrence

    R_0 = D_0,
    R_j = min(max(R_(j-1),I_j),D_j).

Distributing minimum over maximum and using (2) yields

    R_raw(t,x)
      = max{D_0(V), min(I_1(U),D_1(V)), ...,
                       min(I_k(U),D_k(V))}.             (3)

This is an equality, including parameter atoms and coincidence thresholds.
For example, the five-leg case k=2 is

    R_raw = max{D_0, min(I_1,D_1), min(I_2,D_2)}.         (4)

To account for absorption, put

    E(t)=Pr(sup_(0<=s<=t) b(s,q) < 1).

The unabsorbed ranks form an initial interval, and E is nonincreasing in
t. For x<1, an absorbed path does not belong to the CDF event. Hence

    R(t,x)=Pr(p_q(t)<=x)=min(E(t),R_raw(t,x)).             (5)

Equivalently, replace every D_j, including D_0, by min(D_j,E) in (3).
These capped functions remain nested and nonincreasing along the trajectories
used below.

For the strict CDF Pr(p_q(t)<x), when 0<x<1 use the same formulas with
a<-V, A_j<U, and C_j>V. At x=0 the strict CDF is zero; the nonstrict CDF
R(t,0) is the mass presently at zero. At x=1 the nonstrict CDF is one.
These endpoint conventions cannot be replaced by their interior formulas.

## 3. A global rank-phase bound along every monster

Let m be any 1-Lipschitz monster path, and put r(t)=abs(m(t)). This is also
1-Lipschitz. Consequently both

    U(t)=t+r(t),      V(t)=t-r(t)

are nondecreasing, even when m changes sign or reverses direction repeatedly.
Consider the radial rank R(t,r(t)) before the monster's first endpoint visit.
Each I_j(U(t)) is nondecreasing, while every capped D_j(V(t)) is
nonincreasing.

Write H_j(t)=min(I_j(t),D_j(t)). Each H_j has an increasing phase followed
by a decreasing phase. More is true: the ordering in (2) prevents the upper
envelope of the humps from switching backward between them.

For i<j, if D_i>=I_j, then

    H_i >= I_j >= H_j.

If D_i<=I_j, then

    H_i <= D_i <= H_j.

The first comparison follows from I_i>=I_j, and the second from D_j>=D_i.
Thus the dominance of H_i over H_j changes only when the decreasing D_i
passes the increasing I_j. It cannot change back. The initial term D_0
also cannot regain dominance once I_1 passes it, because D_0 decreases,
I_1 increases, and D_1>=D_0.

It follows that (3) can be partitioned into at most 2k+1 successive
monotonicity phases of the form

    decreasing, increasing, decreasing, ..., increasing, decreasing. (6)

Some phases may be empty; plateaus and coincident switches are permitted.
The absorbing cap E preserves every comparison used in the argument.
The same conclusion holds for the strict interior radial CDF.

**Theorem.** For the ordered law (1), the radial rank of every admissible
monster, before its first endpoint visit, has at most 2k local extrema in
the sense of the monotone decomposition (6). In particular:

* three alternating legs give at most two radial-rank extrema;
* five alternating legs give at most four radial-rank extrema.

The assertion bounds rank phases, not physical turns of the monster. Turning
can occur inside a single phase, and at center atoms the full signed CDF has
different left and right values. An all-monster capture-order theorem must
still show that those motions can be replaced without increasing expected
capture time.

## 4. Relation to the proposed continuum response family

The corrected princess response to the M1/M2 law has characteristic vertices

    (a,-a) -> (u,-a) -> (u,c) -> (1+epsilon,c)
       -> (1+epsilon,y) -> endpoint,

with the optional center wait when c exceeds u. It is an instance of (1)
with

    A_1=u, C_1=c, A_2=1+epsilon, C_2=y,

provided the parameters can be ordered so that a,u increase with rank and
c,y decrease with rank. This ordering is a substantive condition on a
candidate mixture, not an automatic consequence of having five legs.

The free endpoint-start suffix can therefore spread the time-one locations
while retaining the rank-phase bound. In contrast, arbitrary quantile
rearrangement of unordered five-leg paths can introduce many extra physical
legs. One must verify the ordered parameter representation itself.

The next required theorem is to turn the finite rank-phase structure into
an exact finite-parameter monster-response reduction, including center atoms
and endpoint continuation. After that, a matching candidate law still has
to be found and checked. Neither (3) nor (6) identifies the game value.
