# Complete short-hinge deletion for finite off-front terminal renewal chains

Date: 2026-11-12. This note closes the remaining **strict short-hinge
branches** of the finite productive center-renewal problem on the saved
affine terminal wedge. The theorem is conditional on the previously
proved physical transport/inverse gates. It is **not** a new global
Princess–Monster game bound, and it does not solve the no-hinge
two-source count-selection or exterior attachment problem.

## 1. Setup and exact scope

On the saved field's terminal wedge
\[
7/8\le V\le U\le b=15/16,\qquad
R(U,V)=kU-\ell V+c,\quad
k=\frac{655898601421}{62500000000},\quad
\ell=\frac{820954217}{12500000000},
\]
put \(d=k-\ell\), \(Z(t)=dt+c\) and \(A=k/8-\ell/2\).
Here \(0<\ell/k<1/8\), \(0<H=b-t\le1/16\), and the
closed endpoint/inverse gates of
[AFFINE_CENTER_CHAIN_IDENTITIES.md](../10-turn-density/AFFINE_CENTER_CHAIN_IDENTITIES.md)
hold.

Start at balanced center rank \(Z(t)+y\), \(y\ge0\).
An \(m\)-return productive fixed-\(b\) chain consists of positive
\(h_1,\ldots,h_m\) with \(\sum h_j=H\) and
\[
k h_1\ge y,\qquad
k h_j\ge \ell h_{j-1}\quad(2\le j\le m).                 \tag{1}
\]
Its **complete**, terminal-jump-aware excess energy is
\[
\begin{split}
E_y(h)={}&A\sum_jh_j^2-\frac\ell2\sum_{j<m}h_jh_{j+1}
 -\frac{3\ell}2h_m-\frac y2h_1-\frac{y^2}{8k}\\
 &-\frac{(y-dh_1)_+^2}{8k}
 -\sum_{j=2}^{m-1}\frac{(\ell h_{j-1}-dh_j)_+^2}{8k}
 -\frac{(\ell h_{m-1}-dh_m)_+}{2}.                     \tag{2}
\end{split}
\]
The final term is omitted for \(m=1\).
Formula (2) is imported from the already independently checked
[INFINITE_TURN_RENEWAL.md](INFINITE_TURN_RENEWAL.md).

Call the **initial hinge** active when \(y>dh_1\);
an **interior hinge** at \(2\le j<m\) active when
\(\ell h_{j-1}>dh_j\);
and the **terminal hinge** active when
\(\ell h_{m-1}>dh_m\).
The preceding
[HIGH_SURPLUS_SINGLE_RETURN.md](HIGH_SURPLUS_SINGLE_RETURN.md)
already deletes the terminal hinge for every \(y\), with an exact
strict cost decrease. We now delete the initial and *all* interior
hinges as well, uniformly in the number of returns.

## 2. The forward short-source merger

**Theorem 1 (an arbitrary later balanced continuation is allowed).**
Suppose two productive maximal center tents have durations \(p,q>0\),
starting at center time \(s\) with balanced rank \(Z(s)+Y\), and
\[
dp<Y\le kp,\qquad kq\ge\ell p.                         \tag{3}
\]
Let \(e=s+p+q<b\). Assume the old lower rank band has its
true outgoing inverse in the affine wedge at \(e\), and the actual
post-\(e\) inverse on the added upper band is bounded below by the
affine inverse, exactly as in
[AFFINE_CENTER_OFFFRONT_TRANSFER.md](../10-turn-density/AFFINE_CENTER_OFFFRONT_TRANSFER.md)
Section 3.

Replace the two tents by the **one** maximal tent from \(s\) to \(e\),
and compare the ensuing *genuine* balanced continuation, without
requiring any later old tent to remain productive after the replacement.
For every fixed future center policy, or after optimizing that policy,
the new total expected first-capture contribution is smaller by at least
\[
\boxed{\frac{k p q}{4}>0.}                             \tag{4}
\]

