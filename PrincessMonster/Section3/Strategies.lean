module

public import PrincessMonster.Section2.Symmetric
public import Basic.Analysis.TriangleWave

/-!
# Section 3: the strategies of Figures 1 and 2

Searcher paths (they turn back at the ends; `Real.triangleWave` folds a unit-speed motion on `ℝ`
onto `[-1, 1]`):
* `sweeperA`: the sweeper `A(t) = 1 - t`, from `+1` to `-1` and back; `-A` is its reflection;
* `stratB`: start at `0`, run left, join `-A` at time `1/2`, run to `+1`, then to `-1`;
* `stratC`, `stratD`: start at `1/2`, run to the near end (`C`) or the remote end (`D`) and back;
* `stratM`: start at `0`, run to the end `-1` and back.

Hider paths, with the parameter `ε > 0` of the paper:
* `hiderE`: wait at the end `+1`;
* `hiderF ε`: `F(t) = max {0, t + ε - 1}`: loiter at the centre until `1 - ε`, then run to `+1`;
* `hiderG ε`: wait at `1/2` until the sweeper `A` is `ε`-close (time `1/2 - ε`), run towards the
  middle just ahead of it, turn at `ε` and run back to the end `+1`;
* `hiderH ε`: wait at `1/2` until time `1/2 - ε`, then run to the end `+1`.
-/

@[expose] public section

open scoped NNReal ENNReal
open MeasureTheory

namespace PrincessMonster

/-- The sweeper `A`: start at `+1` and run to `-1` (`A(t) = 1 - t`), and back. -/
noncomputable def sweeperA : C(ℝ≥0, ℝ) :=
  pathOf (fun t => Real.triangleWave (1 - t)) (by fun_prop)

/-- Strategy `B`: start at `0`, run left, join the sweeper `-A` from time `1/2`, reach `+1` at
time `2`, then run to `-1`. -/
noncomputable def stratB : C(ℝ≥0, ℝ) :=
  pathOf (fun t => Real.triangleWave (|t - 1 / 2| - 1 / 2)) (by fun_prop)

/-- Strategy `C`: start at `1/2` and run to the near end `+1`, then to `-1`. -/
noncomputable def stratC : C(ℝ≥0, ℝ) :=
  pathOf (fun t => Real.triangleWave (1 / 2 + t)) (by fun_prop)

/-- Strategy `D`: start at `1/2` and run to the remote end `-1`, then to `+1`. -/
noncomputable def stratD : C(ℝ≥0, ℝ) :=
  pathOf (fun t => Real.triangleWave (1 / 2 - t)) (by fun_prop)

/-- Strategy `M`: start at `0`, run to the end `-1` and back. -/
noncomputable def stratM : C(ℝ≥0, ℝ) :=
  pathOf (fun t => Real.triangleWave (-t)) (by fun_prop)

/-- Hider `E`: wait at the end `+1`. -/
noncomputable def hiderE : C(ℝ≥0, ℝ) := ContinuousMap.const _ 1

/-- Hider `F`: `F(t) = max {0, t + ε - 1}` (until it reaches `+1`). -/
noncomputable def hiderF (ε : ℝ) : C(ℝ≥0, ℝ) :=
  pathOf (fun t => max 0 (min 1 (t + ε - 1))) (by fun_prop)

/-- Hider `G`: wait at `1/2` until time `1/2 - ε`, run towards the middle just ahead of the
sweeper `A`, turn at `ε` (time `1 - 2ε`) and run back to `+1`. -/
noncomputable def hiderG (ε : ℝ) : C(ℝ≥0, ℝ) :=
  pathOf (fun t => min 1 (max (min (1 / 2) (1 - ε - t)) (t - 1 + 3 * ε))) (by fun_prop)

/-- Hider `H`: wait at `1/2` until time `1/2 - ε`, then run to the end `+1`. -/
noncomputable def hiderH (ε : ℝ) : C(ℝ≥0, ℝ) :=
  pathOf (fun t => min 1 (max (1 / 2) (t + ε))) (by fun_prop)

lemma abs_min_sub_min_le_of {a b c d e : ℝ} (h1 : |a - c| ≤ e) (h2 : |b - d| ≤ e) :
    |min a b - min c d| ≤ e :=
  (abs_min_sub_min_le_max a b c d).trans (max_le h1 h2)

lemma abs_max_sub_max_le_of {a b c d e : ℝ} (h1 : |a - c| ≤ e) (h2 : |b - d| ≤ e) :
    |max a b - max c d| ≤ e :=
  (abs_max_sub_max_le_max a b c d).trans (max_le h1 h2)

