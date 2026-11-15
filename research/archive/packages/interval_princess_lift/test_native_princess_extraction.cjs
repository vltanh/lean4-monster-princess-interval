"use strict";
// A small actual native replay checks extraction provenance and both input
// encodings. The existing independent BigInt verifier checks compatibility
// on this n=6 regression only; the cheap extractor itself never runs it.
const fs = require("node:fs"), path = require("node:path"), os = require("node:os");
const crypto = require("node:crypto"), { execFileSync } = require("node:child_process");
const { Q, inspectProfile, createEvaluator, verifyExtraction } = require("../interval_clock_grid/extract_normalized_princess.cjs");
const { expandField } = require("../interval_clock_grid/qout_field_codec.cjs");
const { extractNative, writeExtraction } = require("./extract_native_princess.cjs");
const ROOT = path.resolve(__dirname, "../..");
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const encode = obj => Buffer.from(JSON.stringify(obj, null, 2) + "\n");
const assert = (ok, why) => { if (!ok) throw Error(why); };

function main() {
  const work = fs.mkdtempSync(path.join(os.tmpdir(), "native-princess-lift-"));
  try {
    const fixture = JSON.parse(fs.readFileSync(path.join(ROOT, "packages/interval_clock_grid/normalized_princess_n6_fixture.json")));
    fixture.global_lower = new Q(fixture.minimum_units, fixture.objective_denominator).sub(new Q(1n, 2n * BigInt(fixture.n))).toString();
    const full = expandField(fixture);
    delete full.format; delete full.encoding; delete full.pre_two_values_base64;
    const input = path.join(work, "full.json"), native = path.join(work, "native.json");
    fs.writeFileSync(input, encode(full));
    const verifyNative = (field, report) => execFileSync("python3", [
      path.join(ROOT, "packages/interval_clock_grid/normalized_native/verify_native_field.py"),
      field, "--output", report
    ], { cwd: ROOT, stdio: "pipe" });
    verifyNative(input, native);
    const prefix = path.join(work, "lift"), bridge = writeExtraction(input, native, prefix);
    assert(bridge.status === "PASS" && bridge.independent_bigint_replay_performed === false,
           "cheap extraction overclaims BigInt replay");
    assert(bridge.native_exhaustive_search_replayed_by_this_extractor === false,
           "cheap extraction overclaims native replay");
    const compactBytes = fs.readFileSync(prefix + ".field.json");
    const strategy = JSON.parse(fs.readFileSync(prefix + ".princess.json"));
    assert(fs.readFileSync(native).equals(fs.readFileSync(prefix + ".native-source-replay.json")),
           "original native report was not byte-preserved");
    assert(bridge.original_field_sha256 === sha256(fs.readFileSync(input)) &&
           bridge.compact_field_sha256 === sha256(compactBytes), "old/new input hashes differ");
    assert(inspectProfile(full).raw.equals(inspectProfile(JSON.parse(compactBytes)).raw),
           "compaction changed nodal values");
    assert(strategy.interpolation_epsilon === "1/12", "wrong default epsilon");
    const future = verifyExtraction(compactBytes, strategy);
    assert(future.status === "PASS" && future.guaranteed_security === strategy.guaranteed_security,
           "future independent BigInt extraction replay is incompatible");

    // A separately replayed compact input is accepted without special casing
    // its earlier source provenance or reusing the full-input byte hash.
    const compactReplay = path.join(work, "compact-native.json");
    verifyNative(prefix + ".field.json", compactReplay);
    const fromCompact = extractNative(compactBytes, fs.readFileSync(compactReplay));
    assert(fromCompact.strategy.guaranteed_security === strategy.guaranteed_security,
           "full/compact exact guarantees differ");
    const first = createEvaluator(strategy), second = createEvaluator(fromCompact.strategy);
    for (const t of ["0", "1/2", "1", "3/2", "2", "3"]) {
      for (const x of ["-1", "-1/3", "0", "1/3", "1"]) {
        assert(first.strictCDF(t, x).cmp(second.strictCDF(t, x)) === 0,
               "full/compact CDF evaluations differ");
      }
    }

    const good = JSON.parse(fs.readFileSync(native));
    let rejected = 0;
    function reject(mutator, epsilon) {
      const bad = JSON.parse(JSON.stringify(good));
      mutator(bad);
      try { extractNative(input, encode(bad), epsilon); }
      catch (_) { rejected++; return; }
      throw Error("tampered or incomplete native report accepted");
    }
    reject(x => { x.status = "RUNNING"; });
    reject(x => { x.input_sha256 = "0".repeat(64); });
    reject(x => { x.verifier_source_sha256 = "0".repeat(64); });
    reject(x => { x.n++; });
    reject(x => { x.pricing.certifies_lower = false; });
    reject(x => { x.pricing.minimum_units = String(BigInt(x.pricing.minimum_units) + 1n); });
    reject(x => { x.global_value_lower = "2"; });
    reject(() => {}, "0");
    reject(() => {}, "3/4");
    // Even a report rebound to altered bytes cannot bypass independent Qout
    // validation: the source's first radial value is made greater than one.
    const badField = JSON.parse(JSON.stringify(full));
    badField.radial_nodes[0][2] = String(BigInt(full.field_denominator) + 1n);
    const badBytes = encode(badField), rebound = { ...good, input_sha256: sha256(badBytes) };
    let qoutRejected = false;
    try { extractNative(badBytes, encode(rebound)); } catch (_) { qoutRejected = true; }
    assert(qoutRejected, "independent Qout guard accepted an illegal field");
    process.stdout.write(JSON.stringify({ status: "PASS", grid: 6,
      actual_native_replays: 2, independent_bigint_regression: "PASS",
      source_report_byte_preservation: true, full_and_compact_inputs: true,
      canonical_future_extraction_compatible: true, rejected_cases: rejected + 1,
      explicit_princess_security: strategy.guaranteed_security }, null, 2) + "\n");
  } finally {
    fs.rmSync(work, { recursive: true, force: true });
  }
}

if (require.main === module) main();
