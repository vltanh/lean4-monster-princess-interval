module

public import PrincessMonster.CaptureTime

/-!
# Section 2: noncrossing hider strategies (Definition 6, Propositions 7 and 8)

* `Noncrossing`, `Nonintersecting`: Definition 6.
* `proposition7`: mixing `H₁, H₂` equally is dominated by mixing `H₁ ∧ H₂, H₁ ∨ H₂` equally.
* `proposition7_finite`: consequently every finite mixed hider strategy is dominated by one
  whose pure strategies are pairwise noncrossing.
* `proposition8`: in a symmetric mixed strategy whose pure strategies are pairwise
  nonintersecting, each pure strategy stays in one half of the interval.
-/

@[expose] public section

open scoped NNReal ENNReal

namespace PrincessMonster

/-- **Definition 6** (`def:6`). Two hider paths are *noncrossing* if one lies weakly below the
other at all times. -/
def Noncrossing (H₁ H₂ : C(ℝ≥0, ℝ)) : Prop :=
  (∀ t, H₁ t ≤ H₂ t) ∨ (∀ t, H₂ t ≤ H₁ t)

/-- **Definition 6** (`def:6`). Two hider paths are *nonintersecting* if one lies strictly below
the other at all times. -/
def Nonintersecting (H₁ H₂ : C(ℝ≥0, ℝ)) : Prop :=
  (∀ t, H₁ t < H₂ t) ∨ (∀ t, H₂ t < H₁ t)

/-- **Proposition 7** (`prop:7`). The hider strategy that mixes `H₁, H₂` with equal probability
is dominated by the noncrossing strategy that mixes `H₁ ∧ H₂, H₁ ∨ H₂` with equal probability:
against every searcher path the sum of the two capture times does not decrease. -/
theorem proposition7 {H₁ H₂ : C(ℝ≥0, ℝ)} (h₁ : H₁ ∈ hiderPaths) (h₂ : H₂ ∈ hiderPaths)
    {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    captureTime S H₁ + captureTime S H₂ ≤ captureTime S (H₁ ⊓ H₂) + captureTime S (H₁ ⊔ H₂) := by
  sorry

/-- **Proposition 7** (`prop:7`), its consequence: every finite mixed hider strategy (pure
strategies `H i` with weights `w i`) is dominated by a finite mixed strategy of the same total
weight whose pure strategies are pairwise noncrossing. -/
theorem proposition7_finite {n : ℕ} (w : Fin n → ℝ≥0∞) (H : Fin n → C(ℝ≥0, ℝ))
    (hH : ∀ i, H i ∈ hiderPaths) :
    ∃ (m : ℕ) (w' : Fin m → ℝ≥0∞) (H' : Fin m → C(ℝ≥0, ℝ)),
      (∀ k, H' k ∈ hiderPaths) ∧ (∀ k l, Noncrossing (H' k) (H' l)) ∧
      ∑ k, w' k = ∑ i, w i ∧
      ∀ S ∈ searcherPaths, ∑ i, w i * captureTime S (H i) ≤ ∑ k, w' k * captureTime S (H' k) := by
  sorry

/-- **Proposition 8** (`prop:8`). In a symmetric hider strategy whose pure strategies (its
support `P`) are pairwise nonintersecting, each pure strategy is contained in half of the
interval. -/
theorem proposition8 (P : Finset C(ℝ≥0, ℝ)) (hP : ∀ H ∈ P, H ∈ hiderPaths)
    (hsymm : ∀ H ∈ P, -H ∈ P)
    (hni : ∀ H₁ ∈ P, ∀ H₂ ∈ P, H₁ ≠ H₂ → Nonintersecting H₁ H₂) :
    ∀ H ∈ P, (∀ t, H t ∈ Set.Icc (-1 : ℝ) 0) ∨ (∀ t, H t ∈ Set.Icc (0 : ℝ) 1) := by
  sorry

end PrincessMonster
