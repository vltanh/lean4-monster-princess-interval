"use strict";

// Recompute the exact complete Princess response, then replay the generated
// feasible flow against a separately rebuilt graph. No numerical LP solver
// or discovery checkpoint is needed to verify this bound.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const E = require("../interval_turn_density/atomic_survival_v8.cjs");
const Q = E.Physical.Q;
const data = JSON.parse(fs.readFileSync(path.join(__dirname,
  "warped_order_upper_exact.json"), "utf8"));
const expected = "3737990218889184863163116789182923230981219/2621440000000000000000000000000000000000000";
const oldUpper = new Q("186901335715700435697848697352853/131072000000000000000000000000000");
const denominator = BigInt(data.weights_denominator);
assert(denominator > 0n);
let mass = 0n, baseline = new Q(0n);
let maxCompletion = new Q(0n), legs = 0;
for (const atom of data.atoms) {
  const weight = BigInt(atom.weight_numerator);
  assert(weight > 0n);
  mass += weight;
  const vertices = atom.exact_light.map(([u,v]) => [new Q(u),new Q(v)]);
  assert(vertices.length >= 2);
  assert.equal(String(vertices[0][0].add(vertices[0][1])), "0");
  const firstEndpoint = new Map();
  for (let k=0;k<vertices.length;k++) {
    const [u,v] = vertices[k], time=u.add(v).div(new Q(2n));
    const position=u.sub(v).div(new Q(2n));
    assert(time.cmp(new Q(0n)) >= 0);
    assert(position.abs().cmp(new Q(1n)) <= 0);
    if (k) {
      const [a,b]=vertices[k-1];
      assert((u.cmp(a)>0 && v.cmp(b)===0) ||
        (v.cmp(b)>0 && u.cmp(a)===0), "unit-speed physical leg");
      legs++;
    }
    if (position.abs().cmp(new Q(1n))===0 &&
      !firstEndpoint.has(String(position)))
      firstEndpoint.set(String(position),time);
  }
  assert(firstEndpoint.has("-1") && firstEndpoint.has("1"));
  const a=firstEndpoint.get("-1"), b=firstEndpoint.get("1");
  baseline=baseline.add(a.add(b).div(new Q(2n))
    .mul(new Q(weight,denominator)));
  for (const t of [a,b]) if (t.cmp(maxCompletion)>0) maxCompletion=t;
}
assert.equal(mass,denominator);
assert.equal(String(baseline),data.endpoint_baseline);
assert(maxCompletion.cmp(new Q(7n))<=0);

const model = new E.Rational.Model(data.atoms);
const numerators = data.atoms.map(a=>a.weight_numerator);
const result = E.Integer.solveIntegerLaw(E.Cut,E.Physical,E.BigFlow.BigFlow,
  model,numerators,data.weights_denominator);
assert.equal(result.exactValue,expected);
assert.equal(data.exact_value,expected);
assert.deepEqual(result.labels,data.minimum_labels);
assert.deepEqual(result.maxlabels,data.maximum_labels);
assert.deepEqual(result.certificate,data.expected_graph);
const replay = E.Integer.verifyIntegerFlow(E.Cut,E.Physical,E.BigFlow.BigFlow,
  model,numerators,data.weights_denominator,result.flowCertificate);
assert.equal(replay.exactValue,expected);
assert.equal(String(new Q(expected).sub(baseline)),data.deficiency);
assert(new Q(expected).cmp(oldUpper)<0);
console.log(JSON.stringify({scope:"exact unrestricted Princess upper certificate",
  exact_value:expected,decimal_value:new Q(expected).number(),
  improvement:String(oldUpper.sub(new Q(expected))),pairs:data.atoms.length,
  physical_unit_legs:legs,completion_horizon:String(maxCompletion),
  endpoint_baseline:String(baseline),deficiency:data.deficiency,
  graph_replay:replay,all_checks_passed:true},null,2));
