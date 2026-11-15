# Exact affine regions for the record Bellman gate

## Scope and source

This audit concerns the remaining outward inequality in PREONE_RECORD_BELLMAN.md. It does not certify an unrestricted lower payoff, repair the known global cost deficits of the snapshot, or identify an equilibrium.

The input is the exact saved field:

- repository: vltanh/lean4-monster-princess;
- source commit: 7fc6bf61b26afe034b27bc0d621721b8f7272ead;
- path: packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json;
- Git blob: 5c45d042ee9948faebc03354c3e1e2ee3cbec1a5.

The V8 verifier embeds the independently checked rational field reader preserved as blob 5714f57ada458f38ef8b46adb32be2472a009622. Coordinates use the same signed continued-fraction recovery with denominator at most \(2^{22}\); CDF values remain exact decimal rationals. The Node entry point checks the input Git blob hash. The same verification and the complete classification were run with BigInt rationals in the tool V8 isolate during the executor outage. Python and Node were not rerun during that outage.

## 1. Eliminate the lower record in a positive branch

In the nonautomatic case, let
\[
M=R(U,V),\qquad l_0=R(U,w),\qquad l_0<L\le M.
\]
The direct first-turn flux formula makes \(G(L)\) nondecreasing. At \(L=l_0\) its entire prefix-flux term vanishes: for every \(z\le w\), transport gives \(R(U,z)\ge R(U,w)=l_0\). Therefore
\[
G(l_0)=
\left[\alpha_{l_0+}(s)-\frac{U+w}{2}\right]R_U(U,w)
-\left[\beta_{M+}(w)-\frac{U+V}{2}\right]R_U(U,V).
\tag{1}
\]
A nonnegative lower bound for (1) proves the outward derivative inequality for every permitted lower record \(L\), without using a sampled \(L\) or a comparator threshold.

## 2. Four-triangle Farkas identities

Fix four triangles giving the current field at \((U,V)\), the first-turn field at \((U,w)\), the inverse point \((s,z_\alpha)\), and the inverse point \((u_\beta,w)\). On an interior inverse branch,
\[
R(s,z_\alpha)=l_0,\qquad R(u_\beta,w)=M,
\]
with negative \(R_V\) on the alpha triangle and positive \(R_U\) on the beta triangle. Both inverse coordinates are affine in \((U,V,w,s)\). Hence (1) is affine on the joint branch.

For each recorded branch the JSON contains nonnegative rational multipliers and a positive rational constant satisfying
\[
G(l_0)=b+\sum_j\lambda_j E_j(U,V,w,s),\qquad
b>0,\quad \lambda_j\ge0,
\tag{2}
\]
where \(E_j\ge0\) are oriented triangle-edge inequalities. The verifier reconstructs the edge forms and proves all five affine coefficients equal exactly. No numerical linear-programming output is trusted by the verifier.

There are **380 exact identities**. They use triangle inequalities alone; no record, active-cost, or sampled-plan constraint is needed for their positive lower bounds. Their original seeds were finite discovery probes, so these 380 branches are not asserted to exhaust the geometric branch universe.

The branch with current/first/alpha/beta indices
\[
(2048,2050,2203,2182)
\]
has the exact lower bound
\[
\frac{207757068038168920878156147417914545027047}
 {235839619970279691493723400000000000000000000}
>0.
\]
It is approximately \(0.0008809252154678263\). This is a Bellman derivative residual, not a game-value bound. The full edge multipliers, witness coordinates, and other branch identities are in the companion JSON.

For each identity the verifier also checks the witness belongs to the declared domain, the current and first-turn triangles give the actual right-\(U\) derivative, and the two actual right-rank first inverses equal the declared affine inverse points. There are **760 exact inverse-witness checks**.

## 3. Inverse faces remain separate

A continuous CDF can have an inverse jump across a flat row. Thus an interior affine identity cannot automatically be applied on every boundary face with the same formula.

The separate one-sided inspection checks the vertices and edge interiors of all distinct inverse triangles. It has **582 checks** and flags **23 jump contacts**: ten alpha contacts and thirteen beta contacts. These are reported as unresolved, not silently accepted. Current/first derivative faces likewise use their actual right-\(U\) triangle.

For example, a pre-one alpha row can reach a flat-rank interval extending left of the nominal inverse point; the right-rank alpha then moves to its left edge. At a beta point with \(U=1\), a post-one plateau can move the right-rank beta later. Both effects can lower (1). The manifest therefore describes the certificates as positive affine extensions on their declared branches, with actual jump faces separately identified.

## 4. A universal bound for every second turn at s >= 1

Two speed bounds remove the whole beta arrangement and every post-one alpha arrangement:
\[
\beta_{q+}(w)\le w+1,
\qquad
\alpha_{q+}(s)\ge\alpha_{q+}(1)+\frac{s-1}{2}
\quad(s\ge1).
\tag{3}
\]
The first follows from \(p_q(t)\le1\). The second follows from the speed bound \(d(t+p_q(t))/dt\le2\), with the same first-inverse convention. Right-rank limits preserve both inequalities.

