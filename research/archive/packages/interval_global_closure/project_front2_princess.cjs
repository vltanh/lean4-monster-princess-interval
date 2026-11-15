"use strict";
// Exact front projection of the independently certified n256 Princess law.
// The inherited lower follows from per-path atomic-record monotonicity, not
// a fresh search or an assertion that the new bank minimum is attained.
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const zlib = require("node:zlib");
const E = require("../interval_clock_grid/extract_normalized_princess.cjs");
const sha256 = b => crypto.createHash("sha256").update(b).digest("hex");
const jsonBytes = value => Buffer.from(JSON.stringify(value, null, 2) + "\n");
const FIELD_HASH = "81483589b60c14d823d2bb467015a321d77cf555076fe8d69a36d63cd829d7d5";
const STRATEGY_HASH = "d1432172efe4aca9c67394ae7c12fd5b553302e5c9e067d930cc343cb0db4086";

function projectProfile(input) {
  const p = E.inspectProfile(input), raw = Buffer.from(p.raw);
  let outside = 0, changed = 0, maximumDecrease = 0, totalDecrease = 0n;
  for (let j = 0; j <= p.C; j++) for (let k = 1; k <= p.R; k++) {
    if ((j+k)%2 || j+k <= p.C) continue;
    outside++;
    const uIndex = (p.C+j-k)/2, rIndex = (p.C-j+k)/2;
    if (!Number.isSafeInteger(uIndex) || !Number.isSafeInteger(rIndex)) {
      throw Error("non-grid front intersection");
    }
    const value = j-k >= p.C ? 0 : Number(p.node(uIndex, rIndex));
    const at = 4*(j*p.n+Math.floor((k-1)/2)), previous = raw.readUInt32LE(at);
    if (value > previous) throw Error("front projection increases radial CDF");
    raw.writeUInt32LE(value, at);
    if (value !== previous) changed++;
    maximumDecrease = Math.max(maximumDecrease, previous-value);
    totalDecrease += BigInt(previous-value);
  }
  const profile = {
    ...p.profile,
    encoding: { ...p.profile.encoding, uncompressed_sha256: sha256(raw) },
    pre_two_values_base64: zlib.deflateSync(raw, {level: 9}).toString("base64")
  };
  const q = E.inspectProfile(profile);
  let frontChecks = 0;
  for (let j = 0; j <= q.C; j++) for (let k = 1; k <= q.R; k++) {
    if ((j+k)%2 || j+k < q.C) continue;
    const expected = j-k >= q.C ? 0n : q.node((q.C+j-k)/2, (q.C-j+k)/2);
    if (q.node(j,k) !== expected) throw Error("front identity fails");
    frontChecks++;
  }
  // The original starting distribution must remain exactly the same.
  for (let k = 0; k <= p.R; k += 2) {
    if (p.node(0,k) !== q.node(0,k)) throw Error("initial distribution changed");
  }
  return {profile, raw, audit: {
    stored_nodes: p.count, nodes_strictly_beyond_front: outside,
    changed_nodes: changed, remaining_front_domain_nodes: p.count-outside,
    maximum_nodal_decrease_units: maximumDecrease,
    total_nodal_decrease_units: String(totalDecrease),
    exact_front_identities: frontChecks,
    transport_inequalities: q.coneChecks,
    sticky_endpoint_inequalities: q.endpointChecks
  }};
}

function sourceData(fieldPath, strategyPath) {
  const field = E.readSource(fieldPath), strategy = E.readSource(strategyPath);
  if (field.input_sha256 !== FIELD_HASH || strategy.input_sha256 !== STRATEGY_HASH) {
    throw Error("input differs from the independently certified frozen source");
  }
  E.createEvaluator(strategy.data);
  if (strategy.data.source_input_sha256 !== field.input_sha256 ||
      strategy.data.verified_lower_units !== String(field.data.minimum_units) ||
      strategy.data.finite_dual_lower !== field.data.normalized_bank_dual_value ||
      !E.inspectProfile(strategy.data.nodal_profile).raw.equals(E.inspectProfile(field.data).raw)) {
    throw Error("source strategy is not bound to the source field");
  }
  return {field, strategy};
}

