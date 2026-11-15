# A negative-M2 shift, with arbitrary-path boundary control

## 1. Setting

Use a symmetric signed-M1/M2 law M with endpoint mass w0, densities
f,g,h,ell, and total mass one, as in `SIGNED_M1_SUFFIX_REDUCTION.md`.
Assume f is nondecreasing. For the scalar response and stability statements
below, also assume f+g and h+ell are nondecreasing and the densities bounded.

Write S for its unrestricted princess response ceiling. By the reflected-
pair absolute-value comparison, nonnegative princess paths suffice. For
any such path p put

    a=p(0), U=t+p(t), V=t-p(t),
    A(r)=inf{t:U(t)>=r}, B(r)=inf{t:V(t)>=r},
    e_s=inf{t:U(t)>s}, c_s=V(e_s), c=c_1.

The last inverse e_s selects the end of a U=s plateau. Thus c_s is
nondecreasing in s. All inverse conventions in this note are literal.

For 0<eta<1 replace only each negative-parameter M2(-z), 0<=z<=1,
by the path with vertices

    (0,-z), ((1+eta+z)/2,(1+eta-z)/2),
    (2+eta,-1), (4+eta,1),

and reflect fairly. All these paths are legal. Keep every other component
of M unchanged, obtaining M_eta. Positive M2 starts are not moved.

## 2. A global cap lemma controls both late inverse traces

Define

    B0(a)=w0+mu_2((-a,1]),
    T0(c)=mu_2([-1,-c)).

The endpoint conventions omit reflected initial coincidences and include
only old late unreflected M2 captures.

**Trace lemma.** For every admissible nonnegative p,

    S-J_M(p)
      >= [B0(a)(2-B(1))+T0(c)(4-B(3))]/2.               (1)

This includes a=1, c=1, initial coincidences, and U/V plateaus. It does
not assume that p is a four-parameter representative or reaches an
endpoint by time two.

### Construction and quantitative proof

Represent the characteristic path as its nondecreasing graph V(U), with
vertical segments retained. For 0<delta<1, replace it by

    V_delta(U)=min(V(U),1-delta)      for U<=3-delta,
    V_delta(U)=U-2                  for U>=3-delta.     (2)

The initial point (a,-a) is unchanged. The graph is legal: clipping V
downward preserves V<=U; before the junction, both entries of the minimum
are at least U-2. At U=3-delta feasibility forces V>=1-delta, so the
pieces join continuously. The new path reaches +1 at time 2-delta and
then stays there. Consequently

    B_delta(1)=2, B_delta(3)=4,
    c_delta=min(c,1-delta).

Every B inverse weakly increases. Every A inverse at a threshold at most
one advances by at most delta/2: its V coordinate can decrease only from
a value at most one to 1-delta. This assertion also holds at a vertical
plateau's first point, so it does not replace a first inverse by a last
inverse.

The M2 cutoff can only decrease. Thus old late unreflected M2 parameters
stay late, and old early parameters changed by the cutoff become late;
this change increases their capture times. The old reflected B(1) terms
gain exactly 2-B(1), and the old unreflected B(3) terms gain exactly
4-B(3). All remaining B changes are favorable.

Only A terms can lose. The total mass of A terms at thresholds at most
one is at most w0+integral ell+mu_2([-1,1]); their pair-weighted loss is
at most delta/4 times that mass.

For the positive M1 component, use its graph score. On 1<U<2-a its
alpha density is f(2-U), and its beta tail has density f(2-V) on (1,2).
For 1<=V<=U<2-a, monotonicity of f gives

    integral_1^V f(2-r)dr >= f(2-U)(V-1).

Thus clipping to the limiting level 1- cannot decrease this component's
score. Clipping instead to 1-delta can lose at most delta*f(2-U).
Outside the active alpha interval, lowering V only improves the beta
tail. After integration, its pair-weighted loss is at most
delta*Fbar(a)/4, hence at most delta/4 times the positive M1 mass.

