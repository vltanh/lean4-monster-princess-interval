"use strict";
// Cheap retention check only. The completed CI reports contain the all-bank
// searches; this script checks their exact bindings and regenerates the law.
const fs = require("node:fs");
const path = require("node:path");
const crypto = require("node:crypto");
const assert = require("node:assert/strict");
const extractorPath = path.resolve(__dirname, "../../interval_clock_grid/extract_normalized_princess.cjs");
const { Q, makeStrategy, assertSameStrategy, createEvaluator, inspectProfile } = require(extractorPath);
const { checkProvenance } = require("./check_provenance.cjs");
const sha = b => crypto.createHash("sha256").update(b).digest("hex");
const equalQ = (a, b, label) => assert.equal(Q.of(a).cmp(Q.of(b)), 0, label);

function check(folder = __dirname) {
  const read = name => fs.readFileSync(path.join(folder, name));
  const manifest = JSON.parse(read("manifest.json"));
  assert.equal(manifest.format, "retained-normalized-princess-certificate-v1");
  const required = ["field.json", "princess.json", "original.replay.json",
    "center.replay.json", "independent.replay.json", "extraction.replay.json"];
  assert.deepEqual(Object.keys(manifest.files).sort(), [...required].sort());
  const bytes = {}, data = {};
  for (const name of required) {
    bytes[name] = read(name);
    assert.equal(bytes[name].length, manifest.files[name].bytes, `${name} length`);
    assert.equal(sha(bytes[name]), manifest.files[name].sha256, `${name} SHA-256`);
    data[name] = JSON.parse(bytes[name]);
  }
  const field = data["field.json"], original = data["original.replay.json"];
  const center = data["center.replay.json"], independent = data["independent.replay.json"];
  const extraction = data["extraction.replay.json"], princess = data["princess.json"];
  const provenance = checkProvenance(folder, manifest, bytes, data);
  const inputHash = manifest.files["field.json"].sha256;
  assert.equal(manifest.n, 512);
  assert.equal(field.n, manifest.n);
  assert.equal(field.field_denominator, manifest.field_denominator);
  assert.equal(field.source_seed_sha256, manifest.discovery.source_seed_sha256);
  assert.equal(field.exact_fullwidth_refinement, true);
  assert.equal(field.minimum_units, manifest.verified_lower_units);
  assert.equal(field.objective_denominator, manifest.objective_denominator);
  const denominator = 4n * BigInt(field.n) * BigInt(field.field_denominator);
  assert.equal(denominator.toString(), manifest.objective_denominator);
  const bank = new Q(manifest.verified_lower_units, denominator);
  const gameLoss = new Q(1n, 2n * BigInt(field.n));
  const epsilon = Q.of(manifest.interpolation_epsilon);
  const explicitLoss = Q.of(1).add(epsilon).mul(gameLoss);
  equalQ(bank, manifest.normalized_bank_lower, "bank arithmetic");
  equalQ(gameLoss, manifest.game_value_transfer_loss, "game transfer");
  equalQ(bank.sub(gameLoss), manifest.game_value_lower, "game lower");
  equalQ(explicitLoss, manifest.explicit_princess_transfer_loss, "explicit transfer");
  equalQ(bank.sub(explicitLoss), manifest.explicit_princess_security, "explicit security");
  equalQ(field.normalized_bank_dual_value, bank, "field bank");
  equalQ(field.global_lower, manifest.game_value_lower, "field game lower");

  for (const report of [original, center]) {
    assert.equal(report.input_sha256, inputHash);
    assert.equal(report.pricing.status, "PASS");
    assert.equal(report.pricing.n, field.n);
    assert.equal(report.pricing.field_denominator, field.field_denominator);
    assert.equal(report.pricing.minimum_units, manifest.verified_lower_units);
    assert.equal(report.pricing.objective_denominator, manifest.objective_denominator);
  }
  assert.equal(original.verifier_source_sha256, manifest.discovery.original_verifier_source_sha256);
  assert.equal(center.verifier_source_sha256, manifest.discovery.center_verifier_source_sha256);
  assert.equal(center.status, "PASS");
  assert.equal(center.pricing.center_policy, 4);
  equalQ(center.exact_bank_dual, bank, "center bank");
  equalQ(center.global_value_lower, manifest.game_value_lower, "center game lower");
  assert.equal(independent.status, "PASS");
  assert.equal(independent.input_sha256, inputHash);
  assert.equal(independent.verifier_source_sha256, manifest.independent_replay.verifier_source_sha256);
  assert.equal(independent.n, field.n);
  assert.equal(independent.verified_lower_units, manifest.verified_lower_units);
  assert.equal(independent.objective_denominator, manifest.objective_denominator);
  assert.equal(independent.verification_mode, "target lower bound");
  assert.equal(independent.cost_arithmetic, "BigInt throughout");
  assert.equal(independent.qout_verified, true);
  assert.equal(independent.sticky_verified, true);
  assert.equal(independent.incoming_front_verified, true);
  assert.equal(independent.center_policy, 4);
  assert.equal(independent.attainment_checked, true);
  assert.equal(original.pricing.retained_states, 2609003114);
  assert.equal(center.pricing.retained_states, 508713709);
  equalQ(independent.normalized_bank_lower, bank, "independent bank");
  equalQ(independent.global_lower, manifest.game_value_lower, "independent game lower");
  for (const name of ["record_states", "generated_transitions", "elapsed_ms"])
    assert.equal(independent[name], manifest.independent_replay[name], name);

  assert.equal(sha(fs.readFileSync(extractorPath)), manifest.independent_replay.extractor_source_sha256);
  // makeStrategy validates every pre-time-two transport inequality; its
  // outward continuation is explicit. It does not invoke response pricing.
  const regenerated = makeStrategy(bytes["field.json"], independent, manifest.interpolation_epsilon);
  assertSameStrategy(princess, regenerated);
  const evaluator = createEvaluator(princess);
  // Recheck the finite incoming-front identities directly; this is a nodal
  // equality scan, not a response search. Qout supplies all post-two values.
  const profile = inspectProfile(field), n = field.n;
  let incomingFrontChecks = 0;
  for (let j = 0; j <= 4 * n; j++) for (let k = j % 2; k <= 2 * n; k += 2) {
    if (j + k <= 4 * n) continue;
    const shift = (j + k - 4 * n) / 2, radius = k - shift;
    assert.equal(profile.node(j, k), radius <= 0 ? 0n : profile.node(j - shift, radius), "incoming-front identity");
    incomingFrontChecks++;
  }
  assert.equal(incomingFrontChecks, n * n, "complete pre-two incoming-front coverage");
  assert.equal(extraction.status, "PASS");
  assert.equal(extraction.input_sha256, inputHash);
  assert.equal(extraction.n, field.n);
  assert.equal(extraction.stored_radial_nodes, evaluator.stored_radial_nodes);
  assert.deepEqual(extraction.validation, evaluator.validation);
  equalQ(extraction.finite_dual_lower, bank, "extraction bank");
  equalQ(extraction.epsilon, epsilon, "extraction epsilon");
  equalQ(extraction.exact_transfer_loss, explicitLoss, "extraction transfer");
  equalQ(extraction.guaranteed_security, manifest.explicit_princess_security, "extraction security");
  return {
    status: "PASS",
    scope: "Cheap retention check: reviewed source/proof bytes, completed CI report and artifact-member bindings, exact rational arithmetic, complete nodal transport/front validation, and regenerated Princess strategy. No all-bank search is rerun.",
    full_bank_search_replayed: false,
    archive_zip_digests_rechecked: false,
    saved_ci_reports_rebound: true,
    strategy_regenerated_and_matched: true,
    field_sha256: inputHash,
    princess_sha256: manifest.files["princess.json"].sha256,
    independent_report_sha256: manifest.files["independent.replay.json"].sha256,
    historical_independent_verifier_sha256: independent.verifier_source_sha256,
    n: field.n,
    normalized_bank_lower: bank.toString(),
    game_value_lower: manifest.game_value_lower,
    explicit_princess_security: princess.guaranteed_security,
    validation: { ...evaluator.validation, incoming_front_identities: incomingFrontChecks },
    provenance
  };
}

module.exports = { check };
if (require.main === module) {
  try { process.stdout.write(JSON.stringify(check(), null, 2) + "\n"); }
  catch (error) { process.stderr.write(error.stack + "\n"); process.exitCode = 1; }
}
