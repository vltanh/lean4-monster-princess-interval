# High-surplus all-count exclusion and one-return departure reduction

Date: 2026-11-12. **Two new exact reductions for the affine terminal-center component.**
These are conditional statements for the prescribed terminal row, **not** a new unrestricted Princess–Monster game bound or a globally attached center solution.

## 1. Setting and physical scope

Use the affine terminal wedge and its endpoint/inverse gates in
[AFFINE_CENTER_CHAIN_IDENTITIES.md](../10-turn-density/AFFINE_CENTER_CHAIN_IDENTITIES.md):
\[
R(U,V)=kU-\ell V+c,\quad Z(t)=(k-\ell)t+c,\quad
d=k-\ell,\quad 0<\ell/k<1/8.
\]
Let \(t<b\), \(H=b-t>0\), and let the balanced captured rank at the center be
\(n=Z(t)+y\), with \(y\ge0\).
A productive single return at the *prescribed* terminal row \(b\) is available whenever
\(y<kH\); the equality case is treated by a nonproductive limit.

A chronological productive chain has \(m\ge1\) positive durations
\(h_1,\ldots,h_m\) summing to \(H\), ending at \(b\), with
\[
k h_1\ge y,\qquad k h_j\ge\ell h_{j-1}\quad (2\le j\le m).
\tag{P}
\]
All its radial ranks and inverses must remain in the affine wedge and satisfy
the original terminal gate. The saved field has \(b=15/16\), starts \(t\ge7/8\),
and therefore \(H\le1/16\). Its constants are
\[
k=\frac{655898601421}{62500000000},\qquad
\ell=\frac{820954217}{12500000000}.
\]

The exact off-front energy from [INFINITE_TURN_RENEWAL.md](INFINITE_TURN_RENEWAL.md), after subtracting the *same* chain-independent baseline, is
\[
\begin{split}
E_y(h)={}&A\sum_{j=1}^m h_j^2
-\frac{\ell}{2}\sum_{j=1}^{m-1}h_jh_{j+1}
-\frac{3\ell}{2}h_m
-\frac y2h_1-\frac{y^2}{8k}\\
&-\frac{(y-dh_1)_+^2}{8k}
-\frac1{8k}\sum_{j=2}^{m-1}(\ell h_{j-1}-dh_j)_+^2
-\frac12(\ell h_{m-1}-dh_m)_+,
\qquad A=\frac k8-\frac\ell2 .
\end{split}
\tag{1}
\]
The last term is absent for \(m=1\). Formula (1) includes the initial,
interior, and terminal short-return hinges. No short-hinge exclusion or
finite turn cutoff is assumed in the theorem.

## 2. Theorem: high surplus forces one return, uniformly in turn count

**Theorem 1 (quantitative all-count exclusion).**
Suppose (P), \(\sum h_j=H\), and
\[
\frac{3}{8}kH\le y<kH,\qquad 0<H\le\frac1{16}.
\tag{2}
\]
For the saved rational \(k,\ell\), every productive chain with \(m\ge2\)
satisfies
\[
\boxed{
E_y(h_1,\ldots,h_m)-E_y(H)\ge \mu H>0,
\qquad
\mu=\frac{-25k+4748\ell-1576\ell^2/k}{8192}
=\frac{400295280226865161073511}
{67164016785510400000000000}
\approx0.005959966353787564 .
}
\tag{3}
\]
Here \(E_y(H)\) is the actual one-tent energy, with its own initial hinge.
The bound is independent of \(m\). Thus **no multiple-return chain ending
at \(b\) can optimize this component** in the high-surplus region.
This includes chains with active interior or terminal hinges.

The nominal physical interval \(0\le y\le kH\) has its upper \(5/8\)
closed by this comparison. No statement about a different terminal exit,
an intermediate center reset, or an initial wait is inferred from it.

### Proof

Write
\[
\alpha=\sum_{j=2}^m h_j=H-h_1,\quad
B=2A+\ell/2=k/4-\ell/2,\quad
c_y=\frac{k+\ell}{4k},\quad
\delta=\frac{\ell^2}{8k},\quad
T=\frac{\ell}{2}(3-\ell/k).
\]
Productivity of the first return and (2) imply
\[
0\le\alpha\le5H/8.                                      \tag{4}
\]

