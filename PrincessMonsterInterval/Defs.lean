module

public import Mathlib.MeasureTheory.Constructions.BorelSpace.ContinuousMap
public import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
public import Mathlib.Topology.ContinuousMap.Ordered

/-!
# The princess and monster game on the interval: definitions

Alpern, Fokkink, Lindelauf, Olsder, *The "Princess and Monster" game on an interval*,
SIAM J. Control Optim. 47 (2008), 1178–1190, Section 1 and the start of Section 2.

* `hiderPaths`: the hider's pure strategies, the continuous paths `H : [0,∞) → I = [-1,1]`.
* `searcherPaths`: the searcher's pure strategies, the paths `S : [0,∞) → I` with
  `|S t - S t'| ≤ |t - t'|` (equation (2)).
* `captureTime S H`: the capture time `T(S,H) = min {t : S t = H t}` (equation (1)), equal to
  `∞` when the paths never meet.
* `upperValue`, `lowerValue`: the upper and lower values of the game in mixed strategies, that
  is in probability measures on the Borel σ-algebras of the strategy spaces, each carrying the
  topology of uniform convergence on compact sets (the compact-open topology of `C(ℝ≥0, ℝ)`).

Representation: a path is an element of `C(ℝ≥0, ℝ)` (time `[0,∞)` is `ℝ≥0`) whose values lie
in `I`; a strategy space is a subset of `C(ℝ≥0, ℝ)`, so that the searcher's paths are hider
paths too, as in the paper. Payoffs take values in `ℝ≥0∞`, and expected payoffs are lower
Lebesgue integrals.
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

/-- The game has value `V` when its lower and upper values both equal `V`. -/
def HasValue (V : ℝ≥0∞) : Prop := lowerValue = V ∧ upperValue = V

/-- The interval `I = [-1, 1]`. -/
abbrev I : Set ℝ := Set.Icc (-1) 1

lemma searcherPaths_subset_hiderPaths : searcherPaths ⊆ hiderPaths := fun _ h => h.1

end PrincessMonsterInterval
