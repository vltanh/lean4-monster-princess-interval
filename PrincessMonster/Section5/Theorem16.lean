module

public import PrincessMonster.Section3.Strategies
public import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
public import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
public import Mathlib.Order.Filter.Basic
public import Mathlib.Topology.Instances.ENNReal.Lemmas

/-!
# Section 5: a hider strategy with a continuous initial distribution; Theorem 16, `V ≥ 15/11`

The loitering hider of `h_Φ` picks `x` according to `Φ`, waits at `x` until the sweeper `A` is
`ε`-close, runs ahead of it to `ε`, turns, and runs back to `1`; `-h_Φ` is its mirror image. The
hider strategy `γ` uses the ends `±1` with total probability `3/11` and `h_Φ`, with `Φ` uniform,
with probability `8/11`. The searcher's best response is worth `15/11` (as `ε → 0`).

* `loiterer ε x`, `hPhi ρ ε` (the loiterers with starting distribution `ρ`, both sides), `gamma ε`;
* `pathS1 y ε`, `pathS2 y ε`: the searcher paths `S₁`, `S₂` of the paper (start at `1 - 2y - ε`,
  run right until `ε`-close to `A` at time `y`; then turn and run to `-1` and back (`S₁`), or
  continue to `+1` and back (`S₂`));
* `equation15`: their payoffs against `h_Φ`, formula (15), corrected;
* `theorem16`.

## Proofs

Theorem 16 is proved by the repaired argument (notes/plans/thm16.md), not by (15) and
Proposition 5. Write `W(S) = 22 E_γ T(S, ·) = 3a + 3b + (8/(1-2ε)) (∫ T(S, P_x) + ∫ T(S, -P_x))`
with `a = T(S, E)`, `b = T(S, -E)` (`s5_lintegral_gamma`).
* Upper bound (`s5_upper`): against the sweeper `A`, `T(A, ±E) ≤ 0, 2`, `T(A, P_x) ≤ 1`,
  `T(A, -P_x) ≤ 2`, so `E_γ T(A, ·) ≤ 15/11`.
* Lower bound (`s5_lower`): `E_γ T(S, ·) ≥ (30 - 200ε)/22` for every searcher path `S`. Let `τ` be
  the exit time from the diamond `|p| < F(t) = 1 - ε - t` (`s5_exists_tau`), reflected so that
  `S(τ) ≥ F(τ)` (`s5_lintegral_gamma_neg`). Lemma B (`s5_visited_pos`, `s5_measure_visited`): the
  loiterers met before `τ` sit in `S([0, t])`, so at most mass `t` is met by time `t`, and the
  layer cake bound gives them total capture time `≥ L²/2` (`s5_layer_cake`, `s5_visited`).
  Lemma D (`s5_neg_after`): the unvisited negative loiterers are met at `-1`, at time `b ≥ 2 - ε`
  (`s5_b_ge`). Lemma E (`s5_lemmaE`): meeting the front at `t` gives `a ≥ 2t + ε`. Lemma F
  (`s5_pos_after`): an unvisited positive loiterer is met no earlier than `ℓ(x)` (`s5_ell`). The
  cases `b < a`, `a < b` (`s5_caseI`) and `|S| < F` on `[0, 1 - 2ε]` (`s5_caseII`) end with
  explicit polynomial inequalities (`s5_ineq_ba`, `s5_ineq_ab1`–`s5_ineq_ab3`, `s5_ineq_II`).

Formula (15) is proved by computing, for small `ε`, the capture time of every loiterer by `S₁`
and `S₂` exactly (`s5_T1p_a` … `s5_T2n_b`), and passing to the limit by dominated convergence.
-/

@[expose] public section

open scoped NNReal ENNReal Topology
open MeasureTheory Filter

namespace PrincessMonster

/-- The loitering hider of `h_Φ`: wait at `x` until the sweeper `A` is `ε`-close (time
`1 - x - ε`), run just ahead of it to `ε` (time `1 - 2ε`), turn and run to `+1`. -/
noncomputable def loiterer (ε x : ℝ) : C(ℝ≥0, ℝ) :=
  pathOf (fun t => min 1 (max (min x (1 - ε - t)) (t - 1 + 3 * ε))) (by fun_prop)

/-- The hider strategy `h_Φ` together with its reflection `-h_Φ`, each with probability `1/2`:
the loiterers start at `x ∼ ρ` (respectively `-x`). -/
noncomputable def hPhi (ρ : Measure ℝ) (ε : ℝ) : Measure hiderPaths :=
  (1 / 2 : ℝ≥0∞) • (ρ.map (fun x => toHider (loiterer ε x)) +
    ρ.map (fun x => toHider (-loiterer ε x)))

/-- The uniform distribution on `[a, b]`. -/
noncomputable def uniformOn (a b : ℝ) : Measure ℝ :=
  (ENNReal.ofReal (b - a))⁻¹ • volume.restrict (Set.Icc a b)

/-- The hider strategy `γ` of Theorem 16: the ends `±1` with probability `3/22` each, and `h_Φ`,
with `Φ` uniform on `[ε, 1 - ε]`, with probability `8/11`. -/
noncomputable def gamma (ε : ℝ) : Measure hiderPaths :=
  (3 / 11 : ℝ≥0∞) • symDiracH hiderE + (8 / 11 : ℝ≥0∞) • hPhi (uniformOn ε (1 - ε)) ε

/-- The searcher path `S₁`: start at `1 - 2y - ε`, run right until `ε`-close to the sweeper `A`
(time `y`), turn and run to `-1`, and back. -/
noncomputable def pathS1 (y ε : ℝ) : C(ℝ≥0, ℝ) :=
  pathOf (fun t => Real.triangleWave (min (1 - 2 * y - ε + t) (1 - ε - t))) (by fun_prop)

/-- The searcher path `S₂`: start at `1 - 2y - ε`, run right to `+1`, and back to `-1`. -/
noncomputable def pathS2 (y ε : ℝ) : C(ℝ≥0, ℝ) :=
  pathOf (fun t => Real.triangleWave (1 - 2 * y - ε + t)) (by fun_prop)

/-- Formula (15) for `V(S₁, h_Φ)`, corrected (the density `f` vanishes outside `[0, 1]`). -/
noncomputable def formula15S1 (Φ f : ℝ → ℝ) (y : ℝ) : ℝ :=
  (1 - Φ (2 * y - 1)) + 1 / 2 * (∫ t in (0 : ℝ)..(2 * y - 1), (2 * y - 1 - t) * f t) +
    1 / 2 * (y * (1 - Φ (1 - y)) + (∫ t in (0 : ℝ)..(1 - 2 * y), (1 - t) * f t) +
      ∫ t in (1 - 2 * y)..(1 - y), (t - 1 + 2 * y) * f t)

/-- Formula (15) for `V(S₂, h_Φ)`, corrected (the density `f` vanishes outside `[0, 1]`). -/
noncomputable def formula15S2 (Φ f : ℝ → ℝ) (y : ℝ) : ℝ :=
  (1 + y) * (1 - Φ (2 * y - 1)) + 1 / 2 * (∫ t in (0 : ℝ)..(2 * y - 1), (2 * y - 1 - t) * f t) +
    1 / 2 * (y * (1 - Φ (1 - y)) + (1 + y) * Φ (1 - 2 * y) +
      ∫ t in (1 - 2 * y)..(1 - y), (t - 1 + 2 * y) * f t)

/-! ### Measurability and the integral against `γ` -/

/-- The capture time is lower semicontinuous in the hider's path. -/
theorem s5_lsc_captureTime (S : C(ℝ≥0, ℝ)) :
    LowerSemicontinuous fun H : C(ℝ≥0, ℝ) => captureTime S H := by
  rw [lowerSemicontinuous_iff_isOpen_preimage]
  intro y
  have hset : (fun H : C(ℝ≥0, ℝ) => captureTime S H) ⁻¹' Set.Ioi y =
      ⋃ (r : ℝ≥0) (_ : y < r), (fun H : C(ℝ≥0, ℝ) => H - S) ⁻¹'
        {G : C(ℝ≥0, ℝ) | Set.MapsTo G (Set.Icc 0 r) {0}ᶜ} := by
    ext H
    simp only [Set.mem_preimage, Set.mem_Ioi, Set.mem_iUnion, Set.mem_ofPred_eq, exists_prop]
    constructor
    · intro h
      by_cases htop : captureTime S H = ⊤
      · have hy : y ≠ ⊤ := ne_top_of_lt h
        refine ⟨y.toNNReal + 1, ?_, fun t _ => ?_⟩
        · rw [ENNReal.coe_add, ENNReal.coe_toNNReal hy]
          exact ENNReal.lt_add_right hy one_ne_zero
        · simp only [Set.mem_compl_iff, Set.mem_singleton_iff, ContinuousMap.sub_apply,
            sub_eq_zero]
          exact fun he => captureTime_eq_top_iff.mp htop t he.symm
      · obtain ⟨t₀, -, he⟩ := exists_eq_captureTime htop
        rw [he] at h
        obtain ⟨r, hyr, hrt⟩ := ENNReal.lt_iff_exists_nnreal_btwn.mp h
        refine ⟨r, hyr, fun t ht => ?_⟩
        simp only [Set.mem_compl_iff, Set.mem_singleton_iff, ContinuousMap.sub_apply, sub_eq_zero]
        intro heq
        have h1 := captureTime_le (S := S) (H := H) heq.symm
        rw [he] at h1
        have : (t : ℝ≥0∞) ≤ r := ENNReal.coe_le_coe.mpr ht.2
        exact absurd (h1.trans this) (not_le.mpr hrt)
    · rintro ⟨r, hyr, hmaps⟩
      refine lt_of_lt_of_le hyr ?_
      rw [le_captureTime_iff]
      intro t ht
      by_contra hlt
      push Not at hlt
      have := hmaps (show t ∈ Set.Icc 0 r from ⟨zero_le, (ENNReal.coe_lt_coe.mp hlt).le⟩)
      simp [ht] at this
  rw [hset]
  refine isOpen_iUnion fun r => isOpen_iUnion fun _ => ?_
  exact (ContinuousMap.isOpen_setOfPred_mapsTo isCompact_Icc isOpen_compl_singleton).preimage
    (continuous_id.sub continuous_const)

theorem s5_measurable_captureTime (S : C(ℝ≥0, ℝ)) :
    Measurable fun H : hiderPaths => captureTime S H :=
  (s5_lsc_captureTime S).measurable.comp measurable_subtype_coe

lemma s5_loiterer_apply (ε x : ℝ) (t : ℝ≥0) :
    loiterer ε x t = min 1 (max (min x (1 - ε - t)) (t - 1 + 3 * ε)) := rfl

lemma s5_loiterer_mem {ε : ℝ} (hε : 0 ≤ ε) (x : ℝ) : loiterer ε x ∈ hiderPaths := by
  intro t
  rw [s5_loiterer_apply, Set.mem_Icc]
  exact ⟨le_min (by norm_num) (le_max_of_le_right (by linarith [NNReal.coe_nonneg t])),
    min_le_left _ _⟩

lemma s5_continuous_loiterer (ε : ℝ) : Continuous fun x => loiterer ε x := by
  let G : C(ℝ × ℝ≥0, ℝ) :=
    ⟨fun p => min 1 (max (min p.1 (1 - ε - p.2)) (p.2 - 1 + 3 * ε)), by fun_prop⟩
  have : (fun x => loiterer ε x) = fun x => G.curry x := by
    funext x; ext t; rfl
  rw [this]
  exact G.curry.continuous

lemma s5_toHider_of_mem {H : C(ℝ≥0, ℝ)} (h : H ∈ hiderPaths) : toHider H = ⟨H, h⟩ := by
  simp [toHider, h]

lemma s5_measurable_toHider_loiterer {ε : ℝ} (hε : 0 ≤ ε) :
    Measurable fun x => toHider (loiterer ε x) := by
  have : (fun x => toHider (loiterer ε x)) =
      fun x => (⟨loiterer ε x, s5_loiterer_mem hε x⟩ : hiderPaths) := by
    funext x; exact s5_toHider_of_mem _
  rw [this]
  exact ((s5_continuous_loiterer ε).subtype_mk _).measurable

lemma s5_measurable_toHider_neg_loiterer {ε : ℝ} (hε : 0 ≤ ε) :
    Measurable fun x => toHider (-loiterer ε x) := by
  have : (fun x => toHider (-loiterer ε x)) =
      fun x => (⟨-loiterer ε x, neg_mem_hiderPaths (s5_loiterer_mem hε x)⟩ : hiderPaths) := by
    funext x; exact s5_toHider_of_mem _
  rw [this]
  exact ((continuous_neg.comp (s5_continuous_loiterer ε)).subtype_mk _).measurable

lemma s5_measurable_T_loiterer (ε : ℝ) (S : C(ℝ≥0, ℝ)) :
    Measurable fun x => captureTime S (loiterer ε x) :=
  (s5_lsc_captureTime S).measurable.comp (s5_continuous_loiterer ε).measurable

lemma s5_measurable_T_neg_loiterer (ε : ℝ) (S : C(ℝ≥0, ℝ)) :
    Measurable fun x => captureTime S (-loiterer ε x) :=
  (s5_lsc_captureTime S).measurable.comp
    (continuous_neg.comp (s5_continuous_loiterer ε)).measurable

lemma s5_lintegral_hPhi {ε : ℝ} (hε : 0 ≤ ε) (ρ : Measure ℝ) (S : C(ℝ≥0, ℝ)) :
    ∫⁻ H, captureTime S H ∂(hPhi ρ ε) =
      1 / 2 * (∫⁻ x, captureTime S (loiterer ε x) ∂ρ +
        ∫⁻ x, captureTime S (-loiterer ε x) ∂ρ) := by
  rw [hPhi, lintegral_smul_measure, lintegral_add_measure,
    lintegral_map (s5_measurable_captureTime S) (s5_measurable_toHider_loiterer hε),
    lintegral_map (s5_measurable_captureTime S) (s5_measurable_toHider_neg_loiterer hε)]
  simp only [s5_toHider_of_mem (s5_loiterer_mem hε _),
    s5_toHider_of_mem (neg_mem_hiderPaths (s5_loiterer_mem hε _)), smul_eq_mul]

lemma s5_lintegral_symDiracH (S H₀ : C(ℝ≥0, ℝ)) (h : H₀ ∈ hiderPaths) :
    ∫⁻ H, captureTime S H ∂(symDiracH H₀) =
      1 / 2 * (captureTime S H₀ + captureTime S (-H₀)) := by
  rw [symDiracH, lintegral_smul_measure, lintegral_add_measure, lintegral_dirac, lintegral_dirac,
    s5_toHider_of_mem h, s5_toHider_of_mem (neg_mem_hiderPaths h), smul_eq_mul]

lemma s5_lintegral_uniformOn (a b : ℝ) (g : ℝ → ℝ≥0∞) :
    ∫⁻ x, g x ∂(uniformOn a b) = (ENNReal.ofReal (b - a))⁻¹ * ∫⁻ x in Set.Icc a b, g x := by
  rw [uniformOn, lintegral_smul_measure, smul_eq_mul]

lemma s5_hiderE_mem : hiderE ∈ hiderPaths := searcherPaths_subset_hiderPaths hiderE_mem

/-- The expected capture time against `γ`. -/
lemma s5_lintegral_gamma {ε : ℝ} (hε : 0 ≤ ε) (S : C(ℝ≥0, ℝ)) :
    ∫⁻ H, captureTime S H ∂(gamma ε) =
      3 / 11 * (1 / 2 * (captureTime S hiderE + captureTime S (-hiderE))) +
      8 / 11 * (1 / 2 * ((ENNReal.ofReal (1 - ε - ε))⁻¹ *
          (∫⁻ x in Set.Icc ε (1 - ε), captureTime S (loiterer ε x)) +
        (ENNReal.ofReal (1 - ε - ε))⁻¹ *
          ∫⁻ x in Set.Icc ε (1 - ε), captureTime S (-loiterer ε x))) := by
  rw [gamma, lintegral_add_measure, lintegral_smul_measure, lintegral_smul_measure,
    s5_lintegral_symDiracH S hiderE s5_hiderE_mem, s5_lintegral_hPhi hε,
    s5_lintegral_uniformOn, s5_lintegral_uniformOn, smul_eq_mul, smul_eq_mul]

