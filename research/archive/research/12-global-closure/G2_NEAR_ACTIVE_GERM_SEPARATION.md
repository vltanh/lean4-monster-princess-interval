# G2 global response-germ obstruction: a certified failed Monster update

Date: 2026-11-12. **G2 is still OPEN.** This is a reproducible **global
Princess adversary against a proposed Monster update**, not an equilibrium
and not an improvement of the unrestricted value interval.

## 1. Why an exact optimal-response face is not the whole directional test

Let \(\nu_0,\nu_1\) be Monster trajectory distributions which have both
visited both endpoints by a common finite time \(D\). Define
\[
 f(p)=\mathbb E_{\nu_0}T(M,p),\quad
 h(p)=\mathbb E_{\nu_1}T(M,p)-f(p),\quad
 U_0=\sup_{p\text{ legal}}f(p),
\]
and
\[
 U(\lambda)=\sup_{p\text{ legal}}\{f(p)+\lambda h(p)\},
 \qquad0\le\lambda\le1.
\]

**Theorem 1 (near-active Monster dual derivative).** Without assuming
a Princess maximizing path exists, or continuity at exact contact,
\[
\boxed{
 U'_+(0)=
 \lim_{\eta\downarrow0}
 \sup_{\{p:\ f(p)\ge U_0-\eta\}}
 \big(\mathbb E_{\nu_1}T(M,p)-f(p)\big).
}                                                      \tag{1}
\]
The right side exists because the near-active sets shrink.
In particular, checking just the two extremal minimizing/maximizing
label responses of an existing exact max-flow certificate is
**not** a correct general derivative test.

**Proof.** For any bounded family \(f_i,g_i\), the exact right
derivative of \(\sup_i(f_i+\lambda g_i)\) is the limit of the
supremum of \(g_i\) on \(\eta\)-near-maximizers of \(f\). This
follows by applying the bounded-family infimum envelope Lemma 4
of GLOBAL_CDF_VARIATIONAL_STATIONARITY.md to \(-f_i,-g_i\).
Both \(f\) and \(h\) are uniformly bounded by the common
completion horizon, so the lemma applies to the entire legal
Princess path space regardless of its infinite dimension.
The supremum of linear functions is convex, hence the right
derivative exists. \(\square\)

There is also an exact **one-path directional exclusion**:

**Theorem 2.** If an actual legal Princess path \(p_\dagger\)
has \(A=f(p_\dagger)<U_0\) and
\(B=\mathbb E_{\nu_1}T(M,p_\dagger)>U_0\),
then for **every** fixed
\[
\boxed{\lambda>\lambda_{\rm crit}
  :=\frac{U_0-A}{B-A},\qquad \lambda\le1,}
\]
one has
\[
U(\lambda)\ge(1-\lambda)A+\lambda B>U_0.             \tag{2}
\]
This conclusion is exact and needs neither maximization of
\(U(\lambda)\) nor any tangent approximation.

## 2. Exact source law and added physical route

