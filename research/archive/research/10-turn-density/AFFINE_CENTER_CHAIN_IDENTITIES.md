# Affine center-chain identities and reset bounds

## Scope

This note supplies exact local components for the center renewal equation in
[CENTER_IMBALANCE_RENEWAL.md](CENTER_IMBALANCE_RENEWAL.md).
It does not identify an equilibrium law or certify a game value.

Assume a legal ordered radial field has an affine characteristic wedge
\[
 R(U,V)=kU-\ell V+c,\qquad a_0\le V\le U\le b,
 \quad k>0,\quad 0<r:=\ell/k<1/8.
\]
Write \(d=k-\ell\), \(z(t)=dt+c\). All ranks used below must lie in
\([0,1]\). At a center state, a *front state* means that both captured
rank prefixes equal \(z(t)\).

For the terminal-chain statements, impose two additional boundary gates:

1. The entire outgoing row \(V=b\), before the endpoint, is constant
   \(R(U,b)=z(b)\). Thus, up to a null rank endpoint,
   \[
   \beta_b(q)=
   \begin{cases}b,&q\le z(b),\\ b+1,&q>z(b).\end{cases}
   \]
2. No rank above \(z(b)\) can be captured in the interior after a center
   departure at \(b\). The sufficient field gate is that every future
   interior radial CDF with \(V\ge b\) is at most \(z(b)\).
   Hence the balanced terminal continuation is
   \(V(b,n)=(b+2)(1-n)\) for \(n\ge z(b)\).

The chain formulas concern productive center-return actions ending at
\(b\), or a chain followed by a productive wait that returns it to the
center front. They retain the actual first-inverse convention. A final
empty wait whose last required inverse lies beyond \(U=b\), a triangle
crossing the affine wedge, and an earlier endpoint tour remain exterior
branches. The local theorem must not silently include them.

## 1. Exact productive-chain energy

Let
\[
 t_0=a<t_1<\cdots<t_m=b,\qquad h_j=t_j-t_{j-1}.
\]
Start with the balanced frontier \(n_0=z(a)\). A productive return gives
\[
 n_j=R(t_j,t_{j-1})=z(t_j)+\ell h_j.
\]
Productivity is equivalent to
\[
 kh_j\ge\ell h_{j-1}\quad(j\ge2),                       \tag{1}
\]
with \(h_0=0\). It also puts every intermediate first inverse inside the
wedge: the outgoing inverse of \(n_j\) from \(t_j\) has characteristic
coordinate \(t_j+r h_j\le t_{j+1}\).

Inside the wedge,
\[
 T_t(q)=tq+\frac{(q-z(t))_+^2}{4k}.
\]
The exact balanced renewal cost of a return is
\[
 K_j=\frac12\{T_{t_{j-1}}(n_j)-T_{t_{j-1}}(n_{j-1})
                 +T_{t_j}(n_j)-T_{t_j}(n_{j-1})\}.     \tag{2}
\]
At the final row use the displayed piecewise-linear \(T_b\), rather
than continuing the affine incoming formula past \(b\).

Subtract the cost of waiting on the front to \(b\) and then taking the
terminal endpoint tour:
\[
 B_{\rm wait}(a)=\frac d2(b^2-a^2)+(b+2)(1-z(b)).
\]
Put \(A=k/8-\ell/2\) and
\[
 Q(h)=A\sum_{j=1}^m h_j^2
       -\frac{\ell}{2}\sum_{j=1}^{m-1}h_jh_{j+1}
       -\frac{3\ell}{2}h_m.
\]
The exact excess cost is
\[
\boxed{
 E(h)=Q(h)
  -\frac1{8k}\sum_{j=2}^{m-1}
        (\ell h_{j-1}-d h_j)_+^2
  -\frac12(\ell h_{m-1}-d h_m)_+ .
}                                                       \tag{3}
\]
The sums and final hinge are absent when \(m=1\).
Both short-return corrections have a **negative** sign.
The final correction is linear because the row at \(b\) has the
endpoint capture jump.

To derive (3), insert (2). The terms
\(\ell^2h_j^2/(8k)\) telescope between adjacent returns. The time terms
give
\[
 \ell b h_m-\frac{\ell}{2}\sum h_j^2
                  -\frac{\ell}{2}\sum h_jh_{j+1}.
\]
The terminal inverse contributes \(\ell h_m/2\), and the extra captured
terminal rank \(\ell h_m\) removes \((b+2)\ell h_m\) from the continuation.
Their remaining linear term is \(-3\ell h_m/2\).
The subtracted inverse of each previous frontier gives exactly the
hinges in (3).

## 2. A lower bound retaining every short return

