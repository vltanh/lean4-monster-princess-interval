module

public import PrincessMonster.Section3.Strategies
public import PrincessMonster.Section2.Greedy
public import Mathlib.Order.Filter.Basic
public import Mathlib.Topology.Instances.ENNReal.Lemmas
public import Mathlib.Data.Fin.VecNotation
public import Mathlib.Algebra.BigOperators.Fin

/-!
# Section 3: the matrix game (4) and Theorem 10, `V ≥ 97/75`

The hider mixes `E, F, G, H` and their reflections; by Proposition 5 the searcher's relevant
responses are, up to symmetry, `A, B, C, D, M`. Ignoring `ε`, the expected capture times give
the zero-sum matrix game (4), whose value `97/75` is a lower bound on `V`.

* `matrix4`: the matrix (4), rows `A, B, C, D, M`, columns `E, F, G, H`.
* `equation4`: each entry is the limit, as `ε → 0`, of the average capture time of the row path
  against the column path and its reflection.
* `matrix4_value`: the matrix game (4) has value `97/75`.
* `theorem10`: `97/75 ≤ V` (the lower value).
-/

@[expose] public section

open scoped NNReal ENNReal Topology
open MeasureTheory Filter

namespace PrincessMonster

/-- The matrix (4): rows `A, B, C, D, M` (searcher), columns `E, F, G, H` (hider). -/
def matrix4 : Fin 5 → Fin 4 → ℚ :=
  ![![1, 3 / 2, 3 / 2, 5 / 4],
    ![3, 0, 5 / 4, 3],
    ![3 / 2, 15 / 8, 5 / 4, 5 / 4],
    ![5 / 2, 1 / 2, 3 / 8, 3 / 4],
    ![2, 0, 7 / 4, 2]]

/-- The searcher paths of the rows of (4). -/
noncomputable def rowPath : Fin 5 → C(ℝ≥0, ℝ) := ![sweeperA, stratB, stratC, stratD, stratM]

/-- The hider paths of the columns of (4), for the parameter `ε`. -/
noncomputable def colPath (ε : ℝ) : Fin 4 → C(ℝ≥0, ℝ) :=
  ![hiderE, hiderF ε, hiderG ε, hiderH ε]

/-! ### The forty capture times of the matrix (4)

For `0 < ε ≤ 1/100` every capture time of a row path against a column path or its reflection is
an explicit affine function of `ε`. Each one is computed from the formulas of the paths: the
paths meet at the stated time and are strictly ordered before it. -/

/-- A capture time computed from formulas: if `S` and `X` are given by `s` and `x` up to time
`t₀`, meet at `t₀` and differ before, the capture time is `t₀`. -/
lemma s3b_captureTime_eq {S X : C(ℝ≥0, ℝ)} {s x : ℝ → ℝ} {t₀ : ℝ} (h0 : 0 ≤ t₀)
    (hS : ∀ t : ℝ≥0, (t : ℝ) ≤ t₀ → S t = s t) (hX : ∀ t : ℝ≥0, (t : ℝ) ≤ t₀ → X t = x t)
    (hmeet : s t₀ = x t₀) (hne : ∀ t : ℝ, 0 ≤ t → t < t₀ → s t ≠ x t) :
    captureTime S X = ENNReal.ofReal t₀ := by
  lift t₀ to ℝ≥0 using h0
  rw [ENNReal.ofReal_coe_nnreal]
  apply le_antisymm
  · exact captureTime_le (by rw [hS _ le_rfl, hX _ le_rfl]; exact hmeet)
  · apply le_captureTime_of_ne
    intro t ht
    have ht' : (t : ℝ) < t₀ := ht
    rw [hS _ ht'.le, hX _ ht'.le]
    exact hne t t.2 ht'

/-- Linear arithmetic through `min` and `max`. -/
local macro "s3b_lin" : tactic =>
  `(tactic| ((try dsimp only); (try simp only [min_def, max_def]); (try split_ifs) <;> linarith))

/-- Two formulas differ: one of them is strictly below the other. -/
local macro "s3b_ne" : tactic =>
  `(tactic| first
    | (intro t ht0 ht; apply ne_of_lt; s3b_lin)
    | (intro t ht0 ht; apply ne_of_gt; s3b_lin))

/-- The sweeper `A(t) = 1 - t` on `[0, 2]`. -/
lemma s3b_A_apply (t : ℝ≥0) (h : (t : ℝ) ≤ 2) : sweeperA t = 1 - t :=
  Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith [NNReal.coe_nonneg t]⟩

/-- `B(t)` on `[0, 4]`: `-t` on `[0, 1/2]`, `t - 1` on `[1/2, 2]`, `3 - t` on `[2, 4]`. -/
lemma s3b_B_apply (t : ℝ≥0) (h : (t : ℝ) ≤ 4) :
    stratB t = min (max (-(t : ℝ)) (t - 1)) (3 - t) := by
  have h0 : (0 : ℝ) ≤ t := t.2
  change Real.triangleWave (|(t : ℝ) - 1 / 2| - 1 / 2) = _
  rcases le_total (t : ℝ) (1 / 2) with h1 | h1
  · rw [abs_of_nonpos (by linarith), Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith⟩]
    s3b_lin
  · rw [abs_of_nonneg (by linarith)]
    rcases le_total (t : ℝ) 2 with h2 | h2
    · rw [Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith⟩]
      s3b_lin
    · rw [Real.triangleWave_of_mem_Icc_one_three ⟨by linarith, by linarith⟩]
      s3b_lin

/-- `C(t)` on `[0, 5/2]`: `1/2 + t` on `[0, 1/2]`, `3/2 - t` on `[1/2, 5/2]`. -/
lemma s3b_C_apply (t : ℝ≥0) (h : (t : ℝ) ≤ 5 / 2) :
    stratC t = min (1 / 2 + (t : ℝ)) (3 / 2 - t) := by
  have h0 : (0 : ℝ) ≤ t := t.2
  change Real.triangleWave (1 / 2 + (t : ℝ)) = _
  rcases le_total (t : ℝ) (1 / 2) with h1 | h1
  · rw [Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith⟩]
    s3b_lin
  · rw [Real.triangleWave_of_mem_Icc_one_three ⟨by linarith, by linarith⟩]
    s3b_lin

/-- `D(t)` on `[0, 7/2]`: `1/2 - t` on `[0, 3/2]`, `t - 5/2` on `[3/2, 7/2]`. -/
lemma s3b_D_apply (t : ℝ≥0) (h : (t : ℝ) ≤ 7 / 2) :
    stratD t = max (1 / 2 - (t : ℝ)) (t - 5 / 2) := by
  have h0 : (0 : ℝ) ≤ t := t.2
  change Real.triangleWave (1 / 2 - (t : ℝ)) = _
  rcases le_total (t : ℝ) (3 / 2) with h1 | h1
  · rw [Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith⟩]
    s3b_lin
  · rw [Real.triangleWave_of_mem_Icc_neg_three_neg_one ⟨by linarith, by linarith⟩]
    s3b_lin

