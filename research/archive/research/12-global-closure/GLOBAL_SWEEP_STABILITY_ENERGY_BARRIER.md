# Global G2 coercivity: quantitative near-sweep barrier

Date: 2026-11-13. **Applies to the original unrestricted game, not a
finite-turn or prescribed-route subclass.** The game value and explicit
equilibrium are still unknown.

## 1. Universal endpoint-arrival energy ledger

For any legal 1-Lipschitz Monster trajectory m that eventually visits
both endpoints, write
\[
 \tau_\pm=\inf\{t:m(t)=\pm1\},\quad
 \sigma=\min(\tau_-,\tau_+),\quad
 \tau=\max(\tau_-,\tau_+),\quad \Delta=\tau-2.
\]
The first- and second-endpoint visits satisfy
\(0\le\sigma\le\tau-2\), so \(\Delta\ge0\).
Stop m at the second endpoint after time \(\tau\). This changes
**no first-contact time** against any legal Princess, since visiting
the opposite endpoints already forces a contact by continuity.

Let f be the first endpoint reached and d=-f the direction to its
opposite. Over [sigma,tau] define
\[
 B=\int_\sigma^\tau(-d m')_+dt,\quad
 I=\int_\sigma^\tau(1-|m'|)dt .
\]
Both are nonnegative even for paths with infinitely many reversals.
The forward variation is 2+B, so exact time accounting gives
\[
 \boxed{\tau-\sigma=2+2B+I,\qquad
 \mathcal E:=\frac{\tau_-+\tau_+}{2}-1
       =\sigma+B+\frac I2.}                         \tag{1}
\]
In particular \(\Delta/2\le\mathcal E\le\Delta\).

For **every** globally optimal Monster law \(\nu_*\), not only a
symmetric one, its expected capture time against the stationary
Princess paths at -1 and +1 is at most the unrestricted value V.
Thus
\[
 \mathbb E_{\nu_*}\tau_\pm\le V\le U_{\rm best},
 \quad U_{\rm best}=
 \frac{57045188913812444387410009}
 {40000000000000000000000000}.
\]
It follows that
\[
\boxed{
 \mathbb E_{\nu_*}[\sigma+B+I/2]\le U_{\rm best}-1
 =0.426129722845311\ldots .}                      \tag{2}
\]
Since the first endpoint cannot be reached before
\(1-|m(0)|\), this also gives the unrestricted initial-position
moment restriction
\[
\boxed{\mathbb E_{\nu_*}|M(0)|\ge2-U_{\rm best}
 =0.573870277154688\ldots .}                      \tag{3}
\]

## 2. A UNIFORM rigidity lemma across all Monster paths

Let \(m^c\) be m stopped after the second endpoint.
Let \(m_f(t)=f(1-\min(t,2))\) be the fastest sweep
starting at its FIRST endpoint f.

**Lemma 1.** Irrespective of Monster waits, slower speeds,
or infinitely many interior reversals,
\[
 \boxed{\sup_{t\ge0}|m^c(t)-m_f(t)|\le\tau-2=\Delta.}
                                                               \tag{4}
\]

**Proof.** Before the first endpoint time \(\sigma\), the speed
bound and the future equality m(sigma)=f give
\(|m(t)-f|\le\sigma-t\). The sweep and m stay on the same
interior side of f; their displacement difference is at most
\(\max(\sigma-t,\min(t,2))\le\sigma\le\Delta\).
Between the endpoint visits orient x by d=-f and put
\(y(t)=d(m(t)-f)\in[0,2]\).
From the first endpoint,
\(y(t)\le t-\sigma\). From the required second endpoint,
\(y(t)\ge 2-(\tau-t)\). For times t in [sigma,2], the fast
sweep has oriented position t; the separation
\(t-y(t)\) is between 0 and \(\tau-2\).
For t in [max(sigma,2),tau], the fast sweep is at
oriented position 2, and
\(0\le2-y(t)\le\tau-t\le\tau-2\).
Both routes coincide after tau. QED.

This is a global *control-space rigidity* statement.
Small \(\Delta\) forces uniform physical proximity to one
of the two fastest sweeps even for arbitrary Zeno behavior.

## 3. A physically robust Princess adversary

For epsilon in (0,1), define
\[
 p_\epsilon(t)=\min(-1+\epsilon+t,1),\qquad
 \mu_\epsilon=\tfrac12(\delta_{p_\epsilon}
                      +\delta_{-p_\epsilon}),\qquad
 J_\epsilon(m)=\mathbb E_{\mu_\epsilon}T(m,P).
\]
The exact unrestricted two-runner speed-separation theorem,
proved independently in ALL_MONOTONE_SUBGAME_EXACT.md, gives
\[
 \boxed{J_\epsilon(m)\ge(1-\epsilon)/2}
                                                               \tag{5}
\]
for ALL Monster m; this does not rely on a sweep approximation.

**Lemma 2.** If a Monster visits both endpoints with
\(\Delta<\epsilon\), then
\[
 \boxed{J_\epsilon(m)\ge
 \frac32-\frac{\epsilon}{4}-\frac{3\Delta}{4}.}
                                                               \tag{6}
\]

**Proof.** By symmetry take its first endpoint to be -1.
Lemma 1 gives \(m^c(t)\le m_+(t)+\Delta\), where
\(m_+(t)=-1+\min(t,2)\). The runner \(p_\epsilon\)
is strictly above m until time 2-epsilon because it
is epsilon above m_+; it then remains at +1 and
cannot be captured before 2-Delta. Thus
\(T(m,p_\epsilon)\ge2-\Delta\).
The reflected runner is strictly above m until
\(1-(\epsilon+\Delta)/2\), since its distance above
m_+ before that time is \(2-\epsilon-2t>\Delta\).
Hence \(T(m,-p_\epsilon)\ge
1-(\epsilon+\Delta)/2\). Average, and reflect
the proof when the first endpoint is +1. QED.

**Theorem 1 (GLOBAL affine sweep-stability inequality).**
For ANY endpoint-completed Monster path and ANY epsilon in (0,1),
\[
 \boxed{J_\epsilon(m)\ge
 \frac32-\frac{\epsilon}{4}-
             \left(\frac1\epsilon+\frac14\right)\Delta(m).}
                                                               \tag{7}
\]
For \(\Delta<\epsilon\), use (6) and
\(1/\epsilon+1/4>3/4\). For \(\Delta\ge\epsilon\),
the right side of (7) is no greater than
\((1-\epsilon)/2\), so (5) applies. QED.

The SAME Princess law \(\mu_\epsilon\) works for every Monster
path. Thus, for ANY probability law \(\nu\) of paths completing
both endpoints with \(\bar\Delta=\mathbb E_\nu(\tau-2)<\infty\),
\[
 \boxed{\sup_{p\ {\rm legal}}\mathbb E_\nu T(M,p)
   \ge\frac32-\frac{\epsilon}{4}-
       \left(\frac1\epsilon+\frac14\right)\bar\Delta.}
                                                               \tag{8}
\]
If \(\bar\Delta\le1/4\), optimize by
\(\epsilon=2\sqrt{\bar\Delta}\) (using one-sided limits
at the interval endpoints) to get
\[
 \boxed{\sup_p\mathbb E_\nu T(M,p)
       \ge\frac32-\sqrt{\bar\Delta}-\bar\Delta/4.}
                                                               \tag{9}
\]

**No continuity of physical first-contact time is invoked.**
The proof is based on explicit strict spatial separation,
a common Princess law, and the exact universal two-runner floor.

## 4. EVERY full-game optimal law needs positive macroscopic deviation

For every original-game Monster optimum \(\nu_*\),
global minimax gives \(\sup_p\mathbb E_{\nu_*}T(M,p)
=V\le U_{\rm best}\). Put
\(a=3/2-U_{\rm best}
=0.07387027715468889\ldots>0\).
Equation (9) (or its trivial large-delay alternative) forces
\[
 \boxed{
 \mathbb E_{\nu_*}[\tau(M)-2]
   \ge4(\sqrt{1+a}-1)^2
   =0.005264118822885991\ldots .}                 \tag{10}
\]
The optimizing test-runner displacement is
\(\epsilon_*=4(\sqrt{1+a}-1)
=0.14510849489793478\ldots\).

A simpler RATIONAL certificate follows by fixing
epsilon=1/7 in (8):
\[
 \boxed{
 \mathbb E_{\nu_*}[\tau-2]\ge
 \frac{10683677603312889288129937}
 {2030000000000000000000000000}
 =0.00526289537109\ldots>\frac1{200}.
 }                                                  \tag{11}
\]
In particular every optimal Monster law assigns positive
probability to routes that do not complete the second endpoint
until after time \(2+1/200\). This excludes an entire
infinite-dimensional neighborhood of arbitrarily small
trajectory detours, not only a collection of finite mixing rays.

Equations (1)--(2) and (10) give the **two-sided, full-game
endpoint-delay energy budget**
\[
 \boxed{
 2(\sqrt{1+a}-1)^2
 \le\mathbb E_{\nu_*}[\sigma+B+I/2]
 \le U_{\rm best}-1.}                               \tag{12}
\]
Numerically this is
\(0.00263205941144\ldots\le\mathbb E\mathcal E
 \le0.426129722845311\ldots\).

**Effect on the global CDF/causal-clock dual:** EVERY exact
minimizer in GLOBAL_INFINITE_HORIZON_ACTIVE_DUAL.md
must have an underlying Monster law obeying (10)--(12).
This is a nontrivial global feasibility constraint on the
unknown reversing-history occupation, regardless of the
choice of causal record clock.

## 5. Verification and limits

The accompanying independent standard-library Fraction regression,
packages/interval_global_closure/verify_global_sweep_stability.py,
enumerates **1,050 completed polygonal Monster paths** on a
half-unit space/time grid, including waits and reversals.
For seven exact rational epsilon offsets it checks
physical first contacts, sup-norm sweep rigidity,
the exact B/I time-energy decomposition, and both
inequalities (6) and (7). All checks passed locally.

This analytic theorem does NOT identify the full game value,
construct a matching CDF/Monster law, show an optimal
finite turn bound, or improve the established
\(1.4175898349\ldots\le V\le1.4261297228\ldots\)
numeric interval. No Lean/CI claimed. G2/G5 constructive
closure remain OPEN.

**Next proper global gate:** include the coercive
mean-completion constraint (10) in the exact
Monster-clock occupation optimization, and find
a Monster active-record measure and Princess
transport CDF whose global radial and Monster
Bellman certificates coincide. Do not return to
isolated turn-count classes.


## 5. STRONGER GLOBAL RESULT: a continuum of Princess offsets

The fixed-epsilon argument in Sections 3--4 proves a global bound
but does not exploit the Princess's ability to choose an **entire
continuous offset distribution**. Fix 0<A<1 and independently
sample \(\epsilon\sim\mathrm{Uniform}(0,A)\),
then choose one of \(p_\epsilon,-p_\epsilon\) fairly.
Call this fully legal Princess distribution \(\mu_A\).
This is a strategy tested against the WHOLE Monster path space,
not the proposed global optimal Princess CDF.

For any completed Monster m with
\(d=\tau(m)-2\), integrate the **two rigorous
pathwise response cases (5)--(6)**:
for \(0<\epsilon\le d\), score at least
\((1-\epsilon)/2\); for \(d<\epsilon<A\),
score at least \(3/2-\epsilon/4-3d/4\).
Exact integration yields
\[
 \boxed{ \mathbb E_{\mu_A}T(m,P)\ge L_A(d):=
 \begin{cases}
 \frac32-\frac A8-(\frac1A+\frac34)d+
                         \frac{5d^2}{8A},&0\le d\le A,\\[2mm]
 \frac12-\frac A4,&d\ge A .
 \end{cases}}                                      \tag{14}
\]

**NEW convexity fact.** The function \(d\mapsto L_A(d)\)
is continuous, globally nonincreasing, and **convex** on
\([0,\infty)\): on \([0,A]\) its second derivative is
\(5/(4A)>0\), and its left derivative at A is
\(1/2-1/A<0\), while its right derivative is zero.
This means Jensen applies with NO bound on how the
Monster law mixes tiny and very large detours.

**Theorem 2 (continuum-offset global stability certificate).**
For EVERY Monster probability law on all endpoint-completing
1-Lipschitz paths with finite mean completion lateness,
\[
\boxed{
 \sup_{p\ {\rm legal}}\mathbb E_\nu T(M,p)
 \ge \mathbb E_{\nu,\mu_A}T(M,P)
 \ge \mathbb E_\nu L_A(\Delta(M))
 \ge L_A(\mathbb E_\nu\Delta(M)).
}                                                   \tag{15}
\]
All inequalities are exact and hold with arbitrarily many
Monster turns, countable/uncountable Monster support,
atomic first contacts and Zeno behavior.
The second inequality uses the same fixed continuum
Princess law against all Monster histories.

For \(0<d<1/8\), optimize the first branch
over A. Its maximum occurs at
\[
 A=\sqrt{8d-5d^2}\in(d,1)
\]
and is
\[
\boxed{
 \sup_{p}\mathbb E_\nu T(M,p)
 \ge \frac32-\frac{3d}{4}
      -\sqrt{\frac d2-\frac{5d^2}{16}},
 \quad d=\mathbb E_\nu\Delta(M)\in(0,1/8).
}                                                   \tag{16}
\]

Therefore, for ANY optimal Monster law,
\(V\le U_{\rm best}\) and (15)--(16)
force the **stronger nonzero full-game completion delay**
\[
\boxed{
 \mathbb E_{\nu_*}[\tau-2]\ge
 d_*:=\frac{2}{7}
 \left(1+3a-\sqrt{1+6a-5a^2}\right)
 =0.0090511656481067386\ldots ,
 \quad a=\frac32-U_{\rm best}.
}                                                   \tag{17}
\]
To verify (17), set the right side of (16)
equal to \(U_{\rm best}=3/2-a\), square
with the nonnegative square-root side, and
solve
\(7d^2-(12a+4)d+8a^2=0\).
The smaller root is exactly (17), and the
first-branch expression is decreasing in d
on the relevant interval. If d is at least
1/8, (17) is automatic.

There is also a very simple **rational** proof
of the macroscopic threshold
\[
\boxed{ \mathbb E_{\nu_*}[\tau-2]>
 \frac{181}{20000}=0.00905.}                         \tag{18}
\]
Choose fixed \(A=4/15\). At d=181/20000,
exact Fraction arithmetic gives
\[
 L_{4/15}(181/20000)
  =\frac{2190541249}{1536000000},
\]
and the strictly positive difference from
the archived certified upper \(U_{\rm best}\) is
\[
\boxed{
 \frac{468336687666837769973}
      {120000000000000000000000000}>0.
}
\]
Since \(L_A\) is strictly decreasing for
d<A, any Monster law with mean delay
\(d\le181/20000\) would have
unrestricted Princess response STRICTLY
larger than \(U_{\rm best}\); it therefore
cannot be optimal. The same statement
excludes an entire infinite-dimensional
set of proposed Monster upper certificates
at or below \(U_{\rm best}\).

Using \(\mathcal E\ge\Delta/2\),
the strengthened energy lower bound is now
\[
\boxed{\mathbb E_{\nu_*}[\sigma+B+I/2]
 \ge d_*/2 =0.0045255828240533693\ldots.}           \tag{19}
\]
This supersedes the weaker lower endpoints
in (10)--(13), which remain valid.

**Verification:** the same Fraction script
now independently integrates both pieces of
the continuous-offset lower response and
checks the closed form for rational A,d,
the global affine minorant, and the exact
strictly positive rational U-gap above.
The integral argument is proved in the text;
finite probes do not replace the convexity
and Jensen proof.

**Status unchanged:** this is a global
quantitative obstruction, not a new
unrestricted value bound or a complete saddle.
There is still no finite turn-count cutoff
or explicit matching Monster/Princess field.
