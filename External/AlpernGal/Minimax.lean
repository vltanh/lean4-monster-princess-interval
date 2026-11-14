module

public import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
public import Mathlib.Topology.Semicontinuity.Basic
public import Mathlib.Algebra.BigOperators.Group.Finset.Defs

/-!
# Alpern and Gal's mixed-strategy minimax theorem

S. Alpern and S. Gal, *A mixed strategy minimax theorem without compactness*, SIAM J. Control
Optim. 26 (1988), 1357–1361; also Appendix A of Alpern and Gal, *The Theory of Search Games and
Rendezvous* (2003).

The form used by the paper: a zero-sum game in which the minimizer's pure strategies form a
compact Hausdorff space `X`, the maximizer's pure strategies form an arbitrary set `Y`, and the
payoff `f : X → Y → [0, ∞]` is lower semicontinuous in the minimizer's strategy. Then the game
has a value in mixed strategies: the minimizer's mixed strategies are the Borel probability
measures on `X`, the maximizer's are finitely supported probability distributions on `Y`; the
minimizer has an optimal mixed strategy, and the maximizer has `ε`-optimal finitely supported
ones.
-/

@[expose] public section

open scoped ENNReal
open MeasureTheory

namespace External.AlpernGal

/-- **Alpern and Gal (1988), minimax theorem.** For a compact Hausdorff space `X` (with its Borel
σ-algebra), a set `Y` and a payoff `f : X → Y → [0, ∞]` lower semicontinuous in its first
argument: the upper value in mixed strategies is attained by a probability measure on `X`, and
it equals the lower value in which the maximizer uses finitely supported mixed strategies. -/
theorem minimax {X Y : Type*} [TopologicalSpace X] [CompactSpace X] [T2Space X]
    [MeasurableSpace X] [BorelSpace X] (f : X → Y → ℝ≥0∞)
    (hf : ∀ y, LowerSemicontinuous fun x => f x y) :
    (∃ μ : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ : Measure X) =
        ⨅ μ' : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ' : Measure X)) ∧
      (⨅ μ : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ : Measure X)) =
        ⨆ (s : Finset Y) (w : Y → ℝ≥0∞) (_ : ∑ y ∈ s, w y = 1), ⨅ x, ∑ y ∈ s, w y * f x y := by
  sorry

end External.AlpernGal