/-- `M(t)` on `[0, 3]`: `-t` on `[0, 1]`, `t - 2` on `[1, 3]`. -/
lemma s3b_M_apply (t : ℝ≥0) (h : (t : ℝ) ≤ 3) :
    stratM t = max (-(t : ℝ)) (t - 2) := by
  have h0 : (0 : ℝ) ≤ t := t.2
  change Real.triangleWave (-(t : ℝ)) = _
  rcases le_total (t : ℝ) 1 with h1 | h1
  · rw [Real.triangleWave_of_mem_Icc ⟨by linarith, by linarith⟩]
    s3b_lin
  · rw [Real.triangleWave_of_mem_Icc_neg_three_neg_one ⟨by linarith, by linarith⟩]
    s3b_lin

/-! The capture times against `±E` (independent of `ε`). -/

lemma s3b_T_A_E : captureTime sweeperA hiderE = ENNReal.ofReal 0 :=
  s3b_captureTime_eq (s := fun t => 1 - t) (x := fun _ => 1) le_rfl
    (fun t ht => s3b_A_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_A_nE : captureTime sweeperA (-hiderE) = ENNReal.ofReal 2 :=
  s3b_captureTime_eq (s := fun t => 1 - t) (x := fun _ => -1) (by norm_num)
    (fun t ht => s3b_A_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_B_E : captureTime stratB hiderE = ENNReal.ofReal 2 :=
  s3b_captureTime_eq (s := fun t => min (max (-t) (t - 1)) (3 - t)) (x := fun _ => 1) (by norm_num)
    (fun t ht => s3b_B_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_B_nE : captureTime stratB (-hiderE) = ENNReal.ofReal 4 :=
  s3b_captureTime_eq (s := fun t => min (max (-t) (t - 1)) (3 - t)) (x := fun _ => -1) (by norm_num)
    (fun t ht => s3b_B_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_C_E : captureTime stratC hiderE = ENNReal.ofReal (1 / 2) :=
  s3b_captureTime_eq (s := fun t => min (1 / 2 + t) (3 / 2 - t)) (x := fun _ => 1) (by norm_num)
    (fun t ht => s3b_C_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_C_nE : captureTime stratC (-hiderE) = ENNReal.ofReal (5 / 2) :=
  s3b_captureTime_eq (s := fun t => min (1 / 2 + t) (3 / 2 - t)) (x := fun _ => -1) (by norm_num)
    (fun t ht => s3b_C_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_D_E : captureTime stratD hiderE = ENNReal.ofReal (7 / 2) :=
  s3b_captureTime_eq (s := fun t => max (1 / 2 - t) (t - 5 / 2)) (x := fun _ => 1) (by norm_num)
    (fun t ht => s3b_D_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_D_nE : captureTime stratD (-hiderE) = ENNReal.ofReal (3 / 2) :=
  s3b_captureTime_eq (s := fun t => max (1 / 2 - t) (t - 5 / 2)) (x := fun _ => -1) (by norm_num)
    (fun t ht => s3b_D_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_M_E : captureTime stratM hiderE = ENNReal.ofReal 3 :=
  s3b_captureTime_eq (s := fun t => max (-t) (t - 2)) (x := fun _ => 1) (by norm_num)
    (fun t ht => s3b_M_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_M_nE : captureTime stratM (-hiderE) = ENNReal.ofReal 1 :=
  s3b_captureTime_eq (s := fun t => max (-t) (t - 2)) (x := fun _ => -1) (by norm_num)
    (fun t ht => s3b_M_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

section CaptureTimes

variable {ε : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100)
include hε hε1

lemma s3b_T_A_F : captureTime sweeperA (hiderF ε) = ENNReal.ofReal (1 - ε / 2) :=
  s3b_captureTime_eq (s := fun t => 1 - t) (x := fun t => max 0 (min 1 (t + ε - 1))) (by linarith)
    (fun t ht => s3b_A_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_A_nF : captureTime sweeperA (-hiderF ε) = ENNReal.ofReal 2 :=
  s3b_captureTime_eq (s := fun t => 1 - t) (x := fun t => -max 0 (min 1 (t + ε - 1))) (by norm_num)
    (fun t ht => s3b_A_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_A_G : captureTime sweeperA (hiderG ε) = ENNReal.ofReal (1 - 3 * ε / 2) :=
  s3b_captureTime_eq (s := fun t => 1 - t)
    (x := fun t => min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) (by linarith)
    (fun t ht => s3b_A_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_A_nG : captureTime sweeperA (-hiderG ε) = ENNReal.ofReal 2 :=
  s3b_captureTime_eq (s := fun t => 1 - t)
    (x := fun t => -min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) (by norm_num)
    (fun t ht => s3b_A_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_A_H : captureTime sweeperA (hiderH ε) = ENNReal.ofReal ((1 - ε) / 2) :=
  s3b_captureTime_eq (s := fun t => 1 - t) (x := fun t => min 1 (max (1 / 2) (t + ε))) (by linarith)
    (fun t ht => s3b_A_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_A_nH : captureTime sweeperA (-hiderH ε) = ENNReal.ofReal 2 :=
  s3b_captureTime_eq (s := fun t => 1 - t)
    (x := fun t => -min 1 (max (1 / 2) (t + ε))) (by norm_num)
    (fun t ht => s3b_A_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_B_F : captureTime stratB (hiderF ε) = ENNReal.ofReal 0 :=
  s3b_captureTime_eq (s := fun t => min (max (-t) (t - 1)) (3 - t))
    (x := fun t => max 0 (min 1 (t + ε - 1))) le_rfl
    (fun t ht => s3b_B_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_B_nF : captureTime stratB (-hiderF ε) = ENNReal.ofReal 0 :=
  s3b_captureTime_eq (s := fun t => min (max (-t) (t - 1)) (3 - t))
    (x := fun t => -max 0 (min 1 (t + ε - 1))) le_rfl
    (fun t ht => s3b_B_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_B_G : captureTime stratB (hiderG ε) = ENNReal.ofReal 2 :=
  s3b_captureTime_eq (s := fun t => min (max (-t) (t - 1)) (3 - t))
    (x := fun t => min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) (by norm_num)
    (fun t ht => s3b_B_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_B_nG : captureTime stratB (-hiderG ε) = ENNReal.ofReal ((1 - ε) / 2) :=
  s3b_captureTime_eq (s := fun t => min (max (-t) (t - 1)) (3 - t))
    (x := fun t => -min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) (by linarith)
    (fun t ht => s3b_B_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_B_H : captureTime stratB (hiderH ε) = ENNReal.ofReal 2 :=
  s3b_captureTime_eq (s := fun t => min (max (-t) (t - 1)) (3 - t))
    (x := fun t => min 1 (max (1 / 2) (t + ε))) (by norm_num)
    (fun t ht => s3b_B_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_B_nH : captureTime stratB (-hiderH ε) = ENNReal.ofReal 4 :=
  s3b_captureTime_eq (s := fun t => min (max (-t) (t - 1)) (3 - t))
    (x := fun t => -min 1 (max (1 / 2) (t + ε))) (by norm_num)
    (fun t ht => s3b_B_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_C_F : captureTime stratC (hiderF ε) = ENNReal.ofReal (5 / 4 - ε / 2) :=
  s3b_captureTime_eq (s := fun t => min (1 / 2 + t) (3 / 2 - t))
    (x := fun t => max 0 (min 1 (t + ε - 1))) (by linarith)
    (fun t ht => s3b_C_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_C_nF : captureTime stratC (-hiderF ε) = ENNReal.ofReal (5 / 2) :=
  s3b_captureTime_eq (s := fun t => min (1 / 2 + t) (3 / 2 - t))
    (x := fun t => -max 0 (min 1 (t + ε - 1))) (by norm_num)
    (fun t ht => s3b_C_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_C_G : captureTime stratC (hiderG ε) = ENNReal.ofReal 0 :=
  s3b_captureTime_eq (s := fun t => min (1 / 2 + t) (3 / 2 - t))
    (x := fun t => min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) le_rfl
    (fun t ht => s3b_C_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_C_nG : captureTime stratC (-hiderG ε) = ENNReal.ofReal (5 / 2) :=
  s3b_captureTime_eq (s := fun t => min (1 / 2 + t) (3 / 2 - t))
    (x := fun t => -min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) (by norm_num)
    (fun t ht => s3b_C_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_C_H : captureTime stratC (hiderH ε) = ENNReal.ofReal 0 :=
  s3b_captureTime_eq (s := fun t => min (1 / 2 + t) (3 / 2 - t))
    (x := fun t => min 1 (max (1 / 2) (t + ε))) le_rfl
    (fun t ht => s3b_C_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_C_nH : captureTime stratC (-hiderH ε) = ENNReal.ofReal (5 / 2) :=
  s3b_captureTime_eq (s := fun t => min (1 / 2 + t) (3 / 2 - t))
    (x := fun t => -min 1 (max (1 / 2) (t + ε))) (by norm_num)
    (fun t ht => s3b_C_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_D_F : captureTime stratD (hiderF ε) = ENNReal.ofReal (1 / 2) :=
  s3b_captureTime_eq (s := fun t => max (1 / 2 - t) (t - 5 / 2))
    (x := fun t => max 0 (min 1 (t + ε - 1))) (by norm_num)
    (fun t ht => s3b_D_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_D_nF : captureTime stratD (-hiderF ε) = ENNReal.ofReal (1 / 2) :=
  s3b_captureTime_eq (s := fun t => max (1 / 2 - t) (t - 5 / 2))
    (x := fun t => -max 0 (min 1 (t + ε - 1))) (by norm_num)
    (fun t ht => s3b_D_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_D_G : captureTime stratD (hiderG ε) = ENNReal.ofReal 0 :=
  s3b_captureTime_eq (s := fun t => max (1 / 2 - t) (t - 5 / 2))
    (x := fun t => min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) le_rfl
    (fun t ht => s3b_D_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_D_nG : captureTime stratD (-hiderG ε) = ENNReal.ofReal (3 / 4 - ε / 2) :=
  s3b_captureTime_eq (s := fun t => max (1 / 2 - t) (t - 5 / 2))
    (x := fun t => -min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) (by linarith)
    (fun t ht => s3b_D_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_D_H : captureTime stratD (hiderH ε) = ENNReal.ofReal 0 :=
  s3b_captureTime_eq (s := fun t => max (1 / 2 - t) (t - 5 / 2))
    (x := fun t => min 1 (max (1 / 2) (t + ε))) le_rfl
    (fun t ht => s3b_D_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_D_nH : captureTime stratD (-hiderH ε) = ENNReal.ofReal (3 / 2) :=
  s3b_captureTime_eq (s := fun t => max (1 / 2 - t) (t - 5 / 2))
    (x := fun t => -min 1 (max (1 / 2) (t + ε))) (by norm_num)
    (fun t ht => s3b_D_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_M_F : captureTime stratM (hiderF ε) = ENNReal.ofReal 0 :=
  s3b_captureTime_eq (s := fun t => max (-t) (t - 2))
    (x := fun t => max 0 (min 1 (t + ε - 1))) le_rfl
    (fun t ht => s3b_M_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_M_nF : captureTime stratM (-hiderF ε) = ENNReal.ofReal 0 :=
  s3b_captureTime_eq (s := fun t => max (-t) (t - 2))
    (x := fun t => -max 0 (min 1 (t + ε - 1))) le_rfl
    (fun t ht => s3b_M_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_M_G : captureTime stratM (hiderG ε) = ENNReal.ofReal 3 :=
  s3b_captureTime_eq (s := fun t => max (-t) (t - 2))
    (x := fun t => min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) (by norm_num)
    (fun t ht => s3b_M_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_M_nG : captureTime stratM (-hiderG ε) = ENNReal.ofReal ((1 - ε) / 2) :=
  s3b_captureTime_eq (s := fun t => max (-t) (t - 2))
    (x := fun t => -min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) (by linarith)
    (fun t ht => s3b_M_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_M_H : captureTime stratM (hiderH ε) = ENNReal.ofReal 3 :=
  s3b_captureTime_eq (s := fun t => max (-t) (t - 2))
    (x := fun t => min 1 (max (1 / 2) (t + ε))) (by norm_num)
    (fun t ht => s3b_M_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

lemma s3b_T_M_nH : captureTime stratM (-hiderH ε) = ENNReal.ofReal 1 :=
  s3b_captureTime_eq (s := fun t => max (-t) (t - 2))
    (x := fun t => -min 1 (max (1 / 2) (t + ε))) (by norm_num)
    (fun t ht => s3b_M_apply t (by linarith)) (fun _ _ => rfl) (by s3b_lin) (by s3b_ne)

end CaptureTimes

/-- The limit of an average of two capture times that are, for `0 < ε ≤ 1/100`, given by
continuous formulas `a ε` and `b ε`. -/
lemma s3b_tendsto {u v : ℝ → ℝ≥0∞} {a b : ℝ → ℝ} {m : ℝ} (ha : Continuous a)
    (hb : Continuous b)
    (hu : ∀ ε : ℝ, 0 < ε → ε ≤ 1 / 100 → u ε = ENNReal.ofReal (a ε))
    (hv : ∀ ε : ℝ, 0 < ε → ε ≤ 1 / 100 → v ε = ENNReal.ofReal (b ε))
    (ha0 : ∀ ε : ℝ, 0 < ε → ε ≤ 1 / 100 → 0 ≤ a ε)
    (hb0 : ∀ ε : ℝ, 0 < ε → ε ≤ 1 / 100 → 0 ≤ b ε)
    (hm : (a 0 + b 0) / 2 = m) :
    Tendsto (fun ε => (u ε + v ε) / 2) (𝓝[>] 0) (𝓝 (ENNReal.ofReal m)) := by
  have hev : (fun ε => ENNReal.ofReal ((a ε + b ε) / 2)) =ᶠ[𝓝[>] 0]
      fun ε => (u ε + v ε) / 2 := by
    filter_upwards [Ioo_mem_nhdsGT (show (0 : ℝ) < 1 / 100 by norm_num)] with ε hε
    rw [hu ε hε.1 hε.2.le, hv ε hε.1 hε.2.le, ENNReal.ofReal_div_of_pos two_pos,
      ENNReal.ofReal_add (ha0 ε hε.1 hε.2.le) (hb0 ε hε.1 hε.2.le), ENNReal.ofReal_ofNat]
  refine Tendsto.congr' hev (ENNReal.tendsto_ofReal ?_)
  rw [← hm]
  exact (((ha.add hb).div_const 2).tendsto 0).mono_left nhdsWithin_le_nhds

/-- **Equation (4)** (`eq:4`). Ignoring `ε`, the strategies give the matrix (4): its entry in
row `i` and column `j` is the limit, as `ε → 0⁺`, of the average capture time of the row path
against the column path and against its reflection. -/
theorem equation4 (i : Fin 5) (j : Fin 4) :
    Tendsto (fun ε : ℝ => (captureTime (rowPath i) (colPath ε j) +
        captureTime (rowPath i) (-colPath ε j)) / 2) (𝓝[>] 0)
      (𝓝 (ENNReal.ofReal (matrix4 i j))) := by
  fin_cases i <;> fin_cases j
  · exact s3b_tendsto (a := fun _ => 0) (b := fun _ => 2) (by fun_prop) (by fun_prop)
      (fun _ _ _ => s3b_T_A_E) (fun _ _ _ => s3b_T_A_nE)
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun ε => 1 - ε / 2) (b := fun _ => 2) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_A_F h h') (fun _ h h' => s3b_T_A_nF h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun ε => 1 - 3 * ε / 2) (b := fun _ => 2) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_A_G h h') (fun _ h h' => s3b_T_A_nG h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun ε => (1 - ε) / 2) (b := fun _ => 2) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_A_H h h') (fun _ h h' => s3b_T_A_nH h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 2) (b := fun _ => 4) (by fun_prop) (by fun_prop)
      (fun _ _ _ => s3b_T_B_E) (fun _ _ _ => s3b_T_B_nE)
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 0) (b := fun _ => 0) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_B_F h h') (fun _ h h' => s3b_T_B_nF h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 2) (b := fun ε => (1 - ε) / 2) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_B_G h h') (fun _ h h' => s3b_T_B_nG h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 2) (b := fun _ => 4) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_B_H h h') (fun _ h h' => s3b_T_B_nH h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 1 / 2) (b := fun _ => 5 / 2) (by fun_prop) (by fun_prop)
      (fun _ _ _ => s3b_T_C_E) (fun _ _ _ => s3b_T_C_nE)
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun ε => 5 / 4 - ε / 2) (b := fun _ => 5 / 2) (by fun_prop)
      (by fun_prop)
      (fun _ h h' => s3b_T_C_F h h') (fun _ h h' => s3b_T_C_nF h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 0) (b := fun _ => 5 / 2) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_C_G h h') (fun _ h h' => s3b_T_C_nG h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 0) (b := fun _ => 5 / 2) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_C_H h h') (fun _ h h' => s3b_T_C_nH h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 7 / 2) (b := fun _ => 3 / 2) (by fun_prop) (by fun_prop)
      (fun _ _ _ => s3b_T_D_E) (fun _ _ _ => s3b_T_D_nE)
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 1 / 2) (b := fun _ => 1 / 2) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_D_F h h') (fun _ h h' => s3b_T_D_nF h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 0) (b := fun ε => 3 / 4 - ε / 2) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_D_G h h') (fun _ h h' => s3b_T_D_nG h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 0) (b := fun _ => 3 / 2) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_D_H h h') (fun _ h h' => s3b_T_D_nH h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 3) (b := fun _ => 1) (by fun_prop) (by fun_prop)
      (fun _ _ _ => s3b_T_M_E) (fun _ _ _ => s3b_T_M_nE)
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 0) (b := fun _ => 0) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_M_F h h') (fun _ h h' => s3b_T_M_nF h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 3) (b := fun ε => (1 - ε) / 2) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_M_G h h') (fun _ h h' => s3b_T_M_nG h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])
  · exact s3b_tendsto (a := fun _ => 3) (b := fun _ => 1) (by fun_prop) (by fun_prop)
      (fun _ h h' => s3b_T_M_H h h') (fun _ h h' => s3b_T_M_nH h h')
      (fun _ _ _ => by linarith) (fun _ _ _ => by linarith) (by norm_num [matrix4])

/-- The value of the matrix game (4) is `97/75`: the hider's mixed strategy `q` guarantees at
least `97/75` against every row, and the searcher's mixed strategy `p` concedes at most `97/75`
against every column. -/
theorem matrix4_value :
    ∃ (p : Fin 5 → ℚ) (q : Fin 4 → ℚ), (∀ i, 0 ≤ p i) ∧ ∑ i, p i = 1 ∧
      (∀ j, 0 ≤ q j) ∧ ∑ j, q j = 1 ∧
      (∀ i, 97 / 75 ≤ ∑ j, matrix4 i j * q j) ∧ (∀ j, ∑ i, p i * matrix4 i j ≤ 97 / 75) := by
  refine ⟨![4 / 5, 0, 0, 14 / 75, 1 / 75], ![31 / 75, 24 / 75, 20 / 75, 0], ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro i; fin_cases i <;> norm_num
  · simp [Fin.sum_univ_succ]; norm_num
  · intro j; fin_cases j <;> norm_num
  · simp [Fin.sum_univ_succ]; norm_num
  · intro i; fin_cases i <;> simp [Fin.sum_univ_succ, matrix4] <;> norm_num
  · intro j; fin_cases j <;> simp [Fin.sum_univ_succ, matrix4] <;> norm_num

/-- The hider's mixed strategy of Theorem 10 for the parameter `ε`: it uses `E, F, G, H` with
the optimal probabilities `31/75, 24/75, 20/75, 0` of the matrix game (4), each split equally
between the path and its reflection. -/
noncomputable def strategy10 (ε : ℝ) : Measure hiderPaths :=
  (31 / 75 : ℝ≥0∞) • symDiracH hiderE + (24 / 75 : ℝ≥0∞) • symDiracH (hiderF ε) +
    (20 / 75 : ℝ≥0∞) • symDiracH (hiderG ε)

/-! ### Theorem 10

The hider uses `±E`, `±F`, `±G` with weights `31/150`, `24/150`, `20/150` each. By
Proposition 5 the searcher may be assumed to start where one of these paths starts, at `±1`, `0`
or `±1/2`. By symmetry the starts `1`, `0`, `1/2` suffice, and for each of them a direct bound
on the six capture times gives an expected capture time of at least `97/75 - 7ε/25`. -/

/-- The greedy path starts where the first path of its order starts. -/
lemma s3b_greedyOrder_zero {J : ℕ} (H : Fin (J + 1) → C(ℝ≥0, ℝ))
    (σ : Equiv.Perm (Fin (J + 1))) : greedyOrder H σ 0 = H (σ 0) 0 := by
  rw [greedyOrder, List.ofFn_succ]
  simp [greedyPath, greedyFrom, glue, chase]

lemma s3b_toHider {X : C(ℝ≥0, ℝ)} (h : X ∈ hiderPaths) : (toHider X : C(ℝ≥0, ℝ)) = X := by
  simp [toHider, h]

/-- The expected capture time of a path `P` against the hider strategy of Theorem 10. -/
noncomputable def s3b_pay (ε : ℝ) (P : C(ℝ≥0, ℝ)) : ℝ≥0∞ :=
  31 / 75 * (1 / 2 * (captureTime P hiderE + captureTime P (-hiderE))) +
    24 / 75 * (1 / 2 * (captureTime P (hiderF ε) + captureTime P (-hiderF ε))) +
    20 / 75 * (1 / 2 * (captureTime P (hiderG ε) + captureTime P (-hiderG ε)))

lemma s3b_lintegral {ε : ℝ} (hε : 0 ≤ ε) (hε1 : ε ≤ 1 / 4) (S : C(ℝ≥0, ℝ)) :
    ∫⁻ H, captureTime S H ∂(strategy10 ε) = s3b_pay ε S := by
  have hE := searcherPaths_subset_hiderPaths hiderE_mem
  have hF := searcherPaths_subset_hiderPaths (hiderF_mem (ε := ε))
  have hG := searcherPaths_subset_hiderPaths (hiderG_mem hε)
  simp only [strategy10, symDiracH, lintegral_add_measure, lintegral_smul_measure,
    lintegral_dirac, s3b_toHider hE, s3b_toHider hF, s3b_toHider hG,
    s3b_toHider (neg_mem_hiderPaths hE), s3b_toHider (neg_mem_hiderPaths hF),
    s3b_toHider (neg_mem_hiderPaths hG), smul_eq_mul, s3b_pay]

instance s3b_isProbabilityMeasure (ε : ℝ) : IsProbabilityMeasure (strategy10 ε) := by
  constructor
  simp only [strategy10, symDiracH, Measure.add_apply, Measure.smul_apply, measure_univ,
    smul_eq_mul]
  rw [one_add_one_eq_two, one_div, ENNReal.inv_mul_cancel two_ne_zero ENNReal.ofNat_ne_top,
    mul_one, mul_one, mul_one, ENNReal.div_add_div_same, ENNReal.div_add_div_same]
  norm_num
  exact ENNReal.div_self (by norm_num) (by norm_num)

lemma s3b_captureTime_neg_left (P X : C(ℝ≥0, ℝ)) : captureTime (-P) X = captureTime P (-X) := by
  rw [← captureTime_neg (S := P) (H := -X), neg_neg]

/-- The hider strategy is symmetric: a path and its reflection have the same payoff. -/
lemma s3b_pay_neg (ε : ℝ) (P : C(ℝ≥0, ℝ)) : s3b_pay ε (-P) = s3b_pay ε P := by
  simp only [s3b_pay, s3b_captureTime_neg_left, neg_neg]
  rw [add_comm (captureTime P (-hiderE)), add_comm (captureTime P (-hiderF ε)),
    add_comm (captureTime P (-hiderG ε))]

lemma s3b_pay_top {ε : ℝ} {P : C(ℝ≥0, ℝ)}
    (h : captureTime P hiderE = ⊤ ∨ captureTime P (-hiderE) = ⊤) : s3b_pay ε P = ⊤ := by
  rcases h with h | h <;> simp [s3b_pay, h, ENNReal.mul_top]

/-- No meeting before `c` gives the lower bound `c` on the capture time. -/
lemma s3b_ofReal_le {S X : C(ℝ≥0, ℝ)} {c : ℝ} (h : ∀ t : ℝ≥0, (t : ℝ) < c → S t ≠ X t) :
    ENNReal.ofReal c ≤ captureTime S X := by
  change ((Real.toNNReal c : ℝ≥0) : ℝ≥0∞) ≤ _
  exact le_captureTime_of_ne fun t ht => h t (Real.lt_toNNReal_iff_coe_lt.mp ht)

/-- Lower bounds on the six capture times give a lower bound on the payoff. -/
lemma s3b_pay_ge {ε : ℝ} {P : C(ℝ≥0, ℝ)} {ca cb cf cf' cg cg' : ℝ} (h1 : 0 ≤ ca) (h2 : 0 ≤ cb)
    (h3 : 0 ≤ cf) (h4 : 0 ≤ cf') (h5 : 0 ≤ cg) (h6 : 0 ≤ cg')
    (ha : ENNReal.ofReal ca ≤ captureTime P hiderE)
    (hb : ENNReal.ofReal cb ≤ captureTime P (-hiderE))
    (hf : ENNReal.ofReal cf ≤ captureTime P (hiderF ε))
    (hf' : ENNReal.ofReal cf' ≤ captureTime P (-hiderF ε))
    (hg : ENNReal.ofReal cg ≤ captureTime P (hiderG ε))
    (hg' : ENNReal.ofReal cg' ≤ captureTime P (-hiderG ε))
    (hsum : 194 - 42 * ε ≤ 31 * (ca + cb) + 24 * (cf + cf') + 20 * (cg + cg')) :
    ENNReal.ofReal (97 / 75 - 7 * ε / 25) ≤ s3b_pay ε P := by
  calc ENNReal.ofReal (97 / 75 - 7 * ε / 25)
      ≤ ENNReal.ofReal (31 / 75 * (1 / 2 * (ca + cb)) + 24 / 75 * (1 / 2 * (cf + cf')) +
          20 / 75 * (1 / 2 * (cg + cg'))) := ENNReal.ofReal_le_ofReal (by linarith)
    _ = 31 / 75 * (1 / 2 * (ENNReal.ofReal ca + ENNReal.ofReal cb)) +
          24 / 75 * (1 / 2 * (ENNReal.ofReal cf + ENNReal.ofReal cf')) +
          20 / 75 * (1 / 2 * (ENNReal.ofReal cg + ENNReal.ofReal cg')) := by
        rw [ENNReal.ofReal_add (by positivity) (by positivity),
          ENNReal.ofReal_add (by positivity) (by positivity),
          ENNReal.ofReal_mul (by norm_num), ENNReal.ofReal_mul (by norm_num),
          ENNReal.ofReal_mul (by norm_num), ENNReal.ofReal_mul (by norm_num),
          ENNReal.ofReal_mul (by norm_num), ENNReal.ofReal_mul (by norm_num),
          ENNReal.ofReal_add h1 h2, ENNReal.ofReal_add h3 h4, ENNReal.ofReal_add h5 h6]
        simp only [ENNReal.ofReal_div_of_pos (show (0 : ℝ) < 75 by norm_num),
          ENNReal.ofReal_div_of_pos (show (0 : ℝ) < 2 by norm_num), ENNReal.ofReal_ofNat,
          ENNReal.ofReal_one]
    _ ≤ s3b_pay ε P := by
        unfold s3b_pay
        gcongr

/-- The speed limit. -/
lemma s3b_lip {P : C(ℝ≥0, ℝ)} (hP : P ∈ searcherPaths) (t t' : ℝ≥0) :
    P t' - |(t : ℝ) - t'| ≤ P t ∧ P t ≤ P t' + |(t : ℝ) - t'| := by
  have := abs_le.mp (hP.2 t t')
  constructor <;> linarith [this.1, this.2]

/-- The speed limit from time `0`. -/
lemma s3b_lip0 {P : C(ℝ≥0, ℝ)} (hP : P ∈ searcherPaths) (t : ℝ≥0) :
    P 0 - t ≤ P t ∧ P t ≤ P 0 + t := by
  have h := s3b_lip hP t 0
  rwa [NNReal.coe_zero, sub_zero, abs_of_nonneg (NNReal.coe_nonneg t)] at h

/-- If the searcher reaches `-1` at time `b` before reaching `+1`, he needs `2` more time units to
reach `+1`: `T(P, E) ≥ T(P, -E) + 2`. -/
lemma s3b_E_ge {P : C(ℝ≥0, ℝ)} (hP : P ∈ searcherPaths) {b : ℝ≥0} (hPb : P b = -1)
    (hb : captureTime P (-hiderE) = b) (hle : captureTime P (-hiderE) ≤ captureTime P hiderE) :
    ENNReal.ofReal (b + 2) ≤ captureTime P hiderE := by
  apply s3b_ofReal_le
  intro t ht heq
  change P t = 1 at heq
  rcases lt_or_ge t b with htb | htb
  · have h1 : captureTime P hiderE ≤ t := captureTime_le heq
    have h2 : (t : ℝ≥0∞) < b := ENNReal.coe_lt_coe.mpr htb
    rw [hb] at hle
    exact absurd (hle.trans h1) (not_le.mpr h2)
  · have h := (s3b_lip hP t b).2
    have htb' : (b : ℝ) ≤ t := htb
    rw [hPb, heq, abs_of_nonneg (by linarith)] at h
    linarith

section Theorem10

variable {ε : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100)
include hε hε1

/-- Start at the end `1`. Departure from the paper: the paper cites Proposition 1 ("it is
optimal to adopt strategy `A`"); here the six capture times are bounded directly from the speed
limit, `P t ≥ 1 - t`. -/
lemma s3b_start_one {P : C(ℝ≥0, ℝ)} (hP : P ∈ searcherPaths) (h0 : P 0 = 1) :
    ENNReal.ofReal (97 / 75 - 7 * ε / 25) ≤ s3b_pay ε P := by
  have hlow : ∀ t : ℝ≥0, 1 - (t : ℝ) ≤ P t := fun t => by
    have := (s3b_lip0 hP t).1; rwa [h0] at this
  refine s3b_pay_ge (ca := 0) (cb := 2) (cf := 1 - ε / 2) (cf' := 2) (cg := 1 - 3 * ε / 2)
    (cg' := 2) le_rfl (by norm_num) (by linarith) (by norm_num) (by linarith) (by norm_num)
    (by simp) ?_ ?_ ?_ ?_ ?_ (by linarith)
  · refine s3b_ofReal_le fun t ht => ne_of_gt ?_
    change (-1 : ℝ) < P t
    linarith [hlow t]
  · refine s3b_ofReal_le fun t ht => ne_of_gt ?_
    change max 0 (min 1 ((t : ℝ) + ε - 1)) < P t
    have := hlow t; have := t.2; s3b_lin
  · refine s3b_ofReal_le fun t ht => ne_of_gt ?_
    change -max 0 (min 1 ((t : ℝ) + ε - 1)) < P t
    have := hlow t; have := t.2; s3b_lin
  · refine s3b_ofReal_le fun t ht => ne_of_gt ?_
    change min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε)) < P t
    have := hlow t; have := t.2; s3b_lin
  · refine s3b_ofReal_le fun t ht => ne_of_gt ?_
    change -min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε)) < P t
    have := hlow t; have := t.2; s3b_lin

/-- Start at the centre `0`, reaching `-1` no later than `+1`. -/
lemma s3b_start_zero {P : C(ℝ≥0, ℝ)} (hP : P ∈ searcherPaths) (h0 : P 0 = 0)
    (hle : captureTime P (-hiderE) ≤ captureTime P hiderE) :
    ENNReal.ofReal (97 / 75 - 7 * ε / 25) ≤ s3b_pay ε P := by
  by_cases htop : captureTime P (-hiderE) = ⊤
  · rw [s3b_pay_top (Or.inr htop)]; exact le_top
  obtain ⟨b, hPb, hb⟩ := exists_eq_captureTime htop
  change P b = -1 at hPb
  have hup : ∀ t : ℝ≥0, P t ≤ t := fun t => by
    have := (s3b_lip0 hP t).2; rw [h0] at this; linarith
  have hlo : ∀ t : ℝ≥0, -(t : ℝ) ≤ P t := fun t => by
    have := (s3b_lip0 hP t).1; rw [h0] at this; linarith
  have hb1 : (1 : ℝ) ≤ b := by linarith [hlo b]
  have ha := s3b_E_ge hP hPb hb hle
  have hbb : ENNReal.ofReal b ≤ captureTime P (-hiderE) := by
    rw [hb, ENNReal.ofReal_coe_nnreal]
  have hg : ENNReal.ofReal ((1 - ε) / 2) ≤ captureTime P (hiderG ε) :=
    s3b_ofReal_le fun t ht => ne_of_lt (by
      change P t < min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))
      have := hup t; have := t.2; s3b_lin)
  have hg' : ENNReal.ofReal ((1 - ε) / 2) ≤ captureTime P (-hiderG ε) :=
    s3b_ofReal_le fun t ht => ne_of_gt (by
      change -min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε)) < P t
      have := hlo t; have := t.2; s3b_lin)
  rcases le_or_gt (181 / 100 : ℝ) b with hb2 | hb2
  · exact s3b_pay_ge (ca := b + 2) (cb := b) (cf := 0) (cf' := 0) (cg := (1 - ε) / 2)
      (cg' := (1 - ε) / 2) (by positivity) b.2 le_rfl le_rfl (by linarith) (by linarith)
      ha hbb (by simp) (by simp) hg hg' (by linarith)
  · -- `P` cannot meet `G` before `b` (that would force `b ≥ 2 - ε`), and after `b` it stays
    -- below `G` until it reaches `+1`
    have hg2 : ENNReal.ofReal (b + 2) ≤ captureTime P (hiderG ε) :=
      s3b_ofReal_le fun t ht => ne_of_lt (by
        change P t < min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))
        have h1 := hup t
        have h2 := (s3b_lip hP t b).2
        have := t.2
        rw [hPb] at h2
        rcases le_total (t : ℝ) b with htb | htb
        · rw [abs_of_nonpos (by linarith)] at h2; s3b_lin
        · rw [abs_of_nonneg (by linarith)] at h2; s3b_lin)
    exact s3b_pay_ge (ca := b + 2) (cb := b) (cf := 0) (cf' := 0) (cg := b + 2)
      (cg' := (1 - ε) / 2) (by positivity) b.2 le_rfl le_rfl (by positivity) (by linarith)
      ha hbb (by simp) (by simp) hg2 hg' (by linarith)

/-- Start at `1/2`. -/
lemma s3b_start_half {P : C(ℝ≥0, ℝ)} (hP : P ∈ searcherPaths) (h0 : P 0 = 1 / 2) :
    ENNReal.ofReal (97 / 75 - 7 * ε / 25) ≤ s3b_pay ε P := by
  have hup : ∀ t : ℝ≥0, P t ≤ 1 / 2 + t := fun t => by
    have := (s3b_lip0 hP t).2; rwa [h0] at this
  have hlo : ∀ t : ℝ≥0, 1 / 2 - (t : ℝ) ≤ P t := fun t => by
    have := (s3b_lip0 hP t).1; rwa [h0] at this
  have hf : ENNReal.ofReal (1 / 2) ≤ captureTime P (hiderF ε) :=
    s3b_ofReal_le fun t ht => ne_of_gt (by
      change max 0 (min 1 ((t : ℝ) + ε - 1)) < P t
      have := hlo t; have := t.2; s3b_lin)
  have hf' : ENNReal.ofReal (1 / 2) ≤ captureTime P (-hiderF ε) :=
    s3b_ofReal_le fun t ht => ne_of_gt (by
      change -max 0 (min 1 ((t : ℝ) + ε - 1)) < P t
      have := hlo t; have := t.2; s3b_lin)
  have hg' : ENNReal.ofReal (3 / 4 - ε / 2) ≤ captureTime P (-hiderG ε) :=
    s3b_ofReal_le fun t ht => ne_of_gt (by
      change -min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε)) < P t
      have := hlo t; have := t.2; s3b_lin)
  have hg : ENNReal.ofReal 0 ≤ captureTime P (hiderG ε) := by simp
  rcases le_or_gt (captureTime P (-hiderE)) (captureTime P hiderE) with hle | hlt
  · -- `-1` is reached first
    by_cases htop : captureTime P (-hiderE) = ⊤
    · rw [s3b_pay_top (Or.inr htop)]; exact le_top
    obtain ⟨b, hPb, hb⟩ := exists_eq_captureTime htop
    change P b = -1 at hPb
    have hb1 : (3 / 2 : ℝ) ≤ b := by linarith [hlo b]
    have ha := s3b_E_ge hP hPb hb hle
    have hbb : ENNReal.ofReal b ≤ captureTime P (-hiderE) := by
      rw [hb, ENNReal.ofReal_coe_nnreal]
    exact s3b_pay_ge (ca := b + 2) (cb := b) (cf := 1 / 2) (cf' := 1 / 2) (cg := 0)
      (cg' := 3 / 4 - ε / 2) (by positivity) b.2 (by norm_num) (by norm_num) le_rfl
      (by linarith) ha hbb hf hf' hg hg' (by linarith)
  · -- `+1` is reached first, at time `a`
    obtain ⟨a, hPa, ha⟩ := exists_eq_captureTime (ne_top_of_lt hlt)
    change P a = 1 at hPa
    have ha1 : (1 / 2 : ℝ) ≤ a := by linarith [hup a]
    have haa : ENNReal.ofReal a ≤ captureTime P hiderE := by
      rw [ha, ENNReal.ofReal_coe_nnreal]
    have hb : ENNReal.ofReal (a + 2) ≤ captureTime P (-hiderE) := by
      have h := s3b_E_ge (P := -P) (neg_mem_searcherPaths hP) (b := a)
        (by simp [hPa]) (by rw [captureTime_neg, ha])
        (by rw [captureTime_neg, s3b_captureTime_neg_left]; exact hlt.le)
      rwa [s3b_captureTime_neg_left] at h
    rcases le_or_gt (3 / 2 : ℝ) a with ha2 | ha2
    · exact s3b_pay_ge (ca := a) (cb := a + 2) (cf := 1 / 2) (cf' := 1 / 2) (cg := 0)
        (cg' := 3 / 4 - ε / 2) a.2 (by positivity) (by norm_num) (by norm_num) le_rfl
        (by linarith) haa hb hf hf' hg hg' (by linarith)
    · -- before `a` the searcher stays above `(3/2 - a)/2 > 0` and cannot meet `F` (that would
      -- force `a ≥ 2 - ε`); after `a` he is above `1 + a - t`
      have hL : ∀ t : ℝ≥0, 1 - |(t : ℝ) - a| ≤ P t := fun t => by
        have := (s3b_lip hP t a).1; rwa [hPa] at this
      have hf2 : ENNReal.ofReal (1 + a / 2 - ε / 2) ≤ captureTime P (hiderF ε) :=
        s3b_ofReal_le fun t ht => ne_of_gt (by
          change max 0 (min 1 ((t : ℝ) + ε - 1)) < P t
          have h1 := hlo t; have h2 := hL t; have := t.2
          rcases le_total (t : ℝ) a with hta | hta
          · rw [abs_of_nonpos (by linarith)] at h2; s3b_lin
          · rw [abs_of_nonneg (by linarith)] at h2; s3b_lin)
      have hf2' : ENNReal.ofReal (a + 2) ≤ captureTime P (-hiderF ε) :=
        s3b_ofReal_le fun t ht => ne_of_gt (by
          change -max 0 (min 1 ((t : ℝ) + ε - 1)) < P t
          have h1 := hlo t; have h2 := hL t; have := t.2
          rcases le_total (t : ℝ) a with hta | hta
          · rw [abs_of_nonpos (by linarith)] at h2; s3b_lin
          · rw [abs_of_nonneg (by linarith)] at h2; s3b_lin)
      have hg2' : ENNReal.ofReal (a + 2) ≤ captureTime P (-hiderG ε) :=
        s3b_ofReal_le fun t ht => ne_of_gt (by
          change -min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε)) < P t
          have h1 := hlo t; have h2 := hL t; have := t.2
          rcases le_total (t : ℝ) a with hta | hta
          · rw [abs_of_nonpos (by linarith)] at h2; s3b_lin
          · rw [abs_of_nonneg (by linarith)] at h2; s3b_lin)
      exact s3b_pay_ge (ca := a) (cb := a + 2) (cf := 1 + a / 2 - ε / 2) (cf' := a + 2)
        (cg := 0) (cg' := a + 2) a.2 (by positivity) (by linarith) (by positivity) le_rfl
        (by positivity) haa hb hf2 hf2' hg hg2' (by linarith)

/-- The bound for every start at a hider's starting point `±1`, `0`, `±1/2`, by reflection. -/
lemma s3b_bound {P : C(ℝ≥0, ℝ)} (hP : P ∈ searcherPaths)
    (h0 : P 0 = 1 ∨ P 0 = -1 ∨ P 0 = 0 ∨ P 0 = 1 / 2 ∨ P 0 = -(1 / 2)) :
    ENNReal.ofReal (97 / 75 - 7 * ε / 25) ≤ s3b_pay ε P := by
  have hP' := neg_mem_searcherPaths hP
  rcases h0 with h | h | h | h | h
  · exact s3b_start_one hε hε1 hP h
  · rw [← s3b_pay_neg ε P]
    exact s3b_start_one hε hε1 hP' (by simp [h])
  · rcases le_total (captureTime P (-hiderE)) (captureTime P hiderE) with hle | hle
    · exact s3b_start_zero hε hε1 hP h hle
    · rw [← s3b_pay_neg ε P]
      refine s3b_start_zero hε hε1 hP' (by simp [h]) ?_
      rw [s3b_captureTime_neg_left, s3b_captureTime_neg_left, neg_neg]
      exact hle
  · exact s3b_start_half hε hε1 hP h
  · rw [← s3b_pay_neg ε P]
    exact s3b_start_half hε hε1 hP' (by simp [h])

end Theorem10

/-- The six hider paths `E, -E, F, -F, G, -G` of the strategy of Theorem 10. -/
noncomputable def s3b_hs (ε : ℝ) : Fin 6 → C(ℝ≥0, ℝ) :=
  ![hiderE, -hiderE, hiderF ε, -hiderF ε, hiderG ε, -hiderG ε]

lemma s3b_hs_mem {ε : ℝ} (hε : 0 ≤ ε) (hε1 : ε ≤ 1 / 4) (j : Fin 6) :
    s3b_hs ε j ∈ searcherPaths := by
  have hF := hiderF_mem (ε := ε)
  have hG := hiderG_mem hε
  fin_cases j
  exacts [hiderE_mem, neg_mem_searcherPaths hiderE_mem, hF, neg_mem_searcherPaths hF, hG,
    neg_mem_searcherPaths hG]

/-- The hider paths start at `±1`, `0` and `±1/2`. -/
lemma s3b_hs_zero {ε : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (j : Fin 6) :
    s3b_hs ε j 0 = 1 ∨ s3b_hs ε j 0 = -1 ∨ s3b_hs ε j 0 = 0 ∨ s3b_hs ε j 0 = 1 / 2 ∨
      s3b_hs ε j 0 = -(1 / 2) := by
  have hF : hiderF ε 0 = 0 := by
    change max 0 (min 1 (((0 : ℝ≥0) : ℝ) + ε - 1)) = 0
    rw [NNReal.coe_zero]; s3b_lin
  have hG : hiderG ε 0 = 1 / 2 := by
    change min 1 (max (min (1 / 2) (1 - ε - ((0 : ℝ≥0) : ℝ))) (((0 : ℝ≥0) : ℝ) - 1 + 3 * ε)) =
      1 / 2
    rw [NNReal.coe_zero]; s3b_lin
  fin_cases j
  · exact Or.inl rfl
  · exact Or.inr (Or.inl rfl)
  · exact Or.inr (Or.inr (Or.inl hF))
  · refine Or.inr (Or.inr (Or.inl ?_))
    change -hiderF ε 0 = 0
    rw [hF, neg_zero]
  · exact Or.inr (Or.inr (Or.inr (Or.inl hG)))
  · refine Or.inr (Or.inr (Or.inr (Or.inr ?_)))
    change -hiderG ε 0 = -(1 / 2)
    rw [hG]

/-- Every searcher path concedes at least `97/75 - 7ε/25` against the strategy of Theorem 10:
by Proposition 5 it is dominated by a greedy path, which starts at a hider's starting point. -/
lemma s3b_lintegral_ge {ε : ℝ} (hε : 0 < ε) (hε1 : ε ≤ 1 / 100) (S : searcherPaths) :
    ENNReal.ofReal (97 / 75 - 7 * ε / 25) ≤ ∫⁻ H, captureTime S H ∂(strategy10 ε) := by
  rw [s3b_lintegral hε.le (by linarith) S]
  have hmem := s3b_hs_mem hε.le (by linarith)
  obtain ⟨σ, hσ⟩ := proposition5 (s3b_hs ε) hmem S.2
  have hGr : greedyOrder (s3b_hs ε) σ ∈ searcherPaths := greedyOrder_mem hmem σ
  have h0 := s3b_hs_zero hε hε1 (σ 0)
  rw [← s3b_greedyOrder_zero] at h0
  refine (s3b_bound hε hε1 hGr h0).trans ?_
  unfold s3b_pay
  gcongr
  exacts [hσ 0, hσ 1, hσ 2, hσ 3, hσ 4, hσ 5]

/-- **Theorem 10** (`thm:10`). `V ≥ 97/75`: for every `δ > 0` and every small enough `ε > 0`,
the hider strategy of the matrix game keeps the expected capture time above `97/75 - δ` against
every searcher path, so the lower value is at least `97/75`.

Proof (the paper's, made rigorous): by Proposition 5 the searcher's response to the six hider
paths `±E, ±F, ±G` (the column `H` has weight `0`) is dominated by a greedy path, which starts
where one of them starts, at `±1`, `0` or `±1/2`; by symmetry the starts `1`, `0`, `1/2` suffice.
The six capture times are then bounded case by case, giving an expected capture time of at least
`97/75 - 7ε/25` against every searcher path. The weights are the optimal hider strategy `q` of
`matrix4_value`; the entries of (4) (`equation4`) are not needed for the bound.

Departure from the paper: for the start at an end the paper cites Proposition 1 ("it is optimal
to adopt strategy `A`"); here the six capture times of any path starting at `1` are bounded
directly from the speed limit (`s3b_start_one`), so Proposition 1 is not used. -/
theorem theorem10 :
    (∀ δ : ℝ≥0∞, 0 < δ → ∀ᶠ ε in 𝓝[>] (0 : ℝ), ∀ S : searcherPaths,
        97 / 75 ≤ ∫⁻ H, captureTime S H ∂(strategy10 ε) + δ) ∧
      (97 / 75 : ℝ≥0∞) ≤ lowerValue := by
  have key : ∀ δ : ℝ≥0∞, 0 < δ → ∀ᶠ ε in 𝓝[>] (0 : ℝ), ∀ S : searcherPaths,
      97 / 75 ≤ ∫⁻ H, captureTime S H ∂(strategy10 ε) + δ := by
    intro δ hδ
    by_cases hδt : δ = ⊤
    · exact Eventually.of_forall fun ε S => by rw [hδt, add_top]; exact le_top
    have hδr : 0 < δ.toReal := ENNReal.toReal_pos hδ.ne' hδt
    filter_upwards [Ioo_mem_nhdsGT (show (0 : ℝ) < min (1 / 100) δ.toReal by positivity)]
      with ε hε S
    have hε1 : ε ≤ 1 / 100 := hε.2.le.trans (min_le_left _ _)
    have hεδ : ε < δ.toReal := hε.2.trans_le (min_le_right _ _)
    calc (97 / 75 : ℝ≥0∞) = ENNReal.ofReal ((97 / 75 - 7 * ε / 25) + 7 * ε / 25) := by
          rw [sub_add_cancel, ENNReal.ofReal_div_of_pos (by norm_num)]; simp
      _ ≤ ENNReal.ofReal (97 / 75 - 7 * ε / 25) + ENNReal.ofReal (7 * ε / 25) :=
          ENNReal.ofReal_add_le
      _ ≤ ∫⁻ H, captureTime S H ∂(strategy10 ε) + δ :=
          add_le_add (s3b_lintegral_ge hε.1 hε1 S)
            (ENNReal.ofReal_le_of_le_toReal (by linarith [hε.1]))
  refine ⟨key, ENNReal.le_of_forall_pos_le_add fun η hη _ => ?_⟩
  obtain ⟨ε, hε⟩ := (key η (ENNReal.coe_pos.mpr hη)).exists
  calc (97 / 75 : ℝ≥0∞) ≤ (⨅ S : searcherPaths, ∫⁻ H, captureTime S H ∂(strategy10 ε)) + η := by
        rw [ENNReal.iInf_add]; exact le_iInf hε
    _ ≤ lowerValue + η := by
        gcongr
        exact le_iSup_of_le (⟨strategy10 ε, inferInstance⟩ : ProbabilityMeasure hiderPaths)
          le_rfl

end PrincessMonster
