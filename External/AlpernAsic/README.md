# Alpern–Asic, Theorem 3

**Source.** S. Alpern and M. Asic, *The search value of a network*, Networks 15 (1985),
229–238, Theorem 3: optimal strategies invariant under the isometry group of the network exist.

**Statement here.** The special case used in the paper's Proposition 4, the group `{id, φ}` of
the interval, in game-theoretic terms: `theorem3_minimizer` and `theorem3_maximizer` say that
averaging a mixed strategy with its reflection does not worsen its guarantee, when the payoff is
invariant under the reflection of both players' strategies.

**Use in the paper.** Proposition 4: "The proof is just a special case of Theorem 3 of Alpern
and Asic". The paper's library applies these with `φ(x) = -x` acting on paths, for which the
capture time is invariant (`captureTime_neg`).
