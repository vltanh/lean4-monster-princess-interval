# Exact equilibrium check: scope and reproduction

**Not a solution of the unrestricted game.**

Run `python verify.py` using standard Python 3.

The verified statements are:

1. The minimax problem for the specified 32 monster paths, with unrestricted princess responses, has the exact primal-dual value recorded in `certificate.json`.
2. A different 68-path monster mixture has a strictly smaller unrestricted upper guarantee. Thus the entire original 32-path support is ruled out as globally optimal, not just one choice of its weights.
3. The particular approaching princess family extracted from the first dual is defeated by an explicit omitted monster path. This is verified symbolically for every epsilon in (0,1/64).

The exact value of the full game remains unproved. Read `PROOF.md` for the mathematical reduction and the limits of the assertions.

The `exploratory/` directory contains numerical discovery code and selected logs/checkpoints. It is not part of the exact certificate. Some response searches in those logs were truncated at a node cap; they must not be interpreted as certified lower bounds. Exact polynomial geometry in those searches does not make their floating-point LP weights or objectives exact.

No external optimizer or native compiler is needed for `verify.py`.
