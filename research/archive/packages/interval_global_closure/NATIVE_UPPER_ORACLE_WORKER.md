# Native upper-response worker for the frozen physical exchange

This worker solves the unrestricted atomic Princess response to the positive
support of a supplied finite paired Monster law, then produces NEW physical
Princess germ paths. Every output path is scored exactly against every input
Monster atom. Existing master rows are never re-lifted or re-realized.

## Callable API and CLI

The repository module is packages/interval_global_closure/upper_oracle_worker.mjs.
All default dependencies are repository-relative. A dependencies object can
override atomic, germAtomic, germ, realizer, frozen, exact, and collapsed.

    import {createUpperWorker,solveUpper} from "./upper_oracle_worker.mjs";
    const worker = await createUpperWorker(dependencies);
    const output = await worker({atoms,weights,options});

The CLI accepts an input JSON and an output filename:

    node upper_oracle_worker.mjs input.json output.json

An input may contain atoms and weights directly, or bank_file and weights_file.
File paths are relative to the input JSON. A bank file may be an atom array or
an object with atoms. A weights file may be an array or contain monster_weights
or weights. Persistent JSON-lines service is available with --jsonl.

The isolated native wrapper remains at
/workspace/scratch/f5595f62cf06/upper_oracle_worker_20261112/upper_oracle_worker.mjs.
It re-exports the same API and CLI from the portable package-layout module.

## Input and normalization

Supported Monster forms include exact_light, physical route/exact_path,
ordinary light, flat light-coordinate PATH parameters, M1/M2/M3/I/I1/E parameter
families, and the old numeric kind1/kind2 plus start format. Exact rational-germ
strings are accepted in coordinates. The law uses the symmetric paired
convention. Every Monster must have legal unit legs and complete an endpoint
tour.

Probabilities are nonnegative numeric or exact constant values. The worker
interprets their supplied decimal strings exactly, then divides by their exact
sum. An input whose numerical sum differs from1 by more than1e-8 is rejected
unless allowRenormalization is set. The exact normalization is recorded.
No strictly positive weight is clipped, however small.

Only active atoms determine the upper event universe and subordinate scale.
Inactive atoms are nevertheless included in EVERY returned physical payoff
row. Inserting a zero-weight atom does not move a previously generated
physical candidate.

## Main options

- exactCut:true: run the exact integer limiting-germ cut. The default is a
  numerical limiting cut for discovery.
- exactCollapsed:true: certify the separate ordinary companion by integer
  flow. The default companion response is numerical.
- companionRows:true: also generate physical responses to the collapsed
  ordinary companion, but score them on the ORIGINAL entire Monster bank.
- collapsed:false: omit the companion calculation unless companionRows is true.
- includeCaptureGerms:false: omit the full per-atom rational-function costs;
  exact rational limits and numeric payoff rows are still returned.
- profiles: explicit profile/fill/strictMode choices. Defaults are min/max
  cut profiles with avoided and common-wave clipped connectors. Identical
  physical functions are deduplicated by their exact vertex representation.
- tolerance: numerical cut tolerance, default2e-13.
- progress:true: write stage summaries to stderr.

An optional early fill is legal but can lose payoff on unpriced survival
intervals even when it retains the same query traces. Its maximizing status
is therefore reported explicitly; it is not silently advertised as an
optimal response. The default avoided/common-wave candidates must pass
the own-cut recapture comparison.

## Output and exchange semantics

response describes the original law's unrestricted limiting response.
Numerical output is expressly discovery, not an upper certificate.
The exactCut option includes its integer certificate.

Each rows entry contains:

- id: SHA256-based identity of the frozen physical vertex list;
- path: exact [time,position] germ vertices of the radial Princess path;
- payoffs: numeric limiting payoff against ALL original bank atoms;
- exact_payoffs: the same row as exact rational strings;
- capture_germs: optional full rational-function pair costs;
- weighted_recapture: exact original-bank weighted cost and its limit;
- witness_validation: exact physical recapture under the law whose cut
  generated the path;
- provenance: original/witness law hashes, chosen connector/strictification,
  subordinate scale, and an explicit immutable-path marker.

The path is paired with its reflection. Its final position is extended
constantly. Collinear vertices and a redundant final constant leg are removed
without changing the physical function.

For original-germ witnesses, weighted_recapture and witness_validation refer
to the same law. For collapsed-ordinary witnesses they generally differ.
Every master row always uses payoffs against the ORIGINAL bank. The collapsed
companion must never replace an existing germ Monster column or inherit
its old payoff entries.

All reported weighted costs are accumulated exactly. The worker checks their
limits against the corresponding abstract cut profile. It also rejects a
returned legal path whose original-bank score exceeds the original numerical
cut by more than the stated tolerance. Geometry and contact tests use exact
germ comparisons, not limiting-time comparisons.

## Native verification

verify_upper_oracle_worker.mjs checks all six upper-germ fixtures with exact
original and ordinary companion cuts, physical recapture, ten ordinary input
formats, and a zero-weight epsilon^5 attack that must leave the active
realization unchanged while receiving a new physical payoff entry.

The first full native case had1087 atoms and119 positive probabilities. Two
original-cut paths and three companion paths were produced in about12 seconds.
All five paths have complete1087-entry exact payoff rows. Their own-law
weighted physical recaptures equal their abstract cut scores exactly.

Those runs are response calculations for supplied laws. They do not establish
a matching lower strategy or solve the unrestricted game.
