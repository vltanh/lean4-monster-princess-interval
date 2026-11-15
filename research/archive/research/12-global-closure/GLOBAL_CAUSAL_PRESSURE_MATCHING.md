# G2 conceptual pivot: exact causal-pressure matching, not a path recurrence

Date: 2026-11-13. **A global, assumption-free reformulation of the existing
unrestricted one-clock dual.** The mathematical improvement is an EXACT
reduction of its **full unrestricted Princess radial oracle** to a
maximal *causal-order matching* of two positive measures. There is no
finite path bank, Monster turn limit, Princess endpoint horizon, survival
threshold, smoothness assumption, or assumption that a maximizer exists.

**Status:** Not an explicit optimal Monster law, optimal Princess CDF, or
new numerical game bound. The hard remaining problem is the *physical
Monster-path/clock lift* of the pressure measures, and a matching lower
Princess certificate. This note is not another "halving" strategy or
claim that optimal play changes at an arbitrarily specified event.

## 1. Input from the previously proved unrestricted global dual

[GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md](GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md)
establishes
\[
 V=\min_{\nu,s}\sup_{r\in{\cal R}}J_\alpha(r),\quad
 J_\alpha(r)=\int\Phi(r(t),x)\,\alpha(dt,dx),
 \quad\Phi(r,x)=\mathbf1_{\{x>r\}}+\mathbf1_{\{x>-r\}},
\]
where r is any nonnegative 1-Lipschitz radius path in [0,1], nu is
a symmetric law on full legal Monster trajectories, tau_-(m) is the
first visit to -1, and s_m(t) is a nondecreasing causal backward clock
satisfying 0<=s_m(t)<=t. The finite nonnegative active occupation
\[
 \alpha=\mathbb E_\nu\int_0^{\tau_-(m)}
        \delta_{(s_m(t),m(s_m(t)))}\,dt
\]
has mass \(M=\mathbb E_\nu\tau_-(M)\), and crucially
\(\alpha\{x=-1\}=0\) since \(s_m(t)\le t<\tau_-(m)\).
The minimum above is attained on the outer side, but not necessarily
on the maximizing Princess side.

This note does not re-prove the existing one-clock dual. Its *new*
steps are the signed imbalance decomposition, the exact Lipschitz
upper-set lemma, and Strassen/Hall partial matching.

## 2. Two-sided pressure split and EXACT contact-germ identity

Let X=[0,infinity) x [0,1], with coordinates (t,u).
Define positive measures on X:
\[
 \mu_+(dt,du)=\alpha(dt,dx)|_{x>0}\quad(u=x),\qquad
 \mu_-(dt,du)=\alpha(dt,dx)|_{x<0}\quad(u=-x),
\]
and let \(\alpha_0(dt)=\alpha(dt,\{0\})\). The negative-side
measure has no mass at u=1, because alpha has no mass at x=-1.
Write \(a=\mu_+(X)\), \(b=\mu_-(X)\), and
\(M=a+b+\alpha_0([0,\infty))\).

For EVERY legal radius r, elementary comparison at each (t,x)
gives the exact formula
\[
 \boxed{
 J_\alpha(r)=M+
  (\mu_+-\mu_-)\{(t,u):u>r(t)\}
 -\mu_-\{u=r(t)\}
 -\alpha_0\{t:r(t)=0\}.}                            \tag{1}
\]
All inequalities are STRICT. In particular the two nonpositive
last terms account for exact contact atoms, which a smooth PDE
would miss.

