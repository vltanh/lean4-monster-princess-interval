# The princess and monster game on an interval — a Lean formalization

A searcher (the monster) and a hider (the princess) move in the interval `[-1, 1]` without seeing
each other. The searcher has speed at most `1`; the hider may move as she likes. The searcher pays
the hider the time until they meet. S. Alpern, R. Fokkink, R. Lindelauf and G.-J. Olsder,
[*The "Princess and Monster" game on an interval*](https://doi.org/10.1137/060672054), SIAM J.
Control Optim. 47(3) (2008), 1178–1190, showed that this game, long thought trivial with value
`3/2`, is not: its value `V` satisfies `15/11 ≤ V ≤ 13/9`.

This repository formalizes the whole paper in Lean 4 with Mathlib. That covers every numbered
result, the existence of the value, and the main bounds. It also proves the two results the paper
cites, the minimax theorem of Alpern and Gal and Alpern and Asic's invariance theorem, so nothing
is assumed. The paper's informal arguments in Sections 3–5 are completed into proofs.

## Status

| Part of the paper | Status |
| --- | --- |
| Section 1: the game has a value | proved (`value_exists`), from the minimax theorem of Alpern and Gal, proved in [`External/`](External) |
| Section 2: Propositions 1–8, Definition 6 | proved; Proposition 3 for every continuous hider path |
| Section 3: Theorem 9, matrix (4), Theorem 10 | proved |
| Section 4: Lemmas 11–13, formulas (9)–(12), Theorems 14, 15 | proved; Lemma 11 and formulas (9), (11) in corrected form |
| Section 5: formula (15), Theorem 16 | proved; formula (15) in corrected form |
| Section 6: `15/11 ≤ V ≤ 13/9` | proved (`main`, and the Challenge) |

## Main results

| Paper | Lean | Statement |
| --- | --- | --- |
| Section 1 | `value_exists` ★ | the game has a value: lower and upper values coincide; the searcher has an optimal mixed strategy |
| Theorem 9 | [`theorem9`](PrincessMonster/Section3/Theorem9.lean#L221) | `V ≤ 47/32` (sweepers with probability `7/16` each, strategy `±B` with `1/16` each) |
| Theorem 10 | [`theorem10`](PrincessMonster/Section3/Theorem10.lean#L794) | `V ≥ 97/75`, the value of the matrix game (4) |
| Theorem 14 | [`theorem14`](PrincessMonster/Section4/Theorem14.lean#L347) | `V ≤ 13/9`: sweepers with probability `7/9`, uniformly started runners with `2/9` |
| Theorem 15 | [`theorem15`](PrincessMonster/Section4/Theorem15.lean#L419) | against sweepers mixed with runners started by any atomless `Φ`, the hider gets more than `1.421` |
| Theorem 16 | [`theorem16`](PrincessMonster/Section5/Theorem16.lean#L2139) | `V ≥ 15/11`: ends with probability `3/11`, uniformly started loiterers with `8/11` |
| Main result | `main` ★ | `15/11 ≤ V ≤ 13/9` |

★ The Challenge ([`Challenge.lean`](Challenge.lean)) restates these two theorems in Mathlib's vocabulary. The game
is set up as in the paper:

- hider strategies: continuous paths `[0, ∞) → [-1, 1]`;
- searcher strategies: paths with `|S t - S t'| ≤ |t - t'|`;
- payoff: the first meeting time, `∞` if they never meet;
- mixed strategies: Borel probability measures for the topology of uniform convergence on
  compact sets.

## What the audit found

[`REPORT.md`](REPORT.md) lists 18 findings. None changes the main result. The most important:

| | Finding |
| --- | --- |
| E1 | The capture time is lower semicontinuous, not upper as stated; the minimax theorem needs exactly that. |
| E11 | Lemma 11 is false at one starting point, and its proof applies Proposition 8 to a single path; it holds for every path of speed at most `1` once that point is excluded. |
| E13 | Formula (9) fails when the hider meets both sweepers at once (`y = 1`). |
| E14, E17 | Formulas (11) and (15) are misprinted; Figure 3 does not match the strategy it plots. |
| E5 | Proposition 3's inductive construction can stall; the same path has a closed formula and works for every continuous hider path. |
| E10, E16 | The reductions of all searcher responses to a few explicit paths in Theorems 10 and 16 are informal (Theorem 16 applies Proposition 5 to a continuous mixture). Both are completed by lower bounds valid for every searcher path. |

The proofs follow the paper's arguments. Where a step is wrong or missing, the proof departs from
the paper at that step only. Every departure is listed, with its reason, in
[the report's Section 7](REPORT.md#7-departures-from-the-papers-proofs).

## Trust

- `lake build` prints no warning besides the two intended `sorry`s of [`Challenge.lean`](Challenge.lean). There is
  no `axiom`, `admit` or `native_decide`.
- [`scripts/Audit.lean`](scripts/Audit.lean) checks that every declaration of the library uses
  only [`propext`](https://leanprover-community.github.io/mathlib4_docs/Init/Core.html#propext), [`Classical.choice`](https://leanprover-community.github.io/mathlib4_docs/Init/Prelude.html#Classical.choice) and [`Quot.sound`](https://leanprover-community.github.io/mathlib4_docs/Init/Prelude.html#Quot.sound), and lists what each result depends on.
- The route check ([`scripts/route_check.py`](scripts/route_check.py)) checks that each proof uses the results that the
  paper's proof cites. It passes, with every difference recorded in
  [`docs/route_differences.tsv`](docs/route_differences.tsv).
- Comparator accepts [`Solution.lean`](Solution.lean) against [`Challenge.lean`](Challenge.lean), under the Lean kernel and nanoda.
- The statements, the proofs and the report were checked by independent AI agents against the
  paper. No person has reviewed the proofs yet.

## Building

```sh
lake exe cache get   # Mathlib's compiled files
lake build           # Lean v4.36.0-rc2, Mathlib v4.36.0-rc2
lake env lean scripts/Audit.lean
lake env lake comparator --config=comparator.json   # needs bubblewrap
```

The only dependency is Mathlib.

## Layout

| Path | Contents |
| --- | --- |
| [`PrincessMonster/`](PrincessMonster) | the paper: definitions (`Defs.lean`), capture times, the value, and one directory per section |
| [`External/`](External) | the cited results: Alpern–Gal's minimax theorem, Alpern–Asic's Theorem 3 |
| [`Basic/`](Basic) | general mathematics: the triangle wave that folds a motion onto `[-1, 1]` |
| [`Challenge.lean`](Challenge.lean), [`Solution.lean`](Solution.lean), [`comparator.json`](comparator.json) | the statements of record and their proofs, for [Palomar](https://palomar-registry.org) |
| [`docs/`](docs) | the routes of the paper's proofs and the recorded differences |
| [`scripts/`](scripts) | the audit, the route check, and documentation checks |

## Related work and credits

- No other formalization of this paper or of a search game was found. Since the paper, a
  numerical study by the same authors (2009) and two bachelor's theses (Geupel 2011, van Laere
  2018) have revisited the game, without improving the bounds; the theses already correct some
  of the slips listed in the report (E1, E14, E15, E17). See
  [the report's Section 10](REPORT.md#10-the-paper-in-the-literature).
- Author and maintainer: The-Anh Vu-Le.
- The Lean code, the audit and the documents were written by Claude (Anthropic) agents, using the
  `formalize-math-paper` procedure at the maintainer's request; see [`CREDITS.md`](CREDITS.md).
- License: [Apache-2.0](LICENSE).
