module

public import PrincessMonster.Value
public import PrincessMonster.Section3.Theorem9
public import PrincessMonster.Section3.Theorem10
public import PrincessMonster.Section4.Theorem14
public import PrincessMonster.Section5.Theorem16

/-!
# The main result: `15/11 ≤ V ≤ 13/9`

Abstract and Section 6: the princess and monster game on `[-1, 1]` has a value `V` with
`15/11 ≤ V ≤ 13/9`. In particular `1 < V < 3/2`: the game is not trivial. Section 3 announces
`1 < 97/75 < V < 47/32 < 3/2`.
-/

@[expose] public section

open scoped NNReal ENNReal

namespace PrincessMonster

/-- **Main theorem** (`main`). The game has a value `V`, and `15/11 ≤ V ≤ 13/9`. -/
theorem main : ∃ V : ℝ≥0∞, HasValue V ∧ 15 / 11 ≤ V ∧ V ≤ 13 / 9 := by
  sorry

/-- **Section 3** (`sec:3`). `1 < 97/75 < V < 47/32 < 3/2`. The strict inequalities need the
bounds of Sections 4 and 5: the strategies of Section 3 give only `97/75 ≤ V ≤ 47/32`. -/
theorem section3_bounds :
    ∃ V : ℝ≥0∞, HasValue V ∧ 1 < (97 / 75 : ℝ≥0∞) ∧ 97 / 75 < V ∧ V < 47 / 32 ∧
      (47 / 32 : ℝ≥0∞) < 3 / 2 := by
  sorry

end PrincessMonster
