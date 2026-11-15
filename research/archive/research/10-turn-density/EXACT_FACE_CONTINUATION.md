# Exact response oracles and the unresolved joint candidate

The unrestricted interval-game proof is still open. This checkpoint does not
change the established rigorous bounds or claim a saddle. Its main new
certificate identifies the entire finite maximizing face of the archived
67-pair monster law with exact integer arithmetic.

## Exact primary face of the archived monster law

The law is exactly the one in
`packages/interval_refined_upper/strategy.json`: all 67 positive integer masses
and their paired physical routes agree. Its unrestricted response supremum is

\[
36563170811/25600000000.
\]

The rational event geometry includes 465 candidate routes; 398 have zero mass
in this particular law. They introduce additional query times and levels
without changing its payoff. The resulting cut network has 80,892 nodes and
176,922 directed capacity arcs. A stored flow and cut have equal integer
capacity 19296189851562500000000000.

An independent replay reconstructs capacities, checks every capacity bound
and conservation equation, reconstructs the source cut from positive residual
capacities, and recomputes the complete residual condensation. It contains
10,125 strongly connected components and 19,729 intercomponent edges.
The minimal and maximal response rows both give the displayed rational value
exactly. Replaying these checks does not rerun max-flow augmentation.

This identifies a response face for a supplied monster law. It does not show
that this law is optimal among monster laws. The face is being used to find
directions that lower its unrestricted response, avoiding reliance on an
unstable finite LP objective.

## Exact finite-law monster oracle

`finite_quantile_response.mjs` searches arbitrary monster capture orders
against a specified finite rational polygonal princess law. Its ordered mode
works directly with strict and closed marginal CDF records instead of
expanding every quantile path at every crossing. The existing capture-order
theorem supplies exhaustiveness; same-anchor dominance retains exact
continuation comparisons.

The core and verifier were independently executed in V8. All 40 archived
raw cases and 40 corresponding ordered cases agree; 24 additional subunit
fixtures agree with unpruned and explicitly sorted searches; 1,920 ray queries
agree with independent segment intersections. The archived 60-path optimum
is reproduced exactly as 56305800187/40000000000.

This finite-law theorem does not apply to a sampled continuous component as
a global lower certificate.

## Why the current dual realization is insufficient

A finite-master dual initially gave 37 epsilon-realized radial paths.
Exact unrestricted search defeats its stronger ordered coupling. In
particular, a shared incoming characteristic produces a low capture payoff
even when the common epsilon is made smaller. The relevant first-contact
atom cannot be erased by treating a limiting payoff row as an attained
physical path.

The later mixed law combines the complete saved continuous CDF with a small
finite component. Its payoff must be scored using the ordered coupling of
the full marginal mixture, not by averaging its component capture payoffs.
`mixed_cdf_payoff.mjs` performs that exact strict/closed record integration,
including endpoint and center atoms. Its verifier passes 64 pure-finite and
28 pure-continuous crosschecks, and an independent positive-M1 first-moment
identity. These checks were independently reproduced.

The round-41 mixed candidate still fails a positive-M1 route starting at 3/5:
its exact cost is below 7117/5000. A separate exact early positive-M2 route
starts at a=262143/262144 and turns at U=524287/524288. Its continuous-field
cost is

\[
3037502927420596050426366332305024657/
2134207024934514851840000000000000000,
\]

and its ordered mixed-law cost is approximately 1.4232167207728863.
Both are actual route costs, not value bounds. The exact fractions and
coordinates are saved in `early_positive_m2_tail_attack.json`.

The latter attack probes the final affine incoming corner. A discovery
scan across neighboring scales distinguishes this unresolved corner from
the earlier fixed-U=1 M2 deficit. A proof cannot assume that the last affine
cell already represents a valid analytic endpoint attachment.

## Closed high-start delayed branch

The pre-center record Bellman calculation uses the lower-record floor
\(L\ge R_<(\max(255/256,-V),V)\) implied by the full monster history.
For the specified field and current \(255/256\le U<1\), the genuinely
delayed branch with second turn \(s\ge1\) is now closed. A complete
independent replay regenerated 45,092 active cases, checked 9,321 endpoint
and 8,419 fixed-one quadratic Bernstein pairs, and verified the strict
post-one slope margin \(91472232581/10^{12}\) on all 1,156 relevant triangles.

Direct-inward and immediate-outward boundary plans merge by finite
prepending within the full envelope. Genuinely delayed \(U<s<1\), the
center and record-aware \(U=1\) continuations, initial cost inequalities,
and a matching global upper law remain necessary. This scoped continuation
theorem does not repair the saved field's known global cost deficits.
See RECORD_BELLMAN_POST_GATE.md for the complete domain and proof.

Further exact searches find a late negative-M2 attack on the round-41
mixture with cost approximately 1.4224439541715264. Its four exact small
turn perturbations remain below the candidate's finite-master value,
so this is a robust mass-allocation defect rather than an isolated
characteristic coincidence. A route with a waiting prefix and a separate
unit-speed route with five interior turns also attack that mixture.
Their continuous-field costs differ from their full mixed-law costs;
each saved report retains both.

## Verification scope and reproduction

The saved certificates and mathematical cores were executed in the V8 tool
runtime. The native executor remains unavailable; the new Node command-line
and file-I/O wrappers were not executed there. No Lean compilation or CI was
run. The inaccessible earlier working tree is not claimed fully recovered.

Run the finite and mixed response verifiers using the saved snapshot inputs.
Run `packages/interval_turn_density/verify_atomic_seed_integer.cjs` to replay
the exact incumbent flow/face certificate. The corresponding proof notes
state the reduction theorems and contact conventions on which these finite
computations rely.

The remaining objective is unchanged: construct the same exact constant and
matching unrestricted strategies, with a uniform limiting lower construction
if necessary. The finite LP objectives, failed candidate laws, and completed
response-oracle checks are not substituted for that objective.
