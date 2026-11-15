# Global response recurrence by survival halving

## CORRECTION (2026-11-13): a probability threshold is not a strategic phase

The phrase "a recurrent optimal response strategy" in the original summary
is **too strong**. This is an *exact dynamic-programming decomposition*
of the response against a **given F**, NOT a discovered invariant family,
turning rule, strategic switching threshold, or characterization of the
optimal two-player equilibrium. The Monster may travel straight
through the probability-halving event without any control change.

### All thresholds work — 1/2 has no equilibrium significance

For any fixed \(0<\rho<1\), set
\[
 H_\rho=\max(4,2/\rho),\qquad
 {\cal A}_{F,\rho}(z)=\{\gamma:
       \gamma(0)=x,\ 0<\tau\le H_\rho,\
       S_\tau\le\rho S(z)\}.
\]
Keep the same exact state update and phase capture integral from
(4)--(6), and define
\[
 (\mathcal T_{F,\rho}g)(z)
 =\inf_{\gamma\in{\cal A}_{F,\rho}(z)}
     \bigl[c_z(\gamma)+
            (S_\tau/S(z))g(z_\tau)\bigr].
\]
Then for **EVERY** transport-legal ordered CDF \(F\):
\[
 \boxed{W_F=\mathcal T_{F,\rho}W_F,\qquad
 \|\mathcal T_{F,\rho}g-\mathcal T_{F,\rho}h\|_\infty
       \le\rho\|g-h\|_\infty.}                         \tag{A}
\]
For starting bounds \(l_0=0,u_0=2\), repeated application
gives valid brackets \(l_n\le W_F\le u_n\) and uniform width
\[
 \boxed{\|u_n-l_n\|_\infty\le2\rho^n.}                \tag{B}
\]
For the proof, an optimal unrestricted response exists and
has \(W_F\le2\). Before the first drop to survival fraction
\(\rho\), its survival is greater than \(\rho\), hence that
stopping time is at most \(W_F/\rho\le2/\rho\).
Right-continuity of the survival function includes atoms,
and the exact expectation splitting gives both Bellman
inequalities. The class of phase prefixes still includes
**all** legal controls, regardless of turn count. The
full endpoint tours fit in \(H_\rho\ge4\) and provide
a feasible complete action with total cost \(\le2\),
making the initial bracket invariant. Standard
contraction gives (B).

There is NOTHING strategically special about
\(\rho=1/2\). Any \(\rho\) is a bookkeeping choice,
trading recursion depth against the length and
complexity of the still-infinite-dimensional phase
optimization. This is mathematically valid, but it
does **not** solve or reduce the difficult part of
the original equilibrium problem.

### Example: optimal route crosses half without changing control

Take the **fixed-start** response problem for three
stationary equally weighted Princess positions
\(-1,0,1\), with Monster start at \(-1\).
The -1 Princess is caught at time zero.
Conditionally the survivors are 0 and 1,
each with probability 1/2. The unique
time-optimal capture *times* are 1 and 2,
attained by the single uninterrupted
rightward unit-speed sweep
\(m(t)=-1+t,\ 0\le t\le2\).
Its conditional cost is
\((1+2)/2=3/2\), since speed one forbids
meeting 0 before time 1 or 1 before time 2.

At time 1 its surviving conditional mass
drops from 1 to 1/2; the Monster does **not**
turn, wait or change speed there. This is a
literal optimal-response counterexample to
interpreting the halving clock as a
physical action-switching law.

### No-threshold Bellman semigroup

