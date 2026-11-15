module

public import PrincessMonsterInterval.CaptureTime
import PrincessMonsterInterval.Value
import External.AlpernAsic.Theorem3
import Mathlib.MeasureTheory.Measure.DiracProba

/-!
# Section 2: symmetric strategies (Proposition 4)

The reflection `φ(x) = -x` of the interval acts on paths by `S ↦ -S`. A mixed strategy is
*symmetric* if it is invariant under this action. Proposition 4: there is an optimal searcher
mixed strategy, and for every `ε > 0` an `ε`-optimal hider mixed strategy, that are symmetric.
-/

@[expose] public section

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonsterInterval

lemma neg_mem_searcherPaths {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) : -S ∈ searcherPaths := by
  refine ⟨fun t => ?_, fun t t' => ?_⟩
  · have := hS.1 t
    simp only [ContinuousMap.neg_apply, Set.mem_Icc] at this ⊢
    constructor <;> linarith [this.1, this.2]
  · have := hS.2 t t'
    simp only [ContinuousMap.neg_apply]
    rw [show -S t - -S t' = -(S t - S t') by ring, abs_neg]
    exact this

lemma neg_mem_hiderPaths {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) : -H ∈ hiderPaths := by
  intro t
  have := hH t
  simp only [ContinuousMap.neg_apply, Set.mem_Icc] at this ⊢
  constructor <;> linarith [this.1, this.2]

/-- The reflection `φ(x) = -x` acting on searcher paths. -/
def reflectS (S : searcherPaths) : searcherPaths := ⟨-S.1, neg_mem_searcherPaths S.2⟩

/-- The reflection `φ(x) = -x` acting on hider paths. -/
def reflectH (H : hiderPaths) : hiderPaths := ⟨-H.1, neg_mem_hiderPaths H.2⟩

lemma continuous_reflectS : Continuous reflectS :=
  (continuous_neg.comp continuous_subtype_val).subtype_mk _

lemma continuous_reflectH : Continuous reflectH :=
  (continuous_neg.comp continuous_subtype_val).subtype_mk _

lemma measurable_reflectS : Measurable reflectS :=
  continuous_reflectS.measurable

lemma measurable_reflectH : Measurable reflectH :=
  continuous_reflectH.measurable

/-- The reflection of searcher paths is an involution. -/
lemma val_reflectS_involutive : Function.Involutive reflectS :=
  fun S => Subtype.ext (neg_neg S.1)

/-- The reflection of hider paths is an involution. -/
lemma val_reflectH_involutive : Function.Involutive reflectH :=
  fun H => Subtype.ext (neg_neg H.1)

/-- The capture time is invariant under the reflection of both paths. -/
lemma val_captureTime_reflect (S : searcherPaths) (H : hiderPaths) :
    captureTime (reflectS S) (reflectH H) = captureTime S H :=
  captureTime_neg

/-- The symmetrization `½ (μ + μ ∘ φ⁻¹)` of a probability measure under a measurable map. -/
private noncomputable def val_symmetrize {α : Type*} [MeasurableSpace α] (μ : ProbabilityMeasure α)
    (φ : α → α) (hφ : Measurable φ) : ProbabilityMeasure α :=
  ⟨(1 / 2 : ℝ≥0∞) • ((μ : Measure α) + (μ : Measure α).map φ), ⟨by
    rw [Measure.smul_apply, Measure.add_apply, Measure.map_apply hφ MeasurableSet.univ,
      Set.preimage_univ, measure_univ, smul_eq_mul, one_add_one_eq_two, one_div,
      ENNReal.inv_mul_cancel two_ne_zero ENNReal.ofNat_ne_top]⟩⟩

private lemma val_symmetrize_coe {α : Type*} [MeasurableSpace α] (μ : ProbabilityMeasure α)
    (φ : α → α) (hφ : Measurable φ) :
    (val_symmetrize μ φ hφ : Measure α) =
      (1 / 2 : ℝ≥0∞) • ((μ : Measure α) + (μ : Measure α).map φ) :=
  rfl

