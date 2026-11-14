module

public import PrincessMonster.CaptureTime

/-!
# Section 2: symmetric strategies (Proposition 4)

The reflection `φ(x) = -x` of the interval acts on paths by `S ↦ -S`. A mixed strategy is
*symmetric* if it is invariant under this action. Proposition 4: there is an optimal searcher
mixed strategy, and for every `ε > 0` an `ε`-optimal hider mixed strategy, that are symmetric.
-/

@[expose] public section

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonster

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
        lowerValue ≤ (⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(ν : Measure hiderPaths)) + ε := by
  sorry

end PrincessMonster
