# Rationally warped ordered-CDF upper certificate

Exact unrestricted upper certificate, 2026-11-13.

The complete rational Monster law and independently replayed integer flow give

\[
 V\le U_{\mathrm{warp}}
 =\frac{3737990218889184863163116789182923230981219}
        {2621440000000000000000000000000000000000000}
 =1.425930106692957\ldots.
\]

Together with the retained unrestricted Princess certificate this gives

\[
\frac{36290299773897097}{25600000000000000}
\le V\le U_{\mathrm{warp}}.
\]

The two bounds differ. This certificate does not identify an equilibrium or
improve the Princess lower bound.

## Complete physical law

`packages/interval_global_closure/warped_order_upper_exact.json` contains all
248 reflected path pairs and their positive integer weight numerators over
`1000000000000`. Each pair is given a fair spatial reflection. Every physical
vertex is supplied in exact light coordinates \((u,v)=(t+x,t-x)\).

The paths have 772 unit-speed legs. The latest first visit to either endpoint
is at

\[
\frac{406249920330000007967}{100000000000000000000}<\frac{65}{16}.
\]

The law was found by optimizing a common odd, strictly increasing,
translation-compatible piecewise affine map of both light coordinates of the
[recovered adaptive law](ADAPTIVE_ORDER_UPPER_CERTIFICATE.md). Its 60 rational
increments, source knots, and a small identity mixture are retained as
provenance. The identity mixture has weight `1/10000000000`; it makes every
increment strictly positive after rounding. The verification uses the final
exact physical paths directly, so the validity of the upper bound does not
depend on convergence of the numerical warp search.

The numerical discovery score was about `1.4259301066870502`. The exact
rounded law has the slightly larger fraction stated above. Only that exact
fraction is claimed as an upper bound.

## Exact unrestricted Princess response

Run from the repository root:

```sh
node --stack-size=16384 packages/interval_global_closure/verify_warped_order_upper.cjs
```

The verifier first checks exact mixture normalization, legal unit-speed
physical paths, both endpoint visits, and the endpoint baseline. It then
reconstructs the full ordered Princess-response graph, solves its integer
maximum-flow problem, and replays the generated flow against a separately
rebuilt graph. Both extremal response labelings attain the claimed value.
The complete certificate is reproducible from the compact law without a
floating-point optimizer or the numerical search checkpoint.

The replay has 86,503 nodes, 218,944 arcs, and 94,962 positive-flow entries.
The exact endpoint baseline is

\[
\frac{373796917674812164967589428574913100905809}
     {262144000000000000000000000000000000000000},
\]

and the matching deficiency is

\[
\frac{21042141063213487222503433792221923129}
     {2621440000000000000000000000000000000000000}.
\]

Their sum is \(U_{\mathrm{warp}}\). The unrestricted scope of the fixed-law
response theorem is explained in
[the full-order certificate](FULL_ORDER_CDF_UPPER_CERTIFICATE.md).

## Relation to the interrupted checkpoint

An earlier scratch-only warped law near `1.4259323177214351` was lost in the
compute outage. The present law was regenerated from surviving adaptive
weights, optimized afresh, rationalized, and checked again. It is a different,
stronger law with a complete portable input and replay. The lost checkpoint
is not used as evidence for this result.
