# Recovered adaptive ordered-CDF upper certificate

Exact unrestricted upper certificate, 2026-11-13.

The recovered adaptive Monster law gives

\[
 V\le U_{\mathrm{adaptive}}
 =\frac{186901335715700435697848697352853}
        {131072000000000000000000000000000}
 =1.425944028592685\ldots.
\]

This improves the previously published upper
`1140799301969009059644426513/800000000000000000000000000`.
The retained global Princess lower certificate is unchanged.
No equilibrium or new Princess lower bound is asserted.

## Complete portable input

The law in
`packages/interval_global_closure/adaptive_order_upper_exact.json`
contains 248 rational reflected path pairs, each used with a fair spatial
reflection. Its mixture denominator is `1000000000000`. All physical
vertices are supplied in exact light coordinates. The paths contain 772
unit-speed legs, and both endpoints are visited by time `65/16`.

The original floating discovery had two tiny negative weights. They were
replaced by zero; the positive weights were normalized and rounded by largest
remainders. This produces a new explicitly specified rational law. The proof
uses the stored rational law, not a claim that floating weights are exact.

## Exact unrestricted response

Run from the repository root:

```sh
node --stack-size=16384 packages/interval_global_closure/verify_adaptive_order_upper.cjs
```

The verifier checks every physical leg, both endpoint visits, exact mixture
normalization, endpoint baseline and matching deficiency. It then reconstructs
the full ordered Princess-response problem with the committed rational physical
engine, solves its integer maximum-flow problem, and independently replays the
flow against a rebuilt graph. The engine is the same Git blob used for the
previous independently verified upper certificate.

The replay passed with 86,503 nodes, 218,944 arcs and 94,572 positive-flow
entries. Both extremal response labelings attain the stated fraction.
The exact endpoint baseline is

\[
\frac{37380205684133864080006773865809}
     {26214400000000000000000000000000},
\]

and the remaining deficiency is

\[
\frac{293059378733918967083}{125000000000000000000000000}.
\]

The saved compact law and verifier are sufficient to reproduce the result;
no floating LP, external checkpoint, or separately stored flow file is needed.
The [earlier full-order certificate](FULL_ORDER_CDF_UPPER_CERTIFICATE.md)
describes the fixed-law exact response construction and its unrestricted scope.

## Recovery status

The compute environment initially lost the later adaptive certificate during an
outage. An older snapshot retained its discovery bank and weights. The complete
rational certificate above was regenerated from those surviving files and
checked again after recovery. Its weights differ slightly from the earlier
unpublished checkpoint, so its exact fraction is stated independently here.

The older warped checkpoint near `1.4259323177214351` was not recovered.
A new, stronger common warp was subsequently regenerated and verified exactly;
its complete independent result is in
[WARPED_ORDER_UPPER_CERTIFICATE.md](WARPED_ORDER_UPPER_CERTIFICATE.md).
