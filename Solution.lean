module

public import PrincessMonsterInterval.AlpernEtAl2008.Main
public import PrincessMonsterInterval.AlpernEtAl2008.Section2.Dominance
public import PrincessMonsterInterval.AlpernEtAl2008.Section2.Greedy
public import PrincessMonsterInterval.AlpernEtAl2008.Section2.Noncrossing
public import PrincessMonsterInterval.AlpernEtAl2008.Section4.Theorem15
public import External.AlpernAsic.Theorem3

/-!
# Solution

The Challenge's theorems, proved from the library. This module also imports every module of the
library and serves as its entry point.
-/

@[expose] public section

open scoped NNReal ENNReal

namespace PrincessMonsterInterval.Challenge

theorem value_exists : lowerValue = upperValue :=
  PrincessMonsterInterval.value_exists.1

theorem main :
    ∃ V : ℝ≥0∞, lowerValue = V ∧ upperValue = V ∧ 15 / 11 ≤ V ∧ V ≤ 13 / 9 := by
  obtain ⟨V, ⟨hl, hu⟩, h1, h2⟩ := PrincessMonsterInterval.main
  exact ⟨V, hl, hu, h1, h2⟩

end PrincessMonsterInterval.Challenge
