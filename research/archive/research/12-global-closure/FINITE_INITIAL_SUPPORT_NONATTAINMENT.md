# No finitely supported initial Princess law can attain the value

**Status: proved obstruction for the unrestricted game.** This does not
evaluate the game value or exclude a finite formula for a continuous CDF.

For hidden, independently chosen, unit-speed-bounded paths in `[-1,1]`,
with arbitrary initial positions and capture at first coincidence, **every
Princess law supported on finitely many initial positions has security
strictly below the unrestricted value**. The subsequent path law can be
arbitrary, including continuum support, waiting, infinitely many reversals,
and endpoint atoms. In particular, no finite collection of Princess paths
can be an exact equilibrium law.

Thus the existing 338-path lower certificate cannot be made into an exact
equilibrium simply by optimizing its weights or paths. Adding any fixed
finite number of paths does not remove this obstruction. A fixed spatial
grid whose Princess initial positions must be grid vertices also cannot
contain an exact maximizing Princess law. Finite continuous-CDF formulas,
finite analytic Bellman certificates, and a uniform approaching family of
finite laws remain possible.

## 1. Definitions and existence inputs

Let `A` be the space of all continuous 1-Lipschitz paths
`[0,infinity) -> [-1,1]`, with locally uniform convergence. This is a
compact metric space by Arzela--Ascoli on each bounded time interval
and a diagonal argument. Write

\[
 T(m,p)=\inf\{t\geq0:m(t)=p(t)\},\qquad
 J_\mu(m)=\int T(m,p)\,d\mu(p),\qquad
 B(\mu)=\inf_mJ_\mu(m),\qquad V=\sup_\mu B(\mu).
\]

The sweep from one endpoint to the other catches every Princess by time
two, so `V<=2`. For fixed `p`, first contact is lower semicontinuous in
`m`: a bounded sequence of earlier contact times along locally uniformly
convergent Monster paths would have a convergent subsequence giving an
equally early contact for the limit. For any fixed Princess law,
Fatou's lemma therefore makes `J_mu` lower semicontinuous in `m`.
Thus `B(mu)` is a finite attained minimum on the compact path space.

The constructive proof in Section 4A needs only these compactness facts.
The independent saddle proof in Section 4 uses the unrestricted
minimax/attainment theorem from
[GLOBAL_MINIMAX_AND_CDF_DUALITY.md](GLOBAL_MINIMAX_AND_CDF_DUALITY.md): there
is a Monster law `nu` such that

\[
 \Psi_\nu(p):=\int T(m,p)\,d\nu(m)\leq V
 \quad\hbox{for every legal }p.                         \tag{1}
\]

No Princess attainment theorem is assumed. Symmetry, ordered quantiles,
horizon reductions, clocks, and differentiability are not needed for
the obstruction.

## 2. Every exact response to a finite-start Princess law starts at an atom

Let the initial marginal of `mu` have finite support

\[
 S=\{s_1,\ldots,s_k\},\qquad
 w_i=\mu\{p:p(0)=s_i\}>0,\qquad w_{\min}=\min_iw_i>0.
\]

**Prefix replacement lemma.** If `J_mu(m)<infinity` and `m(0) notin S`,
there is a legal path `m_tilde` and a time `tau>0` such that

\[
 J_\mu(\widetilde m)\leq J_\mu(m)-w_i\tau
 \quad\hbox{for some }i,\qquad
 \tau\geq\tfrac12\operatorname{dist}(m(0),S).            \tag{2}
\]

**Proof.** Let `K=supp(mu)` in the locally uniform path space. This is
compact and has full `mu` measure. Continuity of evaluation at zero and
closedness of `S` imply that `p(0) in S` for every `p in K`.

Finite `J_mu(m)` implies that `m` contacts some member of `K` at a finite
time. Choose one such time `R`. The set

\[
 \{(t,p)\in[0,R]\times K:m(t)=p(t)\}
\]

is nonempty and compact: evaluation `(t,p) -> p(t)` is continuous in
this topology on a bounded time interval. It therefore has a smallest
time coordinate `tau`, attained by a path `p_* in K`. This is the first
contact with **the entire support**, not just the first positive-mass
capture. Before `tau` none of the support paths has been caught.

For any support path, relative speed is at most two. Its initial distance
from `m(0)` is at least `dist(m(0),S)`. Hence the stated lower bound for
`tau` holds and is strictly positive.

Follow `p_*` on `[0,tau]` and then follow `m` from `tau` onward. The pieces
meet at `tau`, so this is a legal 1-Lipschitz Monster path. Every support
Princess caught by `m` is caught no later by `m_tilde`: all old contact
times were at least `tau`, and the suffix is identical. Moreover, if
`p_*(0)=s_i`, then **every** Princess starting at `s_i` is caught by the
new Monster at time zero. That entire group has mass `w_i>0`, whereas
its old capture times were at least `tau`. Integrating proves (2).
The individual earliest path `p_*` need not have positive mass. QED.

Consequently every finite-start Princess law satisfies the useful global
response estimate

