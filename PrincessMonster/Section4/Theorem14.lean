module

public import PrincessMonster.Section4.Lemmas
public import PrincessMonster.Section2.Dominance

/-!
# Section 4: Theorem 14, `V ≤ 13/9`

The searcher uses the sweepers `±A` with probability `p = 7/9` and `s_Φ`, with `Φ` uniform on
`[-1, 1]`, with probability `2/9`. Against a hider path that meets a sweeper first at time `y`,
the payoff is at most `13/9 - y/18 + y²/18`. The hider's best responses are to stay at an end,
which achieves `13/9` exactly, or to run from an end to the middle and back, which achieves
`13/9` in the limit (`y → 1`).
-/

@[expose] public section

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonster

/-! ### The sweepers -/

private lemma s4t_sweeperA_apply {t : ℝ≥0} (ht : (t : ℝ) ≤ 2) : sweeperA t = 1 - t := by
  simp only [sweeperA, pathOf_apply]
  exact Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith [t.coe_nonneg]⟩

private lemma s4t_negA_apply {t : ℝ≥0} (ht : (t : ℝ) ≤ 2) : (-sweeperA) t = t - 1 := by
  rw [ContinuousMap.neg_apply, s4t_sweeperA_apply ht]; ring

/-- Every path meets the sweeper `-A` by time `2`. -/
private lemma s4t_captureTime_negA_le_two {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    captureTime (-sweeperA) H ≤ 2 := by
  have h := captureTime_le_of_le_of_le (S := -sweeperA) (H := H) (t₁ := 0) (t₂ := 2) zero_le
    (by rw [s4t_negA_apply (by simp)]; simp only [NNReal.coe_zero]; linarith [(hH 0).1])
    (by rw [s4t_negA_apply (by simp)]; norm_num; exact (hH 2).2)
  simpa using h

/-- A path that meets `A` no later than `-A` meets it by time `1` (at time `1` the sweepers cross
at `0`). -/
private lemma s4t_captureTime_le_one {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) :
    captureTime sweeperA H ≤ 1 := by
  rcases le_total 0 (H 1) with h1 | h1
  · have h := captureTime_le_of_ge_of_ge (S := sweeperA) (H := H) (t₁ := 0) (t₂ := 1) zero_le
      (by rw [s4t_sweeperA_apply (by simp)]; simp only [NNReal.coe_zero]; linarith [(hH 0).2])
      (by rw [s4t_sweeperA_apply (by simp)]; simpa using h1)
    simpa using h
  · have h := captureTime_le_of_le_of_le (S := -sweeperA) (H := H) (t₁ := 0) (t₂ := 1) zero_le
      (by rw [s4t_negA_apply (by simp)]; simp only [NNReal.coe_zero]; linarith [(hH 0).1])
      (by rw [s4t_negA_apply (by simp)]; simpa using h1)
    exact hfirst.trans (by simpa using h)

/-- Before it meets the sweeper `A` (first, at time `y ≤ 1`), a path lies between `-A` and `A`. -/
private lemma s4t_between {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) (hy1 : (y : ℝ) ≤ 1) :
    ∀ t ∈ Set.Icc (0 : ℝ) y, t - 1 ≤ realPath H t ∧ realPath H t ≤ 1 - t := by
  intro t ht
  have hs : ((t.toNNReal : ℝ≥0) : ℝ) = t := Real.coe_toNNReal t ht.1
  have hsy : t.toNNReal ≤ y := by
    rw [← NNReal.coe_le_coe, hs]; exact ht.2
  have hrp : realPath H t = H t.toNNReal := rfl
  obtain ⟨t₀, h₀, hT⟩ := exists_eq_captureTime (hyA ▸ ENNReal.coe_ne_top)
  have ht₀ : t₀ = y := by rw [hyA] at hT; exact (ENNReal.coe_inj.mp hT).symm
  subst ht₀
  have hHy : H t₀ = 1 - t₀ := by rw [← h₀, s4t_sweeperA_apply (by linarith)]
  have hH0 := hH.1 0
  rw [hrp]
  constructor
  · by_contra hc
    rw [not_le] at hc
    rcases eq_or_lt_of_le hsy with heq | hlt
    · rw [heq, hHy] at hc; rw [heq] at hs; rw [← hs] at hc; linarith
    · have h := captureTime_le_of_le_of_le (S := -sweeperA) (H := H) (t₁ := 0) (t₂ := t.toNNReal)
        zero_le
        (by rw [s4t_negA_apply (by simp)]; simp only [NNReal.coe_zero]; linarith [hH0.1])
        (by rw [s4t_negA_apply (by rw [hs]; linarith [ht.2]), hs]; exact hc.le)
      have : captureTime (-sweeperA) H < captureTime sweeperA H :=
        h.trans_lt (by rw [hT]; exact_mod_cast hlt)
      exact absurd hfirst (not_le.mpr this)
  · by_contra hc
    rw [not_le] at hc
    rcases eq_or_lt_of_le hsy with heq | hlt
    · rw [heq, hHy] at hc; rw [heq] at hs; rw [← hs] at hc; linarith
    · have h := captureTime_le_of_ge_of_ge (S := sweeperA) (H := H) (t₁ := 0) (t₂ := t.toNNReal)
        zero_le
        (by rw [s4t_sweeperA_apply (by simp)]; simp only [NNReal.coe_zero]; linarith [hH0.2])
        (by rw [s4t_sweeperA_apply (by rw [hs]; linarith [ht.2]), hs]; exact hc.le)
      have : captureTime sweeperA H < captureTime sweeperA H :=
        h.trans_lt (by rw [hT]; exact_mod_cast hlt)
      exact lt_irrefl _ this

/-! ### Integrals over the searcher strategies -/

private lemma s4t_toSearcher_val {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    (toSearcher S : C(ℝ≥0, ℝ)) = S := by
  simp [toSearcher, hS]

private lemma s4t_lintegral_symDiracS {S₀ : C(ℝ≥0, ℝ)} (hS₀ : S₀ ∈ searcherPaths)
    (H : C(ℝ≥0, ℝ)) :
    ∫⁻ S, captureTime S H ∂(symDiracS S₀) =
      1 / 2 * (captureTime S₀ H + captureTime (-S₀) H) := by
  simp only [symDiracS, lintegral_smul_measure, lintegral_add_measure, lintegral_dirac,
    s4t_toSearcher_val hS₀, s4t_toSearcher_val (neg_mem_searcherPaths hS₀), smul_eq_mul]

private lemma s4t_lintegral_sigma (p : ℝ≥0∞) (μ : Measure ℝ) (H : C(ℝ≥0, ℝ)) :
    ∫⁻ S, captureTime S H ∂(sigma p μ) =
      p * (1 / 2 * (captureTime sweeperA H + captureTime (-sweeperA) H)) +
        (1 - p) * ∫⁻ S, captureTime S H ∂(sPhi μ) := by
  rw [sigma, lintegral_add_measure, lintegral_smul_measure, lintegral_smul_measure,
    s4t_lintegral_symDiracS sweeperA_mem, smul_eq_mul, smul_eq_mul]

private lemma s4t_continuous_runner : Continuous fun x : ℝ => runner x :=
  ContinuousMap.continuous_of_continuous_uncurry _ (by
    change Continuous fun p : ℝ × ℝ≥0 => Real.triangleWave (min (p.1 + p.2) (1 - p.2))
    fun_prop)

private lemma s4t_continuous_leftRunner : Continuous fun x : ℝ => leftRunner (-x) :=
  ContinuousMap.continuous_of_continuous_uncurry _ (by
    change Continuous fun p : ℝ × ℝ≥0 => Real.triangleWave (max (-p.1 - p.2) (p.2 - 1))
    fun_prop)

private lemma s4t_measurable_runnerS : Measurable fun x : ℝ => toSearcher (runner x) := by
  have : (fun x : ℝ => toSearcher (runner x)) = fun x => ⟨runner x, runner_mem x⟩ :=
    funext fun x => dite_eq_left (runner_mem x)
  rw [this]
  exact (s4t_continuous_runner.subtype_mk _).measurable

private lemma s4t_measurable_leftRunnerS :
    Measurable fun x : ℝ => toSearcher (leftRunner (-x)) := by
  have : (fun x : ℝ => toSearcher (leftRunner (-x))) =
      fun x => ⟨leftRunner (-x), leftRunner_mem (-x)⟩ :=
    funext fun x => dite_eq_left (leftRunner_mem (-x))
  rw [this]
  exact (s4t_continuous_leftRunner.subtype_mk _).measurable

/-! ### Reflection invariance of `σ` -/

/-- The reflection `S ↦ -S` as a measurable equivalence of the searcher's strategy space. -/
private def s4t_reflectEquiv : searcherPaths ≃ᵐ searcherPaths where
  toFun := reflectS
  invFun := reflectS
  left_inv S := Subtype.ext (neg_neg S.1)
  right_inv S := Subtype.ext (neg_neg S.1)
  measurable_toFun := measurable_reflectS
  measurable_invFun := measurable_reflectS

private lemma s4t_reflectS_toSearcher {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    reflectS (toSearcher S) = toSearcher (-S) := by
  apply Subtype.ext
  simp only [reflectS, s4t_toSearcher_val hS, s4t_toSearcher_val (neg_mem_searcherPaths hS)]

private lemma s4t_map_symDiracS : (symDiracS sweeperA).map reflectS = symDiracS sweeperA := by
  have h1 := s4t_reflectS_toSearcher sweeperA_mem
  have h2 := s4t_reflectS_toSearcher (neg_mem_searcherPaths sweeperA_mem)
  rw [neg_neg] at h2
  simp only [symDiracS]
  rw [Measure.map_smul _ measurable_reflectS.aemeasurable,
    Measure.map_add _ _ measurable_reflectS, Measure.map_dirac, Measure.map_dirac, h1, h2,
    add_comm]

private lemma s4t_map_sPhi (μ : Measure ℝ) : (sPhi μ).map reflectS = sPhi μ := by
  have hRL : reflectS ∘ (fun x : ℝ => toSearcher (runner x)) =
      fun x => toSearcher (leftRunner (-x)) := by
    funext x
    simp only [Function.comp]
    rw [s4t_reflectS_toSearcher (runner_mem x), leftRunner_eq_neg_runner, neg_neg]
  have hLR : reflectS ∘ (fun x : ℝ => toSearcher (leftRunner (-x))) =
      fun x => toSearcher (runner x) := by
    funext x
    simp only [Function.comp]
    rw [s4t_reflectS_toSearcher (leftRunner_mem _), leftRunner_eq_neg_runner, neg_neg, neg_neg]
  simp only [sPhi]
  rw [Measure.map_smul _ measurable_reflectS.aemeasurable,
    Measure.map_add _ _ measurable_reflectS,
    Measure.map_map measurable_reflectS s4t_measurable_runnerS,
    Measure.map_map measurable_reflectS s4t_measurable_leftRunnerS, hRL, hLR, add_comm]

private lemma s4t_map_sigma (p : ℝ≥0∞) (μ : Measure ℝ) : (sigma p μ).map reflectS = sigma p μ := by
  simp only [sigma]
  rw [Measure.map_add _ _ measurable_reflectS, Measure.map_smul _ measurable_reflectS.aemeasurable,
    Measure.map_smul _ measurable_reflectS.aemeasurable, s4t_map_symDiracS, s4t_map_sPhi]

/-- `σ` is invariant under the reflection, and `T(-S, -H) = T(S, H)`: reflecting the hider path
does not change its payoff. -/
private lemma s4t_lintegral_sigma_neg (p : ℝ≥0∞) (μ : Measure ℝ) (H : C(ℝ≥0, ℝ)) :
    ∫⁻ S, captureTime S (-H) ∂(sigma p μ) = ∫⁻ S, captureTime S H ∂(sigma p μ) := by
  conv_lhs => rw [← s4t_map_sigma p μ]
  rw [show (reflectS : searcherPaths → searcherPaths) = ⇑s4t_reflectEquiv from rfl,
    lintegral_map_equiv]
  congr 1
  funext S
  exact captureTime_neg

/-! ### Uniform distribution -/

private lemma s4t_uniformI_prob : IsProbabilityMeasure uniformI := by
  constructor
  simp only [uniformI, Measure.smul_apply, Measure.restrict_apply MeasurableSet.univ,
    Set.univ_inter, Real.volume_Icc, smul_eq_mul]
  norm_num
  exact ENNReal.inv_mul_cancel two_ne_zero ENNReal.ofNat_ne_top

private lemma s4t_uniformI_null : NullSingletonClass uniformI := by
  constructor
  intro x
  simp [uniformI]

private lemma s4t_uniformI_compl : uniformI Iᶜ = 0 := by
  simp only [uniformI, Measure.smul_apply, smul_eq_mul]
  rw [Measure.restrict_apply' measurableSet_Icc, Set.compl_inter_self, measure_empty, mul_zero]

private lemma s4t_isProb_sigma : IsProbabilityMeasure (sigma (7 / 9) uniformI) := by
  have := s4t_uniformI_prob
  constructor
  simp only [sigma, sPhi, symDiracS, Measure.add_apply, Measure.smul_apply, smul_eq_mul,
    Measure.map_apply s4t_measurable_runnerS MeasurableSet.univ,
    Measure.map_apply s4t_measurable_leftRunnerS MeasurableSet.univ, Set.preimage_univ,
    measure_univ, Measure.dirac_apply_of_mem (Set.mem_univ _)]
  rw [one_add_one_eq_two, ENNReal.div_mul_cancel two_ne_zero ENNReal.ofNat_ne_top, mul_one,
    mul_one, add_tsub_cancel_of_le (ENNReal.div_le_of_le_mul (by norm_num))]

private lemma s4t_ofReal_frac (a b : ℕ) [a.AtLeastTwo] [b.AtLeastTwo] :
    (OfNat.ofNat a / OfNat.ofNat b : ℝ≥0∞) = ENNReal.ofReal (OfNat.ofNat a / OfNat.ofNat b) := by
  rw [ENNReal.ofReal_div_of_pos Nat.ofNat_pos]
  simp

/-! ### The bound -/

/-- Steps 3–5 of the proof of Theorem 14: against a path of speed at most `1` that meets `A`
first, at time `y ≤ 1`, the payoff of `σ` is at most `(26 - y + y²)/18 ≤ 13/9`. -/
private lemma s4t_bound_of_first {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) :
    ∫⁻ S, captureTime S H ∂(sigma (7 / 9) uniformI) ≤ 13 / 9 := by
  have := s4t_uniformI_prob
  have := s4t_uniformI_null
  have hHh : H ∈ hiderPaths := searcherPaths_subset_hiderPaths hH
  have h1 := s4t_captureTime_le_one hHh hfirst
  have hne : captureTime sweeperA H ≠ ⊤ := ne_top_of_le_ne_top ENNReal.one_ne_top h1
  set y : ℝ≥0 := (captureTime sweeperA H).toNNReal with hy_def
  have hyA : captureTime sweeperA H = y := (ENNReal.coe_toNNReal hne).symm
  have hy1 : (y : ℝ) ≤ 1 := by
    have : (y : ℝ≥0∞) ≤ 1 := hyA ▸ h1
    exact_mod_cast this
  have hy0 : (0 : ℝ) ≤ y := y.coe_nonneg
  have hs := equation9_le uniformI s4t_uniformI_compl hH hyA hfirst
  rw [equation10 (hH.1 0) hy0 hy1 (s4t_between hH hyA hfirst hy1)] at hs
  have hx1 : H 0 ≤ 1 := (hH.1 0).2
  have hx0 : -1 ≤ H 0 := (hH.1 0).1
  have h2 := s4t_captureTime_negA_le_two hHh
  rw [s4t_lintegral_sigma, hyA]
  calc 7 / 9 * (1 / 2 * ((y : ℝ≥0∞) + captureTime (-sweeperA) H)) +
        (1 - 7 / 9) * ∫⁻ S, captureTime S H ∂(sPhi uniformI)
      ≤ ENNReal.ofReal (7 / 9) *
          (ENNReal.ofReal (1 / 2) * (ENNReal.ofReal y + ENNReal.ofReal 2)) +
        ENNReal.ofReal (2 / 9) *
          ENNReal.ofReal ((10 + 2 * H 0 - (7 + H 0) * y + y ^ 2) / 4) := by
        rw [ENNReal.ofReal_coe_nnreal, ← s4t_ofReal_frac, ENNReal.ofReal_div_of_pos two_pos,
          ← s4t_ofReal_frac, ENNReal.ofReal_one, ENNReal.ofReal_ofNat,
          show (1 - 7 / 9 : ℝ≥0∞) = 2 / 9 from ?_]
        · gcongr
        · rw [s4t_ofReal_frac, s4t_ofReal_frac, ← ENNReal.ofReal_one,
            ← ENNReal.ofReal_sub _ (by norm_num)]
          norm_num
    _ = ENNReal.ofReal (7 / 9 * (1 / 2 * (y + 2)) +
          2 / 9 * ((10 + 2 * H 0 - (7 + H 0) * y + y ^ 2) / 4)) := by
        rw [ENNReal.ofReal_add (by positivity) (by nlinarith), ENNReal.ofReal_mul (by norm_num),
          ENNReal.ofReal_mul (by norm_num), ENNReal.ofReal_mul (by norm_num),
          ENNReal.ofReal_add hy0 (by norm_num)]
    _ ≤ ENNReal.ofReal (13 / 9) := by
        apply ENNReal.ofReal_le_ofReal
        -- step 3: `x ≤ 1` and `2 - y ≥ 0`
        have h3 : (10 + 2 * H 0 - (7 + H 0) * (y : ℝ) + (y : ℝ) ^ 2) / 4 ≤
            (12 - 8 * (y : ℝ) + (y : ℝ) ^ 2) / 4 := by
          nlinarith [mul_le_mul_of_nonneg_right hx1 (by linarith : (0 : ℝ) ≤ 2 - y)]
        -- step 5: `(26 - y + y²)/18 ≤ 13/9` for `0 ≤ y ≤ 1`
        calc 7 / 9 * (1 / 2 * ((y : ℝ) + 2)) +
              2 / 9 * ((10 + 2 * H 0 - (7 + H 0) * (y : ℝ) + (y : ℝ) ^ 2) / 4)
            ≤ 7 / 9 * (1 / 2 * ((y : ℝ) + 2)) + 2 / 9 * ((12 - 8 * (y : ℝ) + (y : ℝ) ^ 2) / 4) := by
              linarith
          _ = (26 - (y : ℝ) + (y : ℝ) ^ 2) / 18 := by ring
          _ ≤ 13 / 9 := by nlinarith
    _ = 13 / 9 := (s4t_ofReal_frac 13 9).symm

/-! ### The end strategy `E` -/

private lemma s4t_captureTime_A_E : captureTime sweeperA hiderE = 0 :=
  le_antisymm (by
    have h := captureTime_le (S := sweeperA) (H := hiderE) (t := 0)
      (by rw [s4t_sweeperA_apply (by simp)]; simp [hiderE])
    simpa using h) bot_le

private lemma s4t_captureTime_negA_E : captureTime (-sweeperA) hiderE = 2 := by
  refine le_antisymm
    (s4t_captureTime_negA_le_two (searcherPaths_subset_hiderPaths hiderE_mem)) ?_
  have h := le_captureTime_of_ne (S := -sweeperA) (H := hiderE) (c := 2) fun t ht => by
    have ht' : (t : ℝ) < 2 := by exact_mod_cast ht
    rw [s4t_negA_apply ht'.le]
    simp only [hiderE, ContinuousMap.const_apply]
    linarith
  simpa using h

/-- Step 6 of the proof of Theorem 14: the hider who stays at the end `+1` obtains `13/9`. -/
private lemma s4t_payoff_E : ∫⁻ S, captureTime S hiderE ∂(sigma (7 / 9) uniformI) = 13 / 9 := by
  have := s4t_uniformI_prob
  have := s4t_uniformI_null
  have hE0 : hiderE 0 = 1 := rfl
  have hyA : captureTime sweeperA hiderE = ((0 : ℝ≥0) : ℝ≥0∞) := by
    rw [s4t_captureTime_A_E, ENNReal.coe_zero]
  have hs := equation9 uniformI s4t_uniformI_compl hiderE_mem hyA
    (by rw [s4t_captureTime_A_E, s4t_captureTime_negA_E]; norm_num)
    (fun t _ => by
      simp only [hiderE, ContinuousMap.const_apply, NNReal.coe_zero, sub_zero]
      exact (min_eq_left (by linarith [t.coe_nonneg])).symm)
  rw [NNReal.coe_zero, equation10 (by rw [hE0]; norm_num) le_rfl (by norm_num)
    (fun t ht => by
      have : t = 0 := le_antisymm (by simpa using ht.2) ht.1
      subst this
      simp [realPath, hiderE])] at hs
  rw [s4t_lintegral_sigma, s4t_captureTime_A_E, s4t_captureTime_negA_E, hs, hE0]
  rw [show (1 - 7 / 9 : ℝ≥0∞) = ENNReal.ofReal (2 / 9) from by
      rw [s4t_ofReal_frac, ← ENNReal.ofReal_one, ← ENNReal.ofReal_sub _ (by norm_num)]
      norm_num,
    s4t_ofReal_frac, s4t_ofReal_frac, zero_add,
    ENNReal.div_mul_cancel two_ne_zero ENNReal.ofNat_ne_top, mul_one,
    ← ENNReal.ofReal_mul (by norm_num), ← ENNReal.ofReal_add (by norm_num) (by norm_num)]
  norm_num

/-- **Theorem 14** (`thm:14`). If the searcher uses the mixed strategy `σ` (sweepers with
probability `7/9`, `s_Φ` with uniform `Φ` with probability `2/9`), the optimal response of the
hider gives the value `13/9`. In particular `V ≤ 13/9`.

The proof follows the paper's route ((9), (10), `p = 7/9`), with these departures, each needed
because a step of the paper does not apply as stated (REPORT.md, Section 7): the hider path is
replaced by one of speed at most `1` through `proposition3_of_continuous`, since the paper's
smooth paths are not what Proposition 3 produces; (9) is used as a bound valid for every
continuation after `y` (`equation9_le`), proved through Lemma 13 in integrated form
(`s4_lemma13'`) rather than Lemmas 12 and 13 for smooth paths; and the reflection replaces the
paper's "by Proposition 8, `H ≥ 0`". (1) By Proposition 3 (`prop:3`, in the form
`proposition3_of_continuous`) every hider path `H` is dominated by a path `H'` of speed at most
`1`. (2) `σ` is invariant under the reflection and `T(-S, -H') = T(S, H')`, so we may replace
`H'` by `-H'` and assume that `H'` meets `A` first (the paper takes this for granted through the
proof of Lemma 11, "by Proposition 8 we may assume that `H ≥ 0`"; Proposition 8 is about mixed
strategies and does not apply to a single path, while the reflection does what is needed).
(3) Then `y = T(A, H') ≤ 1`, `H'` lies between `-A` and `A` before `y`, and (9) as a bound
(`equation9_le`) with (10) (`equation10`) give
`V(s_Φ, H') ≤ (10 + 2x - (7 + x)y + y²)/4 ≤ (12 - 8y + y²)/4`. (4) Against `±A` the payoff is
`(y + T(-A, H'))/2 ≤ (y + 2)/2`. (5) In total `(26 - y + y²)/18 ≤ 13/9`. (6) The end strategy `E`
obtains `13/9`: `T(A, E) = 0`, `T(-A, E) = 2`, and `V(s_Φ, E) = 3` by (9) and (10) at `x = 1`,
`y = 0` (`equation9`, `equation10`), as in the paper. -/
theorem theorem14 :
    ⨆ H : hiderPaths, ∫⁻ S, captureTime S H ∂(sigma (7 / 9) uniformI) = 13 / 9 ∧
      upperValue ≤ 13 / 9 := by
  have hsup : ⨆ H : hiderPaths, ∫⁻ S, captureTime S H ∂(sigma (7 / 9) uniformI) = 13 / 9 := by
    refine le_antisymm (iSup_le fun H => ?_) ?_
    · obtain ⟨H', hH', hdom⟩ := proposition3_of_continuous H.2
      refine (lintegral_mono fun S : searcherPaths => hdom S.1 S.2).trans ?_
      rcases le_or_gt (captureTime sweeperA H') (captureTime (-sweeperA) H') with h | h
      · exact s4t_bound_of_first hH' h
      · rw [← s4t_lintegral_sigma_neg]
        refine s4t_bound_of_first (neg_mem_searcherPaths hH') ?_
        rw [captureTime_neg, show captureTime sweeperA (-H') = captureTime (-sweeperA) H' by
          rw [← captureTime_neg (S := -sweeperA), neg_neg]]
        exact h.le
    · exact le_iSup_of_le (⟨hiderE, searcherPaths_subset_hiderPaths hiderE_mem⟩ : hiderPaths)
        s4t_payoff_E.ge
  refine ⟨hsup, ?_⟩
  have := s4t_isProb_sigma
  exact (iInf_le _ (⟨sigma (7 / 9) uniformI, this⟩ : ProbabilityMeasure searcherPaths)).trans
    hsup.le

end PrincessMonster
