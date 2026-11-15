"use strict";
// Compact a native-certified Qout field and extract a canonical explicit law.
// This checks every Qout inequality with the independent JavaScript decoder,
// source/report hashes, and exact bound arithmetic. It neither reruns the
// complete native search nor claims an independent BigInt pricing replay.
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const {
  Q, readSource, inspectProfile, makeStrategy, createEvaluator
} = require("../interval_clock_grid/extract_normalized_princess.cjs");

const ROOT = path.resolve(__dirname, "../..");
const NATIVE_SOURCE = path.join(ROOT, "packages/interval_clock_grid/normalized_native/price_normalized.cpp");
const METHOD = "native-exhaustive-integer-pricing-with-independent-qout-validation";
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const encode = data => Buffer.from(JSON.stringify(data, null, 2) + "\n");

function requireThat(condition, message) {
  if (!condition) throw Error(message);
}

function sameFraction(actual, expected, context) {
  requireThat(actual !== undefined && Q.of(actual).cmp(expected) === 0, context + " disagrees");
}

function extractNative(fieldFilenameOrBytes, replayFilenameOrBytes, epsilon) {
  const source = readSource(fieldFilenameOrBytes);
  const native = readSource(replayFilenameOrBytes);
  const data = source.data, report = native.data;
  // inspectProfile independently reconstructs full/compact inputs and checks
  // every transport, sticky endpoint, and outward continuation constraint.
  // Only after this succeeds may the adapted report say qout_verified=true.
  const p = inspectProfile(data);
  const sourceHash = sha256(fs.readFileSync(NATIVE_SOURCE));
  requireThat(report.status === "PASS", "native replay must have status PASS");
  requireThat(report.n === p.n, "native replay grid differs");
  requireThat(report.input_sha256 === source.input_sha256, "native replay is not bound to the source field bytes");
  requireThat(report.verifier_source_sha256 === sourceHash, "native verifier source hash differs from current C++ source");
  if (data.native_source_sha256 !== undefined) {
    requireThat(data.native_source_sha256 === sourceHash, "source field names a different native verifier");
  }
  const pricing = report.pricing;
  requireThat(pricing && pricing.status === "PASS" && pricing.certifies_lower !== false,
              "native report lacks completed exact pricing");
  requireThat(pricing.n === p.n && BigInt(pricing.field_denominator) === p.D,
              "native pricing dimensions differ");
  const units = BigInt(pricing.minimum_units), denominator = 4n * BigInt(p.n) * p.D;
  requireThat(units >= 0n, "negative native minimum");
  requireThat(BigInt(pricing.objective_denominator) === denominator,
              "native pricing scale differs");
  requireThat(BigInt(data.minimum_units) === units && BigInt(data.objective_denominator) === denominator,
              "source claimed minimum or scale differs");
  const finiteLower = new Q(units, denominator);
  const gameLower = new Q(units - 2n * p.D, denominator);
  sameFraction(data.normalized_bank_dual_value, finiteLower, "source finite lower");
  sameFraction(data.global_lower, gameLower, "source global lower");
  sameFraction(report.exact_bank_dual, finiteLower, "native replay finite lower");
  sameFraction(report.global_value_lower, gameLower, "native replay global lower");
  const e = epsilon === undefined ? new Q(1n, 2n * BigInt(p.n)) : Q.of(epsilon);
  requireThat(e.cmp(0) > 0 && e.cmp(new Q(1n, 2n)) <= 0, "epsilon must lie in (0,1/2]");
  const decodedHash = sha256(p.raw);
  requireThat(decodedHash === p.profile.encoding.uncompressed_sha256,
              "decoded nodal identity disagrees");

  const compact = {
    ...p.profile,
    scope: "Exact compact Qout field with a completed native integer minimum; global value lower uses the proved full-bank normalization and continuum transfer.",
    minimum_units: String(units),
    objective_denominator: String(denominator),
    normalized_bank_dual_value: finiteLower.toString(),
    global_lower: gameLower.toString(),
    native_source_sha256: sourceHash,
    source_certificate: {
      method: METHOD,
      original_field_sha256: source.input_sha256,
      original_native_replay_sha256: native.input_sha256,
      decoded_nodal_profile_sha256: decodedHash,
      verifier_source_sha256: sourceHash
    }
  };
  const compactBytes = encode(compact), compactHash = sha256(compactBytes);
  // This is an exact interface adapter from the independently decoded native
  // replay. It is not presented as a normalized BigInt replay report.
  const adapted = {
    status: "PASS", qout_verified: true, n: p.n,
    input_sha256: compactHash, verified_lower_units: String(units),
    objective_denominator: String(denominator),
    normalized_bank_lower: finiteLower.toString()
  };
  const strategy = makeStrategy(compactBytes, adapted, e.toString());
  // The standard strategy object is deliberately left canonical: a future
  // verifyExtraction(compactBytes,strategy) can regenerate it byte-for-field.
  const evaluator = createEvaluator(strategy);
  requireThat(evaluator.stored_radial_nodes === p.count, "strategy node count differs");
  const strategyBytes = encode(strategy);
  const bridge = {
    status: "PASS",
    certificate_method: METHOD,
    scope: "Hash-bound compaction and explicit Princess extraction from an already completed native exhaustive replay, with independent exact JavaScript Qout validation. This extractor does not reprice the bank.",
    n: p.n,
    original_field_sha256: source.input_sha256,
    compact_field_sha256: compactHash,
    decoded_nodal_profile_sha256: decodedHash,
    original_native_replay_sha256: native.input_sha256,
    copied_native_replay_sha256: sha256(native.bytes),
    current_native_source_sha256: sourceHash,
    native_replay_bound_to_original_field: true,
    complete_native_integer_replay: "PASS (supplied hash-bound report)",
    native_exhaustive_search_replayed_by_this_extractor: false,
    independent_bigint_replay_performed: false,
    independent_qout_validation: {
      status: "PASS", stored_radial_nodes: p.count,
      cone_inequalities: p.coneChecks, sticky_endpoint_inequalities: p.endpointChecks
    },
    finite_dual_lower: finiteLower.toString(),
    certified_game_value_lower: gameLower.toString(),
    interpolation_epsilon: e.toString(),
    exact_transfer_loss: strategy.exact_transfer_loss,
    explicit_princess_security: strategy.guaranteed_security,
    strategy_sha256: sha256(strategyBytes),
    future_independent_replay: "Use extract_normalized_princess.cjs verify with the compact field and canonical strategy; that is a separate optional exhaustive BigInt computation."
  };
  return { compact, compactBytes, strategy, strategyBytes,
           nativeReportBytes: native.bytes, bridge };
}

