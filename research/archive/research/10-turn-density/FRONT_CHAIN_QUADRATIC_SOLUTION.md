# Exact front-chain quadratic solution

## Scope and inputs

This is the exact solution of the **prescribed-terminal productive-chain
component** of the center renewal equation. It does not solve the complete
center continuation, the arbitrary initial-prefix problem, or the interval
game.

Use the affine wedge and terminal gates in
[AFFINE_CENTER_CHAIN_IDENTITIES.md](AFFINE_CENTER_CHAIN_IDENTITIES.md):
\[
 R(U,V)=kU-\ell V+c,\qquad a_0\le V\le U\le b,\qquad
 0<r=\ell/k<1/8.
\]
Let \(d=k-\ell\), \(z(t)=dt+c\). The start is a balanced front state
\(n=z(t)\). The allowed component consists of an initial wait on that
front, followed by productive center-return triangles whose final return
is exactly \(b\), and the exact balanced endpoint continuation at \(b\).

Every triangle duration is at most two, as required for an uncapped
triangle in \([-1,1]\). The complete affine wedge and rank interval must
contain the construction. A sufficient simple duration condition is
\(H=b-t\le2\), together with the rank conditions in the companion note.
The original saved-field wedge has \(H\le1/16\).

A productive wait that resets an earlier front-start prefix can be
removed by the reset theorem in the companion note. A final empty wait,
an exterior inverse, a triangle returning after \(b\), and an earlier
endpoint tour are not part of this component. In particular, the actual
saved field has nonconstant outgoing rows for \(V<b\), so prescribing
the final return at \(b\) is a real restriction.

Subtract the pure front-wait-and-endpoint value
\[
 B_{\rm wait}(t)=\frac d2(b^2-t^2)+(b+2)(1-z(b)).
\]
The theorem below gives the exact infimum of the excess cost in this
component, including arbitrary finite turn counts and its accumulating
limit.

## 1. Sorting removes the short-return branches

For successive productive durations \(h_1,\ldots,h_m>0\), the independently
derived exact energy is
\[
 E(h)=Q(h)-\frac1{8k}\sum_{j=2}^{m-1}
             (\ell h_{j-1}-dh_j)_+^2
           -\frac12(\ell h_{m-1}-dh_m)_+ ,
\]
where
\[
 Q(h)=A\sum_jh_j^2-\frac{\ell}{2}\sum_{j<m}h_jh_{j+1}
                  -\frac{3\ell}{2}h_m,\qquad
 A=k/8-\ell/2.
\]
When \(m=1\), both short-return corrections are absent. The final
correction is linear, because the terminal inverse has the actual
endpoint capture jump.

Let \(\widetilde h\) be the increasing rearrangement, and
\(M=\max_jh_j\le2\). Append the two artificial endpoints
\(h_0=0,h_{m+1}=3\). Then
\[
 Q(h)=(A-\ell/2)\sum_jh_j^2+
       \frac{\ell}{4}\left[\sum_{j=1}^{m+1}(h_j-h_{j-1})^2-9\right].
\]
For the Dirichlet sum in brackets, every gap in the sorted list must have
an upward crossing in the original list. Retain all downward-edge
squares. The last upward edge from \(h_m\) to \(3\) also contributes
the cross term through \(M\). Thus
\[
 S(h)-S(\widetilde h)\ge
 \sum_{\rm down}(a-b)^2+2(3-M)(M-h_m).
\]
Every interior negative hinge is at most
\((\ell/4)(r/2)(a-b)^2\), while the final negative hinge is at most
\((\ell/2)(M-h_m)\). Consequently
\[
 E(h)-Q(\widetilde h)\ge
 \frac{\ell}{4}(1-r/2)\sum_{\rm down}(a-b)^2+
 \frac{\ell}{2}(2-M)(M-h_m)\ge0.                 \tag{1}
\]
Increasing durations satisfy both productivity and the stronger
old-front-below-next-center-trace inequalities, so all their hinges
vanish. Their total duration is unchanged.

It follows that this component is exactly
\[
 \inf_{\substack{m\ge1,\ h_j\ge0\\\sum_jh_j\le H}}Q(h). \tag{2}
\]
The unused duration is an initial front wait. Zero durations are removed.
For \(H\le2\), every feasible duration in (2) is an uncapped legal
triangle. No finite bound on \(m\) has been imposed.

