module

public import PrincessMonster.Section3.Strategies

/-!
# Section 3: Theorem 9, `V ≤ 47/32`

The searcher uses `±A` with probability `7/16` each and `±B` with probability `1/16` each.
Against every hider path the expected capture time is at most `47/32`.

Also the bounds of the "trivial" strategies discussed at the start of Section 3: one of the
sweepers `±A` meets every hider path by time `1`, so the equiprobable sweepers guarantee `3/2`;
the hider at a random end guarantees `1`.
-/

@[expose] public section

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonster

/-! ### The paths `A` and `B` at the times used in the proofs -/

private lemma s3a_A_zero : sweeperA 0 = 1 := by
  simp only [sweeperA, pathOf_apply]; rw [Real.triangleWave_of_mem_Icc] <;> norm_num

private lemma s3a_A_half : sweeperA (1 / 2) = 1 / 2 := by
  simp only [sweeperA, pathOf_apply]; rw [Real.triangleWave_of_mem_Icc] <;> norm_num

private lemma s3a_A_one : sweeperA 1 = 0 := by
  simp only [sweeperA, pathOf_apply]; rw [Real.triangleWave_of_mem_Icc] <;> norm_num

private lemma s3a_A_two : sweeperA 2 = -1 := by
  simp only [sweeperA, pathOf_apply]; rw [Real.triangleWave_of_mem_Icc] <;> norm_num

private lemma s3a_B_zero : stratB 0 = 0 := by
  simp only [stratB, pathOf_apply]; rw [Real.triangleWave_of_mem_Icc] <;> norm_num

private lemma s3a_B_half : stratB (1 / 2) = -1 / 2 := by
  simp only [stratB, pathOf_apply]; rw [Real.triangleWave_of_mem_Icc] <;> norm_num

private lemma s3a_B_two : stratB 2 = 1 := by
  simp only [stratB, pathOf_apply]; rw [Real.triangleWave_of_mem_Icc] <;> norm_num

private lemma s3a_B_four : stratB 4 = -1 := by
  simp only [stratB, pathOf_apply]; rw [Real.triangleWave_of_mem_Icc_one_three] <;> norm_num

/-! ### Mixtures of two Dirac masses -/

