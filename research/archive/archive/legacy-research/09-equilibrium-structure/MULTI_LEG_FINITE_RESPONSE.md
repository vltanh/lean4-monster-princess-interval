# A finite all-monster response theorem for ordered multi-leg laws

## 1. Statement and precise scope

Use the ordered alternating-leg law from
`ORDERED_MULTI_LEG_CDF.md`, with k inward legs and k+1 outward
legs. For clarity, its positive paths are formed from

    z_0(t,q)=a(q)+t,
    z_j(t,q)=max(min(z_(j-1)(t,q),A_j(q)-t),t-C_j(q)),

by clipping below at zero and absorbing at the first visit to one. Reflect
the paths with probability one half. Assume the following:

* a and every A_j are strictly increasing and continuous in q;
* every C_j is strictly decreasing and continuous in q;
* `0<=a<=1`, `a<=A_1<=...<=A_k`, and
  `-a<=C_1<=...<=C_k<=1`.

Thus the paths are strictly ordered at interior positive positions, may
have atoms waiting at zero, and are fixed at their signed endpoints from
time two onward.

Put

    I_j(v)=Pr(A_j(q)<=v),      D_j(v)=Pr(C_j(q)>=v).

Let E(t) be the proportion of positive paths not yet absorbed at one.
Define the capped center tails `d_j(t)=min(D_j(t),E(t))` and let tau_j be
the first time `I_j(t)>=d_j(t)`. The monotonicity hypotheses imply

    0=tau_0 <= tau_1 <= ... <= tau_k <= 1.

For each nonempty stage `(tau_(j-1),tau_j)`, assume I_j is absolutely
continuous, with density b_j. Assume there is a fixed partition of that
stage with J_j internal breakpoints such that on every partition piece
and every contained subinterval `[s,e]`,

    integral_s^e (s+2e-3v)b_j(v)dv >= 0.                 (K_j)

This is a hypothesis about the given law, independent of the monster.
It holds, for example, on a piece where b_j is zero, nonnegative concave,
or bounded between positive m and M with M<=4m. See
`CENTER_RETURN_REDUCTION.md` for the elementary sign proofs.

**Theorem.** Against this law the unrestricted monster-response infimum
equals the infimum over the following finite-dimensional class:

1. an initial unit-speed same-half prefix with at most 2k useful capture
   turns, allowing one additional terminal joining turn, ending at zero
   or at an endpoint;
2. if it ends at zero, at most

       N = sum_j J_j + 3k

   unit-speed zero-return triangles, each with either sign, separated by
   waits at zero;
3. a direct run from the last zero to one endpoint followed by a sweep to
   the other, or a direct sweep from the first endpoint to the other.

All these paths may be taken to finish by time six. The discrete sign words
are finite, and each word has finitely many real position/time parameters.
Waits at zero are explicitly permitted: replacing many small excursions by
a wait does not preserve a purely unit-speed path class.

For five alternating princess legs, k=2 and the bound is
`N=J_1+J_2+6`. The bound is deliberately not claimed sharp.

This theorem controls every monster for a specified law satisfying the
hypotheses. It does not prove that the unrestricted game has an equilibrium
inside this class, identify the density functions, or determine the value.

## 2. The radial CDF and ordered center peaks

For `0<=x<1`, set `U=t+x`, `V=t-x`, and

    D_0(V)=Pr(a(q)<=-V),
    H_j(U,V,t)=min(I_j(U),D_j(V),E(t)).

The exact radial CDF is

    R(t,x)=max{min(D_0(V),E(t)),H_1,...,H_k}.             (1)

This follows by distributing the min/max recurrence in the cited CDF note.
The nested parameter functions give

    I_1>=I_2>=...>=I_k,
    D_0<=D_1<=...<=D_k.

Along any monster, both `t+abs(m(t))` and `t-abs(m(t))` are nondecreasing.
Consequently the radial rank has at most 2k reversals, even for a monster
with arbitrarily many physical turns. This gives the initial same-half
capture-turn bound; it does not alone control returns through a center atom.

At the center, D_0(t)=0, and the j-th hump is

    H_j(t,t,t)=min(I_j(t),d_j(t)).

I_j increases and d_j decreases, so tau_j separates its incoming and
outgoing phases. The nesting shows `tau_j<=tau_(j+1)`: once
`I_(j+1)>=d_(j+1)`, one also has `I_j>=d_j`.
The final bound tau_k<=1 uses C_k<=1 and strict monotonicity, which give
D_k(1)=0. Empty stages and flat equality intervals cause no difficulty.

## 3. What can be newly captured in a zero-return cone

A zero-to-zero path on `[s,e]` satisfies, throughout that interval,

    s <= V(t) <= U(t) <= e.

Suppose the entire interval lies in stage j,
`[s,e] subset [tau_(j-1),tau_j]`. At time s, both reflected radial prefixes
through R(s,0) have already been captured by the zero visit.

For every older hump i<j, the stage ordering gives s>=tau_i. Thus

    H_i(U,V,t)
      <= min(D_i(V),E(t))
      <= min(D_i(s),E(s))
       = H_i(s,s,s)
      <= R(s,0).                                        (2)

Older waves therefore contain no new rank in the cone.

The current hump is exactly incoming, because

    I_j(U) <= I_j(e) <= min(D_j(e),E(e))
                       <= min(D_j(V),E(t)).              (3)

Every later hump is at most I_j(U), since I_l<=I_j for l>j. D_0 is zero
when V>=s>=0. Combining (1)-(3) proves the key reachable-state statement:

    every rank in this cone above the already captured frontiers
    is determined exactly by I_j(U).                    (4)

Unlike a claim only about the original route, this holds for every legal
replacement path between the same zero endpoints.

