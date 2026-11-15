# Complete all-warp ceiling for the archived 338-path Princess law

Date: 2026-11-12. **The unrestricted interval Princess–Monster game remains OPEN.** This proves a global, non-grid-restricted exclusion at the *existing certified upper target*, for one fixed Princess-law deformation class. It does not identify the minimax value or exclude that class from attaining a smaller unknown equilibrium value.

## Theorem

Let `mu` be the exact 338-path reflected Princess law in
`packages/interval_uniform_reduction/princess_strategy.json`. Its certified unrestricted best-response value is

[
c_0=rac{36290299773897097}{25600000000000000}
=1.4175898349178553515625.
]

Let (mathcal W) consist of **all** continuous strictly increasing maps
(psi:mathbb R	omathbb R) satisfying

[
psi(-u)=-psi(u),qquad psi(u+2)=psi(u)+2.
]

There is **no piecewise-affine, fixed-knot, differentiability, or density assumption** on (psi).
Act on each physical path through the common light-coordinate map

[
(U,V)=(t+x,t-x)mapsto(psi(U),psi(V)),
qquad (t',x')=((psi(U)+psi(V))/2,(psi(U)-psi(V))/2).
]

Write (mu_psi) for the transformed Princess law. Then

[
oxed{
c_0  lesup_{psiinmathcal W}inf_{m {m legal}}
mathbb E_{mu_psi}T(m,P)
 leC_{m all}:=rac{570109078983139212403}{400000000000000000000}
=1.4252726974578480310075.
}
]

The upper inequality is certified by **13 actual transformed unit-speed Monster routes** with a fixed rational mixture, selected from the 16 routes in `common_warp_lower_16.cert.json`. It is strict relative to the separately certified unrestricted upper bound

[
U=rac{57045189772271291487410009}{40000000000000000000000000},
qquad
U-C_{m all}=
rac{34281873957370247110009}{40000000000000000000000000}
>0.
]

Thus this entire class of common-coordinate deformations cannot *match the currently certified upper target* (U). It **could** still contain an equilibrium law if the unknown true value is below (C_{m all}). The result is a restriction-of-construction theorem, not an improved full-game bound.

## 1. Why warping does not change the capture event

For any 1-Lipschitz physical path, (U=t+x(t)) and (V=t-x(t)) are nondecreasing. A strictly increasing (psi) preserves that property. Their warped sum (2t') is strictly increasing with physical time, so it reparametrizes a legal 1-Lipschitz path. Also (|U-V|le2), and monotonicity plus (psi(y+2)=psi(y)+2) imply (|psi(U)-psi(V)|le2). Thus warped paths stay in ([-1,1]). Oddness makes the warped starting time zero; the periodic-increment identity makes (t'	oinfty).

The transform is injective on spacetime, so two warped paths meet exactly at the transforms of their original meetings. Along each original path the new time parameter increases. Therefore the **first** original contact ((t_c,x_c)) becomes the first warped contact, at time

[
T_psi=rac{psi(t_c+x_c)+psi(t_c-x_c)}2.
]

This argument also covers starts, endpoint contacts, overlaps, and arbitrary non-piecewise-affine strictly increasing (psi).

## 2. The continuum step-envelope formula

Use the source integer scale (S=256000000). Let (w_p) be the positive integer source weights for the 338 signed Princess paths, with total (W=2cdot10^8). Let (b_ige0) be the new rational Monster numerators with total (Lambda=10^{12}), indexing the original 16 routes. Thirteen are nonzero.

For the physical first contact between Monster route (i) and Princess path (p), record the exact integer light coordinates ((U_{ip},V_{ip})). For any integer coordinate (z), write uniquely

[
z=2k_zS+r_z,qquad -Sle r_z<S,
quad ho_z=|r_z|/S,quad sigma_z=operatorname{sgn}(r_z).
]

The restrictions on (psi) imply

[
psi(z/S)=2k_z+sigma_z,psi(ho_z).
]

