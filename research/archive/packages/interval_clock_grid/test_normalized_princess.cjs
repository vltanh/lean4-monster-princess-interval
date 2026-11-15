"use strict";
// Exact implementation regressions. Continuous legality/security are supplied
// by the extraction and Qout normalization proofs, not by sampled tests.
const fs = require("node:fs"), path = require("node:path"), zlib = require("node:zlib");
const crypto = require("node:crypto");
const ex = require("./extract_normalized_princess.cjs");
const legacy = require("./extract_princess.cjs");
const { expandField } = require("./qout_field_codec.cjs");
const { verifyNormalizedDual } = require("./normalized_record_pricing.cjs");
const { Q } = ex;
const counts = { fixtures: 0, pricing_replays: 0, extractions: 0, exact_nodes: 0,
  legacy_cdf_comparisons: 0, affine_piece_checks: 0, symmetry_checks: 0,
  transport_checks: 0, outward_checks: 0, quantile_inversions: 0,
  quantile_speed_checks: 0, rejected_malformed_inputs: 0 };
function equal(a, b, label) { if (Q.of(a).cmp(b)) throw Error(label + ": " + a + " != " + b); }
function mustThrow(fn, label) {
  let threw = false; try { fn(); } catch (_) { threw = true; }
  if (!threw) throw Error("accepted malformed " + label);
  counts.rejected_malformed_inputs++;
}
function bytes(data) { return Buffer.from(JSON.stringify(data, null, 2) + "\n"); }
function simpleField(n, numerator) {
  const D = 1000 * 2 * n, radial_nodes = [];
  for (let j = 0; j <= 12 * n; j++) for (let k = 1; k <= 2 * n; k++) if ((j + k) % 2 === 0) {
    const foot = Math.max(0, k - Math.max(0, j - 4 * n));
    radial_nodes.push([j, k, String(numerator * foot)]);
  }
  return ex.inspectProfile({ n, field_denominator: String(D), normalized_profile: true, radial_nodes }).profile;
}
function expandedLegacy(profile, epsilon) {
  const full = expandField(profile), n = full.n, values = new Map(full.radial_nodes.map(([j, k, a]) => [j + "," + k, a]));
  const radial_nodal = [];
  for (let k = 0; k <= 2 * n; k++) for (let j = k % 2; j <= 16 * n; j += 2) {
    radial_nodal.push([j, k, k === 0 || j > 12 * n ? "0" : values.get(j + "," + k)]);
  }
  return legacy.createEvaluator({ format: "clock-grid-princess-p1-v1", n,
    interpolation_epsilon: epsilon, cdf_denominator: full.field_denominator,
    outward_time: 2, absorption_time: 3, radial_nodal });
}
function compareCDF(ev, old, t, x) {
  equal(ev.rawTrace(t, x), old.rawTrace(t, x), "raw trace");
  equal(ev.interiorTrace(t, x), old.interiorTrace(t, x), "stopped/outward trace");
  equal(ev.strictCDF(t, x), old.strictCDF(t, x), "strict CDF");
  if (Q.of(x).cmp(0) >= 0) equal(ev.radialCDF(t, x), old.radialCDF(t, x), "radial CDF");
  counts.legacy_cdf_comparisons++;
}
function runFixture(profile, name) {
  const full = expandField(profile), n = profile.n, initial = bytes(profile);
  const rawReport = verifyNormalizedDual(full);
  counts.pricing_replays++;
  const source = bytes({ ...profile, minimum_units: rawReport.verified_lower_units,
    objective_denominator: rawReport.objective_denominator, normalized_bank_dual_value: rawReport.normalized_bank_lower });
  const report = { ...rawReport, input_sha256: ex.readSource(source).input_sha256 };
  const fixtureSummary = { name, n, finite_dual_lower: report.normalized_bank_lower, epsilons: [] };
  for (const epsilon of Array.from(new Set(["1/2", "1/" + (2 * n), "1/512"]))) {
    const strategy = ex.makeStrategy(source, report, epsilon), ev = ex.createEvaluator(strategy), old = expandedLegacy(profile, epsilon);
    const replay = ex.verifyExtraction(source, strategy);
    counts.pricing_replays++; counts.extractions++;
    fixtureSummary.epsilons.push({ epsilon, guaranteed_security: replay.guaranteed_security });
    const table = new Map(full.radial_nodes.map(([j, k, a]) => [j + "," + k, BigInt(a)]));
    for (let j = 0; j <= 16 * n; j++) for (let k = -2 * n; k <= 2 * n; k++) if ((j + k) % 2 === 0) {
      const D = BigInt(profile.field_denominator), v = k === 0 || j > 12 * n ? 0n : table.get(j + "," + Math.abs(k));
      const t = new Q(BigInt(j), BigInt(2 * n)), x = new Q(BigInt(k), BigInt(2 * n));
      equal(ev.rawTrace(t, x), new Q(D + (k >= 0 ? v : -v), 2n * D), "all exact nodes");
      compareCDF(ev, old, t, x); counts.exact_nodes++;
    }
    const times = ["0", new Q(1n, BigInt(4 * n)), "1/2", "3/4", "1", "7/4", "2"];
    for (const t of times) {
      const points = ev.radialBreakpoints(t);
      for (let i = 0; i < points.length; i++) {
        const r = points[i]; compareCDF(ev, old, t, r); compareCDF(ev, old, t, r.mul(-1));
        if (i + 1 < points.length) {
          const left = ev.interiorTrace(t, r), right = ev.interiorTrace(t, points[i + 1]);
          for (const rank of [new Q(1n, 2n), new Q(1n, 3n)]) {
            const middle = r.add(points[i + 1].sub(r).mul(rank));
            equal(ev.interiorTrace(t, middle), left.add(right.sub(left).mul(rank)), "complete affine breakpoint list");
            compareCDF(ev, old, t, middle); counts.affine_piece_checks++;
          }
        }
      }
    }
    const B = 2 * n, dt = new Q(1n, BigInt(B));
    for (let j = 0; j <= 3 * B; j++) for (let k = -B; k <= B; k++) {
      const t = new Q(BigInt(j), BigInt(B)), x = new Q(BigInt(k), BigInt(B)), f = ev.interiorTrace(t, x);
      equal(f.add(ev.interiorTrace(t, x.mul(-1))), 1, "symmetry"); counts.symmetry_checks++;
      if (k > -B) {
        if (ev.interiorTrace(t.add(dt), x.sub(dt)).cmp(f) > 0) throw Error("left transport"); counts.transport_checks++;
      }
      if (k < B) {
        if (ev.interiorTrace(t.add(dt), x.add(dt)).cmp(f) < 0) throw Error("right transport"); counts.transport_checks++;
      }
      if (j >= 2 * B && k >= 0 && k < B) {
        equal(ev.interiorTrace(t.add(dt), x.add(dt)), f, "outward characteristic"); counts.outward_checks++;
      }
    }
    for (const rank of ["0", "1/8", "1/2", "7/8", "99/100"]) {
      let previous = null;
      for (let j = 0; j <= 3 * B; j++) {
        const t = new Q(BigInt(j), BigInt(B)), r = ev.radiusAt(t, rank);
        if (r.cmp(0) < 0 || r.cmp(1) > 0) throw Error("quantile outside interval");
        if (r.cmp(1) < 0) equal(ev.radialCDF(t, r), rank, "quantile inversion");
        else if (ev.interiorTrace(t, 1).mul(2).sub(1).cmp(rank) > 0) throw Error("invalid endpoint atom quantile");
        if (previous !== null) {
          const difference = r.sub(previous);
          if (difference.cmp(dt) > 0 || difference.cmp(dt.mul(-1)) < 0) throw Error("quantile exceeds speed one");
          if (previous.cmp(1) === 0) equal(r, 1, "quantile endpoint stopping");
          counts.quantile_speed_checks++;
        }
        if (j > 2 * B) {
          const outward = ev.radiusAt(2, rank).add(t.sub(2));
          equal(r, outward.cmp(1) < 0 ? outward : 1, "quantile outward formula");
        }
        equal(ev.positionAt(t, rank, -1), r.mul(-1), "fixed negative sign");
        previous = r; counts.quantile_inversions++;
      }
    }
    equal(ev.strictCDF(0, -1), 0, "negative endpoint strict CDF");
    equal(ev.strictCDF(0, "1001/1000"), 1, "outside positive endpoint");
    mustThrow(() => ev.radiusAt(0, 1), "rank one");
    mustThrow(() => ex.makeStrategy(source, { ...report, input_sha256: "0".repeat(64) }, epsilon), "report hash");
    mustThrow(() => ex.makeStrategy(source, { ...report, verified_lower_units: String(BigInt(report.verified_lower_units) + 1n) }, epsilon), "report lower");
    mustThrow(() => ex.createEvaluator({ ...strategy, guaranteed_security: "9" }), "claimed guarantee");
  }
  counts.fixtures++;
  return fixtureSummary;
}