**Initial source.** Define
\(\varphi_y(s)=-ys/2-(y-ds)_+^2/(8k)\). Its one-sided derivative satisfies
\[
\varphi_y'(s)=-y/2+\frac{d}{4k}(y-ds)_+
\le-\frac{k+\ell}{4k}y=-c_y y.
\]
Therefore the initial source in \(E_y(h)-E_y(H)\) contributes
at least \(c_y y\alpha\); the constant \(-y^2/(8k)\) cancels.

**Quadratic part.** Since every duration is nonnegative,
\[
H^2-\sum_j h_j^2
\le2h_1\alpha+\alpha^2,\qquad
\sum_{j<m}h_jh_{j+1}
\le h_1\alpha+\alpha^2/2 .
\]
Consequently the quadratic difference is at least
\[
-B\alpha(h_1+\alpha/2)
=-B\alpha(H-\alpha/2).                                  \tag{5}
\]

**All interior hinges.** For \(j\ge2\), productivity yields
\(\ell h_{j-1}\le k h_j\), so
\((\ell h_{j-1}-dh_j)_+\le\ell h_j\).
The sum of interior negative hinge corrections is at least
\[
-\frac{\ell^2}{8k}\sum_{j=2}^{m-1}h_j^2
\ge-\delta H\alpha.                                     \tag{6}
\]

**Terminal hinge and endpoint source.** Productivity of the last return
also gives the stronger estimate
\[
(\ell h_{m-1}-dh_m)_+
\le \frac{\ell^2}{k}h_{m-1}.
\]
As \(H-h_m\ge h_{m-1},h_1\),
\[
\frac{3\ell}{2}(H-h_m)
-\frac12(\ell h_{m-1}-dh_m)_+
\ge T(H-h_m)\ge T h_1.                                  \tag{7}
\]

Combining the four inequalities gives, **for every number of returns**,
\[
E_y(h)-E_y(H)
\ge T(H-\alpha)+\alpha\{c_y y-B(H-\alpha/2)-\delta H\}.
\tag{8}
\]
Let \(\eta=3/8\) and \(u=\alpha/H\in[0,1-\eta]\). Replacing \(y\)
by its lower bound \(\eta kH\), the right side divided by \(H\)
is at least
\[
f_H(u)=T(1-u)+Hu[c_y\eta k-B(1-u/2)-\delta].
\]
Its derivative in \(u\) obeys
\[
f_H'(u)
=-T+H[c_y\eta k-B(1-u)-\delta]
\le-T+\frac{3\eta\ell}{4}H<0,
\]
since \(c_yk-B=3\ell/4\), \(u\le1-\eta\),
\(H\le1/16\), and \(\ell/k<1/8\).
Hence the minimum is at \(u=5/8\). The coefficient multiplying \(H\)
there is
\[
c_y\eta k-B(1+\eta)/2-\delta
=\frac{-5k+28\ell-8\ell^2/k}{64}<0.
\]
It is therefore safe to use the maximum allowed horizon \(H=1/16\).
Direct rational simplification yields
\[
f_H(u)\ge f_{1/16}(5/8)
=\frac{-25k+4748\ell-1576\ell^2/k}{8192}=\mu.
\]
The displayed exact rational \(\mu\) is positive for the saved field.
This proves (3), including every short-hinge configuration. \(\square\)

The proof does **not** infer global concavity merely from the negative
curvature of one hinge when the fixed-duration equality couples all
variables. Inequalities (5)--(8) are valid on the actual fixed-duration
productive simplex.

### Countably infinite terminal accumulation is also excluded

