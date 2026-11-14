module

public import PrincessMonster.CaptureTime
public import Mathlib.Order.ConditionallyCompleteLattice.Basic
public import Mathlib.Topology.Order.Basic
public import Mathlib.Topology.Piecewise
public import Mathlib.Data.Fin.Tuple.Sort

/-!
# Section 2: the searcher's response to a finite hider strategy (Proposition 5)

Against hider paths `H₁, …, H_J` of speed at most `1`, the searcher may restrict himself to the
*greedy* paths: for an order `σ` of the hiders, start where the first one starts, and as soon
as one has been met, run at unit speed towards the next.

* `chase a p X`: from position `p` at time `a`, run at unit speed towards `X` and follow it once
  it is reached (`min (p + (t - a)) (X t)` if `X` is above, `max (p - (t - a)) (X t)` if below).
* `chaseTime a p X`: the time at which the chase reaches `X`.
* `greedyFrom a p L`: chase the paths of the list `L` in turn, starting from `(a, p)`.
* `greedyPath L`: the greedy path for the list `L`, starting where its first path starts.
* `proposition5`: every searcher path is dominated, against the `H_j`, by a greedy path.
-/

@[expose] public section

open scoped NNReal ENNReal

namespace PrincessMonster

/-- From position `p` at time `a`, run at unit speed towards the path `X`, and follow `X` from
the moment it is reached. -/
noncomputable def chase (a : ℝ≥0) (p : ℝ) (X : C(ℝ≥0, ℝ)) : C(ℝ≥0, ℝ) :=
  if p ≤ X a then ⟨fun t => min (p + ((t : ℝ) - a)) (X t), by fun_prop⟩
  else ⟨fun t => max (p - ((t : ℝ) - a)) (X t), by fun_prop⟩

/-- The first time, not before `a`, at which the chase from `(a, p)` reaches `X`. -/
noncomputable def chaseTime (a : ℝ≥0) (p : ℝ) (X : C(ℝ≥0, ℝ)) : ℝ≥0 :=
  sInf {t | a ≤ t ∧ chase a p X t = X t}

/-- The path equal to `f` up to time `m` and to `g`, shifted to start from `f m`, after `m`. -/
noncomputable def glue (m : ℝ≥0) (f g : C(ℝ≥0, ℝ)) : C(ℝ≥0, ℝ) :=
  ⟨fun t => if t ≤ m then f t else g t - g m + f m, by
    refine Continuous.if_le f.continuous (by fun_prop) continuous_id continuous_const ?_
    intro t ht
    simp [ht]⟩

/-- Starting from position `p` at time `a`, chase the paths of the list in turn. After the
last one, stay put. -/
noncomputable def greedyFrom : ℝ≥0 → ℝ → List C(ℝ≥0, ℝ) → C(ℝ≥0, ℝ)
  | _, p, [] => ContinuousMap.const _ p
  | a, p, X :: rest =>
    glue (chaseTime a p X) (chase a p X) (greedyFrom (chaseTime a p X) (X (chaseTime a p X)) rest)

/-- The greedy path for a list of hider paths: start where the first one starts, and as soon as
a path of the list has been met, run towards the next. -/
noncomputable def greedyPath : List C(ℝ≥0, ℝ) → C(ℝ≥0, ℝ)
  | [] => ContinuousMap.const _ 0
  | X :: rest => greedyFrom 0 (X 0) (X :: rest)

/-- The greedy path that visits the paths `H j` in the order `σ`. -/
noncomputable def greedyOrder {J : ℕ} (H : Fin J → C(ℝ≥0, ℝ)) (σ : Equiv.Perm (Fin J)) :
    C(ℝ≥0, ℝ) :=
  greedyPath (List.ofFn fun j => H (σ j))

/-! ### Elementary facts about the chase and the greedy paths -/

lemma greedy_glue_apply (m : ℝ≥0) (f g : C(ℝ≥0, ℝ)) (t : ℝ≥0) :
    glue m f g t = if t ≤ m then f t else g t - g m + f m := rfl