### Independent algebraic proof and the inverse gate

The old first and second return ranks and the new return rank are
\[
N_1=Z(s)+kp,\quad
N_2=Z(s+p)+kq,\quad
\widehat N=Z(s)+k(p+q)=N_2+\ell p.
\]
Let \(g=Y-dp\in(0,\ell p]\), \(P=\ell p\). The original two
first-inverse moments are \(T_s,T_{s+p}\), with an outgoing record at
\(e\). The strengthened future-rank comparison
\[
C_{\rm future}(e,\widehat N)-C_{\rm future}(e,N_2)
\le-\int_{N_2}^{\widehat N}\beta_e(v)\,dv               \tag{5}
\]
holds for **the same** future policy: ranks removed from both balanced
survivor tails would otherwise require captures no earlier than
\(\beta_e(v)\) on each reflected sign. Equation (5) is equally valid
after taking an infimum over continuations; it must not be replaced by
continuity of hitting times.

Write \(\Delta=\) merged total cost minus original total cost.
Expanding the two renewal kernels, inserting (5), and retaining the
actual exterior inverse lower bound gives
\[
\begin{split}
2\Delta\ \le{}&
-\frac{kpq}{2}-gq-\frac{\ell^2pq}{2k}\\
&+\frac{g^2-P^2+(P-dq)_+^2-(g-dq)_+^2}{4k}.            \tag{6}
\end{split}
\]
This can also be checked independently by expanding
\(T_v(w)=vw+(w-Z(v))_+^2/(4k)\) on its **declared valid bands**.
The exterior values on the added band are not silently replaced by
an equality with this affine expression.

For \(a>0\), \(f(z)=(z-a)_+^2-z^2\) is nonincreasing on \(z\ge0\):
its slopes are \(-2z\) for \(z<a\) and \(-2a\) for \(z>a\).
Because \(0\le g\le P\), the bracket in (6) is
\(f(P)-f(g)\le0\).
Consequently \(2\Delta\le-kpq/2\), proving (4).

For a productive **original** chain, this lemma applies automatically
whenever its short action is \(h_j\) with \(j\le m-2\).
Indeed put \(p=h_j,q=h_{j+1}\), let \(r=h_{j+2}>0\),
and \(Y=y\) for \(j=1\) or \(\ell h_{j-1}\) for \(j\ge2\).
At the second return,
\[
N_1-Z(e)=\ell p-dq\le\ell q\le kr,\qquad e+r\le b.
\]
Thus every old lower-band inverse needed at \(e\) lies inside the
remaining affine wedge, even if it extends past the second return.
The exterior lower bound
\(\beta_e\ge\beta_e^{\rm aff}\) for the *added* band is
already checked for the saved field by the global polygonal inequality
\(R_{\rm actual}\le R_{\rm affine}\), including the endpoint jump.
The new tent is geometrically legal because all three times lie
in \([7/8,b]\) and \(H\le1/16\).

**Important:** After merging, a subsequent tent may become
nonproductive. Formula (2) cannot simply be reapplied to the
resulting duration word. The comparison (5)--(6) works with actual
capture records and is the reason the merger is valid in that case.

## 3. A short penultimate return: the true terminal jump

If the short action is **penultimate** (\(j=m-1\)),
there is no third return to supply the affine-inverse gate at the
second return \(e=b\). The terminal moment is instead
\(T_b(w)=bw+(w-Z(b))_+\). We compare (2) directly.

Put \(p=h_{m-1},q=h_m,H=\sum h_i\le2\) and
\(B=k/4-\ell/2\).

### Case \(m=2\): the first-source hinge

