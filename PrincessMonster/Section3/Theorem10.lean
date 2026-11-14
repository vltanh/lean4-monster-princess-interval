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

/-- **Equation (4)** (`eq:4`). Ignoring `ε`, the strategies give the matrix (4): its entry in
row `i` and column `j` is the limit, as `ε → 0⁺`, of the average capture time of the row path
against the column path and against its reflection. -/
theorem equation4 (i : Fin 5) (j : Fin 4) :
    Tendsto (fun ε : ℝ => (captureTime (rowPath i) (colPath ε j) +
        captureTime (rowPath i) (-colPath ε j)) / 2) (𝓝[>] 0)
      (𝓝 (ENNReal.ofReal (matrix4 i j))) := by
  sorry

/-- The value of the matrix game (4) is `97/75`: the hider's mixed strategy `q` guarantees at
least `97/75` against every row, and the searcher's mixed strategy `p` concedes at most `97/75`
against every column. -/
theorem matrix4_value :
    ∃ (p : Fin 5 → ℚ) (q : Fin 4 → ℚ), (∀ i, 0 ≤ p i) ∧ ∑ i, p i = 1 ∧
      (∀ j, 0 ≤ q j) ∧ ∑ j, q j = 1 ∧
      (∀ i, 97 / 75 ≤ ∑ j, matrix4 i j * q j) ∧ (∀ j, ∑ i, p i * matrix4 i j ≤ 97 / 75) := by
  sorry

/-- The hider's mixed strategy of Theorem 10 for the parameter `ε`: it uses `E, F, G, H` with
the optimal probabilities `31/75, 24/75, 20/75, 0` of the matrix game (4), each split equally
between the path and its reflection. -/
noncomputable def strategy10 (ε : ℝ) : Measure hiderPaths :=
  (31 / 75 : ℝ≥0∞) • symDiracH hiderE + (24 / 75 : ℝ≥0∞) • symDiracH (hiderF ε) +
    (20 / 75 : ℝ≥0∞) • symDiracH (hiderG ε)

/-- **Theorem 10** (`thm:10`). `V ≥ 97/75`: for every `δ > 0` and every small enough `ε > 0`,
the hider strategy of the matrix game keeps the expected capture time above `97/75 - δ` against
every searcher path, so the lower value is at least `97/75`. -/
theorem theorem10 :
    (∀ δ : ℝ≥0∞, 0 < δ → ∀ᶠ ε in 𝓝[>] (0 : ℝ), ∀ S : searcherPaths,
        97 / 75 ≤ ∫⁻ H, captureTime S H ∂(strategy10 ε) + δ) ∧
      (97 / 75 : ℝ≥0∞) ≤ lowerValue := by
  sorry

end PrincessMonster