function targetField(source, projection) {
  return {
    ...projection.profile,
    scope: "Exact incoming-front U=t+radius=2 projection of the certified n256 field. Every normalized-bank path's minimum causal-clock price weakly increases. The stated lower is inherited; no new exact minimum or attaining path is asserted.",
    incoming_front: "2",
    objective_denominator: source.strategy.data.objective_denominator,
    certified_bank_lower_units: source.strategy.data.verified_lower_units,
    normalized_bank_lower: source.strategy.data.finite_dual_lower,
    global_value_lower: source.field.data.global_lower,
    proof_source: {
      field_sha256: source.field.input_sha256,
      strategy_sha256: source.strategy.input_sha256,
      theorem: "research/12-global-closure/GLOBAL_INCOMING_FRONT_COMPLETION.md",
      method: "Exact legal nodal projection and per-path atomic-record monotonicity after the first center visit; the source lower has independent native and BigInt verification."
    }
  };
}

function inheritedReport(source, targetBytes, audit) {
  return {
    status: "PASS", qout_verified: true, n: source.strategy.data.n,
    input_sha256: sha256(targetBytes),
    verified_lower_units: source.strategy.data.verified_lower_units,
    objective_denominator: source.strategy.data.objective_denominator,
    normalized_bank_lower: source.strategy.data.finite_dual_lower,
    source_field_sha256: source.field.input_sha256,
    source_strategy_sha256: source.strategy.input_sha256,
    scope: "Analytically inherited bank lower under exact front projection. This is not a fresh exhaustive pricing run and does not claim equality with the new bank minimum.",
    projection: audit
  };
}

function metadataWithoutCompression(data) {
  const out = {...data}; delete out.pre_two_values_base64; return out;
}

function run(mode, fieldPath, strategyPath, targetFieldPath, targetStrategyPath, reportPath) {
  const source = sourceData(fieldPath, strategyPath);
  const projection = projectProfile(source.field.data);
  const expectedField = targetField(source, projection);
  let targetBytes;
  if (mode === "generate") {
    targetBytes = jsonBytes(expectedField);
    fs.writeFileSync(targetFieldPath, targetBytes);
  } else if (mode === "verify") {
    targetBytes = fs.readFileSync(targetFieldPath);
    const actual = JSON.parse(targetBytes.toString("utf8"));
    if (!E.inspectProfile(actual).raw.equals(projection.raw) ||
        JSON.stringify(metadataWithoutCompression(actual)) !==
        JSON.stringify(metadataWithoutCompression(expectedField))) {
      throw Error("saved field differs from exact source projection");
    }
  } else throw Error("mode must be generate or verify");
  const inherited = inheritedReport(source, targetBytes, projection.audit);
  const expectedStrategy = E.makeStrategy(targetBytes, inherited, source.strategy.data.interpolation_epsilon);
  if (mode === "generate") fs.writeFileSync(targetStrategyPath, jsonBytes(expectedStrategy));
  const actualStrategy = E.readSource(targetStrategyPath);
  E.assertSameStrategy(actualStrategy.data, expectedStrategy);
  if (actualStrategy.data.guaranteed_security !== source.strategy.data.guaranteed_security) {
    throw Error("explicit all-Monster guarantee changed");
  }
  const report = {
    ...inherited,
    projected_strategy_sha256: actualStrategy.input_sha256,
    incoming_front: "2",
    exact_interpolation_epsilon: actualStrategy.data.interpolation_epsilon,
    explicit_security: actualStrategy.data.guaranteed_security,
    global_value_lower: source.field.data.global_lower,
    no_new_pricing_search: true,
    no_claim_of_new_minimum_attainment: true
  };
  if (reportPath) fs.writeFileSync(reportPath, jsonBytes(report));
  return report;
}

module.exports = {projectProfile, run};
if (require.main === module) {
  try {
    const mode = process.argv[2] || "verify";
    const folder = __dirname, bank = path.join(folder, "../interval_clock_grid");
    const args = process.argv.slice(3);
    const defaults = [path.join(bank, "lower_n256_field.json"),
      path.join(bank, "lower_n256_princess.json"),
      path.join(folder, "lower_n256_front2_field.json"),
      path.join(folder, "lower_n256_front2_princess.json"),
      path.join(folder, "front2_princess_projection_replay.json")];
    if (args.length && args.length !== 5) throw Error("usage: [generate|verify] [source_field source_strategy target_field target_strategy report]");
    process.stdout.write(JSON.stringify(run(mode, ...(args.length ? args : defaults)), null, 2)+"\n");
  } catch (error) { process.stderr.write(error.stack+"\n"); process.exitCode = 1; }
}
