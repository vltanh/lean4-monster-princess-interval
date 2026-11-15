# A Princess field on the grid n = 1024: V ≥ 1.4225745

Written 2026-11-15. This note proves

$$
 V\ \ge\ \frac{9322984150699}{6553600000000}=1.422574485885467529296875
$$

for the value $V$ of the interval Princess–Monster game of Alpern, Fokkink, Lindelauf and Olsder
(SIAM J. Control Optim. 47, 2008), who proved $15/11\le V\le 13/9$. The same argument at $n=512$ gives our
earlier bound $V\ge 36409808231/25600000000=1.4222581340234375$.

The proof has two parts.

- One exact integer computation. A table of integers on a space-time grid of mesh $1/2048$ describes a
  Princess strategy. For every Monster path in a finite set of grid paths, the table assigns an integer
  price. The least price is $K=18652368301398$. Two exact C++ programs return this number.
- Written lemmas (Section 4) that turn $K$ into the bound $V\ge (K-2D)/(4nD)$ with $n=1024$ and
  $D=3.2\cdot10^9$.

What has not been done. The independent BigInt replay that confirmed the $n=512$ computation has not been
run to the end for $n=1024$. No one outside the project has reviewed the lemmas. Nothing here is formalized
in Lean. Section 7 lists every gap we know of.

With the upper bound of [UPPER_BOUND.md](UPPER_BOUND.md) the bracket is
$1.4225745\le V\le 1.4240199$, of width $0.0014454$.

## 1. The argument in brief

1. A table $G$ of integers on the nodes of the grid with time step $\Delta=1/(2n)$ is read as the nodal
   values of a radial distribution function for the Princess (Section 3.3).
2. A Monster grid path pays, at each step and for each endpoint it has not yet reached, the smallest
   table price seen so far. The sum is its price $P(m)$ (Section 3.4). The computation gives
   $K=\min P(m)$ over a finite normalized bank of grid paths (Lemma 1).
3. The normalized bank has the same minimum as the full bank of grid paths (Lemma 3).
4. For every $\varepsilon\in(0,1/2]$, a common random rounding of light coordinates turns the table into
   a legal Princess strategy. Against every Monster path it guarantees
   $K/(4nD)-(1+\varepsilon)/(2n)$ (Lemmas 4–7).
5. Letting $\varepsilon\to0$ gives $V\ge K/(4nD)-1/(2n)=(K-2D)/(4nD)$ (Theorem 1).

The computation records cite a second route to the same number, through the optimum $U_n$ of a finite
linear program for the Monster and the inequality $V\ge U_n-1/(2n)$ (Section 5). That route needs
theorems about the continuous game, such as the existence of an optimal Monster strategy. The route of
Section 4 needs none of them.

## 2. The game and ordered Princess laws

The Monster chooses a path $m:[0,\infty)\to[-1,1]$ with $\lvert m(t)-m(s)\rvert\le\lvert t-s\rvert$.
The Princess chooses a continuous path $y:[0,\infty)\to[-1,1]$. Both start anywhere. The payoff is
$T(m,y)=\inf\lbrace t\ge0: m(t)=y(t)\rbrace$, or $\infty$ if they never meet. The game has a value $V$
(the paper; `value_exists` in the Lean formalization). If a mixed Princess strategy $\mu$ satisfies
$\mathbb E_\mu T(m,\cdot)\ge v$ for every Monster path $m$, then $V\ge v$.

All Princess paths used below have speed at most 1, so the bound holds whether or not her speed is
limited.

Light coordinates are $U=t+x$ and $W=t-x$. A path of speed at most 1 is a curve along which $U$ and $W$
are both nondecreasing.

Ordered laws. Let $\Phi(t,r)$, for $t\ge0$ and $0\le r\le1$, be nondecreasing in $r$, with
$\Phi(t,0)=0$ and $\Phi(t,1)=1$. The ordered law with radial distribution $\Phi$ draws a rank $u$ uniform
on $[0,1)$ and an independent fair sign $\varsigma\in\lbrace-1,+1\rbrace$, and follows

$$
 y(t)=\varsigma\,\rho(t,u),\qquad \rho(t,u)=\inf\lbrace a\in[0,1]:\Phi(t,a)>u\rbrace .
$$

Suppose $\Phi$ satisfies the transport inequalities

$$
 \Phi(s,\,a+\lvert t-s\rvert)\ \ge\ \Phi(t,a)\qquad(s,t\ge0,\ 0\le a\le 1),
$$

with $\Phi(\cdot,r)=1$ for $r\ge1$. Then every $\rho(\cdot,u)$ is 1-Lipschitz: if $\Phi(t,a)>u$ then
$\Phi(s,a+\lvert t-s\rvert)>u$, so $\rho(s,u)\le a+\lvert t-s\rvert$; let $a\downarrow\rho(t,u)$ and
exchange $s$ and $t$. The signed paths are ordered: at every time, $y$ is nondecreasing in the signed rank
(every $\varsigma=-1$ comes before every $\varsigma=+1$; among $\varsigma=-1$ a larger $u$ comes first,
among $\varsigma=+1$ a smaller one).

Write $F(t,x)=\mathbb P(y(t)<x)$ for the strict signed distribution function. Lemma 4 in Section 4
expresses the expected capture time through $F$.

## 3. The grid objects

### 3.1 The grid

Fix $n\ge1$. Put $\Delta=1/(2n)$, $R=2n$, $C=4n$ and $H=12n$. A node is a pair of integers $(j,k)$
with $\lvert k\rvert\le R$ and $j\equiv k\pmod 2$. It is the point $t=j\Delta$, $x=k\Delta$. Its light
coordinates $U=(j+k)\Delta$ and $W=(j-k)\Delta$ are multiples of $h=1/n$. The index $R$ is the
endpoint $x=1$, $C$ is time 2 and $H$ is time 6.

### 3.2 Monster grid paths and the two banks

A grid path is a sequence $k_0,k_1,k_2,\dots$ with $k_0$ even, $\lvert k_{j+1}-k_j\rvert=1$ and
$\lvert k_j\rvert\le R$. It is a Monster path of speed 1 that starts at a point of $h\mathbb Z$. Let
$\tau_-$ and $\tau_+$ be the first indices $j$ with $k_j=-R$ and $k_j=R$.

- The full bank $\mathcal B_n$ is the set of grid paths that visit $0$ at some $j\le C$ (by time 2)
  and reach both endpoints by $j=16n$ (time 8).
- The normalized bank $\mathcal N_n\subset\mathcal B_n$ contains the paths of $\mathcal B_n$ that move
  freely only until their first endpoint or until time 2, whichever comes first. If an endpoint is
  reached at some $j\le C$, the path then runs straight to the other endpoint. Otherwise, at $j=C$, it
  runs straight to one endpoint and then straight to the other, in either order.

Every path in $\mathcal N_n$ reaches both endpoints by time 6.

### 3.3 The nodal field and its conditions

A table consists of a positive integer $D$ and integers $G(j,k)$ for the nodes with $0\le k\le R$ and
$0\le j\le H$. Beyond time 6 put $G=0$. The normalized value $g=G/D$ is meant as the nodal value of the
radial distribution $\Phi(t,r)$ of a symmetric ordered Princess law. The integer price of a node is

