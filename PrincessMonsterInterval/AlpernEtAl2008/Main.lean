module

public import PrincessMonsterInterval.Value
public import PrincessMonsterInterval.AlpernEtAl2008.Section3.Theorem9
public import PrincessMonsterInterval.AlpernEtAl2008.Section3.Theorem10
public import PrincessMonsterInterval.AlpernEtAl2008.Section4.Theorem14
public import PrincessMonsterInterval.AlpernEtAl2008.Section5.Theorem16

/-!
# The main result: `15/11 ≤ V ≤ 13/9`

Abstract and Section 6: the princess and monster game on `[-1, 1]` has a value `V` with
`15/11 ≤ V ≤ 13/9`. In particular `1 < V < 3/2`: the game is not trivial. Section 3 announces
`1 < 97/75 < V < 47/32 < 3/2`.
-/

@[expose] public section

open scoped NNReal ENNReal

namespace PrincessMonsterInterval

/-- **Main theorem** (`main`). The game has a value `V`, and `15/11 ≤ V ≤ 13/9`. -/
theorem main : ∃ V : ℝ≥0∞, HasValue V ∧ 15 / 11 ≤ V ∧ V ≤ 13 / 9 := by
  refine ⟨upperValue, ⟨value_exists.1, rfl⟩, ?_, theorem14.2⟩
  rw [← value_exists.1]
  exact theorem16.2

/-- **Section 3** (`sec:3`). `1 < 97/75 < V < 47/32 < 3/2`. The strict inequalities need the
bounds of Sections 4 and 5: the strategies of Section 3 give only `97/75 ≤ V ≤ 47/32`. -/
theorem section3_bounds :
    ∃ V : ℝ≥0∞, HasValue V ∧ 1 < (97 / 75 : ℝ≥0∞) ∧ 97 / 75 < V ∧ V < 47 / 32 ∧
      (47 / 32 : ℝ≥0∞) < 3 / 2 := by
  have frac_lt : ∀ {a b c d : ℕ}, 0 < b → 0 < d → (a : ℝ) / b < c / d →
      (a : ℝ≥0∞) / b < (c : ℝ≥0∞) / d := by
    intro a b c d hb hd h
    have e : ∀ m n : ℕ, 0 < n → (m / n : ℝ≥0∞) = ENNReal.ofReal (m / n) := by
      intro m n hn
      rw [ENNReal.ofReal_div_of_pos (by exact_mod_cast hn)]
      simp
    rw [e a b hb, e c d hd, ENNReal.ofReal_lt_ofReal_iff (lt_of_le_of_lt (by positivity) h)]
    exact h
  obtain ⟨V, hV, h1, h2⟩ := main
  refine ⟨V, hV, ?_, ?_, ?_, ?_⟩
  · simpa using frac_lt (a := 1) (b := 1) (c := 97) (d := 75) (by norm_num) (by norm_num)
      (by norm_num)
  · refine lt_of_lt_of_le ?_ h1
    simpa using frac_lt (a := 97) (b := 75) (c := 15) (d := 11) (by norm_num) (by norm_num)
      (by norm_num)
  · refine lt_of_le_of_lt h2 ?_
    simpa using frac_lt (a := 13) (b := 9) (c := 47) (d := 32) (by norm_num) (by norm_num)
      (by norm_num)
  · simpa using frac_lt (a := 47) (b := 32) (c := 3) (d := 2) (by norm_num) (by norm_num)
      (by norm_num)

end PrincessMonsterInterval