Normalization therefore gives the finite-delta inequality

    J_M(p_delta)-J_M(p)
      >= [B0(a)(2-B(1))+T0(c)(4-B(3))]/2-delta/4.       (3)

Since J_M(p_delta)<=S, let delta decrease to zero to prove (1).
This proof explicitly pays for every possible A-threshold advance;
no continuity of capture times is assumed.

## 3. An exact shift identity for every path

Write c_eta=c_(1+eta), and interpret h as zero outside [0,1]. Let

    H_<(a)=integral_[0,a) h(z)dz,
    H_>(v)=integral_(v,1] h(z)dz.

For density laws the endpoint choices do not change the integrals. Direct
capture comparison gives

    2[J_(M_eta)(p)-J_M(p)]
      =H_>(c_eta)[B(3+eta)-B(3)]
        +H_<(a)[B(1+eta)-B(1)]
        -integral_(c,c_eta] [B(3)-B(z)]h(z)dz.          (4)

Old early unreflected captures remain early. Newly early captures are
exactly c<z<=c_eta. Reflected captures A(z), when z>a, are unchanged;
when z<a their B(1) threshold moves to B(1+eta). At z=a both reflected
captures are the same initial coincidence. These observations prove (4)
without any restriction on the princess's number of turns.

Since B(3+eta)<=4+eta and B(1+eta)<=2+eta, the positive terms in (4)
are controlled by (1). Indeed H_>(c_eta)<=T0(c), H_<(a)<=B0(a), and
their sum is at most twice the total h mass H(1). Therefore

    J_(M_eta)(p)
      <=S+eta H(1)
        -(1/2) integral_(c,c_eta] [B(3)-B(z)]h(z)dz.    (5)

For z in [0,1], B(3)>=3 and B(z)<=1+z<=2, so the integrand's factor
is at least one. A necessary condition on any proposed matching lower
sequence lambda_n is consequently

    limsup_n E_lambda_n H((c,c_eta]) <= 2 eta H(1)      (6)

for every fixed eta, provided its payoffs against M and each fixed
M_eta tend to at least S. This is an arbitrary-path necessary condition,
not a statement only about chosen extremal representatives.

## 4. Exact no-extra and extra-leg comparisons

### No extra leg

For a four-parameter prefix followed by its original outward suffix,
with c<1, B(1)=2 and B(3)=4. For every z in [0,1],

    pair payoff change
      =eta/2 * [1_(z>c)+1_(z<a)].                       (7)

This is uniform as a tends to one and as c tends to -a. If c is so
negative that the princess reaches the endpoint before U=1+eta, the new
cutoff is eta-1<0; every z>=0 still has the same late/early classification.
Thus this boundary does not invalidate (7).

At exact c=1, (7) need not hold: B(1) may be less than two. Formula (4)
retains the resulting penalty. A regularization with final outgoing
characteristic strictly below one has B(1)=2 and does satisfy (7), even
if the regularization scale is much smaller than eta. Merely lifting a
central wait spatially while retaining an outgoing V=1 plateau does
not ensure that property; the trace lemma is needed for such paths.

### A positive extra leg

Take 0<=c<y<1, and place the inward leg at U=1+epsilon. If
0<epsilon<eta<1, then c_eta=y and

    4[J_(M_eta)-J_M]
      =2 eta[H_>(y)+H_<(a)]
        -integral_c^y (7-epsilon-z)h(z)dz.             (8)

The new capture of z in (c,y] is at (1+epsilon+z)/2 instead of four.
Every positive term in (8) is O(eta), independently of the starting
point or the length of the earlier central wait.

For a scalar tuple with deficit d=S-K(a,u,c,y), monotonicity of
k=h+ell and the exact c derivative imply

    integral_c^y (7-z)h(z)dz >= w0(y-c)-4d.             (9)

To see this, integrate K_c while raising c to y at fixed a,u,y. With
q=max(u,z), its derivative can be written

    4K_c=w0+Gbar(a)-(7-z)h(z)+E(u,z),
    E(u,z)=K0bar(q)-(1-q)k(z)>=0.