Since \(R_U(U,w)\ge0\), (1) is bounded below by
\[
\begin{aligned}
Q(U,V,w)={}&
\left[\alpha_{l_0+}(1)-\frac{U+w}{2}\right]R_U(U,w)\\
&-\left[w+1-\frac{U+V}{2}\right]R_U(U,V).
\end{aligned}
\tag{4}
\]
The omitted term \((s-1)R_U(U,w)/2\) is nonnegative. Thus \(Q\ge0\) proves the required derivative condition for **all** second turns \(s\ge1\), including arbitrary post-one inverse plateaus. No post-one density inequality is used in (3)-(4).

This bound is sufficient and can be conservative. A negative value of \(Q\) is not an improving monster route and does not imply that the actual \(G\) is negative.

## 5. Complete finite closed cover for the stronger gate

The high-current-state domain is
\[
255/256\le U<1,\qquad -U\le V\le w<U,\qquad
R(U,V)\ge A(255/256).
\tag{5}
\]
It is the nonautomatic Bellman case for every positive monster history starting at \(a\ge255/256\): its upper record never decreases below \(A(a)\), and an outward derivative can capture new upper ranks only when that record equals the current CDF.

For (4), only the current triangle, the first-turn triangle, and a one-dimensional affine inverse piece of \(R(1,\cdot)\) are needed. The verifier constructs a complete closed cover of (5):

1. Clip every eligible current triangle by (5)'s \(U\) and rank conditions.
2. Clip every eligible first-turn triangle by the same \(U\) range and by each relevant rank interval of the row-one inverse.
3. Couple the two polygons through their common \(U\) and the order \(V\le w\).
4. Retain lower-dimensional intersections as well as interiors. At a flat row-one rank, the actual right inverse uses the piece on the higher-rank side; that closed piece is included.
5. Remove a cell only when \(R(U,V)-R(U,w)\) is identically zero, so no nondegenerate first inward capture \(l_0<L\le M\) is possible.

Every clipping, feasibility comparison, and extremum calculation uses rational arithmetic. There are no floating pruning decisions.

The exact counts are:

| Quantity | Count |
|---|---:|
| Eligible current triangles | 156 |
| Eligible first-turn triangles | 1,254 |
| Nonflat row-one inverse pieces | 52 |
| First-triangle/rank variants | 2,710 |
| Coupled pairs surviving exact bounding-box/rank pruning | 72,389 |
| Empty coupled pairs | 172 |
| Identically zero lower-rank-gap cells | 1,054 |
| Feasible nondegenerate closed cells | 71,163 |
| Cells with \(Q\ge0\) throughout | 38,197 |
| Cells needing a comparator or a sharper actual-inverse bound | 32,966 |

These are cells in a closed cover, including shared faces, not a claim of disjoint parameter regions.

## 6. Why the cell minimum is exact

For a fixed \(U\), the current polygon supplies an interval
\([V_{\min}(U),V_{\max}(U)]\), and the first-turn polygon supplies
\([w_{\min}(U),w_{\max}(U)]\). Their product is clipped by \(V\le w\).

Between consecutive polygon-vertex \(U\) coordinates, all four interval bounds are affine. Add every intersection of these affine bounds as a further \(U\) breakpoint. Within each remaining interval the vertices of the clipped rectangle are affine functions of \(U\). Since \(Q\) is affine, its value at each such vertex is affine in \(U\), and its minimum occurs at a breakpoint. Checking those finitely many rational vertices therefore gives the exact minimum over the entire cell. Degenerate polygons and single-\(U\) slices are retained.

This is an exact finite geometric verification, not a finer sampling mesh.

## 7. Reproduction

The companion files are:

- packages/interval_cdf_discovery/verify_record_bellman_regions.cjs;
- packages/interval_cdf_discovery/snapshots/record_bellman_regions.json.

With Node:
\[
\texttt{node verify\_record\_bellman\_regions.cjs FIELD\_JSON CERTIFICATE\_JSON --universe}
\]
Run from the package directory, or pass absolute paths. Omitting the two paths uses the saved snapshot and companion certificate beside the script. The quick mode verifies all Farkas identities and physical inverse witnesses, and reports the separate jump contacts. Adding the universe flag recomputes the complete exact classification.

In a V8 tool isolate, the file is a self-contained expression. Evaluate it with
\[
\texttt{Function("return (" + source + ")")()}
\]
and call the returned verifyRegions or classifyPostGate functions with the parsed field and certificate. The tool execution reproduced all counts above in about thirty seconds.

## 8. Remaining obligation

The 32,966 cells failing the conservative gate need a cost comparator or a sharper actual first-inverse bound. They are not attacks. The \(s<1\) continuation family is not covered by (3)-(4). The 23 inverse jump contacts in the separate four-triangle certificates remain explicitly distinguished. Finally, the earlier note's boundary continuation and initial-payoff obligations remain necessary.

No complete record Bellman certificate, unrestricted lower bound, or matching equilibrium is claimed here.


## 9. Subsequent high-start post-turn closure

RECORD_BELLMAN_POST_GATE.md and verify_record_bellman_post_gate.cjs
regenerate and close the genuinely delayed \(s\ge1\) branch on the stated
high-start domain, using history floors and exact cost comparators.
That complete later certificate supersedes the conservative failures in
Section 5 for this branch. It does not resolve delayed \(U<s<1\), the
other-domain inverse contacts in Section 3, or the full game's value.