lemma greedy_chase_apply (a : ℝ≥0) (p : ℝ) (X : C(ℝ≥0, ℝ)) (t : ℝ≥0) :
    chase a p X t = if p ≤ X a then min (p + ((t : ℝ) - a)) (X t)
      else max (p - ((t : ℝ) - a)) (X t) := by
  unfold chase
  split_ifs <;> rfl

/-- The chase from `(a, p)` is at `p` at time `a`. -/
lemma greedy_chase_self (a : ℝ≥0) (p : ℝ) (X : C(ℝ≥0, ℝ)) : chase a p X a = p := by
  rw [greedy_chase_apply]
  split_ifs with h
  · rw [sub_self, add_zero, min_eq_left h]
  · rw [sub_self, sub_zero, max_eq_left (le_of_lt (not_le.mp h))]

/-- The chase from `(a, p)` is at `X` at time `t` if `X t` can be reached from `(a, p)` by
time `t` at unit speed. -/
lemma greedy_chase_eq_of_abs_le {a t : ℝ≥0} {p : ℝ} {X : C(ℝ≥0, ℝ)}
    (h : |p - X t| ≤ (t : ℝ) - a) : chase a p X t = X t := by
  rw [greedy_chase_apply]
  have h1 := (abs_le.mp h).1
  have h2 := (abs_le.mp h).2
  split_ifs
  · exact min_eq_right (by linarith)
  · exact max_eq_right (by linarith)

lemma greedy_chaseSet_isClosed (a : ℝ≥0) (p : ℝ) (X : C(ℝ≥0, ℝ)) :
    IsClosed {t | a ≤ t ∧ chase a p X t = X t} :=
  (isClosed_le continuous_const continuous_id).inter
    (isClosed_eq (chase a p X).continuous X.continuous)

lemma greedy_chaseTime_le {a t : ℝ≥0} {p : ℝ} {X : C(ℝ≥0, ℝ)} (hat : a ≤ t)
    (h : chase a p X t = X t) : chaseTime a p X ≤ t :=
  csInf_le (OrderBot.bddBelow _) ⟨hat, h⟩

/-- `chaseTime` is the first meeting time: when `p` and the values of `X` lie in `[-1, 1]`, the
chase reaches `X` by time `a + 2`, and `chaseTime a p X` is a time `≥ a` at which the chase is
at `X`. -/
lemma greedy_chaseTime_spec {a : ℝ≥0} {p : ℝ} (hp : p ∈ I) {X : C(ℝ≥0, ℝ)}
    (hX : X ∈ hiderPaths) :
    a ≤ chaseTime a p X ∧ chase a p X (chaseTime a p X) = X (chaseTime a p X) := by
  have hne : {t | a ≤ t ∧ chase a p X t = X t}.Nonempty := by
    refine ⟨a + 2, le_self_add, greedy_chase_eq_of_abs_le ?_⟩
    have hXt := hX (a + 2)
    have hp1 := hp.1
    have hp2 := hp.2
    have h1 := hXt.1
    have h2 := hXt.2
    push_cast
    rw [abs_le]
    constructor <;> linarith
  exact (greedy_chaseSet_isClosed a p X).csInf_mem hne (OrderBot.bddBelow _)

/-- From time `a` on, the chase stays in `[-1, 1]`. -/
lemma greedy_chase_mem {a t : ℝ≥0} {p : ℝ} (hp : p ∈ I) {X : C(ℝ≥0, ℝ)}
    (hX : X ∈ hiderPaths) (ht : a ≤ t) : chase a p X t ∈ I := by
  have hX' := hX t
  have hta : (a : ℝ) ≤ t := NNReal.coe_le_coe.mpr ht
  have hp1 := hp.1
  have hp2 := hp.2
  rw [greedy_chase_apply]
  split_ifs
  · exact ⟨le_min (by linarith) hX'.1, (min_le_right _ _).trans hX'.2⟩
  · exact ⟨hX'.1.trans (le_max_right _ _), max_le (by linarith) hX'.2⟩

