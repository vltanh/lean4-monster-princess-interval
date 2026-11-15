# Atomic one-turn and two-turn Monster laws: V ≤ 1.42402

**2026-11-15.** A finite Monster law made of one-turn and two-turn paths has an exact upper bound against
every Princess path:

$$
 V\;\le\;\frac{1603303881142469}{1125899906842624}=1.42401990745219\ldots
 \;<\;\frac{142472349375511}{100000000000003}=1.42472349\ldots                      \tag{1}
$$

The bound is a written proof (Sections 2–5) plus one exact integer computation (Section 6). It is not
formalized in Lean and has not been reviewed by anyone else. The comparison value on the right of (1)
is our previous upper bound, from an exact potential certificate for a continuous one-turn law
([archived](archive/research/13-equilibrium-geometry/ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md)). With the lower bound 1.4225745 of [LOWER_BOUND.md](LOWER_BOUND.md) the bracket
has width 0.0014454.

Three laws are used. The first, on 16 bins, was taken from a continuum linear program and gives
$V\le 1.4241299$ on the grid $1/4096$ (Section 6). The other two, on 32 bins, were optimized with the
exact program as the response oracle, one for the grid $1/1024$ ($V\le1.4240687$) and one for the grid
$1/2048$, which gives (1) (Section 7).

Let $\mathcal B_1$ be the class of Monster paths that turn at most once before they first reach an
endpoint and then sweep the interval, and $W_1\ge V$ the value of the game in which the Monster is
restricted to $\mathcal B_1$. Neither law is in $\mathcal B_1$: 0.5% to 0.6% of the mass is on two-turn
paths, so (1) is not a bound on $W_1$. A second law of the same form with one-turn paths only gives

$$
 W_1\;\le\;\frac{25661865897887875}{18014398509481984}=1.42451971873391\ldots                 \tag{2}
$$

which also improves our previous bound $W_1\le 1.42472349\ldots$ (the same certificate).

## 1. The law

Light coordinates are $U=t+x$, $W=t-x$. Two families of unit-speed Monster paths are used.

| Path | Route | Parameters |
| --- | --- | --- |
| $P_b(a)$ | start at $a$, right until $U=b$, left to $-1$, right to $+1$ | $\lvert a\rvert\le b\le 2-a$ |
| $T_2(c,U_1)$ | start at $c$, right until $U=U_1$, left until $W=1$, right to $+1$, left to $-1$ | $\lvert c\rvert\le U_1\le 1$ |

$P_1(1)$ is the endpoint sweep and $P_{2-a}(a)$ is the endpoint-first path, written $S(a)$.
$T_2(c,U_1)$ turns back at $x=(U_1+c)/2$, turns again at $x=(U_1-1)/2$ at time $(1+U_1)/2$, and from
there coincides with the sweep that left $-1$ at time 0. It reaches $+1$ at time 2 and $-1$ at time 4.
$P_b(a)$ reaches $-1$ at time $b+1$ and $+1$ at time $b+3$.

Every atom of the law is a **pair**: a path and its mirror image $x\mapsto -x$, each with half of the
atom's weight. The law is therefore symmetric.

The atoms come from a table of bin masses. For the first law it is
[atomic_law_16bins.txt](code/interval_lightcone/atomic_law_16bins.txt), with denominator
$D=2^{24}$ on the mesh $1/16$:

| Component | Bins | Mass |
| --- | ---: | ---: |
| endpoint sweeps $P_1(1)$ | – | 0.611721 |
| $P_1(a)$, $a>0$ | 13 | 0.094229 |
| $S(a)$, $a>0$ | 7 | 0.184277 |
| $P_1(-c)$, $c>0$ | 12 | 0.062635 |
| $S(-c)$, $c>0$ | 2 | 0.034952 |
| $P_b(a)$, $a>0$, $b\in[15/16,1]$ | 8 | 0.003335 |
| $P_b(-c)$, $c>0$, $b\in[1,17/16]$ | 3 | 0.002902 |
| $T_2(\pm c,U_1)$ | 43 | 0.005950 |

For a grid $h=1/N$ with $N=16r$, each bin is replaced by atoms on the grid points it contains, with
trapezoid weights (end points count half) and, for the two-parameter families, the product rule. In integer
units a one-parameter bin of mass $m$ gives weights $2r\,m\cdot\{1,2\}$ and a two-parameter bin gives
$m\cdot\{1,2\}\cdot\{1,2\}$; the total weight is $W_N=4r^2D$. The bin masses were found by a
floating-point linear program ([continuum_turn_levels.py](code/interval_lightcone/continuum_turn_levels.py))
and rounded. Nothing in the proof depends on how they were found: any nonnegative weights on legal paths
define a Monster law.

