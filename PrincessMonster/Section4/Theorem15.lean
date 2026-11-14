module

public import PrincessMonster.Section4.Lemmas
public import Mathlib.Order.Filter.Basic
public import Mathlib.Topology.Instances.ENNReal.Lemmas

/-!
# Section 4: formulas (11), (12) and Theorem 15

Varying `Φ` improves the bound `13/9` only marginally. The hider path `H_x` starts at `x ≥ 0`,
runs towards the sweeper `A`, turns `ε` in front of it, runs back towards the middle, and at time
`y` turns again to run to the end.

* `pathHx ε x`: the path `H_x` with `y = 1`: it turns at `ε` at time `1 - 2ε`;
* `equation11`: the variational integral (8) over `H_x` (ignoring `ε`) is (11);
* `equation12`: ignoring `ε`, `V(H_x, s_Φ)` is given by (12);
* `theorem15`: against `σ_Φ` (sweepers with any probability, `s_Φ` with any atomless `Φ`) the
  hider can obtain more than `1.421`.
-/

@[expose] public section

open scoped NNReal ENNReal Topology
open MeasureTheory Filter

namespace PrincessMonster

/-- The hider path `H_x` of Section 4 with `y = 1`: start at `min x (1 - ε)`, run right towards
the sweeper `A`, turn `ε` in front of it and run left just ahead of it, turn at `ε` (time
`1 - 2ε`) and run to the end `+1`. -/
noncomputable def pathHx (ε x : ℝ) : C(ℝ≥0, ℝ) :=
  pathOf (fun t => min 1 (max (min (x + t) (1 - ε - t)) (t - 1 + 3 * ε))) (by fun_prop)

lemma pathHx_mem {ε x : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 4) (hx : x ∈ Set.Icc (0 : ℝ) 1) :
    pathHx ε x ∈ searcherPaths := by
  sorry

/-- **Formula (11)** (`eq:11`). Ignoring `ε`, `H_x(t) = min (x + t) (1 - t)` for `t ≤ y`, and the
variational integral (8) over this path is
`(Φ(x)(1 - x) + ∫_{-1}^{-x} Φ + ∫_{1-2y}^{x} Φ)/2`. The paper prints the lower limit of the first
integral as `0`; the computation gives `-1`, and only `-1` agrees with (12). -/
theorem equation11 {Φ : ℝ → ℝ} (hΦ : Continuous Φ) (hΦ₀ : Φ (-1) = 0) {x y : ℝ}
    (hx : x ∈ Set.Icc (0 : ℝ) 1) (hy : (1 - x) / 2 ≤ y) (hy1 : y ≤ 1) :
    (∫ t in (0 : ℝ)..y, (Φ (-t + min (x + t) (1 - t)) + Φ (-t - min (x + t) (1 - t)))) =
      1 / 2 * (Φ x * (1 - x) + (∫ t in (-1 : ℝ)..(-x), Φ t) + ∫ t in (1 - 2 * y)..x, Φ t) := by
  sorry

/-- **Formula (12)** (`eq:12`). Ignoring `ε` (that is, as `ε → 0⁺`), the payoff of `H_x` against
`s_Φ` is `3/2 - Φ(-x) - Φ(x)(1 + x)/4 + (1/4) ∫_{-1}^{-x} Φ + (1/4) ∫_{-1}^{x} Φ`, and against the
sweepers it is `3/2`. -/
theorem equation12 (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ] (hμ : μ Iᶜ = 0)
    {x : ℝ} (hx : x ∈ Set.Icc (0 : ℝ) 1) :
    Tendsto (fun ε => ∫⁻ S, captureTime S (pathHx ε x) ∂(sPhi μ)) (𝓝[>] 0)
        (𝓝 (ENNReal.ofReal (3 / 2 - cdf μ (-x) - cdf μ x * (1 + x) / 4 +
          1 / 4 * (∫ t in (-1 : ℝ)..(-x), cdf μ t) + 1 / 4 * ∫ t in (-1 : ℝ)..x, cdf μ t))) ∧
      Tendsto (fun ε => ∫⁻ S, captureTime S (pathHx ε x) ∂(symDiracS sweeperA)) (𝓝[>] 0)
        (𝓝 (3 / 2)) := by
  sorry

/-- **Theorem 15** (`thm:15`). If the searcher uses a mixed strategy `σ_Φ` on the sweepers and
`s_Φ`, for any atomless distribution `Φ` on `[-1, 1]` and any probability `p` of the sweepers,
the hider can respond with a mixed strategy `γ` such that `V(σ_Φ, γ) > 1.421`. -/
theorem theorem15 (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ] (hμ : μ Iᶜ = 0)
    {p : ℝ≥0∞} (hp : p ≤ 1) :
    ∃ γ : Measure hiderPaths, IsProbabilityMeasure γ ∧
      (1421 / 1000 : ℝ≥0∞) < ∫⁻ H, ∫⁻ S, captureTime S H ∂(sigma p μ) ∂γ := by
  sorry

end PrincessMonster