Define
\[
 w=\sqrt{1-8r},\qquad
 \theta=\frac{1-w}{1+w}\in(0,1),\qquad
 C_0=\frac{\ell}{4\theta}.
\]
Then
\[
 r=\frac{\theta}{2(1+\theta)^2},\qquad
 A=C_0(1+\theta^2).
\]
The no-hinge energy has the exact decomposition
\[
 Q(h)+\frac{9\ell\theta}{4}
 =C_0\left[
    (h_m-3\theta)^2
    +\sum_{j<m}(h_j-\theta h_{j+1})^2
    +\theta^2h_1^2\right].                            \tag{4}
\]

Each interior hinge is absorbed by its own edge square:
\[
 \frac{(\ell a-db)_+^2}{8k}
 \le C_0\frac{r\theta}{2}(a-\theta b)^2.                \tag{5}
\]
Indeed, on the active range \(x=b/a<r/(1-r)\), the positive ratio
\[
 \frac{r-(1-r)x}{1-\theta x}
\]
decreases from \(r\). The multiplier \(r\theta/2\) is less than one.

For the final hinge use the last edge and terminal square together.
If it is active, their difference divided by \(C_0\) is
\[
\begin{split}
 &(a-\theta b)^2+(b-3\theta)^2
          -2\theta a+2\theta(d/\ell)b\\
 &\qquad=(a-\theta b-\theta)^2+b^2
                    +(4+2\theta^2)b+8\theta^2>0.       \tag{6}
\end{split}
\]
If inactive, the two squares are already nonnegative. Thus every finite
productive chain, with all its short returns, satisfies
\[
 \boxed{E(h)\ge E_\infty:=-9\ell\theta/4.}              \tag{7}
\]
The one-action case follows directly from (4).

The bound is attained in the limit by growing tent lengths
\[
 h_j=3\theta^{m-j+1}\quad(1\le j\le m).
\]
Their total tends to
\[
 H_*=\frac{3\theta}{1-\theta},
\]
and their excess tends to \(E_\infty\). All old frontiers lie below the
next center trace, so their hinges vanish. If \(b-a_0\ge H_*\), these
chains fit after an initial front wait. The corresponding infinite
route has an accumulation of increasingly small tents at its initial
departure time, followed by geometrically growing tents. It is a
continuous 1-Lipschitz path. Finite truncations alter only a rank band
whose mass tends to zero and give the same limiting bounded-horizon
cost. This proves the value of this productive-chain component when
the full growing chain fits; it does not settle exterior branches.

## 3. Sorting at a fixed duration

The preceding bound does not need sorting. Sorting additionally reduces
the fixed-duration front problem to a positive quadratic program.

For a chain with each \(h_j\le2\), append \(h_0=0,h_{m+1}=3\), and put
\[
 S=\sum_{j=1}^{m+1}(h_j-h_{j-1})^2.
\]
Then
\[
 Q=(A-\ell/2)\sum h_j^2+(\ell/4)(S-9).
\]
Let \(\widetilde h\) be the increasing rearrangement and \(M=\max h_j\).
A gap decomposition of the path through these lengths gives
\[
 S-S_{\rm sorted}\ge
       \sum_{\text{downward edges}}(h_j-h_{j+1})^2
         +2(3-M)(M-h_m).
\]
One way to see the inequality is to add the artificial upward edge
\(h_m\to M\). Every sorted gap has an upward crossing, while each
downward edge retains its whole squared length. Expanding the final
edge from \(h_m\) to \(3\) supplies the last cross term.

The interior hinge is at most
\((\ell/4)(r/2)(a-b)^2\) on a downward edge. The final hinge is at most
\((\ell/2)(M-h_m)\). Consequently
\[
 E(h)-Q(\widetilde h)\ge
 \frac{\ell}{4}(1-r/2)\sum_{\rm down}(a-b)^2
 +\frac{\ell}{2}(2-M)(M-h_m)\ge0.                       \tag{8}
\]
The sorted chain preserves total duration and satisfies every
productivity and inverse-cell gate. Thus short returns do not improve
the front chain at fixed duration. The all-count constrained quadratic
program and its active-count thresholds are a separate continuation
of this reduction.

## 4. A productive wait resets a front-start prefix

Let a chain end at \(e\), then wait until its balanced frontier
\(n_m=z(e)+\ell h_m\) reaches the center:
\[
 \tau=e+\ell h_m/d.
\]
Assume \(\tau\le b\). The last required inverse lies before \(\tau\), so
this argument does not use the special terminal row at \(b\).

Relative to pure front waiting from \(a\) to \(\tau\), its cost is
\[
 E_{\rm reset}=Q_0(h)-\Lambda h_m^2
     -\frac1{8k}\sum_{j=2}^{m}
             (\ell h_{j-1}-d h_j)_+^2,                 \tag{9}
\]
where \(Q_0=Q+3\ell h_m/2\) and
\[
 \Lambda=\frac{\ell^2}{2d}-\frac{\ell^2}{8k}.
\]
Use the growing-direction square identity for \(Q_0\), without the
terminal linear source. Every hinge is absorbed as in (5), and
\[
 \frac{\Lambda}{C_0}
       =\frac{r\theta(3+r)}{2(1-r)}<\theta^2<1.
\]
It follows that \(E_{\rm reset}\ge0\).

