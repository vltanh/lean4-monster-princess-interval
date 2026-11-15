# Audit of the paper and the formalization

Paper: S. Alpern, R. Fokkink, R. Lindelauf and G.-J. Olsder, *The "Princess and Monster" game on an
interval*, SIAM J. Control Optim. 47(3) (2008), 1178–1190,
[doi:10.1137/060672054](https://doi.org/10.1137/060672054). The paper has no arXiv version and no
public TeX source. The audit was made against the published PDF and the authors' preprint
[LSE-CDAM-2006-17](http://www.cdam.lse.ac.uk/Reports/Files/cdam-2006-17.pdf) (November 2006), whose
text is nearly identical. Section, result and equation numbers are those of the published version;
its equation numbers are the preprint's minus one from (4) to (12). The two formulas for
`V(S₁, h_Φ)` and `V(S₂, h_Φ)` of Section 5 are unnumbered in the published version and numbered
(15) in the preprint; this report calls them (15). Labels such as `thm:16` are the formalization's
own, since there is no TeX source.

Status of the formalization:

- Every numbered result of the paper is stated and proved. So are the paper's Section 1 claim that
  the game has a value and its main result, `15/11 ≤ V ≤ 13/9`.
- The two results that the paper cites in its proofs are proved in [`External/`](External), so the
  formalization assumes nothing:
  - the minimax theorem of Alpern and Gal (1988), from Mathlib's Sion theorem;
  - the special case of Alpern and Asic's Theorem 3 that the paper uses.
- `lake build` prints no warning besides the two intended `sorry`s of [`Challenge.lean`](Challenge.lean). There is
  no `axiom`, `admit` or `native_decide`. [`scripts/Audit.lean`](scripts/Audit.lean) checks that every declaration of
  the library uses only [`propext`](https://leanprover-community.github.io/mathlib4_docs/Init/Core.html#propext), [`Classical.choice`](https://leanprover-community.github.io/mathlib4_docs/Init/Prelude.html#Classical.choice) and [`Quot.sound`](https://leanprover-community.github.io/mathlib4_docs/Init/Prelude.html#Quot.sound).
- [`Challenge.lean`](Challenge.lean) states, in Mathlib's vocabulary, that the game has a value and that
  `15/11 ≤ V ≤ 13/9`. [`Solution.lean`](Solution.lean) proves it, and Comparator accepts it under the Lean kernel
  and nanoda.
- Two statements of the paper are false at a boundary case and are formalized in corrected form
  (E11, E13). Two displayed formulas are misprinted and are formalized corrected (E14, E17).
- The proofs follow the paper's arguments. Where the paper has gaps, a proof departs from it only
  at the defective step; Section 7 lists every departure.

## 1. Summary

| Kind | Findings |
| --- | --- |
| Errors | E1 the capture time is lower, not upper, semicontinuous; E11 Lemma 11 fails at one starting point; E13 formula (9) fails at `y = 1`; E14 formula (11) has a wrong limit; E15 a Riemann-sum inequality points the wrong way; E17 formula (15) is misprinted, and Figure 3 does not match the strategy |
| Gaps | E3 the path of Proposition 1's proof leaves the interval; E4 the restriction to a dense set of hider paths is not justified; E5 Proposition 3's construction can stall; E6 Proposition 5 is "obviously optimal"; E7 Proposition 7's "consequently" has no argument; E8 the approximation by nonintersecting paths; E10 Theorem 10's reduction to five responses; E12 Lemma 12's first-order argument; E16 Theorem 16's reduction to `S₁, S₂` |
| Inconsistencies | E2 "end-reflecting" is defined over one time unit, the text says two; E9 Section 3 claims strict inequalities that its strategies do not give |
| Missing hypotheses | none in the paper's results; the cited minimax theorem needs a nonempty strategy space (Section 2) |
| Redundant hypotheses | Proposition 3: smoothness; Proposition 7: the searcher's speed limit; formula (11): `y ≤ 1` |
| Use of cited results | Alpern–Gal: applied correctly, but its hypothesis is misstated (E1); Alpern–Asic: correct |
| Typos | E18 |

None of the errors affects the main results: `15/11 ≤ V ≤ 13/9` and Theorems 9, 10, 14 and 15
hold as stated.

## 2. Results from prior work and how the paper uses them

### Proved in `External/`

| Result | Where the paper uses it | Source | Theorem in `External/` |
| --- | --- | --- | --- |
| Mixed-strategy minimax theorem: for a compact Hausdorff minimizer space and a payoff lower semicontinuous in the minimizer's strategy, the value exists, the minimizer has an optimal strategy, and the maximizer has `ε`-optimal finitely supported ones | Section 1 (the value `V`); Proposition 4; the remarks after it | Alpern and Gal, SIAM J. Control Optim. 26 (1988); Appendix A of Alpern and Gal, *The Theory of Search Games and Rendezvous* (2003) | [`External.AlpernGal.minimax`](External/AlpernGal/Minimax.lean#L539) |
| Optimal strategies invariant under the isometry group of the network (for the interval, `{id, φ}` with `φ(x) = -x`) | Proposition 4 | Alpern and Asic, Networks 15 (1985), Theorem 3 | [`External.AlpernAsic.theorem3_minimizer`](External/AlpernAsic/Theorem3.lean#L49), [`External.AlpernAsic.theorem3_maximizer`](External/AlpernAsic/Theorem3.lean#L65) |

[`External.AlpernGal.minimax`](External/AlpernGal/Minimax.lean#L539) is proved for every nonempty compact Hausdorff space, without
metrizability, and about non-regular Borel measures too. The proof:

- applies Mathlib's Sion theorem to finitely many maximizer strategies and truncated payoffs;
- passes to the limit with Prokhorov compactness of the probability measures and the
  Riesz–Markov–Kakutani regularization of a limit point.

The space must be nonempty: there is no probability measure on the empty space, so without this
hypothesis the statement is false. The paper's searcher space is nonempty.
[`PrincessMonster.value_exists`](PrincessMonster/Value.lean#L167) applies the theorem to the searcher's paths. It uses that they
form a compact space (Arzelà–Ascoli) and that the capture time is lower semicontinuous in the
searcher's path.

The Alpern–Asic averaging is stated in game-theoretic terms, for a payoff invariant under
involutions of the two strategy spaces; [`proposition4`](PrincessMonster/Section2/Symmetric.lean#L96) applies it to `S ↦ -S`.

### Standard facts used without citation

| Fact | Where | In the formalization |
| --- | --- | --- |
| Intermediate value theorem | Propositions 1, 2, 3, 7; Theorem 9; Lemma 11 | `intermediate_value_Icc'`, through [`captureTime_le_of_le_of_le`](PrincessMonster/CaptureTime.lean#L83) |
| Arzelà–Ascoli: the searcher's paths form a compact space | Section 1 | `ArzelaAscoli.isCompact_of_equicontinuous`, in [`compactSpace_searcherPaths`](PrincessMonster/Value.lean#L100) |
| Integration by parts | Lemma 13 | Mathlib's interval integration by parts |
| Layer-cake formula `E T = ∫ P(T > t) dt` | Theorem 9 (the paper's `P(t)`), Lemma 12 | [`Mathlib.MeasureTheory.Integral.Layercake`](https://leanprover-community.github.io/mathlib4_docs/Mathlib/MeasureTheory/Integral/Layercake.html), and explicit Tonelli arguments |
| Value of small matrix games by linear programming | (4); Theorems 15 and 16 | explicit optimal strategies, checked by `norm_num` |

### Does the paper use each cited result correctly?

| Cited result | Where | Verdict |
| --- | --- | --- |
| Alpern–Gal minimax theorem | Section 1 | Its hypothesis is stated as "the payoff function `T` is upper semicontinuous", which is false (E1). The theorem needs `T` lower semicontinuous in the searcher's path, which is true, so the conclusion stands. |
| Alpern–Asic, Theorem 3 | Proposition 4 | Correct: the special case of the group `{id, φ}`, an averaging argument. |

The paper's other citations give context and are not used in proofs:

- Isaacs (1965);
- the circle: Zelikin (1972), Alpern (1974);
- the immobile hider: Dagan and Gal, Alpern, Gal, and Reijnierse and Potters;
- Kikuta;
- rendezvous: Howard (1999), Chester and Tutuncu (2004);
- Parsons (1978);
- Alpern and Gal's observation for rendezvous on the line, of which Proposition 5 is said to be a
  simplified version.

## 3. Errors and gaps in the paper

### E1. Section 1: the capture time is lower, not upper, semicontinuous

The paper: "Taking the topology of uniform convergence on compact subsets, the payoff function `T`
is upper semicontinuous", and again after Proposition 4: "The capture time `T(S, H)` is upper
semicontinuous as a function on the pure strategies". This is false. Take the searcher path `S ≡ 0` and the hider path
`H(t) = min(1, (t - 1)²)`, which touches `S` at `t = 1`, so `T(S, H) = 1`. The paths
`H + 1/n` (capped at `1`) converge to `H` uniformly and never meet `S`, so their capture times are
`∞`. Hence `limsup T(S, H_n) = ∞ > T(S, H)`.

`T` is lower semicontinuous on pairs of paths. If `T(S, H) > c`, then `|S - H|` has a positive
minimum on `[0, c']` for every `c' < T(S, H)`, and uniform convergence on `[0, c']` preserves this.
Lower semicontinuity in the searcher's path is exactly what the minimax theorem of Alpern and Gal
needs, so the existence of the value is unaffected. Geupel's bachelor's thesis (2011, Section 10)
already calls `T` lower semicontinuous. Lean: [`lowerSemicontinuous_captureTime`](PrincessMonster/Value.lean#L41), `value_exists`.

### E2. Section 2: the definition of end-reflecting

The paper defines `S` to be end-reflecting if `S(t₀) = ±1` implies `|S(t) - S(t₀)| = t - t₀` for
`t₀ ≤ t ≤ t₀ + 1`. The text before it says "once the searcher reaches an end, he should go
directly to the other end", which is the window `t₀ ≤ t ≤ t₀ + 2`. Both versions of Proposition 1
are true and both are proved: [`proposition1`](PrincessMonster/Section2/Dominance.lean#L245) ([`EndReflecting`](PrincessMonster/Section2/Dominance.lean#L31), as printed) and
[`proposition1_sweeping`](PrincessMonster/Section2/Dominance.lean#L257) ([`EndSweeping`](PrincessMonster/Section2/Dominance.lean#L37), as the text describes).

### E3. Proposition 1: the dominating path leaves the interval

The proof defines `S*` "as `S` up to time `t₀` and then equal to `1 + t₀ - t`". This path leaves
`[-1, 1]` after `t₀ + 2`, so it is not a searcher path. The intermediate value argument itself is
sound: `S(t₁) ≥ 1 - (t₁ - t₀) = S*(t₁)` for every meeting time `t₁ ≥ t₀`, and every hider path
is met by `t₀ + 2`.

The repair continues `S*` after `t₀` by sweeping from end to end (a triangle wave), which agrees
with the paper's `S*` on `[t₀, t₀ + 2]`. The proposition holds.
Lean: [`proposition1`](PrincessMonster/Section2/Dominance.lean#L245), [`proposition1_sweeping`](PrincessMonster/Section2/Dominance.lean#L257).

### E4. Section 2: the restriction to a dense set of hider paths

"By reasons that will become clear below, we may restrict the pure hider strategies to any subset
that is dense in `S`. In particular, we may consider smooth paths only, without changing the value
of the game." The reasons are not given later, and "dense in `S`" should presumably read "dense in
`ℋ`".

For the upper value the claim holds. For a searcher mixed strategy `μ`, the map
`H ↦ E_μ T(·, H)` is lower semicontinuous by E1 and Fatou's lemma. So its supremum over a dense
set is its supremum over all paths.

The formalization does not need the claim. Proposition 3 holds for every continuous hider path
(E5), so no restriction to smooth paths is made. The claim itself is not formalized (Section 9).

### E5. Proposition 3: the construction of `H*` can stall

The proof defines `t₀ = inf {t : |H'(t)| > 1}`, lets `H*` run at unit speed until it meets `H` at
some `τ > t₀`, and "repeats the construction inductively".

- The first meeting after `t₀` can be `t₀` itself. Take `H'(t) = 1 + (t - t₀) sin(1/(t - t₀))`
  near `t₀`: the difference `H - H*` changes sign infinitely often near `t₀`.
- The times `t₀ < τ < t₁ < …` can accumulate, and then the induction does not reach every time.

The repair defines the same path, the one that follows `H` when it can and otherwise runs towards
it at unit speed, by a closed formula:

`H*(t) = inf_{s ≤ t} (L(s) + t - s)`, where `L(s) = sup_{r ≤ s} (H(r) - (s - r))`.

This path has speed at most `1`, and `U(t) ≤ H*(t) ≤ L(t)`, where
`U(t) = inf_{s ≤ t} (H(s) + t - s)`. The paper's argument, "`H*` cannot be caught from behind",
then applies verbatim.

The proposition holds for every continuous hider path, smooth or not. Lean: [`proposition3`](PrincessMonster/Section2/Dominance.lean#L477), and
the general form [`proposition3_of_continuous`](PrincessMonster/Section2/Dominance.lean#L491).

### E6. Proposition 5: "obviously optimal"

The proof says that "it is obviously optimal for the searcher to run toward `H_σ(j+1)` after he
has met `H_σ(j)`". The missing step is that the greedy chase reaches the next hider no later than
`S` does. The chase starts from the point where it met the previous hider, at a time no later than
`S` met it. The target has speed at most `1`, and the chase-then-follow path is
`min (p + (t - a)) (X t)`. The bound follows from the triangle inequality along the previous
hider's path and `S`. The proposition holds. Lean: [`proposition5`](PrincessMonster/Section2/Greedy.lean#L359), through [`greedy_chase_fastest`](PrincessMonster/Section2/Greedy.lean#L257).

### E7. Proposition 7: "Consequently, any finite mixed hider strategy may be assumed to consist of noncrossing pure strategies"

The paper proves only the case of two paths with equal probabilities. Repeating it along a sorting
network handles equal weights, hence rational weights (duplicate the paths). Two paths with
weights `p > q` also reduce to it: `p H₁ + q H₂` is dominated by
`q (H₁ ∧ H₂) + q (H₁ ∨ H₂) + (p - q) H₁`, and these three paths do not cross. For several paths
with irrational weights the paper gives no argument.

The statement holds for arbitrary weights. Replace the mixture by its quantile paths:

`Q_u(t) = min over sets A of indices with weight ≥ u of max_{i ∈ A} H_i(t)`.

These paths are noncrossing, finitely many and continuous, and the new mixture dominates the old
one. At each time, the paths that stay above (below) the searcher carry at least the old mass. Lean:
[`proposition7_finite`](PrincessMonster/Section2/Noncrossing.lean#L414), for arbitrary weights in `[0, ∞]`.

### E8. After Proposition 7: approximation by nonintersecting paths

"Any finite collection of noncrossing paths can be approximated arbitrarily closely by a
collection of nonintersecting paths. So, there exist `ε`-optimal mixed hider strategies that are
finite, symmetric and nonintersecting."

Closeness of the paths does not by itself give closeness of the payoffs, since `T` is not
continuous (E1). The step does hold for the hider: by joint lower semicontinuity of `T` and
compactness of the searcher's space, the hider's guaranteed payoff can only increase in the limit.
It needs this argument. The passage is not formalized (Section 9); Proposition 8 takes a
nonintersecting symmetric strategy as its hypothesis.

### E9. Section 3: strict inequalities

Section 3 announces "`1 < 97/75 < V < 47/32 < 3/2`". The strategies of Section 3 give only
`97/75 ≤ V ≤ 47/32` (Theorems 9 and 10). The strict inequalities hold, by the main result
`15/11 ≤ V ≤ 13/9`. Lean: [`section3_bounds`](PrincessMonster/Main.lean#L31), proved from `main`.

### E10. Theorem 10: the reduction to `A, B, C, D, M`

The paper argues as follows. By Proposition 5 the searcher starts at `0`, `±1/2` or `±1` and runs
between hider paths. From an end, "by Proposition 1 it is optimal to adopt strategy `A`". From `0`
he plays `B` or `M`, and from `±1/2` he plays `C` or `D`. The value `97/75` of the matrix game (4)
is then a lower bound on `V`.

Two steps are not justified:

- The enumeration is informal: a greedy path can visit the six hider paths in 720 orders.
- For a start at an end, the construction in the proof of Proposition 1 does give `A`; but its
  statement, which is what the proof cites, says only that some end-reflecting path dominates.
  The formal proof bounds the paths that start at an end directly from the speed limit.

The conclusion holds. Against the optimal hider mixture of (4), weights `31, 24, 20, 0` (over 75)
on `E, F, G, H`, every searcher path starting at `1`, `0` or `1/2` pays at least
`97/75 - 42ε/150`, whatever it does afterwards. The bound comes from the speed limit and the
intermediate value theorem, with a few case splits; reflection gives `-1` and `-1/2`.
Proposition 5 makes these the only starts.

An exhaustive check of all 8! greedy orders (numerically, before the proof) confirms the bound. It
also confirms the paper's matrix entries. Lean: [`theorem10`](PrincessMonster/Section3/Theorem10.lean#L794), [`equation4`](PrincessMonster/Section3/Theorem10.lean#L348), [`matrix4_value`](PrincessMonster/Section3/Theorem10.lean#L418).

### E11. Lemma 11: false at one starting point, and Proposition 8 applied to a single path

The proof begins "By Proposition 8 we may assume that `H ≥ 0`". Proposition 8 concerns the pure
strategies of a symmetric nonintersecting mixed strategy. Lemma 11 is about an arbitrary pure
strategy `H`, so the reduction does not apply.

The statement, an "if and only if", is false at the starting point `x = H(y) - y`. Take
`H(t) = t` on `[0, 1/2]`: `H` runs towards the sweeper `A`, meets it at `y = 1/2`, and then
follows it. The right runner starting at `0 = H(0)` catches `H` at time `0 < y`. But `0` does not
lie in `(H(y) - y, H(0)] = (0, 0] = ∅`.

The lemma holds for every hider path of speed at most `1`, whichever sweeper it meets first,
when the starting points `x = H(y) ∓ y` are excluded. Excluding them does not matter downstream,
since they carry no mass for an atomless `Φ`. Lean: [`lemma11`](PrincessMonster/Section4/Lemmas.lean#L316).

### E12. Lemma 12: the first-order argument, and smoothness

The proof counts the searchers who catch the hider during `[t, t + Δt]` "up to first order". It
writes the probability as `f(H(t) - t)(ΔH - Δt)`, which is negative: it should be
`f(H(t) - t)(Δt - ΔH)` (E18).

The lemma uses `H'`. Proposition 3's dominating path is not smooth (E5), but it has speed at most
`1`, so `H'` exists almost everywhere, and (5) and (6) still hold for it by a change of variables
for Lipschitz functions. The gap is the first-order argument, not smoothness.

The repair is a layer-cake identity that needs neither smoothness nor derivatives. A right runner
starting at `x` has not met `H` by time `s` exactly when `H(s) - s > x`, because `H(t) - t` is
nonincreasing. Hence the expected time of the early catches is
`∫₀^y (Φ(H(t) - t) - Φ(1 - 2y)) dt`: the integrated form of Lemma 13, valid for every path of
speed at most `1` ([`s4_lemma13'`](PrincessMonster/Section4/Lemmas.lean#L694)). Lemma 12, for smooth paths, follows from it by one integration
by parts, and the payoff formula (9) is proved from it. Lean: [`lemma12`](PrincessMonster/Section4/Lemmas.lean#L796), [`s4_lemma13'`](PrincessMonster/Section4/Lemmas.lean#L694),
[`equation9`](PrincessMonster/Section4/Lemmas.lean#L1129).

### E13. Formula (9) fails at `y = 1`

Formula (9) is derived for a hider path of speed at most `1` that meets the sweeper `A` first, at
time `y`, and then runs to the end `+1`. Its derivation says that the left runners starting left
of `x` "catch `H` at time 2". When `y = 1`, the path meets both sweepers at once, at `0`. Running
to `+1` it then moves along `-A`, and the left runners, which have joined `-A`, catch it at time
`1`. Take `H(t) = max(0, t - 1)` with `Φ` uniform. The payoff is `3/4`, while (9) and (10) give
`1`.

For `y < 1` formula (9) is correct, and as an upper bound it holds for every `y`. The formal
[`equation9`](PrincessMonster/Section4/Lemmas.lean#L1129) requires the hider to meet `A` strictly first, which forces `y < 1`. [`equation9_le`](PrincessMonster/Section4/Lemmas.lean#L1181),
the bound that Theorem 14 uses, has no such restriction. The boundary case does not affect
Theorems 14 and 15.

### E14. Formula (11): the lower limit of the first integral

(11) gives the variational integral over `H_x` as
`½ (Φ(x)(1 - x) + ∫₀^{-x} Φ(t) dt + ∫_{1-2y}^{x} Φ(t) dt)`. Substituting `u = -2t - x` on
`[0, (1 - x)/2]` gives `∫_{-1}^{-x} Φ`, not `∫₀^{-x} Φ`. Formula (12), which the paper derives from
(11), has the correct limit `-1`. A simulation confirms (12) to four decimals. Geupel (2011)
writes (11) with the limit `-1`. Lean: [`equation11`](PrincessMonster/Section4/Theorem15.lean#L51), with the limit `-1`.

### E15. Section 4: a Riemann-sum inequality in the wrong direction

"The integrals in (12) can be bounded from below by finite sums such as
`∫_{-1}^{0} Φ(t) dt ≥ ½ Φ(-½) + ½ Φ(0)`." Since `Φ` is nondecreasing, the right-hand side is an
upper Riemann sum, so the inequality fails in general, even for the uniform distribution
(`1/4 < 3/8`). The correct lower sum is `½ Φ(-1) + ½ Φ(-½)`, which Geupel (2011) uses. The matrix that follows uses the correct lower sums, so its entries and the
value `337/237` are right. Lean: the bounds inside [`theorem15`](PrincessMonster/Section4/Theorem15.lean#L419).

### E16. Theorem 16: the reduction to `S₁` and `S₂`

The proof:

- applies Proposition 5 to the hider strategy `h_Φ`, but Proposition 5 needs finitely many hider
  paths and `h_Φ` is a continuous mixture;
- reduces every searcher path to `S₁` or `S₂` ("we leave it to the reader to check this");
- reads the minimum over `y` off Figures 3 and 4, which follow the misprinted formula (15) over
  part of their range (E17).

The theorem holds. The formal proof keeps the paper's structure:

1. the first time `τ` at which the searcher gets `ε`-close to a sweeper (the paper's `y`);
2. before `τ`, only immobile loiterers are caught, at most as many as the swept interval contains;
3. at `τ`, the running loiterers are caught;
4. after `τ`, the searcher either reaches `-1` first (as `S₁` does) or `+1` first (as `S₂` and
   the sweeper do).

It replaces the reduction to two explicit paths by lower bounds valid for every continuation. The
result: every searcher path pays at least `(30 - 200ε)/22`, and the sweeper pays at most `15/11`.
Lean: [`theorem16`](PrincessMonster/Section5/Theorem16.lean#L2139).

### E17. Formula (15) and Figure 3

The two formulas (15) for `V(S₁, h_Φ)` and `V(S₂, h_Φ)` omit the capture-time factors in their
integrands. Written correctly, with `f` the density of `Φ` and `y ∈ (0, 1)`:

- `½ ∫₀^{2y-1} f` should be `½ ∫₀^{2y-1} (2y - 1 - t) f(t) dt` (both formulas);
- `∫_{1-2y}^{1-y} f` should be `∫_{1-2y}^{1-y} (t - 1 + 2y) f(t) dt` (both);
- in `V(S₁, h_Φ)`, `Φ(1 - 2y)` should be `∫₀^{1-2y} (1 - t) f(t) dt`.

Geupel (2011) and van Laere (2018) print (15) with the first two corrections, but keep
`Φ(1 - 2y)`.

The last correction holds because `S₁` turns at `y` and runs with the bunch of loiterers, so it
catches a loiterer at `x < 1 - 2y` at time `1 - x`, when the sweeper reaches it, not at time `1`.

For the uniform distribution the printed formula gives `V(S₁, h_Φ) → 1` as `y → 1`. The corrected
formula and a simulation give `3/4`, the value the paper itself uses. Figure 3 follows the printed
formula on `[0, ½]` and ends at the corrected value `0.75`; Figure 4 peaks at the printed formula's
`21/11` and ends at the corrected `15/11`. The conclusion of Theorem 16 is unaffected (E16). Lean: [`equation15`](PrincessMonster/Section5/Theorem16.lean#L2057),
corrected.

### E18. Typos

- Section 3 cites "Lemma 5" and "Lemma 1" for Propositions 5 and 1.
- Lemma 12's proof says "the probability of a hider starting out in that interval" for a
  searcher, and writes `ΔH - Δt` for `Δt - ΔH` (E12).
- The matrix of Section 4 lists its columns in the order `E, H₁, H₀, H_{½}`, while the text names
  the hider strategy on `{E, H₁, H_{½}, H₀}`.
- Section 5 writes `T` for `y` ("`S` starts in `1 - 2T - ε`", "`V(S₂, E) = 1 + 2T`", the axes of
  Figures 3 and 4).
- The caption of Figure 4 reads "`3/11 V(S₂, h_Φ) + 8/11 V(S₂, h_Φ)`" for
  `3/11 V(S₂, E) + 8/11 V(S₂, h_Φ)`.
- After (9), the text calls the fourth term "`-yΦ(1 - 2y)`"; in (9) it is `-(y/2)Φ(1 - 2y)` (the
  partial-integration constant times the probability `½` of the direction).

The published version corrects several slips of the preprint: Theorem 9's case (ii) reads "A has
been met" (the preprint has `-A`); strategy `B` "joins sweeper `-A`" (the preprint: "follows
sweeper `A`"); Lemma 12's proof refers to (5) and (6) in the right order; Section 5 says "In the
same way we obtain `V(S₂, h_Φ)`" (the preprint: `S₁`).

## 4. Missing hypotheses

No result of the paper needs a hypothesis that it leaves implicit. Two statements fail at a
boundary case instead (E11, E13); their corrected forms exclude that case. The cited minimax
theorem needs the minimizer's space to be nonempty (Section 2).

## 5. Redundant hypotheses

| Result | Hypothesis that is not needed | Lean |
| --- | --- | --- |
| Proposition 3 | smoothness of the hider path (E5) | [`proposition3`](PrincessMonster/Section2/Dominance.lean#L477) keeps it, unused (`_hsmooth`), to match the paper; [`proposition3_of_continuous`](PrincessMonster/Section2/Dominance.lean#L491) omits it |
| Proposition 7 | the searcher's speed limit | [`proposition7`](PrincessMonster/Section2/Noncrossing.lean#L90) holds for every continuous searcher path |
| Formula (11) | `y ≤ 1` | [`equation11`](PrincessMonster/Section4/Theorem15.lean#L51) omits it |

## 6. How the formalization reads the paper

Representation:

- Time `[0, ∞)` is `ℝ≥0`. A path is an element of `C(ℝ≥0, ℝ)` with values in `I = [-1, 1]`.
  The hider's strategies are [`hiderPaths`](Challenge.lean#L40), all such paths. The searcher's strategies are
  [`searcherPaths`](Challenge.lean#L45), the paths with `|S t - S t'| ≤ |t - t'|` (equation (2)). Both are subsets of
  `C(ℝ≥0, ℝ)`, so searcher paths are hider paths too, as in the paper.
- The topology is the compact-open topology of `C(ℝ≥0, ℝ)`, which is the topology of uniform
  convergence on compact sets. Mixed strategies are probability measures on the Borel
  σ-algebra.
- The capture time `captureTime S H` is the infimum of the meeting times, in `[0, ∞]`. It is `∞`
  when the paths never meet ("hiding at some end gives a payoff that is infinite"), and it is
  attained when they meet ([`exists_eq_captureTime`](PrincessMonster/CaptureTime.lean#L57)). Expected payoffs are lower Lebesgue
  integrals.
- [`upperValue`](Challenge.lean#L55) is `inf_μ sup_H`, over searcher mixed strategies and hider paths. [`lowerValue`](Challenge.lean#L61) is
  `sup_ν inf_S`, over hider mixed strategies and searcher paths. The value `V` is their common
  value (`value_exists`).
- "Dominated" means that the capture time is weakly better against every pure strategy of the
  opponent.

Readings of informal statements:

- "Ignoring `ε`" is read as a limit `ε → 0⁺`, as in (4), (12), (15) and the first part of
  Theorem 16, or as a bound valid for all small `ε`, as in Theorem 10.
- Searcher strategies are continued, after the time when the paper's description ends, by
  sweeping from end to end (a triangle wave, [`Real.triangleWave`](Basic/Analysis/TriangleWave.lean#L25)).
- Strategy `B` runs left and joins `-A` at time `½`, as the published version says.
- `s_Φ` in `σ` and in formula (9) contains both directions, each with probability `½`, as the
  factors `½` in (9) show ([`sPhi`](PrincessMonster/Section4/Runners.lean#L57)). `Φ` is the distribution function of an atomless probability
  measure on `[-1, 1]` (`NullSingletonClass`).
- Proposition 5's "the optimal response is concentrated on a finite number of strategies" is
  formalized two ways: every searcher path is dominated by the greedy path for some order
  ([`proposition5`](PrincessMonster/Section2/Greedy.lean#L359)); and the best response to a finite mixture is attained among the greedy paths
  ([`proposition5_response`](PrincessMonster/Section2/Greedy.lean#L378)).
- Proposition 7's "any finite mixed hider strategy" allows arbitrary weights (E7).
- Proposition 8's "nonintersecting symmetric hider strategy" is given by its finite support,
  closed under reflection, with distinct paths nonintersecting.
- The hider strategies of Sections 4 and 5 are the paper's paths. The loiterers of `h_Φ` start
  uniformly on `[ε, 1 - ε]`, wait until the sweeper is `ε` close, run ahead of it to `ε`, turn,
  and run to `+1`. The paths `H_x` turn `ε` in front of the sweeper.

Corrected statements (each documented in its docstring):

- Lemma 11 excludes the two starting points `H(y) ∓ y`, and holds for every hider path of speed
  at most `1` (E11).
- Formula (9), as an equality, requires the hider to meet `A` strictly first (E13).
- Formula (11) has the lower limit `-1` (E14).
- Formula (15) is corrected (E17).

## 7. Departures from the paper's proofs

Every other proof follows the paper's argument step by step. Each departure below is also recorded
in its docstring and in [`docs/route_differences.tsv`](docs/route_differences.tsv).

| Result | The paper's argument | The formalization's | Why it is necessary | E-item |
| --- | --- | --- | --- | --- |
| Proposition 1 | `S*` equals `S` up to the first end time `t₀`, then `1 + t₀ - t` | after `t₀`, `S*` sweeps from end to end | the paper's `S*` leaves `[-1, 1]` | E3 |
| Proposition 3 | `H*` built inductively, alternately following `H` and running at unit speed | the same path, by a closed formula | the induction can stall or not reach all times | E5 |
| Proposition 7, finite mixtures | none ("consequently") | quantile paths and a comparison of survival masses | the paper gives no argument, and the pairwise one does not cover unequal weights | E7 |
| Theorem 10 | Proposition 5, an informal enumeration of five responses, and Proposition 1 for a start at an end | Proposition 5, then a lower bound for every path from each possible start; the start at an end bounded from the speed limit | the enumeration is incomplete, and the statement of Proposition 1 does not give the claim made from it | E10 |
| Lemma 11 | "by Proposition 8 we may assume `H ≥ 0`" | both cases, `A` or `-A` met first, directly | Proposition 8 does not apply to a single path | E11 |
| Lemma 12 | first-order count of the catches in `[t, t + Δt]` | a layer-cake identity, then one integration by parts | the first-order argument is heuristic | E12 |
| Formula (9) and Theorem 14 | Lemmas 12 and 13 for smooth paths of speed at most `1` | Lemma 13 in integrated form for every path of speed at most `1` ([`s4_lemma13'`](PrincessMonster/Section4/Lemmas.lean#L694)) | Proposition 3's dominating path is only Lipschitz; Lemma 12 for it needs a change of variables for Lipschitz functions, which Mathlib lacks in usable form, and the layer-cake identity avoids it | E12 |
| Theorem 14 | "by Proposition 8, `H ≥ 0`" (in Lemma 11) | `σ` is reflection invariant, so the path may be taken to meet `A` first | Proposition 8 does not apply to a single path | E11 |
| Theorem 16 | Proposition 5, the reduction to `S₁, S₂`, and Figures 3 and 4 | the same structure, with lower bounds valid for every continuation | Proposition 5 needs finitely many hider paths; the reduction is not proved; the figures use a misprinted formula | E16 |

## 8. What each result depends on

Generated from [`scripts/Audit.lean`](scripts/Audit.lean). Every result uses only the axioms [`propext`](https://leanprover-community.github.io/mathlib4_docs/Init/Core.html#propext),
[`Classical.choice`](https://leanprover-community.github.io/mathlib4_docs/Init/Prelude.html#Classical.choice) and [`Quot.sound`](https://leanprover-community.github.io/mathlib4_docs/Init/Prelude.html#Quot.sound).

| Result | Lean | Results from prior work used |
| --- | --- | --- |
| The value exists (Section 1) | `value_exists` | [`External.AlpernGal.minimax`](External/AlpernGal/Minimax.lean#L539) |
| Proposition 1 | [`proposition1`](PrincessMonster/Section2/Dominance.lean#L245), [`proposition1_sweeping`](PrincessMonster/Section2/Dominance.lean#L257) | – |
| Proposition 2 | [`proposition2`](PrincessMonster/Section2/Dominance.lean#L264) | – |
| Proposition 3 | [`proposition3`](PrincessMonster/Section2/Dominance.lean#L477), [`proposition3_of_continuous`](PrincessMonster/Section2/Dominance.lean#L491) | – |
| Proposition 4 | [`proposition4`](PrincessMonster/Section2/Symmetric.lean#L96) | [`External.AlpernGal.minimax`](External/AlpernGal/Minimax.lean#L539), [`External.AlpernAsic.theorem3_minimizer`](External/AlpernAsic/Theorem3.lean#L49), [`External.AlpernAsic.theorem3_maximizer`](External/AlpernAsic/Theorem3.lean#L65) |
| Proposition 5 | [`proposition5`](PrincessMonster/Section2/Greedy.lean#L359), [`proposition5_response`](PrincessMonster/Section2/Greedy.lean#L378) | – |
| Proposition 7 | [`proposition7`](PrincessMonster/Section2/Noncrossing.lean#L90), [`proposition7_finite`](PrincessMonster/Section2/Noncrossing.lean#L414) | – |
| Proposition 8 | [`proposition8`](PrincessMonster/Section2/Noncrossing.lean#L454) | – |
| Theorem 9 | [`theorem9`](PrincessMonster/Section3/Theorem9.lean#L221) | – |
| Matrix (4) and its value | [`equation4`](PrincessMonster/Section3/Theorem10.lean#L348), [`matrix4_value`](PrincessMonster/Section3/Theorem10.lean#L418) | – |
| Theorem 10 | [`theorem10`](PrincessMonster/Section3/Theorem10.lean#L794) | – |
| Lemmas 11, 12, 13 | [`lemma11`](PrincessMonster/Section4/Lemmas.lean#L316), [`lemma12`](PrincessMonster/Section4/Lemmas.lean#L796), [`lemma13`](PrincessMonster/Section4/Lemmas.lean#L896), [`s4_lemma13'`](PrincessMonster/Section4/Lemmas.lean#L694) | – |
| Formulas (9), (10) | [`equation9`](PrincessMonster/Section4/Lemmas.lean#L1129), [`equation9_le`](PrincessMonster/Section4/Lemmas.lean#L1181), [`equation10`](PrincessMonster/Section4/Lemmas.lean#L1233) | – |
| Theorem 14 | [`theorem14`](PrincessMonster/Section4/Theorem14.lean#L347) | – |
| Formulas (11), (12) | [`equation11`](PrincessMonster/Section4/Theorem15.lean#L51), [`equation12`](PrincessMonster/Section4/Theorem15.lean#L292) | – |
| Theorem 15 | [`theorem15`](PrincessMonster/Section4/Theorem15.lean#L419) | – |
| Formula (15) | [`equation15`](PrincessMonster/Section5/Theorem16.lean#L2057) | – |
| Theorem 16 | [`theorem16`](PrincessMonster/Section5/Theorem16.lean#L2139) | – |
| Section 3 display | [`section3_bounds`](PrincessMonster/Main.lean#L31) | [`External.AlpernGal.minimax`](External/AlpernGal/Minimax.lean#L539) |
| Main result | `main`; [`PrincessMonster.Challenge.main`](Challenge.lean#L78) | [`External.AlpernGal.minimax`](External/AlpernGal/Minimax.lean#L539) |

The route check ([`scripts/route_check.py`](scripts/route_check.py)) compares, for every result, the results that its formal
proof uses with those that the paper's proof cites ([`docs/paper_routes.tsv`](docs/paper_routes.tsv)). Every difference is
recorded with its reason in [`docs/route_differences.tsv`](docs/route_differences.tsv). They are the departures above, the
paper's uncited use of the existence of the value, and readings such as "(10) evaluates the
right-hand side of (9)".

## 9. Not formalized

- The claim that the hider's strategies may be restricted to any dense set of paths (E4). The
  formalization does not need it.
- The passage after Proposition 7 on noncrossing, symmetric and nonintersecting `ε`-optimal hider
  strategies (E8). Proposition 8 takes such a strategy as its hypothesis.
- The remark after Theorem 10 that the value could in principle be computed iteratively.
- The Euler–Lagrange discussion after Lemma 13, the computer experiments mentioned before
  Theorem 15, and Figures 1–4. Their claims are formalized as Theorem 15, formula (15) and
  Theorem 16.
- The conjecture `V = 1.4` (Section 6).
- The introduction's account of other networks (the circle, networks with nodes).

## 10. The paper in the literature

Searched on 2026-11-14: web search for the title, the authors and the problem; the authors' LSE
and TU Delft repositories; Wikipedia and the sources it cites, through the Internet Archive; the
Lean community's resources. No newer version of the paper and no erratum were found. Two later
bachelor's theses had already corrected some of the slips this report lists (E1, E14, E15, E17).

### Before the paper

- Isaacs introduced princess and monster games in the last chapter of *Differential Games* (1965).
- On the circle, Zelikin (1972) and Alpern (1974) solved the game: both players use the "cohatu"
  strategy. It remains the only solved princess and monster game on a network.
- For an immobile hider, a Chinese postman tour traversed in a random direction is optimal on
  trees and on trees with Eulerian networks attached (Dagan and Gal; Alpern; Gal). On the interval
  this gives value `1`.
- Howard (1999) studied rendezvous on the interval with "sweepers", which the paper reuses.
- Alpern and Gal (1988) proved the mixed-strategy minimax theorem that gives the value its
  existence, and Alpern and Asic (1985) the invariance of optimal strategies.
- The paper showed that the interval game, believed trivial with value `3/2`, has
  `15/11 ≤ V ≤ 13/9`.

### Concurrent work

The same authors' preprint [LSE-CDAM-2006-18](http://www.cdam.lse.ac.uk/Reports/Files/cdam-2006-18.pdf)
(November 2006), published as *A numerical approach to the "Princess and Monster" game on an
interval* in *Advances in Dynamic Games and Their Applications* (Annals of the ISDG 10, Birkhäuser,
2009),
[doi:10.1007/978-0-8176-4834-3_9](https://doi.org/10.1007/978-0-8176-4834-3_9):

- It restricts both players to the strategy types of Sections 4 and 5 and discretizes. It
  estimates the value of the restricted game as `V_r ≈ 1.373`, which it suggests is `11/8`;
  Geupel's recomputation below gives `1.3727`.
- A Taylor-expansion approach gives `1.345`.
- It states that `V` is unknown, and that `V_r ≤ V`.

### Since the paper

- R. Fokkink, L. Geupel and K. Kikuta, *Open problems on search games*, in *Search Theory: A Game
  Theoretic Perspective* (Springer, 2013), pp. 75–81,
  [doi:10.1007/978-1-4614-6825-7_5](https://doi.org/10.1007/978-1-4614-6825-7_5). It lists open
  problems on Isaacs' princess and monster game. Its text was not accessible here.
- [Geupel (2011)](http://web.archive.org/web/20240912163228/https://hempelz.de/lenny/Leonhard%20Geupel%20-%20Bachelor's%20Thesis%20-%20The%20'Princess%20and%20Monster'%20Game%20on%20an%20Interval.pdf): L. Geupel, *The 'Princess and Monster' game on an interval*, bachelor's thesis, TU
  München, September 2011 (supervisor F. Bornemann), archived copy of the PDF that Wikipedia cites.
  It presents the paper's results and recomputes the restricted game of the 2009 chapter, finding
  `V_r ≈ 1.3727` (grid size 1024), which weakens the chapter's suggestion `11/8 = 1.375`. Along the
  way it calls `T` lower semicontinuous (E1), writes (11) with the limit `-1` (E14), uses the lower
  Riemann sums (E15), and prints (15) with two of the three corrections of E17.
- [van Laere (2018)](http://web.archive.org/web/20240708055105/https://studenttheses.uu.nl/bitstream/handle/20.500.12932/29143/The%20princess%20and%20monster%20game%20on%20the%20circle%20and%20the%20interval.pdf): S. M. F. van Laere, *The princess and monster game on the circle and the interval*,
  bachelor's thesis, Utrecht, January 2018 ([record](https://studenttheses.uu.nl/handle/20.500.12932/29143)).
  It presents the circle and the paper's results on the interval, with (15) corrected as in
  Geupel's thesis.
- No published work found improves the bounds `15/11 ≤ V ≤ 13/9` or settles the conjecture
  `V = 1.4`. Wikipedia's article ([Princess and monster game](https://en.wikipedia.org/wiki/Princess_and_monster_game))
  says the value on the interval has been estimated only approximately.

### Formalizations

None found, of this paper or of any search game, in Lean or in other systems.

## 11. What's next

Plans for follow-up papers are kept in `NEXT.md`, which is not published.

### Open directions

- **The value.** Closing the gap `15/11 ≤ V ≤ 13/9` (about `1.364` to `1.444`) is the paper's own
  challenge, together with its conjecture `V = 1.4`.
  - Theorem 15 shows that searcher strategies of the form `σ_Φ` cannot go below `337/237 ≈ 1.422`.
    A better upper bound therefore needs other searcher strategies.
  - The lower bound of Theorem 16 uses only the uniform `Φ`. Optimizing `Φ` and adding loiterers
    at the centre is what the restricted game of the 2009 chapter does. Its value `V_r ≈ 1.3727`
    (Geupel) caps every hider strategy built from loiterers and ends, so this route can gain at
    most about `0.009` over `15/11`, and higher lower bounds need other hider paths.
  - Within that cap, the lower-bound method of the formal proof of Theorem 16 (the exit time from
    the diamond `|p| < 1 - ε - t`, and survival bounds) would turn the restricted game's value into
    a proof.
- **Stronger Theorem 15.** The weights of the hider's response need not depend on `Φ`: the
  mixture `(37, 148, 24, 28)/237` on `(E, H₁, H₀, H_{½})` of the paper's 4×2 game gives
  `(337 + 8(Φ(½) - Φ(0)))/237 ≥ 337/237` for every `Φ` and `p`, in the limit `ε → 0`. At a fixed
  `ε` the guarantee depends on `Φ`, so the formal [`theorem15`](PrincessMonster/Section4/Theorem15.lean#L419) still chooses `ε` for each `Φ`; a
  bound uniform in `Φ` would make the response fully independent of `Φ`.
- **Optimal strategies.** The paper derives properties of optimal strategies (Propositions 1–8).
  The searcher has an optimal strategy, even a symmetric one (`value_exists`, [`proposition4`](PrincessMonster/Section2/Symmetric.lean#L96)). For
  the hider the paper, like the minimax theorem it uses, gives only `ε`-optimal strategies; it
  does not address whether an optimal one exists.

### Simpler proofs

- **Proposition 3 for every continuous path.** The closed formula of E5 gives Proposition 3 for
  every continuous hider path without smoothness, so the reduction to smooth paths (E4) is not
  needed. Checked in Lean.
- **Lemmas 12 and 13 at once.** The layer-cake identity of E12 gives Lemma 13's integrated form
  directly, without derivatives or integration by parts, for every path of speed at most `1`.
  Checked in Lean.
- **A shortcut for Theorem 14.** The survival argument behind Lemma 13' also gives Theorem 14's
  bound without Proposition 3 or the case `H ≥ 0`. Against `s_Φ` with uniform `Φ`, take any
  continuous hider path that meets the sweeper `A` first, at `y`. It is caught:
  - by time `t ≤ y` with probability at least `t/2`;
  - by time `2` with probability at least `(1 + y)/2`, since only the right runners starting
    below `1 - 2y` can miss it;
  - always by time `4`.

  Integrating the survival function gives `E_{s_Φ} T ≤ 3 - 2y + y²/4`, hence
  `E_σ T ≤ (26 - y + y²)/18 ≤ 13/9`. Checked on paper, and by the independent checker of this
  report on random paths, including paths of speed above `1`; not in Lean.

### The formalization

- **Mathlib and other libraries.** Several general facts were proved inside the paper's files and
  could move to [`Basic/`](Basic) and then to Mathlib:
  - the triangle wave and its properties ([`Basic/Analysis/TriangleWave.lean`](Basic/Analysis/TriangleWave.lean));
  - lower semicontinuity of `μ ↦ ∫ f dμ` at regular measures, and the regularization step of the
    minimax proof ([`External/AlpernGal/Minimax.lean`](External/AlpernGal/Minimax.lean));
  - layer-cake lower bounds for `[0, ∞]`-valued functions (in `Section5/Theorem16.lean` and
    `Section4/Lemmas.lean`).
- **The minimax theorem itself.** [`External.AlpernGal.minimax`](External/AlpernGal/Minimax.lean#L539), a mixed-strategy minimax theorem
  for lower semicontinuous payoffs on compact Hausdorff spaces, is general and would be a useful
  addition to Mathlib next to `Mathlib/Topology/Sion.lean`.
- **Exact equations.** The equations of Sections 4 and 5 are stated as limits `ε → 0⁺`.
  Quantitative versions with explicit `O(ε)` bounds, uniform in `Φ`, would let Theorem 15 fix `ε`.
