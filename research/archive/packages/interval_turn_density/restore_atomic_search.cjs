"use strict";
// Discovery checkpoint restorer. It does not certify the unrestricted game.
// Usage: node restore_atomic_search.cjs atomic_search_checkpoint.json
const fs = require("fs");
const Engine = require("./atomic_survival_v8.cjs");
function checksum(r) {
  const b = new ArrayBuffer(8), v = new DataView(b);
  let h = 2166136261, k = 0x9e3779b9;
  for (const x of r) {
    v.setFloat64(0, x, true);
    for (let i = 0; i < 8; i++) {
      const z = v.getUint8(i);
      h = Math.imul(h ^ z, 16777619);
      k = Math.imul(k ^ z, 2246822519);
    }
  }
  return [(h >>> 0).toString(16), (k >>> 0).toString(16)];
}
function restore(data, engine = Engine) {
  const model = new engine.Rational.Model(data.atoms);
  if (JSON.stringify(model.v) !== JSON.stringify(data.modelCoordinates.v) ||
      JSON.stringify(model.base) !== JSON.stringify(data.modelCoordinates.base))
    throw Error("rational event coordinates differ");
  const archiveRows = data.archiveLabels.map((labels, i) => {
    const row = labels === null ? data.continuousResponses[i].numericCosts.slice() : model.row(labels);
    if (JSON.stringify(checksum(row)) !== JSON.stringify(data.archiveRowChecksums[i]))
      throw Error("stored dyadic payoff row mismatch at " + i);
    return row;
  });
  const rows = data.activeArchiveIndices.map(i => archiveRows[i]);
  return {model, archiveRows, rows, basis: {C: data.basis.C, R: data.basis.R},
          weights: data.currentWeights, incumbent: data.incumbent, data};
}
module.exports = {restore, checksum};
if (require.main === module) {
  const data = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const recovered = restore(data);
  console.log(JSON.stringify({
    status: "checkpoint rows reproduced",
    scope: data.scope,
    atoms: data.atoms.length,
    archiveRows: recovered.archiveRows.length,
    activeRows: recovered.rows.length,
    basisWasFeasible: data.basis.done,
    lastFiniteLevel: data.lastFiniteLevel,
    lastGlobalResponse: data.lastGlobalResponse
  }, null, 2));
}