**Theorem 1 (no contact-germ gap in the supremum).** Put
\[
 D_{\rm Lip}(\mu_+,\mu_-)
 =\sup_{r:[0,\infty)\to[0,1],\,|r'|\le1}
  [\mu_+\{u>r(t)\}-\mu_-\{u>r(t)\}].
\]
Then
\[
 \boxed{\sup_{r\in\mathcal R}J_\alpha(r)
       =M+D_{\rm Lip}(\mu_+,\mu_-).}                 \tag{2}
\]
The supremum in D is nonnegative, since r=1 makes both
upper-tail terms zero.

**Proof.** Equation (1) immediately proves the <= direction.
For ANY fixed legal r, set
\(r_\varepsilon(t)=\min(1,r(t)+\varepsilon)\).
This remains a legal 1-Lipschitz radius, and the nonnegative
strict-contact penalties in (1) evaluated at r_epsilon
converge to zero as epsilon decreases to zero. The equality
indicator \(u=r_\varepsilon(t)\) is eventually false at each
negative-side atom with u<1; likewise r_epsilon(t)>0
eventually eliminates the center-atom penalty. The strict
upper-tail indicators converge pointwise to
\(\mathbf1_{\{u>r(t)\}}\). Bounded convergence against
the finite measures proves
\[
 \lim_{\varepsilon\downarrow0}J_\alpha(r_\varepsilon)
 =M+(\mu_+-\mu_-)\{u>r(t)\}.
\]
Take the supremum in r. No Princess attainment or
continuity of chronological first-contact time was assumed.
QED.

This lemma correctly preserves the *unattained* one-sided germ
behavior seen in the two-sweep game: a limit radius may score
much less at literal equality than its legal outward perturbations.

## 3. A specific finite-speed order on time–RADIUS space

On X define a closed partial order
\[
\boxed{
 (t,u)\preceq(s,v)
 \quad\Longleftrightarrow\quad
 v\ge u+|s-t|.}                                      \tag{3}
\]
For a legal radius r, the strict supergraph
\(U_r=\{(t,u):u>r(t)\}\) is an UPPER set for this order.
Indeed \(u>r(t)\) and \(v\ge u+|s-t|\)
imply \(v>r(t)+|s-t|\ge r(s)\).
The time difference appears in ABSOLUTE value because Princess
radii may move either inward or outward, but at speed at most one.

**Theorem 2 (Lipschitz supergraphs are separation-complete).**
For arbitrary finite Borel measures mu_+,mu_- supported on X with
no atoms at u=0,
\[
\boxed{
 D_{\rm Lip}(\mu_+,\mu_-)
 =\sup_{U\subset X\ {\rm Borel,\ upper}}
      [\mu_+(U)-\mu_-(U)].}                           \tag{4}
\]

**Proof.** Every U_r is upper, so <= follows.
Conversely fix a Borel upper U and epsilon>0.
By inner regularity choose compact K+ subset U and
K- subset X\U with
\(\mu_+(U\setminus K+)<\epsilon\),
\(\mu_-((X\setminus U)\setminus K-)<\epsilon\).
No \(z\in K+\) precedes \(w\in K-\), since U is upper.
The continuous function
\(u_z+|t_z-t_w|-u_w\) is STRICTLY positive on
K+ x K-; compactness gives a uniform positive gap
when both sets are nonempty.

Set
\[
 r(t)=\min(1,\max(0,\sup_{(s,v)\in K_-}(v-|t-s|))).
\]
It is 1-Lipschitz. Every point in K- is excluded from U_r
because r(s)>=v, and every point in K+ is included because
u>r(t), by the strict gap above. Thus
\[
 \mu_+(U_r)-\mu_-(U_r)
 \ge\mu_+(K+)-\mu_-(X\setminus K-)
 \ge\mu_+(U)-\mu_-(U)-2\epsilon .
\]
Empty K- or K+ cases follow by r=0 or the trivial
nonpositive estimate. Let epsilon tend to zero. QED.

**Interpretation:** a Princess radius trajectory is precisely
a separating graph for the cone order (3). This is NOT a guessed
"optimal turning phase": the entire Lipschitz path class
is captured by the upper-set order.

## 4. GLOBAL max-flow/min-cut = maximal causal pressure matching

Define the largest matchable positive-pressure mass
\[
 {\rm Match}_{\preceq}(\mu_+,\mu_-)
 =\max\{\pi(X\times X):
   \pi\ge0,\quad
   (\pi_1\le\mu_+),\quad(\pi_2\le\mu_-),\quad
   \operatorname{supp}\pi\subset\{(z,w):z\preceq w\}\}.
\]
The maximum exists: the feasible set of finite partial
couplings is tight (dominated marginals), weakly closed,
and bounded; the relation is closed.

**Theorem 3 (exact global causal matching dual).**
\[
 \boxed{
 D_{\rm Lip}(\mu_+,\mu_-)
 =\mu_+(X)-{\rm Match}_{\preceq}(\mu_+,\mu_-).}       \tag{5}
\]

**Proof.** The result is the deficient-mass form of
Strassen's stochastic-order coupling theorem, for the closed
order (3). Here is a direct reduction to the ordinary theorem.

Let a=mu_+(X), b=mu_-(X) and
d=sup_{upper U}(mu_+(U)-mu_-(U)).
The empty set yields d>=0 and the entire space yields d>=a-b.
Adjoin isolated bottom/top points bot,top to X, declaring
bot <= z <= top for every z. Define equal-mass measures
\[
 \widetilde\mu=\mu_+ +(b-a+d)\delta_{\rm bot},\qquad
 \widetilde\nu=\mu_-+d\delta_{\rm top}.
\]
Every nontrivial upper set in the extended order is
U union {top}, where U is an upper set in X. By definition
of d,
\(\widetilde\mu(U\cup\{\rm top\})=\mu_+(U)
 \le\mu_-(U)+d=\widetilde\nu(U\cup\{\rm top\})\).
The other upper sets satisfy the inequality trivially.
Thus the extended measures are stochastically ordered.

Strassen's theorem (for a Polish space with a closed partial
order) supplies a full order-preserving coupling of the
equal-mass measures. Restrict to X x X: of the a units
originating in mu_+, at most d can go to top, so
the restricted partial matching has mass at least a-d.
Conversely for ANY matching of mass m, any upper set U
can contain at most its matched negative mass in U plus
the unmatched positive mass a-m; therefore
mu_+(U)-mu_-(U)<=a-m. Hence d<=a-m for every
feasible matching, or equivalently m<=a-d. The Strassen
construction attains at least a-d, so the maximal matching
mass is exactly a-d. Combine this with Theorem 2. QED.