The comparison extends to a countably infinite productive center-return
sequence \(t_1<t_2<\cdots\uparrow b\) with **no earlier reset or
accumulation interface**, followed by the prescribed same endpoint tour
from \(b\). Let \(\delta_N=b-t_N\to0\).
Replace its return tail after \(t_N\) by a single maximal tent from
\(t_N\) to \(b\). This tent is productive: the old productivity condition
implies
\[
\delta_N\ge h_{N+1}\ge(\ell/k)h_N
\quad\Longrightarrow\quad
R(b,t_N)-n_N=k\delta_N-\ell h_N\ge0.
\]
Both the original tail and the replacement can change first-capture
times only on the radial rank band
\[
[n_N,R(b,t_N)],\qquad
R(b,t_N)-n_N\le k\delta_N.
\]
All eventual capture times are at most \(b+3\), because the prescribed
endpoint tour completes by then. Using the *same endpoint tour orientation*
in the two paths, their total expected costs therefore differ by at most
\((b+3)k\delta_N\), which tends to zero. The finite replacement is an
ordinary productive chain ending at \(b\), so inequality (3) applies to
each replacement and survives this limit unchanged.

Thus Theorem 1 excludes not only every **finite** multiple-return chain,
but also **terminal Zeno accumulations at \(b\)** of this prescribed type.
This argument does not delete an infinite return sequence accumulating
at an earlier front reset \(T<b\), followed by a new phase. Those remain
in the separate reset envelope.

## 3. Theorem: single-tent center waiting has an endpoint-only optimum

**Theorem 2 (no interior departure-time minimum).**
For any affine terminal cell with \(k>\ell>0\), fix \(t<b\), \(H=b-t\),
and initial rank \(n=Z(t)+y\).
Consider policies which **wait at the center without acquiring new ranks**
until \(s=b-h\), then make one productive unit tent returning to \(b\),
followed by the prescribed terminal endpoint tour.

No capture while waiting is the condition
\[
y-d(H-h)\ge0.
\]
Productivity of the tent requires \(Z(b)+\ell h\ge n\). Thus the full
permitted waiting interval is
\[
\boxed{
h_{\min}=\max\left\{0,\ H-\frac y d,\
\frac{(y-dH)_+}{\ell}\right\}\le h\le H.
}
\tag{9}
\]
Physical wedge/inverse conditions must additionally hold on the entire
chosen interval. Equalities can represent nonproductive boundary limits.

Put \(g=y-dH\) and \(N(h)=Z(b)+\ell h\).
With the original rank moment \(T_s\) and actual terminal jump \(T_b\),
the absolute continuation cost newly charged by this wait/tent policy is
\[
\begin{split}
J(h)={}&
\frac12\bigl[T_{b-h}(N(h))-T_{b-h}(n)
                 +T_b(N(h))-T_b(n)\bigr]
 +(b+2)(1-N(h))\\
={}&(b-h/2)(\ell h-g)+\frac{k h^2}{8}
-\frac{(g+dh)^2}{8k}
+\frac{\ell h-g_+}{2}
+(b+2)(1-Z(b)-\ell h).
\end{split}
\tag{10}
\]
The first line is the *physical* capture-moment expression; the second
uses
\[
T_s(q)=sq+(q-Z(s))_+^2/(4k),\qquad
T_b(q)=bq+(q-Z(b))_+.
\]
All changes to first-hit moments from different departure times are
accounted for, not assumed continuous.

On the interval (9), \(g+dh\ge0\), and \(g_+\) is constant.
Therefore
\[
\boxed{J''(h)=-\frac{\ell(2k+\ell)}{4k}<0.}              \tag{11}
\]
A strictly concave function on a closed interval attains its minimum at
one of its endpoints. Thus **no intermediate center waiting time**
is optimal in this one-return component. It suffices to compare immediate
departure \(h=H\) with the single boundary \(h=h_{\min}\). The latter is
a front-contact reset, a nonproductive equality, or a no-time-left limit
depending on which term defines \(h_{\min}\).

If some part of (9) leaves the physical wedge, each resulting connected
legal subinterval still has endpoint-only minimizers. Theorem 2 does not
suppress a reset followed by *multiple* later returns or an alternative
exterior exit.

## 4. Corollary: an entire high-surplus waiting strip reduces to two policies

