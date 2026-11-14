module

public import PrincessMonster.Main
public import PrincessMonster.Section2.Dominance
public import PrincessMonster.Section2.Greedy
public import PrincessMonster.Section2.Noncrossing
public import PrincessMonster.Section4.Theorem15
public import External.AlpernAsic.Theorem3

/-!
# Solution

The Challenge's theorems, proved from the library. This module also imports every module of the
library and serves as its entry point.
-/

@[expose] public section

open scoped NNReal ENNReal

namespace PrincessMonster.Challenge

theorem value_exists : lowerValue = upperValue :=
  PrincessMonster.value_exists.1

theorem main :
    ∃ V : ℝ≥0∞, lowerValue = V ∧ upperValue = V ∧ 15 / 11 ≤ V ∧ V ≤ 13 / 9 := by
  obtain ⟨V, ⟨hl, hu⟩, h1, h2⟩ := PrincessMonster.main
  exact ⟨V, hl, hu, h1, h2⟩

end PrincessMonster.Challenge