\[
 \boxed{J_\mu(m)\geq
 B(\mu)+\frac{w_{\min}}2\operatorname{dist}(m(0),S).}     \tag{3}
\]

For `m(0) in S` this is the definition of `B(mu)`; infinite payoffs make
the inequality immediate. Otherwise it follows from (2). In particular,
an exact minimizing response must start in `S`. An epsilon-minimizing
response must start within `2 epsilon/w_min` of `S`.

## 3. A charged start cannot maximize against a finite-start Monster law

Suppose a Monster law `nu` starts almost surely in a finite set `S`.
Fix `x in S` with

\[
 a=\nu\{m:m(0)=x\}>0.
\]

If `S\setminus{x}` is nonempty, let
`d=min{|z-x|:z in S\setminus{x}}>0`; otherwise set `d=1`. Choose

\[
 0<\delta<\min\{1/4,d/4\},                             \tag{4}
\]

and, when `-1<x<1`, also require `delta<1-|x|`. This `delta` is fixed
for the start `x`, independently of the Princess path.

**Prefix perturbation lemma.** For every legal `p` with `p(0)=x`, there
is a legal `p_delta` equal to `p` after time `delta` such that, whenever
`Psi_nu(p)` is finite,

\[
 \boxed{\Psi_\nu(p_\delta)\geq
              \Psi_\nu(p)+a\delta/4>\Psi_\nu(p).}       \tag{5}
\]

**Proof.** Put `z=p(delta)`. At an interior start choose

\[
 y=\begin{cases}
     x+\delta/2,&z\geq x,\\
     x-\delta/2,&z<x.
   \end{cases}
\]

At `x=1` choose `y=1-delta/2`, and at `x=-1` choose
`y=-1+delta/2`. The speed bound gives `|z-x|<=delta`. In every case,

\[
 y,z\in[-1,1],\qquad |y-x|=\delta/2,\qquad
 |z-y|\leq\delta/2.                                    \tag{6}
\]

Let `p_delta` travel linearly from `y` at time zero to `z` at time
`delta`, then follow `p` exactly. Its new prefix has speed at most
`1/2`; the concatenation is legal even when the original Princess
prefix had saturated unit speed. Both prefixes stay within distance
`delta` of `x`.

For a Monster starting at a different `s in S`, throughout `[0,delta]`
both the old and new Princess remain at distance at least

\[
 |s-x|-2\delta\geq d-2\delta>0
\]

from the Monster. Neither path has an early contact, and their suffixes
are identical. Their first-contact times with this Monster are therefore
identical, including the possibility of an infinite time.

A Monster starting at `x` catches the old Princess at time zero. Its
initial separation from the new Princess is `delta/2`. Since relative
speed is at most two, its new capture time is at least `delta/4`.
The conclusion holds for every such Monster, regardless of waiting,
reversals, or infinitely many turns immediately after zero. Integrate
over the two start groups to obtain (5). QED.

In particular, if `sup_p Psi_nu(p)=c<infinity`, then every path starting
at this charged `x` obeys

\[
 \Psi_\nu(p)\leq c-a\delta/4.                           \tag{7}
\]

This is a strict uniform gap for all Princess continuations from `x`.
It includes `x=-1` and `x=1`.

## 4. The nonattainment theorem

**Theorem.** For every legal Princess law `mu` whose initial marginal
has finite support,

\[
                       \boxed{B(\mu)<V.}               \tag{8}
\]

**Proof.** Suppose instead that `B(mu)=V`, and take the globally optimal
Monster law `nu` from (1). Tonelli's theorem and the two security
inequalities give

\[
 V\leq\int J_\mu(m)\,d\nu(m)
   =\int\Psi_\nu(p)\,d\mu(p)\leq V.                    \tag{9}
\]

Thus both inequalities are equalities. Since `J_mu(m)-V` is
nonnegative, it vanishes `nu`-almost surely. In particular, almost
every sampled Monster is an exact response to `mu`, with finite cost.
Section 2 forces its start to lie in the finite set `S` of Princess
initial atoms.

Choose `x in S` with `a=nu{m(0)=x}>0`; such an `x` exists because `nu`
is a probability law on finitely many starts. The Princess also assigns
positive mass `b=mu{p(0)=x}>0` to this start, by the definition of `S`.
For every Princess starting there, Section 3 and the global bound (1)
give

\[
                 \Psi_\nu(p)\leq V-a\delta/4.
\]

All remaining Princess paths still have payoff at most `V`. Hence

\[
 \int\Psi_\nu(p)\,d\mu(p)
        \leq V-ab\delta/4<V,
\]

contradicting (9). QED.

The argument assumes a maximizing Princess law only to derive a
contradiction for the finite-start class. It does not prove that any
Princess maximizing law exists. If a maximizing law does exist, its
initial marginal must have **infinite support**. This is weaker than
atomlessness: an infinite-support law with atoms is not excluded.

## 4A. A strictly better law using only short-prefix perturbations and mixing

