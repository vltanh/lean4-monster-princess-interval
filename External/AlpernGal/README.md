# Alpern–Gal minimax theorem

**Source.** S. Alpern and S. Gal, *A mixed strategy minimax theorem without compactness*,
SIAM J. Control Optim. 26 (1988), 1357–1361; used through Appendix A of S. Alpern and S. Gal,
*The Theory of Search Games and Rendezvous* (Kluwer, 2003), or S. Gal, *Search Games* (1980).

**Statement.** `External.AlpernGal.minimax`: for a nonempty compact Hausdorff minimizer space `X`, any
maximizer set `Y` and a payoff `X → Y → [0, ∞]` that is lower semicontinuous in the minimizer's
strategy, the upper value in mixed strategies is attained and equals the lower value over
finitely supported maximizer strategies.

**Use in the paper.** Section 1: "the payoff function T is upper semicontinuous and the searcher
mixed strategy space is compact Hausdorff. Consequently the minimax theorem of Alpern and Gal can
be used ... to establish the existence of the value V(Q), an optimal mixed searcher strategy, and
an ε-optimal hider mixed strategy." The capture time is in fact *lower* semicontinuous, which is
the hypothesis the theorem needs (see `REPORT.md`).

**Proof.** Proved here, for every nonempty compact Hausdorff `X` (no metrizability), from
Mathlib's Sion minimax theorem (`Mathlib/Topology/Sion.lean`) applied to finitely many maximizer
strategies and truncated payoffs, Prokhorov compactness of `ProbabilityMeasure X`, and the
Riesz–Markov–Kakutani regularization of measures (`Measure.exists_regular_eq_of_compactSpace`) to
pass to the limit. Nonemptiness is needed: there is no probability measure on the empty space.
