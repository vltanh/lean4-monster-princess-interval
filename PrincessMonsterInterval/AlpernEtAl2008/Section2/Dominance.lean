module

public import PrincessMonsterInterval.CaptureTime
public import Basic.Analysis.TriangleWave
public import Mathlib.Analysis.Calculus.ContDiff.Defs

/-!
# Section 2: dominated pure strategies (Propositions 1–3)

* `EndReflecting`, `EndAbsorbing`: the paper's definitions.
* `proposition1`: every searcher path is dominated by an end-reflecting one;
  `proposition1_sweeping`: by an end-sweeping one (the same path).
* `proposition2`: every hider path is dominated by an end-absorbing one.
* `proposition3`: every smooth hider path is dominated by a path of speed at most `1`;
  `proposition3_of_continuous` drops smoothness.

A searcher path `S'` dominates `S` when `T(S', H) ≤ T(S, H)` for every hider path `H`; a hider
path `H'` dominates `H` when `T(S, H) ≤ T(S, H')` for every searcher path `S`.
-/

@[expose] public section

open scoped NNReal ENNReal

namespace PrincessMonsterInterval

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

/-! ### Helpers for Propositions 1 and 2 -/

/-- The times at which a path is at an end of the interval form a closed set; when it is
nonempty, it has a least element, the first end time. -/
private lemma dom_first_end_time (S : C(ℝ≥0, ℝ)) (hne : ∃ t, S t = 1 ∨ S t = -1) :
    ∃ t₀ : ℝ≥0, (S t₀ = 1 ∨ S t₀ = -1) ∧ ∀ t, (S t = 1 ∨ S t = -1) → t₀ ≤ t := by
  set E : Set ℝ≥0 := {t | S t = 1 ∨ S t = -1}
  have hcl : IsClosed E :=
    (isClosed_eq S.continuous continuous_const).union (isClosed_eq S.continuous continuous_const)
  exact ⟨sInf E, hcl.csInf_mem hne (OrderBot.bddBelow E),
    fun t ht => csInf_le (OrderBot.bddBelow E) ht⟩

private lemma dom_neg_mem_searcherPaths {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    -S ∈ searcherPaths := by
  refine ⟨fun t => ?_, fun t t' => ?_⟩
  · have := hS.1 t
    simp only [ContinuousMap.neg_apply, Set.mem_Icc] at this ⊢
    constructor <;> linarith [this.1, this.2]
  · simp only [ContinuousMap.neg_apply]
    rw [show -S t - -S t' = -(S t - S t') by ring, abs_neg]
    exact hS.2 t t'

