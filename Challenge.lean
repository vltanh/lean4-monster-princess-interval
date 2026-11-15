module

public import Mathlib.MeasureTheory.Constructions.BorelSpace.ContinuousMap
public import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
public import Mathlib.Topology.ContinuousMap.Ordered

/-!
# Challenge: the princess and monster game on an interval

S. Alpern, R. Fokkink, R. Lindelauf, G.-J. Olsder, *The "Princess and Monster" game on an
interval*, SIAM J. Control Optim. 47 (2008), 1178–1190.

A searcher (the monster) and a hider (the princess) move in the interval `I = [-1, 1]` without
seeing each other. The hider chooses a continuous path `H : [0, ∞) → I`; the searcher chooses a
path `S : [0, ∞) → I` of speed at most `1`, that is `|S t - S t'| ≤ |t - t'|`. The payoff, which
the searcher pays to the hider, is the capture time `T(S, H) = min {t : S t = H t}` (`∞` if the
paths never meet). Mixed strategies are Borel probability measures on the spaces of paths, with
the topology of uniform convergence on compact sets (the compact-open topology of `C(ℝ≥0, ℝ)`);
the expected payoff is a lower Lebesgue integral in `[0, ∞]`.

Conventions: time `[0, ∞)` is `ℝ≥0`; a path is an element of `C(ℝ≥0, ℝ)` with values in `I`;
`upperValue` is `inf_μ sup_H E_μ T(·, H)` over searcher mixed strategies `μ` and hider paths `H`;
`lowerValue` is `sup_ν inf_S E_ν T(S, ·)` over hider mixed strategies `ν` and searcher paths `S`.

* `value_exists`: the game has a value (lower value = upper value). The paper takes this from the
  minimax theorem of Alpern and Gal (1988).
* `main`: the value `V` satisfies `15/11 ≤ V ≤ 13/9` (Theorems 14 and 16, the abstract).
-/

@[expose] public section

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonsterInterval

-- BEGIN SHARED DEFINITIONS

/-- The hider's pure strategies: continuous paths `H : [0,∞) → [-1,1]`. -/
def hiderPaths : Set C(ℝ≥0, ℝ) :=
  {H | ∀ t, H t ∈ Set.Icc (-1 : ℝ) 1}

/-- The searcher's pure strategies (equation (2)): paths `S : [0,∞) → [-1,1]` with
`|S t - S t'| ≤ |t - t'|`. -/
def searcherPaths : Set C(ℝ≥0, ℝ) :=
  {S | (∀ t, S t ∈ Set.Icc (-1 : ℝ) 1) ∧ ∀ t t' : ℝ≥0, |S t - S t'| ≤ |(t : ℝ) - t'|}

/-- The capture time `T(S,H) = min {t : S t = H t}` (equation (1)); it is `∞` when the two paths
never meet. -/
noncomputable def captureTime (S H : C(ℝ≥0, ℝ)) : ℝ≥0∞ :=
  ⨅ (t : ℝ≥0) (_ : S t = H t), (t : ℝ≥0∞)

/-- The upper value of the game: the infimum, over the searcher's mixed strategies `μ`, of the
largest expected capture time that a pure hider strategy achieves against `μ`. -/
noncomputable def upperValue : ℝ≥0∞ :=
  ⨅ μ : ProbabilityMeasure searcherPaths, ⨆ H : hiderPaths,
    ∫⁻ S, captureTime S H ∂(μ : Measure searcherPaths)

/-- The lower value of the game: the supremum, over the hider's mixed strategies `ν`, of the
smallest expected capture time that a pure searcher strategy achieves against `ν`. -/
noncomputable def lowerValue : ℝ≥0∞ :=
  ⨆ ν : ProbabilityMeasure hiderPaths, ⨅ S : searcherPaths,
    ∫⁻ H, captureTime S H ∂(ν : Measure hiderPaths)

-- END SHARED DEFINITIONS

end PrincessMonsterInterval

namespace PrincessMonsterInterval.Challenge

/-- The princess and monster game on `[-1, 1]` has a value: its lower and upper values in mixed
strategies coincide. -/
theorem value_exists : lowerValue = upperValue := by
  sorry

/-- **Main theorem.** The value `V` of the princess and monster game on `[-1, 1]` satisfies
`15/11 ≤ V ≤ 13/9`. -/
theorem main :
    ∃ V : ℝ≥0∞, lowerValue = V ∧ upperValue = V ∧ 15 / 11 ≤ V ∧ V ≤ 13 / 9 := by
  sorry

end PrincessMonsterInterval.Challenge