/-- The symmetrization under a measurable involution is invariant. -/
private lemma val_map_symmetrize {α : Type*} [MeasurableSpace α] (μ : ProbabilityMeasure α)
    {φ : α → α} (hφ : Measurable φ) (hinv : Function.Involutive φ) :
    (val_symmetrize μ φ hφ : Measure α).map φ = val_symmetrize μ φ hφ := by
  rw [val_symmetrize_coe, Measure.map_smul, Measure.map_add _ _ hφ, Measure.map_map hφ hφ,
    hinv.comp_self, Measure.map_id, add_comm]
  exact hφ.aemeasurable

/-- **Proposition 4** (`prop:4`). There is an optimal searcher mixed strategy, and for every
`ε > 0` an `ε`-optimal hider mixed strategy, which are invariant under the reflection
`φ(x) = -x`. An optimal searcher strategy guarantees the upper value; an `ε`-optimal hider
strategy guarantees the lower value up to `ε`. -/
theorem proposition4 :
    (∃ μ : ProbabilityMeasure searcherPaths,
        (μ : Measure searcherPaths).map reflectS = μ ∧
        ⨆ H : hiderPaths, ∫⁻ S, captureTime S H ∂(μ : Measure searcherPaths) = upperValue) ∧
    ∀ ε : ℝ≥0∞, 0 < ε → ∃ ν : ProbabilityMeasure hiderPaths,
        (ν : Measure hiderPaths).map reflectH = ν ∧
        lowerValue ≤
          (⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(ν : Measure hiderPaths)) + ε := by
  obtain ⟨hval, ⟨μ₀, hμ₀⟩, -⟩ := value_exists
  refine ⟨?_, fun ε hε => ?_⟩
  · -- the searcher: symmetrize an optimal strategy (Alpern and Asic, Theorem 3)
    refine ⟨val_symmetrize μ₀ reflectS measurable_reflectS,
      val_map_symmetrize μ₀ measurable_reflectS val_reflectS_involutive, le_antisymm ?_ ?_⟩
    · rw [← hμ₀, val_symmetrize_coe]
      exact External.AlpernAsic.theorem3_minimizer
        (fun (S : searcherPaths) (H : hiderPaths) => captureTime S H)
        (fun H => (val_lowerSemicontinuous_captureTime_left H).measurable) reflectS reflectH
        measurable_reflectS val_reflectH_involutive val_captureTime_reflect μ₀
    · exact iInf_le (fun μ : ProbabilityMeasure searcherPaths =>
        ⨆ H : hiderPaths, ∫⁻ S, captureTime S H ∂(μ : Measure searcherPaths)) _
  · -- the hider: an `ε`-optimal strategy (definition of the lower value), symmetrized
    have hfin : lowerValue ≠ ⊤ :=
      ne_top_of_le_ne_top ENNReal.ofNat_ne_top (hval.le.trans val_upperValue_le_two)
    obtain ⟨ν₀, hν₀⟩ : ∃ ν₀ : ProbabilityMeasure hiderPaths, lowerValue ≤
        (⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(ν₀ : Measure hiderPaths)) + ε := by
      by_cases hL0 : lowerValue = 0
      · have h0 : (0 : C(ℝ≥0, ℝ)) ∈ hiderPaths := fun t => by simp
        exact ⟨diracProba ⟨0, h0⟩, by simp [hL0]⟩
      obtain ⟨ν₀, hν₀⟩ := lt_iSup_iff.1 (ENNReal.sub_lt_self hfin hL0 hε.ne')
      exact ⟨ν₀, tsub_le_iff_right.1 hν₀.le⟩
    refine ⟨val_symmetrize ν₀ reflectH measurable_reflectH,
      val_map_symmetrize ν₀ measurable_reflectH val_reflectH_involutive, hν₀.trans ?_⟩
    gcongr ?_ + ε
    rw [val_symmetrize_coe]
    exact External.AlpernAsic.theorem3_maximizer
      (fun (S : searcherPaths) (H : hiderPaths) => captureTime S H)
      (fun S => (val_lowerSemicontinuous_captureTime_right S).measurable) reflectS reflectH
      measurable_reflectH val_reflectS_involutive val_captureTime_reflect ν₀

end PrincessMonsterInterval