Therefore a front-start prefix ending in a productive center wait may
be replaced by pure waiting to the same balanced front with no larger
cost. A longer productive wait then continues on that front.
An empty wait before the next productive tent can instead be removed
by extending that tent backward. These statements follow the exact
balanced renewal equation; no record is discarded or reset without
paying its imbalance term.

An infinite sequence of productive returns accumulating at \(T\) has
frontiers tending to \(Z(T)\), by continuity. Its front-start reset
comparison follows by the same bounded-moment limit. This does not
remove a chain that accumulates at its *initial* time and then grows
toward the special terminal row.

## 5. Reset from an initial non-front state

Let the initial balanced rank be \(n=z(t)+y\), \(y>0\), and let a chain
be followed by its first productive wait to the front. Define
\[
 h_*=\theta y/\ell,\qquad
 \kappa=\frac{\theta}{4\ell}+\frac1{8k}-\frac1{2d}>0.
\]
Relative to pure waiting from the same initial rank, the exact reset
energy is
\[
\begin{split}
 E_y={}&Q_0-\frac y2h_1
       +y^2\left(\frac1{2d}-\frac1{8k}\right)
       -\Lambda h_m^2\\
 &-\frac{(y-dh_1)_+^2}{8k}
       -\frac1{8k}\sum_{j=2}^{m}
                (\ell h_{j-1}-d h_j)_+^2.             \tag{10}
\end{split}
\]
The opposite square orientation yields
\[
\begin{split}
 E_y+\kappa y^2={}&
 C_0\left[(h_1-h_*)^2
       +\sum_{j=2}^{m}(h_j-\theta h_{j-1})^2
       +\theta^2h_m^2\right]\\
 &-\Lambda h_m^2-\text{the hinges in (10)}.             \tag{11}
\end{split}
\]
Each hinge now absorbs at most
\[
 r/(2\theta)=1/[4(1+\theta)^2]<1
\]
of its corresponding square. The first-source hinge obeys the same
bound after scaling by \(y\). Since
\(\Lambda<C_0\theta^2\), all remaining terms are nonnegative. Therefore
\[
 \boxed{E_y\ge-\kappa y^2.}                            \tag{12}
\]
The decaying equality chain
\(h_j=h_*\theta^{j-1}\) attains this reset bound if its accumulation
point stays in the affine wedge. Its duration is
\[
 \frac{h_*}{1-\theta}
   =\frac{4y}{k\sqrt{1-8r}(1+\sqrt{1-8r})}.
\]
This is the local accumulating-return solution in the preceding note,
now with all short-return corrections retained.

Combining a decaying reset, a front wait, and the growing terminal
chain is an admissible construction. It is **not automatically the
optimal non-front continuation**: a direct finite chain has two
boundary sources, \(-yh_1/2\) and \(-3\ell h_m/2\), whose coupling can
beat the two separated one-source optima. Its fixed-duration
quadratic program and the exterior branches remain in the envelope.

## 6. Saved-field realization and exact checks

For the saved field
`endpoint_joint_i1_field.json`, Git blob
`5c45d042ee9948faebc03354c3e1e2ee3cbec1a5`, the final incoming wedge is
\(7/8\le V\le U\le15/16\), with
\[
 k=655898601421/62500000000,\quad
 \ell=820954217/12500000000,\quad
 c=-71289950193/7812500000.
\]
Its ratio is about \(0.00625824<1/8\).
At \(b=15/16\),
\(z(b)=10184278599/15625000000\).
The exact affine-node audit checks 6,324 future positive-cone vertices,
with maximum exactly \(z(b)\), and all 408 vertices on \(V=b\) have that
value. No triangle crosses the \(V=b\) grid line. Thus the terminal
field gates stated at the beginning hold for this saved field.

The pure-V8/CommonJS verifier
`verify_center_chain_energy.cjs` compares (3) against the complete
saved-field first-inverse primitives for 24 rational chains, including
both interior and terminal short returns and equality productivity
faces. It also checks (10) and (12) for 18 rational non-front reset
chains. All **42 exact checks** passed. This is separate from the
30,864 affine-cell checks and 19,722 physical center-factorization
checks in the preceding note.

A useful exact warning about boundary attachment is retained in the
separate diagnostic: simply taking one triangle to \(b\) is not always
optimal. At \(t=57/64\), initial rank \(z(t)\), inserting the return
\(e=229/256\) before \(b\) improves that one-crossing plan by
\(-819651265201/16384000000000000\).
This is a local policy comparison, not a claim about the game value.
