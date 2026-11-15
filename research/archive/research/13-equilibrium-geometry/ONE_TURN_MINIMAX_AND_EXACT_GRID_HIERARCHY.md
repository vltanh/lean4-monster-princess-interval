# Restricted minimax, attainment, and an exact finite lower hierarchy

**Status: structural theorems for the canonical one-turn game.**
This note proves the restricted minimax identity, existence of an
optimal physical Monster law in \(\mathcal B_1\), and convergence of
a nested sequence of exact finite-game lower bounds to \(W_1\).
It does not identify \(W_1\), prove strict separation from \(U_*\),
or establish a finite optimal support or a finite attaining grid.

The finite hierarchy has **no continuum-transfer subtraction**:
each of its lower values is already valid against every continuous
canonical one-turn Monster. Its convergence has no claimed rate.

## 1. A compact parameter space with harmless added paths

Use
\[
 K=D'\times\{-1,1\},\qquad
 D'=\{(a,b):-1\le a\le1,\quad a\le b\le2-a\},
\tag{1}
\]
and the physical paths
\[
 (0,a),\quad((b-a)/2,(a+b)/2),\quad
 (b+1,-1),\quad(b+3,1),
\tag{2}
\]
with the selected reflection and constant continuation afterwards.
Every such path captures every legal Princess by time six.

The map from \(K\) to continuous physical paths on \([0,6]\) is
continuous in uniform norm. The parameter space is compact.
The complete-domain theorem
[ONE_TURN_COMPLETE_DOMAIN.md](ONE_TURN_COMPLETE_DOMAIN.md)
shows how it represents all canonical \(\mathcal B_1\) strategies:

- true interior turns and the two endpoint-first faces give the
  corresponding canonical path, up to irrelevant continuation
  after every Princess has already been caught;
- the added face \(a=-1\) is pathwise dominated by its immediate
  endpoint sweep, and similarly after reflection.

These replacements form a Borel piecewise-defined map from \(K\)
to canonical strategies, with no larger capture time against
**any** Princess. Conversely canonical strategies have their
ordinary measurable start/direction/turn parameterization inside
\(K\). Applying these maps to probability laws proves that the
extended mixed game has exactly the same minimizing value
\(W_1\). Thus it is legitimate to use compact \(K\) for mixed
strategies as well as for pure-response minimization.

Let \(\mathcal A\) be the legal Princess paths, restricted to
\([0,6]\). A legal continuation afterwards is immaterial.
For \(k\in K\) and \(p\in\mathcal A\), write
\[
 f(k,p)=T(m_k,p)\in[0,6].
\tag{3}
\]
First coincidence is jointly lower semicontinuous in uniform
path convergence: a subsequential limit of coincidence times
is still a coincidence of the limiting paths. Consequently
\(f\) is jointly lower semicontinuous on \(K\times\mathcal A\).

## 2. Minimax identity and attained Monster optimum

Let \(\mathcal P_{\mathrm{fin}}(\mathcal A)\) denote finitely
supported probability laws on actual Princess paths. Then
\[
 \boxed{
 W_1=
 \min_{\nu\in\mathcal P(\mathcal B_1)}
       \sup_{p\in\mathcal A}\mathbb E_\nu T(m,p)
 =
 \sup_{\mu\in\mathcal P_{\mathrm{fin}}(\mathcal A)}
       \min_{m\in\mathcal B_1}\mathbb E_\mu T(m,p).}
\tag{4}
\]
The Monster minimum is attained by a physical probability law.
No finite-support assertion is made about that optimal law.
The Princess supremum in (4) is not asserted to be attained.

### Existence of an optimal Monster law

The space \(\mathcal P(K)\), with weak convergence, is compact.
For every fixed Princess path \(p\), bounded lower
semicontinuity of \(f(\,\cdot\,,p)\) implies that
\[
 \nu\longmapsto\int_K f(k,p)\,d\nu(k)
\tag{5}
\]
is lower semicontinuous. This is the lower-semicontinuous part
of the Portmanteau theorem; equivalently one may approximate a
bounded lower-semicontinuous function increasingly by continuous
functions on compact metric \(K\).

The supremum of (5) over all \(p\) is lower semicontinuous,
hence attains its minimum on \(\mathcal P(K)\). Pushing a
minimizer through the canonical domination map in Section 1
gives a physical law on \(\mathcal B_1\) whose upper value is
no larger. Equality of the two infima then makes that canonical
law optimal.

