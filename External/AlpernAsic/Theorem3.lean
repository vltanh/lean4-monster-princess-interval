module

public import Mathlib.MeasureTheory.Measure.Basic
public import Mathlib.MeasureTheory.Measure.CompleteLattice
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

/-- `½ (a + b) ≤ c` when `a ≤ c` and `b ≤ c`. -/
private lemma val_half_add_le {a b c : ℝ≥0∞} (ha : a ≤ c) (hb : b ≤ c) :
    (1 / 2 : ℝ≥0∞) * (a + b) ≤ c := by
  calc (1 / 2 : ℝ≥0∞) * (a + b) ≤ (1 / 2 : ℝ≥0∞) * (c + c) := by gcongr
    _ = c := by
      rw [← two_mul, ← mul_assoc, one_div, ENNReal.inv_mul_cancel two_ne_zero ENNReal.ofNat_ne_top,
        one_mul]

/-- `c ≤ ½ (a + b)` when `c ≤ a` and `c ≤ b`. -/
private lemma val_le_half_add {a b c : ℝ≥0∞} (ha : c ≤ a) (hb : c ≤ b) :
    c ≤ (1 / 2 : ℝ≥0∞) * (a + b) := by
  calc c = (1 / 2 : ℝ≥0∞) * (c + c) := by
        rw [← two_mul, ← mul_assoc, one_div, ENNReal.inv_mul_cancel two_ne_zero
          ENNReal.ofNat_ne_top, one_mul]
    _ ≤ (1 / 2 : ℝ≥0∞) * (a + b) := by gcongr

omit [MeasurableSpace Y] in
/-- **Alpern and Asic (1985), Theorem 3**, for the minimizer, with the group `{id, φ}`: if the
payoff is invariant under the involutions `φX`, `φY`, the symmetrization of a mixed strategy `μ`
guarantees at least as much as `μ`. -/
theorem theorem3_minimizer (f : X → Y → ℝ≥0∞) (hf : ∀ y, Measurable fun x => f x y)
    (φX : X → X) (φY : Y → Y) (hφX : Measurable φX) (hφY : Function.Involutive φY)
    (hinv : ∀ x y, f (φX x) (φY y) = f x y) (μ : Measure X) :
    ⨆ y, ∫⁻ x, f x y ∂((1 / 2 : ℝ≥0∞) • (μ + μ.map φX)) ≤ ⨆ y, ∫⁻ x, f x y ∂μ := by
  refine iSup_le fun y => ?_
  -- the image measure integrates `f (·, y)` as `μ` integrates `f (·, φY y)`
  have hmap : ∫⁻ x, f x y ∂(μ.map φX) = ∫⁻ x, f x (φY y) ∂μ := by
    rw [lintegral_map (hf y) hφX]
    refine lintegral_congr fun x => ?_
    simpa [hφY y] using hinv x (φY y)
  rw [lintegral_smul_measure, lintegral_add_measure, hmap, smul_eq_mul]
  exact val_half_add_le (le_iSup (fun y => ∫⁻ x, f x y ∂μ) y)
    (le_iSup (fun y => ∫⁻ x, f x y ∂μ) (φY y))

omit [MeasurableSpace X] in
/-- **Alpern and Asic (1985), Theorem 3**, for the maximizer, with the group `{id, φ}`. -/
theorem theorem3_maximizer (f : X → Y → ℝ≥0∞) (hf : ∀ x, Measurable fun y => f x y)
    (φX : X → X) (φY : Y → Y) (hφY : Measurable φY) (hφX : Function.Involutive φX)
    (hinv : ∀ x y, f (φX x) (φY y) = f x y) (ν : Measure Y) :
    ⨅ x, ∫⁻ y, f x y ∂ν ≤ ⨅ x, ∫⁻ y, f x y ∂((1 / 2 : ℝ≥0∞) • (ν + ν.map φY)) := by
  refine le_iInf fun x => ?_
  -- the image measure integrates `f (x, ·)` as `ν` integrates `f (φX x, ·)`
  have hmap : ∫⁻ y, f x y ∂(ν.map φY) = ∫⁻ y, f (φX x) y ∂ν := by
    rw [lintegral_map (hf x) hφY]
    refine lintegral_congr fun y => ?_
    simpa [hφX x] using hinv (φX x) y
  rw [lintegral_smul_measure, lintegral_add_measure, hmap, smul_eq_mul]
  exact val_le_half_add (iInf_le (fun x => ∫⁻ y, f x y ∂ν) x)
    (iInf_le (fun x => ∫⁻ y, f x y ∂ν) (φX x))

end External.AlpernAsic
