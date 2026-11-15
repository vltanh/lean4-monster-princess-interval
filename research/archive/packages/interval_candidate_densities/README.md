# Conditional density algebra

Run from the repository root:

```bash
python packages/interval_candidate_densities/verify.py
```

The verifier uses only Python's standard library and exact `Fraction`
arithmetic. It constructs the integrated capture-time functional for several
polynomial densities, differentiates it with rational dual numbers, and
checks the analytic formulas in
`research/08-continuum/CANDIDATE_DENSITIES.md`. It covers positive and
negative transition parameters and the additional inward-leg parameter.

It also checks the conditional differential equation, its homogeneous
factor's logarithmic derivative, and the exact counterexample to restricting
negative-transition detours to two endpoint choices.

These are algebra checks for a proposed M1/M2 family. They do not prove
global response optimality, construct an unrestricted princess guarantee,
or improve either certified bound for the game value.
