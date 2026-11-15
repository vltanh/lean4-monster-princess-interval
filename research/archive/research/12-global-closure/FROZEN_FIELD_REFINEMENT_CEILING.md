# A ceiling for refinements of a frozen full-width field

Exact response searches at finer resolutions cannot lift the standard
`bank minimum minus mesh width` certificate for either full-width CDF below
to within `1e-4` of the currently retained Monster upper. A single compatible
physical attack proves this independently of how efficiently the complete
bank is priced. This does not preclude reducing the Monster upper itself.

This is a ceiling on that **fixed-input certificate procedure**, not a new
upper bound for the game. A separately extracted narrow interpolation is a
different Princess law; this argument does not bound its actual security.

## 1. The nodal-record bridge

Let \(F\) be a legal symmetric common-threshold CDF with continuous interior
traces and sticky endpoint paths. Use its **full-width** interpolation,
\(\varepsilon=1/2\). Let \(m\) be a unit-speed physical Monster route that
visits both endpoints, completes by \(T\), and belongs to the normalized
physical bank at mesh \(h=1/(2n)\). Every turn and endpoint visit is a grid
node, with the bank's parity convention
\(n(t+x),n(t-x)\in\mathbb Z\).

Write \(S_m(t)\) for actual surviving probability after capture at time
\(t\). Before its own endpoint is reached, the left clock is the running
minimum of the interior CDF trace, and the right clock is the running
minimum of its complement. The corresponding clock is **reset to zero at
its actual endpoint visit**. Thus the two records sum to \(S_m\), including
endpoint atoms and their capture times.

Transport makes \(F(t,m(t))\) nondecreasing on a unit rightward leg and
nonincreasing on a unit leftward leg. Consequently its extrema over each
mesh edge occur at that edge's nodes. The minimum causal vertex-clock
price of this particular route is therefore exactly

\[
 P_n(m;F)=h\sum_{j=0}^{T/h-1}S_m(jh).
 \tag{1}
\]

The left sample includes the update at that node; no mass is charged after
its own endpoint capture. In the integer implementation the clock prices
are \(D\pm g\), so (1) is the sum of raw clock units divided by \(4nD\).
There is no additional reflection factor.

Survival is nonincreasing and \(S_m(T)=0\). Comparing the left and right
rectangle sums gives

\[
 0\le P_n(m;F)-C_m(F)
 \le h\bigl(S_m(0)-S_m(T)\bigr)
 =hS_m(0)\le h,
 \qquad C_m(F)=\int_0^T S_m(t)\,dt.
 \tag{2}
\]

Let \(c_n(F)\) be the complete normalized-bank minimum. The admitted route
implies \(c_n(F)\le P_n(m;F)\), and hence

\[
 \boxed{c_n(F)-\frac1{2n}\le C_m(F).}
 \tag{3}
\]

No complete response search is needed to establish this ceiling. The
route must be admitted by the particular bank; a restricted search that
excludes it does not inherit (3).

## 2. Two exact retained obstructions

The frozen fixtures and their independent chronological integrations are
in [`packages/interval_quantile_certificate`](../../packages/interval_quantile_certificate/README.md).

| Full-width input | Physical route, as `(time, position)` | Exact ceiling on \(c_n-h\) |
|---|---|---|
| Retained n256 field | `(0,31/32) → (63/32,−1) → (127/32,1)` | \(36421298289/25600000000=1.4227069644140625\) |
| Its incoming-front-two completion | `(0,7/8) → (123/128,−11/128) → (131/64,1) → (259/64,−1)` | \(14570592687/10240000000=1.42290944208984375\) |

The first route reaches the center before time two and its first endpoint
at \(63/32<2\). The second reaches the center before time two, continues
along its current unit leg to the first endpoint at \(131/64\), and then
visits the other endpoint. Both are members of the normalized bank,
including its post-time-two endpoint-tour convention. Their turns satisfy
the bank parity condition whenever \(n\) is a multiple of 64.

For the saved n256 profiles, take \(n\in256\mathbb N\) and exact integer
refinement of their full-width fields. Such refinement preserves the CDF,
so (3) applies at every one of these resolutions. The respective source
files and SHA-256 values are:

* `packages/interval_clock_grid/lower_n256_field.json`:
  `81483589b60c14d823d2bb467015a321d77cf555076fe8d69a36d63cd829d7d5`.
* `packages/interval_global_closure/lower_n256_front2_field.json`:
  `a8e1d84d67e66e08d6d1eeb02f18c6e5121108cb4368ededd9db2e792a97189e`.

The attacks also upper-bound the actual security of these two specified
full-width CDFs. They do not upper-bound the security of another law made
from the same nodal data with a different interpolation width. In
particular, they must not be applied as attackers against a saved narrow
Princess law without rescoring that law.

For example, the retained upper `291849329389899/204800000000000`
exceeds the front-two ceiling by exactly
`437475649899/204800000000000 = 0.0021361115717724609375`.
Thus this fixed geometry and the standard transfer alone cannot achieve
the requested `1e-4` width while that upper is held fixed.

## 3. Pure probability flooring

Suppose exact refined radial values are instead replaced by
\(\lfloor Dg\rfloor/D\), without any further modification. At each node
the signed CDF error is less than \(1/(2D)\). Running minimum is
nonexpansive in the uniform norm; the actual endpoint resets are shared.
Thus each clock record changes by at most \(1/(2D)\), and the sum changes
by at most \(1/D\). Directly from the \(T/h\) charged samples,

\[
 |P_n(m;F_D)-P_n(m;F)|\le\frac{T}{D},
 \qquad
 \boxed{c_n(F_D)-\frac1{2n}\le C_m(F)+\frac{T}{D}.}
 \tag{4}
\]

Here \(F_D\) denotes the purely floored nodal field and its prescribed
extension. The comparison needs only its nodal values on the route. The
same error estimate also holds for its full-width continuous interpolation
because the common-threshold averaging weights are nonnegative.

The horizons are \(T=127/32\) and \(T=259/64\), respectively. At
\(D=10^9\), the allowances are less than \(4.05\times10^{-9}\). A different
repair, transport projection, or reoptimization requires a fresh error
bound; (4) does not assume such a change is harmless.

## 4. Small exact regression

```bash
python packages/interval_quantile_certificate/test_refinement_ceiling.py \
  --report /tmp/refinement_ceiling_replay.json
```

The regression binds both input and route hashes, recomputes each exact
continuous payoff using the supporting-plane integrator and an independent
chronological record integrator, and samples each route at
\(n=256,512,1024\). Fraction arithmetic verifies (2), the integer
\(4nD\) normalization, and (4) for \(D=17\) and \(10^9\). It constructs
no refined field table and runs no complete Monster-response oracle.

The useful next change is to the candidate CDF, the lower certificate being
proved, or the physical Monster law. Finer evaluation of either unchanged full-width input through
\(c_n-h\) is subject to the explicit ceilings above.
