# Complete terminal-center gates and fixed-tail start reduction

Date: 2026-11-12 UTC.

The unrestricted interval game is still open. This checkpoint closes complete
center-state regions for the supplied field and removes a continuous initial
parameter from each fixed Monster tail. The numerical strategy exchange is
preserved with its physical paths and exact payoff inputs; its finite master
values are not game values.

## 1. Three exact center results

Use the frozen field with blob
5c45d042ee9948faebc03354c3e1e2ee3cbec1a5, and the notation of
[CENTER_RANK_REMOVAL_AND_EXTERIOR.md](../10-turn-density/CENTER_RANK_REMOVAL_AND_EXTERIOR.md).
Put \(a=7/8,\ b=15/16\), and
\[
R(U,V)=kU-\ell V+c,\qquad Z(t)=(k-\ell)t+c
\]
on the affine wedge. The exact constants are
\[
k=\frac{655898601421}{62500000000},\qquad
\ell=\frac{820954217}{12500000000},\qquad
c=-\frac{71289950193}{7812500000}.
\]
Let \(W(t,n)=V(t,n)+T_t(n)/2\) be the transformed balanced center value,
and let \(E_W(t,n)\) be the actual immediate exterior envelope: every
post-\(b\) return and the direct endpoint tour are included.

First, the front lower certificate
\[
B(t)=C_*+\frac c2t\le W(t,Z(t))
\]
now holds on the entire interval \(a\le t\le b\), with equality on
\(a\le t\le\tau\). Here \(C_*\) and \(\tau\) are the exact quadratic-field
constants in the earlier Zeno attachment. The extension from source
\((57/64,Z(57/64))\) to \((7/8,0)\) was checked on the full reachable domain.

Second, every immediate exterior alternative from every front state
\(t\in[a,b]\) is no better than the return at \(b\):
\[
E_W(t,Z(t))=W_b(t,Z(t)).
\]
This is a complete continuous-parameter comparison. It does not assert that
internal returns are always inferior; the attaining Zeno chain improves
the immediate exterior action on the earlier part of the slab.

Third, define the rational threshold
\[
t_L=b-\frac{6\ell}{k-2\ell}
=\frac{9321277864605}{10363024948016}.
\]
On the entire late slab,
\[
\boxed{W(t,n)=E_W(t,n),\qquad
t_L\le t\le b,\quad Z(t)\le n\le1.}
\]
The proof checks the complete last-two-action comparison against the direct
\(b\) return, reduces the initial-rank parameter by monotonicity, and verifies
productive waits through the front quantity
\(E_W(t,Z(t))-ct/2\). Empty actions, closed endpoint captures and nonproductive
exterior returns are retained. Uniform quantile-record approximation handles
arbitrary later turns and accumulating returns.

The late packet contains 207 front-exterior regions, 130 last-two regions,
343 independent primitive checks in total, 45 physical capture identities
and 24 rank-monotonicity comparisons. Its stationary and boundary checks
are exact. See [CENTER_LATE_EXTERIOR.md](../10-turn-density/CENTER_LATE_EXTERIOR.md).

## 2. Rank removal fills the earlier high-record region

For \(q_b=Z(b)\), the supplied field has the full future barrier
\(R(U,V)\le q_b\) at interior points with \(V\ge b\). If an initial surviving
rank is \(n\ge Z(t)\), any continuation whose first productive center action
occurs by \(b\) has transformed cost at least
\[
L_B(t,n)=B(t)-\frac12\bigl[b(n-Z(t))+(n-q_b)_+\bigr].
\]
The argument compares the same continuation before and after removing the
two reflected copies of the rank band. A first productive wait is handled
separately by an inserted tent, rather than being silently treated as a
return.

Consequently
\[
\min\{E_W(t,n),L_B(t,n)\}\le W(t,n)\le E_W(t,n).
\]
The difference \(E_W-L_B\) is nonincreasing in \(n\). The explicit return
at time one gives \(W_1(t,n)=J(t)-n\), and hence the threshold
\[
n_{\rm crit}(t)
=\frac{J(t)-C_*-[ct+bZ(t)]/2}{1-b/2}.
\]
The exact polynomial \(J\) is recorded in the source note. The interval
checks extend through \(t_L\):
\[
Z(t)<n_{\rm crit}(t)<q_b,\qquad
R(t,0)>n_{\rm crit}(t),\qquad a\le t\le t_L.
\]
It follows that
\[
\boxed{W(t,n)=E_W(t,n),\qquad
a\le t\le t_L,\quad n_{\rm crit}(t)\le n\le1.}
\]
This joins the late all-record result. It does not require solving the
individual front-count transitions between \(\tau\) and \(t_L\).
The incidental inequality \(B>3/2\) holds on the earlier equality interval;
it is not extended to \(t_L\).

## 3. The complete low-record first-arrival gate

For any positive-side prefix from initial position \(a_0\), with first center
time \(t\) and maximal captured radial record \(n\), the optimized total cost
is exactly
\[
W(t,n)+\frac12\int_0^n\tau_q^+\,dq.
\]
This identity permits arbitrary speeds, arbitrary numbers of same-side
turns and limits of such paths.

