module

public import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
public import Mathlib.Topology.Semicontinuity.Basic
public import Mathlib.Algebra.BigOperators.Group.Finset.Defs
import Mathlib.Topology.Sion
import Mathlib.Topology.UrysohnsLemma
import Mathlib.Topology.Instances.EReal.Lemmas
import Mathlib.MeasureTheory.Measure.Prokhorov
import Mathlib.MeasureTheory.Measure.DiracProba
import Mathlib.MeasureTheory.Integral.RieszMarkovKakutani.Real
import Mathlib.MeasureTheory.Integral.BoundedContinuousFunction

/-!
# Alpern and Gal's mixed-strategy minimax theorem

S. Alpern and S. Gal, *A mixed strategy minimax theorem without compactness*, SIAM J. Control
Optim. 26 (1988), 1357–1361; also Appendix A of Alpern and Gal, *The Theory of Search Games and
Rendezvous* (2003).

The form used by the paper: a zero-sum game in which the minimizer's pure strategies form a
compact Hausdorff space `X`, the maximizer's pure strategies form an arbitrary set `Y`, and the
payoff `f : X → Y → [0, ∞]` is lower semicontinuous in the minimizer's strategy. Then the game
has a value in mixed strategies: the minimizer's mixed strategies are the Borel probability
measures on `X`, the maximizer's are finitely supported probability distributions on `Y`; the
minimizer has an optimal mixed strategy, and the maximizer has `ε`-optimal finitely supported
ones.

## Proof