For background on the general closed-order Strassen theorem:
T. Lindvall (1999), *On Strassen's theorem on stochastic
domination*, Electronic Communications in Probability 4,
51–59, DOI 10.1214/ECP.v4-1005. The specialized deficiency
argument and identification with radius graphs above are
included in this proof.

**An immediately usable all-Princess upper certificate:**
For any PHYSICALLY feasible Monster law and causal clock
with record measure alpha, exhibit an explicit positive
partial transport plan pi between mu_+ and mu_-
whose pairs all satisfy (3).
Writing m=pi(total), without solving any Princess
path problem at all,
\[
\boxed{
 \sup_{p\ {\rm legal}}\mathbb E_\nu T(M,p)
 \le M+\mu_+(X)-m.}                                  \tag{6}
\]
The path law/clock causal lift is still a required input!
A coupling pi of two arbitrary spacetime densities is
NOT by itself a Monster strategy. The upper bound (6)
is valid because the causal selector plane majorizes
the physical first-contact payoff and (2),(5) control
that entire plane for all Princess paths.

## 5. Search effort + unmatched pressure: the NEW full-game principle

For a physical Monster path, let sigma be the first endpoint
visit, tau its second, B total wrong-way variation between
endpoint visits and I idle/slow time on that interval.
The exact global endpoint budget already proved in
[GLOBAL_SWEEP_STABILITY_ENERGY_BARRIER.md](GLOBAL_SWEEP_STABILITY_ENERGY_BARRIER.md)
is
\[
 \frac{\tau_-+\tau_+}{2}-1
 =\sigma+B+\frac I2=:\mathcal E(m)\ge0 .
\]
For a symmetric Monster law, the active occupation mass is
\[
 M=\mathbb E_\nu\tau_-(M)
 =\frac12\mathbb E_\nu(\tau_-+\tau_+)
 =1+\mathbb E_\nu\mathcal E(M).
\]
Substitute (2) and (5) into the EXISTING exact global one-clock
dual to obtain the *fully unrestricted*, attained variational formula
\[
 \boxed{
 V=1+\min_{\substack{\nu\ {\rm symmetric\ legal}\\
          s_m\ {\rm causal\ monotone}}}
 \left[
   \underbrace{\mathbb E_\nu\bigl(\sigma+B+I/2\bigr)}
     _{\text{Monster search effort beyond fastest sweep}}
   +
   \underbrace{\mu_+(X)-{\rm Match}_{\preceq}(\mu_+,\mu_-)}
     _{\text{unmatched time--radius record pressure}}
 \right].}                                          \tag{7}
\]
The outer minimizer exists by the underlying global duality
theorem; the inner pressure matching maximum exists by
compactness and Strassen. The formula has ZERO new
strategy-family assumptions and contains NO halving
threshold, number-of-turns parameter or finite trajectory
support.