There is also a threshold-free exact DPP.
For ANY finite \(h>0\) and a fixed F:
\[
\boxed{
R_F(z)=\inf_{\substack{\gamma:[0,h]\to[-1,1]\\
                     \gamma(0)=x,\ |\gamma'|\le1}}
 \left[\int_0^h S_u\,du+
                 R_F(t+h,\gamma(h),a_h,b_h)\right],
}                                                     \tag{C}
\]
where \(R_F(z)=S(z)W_F(z)\), with exact
record updates (4). This follows solely by
splitting an arbitrary full legal Monster
continuation at elapsed time h; it does not
presuppose a turn, phase transition, or
survival threshold. Its local HJB/variational
form is already in the repository's global
CDF Bellman research.

But (C) is the usual dynamic-programming
identity: it gives neither an explicit
optimizer nor a low-dimensional invariant
family. **The hard part remains the
unrestricted minimization over paths
together with identifying the equilibrium
Princess CDF and the all-Princess Monster
dual certificate.**

**Research decision:** Do NOT use halving
as an equilibrium hypothesis, optimize a
half-phase as an assumed component of the
optimal Monster support, or claim this
theorem is a constructive recurrence for
the unknown equilibrium. A substantive
future recurrence would have to be
DERIVED from the coupled global saddle
conditions, with provable closure of its
posterior/occupation class; absent that,
the honest result is only a DPP and
uniform truncation estimate.

---


Date: 2026-11-13. **Analytic response recurrence, not an evaluated equilibrium.**

The previous work has increasingly described complete paths, local turn patterns, and necessary support restrictions. Those are not a generative description of the optimal response. This note instead restarts the same response problem whenever the remaining probability is reduced by at least half.

**Main result.** For every fixed legal ordered Princess field, the unrestricted Monster response is the unique bounded fixed point of an explicit survival-halving Bellman operator. The operator contracts by at most 1/2, has a uniform four-time-unit phase horizon, and requires only time, Monster position, and two rank cutoffs as its dynamic state. Arbitrarily many turns are allowed *inside* each phase. Starting with lower/upper continuation values 0 and 2 gives a uniform response bracket of width at most 2^(1-n) after n phases. This holds without assuming any Princess endpoint-absorption time.

**Crucial remaining difficulty:** an exact application of this operator still requires a continuous-state, finite-horizon control optimization. The theorem is NOT a finite action reduction, a practical exponential-time/accuracy algorithm, or a construction of the unknown equilibrium CDF. It replaces an unbounded turn-count hierarchy with one recurrent response problem and a rigorous stopping criterion.

## 1. Exact sufficient state and survivor restart

Fix ordered legal quantile paths q -> p_q(t), q uniform on (0,1). Write F^-(t,x)=Pr(p_q(t)<x) and F^+(t,x)=Pr(p_q(t)<=x). Along a Monster history ending at (t,x), let

    a = inf_{s<=t} F^-(s,m(s)),
    b = sup_{s<=t} F^+(s,m(s)).

Up to null rank endpoints, the survivors are exactly (0,a) union (b,1). The post-contact state is

    z=(t,x,a,b),
    0<=a<=F^-(t,x)<=F^+(t,x)<=b<=1,
    S(z)=a+1-b.

This rank-state compression was already present in the global Bellman notes; it is not a new claim here. See [GLOBAL_CDF_BELLMAN.md](../10-turn-density/GLOBAL_CDF_BELLMAN.md) and [GLOBAL_CDF_TRANSPORT_LP.md](GLOBAL_CDF_TRANSPORT_LP.md).

What is useful for a recurrence is its exact **conditional restart**. If S>0, the remaining normalized Princess CDF, with time reset to zero, is

    F_z^+(u,y) = [min(a,F^+(t+u,y)) + (F^+(t+u,y)-b)_+] / S,
    F_z^-(u,y) = [min(a,F^-(t+u,y)) + (F^-(t+u,y)-b)_+] / S.       (1)

Proof: intersect the lower quantile interval of mass F^+ (or F^-) with the two surviving rank tails and divide by S. The remaining paths are restrictions of the original legal paths, so they are still 1-Lipschitz and ordered after reindexing. No independence or memoryless assumption is introduced.

Define W_F(z) to be the minimum expected **additional time**, conditional on this survivor law, over all legal Monster continuations starting at x. Set W_F=0 at S=0. The unnormalized remaining contribution is R_F(z)=S(z)W_F(z).

For fixed F, the entire past affects the future response only through these four state variables. The future field F(t+u,y) remains part of the fixed problem data; the claim is NOT that arbitrary Princess fields have a four-parameter representation.

### Why one survivor mass or one symmetric record is insufficient

Take four stationary Princess positions -1,-1/2,1/2,1 with equal weights. At time 2 and Monster position 0 compare two feasible histories:

* Start at -1/2, visit +1/2 by time 1, return to 0 by time 3/2, and wait. Only the two outer endpoints survive: a=1/4,b=3/4,S=1/2. The conditional optimal remaining mean time is (1+3)/2=2.
* Start at -1, go to 0 by time 1, and wait. Only +1/2 and +1 survive: a=0,b=1/2,S=1/2. A rightward sweep captures them at 1/2 and 1, giving conditional value 3/4; the speed bound proves optimality.

The same t,x,S and same original symmetric F have different continuation values. The two rank cutoffs cannot simply be discarded. Symmetry of an *averaged dual law* does not erase this pathwise survivor information.

## 2. Uniform conditional bound: W_F(z)<=2

This bound is stronger than the length-three nearest-endpoint completion bound.

From any fixed current position x, consider L: go at unit speed to -1 and then +1, and R: go at unit speed to +1 and then -1. Both finish by time 4.

For any continuous target p with p(0)<x, the first leftward leg catches it by 1+x, while the R tour catches every target by 3-x. Therefore T(L,p)+T(R,p)<=4. If p(0)>x, interchange L and R. If p(0)=x, both capture times are zero. Thus, pointwise for all target paths,

    [T(L,p)+T(R,p)]/2 <= 2.                            (2)

After averaging over any survivor law, at least one of the two deterministic tours has conditional cost at most 2. Consequently

    0 <= W_F(z) <= 2                                    (3)

uniformly in F, time, current position and both records. This does not assume a moving-target template or symmetry. The endpoint-sweep principle is also consistent with Proposition 1 of Alpern, Fokkink, Lindelauf and Olsder, *The Princess and Monster Game on an Interval*, SIAM J. Control Optim. 47 (2008), DOI 10.1137/060672054.

For each fixed survivor law and starting position, an optimal continuation exists: the legal path space is compact in the local-uniform topology; first-contact time is lower semicontinuous in the Monster path; Fatou preserves lower semicontinuity of its expectation; and (2) supplies a finite competitor. This is minimization-side compactness only, not Princess attainment.

## 3. Define the exact half-survival phase operator

Start from z=(t,x,a,b) with S>0. For a legal Monster prefix gamma:[0,tau]->[-1,1], gamma(0)=x, define updated records and surviving mass at elapsed time u by

    a_u = min(a, inf_{0<=v<=u} F^-(t+v,gamma(v))),
    b_u = max(b, sup_{0<=v<=u} F^+(t+v,gamma(v))),
    S_u = a_u+1-b_u,
    z_u = (t+u,gamma(u),a_u,b_u).                       (4)

Let A_F(z) contain **all** such prefixes whose length satisfies

    0 < tau <= 4,       S_tau <= S/2.                   (5)

The stop need not be the first halving; full completion is also allowed. This matters for the simple uniform upper iteration below. There is no restriction on the number of turns, speed changes, waits, or accumulations inside gamma.

For each prefix define

    c_z(gamma) = (1/S) integral_0^tau S_u du,
    beta_z(gamma) = S_tau/S in [0,1/2].                 (6)

The first quantity is the expected elapsed cost of this phase, conditional on survival at its start. It is NOT the geometric duration tau: targets caught earlier stop contributing.

For a bounded continuation function g, define

    (T_F g)(z) = inf_{gamma in A_F(z)}
                 [c_z(gamma) + beta_z(gamma) g(z_tau)]. (7)

Use zero continuation when S_tau=0, and T_F g=0 at S=0. The action set is nonempty because either full endpoint tour completes within four units. All quantities retain strict/closed first-contact conventions; no differentiability is used.

### Exact recurrence theorem

    W_F = T_F W_F.                                     (8)

Proof, first direction: append an optimal (or arbitrarily close) continuation to any admissible prefix. Conditional expectation and (4) split its full additional cost exactly as c+beta W_F(z_tau). Thus W_F<=T_F W_F.

For the opposite direction, take an optimal full continuation from z. Its surviving fraction S_u/S is the survival function of its first-capture time: nonincreasing and right-continuous. At u=0 it is one because the state is already post-contact. Let tau be the first time this fraction is at most 1/2. It exists because the expected time is finite. Before tau the fraction exceeds 1/2, so

    W_F(z) >= (1/2) tau.

Together with (3), tau<=4. Right-continuity gives S_tau<=S/2. This prefix is in A_F(z). The remaining part has cost at least W_F(z_tau), proving W_F>=T_F W_F. This also handles atoms that jump across the half-mass threshold.

The recurrence uses the same physical response problem again, with conditional CDF (1). It is not a fresh minimax game in which the Princess observes the Monster's private state and chooses a new law.

## 4. Contraction, certified iteration and residuals

For any two bounded continuation functions g,h,

    ||T_F g - T_F h||_infinity <= (1/2)||g-h||_infinity. (9)

Indeed each action has the same immediate cost and a continuation coefficient at most 1/2; taking infima preserves the bound. T_F maps bounded functions to bounded functions, since phase costs are at most 4 and full-completion actions have zero continuation. Banach's contraction theorem gives a unique bounded fixed point, which by (8) is W_F.

Set l_0=0 and u_0=2 on positive-survival states, with both zero at S=0, and iterate l_{n+1}=T_F l_n, u_{n+1}=T_F u_n. Nonnegative costs give T_F 0>=0. Full endpoint tours plus (2) give T_F 2<=2. Monotonicity and contraction therefore yield

    l_n <= l_{n+1} <= W_F <= u_{n+1} <= u_n,
    ||u_n-l_n||_infinity <= 2^(1-n).                  (10)

These are uniform across all times and survivor states and, importantly, across all legal ordered F. The depth n counts **probability-halving phases**, not physical turns. After n executed phases the remaining probability is at most 2^(-n); infinite internal switching is not excluded.

If a bounded candidate g satisfies the globally certified residual

    ||g-T_F g||_infinity <= eta,

then

    ||g-W_F||_infinity <= 2 eta.                       (11)

Similarly, a bounded g<=T_F g is a global lower response certificate; a bounded g>=T_F g is an upper response certificate. These implications follow by iteration and do not require an unproved infinite-horizon terminal condition. A residual measured only on sampled states is NOT a global certificate.

### Consequence for the original minimax value

At a free initial Monster position x use z_x=(0,x,F^-(0,x),F^+(0,x)); immediate contact mass contributes zero. For fixed F its security is

    B(F)=inf_x S(z_x) W_F(z_x).

If v_n=sup_{F legal ordered} inf_x S(z_x) l_n^F(z_x), then

    v_n <= V <= v_n+2^(1-n).                          (12)

Common-quantile dominance justifies optimizing over ordered fields. Equation (12) is an exact accuracy hierarchy for the full game, **not a finite-dimensional solver**: all fields and all phase controls remain included. No numerical value v_n has been computed here.

## 5. A recursive policy, rather than a path catalogue

For a supplied F, select a phase minimizer in (7) for g=W_F, execute the phase if capture has not already occurred, update (4), and repeat with the survivor law (1). This generates an optimal response rather than assigning probabilities to named M1/M2/... routes. Optimal full continuations supply minimizing phases; near-minimizing phases can be used when implementing approximations.

The Monster does not observe the Princess's quantile. All state variables and the phase termination rule are computable from F and the Monster's own chosen history; an actual encounter simply terminates play. Thus the recurrence introduces no forbidden observation.

If infinitely many phase times accumulate, the concatenated unit-Lipschitz path extends continuously to that time. After n phases the survivor mass is <=2^(-n), so the limiting exceptional ranks have measure zero. This is probability accounting, not an assumption of favorable first-hit continuity.

A full optimal Monster mixed strategy could be represented by an initial distribution and a policy kernel supported on Bellman-minimizing phases. However, a best response to F is NOT automatically a minimax Monster strategy. To solve the game one must still establish a common value c and the reverse all-Princess inequality for the resulting Monster law.

## 6. How to evaluate a phase without enumerating complete paths

Equation (7) is a finite-horizon control/stopping problem in the same four state variables. Its stopping region is S_u<=S_0/2; its stop payoff is (S_u/S_0)g(z_u); its running cost is S_u/S_0; and the elapsed phase horizon is four. This is the appropriate target for a characteristic/obstacle solver, with exact atom/reset treatment, rather than a growing path bank.

On smooth interior CDF patches, set d=F_t+vF_x. The unnormalized remaining value R=S W has dynamics

    adot=min(d,0) when a=F, otherwise 0,
    bdot=max(d,0) when b=F, otherwise 0,

and its formal differentiable Bellman equation is

    0=S+R_t+min_{|v|<=1}[v R_x+adot R_a+bdot R_b].     (13)

For the actual value R, adding surviving lower ranks or upper ranks cannot improve the Monster's cost, so R_a>=0 and R_b<=0 wherever these derivatives exist. The Hamiltonian is then concave in v, and a minimizing speed can be taken from {-1,+1} on such a smooth patch. If those monotonicity conditions are not established for an approximate potential, retain the tracking speed -F_t/F_x as an additional critical speed. At singular interfaces, atoms, and Zeno accumulations, use the integral operator (7), not an unsupported smooth PDE extrapolation.

There is also an exact spatial boundary condition without any target-absorption horizon. At x=-1, a=0 and the rightward unit sweep dominates every other continuation, so

    W_F(t,-1,0,b) = integral_0^2
      [1-max(b,F^+(t+u,-1+u))]du / (1-b).

At x=+1, b=1 and the leftward sweep gives

    W_F(t,1,a,1) = integral_0^2
      min(a,F^-(t+u,1-u))du / a.                     (14)

The zero-denominator case is the already terminated state. These boundaries come from the interval endpoint dominance argument, not an assumption that Princess paths have reached endpoints at some fixed time.

## 7. Where a short analytic recurrence could emerge

The exact posterior restart map (1) identifies the right invariance question: find a family of conditional CDF profiles closed under the phase-optimal restart map, and solve its parameter/policy update. Do not guess a geometric ratio first and assume every phase follows it.

The previously solved affine center layer does contain a genuine special-case recurrence: in its no-hinge quadratic sector, stationary excursion lengths satisfy a second-order linear relation of the form

    (1+theta^2) h_j - theta(h_{j-1}+h_{j+1}) = constant,

so homogeneous modes are geometric theta^j and theta^(-j). Its geometric Zeno branch is a special orbit of that local system, not a proof of global self-similarity. See [INFINITE_TURN_RENEWAL.md](INFINITE_TURN_RENEWAL.md). The global response recursion above does not impose those local coefficients or a prescribed terminal center cell.

**Next constructive target:** evaluate the half-survival phase optimization globally for a free transport CDF; inspect whether its minimizing phase maps preserve a small analytic posterior family; then solve that invariant family jointly with the all-Princess dual condition. This is a policy/recurrence search, not a new set of complete-path mixing weights. Do not optimize the Princess anew separately at each hidden Monster state: that changes the information structure and therefore the game.

## 8. Executed exact tests and limitations

The standard-library Fraction program `packages/interval_global_closure/verify_survivor_halving.py` was actually run in the working container. It checks:

* 2,145 direct physical checks of the pointwise two-tour bound (2).
* 31 ordered stationary/moving target models and 155 starting states.
* One-target-at-a-time exact response DP against an independent all-order physical chase/scoring oracle at all 155 starts, plus direct first-contact scoring of 155 reconstructed optimal paths.
* 1,085 lower/upper half-mass iteration brackets, with monotonicity, enclosure and the 2^(1-n) width.
* 28,334 exact strict/closed posterior clipping identities and the two-rank memory counterexample.

Representative finite-fixture recurrence values:

| Fixed-start fixture | True conditional response | Phase brackets n=1,2,3 |
| --- | --- | --- |
| Equal stationary endpoints, start 0 | 2 | [1,2], [2,2], [2,2] |
| Ordered inward runners at +/-3/4, start 0 | 9/16 | [3/8,9/16], [9/16,9/16], [9/16,9/16] |
| Five equally spaced targets drifting right at 1/2, weights (1,2,3,2,1)/9, start 1/3 | 26/27 | [4/9,26/27], [20/27,26/27], [22/27,26/27] |

The test model uses finite canonical capture-prefix actions to compare two independently organized exact response calculations. It does **not** claim that those actions compute the general continuum operator for arbitrary terminal functions. The continuum claims (8)-(12) are justified by the analytic arguments, not by finite fixtures.

No exact equilibrium F, explicit universal optimum policy, improved numerical game-value bound, finite optimal turn theorem, Lean formalization, or CI run is claimed. The deliverable is a global recurrent response description with a quantitative contraction and a precisely isolated remaining phase-control problem.
