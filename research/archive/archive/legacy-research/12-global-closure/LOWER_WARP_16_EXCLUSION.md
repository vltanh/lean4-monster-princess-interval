# A complete no-go certificate for sixteen-knot warps of the archived Princess law

Date: 2026-11-12. **The unrestricted interval game remains open.** This note
closes one *global deformation family* of a specified exact lower law. It
does not produce a new bound on the full game or a matching saddle.

## Statement

Let μ be the archived symmetric **338-path** Princess distribution in
`packages/interval_uniform_reduction/princess_strategy.json`, with exact
unrestricted Monster response
[
c_0=rac{36290299773897097}{25600000000000000}.
]

Let ψ be any continuous odd 2-periodic-increment map satisfying
(ψ(x+2)=ψ(x)+2), (ψ(0)=0), (ψ(1)=1), and nonnegative
piecewise-affine slopes on the **fixed knots** (j/16), (j=0,dots,16).
When its increments are strictly positive, ψ defines a bijection of
legal paths in light coordinates, (U=t+x,V=t-x):
[
 (U,V)mapsto(ψ(U),ψ(V)).
]
Write (μ_ψ) for the image Princess law. Then
[
 oxed{
 c_0le sup_{ψ}inf_{m {m legal}}E_{μ_ψ}T(m,P)
 le C_{16}:=
 rac{2268143746046896063134267573}
 {1600000000000000000000000000}.
 }
]
The left inequality uses the identity warp. The same right inequality
holds for non-strict limiting warps as a bound on their *approaching*
strictly increasing realizations. In particular,
[
 0le C_{16}-c_0
 =rac{10178327500634267573}
 {1600000000000000000000000000}
 <7cdot10^{-9}.
]

Thus all strictly increasing warps on this grid, including highly
nonuniform ones, are effectively excluded as a route to a meaningful
lower-bound improvement. **This is not an upper bound on the full game**:
it concerns only warps of one fixed Princess distribution.

## Proof: one finite Monster mixture controls every warp

Put (d_j=ψ((j+1)/16)-ψ(j/16)), so (d_jge0) and
(sum_{j=0}^{15}d_j=1). Define (Φ_j) on ([0,1]) to be 0 through
(j/16), linear from 0 to 1 on the (j)-th knot interval, and 1
thereafter; extend it oddly and with
(Φ_j(x+2)=Φ_j(x)+2). Then
(ψ=sum_j d_jΦ_j) pointwise on the real line.

For an original Monster route (m), first meeting with any original
Princess path occurs at ((U_c,V_c)). Every strictly increasing common
warp preserves *which event is the first meeting* and maps its time to
((ψ(U_c)+ψ(V_c))/2). Consequently the payoff of the warped
Monster route against the warped 338-path law is **linear** in (d):
[
 C_m(d)=sum_{j=0}^{15}a_{mj}d_j,qquad
 a_{mj}=rac1{2W}sum_{pinmathrm{supp},mu}
 w_p{Φ_j(U_c(m,p))+Φ_j(V_c(m,p))},
]
where (W=sum_p w_p). The response minimization on the Monster side
therefore need not be enumerated to establish the *upper* certificate
for this candidate deformation family.

The JSON certificate specifies **16 actual unit-speed Monster
routes** (m_i) and nonnegative rational probabilities
(lambda_i=b_i/10^{12}), summing to one. The routes are legal and visit
both endpoints. Since μ is reflection-symmetric, each route can
also be fairly paired with its reflection without changing payoff.

The exact verified 16 column inequalities are
[
  sum_ilambda_i a_{ij}le C_{16},
  qquad j=0,dots,15.
]
For every allowable (d),
[
 inf_m E_{mu_psi} T(m,P)
 lesum_ilambda_i C_{m_i}(d)
 =sum_j d_jsum_ilambda_i a_{ij}
 le C_{16}.
]
This proves the theorem. No dual LP or guessed numerical optimality
is used: the supplied rational mixture and inequalities suffice.

## Exact certificate and independent first-contact evaluation

- `packages/interval_global_closure/common_warp_lower_16.cert.json`:
  sixteen oriented legal Monster routes in **integer physical
  time/space coordinates**, probabilities with common denominator
  (10^{12}), and the exact rational ceiling.
- `packages/interval_global_closure/common_warp_lower_bigint.cjs`:
  separately implemented chronological *first* intersections of the
  338 physical Princess paths and every Monster route; exact folded
  characteristic ramp evaluation with BigInt. No limit value or
  solver success flag is trusted.
- `packages/interval_global_closure/verify_lower_warp16.cjs`:
  checks all 5,408 contacts, unit-speed legs, both endpoint visits,
  probability normalization, the archived attaining-response value,
  all sixteen column inequalities, the exact ceiling, and the exact
  difference from the old lower guarantee.

Run from the repository root:
```sh
node packages/interval_global_closure/verify_lower_warp16.cjs
```

An independent V8 replay of the mathematical checks **PASSED** with
5,408 first-contact calculations, including equality of the archived
Monster best response to (c_0). The Node CLI wrapper was created for
reproduction but **not separately executed in this continuation**.
No Lean compilation or CI was performed.

The floating joint-warp exploration and simplex files are retained as
discovery only. The final no-go proof needs only the exact routes and
integer arithmetic certificate.

## Why this matters and what remains

The previously tempting strategy of improving the archived lower law
by changing all clocks together is ineffective on the 16-knot family:
every improvement is bounded by less than seven parts in a billion.
That is a **whole-family exclusion**, not a single failed example.

The conclusion must not be extrapolated to arbitrary smooth or
infinitely refined warps. On the 32/64/128-knot grids, the initial
finite-Monster *masters* have more room; their improved master values
are not unrestricted lower guarantees. A subsequent 32-knot
unrestricted-response run timed out before giving a certificate and
is not promoted to a result.

The full proof still requires a Princess law (or approaching family)
whose response against *all* Monster paths matches an actual Monster
upper law. Changes to the Princess distribution's mass/transport
structure—not merely a 16-knot geometric clock—remain essential.