$$
 p(j,k)=D+\operatorname{sgn}(k)\,G(j,\lvert k\rvert),\qquad p(j,0)=D,\qquad p(j,-k)=2D-p(j,k).
$$

So $p/(2D)$ is the nodal value of $F(t,x)=\mathbb P(y(t)<x)$. The table used here satisfies five
conditions.

- (C1) Range: $0\le G\le D$ and $G(j,0)=0$.
- (C2) Cone order: $G(j,k)\le G(j\pm1,k+1)$ whenever $0\le k<R$ and both nodes exist. By chaining,
  $G$ is nondecreasing under inclusion of the light intervals $[t-r,t+r]$. Equivalently, $p$ is
  nondecreasing in $U$ and nonincreasing in $W$, also across the center. In particular $p(j,\cdot)$ is
  nondecreasing in $k$, and $p$ does not increase along a leftward step.
- (C3) Sticky endpoint: $G(j+2,R)\le G(j,R)$ for even $j<C$.
- (C4) Outward after time 2: for $j>C$, $G(j,k)=G(C,\,k-(j-C))$ if $k>j-C$, and $G(j,k)=0$ otherwise.
  Every rank runs outward at full speed after time 2. In particular $G=0$ from time 3 on.
- (C5) Incoming front at $U=2$: for $j+k>C$, $G(j,k)=G(j-d,\,k-d)$ with $d=(j+k-C)/2$, read as $0$ if
  $k\le d$. Every rank that reaches the line $t+r=2$ runs outward from there.

The data files call a table with (C1)–(C4) a normalized profile. The proof in Section 4 uses (C1), (C2)
and (C4). Condition (C3) is required by the second engine and the BigInt replay, and (C5) by policy 4 of
the second engine (Section 6).

### 3.4 Records, prices and the bank minimum

For a grid path $m=(k_j)$ define the two running records

$$
 a_j=\min_{0\le i\le j}p(i,k_i),\qquad b_j=\min_{0\le i\le j}p(i,-k_i),
$$

and its price

$$
 P(m)=\sum_{0\le j<\tau_-}a_j+\sum_{0\le j<\tau_+}b_j .
$$

The left record $a$ is paid until the Monster reaches $-1$, and the right record $b$ until it reaches
$+1$. The node at which a clock's own endpoint is reached is not charged. The bank minimum and its
scaled value are

$$
 K=\min_{m\in\mathcal N_n}P(m),\qquad c=\frac{K}{4nD}.
$$

The scale is $\Delta\cdot p/(2D)=p/(4nD)$ per step. If the Princess's signed distribution were exactly
$p/(2D)$ at the nodes, $a_j/(2D)$ would be the mass of Princesses that stayed strictly left of the Monster
at all nodes so far. By Lemma 4, $P(m)/(4nD)$ is then a grid version of the expected capture time.

A calendar for a clock that ends at index $\tau$ is a vector $w_0,\dots,w_{\tau-1}\ge0$ with
$\sum_{i\le j}w_i\ge j+1$ for $j<\tau$ and $\sum_iw_i=\tau$. It is a causal clock on the nodes: each of
the $\tau$ steps is paid for at a node already visited, so that by step $j$ at least $j+1$ units sit on
nodes $0,\dots,j$. With prices $q_i$ it costs $\sum_iw_iq_i$.

### 3.5 The table priced here

The source is the field of the package `princess_front_n512`: $n=512$, $D=1.6\cdot10^9$, 1,049,088
stored values. It was found by linear programming on a profile of mesh $1/64$ at $n=256$, projected so
that (C5) holds, and refined once to $n=512$. How it was found does not enter the proof.

It was refined to $n=1024$ by the full-width common-threshold rule: each fine node with $t\le2$ gets the
value at that node of the field $F_{1/2}$ that Lemma 5 builds from the coarse table with $\varepsilon=1/2$.
With a factor 2, every fine node is a coarse node, the midpoint of a coarse light-cell edge, or the center
of a coarse light cell. The value is then a coarse value or the average of two coarse values, an integer
over $2D=3.2\cdot10^9$. No rounding is needed. Beyond time 2 the table follows (C4).

Two programs do this: `refine_retained_field.py` (NumPy arrays; its self-test compares it on random legal
fields at $n=4,6$ with a literal port of the rule in exact fractions) and `refine.py` (integer weights).
Their tables are byte-identical. Raising values to enforce (C2) and (C3) changes no node. The result,
`princess_front_n1024/field.json`, stores the 4,195,328 values with $t\le2$; the decoders rebuild the rest
by (C4).

The proof uses only the final table. Whether the refinement is good or bad affects the size of $K$, not the
validity of the bound.

### 3.6 The clock-grid optimum $U_n$

Section 5 uses the optimum of a finite program for the Monster. A Monster plan $\alpha$ is a probability
law on $\mathcal B_n$ together with a left and a right calendar for each path. For a real radial field $g$
with values in $[0,1]$ that satisfies (C1)–(C2) (with $D=1$) on all nodes up to time 8, put
$q(j,k)=1+\operatorname{sgn}(k)\,g(j,\lvert k\rvert)$ and

$$
 \Pi(\alpha,g)=\frac{\Delta}{2}\,\mathbb E_\alpha\Bigl[\sum_jw^-_j\,q(j,k_j)+\sum_jw^+_j\,q(j,-k_j)\Bigr].
$$

The clock-grid optimum is $U_n=\min_\alpha\max_g\Pi(\alpha,g)$. For fixed $\alpha$, the maximum over $g$
equals the clock mass plus the positive pressure left unmatched by a maximum bipartite matching, which is
how the notes write the Monster's finite linear program. The notes state it for symmetric laws with one
clock per orientation, which gives the same optimum. [LATTICE_GAME.md](LATTICE_GAME.md), Section 3,
computes $U_n$ for small $n$ by another method.

## 4. From $K$ to the bound

Theorem 1. Let a table on the grid $n$ satisfy (C1), (C2) and (C4), and let $c=K/(4nD)$ with $K$ its
normalized-bank minimum. If $c\le3/2$, then

$$
 V\ \ge\ c-\frac1{2n}=\frac{K-2D}{4nD}.
$$

With $n=1024$, $D=3.2\cdot10^9$, $4nD=13107200000000$ and $K=18652368301398$ this is

$$
 c=\frac{9326184150699}{6553600000000}=1.423062767135467529296875,\qquad
 V\ \ge\ \frac{18645968301398}{13107200000000}=\frac{9322984150699}{6553600000000}.
$$

The proof is the chain of Lemmas 1–7 below. The table at the end of this section gives the kind of
argument and the status of each link.

Lemma 1 (computation). The $n=1024$ table of Section 3.5 satisfies (C1)–(C5), and its normalized-bank
minimum is $K=18652368301398$.

Status: exact integer computation, described in Section 6. Two engines return $K$. Both check (C1) and
(C2) on input; the second also checks (C3), (C4) and, in policy 4, (C5). (C4) also holds by construction,
since `field.json` stores only the values with $t\le2$. The independent BigInt replay was not completed.

Lemma 2 (best calendar). For prices $q_0,\dots,q_{\tau-1}$, the least cost of a calendar is
$\sum_{j<\tau}\min_{i\le j}q_i$. Hence $P(m)$ is the least total cost of a pair of calendars on $m$, with
left prices $p(j,k_j)$ and right prices $p(j,-k_j)$.

