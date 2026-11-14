module

public import PrincessMonster.Section4.Runners
public import Mathlib.Analysis.Calculus.Deriv.Basic
public import Mathlib.Analysis.Calculus.ContDiff.Defs

/-!
# Section 4: Lemmas 11–13 and the payoff formulas (9), (10)

Let `H` be a hider path of speed at most `1` and `y` the first time it meets a sweeper.

* `lemma11`: the searchers of `s_Φ` that find `H` before time `y` are exactly the right runners
  starting in `(H(y) - y, H(0)]` and the left runners starting in `[H(0), H(y) + y)` (up to the
  starting point `H(y) ∓ y` itself, where the paper's statement fails).
* `lemma12`: when `Φ` has a continuous density `f` and `H` is smooth, these searchers find `H`
  with expected time (5) and (6).
* `lemma13`: integrating (7) by parts gives `(8) - y Φ(1 - 2y)`.
* `equation9`: the payoff `V(s_Φ, H)` of formula (9), when after time `y` the hider runs to the
  end; `equation9_le`: (9) bounds the payoff whatever the hider does after `y`.
* `equation10`: for the uniform distribution, (9) equals `(10 + 2x - (7 + x) y + y²)/4`.
-/

@[expose] public section

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonster

/-- **Lemma 11** (`lem:11`). Let `H` be a hider path of speed at most `1` and `y` the first
time it meets a sweeper. A searcher of `s_Φ` finds `H` before time `y` if and only if he starts
in `(H(y) - y, H(0)]` and runs right, or starts in `[H(0), H(y) + y)` and runs left. The starting
points `H(y) - y` and `H(y) + y` are excluded: there the paper's statement can fail. -/
theorem lemma11 {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hy : sweepTime H = y) {x : ℝ} (hx : x ∈ I) (hx₁ : x ≠ H y - y) (hx₂ : x ≠ H y + y) :
    (captureTime (runner x) H < y ↔ x ∈ Set.Ioc (H y - y) (H 0)) ∧
      (captureTime (leftRunner x) H < y ↔ x ∈ Set.Ico (H 0) (H y + y)) := by
  sorry

/-- **Lemma 12** (`lem:12`). Let the starting point of `s_Φ` have a continuous density `f`, and
let `H` be a smooth hider path of speed at most `1` that meets the sweeper `A` first, at time
`y`. The right runners starting in `(H(y) - y, H(0)]` catch `H` with expected time (5), and the
left runners starting in `[H(0), H(y) + y)` (whose starting points have density `f(-x)`) with
expected time (6). -/
theorem lemma12 {f : ℝ → ℝ} (hf : Continuous f) (hf0 : ∀ x, 0 ≤ f x)
    {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y) (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H)
    (hsmooth : ContDiffOn ℝ 1 (realPath H) (Set.Icc 0 y)) :
    (∫⁻ x in Set.Ioc (H y - y) (H 0), captureTime (runner x) H
        ∂(volume.withDensity fun x => ENNReal.ofReal (f x))) =
      ENNReal.ofReal (∫ t in (0 : ℝ)..y,
        t * f (realPath H t - t) * (1 - deriv (realPath H) t)) ∧
    (∫⁻ x in Set.Ico (H 0) (H y + y), captureTime (leftRunner x) H
        ∂(volume.withDensity fun x => ENNReal.ofReal (f (-x)))) =
      ENNReal.ofReal (∫ t in (0 : ℝ)..y,
        t * f (-realPath H t - t) * (1 + deriv (realPath H) t)) := by
  sorry

/-- **Lemma 13** (`lem:13`). Integrating (7) by parts: if `Φ' = f`, `Φ(-1) = 0` and the smooth
hider path meets the sweeper `A` at time `y` (so `H(y) = 1 - y`), then (7) equals the
variational integral (8) minus `y Φ(1 - 2y)`. So for given `H(0)` and `y` the optimal hider path
maximizes (8). -/
theorem lemma13 {Φ f : ℝ → ℝ} (hΦ : ∀ x, HasDerivAt Φ (f x) x) (hf : Continuous f)
    (hΦ₀ : Φ (-1) = 0) {h : ℝ → ℝ} {y : ℝ} (hy : 0 ≤ y) (hh : ContDiffOn ℝ 1 h (Set.Icc 0 y))
    (hhy : h y = 1 - y) :
    (∫ t in (0 : ℝ)..y, t * (f (h t - t) * (1 - deriv h t) + f (-h t - t) * (1 + deriv h t))) =
      (∫ t in (0 : ℝ)..y, (Φ (-t + h t) + Φ (-t - h t))) - y * Φ (1 - 2 * y) := by
  sorry

/-- The right-hand side of formula (9), for `x = H(0)`, the meeting time `y` and the path `h`. -/
noncomputable def formula9 (Φ : ℝ → ℝ) (x y : ℝ) (h : ℝ → ℝ) : ℝ :=
  1 - Φ (-x) + 2 * Φ (1 - 2 * y) + y / 2 * (1 - Φ x) - y / 2 * Φ (1 - 2 * y) +
    1 / 2 * ∫ t in (0 : ℝ)..y, (Φ (-t + h t) + Φ (-t - h t))

/-- **Formula (9)** (`eq:9`). Let the starting point of `s_Φ` have an atomless distribution `μ`
on `[-1, 1]`, and let `H` be a hider path of speed at most `1` that meets the sweeper `A` first,
at time `y`, and then runs to the end `+1`. Then `V(s_Φ, H)` is given by (9), with `x = H(0)`.

"First" is strict: a path that meets both sweepers at time `1` (where they cross, at `0`) and then
runs to `+1` runs along `-A` and is met by the left runners at time `1`, not `2`; there (9) fails
(for `H = F` with `ε = 0` and uniform `Φ` the payoff is `3/4`, while (9) gives `1`). -/
theorem equation9 (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ] (hμ : μ Iᶜ = 0)
    {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y) (hfirst : captureTime sweeperA H < captureTime (-sweeperA) H)
    (hrun : ∀ t : ℝ≥0, y ≤ t → H t = min 1 (H y + ((t : ℝ) - y))) :
    ∫⁻ S, captureTime S H ∂(sPhi μ) = ENNReal.ofReal (formula9 (cdf μ) (H 0) y (realPath H)) := by
  sorry

/-- **Formula (9)** (`eq:9`), as a bound: whatever the hider does after meeting the sweeper,
`V(s_Φ, H)` is at most (9). -/
theorem equation9_le (μ : Measure ℝ) [IsProbabilityMeasure μ] [NullSingletonClass μ] (hμ : μ Iᶜ = 0)
    {H : C(ℝ≥0, ℝ)} (hH : H ∈ searcherPaths) {y : ℝ≥0}
    (hyA : captureTime sweeperA H = y) (hfirst : captureTime sweeperA H ≤ captureTime (-sweeperA) H) :
    ∫⁻ S, captureTime S H ∂(sPhi μ) ≤ ENNReal.ofReal (formula9 (cdf μ) (H 0) y (realPath H)) := by
  sorry

/-- **Formula (10)** (`eq:10`). For the uniform distribution on `[-1, 1]` the variational
integral does not depend on the path, and (9) equals `(10 + 2x - (7 + x) y + y²)/4`. -/
theorem equation10 {x y : ℝ} (hx : x ∈ I) (hy0 : 0 ≤ y) (hy1 : y ≤ 1) {h : ℝ → ℝ}
    (hh : ∀ t ∈ Set.Icc 0 y, t - 1 ≤ h t ∧ h t ≤ 1 - t) :
    formula9 (cdf uniformI) x y h = (10 + 2 * x - (7 + x) * y + y ^ 2) / 4 := by
  sorry

end PrincessMonster
