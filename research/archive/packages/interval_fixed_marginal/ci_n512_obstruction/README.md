# Exact n512 obstruction discovered in CI

[Run 43546004339](https://github.com/vltanh/lean4-monster-princess/actions/runs/43546004339),
artifact `14094262180`, stopped the `n512-level08` fixed-marginal experiment
after four completed iterations because its exact all-calendar family floor
already exceeded the retained global upper. The job completed successfully;
it did not establish a new game bound or an equilibrium.

The retained rational field proves

\[
\inf_{\text{all n512 causal calendars for this fixed law}}
\sup_{g\in Q_{\rm out}} R(g)
\ \ge\ \frac{145931157143161}{102400000000000}
\ >\ \frac{291849329389899}{204800000000000}.
\]

Every one of the 676 physical probabilities remains exactly the probability
in `../seed_plain_n128.sparse.json.gz`. The paths are represented on a grid
four times finer. Retention checked every full path and probability against
that committed seed before replacing the 6.88 MB move arrays with 60,999
bytes of exact run-length data.

The actual continuous full-width field response against this physical law
is exactly

\[
\frac{5836196016558091}{4096000000000000}.
\]

This remains below the retained global upper. Thus the certificate-family
obstruction must not be promoted to an obstruction for the actual continuous
physical law. Neither number is a game lower bound.

Replay from the repository root:

```sh
python packages/interval_fixed_marginal/ci_n512_obstruction/verify.py
```

This first checks the file hashes and the identity of all 676 refined physical
paths and probabilities with the committed seed, then calls
`verify_obstruction.py --result-directory` and compares its fresh result with
the retained independent replay.

The standard-library verifier checks every nodal order constraint, every
physical path, the minimum over all causal calendars by prefix minima, and
the actual continuous affine running-minimum integrals. Endpoint capture
and endpoint traces are kept distinct. No LP or native maximum-flow output
is trusted in this replay. The theoretical interpolation and clock arguments
remain manuscript proofs, not Lean formalizations.

`blocking.field.json.gz` is byte-exact CI output. `blocking.report.json`
binds its original report, the original and compacted marginal hashes, source
head and seed, artifact ZIP hash, and the seed-refinement identity. The
independent replay and a file-hash manifest are retained alongside it.