## 2. A single positive quadratic program covers all counts

Set
\[
 \theta=\frac{1-\sqrt{1-8r}}{1+\sqrt{1-8r}}\in(0,1),
 \quad C_0=\frac{\ell}{4\theta},\quad \gamma=3\theta.
\]
The identities
\[
 r=\frac{\theta}{2(1+\theta)^2},\qquad
 A=C_0(1+\theta^2)
\]
give
\[
 Q(h)/C_0=h^\mathsf TK_mh-2\gamma h_m,
\]
where \(K_m\) has diagonal \(1+\theta^2\) and adjacent entries
\(-\theta\).

Reverse the order and pad with zeros, so the last physical excursion is
coordinate zero. All finite counts embed in the one convex problem
\[
 \min_{\substack{x_i\ge0\\\sum_{i\ge0}x_i\le H}}
 \left[(1+\theta^2)\sum_i x_i^2
       -2\theta\sum_i x_ix_{i+1}-2\gamma x_0\right]. \tag{3}
\]
Its quadratic form is at least
\((1-\theta)^2\sum_i x_i^2\). The explicit candidates below satisfy
sufficient Karush--Kuhn--Tucker inequalities against every nonnegative
summable sequence, so no finite-dimensional truncation assumption is
needed.

## 3. The finite active-count formula

For \(m\ge1\), define
\[
 c_m=\frac{1-\theta^m}{(1-\theta)(1+\theta^{m+1})},
 \quad
 P_m=\frac{m-2\theta c_m}{(1-\theta)^2},
 \quad
 u_m=\frac{1-\theta^{2m}}{1-\theta^{2m+2}}.
\]
For a given duration \(H\), put
\[
 \zeta=\frac{\gamma c_m-H}{P_m}.
\]
The positive block, in chronological order, is
\[
 h_j=
 \gamma\frac{\theta^{m-j}(1-\theta^{2j})}
                 {1-\theta^{2m+2}}
 -\frac{\zeta}{(1-\theta)^2}
  \left[1-\frac{\theta^j+\theta^{m+1-j}}
                     {1+\theta^{m+1}}\right],
 \quad 1\le j\le m.                              \tag{4}
\]
These expressions are simply
\(h=K_m^{-1}(\gamma e_m-\zeta{\bf1})\). In particular,
\(\sum_jh_j=H\). The exact minimum is
\[
 \boxed{
 E_H=C_0\left[
   -\gamma^2u_m+\frac{(\gamma c_m-H)^2}{P_m}
 \right].
 }                                                \tag{5}
\]

The count \(m\) is determined explicitly. Set \(H_0=0\), and for \(j\ge1\)
let
\[
 f_j=\frac{\theta^{1-j}(1-\theta^j)(1-\theta^{j+1})}
             {(1-\theta)^2(1+\theta)}.
\]
Define
\[
 H_m=\frac{\gamma}{\theta}\,
             \frac{\sum_{j=1}^m f_j}{f_{m+1}}.       \tag{6}
\]
Choose \(m\) so that \(H_{m-1}\le H\le H_m\). At a shared endpoint,
the longer formula has a leading zero and represents the same physical
chain. In particular,
\[
 H_1=\frac{3\theta}{1+\theta+\theta^2}
     =\frac{6r}{1-2r}.                              \tag{7}
\]

### Proof of the support conditions

The last missing coordinate before the active block has reduced
gradient \(\zeta-\theta h_1\); all earlier missing coordinates have
gradient \(\zeta\). Thus the sufficient inequalities are
\[
 h_j\ge0,\quad \zeta\ge0,\quad
 \zeta-\theta h_1\ge0.
\]
At the upper end of the interval in (6),
\(\zeta=\theta h_1\). The recurrence has
\(h_0=0\), \(h_1=\zeta/\theta\), and
\[
 h_{j+1}=(\theta+\theta^{-1})h_j-h_{j-1}+\zeta/\theta.
\]
Its solution is \(h_j=(\zeta/\theta)f_j\). The terminal equation is
\(\zeta f_{m+1}=\gamma\), which gives (6).

At \(H=H_{m-1}\), formula (4) has its first coordinate zero and agrees
with the preceding block. As \(H\) increases, every coordinate increases
because \(K_m^{-1}{\bf1}\) is positive, while \(\zeta\) decreases.
The missing-coordinate gradient therefore decreases strictly and reaches
zero exactly at \(H_m\). This proves \(H_m>H_{m-1}\) and all the stated
support inequalities.