For a finite set `s` of columns and a truncation level `N`, Sion's theorem (`Sion.minimax'`) is
applied with the simplex of weights on `s` as the compact side and the moments
`(∫ min (f (·, y), N) dμ)_{y ∈ s}` of the probability measures `μ` as the other (convex) side:
some mixed strategy holds every truncated column of `s` to the lower value up to `ε`
(`val_finite_game`). These solution sets form a directed family of nonempty sets; by compactness of
the probability measures (`Prokhorov`) the closures have a common point, which is replaced by a
regular measure with the same neighbourhoods (Riesz–Markov–Kakutani); there the truncated payoffs
are lower semicontinuous (`val_lsc_lintegral`, `val_lsc_measure_open_of_regular`), so it holds
every truncated column to the lower value, and monotone convergence removes the truncation
(`val_exists_le`). Weak duality (`val_weak_duality`) gives the other inequality.

Departure from the plan: the plan embeds the probability measures into `C(X, ℝ) → ℝ` and uses
the lower semicontinuity of `μ ↦ ∫ f dμ` on all of `ProbabilityMeasure X`. For a non-metrizable
compact `X` neither works: a Borel probability measure that is not regular is not determined by
its integrals of continuous functions, and `μ ↦ ∫ f dμ` (for `f` lower semicontinuous) is not
lower semicontinuous at it (on `[0, ω₁]` the Dieudonné measure and the Dirac mass at `ω₁` have
the same integrals of continuous functions but give the open set `[0, ω₁)` the masses `1` and
`0`). So the measures enter Sion's theorem through their moment vectors (on which the payoff is
bilinear), the limit point is replaced by a regular measure, and attainment comes out of the
construction instead of from lower semicontinuity on the whole compact space.

The statement needs `X` nonempty: there is no probability measure on the empty space, so the
first conclusion fails for `X = ∅` (`val_minimax` is the statement with `[Nonempty X]`).
-/

@[expose] public section

open scoped ENNReal NNReal Topology BoundedContinuousFunction
open MeasureTheory Filter

namespace External.AlpernGal

section Proof

/-! ### A staircase below a function

For a step `h` and `m` steps, `∑_{k < m} h · 1[(k + 1) h < z]` lies between `z - h` and `z` when
`z ≤ m h`. -/

private lemma val_staircase_eq (h z : ℝ≥0∞) (m : ℕ) (hz : (m : ℝ≥0∞) * h < z) :
    ∑ k ∈ Finset.range m, (if ((k + 1 : ℕ) : ℝ≥0∞) * h < z then h else 0) = m * h := by
  rw [Finset.sum_congr rfl (g := fun _ => h), Finset.sum_const, Finset.card_range, nsmul_eq_mul]
  intro k hk
  have hk' : ((k + 1 : ℕ) : ℝ≥0∞) * h < z := lt_of_le_of_lt (by
    gcongr; exact_mod_cast Finset.mem_range.1 hk) hz
  exact ite_eq_left hk'

private lemma val_staircase_le (h z : ℝ≥0∞) (m : ℕ) :
    ∑ k ∈ Finset.range m, (if ((k + 1 : ℕ) : ℝ≥0∞) * h < z then h else 0) ≤ z := by
  induction m with
  | zero => simp
  | succ m ih =>
    rw [Finset.sum_range_succ]
    split_ifs with hm
    · have hm' : (m : ℝ≥0∞) * h < z := lt_of_le_of_lt (by gcongr; exact_mod_cast m.le_succ) hm
      rw [val_staircase_eq h z m hm']
      refine le_of_lt (lt_of_le_of_lt (le_of_eq ?_) hm)
      push_cast
      ring
    · simpa using ih

private lemma val_le_staircase (h z : ℝ≥0∞) (m : ℕ) (hz : z ≤ m * h) :
    z ≤ ∑ k ∈ Finset.range m, (if ((k + 1 : ℕ) : ℝ≥0∞) * h < z then h else 0) + h := by
  induction m with
  | zero =>
    simp only [CharP.cast_eq_zero, zero_mul, nonpos_iff_eq_zero] at hz
    simp [hz]
  | succ m ih =>
    rw [Finset.sum_range_succ]
    rcases le_or_gt z (m * h) with hm | hm
    · exact (ih hm).trans (by gcongr; exact le_self_add)
    · rw [val_staircase_eq h z m hm]
      calc z ≤ ((m + 1 : ℕ) : ℝ≥0∞) * h := hz
        _ = m * h + h := by push_cast; ring
        _ ≤ m * h + (if ((m + 1 : ℕ) : ℝ≥0∞) * h < z then h else 0) + h := by
          gcongr; exact le_self_add

/-! ### Lower semicontinuity of integrals -/

variable {X : Type*} [TopologicalSpace X] [MeasurableSpace X]

/-- If the measures `F p` of every open set are lower semicontinuous at `p₀`, so are the integrals
of every bounded lower semicontinuous function (approximation from below by a staircase of
indicators of open sets). -/
private lemma val_lsc_lintegral [OpensMeasurableSpace X] {P : Type*} [TopologicalSpace P]
    (F : P → Measure X) (p₀ : P) [IsFiniteMeasure (F p₀)]
    (hF : ∀ U : Set X, IsOpen U → LowerSemicontinuousAt (fun p => F p U) p₀)
    {g : X → ℝ≥0∞} (hg : LowerSemicontinuous g) {N : ℝ≥0∞} (hN : N ≠ ⊤) (hgN : ∀ x, g x ≤ N) :
    LowerSemicontinuousAt (fun p => ∫⁻ x, g x ∂F p) p₀ := by
  intro c hc
  have hctop : c ≠ ⊤ := ne_top_of_lt hc
  -- a step `h` so small that `c + h * (F p₀ univ) < ∫⁻ g`
  obtain ⟨h₀, hh₀, hh₀lt⟩ := ENNReal.exists_pos_mul_lt (measure_ne_top (F p₀) Set.univ)
    (tsub_pos_of_lt hc).ne'
  set h := min h₀ 1 with hh_def
  have hh : 0 < h := lt_min hh₀ one_pos
  have hhtop : h ≠ ⊤ := ne_top_of_le_ne_top ENNReal.one_ne_top (min_le_right _ _)
  have hlt : c + h * F p₀ Set.univ < ∫⁻ x, g x ∂F p₀ := by
    have : h * F p₀ Set.univ < ∫⁻ x, g x ∂F p₀ - c :=
      lt_of_le_of_lt (by gcongr; exact min_le_left _ _) hh₀lt
    calc c + h * F p₀ Set.univ < c + (∫⁻ x, g x ∂F p₀ - c) := by
          exact ENNReal.add_lt_add_left hctop this
      _ = ∫⁻ x, g x ∂F p₀ := add_tsub_cancel_of_le hc.le
  -- the number of steps
  obtain ⟨m, hm⟩ := ENNReal.exists_nat_mul_gt hh.ne' hN
  -- the open sets of the staircase
  set U : ℕ → Set X := fun k => {x | ((k + 1 : ℕ) : ℝ≥0∞) * h < g x} with hU_def
  have hUo : ∀ k, IsOpen (U k) := fun k => hg.isOpen_preimage _
  set φ : X → ℝ≥0∞ := fun x =>
    ∑ k ∈ Finset.range m, (if ((k + 1 : ℕ) : ℝ≥0∞) * h < g x then h else 0) with hφ_def
  have hφ_ind : ∀ x, φ x = ∑ k ∈ Finset.range m, (U k).indicator (fun _ => h) x := by
    intro x
    simp only [hφ_def, Set.indicator, hU_def, Set.mem_ofPred_eq]
  have hφint : ∀ p, ∫⁻ x, φ x ∂F p = ∑ k ∈ Finset.range m, h * F p (U k) := by
    intro p
    simp_rw [hφ_ind]
    rw [lintegral_finsetSum _ fun k _ => (measurable_const.indicator (hUo k).measurableSet)]
    refine Finset.sum_congr rfl fun k _ => ?_
    exact lintegral_indicator_const (hUo k).measurableSet h
  have hφg : ∀ x, φ x ≤ g x := fun x => val_staircase_le h (g x) m
  have hgφ : ∀ x, g x ≤ φ x + h := fun x => val_le_staircase h (g x) m ((hgN x).trans hm.le)
  have hφmeas : Measurable φ := by
    have : φ = fun x => ∑ k ∈ Finset.range m, (U k).indicator (fun _ => h) x := funext hφ_ind
    rw [this]
    exact Finset.measurable_sum _ fun k _ => measurable_const.indicator (hUo k).measurableSet
  have hcφ : c < ∫⁻ x, φ x ∂F p₀ := by
    have : ∫⁻ x, g x ∂F p₀ ≤ ∫⁻ x, φ x ∂F p₀ + h * F p₀ Set.univ := by
      calc ∫⁻ x, g x ∂F p₀ ≤ ∫⁻ x, φ x + h ∂F p₀ := lintegral_mono hgφ
        _ = ∫⁻ x, φ x ∂F p₀ + h * F p₀ Set.univ := by
          rw [lintegral_add_left hφmeas, lintegral_const]
    exact lt_of_add_lt_add_right (hlt.trans_le this)
  -- the staircase integral is lower semicontinuous at `p₀`
  have hlsc : LowerSemicontinuousAt (fun p => ∑ k ∈ Finset.range m, h * F p (U k)) p₀ := by
    refine lowerSemicontinuousAt_sum fun k _ => ?_
    have := ContinuousAt.comp_lowerSemicontinuousAt (g := fun a : ℝ≥0∞ => h * a)
      (ENNReal.continuous_const_mul hhtop).continuousAt (hF (U k) (hUo k))
      (fun a b hab => mul_le_mul_right hab h)
    exact this
  have hφint' : (fun p => ∫⁻ x, φ x ∂F p) = fun p => ∑ k ∈ Finset.range m, h * F p (U k) :=
    funext hφint
  rw [← hφint'] at hlsc
  filter_upwards [hlsc c hcφ] with p hp
  exact hp.trans_le (lintegral_mono hφg)

/-! ### Regular measures -/

section Compact

variable [CompactSpace X] [T2Space X] [BorelSpace X]

/-- At a regular probability measure, the measure of an open set is lower semicontinuous for the
weak topology (inner regularity and Urysohn's lemma). -/
private lemma val_lsc_measure_open_of_regular (ν : ProbabilityMeasure X)
    (hν : (ν : Measure X).Regular) {U : Set X} (hU : IsOpen U) :
    LowerSemicontinuousAt (fun ρ : ProbabilityMeasure X => (ρ : Measure X) U) ν := by
  intro c hc
  obtain ⟨K, hKU, hK, hcK⟩ := hU.exists_lt_isCompact hc
  obtain ⟨g, hg1, hg0, -, hg01⟩ := exists_continuous_one_zero_of_isCompact hK hU.isClosed_compl
    (Set.disjoint_compl_right_iff_subset.2 hKU)
  let G : X →ᵇ ℝ≥0 := BoundedContinuousFunction.mkOfCompact
    ⟨fun x => (g x).toNNReal, continuous_real_toNNReal.comp g.continuous⟩
  have hG : ∀ x, ((G x : ℝ≥0) : ℝ≥0∞) = ENNReal.ofReal (g x) := fun x => rfl
  have h1 : (ν : Measure X) K ≤ ∫⁻ x, G x ∂(ν : Measure X) := by
    rw [← lintegral_indicator_one hK.measurableSet]
    refine lintegral_mono fun x => ?_
    by_cases hx : x ∈ K
    · simp [hx, hG, hg1 hx]
    · simp [hx]
  have h2 : ∀ ρ : ProbabilityMeasure X, ∫⁻ x, G x ∂(ρ : Measure X) ≤ (ρ : Measure X) U := by
    intro ρ
    rw [← lintegral_indicator_one hU.measurableSet]
    refine lintegral_mono fun x => ?_
    by_cases hx : x ∈ U
    · simp [hx, hG, (hg01 x).2]
    · simp [hx, hG, hg0 hx]
  have hcont := (ProbabilityMeasure.continuous_lintegral_boundedContinuousFunction G).tendsto ν
  filter_upwards [hcont.eventually (lt_mem_nhds (hcK.trans_le h1))] with ρ hρ
  exact hρ.trans_le (h2 ρ)

/-- Every probability measure on a compact Hausdorff space has a regular one with the same
integrals of continuous functions (Riesz–Markov–Kakutani); every neighbourhood of the latter is a
neighbourhood of the former. -/
private lemma val_exists_regular (μ : ProbabilityMeasure X) :
    ∃ ν : ProbabilityMeasure X, (ν : Measure X).Regular ∧ 𝓝 μ ≤ 𝓝 ν := by
  obtain ⟨ν₀, hreg, hfin, heq⟩ := Measure.exists_regular_eq_of_compactSpace (μ : Measure X)
  have hint : ∀ f : X →ᵇ ℝ≥0, ∫⁻ x, f x ∂ν₀ = ∫⁻ x, f x ∂(μ : Measure X) := by
    intro f
    let g : X →ᵇ ℝ := BoundedContinuousFunction.mkOfCompact
      ⟨fun x => (f x : ℝ), NNReal.continuous_coe.comp f.continuous⟩
    have := heq g
    rw [lintegral_coe_eq_integral _ (g.integrable _), lintegral_coe_eq_integral _ (g.integrable _)]
    exact congrArg ENNReal.ofReal this.symm
  have hprob : IsProbabilityMeasure ν₀ := by
    constructor
    simpa using hint 1
  let ν : ProbabilityMeasure X := ⟨ν₀, hprob⟩
  refine ⟨ν, hreg, ?_⟩
  have : Tendsto id (𝓝 μ) (𝓝 ν) := by
    rw [ProbabilityMeasure.tendsto_iff_forall_lintegral_tendsto]
    intro f
    have hf : ∫⁻ x, f x ∂(ν : Measure X) = ∫⁻ x, f x ∂(μ : Measure X) := hint f
    rw [hf]
    exact (ProbabilityMeasure.continuous_lintegral_boundedContinuousFunction f).tendsto μ
  exact this

end Compact

/-! ### The simplex of weights on a finite set -/

/-- The simplex of weights on a finite type. -/
private def val_simplex (ι : Type*) [Fintype ι] : Set (ι → ℝ) :=
  {w | (∀ i, 0 ≤ w i) ∧ ∑ i, w i = 1}

private lemma val_isCompact_simplex (ι : Type*) [Fintype ι] : IsCompact (val_simplex ι) := by
  refine IsCompact.of_isClosed_subset (isCompact_Icc (a := (0 : ι → ℝ)) (b := 1)) ?_ ?_
  · simp only [val_simplex, Set.ofPred_and, Set.ofPred_forall]
    exact (isClosed_iInter fun i => isClosed_le continuous_const (continuous_apply i)).inter
      (isClosed_eq (continuous_finsetSum _ fun i _ => continuous_apply i) continuous_const)
  · intro w hw
    refine ⟨fun i => hw.1 i, fun i => ?_⟩
    have := Finset.single_le_sum (f := w) (fun j _ => hw.1 j) (Finset.mem_univ i)
    simpa [hw.2] using this

private lemma val_convex_simplex (ι : Type*) [Fintype ι] : Convex ℝ (val_simplex ι) := by
  intro x hx y hy a b ha hb hab
  refine ⟨fun i => ?_, ?_⟩
  · simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    exact add_nonneg (mul_nonneg ha (hx.1 i)) (mul_nonneg hb (hy.1 i))
  · simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, Finset.sum_add_distrib,
      ← Finset.mul_sum, hx.2, hy.2, mul_one, hab]

private lemma val_single_mem_simplex {ι : Type*} [Fintype ι] [DecidableEq ι] (i : ι) :
    Pi.single i 1 ∈ val_simplex ι := by
  refine ⟨fun j => ?_, ?_⟩
  · by_cases h : j = i
    · subst h; simp
    · simp [h]
  · simp

private lemma val_sum_single_mul {ι : Type*} [Fintype ι] [DecidableEq ι] (i : ι) (v : ι → ℝ) :
    ∑ j, (Pi.single i 1 : ι → ℝ) j * v j = v i := by
  simp [Pi.single_apply]

/-- The pairing `(w, v) ↦ -∑ i, w i * v i` is affine in each argument. -/
private lemma val_pairing_affine {ι : Type*} [Fintype ι] (w₁ w₂ v₁ v₂ : ι → ℝ) (a b : ℝ) :
    -(∑ i, (a • w₁ + b • w₂) i * v₁ i) = a • -(∑ i, w₁ i * v₁ i) + b • -(∑ i, w₂ i * v₁ i) ∧
    -(∑ i, w₁ i * (a • v₁ + b • v₂) i) = a • -(∑ i, w₁ i * v₁ i) + b • -(∑ i, w₁ i * v₂ i) := by
  constructor <;>
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, add_mul, mul_add, Finset.sum_add_distrib,
    neg_add, mul_neg, Finset.mul_sum, mul_assoc, mul_left_comm (w₁ _) a, mul_left_comm (w₁ _) b]

/-! ### The finite game with truncated payoffs -/

/-- **The finite game** (Sion's theorem with the simplex of weights on `s` as the compact side and
the moments `(∫ min(f(·,y), N) dμ)_{y ∈ s}` of the probability measures `μ` as the other side): if
every mixture of the columns `y ∈ s` is held to at most `V` by some pure strategy, then some mixed
strategy holds every truncated column `y ∈ s` to at most `V + ε`. -/
private lemma val_finite_game [Nonempty X] [OpensMeasurableSpace X] {Y : Type*}
    (f : X → Y → ℝ≥0∞) (hf : ∀ y, LowerSemicontinuous fun x => f x y) {V : ℝ≥0∞} (hV : V ≠ ⊤)
    (s : Finset Y) (hVs : ∀ w : Y → ℝ≥0∞, ∑ y ∈ s, w y = 1 → ⨅ x, ∑ y ∈ s, w y * f x y ≤ V)
    (N : ℕ) {ε : ℝ≥0∞} (hε : 0 < ε) :
    ∃ μ : ProbabilityMeasure X, ∀ y ∈ s, ∫⁻ x, f x y ⊓ N ∂(μ : Measure X) ≤ V + ε := by
  classical
  obtain ⟨x₀⟩ := ‹Nonempty X›
  by_cases hεtop : ε = ⊤
  · exact ⟨diracProba x₀, fun y _ => by simp [hεtop]⟩
  rcases s.eq_empty_or_nonempty with rfl | ⟨y₀, hy₀⟩
  · exact ⟨diracProba x₀, by simp⟩
  -- the truncated payoff
  set g : X → Y → ℝ≥0∞ := fun x y => f x y ⊓ N with hg
  have hgmeas : ∀ y, Measurable fun x => g x y := fun y =>
    ((hf y).inf lowerSemicontinuous_const).measurable
  have hgint : ∀ (μ : ProbabilityMeasure X) y, ∫⁻ x, g x y ∂(μ : Measure X) ≠ ⊤ := by
    intro μ y
    refine ne_top_of_le_ne_top (b := ∫⁻ _, (N : ℝ≥0∞) ∂(μ : Measure X)) ?_
      (lintegral_mono fun x => inf_le_right)
    simp
  -- the moments of a mixed strategy, the moment set, the simplex and the payoff
  let mom : ProbabilityMeasure X → (s → ℝ) := fun μ i => (∫⁻ x, g x i ∂(μ : Measure X)).toReal
  let M : Set (s → ℝ) := Set.range mom
  let Δ : Set (s → ℝ) := val_simplex s
  let φ : (s → ℝ) → (s → ℝ) → EReal := fun w v => ((-(∑ i, w i * v i) : ℝ) : EReal)
  have hφw : ∀ v, Continuous fun w => φ w v := fun v =>
    continuous_coe_real_ereal.comp (continuous_neg.comp
      (continuous_finsetSum _ fun i _ => (continuous_apply i).mul continuous_const))
  have hφv : ∀ w, Continuous fun v => φ w v := fun w =>
    continuous_coe_real_ereal.comp (continuous_neg.comp
      (continuous_finsetSum _ fun i _ => continuous_const.mul (continuous_apply i)))
  have hcM : Convex ℝ M := by
    rintro _ ⟨μ₁, rfl⟩ _ ⟨μ₂, rfl⟩ a b ha hb hab
    let μ₃ : ProbabilityMeasure X :=
      ⟨ENNReal.ofReal a • (μ₁ : Measure X) + ENNReal.ofReal b • (μ₂ : Measure X), ⟨by
        simp [← ENNReal.ofReal_add ha hb, hab]⟩⟩
    refine ⟨μ₃, funext fun i => ?_⟩
    have h₃ : (μ₃ : Measure X) =
        ENNReal.ofReal a • (μ₁ : Measure X) + ENNReal.ofReal b • (μ₂ : Measure X) := rfl
    simp only [mom, h₃, lintegral_add_measure, lintegral_smul_measure, smul_eq_mul,
      Pi.add_apply, Pi.smul_apply]
    rw [ENNReal.toReal_add (ENNReal.mul_ne_top ENNReal.ofReal_ne_top (hgint μ₁ i))
      (ENNReal.mul_ne_top ENNReal.ofReal_ne_top (hgint μ₂ i)), ENNReal.toReal_mul,
      ENNReal.toReal_mul, ENNReal.toReal_ofReal ha, ENNReal.toReal_ofReal hb]
  have hquasiconvex : ∀ v, QuasiconvexOn ℝ Δ fun w => φ w v := by
    intro v
    have hconv : ConvexOn ℝ Δ fun w => -(∑ i, w i * v i) :=
      ⟨val_convex_simplex s, fun w₁ _ w₂ _ a b _ _ _ =>
        le_of_eq (val_pairing_affine w₁ w₂ v v a b).1⟩
    exact hconv.quasiconvexOn.monotone_comp (g := Real.toEReal) EReal.coe_strictMono.monotone
  have hquasiconcave : ∀ w, QuasiconcaveOn ℝ M fun v => φ w v := by
    intro w
    have hconc : ConcaveOn ℝ M fun v => -(∑ i, w i * v i) :=
      ⟨hcM, fun v₁ _ v₂ _ a b _ _ _ => le_of_eq (val_pairing_affine w w v₁ v₂ a b).2.symm⟩
    exact hconc.quasiconcaveOn.monotone_comp (g := Real.toEReal) EReal.coe_strictMono.monotone
  have hsion := Sion.minimax' (f := φ) (X := Δ) (Y := M)
    ⟨_, val_single_mem_simplex (⟨y₀, hy₀⟩ : s)⟩ (val_convex_simplex s) (val_isCompact_simplex s)
    (fun v _ => (hφw v).lowerSemicontinuous.lowerSemicontinuousOn _)
    (fun v _ => hquasiconvex v) hcM
    (fun w _ => (hφv w).upperSemicontinuous.upperSemicontinuousOn _)
    (fun w _ => hquasiconcave w)
  -- real versions of `V` and `ε`
  set Vr := V.toReal with hVr
  set εr := ε.toReal with hεr
  have hεr0 : 0 < εr := ENNReal.toReal_pos hε.ne' hεtop
  -- every mixture of the columns is held to `V + ε / 2` by a pure strategy
  have hL : ∀ w ∈ Δ, (((-(Vr + εr / 2)) : ℝ) : EReal) < ⨆ v ∈ M, φ w v := by
    intro w hw
    let W : Y → ℝ≥0∞ := fun y => if h : y ∈ s then ENNReal.ofReal (w ⟨y, h⟩) else 0
    have hWs : ∀ F : Y → ℝ≥0∞, ∑ y ∈ s, W y * F y = ∑ i : s, ENNReal.ofReal (w i) * F i := by
      intro F
      rw [← Finset.sum_coe_sort s]
      refine Finset.sum_congr rfl fun i _ => ?_
      simp [W, i.2]
    have hW : ∑ y ∈ s, W y = 1 := by
      have := hWs 1
      simp only [Pi.one_apply, mul_one] at this
      rw [this, ← ENNReal.ofReal_sum_of_nonneg fun i _ => hw.1 i, hw.2, ENNReal.ofReal_one]
    have hlt : V < V + ENNReal.ofReal (εr / 2) :=
      ENNReal.lt_add_right hV (ENNReal.ofReal_pos.2 (half_pos hεr0)).ne'
    obtain ⟨x, hx⟩ := iInf_lt_iff.1 ((hVs W hW).trans_lt hlt)
    have hgx : ∑ i : s, ENNReal.ofReal (w i) * g x i < V + ENNReal.ofReal (εr / 2) := by
      rw [← hWs (fun y => g x y)]
      refine lt_of_le_of_lt ?_ hx
      gcongr with y
      exact inf_le_left
    have hfin : ∀ i : s, ENNReal.ofReal (w i) * g x i ≠ ⊤ := fun i =>
      ENNReal.mul_ne_top ENNReal.ofReal_ne_top
        (ne_top_of_le_ne_top (ENNReal.natCast_ne_top N) inf_le_right)
    have hv : mom (diracProba x) = fun i : s => (g x i).toReal := by
      funext i
      simp only [mom]
      rw [show ((diracProba x : ProbabilityMeasure X) : Measure X) = Measure.dirac x from rfl,
        lintegral_dirac' x (hgmeas i)]
    have hsum : ∑ i, w i * mom (diracProba x) i < Vr + εr / 2 := by
      rw [hv]
      have : ∑ i, w i * (g x i).toReal = (∑ i : s, ENNReal.ofReal (w i) * g x i).toReal := by
        rw [ENNReal.toReal_sum fun i _ => hfin i]
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [ENNReal.toReal_mul, ENNReal.toReal_ofReal (hw.1 i)]
      rw [this]
      have h2 := (ENNReal.toReal_lt_toReal (ENNReal.sum_ne_top.2 fun i _ => hfin i)
        (ENNReal.add_ne_top.2 ⟨hV, ENNReal.ofReal_ne_top⟩)).2 hgx
      rwa [ENNReal.toReal_add hV ENNReal.ofReal_ne_top,
        ENNReal.toReal_ofReal (half_pos hεr0).le] at h2
    refine lt_of_lt_of_le ?_ (le_iSup₂_of_le (mom (diracProba x)) ⟨_, rfl⟩ le_rfl)
    exact EReal.coe_lt_coe_iff.2 (neg_lt_neg hsum)
  have hLHS : (((-(Vr + εr / 2)) : ℝ) : EReal) ≤ ⨅ w ∈ Δ, ⨆ v ∈ M, φ w v :=
    le_iInf₂ fun w hw => (hL w hw).le
  rw [hsion] at hLHS
  have hlt : (((-(Vr + εr)) : ℝ) : EReal) < ⨆ v ∈ M, ⨅ w ∈ Δ, φ w v :=
    lt_of_lt_of_le (EReal.coe_lt_coe_iff.2 (by linarith)) hLHS
  obtain ⟨v, hv⟩ := lt_iSup_iff.1 hlt
  obtain ⟨hvM, hv⟩ := lt_iSup_iff.1 hv
  obtain ⟨μ, rfl⟩ := hvM
  refine ⟨μ, fun y hy => ?_⟩
  have h1 := hv.trans_le (iInf₂_le _ (val_single_mem_simplex (⟨y, hy⟩ : s)))
  simp only [φ, val_sum_single_mul] at h1
  have h2 : mom μ ⟨y, hy⟩ < Vr + εr := by
    have := EReal.coe_lt_coe_iff.1 h1
    linarith
  have h3 : ∫⁻ x, g x y ∂(μ : Measure X) = ENNReal.ofReal (mom μ ⟨y, hy⟩) :=
    (ENNReal.ofReal_toReal (hgint μ y)).symm
  calc ∫⁻ x, f x y ⊓ N ∂(μ : Measure X) = ENNReal.ofReal (mom μ ⟨y, hy⟩) := h3
    _ ≤ ENNReal.ofReal (Vr + εr) := ENNReal.ofReal_le_ofReal h2.le
    _ = V + ε := by
      rw [ENNReal.ofReal_add ENNReal.toReal_nonneg ENNReal.toReal_nonneg,
        ENNReal.ofReal_toReal hV, ENNReal.ofReal_toReal hεtop]

/-! ### Weak duality and the optimal mixed strategy -/

omit [TopologicalSpace X] in
/-- Weak duality: the lower value with finitely supported mixed strategies of the maximizer is at
most the guarantee of any mixed strategy of the minimizer. -/
private lemma val_weak_duality {Y : Type*} (f : X → Y → ℝ≥0∞)
    (hf : ∀ y, Measurable fun x => f x y) (μ : ProbabilityMeasure X) :
    (⨆ (s : Finset Y) (w : Y → ℝ≥0∞) (_ : ∑ y ∈ s, w y = 1), ⨅ x, ∑ y ∈ s, w y * f x y) ≤
      ⨆ y, ∫⁻ x, f x y ∂(μ : Measure X) := by
  refine iSup_le fun s => iSup_le fun w => iSup_le fun hw => ?_
  set M := ⨆ y, ∫⁻ x, f x y ∂(μ : Measure X)
  calc ⨅ x, ∑ y ∈ s, w y * f x y = ∫⁻ _, (⨅ x, ∑ y ∈ s, w y * f x y) ∂(μ : Measure X) := by
        rw [lintegral_const, measure_univ, mul_one]
    _ ≤ ∫⁻ x, ∑ y ∈ s, w y * f x y ∂(μ : Measure X) := lintegral_mono fun x => iInf_le _ x
    _ = ∑ y ∈ s, w y * ∫⁻ x, f x y ∂(μ : Measure X) := by
        rw [lintegral_finsetSum _ fun y _ => (hf y).const_mul (w y)]
        exact Finset.sum_congr rfl fun y _ => lintegral_const_mul _ (hf y)
    _ ≤ ∑ y ∈ s, w y * M := by
        gcongr with y
        exact le_iSup (fun y => ∫⁻ x, f x y ∂(μ : Measure X)) y
    _ = M := by rw [← Finset.sum_mul, hw, one_mul]

section Compact

variable [CompactSpace X] [T2Space X] [BorelSpace X]

/-- **The optimal mixed strategy.** If every finitely supported mixed strategy of the maximizer is
held to at most `V` by a pure strategy, some mixed strategy of the minimizer holds every pure
strategy of the maximizer to at most `V`. The solutions of the truncated finite games
(`val_finite_game`) form a directed family of nonempty sets; a point of the intersection of their
closures (compactness of the probability measures) is replaced by a regular measure with the same
neighbourhoods, at which the truncated payoffs are lower semicontinuous; monotone convergence
removes the truncation. -/
private lemma val_exists_le [Nonempty X] {Y : Type*} (f : X → Y → ℝ≥0∞)
    (hf : ∀ y, LowerSemicontinuous fun x => f x y) (V : ℝ≥0∞)
    (hVs : ∀ (s : Finset Y) (w : Y → ℝ≥0∞), ∑ y ∈ s, w y = 1 → ⨅ x, ∑ y ∈ s, w y * f x y ≤ V) :
    ∃ μ : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ : Measure X) ≤ V := by
  classical
  obtain ⟨x₀⟩ := ‹Nonempty X›
  by_cases hV : V = ⊤
  · exact ⟨diracProba x₀, by simp [hV]⟩
  -- the approximate solution sets of the truncated finite games
  let C : Finset Y × ℕ × ℕ → Set (ProbabilityMeasure X) := fun i =>
    {μ | ∀ y ∈ i.1, ∫⁻ x, f x y ⊓ i.2.1 ∂(μ : Measure X) ≤ V + (i.2.2 : ℝ≥0∞)⁻¹}
  have hCne : ∀ i, (C i).Nonempty := by
    rintro ⟨s, N, n⟩
    rcases Nat.eq_zero_or_pos n with rfl | hn
    · exact ⟨diracProba x₀, fun y _ => by simp⟩
    · exact val_finite_game f hf hV s (hVs s) N
        (ENNReal.inv_pos.2 (ENNReal.natCast_ne_top n))
  have hCmono : ∀ (s s' : Finset Y) (N N' n n' : ℕ), s ⊆ s' → N ≤ N' → n ≤ n' →
      C (s', N', n') ⊆ C (s, N, n) := by
    intro s s' N N' n n' hs hN hn μ hμ y hy
    calc ∫⁻ x, f x y ⊓ N ∂(μ : Measure X) ≤ ∫⁻ x, f x y ⊓ N' ∂(μ : Measure X) :=
          lintegral_mono fun x => inf_le_inf_left _ (by exact_mod_cast hN)
      _ ≤ V + (n' : ℝ≥0∞)⁻¹ := hμ y (hs hy)
      _ ≤ V + (n : ℝ≥0∞)⁻¹ := by gcongr
  have hdir : Directed (· ⊇ ·) fun i => closure (C i) := by
    rintro ⟨s, N, n⟩ ⟨s', N', n'⟩
    exact ⟨⟨s ∪ s', max N N', max n n'⟩,
      closure_mono (hCmono _ _ _ _ _ _ Finset.subset_union_left (le_max_left _ _)
        (le_max_left _ _)),
      closure_mono (hCmono _ _ _ _ _ _ Finset.subset_union_right (le_max_right _ _)
        (le_max_right _ _))⟩
  obtain ⟨μ', hμ'⟩ := IsCompact.nonempty_iInter_of_directed_nonempty_isCompact_isClosed _ hdir
    (fun i => (hCne i).closure) (fun _ => isClosed_closure.isCompact) (fun _ => isClosed_closure)
  rw [Set.mem_iInter] at hμ'
  obtain ⟨ν, hreg, hnhds⟩ := val_exists_regular μ'
  refine ⟨ν, iSup_le fun y => ?_⟩
  -- the truncated payoffs are held to `V + 1 / n` at the regular limit
  have htr : ∀ N n : ℕ, ∫⁻ x, f x y ⊓ N ∂(ν : Measure X) ≤ V + (n : ℝ≥0∞)⁻¹ := by
    intro N n
    by_contra hlt
    rw [not_le] at hlt
    have hlsc := val_lsc_lintegral (fun ρ : ProbabilityMeasure X => (ρ : Measure X)) ν
      (fun U hU => val_lsc_measure_open_of_regular ν hreg hU)
      ((hf y).inf lowerSemicontinuous_const) (ENNReal.natCast_ne_top N) (fun x => inf_le_right)
    have hev : ∀ᶠ ρ : ProbabilityMeasure X in 𝓝 μ',
        V + (n : ℝ≥0∞)⁻¹ < ∫⁻ x, f x y ⊓ N ∂(ρ : Measure X) :=
      hnhds (hlsc _ hlt)
    obtain ⟨ρ, hρ1, hρ2⟩ :=
      ((mem_closure_iff_frequently.1 (hμ' ({y}, N, n))).and_eventually hev).exists
    exact absurd (hρ1 y (Finset.mem_singleton_self y)) (not_le.2 hρ2)
  -- monotone convergence removes the truncation
  have hmono : ∫⁻ x, f x y ∂(ν : Measure X) = ⨆ N : ℕ, ∫⁻ x, f x y ⊓ N ∂(ν : Measure X) := by
    rw [← lintegral_iSup (fun N => ((hf y).inf lowerSemicontinuous_const).measurable)
      (fun N N' h x => inf_le_inf_left _ (by exact_mod_cast h))]
    congr 1
    funext x
    rw [← inf_iSup_eq, ENNReal.iSup_natCast, inf_top_eq]
  rw [hmono]
  refine iSup_le fun N => ENNReal.le_of_forall_pos_le_add fun ε hε _ => ?_
  obtain ⟨n, hn⟩ := ENNReal.exists_inv_nat_lt (ENNReal.coe_ne_zero.2 hε.ne')
  exact (htr N n).trans (by gcongr)

/-- **Alpern and Gal (1988), minimax theorem**, for a nonempty compact Hausdorff space `X`. -/
theorem val_minimax [Nonempty X] {Y : Type*} (f : X → Y → ℝ≥0∞)
    (hf : ∀ y, LowerSemicontinuous fun x => f x y) :
    (∃ μ : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ : Measure X) =
        ⨅ μ' : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ' : Measure X)) ∧
      (⨅ μ : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ : Measure X)) =
        ⨆ (s : Finset Y) (w : Y → ℝ≥0∞) (_ : ∑ y ∈ s, w y = 1), ⨅ x, ∑ y ∈ s, w y * f x y := by
  set V := ⨆ (s : Finset Y) (w : Y → ℝ≥0∞) (_ : ∑ y ∈ s, w y = 1), ⨅ x, ∑ y ∈ s, w y * f x y
    with hV
  have hVs : ∀ (s : Finset Y) (w : Y → ℝ≥0∞), ∑ y ∈ s, w y = 1 →
      ⨅ x, ∑ y ∈ s, w y * f x y ≤ V := fun s w hw =>
    le_iSup_of_le s (le_iSup_of_le w (le_iSup_of_le hw le_rfl))
  have weak := val_weak_duality f fun y => (hf y).measurable
  obtain ⟨μ, hμ⟩ := val_exists_le f hf V hVs
  have h1 : (⨅ μ' : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ' : Measure X)) = V :=
    le_antisymm ((iInf_le _ μ).trans hμ) (le_iInf weak)
  exact ⟨⟨μ, le_antisymm (hμ.trans h1.ge) (iInf_le _ μ)⟩, h1⟩

end Compact

end Proof

/-- **Alpern and Gal (1988), minimax theorem.** For a compact Hausdorff space `X` (with its Borel
σ-algebra), a set `Y` and a payoff `f : X → Y → [0, ∞]` lower semicontinuous in its first
argument: the upper value in mixed strategies is attained by a probability measure on `X`, and
it equals the lower value in which the maximizer uses finitely supported mixed strategies.
The minimizer's space is nonempty (there is no probability measure on the empty space). -/
theorem minimax {X Y : Type*} [TopologicalSpace X] [CompactSpace X] [T2Space X] [Nonempty X]
    [MeasurableSpace X] [BorelSpace X] (f : X → Y → ℝ≥0∞)
    (hf : ∀ y, LowerSemicontinuous fun x => f x y) :
    (∃ μ : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ : Measure X) =
        ⨅ μ' : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ' : Measure X)) ∧
      (⨅ μ : ProbabilityMeasure X, ⨆ y, ∫⁻ x, f x y ∂(μ : Measure X)) =
        ⨆ (s : Finset Y) (w : Y → ℝ≥0∞) (_ : ∑ y ∈ s, w y = 1), ⨅ x, ∑ y ∈ s, w y * f x y :=
  val_minimax f hf

end External.AlpernGal
