module

public import PrincessMonster.Section4.Lemmas

/-!
# Section 4: Theorem 14, `V ≤ 13/9`

The searcher uses the sweepers `±A` with probability `p = 7/9` and `s_Φ`, with `Φ` uniform on
`[-1, 1]`, with probability `2/9`. Against a hider path that meets a sweeper first at time `y`,
the payoff is at most `13/9 - y/18 + y²/18`. The hider's best responses are to stay at an end,
which achieves `13/9` exactly, or to run from an end to the middle and back, which achieves
`13/9` in the limit (`y → 1`).
-/

@[expose] public section

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonster

/-- **Theorem 14** (`thm:14`). If the searcher uses the mixed strategy `σ` (sweepers with
probability `7/9`, `s_Φ` with uniform `Φ` with probability `2/9`), the optimal response of the
hider gives the value `13/9`. In particular `V ≤ 13/9`. -/
theorem theorem14 :
    ⨆ H : hiderPaths, ∫⁻ S, captureTime S H ∂(sigma (7 / 9) uniformI) = 13 / 9 ∧
      upperValue ≤ 13 / 9 := by
  sorry

end PrincessMonster