Proof. Put $\mu_j=\min_{i\le j}q_i$, which is nonincreasing, and $S_j=\sum_{i\le j}w_i$. Then
$\sum_iw_iq_i\ge\sum_iw_i\mu_i$, and by summation by parts

$$
 \sum_iw_i\mu_i=\sum_{j<\tau-1}S_j(\mu_j-\mu_{j+1})+S_{\tau-1}\mu_{\tau-1}
 \ \ge\ \sum_{j<\tau-1}(j+1)(\mu_j-\mu_{j+1})+\tau\mu_{\tau-1}=\sum_{j<\tau}\mu_j .
$$

For equality, give each step $j$ one unit placed at an index $i\le j$ where $q_i=\mu_j$. ∎

Status: elementary, proved here.

Lemma 3 (the normalized bank suffices). If a table satisfies (C2) and (C4), then
$\min_{m\in\mathcal B_n}P(m)=\min_{m\in\mathcal N_n}P(m)$.

Proof. Since $\mathcal N_n\subset\mathcal B_n$, it is enough to find for each $m\in\mathcal B_n$ some
$m'\in\mathcal N_n$ with $P(m')\le P(m)$.

Case A: the first endpoint is reached at an index $\sigma\le C$; by reflection say $k_\sigma=R$. Let $m'$
follow $m$ up to $\sigma$ and then step left at every index until $-R$, reached at $\sigma+2R\le\tau_-$.
Only the left record is still paid after $\sigma$. For $j\ge\sigma$ we have $k'_j=R-(j-\sigma)\le k_j$,
so $p(j,k'_j)\le p(j,k_j)$ by (C2). Along the leftward run $p(j,k'_j)$ does not increase, so
$a'_j=\min(a_{\sigma-1},p(j,k'_j))$, while $a_j\ge\min(a_{\sigma-1},\min_{\sigma\le i\le j}p(i,k'_i))=a'_j$.
So $m'$ pays no more at each step and stops paying no later. If $m$ first visits the center after
$\sigma$, it does so at some index $\ge\sigma+R$ and $\le C$, and $m'$ reaches the center at $\sigma+R$.
So $m'\in\mathcal N_n$.

Case B: neither endpoint is reached by index $C$. Since $m$ has visited the center by then,
$a_C\le D$ and $b_C\le D$. For $j>C$ the left price is at least $a_C$: if $k_j\ge0$ it is at least $D$.
If $k_j<0$, let $e=-k_j-(j-C)$. If $e\le0$ then $G(j,\lvert k_j\rvert)=0$ by (C4) and the price is $D$.
If $e>0$, then $p(j,k_j)=D-G(C,e)$ by (C4). Speed 1 gives $k_j\ge k_C-(j-C)$, so $e\le-k_C$. Then
$k_C<0$ and $G(C,e)\le G(C,-k_C)$ by (C2), so $p(j,k_j)\ge p(C,k_C)\ge a_C$. The right price is the
reflection. So the records are frozen after index $C$:

$$
 P(m)=\sum_{j<C}(a_j+b_j)+a_C(\tau_--C)+b_C(\tau_+-C).
$$

Let $m'$ follow $m$ up to $C$ and then run straight to the endpoint that $m$ reaches first, and straight
on to the other. Its two arrival indices are no later than those of $m$, and the same argument freezes
its records at the same $a_C,b_C$. So $P(m')\le P(m)$, and $m'\in\mathcal N_n$. ∎

Status: written proof in the notes (Section 5 of the archived
[NORMALIZED_GRID_BANK_PRICING.md](archive/research/12-global-closure/NORMALIZED_GRID_BANK_PRICING.md)),
restated in full here.

Lemma 4 (capture time against an ordered law). Let $\mu$ be an ordered law as in Section 2. Suppose the
restriction of $F$ to $[0,\infty)\times(-1,1]$ extends to a continuous function $\bar F$ on
$[0,\infty)\times[-1,1]$. Let $m$ be a Monster path that first reaches $-1$ at $\tau_-$ and $+1$ at
$\tau_+$ (possibly $\infty$). Then

$$
 \mathbb E_\mu T(m,\cdot)=\int_0^{\tau_-}\min_{s\le t}\bar F(s,m(s))\,dt
 +\int_0^{\tau_+}\min_{s\le t}\bigl(1-\bar F(s,m(s))\bigr)\,dt .
$$

Proof. $\mathbb E\,T=\int_0^\infty\mathbb P(T>t)\,dt$. By continuity, $T>t$ exactly when the Princess is
strictly left of the Monster on all of $[0,t]$ or strictly right of it on all of $[0,t]$. The paths are
ordered by signed rank and the law has no atom inside $(-1,1)$. So at time $s$ the Princesses strictly
left of $m(s)$ form an initial segment of signed ranks of mass $F(s,m(s))$. At $m(s)=1$ this excludes the
atom at $+1$, as it should. The intersection over $s\le t$ has mass $\min_{s\le t}F(s,m(s))$. For
$t<\tau_-$ the Monster has stayed above $-1$, so $F=\bar F$ along its path; from $\tau_-$ on no Princess
is strictly left of it. The right side is the same with $1-\bar F$: the mass strictly right of $x$ is
$1-\bar F(s,x)$ for $-1\le x<1$, including the atom at $-1$ when $x=-1$. ∎

Status: proved here. It is the record formula of the notes (Section 4 of the archived
[CONSTRUCTIVE_PRINCESS_GRID_DUAL.md](archive/research/12-global-closure/CONSTRUCTIVE_PRINCESS_GRID_DUAL.md)).

Lemma 5 (common odd rounding and the interpolated field). Let $h=1/n$ and $0<\varepsilon\le1/2$. Give the
cell $[ih,(i+1)h]$ the orientation $+$ if $0\le i\bmod 2n<n$ and $-$ otherwise; the map
$i\mapsto-i-1\pmod{2n}$ pairs each $+$ cell with a $-$ cell. Draw $Z$ uniform on
$(1/2-\varepsilon,1/2+\varepsilon)$. For $z=(i+\theta)h$ with $0<\theta<1$, let $T_Z(z)=ih$ if
$\theta<Z$ in a $+$ cell or $\theta<1-Z$ in a $-$ cell, and $T_Z(z)=(i+1)h$ if the inequality is
reversed. At a tie choose $ih$ in a $+$ cell and $(i+1)h$ in a $-$ cell. Grid points are fixed. Then
$T_Z$ is nondecreasing, $T_Z(-z)=-T_Z(z)$, $T_Z(z+2)=T_Z(z)+2$, and

$$
 \lvert T_Z(z)-z\rvert\le b(Z)=h\max(Z,1-Z),\qquad \mathbb E\,b(Z)=\frac{1+\varepsilon}{2n}.
$$

Define

$$
 F_\varepsilon(t,x)=\mathbb E_Z\Bigl[\frac{p}{2D}\ \text{at the node with light coordinates}\
 \bigl(T_Z(t+x),\,T_Z(t-x)\bigr)\Bigr]\qquad(0\le t\le8,\ \lvert x\rvert\le1).
$$

By (C4), $F_\varepsilon=1/2$ from time $3+1/n$ on: all mass is then at the endpoints. Keep it so after
time 8.

Under (C1) and (C2), $F_\varepsilon$ is continuous, equals $p/(2D)$ at the nodes, satisfies
$F_\varepsilon(t,-x)=1-F_\varepsilon(t,x)$ and $F_\varepsilon(t,0)=1/2$, and is nondecreasing in $U$ and
nonincreasing in $W$. The radial function $\Phi_\varepsilon(t,r)=2F_\varepsilon(t,r)-1$ for $0\le r<1$,
with $\Phi_\varepsilon(t,1)=1$, therefore satisfies the transport inequalities. Its ordered law
$\mu_\varepsilon$ is legal, and its strict signed distribution is $F_\varepsilon$ on $(-1,1]$.

Proof sketch. Oddness comes from the pairing: the mirror of a point at fraction $\theta$ of a $+$ cell is
at fraction $1-\theta$ of the paired $-$ cell, whose threshold is $1-Z$; the tie rules are mirror images.
Period 2 holds because $2/h=2n$ is a multiple of the orientation period $2n$. The image of a point of the
strip $0\le t\le8$, $\lvert x\rvert\le1$ is a node of the same strip, by monotonicity, oddness and period
2. Each rounded field $p/(2D)$ at $(T_Z(U),T_Z(W))$ is monotone in $U$ and $W$ in the stated directions
by (C2), and so is the average. Inside a cell, moving a coordinate by $\delta$ changes its rounded value
with probability at most $\delta/(2\varepsilon h)$, which gives a Lipschitz bound. At $x=0$ both light
coordinates round to the same value, so the image is a center node and $F_\varepsilon(t,0)=1/2$, that is
$\Phi_\varepsilon(t,0)=0$. Continuity rules out atoms inside $(-1,1)$. ∎

Status: written proof in the notes (Sections 2–3 of the archived
[CONSTRUCTIVE_PRINCESS_GRID_DUAL.md](archive/research/12-global-closure/CONSTRUCTIVE_PRINCESS_GRID_DUAL.md)
and Section 2 of [NORMALIZED_PRINCESS_EXTRACTION.md](archive/research/12-global-closure/NORMALIZED_PRINCESS_EXTRACTION.md)),
sketched here. The positive width $\varepsilon$ is what makes $F_\varepsilon$ continuous. A deterministic
rounding ($\varepsilon=0$) can create a jump at the center or along a characteristic, and then Lemma 4
fails.

Lemma 6 (one Monster path). Let the table satisfy (C1), (C2) and (C4), and let $0<\varepsilon\le1/2$.
For every Monster path $m$ that visits $0$ by time 2 and both endpoints by time 8,

$$
 \mathbb E_{\mu_\varepsilon}T(m,\cdot)\ \ge\ c-\frac{1+\varepsilon}{2n}.
$$

Proof sketch. Write $F=F_\varepsilon$ and $\varphi=p/(2D)$ at nodes.

1. Clocks for $m$. For $t<\tau_-$ let $\sigma_-(t)\le t$ be the first time at which
   $s\mapsto F(s,m(s))$ attains its minimum over $[0,t]$. It is nondecreasing in $t$. Let $\eta_-$ be the
   image of Lebesgue measure on $[0,\tau_-)$ under $\sigma_-$. It has mass $\tau_-$ and satisfies
   $\eta_-([0,s])\ge s$ for $s<\tau_-$. Define $\eta_+$ in the same way from $1-F$ and $\tau_+$. Lemma 4
   gives
   $$
    \mathbb E\,T(m)=\int F(s,m(s))\,\eta_-(ds)+\int\bigl(1-F(s,m(s))\bigr)\,\eta_+(ds).
   $$
   These clocks are fixed before $Z$ is drawn.
2. A grid path for each $Z$. The image $s\mapsto(T_Z(U(s)),T_Z(W(s)))$ of the light coordinates of $m$ is
   nondecreasing in both coordinates, stays in the strip, and changes by one lattice step in one or both
   coordinates at a time. Join consecutive image nodes by unit lattice steps, keeping every image node and
   staying in the strip. Each step is a physical step of duration $\Delta$ and size $\Delta$,
   so this is a grid path $m_Z$. It starts at $T_Z(m(0))\in h\mathbb Z$ at time 0. It is in
   $\mathcal B_n$: a center visit at $s\le2$ maps to a center visit at time $T_Z(s)\le2$, and an endpoint
   visit at $s\le8$ maps to an endpoint visit at time $1+T_Z(s-1)\le8$. The old time $s$ goes to the node
   $\pi_Z(s)$ at time $\rho_Z(s)=\tfrac12\bigl(T_Z(U(s))+T_Z(W(s))\bigr)$, and
   $\lvert\rho_Z(s)-s\rvert\le b(Z)$. Since $x=-1$ maps to $x=-1$, the new path reaches $-1$ at some
   $\tau'_-\le\tau_-+b(Z)$; the same holds at $+1$.
3. Moved clocks with a buffer. Let $\zeta_-$ be the image of $\eta_-$ under $\rho_Z$ plus an atom of mass
   $b(Z)$ at time 0. For $t<\tau'_-$: if $t<b(Z)$ the atom gives $\zeta_-([0,t])>t$; otherwise
   $t-b(Z)<\tau_-$ and every old $s\le t-b(Z)$ has $\rho_Z(s)\le t$, so
   $\zeta_-([0,t])\ge b(Z)+(t-b(Z))=t$. Keep the earliest $\tau'_-$ units of $\zeta_-$. The result
   $\eta'_-$ lies strictly before $\tau'_-$ on nodes of $m_Z$ and, in units of $\Delta$, is a calendar
   for the left clock of $m_Z$. The same construction gives $\eta'_+$.
4. Bound for each $Z$. By Lemmas 2 and 3, and since $m_Z\in\mathcal B_n$,
   $$
    c\le\frac{P(m_Z)}{4nD}\le\int\varphi\,d\eta'_-+\int(1-\varphi)\,d\eta'_+ .
   $$
   Since $\eta'_\pm\le\zeta_\pm$ and the prices are nonnegative,
   $$
    c\le\int\varphi(\pi_Z(s))\,\eta_-(ds)+\int\bigl(1-\varphi(\pi_Z(s))\bigr)\,\eta_+(ds)+b(Z),
   $$
   because the two buffer atoms sit on the same start node and cost $b(Z)(\varphi+1-\varphi)=b(Z)$.
5. Average over $Z$. By the definition of $F_\varepsilon$,
   $\mathbb E_Z\,\varphi(\pi_Z(s))=F(s,m(s))$. Fubini (the integrand is bounded and piecewise constant in
   $Z$) and step 1 give $c\le\mathbb E\,T(m)+\mathbb E\,b(Z)=\mathbb E\,T(m)+(1+\varepsilon)/(2n)$. ∎

The fill in step 2 can be any legal fill; nothing needs to be measurable in it, because step 4 holds for
each $Z$ separately.

Status: written proof in the notes (Sections 4–5 of the archived
[CONSTRUCTIVE_PRINCESS_GRID_DUAL.md](archive/research/12-global-closure/CONSTRUCTIVE_PRINCESS_GRID_DUAL.md),
with the optimal value $U_n$ replaced by the computed $c$ as in Section 1 of
[NORMALIZED_PRINCESS_EXTRACTION.md](archive/research/12-global-closure/NORMALIZED_PRINCESS_EXTRACTION.md)).
The notes use one clock per orientation of a mirrored pair of paths; here both clocks are on one path,
which is equivalent and avoids a reflection-invariant choice of fills.

Lemma 7 (all Monster paths). Let $\tilde\mu_\varepsilon$ be $\mu_\varepsilon$ with every path stopped at
its first contact with an endpoint and, after time 2, moved outward at full speed:
$\tilde y(t)=\pm\min(1,\lvert\tilde y(2)\rvert+t-2)$. If $c\le3/2$, then for every Monster path $m$,

$$
 \mathbb E_{\tilde\mu_\varepsilon}T(m,\cdot)\ \ge\ c-\frac{1+\varepsilon}{2n}.
$$

Proof. Stopping and outward motion keep each path legal.

Case 1: $m$ does not visit $0$ during $[0,2]$; say $m>0$ there. The Princesses with negative sign are at
positions $\le0<m(t)$ up to time 2. Then they run left at full speed to $-1$ and stay. The gap
$m(t)-\tilde y(t)$ does not shrink while they run, and the Monster cannot reach $-1$ before time
$3+m(2)>3$. So half the Princess mass survives until after time 3, and $\mathbb E\,T>3/2\ge c$.

Case 2: $m$ visits $0$ by time 2. Let $\hat m$ follow $m$ to time 2 and then run straight to the endpoint
that $m$ reaches first after time 2 (either one if there is none), and straight on to the other.
Then $\hat m$ visits $0$ by time 2 and both endpoints by time 6, and

$$
 \mathbb E_{\tilde\mu_\varepsilon}T(m)\ \ge\ \mathbb E_{\tilde\mu_\varepsilon}T(\hat m)
 \ \ge\ \mathbb E_{\mu_\varepsilon}T(\hat m)\ \ge\ c-\frac{1+\varepsilon}{2n}.
$$

The last inequality is Lemma 6. For the middle one, compare each path of $\tilde\mu_\varepsilon$ with
the path of $\mu_\varepsilon$ of the same rank and sign. Stopping cannot hasten capture. Suppose the
Monster meets the stopped path at its endpoint at a time $t$ after the contact time. At the contact time
the original path is at the endpoint and the Monster is not beyond it; at $t$ the Monster is at the
endpoint and the original path is not beyond it. By continuity they met in between. Outward motion after
time 2 cannot hasten capture by a Monster that visited the center by time 2: a Princess not yet caught is
strictly on her own side of the Monster at time 2, and the outward path stays at least as far out as the
original.

For the first inequality, take a Princess of $\tilde\mu_\varepsilon$ not caught by time 2, say on the
positive side. At time 2 she is strictly right of the Monster, and from then on she runs to $+1$ at full
speed or already sits there. So the gap does not shrink, and she can only be caught at $+1$. She arrives
by time $3-\tilde y(2)$; the Monster cannot arrive before $3-m(2)$, which is later. So she is caught when
the Monster first reaches $+1$ after time 2. The same holds on the negative side, and $\hat m$ reaches
each endpoint no later than $m$. Before time 2 the two Monster paths agree. ∎

Status: written proof in the notes (Section 6 of the archived
[CONSTRUCTIVE_PRINCESS_GRID_DUAL.md](archive/research/12-global-closure/CONSTRUCTIVE_PRINCESS_GRID_DUAL.md)),
restated here with one change. For Case 1 the notes argue that the target is at most $V$ by the bound
$V\ge U_n-1/(2n)$ and that $V<3/2$. That uses the inequality being proved. Here Case 1 uses the hypothesis
$c\le3/2$ instead, which holds for the computed $c=1.4230628$.

Proof of Theorem 1. By Lemma 7, for each $\varepsilon\in(0,1/2]$ the Princess has a strategy that
guarantees $c-(1+\varepsilon)/(2n)$ against every Monster path, hence against every mixed Monster
strategy. So $V\ge c-(1+\varepsilon)/(2n)$ for every such $\varepsilon$. Let $\varepsilon\to0$. ∎

No single strategy of this construction guarantees $c-1/(2n)$; each $\tilde\mu_\varepsilon$ guarantees
$c-(1+\varepsilon)/(2n)$. At $n=512$ the law with $\varepsilon=1/1024$ was written out and saved; it
guarantees $582556541071/409600000000=1.42225718034912109375$. At $n=1024$ no law was written out. With
$\varepsilon=1/2048$ it would guarantee $9322982588199/6553600000000=1.42257424746\ldots$

| Link | Statement | Kind of argument | Status |
| --- | --- | --- | --- |
| Lemma 1 | the table satisfies (C1)–(C5); $K=18652368301398$ | exact integer computation | two engines agree; BigInt replay not completed |
| Lemma 2 | a calendar costs at least the running-minimum sum | summation by parts | proved here |
| Lemma 3 | the normalized bank has the full bank's minimum | exchange of path tails | proved here; written proof in the notes |
| Lemma 4 | capture time against an ordered law | survival integral | proved here; written proof in the notes |
| Lemma 5 | common odd rounding; the legal field $F_\varepsilon$ | elementary | sketched here; written proof in the notes |
| Lemma 6 | guarantee against one Monster path that visits the center by 2 | moving fixed clocks to the grid with a buffer | precise sketch here; written proof in the notes |
| Lemma 7 | guarantee against every Monster path | pathwise exchanges | proved here; the notes' Case 1 is circular and is replaced |
| Theorem 1 | $V\ge c-1/(2n)$ | limit $\varepsilon\to0$ | assembled here from the lemmas |

## 5. The route through the clock-grid optimum $U_n$

The computation records and the notes derive the bound as $V\ge U_n-1/(2n)\ge c-1/(2n)$.

Lemma 8 ($c\le U_n$). If a table satisfies (C1), (C2) and (C4), then $c\le U_n$.

Proof. Let $g=G/D$. For any Monster plan $\alpha$, Lemma 2 and Lemma 3 give
$\Pi(\alpha,g)\ge\mathbb E_\alpha P(m)/(4nD)\ge c$. So $\max_g\Pi(\alpha,g)\ge c$ for every $\alpha$. ∎

Status: elementary given Lemma 3; this is weak duality for the finite program. The notes reach the same
inequality without (C4), from a theorem that the normalized bank and the full bank have the same
minimax value against an unrestricted Princess (Sections 1–2 of the archived
[NORMALIZED_GRID_BANK_PRICING.md](archive/research/12-global-closure/NORMALIZED_GRID_BANK_PRICING.md))
together with the statement that vertex calendars give that value exactly
([LEFT_FLOOR_CLOCK_ATOMIZATION.md](archive/research/12-global-closure/LEFT_FLOOR_CLOCK_ATOMIZATION.md)).

Theorem 2 (from the notes). $U_n-1/(2n)\le V\le U_n$.

Proof idea. $V\le U_n$ holds because each Monster plan, with a maximum matching, is an upper certificate
against every Princess. For $U_n\le V+1/(2n)$, take an optimal Monster strategy with a clock and matching
certificate whose value is $V$. Round all light coordinates of all paths, clock events and matching edges by
one common map $T_h(z)=h\,\mathrm{round}(z/h)$ with ties to even. This moves every event by at most
$\delta=1/(2n)$ and preserves the matching. Add a clock buffer of mass $\delta$ at time 0, which costs at
most $\delta$ because it is symmetric. The result is a feasible plan on $\mathcal B_n$ of value at most
$V+\delta$.

Its inputs, as traced through the archived notes in `archive/research/12-global-closure/`:

| Input | Note | Argument | Status in the notes |
| --- | --- | --- | --- |
| an optimal Monster strategy exists and can be taken symmetric | `GLOBAL_MINIMAX_AND_CDF_DUALITY.md`, Theorem 1 | weak compactness of laws on 1-Lipschitz paths, lower semicontinuity of capture time, finite-dimensional separation | dated 2026-11-12; no review recorded |
| it visits the center by time $2V-1\le2$ and can be made to finish by time 6 | `SHARP_OUTWARD_HORIZON_REDUCTION.md`, Sections 3–4 | pathwise exchange against outward-forced Princesses; uses $V\le3/2$ | no status line |
| for that strategy, the Princess's best payoff equals the least supremum of a causal clock plane, and the least is attained | `GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md`, Theorem 1 | Prokhorov compactness of clocks, lower semicontinuity, separation | dated 2026-11-12; no review recorded |
| the plane's supremum equals clock mass plus unmatched positive pressure | `GLOBAL_CAUSAL_PRESSURE_MATCHING.md`, Theorems 1–3 | Strassen's theorem for closed orders (Lindvall 1999) | dated 2026-11-13; no review recorded |
| rounding with a buffer costs at most $1/(2n)$ | `EFFECTIVE_FINITE_UPPER_REDUCTION.md`, Sections 2–6 | common monotone rounding, prefix repair | "research proof for independent review" |

The quantization note takes as input an optimal strategy whose positive pressure is fully matched
($d=0$), with center by 2 and completion by 8. That result is in three notes
(`POST_FIRST_ENDPOINT_PRESSURE_LOCALIZATION.md`, `GLOBAL_ZERO_DEFICIENCY_REDUCTION.md`,
`GLOBAL_ZERO_DEFICIENCY_ATTAINMENT.md`). Their proofs give center by 3 and completion by 9; the form with
2 and 8 is a later header that refers to the outward-horizon note and does not redo the limit argument.
These three notes carry the label "independently reviewed"; who reviewed them, and whether the review
covered the header, is not recorded. The stronger input is not needed: the rounding lemma accepts any
unmatched mass $d$, and the four inputs above already give a certificate of value exactly $V$.

Route B gives the same number as Theorem 1. It also gives $V\le U_n$, which is not needed here. Route A
(Section 4) needs neither the existence of an optimal Monster strategy nor any duality theorem for the
continuous game. Both routes need Lemma 1 and Lemma 3.

## 6. The computation and its checks

### 6.1 Engine 1: `price_normalized.cpp`

The program reads a binary table (version 1, $n$, $D$, then the values $G(j,k)$ for $0\le j\le 12n$,
$0\le k\le 2n$, as little-endian unsigned 64-bit integers). It rejects the input unless (C1) and (C2) hold.
It detects (C4) and uses it only to choose the stronger pruning bound below.

It searches $\mathcal N_n$ exhaustively, layer by layer in $j\le C$. A state is a position, a
center-visited flag, the two records and the cost so far. Only starts with $k_0\ge0$ are used, because
$P(m)=P(-m)$. A state that can no longer reach the center by time 2 is dropped. At an endpoint, or at
$j=C$ with the center visited, the exact cost of the deterministic tail (the sweep, or the cheaper of the
two tours) is added by scanning its prices. Initial direct tours give a first complete price. Two rules
remove states.

- Dominance: at the same $j$, position and flag, a state whose two records and cost are all no larger
  than another's dominates it, because every future charge is a minimum with the records and so is
  nondecreasing in them.
- Pursuit bound: a state is dropped only if its cost plus a lower bound on any completion is at least the
  price of a complete path already found. The lower bound lets each clock chase its own endpoint at full
  speed; along such a run the price does not increase and lies below any other continuation's price, as
  in Case A of Lemma 3. Under (C4) the bound adds the frozen-record two-tour cost of Case B, minimized over
  the positions reachable at time 2; that cost is concave in the position, so the two ends of the
  reachable interval suffice. Written proof in the archived
  [NORMALIZED_PURSUIT_LOWER_BOUND.md](archive/research/12-global-closure/NORMALIZED_PURSUIT_LOWER_BOUND.md).

All arithmetic is in unsigned 64-bit integers, with the guard $24nD<2^{63}$ ($7.9\cdot10^{13}$ here).
There is no beam, sampling, floating point or state limit. The returned $K$ is the price of an actual
path of $\mathcal N_n$, so it is at least the minimum. That it is not larger than the minimum rests on the
exhaustive search and the soundness of the two rules.

| Run | Time | Peak memory | Retained states | Transitions | Dominated | Pursuit-pruned |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| $n=512$ | 938 s | 2.3 GB | 2,609,003,114 | 5,117,238,127 | 2,508,235,526 | 50,371,986 |
| $n=1024$ | 17,862 s | 16.2 GB | 36,178,048,329 | 71,614,961,981 | 35,436,914,677 | 370,538,693 |

The $n=1024$ run was made with a binary byte-identical to a fresh `g++ -O3 -std=c++17` build of the
source. It was given the table built by `refine_retained_field.py`, before `refine.py` wrote `field.json`.
The two tables are identical (Section 6.5).

### 6.2 Engine 2: `price_center.cpp`, policies 3 and 4

The second engine reads the same input. It rejects it unless (C1)–(C4) hold, and for policy 4 also (C5).
Before the first center visit it branches exactly like engine 1. After it, it searches only a normal form
that is proved to keep the minimum (archived
[DISCRETE_CENTER_BALANCE_PRICING.md](archive/research/12-global-closure/DISCRETE_CENTER_BALANCE_PRICING.md)):
excursions from the center are straight out-and-back triangles; each starts toward the side with the larger
surviving record; a turn back to the center is allowed only once the record it attacks has fallen to at
most the other record; and the straight return is evaluated in one step (policy 3). Dominance is applied
separately within each phase, justified by a lemma that the conditional value of each phase is monotone
in the records. Policy 4 also finishes a post-center state on
the front $t+\lvert x\rvert\ge2$ with the two direct tours, which (C5) makes exact (Section 7 of the
archived [GLOBAL_INCOMING_FRONT_COMPLETION.md](archive/research/12-global-closure/GLOBAL_INCOMING_FRONT_COMPLETION.md)).

| Run | Time | Peak memory | Retained states | Transitions |
| --- | ---: | ---: | ---: | ---: |
| $n=512$, policy 3 | 148 s | not recorded | not recorded | not recorded |
| $n=512$, policy 4 | 144 s (CI record: 109 s) | not recorded | 508,713,709 | 895,637,791 |
| $n=1024$, policy 4, run by `refine.py` | 1,458 s | not recorded | 6,711,010,516 | 11,791,338,882 |
| $n=1024$, policy 4, same binary input | 1,515 s | 6.3 GB | 6,711,010,516 | 11,791,338,882 |
| $n=1024$, policy 3, same binary input | 1,535 s | 8.6 GB | 7,366,755,383 | 12,458,630,510 |

Every run returns the same minimum as engine 1: $4663655453568$ at $n=512$ and $18652368301398$ at
$n=1024$. Times and memory in both tables are from runs on one local machine; the $n=512$ state counts
come from the CI records of the same engines on the same input.

### 6.3 What the agreement shows

The two engines share their input checks, tail scans and pursuit bound verbatim: `price_center.cpp` is
`price_normalized.cpp` with the center normal form added. Their agreement therefore tests the normal form
against the plain search. It does not test the shared code. The shared code was tested in two other ways.

- Small grids. `test_price_normalized.py` compares engine 1 on 72 small fields with exhaustive enumeration
  of 29,448 normalized paths in exact fractions, with no pruning, and with a separate record dynamic
  program on the exact certificates for $n\le6$; it replays 1,006 returned routes. Its saved record is
  bound to the current source hash. `test_center_pricing.py` compares policies 1–4 of engine 2 with
  engine 1 on 91 legal fields (14,724 enumerated paths, 765 replayed routes), and checks that a table
  violating the conditions is rejected; no record of that run is saved.
- The full $n=512$ computation was replayed by the independent BigInt program below.

### 6.4 The independent BigInt replay

`verify_bigint.cjs` is a separate JavaScript implementation. It decodes `field.json` itself (so (C4) is its
decoding rule), checks (C1)–(C3), detects (C5), and runs a target search with BigInt costs: given the
claimed $K$, it fails if any complete normalized path costs less, and it drops a branch only when its lower
bound reaches $K$. So a pass proves that no normalized path costs less than $K$, without assuming that the
search finds an attaining path. After the first center visit it uses the center normal form of engine 2,
so it is independent in code and arithmetic, not in the center-phase mathematics.

- $n=512$: passed in a CI run of the development repository, in 780.2 s, with 507,231,825 states,
  893,765,461 transitions and 3.9 GB resident memory. The verifier used there (SHA-256 `3ca39089…`)
  differs from the current file only in when it records its own hash. A later local run took 1,029 s.
- $n=1024$: started on 2026-11-15 and stopped after about 15 minutes. It has not been completed. It is
  expected to take several hours; its memory need has not been measured.

### 6.5 Hashes

| Object | SHA-256 |
| --- | --- |
| $n=512$ `field.json` | `a4fe152dbf70f5896c256d3a329f6ac2ab31028421795ae74a3163b399c28e10` |
| $n=1024$ `field.json` | `f210be8e2002d3e408cf3ff1f74ca6b750f19d91b9bc2a259bc229cca0dbfcd3` |
| $n=1024$ table, $12289\times2049$ little-endian 64-bit values | `9bda91423bbeab79f7456751c5648a21c1c31539a6a54011d96f304ea1935e08` |
| $n=1024$ engine input, 16-byte header plus that table | `085285a8d69f53b108ac88cb800145ecb98cf8d9ce561f30510e9b2b258dcd80` |
| `price_normalized.cpp` | `9fe59dd962f76665af8d6f2fceee0bec1f626dfff96f6d918802d67ceb28f9bd` |
| `price_center.cpp` | `1835b5a33da7fb256bfe80317df8edc01e7ed166ee3d490c037b5d645da3c4fa` |
| `verify_bigint.cjs`, current | `9ff33b8b0cfe3afcd04829aade627e7465264f641246cc2a795c96609b4d2b97` |
| `verify_bigint.cjs`, used for the $n=512$ replay | `3ca39089073633d89e12a7ebec1b46257ee037d3ff4ed71d58614f5f6aa73092` |

The records give the table hash in two forms: `refined_n1024_lower_replay.json` hashes the values without
the header, and the engine records hash the input file with it. While this note was written, the table was
rebuilt from the $n=512$ field with `refine_retained_field.py`. It gave both hashes, matched the table
decoded from the $n=1024$ `field.json` value for value, and satisfied (C1)–(C5).

### 6.6 Notes on the records

- The policy-4 time 1,458 s is the wall time of the `refine.py` run, including compilation and decoding;
  that run did not record memory. The 6.3 GB belongs to the separate 1,515 s run on the same input.
- `refined_n1024_lower_replay.json` has three fields (`max_rss_kb`, `run`, `second_engine`) that its
  script does not write; they were added by hand. Running the script again overwrites the file without
  them.
- `princess_front_n1024/manifest.json` lists a file `prepared.field.json` that is not kept. It is
  `field.json` without its seven pricing fields, and its hash can be checked that way.
- The flags `independent_original_replay: false` and `independent_bigint_replay: false` in the files
  written by `refine.py` describe that run alone. Engine 1 was run separately (Section 6.1); the BigInt
  replay was not run.
- Compiler version and processor are not recorded.

## 7. Gaps and unchecked steps

1. The BigInt replay of $K$ at $n=1024$ has not been completed. The two native engines agree, but share the
   code that validates the table, scans the tails and computes the pursuit bound (Section 6.3).
2. No one outside the project has reviewed Lemmas 3–7, the pursuit bound, the center normal form or the
   front guard. Nothing is formalized in Lean.
3. Route A in the form of Theorem 1, which does not use $V$, is assembled in this note. The notes prove
   its pieces for normalized tables, but their version of Case 1 in Lemma 7 cites $V\ge U_n-1/(2n)$, the
   inequality being proved. The replacement ($c\le3/2$) is ours. The notes take the limit
   $\varepsilon\to0$ only at $n=512$, and there next to Route B.
4. Route B rests on four theorems about the continuous game (Section 5) for which no review is recorded,
   and on external results: Strassen's theorem, Prokhorov's and the Arzelà–Ascoli theorems, and measurable
   selection.
5. Lemmas 4–6 use standard measure theory (the measurable selection $\sigma_\pm$, Fubini) that is
   stated, not written out.
6. The record discrepancies of Section 6.6.

## 8. How far refinement and finer profiles go

The bank minimum of one field falls as the grid gets finer, while the loss $1/(2n)$ halves.

| $n$ | bank minimum $c$ | lower bound $c-1/(2n)$ | engine 1 |
| ---: | --- | --- | --- |
| 256 | $583091421641/409600000000=1.4235630$ | $582291421641/409600000000=1.4216099$ | |
| 512 | $36434808231/25600000000=1.4232347$ | $36409808231/25600000000=1.4222581$ | 938 s, 2.3 GB |
| 1024 | $9326184150699/6553600000000=1.4230628$ | $9322984150699/6553600000000=1.4225745$ | 17,862 s, 16.2 GB |

The falls are $3.3\cdot10^{-4}$ and $1.7\cdot10^{-4}$ (the first step also includes the projection to
(C5)). If the fall halves again, $n=2048$ would give about 1.42273, and the limit for this field is about
1.4229. From $n=512$ to $1024$ engine 1 grew by a factor 19 in time and 7 in memory, so $n=2048$ would
take about four days and 110 GB with it, or about 4.5 hours and 42 GB with engine 2. It was not attempted.

Finer profiles. The field is the full-width interpolant of a profile on the mesh $1/k$ with $k=64$. The
optimizer `solve_normalized.py n --profile-grid k` ran in 143 s for $k=16$ at $n=32$ from scratch and,
seeded from the next coarser solution, in 98 s for $k=32$ at $n=64$ and 18 minutes for $k=64$ at
$n=128$ (to a gap of $7\cdot10^{-6}$). Each optimum was
refined by factors of 2 and priced with engine 2, policy 3:

| profile | optimized at | $n=32$ | 64 | 128 | 256 | 512 | 1024 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| $k=16$ | $n=32$ | 1.4246923 | 1.4217905 | 1.4204372 | 1.4197595 | 1.4194182 | |
| $k=32$ | $n=64$ | | 1.4243495 | 1.4229441 | 1.4222568 | 1.4219089 | |
| $k=64$ | $n=128$ | | | 1.4241504 | 1.4234482 | 1.4230955 | |
| $k=64$, the field above | $n=256$ | | | | 1.4235630 | 1.4232347 | 1.4230628 |

Each entry minus $1/(2n)$ is a lower bound on $V$ by Theorem 1; none beats the bound of this note. No run
records were kept for the first three rows. The bank minimum of a fixed field exceeds its limit by about
$0.18/n$. The limits, about 1.41908, 1.42156 and 1.42274 (1.42289 for the retained field), suggest that a
profile on the mesh $1/k$ is worth about $0.078/k$ less than the value 1.42397 estimated from the Monster's
side. A profile on the mesh $1/128$ should then certify about 1.4231 at $n=1024$. The stage $k=128$ at
$n=256$ (65,664 variables) needs a longer time limit for each linear program than the 120 s built into the
optimizer; its first solve takes 6.5 minutes, and an hour-long run did not improve its seed. These are
estimates, not bounds. The optimizer and its linear-programming helpers are not part of the reproduction
in Section 9.

## 9. Reproduce

Run from the repository root. The files are in [`code/`](code), under the package names of the
development repository (`interval_clock_grid`, `interval_center_pricing`, `interval_lightcone`,
`interval_discovery_certificates`; the whole repository is in [`archive/`](archive/README.md)). The
commands need a C++17 compiler, Python 3 with NumPy, and Node.js for the BigInt replay.

```sh
CODE=research/code
# Hashes of the inputs and engines (Section 6.5).
sha256sum $CODE/interval_discovery_certificates/princess_front_n512/field.json \
          $CODE/interval_discovery_certificates/princess_front_n1024/field.json \
          $CODE/interval_clock_grid/normalized_native/price_normalized.cpp \
          $CODE/interval_center_pricing/price_center.cpp

# Refinement rule against a literal port in exact fractions (seconds).
python3 $CODE/interval_lightcone/refine_retained_field.py --selftest

# Rebuild the n=1024 field from the n=512 field and price it with engine 2, policy 4
# (about 25 minutes, 6.3 GB). With price_center.cpp unchanged, the output equals the
# stored field byte for byte (field.json records the engine's hash).
python3 $CODE/interval_center_pricing/refine.py \
  --source $CODE/interval_discovery_certificates/princess_front_n512/field.json \
  --n 1024 --policy 4 --output /tmp/front_n1024
cmp /tmp/front_n1024/field.json $CODE/interval_discovery_certificates/princess_front_n1024/field.json
sha256sum /tmp/front_n1024/work/pricing.input.bin        # 085285a8...

# Engine 2, policy 3, on the same input (about 26 minutes, 8.6 GB).
g++ -O3 -std=c++17 $CODE/interval_center_pricing/price_center.cpp -o /tmp/price_center
/tmp/price_center /tmp/front_n1024/work/pricing.input.bin 0 3

# Engine 1 on the stored field, decoded by a separate standard-library reader. It asserts
# that K and the lower bound equal the values stored in field.json (about 5 hours, 16.2 GB).
python3 $CODE/interval_clock_grid/normalized_native/verify_native_field.py \
  $CODE/interval_discovery_certificates/princess_front_n1024/field.json --output /tmp/original.replay.json

# The independent BigInt replay: done at n=512 (about 17 minutes), not yet at n=1024.
node --max-old-space-size=6000 $CODE/interval_center_pricing/verify_bigint.cjs \
  $CODE/interval_discovery_certificates/princess_front_n512/field.json --front --progress 128
# The heap needed at n=1024 is not known; MB is a placeholder.
node --max-old-space-size=MB $CODE/interval_center_pricing/verify_bigint.cjs \
  $CODE/interval_discovery_certificates/princess_front_n1024/field.json --front --progress 128 \
  > /tmp/independent_n1024.replay.json

# Optional small-grid regressions of the two engines.
python3 $CODE/interval_clock_grid/normalized_native/test_price_normalized.py --output /tmp/native_oracle_replay.json
python3 $CODE/interval_center_pricing/test_center_pricing.py /tmp/center-regression.json
```

`refine.py --classic` also runs engine 1 on the same binary (5 more hours). The original engine-1 run is
`python3 $CODE/interval_lightcone/refine_retained_field.py --price`. It rebuilds the table with the second
refinement program and overwrites `refined_n1024_lower_replay.json`, including the fields added by hand.

Files the commands need:

| File | Role |
| --- | --- |
| `interval_discovery_certificates/princess_front_n512/field.json` | the $n=512$ source field |
| `interval_discovery_certificates/princess_front_n1024/field.json` | the $n=1024$ table, with $K$ and the bound |
| `interval_discovery_certificates/princess_front_n1024/manifest.json` | hashes written by `refine.py` |
| `interval_discovery_certificates/princess_front_n1024/center.replay.json` | engine 2, policy 4 |
| `interval_discovery_certificates/princess_front_n1024/center_policy3.replay.json` | engine 2, policy 3 |
| `interval_discovery_certificates/princess_front_n1024/original.replay.json` | engine 1 |
| `interval_discovery_certificates/princess_front_n512/original.replay.json`, `center.replay.json`, `independent.replay.json` | the $n=512$ records of both engines and the BigInt replay |
| `interval_lightcone/refine_retained_field.py` | second refinement program, self-test, original engine-1 run |
| `interval_lightcone/refined_n1024_lower_replay.json` | record of the engine-1 run and both engine-2 runs |
| `interval_clock_grid/normalized_native/price_normalized.cpp` | engine 1 |
| `interval_clock_grid/normalized_native/verify_native_field.py` | standard-library decoder and engine-1 driver; imported by `refine.py` |
| `interval_center_pricing/price_center.cpp` | engine 2 |
| `interval_center_pricing/refine.py` | refinement and engine-2 driver that wrote `princess_front_n1024/` |
| `interval_center_pricing/verify_bigint.cjs` | the BigInt replay; no local imports |
| `interval_clock_grid/normalized_native/test_price_normalized.py`, `native_oracle_replay.json` | optional: engine-1 regression and its saved record |
| `interval_clock_grid/grid_n1_certificate.json` … `grid_n6_certificate.json` (n = 1, 2, 3, 4, 6) | optional: read by `test_price_normalized.py` |
| `interval_center_pricing/test_center_pricing.py`, `interval_clock_grid/normalized_princess_n6_fixture.json` | optional: engine-2 regression and its fixture |

For this layout, `refine.py` and `test_center_pricing.py` were changed to find their neighbours under
`research/code` instead of `packages/`; no other file was changed. `test_price_normalized.py` overwrites
its saved record unless `--output` is given. From this layout, on 2026-11-15, the refinement self-test and
both small-grid regressions passed, with the engine hashes of Section 6.5.