### A self-contained finite-mixture minimax argument

Fix \(c<W_1\). For every \(\nu\in\mathcal P(K)\) there is an
actual Princess path \(p\) with
\[
 \int f(k,p)\,d\nu(k)>c.
\]
By (5), these strict superlevel sets are open and cover compact
\(\mathcal P(K)\). A finite subcover supplies Princess paths
\(p_1,\ldots,p_N\).

Consider the upward payoff set
\[
 E=\{r\in\mathbb R^N:
       \text{there is }\nu\in\mathcal P(K)
       \text{ with }
       r_i\ge\int f(k,p_i)\,d\nu(k)\ \text{for all }i\}.
\tag{6}
\]
It is convex because expectation is affine in \(\nu\).
It is closed: if \(r^{(j)}\to r\) and \(\nu_j\) witness
membership, compactness supplies a weakly convergent
subsequence. Lower semicontinuity of every coordinate (5)
makes its limiting measure a witness for \(r\in E\).

The finite-subcover property says that \((c,\ldots,c)\notin E\).
Strict separation of this point from the closed convex set
\(E\) gives a nonzero vector \(\lambda\) and a positive margin
\(\eta\) such that
\[
 \lambda\cdot r>
 c\sum_i\lambda_i+\eta
 \quad\text{for every }r\in E,
\]
after decreasing the margin if necessary.
Since \(E\) is upward closed, every \(\lambda_i\) must be
nonnegative: otherwise increasing one coordinate of \(r\)
would violate the separating inequality. Normalize
\(\sum_i\lambda_i=1\). Applying the inequality to each actual
payoff vector gives
\[
 \inf_{\nu\in\mathcal P(K)}
       \sum_i\lambda_i\int f(k,p_i)\,d\nu(k)>c.
\tag{7}
\]
In particular every Dirac Monster satisfies (7), so the actual
finite Princess law \(\sum_i\lambda_i\delta_{p_i}\) secures
strictly more than \(c\). Conversely weak duality bounds every
Princess security by \(W_1\). Letting \(c\uparrow W_1\)
proves (4).

