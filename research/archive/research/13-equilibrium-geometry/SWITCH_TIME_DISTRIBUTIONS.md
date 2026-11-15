# Switch-time distributions: exact audit and a timing obstruction

> **Historical law audit.** The decomposition and ablations below concern the retained 752-pair law. The later [continuum one-turn certificate](ONE_TURN_SEPARATION_COUNTERCERTIFICATE.md) gives the stronger upper 142472349375511/100000000000003 and closes the frozen separation comparison negatively. The earlier fixed-law obstructions remain valid; exact one-turn and unrestricted optimality remain open.

This investigates whether the retained Monster law is essentially a mixture of a few one-parameter switch families. The answer is partly positive: its main mass is simple. But exact ablation shows the low-mass residual is important for the saved probabilities. This is **not** a proof that every continuous reweighting of the main families fails, nor a classification of the unrestricted equilibrium.

## 1. Exact physical decomposition

The source is `packages/interval_discovery_certificates/monster_boundary_n256.physical.json.gz`, whose uncompressed SHA256 is `5c736b0c6ef59b418cce0e2e2ef24b0a8dbe4d017a6eca7578d9e1c79616b31d`. Merge duplicate physical paths with different causal calendars, and identify reflected pairs before counting. This gives:

| Physical family | Reflected pairs | Exact probability numerator / 10^12 | Percent |
| --- | ---: | ---: | ---: |
| Direct endpoint sweep | 1 | 629535049023 | 62.9535049023 |
| Endpoint first, then opposite endpoint | 41 | 195416487863 | 19.5416487863 |
| One interior turn, first endpoint exactly at time 2 | 140 | 162756363786 | 16.2756363786 |
| One interior turn, other first-endpoint time | 150 | 6136104025 | 0.6136104025 |
| Two interior turns, then endpoint tour | 387 | 6054719396 | 0.6054719396 |
| Three interior turns, then endpoint tour | 31 | 92665891 | 0.0092665891 |
| Four interior turns, then endpoint tour | 2 | 8610016 | 0.0008610016 |

An **interior turn** is a reversal before the first endpoint hit. The reversal at that endpoint is counted separately. Thus the maximum total reversal count in this retained law is five. The table has 752 physical pairs, not 770 different motions; 770 is the number of path/calendar plans.

The first three rows have total mass **987707900672/10^12 = 98.7707900672%**. Allowing an arbitrary first-endpoint time but still at most one interior turn covers **99.3844004697%**. Allowing at most two interior turns covers **99.9898724093%**.

Use signed initial position a and orient the initial motion rightwards; fair reflection is implicit. In the notation of the bulk-contact manuscript:

- `S(a)` has vertices `(0,a), (1-a,1), (3-a,-1)`, with `-1<a<1`.
- `P(a,b)` has vertices `(0,a), ((b-a)/2,(a+b)/2), (b+1,-1), (b+3,1)`.
- The principal row is `P(a,1)`, so its first switch is `(1-a)/2`, its first endpoint time is 2, and its second endpoint time is 4.
- Endpoint sweeps are separate because actual initial endpoint capture differs from interior limits.

Negative a is necessary: after reflection it describes the positive-start initial-inward branch. Both S and principal P are one-parameter families. The off-schedule P family has two parameters, not one.

## 2. The residual is not dispensable at the saved proportions

Set epsilon = 1/65536. Consider the legal deterministic Princess

`p(t)=epsilon` for `0<=t<=1`, then `p(t)=min(1,epsilon+t-1)`.

She waits just off center until time one, then runs right to the endpoint. Because all tested Monster laws are symmetric, using the fair reflected Princess pair gives the same expectation.

Exact chronological intersection against all 1,504 oriented physical paths gives:

| Fixed physical law | Payoff to this Princess |
| --- | ---: |
| Original saved law | 373447515557123123/262144000000000000 = **1.4245892164502072** |
| Delete all but sweep, S and P(a,1), then renormalize | 370929262655146955/258921699913760768 = **1.4325924122184144** |
| Delete only off-schedule one-interior-turn paths, then renormalize | 124018100879436817/86845152382156800 = **1.4280371152289850** |
| Delete only paths with two or more interior turns, then renormalize | 372322475573959627/260530242767290368 = **1.4290950318060534** |

All three ablated laws have an actual Princess response strictly above the saved global upper **291849329389899/204800000000000 = 1.4250455536616162**. This excludes those **specific renormalized laws** as equally good substitutes. It does not exclude changing the weights or continuous supports of S and P(a,1).

The original residual mass is 1.2292099328%. Its conditional mean capture time against this witness is approximately 0.78150788, versus 1.43259241 for the retained core. Thus the small mass has a substantial strategic role: it catches an escape that the synchronized core handles poorly.

More generally, let mu_core be that fixed renormalized core and let nu be ANY other legal Monster law. For `(1-q)mu_core+q nu`, nonnegativity of capture time implies expectation at least `(1-q)*1.4325924122184144` against this witness. Achieving the old upper therefore requires

`q >= 95412375319086671352367/18111780403083347412109375`, approximately **0.5267973%**.

This is a replacement bound relative to the **fixed core proportions**, not a universal lower bound on mass outside the S/P families.

## 3. Why nearly identical switch times need not be interchangeable

For the same waiting Princess, take `epsilon<a<b<2-a` and the fair pair of P(a,b). The exact physical payoff is