Since (g(s)=psi(s)) on ([0,1]) is continuous and strictly increasing with (g(0)=0,g(1)=1), the nonatomic Stieltjes probability measure (dg) satisfies
(psi(ho)=int_0^1 {f1}_{s<ho},dg(s)); the strict convention is immaterial because (dg) has no atoms.

Define the step function

[
A(s)=
rac1{2WLambda}
sum_{i,p}b_iw_p
sum_{zin{U_{ip},V_{ip}}}
igl(2k_z+sigma_z{f1}_{s<ho_z}igr)
quad(0<s<1).
]

If (
u_psi) is the physical mixture of the transformed Monster routes, then the first-contact formula gives the **exact identity**

[
mathbb E_{
u_psi,mu_psi}T
=int_0^1 A(s),dg(s)
le sup_{0<s<1}A(s).
]

Only those (ho_z) strictly between 0 and 1 can change (A). The source contact list has **4,394** first contacts for the 13 positive routes, but only **75 distinct nontrivial step thresholds**. There are hence only 76 open step cells to check, not 16 warp bins and not a sampled continuum.

In integer arithmetic, the initial open-cell numerator is

[
B_0=sum_{i,p,z}b_iw_p(2k_z+sigma_z),
]

and crossing threshold (r) adds

[
Delta(r)= -sum_{i,p,z: |r_z|/S=r}b_iw_psigma_z.
]

Sweep all 75 thresholds in sorted order. The maximum of the 76 cumulative numerators, divided by (2WLambda), is exactly

[
max A(s)=
rac{570109078983139212403}{400000000000000000000}.
]

One maximizing open cell starts just to the right of (s=15/16). Concentrating (dg) arbitrarily strongly in such a cell, while retaining a small positive density elsewhere, shows this is also the **supremum of the payoff of this *fixed Monster mixture*** over (mathcal W). It is not the optimum response value of the warped Princess law.

Because any Monster mixture provides an upper bound on the Princess law's best-response guarantee, the displayed theorem follows. The identity warp proves its left inequality. Uniform limits of strictly increasing warps obey the same bound as an approaching-family statement; noninjective limiting maps are not treated as literal contact-preserving transformations.

## 3. Exact machine certificate and its limits

The complete certificate is:

- `packages/interval_global_closure/common_warp_lower_all.cert.json` — all 16 weight numerators (three zero), the exact ceiling, source Git blob IDs, and the full-game upper comparator.
- `packages/interval_global_closure/verify_lower_warp_all.cjs` — full Monster/Princess geometry validation, 4,394 first-contact computations, the independent exact step sweep, a second envelope implementation, and **16 independent folded-ramp versus step-integral equalities**.
- `packages/interval_global_closure/common_warp_lower_bigint.cjs` — the preexisting exact chronological first-contact engine and independent step-envelope implementation.

At the repository root, run:

```sh
node packages/interval_global_closure/verify_lower_warp_all.cjs
```

The complete certificate computation and all 16 cross-checks **PASSED in V8** on the exact committed source contents. This continuation does not claim a separately executed native Node invocation, Lean compilation, or CI. Discovery used a floating-point finite LP on the 76 exact cells; **its optimality is not claimed or needed**. Only the frozen rational mixture, exact contact computation, and the 75-breakpoint verification establish this theorem.

## 4. Interpretation for the global proof

The prior 16-knot certificate bounds its smaller deformation family by (1.41758984127931ldots), but does not cover finer, smooth, or singular-continuous warps. Indeed its *old* 16-route weights have exact all-warp worst payoff
(
122872075489310371129/80000000000000000000
=1.535900943616379ldots
)
and cannot simply be extrapolated.

The new 13-route mixture is adapted to **every** infinitesimal warp interval. Its ceiling is weaker numerically than the 16-knot ceiling but has no warp-resolution restriction.

Nothing here supplies the missing unrestricted saddle pair. In particular, a value (V<C_{m all}) remains possible, and an arbitrary Princess law outside the orbit ({mu_psi}) is unrestricted by this result. The main G5–G8 obligations remain open.