This is also an application of
[Sion (1958), Theorem 4.2′](https://msp.org/pjm/1958/8-1/pjm-v8-n1-p14-p.pdf):
the minimizing probability space is compact, expectation is
affine in each mixed strategy, and it is lower semicontinuous
in the minimizing variable. The elementary proof above makes
clear that no Princess best-response attainment or finite
optimal support is being assumed.

## 3. Stability of strict security under actual path approximation

Suppose a fixed finite actual Princess law has paths \(p_i\),
weights \(w_i\), and security \(c\). Let \(p_i^{(j)}\) converge
uniformly to \(p_i\) on \([0,6]\), with every approximating path
legal. Then
\[
 \liminf_j
    \min_{k\in K}\sum_iw_i f(k,p_i^{(j)})
 \ \ge\
    \min_{k\in K}\sum_iw_i f(k,p_i)=c.
\tag{8}
\]
To prove this, take approximate minimizing \(k_j\) along a
subsequence realizing the lower limit. Compactness gives a
further convergent subsequence \(k_j\to k\). Joint lower
semicontinuity of first coincidence, followed by the finite
nonnegative sum, gives a lower limit at least the original
payoff against \(k\), which is at least \(c\).

The same statement follows by Fatou for a coupled perturbation
with additional randomness. In particular it justifies the
continuous regularization in Section 6 below.

For fixed paths, changing weights from \(w\) to \(w'\) changes
every Monster payoff by at most
\[
 6\|w-w'\|_1.
\tag{9}
\]
Therefore a strict finite-mixture security margin survives
sufficiently close rational probability weights.

Any finite set of legal paths can also be uniformly approximated
by legal rational piecewise-affine paths: first contract their
positions slightly towards zero, creating spatial and speed
slack, then sample at sufficiently close rational times and
round sampled positions to rational values using less than
the available speed slack. Linear interpolation stays in the
arena with speed at most one. Equation (8) preserves every
strict security margin eventually.

Together with the general finite attack theorem
[ONE_TURN_FINITE_PRINCESS_ATTACK_SET.md](ONE_TURN_FINITE_PRINCESS_ATTACK_SET.md),
this already yields a countable complete search for strict
lower certificates. There is a more structured exact hierarchy.

## 4. A finite grid game with no transfer loss

Fix an integer \(n\ge1\) and \(\Delta=1/(2n)\).
Let \(\mathcal A_n\) be the finite Princess bank defined by:

- initial positions in \(n^{-1}\mathbb Z\cap[-1,1]\);
- unit-speed steps of length \(\Delta\), each to the left or
  right, on the physical clock \(j\Delta\), through time six;
- paths stay in the arena and stop permanently at their first
  endpoint contact, if they reach one before six.

Paths still interior at time six may be continued constantly
afterwards. That continuation is beyond the entire capture
horizon. Thus the bank is finite; at most
\((2n+1)2^{12n}\) step descriptions are possible before removing
duplicates and invalid paths.

Define the Monster parameter grid
\[
 \mathcal M_n=
 \{(a,b,s)\in K:a,b\in n^{-1}\mathbb Z\}.
\tag{10}
\]
There are exactly \((2n+1)^2\) parameter pairs before reflection
and removal of duplicate/payoff-equivalent boundary paths.

**Exact grid reduction.** For every probability law \(\mu\)
on \(\mathcal A_n\),
\[
 \boxed{
 \min_{m\in\mathcal B_1}\mathbb E_\mu T(m,p)
 =
 \min_{k\in\mathcal M_n}\mathbb E_\mu f(k,p).}
\tag{11}
\]
There is no discretization subtraction in this equality.

To prove it, express Princess positions as \(k_j/(2n)\).
Before an endpoint is reached, even initial parity and unit
steps give \(k_j\equiv j\pmod2\). Hence every light-coordinate
vertex \(U=(j+k_j)/(2n)\), \(W=(j-k_j)/(2n)\) lies in
\(n^{-1}\mathbb Z\). An endpoint can first be reached only at
an even clock index. Compress its stationary tail to a single
segment ending at time six; the endpoints of that tail also
have light coordinates on \(n^{-1}\mathbb Z\).
There is no arbitrary endpoint waiting followed by departure.

The complete rectangular attack arrangement for any law on this
bank therefore has every vertical and horizontal level on
\(n^{-1}\mathbb Z\). Intersections with \(b=a\) and \(a+b=2\)
stay on that same grid. All actual minimizing vertices from the
finite attack theorem belong to \(\mathcal M_n\), proving (11).

Every capture in the finite matrix occurs on the physical clock
\(\Delta\mathbb Z\). Until stopping, the two players have the
same grid parity; two opposite-speed legs therefore first meet
at a clock vertex, not strictly between adjacent clock vertices.
A stationary endpoint is met at a Monster endpoint arrival,
also on the clock. Thus the matrix consists of exact integer
multiples of \(1/(2n)\), with closed/time-zero captures included.

## 5. The exact finite lower values increase to \(W_1\)

Let \(L_n\) be the value of the finite matrix game with Princess
bank \(\mathcal A_n\) and Monster grid \(\mathcal M_n\):
\[
 L_n=
 \max_{\mu\in\mathcal P(\mathcal A_n)}
      \min_{k\in\mathcal M_n}\mathbb E_\mu f(k,p).
\tag{12}
\]
This is a finite rational LP, so its value and some optimal
Princess weights are rational. By (11),
\[
 L_n=
 \max_{\mu\in\mathcal P(\mathcal A_n)}
      \min_{m\in\mathcal B_1}\mathbb E_\mu T(m,p)
 \le W_1.
\tag{13}
\]

For dyadic refinements, every old unit step subdivides into two
unit steps on the finer clock. Initial positions and endpoint
stopping remain admissible. Thus
\(\mathcal A_n\subseteq\mathcal A_{2n}\), and (13) proves
\[
 L_n\le L_{2n}.
\tag{14}
\]
This monotonicity follows by comparing Princess banks against
the **same full** Monster class, not merely by enlarging both
players' finite banks.

To prove convergence, fix a finite actual Princess law securing
more than some \(c<W_1\), as supplied by Section 2.
Its paths can be uniformly approximated by paths in the dyadic
banks. Here is a direct construction. Contract a path to
\(q(t)=(1-\eta)p(t)\), with \(\eta>2\Delta\).
Choose its first even-parity grid point within \(\Delta\) of
\(q(0)\). At each clock step choose the closer of the two
neighbors of the current grid point to the next sampled value
of \(q\). If the current error is at most \(\Delta\), the next
sample is at distance at most \(2\Delta\) from the current grid
point, so one of its two neighbors is again within \(\Delta\).
The contraction and \(\eta>2\Delta\) keep both neighbors inside
the arena. The polygonal interpolation has uniform error at
most \(2\Delta\) from \(q\), hence at most
\(\eta+2\Delta\) from the original path.

Choose \(\eta\downarrow0\) and dyadic \(\Delta\downarrow0\).
The approximants remain interior through time six and therefore
belong to the allowed bank. Apply (8) to the finite original
law. Its approximating grid laws eventually secure more than
\(c\); consequently \(L_{2^j}>c\) eventually. Since \(c<W_1\)
was arbitrary, (13)–(14) imply
\[
 \boxed{L_1\le L_2\le L_4\le\cdots,\qquad
        \lim_{j\to\infty}L_{2^j}=W_1.}
\tag{15}
\]

Several limits of this statement matter:

- No finite \(n\) is proved to attain \(W_1\).
- No numerical rate for \(W_1-L_n\) is obtained. Uniform path
  approximation does not supply a uniform Lipschitz bound on
  first-capture time; contact discontinuities are retained.
- The Monster dual of the finite matrix controls only its
  finite Princess bank. It is not automatically an
  all-Princess physical upper. Such an upper needs its separate
  complete causal-clock or physical-response certificate.
- The finite Princess bank may be very large. The theorem
  gives exact scope for a column-generation implementation,
  not a claim that the entire bank has been enumerated here.

In particular, if the strict target \(W_1>U_*\) is true,
some finite grid LP has \(L_n>U_*\). An exact search through
the dyadic hierarchy will eventually certify it. If
\(W_1\le U_*\), no termination of this lower search is
asserted. This is a complete search for positive separation,
not a decision procedure promised to halt in both cases.

## 6. Continuous piecewise-affine approaching laws

A finite rational law \(\mu=\sum_iw_i\delta_{p_i}\) can be
regularized by one independent
\(Z\sim\operatorname{Uniform}[-1,1]\) per selected trajectory:
\[
 p_\varepsilon(t)=(1-\varepsilon)p_i(t)+\varepsilon Z.
\tag{16}
\]
The paths stay in the arena, have speed at most
\(1-\varepsilon\), and differ uniformly from the original
paths by at most \(2\varepsilon\). Their one-time CDF is
\[
 F_\varepsilon(t,x)=
 \sum_iw_i
 \left[\frac{x-(1-\varepsilon)p_i(t)+\varepsilon}
                  {2\varepsilon}\right]_0^1,
 \qquad [y]_0^1=\min\{1,\max\{0,y\}\}.
\tag{17}
\]
For rational polygonal input and rational positive width this
is a legal continuous rational piecewise-affine CDF.
Common-quantile ordering of its marginals can only improve
security.

The compactness and joint-lower-semicontinuity argument in
Section 3, now followed by Fatou over \(Z\), gives
\[
 \liminf_{\varepsilon\downarrow0}
       \inf_{m\in\mathcal B_1}J(F_\varepsilon,m)
 \ge \inf_{m\in\mathcal B_1}J(\mu,m).
\tag{18}
\]
Thus the exact finite laws from (15), with sufficiently small
positive regularization widths, give continuous
piecewise-affine approaching laws with security tending to
\(W_1\). A strict finite-law lower above \(U_*\) implies a
continuous-law strict lower as well. No particular smoothing
width or finite optimal field is asserted without its own
all-parameter verification.

## 7. What this closes and what it leaves open

The earlier restricted-game bracket deliberately did not claim
a separate minimax identity. Equation (4) now supplies that
identity and an attained optimal Monster law for the precise
canonical one-turn class. Equations (11) and (15) give a complete
exact finite lower hierarchy, and (17) gives an explicit
continuous CDF representation for approaching laws.

The later [continuum countercertificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md)
proves \(W_1\le142472349375511/100000000000003<U_*\), resolving
the sign comparison negatively. The exact value of \(W_1\) and
whether \(W_1=V\) remain open. The minimax and approximation
theorems in this note remain valid independently of that comparison.
None of these theorems silently enlarges \(\mathcal B_1\) to
arbitrary waiting or variable-speed one-reversal Monsters, and
none solves the unrestricted game's exact equilibrium.

