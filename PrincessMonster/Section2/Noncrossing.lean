module

public import PrincessMonster.CaptureTime
public import Mathlib.MeasureTheory.Measure.Lebesgue.Basic

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

/-- If every meeting of `S` with `C` or `D` is a meeting with `A` or `B`, then `S` meets `A` or `B`
no later than it meets `C` or `D`. -/
private lemma dom_min_le_min {S A B C D : C(ℝ≥0, ℝ)}
    (h : ∀ t, S t = C t ∨ S t = D t → S t = A t ∨ S t = B t) :
    min (captureTime S A) (captureTime S B) ≤ min (captureTime S C) (captureTime S D) := by
  refine le_min ?_ ?_ <;> rw [le_captureTime_iff] <;> intro t ht
  · rcases h t (Or.inl ht) with h' | h'
    · exact min_le_of_left_le (captureTime_le h')
    · exact min_le_of_right_le (captureTime_le h')
  · rcases h t (Or.inr ht) with h' | h'
    · exact min_le_of_left_le (captureTime_le h')
    · exact min_le_of_right_le (captureTime_le h')

/-- At every time the pairs `{H₁ t, H₂ t}` and `{(H₁ ∧ H₂) t, (H₁ ∨ H₂) t}` are the same. -/
private lemma dom_meet_inf_sup_iff (S H₁ H₂ : C(ℝ≥0, ℝ)) (t : ℝ≥0) :
    (S t = (H₁ ⊓ H₂) t ∨ S t = (H₁ ⊔ H₂) t) ↔ (S t = H₁ t ∨ S t = H₂ t) := by
  simp only [ContinuousMap.inf_apply, ContinuousMap.sup_apply]
  rcases le_total (H₁ t) (H₂ t) with h | h
  · rw [inf_eq_left.mpr h, sup_eq_right.mpr h]
  · rw [inf_eq_right.mpr h, sup_eq_left.mpr h]
    exact or_comm

/-- If `S` first meets `H₁` at `t₁`, with `H₁ t₁ ≤ H₂ t₁`, then `S` meets `H₂` no later than
`H₁ ∨ H₂`. -/
private lemma dom_captureTime_le_sup {S H₁ H₂ : C(ℝ≥0, ℝ)} {t₁ : ℝ≥0} (hm : S t₁ = H₁ t₁)
    (hle : H₁ t₁ ≤ H₂ t₁) (hfirst : ∀ t < t₁, S t ≠ H₁ t) :
    captureTime S H₂ ≤ captureTime S (H₁ ⊔ H₂) := by
  rw [le_captureTime_iff]
  intro t ht
  rw [ContinuousMap.sup_apply] at ht
  rcases lt_or_ge t t₁ with htt | htt
  · rcases max_choice (H₁ t) (H₂ t) with h | h
    · rw [h] at ht
      exact absurd ht (hfirst t htt)
    · rw [h] at ht
      exact captureTime_le ht
  · exact captureTime_le_of_le_of_le htt (hm ▸ hle) (ht ▸ le_sup_right)

/-- If `S` first meets `H₁` at `t₁`, with `H₂ t₁ ≤ H₁ t₁`, then `S` meets `H₂` no later than
`H₁ ∧ H₂`. -/
private lemma dom_captureTime_le_inf {S H₁ H₂ : C(ℝ≥0, ℝ)} {t₁ : ℝ≥0} (hm : S t₁ = H₁ t₁)
    (hle : H₂ t₁ ≤ H₁ t₁) (hfirst : ∀ t < t₁, S t ≠ H₁ t) :
    captureTime S H₂ ≤ captureTime S (H₁ ⊓ H₂) := by
  rw [le_captureTime_iff]
  intro t ht
  rw [ContinuousMap.inf_apply] at ht
  rcases lt_or_ge t t₁ with htt | htt
  · rcases min_choice (H₁ t) (H₂ t) with h | h
    · rw [h] at ht
      exact absurd ht (hfirst t htt)
    · rw [h] at ht
      exact captureTime_le ht
  · exact captureTime_le_of_ge_of_ge htt (hm ▸ hle) (ht ▸ inf_le_right)

/-- **Proposition 7** (`prop:7`). The hider strategy that mixes `H₁, H₂` with equal probability
is dominated by the noncrossing strategy that mixes `H₁ ∧ H₂, H₁ ∨ H₂` with equal probability:
against every searcher path the sum of the two capture times does not decrease. -/
theorem proposition7 {H₁ H₂ : C(ℝ≥0, ℝ)} (h₁ : H₁ ∈ hiderPaths) (h₂ : H₂ ∈ hiderPaths)
    {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    captureTime S H₁ + captureTime S H₂ ≤ captureTime S (H₁ ⊓ H₂) + captureTime S (H₁ ⊔ H₂) := by
  -- renumber so that `H₁` is caught first
  wlog h12 : captureTime S H₁ ≤ captureTime S H₂ generalizing H₁ H₂
  · have := this h₂ h₁ (not_le.mp h12).le
    rwa [inf_comm, sup_comm, add_comm (captureTime S H₂)] at this
  -- the first catch of either pair happens at the same time `t₁ = T(S, H₁)`
  have hmin : captureTime S H₁ = min (captureTime S (H₁ ⊓ H₂)) (captureTime S (H₁ ⊔ H₂)) := by
    rw [← min_eq_left h12]
    exact le_antisymm (dom_min_le_min fun t ht => (dom_meet_inf_sup_iff S H₁ H₂ t).mp ht)
      (dom_min_le_min fun t ht => (dom_meet_inf_sup_iff S H₁ H₂ t).mpr ht)
  by_cases htop : captureTime S H₁ = ⊤
  · have : captureTime S (H₁ ⊓ H₂) = ⊤ := by
      apply top_le_iff.mp
      rw [← htop, hmin]
      exact min_le_left _ _
    rw [this, top_add]
    exact le_top
  obtain ⟨t₁, hm, ht₁⟩ := exists_eq_captureTime htop
  have hfirst : ∀ t < t₁, S t ≠ H₁ t := fun t ht he => by
    have := captureTime_le he
    rw [ht₁] at this
    exact absurd (ENNReal.coe_le_coe.mp this) (not_le.mpr ht)
  -- the searcher is on the side of `H₁` at `t₁`; the path on the other side is caught no earlier
  -- than `H₂`
  rcases le_total (H₁ t₁) (H₂ t₁) with hle | hle
  · refine add_le_add ?_ (dom_captureTime_le_sup hm hle hfirst)
    rw [hmin]
    exact min_le_left _ _
  · calc captureTime S H₁ + captureTime S H₂
        ≤ captureTime S (H₁ ⊔ H₂) + captureTime S (H₁ ⊓ H₂) := by
          refine add_le_add ?_ (dom_captureTime_le_inf hm hle hfirst)
          rw [hmin]
          exact min_le_right _ _
      _ = _ := add_comm _ _

/-! ### Quantile paths

The tools for `proposition7_finite`. For weights `w i ≥ 0` of total `W` and `0 < u ≤ W`, the
*`u`-quantile path* is `Q_u = min_{A : w(A) ≥ u} max_{i ∈ A} H i`; at each time it is the smallest
value `x` such that the paths at or below `x` carry weight at least `u`. The quantile paths are
ordered by `u`, so pairwise noncrossing, and `u ↦ Q_u` takes finitely many values. -/

section Quantile

open MeasureTheory

variable {n : ℕ}

/-- The upper envelope `max_{i ∈ A} H i` of a set `A` of paths (equal to `-1` when `A = ∅`). -/
private noncomputable def dom_maxPath (H : Fin n → C(ℝ≥0, ℝ)) (A : Finset (Fin n)) :
    C(ℝ≥0, ℝ) :=
  A.fold (· ⊔ ·) (ContinuousMap.const ℝ≥0 (-1)) H

private lemma dom_maxPath_apply (H : Fin n → C(ℝ≥0, ℝ)) (A : Finset (Fin n)) (s : ℝ≥0) :
    dom_maxPath H A s = A.fold max (-1) (fun i => H i s) :=
  (Finset.fold_hom (m := fun f : C(ℝ≥0, ℝ) => f s) fun _ _ => rfl).symm

/-- The lower envelope `min_{A ∈ 𝒜} max_{i ∈ A} H i` (equal to `1` when `𝒜 = ∅`). -/
private noncomputable def dom_quantPath (H : Fin n → C(ℝ≥0, ℝ)) (𝒜 : Finset (Finset (Fin n))) :
    C(ℝ≥0, ℝ) :=
  𝒜.fold (· ⊓ ·) (ContinuousMap.const ℝ≥0 1) (dom_maxPath H)

private lemma dom_quantPath_apply (H : Fin n → C(ℝ≥0, ℝ)) (𝒜 : Finset (Finset (Fin n)))
    (s : ℝ≥0) : dom_quantPath H 𝒜 s = 𝒜.fold min 1 (fun A => dom_maxPath H A s) :=
  (Finset.fold_hom (m := fun f : C(ℝ≥0, ℝ) => f s) fun _ _ => rfl).symm

/-- The sets of indices of weight at least `u`. -/
private noncomputable def dom_heavy (w : Fin n → ℝ) (u : ℝ) : Finset (Finset (Fin n)) :=
  Finset.univ.filter fun A => u ≤ ∑ i ∈ A, w i

/-- The `u`-quantile path `Q_u = min_{A : w(A) ≥ u} max_{i ∈ A} H i`. -/
private noncomputable def dom_quantile (w : Fin n → ℝ) (H : Fin n → C(ℝ≥0, ℝ)) (u : ℝ) :
    C(ℝ≥0, ℝ) :=
  dom_quantPath H (dom_heavy w u)

private lemma dom_quantile_mem (w : Fin n → ℝ) (H : Fin n → C(ℝ≥0, ℝ)) (u : ℝ) :
    dom_quantile w H u ∈ hiderPaths := by
  intro s
  rw [dom_quantile, dom_quantPath_apply]
  refine ⟨(Finset.le_fold_min _).mpr ⟨by norm_num, fun A _ => ?_⟩,
    (Finset.fold_min_le _).mpr (Or.inl le_rfl)⟩
  rw [dom_maxPath_apply]
  exact (Finset.le_fold_max _).mpr (Or.inl le_rfl)

/-- The quantile paths are ordered by their level. -/
private lemma dom_quantile_mono (w : Fin n → ℝ) (H : Fin n → C(ℝ≥0, ℝ)) {u u' : ℝ} (h : u ≤ u')
    (s : ℝ≥0) : dom_quantile w H u s ≤ dom_quantile w H u' s := by
  rw [dom_quantile, dom_quantile, dom_quantPath_apply, dom_quantPath_apply]
  refine (Finset.le_fold_min _).mpr ⟨(Finset.fold_min_le _).mpr (Or.inl le_rfl), fun A hA => ?_⟩
  refine (Finset.fold_min_le _).mpr (Or.inr ⟨A, ?_, le_rfl⟩)
  simp only [dom_heavy, Finset.mem_filter, Finset.mem_univ, true_and] at hA ⊢
  exact h.trans hA

/-- If the paths `H i`, `i ∈ B`, are above `S` at time `s`, then so are the quantile paths of
levels `u > W - w(B)`. -/
private lemma dom_quantile_above {w : Fin n → ℝ} (hw : ∀ i, 0 ≤ w i) {H : Fin n → C(ℝ≥0, ℝ)}
    (hH : ∀ i, H i ∈ hiderPaths) {S : C(ℝ≥0, ℝ)} {s : ℝ≥0} {B : Finset (Fin n)}
    (hB : ∀ i ∈ B, S s < H i s) {u : ℝ} (hu : ∑ i, w i - ∑ i ∈ B, w i < u)
    (huW : u ≤ ∑ i, w i) : S s < dom_quantile w H u s := by
  classical
  obtain ⟨i₀, hi₀⟩ : B.Nonempty := by
    rw [Finset.nonempty_iff_ne_empty]
    rintro rfl
    simp only [Finset.sum_empty, sub_zero] at hu
    linarith
  rw [dom_quantile, dom_quantPath_apply, Finset.lt_fold_min]
  refine ⟨(hB i₀ hi₀).trans_le (hH i₀ s).2, fun A hA => ?_⟩
  simp only [dom_heavy, Finset.mem_filter, Finset.mem_univ, true_and] at hA
  obtain ⟨i, hiA, hiB⟩ : ∃ i ∈ A, i ∈ B := by
    by_contra hcon
    have hd : Disjoint A B := Finset.disjoint_left.mpr fun i hiA hiB => hcon ⟨i, hiA, hiB⟩
    have : ∑ i ∈ A, w i + ∑ i ∈ B, w i ≤ ∑ i, w i := by
      rw [← Finset.sum_union hd]
      exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _) fun i _ _ => hw i
    linarith
  rw [dom_maxPath_apply, Finset.lt_fold_max]
  exact Or.inr ⟨i, hiA, hB i hiB⟩

/-- If the paths `H i`, `i ∈ B`, are below `S` at time `s`, then so are the quantile paths of
levels `0 < u ≤ w(B)`. -/
private lemma dom_quantile_below {w : Fin n → ℝ} {H : Fin n → C(ℝ≥0, ℝ)}
    (hH : ∀ i, H i ∈ hiderPaths) {S : C(ℝ≥0, ℝ)} {s : ℝ≥0} {B : Finset (Fin n)}
    (hB : ∀ i ∈ B, H i s < S s) {u : ℝ} (hu0 : 0 < u) (hu : u ≤ ∑ i ∈ B, w i) :
    dom_quantile w H u s < S s := by
  obtain ⟨i₀, hi₀⟩ : B.Nonempty := by
    rw [Finset.nonempty_iff_ne_empty]
    rintro rfl
    simp only [Finset.sum_empty] at hu
    linarith
  rw [dom_quantile, dom_quantPath_apply, Finset.fold_min_lt]
  refine Or.inr ⟨B, by simpa [dom_heavy] using hu, ?_⟩
  rw [dom_maxPath_apply, Finset.fold_max_lt]
  exact ⟨(hH i₀ s).1.trans_lt (hB i₀ hi₀), hB⟩

/-- A path that differs from `S` on `[0, τ]` is caught after `τ`. -/
private lemma dom_lt_captureTime {S H : C(ℝ≥0, ℝ)} {τ : ℝ≥0} (h : ∀ s ≤ τ, S s ≠ H s) :
    (τ : ℝ≥0∞) < captureTime S H := by
  by_contra hle
  rw [not_lt] at hle
  obtain ⟨t, ht, hT⟩ := exists_eq_captureTime (ne_top_of_le_ne_top ENNReal.coe_ne_top hle)
  rw [hT] at hle
  exact h t (ENNReal.coe_le_coe.mp hle) ht

/-- A path caught after `τ` stays on one side of `S` during `[0, τ]`. -/
private lemma dom_sign_of_lt_captureTime {S H : C(ℝ≥0, ℝ)} {τ : ℝ≥0}
    (h : (τ : ℝ≥0∞) < captureTime S H) : (∀ s ≤ τ, S s < H s) ∨ (∀ s ≤ τ, H s < S s) := by
  have hT : ∀ s ≤ τ, ¬ captureTime S H ≤ s := fun s hs hle =>
    absurd (h.trans_le (hle.trans (ENNReal.coe_le_coe.mpr hs))) (lt_irrefl _)
  have h0 : S 0 ≠ H 0 := fun he => hT 0 zero_le (captureTime_le he)
  rcases lt_or_gt_of_ne h0 with h0 | h0
  · left
    intro s hs
    by_contra hc
    exact hT s hs (captureTime_le_of_le_of_le zero_le h0.le (not_lt.mp hc))
  · right
    intro s hs
    by_contra hc
    exact hT s hs (captureTime_le_of_ge_of_ge zero_le h0.le (not_lt.mp hc))

private lemma dom_measurable_lt (z : ℝ≥0∞) :
    Measurable fun t : ℝ => if ENNReal.ofReal t < z then (1 : ℝ≥0∞) else 0 :=
  Measurable.ite (measurableSet_lt ENNReal.measurable_ofReal measurable_const) measurable_const
    measurable_const

/-- The layer-cake formula for one number: `∫₀^∞ 1[t < x] dt = x`. -/
private lemma dom_lintegral_lt (x : ℝ≥0∞) :
    ∫⁻ t in Set.Ioi (0 : ℝ), (if ENNReal.ofReal t < x then 1 else 0) = x := by
  have hm : MeasurableSet {t : ℝ | ENNReal.ofReal t < x} :=
    measurableSet_lt ENNReal.measurable_ofReal measurable_const
  have hind : (fun t : ℝ => if ENNReal.ofReal t < x then (1 : ℝ≥0∞) else 0) =
      {t : ℝ | ENNReal.ofReal t < x}.indicator 1 := by
    ext t
    simp [Set.indicator_apply]
  rw [hind, lintegral_indicator_one hm, Measure.restrict_apply hm]
  rcases eq_or_ne x ⊤ with rfl | hx
  · simp [Real.volume_Ioi]
  · have hset : {t : ℝ | ENNReal.ofReal t < x} ∩ Set.Ioi 0 = Set.Ioo 0 x.toReal := by
      ext t
      simp only [Set.mem_inter_iff, Set.mem_ofPred_eq, Set.mem_Ioi, Set.mem_Ioo]
      constructor
      · rintro ⟨h1, h2⟩
        exact ⟨h2, (ENNReal.ofReal_lt_iff_lt_toReal h2.le hx).mp h1⟩
      · rintro ⟨h1, h2⟩
        exact ⟨(ENNReal.ofReal_lt_iff_lt_toReal h1.le hx).mpr h2, h1⟩
    rw [hset, Real.volume_Ioo, sub_zero, ENNReal.ofReal_toReal hx]

private lemma dom_sum_eq_lintegral {β : Type*} (s : Finset β) (c z : β → ℝ≥0∞) :
    ∑ i ∈ s, c i * z i =
      ∫⁻ t in Set.Ioi (0 : ℝ), ∑ i ∈ s, c i * (if ENNReal.ofReal t < z i then 1 else 0) := by
  rw [lintegral_finsetSum _ fun i _ => (dom_measurable_lt (z i)).const_mul (c i)]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [lintegral_const_mul _ (dom_measurable_lt (z i)), dom_lintegral_lt]

/-- Comparison of weighted sums of times through their survival weights: if at every time `τ`
the weight of the times `x i > τ` is at most the weight of the times `y k > τ`, then
`∑ a i * x i ≤ ∑ b k * y k`. -/
private lemma dom_sum_le_of_survival {ι κ : Type*} (s : Finset ι) (s' : Finset κ)
    (a x : ι → ℝ≥0∞) (b y : κ → ℝ≥0∞)
    (h : ∀ τ : ℝ≥0, ∑ i ∈ s, a i * (if (τ : ℝ≥0∞) < x i then 1 else 0) ≤
      ∑ k ∈ s', b k * (if (τ : ℝ≥0∞) < y k then 1 else 0)) :
    ∑ i ∈ s, a i * x i ≤ ∑ k ∈ s', b k * y k := by
  rw [dom_sum_eq_lintegral s a x, dom_sum_eq_lintegral s' b y]
  exact lintegral_mono fun t => h t.toNNReal

/-- The quantile family of finitely many paths with finite weights: noncrossing paths with the
same total weight that dominate the given mixture against every searcher path. -/
private lemma dom_quantile_family (w : Fin n → ℝ) (hw : ∀ i, 0 ≤ w i) (H : Fin n → C(ℝ≥0, ℝ))
    (hH : ∀ i, H i ∈ hiderPaths) :
    ∃ (m : ℕ) (w' : Fin m → ℝ≥0∞) (H' : Fin m → C(ℝ≥0, ℝ)),
      (∀ k, H' k ∈ hiderPaths) ∧ (∀ k l, Noncrossing (H' k) (H' l)) ∧
      ∑ k, w' k = ∑ i, ENNReal.ofReal (w i) ∧
      ∀ S : C(ℝ≥0, ℝ), ∑ i, ENNReal.ofReal (w i) * captureTime S (H i) ≤
        ∑ k, w' k * captureTime S (H' k) := by
  classical
  set W := ∑ i, w i with hW
  set g : ℝ → Finset (Finset (Fin n)) := dom_heavy w with hg
  set μ : Measure ℝ := volume.restrict (Set.Ioc 0 W) with hμ
  -- the new paths are indexed by the possible families `g u` of heavy sets; each carries the
  -- Lebesgue measure of the levels `u ∈ (0, W]` that produce it
  let rep : Finset (Finset (Fin n)) → ℝ := fun 𝒜 => Classical.epsilon fun u => g u = 𝒜
  have hrep : ∀ u, g (rep (g u)) = g u := fun u =>
    Classical.epsilon_spec (p := fun u' => g u' = g u) ⟨u, rfl⟩
  let P : Finset (Finset (Fin n)) → C(ℝ≥0, ℝ) := fun 𝒜 => dom_quantile w H (rep 𝒜)
  have hP : ∀ u, P (g u) = dom_quantile w H u := fun u => by
    simp only [P, dom_quantile]
    rw [← hg, hrep]
  let d : Finset (Finset (Fin n)) → ℝ≥0∞ := fun 𝒜 => μ (g ⁻¹' {𝒜})
  have hmeas : ∀ 𝒜, MeasurableSet (g ⁻¹' {𝒜}) := by
    intro 𝒜
    have : g ⁻¹' {𝒜} = ⋂ A : Finset (Fin n), {u | u ≤ ∑ i ∈ A, w i ↔ A ∈ 𝒜} := by
      ext u
      simp only [Set.mem_preimage, Set.mem_singleton_iff, Set.mem_iInter, Set.mem_ofPred_eq, hg,
        dom_heavy, Finset.ext_iff, Finset.mem_filter, Finset.mem_univ, true_and]
    rw [this]
    refine MeasurableSet.iInter fun A => ?_
    by_cases hA : A ∈ 𝒜
    · simp only [hA, iff_true]
      exact measurableSet_Iic
    · simp only [hA, iff_false, not_le]
      exact measurableSet_Ioi
  let e := Fintype.equivFin (Finset (Finset (Fin n)))
  refine ⟨Fintype.card (Finset (Finset (Fin n))), fun k => d (e.symm k), fun k => P (e.symm k),
    fun k => dom_quantile_mem _ _ _, fun k l => ?_, ?_, fun S => ?_⟩
  · rcases le_total (rep (e.symm k)) (rep (e.symm l)) with h | h
    · exact Or.inl (dom_quantile_mono w H h)
    · exact Or.inr (dom_quantile_mono w H h)
  · rw [Equiv.sum_comp e.symm d]
    simp only [d]
    rw [sum_measure_preimage_singleton _ fun 𝒜 _ => hmeas 𝒜, Finset.coe_univ, Set.preimage_univ,
      hμ, Measure.restrict_apply_univ, Real.volume_Ioc, sub_zero, hW,
      ENNReal.ofReal_sum_of_nonneg fun i _ => hw i]
  · rw [Equiv.sum_comp e.symm (fun 𝒜 => d 𝒜 * captureTime S (P 𝒜))]
    refine dom_sum_le_of_survival _ _ _ _ _ _ fun τ => ?_
    -- the paths not met by time `τ`: those above `S` and those below `S` on `[0, τ]`
    set Ap := Finset.univ.filter fun i => ∀ s ≤ τ, S s < H i s with hAp
    set Am := Finset.univ.filter fun i => ∀ s ≤ τ, H i s < S s with hAm
    have hdisj : Disjoint Ap Am := by
      rw [hAp, hAm, Finset.disjoint_filter]
      intro i _ h1 h2
      exact lt_asymm (h1 0 zero_le) (h2 0 zero_le)
    have hsum : ∑ i ∈ Ap, w i + ∑ i ∈ Am, w i ≤ W := by
      rw [← Finset.sum_union hdisj]
      exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _) fun i _ _ => hw i
    have hp0 : 0 ≤ ∑ i ∈ Ap, w i := Finset.sum_nonneg fun i _ => hw i
    have hm0 : 0 ≤ ∑ i ∈ Am, w i := Finset.sum_nonneg fun i _ => hw i
    -- the levels whose quantile paths are not met by time `τ`
    set Y := Set.Ioc 0 (∑ i ∈ Am, w i) ∪ Set.Ioc (W - ∑ i ∈ Ap, w i) W with hY
    have hYsub : Y ⊆ Set.Ioc 0 W := by
      refine Set.union_subset (Set.Ioc_subset_Ioc_right (by linarith))
        (Set.Ioc_subset_Ioc_left (by linarith))
    have hYsurv : ∀ u ∈ Y, (τ : ℝ≥0∞) < captureTime S (dom_quantile w H u) := by
      rintro u (⟨hu0, hu⟩ | ⟨hu1, hu2⟩)
      · refine dom_lt_captureTime fun s hs => (dom_quantile_below hH ?_ hu0 hu).ne'
        intro i hi
        exact (Finset.mem_filter.mp hi).2 s hs
      · refine dom_lt_captureTime fun s hs => (dom_quantile_above hw hH ?_ hu1 hu2).ne
        intro i hi
        exact (Finset.mem_filter.mp hi).2 s hs
    calc ∑ i, ENNReal.ofReal (w i) * (if (τ : ℝ≥0∞) < captureTime S (H i) then 1 else 0)
        = ∑ i ∈ Finset.univ.filter fun i => (τ : ℝ≥0∞) < captureTime S (H i),
            ENNReal.ofReal (w i) := by
          rw [Finset.sum_filter]
          refine Finset.sum_congr rfl fun i _ => ?_
          split_ifs <;> simp
      _ ≤ ∑ i ∈ Ap ∪ Am, ENNReal.ofReal (w i) := by
          refine Finset.sum_le_sum_of_subset fun i hi => ?_
          rcases dom_sign_of_lt_captureTime (Finset.mem_filter.mp hi).2 with h | h
          · exact Finset.mem_union_left _ (Finset.mem_filter.mpr ⟨Finset.mem_univ _, h⟩)
          · exact Finset.mem_union_right _ (Finset.mem_filter.mpr ⟨Finset.mem_univ _, h⟩)
      _ = μ Y := by
          rw [Finset.sum_union hdisj, ← ENNReal.ofReal_sum_of_nonneg fun i _ => hw i,
            ← ENNReal.ofReal_sum_of_nonneg fun i _ => hw i, hμ,
            Measure.restrict_apply' measurableSet_Ioc, Set.inter_eq_left.mpr hYsub, hY,
            measure_union (Set.Ioc_disjoint_Ioc_of_le (by linarith)) measurableSet_Ioc,
            Real.volume_Ioc, Real.volume_Ioc, sub_zero, sub_sub_cancel, add_comm]
      _ ≤ μ (⋃ 𝒜 ∈ Finset.univ.filter fun 𝒜 => (τ : ℝ≥0∞) < captureTime S (P 𝒜), g ⁻¹' {𝒜}) := by
          refine measure_mono fun u hu => ?_
          simp only [Set.mem_iUnion, Set.mem_preimage, Set.mem_singleton_iff, Finset.mem_filter,
            Finset.mem_univ, true_and, exists_prop]
          exact ⟨g u, by rw [hP]; exact hYsurv u hu, rfl⟩
      _ ≤ ∑ 𝒜 ∈ Finset.univ.filter fun 𝒜 => (τ : ℝ≥0∞) < captureTime S (P 𝒜), d 𝒜 :=
          measure_biUnion_finset_le _ _
      _ = ∑ 𝒜, d 𝒜 * (if (τ : ℝ≥0∞) < captureTime S (P 𝒜) then 1 else 0) := by
          rw [Finset.sum_filter]
          refine Finset.sum_congr rfl fun 𝒜 _ => ?_
          split_ifs <;> simp

end Quantile

/-- **Proposition 7** (`prop:7`), its consequence: every finite mixed hider strategy (pure
strategies `H i` with weights `w i`) is dominated by a finite mixed strategy of the same total
weight whose pure strategies are pairwise noncrossing.

The paper states this ("consequently") without an argument; the argument here is the
formalization's. The new strategy mixes the quantile paths `Q_u = min_{w(A) ≥ u} max_{i ∈ A} H i`
(`0 < u ≤ W`, `W` the total weight), each with the Lebesgue measure of the levels `u` that produce
it; they are noncrossing because `Q_u` increases with `u`. Domination compares survival weights:
the paths not caught by time `τ` lie above or below the searcher on `[0, τ]`; if those above
carry weight `a` and those below weight `b`, the quantile paths of levels in `(W - a, W]` and in
`(0, b]` are not caught by time `τ` either; integrating over `τ` gives the inequality. An infinite
weight is handled by giving every quantile path of the equally weighted family infinite weight.
(For equal weights, repeated use of `proposition7` along a sorting network would also do.) -/
theorem proposition7_finite {n : ℕ} (w : Fin n → ℝ≥0∞) (H : Fin n → C(ℝ≥0, ℝ))
    (hH : ∀ i, H i ∈ hiderPaths) :
    ∃ (m : ℕ) (w' : Fin m → ℝ≥0∞) (H' : Fin m → C(ℝ≥0, ℝ)),
      (∀ k, H' k ∈ hiderPaths) ∧ (∀ k l, Noncrossing (H' k) (H' l)) ∧
      ∑ k, w' k = ∑ i, w i ∧
      ∀ S ∈ searcherPaths, ∑ i, w i * captureTime S (H i) ≤ ∑ k, w' k * captureTime S (H' k) := by
  by_cases htop : ∃ i, w i = ⊤
  · -- an infinite weight: the quantile paths of equal weights, each with infinite weight
    obtain ⟨i₀, hi₀⟩ := htop
    obtain ⟨m, d, Q, hQ, hnc, hsum, hdom⟩ :=
      dom_quantile_family (fun _ => (1 : ℝ)) (fun _ => zero_le_one) H hH
    refine ⟨m, fun k => ⊤ * d k, Q, hQ, hnc, ?_, fun S _ => ?_⟩
    · rw [← Finset.mul_sum, hsum, ENNReal.sum_eq_top.mpr ⟨i₀, Finset.mem_univ _, hi₀⟩]
      refine ENNReal.top_mul ?_
      have h1 : (1 : ℝ≥0∞) ≤ ∑ _i : Fin n, ENNReal.ofReal 1 := by
        rw [ENNReal.ofReal_one]
        exact Finset.single_le_sum (f := fun _ => (1 : ℝ≥0∞)) (fun _ _ => zero_le)
          (Finset.mem_univ i₀)
      exact (one_pos.trans_le h1).ne'
    · calc ∑ i, w i * captureTime S (H i)
          ≤ ∑ i, ⊤ * (ENNReal.ofReal 1 * captureTime S (H i)) :=
            Finset.sum_le_sum fun i _ => by
              rw [ENNReal.ofReal_one, one_mul]
              exact mul_le_mul_left le_top _
        _ = ⊤ * ∑ i, ENNReal.ofReal 1 * captureTime S (H i) := (Finset.mul_sum _ _ _).symm
        _ ≤ ⊤ * ∑ k, d k * captureTime S (Q k) := mul_le_mul_right (hdom S) _
        _ = ∑ k, ⊤ * d k * captureTime S (Q k) := by
            rw [Finset.mul_sum]
            simp only [mul_assoc]
  · -- finite weights: the quantile paths
    simp only [not_exists] at htop
    obtain ⟨m, d, Q, hQ, hnc, hsum, hdom⟩ :=
      dom_quantile_family (fun i => (w i).toReal) (fun _ => ENNReal.toReal_nonneg) H hH
    have hw : ∀ i, ENNReal.ofReal (w i).toReal = w i := fun i => ENNReal.ofReal_toReal (htop i)
    simp only [hw] at hsum hdom
    exact ⟨m, d, Q, hQ, hnc, hsum, fun S _ => hdom S⟩

/-- **Proposition 8** (`prop:8`). In a symmetric hider strategy whose pure strategies (its
support `P`) are pairwise nonintersecting, each pure strategy is contained in half of the
interval. -/
theorem proposition8 (P : Finset C(ℝ≥0, ℝ)) (hP : ∀ H ∈ P, H ∈ hiderPaths)
    (hsymm : ∀ H ∈ P, -H ∈ P)
    (hni : ∀ H₁ ∈ P, ∀ H₂ ∈ P, H₁ ≠ H₂ → Nonintersecting H₁ H₂) :
    ∀ H ∈ P, (∀ t, H t ∈ Set.Icc (-1 : ℝ) 0) ∨ (∀ t, H t ∈ Set.Icc (0 : ℝ) 1) := by
  intro H hH
  have hI := hP H hH
  by_cases hz : ∃ t, H t = 0
  · -- `H` and `-H` meet at a zero of `H`, so they are equal, and `H` stays at `0`
    obtain ⟨t₀, ht₀⟩ := hz
    have hHH : H = -H := by
      by_contra hne
      rcases hni H hH (-H) (hsymm H hH) hne with h | h
      · have := h t₀
        simp [ht₀] at this
      · have := h t₀
        simp [ht₀] at this
    left
    intro t
    have h1 : H t = -H t := by
      conv_lhs => rw [hHH]
      rfl
    have h0 : H t = 0 := by linarith
    simp [h0]
  · -- `H` never vanishes, so by the intermediate value theorem it keeps the sign of `H 0`
    simp only [not_exists] at hz
    rcases lt_or_gt_of_ne (hz 0) with h0 | h0
    · left
      intro t
      refine ⟨(hI t).1, ?_⟩
      by_contra hpos
      replace hpos := lt_of_not_ge hpos
      obtain ⟨s, -, hs⟩ := intermediate_value_Icc (zero_le : (0 : ℝ≥0) ≤ t)
        H.continuous.continuousOn (show (0 : ℝ) ∈ Set.Icc (H 0) (H t) from ⟨h0.le, hpos.le⟩)
      exact hz s hs
    · right
      intro t
      refine ⟨?_, (hI t).2⟩
      by_contra hneg
      replace hneg := lt_of_not_ge hneg
      obtain ⟨s, -, hs⟩ := intermediate_value_Icc' (zero_le : (0 : ℝ≥0) ≤ t)
        H.continuous.continuousOn (show (0 : ℝ) ∈ Set.Icc (H t) (H 0) from ⟨hneg.le, h0.le⟩)
      exact hz s hs

end PrincessMonster