## 2. Reduction to radial Princess paths

The Princess may be taken to move at speed at most 1. By the paper's Proposition 3, every continuous
Princess path $p$ has a path $p^*$ of speed at most 1 with $T(m,p)\le T(m,p^*)$ for every Monster path
$m$; the formalization proves this for every continuous path
([`proposition3_of_continuous`](../PrincessMonsterInterval/AlpernEtAl2008/Section2/Dominance.lean#L512)).
So a bound on $\mathbb E\,T(m,p)$ over 1-Lipschitz $p$ holds for all continuous $p$. From here on
Princess paths are 1-Lipschitz.

Let $T(m,p)$ be the first time the Monster path $m$ and the Princess path $p$ coincide.

**Lemma 1.** For continuous $m$ and $p$,
$T(m,\lvert p\rvert)+T(-m,\lvert p\rvert)\ \ge\ T(m,p)+T(-m,p)$.

*Proof.* The sets $\{t: m=p\}\cup\{t:m=-p\}$ and $\{t:m=\lvert p\rvert\}\cup\{t:m=-\lvert p\rvert\}$
are equal, so the smaller of the two times is the same on both sides. For the larger one, suppose
$m(s_1)=\lvert p(s_1)\rvert$ and $m(s_2)=-\lvert p(s_2)\rvert$. Then $f=m-p$ and $g=m+p$ are both
nonnegative at $s_1$ and both nonpositive at $s_2$, so each has a zero between $s_1$ and $s_2$. Hence
$m$ has met both $p$ and $-p$ by time $\max(s_1,s_2)$. ∎

Since the law is symmetric, Lemma 1 gives $\mathbb E\,T(m,p)\le \mathbb E\,T(m,\lvert p\rvert)$. It is
enough to bound **radial** paths, $0\le p\le 1$.

**Lemma 2.** If $p_n\to p$ uniformly on $[0,6]$, then $T(m,p)\le\liminf T(m,p_n)$ for every atom $m$.

*Proof.* All capture times are at most 6. Along a subsequence $t_n=T(m,p_n)\to t^*$, and
$m(t_n)=p_n(t_n)$ gives $m(t^*)=p(t^*)$. ∎

Call a radial path **generic** if its curve $\Gamma=\{(t+p(t),\,t-p(t))\}$ contains no lattice point
$(ih,jh)$. For a radial $p$ and a constant $c\in(0,1)$ with $c\notin \tfrac h2\mathbb Z$, the paths
$p_s=(1-s)p+sc$ are radial and 1-Lipschitz, and each of the countably many lattice points lies on
$p_s$ for at most one $s$. So generic paths $p_s\to p$ exist, and by Lemma 2 it is enough to bound
generic radial paths.

## 3. Capture times in light coordinates

A 1-Lipschitz path is a curve in the $(U,W)$ plane along which both coordinates are nondecreasing, and
time is $(U+W)/2$. Two paths coincide at time $t$ exactly when their curves share a point, so capture
happens at the first common point. A radial Princess curve $\Gamma$ starts at $(r_0,-r_0)$ and stays in
$0\le U-W\le 2$. Write

$$
 w(c)=\min\{W:(c,W)\in\Gamma\},\qquad u(y)=\min\{U:(U,y)\in\Gamma\}.
$$

The curve of $P_b(a)$ is the staircase $W=-a$ for $U\in[a,b]$, then $U=b$ for $W\in[-a,b+2]$, then
$W=b+2$. Its mirror image exchanges $U$ and $W$. The curve of $T_2(c,U_1)$ is $W=-c$ for
$U\in[c,U_1]$, then $U=U_1$ for $W\in[-c,1]$, then $W=1$ for $U\in[U_1,3]$, then $U=3$.

| Monster path | Case | Capture time |
| --- | --- | --- |
| $P_b(a)$ | $a>r_0$ | $(b+w(b))/2$ |
| | $a<r_0$, $u(-a)\le b$ | $(u(-a)-a)/2$ |
| | $a<r_0$, $u(-a)>b$ | at most $b+3$ |
| mirror of $P_b(a)$ | $-a>r_0$ | $(-a+w(-a))/2$ |
| | $-a<r_0$ | $(b+u(b))/2$ |
| $T_2(c,U_1)$ | $c>r_0$ | $(U_1+w(U_1))/2$ |
| | $c<r_0$, $u(-c)\le U_1$ | $(u(-c)-c)/2$ |
| | $c<r_0$, $u(-c)>U_1$ | at most 2 |
| mirror of $T_2(c,U_1)$ | $-c>r_0$ | $(-c+w(-c))/2$ |
| | $-c<r_0$, $u(U_1)\le 1$ | $(U_1+u(U_1))/2$ |
| | $-c<r_0$, $u(U_1)>1$ | at most 4 |

*Proof of the table.* Take $P_b(a)$ with $a>r_0$. The Princess starts with $W=-r_0>-a$, so she is
above the first leg forever, and with $U=r_0<b$. Until she reaches $U=b$ no point of the Monster's curve
other than that first leg has $U<b$. She reaches $U=b$ at height $w(b)\in(-a,b]$, which is on the
second leg. For $a<r_0$ she starts below the first leg and reaches its height at $U=u(-a)>a$; this point
is on the leg exactly when $u(-a)\le b$. Otherwise she is caught at the latest when the Monster completes
its tour at time $b+3$. For the mirror with $-a>r_0$, she reaches the first mirrored leg $U=-a$ at
height $w(-a)\in(a,-a]\subset[a,b]$. With $-a<r_0$ she is to the right of that leg forever and reaches
$W=b$ at $u(b)\in[b,b+2]$, which is on the second mirrored leg $W=b$, $U\in[-a,b+2]$. The four
$T_2$ cases with a capture on the first two legs are identical, with $w(U_1)\le U_1\le 1$ keeping the
crossing on the leg $U=U_1$, $W\in[-c,1]$. If $c<r_0$ and $u(-c)>U_1$, the Princess has $U>U_1$
from then on, so she cannot meet the leg $U=U_1$; she reaches $W=1$ at $u(1)\in(U_1,3]$, on the leg
$W=1$, at time $(1+u(1))/2\le 2$. If $-c<r_0$ and $u(U_1)>1$, she cannot meet the mirror's leg
$U=1$; she reaches $W=3$ at $u(3)\le 5$, on the mirror's last leg, at time at most 4. ∎

The cases $a=r_0$ and $-a=r_0$ are immediate captures and are below every entry.

## 4. Cell staircases

Cells are $(m,k)$: $U\in(mh,(m+1)h)$, $W\in(kh,(k+1)h)$. Let $\Gamma$ be generic and radial, with
$k_0=\lfloor r_0/h\rfloor\in\{0,\dots,N-1\}$. For grid lines put

$$
 K(c)=\lfloor w(ch)/h\rfloor,\qquad M(y)=\lfloor u(yh)/h\rfloor .
$$

**Lemma 3.** The points at which $\Gamma$ first reaches the grid lines are distinct and ordered along
$\Gamma$. In that order they describe a path of cells from $(k_0,-k_0-1)$ that moves one cell right at
each line $U=ch$, from $(c-1,K(c))$, and one cell up at each line $W=yh$, from $(M(y),y-1)$. Every
cell on it has $0\le m-k\le 2N$.

*Proof.* Two first-reach points coincide only at a lattice point, which $\Gamma$ avoids. When $\Gamma$
first reaches $W=yh$, the lines $U=ch$ already crossed are those with $ch<u(yh)$, so the current
column is $\lfloor u(yh)/h\rfloor$; the same holds with the roles exchanged. A cell that contains a point
with $0\le U-W\le 2$ has $(m-k-1)h<2$ and $(m-k+1)h>0$. ∎

Rewards are counted in units of $2T/\delta$, $\delta=h/2$, per unit weight. On a right move from
$(m,k)$ the Princess crosses $U=(m+1)h$ at a height below $(k+1)h$; on an up move she crosses
$W=(k+1)h$ at an abscissa below $(m+1)h$. By the table, a capture at such a crossing has
$2T/\delta\le 2(m+1)+2(k+1)$, the value at the far corner of the cell. A capture on a leg with a cap,
$u(\cdot)\le$ cap, is certain when $m+1\le$ cap, since then $u<(m+1)h\le$ cap. When $m+1>$ cap she
has $u>mh\ge$ cap, and the reward is the bound from the table ($4b+12N$, $8N$ or $16N$ in these
units). Which atoms count at a line is decided by $k_0$ alone: $a>r_0$ is
$a/h\ge k_0+1$.

So for every generic radial path, the expected capture time is at most $R/(8NW_N)$, where $R$ is the
total reward of its cell staircase. Each atom is rewarded exactly twice, once for the path and once for the
mirror. Lines beyond $U=3$ and $W=3$ carry no atoms, so the staircase can be cut at the row $k=3N$.

## 5. The bound

Let $K_N$ be the maximum of $R$ over all start cells and all cell staircases in the strip
$0\le m-k\le 2N$. Sections 2–4 give

$$
 V\le \sup_p \mathbb E\,T(m,p)\le \frac{K_N}{8NW_N}.
$$

$K_N$ is the value of a dynamic program over the cells, one start cell at a time:

$$
 \varphi(m,k)=\max\bigl\{\varphi(m+1,k)+\text{(reward of the right move)},\
                         \varphi(m,k+1)+\text{(reward of the up move)}\bigr\},\qquad \varphi=0\text{ on }k=3N .
$$

Apart from the three "at most" entries the bound is the exact supremum for the atomic law: a Princess can
cross every line arbitrarily close to the far corner of her cell.

## 6. The computation

[atomic_upper.cpp](code/interval_lightcone/atomic_upper.cpp) builds the atoms, checks that each is
legal, and runs the dynamic program in 64-bit integers. An a-priori guard, $(48N+8)W_N<2^{62}$, excludes
overflow: each atom is rewarded twice and no reward exceeds $(24N+4)$ times its weight.

| $N$ | $K_N$ | $K_N/(8NW_N)$ | Decimal |
| ---: | ---: | --- | --- |
| 256 | 50123667351588 | 12530916837897/8796093022208 | 1.4246003090 |
| 512 | 400918328344096 | 12528697760753/8796093022208 | 1.4243480292 |
| 1024 | 3207064631126520 | 400883078890815/281474976710656 | 1.4242227980 |
| 2048 | 25655401760869524 | 6413850440217381/4503599627370496 | 1.4241608870 |
| 4096 | 205238754671383148 | 51309688667845787/36028797018963968 | 1.4241299436 |

Each row is a separate theorem about a separate atomic law. All five are below the previous upper bound.
The values fall by about $0.127/N$ and extrapolate to 1.42410, the response to the continuous law that
the bins describe.

The one-turn law
[atomic_law_16bins_one_turn.txt](code/interval_lightcone/atomic_law_16bins_one_turn.txt) has no
$T_2$ bins (sweeps 0.627898, 52 other bins). The same program gives bounds on $W_1$:

| $N$ | $K_N$ | $K_N/(8NW_N)$ | Decimal |
| ---: | ---: | --- | --- |
| 256 | 50137329653864 | 6267166206733/4398046511104 | 1.4249886150 |
| 512 | 401027727902416 | 25064232993901/17592186044416 | 1.4247366945 |
| 1024 | 3207942091045376 | 6265511896573/4398046511104 | 1.4246124685 |
| 2048 | 25662422708859904 | 25060959676621/17592186044416 | 1.4245506280 |
| 4096 | 205294927183103000 | 25661865897887875/18014398509481984 | 1.4245197187 |

The rows $N\ge 1024$ are below the previous bound; the limit is 1.42449.

The run record is
[atomic_upper_replay.json](code/interval_lightcone/atomic_upper_replay.json). $N=4096$ takes
about 140 s on 20 threads and 3.2 GB.

### Checks

[check_atomic_upper.py](code/interval_lightcone/check_atomic_upper.py) runs three checks.

1. **Table against physical trajectories.** For every legal atom on the grids $N=1,2,3,4$ and random
   Princess staircases through the cell centres, the first meeting time is computed from the two
   piecewise-linear trajectories in $(t,x)$ with exact fractions. It equals the table value in the cases
   stated as exact (23,929 entries) and is below the bound in the others (13,063 entries). This check does
   not use light coordinates.
2. **Dynamic program against enumeration.** On $N=1,2$, all staircases are enumerated and their rewards
   summed atom by atom from the table. The maximum equals the output of both programs on 260 random laws.
3. **Two implementations.** [atomic_response.py](code/interval_lightcone/atomic_response.py) is an
   independent NumPy program. It returns the same integer as the C++ program for every start cell at
   $N=16,32,64,128,256$ (16-bin law) and $N=32,64,128,256$ (32-bin law).

Beyond the grids of the check script, the Python program was run at $N=512$, $1024$ and $2048$ for
both 16-bin laws, and for each 32-bin law of Section 7 on its own grid ($N=1024$ and $N=2048$), with the
same integers as the C++ program (590 to 870 s per run at $N=1024$, 80 to 98 minutes at $N=2048$). So
the bound (1) has been computed by both programs. The two rows $N=4096$ rest on the C++ program alone.

```sh
python3 research/code/interval_lightcone/check_atomic_upper.py --grids 16 32 64 128 256     # about 45 s, prints PASS
g++ -O3 -fopenmp -std=c++17 research/code/interval_lightcone/atomic_upper.cpp -o /tmp/atomic_upper
/tmp/atomic_upper research/code/interval_lightcone/atomic_law_16bins.txt 4096
```

## 7. A law optimized for one grid

[optimize_atomic_law.py](code/interval_lightcone/optimize_atomic_law.py) treats the bin masses as
the variables of a linear program. For a staircase returned by `atomic_upper.cpp`, the reward is linear in
the bin masses, so every staircase is a cutting plane, and the program alternates between the LP and the
exact response to its current law. The LP is floating point; it only proposes laws. The bound of a law is
the integer that `atomic_upper.cpp` returns for it.

On the mesh $1/32$, with four level bins on each side of $b=1$ and all $T_2$ bins (1,629 variables),
and the grid $1/1024$, 480 rounds gave
[atomic_law_32bins_grid1024.txt](code/interval_lightcone/atomic_law_32bins_grid1024.txt):
sweeps 0.623429, $P_1(a)$ 0.096424, $S(a)$ 0.172042, $P_1(-c)$ 0.066453, $S(-c)$ 0.029579, level
bins 0.007086, $T_2$ 0.004989 in 119 bins. The same variables on the grid $1/2048$, 650 rounds in 3.6
hours, gave
[atomic_law_32bins_grid2048.txt](code/interval_lightcone/atomic_law_32bins_grid2048.txt):
sweeps 0.622786, $P_1(a)$ 0.096213, $S(a)$ 0.172790, $P_1(-c)$ 0.066390, $S(-c)$ 0.029681, level
bins 0.007156, $T_2$ 0.004984 in 118 bins. Each law on its own grid:

| Law | $N$ | $K_N$ | $K_N/(8NW_N)$ | Decimal |
| --- | ---: | ---: | --- | --- |
| for $1/1024$ | 1024 | 801679386526336 | 6263120207237/4398046511104 | 1.4240686613 |
| for $1/2048$ | 2048 | 6413215524569876 | 1603303881142469/1125899906842624 | 1.4240199075 |

When the runs were stopped, the LP values were 1.4240491 and 1.4240143. These are floors for this class:
no law with these bins has a bound below 1.4240491 on the grid $1/1024$ or below 1.4240143 on
$1/2048$, up to the LP's tolerance.

**A law is tied to its grid.** The optimizer uses the positions of the atoms. An earlier law from the same
run has bounds 1.4240893, 1.4242187 and 1.4242835 on the grids $1/1024$, $1/2048$ and $1/4096$, and
a 16-bin law that is optimal for the grid $1/128$ (bound 1.4246690 there) has 1.4265796 on $1/2048$.
The first law of this note behaves the other way, 1.4242228 down to 1.4241299, because it was not fitted to
any grid. So each certificate should be computed on the grid for which its law was optimized, and a better
bound needs an optimization on a finer grid, where one response costs 17 s ($1/2048$) or 140 s
($1/4096$).

**What the optimal bounds say about $V$.** The best bound on the grid $1/N$ with atoms from these two
families is the clock-grid value $U_N$ ([LATTICE_GAME.md](LATTICE_GAME.md), Section 3) restricted to the
families. The values found
are 1.42467 ($N=128$, 16 bins), between 1.42427 and 1.42432 ($N=256$, 32 bins, not converged), between
1.424049 and 1.424069 ($N=1024$) and between 1.424014 and 1.424020 ($N=2048$). A fit $V+c/N$ through
the last two gives $c$ between 0.07 and 0.11 and a value between 1.42396 and 1.42399 for the game in
which the Monster is limited to the two families. This is an estimate, not a bound.

## 8. What this does and does not show

- The unrestricted upper bound improves by $7.0\times10^{-4}$. The lower bound is now the larger part of
  the gap: the estimate of about 1.42397 puts the upper bound within about $5\times10^{-5}$ of the value
  of the two-family game and the lower bound $1.4\times10^{-3}$ below it.
- Two-turn paths are used. The one-turn law of the same form as the first law has limit 1.42449 against
  1.42410, so the two-turn paths are worth about $3.9\times10^{-4}$ there. This is evidence, not a proof,
  that $W_1>V$: a proof needs a Princess law that guarantees more than (1) against every one-turn
  Monster.
- The laws are not optimal. On the lattice the unrestricted Monster also uses paths that loiter near the
  center before sweeping (0.2% of the weight at $n=16$), and these two families do not contain them.
