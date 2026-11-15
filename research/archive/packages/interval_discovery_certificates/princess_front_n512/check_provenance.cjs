"use strict";
// Bind the retained data to completed CI and reviewed proof/source bytes.
// This module never imports or invokes a response-pricing implementation.
const fs = require("node:fs"), path = require("node:path"), crypto = require("node:crypto");
const assert = require("node:assert/strict");
const sha = bytes => crypto.createHash("sha256").update(bytes).digest("hex");
const repositoryRoot = path.resolve(__dirname, "../../..");
const SOURCE_PATHS = [
  "packages/interval_clock_grid/normalized_native/price_normalized.cpp",
  "packages/interval_center_pricing/price_center.cpp",
  "packages/interval_center_pricing/verify_strategy.cjs",
  "packages/interval_clock_grid/extract_normalized_princess.cjs",
  "packages/interval_clock_grid/extract_princess.cjs",
  "packages/interval_clock_grid/record_pricing.cjs",
  "packages/interval_clock_grid/exact_certificate.cjs"
];
const PROOF_PATHS = [
  "research/12-global-closure/EFFECTIVE_FINITE_UPPER_REDUCTION.md",
  "research/12-global-closure/CONSTRUCTIVE_PRINCESS_GRID_DUAL.md",
  "research/12-global-closure/NORMALIZED_GRID_BANK_PRICING.md",
  "research/12-global-closure/LEFT_FLOOR_CLOCK_ATOMIZATION.md",
  "research/12-global-closure/GLOBAL_INCOMING_FRONT_COMPLETION.md",
  "research/12-global-closure/CENTER_HEAVIER_FIRST_BALANCE.md",
  "research/12-global-closure/DISCRETE_CENTER_BALANCE_PRICING.md",
  "research/12-global-closure/FULL_WIDTH_INTERPOLATION_REFINEMENT.md",
  "packages/interval_clock_grid/PURSUIT_PRUNING.md"
];
function bindTable(table, required, label) {
  assert.deepEqual(Object.keys(table).sort(), [...required].sort(), label + " completeness");
  for (const name of required) assert.equal(sha(fs.readFileSync(path.join(repositoryRoot, name))), table[name], label + ": " + name);
}

