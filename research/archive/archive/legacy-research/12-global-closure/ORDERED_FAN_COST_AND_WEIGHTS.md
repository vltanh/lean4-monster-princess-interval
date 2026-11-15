# Exact ordered fan costs and concave weight certificates

## Scope

Fix the physical base paths and nondegenerate translation intervals of a
finite fan basis. The law in this note is the common-quantile coupling of
the symmetric signed marginals. This differs from the raw mixture of
translated paths. The module scores a supplied complete unit-speed Monster
route and computes a global supergradient with respect to the component
weights. It is not an unrestricted Monster-response oracle, an equilibrium
certificate, or a new game bound.

All path coordinates and interval endpoints may use the existing exact
rational-function germ arithmetic. Probability weights are constant
nonnegative rationals and are normalized exactly. Their positivity does
not cause a path to be re-realized or its interval to be changed.

## 1. The signed field and running records

For component \(i\), let \(p_i(t)\) be its fixed base path and let the
translation interval be \([\ell_i,r_i]\), of width \(d_i>0\).
At interior arena positions its symmetric marginal is
\[
 f_i(t,x)=\frac12\left[
 \operatorname{clip}_{[0,1]}\frac{x-p_i(t)-\ell_i}{d_i}
 +\operatorname{clip}_{[0,1]}\frac{x+p_i(t)+r_i}{d_i}\right].
\]
Endpoint strict and closed traces retain the clipping atoms. Put
\(F_w=\sum_iw_i f_i\). The quantile paths are legal by the marginal
transport inequalities.

Along a Monster path, captured quantiles form one interval. With lower
strict record \(L_w\) and upper closed record \(H_w\), the survival
probability is exactly \(1-H_w+L_w\). Thus the expected capture time is
\[
 C_m(w)=\int_0^{T_m}[1-H_w(t)+L_w(t)]\,dt
\]
for a route that has captured every quantile by \(T_m\).
Closed endpoint visits must be evaluated from the actual physical
coordinates, including their germ order.

The upper record is a supremum of functions linear in the weights and
the lower record is an infimum of such functions. Consequently
\(C_m(w)\) is concave on the probability simplex. A raw physical mixture
has no larger payoff, but its row-wise matrix averages are not substituted
for this concave function.

## 2. Exact affine integration

On a unit rightward Monster leg, the marginal \(F_w(t,m(t))\) is
nondecreasing; on a unit leftward leg it is nonincreasing. Its complete
piecewise-affine partition consists of base-path vertices and crossings
of the unit Monster line with translated fan edges.

The code constructs those exact times, evaluates the marginal at all
endpoints, and integrates the positive-part correction to the old record.
The current route and all base paths remain fixed. The same construction
works when two ordinary limiting coordinates agree but their actual
germs differ.

The interval-fan module provides a second exact integration formula.
For each component, the integral of its CDF along a unit leg is obtained
from a difference of capped first-inverse band moments. This formula is
used for all basis components in the gradient, including zero-weight
components. It avoids treating a zero current weight as permanent
exclusion from a later mixture.

## 3. A global weight supergradient

Let one rightward leg run from time \(a\) to time \(b\). Its initial
records are \(L,H\), with active component vectors \(\mathbf L,\mathbf H\).
Let \(\tau\) be the first time the current marginal exceeds \(H\), or
\(b\) if it never does. A valid supergradient contribution is
\[
 (b-a)(\mathbf 1+\mathbf L)
 -(\tau-a)\mathbf H
 -\int_\tau^b\mathbf f(t,m(t))\,dt.
\]
For a leftward leg the corresponding expression is
\[
 (b-a)(\mathbf 1-\mathbf H)
 +(\tau-a)\mathbf L
 +\int_\tau^b\mathbf f(t,m(t))\,dt,
\]
where activation means the marginal falls below \(L\).

These follow by differentiating the active affine branch of the running
maximum or minimum. The moving activation boundary contributes zero
because the two branches agree there. At a tie, either active record
branch is a valid choice; the implementation consistently retains the
older branch until a strict crossing.

Summing the leg contributions gives a vector \(g\) satisfying, for every
other nonnegative normalized weight vector \(v\),
\[
 C_m(v)\le g\cdot v,\qquad g\cdot w=C_m(w).
\]
The equality is the homogeneous Euler identity and is checked exactly.
The inequality is global by concavity, not merely a first-order
approximation for small perturbations.

These planes can support a finite-basis concave cutting-plane search.
They are upper planes for that finite-basis optimization, not upper
strategies against every Princess path. A full-game proof still requires
both unrestricted opposing inequalities.

## 4. Interface and reproduction

The CJS module exports:

    createOrderedFanTools(G, intervalFanModule)

The returned tools provide:

    basis = tools.prepareBasis([{path, lower, upper, id}, ...])
    law = tools.law(basis, exactWeights)
    result = law.score(monsterRoute, {gradient: true})

A complete result contains the exact cost, limiting cost, zero survivor
mass, and exact supergradient vector. By default incomplete routes and
nonunit legs are rejected. The optional incomplete-route mode returns
only a truncated cost and is not a completion certificate.

Run the independent replay:

    node packages/interval_global_closure/verify_ordered_fan_cost.mjs /tmp/ordered_fan_checks.json

The recorded exact V8 replay passes:

- 63 equalities for physical families already ordered throughout time.
- 7 static-mixture equalities against the separate physical fan scorer.
- 21 raw/ordered dominance checks, including 16 strict improvements.
- 84 global supergradient inequalities under distinct rational reweightings.
- 270 CDF-area identities checked against the separate inverse-band primitive.
- 1,007 affine trace pieces in the mixed-law tests.

The common germ radius is \(19683/17641625584\), with maximum degree ten.
The replay uses ordinary, clipped-endpoint, avoided-center and nested
germ cases, with fixed, asymmetric, outward and germ-width intervals.

The numerical native cutting-plane controller was not written before
the development environment failed. This exact scorer and verifier were
completed separately in V8; no result of that interrupted optimization
is asserted.
