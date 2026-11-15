"use strict";

// Native replay of the tight certificate. The historical CLI reads the older
// upper_warp_exact.json; this entry point deliberately pins the later file.
// The flow witness proves the whole finite-event oracle, not sampled paths.
const assert = require("node:assert/strict");
const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const E = require("../interval_turn_density/atomic_survival_v8.cjs");
const W = require("./upper_warp.cjs");
const V = require("./verify_upper_warp.cjs");
const Q = E.Physical.Q;

const EXPECTED_VALUE = "57045188913812444387410009/40000000000000000000000000";
const EXPECTED_SOURCE_BLOB = "188b8b43fad7c69cafb42195d69d045cb44e8f23";
const EXPECTED_TIGHT_BLOB = "d65307fc15a16d9760341599f999f77892463109";

function gitBlob(bytes) {
  return crypto.createHash("sha1")
    .update(Buffer.from("blob " + bytes.length + "\0"))
    .update(bytes).digest("hex");
}

function checkProbabilityAndCompletion(source, candidate) {
  const denominator = BigInt(source.weight_denominator);
  assert(denominator > 0n);
  assert.equal(candidate.weights_denominator, source.weight_denominator);
  let mass = 0n;
  for (const atom of candidate.atoms) {
    const weight = BigInt(atom.weight_numerator);
    assert(weight > 0n, "every stored pair has positive probability");
    mass += weight;
    const vertices = atom.exact_light.map(p => p.map(x => new Q(x)));
    assert.equal(vertices[0][0].add(vertices[0][1]).n, 0n);
    const endpoints = new Set(vertices.map(([u, v]) => String(u.sub(v))));
    assert(endpoints.has("-2") && endpoints.has("2"),
      "every Monster route visits both endpoints");
  }
  assert.equal(mass, denominator);
}

// Recompile the actual warped physical routes, independently of the common-map
// interval decomposition. Every exact reward coefficient must agree with the
// interval basis at this particular (nonidentity) warp. No floating capacities
// are used in the comparison.
function checkWarpedRewardCoefficients(source, candidate) {
  const data = W.build(source);
  const model = new E.Rational.Model(candidate.atoms);
  const denominator = BigInt(candidate.increment_denominator);
  const cumulative = [0n];
  for (const n of candidate.increment_numerators)
    cumulative.push(cumulative.at(-1) + BigInt(n));
  assert.equal(cumulative.at(-1), denominator);
  const index = new Map(data.knots.map((s, i) => [s, i]));
  function warp(s) {
    const f = W.fold(new Q(s));
    const i = index.get(String(f.radius));
    assert.notEqual(i, undefined, "every event coordinate has a stored knot");
    return String(new Q(BigInt(f.constant)).add(
      new Q(BigInt(f.sign) * cumulative[i], denominator)));
  }
  assert.deepEqual(model.v, data.full.v.map(warp));
  assert.deepEqual(model.base, data.full.base.map(warp));
  assert.deepEqual(model.bounds, data.full.bounds);
  assert.deepEqual(model.offset, data.full.offset);
  assert.equal(model.N, data.full.N);
  const reference = E.Rational.restore(data.full, data.atoms);
  // The restored model carries unprojected geometry but not reward definitions.
  // Recompile reference definitions in the same fixed physical route order.
  reference.defs = [];
  reference.defMap = new Map();
  for (let j = 0; j < source.atoms.length; ++j) reference.compile(j);
  assert.deepEqual(model.defs, reference.defs,
    "strict warp preserves every strict/closed capture predicate");

  const fromIntervals = new Array(model.defs.length).fill(0n);
  const fromPhysicalRoutes = new Array(model.defs.length).fill(0n);
  for (const [id, low, high, weight] of data.intervals)
    fromIntervals[id] += BigInt(weight) * (cumulative[high] - cumulative[low]);
  for (let j = 0; j < candidate.atoms.length; ++j) {
    model.compile(j);
    const weight = BigInt(candidate.atoms[j].weight_numerator);
    for (const [id, coefficient] of model.lastExactUnits) {
      assert.equal(denominator % coefficient.d, 0n);
      fromPhysicalRoutes[id] += weight * coefficient.n * (denominator / coefficient.d);
    }
  }
  assert.deepEqual(fromIntervals, fromPhysicalRoutes,
    "all exact reward coefficients agree at the tight warp");
  for (const labels of [candidate.minimum_labels, candidate.maximum_labels]) {
    assert.equal(labels.length, model.bounds.length);
    for (let i = 0; i < labels.length; ++i) {
      assert(Number.isSafeInteger(labels[i]));
      assert(labels[i] >= model.bounds[i][0] && labels[i] <= model.bounds[i][1]);
      if (i) assert(labels[i - 1] <= labels[i]);
    }
    let score = new Q(0n);
    const row = model.rowExact(labels);
    for (let j = 0; j < row.length; ++j)
      score = score.add(row[j].mul(new Q(BigInt(candidate.atoms[j].weight_numerator),
        BigInt(candidate.weights_denominator))));
    assert.equal(String(score), EXPECTED_VALUE);
  }
  return {
    direct_warped_reward_coefficients: model.defs.length,
    direct_warped_event_rows: model.v.length,
    direct_warped_capture_rows: 2,
    direct_warped_capture_predicates_preserved: true
  };
}

function verifyTightUpper() {
  const sourcePath = path.join(__dirname, "../interval_global_closure/upper_dyadic_exact.json");
  const candidatePath = path.join(__dirname, "upper_warp_tight_exact.json");
  const sourceBytes = fs.readFileSync(sourcePath);
  const candidateBytes = fs.readFileSync(candidatePath);
  assert.equal(gitBlob(sourceBytes), EXPECTED_SOURCE_BLOB, "pinned source certificate bytes");
  assert.equal(gitBlob(candidateBytes), EXPECTED_TIGHT_BLOB, "pinned tight certificate bytes");
  const source = JSON.parse(sourceBytes);
  const candidate = JSON.parse(candidateBytes);
  assert.equal(candidate.source_certificate_blob, EXPECTED_SOURCE_BLOB);
  assert.equal(candidate.exact_value, EXPECTED_VALUE);
  checkProbabilityAndCompletion(source, candidate);
  const replay = V.verifyUpperWarp(source, candidate);
  assert.equal(replay.value, EXPECTED_VALUE);
  const coefficients = checkWarpedRewardCoefficients(source, candidate);
  const earlier = new Q("57045189772271291487410009/40000000000000000000000000");
  return {
    scope: "Native exact replay of the tight unrestricted Princess-response upper certificate; no matching game lower bound or Lean verification.",
    candidate_file: "upper_warp_tight_exact.json",
    candidate_git_blob: EXPECTED_TIGHT_BLOB,
    source_git_blob: EXPECTED_SOURCE_BLOB,
    ...replay,
    ...coefficients,
    improvement_over_earlier_warp: String(earlier.sub(new Q(EXPECTED_VALUE)))
  };
}

module.exports = {verifyTightUpper};
if (require.main === module) console.log(JSON.stringify(verifyTightUpper(), null, 2));
