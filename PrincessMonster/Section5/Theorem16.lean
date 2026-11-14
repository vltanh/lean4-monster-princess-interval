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

/-- **Formula (15)** (`eq:15`), corrected. Let the loiterers start with a density `f` on
`[0, 1]` (for instance the uniform density of Theorem 16). Ignoring `ε`, the payoffs of `S₁` and `S₂` are `V(S₁, E) = 3`, `V(S₂, E) = 1 + 2y`,
and `V(S₁, h_Φ)`, `V(S₂, h_Φ)` as in `formula15S1`, `formula15S2`. The paper's display omits
the factors `2y - 1 - t`, `1 - t` and `t - 1 + 2y` in the integrands and writes `Φ(1 - 2y)` for
`∫_0^{1-2y} (1 - t) f(t) dt`. -/
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
  sorry

/-- **Theorem 16** (`thm:16`). If the hider uses the mixed strategy `γ`, the optimal response of
the searcher gives the value `15/11` (as `ε → 0`). In particular `V ≥ 15/11`.

The first part is the precise form of "the optimal response of the searcher gives a matrix game
with value 15/11": the infimum is over every searcher path, whereas the paper reduces to the paths
`S₁`, `S₂` by an argument it leaves to the reader. -/
theorem theorem16 :
    Tendsto (fun ε : ℝ => ⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(gamma ε)) (𝓝[>] 0)
        (𝓝 (15 / 11)) ∧
      (15 / 11 : ℝ≥0∞) ≤ lowerValue := by
  sorry

end PrincessMonster