Take the archived 280-reflected-pair Monster mixture
\(\nu_0\), with exact rational law
\`packages/interval_global_closure/upper_dyadic_exact.json\`,
Git blob \`188b8b43fad7c69cafb42195d69d045cb44e8f23\`.
Its **certified full Princess response supremum** is
\[
\boxed{
U_0=\frac{957063215727541539}
           {671088640000000000}
     \approx1.426135325025829.
}
\]
This is a valid unrestricted upper certificate for **this
specific Monster law**, but is weaker than the best later
branch-wide upper bound of approximately \(1.42612972\).

Take \(\nu_1\) to be the fair reflected pair of the **actual
archived best Monster response to the old 338-path Princess law**:
\[
\begin{array}{c|cc}
 &t&x\\\hline
0&0&11/16\\
1&107999999/128000000&-19999999/128000000\\
2&127999999/64000000&1\\
3&255999999/64000000&-1
\end{array}
\]
In light coordinates \((U,V)=(t+x,t-x)\), its vertices are
\[
(11/16,-11/16),\
(11/16,63999999/64000000),\
(191999999/64000000,63999999/64000000),\
(191999999/64000000,319999999/64000000).
\]
All segments are unit-speed, and both endpoints are visited.

A natural proposal was
\(\nu_\lambda=(1-\lambda)\nu_0+\lambda\nu_1\).
Against the **saved** nearly optimal Princess response to \(\nu_0\)
(158 physical vertices), the added Monster looks attractive:
its fair-pair expected capture time is exactly
\[
\frac{923587198896963974201313412440435221771721444695618849}
     {649556283258179074757193258985014675402636656640000000}
\approx1.42187401261711 < U_0.
\]
The archived optimum-label extremal rows likewise score
\(23295984311/16384000000\approx1.4218740424\)
against \(\nu_1\).
**Those selected responses misdiagnose the direction.**

## 3. A physical, exactly scored 162-vertex Princess counterexample

Running the repository's **unrestricted** Princess response
max-flow on the actual 281-pair mixture with \(\lambda=1/100\)
gave a floating oracle value approximately
\(1.4418739588089375\). This number is **diagnostic only**.

More importantly, the full label assignment from that solve
was realized as an ordinary legal **162-vertex Princess path**
using the repository's exact physical realization routine at
\(\epsilon=1/268435456\). Every one of the \(281\times2=562\)
chronological captures was recomputed with
\`E.Physical.capture\` using **BigInt rational arithmetic**,
not finite path bank optimization.

The immutable certificate
\`packages/interval_global_closure/g2_m1_injection_witness.json\`
contains the exact ordered labels, prescribed epsilon, old/new Monster
routes and weights, and the three exact rational payoffs
\[
\begin{array}{c|c}
\text{Monster law}&\text{payoff against this physical Princess}\\\hline
\nu_0&A\approx1.4261353108936183\\
\nu_1&B\approx2.999999982512355\\
99\nu_0/100+\nu_1/100&
 (99A+B)/100\approx1.4418739576098056
\end{array}
\]
All exact fractions are checked as written in the JSON by the standalone
\`packages/interval_global_closure/verify_g2_m1_injection.cjs\` script.

The exact exclusion threshold is
\[
\boxed{
\lambda_{\rm crit}=
\frac{
2540024296776724647008929857848814678572721410676066730998110403342391}
{
282875384054357938360956661540600777694401119827431434594157674894693263650871}
\approx 8.97930481037766\times10^{-9}.
}
\]
Therefore **every** injection
\[
\lambda_{\rm crit}<\lambda\le1
\]
produces a Monster law whose unrestricted Princess response is
**strictly larger than the old certified ceiling \(U_0\)**.
This is a mathematically rigorous exclusion of almost the entire
one-parameter update ray, established with a *single actual legal
Princess witness*. No conclusion is asserted for
\(0<\lambda\le\lambda_{\rm crit}\): an infinitesimal improvement
may exist, but is too small to address the main game gap.

### Why exact-contact perturbations matter

The same 162-vertex label pattern realized at
\(\epsilon=1/1048576\) scores only about \(1.4218745\)
against \(\nu_1\), and at \(\epsilon=1/16777216\) its
\(\nu_1\) score is about \(1.42187496\).
Shrinking epsilon to \(1/268435456\) instead gives
\(B\approx 2.99999998\), while leaving
\(A\) within \(1.42\times10^{-8}\) of \(U_0\).
Thus *the sign of a proposed dual update* changes because
of an actual microscopic first-contact branch, even though
the old Monster expectation barely changes.

An independent **exact BigInt min-cut** for the augmented
281-route arrangement with zero new-route mass identifies the
primary-optimal response face. A *numerical secondary flow*
optimization on that face produced a rational-label witness whose
primary score was then checked **exactly equal** to \(U_0\).
Its added-route payoff was exactly
\[
46591984119/32768000000\approx1.42187451535<U_0.
\]
**No claim that this is the largest added-route payoff over the
entire primary-optimal face is made:** secondary flow optimality was
not certified in exact arithmetic. This face witness, like the two
archived extremal labels, does not reveal the adverse near-active
physical trajectory. This does not contradict the physical witness;
it demonstrates that a strictly optimal exact label face and
an arbitrarily chosen *near*-optimal physical response family
are not interchangeable.

## 4. Other unrestricted oracle experiments, all rejected

Further discovery-only solves of the full Princess response
oracle (floating flow; each returned route is physically legal,
but no exact bound claim is made here):

| Monster update | Global Princess response |
| --- | ---: |
| Original \(\nu_0\) | 1.42613532502583 |
| Add 1% of the above single route | 1.44187395880894 |
| Add 5% of the above single route | 1.50482854570050 |
| Add 1% equally across starts \(5/8,11/16,3/4\), with aligned terminal characteristics \(V=1,U=3\) | 1.44186375490905 |
| Add 5% across those three starts | 1.50481875471070 |
| Move 0.1% mass from original atom 0 to original atom 120 | 1.42802089865524 |
| Move 0.5% mass from original atom 0 to atom 120 | 1.43589394553024 |
| Move 0.5% mass from original atom 0 to atom 20 | 1.42659318632662 |

The three-start tests share the later outgoing characteristic,
which allows a common high-value response. The last three tests
show that even reweighting toward routes which individually
capture the known adverse Princess paths early can make the
**unrestricted** response worse.

All these experiments are **negative**; none closes G2 or
improves an unrestricted certified bound.

## 5. Corrected G2 implementation requirement

A coupled master should not optimize only against (i) one archived
best Princess response, (ii) only the minimum/maximum exact label
face, or (iii) a fixed finite Princess path basis. It must retain
**near-active contact-germ columns** and rescore every candidate
Monster law against the full global Princess oracle.

A concrete viable workflow is:
1. For each Monster law, compute its complete global Princess-response
   supremum and identify the active/maximal cut.
2. Generate *physically realized* positive-epsilon Princess responses
   for nearby Monster laws, including all previously discovered
   microscopic contact-germ alternatives.
3. Add these as explicit payoff constraints to a **joint Monster
   weight/route-geometry master**, and use exact first-contact rescoring.
4. Obtain exact unrestricted upper certificates only after the
   new rational Monster law passes the full integer max-flow replay.
5. Independently attach a legal Princess CDF and certify every
   Monster response, including waits, resets, and Zeno limits.

The first four steps are a constructive G2 strategy, not a
completed implementation here. The existing global oracle
and the saved exact counterexample supply an adversarial
regression that any such implementation must pass.

## 6. Reproduction

From repository root:

    node packages/interval_global_closure/verify_g2_m1_injection.cjs

The underlying executed pure-V8 rational scoring checked all
562 individual physical captures. The new standalone Node wrapper
is supplied for replay, but no separate native Node invocation,
Lean compilation, or CI run is claimed.

**Status:** G1 mathematical characterization is unchanged.
G2 remains OPEN. This note excludes a tempting, globally invalid
Monster update ray and establishes why the next construction must
price near-optimal Princess response germs.


## 7. Four-column exact physical cut bank and one genuine exchange iteration

The coupled search now retains **four independent legal Princess
trajectory columns**, each evaluated by exact rational first contacts
against all \(280\) original Monster reflection pairs *and* the newly
proposed Monster route (281 pairs):

1. The 162-vertex \(2^{-28}\) near-optimal germ in Section 3;
2. the archived 158-vertex Princess near-best response to \(\nu_0\);
3. a 212-vertex realized response to the failed \(0.001\) mass transfer
   from original Monster atom 0 to atom 120;
4. a 168-vertex realized response to the smaller attempted
   \(0.00003\) transfer along the same atoms.

All \(4\times281\times2=\mathbf{2248}\) individual physical first
contacts and all four source-law expectation sums are stored as exact
rationals in
\`packages/interval_global_closure/g2_near_active_princess_cuts.json\`.
The third and fourth physical routes are fully reproducible from their
saved label/epsilon data in \`g2_sweep_reweight_witness.json\` and
\`g2_balanced_shift_witness.json\`.

The **fourth** new Princess is particularly informative. A master using
only the first three columns predicted that shifting approximately
\(0.0000345\) of sweep mass would give a restricted worst payoff near
\(1.42612022\), below the old Monster ceiling. The full unrestricted
Princess response oracle instead found

\[
\begin{array}{c|c}
\text{transfer from atom 0 to 120}
  & \text{floating global Princess response}\\\hline
0.00003&1.426180879958096\\
0.0000345&1.426189261208015\\
0.00004&1.426199504957917
\end{array}
\]

A separate **exact physical** 168-vertex Princess from the
\(0.00003\) solve scores \(1.42618055940783\ldots\)
against that shifted Monster law. This is a rigorous legal response
**above the old certified ceiling**. Thus the three-column
prediction is conclusively rejected, even though its minimizing
cut mix looked encouraging.

For a proposed probability vector \(w_j\ge0\),
\(\sum_{j=1}^{281}w_j=1\), the exact four-column value
\[
\boxed{
B_{\rm cuts}(w)=
\max_{1\le k\le4}\sum_{j=1}^{281}w_j\,C_{kj}
\ \le\ \sup_{p\ {\rm legal}}\mathbb E_{m\sim w}T(m,p)
}                                                     \tag{3}
\]
is a **valid global Princess-response lower bound**, with no
Princess path-basis assumption in the inequality's direction.
Here every \(C_{kj}\) is the exact mean of the two physical
first contacts for one certified Princess path and reflected
Monster pair.

The committed script
\`packages/interval_global_closure/g2_princess_cut_screen.cjs\`
evaluates (3) using exact rational arithmetic. It can reject a
Monster weight proposal **without** executing the expensive
global Princess max-flow. Examples from repository root:

\`\`\`sh
node packages/interval_global_closure/g2_princess_cut_screen.cjs --baseline
node packages/interval_global_closure/g2_princess_cut_screen.cjs --inject 1/100
node packages/interval_global_closure/g2_princess_cut_screen.cjs --transfer 0 120 300000
\`\`\`

The last transfer is an integer numerator at original denominator
\(10^{10}\), hence mass \(3\times10^{-5}\).
\`verify_g2_princess_cuts.cjs\` independently rebuilds the entire
2,248-hit exact cut matrix from the actual physical Princess
trajectories. All four columns were also directly evaluated while
being generated in the connector V8. The standalone CLI wrappers
were committed but were not separately run by native Node here.

**What is (not) closed:** This completes an actual two-oracle
**rejection cycle** and provides a reusable exact finite cut
bank. The bank is **not globally sufficient** for Princess
responses; passing four cuts is not a Monster upper certificate,
and it cannot prove the original game value. G2, the explicit
coupled saddle, remains OPEN.


## 8. NEW exact full-ray exclusions against the best existing upper bound

The previously certified *strongest* unrestricted upper bound on this
branch is the rational Monster common-warp certificate
\[
\boxed{
U_{\rm best}=
\frac{57045188913812444387410009}
{40000000000000000000000000}
\approx1.4261297228453111,
}
\]
from \`packages/interval_common_warp/upper_warp_tight_exact.json\`.
This is strictly smaller than the original **unwarped**
280-pair certificate \(U_0\simeq1.426135325025829\).

Consequently the first exact physical 162-vertex Princess witness
has an even stronger consequence than Section 3:
its payoff \(A\simeq1.4261353108936183\) against \(\nu_0\)
already exceeds \(U_{\rm best}\), and its payoff
\(B\simeq2.999999982512355\) against the added Monster route
also exceeds \(A\). For **every** \(0\le\lambda\le1\),
\[
\boxed{
\sup_p\mathbb E_{\nu_\lambda}T(M,p)
\ \ge\ (1-\lambda)A+\lambda B
\ \ge\ A>U_{\rm best}.}                              \tag{4}
\]
Thus the **entire original-law-plus-best-response injection ray**,
including all arbitrarily small positive masses, is rigorously
excluded as a way to beat the best known upper bound.
Section 3's smaller threshold is still useful for the stronger
comparison to the *unwarped law's own* ceiling \(U_0\).

The four-column exact bank also excludes a **second complete
one-parameter Monster weight direction**. Let \(\nu_\delta\)
take the original 280-pair law and transfer exactly \(\delta\)
probability mass from source atom 0 to atom 120, with
\(0\le\delta\le w_0\) (original mass \(w_0\)).
The valid Princess columns \(k=0\) and \(k=3\)
have exact expected payoffs
\[
g_0(\delta)=a_0+s_0\delta,\qquad
g_3(\delta)=a_3+s_3\delta
\]
with all four rational coefficients in
\`g2_near_active_princess_cuts.json\`.
The signs and ordering are
\[
a_0>a_3,\quad s_0<0<s_3.
\]
Thus their maximum is minimized over the whole interval at
the unique intersection
\[
\delta_*=\frac{a_0-a_3}{s_3-s_0}
 \approx 0.000004620208384168817,
\]
which is strictly inside \([0,w_0]\).
At that point the two scores equal
\[
\boxed{
L_* = a_0+s_0\delta_*
 \approx1.4261332895524503
 > U_{\rm best},
}                                                    \tag{5}
\]
with rigorously positive gap
\[
L_*-U_{\rm best}\approx0.0000035667071391855776.
\]
This is **not** a sampled inequality. For
\(\delta\le\delta_*\), \(g_0(\delta)\ge L_*\)
because \(s_0<0\); for \(\delta\ge\delta_*\),
\(g_3(\delta)\ge L_*\) because \(s_3>0\).
Hence
\[
\boxed{
\forall\delta\in[0,w_0],\qquad
\sup_p\mathbb E_{\nu_\delta}T(M,p)\ge L_*
 > U_{\rm best}.}                                    \tag{6}
\]
Every member of the **entire 0-to-120 sweep-weight reallocation
family** is therefore incapable of improving the best globally
certified upper bound, even though the three-column master had
predicted a promising crossing at a different weight.

These two continuum exclusions are verified by exact
BigInt fractions in
\`packages/interval_global_closure/verify_g2_ray_exclusions.cjs\`.
Its source-file-based calculations were executed successfully
inside the V8 connector runtime; the native CLI wrapper, Lean,
and CI were not separately run.

**G2 impact:** two entire proposed Monster weight-update
directions are eliminated **for all valid masses**, not just at
a finite list of perturbations. Their common obstacle is an
adversarial near-optimal Princess contact germ. This does not
prove optimality of the existing 280-pair support, rule out
simultaneous weight/geometry changes, or identify either
player's optimal global strategy.
