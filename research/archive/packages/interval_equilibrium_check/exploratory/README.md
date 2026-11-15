# Exploratory code: not proof certificates

Dependencies: NumPy, SciPy, Numba, a C++17 compiler, and Boost headers.

Build the discovery helpers:

```sh
g++ -O3 -std=c++17 poly_monster_memo.cpp -o poly_monster
g++ -O3 -std=c++17 poly_matrix.cpp -o poly_matrix
g++ -O3 -std=c++17 ordered_monster.cpp -o ordered_monster
python run_play.py
```

The driver uses explicit iteration and node caps. Its checkpoint/log values are numerical research data, not a certificate of the full game's value. A completed capture-order search still uses floating-point objective comparisons in this driver. Only the parent directory's `verify.py` supplies the exact certificates stated in PROOF.md.

The run included here was stopped without matching global guarantees. The saved checkpoint contains completed iterations; the log may additionally show the start of an interrupted iteration.