**Corollary 3 (all-count, continuum-wait elimination).**
Assume Theorem 1's saved-field setting and \(y\ge\eta kH\) with
\(\eta=3/8\). Let the Monster wait at the center for \(w\) before beginning
any productive return, and assume no new rank is captured during that wait.
Set
\[
w_{\rm crit}=\frac{y-\eta kH}{d-\eta k},\qquad
w_{\max}=\min\left\{H,\ w_{\rm crit},\ \frac yd,\
                                \frac{kH-y}{\ell}\right\}.
\tag{12}
\]
The denominator \(d-\eta k=k(1-\ell/k-\eta)\) is positive because
\(\ell/k<1/8\).

For every admissible waiting time \(0\le w\le w_{\max}\),
the surviving rank surplus at departure is \(y_w=y-dw\) and the
remaining duration is \(H_w=H-w\). The four bounds in (12) ensure
\[
\eta kH_w\le y_w\le kH_w,\qquad y_w\ge0.
\tag{13}
\]
The first inequality follows from \(w\le w_{\rm crit}\), the second from
\(w\le(kH-y)/\ell\), and the third from \(w\le y/d\).

Apply Theorem 1 at the actual departure state \((t+w,Z(t+w)+y_w)\):
**every** chain with at least two productive returns ending at \(b\)
costs at least \(\mu(H-w)\) more than the one-tent continuation following
the *same wait*. This uniform reduction does not require a bound on
the later turn count or a short-hinge classification.

The one-tent cost as a function of \(h=H-w\) is strictly concave by
Theorem 2. Its minimum on the entire high-surplus waiting strip is
therefore achieved by **one of two policies only**:
\[
\boxed{\text{immediate one tent}\quad\text{or}\quad
  \text{wait }w_{\max}\text{ then one tent}.}
\tag{14}
\]
A boundary equality at \(w_{\max}\) is interpreted as a limiting
nonproductive or front-contact continuation when appropriate.
The argument applies to any subinterval lying within the verified
physical wedge; external exits remain separate.

This closes the combined **waiting time × all productive turn counts**
search on the nonempty strip (12). For instance, an initial surplus
\(y=(3/4)kH\) permits a positive waiting interval bounded by the
first high-rank exit, not merely the single departure \(w=0\).

It does **not** claim that waiting beyond \(w_{\max}\), where the problem
enters the low-surplus region or loses productivity, is dominated.
Nor does it compare a completely different terminal/exterior policy.

## 5. Theorem: every final short-return hinge can be deleted

This result applies **without the high-surplus hypothesis**. It closes
the entire final short-hinge class in the prescribed-\(b\) component.

