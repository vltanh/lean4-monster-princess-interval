"use strict";
// Extract an explicit continuous Princess law from ANY certified Qout lower.
// A supplied pricing report is evidence to bind, not a replacement for replay:
// the `verify` command reruns the independent BigInt normalized-bank pricer.
// CDF evaluation stores only pre-time-2 nodes, and never expands the full bank.
const fs = require("node:fs");
const zlib = require("node:zlib");
const crypto = require("node:crypto");
const { Q } = require("./extract_princess.cjs");

const ZERO = new Q(0n), ONE = new Q(1n), HALF = new Q(1n, 2n);
const FIELD_FORMAT = "qout-clock-grid-field-u32-zlib-v1";
const STRATEGY_FORMAT = "normalized-qout-princess-p1-v1";
const ORIENTATION = "k modulo 2n is positive for 0 <= k < n, negative otherwise";
const DOMAIN = "pre-two radial nodes: j=0..4n, then k=1..2n in ascending order with j+k even; center is zero; after time2 use outward footpoint, zero if footpoint<=0";
const sha256 = bytes => crypto.createHash("sha256").update(bytes).digest("hex");

function readSource(filenameOrBytes) {
  const bytes = Buffer.isBuffer(filenameOrBytes) ? filenameOrBytes : fs.readFileSync(filenameOrBytes);
  const json = bytes[0] === 0x1f && bytes[1] === 0x8b ? zlib.gunzipSync(bytes) : bytes;
  return { bytes, data: JSON.parse(json.toString("utf8")), input_sha256: sha256(bytes) };
}

function inspectProfile(input) {
  const n = input.n, D = BigInt(input.field_denominator);
  if (!Number.isSafeInteger(n) || n < 1 || n > 10000 ||
      D <= 0n || D > 0xffffffffn || input.normalized_profile !== true) {
    throw Error("invalid compact Qout parameters");
  }
  const R = 2 * n, C = 4 * n, count = (C + 1) * n;
  let raw, compressed;
  if (input.format === FIELD_FORMAT) {
    if (input.encoding?.count !== count ||
        input.encoding.integer_type !== "uint32 little-endian" ||
        input.encoding.compression !== "zlib" ||
        typeof input.pre_two_values_base64 !== "string") throw Error("invalid compact encoding");
    compressed = Buffer.from(input.pre_two_values_base64, "base64");
    if (compressed.toString("base64") !== input.pre_two_values_base64) throw Error("noncanonical base64");
    raw = zlib.inflateSync(compressed, { maxOutputLength: 4 * count });
    if (raw.length !== 4 * count || sha256(raw) !== input.encoding.uncompressed_sha256) {
      throw Error("compact field checksum mismatch");
    }
  } else {
    if (!Array.isArray(input.radial_nodes)) throw Error("missing radial field");
    raw = Buffer.alloc(4 * count);
    const seen = new Uint8Array(count), fullSeen = new Set();
    for (const [j, k, a] of input.radial_nodes) {
      if (!Number.isSafeInteger(j) || !Number.isSafeInteger(k) ||
          j < 0 || j > 12 * n || k < 1 || k > R || (j + k) % 2) throw Error("invalid radial node");
      const key = j + "," + k;
      if (fullSeen.has(key)) throw Error("duplicate radial node");
      fullSeen.add(key);
      const value = BigInt(a);
      if (value < 0n || value > D) throw Error("radial value out of range");
      if (j <= C) {
        const index = j * n + Math.floor((k - 1) / 2);
        seen[index] = 1;
        raw.writeUInt32LE(Number(value), 4 * index);
      }
    }
    if (seen.some(v => !v)) throw Error("missing pre-two radial node");
    if (fullSeen.size !== (12 * n + 1) * n) throw Error("incomplete full radial field");
    compressed = zlib.deflateSync(raw, { level: 9 });
  }
  function nodeNumber(j, k) {
    if (!Number.isSafeInteger(j) || !Number.isSafeInteger(k) ||
        j < 0 || j > 16 * n || k < 0 || k > R || (j + k) % 2) throw Error("node outside lattice");
    if (!k) return 0;
    if (j > C) { k -= j - C; j = C; }
    return k <= 0 ? 0 : raw.readUInt32LE(4 * (j * n + Math.floor((k - 1) / 2)));
  }
  let coneChecks = 0, endpointChecks = 0;
  for (let j = 0; j <= C; j++) for (let k = 1; k <= R; k++) if ((j + k) % 2 === 0) {
    const value = nodeNumber(j, k);
    if (BigInt(value) > D) throw Error("radial value out of range");
    if (k < R) for (const step of [-1, 1]) if (j + step >= 0 && j + step <= C) {
      if (value > nodeNumber(j + step, k + 1)) throw Error("nodal transport inequality");
      coneChecks++;
    }
  }
  for (let j = 0; j + 2 <= C; j += 2) {
    if (nodeNumber(j + 2, R) > nodeNumber(j, R)) throw Error("endpoint trace is not sticky");
    endpointChecks++;
  }
  if (input.format !== FIELD_FORMAT) {
    for (const [j, k, a] of input.radial_nodes) {
      if (BigInt(a) !== BigInt(nodeNumber(j, k))) throw Error("outward2 identity fails");
    }
  }
  const profile = {
    format: FIELD_FORMAT, n, field_denominator: String(D), normalized_profile: true,
    encoding: { domain: DOMAIN, integer_type: "uint32 little-endian", compression: "zlib",
      count, uncompressed_sha256: sha256(raw) },
    pre_two_values_base64: compressed.toString("base64")
  };
  return { n, D, R, C, raw, profile, count, coneChecks, endpointChecks,
    node: (j, k) => BigInt(nodeNumber(j, k)) };
}

