module

public import PrincessMonster.CaptureTime
public import External.AlpernGal.Minimax

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

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonster

/-- The capture time is lower semicontinuous on pairs of paths, for the topology of uniform
convergence on compact sets (`claim:value`; the paper says *upper* semicontinuous). -/
theorem lowerSemicontinuous_captureTime :
    LowerSemicontinuous fun p : C(ℝ≥0, ℝ) × C(ℝ≥0, ℝ) => captureTime p.1 p.2 := by
  sorry

/-- The searcher's pure strategy space is compact (`claim:value`). -/
instance compactSpace_searcherPaths : CompactSpace searcherPaths := by
  sorry

/-- **The game has a value** (`claim:value`). The lower and upper values coincide; the searcher
has an optimal mixed strategy; and for every `ε > 0` the hider has an `ε`-optimal mixed strategy
supported on finitely many paths. -/
theorem value_exists :
    lowerValue = upperValue ∧
      (∃ μ : ProbabilityMeasure searcherPaths,
        ⨆ H : hiderPaths, ∫⁻ S, captureTime S H ∂(μ : Measure searcherPaths) = upperValue) ∧
      ∀ ε : ℝ≥0∞, 0 < ε → ∃ (s : Finset hiderPaths) (w : hiderPaths → ℝ≥0∞),
        ∑ H ∈ s, w H = 1 ∧ lowerValue ≤ (⨅ S : searcherPaths, ∑ H ∈ s, w H * captureTime S H) + ε := by
  sorry

end PrincessMonster
