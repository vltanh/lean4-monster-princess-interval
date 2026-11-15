# Status ledger — interval Princess–Monster research

**Snapshot date:** 2026-11-10 (prior conversation work; staged 2026-11-11 UTC)

**Problem.** Both players independently choose hidden 1-Lipschitz paths in the interval [-1,1], including their starting positions. Capture occurs at the first coincidence. The monster minimizes and princess maximizes expected capture time. No prescribed maximum number of turns; both can randomize privately.

**Definitive open item:** The exact minimax value has **not** been determined. There is no pair of matching unrestricted upper/lower saddle certificates and no theorem that all equilibria lie in a fixed bounded-complexity support family.

## Proven within supplied finite verifiers / written arguments (not independently audited)

| ID | Claim | Scope | Evidence | Caveat |
| --- | --- | --- | --- | --- |
| A1 | Upper guarantee V <= 229233/160000 | Against all continuous princess paths, for a fixed 32-path monster mixture | `interval_pm_proof/PROOF.md`; `interval_pm_proof/verify.py`; saved integer flows | Early, superseded upper bound |
| A2 | Exact best princess response to a specified finite piecewise-linear monster mixture via event deadlines | Arbitrary 1-Lipschitz princess paths; fixed finite monster support | `interval_exact_reduction/REDUCTION.md`, `verify_exact.py` | The converse envelope theorem is a written handproof; the verifier checks finite certificates |
| A3 | Exact best monster response to a specified 60-path princess mixture = 56305800187/40000000000 | Arbitrary 1-Lipschitz monster paths; fixed princess mixture | `interval_exact_response_result/PROOF.md`, `verify.py`/`tests.py` | Requires validity of capture-order structural lemma; not game value |
| A4 | The prior exact-response target is strictly suboptimal | Perturbation and all-minimizer enumeration for same fixed princess support | `interval_target_exclusion/PROOF.md`, `verify_target.py` | Exhaustive search is expensive; no global value |
| A5 | Original 32-monster-path support cannot be globally optimal | Exact fixed-support LP and a better 68-path upper strategy | `interval_equilibrium_check/PROOF.md`, `verify.py`, flows | Excludes only that support, not all M1/M2 trajectories |
| A6 | New upper guarantee V <= 5717477/4000000 = 1.42936925 | Against unrestricted princess paths, supplied 68-path mixture | `interval_equilibrium_check/PROOF.md` Section 4, `exclusion_*` certificates | Better current upper candidate, conditional on handwritten deadline-response argument |
| A7 | Exact response of a 338-path princess distribution = 36290299773897097/25600000000000000 = 1.417589834917855... | Unrestricted monster best response to specified mixture | `interval_uniform_reduction/PROOF.md`, `verify.py` | Better current lower candidate, conditional on capture-order reduction |
| A8 | A small, finite grid game has a fully enumerated rational saddle certificate | Only 259 princess and 720 monster paths on the specified grid | `interval_uniform_reduction/grid_case.json`, `verify.py`, `tests.py` | **Not** the unrestricted game |
| A9 | Uniform finite approximation theorem for full unrestricted game | Asymptotic bound between grid values and V | `interval_uniform_reduction/PROOF.md` | Written proof not formalized, and grids are very large; does not determine exact V |

**Best claimed two-sided bounds from these packages:**

`36290299773897097/25600000000000000 <= V <= 5717477/4000000`

That is `1.417589834917855... <= V <= 1.42936925` (gap ~0.0117794). These are not an exact solution and are subject to audit of the mathematical structural reductions. Previously discussed values 11/8 and ~1.373 do not satisfy the claimed lower certificates for this version of the game.

## Verification audit of this handoff

Ran successfully in extracted directory (Python standard library, no Lean compilation):

- `interval_pm_proof/verify.py`: PASS
- `interval_exact_reduction/verify_exact.py`: PASS
- `interval_equilibrium_check/verify.py`: PASS
- `interval_exact_response_result/tests.py`: PASS
- `interval_uniform_reduction/tests.py`: PASS
- `interval_exact_response_result/verify.py`: PASS (full)
- `interval_target_exclusion/verify_target.py`: PASS (full, 751,782 states)
- `interval_uniform_reduction/verify.py`: PASS (full, 48,228 states)

The initially time-capped `interval_target_exclusion/verify_target.py` was rerun without the short cap and **PASSED** (751,782 response-search states). Both `interval_exact_response_result/verify.py` and `interval_uniform_reduction/verify.py` also **PASSED** on full runs. PASS means the arithmetic and finite-response assertions passed, **not** that all continuous theorems were kernel-checked.

## Firm separation of statuses

- **Closed:** finitely specified response examples and fixed-support optimization, each with their own conditions.
- **Open:** identifying an unrestricted equilibrium or proving a globally exhaustive finite strategy family.
- **Open:** exact value of the full game.
- **Not a proof:** numerical LP search logs, shape speculation, truncated response searches, and guessed rational values.
