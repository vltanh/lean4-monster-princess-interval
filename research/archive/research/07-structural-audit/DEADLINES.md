# Exact deadline characterization for arbitrary monster laws

## Status and scope

This note audits the finite deadline/envelope theorem in
`research/02-exact-response-reduction/REDUCTION.md` and extends its equality of
suprema to an arbitrary Borel probability law on monster paths. It does not
identify the unrestricted game value or bound the number of support paths in
an optimal law. The finite event/min-cut computation is still finite only when
the monster support is finite.

The extension is an analytic result. It has not been formalized in Lean.

## 1. Definitions, including atoms and terminal conventions

Fix a finite horizon H > 0 and an initial princess position x in [-1,1]. Let
M_H be the space of all 1-Lipschitz maps m:[0,H] -> [-1,1], with the uniform
metric. This is a compact metric space. Let nu be any Borel probability
measure on M_H.

For two continuous paths define tau_H(m,p) to be their first meeting time,
capped at H. In particular, its value is H if they do not meet before H. Set

    B_x = {m : m(0) < x},
    A_x = {m : m(0) > x},
    E_x = {m : m(0) = x}.

For m in B_x, let d_x(m) be its first visit to +1, capped at H. For m in A_x,
use its first visit to -1, capped at H. For b in B_x and a in A_x, let
alpha(b,a) be their first meeting time, capped at H.

An admissible deadline assignment is a Borel map r:M_H -> [0,H] such that

    r(m) = 0                                      for m in E_x,
    r(m) <= d_x(m)                               for m in B_x or A_x,
    min(r(b),r(a)) <= alpha(b,a)                  for every b in B_x, a in A_x.

The last condition is pointwise, including pairs outside the support of nu.
There is no cost to this convention: any assignment defined on a Borel set
can be extended by zero outside it, and all new pair constraints then hold.

Write D_x for this class of assignments and set

    Gamma_H(nu,x) = sup_{r in D_x} integral r(m) d nu(m).

### Measurability

For any s < H, the condition tau_H(m,p) > s is equivalent to

    min_{0 <= t <= s} |m(t)-p(t)| > 0.

The minimum is continuous in the uniform metric. Thus capped first-meeting
time is lower semicontinuous, hence Borel, as a function of the pair of
continuous paths. The same argument applies to alpha and to first visits to
either wall. Consequently the actual capture-time assignment of every fixed
continuous princess is a Borel map. Ties at time zero and at H are included.

## 2. The continuum deadline theorem

**Theorem.** For every nu, H and x as above,

    sup_{p(0)=x, Lip(p)<=1} integral tau_H(m,p) d nu(m)
      = Gamma_H(nu,x)
      = sup_{p(0)=x, p continuous} integral tau_H(m,p) d nu(m).

These are equalities of suprema. No maximizer is asserted on the princess
side or on the deadline side. In particular, this statement does not pass a
lower capture-time bound through a uniform path limit.

### 2.1 Necessity

Fix any continuous p with p(0)=x. Until its first encounter with b in B_x,
the princess stays strictly above b; until its first encounter with a in A_x,
she stays strictly below a. Therefore both cannot survive an opposite-side
meeting. A lower monster cannot reach +1 while remaining below the princess,
and an upper monster cannot reach -1 while remaining above her. A monster in
E_x captures her at time zero.

It follows that r(m)=tau_H(m,p) belongs to D_x. This proves that the rightmost
supremum is at most Gamma_H(nu,x).

### 2.2 Compact extraction of almost all weighted deadlines

Fix r in D_x, delta > 0, and eta > 0. Consider the finite Borel measures on
the compact metric product M_H x [0,H] obtained by pushing forward nu|B_x
and nu|A_x under m -> (m,r(m)).

The graph of a Borel real-valued map is Borel. Finite Borel measures on a
metric compact space are inner regular. We can therefore choose compact sets

    K_B contained in {(m,r(m)) : m in B_x},
    K_A contained in {(m,r(m)) : m in A_x},

whose projected path sets S_B,S_A satisfy

    nu((B_x union A_x) \ (S_B union S_A)) < eta.

The projections are compact, hence Borel. There is at most one pair (m,r(m))
above each m. The sets need not contain E_x: its deadlines are identically
zero and its actual capture times are identically zero. Thus an arbitrarily
large atom at the princess's starting position causes no problem.

Compactness inside B_x or A_x also puts the retained starting positions a
positive distance from x. This is why a pointwise finite-family argument
cannot simply be copied using unrestricted infinite suprema; the compact
extraction supplies the missing strict margins.

### 2.3 Infinite envelopes on the compact retained sets

For a retained pair (m,r(m)) put e_m=max(0,r(m)-delta). Define

    ell_m(t) = m(t)                       for t <= e_m,
               m(e_m) - (t-e_m)          for t >= e_m,   if m in S_B;

    u_m(t)   = m(t)                       for t <= e_m,
               m(e_m) + (t-e_m)          for t >= e_m,   if m in S_A.

Define the envelopes, with empty suprema/infima omitted,

    L(t) = max(-1, sup_{m in S_B} ell_m(t)),
    U(t) = min( 1, inf_{m in S_A} u_m(t)).

Every continuation is 1-Lipschitz. Supremum and infimum preserve this common
Lipschitz bound, so L and U are 1-Lipschitz.

