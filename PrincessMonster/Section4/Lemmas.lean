module

public import PrincessMonster.Section4.Runners
public import Mathlib.Analysis.Calculus.Deriv.Basic
public import Mathlib.Analysis.Calculus.ContDiff.Defs
public import Mathlib.Analysis.Calculus.ContDiff.Deriv
public import Mathlib.MeasureTheory.Integral.Layercake
public import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts

/-!
# Section 4: Lemmas 11–13 and the payoff formulas (9), (10)

Let `H` be a hider path of speed at most `1` and `y` the first time it meets a sweeper.

* `lemma11`: the searchers of `s_Φ` that find `H` before time `y` are exactly the right runners
  starting in `(H(y) - y, H(0)]` and the left runners starting in `[H(0), H(y) + y)` (up to the
  starting point `H(y) ∓ y` itself, where the paper's statement fails).
* `lemma12`: when `Φ` has a continuous density `f` and `H` is smooth, these searchers find `H`
  with expected time (5) and (6).
* `lemma13`: integrating (7) by parts gives `(8) - y Φ(1 - 2y)`.
* `s4_lemma13'` ("Lemma 13'"): Lemmas 12 and 13 combined for paths of speed at most `1`, with no
  smoothness assumption and any atomless distribution `Φ`: the two groups of searchers contribute
  `∫₀^y (Φ(H(t) - t) - Φ(1 - 2y)) dt` and `∫₀^y Φ(-H(t) - t) dt`. It is needed because the
  dominating path of Proposition 3 is only Lipschitz.
* `equation9`: the payoff `V(s_Φ, H)` of formula (9), when after time `y` the hider runs to the
  end; `equation9_le`: (9) bounds the payoff whatever the hider does after `y`.
* `equation10`: for the uniform distribution, (9) equals `(10 + 2x - (7 + x) y + y²)/4`.

## Proofs

The key computation is the layer-cake identity `E[T] = ∫₀^∞ P(T > s) ds` (`s4_layer_right`,
`s4_layer_left`, valid for any distribution of the starting point): when `H` meets `A` first, a
right runner starting at `x ∈ (H(y) - y, H(0)]` has not caught `H` by time `s` if and only if
`x < H(s) - s`, and a left runner starting at `z ∈ [H(0), H(y) + y)` if and only if
`H(s) + s < z`. It gives Lemma 13' directly, and Lemma 12 after an integration by parts (the
paper's Lemma 13 read backwards). Formula (9) then adds up the five groups of searchers of
Lemma 11. The measurability of the capture time in the searcher path, needed to integrate over
`s_Φ`, is `s4_measurable_captureTime`: `{S | T(S, H) > c}` is open in the compact-open topology.
-/

@[expose] public section

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonster

section Helpers

variable {S H : C(ℝ≥0, ℝ)}

/-- `T(S, H) > c` if and only if the paths do not meet during `[0, c]`. -/
lemma s4_lt_captureTime_iff {c : ℝ≥0} :
    (c : ℝ≥0∞) < captureTime S H ↔ ∀ t : ℝ≥0, t ≤ c → S t ≠ H t := by
  constructor
  · intro h t ht heq
    exact absurd h (not_lt.mpr ((captureTime_le heq).trans (ENNReal.coe_le_coe.mpr ht)))
  · intro h
    by_cases htop : captureTime S H = ⊤
    · rw [htop]; exact ENNReal.coe_lt_top
    · obtain ⟨t, hst, ht⟩ := exists_eq_captureTime htop
      rw [ht, ENNReal.coe_lt_coe]
      by_contra hle
      exact h t (not_lt.mp hle) hst

/-- The capture time is a measurable function of the searcher path. -/
lemma s4_measurable_captureTime (H : C(ℝ≥0, ℝ)) :
    Measurable fun S : C(ℝ≥0, ℝ) => captureTime S H := by
  refine measurable_of_Ioi fun c => ?_
  induction c using ENNReal.recTopCoe with
  | top => simp
  | coe c =>
    apply IsOpen.measurableSet
    have : (fun S : C(ℝ≥0, ℝ) => captureTime S H) ⁻¹' Set.Ioi (c : ℝ≥0∞) =
        (fun S => S - H) ⁻¹' {G : C(ℝ≥0, ℝ) | Set.MapsTo G (Set.Icc 0 c) {0}ᶜ} := by
      ext S
      simp only [Set.mem_preimage, Set.mem_Ioi, Set.mem_ofPred_eq, s4_lt_captureTime_iff]
      constructor
      · intro h t ht
        simpa [sub_eq_zero] using h t ht.2
      · intro h t ht
        simpa [sub_eq_zero] using h ⟨bot_le, ht⟩
    rw [this]
    exact (ContinuousMap.isOpen_setOfPred_mapsTo isCompact_Icc isOpen_compl_singleton).preimage
      (continuous_sub_right H)

lemma s4_continuous_runner : Continuous runner := by
  apply ContinuousMap.continuous_of_continuous_uncurry
  change Continuous fun p : ℝ × ℝ≥0 => Real.triangleWave (min (p.1 + p.2) (1 - p.2))
  fun_prop

lemma s4_continuous_leftRunner : Continuous leftRunner := by
  apply ContinuousMap.continuous_of_continuous_uncurry
  change Continuous fun p : ℝ × ℝ≥0 => Real.triangleWave (max (p.1 - p.2) (p.2 - 1))
  fun_prop

lemma s4_toSearcher_runner (x : ℝ) : (toSearcher (runner x) : C(ℝ≥0, ℝ)) = runner x := by
  simp [toSearcher, runner_mem x]

lemma s4_toSearcher_leftRunner (x : ℝ) :
    (toSearcher (leftRunner x) : C(ℝ≥0, ℝ)) = leftRunner x := by
  simp [toSearcher, leftRunner_mem x]

lemma s4_measurable_toSearcher_runner : Measurable fun x => toSearcher (runner x) := by
  have : (fun x => toSearcher (runner x)) =
      fun x => (⟨runner x, runner_mem x⟩ : searcherPaths) := by
    funext x; simp [toSearcher, runner_mem x]
  rw [this]
  exact s4_continuous_runner.measurable.subtype_mk

lemma s4_measurable_toSearcher_leftRunner :
    Measurable fun x : ℝ => toSearcher (leftRunner (-x)) := by
  have : (fun x : ℝ => toSearcher (leftRunner (-x))) =
      fun x => (⟨leftRunner (-x), leftRunner_mem (-x)⟩ : searcherPaths) := by
    funext x; simp [toSearcher, leftRunner_mem (-x)]
  rw [this]
  exact (s4_continuous_leftRunner.measurable.comp measurable_neg).subtype_mk

/-- The expected capture time against `s_Φ` splits into the right and the left runners. -/
lemma s4_lintegral_sPhi (μ : Measure ℝ) (H : C(ℝ≥0, ℝ)) :
    ∫⁻ S, captureTime S H ∂(sPhi μ) = (1 / 2 : ℝ≥0∞) *
      (∫⁻ x, captureTime (runner x) H ∂μ + ∫⁻ x, captureTime (leftRunner (-x)) H ∂μ) := by
  have hf : Measurable fun S : searcherPaths => captureTime (S : C(ℝ≥0, ℝ)) H :=
    (s4_measurable_captureTime H).comp measurable_subtype_coe
  rw [sPhi, lintegral_smul_measure, lintegral_add_measure,
    lintegral_map hf s4_measurable_toSearcher_runner,
    lintegral_map hf s4_measurable_toSearcher_leftRunner]
  simp only [s4_toSearcher_runner, s4_toSearcher_leftRunner, smul_eq_mul]

lemma s4_measurable_captureTime_runner (H : C(ℝ≥0, ℝ)) :
    Measurable fun x => captureTime (runner x) H :=
  (s4_measurable_captureTime H).comp s4_continuous_runner.measurable

lemma s4_measurable_captureTime_leftRunner (H : C(ℝ≥0, ℝ)) :
    Measurable fun x => captureTime (leftRunner x) H :=
  (s4_measurable_captureTime H).comp s4_continuous_leftRunner.measurable

/-! Evaluation of the sweepers and runners. -/

lemma s4_sweeperA_apply {t : ℝ≥0} (ht : (t : ℝ) ≤ 2) : sweeperA t = 1 - t := by
  simp only [sweeperA, pathOf_apply]
  exact Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith [NNReal.coe_nonneg t]⟩

lemma s4_negA_apply {t : ℝ≥0} (ht : (t : ℝ) ≤ 2) : (-sweeperA) t = t - 1 := by
  rw [ContinuousMap.neg_apply, s4_sweeperA_apply ht]; ring

lemma s4_runner_apply {x : ℝ} (hx : x ∈ I) {t : ℝ≥0} (ht : (t : ℝ) ≤ 2) :
    runner x t = min (x + t) (1 - t) := by
  simp only [runner, pathOf_apply]
  have := NNReal.coe_nonneg t
  exact Real.triangleWave_of_mem_Icc ⟨le_min (by linarith [hx.1]) (by linarith),
    (min_le_right _ _).trans (by linarith)⟩

lemma s4_leftRunner_apply {z : ℝ} (hz : z ∈ I) {t : ℝ≥0} (ht : (t : ℝ) ≤ 2) :
    leftRunner z t = max (z - t) (t - 1) := by
  simp only [leftRunner, pathOf_apply]
  have := NNReal.coe_nonneg t
  exact Real.triangleWave_of_mem_Icc ⟨(by linarith : (-1 : ℝ) ≤ t - 1).trans (le_max_right _ _),
    max_le (by linarith [hz.2]) (by linarith)⟩

lemma s4_runner_zero {x : ℝ} (hx : x ∈ I) : runner x 0 = x := by
  rw [s4_runner_apply hx (by simp)]; simp [hx.2]

lemma s4_leftRunner_zero {z : ℝ} (hz : z ∈ I) : leftRunner z 0 = z := by
  rw [s4_leftRunner_apply hz (by simp)]; simp [hz.1]

lemma s4_speed (hH : H ∈ searcherPaths) {s t : ℝ≥0} (hst : s ≤ t) :
    H t - H s ≤ t - s ∧ H s - H t ≤ t - s := by
  have h := hH.2 t s
  have hst' : (s : ℝ) ≤ t := hst
  rw [abs_of_nonneg (by linarith : (0 : ℝ) ≤ t - s)] at h
  obtain ⟨h1, h2⟩ := abs_le.mp h
  exact ⟨h2, by linarith⟩


/-! Order of two paths before they meet, and the strict intermediate value theorem. -/

/-- Before they meet, a path that starts above `H` stays above it. -/
lemma s4_lt_of_lt_captureTime {t : ℝ≥0} (h0 : H 0 ≤ S 0) (ht : (t : ℝ≥0∞) < captureTime S H) :
    H t < S t := by
  by_contra hle
  exact absurd ht (not_lt.mpr (captureTime_le_of_ge_of_ge bot_le h0 (not_lt.mp hle)))

/-- Before they meet, a path that starts below `H` stays below it. -/
lemma s4_gt_of_lt_captureTime {t : ℝ≥0} (h0 : S 0 ≤ H 0) (ht : (t : ℝ≥0∞) < captureTime S H) :
    S t < H t := by
  by_contra hle
  exact absurd ht (not_lt.mpr (captureTime_le_of_le_of_le bot_le h0 (not_lt.mp hle)))

lemma s4_eq_of_captureTime_eq {t : ℝ≥0} (h : captureTime S H = t) : S t = H t := by
  obtain ⟨t', ht', he⟩ := exists_eq_captureTime (by rw [h]; exact ENNReal.coe_ne_top)
  rw [h, ENNReal.coe_inj] at he
  rwa [he]

/-- Up to their first meeting, a path that starts above `H` stays above it. -/
lemma s4_le_of_le_captureTime {t : ℝ≥0} (h0 : H 0 ≤ S 0) (ht : (t : ℝ≥0∞) ≤ captureTime S H) :
    H t ≤ S t := by
  by_contra hlt
  replace hlt := not_le.mp hlt
  have h2 : captureTime S H = t := le_antisymm (captureTime_le_of_ge_of_ge bot_le h0 hlt.le) ht
  exact hlt.ne (s4_eq_of_captureTime_eq h2)

/-- Up to their first meeting, a path that starts below `H` stays below it. -/
lemma s4_ge_of_le_captureTime {t : ℝ≥0} (h0 : S 0 ≤ H 0) (ht : (t : ℝ≥0∞) ≤ captureTime S H) :
    S t ≤ H t := by
  by_contra hlt
  replace hlt := not_le.mp hlt
  have h2 : captureTime S H = t := le_antisymm (captureTime_le_of_le_of_le bot_le h0 hlt.le) ht
  exact hlt.ne' (s4_eq_of_captureTime_eq h2)

/-- The strict intermediate value theorem: the paths meet strictly before `t₂`. -/
lemma s4_captureTime_lt_of_le_of_lt {t₁ t₂ : ℝ≥0} (h12 : t₁ ≤ t₂) (h1 : S t₁ ≤ H t₁)
    (h2 : H t₂ < S t₂) : captureTime S H < t₂ :=
  lt_of_le_of_ne (captureTime_le_of_le_of_le h12 h1 h2.le) fun heq =>
    h2.ne' (s4_eq_of_captureTime_eq heq)

lemma s4_captureTime_lt_of_ge_of_gt {t₁ t₂ : ℝ≥0} (h12 : t₁ ≤ t₂) (h1 : H t₁ ≤ S t₁)
    (h2 : S t₂ < H t₂) : captureTime S H < t₂ :=
  lt_of_le_of_ne (captureTime_le_of_ge_of_ge h12 h1 h2.le) fun heq =>
    h2.ne (s4_eq_of_captureTime_eq heq)

/-- The capture time is `c` if the paths meet at `c`, and not during `[y, c)`, with `y ≤ T`. -/
lemma s4_captureTime_eq_of {y c : ℝ≥0} (hy : (y : ℝ≥0∞) ≤ captureTime S H)
    (hne : ∀ t : ℝ≥0, y ≤ t → t < c → S t ≠ H t) (hc : S c = H c) : captureTime S H = c := by
  refine le_antisymm (captureTime_le hc) (le_captureTime_iff.mpr fun t ht => ?_)
  by_contra hlt
  have hlt' : t < c := ENNReal.coe_lt_coe.mp (not_le.mp hlt)
  rcases lt_or_ge t y with hty | hty
  · exact absurd ((captureTime_le ht).trans_lt (ENNReal.coe_lt_coe.mpr hty)) (not_lt.mpr hy)
  · exact hne t hty hlt' ht

lemma s4_sweeperA_zero : sweeperA 0 = 1 := by
  rw [s4_sweeperA_apply (by simp)]; simp

lemma s4_negA_zero : (-sweeperA) 0 = -1 := by
  rw [s4_negA_apply (by simp)]; simp

/-- Every hider path meets a sweeper by time `1`. -/
lemma s4_sweepTime_le_one (hH : H ∈ hiderPaths) : sweepTime H ≤ 1 := by
  have hA1 : sweeperA 1 = 0 := by rw [s4_sweeperA_apply (by norm_num)]; norm_num
  have hnA1 : (-sweeperA) 1 = 0 := by rw [s4_negA_apply (by norm_num)]; norm_num
  rcases le_total 0 (H 1) with h | h
  · have := captureTime_le_of_ge_of_ge (S := sweeperA) (H := H) (zero_le_one' ℝ≥0)
      (by rw [s4_sweeperA_zero]; exact (hH 0).2) (by rw [hA1]; exact h)
    exact (min_le_left _ _).trans (by simpa using this)
  · have := captureTime_le_of_le_of_le (S := -sweeperA) (H := H) (zero_le_one' ℝ≥0)
      (by rw [s4_negA_zero]; exact (hH 0).1) (by rw [hnA1]; exact h)
    exact (min_le_right _ _).trans (by simpa using this)

/-- The facts used about a path of speed at most `1` that meets the sweeper `A` first, at `y`. -/
lemma s4_meetA (hH : H ∈ searcherPaths) {y : ℝ≥0} (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) :
    (y : ℝ) ≤ 1 ∧ H y = 1 - y ∧ (∀ t : ℝ≥0, t ≤ y → H t ≤ 1 - t) ∧
      (∀ t : ℝ≥0, t ≤ y → (t : ℝ) - 1 ≤ H t) ∧ (∀ t : ℝ≥0, t < y → H t < 1 - t) ∧
      (∀ t : ℝ≥0, t < y → (t : ℝ) - 1 < H t) := by
  have hy1 : (y : ℝ) ≤ 1 := by
    have h := s4_sweepTime_le_one (searcherPaths_subset_hiderPaths hH)
    rw [sweepTime, min_eq_left hfirst, hyA] at h
    exact_mod_cast h
  have hA0 : H 0 ≤ sweeperA 0 := by rw [s4_sweeperA_zero]; exact (hH.1 0).2
  have hnA0 : (-sweeperA) 0 ≤ H 0 := by rw [s4_negA_zero]; exact (hH.1 0).1
  refine ⟨hy1, ?_, fun t ht => ?_, fun t ht => ?_, fun t ht => ?_, fun t ht => ?_⟩
  · rw [← s4_eq_of_captureTime_eq hyA, s4_sweeperA_apply (by linarith)]
  · have ht' : (t : ℝ) ≤ y := ht
    rw [← s4_sweeperA_apply (by linarith)]
    exact s4_le_of_le_captureTime hA0 (by rw [hyA]; exact_mod_cast ht)
  · have ht' : (t : ℝ) ≤ y := ht
    rw [← s4_negA_apply (by linarith)]
    have h1 : (t : ℝ≥0∞) ≤ captureTime sweeperA H := by rw [hyA]; exact_mod_cast ht
    exact s4_ge_of_le_captureTime hnA0 (h1.trans hfirst)
  · have ht' : (t : ℝ) < y := ht
    rw [← s4_sweeperA_apply (by linarith)]
    exact s4_lt_of_lt_captureTime hA0 (by rw [hyA]; exact_mod_cast ht)
  · have ht' : (t : ℝ) < y := ht
    rw [← s4_negA_apply (by linarith)]
    have h1 : (t : ℝ≥0∞) < captureTime sweeperA H := by rw [hyA]; exact_mod_cast ht
    exact s4_gt_of_lt_captureTime hnA0 (h1.trans_le hfirst)

/-- The facts used about a path of speed at most `1` that meets the sweeper `-A` first (strictly),
at `y`. -/
lemma s4_meetNegA (hH : H ∈ searcherPaths) {y : ℝ≥0} (hyA : captureTime (-sweeperA) H = y)
    (hfirst : captureTime (-sweeperA) H < captureTime sweeperA H) :
    (y : ℝ) < 1 ∧ H y = y - 1 ∧ (∀ t : ℝ≥0, t ≤ y → H t < 1 - t) ∧
      (∀ t : ℝ≥0, t < y → (t : ℝ) - 1 < H t) := by
  have hy1 : (y : ℝ) ≤ 1 := by
    have h := s4_sweepTime_le_one (searcherPaths_subset_hiderPaths hH)
    rw [sweepTime, min_eq_right hfirst.le, hyA] at h
    exact_mod_cast h
  have hA0 : H 0 ≤ sweeperA 0 := by rw [s4_sweeperA_zero]; exact (hH.1 0).2
  have hnA0 : (-sweeperA) 0 ≤ H 0 := by rw [s4_negA_zero]; exact (hH.1 0).1
  have hHy : H y = y - 1 := by rw [← s4_eq_of_captureTime_eq hyA, s4_negA_apply (by linarith)]
  have hlt : ∀ t : ℝ≥0, t ≤ y → H t < 1 - t := fun t ht => by
    have ht' : (t : ℝ) ≤ y := ht
    rw [← s4_sweeperA_apply (by linarith)]
    have h1 : (t : ℝ≥0∞) ≤ captureTime (-sweeperA) H := by rw [hyA]; exact_mod_cast ht
    exact s4_lt_of_lt_captureTime hA0 (h1.trans_lt hfirst)
  refine ⟨lt_of_le_of_ne hy1 fun h1 => ?_, hHy, hlt, fun t ht => ?_⟩
  · have := hlt y le_rfl
    rw [hHy, h1] at this
    norm_num at this
  · have ht' : (t : ℝ) < y := ht
    rw [← s4_negA_apply (by linarith)]
    exact s4_gt_of_lt_captureTime hnA0 (by rw [hyA]; exact_mod_cast ht)

end Helpers

/-- **Lemma 11** (`lem:11`). Let `H` be a hider path of speed at most `1` and `y` the first
time it meets a sweeper. A searcher of `s_Φ` finds `H` before time `y` if and only if he starts
in `(H(y) - y, H(0)]` and runs right, or starts in `[H(0), H(y) + y)` and runs left. The starting
points `H(y) - y` and `H(y) + y` are excluded: there the paper's statement can fail.

Proof (as repaired in the plan): the two cases, `H` meets `A` first (`H(y) = 1 - y`) and `H`
meets `-A` first (`H(y) = y - 1`), are treated directly; the paper's reduction to `H ≥ 0` by
Proposition 8 does not apply to a single pure path. In each case the runners are compared with
`H` and the sweepers, using the intermediate value theorem and the speed bound on `H`. -/
theorem lemma11 {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hy : sweepTime H = y) {x : ℝ} (hx : x ∈ I) (hx₁ : x ≠ H y - y) (hx₂ : x ≠ H y + y) :
    (captureTime (runner x) H < y ↔ x ∈ Set.Ioc (H y - y) (H 0)) ∧
      (captureTime (leftRunner x) H < y ↔ x ∈ Set.Ico (H 0) (H y + y)) := by
  have hmeet : ∀ {S : C(ℝ≥0, ℝ)}, captureTime S H < y → ∃ t : ℝ≥0, t < y ∧ S t = H t := by
    intro S hS
    obtain ⟨t, ht, he⟩ := exists_eq_captureTime hS.ne_top
    exact ⟨t, by rw [he] at hS; exact_mod_cast hS, ht⟩
  have hR0 := s4_runner_zero hx
  have hL0 := s4_leftRunner_zero hx
  have h0t : ∀ t : ℝ≥0, H t - H 0 ≤ t ∧ H 0 - H t ≤ t := fun t => by
    simpa using s4_speed hH (bot_le : (0 : ℝ≥0) ≤ t)
  rcases le_or_gt (captureTime sweeperA H) (captureTime (-sweeperA) H) with hfirst | hfirst
  · -- `H` meets `A` first: `H(y) = 1 - y`
    have hyA : captureTime sweeperA H = y := by rw [← hy, sweepTime, min_eq_left hfirst]
    obtain ⟨hy1, hHy, -, -, hlt, hgt⟩ := s4_meetA hH hyA hfirst
    rw [hHy] at hx₁ hx₂ ⊢
    refine ⟨⟨fun hT => ?_, fun hxE => ?_⟩, ⟨fun hT => ?_, fun hxE => ?_⟩⟩
    · -- a right runner that catches `H` before `y` starts in `(1 - 2y, H(0)]`
      obtain ⟨t, hty, hmt⟩ := hmeet hT
      have hty' : (t : ℝ) < y := hty
      rw [s4_runner_apply hx (by linarith)] at hmt
      have hsp := (s4_speed hH hty.le).1
      rw [hHy] at hsp
      have hlt' := hlt t hty
      have h0 := (h0t t).1
      constructor
      · by_contra hcon
        have : x < 1 - y - y := lt_of_le_of_ne (not_lt.mp hcon) hx₁
        have := min_le_left (x + (t : ℝ)) (1 - t)
        linarith
      · by_contra hcon
        have hcon := not_le.mp hcon
        rcases min_choice (x + (t : ℝ)) (1 - t) with h | h <;> rw [h] at hmt <;> linarith
    · -- a right runner starting in `(1 - 2y, H(0)]` meets `A` at `(1 - x)/2 < y`, above `H`
      obtain ⟨h1, h2⟩ := hxE
      obtain ⟨τ, hτ⟩ : ∃ τ : ℝ≥0, (τ : ℝ) = (1 - x) / 2 :=
        ⟨⟨(1 - x) / 2, by linarith [hx.2]⟩, rfl⟩
      have hτy : τ < y := by rw [← NNReal.coe_lt_coe, hτ]; linarith
      refine (s4_captureTime_lt_of_le_of_lt (t₂ := τ) zero_le (by rw [hR0]; exact h2) ?_).trans
        (ENNReal.coe_lt_coe.mpr hτy)
      have := hlt τ hτy
      rw [s4_runner_apply hx (by rw [hτ]; linarith [hx.1]), hτ, min_eq_right (by linarith)]
      rw [hτ] at this
      exact this
    · -- a left runner that catches `H` before `y` starts in `[H(0), 1)`
      obtain ⟨t, hty, hmt⟩ := hmeet hT
      have hty' : (t : ℝ) < y := hty
      rw [s4_leftRunner_apply hx (by linarith)] at hmt
      have hgt' := hgt t hty
      have h0 := (h0t t).2
      constructor
      · by_contra hcon
        have hcon := not_le.mp hcon
        rcases max_choice (x - (t : ℝ)) (t - 1) with h | h <;> rw [h] at hmt <;> linarith
      · exact lt_of_le_of_ne (by linarith [hx.2]) hx₂
    · -- a left runner starting in `[H(0), 1)` crosses `H` before `y`
      obtain ⟨h1, h2⟩ := hxE
      obtain ⟨τ, hτ⟩ : ∃ τ : ℝ≥0, (τ : ℝ) = (1 + x) / 2 :=
        ⟨⟨(1 + x) / 2, by linarith [hx.1]⟩, rfl⟩
      rcases lt_or_ge τ y with hτy | hτy
      · -- it joins `-A` at time `(1 + x)/2 < y`, below `H`
        have hτy' : (τ : ℝ) < y := hτy
        refine (s4_captureTime_lt_of_ge_of_gt (t₂ := τ) zero_le (by rw [hL0]; exact h1) ?_).trans
          (ENNReal.coe_lt_coe.mpr hτy)
        rw [s4_leftRunner_apply hx (by linarith), max_eq_right (by linarith)]
        exact hgt τ hτy
      · -- it is below `H` at time `y`
        have hτy' : (y : ℝ) ≤ τ := hτy
        refine s4_captureTime_lt_of_ge_of_gt zero_le (by rw [hL0]; exact h1) ?_
        rw [s4_leftRunner_apply hx (by linarith), max_eq_left (by linarith), hHy]
        linarith
  · -- `H` meets `-A` first: `H(y) = y - 1`
    have hyA : captureTime (-sweeperA) H = y := by rw [← hy, sweepTime, min_eq_right hfirst.le]
    obtain ⟨hy1, hHy, hlt, hgt⟩ := s4_meetNegA hH hyA hfirst
    rw [hHy] at hx₁ hx₂ ⊢
    refine ⟨⟨fun hT => ?_, fun hxE => ?_⟩, ⟨fun hT => ?_, fun hxE => ?_⟩⟩
    · -- a right runner that catches `H` before `y` starts in `(-1, H(0)]`
      obtain ⟨t, hty, hmt⟩ := hmeet hT
      have hty' : (t : ℝ) < y := hty
      rw [s4_runner_apply hx (by linarith)] at hmt
      have hlt' := hlt t hty.le
      have h0 := (h0t t).1
      constructor
      · exact lt_of_le_of_ne (by linarith [hx.1]) (fun h => hx₁ h.symm)
      · by_contra hcon
        have hcon := not_le.mp hcon
        rcases min_choice (x + (t : ℝ)) (1 - t) with h | h <;> rw [h] at hmt <;> linarith
    · -- a right runner starting in `(-1, H(0)]` is above `H` at time `y`
      obtain ⟨h1, h2⟩ := hxE
      refine s4_captureTime_lt_of_le_of_lt zero_le (by rw [hR0]; exact h2) ?_
      rw [s4_runner_apply hx (by linarith), hHy]
      exact lt_min (by linarith) (by linarith)
    · -- a left runner that catches `H` before `y` starts in `[H(0), 2y - 1)`
      obtain ⟨t, hty, hmt⟩ := hmeet hT
      have hty' : (t : ℝ) < y := hty
      rw [s4_leftRunner_apply hx (by linarith)] at hmt
      have hsp := (s4_speed hH hty.le).2
      rw [hHy] at hsp
      have hgt' := hgt t hty
      have h0 := (h0t t).2
      constructor
      · by_contra hcon
        have hcon := not_le.mp hcon
        rcases max_choice (x - (t : ℝ)) (t - 1) with h | h <;> rw [h] at hmt <;> linarith
      · by_contra hcon
        have : y - 1 + y < x := lt_of_le_of_ne (not_lt.mp hcon) (fun h => hx₂ h.symm)
        have := le_max_left (x - (t : ℝ)) (t - 1)
        linarith
    · -- a left runner starting in `[H(0), 2y - 1)` meets `-A` at `(1 + x)/2 < y`, below `H`
      obtain ⟨h1, h2⟩ := hxE
      obtain ⟨τ, hτ⟩ : ∃ τ : ℝ≥0, (τ : ℝ) = (1 + x) / 2 :=
        ⟨⟨(1 + x) / 2, by linarith [hx.1]⟩, rfl⟩
      have hτy : τ < y := by rw [← NNReal.coe_lt_coe, hτ]; linarith
      refine (s4_captureTime_lt_of_ge_of_gt (t₂ := τ) zero_le (by rw [hL0]; exact h1) ?_).trans
        (ENNReal.coe_lt_coe.mpr hτy)
      have := hgt τ hτy
      rw [s4_leftRunner_apply hx (by rw [hτ]; linarith [hx.2]), hτ, max_eq_right (by linarith)]
      rw [hτ] at this
      exact this

/-! ### The layer-cake identity (Lemma 13') -/

section Layer

variable {H : C(ℝ≥0, ℝ)}

lemma s4_continuous_realPath (H : C(ℝ≥0, ℝ)) : Continuous (realPath H) :=
  H.continuous.comp continuous_real_toNNReal

lemma s4_realPath_coe (H : C(ℝ≥0, ℝ)) (t : ℝ≥0) : realPath H t = H t := by
  simp [realPath]

lemma s4_realPath_zero (H : C(ℝ≥0, ℝ)) : realPath H 0 = H 0 := by
  simp [realPath]

lemma s4_realPath_lip (hH : H ∈ searcherPaths) (s t : ℝ) :
    |realPath H t - realPath H s| ≤ |t - s| := by
  refine (hH.2 t.toNNReal s.toNNReal).trans ?_
  rw [Real.coe_toNNReal', Real.coe_toNNReal']
  exact (abs_max_sub_max_le_max t 0 s 0).trans (by simp)

/-- `g(t) = H(t) - t` is nonincreasing. -/
lemma s4_antitone_g (hH : H ∈ searcherPaths) : Antitone fun t => realPath H t - t := by
  intro s t hst
  have h := s4_realPath_lip hH s t
  rw [abs_of_nonneg (sub_nonneg.mpr hst)] at h
  have := (abs_le.mp h).2
  simp only
  linarith

/-- `g₂(t) = H(t) + t` is nondecreasing. -/
lemma s4_monotone_g₂ (hH : H ∈ searcherPaths) : Monotone fun t => realPath H t + t := by
  intro s t hst
  have h := s4_realPath_lip hH s t
  rw [abs_of_nonneg (sub_nonneg.mpr hst)] at h
  have := (abs_le.mp h).1
  simp only
  linarith

/-- A right runner starting in `(H(y) - y, H(0)]` has not caught `H` by time `σ` if and only if
`x < H(σ) - σ`. -/
lemma s4_runner_lt_captureTime_iff (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H)
    {x : ℝ} (hx : x ∈ Set.Ioc (H y - y) (H 0)) (σ : ℝ≥0) :
    (σ : ℝ≥0∞) < captureTime (runner x) H ↔ x < H σ - σ := by
  obtain ⟨hy1, hHy, hle, -, -, -⟩ := s4_meetA hH hyA hfirst
  have hxI : x ∈ I := ⟨by linarith [hx.1], hx.2.trans (hH.1 0).2⟩
  constructor
  · intro h
    by_contra hcon
    replace hcon := not_lt.mp hcon
    have key : ∀ t : ℝ≥0, t ≤ y → H t - t ≤ x → captureTime (runner x) H ≤ t := by
      intro t hty hxt
      have hty' : (t : ℝ) ≤ y := hty
      refine captureTime_le_of_le_of_le zero_le (by rw [s4_runner_zero hxI]; exact hx.2) ?_
      rw [s4_runner_apply hxI (by linarith)]
      exact le_min (by linarith) (hle t hty)
    rcases le_total σ y with hσy | hσy
    · exact absurd h (not_lt.mpr (key σ hσy hcon))
    · exact absurd h (not_lt.mpr ((key y le_rfl hx.1.le).trans (ENNReal.coe_le_coe.mpr hσy)))
  · intro h
    rw [s4_lt_captureTime_iff]
    intro t ht heq
    have hσy : (σ : ℝ) < y := by
      by_contra hcon
      have := (s4_speed hH (show y ≤ σ from not_lt.mp hcon)).1
      linarith [hx.1]
    have ht' : (t : ℝ) ≤ σ := ht
    have := (s4_speed hH ht).1
    rw [s4_runner_apply hxI (by linarith)] at heq
    have := min_le_left (x + (t : ℝ)) (1 - t)
    linarith

/-- A left runner starting in `[H(0), H(y) + y)` has not caught `H` by time `σ` if and only if
`H(σ) + σ < z`. -/
lemma s4_leftRunner_lt_captureTime_iff (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H)
    {z : ℝ} (hz : z ∈ Set.Ico (H 0) (H y + y)) (σ : ℝ≥0) :
    (σ : ℝ≥0∞) < captureTime (leftRunner z) H ↔ H σ + σ < z := by
  obtain ⟨hy1, hHy, -, hge, -, -⟩ := s4_meetA hH hyA hfirst
  have hzI : z ∈ I := ⟨(hH.1 0).1.trans hz.1, by linarith [hz.2]⟩
  constructor
  · intro h
    by_contra hcon
    replace hcon := not_lt.mp hcon
    have key : ∀ t : ℝ≥0, t ≤ y → z ≤ H t + t → captureTime (leftRunner z) H ≤ t := by
      intro t hty hzt
      have hty' : (t : ℝ) ≤ y := hty
      refine captureTime_le_of_ge_of_ge zero_le (by rw [s4_leftRunner_zero hzI]; exact hz.1) ?_
      rw [s4_leftRunner_apply hzI (by linarith)]
      exact max_le (by linarith) (hge t hty)
    rcases le_total σ y with hσy | hσy
    · exact absurd h (not_lt.mpr (key σ hσy hcon))
    · exact absurd h (not_lt.mpr ((key y le_rfl hz.2.le).trans (ENNReal.coe_le_coe.mpr hσy)))
  · intro h
    rw [s4_lt_captureTime_iff]
    intro t ht heq
    have hσy : (σ : ℝ) < y := by
      by_contra hcon
      have := (s4_speed hH (show y ≤ σ from not_lt.mp hcon)).2
      linarith [hz.2]
    have ht' : (t : ℝ) ≤ σ := ht
    have := (s4_speed hH ht).2
    rw [s4_leftRunner_apply hzI (by linarith)] at heq
    have := le_max_left (z - (t : ℝ)) (t - 1)
    linarith

/-- The layer-cake identity for the right runners, for any measure `ν` of the starting point. -/
lemma s4_layer_right (ν : Measure ℝ) (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) :
    ∫⁻ x in Set.Ioc (H y - y) (H 0), captureTime (runner x) H ∂ν =
      ∫⁻ s in Set.Ioi 0, ν (Set.Ioo (H y - y) (realPath H s - s)) := by
  have hiff := fun {x} => s4_runner_lt_captureTime_iff hH hyA hfirst (x := x)
  have hfin : ∀ x ∈ Set.Ioc (H y - y) (H 0), captureTime (runner x) H ≠ ⊤ := by
    intro x hx htop
    have := (hiff hx y).mp (by rw [htop]; exact ENNReal.coe_lt_top)
    linarith [hx.1]
  rw [setLIntegral_congr_fun measurableSet_Ioc
      (fun x hx => (ENNReal.ofReal_toReal (hfin x hx)).symm),
    lintegral_eq_lintegral_meas_lt _ (ae_of_all _ fun _ => ENNReal.toReal_nonneg)
      (ENNReal.measurable_toReal.comp (s4_measurable_captureTime_runner H)).aemeasurable]
  refine setLIntegral_congr_fun measurableSet_Ioi fun s hs => ?_
  have hs0 : (0 : ℝ) ≤ s := le_of_lt hs
  have hgs : realPath H s - s ≤ H 0 := by
    have := s4_antitone_g hH hs0
    simp only [sub_zero, s4_realPath_zero] at this
    exact this
  have key : ∀ x ∈ Set.Ioc (H y - y) (H 0),
      (s < (captureTime (runner x) H).toReal ↔ x < realPath H s - s) := by
    intro x hx
    rw [← ENNReal.ofReal_lt_iff_lt_toReal hs0 (hfin x hx)]
    have := hiff hx s.toNNReal
    rw [Real.coe_toNNReal s hs0] at this
    exact this
  rw [Measure.restrict_apply' measurableSet_Ioc]
  congr 1
  ext x
  simp only [Set.mem_inter_iff, Set.mem_ofPred_eq, Set.mem_Ioo]
  constructor
  · rintro ⟨h1, hx⟩
    exact ⟨hx.1, (key x hx).mp h1⟩
  · rintro ⟨h1, h2⟩
    have hx : x ∈ Set.Ioc (H y - y) (H 0) := ⟨h1, (h2.trans_le hgs).le⟩
    exact ⟨(key x hx).mpr h2, hx⟩

/-- The layer-cake identity for the left runners, for any measure `ν` of the starting point. -/
lemma s4_layer_left (ν : Measure ℝ) (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) :
    ∫⁻ z in Set.Ico (H 0) (H y + y), captureTime (leftRunner z) H ∂ν =
      ∫⁻ s in Set.Ioi 0, ν (Set.Ioo (realPath H s + s) (H y + y)) := by
  have hiff := fun {z} => s4_leftRunner_lt_captureTime_iff hH hyA hfirst (z := z)
  have hfin : ∀ z ∈ Set.Ico (H 0) (H y + y), captureTime (leftRunner z) H ≠ ⊤ := by
    intro z hz htop
    have := (hiff hz y).mp (by rw [htop]; exact ENNReal.coe_lt_top)
    linarith [hz.2]
  rw [setLIntegral_congr_fun measurableSet_Ico
      (fun z hz => (ENNReal.ofReal_toReal (hfin z hz)).symm),
    lintegral_eq_lintegral_meas_lt _ (ae_of_all _ fun _ => ENNReal.toReal_nonneg)
      (ENNReal.measurable_toReal.comp (s4_measurable_captureTime_leftRunner H)).aemeasurable]
  refine setLIntegral_congr_fun measurableSet_Ioi fun s hs => ?_
  have hs0 : (0 : ℝ) ≤ s := le_of_lt hs
  have hgs : H 0 ≤ realPath H s + s := by
    have := s4_monotone_g₂ hH hs0
    simp only [add_zero, s4_realPath_zero] at this
    exact this
  have key : ∀ z ∈ Set.Ico (H 0) (H y + y),
      (s < (captureTime (leftRunner z) H).toReal ↔ realPath H s + s < z) := by
    intro z hz
    rw [← ENNReal.ofReal_lt_iff_lt_toReal hs0 (hfin z hz)]
    have := hiff hz s.toNNReal
    rw [Real.coe_toNNReal s hs0] at this
    exact this
  rw [Measure.restrict_apply' measurableSet_Ico]
  congr 1
  ext z
  simp only [Set.mem_inter_iff, Set.mem_ofPred_eq, Set.mem_Ioo]
  constructor
  · rintro ⟨h1, hz⟩
    exact ⟨(key z hz).mp h1, hz.2⟩
  · rintro ⟨h1, h2⟩
    have hz : z ∈ Set.Ico (H 0) (H y + y) := ⟨hgs.trans h1.le, h2⟩
    exact ⟨(key z hz).mpr h1, hz⟩

/-- Turning `∫⁻ s > 0, F s` into a real integral over `(0, y)`. -/
lemma s4_lintegral_Ioi_eq {F : ℝ → ℝ≥0∞} {φ : ℝ → ℝ} {y : ℝ} (hy : 0 ≤ y)
    (hF0 : ∀ s, y ≤ s → F s = 0) (hFφ : ∀ s ∈ Set.Ioo 0 y, F s = ENNReal.ofReal (φ s))
    (hφ0 : ∀ s ∈ Set.Ioo 0 y, 0 ≤ φ s) (hφi : IntervalIntegrable φ volume 0 y) :
    ∫⁻ s in Set.Ioi 0, F s = ENNReal.ofReal (∫ s in (0 : ℝ)..y, φ s) := by
  rw [← lintegral_inter_add_sdiff F (Set.Ioi 0) (measurableSet_Iio (a := y)), Set.Ioi_inter_Iio]
  have h2 : ∫⁻ s in Set.Ioi 0 \ Set.Iio y, F s = 0 := by
    rw [setLIntegral_congr_fun (measurableSet_Ioi.diff measurableSet_Iio) (g := fun _ => 0)
      (fun s hs => hF0 s (not_lt.mp hs.2))]
    simp
  rw [h2, add_zero, setLIntegral_congr_fun measurableSet_Ioo hFφ,
    intervalIntegral.integral_of_le hy, integral_Ioc_eq_integral_Ioo,
    ofReal_integral_eq_lintegral_ofReal (hφi.1.mono_set Set.Ioo_subset_Ioc_self)
      ((ae_restrict_iff' measurableSet_Ioo).mpr (ae_of_all _ hφ0))]

end Layer

/-! ### Distribution functions -/

section Cdf

variable (μ : Measure ℝ)

lemma s4_cdf_mono [IsFiniteMeasure μ] : Monotone (cdf μ) := fun _ _ hab =>
  ENNReal.toReal_mono (measure_ne_top _ _) (measure_mono (Set.Iic_subset_Iic.mpr hab))

lemma s4_cdf_nonneg (a : ℝ) : 0 ≤ cdf μ a := ENNReal.toReal_nonneg

lemma s4_cdf_le_one [IsProbabilityMeasure μ] (a : ℝ) : cdf μ a ≤ 1 :=
  ENNReal.toReal_le_of_le_ofReal zero_le_one (by rw [ENNReal.ofReal_one]; exact prob_le_one)

lemma s4_measure_Iic [IsFiniteMeasure μ] (a : ℝ) :
    μ (Set.Iic a) = ENNReal.ofReal (cdf μ a) :=
  (ENNReal.ofReal_toReal (measure_ne_top _ _)).symm

lemma s4_measure_Ioi [IsProbabilityMeasure μ] (a : ℝ) :
    μ (Set.Ioi a) = ENNReal.ofReal (1 - cdf μ a) := by
  rw [← Set.compl_Iic, prob_compl_eq_one_sub measurableSet_Iic, s4_measure_Iic,
    ENNReal.ofReal_sub _ (s4_cdf_nonneg _ _), ENNReal.ofReal_one]

lemma s4_measure_Ioo [IsFiniteMeasure μ] [NullSingletonClass μ] {a b : ℝ} (hab : a ≤ b) :
    μ (Set.Ioo a b) = ENNReal.ofReal (cdf μ b - cdf μ a) := by
  have h : μ (Set.Iic b) = μ (Set.Iic a) + μ (Set.Ioc a b) := by
    rw [← measure_union (Set.Iic_disjoint_Ioc le_rfl) measurableSet_Ioc,
      Set.Iic_union_Ioc_eq_Iic hab]
  have h' : cdf μ b = cdf μ a + (μ (Set.Ioc a b)).toReal := by
    rw [cdf, cdf, h, ENNReal.toReal_add (measure_ne_top _ _) (measure_ne_top _ _)]
  rw [measure_congr Ioo_ae_eq_Ioc, h', add_sub_cancel_left,
    ENNReal.ofReal_toReal (measure_ne_top _ _)]

lemma s4_measure_Iic_neg_one [NullSingletonClass μ] (hμ : μ Iᶜ = 0) : μ (Set.Iic (-1)) = 0 := by
  refine measure_mono_null (t := Iᶜ ∪ {-1}) (fun x hx => ?_) ?_
  · rcases (Set.mem_Iic.mp hx).lt_or_eq with h | h
    · exact Or.inl fun hI => absurd hI.1 (not_le.mpr h)
    · exact Or.inr h
  · exact measure_union_null hμ (measure_singleton _)

lemma s4_cdf_neg_one [NullSingletonClass μ] (hμ : μ Iᶜ = 0) : cdf μ (-1) = 0 := by
  rw [cdf, s4_measure_Iic_neg_one μ hμ, ENNReal.toReal_zero]

end Cdf

/-- **Lemma 13'** (`lem:13`): Lemmas 12 and 13 combined, for paths of speed at most `1` (Lipschitz
paths, with no smoothness assumption) and any atomless distribution `μ` of the starting point on
`[-1, 1]`, with distribution function `Φ`. Let `H` meet the sweeper `A` first, at time `y`. The
right runners starting in `(H(y) - y, H(0)]` contribute `∫₀^y (Φ(H(t) - t) - Φ(1 - 2y)) dt` to the
expected capture time (`(5)` after the integration by parts of Lemma 13), and the left runners
starting in `[H(0), H(y) + y)` contribute `∫₀^y Φ(-H(t) - t) dt` (`(6)` after it). The proof is the
layer-cake identity `E[T] = ∫₀^∞ P(T > s) ds`: a right runner starting at `x` has not caught `H` by
time `s` if and only if `x < H(s) - s`. -/
theorem s4_lemma13' (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ]
    (hμ : μ Iᶜ = 0) {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) :
    (∫⁻ x in Set.Ioc (H y - y) (H 0), captureTime (runner x) H ∂μ =
      ENNReal.ofReal (∫ t in (0 : ℝ)..y, (cdf μ (realPath H t - t) - cdf μ (1 - 2 * y)))) ∧
    (∫⁻ x in Set.Ioc (-(H y + y)) (-H 0), captureTime (leftRunner (-x)) H ∂μ =
      ENNReal.ofReal (∫ t in (0 : ℝ)..y, cdf μ (-realPath H t - t))) := by
  obtain ⟨hy1, hHy, -⟩ := s4_meetA hH hyA hfirst
  have hgy : realPath H y - y = 1 - 2 * y := by rw [s4_realPath_coe, hHy]; ring
  have hg₂y : realPath H y + y = 1 := by rw [s4_realPath_coe, hHy]; ring
  have hanti := s4_antitone_g hH
  have hmono := s4_monotone_g₂ hH
  have hΦ := s4_cdf_mono μ
  constructor
  · rw [s4_layer_right μ hH hyA hfirst]
    refine s4_lintegral_Ioi_eq y.coe_nonneg (fun s hs => ?_) (fun s hs => ?_) (fun s hs => ?_) ?_
    · have := hanti hs
      simp only at this
      rw [Set.Ioo_eq_empty_of_le (by rw [← s4_realPath_coe]; exact this), measure_empty]
    · have hgs : 1 - 2 * (y : ℝ) ≤ realPath H s - s := by rw [← hgy]; exact hanti hs.2.le
      rw [hHy, show (1 : ℝ) - y - y = 1 - 2 * y by ring]
      exact s4_measure_Ioo μ hgs
    · exact sub_nonneg.mpr (hΦ (by rw [← hgy]; exact hanti hs.2.le))
    · exact (hΦ.comp_antitone hanti).intervalIntegrable.sub intervalIntegrable_const
  · have hpre : Neg.neg ⁻¹' Set.Ico (H 0) (H y + y) = Set.Ioc (-(H y + y)) (-H 0) := by
      rw [← Set.neg_Ico]; rfl
    have hmap : ∫⁻ x in Set.Ioc (-(H y + y)) (-H 0), captureTime (leftRunner (-x)) H ∂μ =
        ∫⁻ z in Set.Ico (H 0) (H y + y), captureTime (leftRunner z) H ∂(μ.map Neg.neg) := by
      rw [Measure.restrict_map measurable_neg measurableSet_Ico, hpre,
        lintegral_map (s4_measurable_captureTime_leftRunner H) measurable_neg]
    have hanti₂ : Antitone fun t => -realPath H t - t := fun s t hst => by
      have := hmono hst
      simp only at this ⊢
      linarith
    rw [hmap, s4_layer_left _ hH hyA hfirst]
    refine s4_lintegral_Ioi_eq y.coe_nonneg (fun s hs => ?_) (fun s hs => ?_)
      (fun s _ => s4_cdf_nonneg μ _) (hΦ.comp_antitone hanti₂).intervalIntegrable
    · have := hmono hs
      simp only at this
      rw [Set.Ioo_eq_empty_of_le (by rw [← s4_realPath_coe]; exact this), measure_empty]
    · have hgs : realPath H s + s ≤ H y + y := by rw [← s4_realPath_coe]; exact hmono hs.2.le
      rw [Measure.map_apply measurable_neg measurableSet_Ioo]
      change μ (-Set.Ioo _ _) = _
      rw [Set.neg_Ioo, s4_measure_Ioo μ (neg_le_neg hgs), ← s4_realPath_coe, hg₂y,
        s4_cdf_neg_one μ hμ, sub_zero, neg_add']

/-! ### Lemmas 12 and 13: integration by parts -/

/-- The derivative of a `C¹` function on `[0, y]` is integrable on `[0, y]`. -/
lemma s4_intervalIntegrable_deriv {h : ℝ → ℝ} {y : ℝ} (hy : 0 ≤ y)
    (hh : ContDiffOn ℝ 1 h (Set.Icc 0 y)) : IntervalIntegrable (deriv h) volume 0 y := by
  rcases hy.eq_or_lt with rfl | hy'
  · exact IntervalIntegrable.refl
  · have hc : ContinuousOn (derivWithin h (Set.Icc 0 y)) (Set.Icc 0 y) :=
      hh.continuousOn_derivWithin (uniqueDiffOn_Icc hy') le_rfl
    refine (hc.intervalIntegrable_of_Icc hy).congr_uIoo fun t ht => ?_
    rw [Set.uIoo_of_le hy] at ht
    exact derivWithin_of_mem_nhds (Icc_mem_nhds ht.1 ht.2)

/-- Integration by parts in the form used for (5) and (6):
`∫₀^y ∫_{g(y)}^{g(s)} k ds = -∫₀^y t k(g(t)) g'(t) dt`. -/
lemma s4_ibp_layer {k g g' : ℝ → ℝ} (hk : Continuous k) {y : ℝ} (hy : 0 ≤ y)
    (hg : Continuous g) (hgd : ∀ t ∈ Set.Ioo 0 y, HasDerivAt g (g' t) t)
    (hg' : IntervalIntegrable g' volume 0 y) :
    ∫ s in (0 : ℝ)..y, (∫ x in g y..g s, k x) = -∫ t in (0 : ℝ)..y, t * (k (g t) * g' t) := by
  have hG : ∀ u, HasDerivAt (fun u => ∫ x in g y..u, k x) (k u) u := fun u =>
    (hk.integral_hasStrictDerivAt (g y) u).hasDerivAt
  have hvc : Continuous fun s => ∫ x in g y..g s, k x :=
    (continuous_iff_continuousAt.mpr fun u => (hG u).continuousAt).comp hg
  have hv : ∀ t ∈ Set.Ioo (min 0 y) (max 0 y),
      HasDerivAt (fun s => ∫ x in g y..g s, k x) (k (g t) * g' t) t := by
    intro t ht
    rw [min_eq_left hy, max_eq_right hy] at ht
    exact (hG (g t)).comp t (hgd t ht)
  have h := intervalIntegral.integral_mul_deriv_eq_deriv_mul_of_hasDerivAt
    (u := fun t => t) (u' := fun _ => 1) continuousOn_id hvc.continuousOn
    (fun t _ => hasDerivAt_id' t) hv intervalIntegrable_const
    (hg'.continuousOn_mul (hk.comp hg).continuousOn)
  simp only [intervalIntegral.integral_same, mul_zero, zero_mul, sub_zero, one_mul] at h
  linarith

/-- The mass of an interval under a continuous density. -/
lemma s4_withDensity_Ioo {k : ℝ → ℝ} (hk : Continuous k) (hk0 : ∀ x, 0 ≤ k x) {a b : ℝ}
    (hab : a ≤ b) :
    (volume.withDensity fun x => ENNReal.ofReal (k x)) (Set.Ioo a b) =
      ENNReal.ofReal (∫ x in a..b, k x) := by
  rw [withDensity_apply _ measurableSet_Ioo, intervalIntegral.integral_of_le hab,
    integral_Ioc_eq_integral_Ioo,
    ofReal_integral_eq_lintegral_ofReal (hk.integrableOn_Icc.mono_set Set.Ioo_subset_Icc_self)
      (ae_of_all _ fun x => hk0 x)]

/-- **Lemma 12** (`lem:12`). Let the starting point of `s_Φ` have a continuous density `f`, and
let `H` be a smooth hider path of speed at most `1` that meets the sweeper `A` first, at time
`y`. The right runners starting in `(H(y) - y, H(0)]` catch `H` with expected time (5), and the
left runners starting in `[H(0), H(y) + y)` (whose starting points have density `f(-x)`) with
expected time (6).

Proof: the layer-cake identity of Lemma 13' (for the measure with density `f`, a right runner
starting at `x` has not caught `H` by time `s` iff `x < H(s) - s`) followed by an integration by
parts, which is the paper's Lemma 13 read backwards; this replaces the paper's first-order
argument on `[t, t + Δt]`. -/
theorem lemma12 {f : ℝ → ℝ} (hf : Continuous f) (hf0 : ∀ x, 0 ≤ f x)
    {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y) (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H)
    (hsmooth : ContDiffOn ℝ 1 (realPath H) (Set.Icc 0 y)) :
    (∫⁻ x in Set.Ioc (H y - y) (H 0), captureTime (runner x) H
        ∂(volume.withDensity fun x => ENNReal.ofReal (f x))) =
      ENNReal.ofReal (∫ t in (0 : ℝ)..y,
        t * f (realPath H t - t) * (1 - deriv (realPath H) t)) ∧
    (∫⁻ x in Set.Ico (H 0) (H y + y), captureTime (leftRunner x) H
        ∂(volume.withDensity fun x => ENNReal.ofReal (f (-x)))) =
      ENNReal.ofReal (∫ t in (0 : ℝ)..y,
        t * f (-realPath H t - t) * (1 + deriv (realPath H) t)) := by
  have hy0 := y.coe_nonneg
  have hcont := s4_continuous_realPath H
  have hanti := s4_antitone_g hH
  have hmono := s4_monotone_g₂ hH
  have hd : ∀ t ∈ Set.Ioo (0 : ℝ) y, HasDerivAt (realPath H) (deriv (realPath H) t) t :=
    fun t ht => ((hsmooth.differentiableOn one_ne_zero).differentiableAt
      (Icc_mem_nhds ht.1 ht.2)).hasDerivAt
  have hdi := s4_intervalIntegrable_deriv hy0 hsmooth
  constructor
  · -- right runners: `g(t) = H(t) - t`
    have hgy : realPath H y - y = H y - y := by rw [s4_realPath_coe]
    have h0 : ∀ s : ℝ, (y : ℝ) ≤ s →
        (volume.withDensity fun x => ENNReal.ofReal (f x))
          (Set.Ioo (H y - y) (realPath H s - s)) = 0 := fun s hs => by
      have := hanti hs
      simp only at this
      rw [Set.Ioo_eq_empty_of_le (by rw [← hgy]; exact this), measure_empty]
    have hFφ : ∀ s ∈ Set.Ioo (0 : ℝ) y,
        (volume.withDensity fun x => ENNReal.ofReal (f x))
          (Set.Ioo (H y - y) (realPath H s - s)) =
        ENNReal.ofReal (∫ x in (realPath H y - y)..(realPath H s - s), f x) := fun s hs => by
      rw [← hgy]
      exact s4_withDensity_Ioo hf hf0 (hanti hs.2.le)
    have hφ0 : ∀ s ∈ Set.Ioo (0 : ℝ) y,
        0 ≤ ∫ x in (realPath H y - y)..(realPath H s - s), f x := fun s hs =>
      intervalIntegral.integral_nonneg (hanti hs.2.le) fun x _ => hf0 x
    have hφi : IntervalIntegrable
        (fun s => ∫ x in (realPath H y - y)..(realPath H s - s), f x) volume 0 y := by
      have hG : Continuous fun u => ∫ x in (realPath H y - y)..u, f x :=
        continuous_iff_continuousAt.mpr fun u =>
          (hf.integral_hasStrictDerivAt _ u).hasDerivAt.continuousAt
      exact (hG.comp (hcont.sub continuous_id)).intervalIntegrable _ _
    rw [s4_layer_right _ hH hyA hfirst, s4_lintegral_Ioi_eq hy0 h0 hFφ hφ0 hφi,
      s4_ibp_layer (g := fun t => realPath H t - t) hf hy0 (hcont.sub continuous_id)
        (fun t ht => (hd t ht).sub (hasDerivAt_id' t)) (hdi.sub intervalIntegrable_const),
      ← intervalIntegral.integral_neg]
    congr 1
    congr 1
    ext t
    ring
  · -- left runners: `g₂(t) = H(t) + t`, density `f(-x)`
    have hgy : realPath H y + y = H y + y := by rw [s4_realPath_coe]
    have hk : Continuous fun x => f (-x) := hf.comp continuous_neg
    have h0 : ∀ s : ℝ, (y : ℝ) ≤ s →
        (volume.withDensity fun x => ENNReal.ofReal (f (-x)))
          (Set.Ioo (realPath H s + s) (H y + y)) = 0 := fun s hs => by
      have := hmono hs
      simp only at this
      rw [Set.Ioo_eq_empty_of_le (by rw [← hgy]; exact this), measure_empty]
    have hFφ : ∀ s ∈ Set.Ioo (0 : ℝ) y,
        (volume.withDensity fun x => ENNReal.ofReal (f (-x)))
          (Set.Ioo (realPath H s + s) (H y + y)) =
        ENNReal.ofReal (∫ x in (realPath H s + s)..(realPath H y + y), f (-x)) := fun s hs => by
      rw [← hgy]
      exact s4_withDensity_Ioo hk (fun x => hf0 (-x)) (hmono hs.2.le)
    have hφ0 : ∀ s ∈ Set.Ioo (0 : ℝ) y,
        0 ≤ ∫ x in (realPath H s + s)..(realPath H y + y), f (-x) := fun s hs =>
      intervalIntegral.integral_nonneg (hmono hs.2.le) fun x _ => hf0 (-x)
    have hφi : IntervalIntegrable
        (fun s => ∫ x in (realPath H s + s)..(realPath H y + y), f (-x)) volume 0 y := by
      have hG : Continuous fun u => ∫ x in u..(realPath H y + y), f (-x) := by
        have : (fun u => ∫ x in u..(realPath H y + y), f (-x)) =
            fun u => -∫ x in (realPath H y + y)..u, f (-x) := by
          funext u; exact intervalIntegral.integral_symm _ _
        rw [this]
        exact (continuous_iff_continuousAt.mpr fun u =>
          (hk.integral_hasStrictDerivAt _ u).hasDerivAt.continuousAt).neg
      exact (hG.comp (hcont.add continuous_id)).intervalIntegrable _ _
    have hsymm : ∫ s in (0 : ℝ)..y, (∫ x in (realPath H s + s)..(realPath H y + y), f (-x)) =
        -∫ s in (0 : ℝ)..y, (∫ x in (realPath H y + y)..(realPath H s + s), f (-x)) := by
      rw [← intervalIntegral.integral_neg]
      congr 1
      ext s
      exact intervalIntegral.integral_symm _ _
    rw [s4_layer_left _ hH hyA hfirst, s4_lintegral_Ioi_eq hy0 h0 hFφ hφ0 hφi,
      hsymm, s4_ibp_layer (g := fun t => realPath H t + t) hk hy0 (hcont.add continuous_id)
        (fun t ht => (hd t ht).add (hasDerivAt_id' t)) (hdi.add intervalIntegrable_const),
      neg_neg]
    congr 1
    congr 1
    ext t
    rw [neg_add']
    ring

/-- **Lemma 13** (`lem:13`). Integrating (7) by parts: if `Φ' = f`, `Φ(-1) = 0` and the smooth
hider path meets the sweeper `A` at time `y` (so `H(y) = 1 - y`), then (7) equals the
variational integral (8) minus `y Φ(1 - 2y)`. So for given `H(0)` and `y` the optimal hider path
maximizes (8). -/
theorem lemma13 {Φ f : ℝ → ℝ} (hΦ : ∀ x, HasDerivAt Φ (f x) x) (hf : Continuous f)
    (hΦ₀ : Φ (-1) = 0) {h : ℝ → ℝ} {y : ℝ} (hy : 0 ≤ y) (hh : ContDiffOn ℝ 1 h (Set.Icc 0 y))
    (hhy : h y = 1 - y) :
    (∫ t in (0 : ℝ)..y, t * (f (h t - t) * (1 - deriv h t) + f (-h t - t) * (1 + deriv h t))) =
      (∫ t in (0 : ℝ)..y, (Φ (-t + h t) + Φ (-t - h t))) - y * Φ (1 - 2 * y) := by
  have hΦc : Continuous Φ := continuous_iff_continuousAt.mpr fun x => (hΦ x).continuousAt
  have hhc : ContinuousOn h (Set.Icc 0 y) := hh.continuousOn
  have huIcc : Set.uIcc 0 y = Set.Icc 0 y := Set.uIcc_of_le hy
  have hvc : ContinuousOn (fun t => -(Φ (h t - t) + Φ (-h t - t))) (Set.uIcc 0 y) := by
    rw [huIcc]
    exact ((hΦc.comp_continuousOn (hhc.sub continuousOn_id)).add
      (hΦc.comp_continuousOn (hhc.neg.sub continuousOn_id))).neg
  have hvd : ∀ t ∈ Set.Ioo (min 0 y) (max 0 y), HasDerivAt (fun t => -(Φ (h t - t) + Φ (-h t - t)))
      (f (h t - t) * (1 - deriv h t) + f (-h t - t) * (1 + deriv h t)) t := by
    intro t ht
    rw [min_eq_left hy, max_eq_right hy] at ht
    have hd : HasDerivAt h (deriv h t) t :=
      ((hh.differentiableOn one_ne_zero).differentiableAt (Icc_mem_nhds ht.1 ht.2)).hasDerivAt
    have hg1 : HasDerivAt (fun t => h t - t) (deriv h t - 1) t := hd.sub (hasDerivAt_id' t)
    have hg2 : HasDerivAt (fun t => -h t - t) (-deriv h t - 1) t := hd.neg.sub (hasDerivAt_id' t)
    have h1 := (hΦ (h t - t)).comp (h := fun t => h t - t) t hg1
    have h2 := (hΦ (-h t - t)).comp (h := fun t => -h t - t) t hg2
    exact ((h1.add h2).neg).congr_deriv (by ring)
  have hv'i : IntervalIntegrable
      (fun t => f (h t - t) * (1 - deriv h t) + f (-h t - t) * (1 + deriv h t)) volume 0 y := by
    have hd := s4_intervalIntegrable_deriv hy hh
    have c1 : ContinuousOn (fun t => f (h t - t)) (Set.uIcc 0 y) := by
      rw [huIcc]; exact hf.comp_continuousOn (hhc.sub continuousOn_id)
    have c2 : ContinuousOn (fun t => f (-h t - t)) (Set.uIcc 0 y) := by
      rw [huIcc]; exact hf.comp_continuousOn (hhc.neg.sub continuousOn_id)
    exact ((intervalIntegrable_const.sub hd).continuousOn_mul c1).add
      ((intervalIntegrable_const.add hd).continuousOn_mul c2)
  have key := intervalIntegral.integral_mul_deriv_eq_deriv_mul_of_hasDerivAt
    (u := fun t => t) (u' := fun _ => 1) continuousOn_id hvc (fun t _ => hasDerivAt_id' t) hvd
    intervalIntegrable_const hv'i
  have hcongr : ∫ t in (0 : ℝ)..y, (Φ (-t + h t) + Φ (-t - h t)) =
      ∫ t in (0 : ℝ)..y, (Φ (h t - t) + Φ (-h t - t)) := by
    congr 1
    ext t
    rw [show -t + h t = h t - t by ring, show -t - h t = -h t - t by ring]
  simp only [one_mul, zero_mul, sub_zero, intervalIntegral.integral_neg] at key
  rw [key, hcongr, hhy, show 1 - y - y = 1 - 2 * y by ring, show -(1 - y) - y = -1 by ring, hΦ₀]
  ring

/-- The right-hand side of formula (9), for `x = H(0)`, the meeting time `y` and the path `h`. -/
noncomputable def formula9 (Φ : ℝ → ℝ) (x y : ℝ) (h : ℝ → ℝ) : ℝ :=
  1 - Φ (-x) + 2 * Φ (1 - 2 * y) + y / 2 * (1 - Φ x) - y / 2 * Φ (1 - 2 * y) +
    1 / 2 * ∫ t in (0 : ℝ)..y, (Φ (-t + h t) + Φ (-t - h t))

/-! ### The payoff formula (9) -/

section Payoff

variable {H : C(ℝ≥0, ℝ)}

lemma s4_lintegral_split (ν : Measure ℝ) (F : ℝ → ℝ≥0∞) {a b : ℝ} (hab : a ≤ b) :
    ∫⁻ x, F x ∂ν = ∫⁻ x in Set.Iic a, F x ∂ν + ∫⁻ x in Set.Ioc a b, F x ∂ν +
      ∫⁻ x in Set.Ioi b, F x ∂ν := by
  rw [← lintegral_union measurableSet_Ioc (Set.Iic_disjoint_Ioc le_rfl),
    Set.Iic_union_Ioc_eq_Iic hab, ← Set.compl_Iic, lintegral_add_compl _ measurableSet_Iic]

lemma s4_runner_two {x : ℝ} (hx : x ∈ I) : runner x 2 = -1 := by
  simp only [runner, pathOf_apply, NNReal.coe_ofNat]
  rw [min_eq_right (by linarith [hx.1]), show (1 : ℝ) - 2 = -1 by norm_num]
  exact Real.triangleWave_of_mem_Icc ⟨le_rfl, by norm_num⟩

lemma s4_runner_four {x : ℝ} (hx : x ∈ I) : runner x 4 = 1 := by
  simp only [runner, pathOf_apply, NNReal.coe_ofNat]
  rw [min_eq_right (by linarith [hx.1]),
    Real.triangleWave_of_mem_Icc_neg_three_neg_one ⟨by norm_num, by norm_num⟩]
  norm_num

lemma s4_leftRunner_two {z : ℝ} (hz : z ∈ I) : leftRunner z 2 = 1 := by
  simp only [leftRunner, pathOf_apply, NNReal.coe_ofNat]
  rw [max_eq_right (by linarith [hz.2]), show (2 : ℝ) - 1 = 1 by norm_num]
  exact Real.triangleWave_of_mem_Icc ⟨by norm_num, le_rfl⟩

/-- Every right runner meets every hider path by time `4`: it sweeps `[-1, 1]` during `[2, 4]`. -/
lemma s4_runner_le_four (hH : H ∈ hiderPaths) {x : ℝ} (hx : x ∈ I) :
    captureTime (runner x) H ≤ 4 := by
  have := captureTime_le_of_le_of_le (S := runner x) (H := H) (t₁ := 2) (t₂ := 4) (by norm_num)
    (by rw [s4_runner_two hx]; exact (hH 2).1) (by rw [s4_runner_four hx]; exact (hH 4).2)
  simpa using this

/-- A left runner starting below `H` meets it by time `2`: it joins `-A`, which reaches `+1` at
time `2`. -/
lemma s4_leftRunner_le_two (hH : H ∈ hiderPaths) {z : ℝ} (hz : z ∈ I) (hzH : z ≤ H 0) :
    captureTime (leftRunner z) H ≤ 2 := by
  have := captureTime_le_of_le_of_le (S := leftRunner z) (H := H) (t₁ := 0) (t₂ := 2)
    (by norm_num) (by rw [s4_leftRunner_zero hz]; exact hzH)
    (by rw [s4_leftRunner_two hz]; exact (hH 2).2)
  simpa using this

/-- A right runner starting above `H(0)`, when `H` meets `A` first at `y`, catches `H` by time
`y`: it runs along `A` from time `(1 - x)/2 ≤ y`. -/
lemma s4_runner_le_y (hH : H ∈ searcherPaths) {y : ℝ≥0} (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) {x : ℝ} (hx : x ∈ I)
    (hxH : H 0 < x) : captureTime (runner x) H ≤ y := by
  obtain ⟨hy1, hHy, -⟩ := s4_meetA hH hyA hfirst
  have h0 : H y - H 0 ≤ y := by simpa using (s4_speed hH (zero_le : (0 : ℝ≥0) ≤ y)).1
  refine captureTime_le ?_
  rw [s4_runner_apply hx (by linarith), hHy, min_eq_right (by linarith)]

/-- If `H` meets `A` strictly first, it does so before time `1`. -/
lemma s4_lt_one_of_first (hH : H ∈ searcherPaths) {y : ℝ≥0} (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H < captureTime (-sweeperA) H) : (y : ℝ) < 1 := by
  obtain ⟨hy1, hHy, -⟩ := s4_meetA hH hyA hfirst.le
  refine lt_of_le_of_ne hy1 fun h => ?_
  have hmeet : (-sweeperA) y = H y := by rw [s4_negA_apply (by linarith), hHy, h]
  exact absurd (hfirst.trans_le ((captureTime_le hmeet).trans hyA.symm.le)) (lt_irrefl _)

/-- Equality cases of (9). A right runner starting below `H(y) - y = 1 - 2y` catches `H` at
time `4` if `H` runs to `+1` after meeting `A` (first) at `y`. -/
lemma s4_runner_eq_four (hH : H ∈ searcherPaths) {y : ℝ≥0} (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H < captureTime (-sweeperA) H)
    (hrun : ∀ t : ℝ≥0, y ≤ t → H t = min 1 (H y + ((t : ℝ) - y))) {x : ℝ} (hx : x ∈ I)
    (hxy : x < H y - y) : captureTime (runner x) H = 4 := by
  have hsw : sweepTime H = y := by rw [sweepTime, min_eq_left hfirst.le, hyA]
  obtain ⟨hy1, hHy, -⟩ := s4_meetA hH hyA hfirst.le
  have hy0 := y.coe_nonneg
  have hxy' : x < 1 - 2 * y := by rw [hHy] at hxy; linarith
  have hL := (lemma11 hH hsw hx hxy.ne (by rw [hHy]; intro h; linarith)).1
  have hyT : (y : ℝ≥0∞) ≤ captureTime (runner x) H := by
    by_contra hcon
    exact absurd (hL.mp (not_le.mp hcon)).1 (not_lt.mpr hxy.le)
  have hy4 : y ≤ 4 := by rw [← NNReal.coe_le_coe]; push_cast; linarith
  have hH4 : H 4 = 1 := by
    rw [hrun 4 hy4, hHy, min_eq_left (by push_cast; linarith)]
  rw [s4_captureTime_eq_of hyT (fun t hyt ht4 => ?_) (by rw [s4_runner_four hx, hH4])]
  · norm_num
  have hyt' : (y : ℝ) ≤ t := hyt
  have ht4' : (t : ℝ) < 4 := ht4
  rw [hrun t hyt, hHy]
  apply ne_of_lt
  rcases le_or_gt (t : ℝ) 2 with ht2 | ht2
  · rw [s4_runner_apply hx ht2]
    have := min_le_left (x + (t : ℝ)) (1 - t)
    have := min_le_right (x + (t : ℝ)) (1 - t)
    exact lt_min (by linarith) (by linarith)
  · simp only [runner, pathOf_apply]
    rw [min_eq_right (by linarith [hx.1]),
      Real.triangleWave_of_mem_Icc_neg_three_neg_one ⟨by linarith, by linarith⟩]
    exact lt_min (by linarith) (by linarith)

/-- A right runner starting above `H(0)` catches `H` exactly at `y`. -/
lemma s4_runner_eq_y (hH : H ∈ searcherPaths) {y : ℝ≥0} (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) {x : ℝ} (hx : x ∈ I)
    (hxH : H 0 < x) (hx1 : x ≠ 1) : captureTime (runner x) H = y := by
  have hsw : sweepTime H = y := by rw [sweepTime, min_eq_left hfirst, hyA]
  obtain ⟨hy1, hHy, -⟩ := s4_meetA hH hyA hfirst
  have h0 : H y - H 0 ≤ y := by simpa using (s4_speed hH (zero_le : (0 : ℝ≥0) ≤ y)).1
  have hL := (lemma11 hH hsw hx (ne_of_gt (by linarith)) (by rw [hHy, sub_add_cancel]; exact hx1)).1
  refine le_antisymm (s4_runner_le_y hH hyA hfirst hx hxH) ?_
  by_contra hcon
  exact absurd (hL.mp (not_le.mp hcon)).2 (not_le.mpr hxH)

/-- A left runner starting below `H(0)` catches `H` at time `2` if `H` runs to `+1` after meeting
`A` (strictly first) at `y`. -/
lemma s4_leftRunner_eq_two (hH : H ∈ searcherPaths) {y : ℝ≥0} (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H < captureTime (-sweeperA) H)
    (hrun : ∀ t : ℝ≥0, y ≤ t → H t = min 1 (H y + ((t : ℝ) - y))) {z : ℝ} (hz : z ∈ I)
    (hzH : z < H 0) (hz1 : z ≠ H y - y) : captureTime (leftRunner z) H = 2 := by
  have hsw : sweepTime H = y := by rw [sweepTime, min_eq_left hfirst.le, hyA]
  obtain ⟨hy1, hHy, -⟩ := s4_meetA hH hyA hfirst.le
  have hy1' := s4_lt_one_of_first hH hyA hfirst
  have h0 : H 0 - H y ≤ y := by simpa using (s4_speed hH (zero_le : (0 : ℝ≥0) ≤ y)).2
  have hL := (lemma11 hH hsw hz hz1 (by rw [hHy]; intro h; linarith)).2
  have hyT : (y : ℝ≥0∞) ≤ captureTime (leftRunner z) H := by
    by_contra hcon
    exact absurd (hL.mp (not_le.mp hcon)).1 (not_le.mpr hzH)
  have hy2 : y ≤ 2 := by rw [← NNReal.coe_le_coe]; push_cast; linarith
  have hH2 : H 2 = 1 := by
    rw [hrun 2 hy2, hHy, min_eq_left (by push_cast; linarith)]
  rw [s4_captureTime_eq_of hyT (fun t hyt ht2 => ?_) (by rw [s4_leftRunner_two hz, hH2])]
  · norm_num
  have hyt' : (y : ℝ) ≤ t := hyt
  have ht2' : (t : ℝ) < 2 := ht2
  have ht0 := NNReal.coe_nonneg t
  have hH0 := (hH.1 0).2
  rw [s4_leftRunner_apply hz ht2'.le, hrun t hyt, hHy]
  exact ne_of_lt (max_lt (lt_min (by linarith) (by linarith)) (lt_min (by linarith) (by linarith)))

/-- Assembling (9) from the five groups of searchers. -/
lemma s4_formula9_sum (μ : Measure ℝ) [IsProbabilityMeasure μ] (b : ℝ) (y : ℝ≥0) (h : ℝ → ℝ)
    (hi1 : IntervalIntegrable (fun t => cdf μ (h t - t)) volume 0 y)
    (hi2 : IntervalIntegrable (fun t => cdf μ (-h t - t)) volume 0 y)
    (hI1 : 0 ≤ ∫ t in (0 : ℝ)..y, (cdf μ (h t - t) - cdf μ (1 - 2 * y)))
    (hI2 : 0 ≤ ∫ t in (0 : ℝ)..y, cdf μ (-h t - t)) :
    (1 / 2 : ℝ≥0∞) * ((4 * μ (Set.Iic (1 - 2 * y)) +
        ENNReal.ofReal (∫ t in (0 : ℝ)..y, (cdf μ (h t - t) - cdf μ (1 - 2 * y))) +
        (y : ℝ≥0∞) * μ (Set.Ioi b)) +
      (0 + ENNReal.ofReal (∫ t in (0 : ℝ)..y, cdf μ (-h t - t)) + 2 * μ (Set.Ioi (-b)))) =
      ENNReal.ofReal (formula9 (cdf μ) b y h) := by
  have ha0 := s4_cdf_nonneg μ (1 - 2 * y)
  have hb1 := s4_cdf_le_one μ b
  have hb2 := s4_cdf_le_one μ (-b)
  have hy0 := y.coe_nonneg
  have e1 : (4 : ℝ≥0∞) * μ (Set.Iic (1 - 2 * y)) = ENNReal.ofReal (4 * cdf μ (1 - 2 * y)) := by
    rw [s4_measure_Iic, ENNReal.ofReal_mul (by norm_num)]; norm_num
  have e2 : (y : ℝ≥0∞) * μ (Set.Ioi b) = ENNReal.ofReal (y * (1 - cdf μ b)) := by
    rw [s4_measure_Ioi, ENNReal.ofReal_mul hy0, ENNReal.ofReal_coe_nnreal]
  have e3 : (2 : ℝ≥0∞) * μ (Set.Ioi (-b)) = ENNReal.ofReal (2 * (1 - cdf μ (-b))) := by
    rw [s4_measure_Ioi, ENNReal.ofReal_mul (by norm_num)]; norm_num
  have e4 : (1 / 2 : ℝ≥0∞) = ENNReal.ofReal (1 / 2) := by
    rw [ENNReal.ofReal_div_of_pos two_pos]; norm_num
  rw [e1, e2, e3, e4, zero_add, ← ENNReal.ofReal_add (by positivity) hI1,
    ← ENNReal.ofReal_add (by positivity) (mul_nonneg hy0 (by linarith)),
    ← ENNReal.ofReal_add hI2 (by linarith),
    ← ENNReal.ofReal_add (by positivity) (by nlinarith), ← ENNReal.ofReal_mul (by norm_num)]
  congr 1
  have hcongr : ∫ t in (0 : ℝ)..y, (cdf μ (-t + h t) + cdf μ (-t - h t)) =
      ∫ t in (0 : ℝ)..y, (cdf μ (h t - t) + cdf μ (-h t - t)) := by
    congr 1
    ext t
    rw [show -t + h t = h t - t by ring, show -t - h t = -h t - t by ring]
  rw [formula9, hcongr, intervalIntegral.integral_add hi1 hi2,
    intervalIntegral.integral_sub hi1 intervalIntegrable_const, intervalIntegral.integral_const,
    smul_eq_mul]
  ring

end Payoff

/-- **Formula (9)** (`eq:9`). Let the starting point of `s_Φ` have an atomless distribution `μ`
on `[-1, 1]`, and let `H` be a hider path of speed at most `1` that meets the sweeper `A` first,
at time `y`, and then runs to the end `+1`. Then `V(s_Φ, H)` is given by (9), with `x = H(0)`.

"First" is strict: a path that meets both sweepers at time `1` (where they cross, at `0`) and then
runs to `+1` runs along `-A` and is met by the left runners at time `1`, not `2`; there (9) fails
(for `H = F` with `ε = 0` and uniform `Φ` the payoff is `3/4`, while (9) gives `1`).

Proof: as for `equation9_le`; now the right runners starting above `H(0)` catch `H` exactly at
`y`, those starting below `1 - 2y` exactly at `4`, and the left runners starting below `H(0)`
exactly at `2` (Lemma 11 rules out an earlier meeting). -/
theorem equation9 (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ] (hμ : μ Iᶜ = 0)
    {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y) (hfirst : captureTime sweeperA H < captureTime (-sweeperA) H)
    (hrun : ∀ t : ℝ≥0, y ≤ t → H t = min 1 (H y + ((t : ℝ) - y))) :
    ∫⁻ S, captureTime S H ∂(sPhi μ) = ENNReal.ofReal (formula9 (cdf μ) (H 0) y (realPath H)) := by
  obtain ⟨hy1, hHy, -⟩ := s4_meetA hH hyA hfirst.le
  have hI : ∀ᵐ x ∂μ, x ∈ I := by rw [ae_iff]; exact hμ
  have h0 : H y - H 0 ≤ y := by simpa using (s4_speed hH (zero_le : (0 : ℝ≥0) ≤ y)).1
  have hgy : realPath H y - y = 1 - 2 * y := by rw [s4_realPath_coe, hHy]; ring
  have hHI := hH.1 0
  have hΦ := s4_cdf_mono μ
  have hanti := s4_antitone_g hH
  have hanti₂ : Antitone fun t => -realPath H t - t := fun s t hst => by
    have := s4_monotone_g₂ hH hst
    simp only at this ⊢
    linarith
  obtain ⟨h13r, h13l⟩ := s4_lemma13' μ hμ hH hyA hfirst.le
  have R1 : ∫⁻ x in Set.Iic (H y - y), captureTime (runner x) H ∂μ =
      4 * μ (Set.Iic (H y - y)) := by
    rw [← setLIntegral_const]
    refine setLIntegral_congr_fun_ae measurableSet_Iic ?_
    filter_upwards [hI, Measure.ae_ne μ (H y - y)] with x hx hxa hxs
    exact s4_runner_eq_four hH hyA hfirst hrun hx (lt_of_le_of_ne hxs hxa)
  have R3 : ∫⁻ x in Set.Ioi (H 0), captureTime (runner x) H ∂μ = y * μ (Set.Ioi (H 0)) := by
    rw [← setLIntegral_const]
    refine setLIntegral_congr_fun_ae measurableSet_Ioi ?_
    filter_upwards [hI, Measure.ae_ne μ 1] with x hx hx1 hxs
    exact s4_runner_eq_y hH hyA hfirst.le hx hxs hx1
  have L3 : ∫⁻ x in Set.Ioi (-H 0), captureTime (leftRunner (-x)) H ∂μ =
      2 * μ (Set.Ioi (-H 0)) := by
    rw [← setLIntegral_const]
    refine setLIntegral_congr_fun_ae measurableSet_Ioi ?_
    filter_upwards [hI, Measure.ae_ne μ (-(H y - y))] with x hx hxa hxs
    exact s4_leftRunner_eq_two hH hyA hfirst hrun ⟨by linarith [hx.2], by linarith [hx.1]⟩
      (by linarith [Set.mem_Ioi.mp hxs]) (fun h => hxa (by rw [← h, neg_neg]))
  rw [s4_lintegral_sPhi, s4_lintegral_split μ _ (show H y - y ≤ H 0 by linarith),
    s4_lintegral_split μ _ (show -(H y + y) ≤ -H 0 by linarith [hHI.2]), h13r, h13l, R1, R3, L3,
    show H y - (y : ℝ) = 1 - 2 * y by rw [hHy]; ring, show -(H y + (y : ℝ)) = -1 by rw [hHy]; ring,
    setLIntegral_measure_zero _ _ (s4_measure_Iic_neg_one μ hμ)]
  exact s4_formula9_sum μ (H 0) y (realPath H)
    ((hΦ.comp_antitone hanti).intervalIntegrable) ((hΦ.comp_antitone hanti₂).intervalIntegrable)
    (intervalIntegral.integral_nonneg y.coe_nonneg fun t ht =>
      sub_nonneg.mpr (hΦ (by rw [← hgy]; exact hanti ht.2)))
    (intervalIntegral.integral_nonneg y.coe_nonneg fun t _ => s4_cdf_nonneg μ _)

/-- **Formula (9)** (`eq:9`), as a bound: whatever the hider does after meeting the sweeper,
`V(s_Φ, H)` is at most (9).

Proof: split `s_Φ` into the five groups of searchers of Lemma 11. The right runners starting in
`(1 - 2y, H(0)]` and the left runners starting in `[H(0), 1)` contribute the two integrals of
Lemma 13'; the right runners starting above `H(0)` catch `H` by time `y`, those starting below
`1 - 2y` by time `4`, and the left runners starting below `H(0)` by time `2`. -/
theorem equation9_le (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ] (hμ : μ Iᶜ = 0)
    {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y)
    (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) :
    ∫⁻ S, captureTime S H ∂(sPhi μ) ≤ ENNReal.ofReal (formula9 (cdf μ) (H 0) y (realPath H)) := by
  obtain ⟨hy1, hHy, -⟩ := s4_meetA hH hyA hfirst
  have hI : ∀ᵐ x ∂μ, x ∈ I := by rw [ae_iff]; exact hμ
  have h0 : H y - H 0 ≤ y := by simpa using (s4_speed hH (zero_le : (0 : ℝ≥0) ≤ y)).1
  have hgy : realPath H y - y = 1 - 2 * y := by rw [s4_realPath_coe, hHy]; ring
  have hHI := hH.1 0
  have hΦ := s4_cdf_mono μ
  have hanti := s4_antitone_g hH
  have hanti₂ : Antitone fun t => -realPath H t - t := fun s t hst => by
    have := s4_monotone_g₂ hH hst
    simp only at this ⊢
    linarith
  obtain ⟨h13r, h13l⟩ := s4_lemma13' μ hμ hH hyA hfirst
  rw [s4_lintegral_sPhi, s4_lintegral_split μ _ (show H y - y ≤ H 0 by linarith),
    s4_lintegral_split μ _ (show -(H y + y) ≤ -H 0 by linarith [hHI.2]), h13r, h13l,
    show H y - (y : ℝ) = 1 - 2 * y by rw [hHy]; ring, show -(H y + (y : ℝ)) = -1 by rw [hHy]; ring,
    setLIntegral_measure_zero _ _ (s4_measure_Iic_neg_one μ hμ)]
  rw [← s4_formula9_sum μ (H 0) y (realPath H)
    ((hΦ.comp_antitone hanti).intervalIntegrable) ((hΦ.comp_antitone hanti₂).intervalIntegrable)
    (intervalIntegral.integral_nonneg y.coe_nonneg fun t ht =>
      sub_nonneg.mpr (hΦ (by rw [← hgy]; exact hanti ht.2)))
    (intervalIntegral.integral_nonneg y.coe_nonneg fun t _ => s4_cdf_nonneg μ _)]
  gcongr
  · rw [← setLIntegral_const]
    exact setLIntegral_mono_ae aemeasurable_const
      (hI.mono fun x hx _ => s4_runner_le_four (searcherPaths_subset_hiderPaths hH) hx)
  · rw [← setLIntegral_const]
    exact setLIntegral_mono_ae aemeasurable_const
      (hI.mono fun x hx hxs => s4_runner_le_y hH hyA hfirst hx hxs)
  · rw [← setLIntegral_const]
    exact setLIntegral_mono_ae aemeasurable_const
      (hI.mono fun x hx hxs => s4_leftRunner_le_two (searcherPaths_subset_hiderPaths hH)
        ⟨by linarith [hx.2], by linarith [hx.1]⟩ (by linarith [Set.mem_Ioi.mp hxs]))

lemma s4_cdf_uniformI {u : ℝ} (hu : u ∈ I) : cdf uniformI u = (u + 1) / 2 := by
  have hset : Set.Iic u ∩ Set.Icc (-1) 1 = Set.Icc (-1) u := by
    ext v
    simp only [Set.mem_inter_iff, Set.mem_Iic, Set.mem_Icc]
    constructor
    · rintro ⟨h1, h2, -⟩; exact ⟨h2, h1⟩
    · rintro ⟨h1, h2⟩; exact ⟨h2, h1, h2.trans hu.2⟩
  rw [cdf, uniformI, Measure.smul_apply, Measure.restrict_apply measurableSet_Iic, hset,
    Real.volume_Icc, smul_eq_mul, ENNReal.toReal_mul, ENNReal.toReal_ofReal (by linarith [hu.1])]
  norm_num
  ring

/-- **Formula (10)** (`eq:10`). For the uniform distribution on `[-1, 1]` the variational
integral does not depend on the path, and (9) equals `(10 + 2x - (7 + x) y + y²)/4`. -/
theorem equation10 {x y : ℝ} (hx : x ∈ I) (hy0 : 0 ≤ y) (hy1 : y ≤ 1) {h : ℝ → ℝ}
    (hh : ∀ t ∈ Set.Icc 0 y, t - 1 ≤ h t ∧ h t ≤ 1 - t) :
    formula9 (cdf uniformI) x y h = (10 + 2 * x - (7 + x) * y + y ^ 2) / 4 := by
  have hint : ∫ t in (0 : ℝ)..y, (cdf uniformI (-t + h t) + cdf uniformI (-t - h t)) =
      ∫ t in (0 : ℝ)..y, (1 - t) := by
    refine intervalIntegral.integral_congr fun t ht => ?_
    rw [Set.uIcc_of_le hy0] at ht
    obtain ⟨h1, h2⟩ := hh t ht
    have := ht.1
    rw [s4_cdf_uniformI ⟨by linarith, by linarith⟩, s4_cdf_uniformI ⟨by linarith, by linarith⟩]
    ring
  have hlin : ∫ t in (0 : ℝ)..y, (1 - t) = y - y ^ 2 / 2 := by
    rw [intervalIntegral.integral_eq_sub_of_hasDerivAt (f := fun t => t - t * t / 2)
      (fun t _ => ((hasDerivAt_id' t).sub
        (((hasDerivAt_id' t).mul (hasDerivAt_id' t)).div_const 2)).congr_deriv (by ring))
      ((by fun_prop : Continuous fun t : ℝ => 1 - t).intervalIntegrable 0 y)]
    ring
  rw [formula9, hint, hlin, s4_cdf_uniformI (u := -x) ⟨by linarith [hx.2], by linarith [hx.1]⟩,
    s4_cdf_uniformI hx, s4_cdf_uniformI (u := 1 - 2 * y) ⟨by linarith, by linarith⟩]
  ring

end PrincessMonster