The endpoint tuple K(a,u,y,y) is at most S. This proves (9), including
prefix branch changes during the integral. Equations (8)-(9) show that
negative M2 shifts alone remove every positive-extra scalar maximizer
by a definite amount proportional to y-c, while no-extra responses
have only the O(eta) increase in (7).

## 5. A strictness lemma for arbitrary near-best suffixes

Here is an explicit sufficient condition for transferring that conclusion
away from representatives. Fix alpha,kappa>0 and consider paths with

    a<=1-alpha,  0<=c<=1-kappa.

Assume f is absolutely continuous and f'>=gamma>0 almost everywhere
on every relevant interval [a,1]. Let M0 bound f+ell. Apply the cap
construction with delta<kappa, so a,c are unchanged. Write q=p_delta,
d_q=S-J_M(q), L=2-a, and let V be q's suffix graph on [1,L].
The finite-delta trace bound gives
`d_q<=S-J_M(p)+delta/4`, which is the deficit comparison used below.

The opposite-Chebyshev deficit in the global suffix proof is at most
4d_q. Strict decrease of f(2-U) bounds it from below by

    (gamma/2) integral_1^L (U-1)(L-U) dV(U).

Hence, for 0<eta<alpha/4,

    V(L-eta)-V(1+eta)
      <=8d_q/[gamma eta(alpha-eta)].                    (10)

Put v=V(1+eta), using the upper end of a vertical segment. On the two
end strips of total length 2eta, all relevant V values lie in [0,1].
On the middle strip, (10) controls their variation. The suffix score
has Lipschitz constant at most M0 in V below one. Replacing it by the
constant level v and using the minimal continuation therefore loses at
most

    M0 eta/2+2M0 d_q/[gamma eta(alpha-eta)]              (11)

in expected payoff. Optimizing the prefix at the same a,c cannot make
the payoff smaller. Consequently some scalar tuple (a,u,c,v) satisfies

    S-K(a,u,c,v)
      <=d_q[1+2M0/(gamma eta(alpha-eta))]+M0 eta/2.       (12)

The original path's c_eta is at least v, because the cap only lowers V.
Combining (9), (12), and (6) shows that a matching near-best lower
sequence cannot carry positive mass on a compact region whose scalar
near-maximizers require v-c bounded away from zero. The limit order is
fixed eta first, then the near-best limit and delta to zero, and only
afterward eta to zero.

### One precise whole-law exclusion under strict localization

Suppose w0>0 and there are alpha,kappa,lambda,d0,gamma>0 such that:

* f'>=gamma on the relevant suffix intervals;
* every scalar tuple with K>=S-d0, including its one-sided boundary
  limits, has a<=1-alpha and 0<=c<=1-kappa;
* every such tuple has y-c>=lambda.

Then M is strictly improvable by a finite mixture of M and negative-M2
shifted laws M_eta. Otherwise finite-row minimax, applied to M and the
countable shifts eta_j decreasing to zero, would give princess laws
near best against M and with payoff approaching S against every fixed
shift. The global four-parameter response theorem localizes their a,c
parameters except for vanishing mass. Equations (10)-(12) then produce
near-maximal scalar tuples with v-c>=lambda, while (6) and (9) force
their average v-c to vanish. This contradiction is the same finite-row
argument used in `SUFFIX_GAP_EXCLUSION.md`; bounded capture horizons
justify the compact payoff-vector construction.

This theorem excludes arbitrary near-best paths under explicit strictness
and localization assumptions. It does not assume that the original
princess law was supported on the four-parameter representatives.

## 6. A local exclusion even when no-extra responses remain active elsewhere

The preceding whole-law localization is stronger than necessary. A
positive M1 density itself forces a matching lower law to put initial
mass in selected parameter intervals. This permits a local exclusion.

### A finite-row initial-mass estimate

Choose 0<l<r<1 and a subinterval J of [l,r) whose right endpoint is
at most r-d for some d>0. Suppose

    w=integral_J f(x)dx>0.

