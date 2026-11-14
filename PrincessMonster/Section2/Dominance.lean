module

public import PrincessMonster.CaptureTime
public import Mathlib.Analysis.Calculus.ContDiff.Defs

/-!
# Section 2: dominated pure strategies (Propositions 1–3)

* `EndReflecting`, `EndAbsorbing`: the paper's definitions.
* `proposition1`: every searcher path is dominated by an end-reflecting one.
* `proposition2`: every hider path is dominated by an end-absorbing one.
* `proposition3`: every smooth hider path is dominated by a path of speed at most `1`;
  `proposition3_of_continuous` drops smoothness.

A searcher path `S'` dominates `S` when `T(S', H) ≤ T(S, H)` for every hider path `H`; a hider
path `H'` dominates `H` when `T(S, H) ≤ T(S, H')` for every searcher path `S`.
-/

@[expose] public section

open scoped NNReal ENNReal

namespace PrincessMonster

/-- A path is *end-reflecting* if, whenever it is at an end `±1` at a time `t₀`, it moves away at
unit speed for the next unit of time: `|S t - S t₀| = t - t₀` for `t₀ ≤ t ≤ t₀ + 1`. This is the
paper's definition as printed; the surrounding text ("once the searcher reaches an end, he should
go directly to the other end") describes the stronger property `EndSweeping`. -/
def EndReflecting (S : C(ℝ≥0, ℝ)) : Prop :=
  ∀ t₀ : ℝ≥0, (S t₀ = 1 ∨ S t₀ = -1) →
    ∀ t : ℝ≥0, t₀ ≤ t → (t : ℝ) ≤ t₀ + 1 → |S t - S t₀| = t - t₀

/-- A path is *end-sweeping* if, whenever it is at an end at a time `t₀`, it runs directly to the
other end: `|S t - S t₀| = t - t₀` for `t₀ ≤ t ≤ t₀ + 2`. -/
def EndSweeping (S : C(ℝ≥0, ℝ)) : Prop :=
  ∀ t₀ : ℝ≥0, (S t₀ = 1 ∨ S t₀ = -1) →
    ∀ t : ℝ≥0, t₀ ≤ t → (t : ℝ) ≤ t₀ + 2 → |S t - S t₀| = t - t₀

/-- A path is *end-absorbing* if, once it is at an end `±1`, it stays there. -/
def EndAbsorbing (H : C(ℝ≥0, ℝ)) : Prop :=
  ∀ t₀ : ℝ≥0, (H t₀ = 1 ∨ H t₀ = -1) → ∀ t : ℝ≥0, t₀ ≤ t → H t = H t₀

/-- **Proposition 1** (`prop:1`). Every pure searcher strategy is dominated by one which is
end-reflecting. -/
theorem proposition1 {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    ∃ S' ∈ searcherPaths, EndReflecting S' ∧ ∀ H ∈ hiderPaths, captureTime S' H ≤ captureTime S H := by
  sorry

/-- **Proposition 1** (`prop:1`), in the form the text describes: every pure searcher strategy is
dominated by one that, once it reaches an end, goes directly to the other end. -/
theorem proposition1_sweeping {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    ∃ S' ∈ searcherPaths, EndSweeping S' ∧ ∀ H ∈ hiderPaths, captureTime S' H ≤ captureTime S H := by
  sorry

/-- **Proposition 2** (`prop:2`). Every pure hider strategy is dominated by one which is
end-absorbing. -/
theorem proposition2 {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    ∃ H' ∈ hiderPaths, EndAbsorbing H' ∧ ∀ S ∈ searcherPaths, captureTime S H ≤ captureTime S H' := by
  sorry

/-- A path is *smooth* if it is continuously differentiable on `[0, ∞)` (one-sided at `0`). -/
def Smooth (H : C(ℝ≥0, ℝ)) : Prop :=
  ContDiffOn ℝ 1 (fun t : ℝ => H t.toNNReal) (Set.Ici 0)

/-- **Proposition 3** (`prop:3`). Every smooth hider strategy is dominated by one in `𝒮`, that is,
one with speed bounded by `1`. -/
theorem proposition3 {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (hsmooth : Smooth H) :
    ∃ H' ∈ searcherPaths, ∀ S ∈ searcherPaths, captureTime S H ≤ captureTime S H' := by
  sorry

end PrincessMonster

namespace PrincessMonster

/-- Proposition 3 holds for every continuous hider path, smooth or not: the path `H'` that
follows `H` when it can and otherwise runs towards it at unit speed dominates `H`. -/
theorem proposition3_of_continuous {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    ∃ H' ∈ searcherPaths, ∀ S ∈ searcherPaths, captureTime S H ≤ captureTime S H' := by
  sorry

end PrincessMonster