/-- The chase of a path of speed at most `1` has speed at most `1`. -/
lemma greedy_chase_lip (a : ℝ≥0) (p : ℝ) {X : C(ℝ≥0, ℝ)} (hX : X ∈ searcherPaths)
    (s t : ℝ≥0) : |chase a p X s - chase a p X t| ≤ |(s : ℝ) - t| := by
  rw [greedy_chase_apply, greedy_chase_apply]
  have hXst := hX.2 s t
  split_ifs
  · refine (abs_min_sub_min_le_max _ _ _ _).trans (max_le (le_of_eq ?_) hXst)
    rw [show p + ((s : ℝ) - a) - (p + ((t : ℝ) - a)) = (s : ℝ) - t by ring]
  · refine (abs_max_sub_max_le_max _ _ _ _).trans (max_le (le_of_eq ?_) hXst)
    rw [show p - ((s : ℝ) - a) - (p - ((t : ℝ) - a)) = (t : ℝ) - s by ring, abs_sub_comm]

/-- A function of speed at most `1` on `[a, c]` and on `[c, ∞)` has speed at most `1` on
`[a, ∞)`. -/
lemma greedy_lip_of_split {f : ℝ≥0 → ℝ} {a c : ℝ≥0}
    (h1 : ∀ s t, a ≤ s → s ≤ c → a ≤ t → t ≤ c → |f s - f t| ≤ |(s : ℝ) - t|)
    (h2 : ∀ s t, c ≤ s → c ≤ t → |f s - f t| ≤ |(s : ℝ) - t|) (hac : a ≤ c) :
    ∀ s t, a ≤ s → a ≤ t → |f s - f t| ≤ |(s : ℝ) - t| := by
  have key : ∀ s t, a ≤ s → s ≤ c → c ≤ t → |f s - f t| ≤ |(s : ℝ) - t| := by
    intro s t has hsc hct
    have hsc' : (s : ℝ) ≤ c := NNReal.coe_le_coe.mpr hsc
    have hct' : (c : ℝ) ≤ t := NNReal.coe_le_coe.mpr hct
    calc |f s - f t| ≤ |f s - f c| + |f c - f t| := abs_sub_le _ _ _
      _ ≤ |(s : ℝ) - c| + |(c : ℝ) - t| :=
          add_le_add (h1 s c has hsc hac le_rfl) (h2 c t le_rfl hct)
      _ = |(s : ℝ) - t| := by
        rw [abs_of_nonpos (show (s : ℝ) - c ≤ 0 by linarith),
          abs_of_nonpos (show (c : ℝ) - t ≤ 0 by linarith),
          abs_of_nonpos (show (s : ℝ) - t ≤ 0 by linarith)]
        ring
  intro s t has hat
  rcases le_total s c with hsc | hcs <;> rcases le_total t c with htc | hct
  · exact h1 s t has hsc hat htc
  · exact key s t has hsc hct
  · rw [abs_sub_comm, abs_sub_comm (s : ℝ)]
    exact key t s hat htc hcs
  · exact h2 s t hcs hct

lemma greedy_greedyFrom_cons (a : ℝ≥0) (p : ℝ) (X : C(ℝ≥0, ℝ)) (rest : List C(ℝ≥0, ℝ)) :
    greedyFrom a p (X :: rest) = glue (chaseTime a p X) (chase a p X)
      (greedyFrom (chaseTime a p X) (X (chaseTime a p X)) rest) := by
  rw [greedyFrom]

/-- `greedyFrom a p L` is at `p` at time `a`. -/
lemma greedy_greedyFrom_self {a : ℝ≥0} {p : ℝ} (hp : p ∈ I) :
    ∀ {L : List C(ℝ≥0, ℝ)}, (∀ X ∈ L, X ∈ hiderPaths) → greedyFrom a p L a = p
  | [], _ => rfl
  | X :: _, hL => by
    obtain ⟨hac, -⟩ := greedy_chaseTime_spec (a := a) hp (hL X List.mem_cons_self)
    rw [greedy_greedyFrom_cons, greedy_glue_apply, ite_eq_left hac, greedy_chase_self]