function checkedLower(input, report, inputHash, p) {
  if (report.status !== "PASS" || report.qout_verified !== true ||
      report.n !== p.n || report.input_sha256 !== inputHash) throw Error("pricing report is not bound to this Qout input");
  const units = BigInt(report.verified_lower_units), denominator = 4n * BigInt(p.n) * p.D;
  if (units < 0n || BigInt(report.objective_denominator) !== denominator) throw Error("invalid exact pricing scale");
  const lower = new Q(units, denominator);
  if (Q.of(report.normalized_bank_lower).cmp(lower) !== 0) throw Error("pricing lower disagrees with integer units");
  if (input.minimum_units !== undefined && BigInt(input.minimum_units) !== units) throw Error("input claimed units disagree");
  if (input.objective_denominator !== undefined && BigInt(input.objective_denominator) !== denominator) throw Error("input claimed scale disagrees");
  if (input.normalized_bank_dual_value !== undefined && Q.of(input.normalized_bank_dual_value).cmp(lower) !== 0) throw Error("input claimed lower disagrees");
  return { units, denominator, lower };
}

function makeStrategy(filenameOrBytes, pricingReport, epsilon) {
  const source = readSource(filenameOrBytes), p = inspectProfile(source.data), e = Q.of(epsilon);
  if (e.cmp(0) <= 0 || e.cmp(HALF) > 0) throw Error("epsilon must lie in (0,1/2]");
  const { units, denominator, lower } = checkedLower(source.data, pricingReport, source.input_sha256, p);
  const loss = ONE.add(e).div(2 * p.n);
  return {
    format: STRATEGY_FORMAT,
    scope: "Explicit legal symmetric ordered Princess law from a verified feasible Qout dual lower; finite optimality is not assumed.",
    n: p.n, interpolation_epsilon: e.toString(), cdf_denominator: String(p.D),
    nodal_profile: p.profile, cell_orientation: ORIENTATION,
    quantile_rule: "Choose u uniformly in [0,1), use inf {r in [0,1] : radialCDF(t,r) > u}, and choose one independent fair sign for the entire path.",
    outward_time: 2, absorption_time: 3,
    source_input_sha256: source.input_sha256,
    verified_lower_units: String(units), objective_denominator: String(denominator),
    finite_dual_lower: lower.toString(), exact_transfer_loss: loss.toString(),
    guaranteed_security: lower.sub(loss).toString(),
    proof: "CONSTRUCTIVE_PRINCESS_GRID_DUAL.md, with its per-clock-plane lower replaced by the certified feasible lower; Qout full-bank pricing and the absence of additional stopping follow from NORMALIZED_GRID_BANK_PRICING.md."
  };
}

