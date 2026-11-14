module

public import PrincessMonster.CaptureTime
public import Mathlib.Order.ConditionallyCompleteLattice.Basic
public import Mathlib.Topology.Order.Basic
public import Mathlib.Topology.Piecewise

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

lemma greedyOrder_mem {J : ℕ} {H : Fin J → C(ℝ≥0, ℝ)} (hH : ∀ j, H j ∈ searcherPaths)
    (σ : Equiv.Perm (Fin J)) : greedyOrder H σ ∈ searcherPaths := by
  sorry

/-- **Proposition 5** (`prop:5`). Suppose the hider uses a mixed strategy concentrated on
finitely many pure strategies `H j ∈ 𝒮`. Every searcher path `S` is dominated, against each
`H j`, by the greedy path for the order in which `S` meets them: the searcher picks an order
`σ` and runs towards `H (σ (j+1))` as soon as he has met `H (σ j)`. -/
theorem proposition5 {J : ℕ} (H : Fin J → C(ℝ≥0, ℝ)) (hH : ∀ j, H j ∈ searcherPaths)
    {S : C(ℝ≥0, ℝ)} (hS : S ∈ searcherPaths) :
    ∃ σ : Equiv.Perm (Fin J), ∀ j, captureTime (greedyOrder H σ) (H j) ≤ captureTime S (H j) := by
  sorry

/-- **Proposition 5** (`prop:5`), for mixed strategies: the optimal response to the hider
strategy that uses `H j` with weight `q j` is concentrated on the finitely many greedy paths. -/
theorem proposition5_response {J : ℕ} (H : Fin J → C(ℝ≥0, ℝ)) (hH : ∀ j, H j ∈ searcherPaths)
    (q : Fin J → ℝ≥0∞) :
    ⨅ S ∈ searcherPaths, ∑ j, q j * captureTime S (H j) =
      ⨅ σ : Equiv.Perm (Fin J), ∑ j, q j * captureTime (greedyOrder H σ) (H j) := by
  sorry

end PrincessMonster