The obstruction admits a stronger constructive form. Every finite-start
Princess law can be strictly improved while retaining finite initial
support. The argument gives the shape of an improvement; the size of
the mixing weight depends on a global response gap that is not
numerically evaluated here.

**Improvement theorem.** Fix any Princess law `mu` with finite initial
support `S`. There is a law `mu'` obtained by changing only the Princess
prefixes on a common interval `[0,delta]`, and a number `0<lambda<=1`,
such that

\[
 B\bigl((1-\lambda)\mu+\lambda\mu'\bigr)>B(\mu).         \tag{10}
\]

If `mu` has `k` initial sites, `mu'` has at most `2k` and the improved
mixture at most `3k`. If `mu` is supported on `N` whole trajectories,
the improved mixture uses at most `2N` trajectories.

**Proof.** Choose a common positive `delta` satisfying (4) for every
`x in S`, and below `1-|x|` for every interior `x in S`. Apply the
prefix map of Section 3 to every Princess path, using its own initial
point `x`. This is a Borel map: it uses evaluation at `delta`, a
two-case sign choice, an affine prefix, and the unchanged suffix.
Let `mu'` be its pushforward. Initial points belong to the finite set
`{x-delta/2,x+delta/2:x in S}`, with the inward choice at endpoints.

For any Monster starting at `x in S`, the whole Princess group starting
at `x` changes its capture time from zero to at least `delta/4`.
For every other initial group, both Princess prefixes stay separated
from the Monster up to `delta`, and both suffixes are unchanged. Thus

\[
 J_{\mu'}(m)\geq J_\mu(m)+\epsilon
 \quad\hbox{whenever }m(0)\in S,\qquad
 \epsilon=w_{\min}\delta/4>0.                           \tag{11}
\]

Put `B=B(mu)` and let `K_*={m:J_mu(m)=B}`. This is a nonempty compact
set. Section 2 places every one of these exact responses at a start in
`S`. Lower semicontinuity of `J_mu'` therefore makes

\[
            O=\{m:J_{\mu'}(m)>B+\epsilon/2\}
\]

an open neighborhood of `K_*`. If `O=A`, then
`B(mu')>=B+epsilon/2`, and we can take `lambda=1`.

Otherwise its compact complement is disjoint from `K_*`. Lower
semicontinuity of `J_mu` gives an `eta>0` such that
`J_mu(m)>=B+eta` outside `O`; if that minimum is infinite, any finite
positive `eta` suffices. Choose

\[
              \lambda=\frac{\eta}{2(B+\eta)}\in(0,1/2].
\]

For `m in O`, linearity in the Princess law and `J_mu(m)>=B` give

\[
 J_{(1-\lambda)\mu+\lambda\mu'}(m)
     \geq B+\lambda\epsilon/2.
\]

Outside `O`, use `J_mu'>=0` instead to obtain

\[
 J_{(1-\lambda)\mu+\lambda\mu'}(m)
     \geq(1-\lambda)(B+\eta)=B+\eta/2.
\]

Taking the infimum proves the explicit, strictly positive guarantee

\[
 B\bigl((1-\lambda)\mu+\lambda\mu'\bigr)
 \geq B+\min\{\lambda\epsilon/2,\eta/2\}>B.             \tag{12}
\]

There is one new trajectory for each old trajectory in the finite-law
case, proving the support count. QED.

This proves (8) independently of unrestricted minimax and Monster-law
attainment. It also explains why simply replacing the entire law by
`mu'` is not justified: previously nonoptimal Monster starts can become
competitive. The mixture preserves a positive margin against those
responses. To turn this improvement theorem into a new numerical
certificate, one must certify `eta` or directly certify the mixed
law's unrestricted response. No unverified value improvement follows
from a chosen floating-point mixing weight.

## 5. Consequences for the current proof search and exact replay

1. A finite path bank, with any real weights and any legal trajectories,
   cannot supply an attained exact Princess saddle. This is not merely
   a limitation of the present 338-path implementation or its mesh.
2. Finite-grid Princess extraction remains a valid approximation method.
   Its finite initial support prevents an extracted law from attaining
   the unrestricted value. A limiting argument can still prove the value
   if a uniform family approaches a matching exact upper certificate.
3. Finite formulas for a Princess CDF with infinite initial support remain
   eligible. The four-state analytic-exit certificate approach is not
   excluded, nor is a finite sufficient classification of continuous
   CDF phases. Any proposed sufficiency theorem must respect this
   distinction.
4. No numeric improvement of the current interval follows from (8).
   The theorem establishes a strict gap for each finite-start law, but
   does not give a uniform positive gap over all laws with a given
   support cardinality.

The exact arithmetic regression script

```sh
python packages/interval_global_closure/verify_finite_initial_support_obstruction.py
```

checks the prefix geometry and first-contact comparisons for rational
polygonal fixtures, including both endpoints, saturated speeds, waiting,
reversals, and contact at the rejoining time. It also checks a direct
support-prefix replacement example with unequal masses. The regression
does not replace the compactness and minimax arguments above or claim
to kernel-check this continuum theorem.
