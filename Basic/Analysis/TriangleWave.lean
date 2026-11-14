module

public import Mathlib.Topology.MetricSpace.HausdorffDistance
public import Mathlib.Topology.Algebra.Order.Field
public import Mathlib.Algebra.Order.Archimedean.Real.Basic

/-!
# The triangle wave

`Real.triangleWave u` folds the real line onto `[-1, 1]` by reflecting at `±1`: it equals `u` on
`[-1, 1]`, `2 - u` on `[1, 3]`, and has period `4`. It is `1`-Lipschitz. Composing an
unconstrained unit-speed motion on `ℝ` with it gives a motion in `[-1, 1]` that turns back at the
ends, which is how the searcher's end-reflecting paths are written.

The key computation is `infDist_range_four_mul_eq`: the distance from `v` to `4ℤ` is `|v - 4n|`
whenever `|v - 4n| ≤ 2`.
-/

@[expose] public section

namespace Real

/-- The triangle wave of period `4` and amplitude `1`, equal to the identity on `[-1, 1]`:
`u ↦ dist(u + 1, 4ℤ) - 1`. -/
noncomputable def triangleWave (u : ℝ) : ℝ :=
  Metric.infDist (u + 1) (Set.range fun n : ℤ => (4 * n : ℝ)) - 1

lemma lipschitzWith_triangleWave : LipschitzWith 1 triangleWave := by
  refine LipschitzWith.of_dist_le_mul fun u v => ?_
  have h := (Metric.lipschitz_infDist_pt (Set.range fun n : ℤ => (4 * n : ℝ))).dist_le_mul
    (u + 1) (v + 1)
  simp only [triangleWave, Real.dist_eq, NNReal.coe_one, one_mul] at h ⊢
  calc |Metric.infDist (u + 1) _ - 1 - (Metric.infDist (v + 1) _ - 1)|
      = |Metric.infDist (u + 1) (Set.range fun n : ℤ => (4 * n : ℝ)) -
          Metric.infDist (v + 1) (Set.range fun n : ℤ => (4 * n : ℝ))| := by ring_nf
    _ ≤ |u + 1 - (v + 1)| := h
    _ = |u - v| := by ring_nf

@[fun_prop]
lemma continuous_triangleWave : Continuous triangleWave :=
  lipschitzWith_triangleWave.continuous

/-- The distance from `v` to `4ℤ` is `|v - 4n|` when `|v - 4n| ≤ 2`. -/
lemma infDist_range_four_mul_eq {v : ℝ} {n : ℤ} (h : |v - 4 * n| ≤ 2) :
    Metric.infDist v (Set.range fun m : ℤ => (4 * m : ℝ)) = |v - 4 * n| := by
  apply le_antisymm
  · simpa [Real.dist_eq] using Metric.infDist_le_dist_of_mem (Set.mem_range_self n)
      (x := v) (s := Set.range fun m : ℤ => (4 * m : ℝ))
  · rw [Metric.le_infDist ⟨_, Set.mem_range_self 0⟩]
    rintro _ ⟨m, rfl⟩
    rw [Real.dist_eq]
    rcases eq_or_ne m n with rfl | hmn
    · exact le_rfl
    · have h1 : (1 : ℝ) ≤ |(m : ℝ) - n| := by
        have : (1 : ℤ) ≤ |m - n| := Int.one_le_abs (sub_ne_zero.mpr hmn)
        exact_mod_cast this
      have h2 : |(4 * m : ℝ) - 4 * n| ≤ |v - 4 * m| + |v - 4 * n| := by
        calc |(4 * m : ℝ) - 4 * n| = |(v - 4 * n) - (v - 4 * m)| := by ring_nf
          _ ≤ |v - 4 * n| + |v - 4 * m| := abs_sub _ _
          _ = _ := add_comm _ _
      have h3 : |(4 * m : ℝ) - 4 * n| = 4 * |(m : ℝ) - n| := by
        rw [← mul_sub, abs_mul]; norm_num
      linarith

/-- Every real number is within `2` of a multiple of `4`. -/
lemma exists_abs_sub_four_mul_le (v : ℝ) : ∃ n : ℤ, |v - 4 * n| ≤ 2 := by
  refine ⟨round (v / 4), ?_⟩
  have h := abs_sub_round (v / 4)
  have : v - 4 * (round (v / 4) : ℝ) = 4 * (v / 4 - round (v / 4)) := by ring
  rw [this, abs_mul]
  norm_num
  linarith

lemma triangleWave_eq_of_abs_le {u : ℝ} {n : ℤ} (h : |u + 1 - 4 * n| ≤ 2) :
    triangleWave u = |u + 1 - 4 * n| - 1 := by
  simp [triangleWave, infDist_range_four_mul_eq h]

lemma triangleWave_mem_Icc (u : ℝ) : triangleWave u ∈ Set.Icc (-1 : ℝ) 1 := by
  obtain ⟨n, hn⟩ := exists_abs_sub_four_mul_le (u + 1)
  rw [triangleWave_eq_of_abs_le hn]
  constructor <;> linarith [abs_nonneg (u + 1 - 4 * n)]

