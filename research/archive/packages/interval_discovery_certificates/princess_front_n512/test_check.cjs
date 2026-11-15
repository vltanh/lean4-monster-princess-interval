"use strict";
// Regression for receipt/source/transfer rejection. No response search runs.
const fs = require("node:fs"), path = require("node:path"), os = require("node:os");
const crypto = require("node:crypto"), assert = require("node:assert/strict"), Module = require("node:module");
const sha = b => crypto.createHash("sha256").update(b).digest("hex");
const json = (directory, name) => JSON.parse(fs.readFileSync(path.join(directory, name)));
const write = (directory, name, value) => fs.writeFileSync(path.join(directory, name), JSON.stringify(value, null, 2) + "\n");
function changeProvenance(directory, mutation) {
  const p = json(directory, "provenance.json"); mutation(p); write(directory, "provenance.json", p);
  const b = fs.readFileSync(path.join(directory, "provenance.json")), m = json(directory, "manifest.json");
  m.provenance.bytes = b.length; m.provenance.sha256 = sha(b); write(directory, "manifest.json", m);
}
function changeCommittedFile(directory, name, mutation) {
  const value = json(directory, name); mutation(value); write(directory, name, value);
  const b = fs.readFileSync(path.join(directory, name)), m = json(directory, "manifest.json");
  m.files[name].bytes = b.length; m.files[name].sha256 = sha(b); write(directory, "manifest.json", m);
}
function doTests(check) {
  const baseline = check(), rejected = [];
  assert.equal(baseline.full_bank_search_replayed, false);
  const mutations = [
    ["field byte change", d => fs.appendFileSync(path.join(d, "field.json"), " ")],
    ["report input retargeted with updated outer hash", d => changeCommittedFile(d, "independent.replay.json", x => x.input_sha256 = "0".repeat(64))],
    ["Princess guarantee altered with updated outer hash", d => changeCommittedFile(d, "princess.json", x => x.guaranteed_security = "3/2")],
    ["game transfer halved", d => { const m = json(d, "manifest.json"); m.game_value_transfer_loss = "1/2048"; write(d, "manifest.json", m); }],
    ["positive-width allowance omitted", d => { const m = json(d, "manifest.json"); m.explicit_princess_transfer_loss = m.game_value_transfer_loss; write(d, "manifest.json", m); }],
    ["completed CI job relabeled", d => { const m = json(d, "manifest.json"); m.independent_replay.job_id += 1; write(d, "manifest.json", m); }],
    ["critical CI step failed", d => changeProvenance(d, p => p.actions.independent.job.steps.find(s => s.name.startsWith("Independently check")).conclusion = "failure")],
    ["proof commitment removed", d => changeProvenance(d, p => delete p.proof_sources[Object.keys(p.proof_sources)[0]])],
    ["proof bytes mismatched", d => changeProvenance(d, p => p.proof_sources[Object.keys(p.proof_sources)[0]] = "0".repeat(64))],
    ["prepared-field reconstruction changed", d => changeProvenance(d, p => p.prepared_field_reconstruction.drop_keys.pop())],
    ["historical verifier bytes changed", d => fs.appendFileSync(path.join(d, "provenance/verify_bigint_4503f3e.cjs"), "\n")]
  ];
  for (const [name, mutate] of mutations) {
    const directory = fs.mkdtempSync(path.join(os.tmpdir(), "front-lower-packet-"));
    try {
      fs.cpSync(__dirname, directory, { recursive: true });
      mutate(directory);
      let error;
      try { check(directory); } catch (e) { error = e; }
      assert(error, "tampered packet accepted: " + name);
      rejected.push(name);
    } finally { fs.rmSync(directory, { recursive: true, force: true }); }
  }
  return { status: "PASS", scope: "Cheap retained-packet rejection regressions; complete-bank pricer imports are forbidden during this test.",
    full_bank_search_replayed: false, valid_packet_passed: true, rejected_mutations: rejected,
    original_field_sha256: baseline.field_sha256, explicit_princess_security: baseline.explicit_princess_security };
}
function runTests() {
  const originalLoad = Module._load;
  Module._load = function(request, parent, isMain) {
    if (/verify_bigint|verify_strategy|normalized_record_pricing/.test(request))
      throw Error("retention check attempted to import a complete-bank pricer");
    return originalLoad.call(this, request, parent, isMain);
  };
  try { return doTests(require("./check.cjs").check); }
  finally { Module._load = originalLoad; }
}
module.exports = { runTests };
if (require.main === module) {
  try { process.stdout.write(JSON.stringify(runTests(), null, 2) + "\n"); }
  catch (error) { process.stderr.write(error.stack + "\n"); process.exitCode = 1; }
}