function createEvaluator(strategy) {
  if (strategy.format !== STRATEGY_FORMAT || strategy.outward_time !== 2 || strategy.absorption_time !== 3 ||
      strategy.cell_orientation !== ORIENTATION) throw Error("bad normalized strategy format");
  const p = inspectProfile(strategy.nodal_profile), { n, D, node } = p;
  const e = Q.of(strategy.interpolation_epsilon);
  if (strategy.n !== n || BigInt(strategy.cdf_denominator) !== D || e.cmp(0) <= 0 || e.cmp(HALF) > 0) throw Error("strategy parameters disagree");
  const lower = new Q(strategy.verified_lower_units, 4n * BigInt(n) * D), loss = ONE.add(e).div(2 * n);
  if (BigInt(strategy.objective_denominator) !== 4n * BigInt(n) * D ||
      Q.of(strategy.finite_dual_lower).cmp(lower) || Q.of(strategy.exact_transfer_loss).cmp(loss) ||
      Q.of(strategy.guaranteed_security).cmp(lower.sub(loss))) throw Error("strategy guarantee arithmetic disagrees");
  const A = HALF.sub(e), B = HALF.add(e), width = e.mul(2);
  function coordinate(z) {
    const q = Q.of(z).mul(n), cell = q.floor(), alpha = q.sub(new Q(cell));
    const mod = Number((cell % BigInt(2 * n) + BigInt(2 * n)) % BigInt(2 * n));
    return { cell: Number(cell), alpha, plus: mod < n, threshold: mod < n ? alpha : ONE.sub(alpha) };
  }
  function rawTrace(t, x) {
    t = Q.of(t); x = Q.of(x);
    if (t.cmp(0) < 0 || t.cmp(8) > 0 || x.cmp(-1) < 0 || x.cmp(1) > 0) throw Error("outside raw strip");
    const u = coordinate(t.add(x)), w = coordinate(t.sub(x)), cuts = [A, B];
    for (const c of [u, w]) if (c.alpha.cmp(0) && c.threshold.cmp(A) > 0 && c.threshold.cmp(B) < 0) cuts.push(c.threshold);
    cuts.sort((a, b) => a.cmp(b));
    function rounded(c, z) {
      if (c.alpha.cmp(0) === 0) return c.cell;
      return c.cell + +(c.plus ? z.cmp(c.alpha) < 0 : z.cmp(ONE.sub(c.alpha)) > 0);
    }
    let result = ZERO;
    for (let i = 0; i + 1 < cuts.length; i++) {
      const length = cuts[i + 1].sub(cuts[i]);
      if (length.cmp(0) === 0) continue;
      const z = cuts[i + 1].add(cuts[i]).div(2), U = rounded(u, z), W = rounded(w, z), k = U - W;
      const value = node(U + W, Math.abs(k));
      result = result.add(length.div(width).mul(new Q(D + (k >= 0 ? value : -value), 2n * D)));
    }
    return result;
  }
  function rawRadial(t, r) { return rawTrace(t, r).mul(2).sub(1); }
  function radialTrace(t, r) {
    if (t.cmp(2) <= 0) return rawRadial(t, r);
    const foot = r.sub(t.sub(2));
    return foot.cmp(0) <= 0 ? ZERO : rawRadial(new Q(2n), foot);
  }
  function radialCDF(t, r) {
    t = Q.of(t); r = Q.of(r);
    if (t.cmp(0) < 0) throw Error("negative time");
    if (r.cmp(0) < 0) return ZERO;
    if (r.cmp(1) >= 0) return ONE;
    return radialTrace(t, r);
  }
  function interiorTrace(t, x) {
    t = Q.of(t); x = Q.of(x);
    if (t.cmp(0) < 0 || x.cmp(-1) < 0 || x.cmp(1) > 0) throw Error("outside physical strip");
    if (x.cmp(0) === 0) return HALF;
    const positive = x.cmp(0) > 0, value = radialTrace(t, positive ? x : ZERO.sub(x));
    return ONE.add(positive ? value : ZERO.sub(value)).div(2);
  }
  function strictCDF(t, x) {
    t = Q.of(t); x = Q.of(x);
    if (t.cmp(0) < 0) throw Error("negative time");
    if (x.cmp(-1) <= 0) return ZERO;
    if (x.cmp(1) > 0) return ONE;
    return interiorTrace(t, x);
  }
  // At fixed pre-two t, changes of cells, clipping thresholds, and the two
  // threshold orders are the only possible affine breakpoints in r. The last
  // kind is r=k/(2n); for opposite orientations the order depends only on t.
  function radialBreakpoints(t) {
    t = Q.of(t);
    if (t.cmp(0) < 0 || t.cmp(2) > 0) throw Error("breakpoints require 0 <= t <= 2");
    const points = new Map();
    function add(r) { if (r.cmp(0) >= 0 && r.cmp(1) <= 0) points.set(r.toString(), r); }
    for (let k = 0; k <= 2 * n; k++) add(new Q(BigInt(k), BigInt(2 * n)));
    const first = Number(t.sub(1).mul(n).floor()) - 1, last = Number(t.add(1).mul(n).floor()) + 1;
    for (let i = first; i <= last; i++) for (const alpha of [ZERO, A, B]) {
      const z = new Q(BigInt(i)).add(alpha).div(n);
      add(z.sub(t)); add(t.sub(z));
    }
    return Array.from(points.values()).sort((a, b) => a.cmp(b));
  }
  function radiusAt(t, u) {
    t = Q.of(t); u = Q.of(u);
    if (t.cmp(0) < 0 || u.cmp(0) < 0 || u.cmp(1) >= 0) throw Error("quantile requires t >= 0 and 0 <= u < 1");
    if (t.cmp(2) > 0) {
      const radius = radiusAt(new Q(2n), u).add(t.sub(2));
      return radius.cmp(1) > 0 ? ONE : radius;
    }
    if (rawRadial(t, ONE).cmp(u) <= 0) return ONE;
    const points = radialBreakpoints(t);
    let lo = 0, hi = points.length - 1;
    while (lo + 1 < hi) {
      const mid = (lo + hi) >> 1;
      if (rawRadial(t, points[mid]).cmp(u) <= 0) lo = mid; else hi = mid;
    }
    const left = rawRadial(t, points[lo]), right = rawRadial(t, points[hi]);
    if (right.cmp(left) <= 0) throw Error("quantile inversion found a flat bracket");
    return points[lo].add(points[hi].sub(points[lo]).mul(u.sub(left)).div(right.sub(left)));
  }
  function positionAt(t, u, sign) {
    if (sign !== -1 && sign !== 1) throw Error("sign must be -1 or +1");
    return radiusAt(t, u).mul(sign);
  }
  return { rawTrace, radialCDF, interiorTrace, strictCDF, radialBreakpoints, radiusAt, positionAt,
    stored_radial_nodes: p.count, stored_bytes: p.raw.length,
    validation: { cone_inequalities: p.coneChecks, sticky_endpoint_inequalities: p.endpointChecks } };
}

