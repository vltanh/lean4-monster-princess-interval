# Arbitrary excursions at a stationary affine CDF interface

## Status

This is a local domination theorem for an arbitrary same-side excursion, including arbitrary speeds and infinitely many turns. It supplies a normal form for the pieces between returns to a stationary density interface. It does **not** by itself bound the number of interface returns or prove a global game-value claim.

The theorem was independently audited by the lower-strategy agent. Its proof uses two-target capture order and explicit future-rank credit, not a turn scan.

## 1. Local model and persistence

Translate an interface point and its time to \((0,0)\). Let the continuous signed CDF on the left side be
\[
F(t,x)=q_0+\alpha t+B x,\qquad x\le0,\quad
0\le\alpha<B.
\]
Write
\[
C=B-\alpha>0,\qquad D=B+\alpha.
\]

A Monster excursion \(m\) starts and ends at the interface over a duration \(T>0\):
\[
m(0)=m(T)=0,\qquad m(t)\le0,\qquad |\dot m|\le1.
\]
Before this excursion, suppose its captured rank interval relative to \(q_0\) is \([-L_0,H_0]\), with \(L_0,H_0\ge0\).

Assume the affine formula is valid on the excursion's reachable left cone and on the future unit-left ray
\[
(t,x)=(t,T-t),\qquad
T\le t\le\gamma T,\qquad
\gamma=\frac{B}{C}+\frac12.
\]
The latter is the precise future-persistence gate. An initial two-half-cell neighborhood containing the corresponding forward cone is a sufficient condition. The global continuation itself need not remain in that neighborhood.

The maximal left tent is
\[
m_*(t)=-\min(t,T-t),\qquad 0\le t\le T.
\]
After time \(T\), use exactly the same Monster continuation for \(m\) and \(m_*\).

## 2. The theorem

If the excursion creates a new lower record, replacing it by \(m_*\) cannot increase expected first-capture time. It preserves the exit point, exit time, and continuation. It may capture additional lower ranks during the excursion.

If the excursion creates no new lower record, replacing it by waiting at the interface cannot increase the payoff: the wait raises the CDF pointwise, so it captures every new upper rank no later and loses no new lower capture.

For a productive excursion let \(-L\) be its lowest visited rank relative to \(q_0\), so \(L>L_0\). Put
\[
L_*=\frac{CT}{2}.
\]
The maximal tent has this lower record. The proof gives the quantitative unweighted rank-moment margin
\[
\operatorname{Cost}(m)-\operatorname{Cost}(m_*)
\ge \frac{BC\,T}{D^2}(L_*-L)\ge0.
\]
The inequality uses the same continuation and includes the earliest possible future captures of the newly added lower band. If one works with a radial pair CDF rather than the full signed CDF, the common factor \(1/2\) is applied to both sides.

## 3. Lower ranks and their future credit

Every first capture of a lower rank \(-l\) satisfies
\[
\tau_{-l}\ge \frac lC.
\]
The maximal tent attains this time for every \(l\le L_*\).

At time \(T\), a lower rank \(l>L\) is still uncaptured by the original excursion. Every legal continuation satisfies \(m(t)\ge T-t\). The CDF on that leftmost possible ray is
\[
F(t,T-t)-q_0=BT-Ct.
\]
Consequently that rank cannot be captured before
\[
\frac{BT+l}{C}.
\]
The last such earliest time, at \(l=L_*\), is exactly \(\gamma T\).

The lower-rank moment on the original excursion plus its continuation is therefore at least the maximal-tent lower moment plus
\[
\frac{BT}{C}(L_*-L).
\]
An already captured lower band cancels from this comparison because \(L>L_0\). A continuation which never captures an added rank only makes the inequality stronger.

## 4. A capture-order lower bound for upper ranks

Set \(r=L/L_*\in[0,1]\). Let \(t_L\) be a time when the excursion reaches rank \(-L\).

Starting at rank \(0\), the fastest rank decrease has speed \(C\), so \(t_L\ge L/C\). Returning from its physical location to the interface by time \(T\) also gives
\[
t_L\le \frac{BT-L}{D}.
\]

For an upper rank \(h\in[0,\alpha T]\), any capture inside the left half satisfies
\[
\tau_h\ge h/\alpha
\]
when \(\alpha>0\), because \(F(t,m(t))-q_0\le\alpha t\).

If \(h\) is captured **before** the lower extremum \(-L\), then
\[
t_L\ge \tau_h+\frac{h+L}{C}.
\]
Combining the three inequalities yields
\[
h\le h_*:=\frac{\alpha(CT-2L)}{D}.
\]
Thus every \(h>h_*\) is captured after that lower extremum. Its first capture obeys
\[
\tau_h\ge
\max\left\{\frac h\alpha,\ \frac hD+\frac{2BL}{CD}\right\}.
\]
The two expressions meet at
\[
h_c=\frac{2\alpha L}{C}=\alpha T r.
\]

