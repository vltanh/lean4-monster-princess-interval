"use strict";
// Only the maximum-flow search is native. Existing BigInt physical/edge/flow
// verification runs afterward, followed by an independent Python replay.
const fs = require("node:fs");
const S = require("../interval_sparse_upper/sparse_certificate.cjs");
const N = require("../interval_integer_flow/native_server.cjs");
const E = require("../interval_clock_grid/exact_certificate.cjs");

if (process.argv.length !== 5)
  throw Error("usage: solve_upper.cjs input.json output.json integer_maxflow");
const [input, output, binary] = process.argv.slice(2);
const c = JSON.parse(fs.readFileSync(input, "utf8"));
const expected = c.global_upper;
const g = S.buildClosure(c);
const f = N.nativeMaximumFlow(g, binary);
c.closure_flow = f.entries;
c.closure_source_side = f.source_side;
c.global_upper = E.fraction(g.stats.mass + g.positive - f.flow,
                           4n * BigInt(g.n) * g.W);
if (c.global_upper !== expected) throw Error("saved upper differs from exact flow");
const replay = S.verify(c);
fs.writeFileSync(output, JSON.stringify(c) + "\n");
fs.writeFileSync(output.replace(/\.json$/, ".node_replay.json"),
                 JSON.stringify(replay, null, 2) + "\n");
console.log(JSON.stringify(replay));