function assertSameStrategy(actual, expected) {
  createEvaluator(actual);
  // Zlib byte streams can differ across versions. Compare their exact decoded
  // profiles, then every remaining field of the deterministic extraction.
  if (!inspectProfile(actual.nodal_profile).raw.equals(inspectProfile(expected.nodal_profile).raw)) {
    throw Error("strategy decoded nodes differ from exact extraction");
  }
  const a = { ...actual, nodal_profile: { ...actual.nodal_profile } };
  const b = { ...expected, nodal_profile: { ...expected.nodal_profile } };
  delete a.nodal_profile.pre_two_values_base64;
  delete b.nodal_profile.pre_two_values_base64;
  if (JSON.stringify(a) !== JSON.stringify(b)) throw Error("strategy differs from exact extraction");
}

function verifyExtraction(filenameOrBytes, strategy, options = {}) {
  const source = readSource(filenameOrBytes);
  const { expandField } = require("./qout_field_codec.cjs");
  const { verifyNormalizedDual } = require("./normalized_record_pricing.cjs");
  const target = BigInt(strategy.verified_lower_units);
  const pricing = verifyNormalizedDual(expandField(source.data), { ...options, targetUnits: target, witness: false });
  pricing.input_sha256 = source.input_sha256;
  const expected = makeStrategy(source.bytes, pricing, strategy.interpolation_epsilon);
  assertSameStrategy(strategy, expected);
  const ev = createEvaluator(strategy);
  return { status: "PASS", scope: "Independent exact BigInt full-bank target-bound pricing, exact Qout validation, and regenerated compact continuous Princess extraction.",
    input_sha256: source.input_sha256, n: strategy.n, stored_radial_nodes: ev.stored_radial_nodes,
    finite_dual_lower: strategy.finite_dual_lower, epsilon: strategy.interpolation_epsilon,
    exact_transfer_loss: strategy.exact_transfer_loss, guaranteed_security: strategy.guaranteed_security,
    validation: ev.validation, pricing };
}