/-- After the first chase time, `greedyFrom a p (X :: rest)` is the greedy path for `rest` from
the point where `X` was met (the shift in `glue` vanishes). -/
lemma greedy_greedyFrom_cons_of_le {a : ℝ≥0} {p : ℝ} (hp : p ∈ I) {X : C(ℝ≥0, ℝ)}
    {rest : List C(ℝ≥0, ℝ)} (hX : X ∈ hiderPaths) (hrest : ∀ Y ∈ rest, Y ∈ hiderPaths)
    {t : ℝ≥0} (ht : chaseTime a p X ≤ t) :
    greedyFrom a p (X :: rest) t = greedyFrom (chaseTime a p X) (X (chaseTime a p X)) rest t := by
  obtain ⟨-, hmeet⟩ := greedy_chaseTime_spec (a := a) hp hX
  have hself := greedy_greedyFrom_self (a := chaseTime a p X) (hX (chaseTime a p X)) hrest
  rw [greedy_greedyFrom_cons, greedy_glue_apply]
  split_ifs with h
  · rw [le_antisymm h ht, hmeet, hself]
  · rw [hself, hmeet, sub_add_cancel]

/-- From time `a` on, `greedyFrom a p L` has speed at most `1` and values in `[-1, 1]`. -/
lemma greedy_greedyFrom_spec :
    ∀ (L : List C(ℝ≥0, ℝ)), (∀ X ∈ L, X ∈ searcherPaths) → ∀ (a : ℝ≥0) (p : ℝ), p ∈ I →
      (∀ t, a ≤ t → greedyFrom a p L t ∈ I) ∧
      (∀ s t, a ≤ s → a ≤ t → |greedyFrom a p L s - greedyFrom a p L t| ≤ |(s : ℝ) - t|)
  | [], _, _, p, hp => ⟨fun _ _ => hp, fun s t _ _ => by
      change |p - p| ≤ _
      rw [sub_self, abs_zero]
      exact abs_nonneg _⟩
  | X :: rest, hL, a, p, hp => by
    have hX := hL X List.mem_cons_self
    have hrest : ∀ Y ∈ rest, Y ∈ searcherPaths := fun Y hY => hL Y (List.mem_cons_of_mem _ hY)
    obtain ⟨hac, -⟩ := greedy_chaseTime_spec (a := a) hp hX.1
    obtain ⟨ih1, ih2⟩ :=
      greedy_greedyFrom_spec rest hrest (chaseTime a p X) (X (chaseTime a p X)) (hX.1 _)
    have hlow : ∀ t, t ≤ chaseTime a p X → greedyFrom a p (X :: rest) t = chase a p X t := by
      intro t ht
      rw [greedy_greedyFrom_cons, greedy_glue_apply, ite_eq_left ht]
    have hhigh : ∀ t, chaseTime a p X ≤ t →
        greedyFrom a p (X :: rest) t =
          greedyFrom (chaseTime a p X) (X (chaseTime a p X)) rest t :=
      fun t ht => greedy_greedyFrom_cons_of_le hp hX.1 (fun Y hY => (hrest Y hY).1) ht
    refine ⟨fun t hat => ?_, greedy_lip_of_split ?_ ?_ hac⟩
    · rcases le_total t (chaseTime a p X) with htc | hct
      · rw [hlow t htc]
        exact greedy_chase_mem hp hX.1 hat
      · rw [hhigh t hct]
        exact ih1 t hct
    · intro s t _ hsc _ htc
      rw [hlow s hsc, hlow t htc]
      exact greedy_chase_lip a p hX s t
    · intro s t hcs hct
      rw [hhigh s hcs, hhigh t hct]
      exact ih2 s t hcs hct

