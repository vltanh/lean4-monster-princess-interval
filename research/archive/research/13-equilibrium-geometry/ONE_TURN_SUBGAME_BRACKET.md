# One-interior-turn Monster subgame: rigorous bound, exact value OPEN

**Status:** This is a proved **restricted-game enclosure**, not a solution of the restricted or unrestricted minimax problem. The Princess is fully unrestricted. The Monster has at most one *interior* direction reversal before its first endpoint visit, then completes the opposite endpoint at unit speed. The compulsory reversal at the first endpoint does **not** count as an interior turn.

## Latest physical upper: the separation target is closed

The [continuum countercertificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) proves
\[
 V\le W_1\le\frac{142472349375511}{100000000000003}
 =1.424723493755067\ldots<\frac{57}{40}<U_*.
\]
The proposed target W_1>U_* is false. The exact restricted value and whether W_1=V remain open. The physical law has continuous start densities, and its complete all-Princess potential certificate passes 730,146 exact inequalities with zero repair.

The [375-pair projected certificate](ONE_TURN_PROJECTED_PHYSICAL_UPPER.md), with upper 478205958821456999/335544320000000000, and the older pruning argument below remain valid, weaker certificates. Their bounds are historical rather than current. Since B_1 is contained in B_k for k≥1, the new upper also applies to those larger canonical Monster classes.

## 1. The precise game and theorem

Let \(\mathcal B_k\) comprise all piecewise unit-speed physical Monster paths in \([-1,1]\) that start anywhere, have at most \(k\) interior reversals before their first endpoint, and then sweep directly to the opposite endpoint. This contains endpoint-start sweeps, endpoint-first \(S(a)\), and for \(k\ge1\), interior-turn \(P(a,b)\) routes, including all reflected paths. Set
\[
W_k=\inf_{\nu\in\mathcal P(\mathcal B_k)}
        \sup_{p\in\mathcal A}\mathbb E_{m\sim\nu}T(m,p)
\]
with \(\mathcal A\) the **unrestricted** legal Princess path class. Randomizing the Princess does not increase the displayed supremum against a fixed Monster law. The full-game minimax theorem gives \(V\le W_k\). For \(k=1\), the new [restricted minimax theorem](ONE_TURN_MINIMAX_AND_EXACT_GRID_HIERARCHY.md) proves a separate minimax identity and existence of an optimal physical Monster measure. It also proves convergence of exact dyadic finite Princess lower LPs, without claiming finite optimal support or a finite attaining grid. No corresponding statement for arbitrary \(k\) is asserted here.

**Historical pruning theorem.** Using the earlier retained physical Monster law:
\[
\boxed{\frac{36409808231}{25600000000}\le W_1\le
\frac{1458323028259559}{1017696260809728}
=1.432964907524812\ldots<\frac32.}\tag{1}
\]
With two interior turns:
\[
\boxed{\frac{36409808231}{25600000000}\le W_2\le
\frac{1459235032632867}{1023896293471232}
=1.425178547805600\ldots.}\tag{2}
\]
Both historical pruning bounds are all-Princess inequalities and remain valid. The new continuum certificate above is stronger and improves the unrestricted upper as well.

The \(\mathcal B_0\) class **differs** from the monotone Monster game (whose exact value is \(3/2\)), because an endpoint-first path in \(\mathcal B_0\) reverses at that endpoint. Formula (1) does not prove that an *interior* reversal is necessary to beat \(3/2\).

## 2. Reflected-start separation lemma

**Lemma.** For any continuous unit-speed-bounded Monster path \(m\) starting at \(a\), its reflection \(-m\), and any 1-Lipschitz Princess path \(p\), writing \(s=T(m,p)\), \(t=T(-m,p)\),
\[
\boxed{s+t\ge|a|.}\tag{3}
\]
If either time is infinite, this is trivial. Otherwise \(m(s)=p(s)\), \(-m(t)=p(t)\). Triangle inequality and each path's unit speed give
\[
2|a|
\le |m(0)-m(s)|+|p(s)-p(t)|+|-m(t)-(-m(0))|
\le s+|s-t|+t=2\max\{s,t\}.
\]
Therefore \(s+t\ge\max\{s,t\}\ge |a|\). This includes time-zero captures, endpoint starts, and arbitrarily many original reversals. Sharpness: for \(a>0\), choose \(m(t)=a-t\) until it reaches its endpoint, \(p=m\), giving \(s=0,t=a\). For a fair reflected pair the Princess's expected capture time is thus at least \(|a|/2\).

