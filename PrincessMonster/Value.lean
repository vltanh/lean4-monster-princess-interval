module

public import PrincessMonster.CaptureTime
public import External.AlpernGal.Minimax
import Mathlib.Topology.UniformSpace.Ascoli
import Mathlib.Topology.UniformSpace.CompactConvergence
import Mathlib.Topology.MetricSpace.UniformConvergence
import Mathlib.MeasureTheory.Measure.DiracProba

/-!
# Section 1: the game has a value

The paper (Section 1): "Taking the topology of uniform convergence on compact subsets, the payoff
function `T` is upper semicontinuous and the searcher mixed strategy space is compact Hausdorff.
Consequently the minimax theorem of Alpern and Gal can be used ... to establish the existence of
the value `V(Q)`, an optimal mixed searcher strategy, and an `ε`-optimal hider mixed strategy."
And after Proposition 4: "for any `ε` there exists an `ε`-optimal finite mixed strategy".

* `lowerSemicontinuous_captureTime`: the capture time is *lower* semicontinuous (it is not upper
  semicontinuous: a hider path that touches a searcher path and is pushed away is met much later);
* `compactSpace_searcherPaths`: the searcher's strategy space is compact (Arzelà–Ascoli);
* `value_exists`: the lower and upper values coincide, the searcher has an optimal mixed strategy,
  and the hider has `ε`-optimal finitely supported mixed strategies.
-/

@[expose] public section

open scoped NNReal ENNReal Topology
open MeasureTheory Filter

namespace PrincessMonster

/-- Paths close to a given one, uniformly on a compact set, form a neighbourhood of it. -/
private lemma val_eventually_dist_lt (S₀ : C(ℝ≥0, ℝ)) {K : Set ℝ≥0} (hK : IsCompact K) {ε : ℝ}
    (hε : 0 < ε) : ∀ᶠ S in 𝓝 S₀, ∀ t ∈ K, dist (S₀ t) (S t) < ε :=
  Metric.tendstoUniformlyOn_iff.1
    ((ContinuousMap.tendsto_iff_forall_isCompact_tendstoUniformlyOn.1 tendsto_id) K hK) ε hε

