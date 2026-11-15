# Complete singular-tail attachment experiment

This experiment constructs an admissible normalized monster law with a
continuous integrable endpoint density. It does **not** construct a matching
princess law or close the unrestricted equilibrium proof. Its unsuccessful
phase selection is retained as a reproducible structural test.

## Representation

The old eleven outer density intervals and the signed-M3 geometry are unchanged.
The public coefficient vector is `(w0, f, g, k, ell, B)`, with one new scalar
`B >= 0`. The last old `f` coefficient is fixed to zero. Its interval is replaced
by

\[
 f(1-\epsilon)=B\epsilon^{-2/3}
 H(\log(16/\epsilon)),\qquad 0<\epsilon<1/64.
\]

The last old `k=ell` coefficient stops at `1-10^-5`; on the remaining interval,

\[
 k(1-\epsilon)=\ell(1-\epsilon)
 =\frac B2\epsilon^{-1/6}H(\log(16/\epsilon)).
\]

The original last `g` coefficient remains free. The extra knot at `1-10^-5`
only integrates the fixed replacement: it adds no constant-density variable.
`H` uses twelve terms of the convergent pantograph series in `endpoint_tail.py`.
The density itself is positive and increasing on these supports; the fitted
law need not solve the endpoint stationarity system exactly.

The column includes the changes in both late-M2 sheets, the negative early-M2
sheet, and both small-start early-M3 sheets. It also includes the compensating
line-mass changes. The column alone is a signed linear perturbation; the **full
law** becomes a probability law only after the line residual, edge, join,
normalization and suffix conditions are imposed.

`TailLaw` in `singular_tail_law.py` owns the truncation map and all 54 inequality
rows and 6 equality rows. The monotonicity condition on `p=f+g` is removed using
the ordered-prefix theorem. Monotonicity of `f` and `k`, the physical residuals,
and the late suffix conditions remain explicit. The normalization is

\[
 w_0+\int_0^1(f+g+k)_{\rm step}
 +B(F_0+K_0)=1,
 \qquad F_0+K_0=1.264436350941335.
\]

## Continuous response and verification

`singular_tail_negative.py` pools the reversed continuous `p` tail using its
exact partial mass, then solves for the total-`k` crossing. Negative inverse
pieces remain constant ordered blocks. `singular_tail_prefix.py` solves the
positive-prefix crossing and treats the total-`k` endpoint as infinite when
`B>0`; it does not clip that crossing at `1-10^-12`. Frozen rows retain both
negative blocks and positive affine pieces.

The following independent checks were completed:

* 24 moment comparisons with adaptive integration, maximum relative error
  `2.283e-12`.
* 8 f/k Stieltjes reconstructions of complete tail features from previously
  capture-checked step laws, maximum absolute error `1.811e-10`.
* 6 further block-aware f/k reconstructions, maximum absolute error
  `1.850e-10`, plus 24 zero-tail block consistency checks.
* 42 independent continuous sheet-mass kernel checks, maximum absolute error
  `2.887e-12`. A separate feasibility solve produces a normalized attachment
  with `B=.06` and nonnegative structural slack.
* On all 18 active fitted rows with positive `c`, reducing positive-prefix
  interpolation tolerance from `2e-7` to `2e-9` changed the score by at most
  `9.28e-18`.

These are floating verification results, not interval enclosures. The driver
searches the ordinary four-scalar domain, a logarithmic endpoint domain, and
the exact face `y=c`. This resolves the terminal scale without adding density
bins, but is still numerical global separation.

For the integrable extension of the response calculation, the primitives stay
finite and continuous. Monotone integrability gives
`(1-s)f(s),(1-s)k(s) -> 0`, removing the integration-by-parts endpoint terms.
On the fixed M3 support, `4 +/- z - s >= 23/8`, so its marginal mass is bounded
by a constant times `integral k`; the M2 masses have the same type of bound.
Finite first-capture payoffs then control discarded tail mass uniformly.
This direct argument avoids claiming that naive capping preserves every late
Gamma jump, which it need not do.

## What the full-law fit found

`discover_singular_tail.py --rounds 6` writes `singular_tail_discovery.json`.
The final full law has normalization `1`, minimum imposed slack `0`, and

| Quantity | Fitted value |
| --- | ---: |
| Common amplitude B | 0.04375050127508108 |
| Analytic f mass | 0.05531605430600686 |
| Analytic k mass | 0.000003669878110880889 |
| f at its outer join | 1.0072346401563779 |
| k at its outer join | 0.2967499553981415 |

The numerical scalar response was `1.42634015855`, while the finite response
LP objective was `1.42633987512`. These numbers report the experiment and its
remaining separation gap; they are not a new game-value interval. This law is
worse than the preceding relaxed-p density law.

More consequentially, none of its positive-weight frozen response rows has a
negative `c` and `y=c`. Negative-c rows instead have total dual weight
approximately `.13834`, initial points near `.9903`, and an extra excursion to
`y approx .625`. The incoming cutoff varies over those rows. These multipliers
are not a certified lower strategy because shape normals remain nonzero.

The strongest relevant normal is the `k` join at `.99999`, of magnitude
`.0032169`. Other nonzero genuine shape normals occur at the `f` joins
`.96875` and `.984375`, and at the `k` join `.96875`. The nonzero multiplier at
the first f join is degenerate at two zero densities. The residual after the
negative M3 sheet is a physical nonnegativity constraint and is recorded
separately from these shape conditions.

For a direct suffix diagnostic, at `(a,c)=(.99,-.6)` the best incoming inverse
for `y=c` gives score `1.41471675`; keeping that prefix and taking `y=.625`
increases the score by approximately `.011591`. The negative ordinary phase
therefore has a concrete profitable suffix change in this attached law.

The fixed old condition `k=ell` above `.875` pins the outer terminal density
near `.274-.297`. This does not supply the smaller intermediate `ell` required
by the prospective ordinary endpoint stationarity. The conclusion is a failure
of this **fixed outer attachment**, not an exclusion of integrable endpoint
tails. The next construction changes the initial-inward support and the outer
prices jointly; repeated cutoff fits would not address this missing condition.

## Reproduction

From the repository root, using the session's experiment dependencies:

```sh
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_density/singular_tail_basis.py
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_density/verify_singular_tail_basis.py
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_density/verify_singular_tail_negative.py
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_density/verify_singular_tail_law.py
PYTHONPATH=/workspace/scratch/f5595f62cf06/experiment_deps python -B packages/interval_turn_density/discover_singular_tail.py --rounds 6
```