private lemma dom_neg_mem_hiderPaths {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    -H ∈ hiderPaths := by
  intro t
  have := hH t
  simp only [ContinuousMap.neg_apply, Set.mem_Icc] at this ⊢
  constructor <;> linarith [this.1, this.2]

private lemma dom_endSweeping_neg {S : C(ℝ≥0, ℝ)} (h : EndSweeping S) : EndSweeping (-S) := by
  intro t₀ ht₀ t h1 h2
  simp only [ContinuousMap.neg_apply] at ht₀ ⊢
  rw [show -S t - -S t₀ = -(S t - S t₀) by ring, abs_neg]
  exact h t₀ (by rcases ht₀ with h | h <;> [right; left] <;> linarith) t h1 h2

/-- A function that is `1`-Lipschitz before and after `t₀` is `1`-Lipschitz. -/
private lemma dom_lipschitz_glue {f : ℝ≥0 → ℝ} {t₀ : ℝ≥0}
    (h1 : ∀ t t', t ≤ t₀ → t' ≤ t₀ → |f t - f t'| ≤ |(t : ℝ) - t'|)
    (h2 : ∀ t t', t₀ ≤ t → t₀ ≤ t' → |f t - f t'| ≤ |(t : ℝ) - t'|) (t t' : ℝ≥0) :
    |f t - f t'| ≤ |(t : ℝ) - t'| := by
  have key : ∀ a b : ℝ≥0, a ≤ t₀ → t₀ ≤ b → |f a - f b| ≤ |(a : ℝ) - b| := by
    intro a b ha hb
    have ha' : (a : ℝ) ≤ t₀ := ha
    have hb' : (t₀ : ℝ) ≤ b := hb
    have e1 := h1 a t₀ ha le_rfl
    have e2 := h2 t₀ b le_rfl hb
    rw [abs_of_nonpos (show (a : ℝ) - t₀ ≤ 0 by linarith)] at e1
    rw [abs_of_nonpos (show (t₀ : ℝ) - b ≤ 0 by linarith)] at e2
    rw [abs_of_nonpos (show (a : ℝ) - b ≤ 0 by linarith)]
    calc |f a - f b| ≤ |f a - f t₀| + |f t₀ - f b| := abs_sub_le _ _ _
      _ ≤ _ := by linarith
  rcases le_total t t₀ with ht | ht <;> rcases le_total t' t₀ with ht' | ht'
  · exact h1 t t' ht ht'
  · exact key t t' ht ht'
  · rw [abs_sub_comm, abs_sub_comm (t : ℝ)]
    exact key t' t ht' ht
  · exact h2 t t' ht ht'

/-- The triangle wave, started at an end, sweeps to the other end at unit speed. -/
private lemma dom_triangleWave_sweep {a h : ℝ}
    (ha : Real.triangleWave a = 1 ∨ Real.triangleWave a = -1) (h0 : 0 ≤ h) (h2 : h ≤ 2) :
    |Real.triangleWave (a - h) - Real.triangleWave a| = h := by
  obtain ⟨k, hk⟩ := Real.exists_abs_sub_four_mul_le (a + 1)
  have hta := Real.triangleWave_eq_of_abs_le hk
  rcases ha with ha | ha
  · -- `a + 1 - 4k = ±2`: the wave comes down from `1`
    have habs : |a + 1 - 4 * k| = 2 := by linarith
    have hval : Real.triangleWave (a - h) = 1 - h := by
      rcases (abs_eq (by norm_num : (0 : ℝ) ≤ 2)).mp habs with he | he
      · have he' : a - h + 1 - 4 * (k : ℝ) = 2 - h := by linarith
        have hk' : |a - h + 1 - 4 * (k : ℝ)| ≤ 2 := by
          rw [he', abs_of_nonneg (by linarith)]
          linarith
        rw [Real.triangleWave_eq_of_abs_le hk', he', abs_of_nonneg (by linarith)]
        ring
      · have he' : a - h + 1 - 4 * ((k + 1 : ℤ) : ℝ) = -2 - h - 4 := by push_cast; linarith
        have he'' : a - h + 1 - 4 * ((k - 1 : ℤ) : ℝ) = 2 - h := by push_cast; linarith
        have hk' : |a - h + 1 - 4 * ((k - 1 : ℤ) : ℝ)| ≤ 2 := by
          rw [he'', abs_of_nonneg (by linarith)]
          linarith
        rw [Real.triangleWave_eq_of_abs_le hk', he'', abs_of_nonneg (by linarith)]
        ring
    rw [hval, ha, show 1 - h - 1 = -h by ring, abs_neg, abs_of_nonneg h0]
  · -- `a + 1 = 4k`: the wave goes up from `-1`
    have habs : |a + 1 - 4 * k| = 0 := by linarith
    have he : a + 1 - 4 * (k : ℝ) = 0 := abs_eq_zero.mp habs
    have he' : a - h + 1 - 4 * (k : ℝ) = -h := by linarith
    have hk' : |a - h + 1 - 4 * (k : ℝ)| ≤ 2 := by
      rw [he', abs_neg, abs_of_nonneg h0]
      exact h2
    rw [Real.triangleWave_eq_of_abs_le hk', he', abs_neg, abs_of_nonneg h0, ha,
      show h - 1 - -1 = h by ring, abs_of_nonneg h0]

/-- The construction of Proposition 1 for a path whose first end time `t₀` is at `+1`: follow `S`
until `t₀`, then sweep between the ends at unit speed (the triangle wave `1 - (t - t₀)`). -/
private lemma dom_prop1_aux {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) {t₀ : ℝ≥0} (ht₀ : S t₀ = 1)
    (hfirst : ∀ t, (S t = 1 ∨ S t = -1) → t₀ ≤ t) :
    ∃ S' ∈ searcherPaths, EndSweeping S' ∧
      (∀ t, t₀ ≤ t → S' t = Real.triangleWave (1 - ((t : ℝ) - t₀))) ∧
      ∀ H ∈ hiderPaths, captureTime S' H ≤ captureTime S H := by
  have htw1 : Real.triangleWave 1 = 1 := Real.triangleWave_of_mem_Icc ⟨by norm_num, le_rfl⟩
  let S' : C(ℝ≥0, ℝ) :=
    ⟨fun t => S (min t t₀) + (Real.triangleWave (1 - max ((t : ℝ) - t₀) 0) - 1), by fun_prop⟩
  have hS'1 : ∀ t, t ≤ t₀ → S' t = S t := fun t ht => by
    have ht' : (t : ℝ) ≤ t₀ := ht
    simp only [S', ContinuousMap.coe_mk, min_eq_left ht,
      max_eq_right (by linarith : (t : ℝ) - t₀ ≤ 0), sub_zero, htw1, sub_self, add_zero]
  have hS'2 : ∀ t, t₀ ≤ t → S' t = Real.triangleWave (1 - ((t : ℝ) - t₀)) := fun t ht => by
    have ht' : (t₀ : ℝ) ≤ t := ht
    simp only [S', ContinuousMap.coe_mk, min_eq_right ht,
      max_eq_left (by linarith : (0 : ℝ) ≤ t - t₀), ht₀]
    ring
  refine ⟨S', ⟨fun t => ?_, dom_lipschitz_glue (t₀ := t₀) (fun t t' ht ht' => ?_)
    (fun t t' ht ht' => ?_)⟩, ?_, hS'2, ?_⟩
  · rcases le_total t t₀ with ht | ht
    · rw [hS'1 t ht]
      exact hS.1 t
    · rw [hS'2 t ht]
      exact Real.triangleWave_mem_Icc _
  · rw [hS'1 t ht, hS'1 t' ht']
    exact hS.2 t t'
  · rw [hS'2 t ht, hS'2 t' ht']
    refine (Real.abs_triangleWave_sub_le _ _).trans (le_of_eq ?_)
    rw [show 1 - ((t : ℝ) - t₀) - (1 - ((t' : ℝ) - t₀)) = -((t : ℝ) - t') by ring, abs_neg]
  · -- end-sweeping: an end is reached only from `t₀` on, where `S'` is the triangle wave
    intro s hs t hst ht2
    have hs0 : t₀ ≤ s := by
      by_contra hlt
      rw [not_le] at hlt
      rw [hS'1 s hlt.le] at hs
      exact absurd (hfirst s hs) (not_le.mpr hlt)
    have hs0' : (t₀ : ℝ) ≤ s := hs0
    have hst' : (s : ℝ) ≤ t := hst
    rw [hS'2 s hs0] at hs ⊢
    rw [hS'2 t (hs0.trans hst),
      show 1 - ((t : ℝ) - t₀) = (1 - ((s : ℝ) - t₀)) - ((t : ℝ) - s) by ring]
    exact dom_triangleWave_sweep hs (by linarith) (by linarith)
  · -- domination
    intro H hH
    by_cases htop : captureTime S H = ⊤
    · rw [htop]
      exact le_top
    obtain ⟨t₁, hm, hT⟩ := exists_eq_captureTime htop
    rw [hT]
    rcases le_total t₁ t₀ with h10 | h01
    · exact captureTime_le (by rw [hS'1 t₁ h10]; exact hm)
    have hH0 : H t₀ ≤ S' t₀ := by
      rw [hS'2 t₀ le_rfl, sub_self, sub_zero, htw1]
      exact (hH t₀).2
    have h01' : (t₀ : ℝ) ≤ t₁ := h01
    by_cases h12 : (t₁ : ℝ) ≤ t₀ + 2
    · -- `S` cannot have run ahead of `S'`, which went straight down from `1` at `t₀`
      refine captureTime_le_of_ge_of_ge h01 hH0 ?_
      rw [hS'2 t₁ h01, Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith⟩, ← hm]
      have hlip := hS.2 t₁ t₀
      rw [ht₀, abs_of_nonneg (by linarith : (0 : ℝ) ≤ t₁ - t₀)] at hlip
      linarith [neg_abs_le (S t₁ - 1)]
    · -- `S'` has swept the whole interval by `t₀ + 2`
      rw [not_le] at h12
      have h02 : t₀ ≤ t₀ + 2 := le_self_add
      have hle : captureTime S' H ≤ ((t₀ + 2 : ℝ≥0) : ℝ≥0∞) := by
        refine captureTime_le_of_ge_of_ge h02 hH0 ?_
        rw [hS'2 _ h02, NNReal.coe_add, NNReal.coe_ofNat,
          show (1 : ℝ) - (t₀ + 2 - t₀) = -1 by ring,
          Real.triangleWave_of_mem_Icc ⟨le_rfl, by norm_num⟩]
        exact (hH _).1
      refine hle.trans (ENNReal.coe_le_coe.mpr ?_)
      rw [← NNReal.coe_le_coe, NNReal.coe_add, NNReal.coe_ofNat]
      exact h12.le

/-- The construction of Proposition 1: follow `S` up to its first end time `t₀`, then sweep
between the ends at unit speed (`S` itself if it never reaches an end).

Departure from the paper: the paper continues `S` after `t₀` by `1 + t₀ - t`, which leaves the
interval after `t₀ + 2`; here the motion turns back at each end (the triangle wave). -/
private lemma dom_exists_endSweeping {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    ∃ S' ∈ searcherPaths, EndSweeping S' ∧
      ∀ H ∈ hiderPaths, captureTime S' H ≤ captureTime S H := by
  by_cases hne : ∃ t, S t = 1 ∨ S t = -1
  · obtain ⟨t₀, ht₀, hfirst⟩ := dom_first_end_time S hne
    rcases ht₀ with h1 | h1
    · obtain ⟨S', hS', hsw, -, hdom⟩ := dom_prop1_aux hS h1 hfirst
      exact ⟨S', hS', hsw, hdom⟩
    · -- the first end is `-1`: reflect the interval
      obtain ⟨S', hS', hsw, -, hdom⟩ := dom_prop1_aux (dom_neg_mem_searcherPaths hS)
        (by simp [h1]) fun t ht => hfirst t (by
          simp only [ContinuousMap.neg_apply] at ht
          rcases ht with h | h <;> [right; left] <;> linarith)
      refine ⟨-S', dom_neg_mem_searcherPaths hS', dom_endSweeping_neg hsw, fun H hH => ?_⟩
      calc captureTime (-S') H = captureTime (-S') (-(-H)) := by rw [neg_neg]
        _ = captureTime S' (-H) := captureTime_neg
        _ ≤ captureTime (-S) (-H) := hdom (-H) (dom_neg_mem_hiderPaths hH)
        _ = captureTime S H := captureTime_neg
  · -- `S` never reaches an end, so it is end-sweeping
    refine ⟨S, hS, fun t₀ ht₀ => absurd ⟨t₀, ht₀⟩ hne, fun H _ => le_rfl⟩

/-- **Proposition 1** (`prop:1`). Every pure searcher strategy is dominated by one which is
end-reflecting.

The dominating path is the end-sweeping one of `proposition1_sweeping`. Departure from the
paper: the paper's `S*` (equal to `S` up to the first end time `t₀`, then `1 + t₀ - t`) leaves the
interval after `t₀ + 2`; here it turns back at each end and keeps sweeping (a triangle wave). -/
theorem proposition1 {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    ∃ S' ∈ searcherPaths, EndReflecting S' ∧
      ∀ H ∈ hiderPaths, captureTime S' H ≤ captureTime S H := by
  obtain ⟨S', hS', hsw, hdom⟩ := dom_exists_endSweeping hS
  exact ⟨S', hS', fun t₀ ht₀ t h1 h2 => hsw t₀ ht₀ t h1 (by linarith), hdom⟩

/-- **Proposition 1** (`prop:1`), in the form the text describes: every pure searcher strategy is
dominated by one that, once it reaches an end, goes directly to the other end.

Departure from the paper: the paper's `S*` (equal to `S` up to the first end time `t₀`, then
`1 + t₀ - t`) leaves the interval after `t₀ + 2`; here it turns back at each end and keeps
sweeping (a triangle wave). -/
theorem proposition1_sweeping {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    ∃ S' ∈ searcherPaths, EndSweeping S' ∧
      ∀ H ∈ hiderPaths, captureTime S' H ≤ captureTime S H := by
  exact dom_exists_endSweeping hS

/-- **Proposition 1** (`prop:1`), for a path that starts at the end `+1`: the dominating path of
the proof is then the sweeper `t ↦ 1 - t` (folded by the triangle wave), so a searcher who starts
at an end may adopt the sweeper (the paper uses this in Section 3: "If the searcher starts out
from an end, then by Proposition 1 it is optimal to adopt strategy A"). -/
theorem proposition1_start_one {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) (h0 : S 0 = 1) :
    ∀ H ∈ hiderPaths,
      captureTime (pathOf (fun t => Real.triangleWave (1 - t)) (by fun_prop)) H ≤
        captureTime S H := by
  -- the first end time is `t₀ = 0`, after which the construction is the triangle wave `1 - t`
  obtain ⟨S', -, -, hform, hdom⟩ := dom_prop1_aux hS h0 fun t _ => zero_le
  have hS' : S' = pathOf (fun t => Real.triangleWave (1 - t)) (by fun_prop) := by
    ext t
    rw [hform t zero_le, pathOf_apply, NNReal.coe_zero, sub_zero]
  exact hS' ▸ hdom

/-- **Proposition 2** (`prop:2`). Every pure hider strategy is dominated by one which is
end-absorbing. -/
theorem proposition2 {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    ∃ H' ∈ hiderPaths, EndAbsorbing H' ∧
      ∀ S ∈ searcherPaths, captureTime S H ≤ captureTime S H' := by
  by_cases hne : ∃ t, H t = 1 ∨ H t = -1
  · obtain ⟨t₀, ht₀, hfirst⟩ := dom_first_end_time H hne
    -- `H'` agrees with `H` up to `t₀` and then stays at the end `H t₀`
    let H' : C(ℝ≥0, ℝ) := ⟨fun t => H (min t t₀), by fun_prop⟩
    have hH'1 : ∀ t, t ≤ t₀ → H' t = H t := fun t ht => by
      simp only [H', ContinuousMap.coe_mk, min_eq_left ht]
    have hH'2 : ∀ t, t₀ ≤ t → H' t = H t₀ := fun t ht => by
      simp only [H', ContinuousMap.coe_mk, min_eq_right ht]
    refine ⟨H', fun t => hH _, fun s hs t hst => ?_, fun S hS => ?_⟩
    · have hs0 : t₀ ≤ s := by
        by_contra hlt
        rw [not_le] at hlt
        rw [hH'1 s hlt.le] at hs
        exact absurd (hfirst s hs) (not_le.mpr hlt)
      rw [hH'2 t (hs0.trans hst), hH'2 s hs0]
    · rw [le_captureTime_iff]
      intro t ht
      rcases le_total t t₀ with htt | htt
      · rw [hH'1 t htt] at ht
        exact captureTime_le ht
      · -- `S` is at the end `H t₀` at time `t` and on the inner side of it at `t₀`
        rw [hH'2 t htt] at ht
        rcases ht₀ with h1 | h1
        · exact captureTime_le_of_le_of_le htt (by rw [h1]; exact (hS.1 t₀).2)
            (by rw [ht, h1]; exact (hH t).2)
        · exact captureTime_le_of_ge_of_ge htt (by rw [h1]; exact (hS.1 t₀).1)
            (by rw [ht, h1]; exact (hH t).1)
  · -- `H` never reaches an end, so it is end-absorbing
    refine ⟨H, hH, fun t₀ ht₀ => absurd ⟨t₀, ht₀⟩ hne, fun S _ => le_rfl⟩

/-- A path is *smooth* if it is continuously differentiable on `[0, ∞)` (one-sided at `0`). -/
def Smooth (H : C(ℝ≥0, ℝ)) : Prop :=
  ContDiffOn ℝ 1 (fun t : ℝ => H t.toNNReal) (Set.Ici 0)

/-! ### Helpers for Proposition 3

For a hider path `H` the dominating path of speed at most `1` is, in closed form,
`H*(t) = inf_{s ≤ t} (L(s) + (t - s))` with `L(s) = sup_{r ≤ s} (H r - (s - r))`; it lies between
`U(t) = inf_{s ≤ t} (H s + (t - s))` and `L(t)`. -/

private lemma dom_isCompact_Iic (s : ℝ≥0) : IsCompact (Set.Iic s) := by
  rw [← Set.Icc_bot]
  exact isCompact_Icc

/-- `L(s) = sup_{r ≤ s} (H r - (s - r))`: the highest position from which `H` can be reached at
time `s` running down at unit speed. -/
private noncomputable def dom_L (H : C(ℝ≥0, ℝ)) (s : ℝ≥0) : ℝ :=
  sSup ((fun r : ℝ≥0 => H r - ((s : ℝ) - r)) '' Set.Iic s)

/-- `U(t) = inf_{s ≤ t} (H s + (t - s))`. -/
private noncomputable def dom_U (H : C(ℝ≥0, ℝ)) (t : ℝ≥0) : ℝ :=
  sInf ((fun s : ℝ≥0 => H s + ((t : ℝ) - s)) '' Set.Iic t)

/-- `H*(t) = inf_{s ≤ t} (L(s) + (t - s))`. -/
private noncomputable def dom_Hstar (H : C(ℝ≥0, ℝ)) (t : ℝ≥0) : ℝ :=
  sInf ((fun s : ℝ≥0 => dom_L H s + ((t : ℝ) - s)) '' Set.Iic t)

private lemma dom_L_image_compact (H : C(ℝ≥0, ℝ)) (s : ℝ≥0) :
    IsCompact ((fun r : ℝ≥0 => H r - ((s : ℝ) - r)) '' Set.Iic s) :=
  (dom_isCompact_Iic s).image (by fun_prop)

private lemma dom_U_image_compact (H : C(ℝ≥0, ℝ)) (t : ℝ≥0) :
    IsCompact ((fun s : ℝ≥0 => H s + ((t : ℝ) - s)) '' Set.Iic t) :=
  (dom_isCompact_Iic t).image (by fun_prop)

private lemma dom_le_L (H : C(ℝ≥0, ℝ)) {r s : ℝ≥0} (hr : r ≤ s) :
    H r - ((s : ℝ) - r) ≤ dom_L H s :=
  le_csSup (dom_L_image_compact H s).bddAbove ⟨r, hr, rfl⟩

/-- The supremum defining `L(s)` is attained. -/
private lemma dom_L_attained (H : C(ℝ≥0, ℝ)) (s : ℝ≥0) :
    ∃ r ≤ s, H r - ((s : ℝ) - r) = dom_L H s := by
  obtain ⟨r, hr, he⟩ := (dom_L_image_compact H s).sSup_mem ⟨_, s, le_rfl, rfl⟩
  exact ⟨r, hr, he⟩

private lemma dom_self_le_L (H : C(ℝ≥0, ℝ)) (s : ℝ≥0) : H s ≤ dom_L H s := by
  simpa using dom_le_L H (le_refl s)

private lemma dom_L_le_one {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (s : ℝ≥0) : dom_L H s ≤ 1 := by
  refine csSup_le ⟨_, s, le_rfl, rfl⟩ ?_
  rintro _ ⟨r, hr, rfl⟩
  have : (r : ℝ) ≤ s := hr
  linarith [(hH r).2]

/-- `L` falls at speed at most `1`. -/
private lemma dom_L_sub_le (H : C(ℝ≥0, ℝ)) {s s' : ℝ≥0} (h : s ≤ s') :
    dom_L H s - ((s' : ℝ) - s) ≤ dom_L H s' := by
  have : dom_L H s ≤ dom_L H s' + ((s' : ℝ) - s) := by
    refine csSup_le ⟨_, s, le_rfl, rfl⟩ ?_
    rintro _ ⟨r, hr, rfl⟩
    have := dom_le_L H (hr.trans h)
    simp only at this ⊢
    linarith
  linarith

private lemma dom_U_le (H : C(ℝ≥0, ℝ)) {s t : ℝ≥0} (hs : s ≤ t) :
    dom_U H t ≤ H s + ((t : ℝ) - s) :=
  csInf_le (dom_U_image_compact H t).bddBelow ⟨s, hs, rfl⟩

/-- The infimum defining `U(t)` is attained. -/
private lemma dom_U_attained (H : C(ℝ≥0, ℝ)) (t : ℝ≥0) :
    ∃ s ≤ t, H s + ((t : ℝ) - s) = dom_U H t := by
  obtain ⟨s, hs, he⟩ := (dom_U_image_compact H t).sInf_mem ⟨_, t, le_rfl, rfl⟩
  exact ⟨s, hs, he⟩

private lemma dom_Hstar_bddBelow {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (t : ℝ≥0) :
    BddBelow ((fun s : ℝ≥0 => dom_L H s + ((t : ℝ) - s)) '' Set.Iic t) := by
  refine ⟨-1, ?_⟩
  rintro _ ⟨s, hs, rfl⟩
  have : (s : ℝ) ≤ t := hs
  linarith [dom_self_le_L H s, (hH s).1]

private lemma dom_Hstar_le {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) {s t : ℝ≥0} (hs : s ≤ t) :
    dom_Hstar H t ≤ dom_L H s + ((t : ℝ) - s) :=
  csInf_le (dom_Hstar_bddBelow hH t) ⟨s, hs, rfl⟩

private lemma dom_le_Hstar (H : C(ℝ≥0, ℝ)) {c : ℝ} {t : ℝ≥0}
    (h : ∀ s ≤ t, c ≤ dom_L H s + ((t : ℝ) - s)) : c ≤ dom_Hstar H t := by
  refine le_csInf ⟨_, t, le_rfl, rfl⟩ ?_
  rintro _ ⟨s, hs, rfl⟩
  exact h s hs

/-- `H* ≤ L`. -/
private lemma dom_Hstar_le_L {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (t : ℝ≥0) :
    dom_Hstar H t ≤ dom_L H t := by
  simpa using dom_Hstar_le hH (le_refl t)

/-- `U ≤ H*`. -/
private lemma dom_U_le_Hstar (H : C(ℝ≥0, ℝ)) (t : ℝ≥0) : dom_U H t ≤ dom_Hstar H t :=
  dom_le_Hstar H fun s hs => (dom_U_le H hs).trans (by linarith [dom_self_le_L H s])

/-- `H*` has speed at most `1`. -/
private lemma dom_Hstar_lipschitz {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (t t' : ℝ≥0) :
    |dom_Hstar H t - dom_Hstar H t'| ≤ |(t : ℝ) - t'| := by
  have key : ∀ a b : ℝ≥0, a ≤ b → |dom_Hstar H a - dom_Hstar H b| ≤ |(a : ℝ) - b| := by
    intro a b hab
    have hab' : (a : ℝ) ≤ b := hab
    rw [abs_sub_comm (a : ℝ), abs_of_nonneg (by linarith : (0 : ℝ) ≤ b - a), abs_le]
    constructor
    · -- `H* b ≤ H* a + (b - a)`
      have : dom_Hstar H b - ((b : ℝ) - a) ≤ dom_Hstar H a := by
        refine dom_le_Hstar H fun s hs => ?_
        have := dom_Hstar_le hH (hs.trans hab)
        linarith
      linarith
    · -- `H* a - (b - a) ≤ H* b`
      have : dom_Hstar H a - ((b : ℝ) - a) ≤ dom_Hstar H b := by
        refine dom_le_Hstar H fun s hs => ?_
        have hs' : (s : ℝ) ≤ b := hs
        rcases le_total s a with hsa | has
        · have hsa' : (s : ℝ) ≤ a := hsa
          have := dom_Hstar_le hH hsa
          linarith
        · have has' : (a : ℝ) ≤ s := has
          have h1 := dom_L_sub_le H has
          have h2 := dom_Hstar_le_L hH a
          linarith
      linarith
  rcases le_total t t' with h | h
  · exact key t t' h
  · rw [abs_sub_comm, abs_sub_comm (t : ℝ)]
    exact key t' t h

/-- Every hider path is dominated by a path of speed at most `1`, given in closed form: it stays
between the envelopes `U(t) = inf_{s ≤ t} (H s + (t - s))` and `L(t) = sup_{s ≤ t} (H s - (t - s))`,
so it cannot be caught from behind. -/
private lemma dom_exists_dominating {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    ∃ H' ∈ searcherPaths, ∀ S ∈ searcherPaths, captureTime S H ≤ captureTime S H' := by
  have hcont : Continuous (dom_Hstar H) := by
    refine (LipschitzWith.of_dist_le_mul (K := 1) fun x y => ?_).continuous
    rw [Real.dist_eq, NNReal.dist_eq, NNReal.coe_one, one_mul]
    exact dom_Hstar_lipschitz hH x y
  let H' : C(ℝ≥0, ℝ) := ⟨dom_Hstar H, hcont⟩
  have hH' : ∀ t, H' t = dom_Hstar H t := fun _ => rfl
  refine ⟨H', ⟨fun t => ⟨?_, ?_⟩, fun t t' => ?_⟩, fun S hS => ?_⟩
  · rw [hH']
    obtain ⟨s, hs, he⟩ := dom_U_attained H t
    have : (s : ℝ) ≤ t := hs
    linarith [dom_U_le_Hstar H t, (hH s).1]
  · rw [hH']
    exact (dom_Hstar_le_L hH t).trans (dom_L_le_one hH t)
  · rw [hH', hH']
    exact dom_Hstar_lipschitz hH t t'
  · -- `H'` cannot be caught from behind
    rw [le_captureTime_iff]
    intro t ht
    rw [hH'] at ht
    have hlip : ∀ s ≤ t, |S t - S s| ≤ (t : ℝ) - s := fun s hs => by
      have := hS.2 t s
      have hs' : (s : ℝ) ≤ t := hs
      rwa [abs_of_nonneg (show (0 : ℝ) ≤ t - s by linarith)] at this
    rcases le_total (dom_Hstar H t) (H t) with hle | hle
    · -- `H` is weakly ahead: the searcher was at or above `H` at the time `s` attaining `U(t)`
      obtain ⟨s, hs, he⟩ := dom_U_attained H t
      have h1 := hlip s hs
      have h2 := dom_U_le_Hstar H t
      refine captureTime_le_of_ge_of_ge hs ?_ (by rw [ht]; exact hle)
      linarith [le_abs_self (S t - S s), neg_abs_le (S t - S s)]
    · -- symmetric, with the time `r` attaining `L(t)`
      obtain ⟨r, hr, he⟩ := dom_L_attained H t
      have h1 := hlip r hr
      have h2 := dom_Hstar_le_L hH t
      refine captureTime_le_of_le_of_le hr ?_ (by rw [ht]; exact hle)
      linarith [le_abs_self (S t - S r), neg_abs_le (S t - S r)]

/-- **Proposition 3** (`prop:3`). Every smooth hider strategy is dominated by one in `𝒮`, that is,
one with speed bounded by `1`.

Departure from the paper: the inductive construction of `H*` (which can stall: `τ` may equal
`t₀`, and the times may accumulate) is replaced by a different dominating path in closed form;
the domination argument is the paper's. Smoothness is not used; see
`proposition3_of_continuous`. -/
theorem proposition3 {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) (_hsmooth : Smooth H) :
    ∃ H' ∈ searcherPaths, ∀ S ∈ searcherPaths, captureTime S H ≤ captureTime S H' :=
  dom_exists_dominating hH

end PrincessMonsterInterval

namespace PrincessMonsterInterval

/-- **Proposition 3** (`prop:3`) holds for every continuous hider path, smooth or not.

Departure from the paper: the inductive construction of `H*` (which can stall: `τ` may equal
`t₀`, and the times may accumulate) is replaced by a different dominating path in closed form,
`H*(t) = inf_{s ≤ t} (L(s) + (t - s))` with `L(s) = sup_{r ≤ s} (H r - (s - r))`. It has speed at
most `1` and stays between the envelopes `U ≤ H* ≤ L`, which gives the paper's argument: `H*`
cannot be caught from behind. Unlike the paper's path it may move away from `H` (it rises at unit
speed until it reaches `L`). -/
theorem proposition3_of_continuous {H : C(ℝ≥0, ℝ)} (hH : H ∈ hiderPaths) :
    ∃ H' ∈ searcherPaths, ∀ S ∈ searcherPaths, captureTime S H ≤ captureTime S H' :=
  dom_exists_dominating hH

end PrincessMonsterInterval