function changedEncoding(profile, edit) {
  const raw = zlib.inflateSync(Buffer.from(profile.pre_two_values_base64, "base64")); edit(raw);
  return { ...profile, encoding: { ...profile.encoding, uncompressed_sha256: crypto.createHash("sha256").update(raw).digest("hex") },
    pre_two_values_base64: zlib.deflateSync(raw).toString("base64") };
}
function main() {
  const endpoint = simpleField(1, 0), mixture = simpleField(2, 731);
  const n6 = JSON.parse(fs.readFileSync(path.join(__dirname, "normalized_princess_n6_fixture.json"), "utf8"));
  const fixtures = [runFixture(endpoint, "constant endpoint law"), runFixture(mixture, "stationary uniform plus endpoint atom"), runFixture(n6, "nonoptimal native n6 Qout profile")];
  mustThrow(() => ex.inspectProfile({ ...n6, encoding: { ...n6.encoding, uncompressed_sha256: "0".repeat(64) } }), "checksum");
  mustThrow(() => ex.inspectProfile(changedEncoding(mixture, raw => raw.writeUInt32LE(0xffffffff, 0))), "out-of-range value");
  mustThrow(() => ex.inspectProfile(changedEncoding(mixture, raw => raw.writeUInt32LE(Number(mixture.field_denominator), 4 * mixture.n))), "transport violation");
  mustThrow(() => ex.inspectProfile(changedEncoding(endpoint, raw => raw.writeUInt32LE(Number(endpoint.field_denominator), 8))), "nonsticky endpoint trace");
  const full = expandField(mixture), corrupt = { ...full, format: undefined, radial_nodes: full.radial_nodes.map(a => a.slice()) };
  const item = corrupt.radial_nodes.find(([j]) => j > 4 * mixture.n); item[2] = String(BigInt(item[2]) + 1n);
  mustThrow(() => ex.inspectProfile(corrupt), "nonoutward full table");
  return { status: "PASS", scope: "Independent expanded-v1 CDF comparisons, exact nodal recovery, complete fixed-time affine breakpoints, quantile inversion and speed/stopping regressions; exact BigInt target-bound regeneration on each fixture.",
    counts, fixtures };
}
module.exports = { main };
if (require.main === module) {
  try { process.stdout.write(JSON.stringify(main(), null, 2) + "\n"); }
  catch (error) { process.stderr.write(error.stack + "\n"); process.exitCode = 1; }
}