/-- The greedy path for a list of searcher paths is a searcher path. -/
lemma greedy_greedyPath_mem :
    ∀ {L : List C(ℝ≥0, ℝ)}, (∀ X ∈ L, X ∈ searcherPaths) → greedyPath L ∈ searcherPaths
  | [], _ => ⟨fun _ => show (0 : ℝ) ∈ I by norm_num, fun s t => by
      change |(0 : ℝ) - 0| ≤ _
      rw [sub_self, abs_zero]
      exact abs_nonneg _⟩
  | X :: rest, hL => by
    obtain ⟨h1, h2⟩ :=
      greedy_greedyFrom_spec (X :: rest) hL 0 (X 0) ((hL X List.mem_cons_self).1 0)
    exact ⟨fun t => h1 t zero_le, fun s t => h2 s t zero_le zero_le⟩

lemma greedyOrder_mem {J : ℕ} {H : Fin J → C(ℝ≥0, ℝ)} (hH : ∀ j, H j ∈ searcherPaths)
    (σ : Equiv.Perm (Fin J)) : greedyOrder H σ ∈ searcherPaths :=
  greedy_greedyPath_mem fun X hX => by
    obtain ⟨j, rfl⟩ := (List.mem_ofFn' _ _).mp hX
    exact hH _

/-! ### The proof of Proposition 5 -/

/-- **The chase is fastest** (proof of Proposition 5). Suppose the searcher `S` meets `X₀` at
time `t₀` and `X₁` at a later time `t₁`. Starting at time `g ≤ t₀` from the position `X₀ g` of
`X₀`, the chase of `X₁` meets `X₁` by time `t₁`. Indeed, the path equal to `X₀` on `[g, t₀]`
and to `S` on `[t₀, t₁]` has speed at most `1` and joins `(g, X₀ g)` to `(t₁, X₁ t₁)`, so
`|X₀ g - X₁ t₁| ≤ t₁ - g`, and the unit-speed run from `X₀ g` cannot have passed `X₁` at
time `t₁`. -/
lemma greedy_chase_fastest {S X₀ X₁ : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths)
    (hX₀ : X₀ ∈ searcherPaths) {g t₀ t₁ : ℝ≥0} (hg : g ≤ t₀) (h01 : t₀ ≤ t₁)
    (h₀ : S t₀ = X₀ t₀) (h₁ : S t₁ = X₁ t₁) :
    chase g (X₀ g) X₁ t₁ = X₁ t₁ ∧ chaseTime g (X₀ g) X₁ ≤ t₁ := by
  have hg' : (g : ℝ) ≤ t₀ := NNReal.coe_le_coe.mpr hg
  have h01' : (t₀ : ℝ) ≤ t₁ := NNReal.coe_le_coe.mpr h01
  have hlip : |X₀ g - X₁ t₁| ≤ (t₁ : ℝ) - g := by
    calc |X₀ g - X₁ t₁| = |(X₀ g - X₀ t₀) + (S t₀ - S t₁)| := by
          rw [h₀, h₁, sub_add_sub_cancel]
      _ ≤ |X₀ g - X₀ t₀| + |S t₀ - S t₁| := abs_add_le _ _
      _ ≤ |(g : ℝ) - t₀| + |(t₀ : ℝ) - t₁| := add_le_add (hX₀.2 g t₀) (hS.2 t₀ t₁)
      _ = (t₁ : ℝ) - g := by
          rw [abs_of_nonpos (show (g : ℝ) - t₀ ≤ 0 by linarith),
            abs_of_nonpos (show (t₀ : ℝ) - t₁ ≤ 0 by linarith)]
          ring
  have hmeet := greedy_chase_eq_of_abs_le hlip
  exact ⟨hmeet, greedy_chaseTime_le (hg.trans h01) hmeet⟩

/-- The induction along the list in the proof of Proposition 5. The searcher `S` meets the
paths of `L` in the order of the list, the first of them not before time `t₀`, and at time
`t₀` it meets `X₀`. Then the greedy path for `L` from `(a, X₀ a)`, `a ≤ t₀`, meets every path
of `L` that `S` meets, not later than `S` does. -/
lemma greedy_greedyFrom_meets {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    ∀ (L : List C(ℝ≥0, ℝ)), (∀ X ∈ L, X ∈ searcherPaths) →
      L.Pairwise (fun X Y => captureTime S X ≤ captureTime S Y) →
      ∀ (X₀ : C(ℝ≥0, ℝ)), X₀ ∈ searcherPaths → ∀ (a t₀ : ℝ≥0), a ≤ t₀ → S t₀ = X₀ t₀ →
      (∀ X ∈ L, (t₀ : ℝ≥0∞) ≤ captureTime S X) →
      ∀ Y ∈ L, ∀ t₁ : ℝ≥0, S t₁ = Y t₁ → captureTime S Y = t₁ →
        ∃ t, a ≤ t ∧ t ≤ t₁ ∧ greedyFrom a (X₀ a) L t = Y t
  | [], _, _, _, _, _, _, _, _, _, _, hY, _, _, _ => absurd hY List.not_mem_nil
  | X :: rest, hL, hsort, X₀, hX₀, a, t₀, ha, h₀, hle, Y, hY, t₁, _, hT₁ => by
    have hX := hL X List.mem_cons_self
    have hrest : ∀ Z ∈ rest, Z ∈ searcherPaths := fun Z hZ => hL Z (List.mem_cons_of_mem _ hZ)
    rw [List.pairwise_cons] at hsort
    -- `S` meets `X`, at time `τ`, and not after `Y`
    have hXY : captureTime S X ≤ t₁ := by
      rcases List.mem_cons.mp hY with hYX | hY'
      · rw [← hT₁, hYX]
      · rw [← hT₁]
        exact hsort.1 Y hY'
    obtain ⟨τ, hτ, hTτ⟩ := exists_eq_captureTime (ne_top_of_le_ne_top ENNReal.coe_ne_top hXY)
    have hτ1 : τ ≤ t₁ := by
      rw [hTτ] at hXY
      exact ENNReal.coe_le_coe.mp hXY
    have h0τ : t₀ ≤ τ := by
      have := hle X List.mem_cons_self
      rw [hTτ] at this
      exact ENNReal.coe_le_coe.mp this
    -- the chase of `X` meets it by time `τ`
    obtain ⟨-, hcτ⟩ := greedy_chase_fastest hS hX₀ ha h0τ h₀ hτ
    have hp := hX₀.1 a
    obtain ⟨hac, hcm⟩ := greedy_chaseTime_spec (a := a) hp hX.1
    rcases List.mem_cons.mp hY with hYX | hY'
    · -- `Y = X`: the greedy path is at `X` when the chase ends
      rw [hYX]
      refine ⟨chaseTime a (X₀ a) X, hac, hcτ.trans hτ1, ?_⟩
      rw [greedy_greedyFrom_cons, greedy_glue_apply, ite_eq_left le_rfl, hcm]
    · -- `Y` in `rest`: from the meeting with `X` on, the greedy path runs towards the next one
      obtain ⟨t, hct, ht1, hmt⟩ := greedy_greedyFrom_meets hS rest hrest hsort.2 X hX
        (chaseTime a (X₀ a) X) τ hcτ hτ
        (fun Z hZ => by rw [← hTτ]; exact hsort.1 Z hZ) Y hY' t₁ ‹_› hT₁
      refine ⟨t, hac.trans hct, ht1, ?_⟩
      rw [greedy_greedyFrom_cons_of_le hp hX.1 (fun Z hZ => (hrest Z hZ).1) hct]
      exact hmt

/-- The greedy path for a list of searcher paths, ordered by the times at which `S` meets them,
meets each of them no later than `S`. -/
lemma greedy_greedyPath_le {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) {L : List C(ℝ≥0, ℝ)}
    (hL : ∀ X ∈ L, X ∈ searcherPaths)
    (hsort : L.Pairwise (fun X Y => captureTime S X ≤ captureTime S Y)) :
    ∀ Y ∈ L, captureTime (greedyPath L) Y ≤ captureTime S Y := by
  intro Y hY
  cases L with
  | nil => exact absurd hY List.not_mem_nil
  | cons X rest =>
    by_cases hTop : captureTime S Y = ⊤
    · rw [hTop]
      exact le_top
    obtain ⟨t₁, h₁, hT₁⟩ := exists_eq_captureTime hTop
    have hsort' := List.pairwise_cons.mp hsort
    have hXY : captureTime S X ≤ t₁ := by
      rcases List.mem_cons.mp hY with hYX | hY'
      · rw [← hT₁, hYX]
      · rw [← hT₁]
        exact hsort'.1 Y hY'
    obtain ⟨τ, hτ, hTτ⟩ := exists_eq_captureTime (ne_top_of_le_ne_top ENNReal.coe_ne_top hXY)
    have hX := hL X List.mem_cons_self
    have hle : ∀ Z ∈ X :: rest, (τ : ℝ≥0∞) ≤ captureTime S Z := by
      intro Z hZ
      rcases List.mem_cons.mp hZ with hZX | hZ'
      · rw [hZX, hTτ]
      · rw [← hTτ]
        exact hsort'.1 Z hZ'
    obtain ⟨t, -, ht1, hmt⟩ := greedy_greedyFrom_meets hS (X :: rest) hL hsort X hX 0 τ
      zero_le hτ hle Y hY t₁ h₁ hT₁
    rw [hT₁]
    exact (captureTime_le (S := greedyPath (X :: rest)) hmt).trans (ENNReal.coe_le_coe.mpr ht1)

/-- **Proposition 5** (`prop:5`). Suppose the hider uses a mixed strategy concentrated on
finitely many pure strategies `H j ∈ 𝒮`. Every searcher path `S` is dominated, against each
`H j`, by the greedy path for the order in which `S` meets them: the searcher picks an order
`σ` and runs towards `H (σ (j+1))` as soon as he has met `H (σ j)`. -/
theorem proposition5 {J : ℕ} (H : Fin J → C(ℝ≥0, ℝ)) (hH : ∀ j, H j ∈ searcherPaths)
    {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    ∃ σ : Equiv.Perm (Fin J), ∀ j, captureTime (greedyOrder H σ) (H j) ≤ captureTime S (H j) := by
  -- `σ` orders the `H j` by the time at which `S` meets them (those never met last)
  let f : Fin J → ℝ≥0∞ := fun j => captureTime S (H j)
  refine ⟨Tuple.sort f, fun j => ?_⟩
  have hmono := Tuple.monotone_sort f
  refine greedy_greedyPath_le hS ?_ ?_ (H j) ?_
  · intro X hX
    obtain ⟨k, rfl⟩ := (List.mem_ofFn' _ _).mp hX
    exact hH _
  · rw [List.pairwise_ofFn]
    intro i k hik
    exact hmono hik.le
  · rw [List.mem_ofFn']
    exact ⟨(Tuple.sort f).symm j, by simp⟩

/-- **Proposition 5** (`prop:5`), for mixed strategies: the optimal response to the hider
strategy that uses `H j` with weight `q j` is concentrated on the finitely many greedy paths. -/
theorem proposition5_response {J : ℕ} (H : Fin J → C(ℝ≥0, ℝ)) (hH : ∀ j, H j ∈ searcherPaths)
    (q : Fin J → ℝ≥0∞) :
    ⨅ S ∈ searcherPaths, ∑ j, q j * captureTime S (H j) =
      ⨅ σ : Equiv.Perm (Fin J), ∑ j, q j * captureTime (greedyOrder H σ) (H j) := by
  apply le_antisymm
  · exact le_iInf fun σ => iInf₂_le (greedyOrder H σ) (greedyOrder_mem hH σ)
  · refine le_iInf₂ fun S hS => ?_
    obtain ⟨σ, hσ⟩ := proposition5 H hH hS
    refine (iInf_le _ σ).trans ?_
    gcongr with j
    exact hσ j

end PrincessMonster