/-- A unit-speed motion folded by the triangle wave is a searcher path. -/
lemma pathOf_triangleWave_mem {g : ℝ → ℝ} (hg : Continuous g) (hL : ∀ s t, |g s - g t| ≤ |s - t|) :
    pathOf (fun t => Real.triangleWave (g t)) (by fun_prop) ∈ searcherPaths :=
  pathOf_mem_searcherPaths _
    (fun s t => (Real.abs_triangleWave_sub_le _ _).trans (hL s t))
    (fun _ _ => Real.triangleWave_mem_Icc _)

lemma sweeperA_mem : sweeperA ∈ searcherPaths :=
  pathOf_triangleWave_mem (by fun_prop) fun s t => by
    rw [show 1 - s - (1 - t) = -(s - t) by ring, abs_neg]

lemma stratB_mem : stratB ∈ searcherPaths :=
  pathOf_triangleWave_mem (by fun_prop) fun s t => by
    rw [show |s - 1 / 2| - 1 / 2 - (|t - 1 / 2| - 1 / 2) = |s - 1 / 2| - |t - 1 / 2| by ring]
    exact (abs_abs_sub_abs_le_abs_sub _ _).trans (le_of_eq (by ring_nf))

lemma stratC_mem : stratC ∈ searcherPaths :=
  pathOf_triangleWave_mem (by fun_prop) fun s t => by ring_nf; exact le_rfl

lemma stratD_mem : stratD ∈ searcherPaths :=
  pathOf_triangleWave_mem (by fun_prop) fun s t => by
    rw [show 1 / 2 - s - (1 / 2 - t) = -(s - t) by ring, abs_neg]

lemma stratM_mem : stratM ∈ searcherPaths :=
  pathOf_triangleWave_mem (by fun_prop) fun s t => by
    rw [show -s - -t = -(s - t) by ring, abs_neg]

lemma hiderE_mem : hiderE ∈ searcherPaths :=
  ⟨fun _ => by simp [hiderE], fun _ _ => by simp [hiderE]⟩

lemma hiderF_mem {ε : ℝ} : hiderF ε ∈ searcherPaths :=
  pathOf_mem_searcherPaths _
    (fun s t => abs_max_sub_max_le_of (by simp)
      (abs_min_sub_min_le_of (by simp) (le_of_eq (by ring_nf))))
    (fun t _ => ⟨by linarith [le_max_left 0 (min 1 (t + ε - 1))],
      max_le (by norm_num) (min_le_left _ _)⟩)

lemma hiderG_mem {ε : ℝ} (hε : 0 ≤ ε) : hiderG ε ∈ searcherPaths :=
  pathOf_mem_searcherPaths _
    (fun s t => abs_min_sub_min_le_of (by simp)
      (abs_max_sub_max_le_of (abs_min_sub_min_le_of (by simp)
        (by rw [show 1 - ε - s - (1 - ε - t) = -(s - t) by ring, abs_neg]))
        (le_of_eq (by ring_nf))))
    (fun t ht => ⟨le_min (by norm_num) (le_max_of_le_right (by linarith)), min_le_left _ _⟩)

lemma hiderH_mem {ε : ℝ} : hiderH ε ∈ searcherPaths :=
  pathOf_mem_searcherPaths _
    (fun s t => abs_min_sub_min_le_of (by simp)
      (abs_max_sub_max_le_of (by simp) (le_of_eq (by ring_nf))))
    (fun t _ => ⟨le_min (by norm_num) (le_max_of_le_left (by norm_num)), min_le_left _ _⟩)

open scoped Classical in
/-- A searcher path as a point of the strategy space (the junk value `A` for non-members). -/
noncomputable def toSearcher (S : C(ℝ≥0, ℝ)) : searcherPaths :=
  if h : S ∈ searcherPaths then ⟨S, h⟩ else ⟨sweeperA, sweeperA_mem⟩

open scoped Classical in
/-- A hider path as a point of the strategy space (the junk value `E` for non-members). -/
noncomputable def toHider (H : C(ℝ≥0, ℝ)) : hiderPaths :=
  if h : H ∈ hiderPaths then ⟨H, h⟩ else ⟨hiderE, searcherPaths_subset_hiderPaths hiderE_mem⟩

/-- The mixed strategy that uses the searcher path `S` and its reflection `-S` with probability
`1/2` each. -/
noncomputable def symDiracS (S : C(ℝ≥0, ℝ)) : Measure searcherPaths :=
  (1 / 2 : ℝ≥0∞) • (Measure.dirac (toSearcher S) + Measure.dirac (toSearcher (-S)))

/-- The mixed strategy that uses the hider path `H` and its reflection `-H` with probability
`1/2` each. -/
noncomputable def symDiracH (H : C(ℝ≥0, ℝ)) : Measure hiderPaths :=
  (1 / 2 : ℝ≥0∞) • (Measure.dirac (toHider H) + Measure.dirac (toHider (-H)))

end PrincessMonster