This is a **tradeoff**, not a claim that either summand
vanishes at equilibrium. Physical detours and reversals
raise effort, but can create negative record pressure at
causally matching time--radius locations, reducing the
unmatched component. Pointwise/spacetime perfect balance
(\(\mu_+\le\mu_-\)) would be a very strong SUFFICIENT
certificate for the second term to vanish; it is NOT
asserted necessary or optimal.

Because the full-game optimal Monster law has the
previously proved positive completion-delay lower bound,
an optimal symmetric active record measure also obeys
the new quantitative **mass** restriction
\[
\boxed{
 1.004525582824\ldots
 \le\alpha([0,\infty)\times[-1,1])
 =1+\mathbb E_\nu\mathcal E
 \le V\le1.426129722846\ldots .}                    \tag{8}
\]
The left side is half of the earlier rigorous
\(\mathbb E(\tau-2)\ge0.009051165648\ldots\)
inequality, now translated directly to the globally
optimal occupation variable. This is a consequence of
existing structural bounds, not a new game-value bound.

### A quantitative global effort–mismatch tradeoff

The full-strategy sweep-stability theorem supplies a nontrivial
GLOBAL restriction on the two new summands, without requiring
an equilibrium candidate. For every symmetric completed
Monster law and causal clock with finite active mass, put
\(e=\mathbb E_\nu\mathcal E=M-1\) and
\(D=D_{\rm Lip}=\mu_+(X)-{\rm Match}_\preceq\).
If \(\bar\Delta=\mathbb E_\nu(\tau-2)\), the
pathwise endpoint-time identity gives
\(\bar\Delta\le2e\). The previously proved
unrestricted two-runner stability inequality
states that, for \(\bar\Delta\le1/4\),
\[
 M+D\ge\sup_p\mathbb E_\nu T(M,p)
 \ge\frac32-\sqrt{\bar\Delta}-\frac{\bar\Delta}4.
\]
For \(e\le1/8\), use \(\bar\Delta\le2e\)
and monotonicity of the lower envelope;
for \(e>1/8\), the right side below is
negative and the conclusion is trivial because D>=0.
Thus the exact, unconditional **search-effort /
causal-matching uncertainty inequality** is
\[
 \boxed{
 D\ge\max\left(0,\frac12-\sqrt{2e}-\frac32e\right).
 }                                                    \tag{7a}
\]
In particular, an entirely *matched* active
record pressure field \(D=0\) requires
\[
 \boxed{
 e\ge\frac{7-2\sqrt{10}}9
   =0.0750494088514712\ldots.
 }                                                    \tag{7b}
\]
This does not establish that D=0 is optimal,
or that e in this range can be realized
with a causal Monster/clock law. It does prove
that **no infinitesimal perturbation of the fast
two-sweep Monster law can annihilate the entire
spacetime mismatch**, even using arbitrarily many
turns, waits or Zeno. It is an actual joint
constraint on the physical dual variables,
not a choice of a "switching threshold".

### Universal geometric Hall cuts

For EVERY compact set A of positive-pressure points, let
\[
 R(A)=\{(s,v):\exists(t,u)\in A,\quad
                      v\ge u+|s-t|\}.
\]
Every matching sends mass in A only into R(A), so
\[
 \boxed{
 \mu_+(A)-\mu_-(R(A))
   \le D_{\rm Lip}.}                                 \tag{9}
\]
This is an exact family of global **finite-speed
pressure-balance inequalities**, not a trajectory list.
In particular any positive record pressure at u=1
can never match negative pressure (which has u<1);
it contributes fully to the deficiency.

A constructive attack could prove a sharp, global lower
inequality on effort+deficiency in (7), or exhibit a
physical causal Monster/clock law and a matching pi with
effort+deficiency at or below the existing best upper
certificate. Neither task has been achieved.

## 6. Worked full-oracle regression: the TWO fastest sweeps