Integrating the resulting pointwise lower bound gives
\[
M_{\rm upper}(m)\ge
\frac{\alpha T^2}{2}
+\frac{\alpha BT^2}{2D^3}(2Br-C)_+^2.
\]
This is an exact triangular area: the second term is the area between the two affine first-hit bounds on \([h_*,h_c]\), when that interval has positive length.

The maximal tent captures these upper ranks on its return leg:
\[
\tau_h^*=\frac{h+BT}{D},
\qquad
M_{\rm upper}(m_*)=
\frac{\alpha T^2}{2}+\frac{\alpha BT^2}{2D}.
\]

The lower bound for \(\tau_h\) used above is everywhere at most \(\tau_h^*\). Excluding an already captured upper band \([0,H_0]\) therefore only decreases the possible upper-rank loss. This justifies the same bound with arbitrary old records.

When \(\alpha=0\), there are no new upper ranks inside a left excursion, and this part of the proof is unnecessary.

## 5. The exact comparison

Let \(d=1-r\). Divide the lower-rank credit minus the upper-rank deficit by \(BT^2/2\). The result is
\[
d-\frac{\alpha}{D}
\left[1-\frac{(2Br-C)_+^2}{D^2}\right].
\]
It is at least \(C^2d/D^2\).

If \(2Br>C\), use \(2Br-C=D-2Bd\); the difference from \(C^2d/D^2\) is
\[
\frac{4\alpha B^2d^2}{D^3}\ge0.
\]
If \(2Br\le C\), then \(d\ge D/(2B)\), and the same conclusion follows from
\[
4BDd-D^2\ge D^2>0.
\]
This proves the stated margin after restoring the factor \(BT^2/2\).

Ranks outside the changed lower band and the old/new upper bands have identical future first captures: both paths have the same exit point and use the same continuation. The argument is consequently a full payoff comparison, not just a comparison of prefix costs.

## 6. Consequence for a two-half-cell initial cone

Suppose
\[
F(t,x)=q_0+\alpha t+\beta_\pm x,\qquad x\gtrless0,
\quad \beta_\pm\ge|\alpha|.
\]
Take \(\alpha>0\); reflect the local spatial and rank coordinates when \(\alpha<0\).

Every right-side interface excursion has \(F\ge q_0\) and creates no lower record below the entry rank. Its maximal right tent is a pointwise upper envelope for all legal right excursions with the same endpoints and duration, so it dominates without a future assumption.

Every productive left excursion has the domination proved above, with \(B=\beta_-\). A nonproductive left excursion becomes an interface wait. Thus arbitrary internal oscillations of either excursion can be removed before addressing the count of alternating interface returns.

This is also valid for a countable collection of excursions within a sufficiently small initial neighborhood. Apply the finite replacements first and use uniform path approximation and continuity of running CDF records for the limiting statement. For excursions ending before \(T_0\), the sufficient common persistence requirement is \(\gamma T_0\) inside the affine neighborhood.

This normal form leaves an alternating chain of unit tents and possible interface waits. The number of such pieces, the deletion of a flow-overtaken right/left pair, and any global finite-prefix theorem are separate obligations. They are not asserted by this note.

If \(B=\alpha\), no lower rank can be created in the left half, so the nonproductive/interface-wait case applies. With \(\alpha=0\), each half creates only its corresponding record, and pointwise maximal tents suffice.

## 7. Exact implementation and replay

Portable files:

- \`packages/interval_turn_sheet/affine_interface_excursion.cjs\`
- \`packages/interval_turn_sheet/verify_affine_interface_excursion.cjs\`
- \`packages/interval_turn_sheet/affine_interface_excursion_checks.json\`

The verifier uses the exact rational arithmetic from \`affine_record_prefix.cjs\`. It independently integrates first physical contacts over the changed rank interval for multi-turn, waiting, and slower-speed excursions, followed by the identical future unit-left ray.

Saved replay:

- 520 exact integrated algebraic bounds;
- 2,275 exact per-rank capture-order trace inequalities;
- 88 arbitrary productive excursion fixtures;
- 1,056 combinations with pre-existing upper and lower records;
- 2,112 chronological physical rank integrals, inspecting 16,817 segments;
- 76 nonproductive/interface-wait comparisons;
- 71 pointwise maximal-right-tent checks.

The fixtures verify the implementation and boundary cases. The arbitrary-path theorem follows from the capture-order argument, which does not assume a finite number of turns.
