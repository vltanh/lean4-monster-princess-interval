module

public import Mathlib.MeasureTheory.Measure.MeasureSpace
public import Mathlib.MeasureTheory.Integral.Lebesgue.Map

/-!
# Alpern and Asic, Theorem 3: invariant optimal strategies

S. Alpern and M. Asic, *The search value of a network*, Networks 15 (1985), 229–238,
Theorem 3: in a search game on a network `Q`, there are optimal strategies invariant under the
isometry group of `Q`.

The special case used by the paper (Proposition 4): the interval, whose isometry group is
`{id, φ}` with `φ(x) = -x`. In the source's game-theoretic terms: if a payoff is invariant under
involutions of the two strategy spaces, averaging a mixed strategy with its image under the
involution does not worsen its guarantee, for either player.
-/

@[expose] public section

open scoped ENNReal
open MeasureTheory

namespace External.AlpernAsic

variable {X Y : Type*} [MeasurableSpace X] [MeasurableSpace Y]

/-- **Alpern and Asic (1985), Theorem 3**, for the minimizer, with the group `{id, φ}`: if the
payoff is invariant under the involutions `φX`, `φY`, the symmetrization of a mixed strategy `μ`
guarantees at least as much as `μ`. -/
theorem theorem3_minimizer (f : X → Y → ℝ≥0∞) (hf : ∀ y, Measurable fun x => f x y)
    (φX : X → X) (φY : Y → Y) (hφX : Measurable φX) (hφY : Function.Involutive φY)
    (hinv : ∀ x y, f (φX x) (φY y) = f x y) (μ : Measure X) :
    ⨆ y, ∫⁻ x, f x y ∂((1 / 2 : ℝ≥0∞) • (μ + μ.map φX)) ≤ ⨆ y, ∫⁻ x, f x y ∂μ := by
  sorry

/-- **Alpern and Asic (1985), Theorem 3**, for the maximizer, with the group `{id, φ}`. -/
theorem theorem3_maximizer (f : X → Y → ℝ≥0∞) (hf : ∀ x, Measurable fun y => f x y)
    (φX : X → X) (φY : Y → Y) (hφY : Measurable φY) (hφX : Function.Involutive φX)
    (hinv : ∀ x y, f (φX x) (φY y) = f x y) (ν : Measure Y) :
    ⨅ x, ∫⁻ y, f x y ∂ν ≤ ⨅ x, ∫⁻ y, f x y ∂((1 / 2 : ℝ≥0∞) • (ν + ν.map φY)) := by
  sorry

end External.AlpernAsic
