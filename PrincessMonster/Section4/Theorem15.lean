module

public import PrincessMonster.Section4.Lemmas
public import Mathlib.Order.Filter.Basic
public import Mathlib.Topology.Instances.ENNReal.Lemmas
public import Mathlib.Probability.CDF
public import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-!
# Section 4: formulas (11), (12) and Theorem 15

Varying `Φ` improves the bound `13/9` only marginally. The hider path `H_x` starts at `x ≥ 0`,
runs towards the sweeper `A`, turns `ε` in front of it, runs back towards the middle, and at time
`y` turns again to run to the end.

* `pathHx ε x`: the path `H_x` with `y = 1`: it turns at `ε` at time `1 - 2ε`;
* `equation11`: the variational integral (8) over `H_x` (ignoring `ε`) is (11);
* `equation12`: ignoring `ε`, `V(H_x, s_Φ)` is given by (12);
* `theorem15`: against `σ_Φ` (sweepers with any probability, `s_Φ` with any atomless `Φ`) the
  hider can obtain more than `1.421`.
-/

@[expose] public section

open scoped NNReal ENNReal Topology
open MeasureTheory Filter

namespace PrincessMonster

/-- The hider path `H_x` of Section 4 with `y = 1`: start at `min x (1 - ε)`, run right towards
the sweeper `A`, turn `ε` in front of it and run left just ahead of it, turn at `ε` (time
`1 - 2ε`) and run to the end `+1`. -/
noncomputable def pathHx (ε x : ℝ) : C(ℝ≥0, ℝ) :=
  pathOf (fun t => min 1 (max (min (x + t) (1 - ε - t)) (t - 1 + 3 * ε))) (by fun_prop)

/-- `H_x` has speed at most `1` and stays in `[-1, 1]`: it is a minimum and maximum of unit-speed
motions, cut off at `1`, and it never goes below `3ε - 1`. -/
lemma pathHx_mem {ε x : ℝ} (hε : 0 < ε) :
    pathHx ε x ∈ searcherPaths :=
  pathOf_mem_searcherPaths _
    (fun s t => abs_min_sub_min_le_of (by simp)
      (abs_max_sub_max_le_of (abs_min_sub_min_le_of (le_of_eq (by ring_nf))
        (by rw [show 1 - ε - s - (1 - ε - t) = -(s - t) by ring, abs_neg]))
        (le_of_eq (by ring_nf))))
    (fun t ht => ⟨le_min (by norm_num) (le_max_of_le_right (by linarith)), min_le_left _ _⟩)

/-- **Formula (11)** (`eq:11`). Ignoring `ε`, `H_x(t) = min (x + t) (1 - t)` for `t ≤ y`, and the
variational integral (8) over this path is
`(Φ(x)(1 - x) + ∫_{-1}^{-x} Φ + ∫_{1-2y}^{x} Φ)/2`. The paper prints the lower limit of the first
integral as `0`; the computation gives `-1`, and only `-1` agrees with (12). -/
theorem equation11 {Φ : ℝ → ℝ} (hΦ : Continuous Φ) (hΦ₀ : Φ (-1) = 0) {x y : ℝ}
    (hx : x ∈ Set.Icc (0 : ℝ) 1) (hy : (1 - x) / 2 ≤ y) :
    (∫ t in (0 : ℝ)..y, (Φ (-t + min (x + t) (1 - t)) + Φ (-t - min (x + t) (1 - t)))) =
      1 / 2 * (Φ x * (1 - x) + (∫ t in (-1 : ℝ)..(-x), Φ t) + ∫ t in (1 - 2 * y)..x, Φ t) := by
  have ha0 : 0 ≤ (1 - x) / 2 := by linarith [hx.2]
  have hcont : Continuous fun t =>
      Φ (-t + min (x + t) (1 - t)) + Φ (-t - min (x + t) (1 - t)) := by fun_prop
  rw [← intervalIntegral.integral_add_adjacent_intervals (b := (1 - x) / 2)
    (hcont.intervalIntegrable _ _) (hcont.intervalIntegrable _ _)]
  -- before the turn, `H_x(t) = x + t`
  have h1 : (∫ t in (0 : ℝ)..(1 - x) / 2,
      (Φ (-t + min (x + t) (1 - t)) + Φ (-t - min (x + t) (1 - t)))) =
      ∫ t in (0 : ℝ)..(1 - x) / 2, (Φ x + Φ ((-2) * t + -x)) := by
    refine intervalIntegral.integral_congr fun t ht => ?_
    rw [Set.uIcc_of_le ha0] at ht
    have : min (x + t) (1 - t) = x + t := min_eq_left (by linarith [ht.2])
    simp only [this]
    congr 2 <;> ring
  -- after the turn, `H_x(t) = 1 - t`, and `Φ(-1) = 0`
  have h2 : (∫ t in (1 - x) / 2..y,
      (Φ (-t + min (x + t) (1 - t)) + Φ (-t - min (x + t) (1 - t)))) =
      ∫ t in (1 - x) / 2..y, Φ ((-2) * t + 1) := by
    refine intervalIntegral.integral_congr fun t ht => ?_
    rw [Set.uIcc_of_le hy] at ht
    have : min (x + t) (1 - t) = 1 - t := min_eq_right (by linarith [ht.1])
    simp only [this]
    rw [show -t - (1 - t) = -1 by ring, hΦ₀, add_zero]
    congr 1
    ring
  rw [h1, h2, intervalIntegral.integral_add intervalIntegrable_const
      ((by fun_prop : Continuous fun t : ℝ => Φ ((-2) * t + -x)).intervalIntegrable _ _),
    intervalIntegral.integral_const, intervalIntegral.integral_comp_mul_add Φ (by norm_num),
    intervalIntegral.integral_comp_mul_add Φ (by norm_num),
    show (-2) * ((1 - x) / 2) + -x = -1 by ring, show (-2) * (0 : ℝ) + -x = -x by ring,
    show (-2) * ((1 - x) / 2) + 1 = x by ring, show (-2) * y + 1 = 1 - 2 * y by ring,
    intervalIntegral.integral_symm (-1) (-x), intervalIntegral.integral_symm (1 - 2 * y) x]
  simp only [smul_eq_mul]
  ring


