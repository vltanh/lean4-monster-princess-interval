module

public import PrincessMonsterInterval.AlpernEtAl2008.Section3.Strategies
public import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
public import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic

/-!
# Section 4: the searcher strategy `s_Φ` with a continuous initial distribution

* `runner x`: start at `x`, run right until meeting the sweeper `A` (at time `(1 - x)/2`), join
  `A` until `-1`, then run back to the other end;
* `leftRunner x`: its mirror image, start at `x`, run left until meeting `-A`, join `-A`;
  `leftRunner x = -runner (-x)`;
* `sPhi μ`: the mixed strategy `s_Φ` together with its reflection `-s_Φ`, each with probability
  `1/2`: the start is distributed by `μ` (distribution function `Φ`); right runners start at
  `x ∼ μ`, left runners at `-x`;
* `sigma p μ`: the mixed strategy `σ`, which uses the sweepers `±A` with probability `p` and
  `s_Φ` with probability `1 - p`;
* `uniformI`: the uniform distribution on `[-1, 1]`, and `cdf μ` the distribution function `Φ`.
-/

@[expose] public section

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonsterInterval

/-- The path of `s_Φ` that starts at `x` and runs right: it meets the sweeper `A` at time
`(1 - x)/2`, joins it until `-1`, and then runs back to the other end. -/
noncomputable def runner (x : ℝ) : C(ℝ≥0, ℝ) :=
  pathOf (fun t => Real.triangleWave (min (x + t) (1 - t))) (by fun_prop)

/-- The path of `-s_Φ` that starts at `x` and runs left until meeting `-A`, then joins it. -/
noncomputable def leftRunner (x : ℝ) : C(ℝ≥0, ℝ) :=
  pathOf (fun t => Real.triangleWave (max (x - t) (t - 1))) (by fun_prop)

lemma runner_mem (x : ℝ) : runner x ∈ searcherPaths :=
  pathOf_triangleWave_mem (by fun_prop) fun s t => abs_min_sub_min_le_of (by ring_nf; rfl)
    (by rw [show 1 - s - (1 - t) = -(s - t) by ring, abs_neg])

lemma leftRunner_mem (x : ℝ) : leftRunner x ∈ searcherPaths :=
  pathOf_triangleWave_mem (by fun_prop) fun s t => abs_max_sub_max_le_of
    (by rw [show x - s - (x - t) = -(s - t) by ring, abs_neg]) (by ring_nf; rfl)

lemma leftRunner_eq_neg_runner (x : ℝ) : leftRunner x = -runner (-x) := by
  ext t
  simp only [leftRunner, runner, pathOf_apply, ContinuousMap.neg_apply]
  rw [← Real.triangleWave_neg]
  congr 1
  rcases le_total (-x + t) (1 - t) with h | h
  · rw [min_eq_left h, max_eq_left (by linarith)]; ring
  · rw [min_eq_right h, max_eq_right (by linarith)]; ring

/-- The searcher strategy `s_Φ` together with its reflection, each with probability `1/2`:
right runners start at `x ∼ μ`, left runners at `-x`. -/
noncomputable def sPhi (μ : Measure ℝ) : Measure searcherPaths :=
  (1 / 2 : ℝ≥0∞) • (μ.map (fun x => toSearcher (runner x)) +
    μ.map (fun x => toSearcher (leftRunner (-x))))

/-- The mixed strategy `σ`: the sweepers `±A` with probability `p`, `s_Φ` with probability
`1 - p`. -/
noncomputable def sigma (p : ℝ≥0∞) (μ : Measure ℝ) : Measure searcherPaths :=
  p • symDiracS sweeperA + (1 - p) • sPhi μ

/-- The uniform distribution on `[-1, 1]`. -/
noncomputable def uniformI : Measure ℝ :=
  (1 / 2 : ℝ≥0∞) • volume.restrict (Set.Icc (-1) 1)

/-- The distribution function `Φ(x) = μ (-∞, x]`. -/
noncomputable def cdf (μ : Measure ℝ) (x : ℝ) : ℝ := (μ (Set.Iic x)).toReal

/-- The path `t ↦ H t` on the real half-line, extended to `t < 0` by `H 0`. -/
noncomputable def realPath (H : C(ℝ≥0, ℝ)) (t : ℝ) : ℝ := H t.toNNReal

/-- The first time at which a path meets one of the sweepers `±A`. -/
noncomputable def sweepTime (H : C(ℝ≥0, ℝ)) : ℝ≥0∞ :=
  min (captureTime sweeperA H) (captureTime (-sweeperA) H)

end PrincessMonsterInterval
