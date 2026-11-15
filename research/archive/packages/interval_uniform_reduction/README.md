# Interval Princess–Monster research result

**Not a solution of the exact unrestricted value.**

`PROOF.md` proves a uniform, explicit finite-game approximation theorem for the full game. It also records the scope of the exact computational certificates and the remaining missing saddle-point argument.

Run with Python's standard library:

```sh
python verify.py
python tests.py
```

The checks establish:

1. The exact unrestricted monster response to the supplied 338-path princess distribution.
2. A rational saddle certificate for all paths in a specified small finite grid game.
3. An explicit exact counterexample to the rationalized dual monster candidate.
4. Regression agreement with unpruned exact searches and with direct capture-time integration.

The continuous mathematical arguments are written proofs, not machine formalizations. The discovery logs in `research/` are not exact certificates. They did not produce matching unrestricted guarantees.

Optional independent C++ cross-check:

```sh
g++ -O2 -std=c++17 exact_ordered.cpp -o exact_ordered
python verify_cpp.py
```

This uses Boost multiprecision headers and checks both cached and naive exact searches. The continuous proof remains a written mathematical argument; these runs are not a formal verification of that argument.