Take symmetric Monster law with probability 1/2 on
each fastest endpoint-to-endpoint sweep. Its active
occupation (one lower-record current-time clock) is
\[
 \alpha(dt,dx)=\tfrac12\mathbf1_{0<t<2}\,dt\,
                         \delta_{x=1-t}.
\]
The +pressure is on \(0<t<1,u=1-t\), mass 1/2.
The -pressure is on \(1<s<2,v=s-1\), mass 1/2.
For every such pair,
\[
 v-u-|s-t|=(s-1)-(1-t)-(s-t)=2t-2<0.
\]
Thus there is **no allowed matching**, Match=0.
Meanwhile \(M=1\), effort=0, and deficiency=1/2.
Equation (7) for this supplied Monster law gives
\[
 \boxed{\sup_p\mathbb E_\nu T(M,p)=1+1/2=3/2.}
\]

This exactly recovers the already solved monotone
subgame, but explains its failure as **a missing
causal match between early positive and late negative
record occupation**, not as a failure to mix enough
handpicked Princess trajectories.

For the saturated radius \(r_0(t)=|1-t|\) on (0,2),
the literal strict-contact score is 1/2.
For the legal displaced runner
\(r_\varepsilon(t)=|\min(-1+\varepsilon+t,1)|\),
the score is \(3/2-\varepsilon/4\).
The order-one discontinuity is accurately handled
by the outward perturbation in Theorem 1; do NOT
evaluate the supremum at the limiting contact path.

## 7. An independent CLOCK conservation law for physical feasibility

The pressure-matching result concerns the **Princess
side** of a supplied causal dual. Here is a second
global constraint on what Monster record measures
are PHYSICALLY realizable.