private lemma s3a_toSearcher_coe {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    ((toSearcher S : searcherPaths) : C(ℝ≥0, ℝ)) = S := by
  simp [toSearcher, hS]

private lemma s3a_toHider_coe {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    ((toHider H : hiderPaths) : C(ℝ≥0, ℝ)) = H := by
  simp [toHider, hH]

private lemma s3a_lintegral_symDiracS (S : C(ℝ≥0, ℝ)) (f : searcherPaths → ℝ≥0∞) :
    ∫⁻ x, f x ∂symDiracS S = 1 / 2 * (f (toSearcher S) + f (toSearcher (-S))) := by
  simp only [symDiracS, lintegral_smul_measure, lintegral_add_measure, lintegral_dirac,
    smul_eq_mul]

private lemma s3a_lintegral_symDiracH (H : C(ℝ≥0, ℝ)) (f : hiderPaths → ℝ≥0∞) :
    ∫⁻ x, f x ∂symDiracH H = 1 / 2 * (f (toHider H) + f (toHider (-H))) := by
  simp only [symDiracH, lintegral_smul_measure, lintegral_add_measure, lintegral_dirac,
    smul_eq_mul]

private lemma s3a_half_mul_two : (1 / 2 : ℝ≥0∞) * 2 = 1 := by
  rw [one_div, ENNReal.inv_mul_cancel two_ne_zero ENNReal.ofNat_ne_top]

private lemma s3a_isProbabilityMeasure_symDiracS (S : C(ℝ≥0, ℝ)) :
    IsProbabilityMeasure (symDiracS S) := by
  constructor
  simp only [symDiracS, Measure.smul_apply, Measure.add_apply, measure_univ, smul_eq_mul,
    one_add_one_eq_two, s3a_half_mul_two]

private lemma s3a_isProbabilityMeasure_symDiracH (H : C(ℝ≥0, ℝ)) :
    IsProbabilityMeasure (symDiracH H) := by
  constructor
  simp only [symDiracH, Measure.smul_apply, Measure.add_apply, measure_univ, smul_eq_mul,
    one_add_one_eq_two, s3a_half_mul_two]

/-! ### Capture times of the sweepers -/

/-- Against any hider path, one of the sweepers `A`, `-A` has met it by time `1`. -/
theorem min_captureTime_sweepers_le_one {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    min (captureTime sweeperA H) (captureTime (-sweeperA) H) ≤ 1 := by
  -- `A(1) = -A(1) = 0`: the sweeper on the other side of `H(1)` from its start has met `H`
  rcases le_total 0 (H 1) with h1 | h1
  · refine min_le_of_left_le ?_
    have := captureTime_le_of_ge_of_ge (S := sweeperA) (H := H) (t₁ := 0) (t₂ := 1) zero_le_one
      (by rw [s3a_A_zero]; exact (hH 0).2) (by rw [s3a_A_one]; exact h1)
    simpa using this
  · refine min_le_of_right_le ?_
    have := captureTime_le_of_le_of_le (S := -sweeperA) (H := H) (t₁ := 0) (t₂ := 1) zero_le_one
      (by rw [ContinuousMap.neg_apply, s3a_A_zero]; exact (hH 0).1)
      (by rw [ContinuousMap.neg_apply, s3a_A_one, neg_zero]; exact h1)
    simpa using this

/-- The sweeper `A` meets every hider path by time `2`. -/
private lemma s3a_A_le_two {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    captureTime sweeperA H ≤ ((2 : ℝ≥0) : ℝ≥0∞) :=
  captureTime_le_of_ge_of_ge (t₁ := 0) (by norm_num) (by rw [s3a_A_zero]; exact (hH 0).2)
    (by rw [s3a_A_two]; exact (hH 2).1)

/-- The sweeper `-A` meets every hider path by time `2`. -/
private lemma s3a_negA_le_two {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    captureTime (-sweeperA) H ≤ ((2 : ℝ≥0) : ℝ≥0∞) :=
  captureTime_le_of_le_of_le (t₁ := 0) (by norm_num)
    (by rw [ContinuousMap.neg_apply, s3a_A_zero]; exact (hH 0).1)
    (by rw [ContinuousMap.neg_apply, s3a_A_two, neg_neg]; exact (hH 2).2)

/-- `B` follows `-A` on `[1/2, 2]`: it meets every hider path with `H(1/2) ≥ -1/2` by time `2`. -/
private lemma s3a_B_le_two {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (h : -1 / 2 ≤ H (1 / 2)) :
    captureTime stratB H ≤ ((2 : ℝ≥0) : ℝ≥0∞) :=
  captureTime_le_of_le_of_le (t₁ := 1 / 2) (by rw [← NNReal.coe_le_coe]; norm_num)
    (by rw [s3a_B_half]; exact h)
    (by rw [s3a_B_two]; exact (hH 2).2)

/-- `-B` follows `A` on `[1/2, 2]`: it meets every hider path with `H(1/2) ≤ 1/2` by time `2`. -/
private lemma s3a_negB_le_two {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (h : H (1 / 2) ≤ 1 / 2) :
    captureTime (-stratB) H ≤ ((2 : ℝ≥0) : ℝ≥0∞) :=
  captureTime_le_of_ge_of_ge (t₁ := 1 / 2) (by rw [← NNReal.coe_le_coe]; norm_num)
    (by rw [ContinuousMap.neg_apply, s3a_B_half]; linarith)
    (by rw [ContinuousMap.neg_apply, s3a_B_two]; exact (hH 2).1)

/-- `-B` sweeps from `-1` to `1` on `[2, 4]`: it meets every hider path by time `4`. -/
private lemma s3a_negB_le_four {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    captureTime (-stratB) H ≤ ((4 : ℝ≥0) : ℝ≥0∞) :=
  captureTime_le_of_le_of_le (t₁ := 2) (by norm_num)
    (by rw [ContinuousMap.neg_apply, s3a_B_two]; exact (hH 2).1)
    (by rw [ContinuousMap.neg_apply, s3a_B_four, neg_neg]; exact (hH 4).2)

/-- If `|H(1/2)| ≤ 1/2`, one of `B`, `-B` has met `H` by time `1/2` (they run from `0` to
`∓1/2` on `[0, 1/2]`). -/
private lemma s3a_min_B_le_half {H : C(ℝ≥0, ℝ)} (h1 : -1 / 2 ≤ H (1 / 2))
    (h2 : H (1 / 2) ≤ 1 / 2) :
    min (captureTime stratB H) (captureTime (-stratB) H) ≤ ((1 / 2 : ℝ≥0) : ℝ≥0∞) := by
  rcases le_total (H 0) 0 with h0 | h0
  · exact min_le_of_left_le <| captureTime_le_of_ge_of_ge (t₁ := 0) (by norm_num)
      (by rw [s3a_B_zero]; exact h0) (by rw [s3a_B_half]; exact h1)
  · exact min_le_of_right_le <| captureTime_le_of_le_of_le (t₁ := 0) (by norm_num)
      (by rw [ContinuousMap.neg_apply, s3a_B_zero, neg_zero]; exact h0)
      (by rw [ContinuousMap.neg_apply, s3a_B_half]; linarith)

/-- If `H(1/2) ≥ 1/2`, the sweeper `A` (at `1/2` at time `1/2`) has met `H` by time `1/2`. -/
private lemma s3a_A_le_half {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (h : 1 / 2 ≤ H (1 / 2)) :
    captureTime sweeperA H ≤ ((1 / 2 : ℝ≥0) : ℝ≥0∞) :=
  captureTime_le_of_ge_of_ge (t₁ := 0) (by norm_num) (by rw [s3a_A_zero]; exact (hH 0).2)
    (by rw [s3a_A_half]; exact h)

/-! ### Theorem 9 -/

private lemma s3a_add_le_of_min_le {x y a b : ℝ≥0∞} (hmin : min x y ≤ a) (hx : x ≤ b)
    (hy : y ≤ b) : x + y ≤ a + b := by
  rw [← min_add_max]
  exact add_le_add hmin (max_le hx hy)

/-- Case (i) of Theorem 9, `|H(1/2)| ≤ 1/2`: one of `±B` has met `H` by `1/2`, one of `±A` by `1`,
and all four by `2`. -/
private lemma s3a_case_i {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (h1 : -1 / 2 ≤ H (1 / 2))
    (h2 : H (1 / 2) ≤ 1 / 2) :
    captureTime sweeperA H + captureTime (-sweeperA) H ≤ ((1 + 2 : ℝ≥0) : ℝ≥0∞) ∧
      captureTime stratB H + captureTime (-stratB) H ≤ ((1 / 2 + 2 : ℝ≥0) : ℝ≥0∞) := by
  rw [ENNReal.coe_add, ENNReal.coe_add]
  exact ⟨s3a_add_le_of_min_le (by simpa using min_captureTime_sweepers_le_one hH)
      (s3a_A_le_two hH) (s3a_negA_le_two hH),
    s3a_add_le_of_min_le (s3a_min_B_le_half h1 h2) (s3a_B_le_two hH h1) (s3a_negB_le_two hH h2)⟩

/-- Case (ii) of Theorem 9, `H(1/2) ≥ 1/2`: `A` has met `H` by `1/2`, `-A` and `B` by `2`, and
`-B` by `4`. -/
private lemma s3a_case_ii {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (h : 1 / 2 ≤ H (1 / 2)) :
    captureTime sweeperA H + captureTime (-sweeperA) H ≤ ((1 / 2 + 2 : ℝ≥0) : ℝ≥0∞) ∧
      captureTime stratB H + captureTime (-stratB) H ≤ ((2 + 4 : ℝ≥0) : ℝ≥0∞) := by
  rw [ENNReal.coe_add, ENNReal.coe_add]
  exact ⟨add_le_add (s3a_A_le_half hH h) (s3a_negA_le_two hH),
    add_le_add (s3a_B_le_two hH (by linarith)) (s3a_negB_le_four hH)⟩

/-- The expected capture time of `s`, `(7/16)(T(A,H) + T(-A,H)) + (1/16)(T(B,H) + T(-B,H))`, from
bounds `a` on `T(A,H) + T(-A,H)` and `b` on `T(B,H) + T(-B,H)`. -/
private lemma s3a_expectation_le {x y : ℝ≥0∞} {a b : ℝ≥0} (hx : x ≤ a) (hy : y ≤ b)
    (h : 7 / 16 * a + 1 / 16 * b ≤ (47 / 32 : ℝ≥0)) :
    7 / 8 * (1 / 2 * x) + 1 / 8 * (1 / 2 * y) ≤ 47 / 32 := by
  calc 7 / 8 * (1 / 2 * x) + 1 / 8 * (1 / 2 * y)
        ≤ 7 / 8 * (1 / 2 * (a : ℝ≥0∞)) + 1 / 8 * (1 / 2 * (b : ℝ≥0∞)) := by gcongr
    _ = ((7 / 8 * (1 / 2 * a) + 1 / 8 * (1 / 2 * b) : ℝ≥0) : ℝ≥0∞) := by
        simp [ENNReal.coe_div]
    _ ≤ ((47 / 32 : ℝ≥0) : ℝ≥0∞) := ENNReal.coe_le_coe.mpr (by ring_nf; ring_nf at h; exact h)
    _ = 47 / 32 := by simp [ENNReal.coe_div]

/-- The searcher mixed strategy `s` of Theorem 9: `±A` with probability `7/16` each, `±B` with
probability `1/16` each. -/
noncomputable def strategy9 : Measure searcherPaths :=
  (7 / 8 : ℝ≥0∞) • symDiracS sweeperA + (1 / 8 : ℝ≥0∞) • symDiracS stratB

instance : IsProbabilityMeasure strategy9 := by
  constructor
  have hA := (s3a_isProbabilityMeasure_symDiracS sweeperA).measure_univ
  have hB := (s3a_isProbabilityMeasure_symDiracS stratB).measure_univ
  simp only [strategy9, Measure.add_apply, Measure.smul_apply, smul_eq_mul, hA, hB, mul_one]
  rw [ENNReal.div_add_div_same, show (7 + 1 : ℝ≥0∞) = 8 by norm_num]
  exact ENNReal.div_self (by norm_num) (by norm_num)

private lemma s3a_lintegral_strategy9 (H : C(ℝ≥0, ℝ)) :
    ∫⁻ S, captureTime S H ∂strategy9 =
      7 / 8 * (1 / 2 * (captureTime sweeperA H + captureTime (-sweeperA) H)) +
        1 / 8 * (1 / 2 * (captureTime stratB H + captureTime (-stratB) H)) := by
  rw [strategy9, lintegral_add_measure, lintegral_smul_measure, lintegral_smul_measure,
    s3a_lintegral_symDiracS, s3a_lintegral_symDiracS, s3a_toSearcher_coe sweeperA_mem,
    s3a_toSearcher_coe (neg_mem_searcherPaths sweeperA_mem), s3a_toSearcher_coe stratB_mem,
    s3a_toSearcher_coe (neg_mem_searcherPaths stratB_mem)]
  rfl

/-- **Theorem 9** (`thm:9`). The searcher strategy `s` keeps the expected capture time at most
`47/32` against every hider path; in particular `V ≤ 47/32`.

The paper's cases (i) `|H(1/2)| ≤ 1/2` and (ii) `|H(1/2)| > 1/2` (by symmetry `H(1/2) > 1/2`).
The expectation is bounded through the four capture times `T(±A, H)`, `T(±B, H)` directly instead
of through `P(t) = P(T ≤ t)`; the bounds are the paper's meeting times. -/
theorem theorem9 :
    (∀ H : hiderPaths, ∫⁻ S, captureTime S H ∂strategy9 ≤ 47 / 32) ∧ upperValue ≤ 47 / 32 := by
  have key : ∀ H : hiderPaths, ∫⁻ S, captureTime S H ∂strategy9 ≤ 47 / 32 := by
    rintro ⟨H, hH⟩
    rw [s3a_lintegral_strategy9]
    rcases le_or_gt (H (1 / 2)) (1 / 2) with h2 | h2
    · rcases le_or_gt (-1 / 2) (H (1 / 2)) with h1 | h1
      · -- case (i): `|H(1/2)| ≤ 1/2`
        obtain ⟨hA, hB⟩ := s3a_case_i hH h1 h2
        exact s3a_expectation_le hA hB (by norm_num)
      · -- case (ii) for the reflection `-H`, which has `-H(1/2) > 1/2`
        obtain ⟨hA, hB⟩ := s3a_case_ii (neg_mem_hiderPaths hH)
          (by rw [ContinuousMap.neg_apply]; linarith)
        have eA : captureTime sweeperA (-H) = captureTime (-sweeperA) H := by
          simpa using captureTime_neg (S := -sweeperA) (H := H)
        have eA' : captureTime (-sweeperA) (-H) = captureTime sweeperA H := captureTime_neg
        have eB : captureTime stratB (-H) = captureTime (-stratB) H := by
          simpa using captureTime_neg (S := -stratB) (H := H)
        have eB' : captureTime (-stratB) (-H) = captureTime stratB H := captureTime_neg
        rw [eA, eA', add_comm] at hA
        rw [eB, eB', add_comm] at hB
        exact s3a_expectation_le hA hB (by norm_num)
    · -- case (ii): `H(1/2) > 1/2`
      obtain ⟨hA, hB⟩ := s3a_case_ii hH h2.le
      exact s3a_expectation_le hA hB (by norm_num)
  refine ⟨key, ?_⟩
  exact iInf_le_of_le ⟨strategy9, inferInstance⟩ (iSup_le key)

/-- Every searcher path meets the end `1` and the end `-1` at times `a`, `b` with `|a - b| ≥ 2`,
so `T(S, E) + T(S, -E) ≥ 2`. -/
private lemma s3a_two_le_captureTime_ends {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    2 ≤ captureTime S hiderE + captureTime S (-hiderE) := by
  by_cases ha : captureTime S hiderE = ⊤
  · rw [ha, top_add]; exact le_top
  by_cases hb : captureTime S (-hiderE) = ⊤
  · rw [hb, add_top]; exact le_top
  obtain ⟨a, ha', hae⟩ := exists_eq_captureTime ha
  obtain ⟨b, hb', hbe⟩ := exists_eq_captureTime hb
  rw [hae, hbe]
  have hSa : S a = 1 := by simpa [hiderE] using ha'
  have hSb : S b = -1 := by simpa [hiderE] using hb'
  have hL := hS.2 a b
  rw [hSa, hSb] at hL
  have hab : |(a : ℝ) - b| ≤ a + b :=
    abs_le.mpr ⟨by linarith [a.coe_nonneg, b.coe_nonneg], by linarith [a.coe_nonneg, b.coe_nonneg]⟩
  have h2 : (2 : ℝ) ≤ a + b := by norm_num at hL; linarith
  exact_mod_cast h2

/-- The equiprobable sweepers guarantee `3/2`, and the hider at a random end guarantees `1`:
`1 ≤ V ≤ 3/2` (Section 3, before Theorem 9). -/
theorem one_le_lowerValue_and_upperValue_le_three_halves :
    1 ≤ lowerValue ∧ upperValue ≤ 3 / 2 := by
  constructor
  · -- the hider at a random end, `½(δ_E + δ_{-E})`
    have := s3a_isProbabilityMeasure_symDiracH hiderE
    have hE : hiderE ∈ hiderPaths := searcherPaths_subset_hiderPaths hiderE_mem
    refine le_iSup_of_le (⟨symDiracH hiderE, inferInstance⟩ : ProbabilityMeasure hiderPaths)
      (le_iInf fun S => ?_)
    change 1 ≤ ∫⁻ H, captureTime S H ∂(symDiracH hiderE)
    rw [s3a_lintegral_symDiracH, s3a_toHider_coe hE, s3a_toHider_coe (neg_mem_hiderPaths hE)]
    calc (1 : ℝ≥0∞) = 1 / 2 * 2 := s3a_half_mul_two.symm
      _ ≤ _ := by gcongr; exact s3a_two_le_captureTime_ends S.2
  · -- the equiprobable sweepers, `½(δ_A + δ_{-A})`
    have := s3a_isProbabilityMeasure_symDiracS sweeperA
    refine iInf_le_of_le (⟨symDiracS sweeperA, inferInstance⟩ : ProbabilityMeasure searcherPaths)
      (iSup_le fun H => ?_)
    change ∫⁻ S, captureTime S H ∂(symDiracS sweeperA) ≤ 3 / 2
    rw [s3a_lintegral_symDiracS, s3a_toSearcher_coe sweeperA_mem,
      s3a_toSearcher_coe (neg_mem_searcherPaths sweeperA_mem)]
    calc 1 / 2 * (captureTime sweeperA H + captureTime (-sweeperA) H)
          ≤ 1 / 2 * (((1 : ℝ≥0) : ℝ≥0∞) + ((2 : ℝ≥0) : ℝ≥0∞)) := by
          refine mul_le_mul' le_rfl ?_
          exact s3a_add_le_of_min_le (by simpa using min_captureTime_sweepers_le_one H.2)
            (s3a_A_le_two H.2) (s3a_negA_le_two H.2)
      _ = ((1 / 2 * (1 + 2) : ℝ≥0) : ℝ≥0∞) := by simp
      _ = 3 / 2 := by
          rw [show (1 / 2 * (1 + 2) : ℝ≥0) = 3 / 2 by norm_num]
          simp [ENNReal.coe_div]

end PrincessMonster
