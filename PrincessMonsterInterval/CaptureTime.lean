module

public import PrincessMonsterInterval.Defs

/-!
# Basic properties of the capture time

Elementary facts about `captureTime` used throughout: the infimum is attained when the paths
meet, the intermediate value theorem in the form "if the order of the two paths changes, they
have met", symmetry, and the evaluation of paths given by real formulas.
-/

@[expose] public section

open scoped NNReal ENNReal

namespace PrincessMonsterInterval

/-- The continuous path `t ↦ f t` on `[0, ∞)` given by a continuous real function. -/
def pathOf (f : ℝ → ℝ) (hf : Continuous f) : C(ℝ≥0, ℝ) :=
  ⟨fun t => f t, hf.comp NNReal.continuous_coe⟩

@[simp] lemma pathOf_apply (f : ℝ → ℝ) (hf : Continuous f) (t : ℝ≥0) :
    pathOf f hf t = f t := rfl

/-- A path given by a real function of speed at most `1` with values in `[-1, 1]` on `[0, ∞)` is
a searcher path. -/
lemma pathOf_mem_searcherPaths {f : ℝ → ℝ} (hf : Continuous f)
    (hL : ∀ s t : ℝ, |f s - f t| ≤ |s - t|) (hI : ∀ t : ℝ, 0 ≤ t → f t ∈ Set.Icc (-1 : ℝ) 1) :
    pathOf f hf ∈ searcherPaths :=
  ⟨fun t => hI t t.2, fun t t' => hL t t'⟩

/-- A path given by a real function with values in `[-1, 1]` on `[0, ∞)` is a hider path. -/
lemma pathOf_mem_hiderPaths {f : ℝ → ℝ} (hf : Continuous f)
    (hI : ∀ t : ℝ, 0 ≤ t → f t ∈ Set.Icc (-1 : ℝ) 1) : pathOf f hf ∈ hiderPaths :=
  fun t => hI t t.2

variable {S H : C(ℝ≥0, ℝ)}

lemma captureTime_le {t : ℝ≥0} (h : S t = H t) : captureTime S H ≤ t :=
  iInf₂_le t h

lemma le_captureTime_iff {c : ℝ≥0∞} : c ≤ captureTime S H ↔ ∀ t, S t = H t → c ≤ t := by
  simp [captureTime]

lemma captureTime_eq_top_iff : captureTime S H = ⊤ ↔ ∀ t, S t ≠ H t := by
  constructor
  · intro h t ht
    have := captureTime_le (S := S) (H := H) ht
    rw [h] at this
    exact ENNReal.coe_ne_top (top_le_iff.mp this)
  · intro h
    simp [captureTime, h]

/-- When the paths meet, the capture time is the first meeting time (the set of meeting times is
closed). -/
lemma exists_eq_captureTime (h : captureTime S H ≠ ⊤) :
    ∃ t : ℝ≥0, S t = H t ∧ captureTime S H = t := by
  set Z : Set ℝ≥0 := {t | S t = H t} with hZ
  have hne : Z.Nonempty := by
    by_contra hcon
    rw [Set.not_nonempty_iff_eq_empty] at hcon
    apply h
    rw [captureTime_eq_top_iff]
    intro t ht
    have : t ∈ Z := ht
    simp [hcon] at this
  have hcl : IsClosed Z := isClosed_eq S.continuous H.continuous
  have hmem : sInf Z ∈ Z := hcl.csInf_mem hne (OrderBot.bddBelow Z)
  refine ⟨sInf Z, hmem, le_antisymm (captureTime_le hmem) ?_⟩
  rw [le_captureTime_iff]
  intro t ht
  exact ENNReal.coe_le_coe.mpr (csInf_le (OrderBot.bddBelow Z) ht)

lemma captureTime_comm : captureTime S H = captureTime H S := by
  simp only [captureTime, eq_comm]

lemma captureTime_neg : captureTime (-S) (-H) = captureTime S H := by
  simp [captureTime]

/-- The intermediate value theorem: if `S ≤ H` at time `t₁` and `H ≤ S` at a later time `t₂`, the
paths meet by time `t₂`. -/
lemma captureTime_le_of_le_of_le {t₁ t₂ : ℝ≥0} (h12 : t₁ ≤ t₂) (h1 : S t₁ ≤ H t₁)
    (h2 : H t₂ ≤ S t₂) : captureTime S H ≤ t₂ := by
  have hc : ContinuousOn (fun t => H t - S t) (Set.Icc t₁ t₂) :=
    (H.continuous.sub S.continuous).continuousOn
  obtain ⟨t, ht, hzero⟩ := intermediate_value_Icc' h12 hc
    (show (0 : ℝ) ∈ Set.Icc (H t₂ - S t₂) (H t₁ - S t₁) from ⟨by linarith, by linarith⟩)
  calc captureTime S H ≤ t := captureTime_le (by linarith [hzero])
    _ ≤ t₂ := ENNReal.coe_le_coe.mpr ht.2

/-- The intermediate value theorem, with the order of the two paths reversed. -/
lemma captureTime_le_of_ge_of_ge {t₁ t₂ : ℝ≥0} (h12 : t₁ ≤ t₂) (h1 : H t₁ ≤ S t₁)
    (h2 : S t₂ ≤ H t₂) : captureTime S H ≤ t₂ := by
  rw [captureTime_comm]
  exact captureTime_le_of_le_of_le h12 h1 h2

/-- No meeting before `c`: if the paths differ at every time `t < c`, then `c ≤ T(S,H)`. -/
lemma le_captureTime_of_ne {c : ℝ≥0} (h : ∀ t : ℝ≥0, t < c → S t ≠ H t) :
    (c : ℝ≥0∞) ≤ captureTime S H := by
  rw [le_captureTime_iff]
  intro t ht
  by_contra hlt
  exact h t (ENNReal.coe_lt_coe.mp (not_le.mp hlt)) ht

end PrincessMonsterInterval