Fix b in S_B and a in S_A, and put e=min(e_b,e_a). If e>0, then

    e < min(r(b),r(a)) <= alpha(b,a),

so b(s)<a(s) for all s<=e. If e=0, their initial order is strict. Once the
first constraint expires, its continuation moves away from the other at
speed one, which the other cannot exceed. After both expire they move apart.
Consequently ell_b(t)<u_a(t) for every t. Likewise ell_b(t)<1 and u_a(t)>-1:
the corresponding wall has not been reached before its shortened deadline,
and the continuation subsequently moves away from that wall.

The functions ell_m(t) and u_m(t) depend continuously on (m,r(m),t) on the
compact graph sets. For example,

    ell_m(t) = m(min(t,e_m)) - max(0,t-e_m).

The strict pairwise inequalities therefore have positive minima on
K_B x K_A x [0,H], and the wall inequalities have positive minima on the
respective compact products. Empty sides are handled by the walls. It
follows that L(t)<U(t) for every t, and that L(0)<x<U(0) when -1<x<1.

For an interior x choose

    lambda = (x-L(0))/(U(0)-L(0)),
    q(t) = (1-lambda)L(t) + lambda U(t).

Then q is 1-Lipschitz, q(0)=x, and lies strictly between every retained active
lower and upper constraint. Hence

    tau_H(m,q) >= r(m)-delta       for every m in S_B union S_A.

At x=-1 there are no lower monsters. Instead use q(t)=L(t)=-1, with the
same strict avoidance conclusion for all upper constraints until their
shortened deadlines; their wall deadline is their first visit to -1. At
x=+1 use the constant path +1. These boundary cases in fact attain their
wall-deadline upper bounds without an approximation.

### 2.4 Weighted conclusion

Capture times are nonnegative, deadlines are at most H, and r=0 on E_x.
Thus the constructed q satisfies

    integral tau_H(m,q) d nu(m)
      >= integral_{S_B union S_A} (r(m)-delta) d nu(m)
      >= integral r(m) d nu(m) - H eta - delta.

Let eta and delta tend to zero, and then take the supremum over r. This
proves the leftmost supremum is at least Gamma_H(nu,x). The reverse inclusion
of 1-Lipschitz princess paths in continuous princess paths completes the
proof.

## 3. Dependence on the princess's starting point

Let rho be the initial-position marginal of nu. For -1 <= x < y <= 1,

    -H rho((x,y]) <= Gamma_H(nu,y)-Gamma_H(nu,x)
                         <= H rho([x,y)).

To prove the first inequality, take an admissible deadline assignment at x
and set its deadlines to zero on monsters starting in (x,y]. Its remaining
nonzero deadlines have the same side classification, wall deadlines and
opposite-side constraints at y. The objective decreases by at most
H rho((x,y]). Take suprema. Apply the same argument from y to x, zeroing
starts in [x,y), for the other inequality.

Consequences:

* With finite monster support, the response supremum is constant throughout
  each open initial-position chamber. The value at a monster starting
  position is covered by neighboring upper bounds, since the corresponding
  paths capture at time zero.
* If rho has no atoms, Gamma_H(nu,x) is continuous in x. More quantitatively,
  its variation between x and y is at most H rho((x,y)).
* If rho has a density bounded by D, the response function is HD-Lipschitz.
  This permits a rigorous initial-position mesh error for a proposed
  continuum monster law, independently of its path-support cardinality.

## 4. Equal speed versus arbitrary continuous princess motion

For every fixed monster law, the best expected truncated capture time is
unchanged when the princess is permitted arbitrary continuous motion instead
of speed at most one. The same conclusion holds for untruncated expected
capture time, possibly infinite: for either princess class,

    sup_p E T(M,p) = sup_{H>0} sup_p E min(T(M,p),H),

by monotone convergence and the commutation of two suprema. Apply the theorem
at every H. Thus the monster's unrestricted upper value is also identical
for these two princess speed conventions.

This conclusion uses probability measures and approximation in payoff. It
does not assert a single 1-Lipschitz path with every capture time at least as
large as that of an arbitrary continuous path.

## 5. Audit of the earlier finite theorem

The following details are sound in the finite proof:

* Keeping the time-zero constraint when r_i=0 preserves the desired start;
  no positive capture-time guarantee is requested for that coordinate.
* Taking e_i=max(0,r_i-delta) creates strict separation before every relevant
  first contact, including tangencies and coincident later segments.
* A common speed bound of one is sufficient to preserve a positive gap after
  either constraint expires. Piecewise linearity is not needed here.
* Capture at time zero gives zero payoff, so chamber-boundary starts cannot
  violate an adjacent chamber's upper certificate.
* Rounding deadlines upward to event times preserves the deadline
  inequalities; the assertion concerns a supremum and need not produce an
  attaining princess.
* For a truncated game, cap all first-wall and first-meeting times at H.
  A common endpoint-to-endpoint sweep is not required. The earlier
  guaranteed-capture hypothesis merely allows replacing capped payoff by
  the full payoff.

The continuum extension does not make the event set finite. It provides a
precise functional optimization problem for a proposed continuum monster
strategy. A solution of the full game still requires a specific strategy and
an exact matching unrestricted lower guarantee.