The coordinates are increasing in chronological order. If
\(\delta_j=h_{j+1}-h_j\), the recurrence gives
\[
 \delta_j-\delta_{j-1}
   =\frac{(1-\theta)^2h_j+\zeta}{\theta}\ge0,
 \qquad \delta_0=h_1\ge0.
\]
Therefore the candidate has no short-return hinges and is admissible
for the original component.

For completeness, the global convex certificate is obtained by expanding
the objective around this block. The difference for any feasible
summable sequence is the nonnegative quadratic form of its difference,
plus the nonnegative missing-coordinate gradients, plus
\(2\zeta(H-\sum x_i)\). This proves optimality simultaneously over every
finite count and every infinite summable sequence.

## 4. The accumulating regime

The thresholds increase to
\[
 H_*=\frac{\gamma}{1-\theta}=\frac{3\theta}{1-\theta}.
\]
One explicit positive difference is
\[
 H_*-H_m=
 \frac{\gamma\theta^m(1+\theta)
       \bigl[m(1-\theta)+1-2\theta+\theta^{m+2}\bigr]}
 {(1-\theta)(1-\theta^{m+1})(1-\theta^{m+2})}.
\]
The bracket equals
\(m+1-(m+2)\theta+\theta^{m+2}\), which is positive on \(0<\theta<1\);
the expression tends to zero.

For \(H\ge H_*\), the zero-multiplier solution of (3) is
\(x_j=\gamma\theta^j\). It has mass \(H_*\) and value
\[
 \boxed{E_H=-C_0\gamma^2=-9\ell\theta/4.}            \tag{8}
\]
Use an initial front wait of duration \(H-H_*\), then the infinitely
many increasingly long excursions. Their start times accumulate at
the end of that wait. Since their amplitudes tend to zero, the resulting
path is continuous and 1-Lipschitz.

Finite truncations are enough to realize the same infimum without relying
on an informal limit of capture orders. With \(m\) excursions
\[
 h_j=\gamma\theta^{m-j},
\]
their duration is \(H_*(1-\theta^m)\), and the exact excess is
\[
 Q(h)=-C_0\gamma^2+C_0\gamma^2\theta^{2m}.
\]
Precede them by the remaining front wait. This gives a quantitative
approaching realization with the stated exact limiting payoff.

## 5. What is closed, and what still has to be attached

Equations (5)--(8) solve the prescribed-terminal front component without
a turn-count cutoff. The original saved field has
\[
 k=655898601421/62500000000,\qquad
 \ell=820954217/12500000000,\qquad b=15/16.
\]
For orientation only, its ratio gives
\(\theta\approx0.01283996659\) and
\(H_*\approx0.03902092717\). The first threshold is
\(H_1\approx0.03802538604\). The exact formulas above, rather than these
decimals, define the solution.

These quantities explain why a single crossing to \(b\) can fail even
in a narrow affine slab. They also show that a blanket finite-turn
normal form would discard an actual limiting response mechanism.

The outgoing field is not flat for every \(V<b\). Consequently one
must still compare the optimized component with later-return
triangles, their exact inverse branches, and earlier endpoint tours.
A non-front start adds a second boundary source, and its interaction
with the terminal source is not solved by adding two one-source
optima. None of these local formulas determines an equilibrium
Princess law or supplies a matching upper strategy.

## 6. Exact replay

`packages/interval_turn_sheet/verify_front_chain_quadratic.cjs` is a
self-contained CommonJS/pure-V8 verifier. Its computational body was
executed in V8. The exact report is
`snapshots/front_chain_quadratic_checks.json`.

The 6,072 checks cover the Riccati identities, every KKT coordinate and
support sign in the selected rational fixtures, threshold identities,
sorting with both negative short-return corrections, and geometric
truncation errors. There are also 606 independent comparisons with the
balanced renewal rank primitives, using the actual piecewise-linear
terminal inverse rather than continuing its incoming quadratic formula.

```sh
node packages/interval_turn_sheet/verify_front_chain_quadratic.cjs
```

The command-line wrapper was not executed while the native executor was
unavailable. The theorem is the proof above; the finite fixtures audit its
arithmetic and indexing, not the universal quantifiers.