module.exports = { Q, readSource, inspectProfile, makeStrategy, createEvaluator, verifyExtraction, assertSameStrategy };
if (require.main === module) {
  try {
    const [command, a, b, c, d] = process.argv.slice(2);
    if (command === "generate") {
      if (!a || !b || !c || !d) throw Error("usage: generate field.json exact_pricing_report.json epsilon strategy.json");
      const report = readSource(b).data, strategy = makeStrategy(a, report, c), ev = createEvaluator(strategy);
      const output = Buffer.from(JSON.stringify(strategy, null, 2) + "\n");
      fs.writeFileSync(d, d.endsWith(".gz") ? zlib.gzipSync(output) : output);
      process.stdout.write(JSON.stringify({ status: "PASS", scope: "Exact extraction from the supplied hash-bound pricing report; this command does not rerun pricing. Use verify for independent replay.",
        input_sha256: strategy.source_input_sha256, n: strategy.n, stored_radial_nodes: ev.stored_radial_nodes,
        finite_dual_lower: strategy.finite_dual_lower, epsilon: strategy.interpolation_epsilon,
        exact_transfer_loss: strategy.exact_transfer_loss, guaranteed_security: strategy.guaranteed_security,
        validation: ev.validation }, null, 2) + "\n");
    } else if (command === "verify") {
      if (!a || !b) throw Error("usage: verify field.json strategy.json");
      process.stdout.write(JSON.stringify(verifyExtraction(a, readSource(b).data), null, 2) + "\n");
    } else if (command === "cdf" || command === "radius") {
      if (!a || b === undefined || c === undefined) throw Error("usage: cdf strategy.json time position | radius strategy.json time rank");
      const ev = createEvaluator(readSource(a).data);
      const value = command === "cdf" ? ev.strictCDF(b, c) : ev.radiusAt(b, c);
      process.stdout.write(value.toString() + "\n");
    } else throw Error("commands: generate, verify, cdf, radius");
  } catch (error) { process.stderr.write(error.stack + "\n"); process.exitCode = 1; }
}