For s>=tau_k all humps are older, so the same argument shows that a
zero-return excursion after the last center peak captures nothing new.

## 4. Normalizing excursions and handling initial asymmetry

For a finite midpoint-quantile sample, use the capture-order domination
theorem to obtain a canonical monster. Before its first zero or endpoint,
strict interior ordering and the 2k radial-rank bound permit at most 2k
useful capture turns.

After a zero visit, a same-half zero-return excursion can be replaced by
its maximal tent `min(t-s,e-t)` without delaying any capture in that half.
Uncaptured paths start strictly on the outer side of the monster, and the
larger radial path crosses them no later. Opposite-side captures occur only
at the zero junctions. If the tent reaches an endpoint, finish by sweeping
directly to the other endpoint; the old same-half excursion could not
capture an opposite-side path before its return to zero. Hence retained
pre-endpoint excursions are triangles.

Work within one peak stage j. At its first relevant zero visit let the
captured frontiers be r_+,r_-, and put M=max(r_+,r_-). For all complete
triangles ending while I_j(e)<=M, the larger frontier is already beyond
every new rank accessible in the cone. These triangles can only improve
the deficient side. Merge them into one maximal triangle on that side
over their combined interval: it crosses every newly captured deficient-side
path no later and returns to the same final zero. The other side loses no
new capture. This costs at most one exceptional triangle.

At most one more triangle can cross the balance threshold

    I_j(s)<M<I_j(e).

At its end, both captured frontiers equal I_j(e): older waves are below
the previous frontiers by (2), and every new radial rank through I_j(e)
is present at the center by (3). Subsequent zero visits in that stage are
balanced, with frontiers exactly I_j(t). If the two initial frontiers are
equal but still larger than I_j(s), this remains in the pre-balance case;
one must not apply the fresh-arrival formula until I_j has reached that
already captured frontier. Thus each stage needs at most two asymmetry
exceptions.

This is the same initial-frontier argument as in the three-leg theorem,
with (4) replacing the exact single-wave formula. It does not assume that
the surviving law is symmetric after an arbitrary monster history.

## 5. Balanced triangles and the finite count

For a balanced triangle `[s,e]` in stage j, a fresh radial label has
arrival characteristic `v=A_j(q)` in `(s,e]`. Its capture time on the
excursion side is `(s+v)/2`, and its reflection is caught at the return
time e. Waiting at zero instead captures both at time v. Their average
cost difference, integrated over the incoming labels, is

    (1/4) integral_s^e (s+2e-3v)b_j(v)dv.                (5)

At time e both alternatives have exactly the same frontiers I_j(e), so
no future cost is hidden in this comparison. The identities follow from
(4), even if the paths have earlier or later inward waves.

Condition (K_j) removes every such triangle contained in one density
piece. Each retained balanced triangle must contain a partition breakpoint
in `(s,e]`. The triangle intervals are disjoint, so stage j retains at
most J_j balanced triangles, in addition to its two exceptions.

A triangle not contained in one peak stage must straddle at least one of
the k peak times tau_1,...,tau_k. Disjoint triangle intervals give at most
k of these. Returns after the last peak have already been removed. The
total is therefore at most

    sum_j (J_j+2) + k = sum_j J_j+3k.

The last zero is followed by direct outward travel and an endpoint sweep.
It captures every path caught by the previous same-half final prefix no
later, and then captures all remaining paths on the other side.

## 6. Full-payoff continuum transfer

Use an even n of midpoint quantiles so no sample lies at the central
rank boundary. For any proposed monster m, extend it after time six, if
necessary, to capture every selected princess. Canonical domination gives
a finite-sample response m_n capturing each sampled path no later.

All selected princesses are fixed at endpoints by time two. Consequently
the last useful interior turn of m_n is by time two, the next endpoint
is reached by four, and the opposite endpoint by six. If all sample paths
are caught earlier, append these endpoint sweeps. Hence, separately from
domination, every sampled capture time of m_n is at most six. Combining
the two inequalities gives

    T(m_n,p_i) <= min(T(m,p_i),6).

Apply the preceding replacements using the original continuum law, not
an empirical density. They produce b_n in the finite class with
`J(b_n)<=J(m_n)` and with the same uniform endpoint-completion horizon.
The uniform midpoint-quantile error for truncation at six is at most 6/n.
Therefore

    inf_b J(b) <= J(b_n) <= J(m_n)
      <= J_(6,n)(m_n)+6/n
      <= J_(6,n)(m)+6/n
      <= J_6(m)+12/n
      <= J(m)+12/n.

Let n increase through the even integers and take the infimum over m.
The reverse inequality follows from inclusion of the finite class in
the legal monster class. This proves the full-payoff equality claimed
in Section 1, without truncating the original game by assumption.

## 7. Candidate compatibility and the remaining equilibrium step

The corrected M1/M2 response family has the five-leg parameters

    A_1=u, C_1=c, A_2=1+epsilon, C_2=y.

An ordered mixture can fit the present class when a,u increase and c,y
decrease with rank. The theorem as stated requires strict continuous
parameter functions and the density condition on every incoming peak
stage. A constant A_2 violates the strict-parameter hypothesis and is not
silently included. It may be replaced by an explicitly specified strict
regularization in a candidate family. For example, if
`A_2(q)=1+epsilon+epsilon^2 q`, its entire incoming characteristic lies
above one, so I_2 is identically zero on its center-peak stage and satisfies
the local density condition trivially. The other ordering conditions,
density pieces, and all response bounds still have to be checked for the
actual law. No uniform lower guarantee follows merely by taking a singular
limit.

The new result makes the lower response check a finite-dimensional problem
for this broad class, including center waits and several inward waves.
It still does not provide an optimal law, a matching upper strategy, or
an exact value for the unrestricted game.