function writeExtraction(fieldPath, replayPath, outputPrefix, epsilon) {
  const result = extractNative(fieldPath, replayPath, epsilon);
  const prefix = path.resolve(outputPrefix);
  fs.mkdirSync(path.dirname(prefix), { recursive: true });
  const nativeGzip = result.nativeReportBytes[0] === 0x1f && result.nativeReportBytes[1] === 0x8b;
  const files = {
    compact_field: prefix + ".field.json",
    princess_strategy: prefix + ".princess.json",
    native_source_replay: prefix + ".native-source-replay.json" + (nativeGzip ? ".gz" : ""),
    extraction_report: prefix + ".extraction.json"
  };
  fs.writeFileSync(files.compact_field, result.compactBytes);
  fs.writeFileSync(files.princess_strategy, result.strategyBytes);
  fs.writeFileSync(files.native_source_replay, result.nativeReportBytes);
  result.bridge.files = Object.fromEntries(Object.entries(files).map(([key, value]) => [key, path.basename(value)]));
  fs.writeFileSync(files.extraction_report, encode(result.bridge));
  return result.bridge;
}

module.exports = { extractNative, writeExtraction };
if (require.main === module) {
  try {
    const [field, replay, ...args] = process.argv.slice(2);
    if (!field || !replay) throw Error("usage: FIELD NATIVE_REPLAY --output PREFIX [--epsilon RATIONAL]");
    let output, epsilon;
    for (let i = 0; i < args.length; i++) {
      if (args[i] === "--output" && args[i + 1]) output = args[++i];
      else if (args[i] === "--epsilon" && args[i + 1]) epsilon = args[++i];
      else throw Error("unknown or incomplete option: " + args[i]);
    }
    if (!output) throw Error("--output PREFIX is required");
    process.stdout.write(JSON.stringify(writeExtraction(field, replay, output, epsilon), null, 2) + "\n");
  } catch (error) {
    process.stderr.write(error.stack + "\n");
    process.exitCode = 1;
  }
}