**Theorem 4 (strict final-hinge merger).**
Let \(0<\ell/k<1/8\), and let a productive affine terminal chain
\(h=(h_1,\dots,h_m)\) have \(m\ge2\) and total duration \(H\le2\).
Write \(a=h_{m-1}>0\), \(v=h_m>0\).
Assume the *final* short-return hinge is active:
\[
kv\ge\ell a,\qquad \ell a-dv>0.                  \tag{15}
\]
Replace the last two tents with one of duration \(a+v\), keeping all
earlier returns and the terminal row \(b\) fixed:
\[
h'=(h_1,\ldots,h_{m-2},a+v).
\]
The new chain remains productive. Provided the merged tent and its
rank inverse remain in the same verified affine wedge, its exact
energy satisfies
\[
\boxed{
E_y(h')-E_y(h)\le-\frac{15}{32}\ell a<0.
}                                                   \tag{16}
\]
The estimate holds for **every** initial surplus \(y\) compatible
with the original productive chain, every earlier hinge pattern, and
every finite turn count \(m\ge2\).

### Proof

Use \(B=k/4-\ell/2>0\) and \(d=k-\ell>0\).
From (15),
\[
0<v<\ell a/d,\qquad \ell/k<1/8.
\]
For \(m\ge3\), denote the predecessor \(q=h_{m-2}\).
Subtract the two exact expressions (1); all earlier-source and
unchanged internal-hinge terms cancel:
\[
\begin{split}
E_y(h')-E_y(h)={}&Bav-\frac{\ell}{2}qv-\frac{3\ell}{2}a\\
 &+\frac{(\ell q-da)_+^2}{8k}
 +\frac{(\ell a-dv)_+}{2}
 -\frac{(\ell q-d(a+v))_+}{2}.
\end{split}                                             \tag{17}
\]
The old productivity condition \(ka\ge\ell q\) gives
\((\ell q-da)_+\le\ell a\).
Drop the nonpositive terms \(-\ell qv/2\) and the final new hinge,
and bound the removed terminal hinge by \(\ell a/2\).
Then
\[
E_y(h')-E_y(h)
\le Bav-\ell a+\frac{\ell^2a^2}{8k}
<\ell a\left[-1+a\left(\frac Bd+\frac{\ell}{8k}\right)\right].
\]
Since \(r=\ell/k\in(0,1/8)\),
\[
\frac Bd=\frac{1-2r}{4(1-r)}<\frac14,\qquad
\frac{\ell}{8k}=\frac r8<\frac1{64}.
\]
Also \(a\le H\le2\). Hence the last bracket is strictly below
\(-1+2(1/4+1/64)=-15/32\), proving (16) for \(m\ge3\).

When \(m=2\), the initial source changes because \(h_1=a\) becomes
\(a+v\). But the function \(\varphi_y\) from Theorem 1 is
nonincreasing, so
\[
E_y(a+v)-E_y(a,v)
\le Bav-\frac{3\ell}{2}a+\frac{(\ell a-dv)_+}{2}
\le Bav-\ell a
<-\frac12\ell a
\]
by \(v<\ell a/d\), \(B/d<1/4\), and \(a\le2\).
This is stronger than (16). The theorem follows. \(\square\)

For the saved field, every merged duration is at most \(H\le1/16\);
it is an uncapped arena-legal tent, and the complete affine wedge
contains its characteristic diamond. Its rank at the terminal row
is at most \(Z(b)+\ell H<1\), so the physical gates remain valid.

**Consequences.** Whenever a finite prescribed-terminal productive
chain has an active terminal hinge, replace its last two returns.
The replacement is strictly cheaper and has one fewer return.
Repeating this finite procedure produces a no-worse chain that either
has only one return or has **no terminal short hinge**. Thus the
terminal-hinge branch itself needs *no separate optimization for any
turn count*. The earlier interior and first-source hinges remain
explicit.

This is an exact merger under the balanced renewal formula; it is not a
pointwise claim that the new physical Monster path captures every target
no later than the old one. Those are different notions of dominance.

## 6. Verification and precise remaining gate

The standard-library script
`packages/interval_turn_sheet/verify_high_surplus_single_return.py`
checks the exact saved-field coefficient \(\mu>0\), its critical-duration
arithmetic, and **980 independent rational comparisons** of formula (1)
against the physical first-inverse/terminal-row moment calculation, for
productive chains of two through eight returns at seven rational horizons.

It separately performs **288 exact wait-departure checks** using (10):
direct moment formula versus closed polynomial at three rational departure
positions, plus the exact midpoint concavity gap
\[
J((a+b)/2)-[J(a)+J(b)]/2
=\ell(2k+\ell)(b-a)^2/(32k).
\]
An additional **60 rational high-surplus waited-chain cases** verify the
combined inequality and two-endpoint reduction in Corollary 3.
A further **165 exact rational terminal-hinge fixtures** verify strict
last-two-return merging, the quantitative gap (16), and agreement with
the independent physical rank-moment recurrence.
The script checks arithmetic fixtures; the unrestricted all-count theorem
is the hand proof above. No Lean compilation or CI is claimed.

**Closed in this checkpoint:** the entire high-surplus, no-initial-wait,
fixed-\(b\) productive-chain sector (all counts and hinge patterns), the
continuous departure-time optimization of a single waited tent, and the
whole high-surplus waiting strip of Corollary 3, and **all terminal
short-return hinges across every initial surplus** by Theorem 4.

**Still open:** low-surplus all-count chains, initial waits followed by
multiple returns or a front reset, and competition with earlier/later
physical exterior exits. In particular the full off-front continuation,
the globally sufficient Princess law, and the unrestricted game-value
bound remain open.