\[
 J_\epsilon(a,b)=\begin{cases}
 b,&b\le1-\epsilon,\\
 b+(1-\epsilon)/2,&1-\epsilon<b\le1+\epsilon,\\
 3(b+1)/4-\epsilon/4,&b>1+\epsilon.
 \end{cases}
\]

**Proof.** The right-oriented Monster stays above the Princess until its inward leg. It catches her at `b-epsilon` if that is at most 1, otherwise at `(b+1-epsilon)/2`. The reflected Monster catches her while she is waiting at `b+epsilon` when `b+epsilon<=1`. If it arrives later, it follows behind her at equal speed and cannot catch her until its positive endpoint at `b+1`. Averaging gives the three branches, including capture at the equality boundary. The parameter assumptions ensure that none of these contacts precedes the Monster turn.

At `b=1-epsilon`, the right limit exceeds the actual contact value by `(1-epsilon)/2`. One-sided contact conventions are therefore essential.

In particular, with `a=1/2`, compare `b=1` and `b=1-2*epsilon`. Their physical Monster paths, including their completed endpoint tours, are uniformly within **2*epsilon** of one another, but

\[
 J_\epsilon(1/2,1)=3/2-\epsilon/2,
 \qquad
 J_\epsilon(1/2,1-2\epsilon)=1-2\epsilon.
\]

For epsilon = 1/65536, the path distance is **1/32768**, while the payoff difference is **65539/131072**, approximately **0.50002289**. The distance bound follows by comparing their common unit-slope segments and the short intervals between their displaced turns; the maximum is attained on the shifted inward leg. The verifier also checks all union-of-knot endpoints, which determine the supremum of the piecewise-affine difference.

This does not prove the optimal law has infinitely many turns. It shows why replacing a narrow collection of switch times by one representative time can fail badly. The rare off-front paths must not be dismissed from their proximity to a main family alone.

## 4. The useful finite-dimensional hierarchy

For an initially rightward unit-speed path with k interior reversals, let `d_0,...,d_k` be the successive leg durations before its first endpoint, and let H be that endpoint time. The endpoint is `e=(-1)^k`, and

\[
 \sum_i d_i=H,\qquad
 \sum_i(-1)^i d_i=e-a.
\]

Hence the total rightward and leftward travel are `(H+e-a)/2` and `(H-e+a)/2`. The path must also remain strictly inside the arena before H. After H, the saved paths take the direct sweep to the opposite endpoint.

For fixed H, the geometric parameter count is k, including a; allowing H to vary adds one. At k=1,H=2 the first leg is forced to `(1-a)/2`. At k=2,H=2 the middle leg is forced to `(1+a)/2`, leaving a and the first-leg duration free. This gives simple parameter domains for the first missing branches.

A natural candidate description is a positive measure on S(a), a measure on P(a,b), and measures on the higher-leg duration domains, all with fair reflection. This is **a distribution on correlated switch histories**, not independent draws of initial position and each switch time. A general optimal-path finite-switch representation is not proved; waiting, non-bang-bang controls and initial-time Zeno limits require their own treatment.

The next geometric question is whether active off-front parameters lie on curves `b=b(a)`, and whether active extra-excursion durations are similarly pinned by record-balance/contact equations. These could yield a few density functions without elementary closed forms. Numerical concentration on a curve is not proof of this support theorem.

## 5. A certified simplification, not a tighter bound

Delete only the 33 pairs with three or four interior turns. Their total mass is **101275907/10^12**. The remaining 719-pair law has at most **two interior turns**, followed by the endpoint reversal. For any Princess, nonnegative capture time gives

\[
 \mathbb E_{\mu_{\rm keep}}T
 \le \frac{U}{1-101275907/10^{12}}
 =\frac{1459246646949495}{1023896293471232}
 \approx1.4251898910604806.
\]

Thus a law with at most three total reversals per trajectory already has an all-Princess guarantee within **0.000144338** of the saved upper. This is a weaker upper inherited from the existing certificate, not a newly optimized law, a new best value bound, or proof that these turn counts are sufficient at equilibrium.

## 6. Reproduction and remaining gate

Run `python3 packages/interval_switch_geometry/audit_switch_geometry.py --output /tmp/switch-geometry.json` from the repository root. It checks the source hash, weights, every physical grid step, duplicate/reflection aggregation, the switch identities, both independent chronological first-contact implementations, 1,504 oriented capture comparisons, and 102 exact rational timing-formula fixtures. It does not rerun the original max-flow upper or prove continuum family optimality by sampling.

**Unresolved:** whether ANY optimally reweighted continuous mixture of sweep, S(a) and P(a,1) attains the unrestricted value; whether the extra families can be eliminated by a different bulk law; and whether a finite collection of switch-history density equations is globally sufficient. The ablation makes it unjustified to set the residual to zero without solving those questions.

## Follow-up: rigorous restricted-game enclosure

The [one-interior-turn subgame proof](ONE_TURN_SUBGAME_BRACKET.md) uses the same exact saved law, a universal reflected-start collision inequality, and quantitative removal of higher-turn paths to show **W_1 <= 1.432964907524812...** against *every* legal Princess. This is a strict improvement over the monotone game value 3/2, but the exact one-turn value and continuous reweighted equilibrium remain open.