lemma triangleWave_of_mem_Icc {u : ℝ} (hu : u ∈ Set.Icc (-1 : ℝ) 1) : triangleWave u = u := by
  have h : |u + 1 - 4 * ((0 : ℤ) : ℝ)| ≤ 2 := by
    rw [abs_le]; constructor <;> push_cast <;> linarith [hu.1, hu.2]
  rw [triangleWave_eq_of_abs_le h]
  push_cast
  rw [abs_of_nonneg (by linarith [hu.1])]
  ring

/-- On `[1, 3]` the triangle wave is `2 - u`. -/
lemma triangleWave_of_mem_Icc_one_three {u : ℝ} (hu : u ∈ Set.Icc (1 : ℝ) 3) :
    triangleWave u = 2 - u := by
  have h : |u + 1 - 4 * ((1 : ℤ) : ℝ)| ≤ 2 := by
    rw [abs_le]; constructor <;> push_cast <;> linarith [hu.1, hu.2]
  rw [triangleWave_eq_of_abs_le h]
  push_cast
  rw [abs_of_nonpos (by linarith [hu.2])]
  ring

/-- On `[-3, -1]` the triangle wave is `-2 - u`. -/
lemma triangleWave_of_mem_Icc_neg_three_neg_one {u : ℝ} (hu : u ∈ Set.Icc (-3 : ℝ) (-1)) :
    triangleWave u = -2 - u := by
  have h : |u + 1 - 4 * ((0 : ℤ) : ℝ)| ≤ 2 := by
    rw [abs_le]; constructor <;> push_cast <;> linarith [hu.1, hu.2]
  rw [triangleWave_eq_of_abs_le h]
  push_cast
  rw [abs_of_nonpos (by linarith [hu.2])]
  ring

lemma triangleWave_add_four (u : ℝ) : triangleWave (u + 4) = triangleWave u := by
  obtain ⟨n, hn⟩ := exists_abs_sub_four_mul_le (u + 1)
  have h' : |u + 4 + 1 - 4 * ((n + 1 : ℤ) : ℝ)| ≤ 2 := by
    push_cast; convert hn using 2; ring
  rw [triangleWave_eq_of_abs_le hn, triangleWave_eq_of_abs_le h']
  push_cast; ring_nf

lemma triangleWave_neg (u : ℝ) : triangleWave (-u) = -triangleWave u := by
  obtain ⟨n, hn⟩ := exists_abs_sub_four_mul_le (u + 1)
  rw [triangleWave_eq_of_abs_le hn]
  set w := u + 1 - 4 * (n : ℝ) with hw
  rcases le_total 0 w with h0 | h0
  · -- `-u + 1 = (2 - w) + 4 (-n)` with `2 - w ∈ [0, 2]`
    have h' : |-u + 1 - 4 * ((-n : ℤ) : ℝ)| ≤ 2 := by
      push_cast
      rw [abs_le]; constructor <;> linarith [(abs_le.mp hn).1, (abs_le.mp hn).2]
    rw [triangleWave_eq_of_abs_le h', abs_of_nonneg h0]
    push_cast
    rw [abs_of_nonneg (by linarith [(abs_le.mp hn).2])]
    linarith
  · -- `-u + 1 = (-2 - w) + 4 (1 - n)` with `-2 - w ∈ [-2, 0]`
    have h' : |-u + 1 - 4 * ((1 - n : ℤ) : ℝ)| ≤ 2 := by
      push_cast
      rw [abs_le]; constructor <;> linarith [(abs_le.mp hn).1, (abs_le.mp hn).2]
    rw [triangleWave_eq_of_abs_le h', abs_of_nonpos h0]
    push_cast
    rw [abs_of_nonpos (by linarith [(abs_le.mp hn).1])]
    linarith

lemma triangleWave_two_sub (u : ℝ) : triangleWave (2 - u) = triangleWave u := by
  have h1 : triangleWave (2 - u) = -triangleWave (u - 2) := by
    rw [← triangleWave_neg]; ring_nf
  have h2 : triangleWave (u - 2) = -triangleWave u := by
    obtain ⟨n, hn⟩ := exists_abs_sub_four_mul_le (u + 1)
    rw [triangleWave_eq_of_abs_le hn]
    set w := u + 1 - 4 * (n : ℝ) with hw
    rcases le_total 0 w with h0 | h0
    · have h' : |u - 2 + 1 - 4 * ((n : ℤ) : ℝ)| ≤ 2 := by
        rw [abs_le]; constructor <;> linarith [(abs_le.mp hn).1, (abs_le.mp hn).2]
      rw [triangleWave_eq_of_abs_le h', abs_of_nonneg h0]
      rw [abs_of_nonpos (by linarith [(abs_le.mp hn).2])]
      linarith
    · have h' : |u - 2 + 1 - 4 * ((n - 1 : ℤ) : ℝ)| ≤ 2 := by
        push_cast
        rw [abs_le]; constructor <;> linarith [(abs_le.mp hn).1, (abs_le.mp hn).2]
      rw [triangleWave_eq_of_abs_le h', abs_of_nonpos h0]
      push_cast
      rw [abs_of_nonneg (by linarith [(abs_le.mp hn).1])]
      linarith
  rw [h1, h2, neg_neg]

lemma abs_triangleWave_sub_le (u v : ℝ) : |triangleWave u - triangleWave v| ≤ |u - v| := by
  have := lipschitzWith_triangleWave.dist_le_mul u v
  simpa [Real.dist_eq] using this

end Real