Let \(Y=y\in(dp,kp]\) and define
\(\varphi_y(v)=-yv/2-(y-dv)_+^2/(8k)\).
The exact energy difference after merging \(p,q\) is
\[
\Delta=Bpq-\frac{3\ell}{2}p+
 \varphi_y(p+q)-\varphi_y(p)
 +\frac{(\ell p-dq)_+}{2}.                              \tag{7}
\]
Because \(\varphi_y'(v)\le-(k+\ell)y/(4k)\) and \(y\ge dp\),
\[
\begin{split}
\Delta&\le
\left[B-\frac{(k+\ell)d}{4k}\right]pq-\ell p\\
&=\left(-\frac\ell2+\frac{\ell^2}{4k}\right)pq-\ell p
\le-\ell p<0.                                         \tag{8}
\end{split}
\]

### Case \(m\ge3\): an interior penultimate hinge

Write \(a=h_{m-2}\), with
\(0<\ell a-dp\le\ell p\) by shortness and productivity.
When \(p,q\) are replaced by \(p+q\), the exact difference is
\[
\begin{split}
\Delta={}&Bpq-\frac\ell2 aq-\frac{3\ell}{2}p
 +\frac{(\ell a-dp)_+^2}{8k}\\
&+\frac{(\ell p-dq)_+}{2}
 -\frac{(\ell a-d(p+q))_+}{2}.                          \tag{9}
\end{split}
\]
The previous productivity inequality gives \(\ell a>dp\),
so \(Bpq-\ell aq/2\le-kpq/4\).
The old interior square is at most \(\ell^2p^2/(8k)\),
and the old terminal hinge is at most \(\ell p/2\).
Using \(p\le H\le2\) and \(\ell/k<1/8\) yields
\[
\boxed{\Delta
\le-\frac{kpq}{4}-\ell p+\frac{\ell^2p^2}{8k}
\le-\frac{kpq}{4}-\frac{31}{32}\ell p<0.}             \tag{10}
\]
The merged final return is productive because
\(k(p+q)\ge kp\ge\ell a\).
All terms use the *actual* terminal jump.

Hence every short initial or interior source followed immediately
by the terminal return can also be deleted at strictly lower cost.

## 4. All three hinge types: one finite-chain normal form

**Theorem 2 (finite all-short-hinge elimination).**
For the saved affine terminal wedge and its certified continuation
gates, every finite productive center-return chain ending at \(b\)
can be replaced by a physically legal center policy with no greater
first-capture cost and with **no active short hinge**, except that the
one-return policy is retained as a separate explicit terminal formula.
This comparison is uniform in the original number \(m\) of returns.

Apply Theorem 1 to a short initial/interior return with at least
two later actions. Apply Section 3 to a short penultimate return.
Use Theorem 4 of HIGH_SURPLUS_SINGLE_RETURN.md to delete a short
*final* return. Each strict merger removes one return.

If a merger makes a subsequent old return nonproductive, it has
captured no new rank; the center-record inequality
\(R(v,s)\ge\sup_{s\le u\le v}Z(u)\) shows that a center wait to
the same later clock time also captures none. Remove that empty
tent, and extend the next productive tent backward over any
empty wait. Its maximal bridge contains the old chosen-side
capture region and does not delay later center contacts.
This is the nonproductive/empty-wait normalization already
established for the balanced renewal in
[CENTER_IMBALANCE_RENEWAL.md](../10-turn-density/CENTER_IMBALANCE_RENEWAL.md).
If the last prefix is empty, extend the preceding productive return
to the prescribed terminal row. The count decreases; therefore
the procedure terminates for finite chains.

Once normalized, repeat. Every strict short hinge is eventually
removed, and no unbounded list of M4/M5/... hinge cases survives.

**Resulting finite-chain optimization.** Apart from the explicit
one-return expression, only the no-hinge quadratic is needed:
\[
Q(h)=A\sum h_j^2-\frac\ell2\sum h_jh_{j+1}
-\frac{3\ell}{2}h_m-\frac y2h_1-\frac{y^2}{8k},
\]
subject to \(h_j\ge0,\ \sum h_j=H\) and
\[
dh_1\ge y,\qquad
dh_j\ge\ell h_{j-1}\quad (2\le j\le m).               \tag{11}
\]
This is a **convex tridiagonal quadratic program** for each count,
with exact Green kernel as in INFINITE_TURN_RENEWAL.md. Equality
interfaces are retained; a strictly positive hinge is unnecessary.
A one-return policy may have \(y>dh_1\) and is therefore checked
by its full formula rather than by the no-hinge quadratic.

**Limitations:** The theorem classifies finite productive chains
under the saved field's prescribed-\(b\) comparison gates.
A countable accumulation can be approached using its bounded
rank-band cost limit, but the theorem does not classify arbitrary
earlier front resets or rule out Zeno controls on the no-hinge
boundary. The minimum over all counts of (11), initial productive
center waits, and comparison with actual exterior exits remain the
next substantive gates. This is **not** a new lower or upper
certificate for the unrestricted game.

## 5. Corollary: no strict short hinge in a terminal Zeno optimizer

The forward merger is not restricted to finite future sequences.
Consider a countably infinite productive chain
\[
t_0<t_1<t_2<\cdots\uparrow b
\]
whose first center state is \(Z(t_0)+y\), whose return-to-center
durations are \(h_j=t_j-t_{j-1}>0\), and whose terminal endpoint tour
is performed at \(b\). Assume all returns are inside the same saved
affine wedge, with no intermediate front reset or other accumulation
interface.

If the initial hinge is active (\(y>dh_1\)), merge \(h_1,h_2\).
If any interior hinge at a finite index \(j\ge2\) is active
(\(\ell h_{j-1}>dh_j\)), merge \(h_j,h_{j+1}\).
A third positive return always follows, at a time strictly below \(b\),
so the affine inverse gate in Theorem 1 applies. The future policy in
(5) may contain infinitely many further returns: removing a captured
rank interval lowers its remaining absolute capture contribution by
at least the integral of the earliest possible direct-ray times,
irrespective of the number of remaining turns.

All capture times are bounded by \(b+3\) under the prescribed terminal
tour. Thus (5) remains valid for the infinite future by bounded
rank-layer integration. If one instead uses finite approximations to
the infinite suffix, the difference is controlled by the shrinking
captured-rank bands, not by an unsupported pointwise continuity of
first-contact time.

Consequently the replacement decreases the infinite policy's total
cost by at least \(kpq/4>0\), a contradiction to optimality.

**Therefore every optimizing countably infinite productive chain
accumulating at the prescribed terminal row must satisfy**
\[
\boxed{
dh_1\ge y,\qquad dh_j\ge\ell h_{j-1}
\quad\text{for all finite }j\ge2.
}                                                      \tag{12}
\]
There is no "final" short hinge in a terminal Zeno sequence; its
finite-index initial/interior hinges are all excluded. The actual
front Zeno optimizer proved in AFFINE_CENTER_ZENO_ATTACHMENT.md
has increasing geometric durations and obeys these inequalities.

This corollary **does not** exclude infinite turns themselves. It
excludes only short-hinge structures within their terminal-accumulating
renewal layer. Infinite chains accumulating at an *earlier reset*
remain in the separate reset/free-boundary analysis.

## 6. Independent exact audit

Run
```sh
python packages/interval_turn_sheet/verify_short_source_mergers.py
```

The script checks **5,760 exact two-source moment identities** using
two independently computed expressions for (6), **3,240 exact
short-penultimate merger costs/margins**, and **6,480 complete
physical rank-moment comparisons** between original and merged
multi-return paths on the synthetic affine terminal field.
Nine of the last category intentionally have a newly
nonproductive subsequent return, which is retained in the
direct record recurrence. Four independent ratios \(\ell/k\) are
used in the algebraic tests.

The universal statements are the analytic derivations (3)--(11)
and the imported saved-field inverse inequalities; sampled checks
do not replace the latter. No native Lean build or CI is claimed.