A lower bound for the positive capture moment can be obtained by bounding
its captured rank area. If \(J(a_0,t,n)=tn-\operatorname{Area}(a_0,t,n)\)
uses a valid upper envelope of captured area, then
\(J(N)-J(n)\le t(N-n)\). Rank removal gives
\[
W(t,n)\ge W(t,N)+\frac12\int_n^N\beta_t(q)\,dq,\qquad \beta_t(q)\ge t.
\]
Thus the record can be lifted to an already certified center state without
assuming that a particular finite-turn prefix is exhaustive.

The independent fastest-ray moment is too weak on part of this interval.
The stronger shared-travel-budget area envelope now has a complete exact
certificate. Every same-side prefix whose FIRST center arrival is
t in [7/8,t_L] and whose captured rank is at most ncrit(t) has optimally
continued total cost at least 7131/5000 = 1.4262.

The saved replay checks all 874 accepted boxes and a separate 22-slab
coverage sweep. It passes 12,385 logical, cone, rank and coverage checks,
3,061,252 rational envelope comparisons, 7,542 complete-exterior
identities, and 108 independent physical-prefix moment comparisons.
The smallest exact enclosure is approximately 1.4262008472927297,
strictly above the stated exclusion target.

See [SAME_SIDE_PREFIX_SHARED_BUDGET.md](../10-turn-density/SAME_SIDE_PREFIX_SHARED_BUDGET.md).
This closes low-record FIRST arrivals in the slab. Higher records already
have the exact exterior continuation, as do all records from t_L onward.
Low-record INTERMEDIATE center states reached after earlier center visits
do not acquire the initial-prefix moment used here, so this exclusion
cannot be transplanted to them. Earlier center waves before 7/8 and
their attachment to those states remain to be resolved.

## 4. A finite initial-start theorem for every fixed tail

Fix a Monster's first direction \(d\in\{-1,1\}\), its outgoing characteristic
\(c=t+d\,x\) at the first reversal, and its later physical tail. In oriented
coordinates \(y=d\,x,\ b_0=d\,a_0\), the initial two legs are
\[
y_{b_0}(t)=\min(b_0+t,c-t).
\]
If the next fixed tail vertex is at time \(t_2\), legality is exactly
\[
\max(-1,c-2t_2)\le b_0\le\min(1,c,2-c).
\]

Between successive actual Princess initial positions, increasing \(b_0\)
cannot increase capture time: initially ahead paths meet the pointwise
higher initial tent no later; initially behind paths first meet its common
returning branch. At an initial atom, exact time-zero contact supplies the
lower trace. Therefore the best start for this fixed tail occurs at an
actual initial support point or a legality boundary. The theorem holds
for actual rational germs, and for the implicit comonotone law.

This is a fixed-tail theorem, not a global bound on the number of turns.
The executable separator initially tested all same-limit substitutions
and legality boundaries of 345 supplied tails. Its 2,363 exact candidates
rejected the pinned M1-repaired mixture. The new attack starts at
\(3/16-\epsilon\), turns on \(U=1\), then visits \(-1\) at time two and
\(+1\) at time four. Its cost is exactly
\[
\frac{57919504145512204712631367442479}
     {41215599999999996741371017200000}
=1.405281110684115\ldots.
\]
This is a response to that particular mixture, not a game upper bound.
See [FIXED_TAIL_INITIAL_REDUCTION.md](FIXED_TAIL_INITIAL_REDUCTION.md).

## 5. Recoverable coupled search

The known certified 169-pair Princess strategy is now included as a source.
Its full 48,228-state response certificate was independently replayed.
The old 159 physical paths are retained unchanged; new upper responses
are additional paths. Both germ and separately collapsed Monster attacks
are retained as distinct columns.

The complete M1 start universe was generated for all frozen paths, including
zero-weight rows. For the 332-row checkpoint this gives 756 oriented starts,
378 reflection classes and 40 additional collapsed companions. Every future
probability vector on those paths is covered. Newly added paths receive
their initial M1 columns immediately.

The preserved later checkpoint contains 349 physical pairs and 1,465 Monster
atoms, with this complete M1 coverage. Its numerical finite-master value is
about 1.4193714116482343. This number is not an unrestricted lower guarantee.
A short full capture-order run on an earlier iterate was unfinished and is
explicitly recorded as such. The fixed-tail attack above was incorporated
before the preserved later checkpoint.

The repository includes the exact compressed base geometry, new paths and
atoms, probability weights, identities and an independently replayed restore
script. The full 332-row all-M1 matrix and fixed-tail rejection matrix are
also preserved. All matrix entries are raw physical-pair capture payoffs;
the higher comonotone-law scores are kept separate.

The current global exact bounds are unchanged. No matching unrestricted
saddle, exact game value, Lean compilation or CI result is claimed.

## 6. Reproduction

From the repository root:

    node packages/interval_turn_sheet/verify_center_rank_removal.cjs > /tmp/center_rank.json
    node packages/interval_turn_sheet/verify_center_late_exterior.cjs > /tmp/center_late.json
    node packages/interval_turn_sheet/verify_shared_prefix_budget.cjs > /tmp/shared_prefix.json

Restore the current frozen geometry and weights:

    python packages/interval_global_closure/rebuild_frozen_checkpoint.py \
      packages/interval_global_closure/snapshots/frozen349_checkpoint_delta.json.gz.b64 \
      . /tmp/frozen349

The output contains rows.json, bank.json, master.json and a checked identity
report. The upper and lower workers accept these literal strategy files;
their notes distinguish numerical discovery from completed exact response
certificates. The source manifest and unpacker preserve the earlier pinned
rejection instance independently.
