# Tight all-resolution common-warp ceiling for the archived Princess law

Date: 2026-11-12. **Certified, scoped result:** this concerns the common-coordinate-warp **orbit of one archived Princess law**, not the exact value of the unrestricted Princess–Monster game.

## Theorem

Let \(\mu_0\) denote the archived symmetric 338-path Princess law in
`packages/interval_uniform_reduction/princess_strategy.json`.
Let \(\mathcal W\) consist of every strictly increasing continuous
\(\psi:\mathbb R\to\mathbb R\) satisfying
\[
\psi(-u)=-\psi(u),\qquad \psi(u+2)=\psi(u)+2.
\]
Apply the same map in both light coordinates \(U=t+x,V=t-x\) to all Princess paths, and denote the resulting legal law by \(\mu_\psi\).
Without any fixed-knot or bounded-derivative hypothesis on \(\psi\),
\[
\boxed{
\frac{36290299773897097}{25600000000000000}
\ \le\
\sup_{\psi\in\mathcal W}\inf_{m\ {\rm legal}}\mathbb E_{\mu_\psi}T(m,P)
\ \le\
\frac{567055553277100451603891}{400000000000000000000000}.
}
\]
The upper endpoint is exactly \(1.4176388831927511290097275\).
The remaining interval width is
\[
\boxed{
\frac{19619309958310978891}{400000000000000000000000}
=0.000049048274895777455.
}
\]
The identity warp supplies the lower inequality from the archived exact unrestricted Monster response to \(\mu_0\).

The previous all-warp ceiling was
\(570109078983139212403/400000000000000000000=1.425272697457848\ldots\).
The new ceiling reduces it by the **exact positive amount**
\[
\frac{3053525706038760799109}{400000000000000000000000}
=0.007633814265096902\ldots.
\]
This narrows the interval for the **restricted warp orbit** by approximately **99.36%**. It does not narrow the full-game interval.

## 1. Concrete physical Monster mixture

The candidate bank consists of 16 archived unit-speed Monster routes, followed by a full endpoint sweep from -1 to +1 to -1, followed by 33 right-first endpoint sweeps beginning at \(x=k/64\) for \(32\le k\le64\). For \(k<64\), the new sweep vertices are
\[
(0,k/64),\qquad (1-k/64,1),\qquad (3-k/64,-1).
\]
For \(k=64\), start at +1 and travel directly to -1. All routes are physically legal, complete both endpoints, and are specified by integers at scale \(S=256000000\).

The frozen certificate `packages/interval_global_closure/common_warp_lower_all_tight.cert.json` gives nonnegative rational Monster route weights with common denominator \(\Lambda=10^{15}\). Of the 50 routes, **35 have positive weight**. No numerical LP optimality assertion is needed for validity; the rational weights alone provide the upper bound.

## 2. Continuum step envelope

For the first meeting of original Monster route \(i\) and original Princess path \(p\), record its integer light coordinates \((U_{ip},V_{ip})\).
Every integer \(z\) admits a unique representation
\[
z=2k_zS+r_z,\qquad -S\le r_z<S,\qquad
\rho_z=|r_z|/S,\quad\sigma_z=\operatorname{sgn}(r_z).
\]
Oddness and the period-two increment imply
\(\psi(z/S)=2k_z+\sigma_z\psi(\rho_z)\).

Write \(g=\psi|_{[0,1]}\). Its Stieltjes probability measure \(dg\) is nonatomic because \(g\) is continuous, and
\[
g(\rho)=\int_0^1{\bf1}_{s<\rho}\,dg(s).
\]
The light-coordinate transformation preserves each path's legality and chronological first contacts: both light coordinates remain nondecreasing, the arena condition is preserved by \(|\psi(U)-\psi(V)|\le2\), and strict monotonicity preserves the ordering of times. Thus an original first contact with coordinates \((U,V)\) transforms to a first contact at time
\([\psi(U/S)+\psi(V/S)]/2\).

Let \(b_i\) be the Monster weight numerators, and \(w_p\) the 338 original signed Princess integer weights (total \(W=2\cdot10^8\)).
The mixture's transformed payoff equals \(\int_0^1 A(s)\,dg(s)\), where
\[
A(s)=\frac{1}{2W\Lambda}
\sum_{i,p}b_iw_p
\sum_{z\in\{U_{ip},V_{ip}\}}
\left(2k_z+\sigma_z{\bf1}_{s<\rho_z}\right).
\]
Therefore every allowed warp's payoff is at most \(\sup_s A(s)\).
This calculation is **exact** and does not approximate a warp on a prescribed grid.

There are **11,830 first meetings** across the 35 positive Monster routes and 338 Princess paths. Their folded light coordinates give precisely **84 nontrivial step thresholds** in \((0,1)\). Sweep the 85 open step intervals by integer addition:
\[
B_0=\sum_{i,p,z}b_iw_p(2k_z+\sigma_z),\quad
\Delta(r)=-\sum_{i,p,z:\rho_z=r}b_iw_p\sigma_z.
\]
The maximum cumulative numerator divided by \(2W\Lambda\) is
\[
\boxed{
\max A(s)=\frac{567055553277100451603891}
{400000000000000000000000}.
}
\]
One maximizing cell begins just right of \(s=31/32\).
The maximum is the supremum payoff of **this fixed Monster mixture** over allowed warps, because a strictly positive smooth warp derivative can concentrate arbitrarily near the maximizing open cell. It is not claimed to be the best Monster mixture.

For each warp, the displayed legal transformed Monster mixture bounds the warp's best-response payoff from above. The identity warp gives the lower inequality. This proves the theorem.

## 3. Independent integer verification

Run from the repository root:

```sh
node packages/interval_global_closure/verify_lower_warp_all_tight.cjs
```

The verifier checks source Git blob hashes; all archived Princess weights, speed/arena constraints and all Monster routes; the normalized rational Monster mixture; and **all 11,830 chronological first-contact coordinates using two independently implemented methods** (piecewise-linear chronological intersections versus characteristic generalized inverses).

It independently computes the exact 84-threshold step sweep and compares it with the previously written envelope engine. It also checks **80 exact ramp-integral identities** across all 16 original bins and all 64 finer bins, together with the exact new-minus-old ceiling and exact gap to the archived lower guarantee.

**All these checks PASSED in V8** on the pinned committed data. This continuation does not claim a separate native Node run, Lean compilation or CI. The floating LP is only a discovery tool; the proof is the fixed rational mixture and reproducible integer certificate.

## 4. Scope and remaining gap

This nearly closes the **entire warp orbit** of the archived law: the upper and lower restrictions differ by \(4.9048274896\times10^{-5}\), even for smooth or singular-continuous increasing common-coordinate warps.

The result does not cover changing the Princess law's marginal masses or transport structure, nor arbitrary mixtures of different warped laws. It is **not** a new unrestricted-game upper bound. The unrestricted value remains between the previously certified
\(1.417589834917855\ldots\) and \(1.426129744306782\ldots\).
G5–G8 are still open. An exact orbit value would need a further matching argument; an exact full-game value would additionally need strategies valid against **all** opposing legal paths.
