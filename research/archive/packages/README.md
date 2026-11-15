# Package map — geometry program, verification and frozen discovery

**Preserve all executable and data paths.** This is a navigation and CI-policy reorganization, not a mass move of packages: existing scripts use hard-coded relative file paths, retained SHA256 manifests and independent replay inputs. The pre-squash history and the detailed numerical-era handoffs are archived.

## Priority: geometry identities and response logic

| Package | Scope |
| --- | --- |
| [interval_one_turn](interval_one_turn/) | Closed-negative one-turn comparison: physical continuum law with exact all-Princess potential certificate; complete domain, minimax, finite-law response and earlier upper checks |
| [interval_global_closure](interval_global_closure/) | Exact physical contact integrals, transport/front projections, initial inward and moving-front obstacles, shadow and front-one diagnostics, record Bellman fixtures |
| [interval_continuous_rank](interval_continuous_rank/) / [interval_characteristic_response](interval_characteristic_response/) | Continuous rank and characteristic response experiments; **not** globally sufficient equilibrium classifications |
| [interval_princess_geometry](interval_princess_geometry/) / [interval_turn_sheet](interval_turn_sheet/) | Earlier geometric candidate/turn-sheet construction code; use as source of hypotheses, not final proof |
| [interval_center_pricing](interval_center_pricing/) | Exact postcenter phase reduction and independent response pricing; complete precenter behavior is not thereby reduced |
| [interval_lightcone](interval_lightcone/) | Light-coordinate lattice solvers and continuum LPs (**numerical**, validated against the exact clock-grid optima for n = 1, 2, 3, 4, 6); the exact upper-bound program `atomic_upper.cpp` and its laws; the n = 1024 refinement of the retained field; continuous-time pricing of finite Princess laws; the builder of the strategy page |

Active research questions and links to full arguments live under [research/13-equilibrium-geometry](../research/13-equilibrium-geometry/).

## Frozen certificates — keep intact

| Package | Purpose |
| --- | --- |
| [interval_discovery_certificates](interval_discovery_certificates/) | Retained n512 legal Princess data and independently checked 752-pair physical Monster upper, reports and bound manifests |
| [interval_clock_grid](interval_clock_grid/) | Exact normalized bank, clock/dual construction and independent native verifier |
| [interval_princess_lift](interval_princess_lift/) / [interval_quantile_certificate](interval_quantile_certificate/) | Explicit legal Princess extraction, continuous attack witnesses and exact refinement-ceiling diagnostics |
| [interval_fixed_marginal](interval_fixed_marginal/) / [interval_integer_flow](interval_integer_flow/) | Preserved fixed-law obstruction and independent exact integer-flow regression; scopes are limited to their stated laws |

[REPRODUCE.md](../REPRODUCE.md) distinguishes cheap retention checks from expensive complete response searches. Preserve original source hashes, legal physical strategies and fixed versus limiting lower bounds.

## Legacy discovery, manual-only

The former CDF shape, continuous-record, sparse lower/upper, target-width and joint Monster optimizer packages remain in place for reproducibility and **hypothesis-driven diagnostics**, not automatic bound chasing. Notable: [interval_continuous_lower](interval_continuous_lower/), [interval_mixture_cut](interval_mixture_cut/), [interval_discovery](interval_discovery/), [interval_cdf_shape](interval_cdf_shape/), [interval_lower_bundle](interval_lower_bundle/) and [interval_sparse_upper](interval_sparse_upper/).

Workflows for large discovery searches are now manually dispatched. Geometry-specific exact fixtures have their own push-triggered [structural regression workflow](../.github/workflows/geometry-structural-checks.yml). Tests only audit concrete calculations; a green check cannot establish universal phase sufficiency.

Do not delete or relocate a package merely because its current search class is exhausted: [REPRODUCE.md](../REPRODUCE.md) and retained manifests may depend on its path. A future code move needs a complete import/reference audit and independent replay.
