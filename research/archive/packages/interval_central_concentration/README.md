# Exact central-concentration exclusion

Run with Python's standard library:

```sh
python packages/interval_central_concentration/verify.py
```

The verifier constructs 124 rational admissible princess paths from
`candidate.json`, checks the relevant initial and time-one marginals, and
certifies an unrestricted monster response bound of
`1554318825101/1279999999616 < 1.215`.

The result also holds after ordered quantile rearrangement because the proof
uses only those two time marginals. A simpler bound is `4103/3200 = 1.2821875`.
Both are below the previously established exact full-game lower bound, so the
specified candidate cannot be an equilibrium lower strategy. The verifier does
not assert that this response is optimal or that the game has been solved.

The complete proof and scope are in
`research/08-continuum/CENTRAL_CONCENTRATION.md`. The input weights are integer
reconstructions of exploratory numerical weights, normalized by their exact
sum; no floating-point values or solver tolerances enter the certificate.