This simple lower bound on a *removed* part of a Monster mixture makes the restricted upper sharper than ordinary nonnegative-payoff renormalization.

## 3. Pruning a certified law

The unchanged physical source
[monster_boundary_n256.physical.json.gz](../../packages/interval_discovery_certificates/monster_boundary_n256.physical.json.gz)
has 770 rational-weighted physical/calendar plans over 752 distinct reflected path pairs. Its original independently reconstructed physical/casual-clock flow and cut certify
\[
\mathbb E_\nu T(m,p)\le U
:=\frac{291849329389899}{204800000000000}
\quad\text{for every legal Princess }p.
\]
Weights have denominator \(10^{12}\) and initial positions are on the \(1/512\) physical grid. Every retained path has a direct unit-speed tour from its first endpoint to its opposite endpoint, checked byte-for-byte by the script below.

For \(k=1,2\), split this law into an unnormalized retained part of mass \(1-q_k\) on \(\mathcal B_k\), and a discarded part of mass \(q_k\). Let
\[
A_k:=\sum_{\text{discarded reflected pairs }i}w_i\,\frac{|a_i|}{2}.
\]
By (3), for every unrestricted Princess \(p\),
\[
(1-q_k)\mathbb E_{\nu_{\mathrm{keep},k}}T(m,p)+A_k
\le \mathbb E_\nu T(m,p)\le U.
\]
Thus \(W_k\le(U-A_k)/(1-q_k)\), proving the upper parts of (1) and (2).

| Interior turn cap | Discarded mass \(q_k\) | Universal discarded payoff \(A_k\) | Resulting all-Princess upper |
|---|---|---|---|
| \(k=1\) | \(6155995303/10^{12}\) | \(57726168121/64000000000000\) | \(1458323028259559/1017696260809728\) |
| \(k=2\) | \(101275907/10^{12}\) | \(2903579157/256000000000000\) | \(1459235032632867/1023896293471232\) |

There are 345 saved physical/calendar plans in the \(k=1\) retained law: 46 with zero interior reversals, 299 with one interior reversal. The full-game lower \(V\ge36409808231/25600000000\) applies to each restricted Monster game, proving the lower parts of (1) and (2).

Using only nonnegativity would have given \(W_1\le U/(1-q_1)=1.433872465826344\ldots\). The reflected-start inequality improves this to \(1.432964907524812\ldots\). The numerical size of this proof improvement is not a change to the unrestricted game bracket.

## 4. The genuine outstanding subgame problem

The exact \(W_1\) remains **UNKNOWN**, and the result does not determine optimal one-turn weights, support size, or switch-time curves. The exact \(S(a)\) and \(P(a,b)\) *Monster costs against a supplied Princess CDF* are in [BULK_CONTACT_AND_CUSP_EQUATIONS.md](../12-global-closure/BULK_CONTACT_AND_CUSP_EQUATIONS.md). Closing the restricted saddle requires a physical Monster law with an all-Princess upper **and** a matching all-\(\mathcal B_1\) Princess lower. No absolute continuity or finite support of an optimal Monster measure is assumed. Strict/closed first-contact discontinuities matter (see [SWITCH_TIME_DISTRIBUTIONS.md](SWITCH_TIME_DISTRIBUTIONS.md)). Neither finite-bank optimization nor the retained current-law ablations prove that every continuous reweighting of the three principal families fails.

The next structural gate is to solve the \(S(a),P(a,b)\) distribution/contact complementarity with a provably exhaustive Princess response, rather than merely shrinking the numerical interval again.

## 5. Reproduce exact retained-data calculation

Run:
```sh
python3 packages/interval_switch_geometry/verify_one_turn_subgame.py
```

The pure-standard-library script checks the *compressed and uncompressed* source hashes, upper manifest, 770 exact weights, first-endpoint turn counts, direct post-endpoint tours, and every rational fraction in (1)–(2). It does not rerun the already independently certified upper max-flow, prove the global hand-theorem in Lean, or claim an equilibrium solution.