/-- The capture time is lower semicontinuous on pairs of paths, for the topology of uniform
convergence on compact sets (`claim:value`; the paper says *upper* semicontinuous). -/
theorem lowerSemicontinuous_captureTime :
    LowerSemicontinuous fun p : C(ℝ≥0, ℝ) × C(ℝ≥0, ℝ) => captureTime p.1 p.2 := by
  rintro ⟨S₀, H₀⟩ c hc
  obtain ⟨c', hcc', hc'T⟩ := exists_between hc
  have hc'top : c' ≠ ⊤ := ne_top_of_lt hc'T
  set b : ℝ≥0 := c'.toNNReal with hb
  have hbc' : ((b : ℝ≥0) : ℝ≥0∞) = c' := ENNReal.coe_toNNReal hc'top
  -- before time `b` the two paths differ
  have hne : ∀ t ∈ Set.Icc (0 : ℝ≥0) b, S₀ t ≠ H₀ t := by
    intro t ht heq
    have h1 : captureTime S₀ H₀ ≤ t := captureTime_le heq
    have h2 : (t : ℝ≥0∞) ≤ c' := hbc' ▸ ENNReal.coe_le_coe.mpr ht.2
    exact absurd (hc'T.trans_le (h1.trans h2)) (lt_irrefl _)
  -- their distance has a positive minimum `η` on `[0, b]`
  obtain ⟨t₀, ht₀, hmin⟩ :=
    isCompact_Icc.exists_isMinOn (Set.nonempty_Icc.2 (zero_le : (0 : ℝ≥0) ≤ b))
    ((continuous_abs.comp (S₀.continuous.sub H₀.continuous)).continuousOn)
  set η := |S₀ t₀ - H₀ t₀| with hη_def
  have hη : 0 < η := abs_pos.2 (sub_ne_zero.2 (hne t₀ ht₀))
  have hS := val_eventually_dist_lt S₀ (isCompact_Icc (a := (0 : ℝ≥0)) (b := b)) (half_pos hη)
  have hH := val_eventually_dist_lt H₀ (isCompact_Icc (a := (0 : ℝ≥0)) (b := b)) (half_pos hη)
  have hp : ∀ᶠ p in 𝓝 (S₀, H₀), (∀ t ∈ Set.Icc (0 : ℝ≥0) b, dist (S₀ t) (p.1 t) < η / 2) ∧
      ∀ t ∈ Set.Icc (0 : ℝ≥0) b, dist (H₀ t) (p.2 t) < η / 2 := by
    rw [nhds_prod_eq]
    exact hS.prod_mk hH
  filter_upwards [hp] with p hp
  refine hcc'.trans_le ?_
  rw [← hbc']
  refine le_captureTime_of_ne fun t ht heq => ?_
  have htI : t ∈ Set.Icc (0 : ℝ≥0) b := ⟨zero_le, ht.le⟩
  have h1 := hp.1 t htI
  have h2 := hp.2 t htI
  have h3 : η ≤ |S₀ t - H₀ t| := hmin htI
  rw [Real.dist_eq] at h1 h2
  have h4 : |S₀ t - H₀ t| ≤ |S₀ t - p.1 t| + |H₀ t - p.2 t| := by
    rw [heq]
    calc |S₀ t - H₀ t| = |(S₀ t - p.2 t) - (H₀ t - p.2 t)| := by ring_nf
      _ ≤ |S₀ t - p.2 t| + |H₀ t - p.2 t| := abs_sub _ _
  linarith

/-- The values of the searcher's paths, as functions: `1`-Lipschitz functions into `[-1, 1]`. -/
private lemma val_image_searcherPaths :
    ContinuousMap.toFun '' searcherPaths =
      {f : ℝ≥0 → ℝ | (∀ t, f t ∈ Set.Icc (-1 : ℝ) 1) ∧
        ∀ t t' : ℝ≥0, |f t - f t'| ≤ |(t : ℝ) - t'|} := by
  ext f
  constructor
  · rintro ⟨S, hS, rfl⟩
    exact hS
  · rintro hf
    have hcont : Continuous f := by
      refine (LipschitzWith.of_dist_le_mul (K := 1) fun t t' => ?_).continuous
      rw [Real.dist_eq, NNReal.dist_eq, NNReal.coe_one, one_mul]
      exact hf.2 t t'
    exact ⟨⟨f, hcont⟩, hf, rfl⟩

/-- The searcher's pure strategy space is compact (`claim:value`; Arzelà–Ascoli: the paths are
equicontinuous, being `1`-Lipschitz, and form a closed set of functions into `[-1, 1]` for the
topology of pointwise convergence). -/
instance compactSpace_searcherPaths : CompactSpace searcherPaths := by
  rw [← isCompact_iff_compactSpace]
  refine ArzelaAscoli.isCompact_of_equicontinuous searcherPaths ?_ ?_
  · rw [val_image_searcherPaths]
    refine IsCompact.of_isClosed_subset (isCompact_univ_pi fun _ => isCompact_Icc (a := (-1 : ℝ))
      (b := 1)) ?_ fun f hf => Set.mem_univ_pi.2 hf.1
    simp only [Set.ofPred_and, Set.ofPred_forall]
    refine IsClosed.inter ?_ ?_
    · exact isClosed_iInter fun t => isClosed_Icc.preimage (continuous_apply t)
    · exact isClosed_iInter fun t => isClosed_iInter fun t' =>
        isClosed_le ((continuous_apply t).sub (continuous_apply t')).abs continuous_const
  · refine (LipschitzWith.uniformEquicontinuous _ 1 fun S => ?_).equicontinuous
    refine LipschitzWith.of_dist_le_mul fun t t' => ?_
    rw [Real.dist_eq, NNReal.dist_eq, NNReal.coe_one, one_mul]
    exact S.2.2 t t'


/-! ### The value -/

/-- The capture time is lower semicontinuous in the searcher's path. -/
lemma val_lowerSemicontinuous_captureTime_left (H : C(ℝ≥0, ℝ)) :
    LowerSemicontinuous fun S : searcherPaths => captureTime S H :=
  lowerSemicontinuous_captureTime.comp (g := fun S : searcherPaths => ((S : C(ℝ≥0, ℝ)), H))
    (continuous_subtype_val.prodMk continuous_const)

/-- The capture time is lower semicontinuous in the hider's path. -/
lemma val_lowerSemicontinuous_captureTime_right (S : C(ℝ≥0, ℝ)) :
    LowerSemicontinuous fun H : hiderPaths => captureTime S H :=
  lowerSemicontinuous_captureTime.comp (g := fun H : hiderPaths => (S, (H : C(ℝ≥0, ℝ))))
    (continuous_const.prodMk continuous_subtype_val)

/-- The searcher path that sweeps the interval once, from `-1` to `1`, and then stays at `1`. -/
private def val_sweep : C(ℝ≥0, ℝ) :=
  pathOf (fun t => min 1 (t - 1)) (continuous_const.min (continuous_id.sub continuous_const))

private lemma val_sweep_mem : val_sweep ∈ searcherPaths := by
  refine pathOf_mem_searcherPaths _ (fun s t => ?_) (fun t ht => ⟨?_, min_le_left _ _⟩)
  · calc |min 1 (s - 1) - min 1 (t - 1)| ≤ max |1 - 1| |(s - 1) - (t - 1)| :=
          abs_min_sub_min_le_max _ _ _ _
      _ = |s - t| := by simp
  · exact le_min (by norm_num) (by linarith)

/-- The sweep meets every hider path by time `2`. -/
private lemma val_captureTime_sweep_le {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    captureTime val_sweep H ≤ 2 := by
  have h := captureTime_le_of_le_of_le (S := val_sweep) (H := H) (t₁ := 0) (t₂ := 2) zero_le
    (by simp only [val_sweep, pathOf_apply, NNReal.coe_zero]; norm_num; exact (hH 0).1)
    (by simp only [val_sweep, pathOf_apply]; norm_num; exact (hH 2).2)
  simpa using h

/-- The upper value is at most `2` (the sweep). -/
lemma val_upperValue_le_two : upperValue ≤ 2 := by
  refine (iInf_le _ (diracProba (⟨val_sweep, val_sweep_mem⟩ : searcherPaths))).trans ?_
  refine iSup_le fun H => ?_
  rw [show ((diracProba (⟨val_sweep, val_sweep_mem⟩ : searcherPaths) :
      ProbabilityMeasure searcherPaths) : Measure searcherPaths) =
      Measure.dirac ⟨val_sweep, val_sweep_mem⟩ from rfl,
    lintegral_dirac' _ (val_lowerSemicontinuous_captureTime_left H).measurable]
  exact val_captureTime_sweep_le H.2

/-- **The game has a value** (`claim:value`). The lower and upper values coincide; the searcher
has an optimal mixed strategy; and for every `ε > 0` the hider has an `ε`-optimal mixed strategy
supported on finitely many paths.

Proof: the minimax theorem of Alpern and Gal (`External.AlpernGal.minimax`), with the capture
time lower semicontinuous in the searcher's path and the searcher's space compact. The ε-optimal
hider strategies need `lowerValue < ∞`, from `val_upperValue_le_two`. -/
theorem value_exists :
    lowerValue = upperValue ∧
      (∃ μ : ProbabilityMeasure searcherPaths,
        ⨆ H : hiderPaths, ∫⁻ S, captureTime S H ∂(μ : Measure searcherPaths) = upperValue) ∧
      ∀ ε : ℝ≥0∞, 0 < ε → ∃ (s : Finset hiderPaths) (w : hiderPaths → ℝ≥0∞),
        ∑ H ∈ s, w H = 1 ∧
          lowerValue ≤ (⨅ S : searcherPaths, ∑ H ∈ s, w H * captureTime S H) + ε := by
  have hne : Nonempty searcherPaths := ⟨⟨val_sweep, val_sweep_mem⟩⟩
  -- the minimax theorem of Alpern and Gal
  obtain ⟨hopt, hval⟩ := External.AlpernGal.minimax (X := searcherPaths) (Y := hiderPaths)
    (fun S H => captureTime S H) fun H => val_lowerSemicontinuous_captureTime_left H
  -- finitely supported hider strategies are mixed strategies
  have hge : ∀ (s : Finset hiderPaths) (w : hiderPaths → ℝ≥0∞), ∑ H ∈ s, w H = 1 →
      ⨅ S : searcherPaths, ∑ H ∈ s, w H * captureTime S H ≤ lowerValue := by
    intro s w hw
    let ν : ProbabilityMeasure hiderPaths :=
      ⟨∑ H ∈ s, w H • Measure.dirac H, ⟨by simp [hw]⟩⟩
    have hν : ∀ S : searcherPaths, ∫⁻ H, captureTime S H ∂(ν : Measure hiderPaths) =
        ∑ H ∈ s, w H * captureTime S H := by
      intro S
      rw [show (ν : Measure hiderPaths) = ∑ H ∈ s, w H • Measure.dirac H from rfl,
        lintegral_finsetSum_measure]
      refine Finset.sum_congr rfl fun H _ => ?_
      rw [lintegral_smul_measure,
        lintegral_dirac' _ (val_lowerSemicontinuous_captureTime_right S).measurable, smul_eq_mul]
    calc ⨅ S : searcherPaths, ∑ H ∈ s, w H * captureTime S H
        = ⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(ν : Measure hiderPaths) := by
          simp_rw [hν]
      _ ≤ lowerValue :=
          le_iSup (fun ν : ProbabilityMeasure hiderPaths =>
            ⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(ν : Measure hiderPaths)) ν
  -- weak duality (Tonelli; the capture time is jointly lower semicontinuous, hence measurable)
  have hmeas : Measurable fun p : searcherPaths × hiderPaths => captureTime p.1 p.2 :=
    (lowerSemicontinuous_captureTime.comp (g := fun p : searcherPaths × hiderPaths =>
      ((p.1 : C(ℝ≥0, ℝ)), (p.2 : C(ℝ≥0, ℝ))))
      ((continuous_subtype_val.comp continuous_fst).prodMk
        (continuous_subtype_val.comp continuous_snd))).measurable
  have hle : lowerValue ≤ upperValue := by
    refine iSup_le fun ν => le_iInf fun μ => ?_
    calc ⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(ν : Measure hiderPaths)
        = ∫⁻ _, (⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(ν : Measure hiderPaths))
            ∂(μ : Measure searcherPaths) := by
          rw [lintegral_const, measure_univ, mul_one]
      _ ≤ ∫⁻ S, ∫⁻ H, captureTime S H ∂(ν : Measure hiderPaths) ∂(μ : Measure searcherPaths) :=
          lintegral_mono fun S => iInf_le _ S
      _ = ∫⁻ H, ∫⁻ S, captureTime S H ∂(μ : Measure searcherPaths) ∂(ν : Measure hiderPaths) :=
          lintegral_lintegral_swap hmeas.aemeasurable
      _ ≤ ∫⁻ _, (⨆ H : hiderPaths, ∫⁻ S, captureTime S H ∂(μ : Measure searcherPaths))
            ∂(ν : Measure hiderPaths) :=
          lintegral_mono fun H =>
            le_iSup (fun H : hiderPaths => ∫⁻ S, captureTime S H ∂(μ : Measure searcherPaths)) H
      _ = ⨆ H : hiderPaths, ∫⁻ S, captureTime S H ∂(μ : Measure searcherPaths) := by
          rw [lintegral_const, measure_univ, mul_one]
  have hup : upperValue = ⨆ (s : Finset hiderPaths) (w : hiderPaths → ℝ≥0∞)
      (_ : ∑ H ∈ s, w H = 1), ⨅ S : searcherPaths, ∑ H ∈ s, w H * captureTime S H := hval
  have heq : lowerValue = upperValue := by
    refine le_antisymm hle ?_
    rw [hup]
    exact iSup_le fun s => iSup_le fun w => iSup_le fun hw => hge s w hw
  refine ⟨heq, hopt, fun ε hε => ?_⟩
  -- `ε`-optimal finitely supported hider strategies
  have hfin : lowerValue ≠ ⊤ :=
    ne_top_of_le_ne_top ENNReal.ofNat_ne_top (heq.le.trans val_upperValue_le_two)
  by_cases hL0 : lowerValue = 0
  · let H₀ : hiderPaths := ⟨val_sweep, searcherPaths_subset_hiderPaths val_sweep_mem⟩
    exact ⟨{H₀}, fun _ => 1, by simp, by simp [hL0]⟩
  have hlt : lowerValue - ε < lowerValue := ENNReal.sub_lt_self hfin hL0 hε.ne'
  rw [heq, hup] at hlt
  obtain ⟨s, hs⟩ := lt_iSup_iff.1 hlt
  obtain ⟨w, hw⟩ := lt_iSup_iff.1 hs
  obtain ⟨hw1, hw⟩ := lt_iSup_iff.1 hw
  refine ⟨s, w, hw1, ?_⟩
  rw [heq, hup]
  exact tsub_le_iff_right.1 hw.le

end PrincessMonster