lemma s5_uniformOn_univ {a b : ℝ} (hab : a < b) : uniformOn a b Set.univ = 1 := by
  rw [uniformOn, Measure.smul_apply, Measure.restrict_apply_univ, Real.volume_Icc, smul_eq_mul,
    ENNReal.inv_mul_cancel (ENNReal.ofReal_pos.mpr (sub_pos.mpr hab)).ne' ENNReal.ofReal_ne_top]

lemma s5_isProb_gamma {ε : ℝ} (hε : 0 ≤ ε) (hε' : ε < 1 / 2) :
    IsProbabilityMeasure (gamma ε) := by
  constructor
  have hU : uniformOn ε (1 - ε) Set.univ = 1 := s5_uniformOn_univ (by linarith)
  simp only [gamma, hPhi, symDiracH, Measure.add_apply, Measure.smul_apply, smul_eq_mul,
    measure_univ, Measure.map_apply (s5_measurable_toHider_loiterer hε) MeasurableSet.univ,
    Measure.map_apply (s5_measurable_toHider_neg_loiterer hε) MeasurableSet.univ,
    Set.preimage_univ, hU]
  rw [one_add_one_eq_two, one_div, ENNReal.inv_mul_cancel two_ne_zero ENNReal.ofNat_ne_top,
    mul_one, mul_one, ENNReal.div_add_div_same, show (3 : ℝ≥0∞) + 8 = 11 by norm_num]
  exact ENNReal.div_self (by norm_num) (by norm_num)

/-! ### Arithmetic in `ℝ≥0∞` -/

lemma s5_ofReal_ratio (p q : ℕ) (hq : 0 < q) :
    ((p : ℝ≥0∞) / q) = ENNReal.ofReal ((p : ℝ) / q) := by
  rw [ENNReal.ofReal_div_of_pos (by exact_mod_cast hq)]
  simp

lemma s5_combine {a b c d : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c) (hd : 0 ≤ d) :
    (3 / 11 : ℝ≥0∞) * (1 / 2 * (ENNReal.ofReal a + ENNReal.ofReal b)) +
      8 / 11 * (1 / 2 * (ENNReal.ofReal c + ENNReal.ofReal d)) =
      ENNReal.ofReal ((3 * (a + b) + 8 * (c + d)) / 22) := by
  have h3 : (3 / 11 : ℝ≥0∞) = ENNReal.ofReal (3 / 11) := by
    exact_mod_cast s5_ofReal_ratio 3 11 (by norm_num)
  have h8 : (8 / 11 : ℝ≥0∞) = ENNReal.ofReal (8 / 11) := by
    exact_mod_cast s5_ofReal_ratio 8 11 (by norm_num)
  have h2 : (1 / 2 : ℝ≥0∞) = ENNReal.ofReal (1 / 2) := by
    rw [ENNReal.ofReal_div_of_pos (by norm_num)]; simp
  rw [h3, h8, h2, ← ENNReal.ofReal_add ha hb, ← ENNReal.ofReal_add hc hd,
    ← ENNReal.ofReal_mul (by norm_num), ← ENNReal.ofReal_mul (by norm_num),
    ← ENNReal.ofReal_mul (by norm_num), ← ENNReal.ofReal_mul (by norm_num),
    ← ENNReal.ofReal_add (by positivity) (by positivity)]
  congr 1
  ring

/-! ### The sweeper `A` against `γ` -/

lemma s5_sweeperA_apply_of_le {t : ℝ≥0} (ht : (t : ℝ) ≤ 2) : sweeperA t = 1 - t := by
  simp only [sweeperA, pathOf_apply]
  exact Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith [NNReal.coe_nonneg t]⟩

lemma s5_loiterer_late {ε x : ℝ} {t : ℝ≥0} (ht : 1 - 2 * ε ≤ (t : ℝ)) :
    loiterer ε x t = min 1 (t - 1 + 3 * ε) := by
  rw [s5_loiterer_apply, max_eq_right]
  exact (min_le_right _ _).trans (by linarith)

lemma s5_loiterer_early {ε x : ℝ} (hxε : ε ≤ x) (hx1 : x ≤ 1) {t : ℝ≥0}
    (ht : (t : ℝ) ≤ 1 - 2 * ε) : loiterer ε x t = min x (1 - ε - t) := by
  have h1 : t - 1 + 3 * ε ≤ min x (1 - ε - t) := le_min (by linarith) (by linarith)
  have h2 : min x (1 - ε - t) ≤ 1 := (min_le_left _ _).trans hx1
  rw [s5_loiterer_apply, max_eq_left h1, min_eq_right h2]

lemma s5_coe_le_ofReal {t : ℝ≥0} {r : ℝ} (h : (t : ℝ) ≤ r) : (t : ℝ≥0∞) ≤ ENNReal.ofReal r := by
  rw [← ENNReal.ofReal_coe_nnreal]; exact ENNReal.ofReal_le_ofReal h

lemma s5_le_of_ofReal_le {t : ℝ≥0} {r : ℝ} (h : ENNReal.ofReal r ≤ t) : r ≤ t := by
  rwa [← ENNReal.ofReal_coe_nnreal, ENNReal.ofReal_le_ofReal_iff (NNReal.coe_nonneg t)] at h

lemma s5_T_A_E : captureTime sweeperA hiderE ≤ ENNReal.ofReal 0 := by
  have h : sweeperA 0 = hiderE 0 := by
    rw [s5_sweeperA_apply_of_le (by simp)]; simp [hiderE]
  exact (captureTime_le h).trans (s5_coe_le_ofReal (by simp))

lemma s5_T_A_negE : captureTime sweeperA (-hiderE) ≤ ENNReal.ofReal 2 := by
  have h : sweeperA 2 = (-hiderE) 2 := by
    rw [s5_sweeperA_apply_of_le (by norm_num)]; simp [hiderE]; norm_num
  exact (captureTime_le h).trans (s5_coe_le_ofReal (by simp))

lemma s5_T_A_loiterer {ε x : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 4) :
    captureTime sweeperA (loiterer ε x) ≤ ENNReal.ofReal 1 := by
  set t₀ : ℝ≥0 := ⟨1 - 3 * ε / 2, by linarith⟩
  have ht₀ : (t₀ : ℝ) = 1 - 3 * ε / 2 := rfl
  have h : sweeperA t₀ = loiterer ε x t₀ := by
    rw [s5_sweeperA_apply_of_le (by rw [ht₀]; linarith), s5_loiterer_late (by rw [ht₀]; linarith),
      ht₀, min_eq_right (by linarith)]
    ring
  exact (captureTime_le h).trans (s5_coe_le_ofReal (by rw [ht₀]; linarith))

lemma s5_T_A_neg_loiterer {ε x : ℝ} (hε : 0 < ε) :
    captureTime sweeperA (-loiterer ε x) ≤ ENNReal.ofReal 2 := by
  have h : sweeperA 2 = (-loiterer ε x) 2 := by
    rw [s5_sweeperA_apply_of_le (by norm_num), ContinuousMap.neg_apply,
      s5_loiterer_late (by norm_num; linarith), min_eq_left (by norm_num; linarith)]
    norm_num
  exact (captureTime_le h).trans (s5_coe_le_ofReal (by simp))

lemma s5_avg_le {ε : ℝ} (hε' : ε < 1 / 2) {g : ℝ → ℝ≥0∞} {c : ℝ}
    (h : ∀ x ∈ Set.Icc ε (1 - ε), g x ≤ ENNReal.ofReal c) :
    (ENNReal.ofReal (1 - ε - ε))⁻¹ * ∫⁻ x in Set.Icc ε (1 - ε), g x ≤ ENNReal.ofReal c := by
  have hu : ENNReal.ofReal (1 - ε - ε) ≠ 0 := (ENNReal.ofReal_pos.mpr (by linarith)).ne'
  calc (ENNReal.ofReal (1 - ε - ε))⁻¹ * ∫⁻ x in Set.Icc ε (1 - ε), g x
      ≤ (ENNReal.ofReal (1 - ε - ε))⁻¹ * ∫⁻ x in Set.Icc ε (1 - ε), ENNReal.ofReal c :=
        mul_le_mul_right (setLIntegral_mono' measurableSet_Icc h) _
    _ = ENNReal.ofReal c := by
        rw [setLIntegral_const, Real.volume_Icc, mul_comm (ENNReal.ofReal c), ← mul_assoc,
          ENNReal.inv_mul_cancel hu ENNReal.ofReal_ne_top, one_mul]

/-- The upper bound: against `γ`, the sweeper `A` has expected capture time at most `15/11`. -/
lemma s5_upper {ε : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 4) :
    ∫⁻ H, captureTime sweeperA H ∂(gamma ε) ≤ 15 / 11 := by
  rw [s5_lintegral_gamma hε.le]
  calc _ ≤ 3 / 11 * (1 / 2 * (ENNReal.ofReal 0 + ENNReal.ofReal 2)) +
        8 / 11 * (1 / 2 * (ENNReal.ofReal 1 + ENNReal.ofReal 2)) := by
        gcongr
        · exact s5_T_A_E
        · exact s5_T_A_negE
        · exact s5_avg_le (by linarith) fun x _ => s5_T_A_loiterer hε hε1
        · exact s5_avg_le (by linarith) fun x _ => s5_T_A_neg_loiterer hε
    _ = 15 / 11 := by
        rw [s5_combine (by norm_num) (by norm_num) (by norm_num) (by norm_num),
          show (15 / 11 : ℝ≥0∞) = ENNReal.ofReal (15 / 11) by
            exact_mod_cast s5_ofReal_ratio 15 11 (by norm_num)]
        norm_num

/-- Lebesgue measure on `ℝ` is invariant under `x ↦ -x`. -/
lemma s5_volume_neg (A : Set ℝ) : volume (-A) = volume A := by
  have := Real.volume_preimage_mul_left (a := -1) (by norm_num) A
  rw [show ((fun x : ℝ => -1 * x) ⁻¹' A) = -A by ext x; simp [Set.mem_neg]] at this
  rw [this]; simp

/-! ### Elementary facts about a searcher path against the loiterers -/

section s5_lemmas

variable {ε : ℝ} {S : C(ℝ≥0, ℝ)}

lemma s5_lip (hS : S ∈ searcherPaths) {s t : ℝ≥0} (h : s ≤ t) :
    S t ≤ S s + (t - s) ∧ S s - (t - s) ≤ S t := by
  have h1 := hS.2 t s
  have h2 : (0 : ℝ) ≤ t - s := sub_nonneg.mpr (NNReal.coe_le_coe.mpr h)
  rw [abs_of_nonneg h2] at h1
  constructor <;> linarith [(abs_le.mp h1).1, (abs_le.mp h1).2]

/-- Once the searcher is at or ahead of the front `F(t) = 1 - ε - t`, it stays there. -/
lemma s5_contact (hS : S ∈ searcherPaths) {τ t : ℝ≥0} (hτ : 1 - ε - τ ≤ S τ) (ht : τ ≤ t) :
    1 - ε - t ≤ S t := by
  have := (s5_lip hS ht).2
  linarith

lemma s5_exists_lt {H : C(ℝ≥0, ℝ)} {r : ℝ} (h : captureTime S H < ENNReal.ofReal r) :
    ∃ s : ℝ≥0, (s : ℝ) < r ∧ S s = H s := by
  obtain ⟨s, hs, he⟩ := exists_eq_captureTime (ne_top_of_lt h)
  refine ⟨s, ?_, hs⟩
  rw [he, ← ENNReal.ofReal_coe_nnreal, ENNReal.ofReal_lt_ofReal_iff'] at h
  exact h.1

lemma s5_exists_le {H : C(ℝ≥0, ℝ)} {r : ℝ} (hr : 0 ≤ r) (h : captureTime S H ≤ ENNReal.ofReal r) :
    ∃ s : ℝ≥0, (s : ℝ) ≤ r ∧ S s = H s := by
  obtain ⟨s, hs, he⟩ := exists_eq_captureTime (ne_top_of_le_ne_top ENNReal.ofReal_ne_top h)
  refine ⟨s, ?_, hs⟩
  rwa [he, ← ENNReal.ofReal_coe_nnreal, ENNReal.ofReal_le_ofReal_iff hr] at h

lemma s5_attained {H : C(ℝ≥0, ℝ)} {a : ℝ} (ha : captureTime S H = ENNReal.ofReal a)
    (ha0 : 0 ≤ a) : ∃ s : ℝ≥0, S s = H s ∧ (s : ℝ) = a := by
  obtain ⟨s, hs, hse⟩ := exists_eq_captureTime
    (show captureTime S H ≠ ⊤ by rw [ha]; exact ENNReal.ofReal_ne_top)
  refine ⟨s, hs, ?_⟩
  rw [ha, ← ENNReal.ofReal_coe_nnreal] at hse
  exact ((ENNReal.ofReal_eq_ofReal_iff ha0 (NNReal.coe_nonneg s)).mp hse).symm

lemma s5_hiderE_apply (t : ℝ≥0) : hiderE t = 1 := rfl

/-- Lemma B (positive loiterers): before the exit time, a loiterer is met only where it sits. -/
lemma s5_visited_pos (hε : 0 ≤ ε) {x : ℝ} (hx : x ∈ Set.Icc ε (1 - ε)) {s : ℝ≥0}
    (hs : (s : ℝ) ≤ 1 - 2 * ε) (hin : |S s| < 1 - ε - s) (h : S s = loiterer ε x s) :
    S s = x := by
  rw [s5_loiterer_early hx.1 (by linarith [hx.2]) hs] at h
  rcases min_choice x (1 - ε - s) with h' | h' <;> rw [h'] at h
  · exact h
  · linarith [le_abs_self (S s)]

/-- Lemma B (negative loiterers). -/
lemma s5_visited_neg (hε : 0 ≤ ε) {x : ℝ} (hx : x ∈ Set.Icc ε (1 - ε)) {s : ℝ≥0}
    (hs : (s : ℝ) ≤ 1 - 2 * ε) (hin : |S s| < 1 - ε - s) (h : S s = (-loiterer ε x) s) :
    S s = -x := by
  rw [ContinuousMap.neg_apply, s5_loiterer_early hx.1 (by linarith [hx.2]) hs] at h
  rcases min_choice x (1 - ε - s) with h' | h' <;> rw [h'] at h
  · exact h
  · linarith [neg_abs_le (S s)]

/-- Lemma B, measure form: the loiterers met by time `r` before the exit time sit in `S([0, r])`,
an interval of length at most `r`. -/
lemma s5_measure_visited (hS : S ∈ searcherPaths) (hε : 0 < ε) {r : ℝ}
    {A₁ A₂ : Set ℝ} (hA₁ : A₁ ⊆ Set.Icc ε (1 - ε)) (hA₂ : A₂ ⊆ Set.Icc ε (1 - ε))
    (hm : MeasurableSet A₂)
    (h₁ : ∀ x ∈ A₁, ∃ s : ℝ≥0, (s : ℝ) ≤ r ∧ S s = x)
    (h₂ : ∀ x ∈ A₂, ∃ s : ℝ≥0, (s : ℝ) ≤ r ∧ S s = -x) :
    volume A₁ + volume A₂ ≤ ENNReal.ofReal r := by
  set R : Set ℝ := {z | ∃ s : ℝ≥0, (s : ℝ) ≤ r ∧ S s = z} with hR
  have hdisj : Disjoint A₁ (-A₂) := by
    rw [Set.disjoint_left]
    intro z hz hz'
    have h1 := (hA₁ hz).1
    have h2 := (hA₂ (Set.mem_neg.mp hz')).1
    linarith
  calc volume A₁ + volume A₂ = volume A₁ + volume (-A₂) := by rw [s5_volume_neg]
    _ = volume (A₁ ∪ -A₂) := (measure_union hdisj hm.neg).symm
    _ ≤ volume R := by
        apply measure_mono
        apply Set.union_subset
        · intro z hz; exact h₁ z hz
        · intro z hz
          obtain ⟨s, hs, he⟩ := h₂ (-z) (Set.mem_neg.mp hz)
          exact ⟨s, hs, by rw [he, neg_neg]⟩
    _ ≤ Metric.ediam R := Real.volume_le_diam R
    _ ≤ ENNReal.ofReal r := by
        apply Metric.ediam_le
        rintro _ ⟨s, hs, rfl⟩ _ ⟨s', hs', rfl⟩
        rw [edist_dist, Real.dist_eq]
        apply ENNReal.ofReal_le_ofReal
        refine (hS.2 s s').trans ?_
        rw [abs_le]; constructor <;> linarith [NNReal.coe_nonneg s, NNReal.coe_nonneg s']

/-- Lemma E: meeting the front `F(t)` at time `t` costs `2t + ε` to reach `+1`. -/
lemma s5_lemmaE (hε : 0 < ε) (hS : S ∈ searcherPaths) {t : ℝ≥0} (ht : S t = 1 - ε - t) :
    ENNReal.ofReal (2 * t + ε) ≤ captureTime S hiderE := by
  rw [le_captureTime_iff]
  intro s hs
  have h1 : S s = 1 := by rw [hs]; rfl
  rw [← ENNReal.ofReal_coe_nnreal]
  apply ENNReal.ofReal_le_ofReal
  rcases le_total s t with h | h
  · have := (s5_lip hS h).2
    linarith [NNReal.coe_nonneg s]
  · have := (s5_lip hS h).1
    linarith

/-- Lemma D: after contact with the front, the unvisited negative loiterers are met at `-1`. -/
lemma s5_neg_after (hε : 0 < ε) (hS : S ∈ searcherPaths) {τ : ℝ≥0}
    (hτ : 1 - ε - τ ≤ S τ) {x : ℝ} (hx : x ∈ Set.Icc ε (1 - ε))
    (hT : ENNReal.ofReal τ ≤ captureTime S (-loiterer ε x)) :
    captureTime S (-hiderE) ≤ captureTime S (-loiterer ε x) := by
  rw [le_captureTime_iff]
  intro t ht
  have htτ : τ ≤ t := by
    have := s5_le_of_ofReal_le (hT.trans (captureTime_le ht))
    exact_mod_cast this
  have hc := s5_contact hS hτ htτ
  have ht2 : 2 - ε ≤ (t : ℝ) := by
    by_contra hlt
    push Not at hlt
    rw [ContinuousMap.neg_apply] at ht
    rcases le_total (t : ℝ) (1 - 2 * ε) with h1 | h1
    · rw [s5_loiterer_early hx.1 (by linarith [hx.2]) h1] at ht
      have : ε ≤ min x (1 - ε - t) := le_min hx.1 (by linarith)
      linarith
    · rw [s5_loiterer_late h1] at ht
      rcases min_choice 1 ((t : ℝ) - 1 + 3 * ε) with h' | h' <;> rw [h'] at ht <;> linarith
  have h' : S t = (-hiderE) t := by
    rw [ht, ContinuousMap.neg_apply, ContinuousMap.neg_apply, s5_loiterer_late (by linarith),
      min_eq_left (by linarith), s5_hiderE_apply]
  exact captureTime_le h'

/-- After contact with the front, `-1` is not reached before `2 - ε`. -/
lemma s5_b_ge (hε : 0 < ε) (hS : S ∈ searcherPaths) {τ : ℝ≥0} (hτ : 1 - ε - τ ≤ S τ)
    (hin : ∀ s : ℝ≥0, s < τ → |S s| < 1 - ε - s) :
    ENNReal.ofReal (2 - ε) ≤ captureTime S (-hiderE) := by
  rw [le_captureTime_iff]
  intro t ht
  have h1 : S t = -1 := by rw [ht, ContinuousMap.neg_apply, s5_hiderE_apply]
  rw [← ENNReal.ofReal_coe_nnreal]
  apply ENNReal.ofReal_le_ofReal
  rcases lt_or_ge t τ with h | h
  · have := hin t h
    rw [h1, abs_neg, abs_one] at this
    linarith [NNReal.coe_nonneg t]
  · have := s5_contact hS hτ h
    linarith

/-- The lower bound `ℓ` of Lemma F: below `1 - a/2 - ε` the threshold `c_min`. -/
noncomputable def s5_cmin (ε a : ℝ) : ℝ := if a < 2 - 3 * ε then 1 + a / 2 - 2 * ε else 1 - 2 * ε

/-- The lower bound `ℓ(x)` of Lemma F for the capture time of an unvisited positive loiterer. -/
noncomputable def s5_ell (ε a τ x : ℝ) : ℝ :=
  if x < 1 - a / 2 - ε then s5_cmin ε a else if x < 1 - ε - τ then 1 - x - ε else τ

/-- Lemma F: after contact with the front, an unvisited positive loiterer `P_x` is met no
earlier than `ℓ(x)`. -/
lemma s5_pos_after (hε : 0 < ε) (hS : S ∈ searcherPaths) {τ : ℝ≥0}
    (hτ : 1 - ε - τ ≤ S τ) {a : ℝ} (ha : captureTime S hiderE = ENNReal.ofReal a) (ha0 : 0 ≤ a)
    (hτa : 2 * (τ : ℝ) ≤ a) {x : ℝ} (hx : x ∈ Set.Icc ε (1 - ε))
    (hT : ENNReal.ofReal τ ≤ captureTime S (loiterer ε x)) :
    ENNReal.ofReal (s5_ell ε a τ x) ≤ captureTime S (loiterer ε x) := by
  rw [le_captureTime_iff]
  intro t ht
  have htτ' : (τ : ℝ) ≤ t := s5_le_of_ofReal_le (hT.trans (captureTime_le ht))
  have htτ : τ ≤ t := by exact_mod_cast htτ'
  have hc := s5_contact hS hτ htτ
  -- (ii): an immobile loiterer behind the searcher is not met before it starts running
  have hii : x < 1 - ε - τ → 1 - x - ε ≤ t := by
    intro _
    by_contra hlt
    push Not at hlt
    rw [s5_loiterer_early hx.1 (by linarith [hx.2]) (by linarith [hx.1]),
      min_eq_left (by linarith)] at ht
    linarith
  -- (iii): a meeting time `t ≤ 1 - 2ε` is a meeting with the front, so Lemma E applies
  have hE : (t : ℝ) ≤ 1 - 2 * ε → 2 * t + ε ≤ a := by
    intro htu
    have hle : loiterer ε x t ≤ 1 - ε - t := by
      rw [s5_loiterer_early hx.1 (by linarith [hx.2]) htu]; exact min_le_right _ _
    have hSt : S t = 1 - ε - t := le_antisymm (by linarith) hc
    have := s5_lemmaE hε hS hSt
    rwa [ha, ENNReal.ofReal_le_ofReal_iff ha0] at this
  rw [← ENNReal.ofReal_coe_nnreal]
  apply ENNReal.ofReal_le_ofReal
  unfold s5_ell
  split_ifs with h1 h2
  · have h3 := hii (by linarith)
    have hgt : 1 - 2 * ε < t := by
      by_contra hle
      push Not at hle
      have := hE hle
      linarith
    unfold s5_cmin
    split_ifs with h4
    · -- (iv)
      rcases le_or_gt (2 - 3 * ε) (t : ℝ) with h5 | h5
      · linarith
      · rw [s5_loiterer_late hgt.le, min_eq_right (by linarith)] at ht
        obtain ⟨s, hs, hsa⟩ := s5_attained ha ha0
        have hs1 : S s = 1 := by rw [hs]; rfl
        rcases le_total t s with h6 | h6
        · have := (s5_lip hS h6).1
          linarith
        · have := (s5_lip hS h6).2
          linarith
    · linarith
  · exact hii h2
  · exact htτ'

/-- If the searcher is strictly inside the diamond before `τ > 0`, then `|S τ| ≤ F(τ)`. -/
lemma s5_le_front (hS : S ∈ searcherPaths) {τ : ℝ≥0} (hτ0 : 0 < τ)
    (hin : ∀ s : ℝ≥0, s < τ → |S s| < 1 - ε - s) : S τ ≤ 1 - ε - τ := by
  by_contra hgt
  push Not at hgt
  set δ := S τ - (1 - ε - τ) with hδ
  set s : ℝ≥0 := Real.toNNReal (τ - δ / 4) with hs_def
  have hs : (s : ℝ) = max (τ - δ / 4) 0 := Real.coe_toNNReal' _
  have hτ0' : (0 : ℝ) < τ := by exact_mod_cast hτ0
  have hsτ : s < τ := by
    rw [← NNReal.coe_lt_coe, hs]; exact max_lt (by linarith) hτ0'
  have h1 := (s5_lip hS hsτ.le).1
  have h2 := hin s hsτ
  have h3 : (τ : ℝ) - δ / 4 ≤ s := by rw [hs]; exact le_max_left _ _
  linarith [le_abs_self (S s)]

/-- The exit time `τ` from the diamond `|p| < F(t)`, when the searcher leaves it by `1 - 2ε`. -/
lemma s5_exists_tau (h : ¬ ∀ s : ℝ≥0, (s : ℝ) ≤ 1 - 2 * ε → |S s| < 1 - ε - s) :
    ∃ τ : ℝ≥0, (τ : ℝ) ≤ 1 - 2 * ε ∧ 1 - ε - τ ≤ |S τ| ∧
      ∀ s : ℝ≥0, s < τ → |S s| < 1 - ε - s := by
  push Not at h
  obtain ⟨t₀, ht₀, ht₀'⟩ := h
  set Z : Set ℝ≥0 := {s | 1 - ε - s ≤ |S s|} with hZdef
  have hZ : IsClosed Z := isClosed_le (by fun_prop) (by fun_prop)
  have hne : Z.Nonempty := ⟨t₀, ht₀'⟩
  refine ⟨sInf Z, ?_, hZ.csInf_mem hne (OrderBot.bddBelow Z), fun s hs => ?_⟩
  · have : sInf Z ≤ t₀ := csInf_le (OrderBot.bddBelow Z) ht₀'
    exact le_trans (NNReal.coe_le_coe.mpr this) ht₀
  · by_contra hge
    push Not at hge
    exact absurd (csInf_le (OrderBot.bddBelow Z) hge) (not_le.mpr hs)

/-- Case II: after `1 - 2ε` both bunches run outwards strictly ahead of the searcher. -/
lemma s5_caseII_after (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hS : S ∈ searcherPaths)
    (hin : ∀ s : ℝ≥0, (s : ℝ) ≤ 1 - 2 * ε → |S s| < 1 - ε - s) {t : ℝ≥0}
    (ht : 1 - 2 * ε ≤ (t : ℝ)) : S t < t - 1 + 3 * ε ∧ -(t - 1 + 3 * ε) < S t := by
  set u : ℝ≥0 := ⟨1 - 2 * ε, by linarith⟩ with hu_def
  have hu : (u : ℝ) = 1 - 2 * ε := rfl
  have hut : u ≤ t := by rw [← NNReal.coe_le_coe, hu]; exact ht
  have h1 := hin u (le_of_eq hu)
  rw [hu] at h1
  have h2 := s5_lip hS hut
  rw [hu] at h2
  constructor <;> linarith [(abs_lt.mp h1).1, (abs_lt.mp h1).2, h2.1, h2.2]

lemma s5_caseII_pos (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hS : S ∈ searcherPaths)
    (hin : ∀ s : ℝ≥0, (s : ℝ) ≤ 1 - 2 * ε → |S s| < 1 - ε - s) {x : ℝ}
    (hT : ENNReal.ofReal (1 - 2 * ε) ≤ captureTime S (loiterer ε x)) :
    captureTime S hiderE ≤ captureTime S (loiterer ε x) := by
  rw [le_captureTime_iff]
  intro t ht
  have htu : 1 - 2 * ε ≤ (t : ℝ) := s5_le_of_ofReal_le (hT.trans (captureTime_le ht))
  obtain ⟨h1, h2⟩ := s5_caseII_after hε hε1 hS hin htu
  rw [s5_loiterer_late htu] at ht
  rcases min_choice 1 ((t : ℝ) - 1 + 3 * ε) with h' | h' <;> rw [h'] at ht
  · exact captureTime_le (show S t = hiderE t by rw [ht]; rfl)
  · linarith

lemma s5_caseII_neg (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hS : S ∈ searcherPaths)
    (hin : ∀ s : ℝ≥0, (s : ℝ) ≤ 1 - 2 * ε → |S s| < 1 - ε - s) {x : ℝ}
    (hT : ENNReal.ofReal (1 - 2 * ε) ≤ captureTime S (-loiterer ε x)) :
    captureTime S (-hiderE) ≤ captureTime S (-loiterer ε x) := by
  rw [le_captureTime_iff]
  intro t ht
  have htu : 1 - 2 * ε ≤ (t : ℝ) := s5_le_of_ofReal_le (hT.trans (captureTime_le ht))
  obtain ⟨h1, h2⟩ := s5_caseII_after hε hε1 hS hin htu
  rw [ContinuousMap.neg_apply, s5_loiterer_late htu] at ht
  rcases min_choice 1 ((t : ℝ) - 1 + 3 * ε) with h' | h' <;> rw [h'] at ht
  · exact captureTime_le
      (show S t = (-hiderE) t by rw [ht, ContinuousMap.neg_apply, s5_hiderE_apply])
  · linarith

lemma s5_caseII_a (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hS : S ∈ searcherPaths)
    (hin : ∀ s : ℝ≥0, (s : ℝ) ≤ 1 - 2 * ε → |S s| < 1 - ε - s) :
    ENNReal.ofReal (2 - 3 * ε) ≤ captureTime S hiderE := by
  rw [le_captureTime_iff]
  intro t ht
  have h1 : S t = 1 := by rw [ht]; rfl
  rw [← ENNReal.ofReal_coe_nnreal]
  apply ENNReal.ofReal_le_ofReal
  rcases le_or_gt (t : ℝ) (1 - 2 * ε) with h | h
  · have := hin t h
    rw [h1, abs_one] at this
    linarith [NNReal.coe_nonneg t]
  · have := (s5_caseII_after hε hε1 hS hin h.le).1
    linarith

lemma s5_caseII_b (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hS : S ∈ searcherPaths)
    (hin : ∀ s : ℝ≥0, (s : ℝ) ≤ 1 - 2 * ε → |S s| < 1 - ε - s) :
    ENNReal.ofReal (2 - 3 * ε) ≤ captureTime S (-hiderE) := by
  rw [le_captureTime_iff]
  intro t ht
  have h1 : S t = -1 := by rw [ht, ContinuousMap.neg_apply, s5_hiderE_apply]
  rw [← ENNReal.ofReal_coe_nnreal]
  apply ENNReal.ofReal_le_ofReal
  rcases le_or_gt (t : ℝ) (1 - 2 * ε) with h | h
  · have := hin t h
    rw [h1, abs_neg, abs_one] at this
    linarith [NNReal.coe_nonneg t]
  · have := (s5_caseII_after hε hε1 hS hin h.le).2
    linarith

/-- The two ends are at distance `2`. -/
lemma s5_ends (hS : S ∈ searcherPaths) {a b : ℝ} (ha : captureTime S hiderE = ENNReal.ofReal a)
    (hb : captureTime S (-hiderE) = ENNReal.ofReal b) (ha0 : 0 ≤ a) (hb0 : 0 ≤ b) :
    a + 2 ≤ b ∨ b + 2 ≤ a := by
  obtain ⟨s, hs, hsa⟩ := s5_attained ha ha0
  obtain ⟨s', hs', hsb⟩ := s5_attained hb hb0
  have h1 : S s = 1 := by rw [hs]; rfl
  have h2 : S s' = -1 := by rw [hs', ContinuousMap.neg_apply, s5_hiderE_apply]
  have := hS.2 s s'
  rw [h1, h2, hsa, hsb, show (1 : ℝ) - -1 = 2 by norm_num, abs_two] at this
  rcases le_abs.mp this with h | h
  · right; linarith
  · left; linarith

end s5_lemmas

/-! ### Integrals: affine functions, the layer cake bound, splitting off the visited set -/

lemma s5_integral_id (a b : ℝ) : ∫ x in a..b, x = (b ^ 2 - a ^ 2) / 2 := by
  have h1 : ∫ x in a..b, (a + b - x) = ∫ x in a..b, x := by
    rw [intervalIntegral.integral_comp_sub_left (fun x => x)]
    ring_nf
  have h2 : ∫ x in a..b, (a + b - x) = (b - a) * (a + b) - ∫ x in a..b, x := by
    rw [intervalIntegral.integral_sub (f := fun _ => a + b) (g := fun x => x)
      intervalIntegrable_const (continuous_id.intervalIntegrable a b)]
    simp; ring
  nlinarith

lemma s5_lintegral_affine {a b c₀ c₁ : ℝ} {f : ℝ → ℝ} (hab : a ≤ b)
    (hf : ∀ x ∈ Set.Icc a b, f x = c₀ + c₁ * x) (hnn : ∀ x ∈ Set.Icc a b, 0 ≤ c₀ + c₁ * x) :
    ∫⁻ x in Set.Icc a b, ENNReal.ofReal (f x) =
      ENNReal.ofReal (c₀ * (b - a) + c₁ * (b ^ 2 - a ^ 2) / 2) := by
  rw [setLIntegral_congr_fun measurableSet_Icc (g := fun x => ENNReal.ofReal (c₀ + c₁ * x))
    (fun x hx => by rw [hf x hx])]
  rw [← ofReal_integral_eq_lintegral_ofReal]
  · congr 1
    rw [integral_Icc_eq_integral_Ioc, ← intervalIntegral.integral_of_le hab]
    have e : ∫ x in a..b, (c₀ + c₁ * x) = (∫ _ in a..b, c₀) + ∫ x in a..b, c₁ * x :=
      intervalIntegral.integral_add intervalIntegrable_const
        ((by fun_prop : Continuous fun x : ℝ => c₁ * x).intervalIntegrable a b)
    rw [e, intervalIntegral.integral_const, intervalIntegral.integral_const_mul, s5_integral_id]
    simp only [smul_eq_mul]
    ring
  · exact (by fun_prop : Continuous fun x : ℝ => c₀ + c₁ * x).integrableOn_Icc
  · exact (ae_restrict_iff' measurableSet_Icc).mpr (Filter.Eventually.of_forall hnn)

lemma s5_layer_aux (μ : Measure ℝ) [SFinite μ] {f : ℝ → ℝ≥0∞} (hf : Measurable f) (L : ℝ) :
    ∫⁻ t in Set.Ico 0 L, μ {x | ENNReal.ofReal t < f x} ≤ ∫⁻ x, f x ∂μ := by
  set E : Set (ℝ × ℝ) := {p | ENNReal.ofReal p.1 < f p.2} with hE
  have hEm : MeasurableSet E :=
    measurableSet_lt (ENNReal.measurable_ofReal.comp measurable_fst) (hf.comp measurable_snd)
  have h1 : ∀ t, μ {x | ENNReal.ofReal t < f x} = ∫⁻ x, E.indicator 1 (t, x) ∂μ := by
    intro t
    rw [← lintegral_indicator_one (measurableSet_lt measurable_const hf)]
    rfl
  have h2 : ∀ x, ∫⁻ t in Set.Ico 0 L, E.indicator 1 (t, x) ≤ f x := by
    intro x
    have e : ∫⁻ t in Set.Ico 0 L, E.indicator 1 (t, x) =
        ∫⁻ t in Set.Ico 0 L, {t : ℝ | ENNReal.ofReal t < f x}.indicator 1 t := rfl
    rw [e, lintegral_indicator_one (measurableSet_lt ENNReal.measurable_ofReal measurable_const),
      Measure.restrict_apply (measurableSet_lt ENNReal.measurable_ofReal measurable_const)]
    by_cases hfx : f x = ⊤
    · rw [hfx]; exact le_top
    · calc volume ({t : ℝ | ENNReal.ofReal t < f x} ∩ Set.Ico 0 L)
          ≤ volume (Set.Ico 0 (f x).toReal) := by
            apply measure_mono
            rintro t ⟨ht, ht0⟩
            exact ⟨ht0.1, (ENNReal.ofReal_lt_iff_lt_toReal ht0.1 hfx).mp ht⟩
        _ = f x := by rw [Real.volume_Ico, sub_zero, ENNReal.ofReal_toReal hfx]
  rw [lintegral_congr (fun t => h1 t)]
  have hmeas : AEMeasurable (Function.uncurry fun t x => E.indicator (1 : ℝ × ℝ → ℝ≥0∞) (t, x))
      ((volume.restrict (Set.Ico (0 : ℝ) L)).prod μ) := by
    have : Function.uncurry (fun t x => E.indicator (1 : ℝ × ℝ → ℝ≥0∞) (t, x)) =
        E.indicator 1 := by
      funext p; rfl
    rw [this]
    exact (measurable_one.indicator hEm).aemeasurable
  rw [lintegral_lintegral_swap hmeas]
  exact lintegral_mono fun x => h2 x

/-- The layer cake bound: if at most `t` of the mass of `C₁ ⊔ C₂` is met by time `t`, the total
capture time on `C₁ ⊔ C₂` is at least `L²/2`, `L` the total mass. -/
lemma s5_layer_cake {f g : ℝ → ℝ≥0∞} (hf : Measurable f) (hg : Measurable g) {C₁ C₂ : Set ℝ}
    {L : ℝ} (hL0 : 0 ≤ L) (hL : volume C₁ + volume C₂ = ENNReal.ofReal L)
    (h : ∀ t : ℝ, 0 ≤ t → t < L → volume (C₁ ∩ {x | f x ≤ ENNReal.ofReal t}) +
      volume (C₂ ∩ {x | g x ≤ ENNReal.ofReal t}) ≤ ENNReal.ofReal t) :
    ENNReal.ofReal (L ^ 2 / 2) ≤ (∫⁻ x in C₁, f x) + ∫⁻ x in C₂, g x := by
  have hint : ENNReal.ofReal (L ^ 2 / 2) = ∫⁻ t in Set.Ico 0 L, ENNReal.ofReal (L - t) := by
    rw [setLIntegral_congr Ico_ae_eq_Icc,
      s5_lintegral_affine (c₀ := L) (c₁ := -1) hL0 (fun x _ => by ring)
        (fun x hx => by linarith [hx.2])]
    congr 1; ring
  have hmf : ∀ t, MeasurableSet {x | ENNReal.ofReal t < f x} :=
    fun t => measurableSet_lt measurable_const hf
  have hmg : ∀ t, MeasurableSet {x | ENNReal.ofReal t < g x} :=
    fun t => measurableSet_lt measurable_const hg
  have hanti : Antitone fun t : ℝ => volume.restrict C₁ {x | ENNReal.ofReal t < f x} := by
    intro t t' htt'
    apply measure_mono
    intro x hx
    exact lt_of_le_of_lt (ENNReal.ofReal_le_ofReal htt') hx
  rw [hint]
  calc ∫⁻ t in Set.Ico 0 L, ENNReal.ofReal (L - t)
      ≤ ∫⁻ t in Set.Ico 0 L, (volume.restrict C₁ {x | ENNReal.ofReal t < f x} +
          volume.restrict C₂ {x | ENNReal.ofReal t < g x}) := by
        apply setLIntegral_mono' measurableSet_Ico
        intro t ht
        rw [Measure.restrict_apply (hmf t), Measure.restrict_apply (hmg t)]
        have e₁ := measure_inter_add_sdiff (μ := volume) C₁
          (measurableSet_le hf measurable_const : MeasurableSet {x | f x ≤ ENNReal.ofReal t})
        have e₂ := measure_inter_add_sdiff (μ := volume) C₂
          (measurableSet_le hg measurable_const : MeasurableSet {x | g x ≤ ENNReal.ofReal t})
        have d₁ : C₁ \ {x | f x ≤ ENNReal.ofReal t} = {x | ENNReal.ofReal t < f x} ∩ C₁ := by
          ext x; simp [not_le, and_comm]
        have d₂ : C₂ \ {x | g x ≤ ENNReal.ofReal t} = {x | ENNReal.ofReal t < g x} ∩ C₂ := by
          ext x; simp [not_le, and_comm]
        rw [d₁] at e₁
        rw [d₂] at e₂
        rw [ENNReal.ofReal_sub _ ht.1, tsub_le_iff_right]
        calc ENNReal.ofReal L
            = (volume (C₁ ∩ {x | f x ≤ ENNReal.ofReal t}) +
                volume (C₂ ∩ {x | g x ≤ ENNReal.ofReal t})) +
              (volume ({x | ENNReal.ofReal t < f x} ∩ C₁) +
                volume ({x | ENNReal.ofReal t < g x} ∩ C₂)) := by
              rw [← hL, ← e₁, ← e₂]; ring
          _ ≤ ENNReal.ofReal t + (volume ({x | ENNReal.ofReal t < f x} ∩ C₁) +
                volume ({x | ENNReal.ofReal t < g x} ∩ C₂)) := by
              gcongr; exact h t ht.1 ht.2
          _ = _ := add_comm _ _
    _ = (∫⁻ t in Set.Ico 0 L, volume.restrict C₁ {x | ENNReal.ofReal t < f x}) +
          ∫⁻ t in Set.Ico 0 L, volume.restrict C₂ {x | ENNReal.ofReal t < g x} :=
        lintegral_add_left hanti.measurable _
    _ ≤ (∫⁻ x in C₁, f x) + ∫⁻ x in C₂, g x :=
        add_le_add (s5_layer_aux _ hf L) (s5_layer_aux _ hg L)

/-- Splitting off the visited set `C`, with a constant lower bound on the rest. -/
lemma s5_split_const {g : ℝ → ℝ≥0∞} {D C : Set ℝ} (hD : MeasurableSet D) (hC : MeasurableSet C)
    (hCD : C ⊆ D) (hDfin : volume D ≠ ⊤) {b : ℝ} (hb0 : 0 ≤ b)
    (h : ∀ x ∈ D \ C, ENNReal.ofReal b ≤ g x) :
    (∫⁻ x in C, g x) + ENNReal.ofReal (b * ((volume D).toReal - (volume C).toReal)) ≤
      ∫⁻ x in D, g x := by
  rw [← lintegral_inter_add_sdiff g D hC, Set.inter_eq_self_of_subset_right hCD]
  gcongr
  have hCfin : volume C ≠ ⊤ := ne_top_of_le_ne_top hDfin (measure_mono hCD)
  calc ENNReal.ofReal (b * ((volume D).toReal - (volume C).toReal))
      = ENNReal.ofReal b * volume (D \ C) := by
        rw [measure_sdiff hCD hC.nullMeasurableSet hCfin, ENNReal.ofReal_mul hb0,
          ENNReal.ofReal_sub _ ENNReal.toReal_nonneg, ENNReal.ofReal_toReal hDfin,
          ENNReal.ofReal_toReal hCfin]
    _ = ∫⁻ x in D \ C, ENNReal.ofReal b := (setLIntegral_const _ _).symm
    _ ≤ ∫⁻ x in D \ C, g x := setLIntegral_mono' (hD.diff hC) h

/-- Splitting off the visited set `C`, with the lower bound `ℓ` on the rest and `ℓ ≤ c` on `C`:
`∫_{D \ C} ℓ ≥ ∫_D ℓ - c |C|`. -/
lemma s5_split_ell {g : ℝ → ℝ≥0∞} {ℓ : ℝ → ℝ} {D C : Set ℝ} (hD : MeasurableSet D)
    (hC : MeasurableSet C) (hCD : C ⊆ D) (hDfin : volume D ≠ ⊤) {c J : ℝ} (hc : 0 ≤ c)
    (hℓc : ∀ x ∈ C, ℓ x ≤ c) (hJ : ENNReal.ofReal J ≤ ∫⁻ x in D, ENNReal.ofReal (ℓ x))
    (h : ∀ x ∈ D \ C, ENNReal.ofReal (ℓ x) ≤ g x) :
    (∫⁻ x in C, g x) + ENNReal.ofReal (J - c * (volume C).toReal) ≤ ∫⁻ x in D, g x := by
  rw [← lintegral_inter_add_sdiff g D hC, Set.inter_eq_self_of_subset_right hCD]
  gcongr
  have hCfin : volume C ≠ ⊤ := ne_top_of_le_ne_top hDfin (measure_mono hCD)
  have h1 : ∫⁻ x in C, ENNReal.ofReal (ℓ x) ≤ ENNReal.ofReal (c * (volume C).toReal) := by
    calc _ ≤ ∫⁻ x in C, ENNReal.ofReal c :=
          setLIntegral_mono' hC (fun x hx => ENNReal.ofReal_le_ofReal (hℓc x hx))
      _ = _ := by rw [setLIntegral_const, ENNReal.ofReal_mul hc, ENNReal.ofReal_toReal hCfin]
  have h2 : ∫⁻ x in D, ENNReal.ofReal (ℓ x) =
      (∫⁻ x in C, ENNReal.ofReal (ℓ x)) + ∫⁻ x in D \ C, ENNReal.ofReal (ℓ x) := by
    rw [← lintegral_inter_add_sdiff _ D hC, Set.inter_eq_self_of_subset_right hCD]
  have h3 : ∫⁻ x in D \ C, ENNReal.ofReal (ℓ x) ≤ ∫⁻ x in D \ C, g x :=
    setLIntegral_mono' (hD.diff hC) h
  rw [ENNReal.ofReal_sub _ (mul_nonneg hc ENNReal.toReal_nonneg), tsub_le_iff_right]
  calc ENNReal.ofReal J ≤ _ := hJ
    _ = _ := h2
    _ ≤ ENNReal.ofReal (c * (volume C).toReal) + ∫⁻ x in D \ C, g x := add_le_add h1 h3
    _ = _ := add_comm _ _

/-- `∫ ℓ` when `ε ≤ 1 - a/2 - ε`: `(1 - 2ε)² - a²/8 + τ²/2`. -/
lemma s5_J1 {ε a τ : ℝ} (hε : 0 < ε) (ha2 : a ≤ 2 * (1 - 2 * ε)) (hτ0 : 0 ≤ τ)
    (hτa : 2 * τ ≤ a) :
    ENNReal.ofReal ((1 - 2 * ε) ^ 2 - a ^ 2 / 8 + τ ^ 2 / 2) ≤
      ∫⁻ x in Set.Icc ε (1 - ε), ENNReal.ofReal (s5_ell ε a τ x) := by
  have h1 : ε ≤ 1 - a / 2 - ε := by linarith
  have h2 : 1 - a / 2 - ε ≤ 1 - ε - τ := by linarith
  have h3 : 1 - ε - τ ≤ 1 - ε := by linarith
  have hcmin : s5_cmin ε a = 1 + a / 2 - 2 * ε := ite_eq_left (by linarith)
  have d1 : Disjoint (Set.Ico ε (1 - ε - τ)) (Set.Icc (1 - ε - τ) (1 - ε)) :=
    Set.disjoint_left.mpr fun x hx hx' => absurd hx'.1 (not_le.mpr hx.2)
  have d2 : Disjoint (Set.Ico ε (1 - a / 2 - ε)) (Set.Ico (1 - a / 2 - ε) (1 - ε - τ)) :=
    Set.disjoint_left.mpr fun x hx hx' => absurd hx'.1 (not_le.mpr hx.2)
  rw [← Set.Ico_union_Icc_eq_Icc (h1.trans h2) h3, lintegral_union measurableSet_Icc d1,
    ← Set.Ico_union_Ico_eq_Ico h1 h2, lintegral_union measurableSet_Ico d2]
  have e1 : ∫⁻ x in Set.Ico ε (1 - a / 2 - ε), ENNReal.ofReal (s5_ell ε a τ x) =
      ENNReal.ofReal ((1 + a / 2 - 2 * ε) * (1 - a / 2 - ε - ε)) := by
    rw [setLIntegral_congr_fun measurableSet_Ico
      (g := fun _ => ENNReal.ofReal (1 + a / 2 - 2 * ε))
      (fun x hx => by simp only [s5_ell, ite_eq_left hx.2, hcmin]),
      setLIntegral_const, Real.volume_Ico, ← ENNReal.ofReal_mul (by linarith)]
  have e2 : ∫⁻ x in Set.Ico (1 - a / 2 - ε) (1 - ε - τ), ENNReal.ofReal (s5_ell ε a τ x) =
      ENNReal.ofReal ((1 - ε) * ((1 - ε - τ) - (1 - a / 2 - ε)) +
        (-1) * ((1 - ε - τ) ^ 2 - (1 - a / 2 - ε) ^ 2) / 2) := by
    rw [setLIntegral_congr Ico_ae_eq_Icc]
    refine s5_lintegral_affine h2 (fun x hx => ?_) (fun x hx => by linarith [hx.2])
    simp only [s5_ell, ite_eq_right (not_lt.mpr hx.1)]
    split_ifs with h
    · ring
    · linarith [hx.2]
  have e3 : ∫⁻ x in Set.Icc (1 - ε - τ) (1 - ε), ENNReal.ofReal (s5_ell ε a τ x) =
      ENNReal.ofReal (τ * ((1 - ε) - (1 - ε - τ))) := by
    rw [setLIntegral_congr_fun measurableSet_Icc (g := fun _ => ENNReal.ofReal τ)
      (fun x hx => by
        simp only [s5_ell, ite_eq_right (not_lt.mpr (h2.trans hx.1)),
          ite_eq_right (not_lt.mpr hx.1)]),
      setLIntegral_const, Real.volume_Icc, ← ENNReal.ofReal_mul hτ0]
  rw [e1, e2, e3, ← ENNReal.ofReal_add (by nlinarith) (by nlinarith),
    ← ENNReal.ofReal_add (by nlinarith) (by nlinarith)]
  apply le_of_eq
  congr 1
  ring

/-- `∫ ℓ` when `1 - a/2 - ε ≤ ε` (no loiterer is below the threshold): `(1 - 2ε)²/2 + τ²/2`. -/
lemma s5_J2 {ε a τ : ℝ} (hα : 1 - a / 2 - ε ≤ ε) (hτ0 : 0 ≤ τ) (hτu : τ ≤ 1 - 2 * ε) :
    ENNReal.ofReal ((1 - 2 * ε) ^ 2 / 2 + τ ^ 2 / 2) ≤
      ∫⁻ x in Set.Icc ε (1 - ε), ENNReal.ofReal (s5_ell ε a τ x) := by
  have h1 : ε ≤ 1 - ε - τ := by linarith
  have h3 : 1 - ε - τ ≤ 1 - ε := by linarith
  have d1 : Disjoint (Set.Ico ε (1 - ε - τ)) (Set.Icc (1 - ε - τ) (1 - ε)) :=
    Set.disjoint_left.mpr fun x hx hx' => absurd hx'.1 (not_le.mpr hx.2)
  rw [← Set.Ico_union_Icc_eq_Icc h1 h3, lintegral_union measurableSet_Icc d1]
  have e2 : ∫⁻ x in Set.Ico ε (1 - ε - τ), ENNReal.ofReal (s5_ell ε a τ x) =
      ENNReal.ofReal ((1 - ε) * ((1 - ε - τ) - ε) + (-1) * ((1 - ε - τ) ^ 2 - ε ^ 2) / 2) := by
    rw [setLIntegral_congr Ico_ae_eq_Icc]
    refine s5_lintegral_affine h1 (fun x hx => ?_) (fun x hx => by linarith [hx.2])
    simp only [s5_ell, ite_eq_right (not_lt.mpr (hα.trans hx.1))]
    split_ifs with h
    · ring
    · linarith [hx.2]
  have e3 : ∫⁻ x in Set.Icc (1 - ε - τ) (1 - ε), ENNReal.ofReal (s5_ell ε a τ x) =
      ENNReal.ofReal (τ * ((1 - ε) - (1 - ε - τ))) := by
    rw [setLIntegral_congr_fun measurableSet_Icc (g := fun _ => ENNReal.ofReal τ)
      (fun x hx => by
        simp only [s5_ell, ite_eq_right (not_lt.mpr (hα.trans (h1.trans hx.1))),
          ite_eq_right (not_lt.mpr hx.1)]),
      setLIntegral_const, Real.volume_Icc, ← ENNReal.ofReal_mul hτ0]
  have hnn : 0 ≤ (1 - ε) * ((1 - ε - τ) - ε) + (-1) * ((1 - ε - τ) ^ 2 - ε ^ 2) / 2 := by
    nlinarith [mul_nonneg (sub_nonneg.mpr h1) (show 0 ≤ τ + (1 - ε - τ) - ε by linarith)]
  rw [e2, e3, ← ENNReal.ofReal_add hnn (by nlinarith)]
  apply le_of_eq
  congr 1
  ring

lemma s5_ell_le {ε a τ x : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hx : x ∈ Set.Icc ε (1 - ε))
    (hτu : τ ≤ 1 - 2 * ε) (hτa : 2 * τ ≤ a) : s5_ell ε a τ x ≤ s5_cmin ε a := by
  unfold s5_ell s5_cmin
  split_ifs <;> linarith [hx.1, hx.2]

lemma s5_ell_nonneg {ε a τ x : ℝ} (hε1 : ε ≤ 1 / 100) (ha : 0 ≤ a) (hτ0 : 0 ≤ τ) :
    0 ≤ s5_ell ε a τ x := by
  unfold s5_ell s5_cmin
  split_ifs <;> linarith

/-- `ℓ` is nonincreasing on `[ε, 1 - ε]`. -/
lemma s5_ell_antitone {ε a τ x x' : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hτa : 2 * τ ≤ a)
    (hx : ε ≤ x) (hxx' : x ≤ x') :
    s5_ell ε a τ x' ≤ s5_ell ε a τ x := by
  unfold s5_ell s5_cmin
  split_ifs <;> linarith

/-- The final arithmetic: from `Xp + Xn ≥ K` and `3a + 3b + 8K ≥ 30 - 200ε` to the bound on
`E_γ T`. -/
lemma s5_final {ε a b K : ℝ} {Xp Xn T₁ T₂ : ℝ≥0∞} (hε : 0 < ε) (ha0 : 0 ≤ a)
    (hb0 : 0 ≤ b) (hT₁ : T₁ = ENNReal.ofReal a) (hT₂ : T₂ = ENNReal.ofReal b)
    (hX : ENNReal.ofReal K ≤ Xp + Xn) (hineq : 30 - 200 * ε ≤ 3 * a + 3 * b + 8 * K) :
    ENNReal.ofReal ((30 - 200 * ε) / 22) ≤
      3 / 11 * (1 / 2 * (T₁ + T₂)) + 8 / 11 * (1 / 2 * ((ENNReal.ofReal (1 - ε - ε))⁻¹ * Xp +
        (ENNReal.ofReal (1 - ε - ε))⁻¹ * Xn)) := by
  have hu1 : 1 ≤ (ENNReal.ofReal (1 - ε - ε))⁻¹ :=
    ENNReal.one_le_inv.mpr (ENNReal.ofReal_le_one.mpr (by linarith))
  have hX' : ENNReal.ofReal (max K 0) ≤
      (ENNReal.ofReal (1 - ε - ε))⁻¹ * Xp + (ENNReal.ofReal (1 - ε - ε))⁻¹ * Xn := by
    rw [← mul_add]
    calc ENNReal.ofReal (max K 0) = ENNReal.ofReal K := by
          rw [ENNReal.ofReal_max, ENNReal.ofReal_zero, max_eq_left zero_le]
      _ ≤ Xp + Xn := hX
      _ ≤ _ := le_mul_of_one_le_left zero_le hu1
  calc ENNReal.ofReal ((30 - 200 * ε) / 22)
      ≤ ENNReal.ofReal ((3 * (a + b) + 8 * (max K 0 + 0)) / 22) :=
        ENNReal.ofReal_le_ofReal (by nlinarith [le_max_left K 0])
    _ = 3 / 11 * (1 / 2 * (ENNReal.ofReal a + ENNReal.ofReal b)) +
          8 / 11 * (1 / 2 * (ENNReal.ofReal (max K 0) + ENNReal.ofReal 0)) :=
        (s5_combine ha0 hb0 (le_max_right _ _) le_rfl).symm
    _ ≤ _ := by
        rw [hT₁, hT₂, ENNReal.ofReal_zero, add_zero]
        gcongr

/-! ### The minimisations (explicit polynomial inequalities) -/

lemma s5_ineq_ba {ε a b τ p m : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hab : b + 2 ≤ a)
    (hb : 2 - ε ≤ b) (hp : 0 ≤ p) (hm : 0 ≤ m) (hpm : p + m ≤ τ) (hτ : τ ≤ 1 - 2 * ε) :
    30 - 200 * ε ≤ 3 * a + 3 * b + 8 * ((p + m) ^ 2 / 2 + τ * (1 - 2 * ε - p) +
      b * (1 - 2 * ε - m)) := by
  have hum : 0 ≤ 1 - 2 * ε - m := by linarith
  have hup : 0 ≤ 1 - 2 * ε - p := by linarith
  have h1 : (1 - 2 * ε - m) * (2 - ε) ≤ (1 - 2 * ε - m) * b := mul_le_mul_of_nonneg_left hb hum
  have h2 : (p + m) * (1 - 2 * ε - p) ≤ τ * (1 - 2 * ε - p) := mul_le_mul_of_nonneg_right hpm hup
  nlinarith [mul_nonneg hp hm, mul_nonneg hp hup, mul_nonneg hm hum,
    mul_nonneg (sub_nonneg.mpr hpm) hup]

lemma s5_ineq_II {ε a b p m : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (ha : 2 - 3 * ε ≤ a)
    (hb : 2 - 3 * ε ≤ b) (hp : 0 ≤ p) (hm : 0 ≤ m) (hpm : p + m ≤ 1 - 2 * ε) :
    30 - 200 * ε ≤ 3 * a + 3 * b + 8 * ((p + m) ^ 2 / 2 + a * (1 - 2 * ε - p) +
      b * (1 - 2 * ε - m)) := by
  have hum : 0 ≤ 1 - 2 * ε - m := by linarith
  have hup : 0 ≤ 1 - 2 * ε - p := by linarith
  have h1 : (1 - 2 * ε - m) * (2 - 3 * ε) ≤ (1 - 2 * ε - m) * b :=
    mul_le_mul_of_nonneg_left hb hum
  have h2 : (1 - 2 * ε - p) * (2 - 3 * ε) ≤ (1 - 2 * ε - p) * a :=
    mul_le_mul_of_nonneg_left ha hup
  nlinarith [mul_nonneg hp hm, mul_nonneg hp hup, mul_nonneg hm hum]

/-- Case I, `a < b`, `a ≤ 2(1 - 2ε)`. -/
lemma s5_ineq_ab1 {ε a b τ p m : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (ha0 : 0 ≤ a)
    (ha2 : a ≤ 2 * (1 - 2 * ε)) (hτa : 2 * τ ≤ a) (hab : a + 2 ≤ b)
    (hp : 0 ≤ p) (hm : 0 ≤ m) (hpm : p + m ≤ τ) :
    30 - 200 * ε ≤ 3 * a + 3 * b + 8 * ((p + m) ^ 2 / 2 +
      (((1 - 2 * ε) ^ 2 - a ^ 2 / 8 + τ ^ 2 / 2) - (1 + a / 2 - 2 * ε) * p) +
      b * (1 - 2 * ε - m)) := by
  have hum : 0 ≤ 1 - 2 * ε - m := by linarith
  have h1 : (1 - 2 * ε - m) * (a + 2) ≤ (1 - 2 * ε - m) * b := mul_le_mul_of_nonneg_left hab hum
  have hτ0 : 0 ≤ τ := by linarith
  have hL : 4 * (p + m) ^ 2 - 8 * (2 + a) * (p + m) ≥ 4 * τ ^ 2 - 8 * (2 + a) * τ := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hpm) (show 0 ≤ 2 * (2 + a) - (p + m) - τ by linarith)]
  have hh : 14 * a - a ^ 2 + 8 * τ ^ 2 - 8 * (2 + a) * τ ≥ 0 := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hτa) (show 0 ≤ 14 - a - 10 * τ by linarith),
      mul_nonneg hτ0 (show 0 ≤ 1 - τ by linarith)]
  nlinarith [mul_nonneg hm (show 0 ≤ (2 + a) by linarith), mul_nonneg hp ha0, mul_nonneg hε.le hp,
    mul_nonneg hε.le hm, mul_nonneg hε.le ha0]

/-- Case I, `a < b`, `2(1 - 2ε) < a < 2 - 3ε`. -/
lemma s5_ineq_ab2 {ε a b τ p m : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100)
    (ha2 : 2 * (1 - 2 * ε) ≤ a) (ha3 : a < 2 - 3 * ε) (hab : a + 2 ≤ b)
    (hp : 0 ≤ p) (hm : 0 ≤ m) (hpm : p + m ≤ τ) (hτ : τ ≤ 1 - 2 * ε) :
    30 - 200 * ε ≤ 3 * a + 3 * b + 8 * ((p + m) ^ 2 / 2 +
      (((1 - 2 * ε) ^ 2 / 2 + τ ^ 2 / 2) - (1 + a / 2 - 2 * ε) * p) +
      b * (1 - 2 * ε - m)) := by
  have hum : 0 ≤ 1 - 2 * ε - m := by linarith
  have h1 : (1 - 2 * ε - m) * (a + 2) ≤ (1 - 2 * ε - m) * b := mul_le_mul_of_nonneg_left hab hum
  have h2 : (1 - 2 * ε - m) * (4 - 4 * ε) ≤ (1 - 2 * ε - m) * (a + 2) :=
    mul_le_mul_of_nonneg_left (by linarith) hum
  have hc : (1 + a / 2 - 2 * ε) * p ≤ 2 * p := mul_le_mul_of_nonneg_right (by linarith) hp
  have hL1 : p + m ≤ 1 := by linarith
  nlinarith [mul_nonneg hm hum, mul_nonneg hp hm,
    mul_nonneg (show 0 ≤ 1 - (p + m) by linarith) (show 0 ≤ 3 - (p + m) by linarith),
    mul_nonneg hε.le hm, mul_nonneg hε.le hp, sq_nonneg (τ - (p + m)),
    mul_nonneg (sub_nonneg.mpr hpm) (show 0 ≤ τ + p + m by linarith)]

/-- Case I, `a < b`, `a ≥ 2 - 3ε`. -/
lemma s5_ineq_ab3 {ε a b τ p m : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100)
    (ha3 : 2 - 3 * ε ≤ a) (hab : a + 2 ≤ b)
    (hp : 0 ≤ p) (hm : 0 ≤ m) (hpm : p + m ≤ τ) (hτ : τ ≤ 1 - 2 * ε) :
    30 - 200 * ε ≤ 3 * a + 3 * b + 8 * ((p + m) ^ 2 / 2 +
      (((1 - 2 * ε) ^ 2 / 2 + τ ^ 2 / 2) - (1 - 2 * ε) * p) +
      b * (1 - 2 * ε - m)) := by
  have hum : 0 ≤ 1 - 2 * ε - m := by linarith
  have h1 : (1 - 2 * ε - m) * (4 - 3 * ε) ≤ (1 - 2 * ε - m) * b :=
    mul_le_mul_of_nonneg_left (by linarith) hum
  have hL1 : p + m ≤ 1 := by linarith
  nlinarith [mul_nonneg hm hum, mul_nonneg hp hm,
    mul_nonneg (show 0 ≤ 1 - (p + m) by linarith) (show 0 ≤ 3 - (p + m) by linarith),
    mul_nonneg hε.le hm, mul_nonneg hε.le hp,
    mul_nonneg (sub_nonneg.mpr hpm) (show 0 ≤ τ + p + m by linarith)]

/-! ### The visited sets and the layer cake bound -/

/-- The positive loiterers met before time `r`. -/
def s5_Cpos (ε : ℝ) (S : C(ℝ≥0, ℝ)) (r : ℝ) : Set ℝ :=
  Set.Icc ε (1 - ε) ∩ {x | captureTime S (loiterer ε x) < ENNReal.ofReal r}

/-- The negative loiterers met before time `r`. -/
def s5_Cneg (ε : ℝ) (S : C(ℝ≥0, ℝ)) (r : ℝ) : Set ℝ :=
  Set.Icc ε (1 - ε) ∩ {x | captureTime S (-loiterer ε x) < ENNReal.ofReal r}

section s5_cases

variable {ε : ℝ} {S : C(ℝ≥0, ℝ)}

lemma s5_Cpos_meas (r : ℝ) : MeasurableSet (s5_Cpos ε S r) :=
  measurableSet_Icc.inter (measurableSet_lt (s5_measurable_T_loiterer ε S) measurable_const)

lemma s5_Cneg_meas (r : ℝ) : MeasurableSet (s5_Cneg ε S r) :=
  measurableSet_Icc.inter (measurableSet_lt (s5_measurable_T_neg_loiterer ε S) measurable_const)

lemma s5_volume_D_ne_top : volume (Set.Icc ε (1 - ε)) ≠ ⊤ := by
  rw [Real.volume_Icc]; exact ENNReal.ofReal_ne_top

/-- Lemma B and the layer cake: the visited loiterers have total mass `L ≤ τ` and total
capture time at least `L²/2`. -/
lemma s5_visited (hε : 0 < ε) (hS : S ∈ searcherPaths) {τ : ℝ≥0}
    (hτu : (τ : ℝ) ≤ 1 - 2 * ε) (hin : ∀ s : ℝ≥0, s < τ → |S s| < 1 - ε - s) :
    (volume (s5_Cpos ε S τ)).toReal + (volume (s5_Cneg ε S τ)).toReal ≤ τ ∧
    ENNReal.ofReal (((volume (s5_Cpos ε S τ)).toReal + (volume (s5_Cneg ε S τ)).toReal) ^ 2 / 2)
      ≤ (∫⁻ x in s5_Cpos ε S τ, captureTime S (loiterer ε x)) +
        ∫⁻ x in s5_Cneg ε S τ, captureTime S (-loiterer ε x) := by
  have hfin₁ : volume (s5_Cpos ε S τ) ≠ ⊤ :=
    ne_top_of_le_ne_top s5_volume_D_ne_top (measure_mono Set.inter_subset_left)
  have hfin₂ : volume (s5_Cneg ε S τ) ≠ ⊤ :=
    ne_top_of_le_ne_top s5_volume_D_ne_top (measure_mono Set.inter_subset_left)
  have hsum : volume (s5_Cpos ε S τ) + volume (s5_Cneg ε S τ) =
      ENNReal.ofReal ((volume (s5_Cpos ε S τ)).toReal + (volume (s5_Cneg ε S τ)).toReal) := by
    rw [ENNReal.ofReal_add ENNReal.toReal_nonneg ENNReal.toReal_nonneg,
      ENNReal.ofReal_toReal hfin₁, ENNReal.ofReal_toReal hfin₂]
  have key₁ : ∀ x ∈ Set.Icc ε (1 - ε), ∀ s : ℝ≥0, s < τ → S s = loiterer ε x s → S s = x :=
    fun x hx s hs he => s5_visited_pos hε.le hx
      (by linarith [(NNReal.coe_lt_coe.mpr hs : (s : ℝ) < τ)]) (hin s hs) he
  have key₂ : ∀ x ∈ Set.Icc ε (1 - ε), ∀ s : ℝ≥0, s < τ → S s = (-loiterer ε x) s →
      S s = -x :=
    fun x hx s hs he => s5_visited_neg hε.le hx
      (by linarith [(NNReal.coe_lt_coe.mpr hs : (s : ℝ) < τ)]) (hin s hs) he
  have hLτ : volume (s5_Cpos ε S τ) + volume (s5_Cneg ε S τ) ≤ ENNReal.ofReal τ := by
    apply s5_measure_visited hS hε Set.inter_subset_left Set.inter_subset_left (s5_Cneg_meas _)
    · rintro x ⟨hx, hT⟩
      obtain ⟨s, hs, he⟩ := s5_exists_lt hT
      exact ⟨s, hs.le, key₁ x hx s (by exact_mod_cast hs) he⟩
    · rintro x ⟨hx, hT⟩
      obtain ⟨s, hs, he⟩ := s5_exists_lt hT
      exact ⟨s, hs.le, key₂ x hx s (by exact_mod_cast hs) he⟩
  have hL : (volume (s5_Cpos ε S τ)).toReal + (volume (s5_Cneg ε S τ)).toReal ≤ τ := by
    rw [hsum] at hLτ
    exact (ENNReal.ofReal_le_ofReal_iff (NNReal.coe_nonneg τ)).mp hLτ
  refine ⟨hL, ?_⟩
  apply s5_layer_cake (s5_measurable_T_loiterer ε S) (s5_measurable_T_neg_loiterer ε S)
    (by positivity) hsum
  intro t ht0 htL
  apply s5_measure_visited hS hε (Set.inter_subset_left.trans Set.inter_subset_left)
    (Set.inter_subset_left.trans Set.inter_subset_left)
    ((s5_Cneg_meas _).inter (measurableSet_le (s5_measurable_T_neg_loiterer ε S) measurable_const))
  · rintro x ⟨⟨hx, -⟩, hT⟩
    obtain ⟨s, hs, he⟩ := s5_exists_le ht0 hT
    exact ⟨s, hs, key₁ x hx s (by
      have : (s : ℝ) < τ := by linarith
      exact_mod_cast this) he⟩
  · rintro x ⟨⟨hx, -⟩, hT⟩
    obtain ⟨s, hs, he⟩ := s5_exists_le ht0 hT
    exact ⟨s, hs, key₂ x hx s (by
      have : (s : ℝ) < τ := by linarith
      exact_mod_cast this) he⟩

/-- The visited positive loiterers lie in `S([0, τ]) ⊆ [1 - ε - 2τ, 1 - ε]`. -/
lemma s5_Cpos_window (hε : 0 < ε) (hS : S ∈ searcherPaths) {τ : ℝ≥0}
    (hτu : (τ : ℝ) ≤ 1 - 2 * ε) (hτ : 1 - ε - τ ≤ S τ)
    (hin : ∀ s : ℝ≥0, s < τ → |S s| < 1 - ε - s) {x : ℝ} (hx : x ∈ s5_Cpos ε S τ) :
    1 - ε - 2 * τ ≤ x := by
  obtain ⟨s, hs, he⟩ := s5_exists_lt hx.2
  have hsτ : s < τ := by exact_mod_cast hs
  have hSx : S s = x := s5_visited_pos hε.le hx.1 (by linarith) (hin s hsτ) he
  have := (s5_lip hS hsτ.le).1
  linarith [NNReal.coe_nonneg s]

lemma s5_volume_D (hε1 : ε ≤ 1 / 100) : (volume (Set.Icc ε (1 - ε))).toReal = 1 - 2 * ε := by
  rw [Real.volume_Icc, ENNReal.toReal_ofReal (by linarith)]; ring

/-- If an end is never reached, the expected capture time is infinite. -/
lemma s5_top_case {T₁ T₂ X : ℝ≥0∞} (h : T₁ = ⊤ ∨ T₂ = ⊤) {r : ℝ≥0∞} :
    r ≤ 3 / 11 * (1 / 2 * (T₁ + T₂)) + X := by
  rcases h with h | h <;> simp [h]

/-- **Case I** (after reflection): the searcher leaves the diamond at `τ ≤ 1 - 2ε` at or ahead of
the front of the positive bunch, `S(τ) ≥ F(τ)`. With `L₊`, `L₋` the masses of the positive and
negative loiterers met before `τ` (`L = L₊ + L₋ ≤ τ`):
* `b < a`: `W ≥ 3a + 3b + 8 (L²/2 + τ (1 - 2ε - L₊) + b (1 - 2ε - L₋))`, using only `T ≥ τ` on
  the unvisited positives;
* `a < b`: `W ≥ 3a + 3b + 8 (L²/2 + ∫ ℓ - L₊ max_{[1-ε-2τ, 1-ε]} ℓ + b (1 - 2ε - L₋))`; the
  visited positives lie in `[1 - ε - 2τ, 1 - ε]` (`s5_Cpos_window`), the maximum of the
  nonincreasing `ℓ` there is at the left end, and it is at most `c_min` (`s5_ell_le`);
  `∫ ℓ` is computed in `s5_J1`, `s5_J2`.
In both cases `W ≥ 30 - 200ε`. -/
lemma s5_caseI (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hS : S ∈ searcherPaths) {τ : ℝ≥0}
    (hτu : (τ : ℝ) ≤ 1 - 2 * ε) (hτ : 1 - ε - τ ≤ S τ)
    (hin : ∀ s : ℝ≥0, s < τ → |S s| < 1 - ε - s) :
    ENNReal.ofReal ((30 - 200 * ε) / 22) ≤ ∫⁻ H, captureTime S H ∂(gamma ε) := by
  rw [s5_lintegral_gamma hε.le]
  by_cases hT : captureTime S hiderE = ⊤ ∨ captureTime S (-hiderE) = ⊤
  · exact s5_top_case hT
  push Not at hT
  obtain ⟨haT, hbT⟩ := hT
  set a := (captureTime S hiderE).toReal with ha_def
  set b := (captureTime S (-hiderE)).toReal with hb_def
  have ha : captureTime S hiderE = ENNReal.ofReal a := (ENNReal.ofReal_toReal haT).symm
  have hb : captureTime S (-hiderE) = ENNReal.ofReal b := (ENNReal.ofReal_toReal hbT).symm
  have ha0 : 0 ≤ a := ENNReal.toReal_nonneg
  have hb0 : 0 ≤ b := ENNReal.toReal_nonneg
  have hτa : 2 * (τ : ℝ) ≤ a := by
    rcases eq_or_ne τ 0 with h0 | h0
    · rw [h0]; simpa using ha0
    · have hSτ : S τ = 1 - ε - τ :=
        le_antisymm (s5_le_front hS (pos_iff_ne_zero.mpr h0) hin) hτ
      have := s5_lemmaE hε hS hSτ
      rw [ha, ENNReal.ofReal_le_ofReal_iff ha0] at this
      linarith
  have hb2 : 2 - ε ≤ b := by
    have := s5_b_ge hε hS hτ hin
    rwa [hb, ENNReal.ofReal_le_ofReal_iff hb0] at this
  obtain ⟨hL, hlayer⟩ := s5_visited hε hS hτu hin
  set p := (volume (s5_Cpos ε S τ)).toReal with hp_def
  set m := (volume (s5_Cneg ε S τ)).toReal with hm_def
  have hp0 : 0 ≤ p := ENNReal.toReal_nonneg
  have hm0 : 0 ≤ m := ENNReal.toReal_nonneg
  -- the negative loiterers (Lemma D)
  have hneg := s5_split_const (g := fun x => captureTime S (-loiterer ε x)) measurableSet_Icc
    (s5_Cneg_meas _) Set.inter_subset_left s5_volume_D_ne_top hb0 (fun x hx => by
      rw [← hb]
      exact s5_neg_after hε hS hτ hx.1 (not_lt.mp fun h => hx.2 ⟨hx.1, h⟩))
  rw [s5_volume_D hε1] at hneg
  rcases s5_ends hS ha hb ha0 hb0 with hab | hab
  · -- `a < b`: the positive loiterers by Lemma F
    have key : ∃ J : ℝ, ENNReal.ofReal J ≤
        ∫⁻ x in Set.Icc ε (1 - ε), ENNReal.ofReal (s5_ell ε a τ x) ∧
        30 - 200 * ε ≤ 3 * a + 3 * b + 8 * ((p + m) ^ 2 / 2 + (J - s5_cmin ε a * p) +
          b * (1 - 2 * ε - m)) := by
      rcases le_or_gt a (2 * (1 - 2 * ε)) with h1 | h1
      · refine ⟨_, s5_J1 hε h1 (NNReal.coe_nonneg τ) hτa, ?_⟩
        rw [show s5_cmin ε a = 1 + a / 2 - 2 * ε from ite_eq_left (by linarith)]
        exact s5_ineq_ab1 hε hε1 ha0 h1 hτa hab hp0 hm0 hL
      · refine ⟨_, s5_J2 (by linarith) (NNReal.coe_nonneg τ) hτu, ?_⟩
        rcases lt_or_ge a (2 - 3 * ε) with h2 | h2
        · rw [show s5_cmin ε a = 1 + a / 2 - 2 * ε from ite_eq_left h2]
          exact s5_ineq_ab2 hε hε1 h1.le h2 hab hp0 hm0 hL hτu
        · rw [show s5_cmin ε a = 1 - 2 * ε from ite_eq_right (not_lt.mpr h2)]
          exact s5_ineq_ab3 hε hε1 h2 hab hp0 hm0 hL hτu
    obtain ⟨J, hJ, hineq⟩ := key
    -- the visited positives lie in the window `[1 - ε - 2τ, 1 - ε]`, where `ℓ ≤ M`, `M` the
    -- value of the nonincreasing `ℓ` at the left end of the window; and `M ≤ c_min`
    set M := s5_ell ε a τ (max ε (1 - ε - 2 * τ)) with hM_def
    have hM0 : 0 ≤ M := s5_ell_nonneg hε1 ha0 (NNReal.coe_nonneg τ)
    have hMc : M ≤ s5_cmin ε a :=
      s5_ell_le hε hε1 ⟨le_max_left _ _, max_le (by linarith) (by linarith [NNReal.coe_nonneg τ])⟩
        hτu hτa
    have hℓM : ∀ x ∈ s5_Cpos ε S τ, s5_ell ε a τ x ≤ M := fun x hx =>
      s5_ell_antitone hε hε1 hτa (le_max_left _ _)
        (max_le hx.1.1 (s5_Cpos_window hε hS hτu hτ hin hx))
    have hineq' : 30 - 200 * ε ≤ 3 * a + 3 * b + 8 * ((p + m) ^ 2 / 2 + (J - M * p) +
        b * (1 - 2 * ε - m)) := by
      nlinarith [mul_le_mul_of_nonneg_right hMc hp0]
    have hpos := s5_split_ell (g := fun x => captureTime S (loiterer ε x)) measurableSet_Icc
      (s5_Cpos_meas _) Set.inter_subset_left s5_volume_D_ne_top hM0 hℓM hJ (fun x hx =>
        s5_pos_after hε hS hτ ha ha0 hτa hx.1 (not_lt.mp fun h => hx.2 ⟨hx.1, h⟩))
    refine s5_final hε ha0 hb0 ha hb ?_ hineq'
    calc ENNReal.ofReal ((p + m) ^ 2 / 2 + (J - M * p) + b * (1 - 2 * ε - m))
        ≤ ENNReal.ofReal ((p + m) ^ 2 / 2) + ENNReal.ofReal (J - M * p) +
            ENNReal.ofReal (b * (1 - 2 * ε - m)) :=
          ENNReal.ofReal_add_le.trans (add_le_add_left ENNReal.ofReal_add_le _)
      _ ≤ ((∫⁻ x in s5_Cpos ε S τ, captureTime S (loiterer ε x)) +
            ∫⁻ x in s5_Cneg ε S τ, captureTime S (-loiterer ε x)) +
            ENNReal.ofReal (J - M * p) + ENNReal.ofReal (b * (1 - 2 * ε - m)) := by
          gcongr
      _ = ((∫⁻ x in s5_Cpos ε S τ, captureTime S (loiterer ε x)) +
            ENNReal.ofReal (J - M * p)) +
          ((∫⁻ x in s5_Cneg ε S τ, captureTime S (-loiterer ε x)) +
            ENNReal.ofReal (b * (1 - 2 * ε - m))) := by ring
      _ ≤ _ := add_le_add hpos hneg
  · -- `b < a`: every unvisited positive loiterer is met after `τ`
    have hpos := s5_split_const (g := fun x => captureTime S (loiterer ε x)) measurableSet_Icc
      (s5_Cpos_meas _) Set.inter_subset_left s5_volume_D_ne_top (NNReal.coe_nonneg τ)
      (fun x hx => not_lt.mp fun h => hx.2 ⟨hx.1, h⟩)
    rw [s5_volume_D hε1] at hpos
    refine s5_final hε ha0 hb0 ha hb ?_
      (s5_ineq_ba hε hε1 hab hb2 hp0 hm0 hL hτu)
    calc ENNReal.ofReal ((p + m) ^ 2 / 2 + τ * (1 - 2 * ε - p) + b * (1 - 2 * ε - m))
        ≤ ENNReal.ofReal ((p + m) ^ 2 / 2) + ENNReal.ofReal (τ * (1 - 2 * ε - p)) +
            ENNReal.ofReal (b * (1 - 2 * ε - m)) :=
          ENNReal.ofReal_add_le.trans (add_le_add_left ENNReal.ofReal_add_le _)
      _ ≤ ((∫⁻ x in s5_Cpos ε S τ, captureTime S (loiterer ε x)) +
            ∫⁻ x in s5_Cneg ε S τ, captureTime S (-loiterer ε x)) +
            ENNReal.ofReal (τ * (1 - 2 * ε - p)) + ENNReal.ofReal (b * (1 - 2 * ε - m)) := by
          gcongr
      _ = ((∫⁻ x in s5_Cpos ε S τ, captureTime S (loiterer ε x)) +
            ENNReal.ofReal (τ * (1 - 2 * ε - p))) +
          ((∫⁻ x in s5_Cneg ε S τ, captureTime S (-loiterer ε x)) +
            ENNReal.ofReal (b * (1 - 2 * ε - m))) := by ring
      _ ≤ _ := add_le_add hpos hneg

/-- **Case II**: the searcher stays strictly inside the diamond until `1 - 2ε`. Then both bunches
run outwards strictly ahead of it, every unvisited positive (negative) loiterer is met at
`a ≥ 2 - 3ε` (`b ≥ 2 - 3ε`), and `W ≥ 3a + 3b + 8 (L²/2 + a (1 - 2ε - L₊) + b (1 - 2ε - L₋))`. -/
lemma s5_caseII (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hS : S ∈ searcherPaths)
    (hII : ∀ s : ℝ≥0, (s : ℝ) ≤ 1 - 2 * ε → |S s| < 1 - ε - s) :
    ENNReal.ofReal ((30 - 200 * ε) / 22) ≤ ∫⁻ H, captureTime S H ∂(gamma ε) := by
  rw [s5_lintegral_gamma hε.le]
  by_cases hT : captureTime S hiderE = ⊤ ∨ captureTime S (-hiderE) = ⊤
  · exact s5_top_case hT
  push Not at hT
  obtain ⟨haT, hbT⟩ := hT
  set a := (captureTime S hiderE).toReal with ha_def
  set b := (captureTime S (-hiderE)).toReal with hb_def
  have ha : captureTime S hiderE = ENNReal.ofReal a := (ENNReal.ofReal_toReal haT).symm
  have hb : captureTime S (-hiderE) = ENNReal.ofReal b := (ENNReal.ofReal_toReal hbT).symm
  have ha0 : 0 ≤ a := ENNReal.toReal_nonneg
  have hb0 : 0 ≤ b := ENNReal.toReal_nonneg
  have ha2 : 2 - 3 * ε ≤ a := by
    have := s5_caseII_a hε hε1 hS hII
    rwa [ha, ENNReal.ofReal_le_ofReal_iff ha0] at this
  have hb2 : 2 - 3 * ε ≤ b := by
    have := s5_caseII_b hε hε1 hS hII
    rwa [hb, ENNReal.ofReal_le_ofReal_iff hb0] at this
  set u : ℝ≥0 := ⟨1 - 2 * ε, by linarith⟩ with hu_def
  have hu : (u : ℝ) = 1 - 2 * ε := rfl
  have hin : ∀ s : ℝ≥0, s < u → |S s| < 1 - ε - s := fun s hs =>
    hII s (by rw [← hu]; exact (NNReal.coe_lt_coe.mpr hs).le)
  obtain ⟨hL, hlayer⟩ := s5_visited hε hS (le_of_eq hu) hin
  set p := (volume (s5_Cpos ε S u)).toReal with hp_def
  set m := (volume (s5_Cneg ε S u)).toReal with hm_def
  replace hL : p + m ≤ 1 - 2 * ε := hL.trans (le_of_eq hu)
  have hp0 : 0 ≤ p := ENNReal.toReal_nonneg
  have hm0 : 0 ≤ m := ENNReal.toReal_nonneg
  have hpos := s5_split_const (g := fun x => captureTime S (loiterer ε x)) measurableSet_Icc
    (s5_Cpos_meas _) Set.inter_subset_left s5_volume_D_ne_top ha0 (fun x hx => by
      rw [← ha]
      refine s5_caseII_pos hε hε1 hS hII ?_
      rw [← hu]
      exact not_lt.mp fun h => hx.2 ⟨hx.1, h⟩)
  have hneg := s5_split_const (g := fun x => captureTime S (-loiterer ε x)) measurableSet_Icc
    (s5_Cneg_meas _) Set.inter_subset_left s5_volume_D_ne_top hb0 (fun x hx => by
      rw [← hb]
      refine s5_caseII_neg hε hε1 hS hII ?_
      rw [← hu]
      exact not_lt.mp fun h => hx.2 ⟨hx.1, h⟩)
  rw [s5_volume_D hε1] at hpos hneg
  refine s5_final hε ha0 hb0 ha hb ?_
    (s5_ineq_II hε hε1 ha2 hb2 hp0 hm0 hL)
  calc ENNReal.ofReal ((p + m) ^ 2 / 2 + a * (1 - 2 * ε - p) + b * (1 - 2 * ε - m))
      ≤ ENNReal.ofReal ((p + m) ^ 2 / 2) + ENNReal.ofReal (a * (1 - 2 * ε - p)) +
          ENNReal.ofReal (b * (1 - 2 * ε - m)) :=
        ENNReal.ofReal_add_le.trans (add_le_add_left ENNReal.ofReal_add_le _)
    _ ≤ ((∫⁻ x in s5_Cpos ε S u, captureTime S (loiterer ε x)) +
          ∫⁻ x in s5_Cneg ε S u, captureTime S (-loiterer ε x)) +
          ENNReal.ofReal (a * (1 - 2 * ε - p)) + ENNReal.ofReal (b * (1 - 2 * ε - m)) := by
        gcongr
    _ = ((∫⁻ x in s5_Cpos ε S u, captureTime S (loiterer ε x)) +
          ENNReal.ofReal (a * (1 - 2 * ε - p))) +
        ((∫⁻ x in s5_Cneg ε S u, captureTime S (-loiterer ε x)) +
          ENNReal.ofReal (b * (1 - 2 * ε - m))) := by ring
    _ ≤ _ := add_le_add hpos hneg

/-- `γ` is invariant under the reflection, so `E_γ T(-S, ·) = E_γ T(S, ·)`. -/
lemma s5_lintegral_gamma_neg (hε : 0 ≤ ε) (S : C(ℝ≥0, ℝ)) :
    ∫⁻ H, captureTime (-S) H ∂(gamma ε) = ∫⁻ H, captureTime S H ∂(gamma ε) := by
  have h1 : ∀ H : C(ℝ≥0, ℝ), captureTime (-S) H = captureTime S (-H) := fun H => by
    have := captureTime_neg (S := S) (H := -H)
    rwa [neg_neg] at this
  rw [s5_lintegral_gamma hε, s5_lintegral_gamma hε]
  simp only [h1, neg_neg]
  ring

/-- **The lower bound**: every searcher path has expected capture time at least
`(30 - 200ε)/22` against `γ`. -/
lemma s5_lower (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (hS : S ∈ searcherPaths) :
    ENNReal.ofReal ((30 - 200 * ε) / 22) ≤ ∫⁻ H, captureTime S H ∂(gamma ε) := by
  by_cases hII : ∀ s : ℝ≥0, (s : ℝ) ≤ 1 - 2 * ε → |S s| < 1 - ε - s
  · exact s5_caseII hε hε1 hS hII
  · obtain ⟨τ, hτu, hτ, hin⟩ := s5_exists_tau hII
    rcases le_abs.mp hτ with h | h
    · exact s5_caseI hε hε1 hS hτu h hin
    · rw [← s5_lintegral_gamma_neg hε.le]
      exact s5_caseI hε hε1 (neg_mem_searcherPaths hS) hτu (by simpa using h)
        (fun s hs => by simpa [abs_neg] using hin s hs)

end s5_cases

/-! ### The paths `S₁`, `S₂` and their capture times (formula (15)) -/

/-- An exact capture time: the paths meet at `r` and not before. -/
lemma s5_captureTime_eq_of {S H : C(ℝ≥0, ℝ)} {r : ℝ} (hr : 0 ≤ r)
    (hmeet : ∀ t : ℝ≥0, (t : ℝ) = r → S t = H t)
    (hbefore : ∀ t : ℝ≥0, (t : ℝ) < r → S t ≠ H t) :
    captureTime S H = ENNReal.ofReal r := by
  apply le_antisymm
  · exact captureTime_le (hmeet (Real.toNNReal r) (Real.coe_toNNReal r hr))
  · refine le_captureTime_of_ne (c := Real.toNNReal r) (fun t ht => hbefore t ?_)
    rw [← Real.coe_toNNReal r hr]
    exact_mod_cast ht

section s5_paths

variable {y ε : ℝ}

lemma s5_S1_early (hy0 : 0 ≤ y) (hε : 0 ≤ ε) (hs0 : -1 ≤ 1 - 2 * y - ε) {t : ℝ≥0}
    (ht : (t : ℝ) ≤ y) : pathS1 y ε t = 1 - 2 * y - ε + t := by
  simp only [pathS1, pathOf_apply]
  rw [min_eq_left (by linarith),
    Real.triangleWave_of_mem_Icc ⟨by linarith [NNReal.coe_nonneg t], by linarith⟩]

lemma s5_S1_mid (hε : 0 ≤ ε) {t : ℝ≥0} (h1 : y ≤ (t : ℝ)) (h2 : (t : ℝ) ≤ 2 - ε) :
    pathS1 y ε t = 1 - ε - t := by
  simp only [pathS1, pathOf_apply]
  rw [min_eq_right (by linarith),
    Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith [NNReal.coe_nonneg t]⟩]

lemma s5_S1_late {t : ℝ≥0} (h1 : y ≤ (t : ℝ)) (h2 : 2 - ε ≤ (t : ℝ)) (h3 : (t : ℝ) ≤ 4 - ε) :
    pathS1 y ε t = t - 3 + ε := by
  simp only [pathS1, pathOf_apply]
  rw [min_eq_right (by linarith),
    Real.triangleWave_of_mem_Icc_neg_three_neg_one ⟨by linarith, by linarith⟩]
  ring

lemma s5_S2_early (hs0 : -1 ≤ 1 - 2 * y - ε) {t : ℝ≥0}
    (ht : (t : ℝ) ≤ 2 * y + ε) : pathS2 y ε t = 1 - 2 * y - ε + t := by
  simp only [pathS2, pathOf_apply]
  rw [Real.triangleWave_of_mem_Icc ⟨by linarith [NNReal.coe_nonneg t], by linarith⟩]

lemma s5_S2_mid {t : ℝ≥0} (h1 : 2 * y + ε ≤ (t : ℝ)) (h2 : (t : ℝ) ≤ 2 + 2 * y + ε) :
    pathS2 y ε t = 1 + 2 * y + ε - t := by
  simp only [pathS2, pathOf_apply]
  rw [Real.triangleWave_of_mem_Icc_one_three ⟨by linarith, by linarith⟩]
  ring

lemma s5_S2_late {t : ℝ≥0} (h1 : 2 + 2 * y + ε ≤ (t : ℝ)) (h2 : (t : ℝ) ≤ 4 + 2 * y + ε) :
    pathS2 y ε t = t - 3 - 2 * y - ε := by
  simp only [pathS2, pathOf_apply]
  have : 1 - 2 * y - ε + (t : ℝ) = (1 - 2 * y - ε + t - 4) + 4 := by ring
  rw [this, Real.triangleWave_add_four, Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith⟩]
  ring

lemma s5_loiterer_end (hε1 : ε ≤ 1) {x : ℝ} {t : ℝ≥0} (ht : 2 - 3 * ε ≤ (t : ℝ)) :
    loiterer ε x t = 1 := by
  rw [s5_loiterer_late (by linarith), min_eq_left (by linarith)]

lemma s5_loiterer_le_max (x : ℝ) (t : ℝ≥0) :
    loiterer ε x t ≤ max (min x (1 - ε - t)) (t - 1 + 3 * ε) := by
  rw [s5_loiterer_apply]; exact min_le_right _ _

lemma s5_loiterer_ge_left (x : ℝ) (t : ℝ≥0) : min 1 (min x (1 - ε - t)) ≤ loiterer ε x t := by
  rw [s5_loiterer_apply]; exact min_le_min_left _ (le_max_left _ _)

lemma s5_loiterer_ge_right (x : ℝ) (t : ℝ≥0) : min 1 ((t : ℝ) - 1 + 3 * ε) ≤ loiterer ε x t := by
  rw [s5_loiterer_apply]; exact min_le_min_left _ (le_max_right _ _)

/-! The capture times of the ends. -/

lemma s5_T1E (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) :
    captureTime (pathS1 y ε) hiderE = ENNReal.ofReal (4 - ε) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S1_late (by linarith) (by linarith) (by linarith), ht, s5_hiderE_apply]
    ring
  · intro t ht hmeet
    rw [s5_hiderE_apply] at hmeet
    rcases le_total (t : ℝ) y with h1 | h1
    · rw [s5_S1_early hy0.le hε.le (by linarith) h1] at hmeet; linarith
    rcases le_total (t : ℝ) (2 - ε) with h2 | h2
    · rw [s5_S1_mid hε.le h1 h2] at hmeet; linarith 
    · rw [s5_S1_late h1 h2 ht.le] at hmeet; linarith

lemma s5_T1negE (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) :
    captureTime (pathS1 y ε) (-hiderE) = ENNReal.ofReal (2 - ε) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S1_mid hε.le (by linarith) (by linarith), ht, ContinuousMap.neg_apply,
      s5_hiderE_apply]
    ring
  · intro t ht hmeet
    rw [ContinuousMap.neg_apply, s5_hiderE_apply] at hmeet
    rcases le_total (t : ℝ) y with h1 | h1
    · rw [s5_S1_early hy0.le hε.le (by linarith) h1] at hmeet
      linarith [NNReal.coe_nonneg t]
    · rw [s5_S1_mid hε.le h1 ht.le] at hmeet; linarith

lemma s5_T2E (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) :
    captureTime (pathS2 y ε) hiderE = ENNReal.ofReal (2 * y + ε) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S2_early (by linarith) ht.le, ht, s5_hiderE_apply]
    ring
  · intro t ht hmeet
    rw [s5_hiderE_apply, s5_S2_early (by linarith) ht.le] at hmeet
    linarith

lemma s5_T2negE (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) :
    captureTime (pathS2 y ε) (-hiderE) = ENNReal.ofReal (2 + 2 * y + ε) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S2_mid (by linarith) ht.le, ht, ContinuousMap.neg_apply, s5_hiderE_apply]
    ring
  · intro t ht hmeet
    rw [ContinuousMap.neg_apply, s5_hiderE_apply] at hmeet
    rcases le_total (t : ℝ) (2 * y + ε) with h1 | h1
    · rw [s5_S2_early (by linarith) h1] at hmeet
      linarith [NNReal.coe_nonneg t]
    · rw [s5_S2_mid h1 ht.le] at hmeet; linarith

/-! Uniform bounds on the capture times of the loiterers. -/

lemma s5_T_le_of {S H : C(ℝ≥0, ℝ)} {r : ℝ} (hr : 0 ≤ r)
    (h : ∀ t : ℝ≥0, (t : ℝ) = r → S t = H t) : captureTime S H ≤ ENNReal.ofReal r :=
  captureTime_le (h (Real.toNNReal r) (Real.coe_toNNReal r hr))

lemma s5_T1p_le (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) (x : ℝ) :
    captureTime (pathS1 y ε) (loiterer ε x) ≤ 7 := by
  refine (s5_T_le_of (r := 4 - ε) (by linarith) fun t ht => ?_).trans ?_
  · rw [s5_S1_late (by linarith) (by linarith) (by linarith),
      s5_loiterer_end (by linarith) (by linarith), ht]
    ring
  · rw [show (7 : ℝ≥0∞) = ENNReal.ofReal 7 by simp]
    exact ENNReal.ofReal_le_ofReal (by linarith)

lemma s5_T1n_le (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) (x : ℝ) :
    captureTime (pathS1 y ε) (-loiterer ε x) ≤ 7 := by
  refine (s5_T_le_of (r := 2 - ε) (by linarith) fun t ht => ?_).trans ?_
  · rw [s5_S1_mid hε.le (by linarith) (by linarith), ContinuousMap.neg_apply,
      s5_loiterer_end (by linarith) (by linarith), ht]
    ring
  · rw [show (7 : ℝ≥0∞) = ENNReal.ofReal 7 by simp]
    exact ENNReal.ofReal_le_ofReal (by linarith)

lemma s5_T2p_le (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) (x : ℝ) :
    captureTime (pathS2 y ε) (loiterer ε x) ≤ 7 := by
  refine (s5_T_le_of (r := 4 + 2 * y + ε) (by linarith) fun t ht => ?_).trans ?_
  · rw [s5_S2_late (by linarith) (by linarith), s5_loiterer_end (by linarith) (by linarith), ht]
    ring
  · rw [show (7 : ℝ≥0∞) = ENNReal.ofReal 7 by simp]
    exact ENNReal.ofReal_le_ofReal (by linarith)

lemma s5_T2n_le (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) (x : ℝ) :
    captureTime (pathS2 y ε) (-loiterer ε x) ≤ 7 := by
  refine (s5_T_le_of (r := 2 + 2 * y + ε) (by linarith) fun t ht => ?_).trans ?_
  · rw [s5_S2_mid (by linarith) (by linarith), ContinuousMap.neg_apply,
      s5_loiterer_end (by linarith) (by linarith), ht]
    ring
  · rw [show (7 : ℝ≥0∞) = ENNReal.ofReal 7 by simp]
    exact ENNReal.ofReal_le_ofReal (by linarith)

end s5_paths

/-! The capture times of the loiterers by `S₁` and `S₂`, for small `ε` (the cases of (15)). -/

section s5_loiterers

variable {y ε : ℝ}

/-- `S₁`, a positive loiterer from `x > 1 - y`: met in the running bunch at time `y`. -/
lemma s5_T1p_a (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) {x : ℝ} (hx : 1 - y < x)
    (hx1 : x ≤ 1) : captureTime (pathS1 y ε) (loiterer ε x) = ENNReal.ofReal y := by
  apply s5_captureTime_eq_of hy0.le
  · intro t ht
    rw [s5_S1_early hy0.le hε.le (by linarith) ht.le,
      s5_loiterer_early (by linarith) hx1 (by linarith), ht, min_eq_right (by linarith)]
    ring
  · intro t ht hmeet
    rw [s5_S1_early hy0.le hε.le (by linarith) ht.le,
      s5_loiterer_early (by linarith) hx1 (by linarith)] at hmeet
    rcases min_choice x (1 - ε - (t : ℝ)) with h | h <;> rw [h] at hmeet <;> linarith

/-- `S₁`, a positive loiterer from `1 - 2y < x < 1 - y`: met where it waits. -/
lemma s5_T1p_b (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) {x : ℝ} (hx : 1 - 2 * y < x)
    (hx' : x < 1 - y - ε) (hxε : ε ≤ x) :
    captureTime (pathS1 y ε) (loiterer ε x) = ENNReal.ofReal (x - 1 + 2 * y + ε) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S1_early hy0.le hε.le (by linarith) (by linarith),
      s5_loiterer_early hxε (by linarith) (by linarith), ht, min_eq_left (by linarith)]
    ring
  · intro t ht hmeet
    rw [s5_S1_early hy0.le hε.le (by linarith) (by linarith),
      s5_loiterer_early hxε (by linarith) (by linarith)] at hmeet
    rcases min_choice x (1 - ε - (t : ℝ)) with h | h <;> rw [h] at hmeet <;> linarith

/-- `S₁`, a positive loiterer from `x < 1 - 2y`: met when it starts running. -/
lemma s5_T1p_c (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) {x : ℝ}
    (hx : x < 1 - 2 * y - ε) (hxε : ε ≤ x) :
    captureTime (pathS1 y ε) (loiterer ε x) = ENNReal.ofReal (1 - x - ε) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S1_mid hε.le (by linarith) (by linarith),
      s5_loiterer_early hxε (by linarith) (by linarith), ht, min_eq_left (by linarith)]
    ring
  · intro t ht hmeet
    have hle : loiterer ε x t ≤ x := by
      rw [s5_loiterer_early hxε (by linarith) (by linarith)]; exact min_le_left _ _
    rcases le_total (t : ℝ) y with h1 | h1
    · rw [s5_S1_early hy0.le hε.le (by linarith) h1] at hmeet
      linarith [NNReal.coe_nonneg t]
    · rw [s5_S1_mid hε.le h1 (by linarith)] at hmeet
      linarith

/-- `S₁`, a negative loiterer from `-x` with `x < 2y - 1`: met where it waits. -/
lemma s5_T1n_a (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) {x : ℝ}
    (hx : x < 2 * y - 1) (hxε : ε ≤ x) :
    captureTime (pathS1 y ε) (-loiterer ε x) = ENNReal.ofReal (2 * y - 1 + ε - x) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S1_early hy0.le hε.le (by linarith) (by linarith), ContinuousMap.neg_apply,
      s5_loiterer_early hxε (by linarith) (by linarith), ht, min_eq_left (by linarith)]
    ring
  · intro t ht hmeet
    rw [s5_S1_early hy0.le hε.le (by linarith) (by linarith), ContinuousMap.neg_apply,
      s5_loiterer_early hxε (by linarith) (by linarith)] at hmeet
    have := min_le_left x (1 - ε - (t : ℝ))
    linarith

/-- `S₁`, a negative loiterer from `-x` with `x > 2y - 1`: met at `-1`. -/
lemma s5_T1n_b (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) {x : ℝ}
    (hx : 2 * y - 1 + ε < x) (hxε : ε ≤ x) (hx1 : x ≤ 1) :
    captureTime (pathS1 y ε) (-loiterer ε x) = ENNReal.ofReal (2 - ε) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S1_mid hε.le (by linarith) (by linarith), ContinuousMap.neg_apply,
      s5_loiterer_end (by linarith) (by linarith), ht]
    ring
  · intro t ht hmeet
    rw [ContinuousMap.neg_apply] at hmeet
    rcases le_total (t : ℝ) y with h1 | h1
    · rw [s5_S1_early hy0.le hε.le (by linarith) h1,
        s5_loiterer_early hxε hx1 (by linarith)] at hmeet
      rcases min_choice x (1 - ε - (t : ℝ)) with h | h <;> rw [h] at hmeet <;>
        linarith [NNReal.coe_nonneg t]
    rcases le_total (t : ℝ) (1 - 2 * ε) with h2 | h2
    · rw [s5_S1_mid hε.le h1 (by linarith), s5_loiterer_early hxε hx1 h2] at hmeet
      rcases min_choice x (1 - ε - (t : ℝ)) with h | h <;> rw [h] at hmeet <;> linarith
    · rw [s5_S1_mid hε.le h1 ht.le, s5_loiterer_late h2] at hmeet
      rcases min_choice 1 ((t : ℝ) - 1 + 3 * ε) with h | h <;> rw [h] at hmeet <;> linarith

/-- `S₂`, a positive loiterer from `x > 1 - y`: met in the running bunch at time `y`. -/
lemma s5_T2p_a (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) {x : ℝ} (hx : 1 - y < x)
    (hx1 : x ≤ 1) : captureTime (pathS2 y ε) (loiterer ε x) = ENNReal.ofReal y := by
  apply s5_captureTime_eq_of hy0.le
  · intro t ht
    rw [s5_S2_early (by linarith) (by linarith),
      s5_loiterer_early (by linarith) hx1 (by linarith), ht, min_eq_right (by linarith)]
    ring
  · intro t ht hmeet
    rw [s5_S2_early (by linarith) (by linarith),
      s5_loiterer_early (by linarith) hx1 (by linarith)] at hmeet
    rcases min_choice x (1 - ε - (t : ℝ)) with h | h <;> rw [h] at hmeet <;> linarith

/-- `S₂`, a positive loiterer from `1 - 2y < x < 1 - y`: met where it waits. -/
lemma s5_T2p_b (hε : 0 < ε) (hεy : ε < (1 - y) / 4) {x : ℝ} (hx : 1 - 2 * y < x)
    (hx' : x < 1 - y - ε) (hxε : ε ≤ x) :
    captureTime (pathS2 y ε) (loiterer ε x) = ENNReal.ofReal (x - 1 + 2 * y + ε) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S2_early (by linarith) (by linarith),
      s5_loiterer_early hxε (by linarith) (by linarith), ht, min_eq_left (by linarith)]
    ring
  · intro t ht hmeet
    rw [s5_S2_early (by linarith) (by linarith),
      s5_loiterer_early hxε (by linarith) (by linarith)] at hmeet
    rcases min_choice x (1 - ε - (t : ℝ)) with h | h <;> rw [h] at hmeet <;> linarith

/-- `S₂`, a positive loiterer from `x < 1 - 2y`: met when it runs back to `+1`. -/
lemma s5_T2p_c (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) {x : ℝ}
    (hx : x < 1 - 2 * y - ε) :
    captureTime (pathS2 y ε) (loiterer ε x) = ENNReal.ofReal (1 + y - ε) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S2_mid (by linarith) (by linarith), s5_loiterer_late (by linarith), ht,
      min_eq_right (by linarith)]
    ring
  · intro t ht hmeet
    have hle := s5_loiterer_le_max (ε := ε) x t
    have h3 := min_le_left x (1 - ε - (t : ℝ))
    have h4 := min_le_right x (1 - ε - (t : ℝ))
    rcases le_total (t : ℝ) (2 * y + ε) with h1 | h1
    · rw [s5_S2_early (by linarith) h1] at hmeet
      have : max (min x (1 - ε - (t : ℝ))) ((t : ℝ) - 1 + 3 * ε) < 1 - 2 * y - ε + t :=
        max_lt (by linarith [NNReal.coe_nonneg t]) (by linarith)
      linarith
    · rw [s5_S2_mid h1 (by linarith)] at hmeet
      have : max (min x (1 - ε - (t : ℝ))) ((t : ℝ) - 1 + 3 * ε) < 1 + 2 * y + ε - t :=
        max_lt (by linarith) (by linarith)
      linarith

/-- `S₂`, a negative loiterer from `-x` with `x < 2y - 1`: met where it waits. -/
lemma s5_T2n_a (hε : 0 < ε) (hεy : ε < (1 - y) / 4) {x : ℝ}
    (hx : x < 2 * y - 1) (hxε : ε ≤ x) :
    captureTime (pathS2 y ε) (-loiterer ε x) = ENNReal.ofReal (2 * y - 1 + ε - x) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S2_early (by linarith) (by linarith), ContinuousMap.neg_apply,
      s5_loiterer_early hxε (by linarith) (by linarith), ht, min_eq_left (by linarith)]
    ring
  · intro t ht hmeet
    rw [s5_S2_early (by linarith) (by linarith), ContinuousMap.neg_apply,
      s5_loiterer_early hxε (by linarith) (by linarith)] at hmeet
    have := min_le_left x (1 - ε - (t : ℝ))
    linarith

/-- `S₂`, a negative loiterer from `-x` with `x > 2y - 1`: met at `-1`. -/
lemma s5_T2n_b (hy0 : 0 < y) (hε : 0 < ε) (hεy : ε < (1 - y) / 4) {x : ℝ}
    (hx : 2 * y - 1 + ε < x) :
    captureTime (pathS2 y ε) (-loiterer ε x) = ENNReal.ofReal (2 + 2 * y + ε) := by
  apply s5_captureTime_eq_of (by linarith)
  · intro t ht
    rw [s5_S2_mid (by linarith) (by linarith), ContinuousMap.neg_apply,
      s5_loiterer_end (by linarith) (by linarith), ht]
    ring
  · intro t ht hmeet
    rw [ContinuousMap.neg_apply] at hmeet
    rcases le_total (t : ℝ) (2 * y + ε) with h1 | h1
    · rw [s5_S2_early (by linarith) h1] at hmeet
      have hge := s5_loiterer_ge_left (ε := ε) x t
      have : -(1 - 2 * y - ε + (t : ℝ)) < min 1 (min x (1 - ε - (t : ℝ))) :=
        lt_min (by linarith [NNReal.coe_nonneg t]) (lt_min (by linarith [NNReal.coe_nonneg t])
          (by linarith))
      linarith
    · rw [s5_S2_mid h1 ht.le] at hmeet
      have hge := s5_loiterer_ge_right (ε := ε) x t
      have : -(1 + 2 * y + ε - (t : ℝ)) < min 1 ((t : ℝ) - 1 + 3 * ε) :=
        lt_min (by linarith) (by linarith)
      linarith

end s5_loiterers

/-! ### Formula (15): the limits `ε → 0` -/

/-- The capture time (as `ε → 0`) of the positive loiterer from `x` by `S₁`. -/
noncomputable def s5_g1p (y x : ℝ) : ℝ :=
  if x ≤ 1 - 2 * y then 1 - x else if x ≤ 1 - y then x - 1 + 2 * y else y

/-- The capture time (as `ε → 0`) of the negative loiterer from `-x` by `S₁`. -/
noncomputable def s5_g1n (y x : ℝ) : ℝ := if x ≤ 2 * y - 1 then 2 * y - 1 - x else 2

/-- The capture time (as `ε → 0`) of the positive loiterer from `x` by `S₂`. -/
noncomputable def s5_g2p (y x : ℝ) : ℝ :=
  if x ≤ 1 - 2 * y then 1 + y else if x ≤ 1 - y then x - 1 + 2 * y else y

/-- The capture time (as `ε → 0`) of the negative loiterer from `-x` by `S₂`. -/
noncomputable def s5_g2n (y x : ℝ) : ℝ := if x ≤ 2 * y - 1 then 2 * y - 1 - x else 2 + 2 * y

lemma s5_tendsto_of_eventually {F : ℝ → ℝ≥0∞} {h : ℝ → ℝ} {c δ : ℝ} (hδ : 0 < δ)
    (hF : ∀ ε, 0 < ε → ε < δ → F ε = ENNReal.ofReal (h ε)) (hh : Continuous h) (hc : h 0 = c) :
    Tendsto F (𝓝[>] 0) (𝓝 (ENNReal.ofReal c)) := by
  have h1 : Tendsto (fun ε => ENNReal.ofReal (h ε)) (𝓝[>] 0) (𝓝 (ENNReal.ofReal c)) := by
    rw [← hc]
    exact ((ENNReal.continuous_ofReal.comp hh).tendsto 0).mono_left nhdsWithin_le_nhds
  refine h1.congr' ?_
  filter_upwards [Ioo_mem_nhdsGT hδ] with ε hε
  exact (hF ε hε.1 hε.2).symm

section s5_limits

variable {y x : ℝ}

lemma s5_tendsto_T1p (hy0 : 0 < y) (hy1 : y < 1) (hx : x ∈ Set.Ioo (0 : ℝ) 1)
    (h1 : x ≠ 1 - 2 * y) (h2 : x ≠ 1 - y) :
    Tendsto (fun ε => captureTime (pathS1 y ε) (loiterer ε x)) (𝓝[>] 0)
      (𝓝 (ENNReal.ofReal (s5_g1p y x))) := by
  rcases lt_or_gt_of_ne h1 with h1 | h1
  · rw [s5_g1p, ite_eq_left h1.le]
    refine s5_tendsto_of_eventually (h := fun ε => 1 - x - ε)
      (lt_min (by linarith) (lt_min hx.1 (by linarith : 0 < 1 - 2 * y - x)))
      (fun ε hε hεδ => s5_T1p_c hy0 hε ((hεδ.trans_le (min_le_left _ _)))
        (by linarith [hεδ.trans_le ((min_le_right _ _).trans (min_le_right _ _))])
        (by linarith [hεδ.trans_le ((min_le_right _ _).trans (min_le_left _ _))]))
      (by fun_prop) (by ring)
  rcases lt_or_gt_of_ne h2 with h2 | h2
  · rw [s5_g1p, ite_eq_right (not_le.mpr h1), ite_eq_left h2.le]
    refine s5_tendsto_of_eventually (h := fun ε => x - 1 + 2 * y + ε)
      (lt_min (by linarith) (lt_min hx.1 (by linarith : 0 < 1 - y - x)))
      (fun ε hε hεδ => s5_T1p_b hy0 hε ((hεδ.trans_le (min_le_left _ _))) h1
        (by linarith [hεδ.trans_le ((min_le_right _ _).trans (min_le_right _ _))])
        (by linarith [hεδ.trans_le ((min_le_right _ _).trans (min_le_left _ _))]))
      (by fun_prop) (by ring)
  · rw [s5_g1p, ite_eq_right (not_le.mpr (by linarith)), ite_eq_right (not_le.mpr h2)]
    exact s5_tendsto_of_eventually (h := fun _ => y) (by linarith : 0 < (1 - y) / 4)
      (fun ε hε hεδ => s5_T1p_a hy0 hε hεδ h2 hx.2.le) (by fun_prop) rfl

lemma s5_tendsto_T1n (hy0 : 0 < y) (hy1 : y < 1) (hx : x ∈ Set.Ioo (0 : ℝ) 1)
    (h1 : x ≠ 2 * y - 1) :
    Tendsto (fun ε => captureTime (pathS1 y ε) (-loiterer ε x)) (𝓝[>] 0)
      (𝓝 (ENNReal.ofReal (s5_g1n y x))) := by
  rcases lt_or_gt_of_ne h1 with h1 | h1
  · rw [s5_g1n, ite_eq_left h1.le]
    refine s5_tendsto_of_eventually (h := fun ε => 2 * y - 1 + ε - x)
      (lt_min (by linarith) hx.1)
      (fun ε hε hεδ => s5_T1n_a hy0 hε ((hεδ.trans_le (min_le_left _ _))) h1
        (by linarith [hεδ.trans_le (min_le_right _ _)]))
      (by fun_prop) (by ring)
  · rw [s5_g1n, ite_eq_right (not_le.mpr h1)]
    refine s5_tendsto_of_eventually (h := fun ε => 2 - ε)
      (lt_min (by linarith) (lt_min hx.1 (by linarith : 0 < x - (2 * y - 1))))
      (fun ε hε hεδ => s5_T1n_b hy0 hε ((hεδ.trans_le (min_le_left _ _)))
        (by linarith [hεδ.trans_le ((min_le_right _ _).trans (min_le_right _ _))])
        (by linarith [hεδ.trans_le ((min_le_right _ _).trans (min_le_left _ _))]) hx.2.le)
      (by fun_prop) (by ring)

lemma s5_tendsto_T2p (hy0 : 0 < y) (hy1 : y < 1) (hx : x ∈ Set.Ioo (0 : ℝ) 1)
    (h1 : x ≠ 1 - 2 * y) (h2 : x ≠ 1 - y) :
    Tendsto (fun ε => captureTime (pathS2 y ε) (loiterer ε x)) (𝓝[>] 0)
      (𝓝 (ENNReal.ofReal (s5_g2p y x))) := by
  rcases lt_or_gt_of_ne h1 with h1 | h1
  · rw [s5_g2p, ite_eq_left h1.le]
    refine s5_tendsto_of_eventually (h := fun ε => 1 + y - ε)
      (lt_min (by linarith) (by linarith : 0 < 1 - 2 * y - x))
      (fun ε hε hεδ => s5_T2p_c hy0 hε ((hεδ.trans_le (min_le_left _ _)))
        (by linarith [hεδ.trans_le (min_le_right _ _)]))
      (by fun_prop) (by ring)
  rcases lt_or_gt_of_ne h2 with h2 | h2
  · rw [s5_g2p, ite_eq_right (not_le.mpr h1), ite_eq_left h2.le]
    refine s5_tendsto_of_eventually (h := fun ε => x - 1 + 2 * y + ε)
      (lt_min (by linarith) (lt_min hx.1 (by linarith : 0 < 1 - y - x)))
      (fun ε hε hεδ => s5_T2p_b hε ((hεδ.trans_le (min_le_left _ _))) h1
        (by linarith [hεδ.trans_le ((min_le_right _ _).trans (min_le_right _ _))])
        (by linarith [hεδ.trans_le ((min_le_right _ _).trans (min_le_left _ _))]))
      (by fun_prop) (by ring)
  · rw [s5_g2p, ite_eq_right (not_le.mpr (by linarith)), ite_eq_right (not_le.mpr h2)]
    exact s5_tendsto_of_eventually (h := fun _ => y) (by linarith : 0 < (1 - y) / 4)
      (fun ε hε hεδ => s5_T2p_a hy0 hε hεδ h2 hx.2.le) (by fun_prop) rfl

lemma s5_tendsto_T2n (hy0 : 0 < y) (hy1 : y < 1) (hx : x ∈ Set.Ioo (0 : ℝ) 1)
    (h1 : x ≠ 2 * y - 1) :
    Tendsto (fun ε => captureTime (pathS2 y ε) (-loiterer ε x)) (𝓝[>] 0)
      (𝓝 (ENNReal.ofReal (s5_g2n y x))) := by
  rcases lt_or_gt_of_ne h1 with h1 | h1
  · rw [s5_g2n, ite_eq_left h1.le]
    refine s5_tendsto_of_eventually (h := fun ε => 2 * y - 1 + ε - x)
      (lt_min (by linarith) hx.1)
      (fun ε hε hεδ => s5_T2n_a hε ((hεδ.trans_le (min_le_left _ _))) h1
        (by linarith [hεδ.trans_le (min_le_right _ _)]))
      (by fun_prop) (by ring)
  · rw [s5_g2n, ite_eq_right (not_le.mpr h1)]
    refine s5_tendsto_of_eventually (h := fun ε => 2 + 2 * y + ε)
      (lt_min (by linarith) (by linarith : 0 < x - (2 * y - 1)))
      (fun ε hε hεδ => s5_T2n_b hy0 hε ((hεδ.trans_le (min_le_left _ _)))
        (by linarith [hεδ.trans_le (min_le_right _ _)]))
      (by fun_prop) (by ring)

end s5_limits

/-! ### Formula (15): integrating against the density `f` -/

lemma s5_half_sum {u v : ℝ} (hu : 0 ≤ u) (hv : 0 ≤ v) :
    (1 / 2 : ℝ≥0∞) * (ENNReal.ofReal u + ENNReal.ofReal v) = ENNReal.ofReal ((u + v) / 2) := by
  rw [← ENNReal.ofReal_add hu hv, show (1 / 2 : ℝ≥0∞) = ENNReal.ofReal (1 / 2) by
    rw [ENNReal.ofReal_div_of_pos (by norm_num)]; simp, ← ENNReal.ofReal_mul (by norm_num)]
  congr 1; ring

lemma s5_tendsto_lintegral_rho {ρ : Measure ℝ} [IsFiniteMeasure ρ] {F : ℝ → ℝ → ℝ≥0∞}
    {g : ℝ → ℝ} (hmeas : ∀ ε, Measurable (F ε)) (hbound : ∀ᶠ ε in 𝓝[>] (0 : ℝ), ∀ x, F ε x ≤ 7)
    (hlim : ∀ᵐ x ∂ρ, Tendsto (fun ε => F ε x) (𝓝[>] 0) (𝓝 (ENNReal.ofReal (g x)))) :
    Tendsto (fun ε => ∫⁻ x, F ε x ∂ρ) (𝓝[>] 0) (𝓝 (∫⁻ x, ENNReal.ofReal (g x) ∂ρ)) :=
  tendsto_lintegral_filter_of_dominated_convergence (fun _ => 7)
    (Eventually.of_forall hmeas) (hbound.mono fun _ h => Eventually.of_forall h)
    (by rw [lintegral_const]; exact ENNReal.mul_ne_top (by simp) (measure_ne_top ρ _)) hlim

section s5_rho

variable {f : ℝ → ℝ}

lemma s5_ae_rho (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0) (c₁ c₂ c₃ : ℝ) :
    ∀ᵐ x ∂(volume.withDensity fun t => ENNReal.ofReal (f t)),
      x ∈ Set.Ioo (0 : ℝ) 1 ∧ x ≠ c₁ ∧ x ≠ c₂ ∧ x ≠ c₃ := by
  have hac := withDensity_absolutelyContinuous (volume : Measure ℝ) (fun t => ENNReal.ofReal (f t))
  have h0 : ∀ᵐ x ∂(volume : Measure ℝ), x ≠ 0 ∧ x ≠ 1 ∧ x ≠ c₁ ∧ x ≠ c₂ ∧ x ≠ c₃ := by
    filter_upwards [Measure.ae_ne volume 0, Measure.ae_ne volume 1, Measure.ae_ne volume c₁,
      Measure.ae_ne volume c₂, Measure.ae_ne volume c₃] with x h1 h2 h3 h4 h5
      using ⟨h1, h2, h3, h4, h5⟩
  have hIcc : ∀ᵐ x ∂(volume.withDensity fun t => ENNReal.ofReal (f t)),
      x ∈ Set.Icc (0 : ℝ) 1 := by
    rw [ae_iff]
    have : {x : ℝ | ¬x ∈ Set.Icc (0 : ℝ) 1} = (Set.Icc (0 : ℝ) 1)ᶜ := rfl
    rw [this, withDensity_apply _ measurableSet_Icc.compl,
      setLIntegral_congr_fun measurableSet_Icc.compl (g := fun _ => 0)
        (fun x hx => by simp [hfsupp x hx])]
    simp
  filter_upwards [hac.ae_le h0, hIcc] with x hx hx'
  exact ⟨⟨lt_of_le_of_ne hx'.1 (Ne.symm hx.1), lt_of_le_of_ne hx'.2 hx.2.1⟩, hx.2.2⟩

lemma s5_integrable_mul (hf : Integrable f) (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0)
    {g : ℝ → ℝ} (hg : Measurable g) {C : ℝ} (hgC : ∀ x ∈ Set.Icc (0 : ℝ) 1, |g x| ≤ C) :
    Integrable (fun x => g x * f x) := by
  refine Integrable.mono' (hf.norm.const_mul C)
    (hg.aestronglyMeasurable.mul hf.aestronglyMeasurable) (Eventually.of_forall fun x => ?_)
  by_cases hx : x ∈ Set.Icc (0 : ℝ) 1
  · rw [norm_mul, Real.norm_eq_abs, Real.norm_eq_abs]
    exact mul_le_mul_of_nonneg_right (hgC x hx) (abs_nonneg _)
  · rw [hfsupp x hx]; simp

lemma s5_gf_nonneg (hf0 : ∀ t, 0 ≤ f t) (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0)
    {g : ℝ → ℝ} (hg0 : ∀ x ∈ Set.Icc (0 : ℝ) 1, 0 ≤ g x) (x : ℝ) : 0 ≤ g x * f x := by
  by_cases hx : x ∈ Set.Icc (0 : ℝ) 1
  · exact mul_nonneg (hg0 x hx) (hf0 x)
  · rw [hfsupp x hx, mul_zero]

lemma s5_lintegral_rho_eq (hf : Integrable f) (hf0 : ∀ t, 0 ≤ f t)
    (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0) {g : ℝ → ℝ} (hg : Measurable g) {C : ℝ}
    (hg0 : ∀ x ∈ Set.Icc (0 : ℝ) 1, 0 ≤ g x) (hgC : ∀ x ∈ Set.Icc (0 : ℝ) 1, g x ≤ C) :
    ∫⁻ x, ENNReal.ofReal (g x) ∂(volume.withDensity fun t => ENNReal.ofReal (f t)) =
      ENNReal.ofReal (∫ x, g x * f x) := by
  have hpt : ∀ x, ENNReal.ofReal (f x) * ENNReal.ofReal (g x) = ENNReal.ofReal (g x * f x) := by
    intro x
    by_cases hx : x ∈ Set.Icc (0 : ℝ) 1
    · rw [← ENNReal.ofReal_mul (hf0 x), mul_comm]
    · rw [hfsupp x hx]; simp
  rw [lintegral_withDensity_eq_lintegral_mul₀ hf.aemeasurable.ennreal_ofReal
      hg.ennreal_ofReal.aemeasurable,
    ofReal_integral_eq_lintegral_ofReal (s5_integrable_mul hf hfsupp hg (C := C)
      (fun x hx => abs_le.mpr ⟨by linarith [hg0 x hx, hgC x hx], hgC x hx⟩))
      (Eventually.of_forall (s5_gf_nonneg hf0 hfsupp hg0))]
  congr 1
  funext x
  exact hpt x

lemma s5_integral_split2 {h : ℝ → ℝ} (hh : Integrable h) (c : ℝ) :
    ∫ x, h x = (∫ x in Set.Iic c, h x) + ∫ x in Set.Ioi c, h x := by
  rw [← integral_add_compl measurableSet_Iic hh, Set.compl_Iic]

lemma s5_integral_split3 {h : ℝ → ℝ} (hh : Integrable h) {c₁ c₂ : ℝ} (hc : c₁ ≤ c₂) :
    ∫ x, h x = (∫ x in Set.Iic c₁, h x) + (∫ x in Set.Ioc c₁ c₂, h x) +
      ∫ x in Set.Ioi c₂, h x := by
  have hd : Disjoint (Set.Iic c₁) (Set.Ioc c₁ c₂) :=
    Set.disjoint_left.mpr fun x hx hx' => absurd hx (not_le.mpr hx'.1)
  rw [s5_integral_split2 hh c₂, ← Set.Iic_union_Ioc_eq_Iic hc,
    setIntegral_union hd measurableSet_Ioc hh.integrableOn hh.integrableOn]

lemma s5_integral_Iic_eq (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0) {h : ℝ → ℝ}
    (hh : Integrable (fun x => h x * f x)) (c : ℝ) :
    ∫ x in Set.Iic c, h x * f x = ∫ x in (0 : ℝ)..c, h x * f x := by
  rcases le_or_gt 0 c with hc | hc
  · have hd : Disjoint (Set.Iio (0 : ℝ)) (Set.Icc 0 c) :=
      Set.disjoint_left.mpr fun x hx hx' => absurd hx'.1 (not_le.mpr hx)
    rw [← Set.Iio_union_Icc_eq_Iic hc,
      setIntegral_union hd measurableSet_Icc hh.integrableOn hh.integrableOn,
      setIntegral_eq_zero_of_forall_eq_zero (fun x hx => by
        rw [hfsupp x (fun h' => absurd h'.1 (not_le.mpr hx)), mul_zero]),
      zero_add, integral_Icc_eq_integral_Ioc, intervalIntegral.integral_of_le hc]
  · rw [setIntegral_eq_zero_of_forall_eq_zero (fun x hx => by
        have hxc : x ≤ c := hx
        rw [hfsupp x (fun h' => by linarith [h'.1]), mul_zero]),
      intervalIntegral.integral_symm, intervalIntegral.integral_of_le hc.le,
      integral_Ioc_eq_integral_Ioo,
      setIntegral_eq_zero_of_forall_eq_zero (fun x hx => by
        rw [hfsupp x (fun h' => by linarith [h'.1, hx.2]), mul_zero]), neg_zero]

lemma s5_integral_Ioi (hf : Integrable f) (hf1 : ∫ t, f t = 1) (c : ℝ) :
    ∫ x in Set.Ioi c, f x = 1 - ∫ t in Set.Iic c, f t := by
  have := s5_integral_split2 hf c
  linarith

lemma s5_measurable_ite3 {c₁ c₂ : ℝ} {A B C : ℝ → ℝ} (hA : Measurable A) (hB : Measurable B)
    (hC : Measurable C) :
    Measurable fun x => if x ≤ c₁ then A x else if x ≤ c₂ then B x else C x :=
  Measurable.ite (measurableSet_le measurable_id measurable_const) hA
    (Measurable.ite (measurableSet_le measurable_id measurable_const) hB hC)

lemma s5_measurable_ite2 {c : ℝ} {A B : ℝ → ℝ} (hA : Measurable A) (hB : Measurable B) :
    Measurable fun x => if x ≤ c then A x else B x :=
  Measurable.ite (measurableSet_le measurable_id measurable_const) hA hB

variable {y : ℝ}

lemma s5_integral_g1p (hf : Integrable f) (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0)
    (hf1 : ∫ t, f t = 1) (hy0 : 0 < y) (hy1 : y < 1) :
    ∫ x, s5_g1p y x * f x = (∫ t in (0 : ℝ)..(1 - 2 * y), (1 - t) * f t) +
      (∫ t in (1 - 2 * y)..(1 - y), (t - 1 + 2 * y) * f t) +
      y * (1 - ∫ t in Set.Iic (1 - y), f t) := by
  have hm : Measurable (s5_g1p y) :=
    s5_measurable_ite3 (by fun_prop) (by fun_prop) measurable_const
  have hi : Integrable (fun x => s5_g1p y x * f x) := s5_integrable_mul hf hfsupp hm (C := 4)
    (fun x hx => by
      unfold s5_g1p; split_ifs <;> rw [abs_le] <;> constructor <;> linarith [hx.1, hx.2])
  rw [s5_integral_split3 hi (show 1 - 2 * y ≤ 1 - y by linarith),
    setIntegral_congr_fun measurableSet_Iic (g := fun x => (1 - x) * f x)
      (fun x hx => by simp only [s5_g1p, ite_eq_left (show x ≤ 1 - 2 * y from hx)]),
    setIntegral_congr_fun measurableSet_Ioc (g := fun x => (x - 1 + 2 * y) * f x)
      (fun x hx => by
        simp only [s5_g1p, ite_eq_right (not_le.mpr hx.1), ite_eq_left hx.2]),
    setIntegral_congr_fun measurableSet_Ioi (g := fun x => y * f x)
      (fun x hx => by
        simp only [s5_g1p, ite_eq_right (not_le.mpr ((show 1 - 2 * y ≤ 1 - y by linarith).trans_lt
          (Set.mem_Ioi.mp hx))), ite_eq_right (not_le.mpr (Set.mem_Ioi.mp hx))]),
    s5_integral_Iic_eq hfsupp (s5_integrable_mul hf hfsupp (by fun_prop) (C := 4)
      (fun x hx => by rw [abs_le]; constructor <;> linarith [hx.1, hx.2])),
    ← intervalIntegral.integral_of_le (show 1 - 2 * y ≤ 1 - y by linarith),
    integral_const_mul, s5_integral_Ioi hf hf1]

lemma s5_integral_g1n (hf : Integrable f) (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0)
    (hf1 : ∫ t, f t = 1) (hy0 : 0 < y) (hy1 : y < 1) :
    ∫ x, s5_g1n y x * f x = (∫ t in (0 : ℝ)..(2 * y - 1), (2 * y - 1 - t) * f t) +
      2 * (1 - ∫ t in Set.Iic (2 * y - 1), f t) := by
  have hm : Measurable (s5_g1n y) := s5_measurable_ite2 (by fun_prop) measurable_const
  have hi : Integrable (fun x => s5_g1n y x * f x) := s5_integrable_mul hf hfsupp hm (C := 4)
    (fun x hx => by
      unfold s5_g1n; split_ifs <;> rw [abs_le] <;> constructor <;> linarith [hx.1, hx.2])
  rw [s5_integral_split2 hi (2 * y - 1),
    setIntegral_congr_fun measurableSet_Iic (g := fun x => (2 * y - 1 - x) * f x)
      (fun x hx => by simp only [s5_g1n, ite_eq_left (show x ≤ 2 * y - 1 from hx)]),
    setIntegral_congr_fun measurableSet_Ioi (g := fun x => 2 * f x)
      (fun x hx => by simp only [s5_g1n, ite_eq_right (not_le.mpr (Set.mem_Ioi.mp hx))]),
    s5_integral_Iic_eq hfsupp (s5_integrable_mul hf hfsupp (by fun_prop) (C := 4)
      (fun x hx => by rw [abs_le]; constructor <;> linarith [hx.1, hx.2])),
    integral_const_mul, s5_integral_Ioi hf hf1]

lemma s5_integral_g2p (hf : Integrable f) (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0)
    (hf1 : ∫ t, f t = 1) (hy0 : 0 < y) (hy1 : y < 1) :
    ∫ x, s5_g2p y x * f x = (1 + y) * (∫ t in Set.Iic (1 - 2 * y), f t) +
      (∫ t in (1 - 2 * y)..(1 - y), (t - 1 + 2 * y) * f t) +
      y * (1 - ∫ t in Set.Iic (1 - y), f t) := by
  have hm : Measurable (s5_g2p y) :=
    s5_measurable_ite3 measurable_const (by fun_prop) measurable_const
  have hi : Integrable (fun x => s5_g2p y x * f x) := s5_integrable_mul hf hfsupp hm (C := 4)
    (fun x hx => by
      unfold s5_g2p; split_ifs <;> rw [abs_le] <;> constructor <;> linarith [hx.1, hx.2])
  rw [s5_integral_split3 hi (show 1 - 2 * y ≤ 1 - y by linarith),
    setIntegral_congr_fun measurableSet_Iic (g := fun x => (1 + y) * f x)
      (fun x hx => by simp only [s5_g2p, ite_eq_left (show x ≤ 1 - 2 * y from hx)]),
    setIntegral_congr_fun measurableSet_Ioc (g := fun x => (x - 1 + 2 * y) * f x)
      (fun x hx => by
        simp only [s5_g2p, ite_eq_right (not_le.mpr hx.1), ite_eq_left hx.2]),
    setIntegral_congr_fun measurableSet_Ioi (g := fun x => y * f x)
      (fun x hx => by
        simp only [s5_g2p, ite_eq_right (not_le.mpr ((show 1 - 2 * y ≤ 1 - y by linarith).trans_lt
          (Set.mem_Ioi.mp hx))), ite_eq_right (not_le.mpr (Set.mem_Ioi.mp hx))]),
    integral_const_mul, ← intervalIntegral.integral_of_le (show 1 - 2 * y ≤ 1 - y by linarith),
    integral_const_mul, s5_integral_Ioi hf hf1]

lemma s5_integral_g2n (hf : Integrable f) (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0)
    (hf1 : ∫ t, f t = 1) (hy0 : 0 < y) (hy1 : y < 1) :
    ∫ x, s5_g2n y x * f x = (∫ t in (0 : ℝ)..(2 * y - 1), (2 * y - 1 - t) * f t) +
      (2 + 2 * y) * (1 - ∫ t in Set.Iic (2 * y - 1), f t) := by
  have hm : Measurable (s5_g2n y) := s5_measurable_ite2 (by fun_prop) measurable_const
  have hi : Integrable (fun x => s5_g2n y x * f x) := s5_integrable_mul hf hfsupp hm (C := 4)
    (fun x hx => by
      unfold s5_g2n; split_ifs <;> rw [abs_le] <;> constructor <;> linarith [hx.1, hx.2])
  rw [s5_integral_split2 hi (2 * y - 1),
    setIntegral_congr_fun measurableSet_Iic (g := fun x => (2 * y - 1 - x) * f x)
      (fun x hx => by simp only [s5_g2n, ite_eq_left (show x ≤ 2 * y - 1 from hx)]),
    setIntegral_congr_fun measurableSet_Ioi (g := fun x => (2 + 2 * y) * f x)
      (fun x hx => by simp only [s5_g2n, ite_eq_right (not_le.mpr (Set.mem_Ioi.mp hx))]),
    s5_integral_Iic_eq hfsupp (s5_integrable_mul hf hfsupp (by fun_prop) (C := 4)
      (fun x hx => by rw [abs_le]; constructor <;> linarith [hx.1, hx.2])),
    integral_const_mul, s5_integral_Ioi hf hf1]

end s5_rho

section s5_eq15

variable {f : ℝ → ℝ} {y : ℝ}

lemma s5_value_S1 (hf : Integrable f) (hf0 : ∀ t, 0 ≤ f t)
    (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0) (hf1 : ∫ t, f t = 1) (hy0 : 0 < y)
    (hy1 : y < 1) :
    (1 / 2 : ℝ≥0∞) *
        ((∫⁻ x, ENNReal.ofReal (s5_g1p y x) ∂(volume.withDensity fun t => ENNReal.ofReal (f t)))
          + ∫⁻ x, ENNReal.ofReal (s5_g1n y x) ∂(volume.withDensity fun t => ENNReal.ofReal (f t)))
      = ENNReal.ofReal (formula15S1 (fun u => ∫ t in Set.Iic u, f t) f y) := by
  have hb1 : ∀ x ∈ Set.Icc (0 : ℝ) 1, 0 ≤ s5_g1p y x ∧ s5_g1p y x ≤ 4 := fun x hx => by
    unfold s5_g1p; split_ifs <;> constructor <;> linarith [hx.1, hx.2]
  have hb2 : ∀ x ∈ Set.Icc (0 : ℝ) 1, 0 ≤ s5_g1n y x ∧ s5_g1n y x ≤ 4 := fun x hx => by
    unfold s5_g1n; split_ifs <;> constructor <;> linarith [hx.1, hx.2]
  have hm1 : Measurable (s5_g1p y) :=
    s5_measurable_ite3 (by fun_prop) (by fun_prop) measurable_const
  have hm2 : Measurable (s5_g1n y) := s5_measurable_ite2 (by fun_prop) measurable_const
  rw [s5_lintegral_rho_eq hf hf0 hfsupp hm1 (fun x hx => (hb1 x hx).1) (fun x hx => (hb1 x hx).2),
    s5_lintegral_rho_eq hf hf0 hfsupp hm2 (fun x hx => (hb2 x hx).1) (fun x hx => (hb2 x hx).2),
    s5_half_sum (integral_nonneg (s5_gf_nonneg hf0 hfsupp fun x hx => (hb1 x hx).1))
      (integral_nonneg (s5_gf_nonneg hf0 hfsupp fun x hx => (hb2 x hx).1)),
    s5_integral_g1p hf hfsupp hf1 hy0 hy1, s5_integral_g1n hf hfsupp hf1 hy0 hy1]
  simp only [formula15S1]
  congr 1
  ring

lemma s5_value_S2 (hf : Integrable f) (hf0 : ∀ t, 0 ≤ f t)
    (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0) (hf1 : ∫ t, f t = 1) (hy0 : 0 < y)
    (hy1 : y < 1) :
    (1 / 2 : ℝ≥0∞) *
        ((∫⁻ x, ENNReal.ofReal (s5_g2p y x) ∂(volume.withDensity fun t => ENNReal.ofReal (f t)))
          + ∫⁻ x, ENNReal.ofReal (s5_g2n y x) ∂(volume.withDensity fun t => ENNReal.ofReal (f t)))
      = ENNReal.ofReal (formula15S2 (fun u => ∫ t in Set.Iic u, f t) f y) := by
  have hb1 : ∀ x ∈ Set.Icc (0 : ℝ) 1, 0 ≤ s5_g2p y x ∧ s5_g2p y x ≤ 4 := fun x hx => by
    unfold s5_g2p; split_ifs <;> constructor <;> linarith [hx.1, hx.2]
  have hb2 : ∀ x ∈ Set.Icc (0 : ℝ) 1, 0 ≤ s5_g2n y x ∧ s5_g2n y x ≤ 4 := fun x hx => by
    unfold s5_g2n; split_ifs <;> constructor <;> linarith [hx.1, hx.2]
  have hm1 : Measurable (s5_g2p y) :=
    s5_measurable_ite3 measurable_const (by fun_prop) measurable_const
  have hm2 : Measurable (s5_g2n y) := s5_measurable_ite2 (by fun_prop) measurable_const
  rw [s5_lintegral_rho_eq hf hf0 hfsupp hm1 (fun x hx => (hb1 x hx).1) (fun x hx => (hb1 x hx).2),
    s5_lintegral_rho_eq hf hf0 hfsupp hm2 (fun x hx => (hb2 x hx).1) (fun x hx => (hb2 x hx).2),
    s5_half_sum (integral_nonneg (s5_gf_nonneg hf0 hfsupp fun x hx => (hb1 x hx).1))
      (integral_nonneg (s5_gf_nonneg hf0 hfsupp fun x hx => (hb2 x hx).1)),
    s5_integral_g2p hf hfsupp hf1 hy0 hy1, s5_integral_g2n hf hfsupp hf1 hy0 hy1]
  simp only [formula15S2]
  congr 1
  ring

end s5_eq15

/-- **Formula (15)** (`eq:15`), corrected. Let the loiterers start with a density `f` on
`[0, 1]` (for instance the uniform density of Theorem 16). Ignoring `ε`, the payoffs of `S₁` and
`S₂` are `V(S₁, E) = 3`, `V(S₂, E) = 1 + 2y`, and `V(S₁, h_Φ)`, `V(S₂, h_Φ)` as in
`formula15S1`, `formula15S2`. The paper's display omits the factors `2y - 1 - t`, `1 - t` and
`t - 1 + 2y` in the integrands and writes `Φ(1 - 2y)` for `∫_0^{1-2y} (1 - t) f(t) dt`.

The proof follows the paper's explanation after (15): for `ε` small, the capture time of each
loiterer is computed exactly (`s5_T1p_a` … `s5_T2n_b`: met where it waits, in the running bunch at
time `y`, when it starts running, on its way back to `+1`, or at the end `-1`), and the payoffs
converge by dominated convergence (`s5_tendsto_lintegral_rho`). Departure from the paper's route:
Proposition 5, which the paper uses to single out the paths `S₁`, `S₂`, is not needed for the
payoffs of these two given paths and is not used. -/
theorem equation15 {f : ℝ → ℝ} (hf : MeasureTheory.Integrable f) (hf0 : ∀ t, 0 ≤ f t)
    (hfsupp : ∀ t, t ∉ Set.Icc (0 : ℝ) 1 → f t = 0) (hf1 : ∫ t, f t = 1)
    {y : ℝ} (hy : y ∈ Set.Ioo (0 : ℝ) 1) :
    let ρ := volume.withDensity fun t => ENNReal.ofReal (f t)
    let Φ := fun u => ∫ t in Set.Iic u, f t
    Tendsto (fun ε => ∫⁻ H, captureTime (pathS1 y ε) H ∂(symDiracH hiderE)) (𝓝[>] 0) (𝓝 3) ∧
    Tendsto (fun ε => ∫⁻ H, captureTime (pathS2 y ε) H ∂(symDiracH hiderE)) (𝓝[>] 0)
      (𝓝 (ENNReal.ofReal (1 + 2 * y))) ∧
    Tendsto (fun ε => ∫⁻ H, captureTime (pathS1 y ε) H ∂(hPhi ρ ε)) (𝓝[>] 0)
      (𝓝 (ENNReal.ofReal (formula15S1 Φ f y))) ∧
    Tendsto (fun ε => ∫⁻ H, captureTime (pathS2 y ε) H ∂(hPhi ρ ε)) (𝓝[>] 0)
      (𝓝 (ENNReal.ofReal (formula15S2 Φ f y))) := by
  intro ρ Φ
  obtain ⟨hy0, hy1⟩ := hy
  have : IsFiniteMeasure ρ := isFiniteMeasure_withDensity_ofReal hf.2
  have hδ : (0 : ℝ) < (1 - y) / 4 := by linarith
  have hev : ∀ᶠ ε in 𝓝[>] (0 : ℝ), 0 < ε ∧ ε < (1 - y) / 4 :=
    Ioo_mem_nhdsGT hδ
  have hae := s5_ae_rho hfsupp (1 - 2 * y) (1 - y) (2 * y - 1)
  refine ⟨?_, ?_, ?_, ?_⟩
  · have h := s5_tendsto_of_eventually
      (F := fun ε => ∫⁻ H, captureTime (pathS1 y ε) H ∂(symDiracH hiderE))
      (h := fun ε => (4 - ε + (2 - ε)) / 2) (c := 3) hδ (fun ε hε hεδ => by
        rw [s5_lintegral_symDiracH _ _ s5_hiderE_mem, s5_T1E hy0 hε hεδ, s5_T1negE hy0 hε hεδ,
          s5_half_sum (by linarith) (by linarith)])
      (by fun_prop) (by norm_num)
    simpa using h
  · exact s5_tendsto_of_eventually
      (F := fun ε => ∫⁻ H, captureTime (pathS2 y ε) H ∂(symDiracH hiderE))
      (h := fun ε => (2 * y + ε + (2 + 2 * y + ε)) / 2) hδ (fun ε hε hεδ => by
        rw [s5_lintegral_symDiracH _ _ s5_hiderE_mem, s5_T2E hy0 hε hεδ, s5_T2negE hy0 hε hεδ,
          s5_half_sum (by linarith) (by linarith)])
      (by fun_prop) (by ring)
  · have hlim := ENNReal.Tendsto.const_mul (a := (1 / 2 : ℝ≥0∞))
      (Tendsto.add
        (s5_tendsto_lintegral_rho (ρ := ρ) (fun ε => s5_measurable_T_loiterer ε (pathS1 y ε))
          (hev.mono fun ε hε x => s5_T1p_le hy0 hε.1 hε.2 x)
          (hae.mono fun x hx => s5_tendsto_T1p hy0 hy1 hx.1 hx.2.1 hx.2.2.1))
        (s5_tendsto_lintegral_rho (ρ := ρ)
          (fun ε => s5_measurable_T_neg_loiterer ε (pathS1 y ε))
          (hev.mono fun ε hε x => s5_T1n_le hy0 hε.1 hε.2 x)
          (hae.mono fun x hx => s5_tendsto_T1n hy0 hy1 hx.1 hx.2.2.2)))
      (Or.inr (by norm_num))
    rw [s5_value_S1 hf hf0 hfsupp hf1 hy0 hy1] at hlim
    refine hlim.congr' ?_
    filter_upwards [hev] with ε hε
    exact (s5_lintegral_hPhi hε.1.le ρ _).symm
  · have hlim := ENNReal.Tendsto.const_mul (a := (1 / 2 : ℝ≥0∞))
      (Tendsto.add
        (s5_tendsto_lintegral_rho (ρ := ρ) (fun ε => s5_measurable_T_loiterer ε (pathS2 y ε))
          (hev.mono fun ε hε x => s5_T2p_le hy0 hε.1 hε.2 x)
          (hae.mono fun x hx => s5_tendsto_T2p hy0 hy1 hx.1 hx.2.1 hx.2.2.1))
        (s5_tendsto_lintegral_rho (ρ := ρ)
          (fun ε => s5_measurable_T_neg_loiterer ε (pathS2 y ε))
          (hev.mono fun ε hε x => s5_T2n_le hy0 hε.1 hε.2 x)
          (hae.mono fun x hx => s5_tendsto_T2n hy0 hy1 hx.1 hx.2.2.2)))
      (Or.inr (by norm_num))
    rw [s5_value_S2 hf hf0 hfsupp hf1 hy0 hy1] at hlim
    refine hlim.congr' ?_
    filter_upwards [hev] with ε hε
    exact (s5_lintegral_hPhi hε.1.le ρ _).symm

/-- **Theorem 16** (`thm:16`). If the hider uses the mixed strategy `γ`, the optimal response of
the searcher gives the value `15/11` (as `ε → 0`). In particular `V ≥ 15/11`.

The first part is the precise form of "the optimal response of the searcher gives a matrix game
with value 15/11": the infimum is over every searcher path, whereas the paper reduces to the paths
`S₁`, `S₂` by an argument it leaves to the reader.

Departure from the paper: the paper's proof uses formula (15) and Proposition 5 to reduce the
searcher to the two paths `S₁`, `S₂` (and then reads the minimisation off Figures 3 and 4).
Proposition 5 does not apply to the continuous mixture `h_Φ`, and the reduction to `S₁`, `S₂` is
left to the reader, so neither (15) nor Proposition 5 is used here. Instead, keeping the paper's
structure (the first time `y` at which `S` gets `ε`-close to a sweeper, the immobile loiterers
caught before it, the running bunch caught at it, and the two continuations), every searcher
path `S` gets the lower bound `E_γ T(S, ·) ≥ (30 - 200ε)/22` (`s5_lower`): `τ` is the exit time
from the diamond `|p| < 1 - ε - t` (`s5_exists_tau`); the loiterers met before `τ` sit in
`S([0, τ])` and cost at least `L²/2` (`s5_visited`, a layer cake bound); after contact with the
front the unvisited negative loiterers are met at `-1` (`s5_neg_after`), the unvisited positive
ones not before `ℓ(x)` (`s5_pos_after`); the cases `b < a`, `a < b` (`s5_caseI`) and the case
that `S` stays inside the diamond (`s5_caseII`) end with explicit polynomial inequalities. The
value is attained by the sweeper `A` (`s5_upper`: `E_γ T(A, ·) ≤ 15/11`). -/
theorem theorem16 :
    Tendsto (fun ε : ℝ => ⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(gamma ε)) (𝓝[>] 0)
        (𝓝 (15 / 11)) ∧
      (15 / 11 : ℝ≥0∞) ≤ lowerValue := by
  have hT : Tendsto (fun ε : ℝ => ⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(gamma ε))
      (𝓝[>] 0) (𝓝 (15 / 11)) := by
    have hg : Tendsto (fun ε : ℝ => ENNReal.ofReal ((30 - 200 * ε) / 22)) (𝓝[>] 0)
        (𝓝 (15 / 11)) := by
      have h1 : Tendsto (fun ε : ℝ => (30 - 200 * ε) / 22) (𝓝 0) (𝓝 (15 / 11)) := by
        have hc : Continuous fun ε : ℝ => (30 - 200 * ε) / 22 := by fun_prop
        have := hc.tendsto 0
        convert this using 2
        norm_num
      have h2 := (ENNReal.continuous_ofReal.tendsto _).comp
        (h1.mono_left (nhdsWithin_le_nhds (s := Set.Ioi 0)))
      have e : (15 / 11 : ℝ≥0∞) = ENNReal.ofReal (15 / 11) := by
        exact_mod_cast s5_ofReal_ratio 15 11 (by norm_num)
      rw [e]
      exact h2
    refine tendsto_of_tendsto_of_tendsto_of_le_of_le' hg tendsto_const_nhds ?_ ?_
    · filter_upwards [Ioc_mem_nhdsGT (show (0 : ℝ) < 1 / 100 by norm_num)] with ε hε
      exact le_iInf fun S => s5_lower hε.1 hε.2 S.2
    · filter_upwards [Ioc_mem_nhdsGT (show (0 : ℝ) < 1 / 100 by norm_num)] with ε hε
      exact (iInf_le _ ⟨sweeperA, sweeperA_mem⟩).trans (s5_upper hε.1 (by linarith [hε.2]))
  refine ⟨hT, le_of_tendsto hT ?_⟩
  filter_upwards [Ioo_mem_nhdsGT (show (0 : ℝ) < 1 / 2 by norm_num)] with ε hε
  have := s5_isProb_gamma hε.1.le hε.2
  rw [lowerValue]
  exact le_iSup (fun ν : ProbabilityMeasure hiderPaths =>
    ⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(ν : Measure hiderPaths)) ⟨gamma ε, this⟩

end PrincessMonster
