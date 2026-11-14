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

/-- Against any hider path, one of the sweepers `A`, `-A` has met it by time `1`. -/
theorem min_captureTime_sweepers_le_one {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    min (captureTime sweeperA H) (captureTime (-sweeperA) H) ≤ 1 := by
  sorry

/-- The searcher mixed strategy `s` of Theorem 9: `±A` with probability `7/16` each, `±B` with
probability `1/16` each. -/
noncomputable def strategy9 : Measure searcherPaths :=
  (7 / 8 : ℝ≥0∞) • symDiracS sweeperA + (1 / 8 : ℝ≥0∞) • symDiracS stratB

instance : IsProbabilityMeasure strategy9 := by
  sorry

/-- **Theorem 9** (`thm:9`). The searcher strategy `s` keeps the expected capture time at most
`47/32` against every hider path; in particular `V ≤ 47/32`. -/
theorem theorem9 :
    (∀ H : hiderPaths, ∫⁻ S, captureTime S H ∂strategy9 ≤ 47 / 32) ∧ upperValue ≤ 47 / 32 := by
  sorry

/-- The equiprobable sweepers guarantee `3/2`, and the hider at a random end guarantees `1`:
`1 ≤ V ≤ 3/2` (Section 3, before Theorem 9). -/
theorem one_le_lowerValue_and_upperValue_le_three_halves :
    1 ≤ lowerValue ∧ upperValue ≤ 3 / 2 := by
  sorry

end PrincessMonster
