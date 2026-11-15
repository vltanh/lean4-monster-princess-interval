"use strict";
// Cheap extraction replay against an ALREADY completed exact pricing report.
// This does not rerun or replace the independent whole-bank BigInt pricing.
const fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const ex = require("./extract_normalized_princess.cjs");
const hash = bytes => crypto.createHash("sha256").update(bytes).digest("hex");

function verifyReportedExtraction(sourceFile, pricingFile, strategyFile) {
  const source = ex.readSource(sourceFile), pricing = ex.readSource(pricingFile), saved = ex.readSource(strategyFile);
  const report = pricing.data, strategy = saved.data;
  const expected = ex.makeStrategy(source.bytes, report, strategy.interpolation_epsilon);
  ex.assertSameStrategy(strategy, expected);
  const ev = ex.createEvaluator(strategy), p = ex.inspectProfile(strategy.nodal_profile), { n, D } = p;
  let nodes = 0, quantiles = 0, speeds = 0, symmetry = 0, outward = 0;
  const times = Array.from(new Set([0, 1, n-1, n, 2*n-1, 2*n, 3*n-1, 3*n, 4*n-1, 4*n, 4*n+1, 6*n, 16*n]));
  for (const j of times) for (const k of Array.from(new Set([j%2, j%2+2, n-2+j%2, 2*n-2+j%2]))) {
    if (k < 0 || k > 2*n || (j+k)%2) continue;
    const value = p.node(j, k), t = new ex.Q(BigInt(j), BigInt(2*n)), r = new ex.Q(BigInt(k), BigInt(2*n));
    if (ev.rawTrace(t, r).cmp(new ex.Q(D + value, 2n*D))) throw Error("selected exact node");
    nodes++;
  }
  const samples = [], dt = new ex.Q(1n, BigInt(4*n));
  for (const t of ["0", "1/2", "1", "3/2", "2", "5/2", "3"]) {
    const radii = [];
    for (const u of ["0", "1/4", "1/2", "3/4", "99/100"]) {
      const r = ev.radiusAt(t, u), next = ev.radiusAt(ex.Q.of(t).add(dt), u), delta = next.sub(r);
      if (delta.cmp(dt) > 0 || delta.cmp(dt.mul(-1)) < 0) throw Error("selected quantile speed");
      speeds++;
      if (r.cmp(1) < 0 && ev.radialCDF(t, r).cmp(u)) throw Error("selected exact quantile inverse");
      if (r.cmp(1) === 0 && ev.interiorTrace(t, 1).mul(2).sub(1).cmp(u) > 0) throw Error("selected endpoint quantile");
      if (ev.positionAt(t, u, -1).cmp(r.mul(-1))) throw Error("quantile sign");
      quantiles++; radii.push([u, r.toString()]);
    }
    samples.push({ t, radial_quantiles: radii });
    for (const x of ["-1", "-3/4", "-1/3", "0", "1/3", "3/4", "1"]) {
      if (ev.interiorTrace(t, x).add(ev.interiorTrace(t, ex.Q.of(x).mul(-1))).cmp(1)) throw Error("reflection");
      symmetry++;
    }
  }
  for (const t of ["2", "9/4", "5/2"]) for (const r of ["1/4", "1/2", "3/4"]) {
    if (ev.interiorTrace(t, r).cmp(ev.interiorTrace(ex.Q.of(t).add("1/16"), ex.Q.of(r).add("1/16")))) throw Error("selected outward identity");
    outward++;
  }
  if (ev.strictCDF(0, -1).cmp(0) || ev.strictCDF(0, "1001/1000").cmp(1)) throw Error("strict endpoint convention");
  return {
    status: "PASS",
    scope: "Exact compact Princess extraction from the separately completed independent BigInt target-bound replay; this step validates decoded-buffer equality, guarantee arithmetic, and selected exact CDF/quantile evaluations without repeating the large pricing run.",
    input_sha256: source.input_sha256, n, stored_radial_nodes: ev.stored_radial_nodes,
    finite_dual_lower: strategy.finite_dual_lower, epsilon: strategy.interpolation_epsilon,
    exact_transfer_loss: strategy.exact_transfer_loss, guaranteed_security: strategy.guaranteed_security,
    validation: ev.validation,
    hashes: { source_sha256: hash(source.bytes), pricing_report_sha256: hash(pricing.bytes), strategy_sha256: hash(saved.bytes) },
    extractor_source_sha256: hash(fs.readFileSync(path.join(__dirname, "extract_normalized_princess.cjs"))),
    pricing_replayed_in_this_step: false,
    pricing_evidence: { status: report.status, verification_mode: report.verification_mode,
      attainment_checked: report.attainment_checked, qout_verified: report.qout_verified,
      verified_lower_units: report.verified_lower_units, objective_denominator: report.objective_denominator,
      record_states: report.record_states },
    checks: { literal_decoded_buffer_equality: true, exact_guarantee_arithmetic: true,
      selected_exact_nodes: nodes, selected_quantile_inversions: quantiles, selected_quantile_speed_checks: speeds,
      selected_symmetry_checks: symmetry, selected_outward_checks: outward, strict_endpoint_convention: true },
    selected_quantiles: samples
  };
}
module.exports = { verifyReportedExtraction };
if (require.main === module) {
  try {
    const [source, report, strategy, output] = process.argv.slice(2);
    if (!source || !report || !strategy) throw Error("usage: node verify_normalized_princess_report.cjs field.json exact_pricing_report.json strategy.json [output.json]");
    const result = JSON.stringify(verifyReportedExtraction(source, report, strategy), null, 2) + "\n";
    if (output) fs.writeFileSync(output, result);
    process.stdout.write(result);
  } catch (error) { process.stderr.write(error.stack + "\n"); process.exitCode = 1; }
}