Let F_J be the normalized reflected M1 mixture on J, and let M_rest
be the normalized law obtained by removing that component from M. Thus
M=w F_J+(1-w)M_rest. Since w0>0, w<1. Write F_r for the single
reflected M1(r) pair and I=[l,r].

If p starts outside I, its unreflected M1 first-inverse branch is the
same for every x in J and at r. Each of its two thresholds decreases
by r-x. Both U and V have speed at most two, so their first inverses
decrease by at least (r-x)/2. Consequently

    F_r(p)-F_J(p)<=-d/2          when a is outside I.

For a inside I the difference is at most three, since all the relevant
M1 paths complete their sweeps by time three. Hence

    F_r(p)-F_J(p)<=-d/2+(3+d/2)1_(a in I).              (13)

Suppose a princess law has payoff at least S-epsilon against both
M_rest and F_r. Its M payoff is at most S, so its F_J payoff is at
most S+(1-w)epsilon/w. Equation (13) then gives

    Pr(a in I)>=[d/2-epsilon/w]/(3+d/2).                (14)

Thus any matching sequence against these fixed rows has limiting
initial mass at least rho_star=d/(6+d)>0 in I. No canonical princess
shape, density of initial positions, or derivative of a capture payoff
is used in this estimate.

### Local scalar assumptions

Assume there are m,kappa,lambda,d0>0 such that:

1. `ess_inf_[l,1] f >= ess_sup_[0,1] ell + m`.
2. Every scalar tuple with a in I and K>=S-d0, including boundary
   payoff limits, has `0<=c<=1-kappa` and `y-c>=lambda`.

No assumption is made about scalar maximizers with a outside I; they
may include central waits, endpoint starts, and no-extra branches.

The first condition replaces strict f' by a strict suffix score. For
a in I, Abar=Fbar(a)/(1-a) exceeds every positive ell density by at
least m. For a capped suffix graph ending at level y on [1,2-a], the
constant-y replacement and minimal continuation therefore gain at least

    (m/4) integral_1^(2-a) [y-V(U)]dU.                  (15)

This is the positive-strip stability estimate from the signed suffix
theorem. A cap below one ensures that no B=1 atom lies inside the
comparison interval.

### Strict improvement using four rows

**Local exclusion theorem.** Under the preceding assumptions, M is
strictly improvable by a mixture of M, M_rest, F_r, and one sufficiently
small negative-M2 shifted law M_eta.

For the proof, suppose that this finite row game had value S. Finite-row
minimax supplies princess laws lambda_n whose payoffs against every row
approach at least S. Their M deficits tend to zero. By (14), their
initial mass in I has liminf at least rho_star.

Apart from vanishing mass, paths in I have individual deficit less than
d0. Fixed-a,c upper reduction and assumption 2 put their c in the stated
compact positive range. Apply the cap with delta_n decreasing to zero
and smaller than kappa. Its deficit d_q is at most the original deficit
plus delta_n/4. Let y be the capped graph's value at U=2-a. The
constant-y replacement, followed by prefix optimization, gives a scalar
tuple with K>=J_M(q), so y-c>=lambda on the near-best part of I.

For fixed 0<eta<1-r, (15) implies

    y-V(1+eta)<=4d_q/(m eta).

Using (9), and writing ||h||_infinity for a bound on h, the original
path therefore satisfies

    H((c,c_eta])
      >=w0 lambda/7
        -d_q[4/7+4||h||_infinity/(m eta)]               (16)

on that near-best part. The cap only lowers c_eta, so the comparison
also applies to the original path. Integrating and passing n to infinity
gives a lower bound w0 lambda rho_star/7. In contrast, the fixed shifted
row and (6) give the upper bound 2eta H(1). Choose

    0<eta<min(1-r, w0 lambda rho_star/[14H(1)]).

These bounds contradict one another. If H(1)=0, (9) contradicts the
positive-extra near-best mass forced into I by (14). The response ceiling over the finite row simplex attains
its minimum, so failure of equality with S gives a strict improvement.