/-! ### Helpers: the sweepers, the integrals over `±A` and `σ`, the distribution function -/

private lemma s4t_sweeperA_apply {t : ℝ≥0} (ht : (t : ℝ) ≤ 2) : sweeperA t = 1 - t := by
  simp only [sweeperA, pathOf_apply]
  exact Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith [t.coe_nonneg]⟩

private lemma s4t_negA_apply {t : ℝ≥0} (ht : (t : ℝ) ≤ 2) : (-sweeperA) t = t - 1 := by
  rw [ContinuousMap.neg_apply, s4t_sweeperA_apply ht]; ring

private lemma s4t_captureTime_negA_le_two {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    captureTime (-sweeperA) H ≤ 2 := by
  have h := captureTime_le_of_le_of_le (S := -sweeperA) (H := H) (t₁ := 0) (t₂ := 2) zero_le
    (by rw [s4t_negA_apply (by simp)]; simp only [NNReal.coe_zero]; linarith [(hH 0).1])
    (by rw [s4t_negA_apply (by simp)]; norm_num; exact (hH 2).2)
  simpa using h

private lemma s4t_toSearcher_val {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    (toSearcher S : C(ℝ≥0, ℝ)) = S := by
  simp [toSearcher, hS]

private lemma s4t_toHider_val {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    (toHider H : C(ℝ≥0, ℝ)) = H := by
  simp [toHider, hH]

private lemma s4t_lintegral_symDiracS (H : C(ℝ≥0, ℝ)) :
    ∫⁻ S, captureTime S H ∂(symDiracS sweeperA) =
      1 / 2 * (captureTime sweeperA H + captureTime (-sweeperA) H) := by
  simp only [symDiracS, lintegral_smul_measure, lintegral_add_measure, lintegral_dirac,
    s4t_toSearcher_val sweeperA_mem, s4t_toSearcher_val (neg_mem_searcherPaths sweeperA_mem),
    smul_eq_mul]

private lemma s4t_lintegral_sigma (p : ℝ≥0∞) (μ : Measure ℝ) (H : C(ℝ≥0, ℝ)) :
    ∫⁻ S, captureTime S H ∂(sigma p μ) =
      p * ∫⁻ S, captureTime S H ∂(symDiracS sweeperA) +
        (1 - p) * ∫⁻ S, captureTime S H ∂(sPhi μ) := by
  rw [sigma, lintegral_add_measure, lintegral_smul_measure, lintegral_smul_measure, smul_eq_mul,
    smul_eq_mul]

private lemma s4t_ofReal_frac (a b : ℕ) [a.AtLeastTwo] [b.AtLeastTwo] :
    (OfNat.ofNat a / OfNat.ofNat b : ℝ≥0∞) = ENNReal.ofReal (OfNat.ofNat a / OfNat.ofNat b) := by
  rw [ENNReal.ofReal_div_of_pos Nat.ofNat_pos]
  simp

private lemma s4t_cdf_eq (μ : Measure ℝ) [IsProbabilityMeasure μ] :
    cdf μ = ProbabilityTheory.cdf μ := by
  funext x
  rw [ProbabilityTheory.cdf_eq_real, cdf, measureReal_def]

/-- The distribution function of an atomless distribution is continuous. -/
private lemma s4t_continuous_cdf (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ] :
    Continuous (cdf μ) := by
  rw [s4t_cdf_eq, continuous_iff_continuousAt]
  intro a
  have hm := (ProbabilityTheory.cdf μ).mono
  rw [hm.continuousAt_iff_leftLim_eq_rightLim, StieltjesFunction.rightLim_eq]
  refine le_antisymm (hm.leftLim_le le_rfl) ?_
  have h := (ProbabilityTheory.cdf μ).measure_singleton a
  rw [ProbabilityTheory.measure_cdf, measure_singleton, eq_comm, ENNReal.ofReal_eq_zero] at h
  linarith

private lemma s4t_monotone_cdf (μ : Measure ℝ) [IsProbabilityMeasure μ] : Monotone (cdf μ) := by
  rw [s4t_cdf_eq]
  exact (ProbabilityTheory.cdf μ).mono

private lemma s4t_cdf_neg_one (μ : Measure ℝ) [NullSingletonClass μ] (hμ : μ Iᶜ = 0) :
    cdf μ (-1) = 0 := by
  have : μ (Set.Iic (-1)) = 0 := by
    refine measure_mono_null (t := Iᶜ ∪ {-1}) ?_ (measure_union_null hμ (measure_singleton _))
    intro z hz
    rcases eq_or_lt_of_le (Set.mem_Iic.mp hz) with h | h
    · exact Or.inr h
    · exact Or.inl fun hI => absurd hI.1 (not_le.mpr h)
  simp [cdf, this]

private lemma s4t_cdf_one (μ : Measure ℝ) [IsProbabilityMeasure μ] (hμ : μ Iᶜ = 0) :
    cdf μ 1 = 1 := by
  have : μ (Set.Iic 1) = 1 := by
    rw [← prob_compl_eq_zero_iff measurableSet_Iic]
    refine measure_mono_null ?_ hμ
    intro z hz hI
    exact hz hI.2
  simp [cdf, this]

/-! ### The paths `H_x` and `E` against the sweepers -/

private lemma s4t_pathHx_apply (ε x : ℝ) (t : ℝ≥0) :
    pathHx ε x t = min 1 (max (min (x + t) (1 - ε - t)) (t - 1 + 3 * ε)) := rfl

/-- At time `1 - 3ε/2` the path `H_x` is at `3ε/2`, where the sweeper `A` is. -/
private lemma s4t_pathHx_meet {ε x : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 4) {t : ℝ≥0}
    (ht : (t : ℝ) = 1 - 3 * ε / 2) : pathHx ε x t = 3 * ε / 2 := by
  rw [s4t_pathHx_apply, ht, max_eq_right (min_le_of_right_le (by linarith)),
    min_eq_right (by linarith)]
  ring

private lemma s4t_captureTime_A_Hx {ε x : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 4) :
    captureTime sweeperA (pathHx ε x) = ((1 - 3 * ε / 2).toNNReal : ℝ≥0∞) := by
  have ht₀ : (((1 - 3 * ε / 2).toNNReal : ℝ≥0) : ℝ) = 1 - 3 * ε / 2 :=
    Real.coe_toNNReal _ (by linarith)
  refine le_antisymm (captureTime_le ?_) (le_captureTime_of_ne fun t ht => ?_)
  · rw [s4t_pathHx_meet hε hε1 ht₀, s4t_sweeperA_apply (by rw [ht₀]; linarith), ht₀]
    ring
  · have ht' : (t : ℝ) < 1 - 3 * ε / 2 := by rw [← ht₀]; exact_mod_cast ht
    rw [s4t_sweeperA_apply (by linarith)]
    refine ne_of_gt (lt_of_le_of_lt (min_le_of_right_le (max_le_max (min_le_right _ _) le_rfl))
      (max_lt (by linarith) (by linarith)))

private lemma s4t_captureTime_negA_Hx {ε x : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 4)
    (hx : x ∈ Set.Icc (0 : ℝ) 1) : captureTime (-sweeperA) (pathHx ε x) = 2 := by
  refine le_antisymm (s4t_captureTime_negA_le_two
    (searcherPaths_subset_hiderPaths (pathHx_mem hε))) ?_
  have h := le_captureTime_of_ne (S := -sweeperA) (H := pathHx ε x) (c := 2) fun t ht => by
    have ht' : (t : ℝ) < 2 := by exact_mod_cast ht
    rw [s4t_negA_apply ht'.le, s4t_pathHx_apply]
    exact ne_of_lt (lt_min (by linarith) (lt_max_of_lt_right (by linarith)))
  simpa using h

private lemma s4t_lintegral_symDiracS_Hx {ε x : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 4)
    (hx : x ∈ Set.Icc (0 : ℝ) 1) :
    ∫⁻ S, captureTime S (pathHx ε x) ∂(symDiracS sweeperA) =
      ENNReal.ofReal (1 / 2 * (1 - 3 * ε / 2 + 2)) := by
  rw [s4t_lintegral_symDiracS, s4t_captureTime_A_Hx hε hε1, s4t_captureTime_negA_Hx hε hε1 hx,
    ENNReal.ofReal_mul (by norm_num), ENNReal.ofReal_add (by linarith) (by norm_num),
    ENNReal.ofReal_div_of_pos two_pos]
  simp [ENNReal.ofReal]

private lemma s4t_captureTime_A_E : captureTime sweeperA hiderE = 0 :=
  le_antisymm (by
    have h := captureTime_le (S := sweeperA) (H := hiderE) (t := 0)
      (by rw [s4t_sweeperA_apply (by simp)]; simp [hiderE])
    simpa using h) bot_le

private lemma s4t_captureTime_negA_E : captureTime (-sweeperA) hiderE = 2 := by
  refine le_antisymm (s4t_captureTime_negA_le_two (searcherPaths_subset_hiderPaths hiderE_mem)) ?_
  have h := le_captureTime_of_ne (S := -sweeperA) (H := hiderE) (c := 2) fun t ht => by
    have ht' : (t : ℝ) < 2 := by exact_mod_cast ht
    rw [s4t_negA_apply ht'.le]
    simp only [hiderE, ContinuousMap.const_apply]
    linarith
  simpa using h

/-- The hider at the end `+1` against `σ_Φ`: `1` against the sweepers, `3` against `s_Φ` (by (9),
`equation9`). -/
private lemma s4t_payoff_E (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ]
    (hμ : μ Iᶜ = 0) (p : ℝ≥0∞) :
    ∫⁻ S, captureTime S hiderE ∂(sigma p μ) = p * 1 + (1 - p) * 3 := by
  have hyA : captureTime sweeperA hiderE = ((0 : ℝ≥0) : ℝ≥0∞) := by
    rw [s4t_captureTime_A_E, ENNReal.coe_zero]
  have hs := equation9 μ hμ hiderE_mem hyA
    (by rw [s4t_captureTime_A_E, s4t_captureTime_negA_E]; norm_num)
    (fun t _ => by
      simp only [hiderE, ContinuousMap.const_apply, NNReal.coe_zero, sub_zero]
      exact (min_eq_left (by linarith [t.coe_nonneg])).symm)
  have hE0 : hiderE 0 = 1 := rfl
  rw [hE0, NNReal.coe_zero, formula9] at hs
  simp only [mul_zero, sub_zero, zero_div, zero_mul, intervalIntegral.integral_same, add_zero,
    s4t_cdf_neg_one μ hμ, s4t_cdf_one μ hμ] at hs
  norm_num at hs
  rw [s4t_lintegral_sigma, s4t_lintegral_symDiracS, s4t_captureTime_A_E, s4t_captureTime_negA_E,
    hs, zero_add, ENNReal.div_mul_cancel two_ne_zero ENNReal.ofNat_ne_top]

/-! ### The payoff of `H_x` against `s_Φ` as a function of `ε` -/

/-- The path `H_x` with the turning parameter `ε`, at real time `s`. -/
private noncomputable def s4t_h (x ε s : ℝ) : ℝ :=
  min 1 (max (min (x + s) (1 - ε - s)) (s - 1 + 3 * ε))

private lemma s4t_realPath_pathHx (ε x : ℝ) :
    realPath (pathHx ε x) = fun t => s4t_h x ε (max t 0) := by
  funext t
  simp only [realPath, pathHx, pathOf_apply, Real.coe_toNNReal', s4t_h]

/-- The right-hand side of (9) for `H_x` with parameter `ε` is continuous in `ε`. -/
private lemma s4t_continuous_formula9 {Φ : ℝ → ℝ} (hΦ : Continuous Φ) (x : ℝ) :
    Continuous fun ε =>
      formula9 Φ (s4t_h x ε 0) (1 - 3 * ε / 2) (fun t => s4t_h x ε (max t 0)) := by
  have hc : Continuous (Function.uncurry fun ε t =>
      Φ (-t + s4t_h x ε (max t 0)) + Φ (-t - s4t_h x ε (max t 0))) := by
    change Continuous fun p : ℝ × ℝ =>
      Φ (-p.2 + s4t_h x p.1 (max p.2 0)) + Φ (-p.2 - s4t_h x p.1 (max p.2 0))
    unfold s4t_h
    fun_prop
  have hI : Continuous fun ε : ℝ => ∫ t in (0 : ℝ)..(1 - 3 * ε / 2),
      (Φ (-t + s4t_h x ε (max t 0)) + Φ (-t - s4t_h x ε (max t 0))) :=
    (intervalIntegral.continuous_parametric_primitive_of_continuous (μ := volume) (a₀ := 0)
      hc).comp (continuous_id.prodMk (by fun_prop : Continuous fun ε : ℝ => 1 - 3 * ε / 2))
  have hh : Continuous fun ε => s4t_h x ε 0 := by unfold s4t_h; fun_prop
  unfold formula9
  fun_prop

/-- **Formula (12)** (`eq:12`). Ignoring `ε` (that is, as `ε → 0⁺`), the payoff of `H_x` against
`s_Φ` is `3/2 - Φ(-x) - Φ(x)(1 + x)/4 + (1/4) ∫_{-1}^{-x} Φ + (1/4) ∫_{-1}^{x} Φ`, and against the
sweepers it is `3/2`.

Proof, as in the paper (`eq:9`, `eq:11`): for `0 < ε < 1/4` the path `H_x = pathHx ε x` meets `A`
first, at `y_ε = 1 - 3ε/2` (where `H_x(y_ε) = 1 - y_ε`), meets `-A` at time `2`, and runs to `+1`
after `y_ε`; so (9) (`equation9`) gives its payoff against `s_Φ` exactly. That expression is
continuous in `ε` (`Φ` is continuous because `μ` is atomless; the integral depends continuously on
its integrand and its upper limit), and at `ε = 0` it is (9) with `y = 1` for the path
`min (x + t) (1 - t)`, which (11) (`equation11`) turns into (12). Against `±A` the payoff is
`(T(A, H_x) + T(-A, H_x))/2 = (1 - 3ε/2 + 2)/2 → 3/2`. -/
theorem equation12 (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ] (hμ : μ Iᶜ = 0)
    {x : ℝ} (hx : x ∈ Set.Icc (0 : ℝ) 1) :
    Tendsto (fun ε => ∫⁻ S, captureTime S (pathHx ε x) ∂(sPhi μ)) (𝓝[>] 0)
        (𝓝 (ENNReal.ofReal (3 / 2 - cdf μ (-x) - cdf μ x * (1 + x) / 4 +
          1 / 4 * (∫ t in (-1 : ℝ)..(-x), cdf μ t) + 1 / 4 * ∫ t in (-1 : ℝ)..x, cdf μ t))) ∧
      Tendsto (fun ε => ∫⁻ S, captureTime S (pathHx ε x) ∂(symDiracS sweeperA)) (𝓝[>] 0)
        (𝓝 (3 / 2)) := by
  have hΦc := s4t_continuous_cdf μ
  have hΦm1 := s4t_cdf_neg_one μ hμ
  have hKc := s4t_continuous_formula9 hΦc x
  -- at `ε = 0` the right-hand side of (9) is (12), by (11)
  have hK0 : formula9 (cdf μ) (s4t_h x 0 0) (1 - 3 * 0 / 2) (fun t => s4t_h x 0 (max t 0)) =
      3 / 2 - cdf μ (-x) - cdf μ x * (1 + x) / 4 +
        1 / 4 * (∫ t in (-1 : ℝ)..(-x), cdf μ t) + 1 / 4 * ∫ t in (-1 : ℝ)..x, cdf μ t := by
    have hx0 : s4t_h x 0 0 = x := by
      unfold s4t_h
      rw [min_eq_left (by linarith [hx.2] : x + 0 ≤ 1 - 0 - 0), max_eq_left (by linarith [hx.1]),
        min_eq_right (by linarith [hx.2])]
      ring
    have hint : (∫ t in (0 : ℝ)..1,
        (cdf μ (-t + s4t_h x 0 (max t 0)) + cdf μ (-t - s4t_h x 0 (max t 0)))) =
        ∫ t in (0 : ℝ)..1,
          (cdf μ (-t + min (x + t) (1 - t)) + cdf μ (-t - min (x + t) (1 - t))) := by
      refine intervalIntegral.integral_congr fun t ht => ?_
      rw [Set.uIcc_of_le zero_le_one] at ht
      have : s4t_h x 0 (max t 0) = min (x + t) (1 - t) := by
        rw [max_eq_left ht.1]
        unfold s4t_h
        rw [sub_zero, mul_zero, add_zero,
          max_eq_left (le_min (by linarith [hx.1]) (by linarith [ht.2])),
          min_eq_right (min_le_of_right_le (by linarith [ht.1]))]
      simp only [this]
    rw [hx0, show (1 : ℝ) - 3 * 0 / 2 = 1 by norm_num, formula9, hint,
      equation11 hΦc hΦm1 hx (by linarith [hx.1]), show (1 : ℝ) - 2 * 1 = -1 by norm_num,
      hΦm1]
    ring
  -- for `0 < ε < 1/4`, (9) gives the payoff exactly
  have hKeq : ∀ ε ∈ Set.Ioo (0 : ℝ) (1 / 4), ∫⁻ S, captureTime S (pathHx ε x) ∂(sPhi μ) =
      ENNReal.ofReal
        (formula9 (cdf μ) (s4t_h x ε 0) (1 - 3 * ε / 2) (fun t => s4t_h x ε (max t 0))) := by
    intro ε hε
    have hA := s4t_captureTime_A_Hx (x := x) hε.1 hε.2.le
    have ht₀ : (((1 - 3 * ε / 2).toNNReal : ℝ≥0) : ℝ) = 1 - 3 * ε / 2 :=
      Real.coe_toNNReal _ (by linarith [hε.2])
    have h9 := equation9 μ hμ (pathHx_mem hε.1) hA
      (by
        rw [hA, s4t_captureTime_negA_Hx hε.1 hε.2.le hx]
        have : (1 - 3 * ε / 2).toNNReal < 2 := by
          rw [← NNReal.coe_lt_coe, ht₀]; norm_num; linarith [hε.1]
        exact_mod_cast this)
      (fun t ht => by
        have ht' : 1 - 3 * ε / 2 ≤ (t : ℝ) := by rw [← ht₀]; exact_mod_cast ht
        rw [s4t_pathHx_meet hε.1 hε.2.le ht₀, ht₀, s4t_pathHx_apply,
          max_eq_right (min_le_of_right_le (by linarith [hε.1]))]
        congr 1
        ring)
    rw [h9, s4t_realPath_pathHx, ht₀]
    rfl
  refine ⟨?_, ?_⟩
  · rw [← hK0]
    refine Tendsto.congr' ?_ ((ENNReal.tendsto_ofReal (hKc.tendsto 0)).mono_left
      nhdsWithin_le_nhds)
    filter_upwards [Ioo_mem_nhdsGT (by norm_num : (0 : ℝ) < 1 / 4)] with ε hε
    exact (hKeq ε hε).symm
  · have hc : Continuous fun ε : ℝ => 1 / 2 * (1 - 3 * ε / 2 + 2) := by fun_prop
    have hlim := (ENNReal.tendsto_ofReal (hc.tendsto 0)).mono_left
      (nhdsWithin_le_nhds (s := Set.Ioi 0))
    rw [show 1 / 2 * (1 - 3 * (0 : ℝ) / 2 + 2) = 3 / 2 by norm_num, ← s4t_ofReal_frac] at hlim
    refine Tendsto.congr' ?_ hlim
    filter_upwards [Ioo_mem_nhdsGT (by norm_num : (0 : ℝ) < 1 / 4)] with ε hε
    exact (s4t_lintegral_symDiracS_Hx hε.1 hε.2.le hx).symm

/-! ### Lower Riemann sums for (12) -/

/-- The payoff (12) of `H_x` against `s_Φ`. -/
private noncomputable def s4t_S (Φ : ℝ → ℝ) (x : ℝ) : ℝ :=
  3 / 2 - Φ (-x) - Φ x * (1 + x) / 4 + 1 / 4 * (∫ t in (-1 : ℝ)..(-x), Φ t) +
    1 / 4 * ∫ t in (-1 : ℝ)..x, Φ t

/-- A lower Riemann sum with one step: for nondecreasing `Φ`, `∫_a^b Φ ≥ (b - a) Φ(a)`. -/
private lemma s4t_integral_ge {Φ : ℝ → ℝ} (hm : Monotone Φ) {a b : ℝ} (hab : a ≤ b) :
    (b - a) * Φ a ≤ ∫ t in a..b, Φ t := by
  have h := intervalIntegral.integral_mono_on hab intervalIntegrable_const
    (hm.intervalIntegrable (μ := volume)) (fun t ht => hm ht.1)
  rwa [intervalIntegral.integral_const, smul_eq_mul] at h

/-- The integrals in (12) bounded below by left Riemann sums with step `1/2`: the second row of
the `2 × 4` matrix game of Theorem 15, with `a = Φ(-1/2)`, `b = Φ(0)`, `c = Φ(1/2)`. -/
private lemma s4t_S_bounds {Φ : ℝ → ℝ} (hm : Monotone Φ) (h0 : Φ (-1) = 0) (h1 : Φ 1 = 1) :
    1 + (Φ (-(1 / 2)) + Φ 0 + Φ (1 / 2)) / 8 ≤ s4t_S Φ 1 ∧
      3 / 2 + Φ (-(1 / 2)) / 4 - 5 * Φ 0 / 4 ≤ s4t_S Φ 0 ∧
      3 / 2 - 7 * Φ (-(1 / 2)) / 8 + Φ 0 / 8 - 3 * Φ (1 / 2) / 8 ≤ s4t_S Φ (1 / 2) := by
  have hi : ∀ a b : ℝ, IntervalIntegrable Φ volume a b := fun a b => hm.intervalIntegrable
  have e1 := intervalIntegral.integral_add_adjacent_intervals (hi (-1) (-(1 / 2))) (hi (-(1 / 2)) 0)
  have e2 := intervalIntegral.integral_add_adjacent_intervals (hi (-1) 0) (hi 0 (1 / 2))
  have e3 := intervalIntegral.integral_add_adjacent_intervals (hi (-1) (1 / 2)) (hi (1 / 2) 1)
  have b1 := s4t_integral_ge hm (show (-1 : ℝ) ≤ -(1 / 2) by norm_num)
  have b2 := s4t_integral_ge hm (show -(1 / 2 : ℝ) ≤ 0 by norm_num)
  have b3 := s4t_integral_ge hm (show (0 : ℝ) ≤ 1 / 2 by norm_num)
  have b4 := s4t_integral_ge hm (show (1 / 2 : ℝ) ≤ 1 by norm_num)
  unfold s4t_S
  rw [neg_zero, intervalIntegral.integral_same, h1]
  refine ⟨by linarith, by linarith, by linarith⟩

/-- One entry of the expected payoff, as a real number: `ofReal` is subadditive. -/
private lemma s4t_term {q P A B : ℝ} (hq : 0 ≤ q) (hP : 0 ≤ P) (hP1 : P ≤ 1) :
    ENNReal.ofReal (q * (P * A + (1 - P) * B)) ≤
      ENNReal.ofReal q *
        (ENNReal.ofReal P * ENNReal.ofReal A + ENNReal.ofReal (1 - P) * ENNReal.ofReal B) := by
  rw [ENNReal.ofReal_mul hq, ← ENNReal.ofReal_mul hP, ← ENNReal.ofReal_mul (sub_nonneg.mpr hP1)]
  exact mul_le_mul_right ENNReal.ofReal_add_le _

/-- **Theorem 15** (`thm:15`). If the searcher uses a mixed strategy `σ_Φ` on the sweepers and
`s_Φ`, for any atomless distribution `Φ` on `[-1, 1]` and any probability `p` of the sweepers,
the hider can respond with a mixed strategy `γ` such that `V(σ_Φ, γ) > 1.421`.

Proof, as in the paper with the hider's mixture `q = (37, 148, 24, 28)/237` on `(E, H_1, H_0,
H_{1/2})`, which does not depend on `Φ` (the paper takes the optimal `γ_Φ` of a `2 × 4` matrix
game; `q` is optimal at the searcher's minimizing `Φ` and good for every `Φ`). Against `±A` the
four paths get `1` and, as `ε → 0⁺`, `3/2` (`equation12`); against `s_Φ` they get `3` (by (9),
`equation9`) and the values (12) (`equation12`). Bounding the integrals in (12) below by left
Riemann sums with step `1/2` (`Φ` is nondecreasing and `Φ(-1) = 0`) gives, with
`a = Φ(-1/2) ≤ b = Φ(0) ≤ c = Φ(1/2)`, the rows `(1, 3/2, 3/2, 3/2)` and
`(3, 1 + (a + b + c)/8, 3/2 + a/4 - 5b/4, 3/2 - 7a/8 + b/8 - 3c/8)`; against them `q` gets
`337/237` and `(337 - 8b + 8c)/237 ≥ 337/237`. So the payoff of `q` tends, as `ε → 0⁺`, to at
least `337/237 = 1.4219… > 1.421`, and a small `ε` (depending on `Φ` and `p`) gives the
required `γ`. -/
theorem theorem15 (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ] (hμ : μ Iᶜ = 0)
    {p : ℝ≥0∞} (hp : p ≤ 1) :
    ∃ γ : Measure hiderPaths, IsProbabilityMeasure γ ∧
      (1421 / 1000 : ℝ≥0∞) < ∫⁻ H, ∫⁻ S, captureTime S H ∂(sigma p μ) ∂γ := by
  have hp_top : p ≠ ⊤ := ne_top_of_le_ne_top ENNReal.one_ne_top hp
  obtain ⟨p', hp'0, rfl⟩ : ∃ p' : ℝ, 0 ≤ p' ∧ p = ENNReal.ofReal p' :=
    ⟨p.toReal, ENNReal.toReal_nonneg, (ENNReal.ofReal_toReal hp_top).symm⟩
  have hp'1 : p' ≤ 1 := by
    rwa [← ENNReal.ofReal_one, ENNReal.ofReal_le_ofReal_iff zero_le_one] at hp
  have h1p : 1 - ENNReal.ofReal p' = ENNReal.ofReal (1 - p') := by
    rw [ENNReal.ofReal_sub _ hp'0, ENNReal.ofReal_one]
  have hm := s4t_monotone_cdf μ
  obtain ⟨hS1, hS0, hSh⟩ := s4t_S_bounds hm (s4t_cdf_neg_one μ hμ) (s4t_cdf_one μ hμ)
  have hbc : cdf μ 0 ≤ cdf μ (1 / 2) := hm (by norm_num)
  have hx1 : (1 : ℝ) ∈ Set.Icc (0 : ℝ) 1 := ⟨zero_le_one, le_rfl⟩
  have hx0 : (0 : ℝ) ∈ Set.Icc (0 : ℝ) 1 := ⟨le_rfl, zero_le_one⟩
  have hxh : (1 / 2 : ℝ) ∈ Set.Icc (0 : ℝ) 1 := ⟨by norm_num, by norm_num⟩
  -- the payoffs: `E` gets `1` against the sweepers and `3` against `s_Φ`
  have hgE : ∫⁻ S, captureTime S hiderE ∂(sigma (ENNReal.ofReal p') μ) =
      ENNReal.ofReal p' * ENNReal.ofReal 1 + ENNReal.ofReal (1 - p') * ENNReal.ofReal 3 := by
    rw [s4t_payoff_E μ hμ, h1p, ENNReal.ofReal_one, ENNReal.ofReal_ofNat]
  -- `H_x` gets `3/2` against the sweepers and (12) against `s_Φ`, as `ε → 0⁺`
  have hlimx : ∀ x ∈ Set.Icc (0 : ℝ) 1,
      Tendsto (fun ε => ∫⁻ S, captureTime S (pathHx ε x) ∂(sigma (ENNReal.ofReal p') μ))
        (𝓝[>] 0) (𝓝 (ENNReal.ofReal p' * ENNReal.ofReal (3 / 2) +
          ENNReal.ofReal (1 - p') * ENNReal.ofReal (s4t_S (cdf μ) x))) := by
    intro x hx
    obtain ⟨hs, ha⟩ := equation12 μ hμ hx
    simp only [s4t_lintegral_sigma, h1p]
    rw [← s4t_ofReal_frac 3 2]
    exact (ENNReal.Tendsto.const_mul ha (Or.inr ENNReal.ofReal_ne_top)).add
      (ENNReal.Tendsto.const_mul hs (Or.inr ENNReal.ofReal_ne_top))
  -- the hider mixture `(37, 148, 24, 28)/237` on `(E, H_1, H_0, H_{1/2})`
  have hlim := ((tendsto_const_nhds (x := ENNReal.ofReal (37 / 237) *
      ∫⁻ S, captureTime S hiderE ∂(sigma (ENNReal.ofReal p') μ))).add
      (ENNReal.Tendsto.const_mul (hlimx 1 hx1)
        (Or.inr (ENNReal.ofReal_ne_top (r := 148 / 237))))).add
      (ENNReal.Tendsto.const_mul (hlimx 0 hx0)
        (Or.inr (ENNReal.ofReal_ne_top (r := 24 / 237)))) |>.add
      (ENNReal.Tendsto.const_mul (hlimx (1 / 2) hxh)
        (Or.inr (ENNReal.ofReal_ne_top (r := 28 / 237))))
  -- its limit payoff is at least `337/237 > 1.421`, whatever `Φ` and `p`
  have hL : (1421 / 1000 : ℝ≥0∞) < ENNReal.ofReal (37 / 237) *
        ∫⁻ S, captureTime S hiderE ∂(sigma (ENNReal.ofReal p') μ) +
      ENNReal.ofReal (148 / 237) * (ENNReal.ofReal p' * ENNReal.ofReal (3 / 2) +
        ENNReal.ofReal (1 - p') * ENNReal.ofReal (s4t_S (cdf μ) 1)) +
      ENNReal.ofReal (24 / 237) * (ENNReal.ofReal p' * ENNReal.ofReal (3 / 2) +
        ENNReal.ofReal (1 - p') * ENNReal.ofReal (s4t_S (cdf μ) 0)) +
      ENNReal.ofReal (28 / 237) * (ENNReal.ofReal p' * ENNReal.ofReal (3 / 2) +
        ENNReal.ofReal (1 - p') * ENNReal.ofReal (s4t_S (cdf μ) (1 / 2))) := by
    rw [hgE]
    have key : 0 ≤ (1 - p') * (148 * s4t_S (cdf μ) 1 + 24 * s4t_S (cdf μ) 0 +
        28 * s4t_S (cdf μ) (1 / 2) - 226) := mul_nonneg (by linarith) (by linarith)
    have hreal : (1421 / 1000 : ℝ) < 37 / 237 * (p' * 1 + (1 - p') * 3) +
        148 / 237 * (p' * (3 / 2) + (1 - p') * s4t_S (cdf μ) 1) +
        24 / 237 * (p' * (3 / 2) + (1 - p') * s4t_S (cdf μ) 0) +
        28 / 237 * (p' * (3 / 2) + (1 - p') * s4t_S (cdf μ) (1 / 2)) := by
      have expand : 37 / 237 * (p' * 1 + (1 - p') * 3) +
          148 / 237 * (p' * (3 / 2) + (1 - p') * s4t_S (cdf μ) 1) +
          24 / 237 * (p' * (3 / 2) + (1 - p') * s4t_S (cdf μ) 0) +
          28 / 237 * (p' * (3 / 2) + (1 - p') * s4t_S (cdf μ) (1 / 2)) =
          337 / 237 + (1 - p') * (148 * s4t_S (cdf μ) 1 + 24 * s4t_S (cdf μ) 0 +
            28 * s4t_S (cdf μ) (1 / 2) - 226) / 237 := by ring
      rw [expand]
      linarith
    calc (1421 / 1000 : ℝ≥0∞) = ENNReal.ofReal (1421 / 1000) := s4t_ofReal_frac _ _
      _ < ENNReal.ofReal (37 / 237 * (p' * 1 + (1 - p') * 3) +
          148 / 237 * (p' * (3 / 2) + (1 - p') * s4t_S (cdf μ) 1) +
          24 / 237 * (p' * (3 / 2) + (1 - p') * s4t_S (cdf μ) 0) +
          28 / 237 * (p' * (3 / 2) + (1 - p') * s4t_S (cdf μ) (1 / 2))) :=
        (ENNReal.ofReal_lt_ofReal_iff (by linarith)).mpr hreal
      _ ≤ _ := ENNReal.ofReal_add_le.trans (add_le_add_left (ENNReal.ofReal_add_le.trans
          (add_le_add_left ENNReal.ofReal_add_le _)) _)
      _ ≤ _ := by
        gcongr ?_ + ?_ + ?_ + ?_ <;> exact s4t_term (by norm_num) hp'0 hp'1
  obtain ⟨ε, hε1, hε2⟩ := ((hlim.eventually_const_lt hL).and
    (Ioo_mem_nhdsGT (by norm_num : (0 : ℝ) < 1 / 4))).exists
  have hmem : ∀ x ∈ Set.Icc (0 : ℝ) 1, pathHx ε x ∈ hiderPaths := fun x hx =>
    searcherPaths_subset_hiderPaths (pathHx_mem hε2.1)
  refine ⟨ENNReal.ofReal (37 / 237) • Measure.dirac (toHider hiderE) +
    ENNReal.ofReal (148 / 237) • Measure.dirac (toHider (pathHx ε 1)) +
    ENNReal.ofReal (24 / 237) • Measure.dirac (toHider (pathHx ε 0)) +
    ENNReal.ofReal (28 / 237) • Measure.dirac (toHider (pathHx ε (1 / 2))), ?_, ?_⟩
  · constructor
    simp only [Measure.add_apply, Measure.smul_apply, measure_univ, smul_eq_mul, mul_one]
    rw [← ENNReal.ofReal_add (by norm_num) (by norm_num),
      ← ENNReal.ofReal_add (by norm_num) (by norm_num),
      ← ENNReal.ofReal_add (by norm_num) (by norm_num)]
    norm_num
  · rw [lintegral_add_measure, lintegral_add_measure, lintegral_add_measure,
      lintegral_smul_measure, lintegral_smul_measure, lintegral_smul_measure,
      lintegral_smul_measure, lintegral_dirac, lintegral_dirac, lintegral_dirac, lintegral_dirac,
      s4t_toHider_val (searcherPaths_subset_hiderPaths hiderE_mem), s4t_toHider_val (hmem 1 hx1),
      s4t_toHider_val (hmem 0 hx0), s4t_toHider_val (hmem _ hxh)]
    simpa only [smul_eq_mul] using hε1

end PrincessMonster