function checkProvenance(folder, manifest, bytes, data) {
  const entry = manifest.provenance;
  assert.equal(entry.file, "provenance.json");
  const raw = fs.readFileSync(path.join(folder, entry.file));
  assert.equal(raw.length, entry.bytes, "provenance length");
  assert.equal(sha(raw), entry.sha256, "provenance hash");
  const p = JSON.parse(raw);
  assert.equal(p.format, "retained-front-refinement-provenance-v1");
  bindTable(p.repository_sources, SOURCE_PATHS, "reviewed implementation");
  bindTable(p.proof_sources, PROOF_PATHS, "reviewed proof");
  const historical = p.historical_verifier;
  assert.equal(historical.path, "provenance/verify_bigint_4503f3e.cjs");
  assert.equal(historical.repository_path, "packages/interval_center_pricing/verify_bigint.cjs");
  assert.equal(historical.commit, manifest.independent_replay.commit);
  const code = fs.readFileSync(path.join(folder, historical.path));
  assert.equal(code.length, historical.bytes, "historical verifier length");
  assert.equal(sha(code), historical.sha256, "historical verifier bytes");
  assert.equal(historical.sha256, data["independent.replay.json"].verifier_source_sha256, "completed independent replay source");
  assert.equal(p.repository_sources[SOURCE_PATHS[0]], data["original.replay.json"].verifier_source_sha256, "completed original replay source");
  assert.equal(p.repository_sources[SOURCE_PATHS[1]], data["center.replay.json"].verifier_source_sha256, "completed center replay source");
  assert.equal(p.repository_sources[SOURCE_PATHS[3]], manifest.independent_replay.extractor_source_sha256, "completed extraction source");

  assert.equal(p.actions.format, "front-refinement-actions-provenance-v1");
  assert.equal(p.actions.repository, "vltanh/lean4-monster-princess");
  for (const [name, manifestKey, jobId, criticalSteps] of [
    ["discovery", "discovery", 132294619792, ["Exactly refine the globally sufficient front geometry and price every response"]],
    ["independent", "independent_replay", 132300097087,
      ["Independently check every normalized-bank response with BigInt costs", "Extract an explicit continuous Princess guarantee from the replay"]]
  ]) {
    const a = p.actions[name], m = manifest[manifestKey];
    assert.equal(a.job.id, jobId, name + " successful job");
    if (m.job_id !== undefined) assert.equal(a.job.id, m.job_id, name + " manifest job binding");
    assert.equal(a.job.run_id, m.run_id, name + " run");
    assert.equal(a.job.status, "completed", name + " completed");
    assert.equal(a.job.conclusion, "success", name + " success");
    for (const step of criticalSteps) assert.equal(a.job.steps.find(s => s.name === step)?.conclusion, "success", name + " critical step");
    assert.equal(a.artifact.id, m.artifact_id, name + " artifact ID");
    assert.equal(a.artifact.workflow_run.id, m.run_id, name + " artifact run");
    assert.equal(a.artifact.workflow_run.head_sha, m.commit, name + " artifact commit");
    assert.equal(a.artifact.digest, "sha256:" + m.artifact_zip_sha256, name + " archive digest");
    assert.equal(a.artifact.size_in_bytes, m.artifact_zip_bytes, name + " archive length");
  }
  assert.equal(p.archive.format, "front-refinement-artifact-members-v1");
  assert.equal(p.archive.artifact_id, manifest.independent_replay.artifact_id);
  assert.equal(p.archive.archive_sha256, manifest.independent_replay.artifact_zip_sha256);
  assert.equal(p.archive.archive_bytes, manifest.independent_replay.artifact_zip_bytes);

  const texts = p.artifact_texts;
  assert.deepEqual(Object.keys(texts).sort(), ["commit.txt", "node-version.txt", "source/manifest.json", "sources.sha256"]);
  assert.equal(texts["commit.txt"].trim(), manifest.independent_replay.commit, "original CI commit");
  assert.equal(texts["node-version.txt"].trim(), manifest.independent_replay.node_version, "original CI runtime");
  const sourceLines = {};
  for (const line of texts["sources.sha256"].trim().split("\n")) {
    const match = /^([0-9a-f]{64})  (.+)$/.exec(line);
    assert(match, "malformed original source line");
    assert(!Object.hasOwn(sourceLines, match[2]), "duplicate original source line");
    sourceLines[match[2]] = match[1];
  }
  assert.deepEqual(sourceLines, {
    "packages/interval_center_pricing/verify_bigint.cjs": historical.sha256,
    "packages/interval_clock_grid/extract_normalized_princess.cjs": p.repository_sources[SOURCE_PATHS[3]]
  }, "byte-preserved completed CI source hashes");
  const originalManifest = JSON.parse(texts["source/manifest.json"]);
  assert.equal(originalManifest.status, "COMPLETE_EXACT_CENTER_PRICING");
  assert.equal(originalManifest.source_n, manifest.discovery.source_n);
  assert.equal(originalManifest.target_n, manifest.n);
  assert.equal(originalManifest.global_value_lower, manifest.game_value_lower);
  assert.equal(originalManifest.source_seed_sha256, manifest.discovery.source_seed_sha256);
  assert.equal(originalManifest.exact_fullwidth_refinement, true);
  assert.equal(originalManifest.independent_original_replay, true);
  assert.equal(originalManifest.independent_bigint_replay, false, "preserve historical pre-BigInt stage");
  assert.equal(originalManifest.same_cdf_security_claimed, false, "retain distinct transfer scopes");

  // Reconstruct the prepared bytes exactly, retaining the original compact
  // serialization while avoiding a second half-megabyte copy of the field.
  const dropKeys = ["minimum_units", "objective_denominator", "normalized_bank_dual_value", "global_lower", "global_lower_decimal", "native_source_sha256", "center_policy"];
  assert.deepEqual(p.prepared_field_reconstruction.drop_keys, dropKeys);
  assert.equal(p.prepared_field_reconstruction.serialization, "JSON.stringify without indentation, followed by one LF");
  const prepared = { ...data["field.json"] };
  for (const key of dropKeys) { assert(Object.hasOwn(prepared, key)); delete prepared[key]; }
  const preparedBytes = Buffer.from(JSON.stringify(prepared) + "\n");
  const reconstructed = { "source/prepared.field.json": preparedBytes };
  for (const [name, text] of Object.entries(texts)) reconstructed[name] = Buffer.from(text);
  for (const [name, file] of Object.entries(manifest.files)) {
    assert(!Object.hasOwn(reconstructed, file.artifact_member), "duplicate artifact member mapping");
    reconstructed[file.artifact_member] = bytes[name];
  }
  const members = p.archive.members;
  assert.equal(members.length, 11, "all independent artifact members");
  assert.deepEqual(members.map(m => m.artifact_path).sort(), Object.keys(reconstructed).sort(), "all artifact bytes recoverable");
  for (const member of members) {
    assert.equal(reconstructed[member.artifact_path].length, member.bytes, "artifact member length: " + member.artifact_path);
    assert.equal(sha(reconstructed[member.artifact_path]), member.sha256, "artifact member bytes: " + member.artifact_path);
  }
  const originalFiles = { "original.replay.json": bytes["original.replay.json"], "field.json": bytes["field.json"],
    "center.replay.json": bytes["center.replay.json"], "prepared.field.json": preparedBytes };
  assert.deepEqual(Object.keys(originalManifest.files_sha256).sort(), Object.keys(originalFiles).sort());
  for (const [name, rawFile] of Object.entries(originalFiles)) assert.equal(sha(rawFile), originalManifest.files_sha256[name], "original discovery binding: " + name);
  return { repository_source_commitments: SOURCE_PATHS.length, proof_source_commitments: PROOF_PATHS.length,
    historical_verifier_retained: true, selected_successful_ci_jobs: 2, exact_artifact_members_recoverable: members.length,
    prepared_field_reconstructed_byte_exact: true, archive_zip_digest_recomputed: false };
}
module.exports = { checkProvenance };