For each Monster path m, write \(\tau=\tau_-(m)\).
Its selected-time marginal \(\eta_m=(s_m)_\#(dt|_{[0,\tau)})\)
has mass tau and satisfies the exact prefix condition
\[
 \eta_m([0,u])\ge\min(u,\tau).
\]
Put \(\kappa_m(u)=\eta_m([0,u])-u\) for 0<=u<tau.
Then \(\kappa_m\ge0\) and
\(0\le\kappa_m(u)\le\tau-u\).

For any absolutely continuous f on [0,tau],
the exact signed-measure integration-by-parts identity is
\[
 \boxed{
 \int f(s)\eta_m(ds)-\int_0^\tau f(s)ds
   =-\int_0^\tau\kappa_m(u)f'(u)\,du.}              \tag{10}
\]
To prove it, use
\(f(s)=f(\tau)-\int_s^\tau f'(u)du\)
and Fubini; the signed measure eta-du has total zero.
This includes arbitrary causal-clock atoms, plateaus
and jumps. In particular, with f(s)=s,
\[
 \boxed{\int_0^\tau(t-s_m(t))dt
       =\int_0^\tau\kappa_m(u)du.}                  \tag{11}
\]
This measures how much scoring time has been moved
back to earlier record positions, **without** choosing
any arbitrary probability-halving events.

Define the chronological killed Monster occupation
\(\sigma(dt,dx)=\mathbb E_\nu\int_0^{\tau_-}
                  \delta_{(t,m(t))}dt\)
and flux j by inserting m'(t) in its integrand.
Define the nonnegative backlog occupation
\(\beta(dt,dx)=\mathbb E_\nu\int_0^{\tau_-}
          \kappa_m(t)\delta_{(t,m(t))}dt\)
and flux k by inserting m'(t).
On compact time intervals they are locally finite
since \(\kappa_m(t)\le\tau_-(m)\) and
\(\mathbb E\tau_-<\infty\). For every smooth
compactly supported test phi, (10) with
\(f(t)=\phi(t,m(t))\) gives the exact
DISTRIBUTIONAL conservation identities
\[
 \boxed{
 \alpha=\sigma+\partial_t\beta+\partial_x k,\qquad
 \partial_t\sigma+\partial_x j
     =\delta_{t=0}\mu_0-\xi_-\otimes\delta_{x=-1},
 \quad |k|\le\beta,\ |j|\le\sigma.}                  \tag{12}
\]
Here \(\mu_0\) is Monster initial-position law,
\(\xi_-\) is its first -1 arrival-time law,
and \(|k|\le\beta\) etc. mean domination of
signed flux total variation by the positive measure.
The equations include correct source/sink terms
at t=0 and the first -1 visit.

A simpler consequence is the EXACT causal-order
inequality for every bounded smooth test phi with
\(\partial_t\phi\ge|\partial_x\phi|\):
\[
 \boxed{\int\phi\,d\alpha\le\int\phi\,d\sigma.}      \tag{13}
\]
This follows either from (12) or directly because
\(\phi(s_m(t),m(s_m(t)))\le\phi(t,m(t))\).
It is valid regardless of how many times Monster
reverses or waits.

**CRITICAL caveat:** (12)--(13) are NECESSARY
Eulerian constraints; the follow-up counterexamples below prove that
they are insufficient to reconstruct one common legal Monster law
together with its *pathwise* causal clock.
Replacing the actual feasible (nu,s) in (7)
by arbitrary measures satisfying them would
be a RELAXATION, not an exact new game.
The joint Monster trajectory/clock lift remains
the important unsolved feasibility gate.

**Follow-up audit (2026-11-13):**
[EULERIAN_RELAXATION_GAP.md](EULERIAN_RELAXATION_GAP.md) now proves
that optimizing only (12)--(13) and the pressure matching has attained
relaxed optimum **1**, even while the chronological Monster flow is
physically valid and symmetric. A separate reversing example survives
the explicitly listed scalar cuts but has fake score **5/4** and an
actual Princess response **13/8**. Every physical clock additionally
satisfies `beta << sigma`, and bounded endpoint horizons give joint
directional moment inequalities; the new note proves these necessary
conditions without asserting sufficiency. The counterexamples do not
contradict (7), whose domain retains the full pathwise lift.

## 8. Why this is a different research direction

The existing PR explored literal path-bank mixing,
local center-return recurrences, arbitrary half-
survival restart operators, and smooth CDF patches.
Those approaches do not generate equilibrium.

The exact formula (7) isolates a global
**search-effort versus ordered-pressure matching**
tradeoff. A possible new constructive attack is:

1. Work on the PHYSICAL Eulerian feasible cone of
   Monster history/clock occupations (12), retaining
   its actual causal lift rather than a fake arbitrary
   density or a finite turn template.
2. Construct an explicit **partial cone-ordered
   coupling pi** of positive to negative active
   record pressure. Its mass directly yields an
   all-Princess upper certificate (6).
3. Use the Hall-cut dual (9) to find a sharp
   unrestricted lower inequality on
   Monster effort plus unmatched pressure,
   with proper contact-side limits.
4. Check whether the two match at one constant
   with a legal Princess CDF and unrestricted
   Monster Bellman certificate.

The **go/no-go test** is whether this matching
construction can reproduce the archived
\(U_{\rm best}=1.426129722845311...\) without
re-optimizing a finite Princess trajectory bank.
If not, the reformulation is NOT yet a
solution method and should not spawn another
large family of local case lemmas. The project
remains OPEN until both global saddle inequalities
are certified.

## 9. Reproduction and status

[verify_global_pressure_matching.py](../../packages/interval_global_closure/verify_global_pressure_matching.py)
independently checks with exact Fraction arithmetic:
the signed pressure/contact identity (1);
the max-flow/min-cut/closed-order matching formula
on finite atomic pressure measures;
explicit 1-Lipschitz threshold realization of
maximal upper sets; the two-sweep contact germ;
and the physical clock/backlog identity (10)
on nontrivial waits, turns, clock plateaus and atoms.

The executed standard-library source passed **200** random finite atomic
pressure cases (exact rational bipartite max flow, independent
upper-set enumeration, and explicitly realized 1-Lipschitz radius),
**1,875** path/causal-clock/backlog identity fixtures,
and **27** independent two-sweep contact-germ offsets.
The committed file's Git blob SHA
`9b2c2ddf46e2ad3b61c1fa643ccc04eee308ec4f`
was byte-matched against the locally executed source.

These **finite fixtures** audit the new formula
and the reduction to standard Strassen's theorem.
They do not mechanically verify the
infinite-dimensional minimax theorem or
solve the physical Monster/clock lifting problem.

**UNCHANGED numerical game bounds:**
\[
1.417589834917855\ldots\le V
   \le1.426129722845311\ldots.
\]
No matching equilibrium, finite turn reduction,
Lean compilation or CI is claimed.

