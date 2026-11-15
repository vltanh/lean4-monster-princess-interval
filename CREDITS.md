# Credits

How this formalization was made, from the run log and the session transcripts.

## Who

- Author and maintainer: The-Anh Vu-Le, who asked for the formalization of the paper and chose
  this repository for it.
- Formalization: Claude Opus 5.5 (`claude-opus-5-5`, Anthropic), as Claude Code 2.1.325 in VS Code.
  One coordinating session and its sub-agents wrote all the Lean code and the documents.
- Procedure: the `formalize-math-paper` skill
  ([repository](https://github.com/vltanh/formalize-math-paper)), in a local copy that differs
  from the repository's commit `e339f64` of 2026-10-17: inventory, statements first
  with an independent statement review, proofs by the paper's arguments, the axiom audit and the
  route check, cleanup, the audit report.
- Review: independent AI agents checked the statements against the paper before any proof was
  written, and the report's findings against the paper and by recomputation. No person has
  reviewed the proofs.

## First formalization (14 November 2026)

How it was made:

- **Coordinating session.** It read the paper and its 2006 preprint, and checked the paper's
  numerical claims in Python:
  - the matrix (4) and all 8! greedy searcher responses;
  - the linear program of Theorem 15;
  - the formulas (11), (12) and (15) against simulations;
  - a lower-bound scheme for Theorem 16.

  It set up the project, stated every result, and proved the shared infrastructure (the triangle
  wave, capture times, the concrete strategies). It wrote repaired proof plans for the results
  whose proofs in the paper are informal (Theorems 10, 14, 16 and Propositions 1, 3, 5, 7).
- **Statement review.** An independent agent compared every statement with the paper. It found
  that formula (9), as first stated, failed at `y = 1`, and that a hypothesis of formula (15)
  excluded the uniform case; both were corrected before the baseline commit.
- **Proving agents.** Eight agents worked in parallel, each owning disjoint files:
  - Propositions 1–3, 7, 8;
  - Proposition 5;
  - the Alpern–Gal minimax theorem, the existence of the value and Proposition 4;
  - Theorem 9;
  - the matrix (4) and Theorem 10;
  - Lemmas 11–13 and formulas (9), (10);
  - Theorems 14 and 15 with formulas (11), (12);
  - Theorem 16 with formula (15).

  The minimax agent found that the cited theorem, as first stated, needed a nonempty space.
- **Integration and checks.** The coordinating session committed each agent's work after checking
  its statements against the baseline. It then ran the axiom audit, the route check and
  Comparator, and removed unused hypotheses in three rounds.
- **The report.** The coordinating session wrote [`REPORT.md`](REPORT.md). An independent agent
  checked its findings against the paper, by recomputation, and against the literature; it found
  the two later theses and several overstated claims, which were corrected.
- **Proof review.** Another independent agent compared every formal proof with the paper's. It
  found one departure that was not necessary (Theorem 10's start at an end) and two inaccurate
  descriptions (Propositions 3 and 7). The two agents that wrote those proofs were resumed: one
  added [`proposition1_start_one`](PrincessMonster/Section2/Dominance.lean#L268), the other made Theorem 10 use it, and the descriptions were
  corrected.
- **Follow-up papers.** A further agent explored follow-up papers, which are kept private.

Figures, from 2026-11-14 16:00 CST (UTC−06:00) to the commit that completes [`REPORT.md`](REPORT.md)
(18:57 CST), from the Claude Code transcripts:

- elapsed time: 2.9 hours;
- sub-agents: 12, at most 8 running at once, 4.7 hours of agent time in total, 2 resumptions;
- tool calls: 702 by the sub-agents and 232 by the main session;
- tokens, sub-agents: 1.65M output, 3.62M input, 121M cache reads;
- tokens, main session: 0.52M output, 0.79M input, 124M cache reads;
- model calls: 884, all to `claude-opus-5-5` (225 by the main session, 659 by the sub-agents).

The figures count the coordinating session and its sub-agents up to that commit. The
exploration of follow-up papers, still running then, is counted only up to that time, and the
packaging that followed is not counted. The formalization started from an empty repository.