This is an arbitrary-near-best exclusion for a mixed active set. Its
remaining numerical or analytic obligation for a proposed law is the
explicit local scalar gap in assumption 2, not a path-space stability
claim. The high positive-f / lower negative-M1-density terminal region
in the discovery is compatible with assumption 1. The separate exact
certificate in [`LOCAL_SCALAR_GAP.md`](LOCAL_SCALAR_GAP.md) verifies both
local assumptions for an explicitly rationalized and normalized version
of that discovery law. It thereby gives a concrete application of this
theorem; it does not treat the original floating-point array as exact.

### An explicit improving mixture

The same estimates give a concrete mixture and improvement amount, so
the finite-row existence argument need not be the final step. Define

    D=d/2, E=3+D, L0=w0 lambda/7, omega=L0/(2E).

Choose 0<eta<1-r with eta H(1)<omega D, and set

    Cstar=max{4/7+4||h||_infinity/(m eta),
              L0/d0, 2omega/w}.                         (17)

If H(1)=0 the local hypotheses are inconsistent, as above. Otherwise
such eta exists. All constants can be rational when the density and
local-gap data are rational.

For every path p, with d_p=S-J_M(p), the estimates extend to

    H((c,c_eta]) >= L0 1_(a in I)-Cstar d_p.             (18)

For a in I and d_p<d0, take cap scales delta smaller than both kappa
and 4(d0-d_p). The projected scalar tuple stays in the near-maximal
set, so (16) applies with d_q<=d_p+delta/4. Let delta decrease to zero.
If d_p>=d0, (18) is immediate from Cstar>=L0/d0. Outside I it is
immediate from nonnegativity of H and d_p. This proves (18) pointwise,
without a limiting princess law.

Combine (5), B(3)-B(z)>=1, and (18) to obtain

    J_(M_eta)(p)
      <=S+eta H(1)-(L0/2)1_(a in I)+(Cstar/2)d_p.

Add omega times (13). Since omega E=L0/2, the initial-mass terms
cancel. Substitute F_J=[M-(1-w)M_rest]/w and move the remaining
J_M term to the left. The following nonnegative coefficients result:

| Monster law | Unnormalized coefficient |
| --- | --- |
| M | Cstar/2-omega/w |
| M_rest | omega(1-w)/w |
| F_r | omega |
| M_eta | 1 |

Their sum is Z=1+Cstar/2. The first is nonnegative by (17). The
normalized mixture therefore has, against every princess path, payoff
at most

    S - [omega D-eta H(1)]/[1+Cstar/2] < S.             (19)

Symmetry extends the inequality from nonnegative paths to arbitrary
paths. Formula (19) gives an explicit strict improvement once the local
gap is certified; computing S itself is unnecessary. An explicit scalar
witness W<=S and a bad-set upper bound below W suffice to obtain d0.

## 7. Scope of the exclusion and the remaining equilibrium problem

The signed-density discovery has both no-extra and positive-extra active
responses. It therefore does not satisfy the last localization condition
in Section 5, and f has flat pieces, so its derivative strictness also
needs separate treatment there. Section 6 permits those other active
branches and flat f pieces. Its local gap has now been verified exactly
for the rational law in `LOCAL_SCALAR_GAP.md`: that fixed law is strictly
improvable against arbitrary princess paths by the explicit mixture
in (19). This closes the candidate-exclusion argument, not the game.

For a broader signed-M1/M2 candidate whose local scalar gap fails, the
remaining possibilities include:

* quantitative control of every flat suffix/prefix equality region,
  followed by an unrestricted attack on the surviving no-extra responses;
* or a matching lower construction that survives (6), which would have
  to use those equality regions in a substantively different way.

Uniform closeness of princess trajectories is not by itself enough for
the first option: first capture is only lower semicontinuous, and an
early crossing can disappear under perturbation. A proposed transfer
must give an explicit capture-order or deadline inequality for the new
attacking monsters. This is the exact remaining stability obligation,
not an assertion that the representative-level calculation already
excludes the full signed-M1/M2 class.
