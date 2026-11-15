#!/usr/bin/env node
/** Exact common-warp replay and continuous M1/fixed-U1 M2 audit.
 * node verify_common_warp.mjs FIELD MATRIX SOLUTION [REPORT]
 * Exact integer/rational arithmetic; no unrestricted lower certificate.
 */
import fs from "node:fs";
import crypto from "node:crypto";
import {createRequire} from "node:module";
const require=createRequire(import.meta.url);
const E=require("./warp_exact_field_core.cjs");
const {createWarpTools}=require("./warp_capture_features.cjs");
const {createWarpFamilyAuditor}=require("./warp_family_audit.cjs");
if(process.argv.length<5)throw Error("Supply FIELD MATRIX SOLUTION [REPORT]");
const texts=process.argv.slice(2,5).map(p=>fs.readFileSync(p,"utf8"));
const [data,matrix,solution]=texts.map(JSON.parse),W=createWarpTools(E);
const field=new E.ExactField(data),warp=new W.WarpCoordinates(solution.knots),d=warp.validate(solution.increments),warped=W.remapExactField(field,warp,d);
if(JSON.stringify(matrix.knots)!==JSON.stringify(solution.knots))throw Error("knot mismatch");
let best=null,bestRow=-1;
for(let j=0;j<matrix.rows.length;j++){
 const row=matrix.rows[j],v=W.dot(row.numerators.map(n=>E.Q(n).dby(row.denominator)),d);
 if(!v.eq(E.Q(solution.all_exact_scores[j])))throw Error("row score mismatch "+j);
 if(best===null||v.cmp(best)<0){best=v;bestRow=j;}
}
if(!best.eq(E.Q(solution.minimum_exact)))throw Error("bank minimum mismatch");
let physical=0;for(const j of [0,1,54,429,466,467,468,475,482]){
 const row=matrix.rows[j];if(!row||row.waiting)continue;
 const v=warped.unitRoutePayoff(warp.route(row.route,d));
 if(!v.eq(E.Q(solution.all_exact_scores[j])))throw Error("physical replay "+j);physical++;
}
const A=createWarpFamilyAuditor(E),families=[];
for(const [family,positive] of [["m1",false],["m1",true],["fixed_one",false],["fixed_one",true]])families.push(A.minimum(warped,family,positive));
const report={scope:"Exact specified-family audit of a legal strict common warp; not an unrestricted lower certificate.",
 input_sha256:texts.map(t=>crypto.createHash("sha256").update(t).digest("hex")),
 nodes:warped.nodes.length,transport_triangles:warped.triangles.length,bank_rows:matrix.rows.length,
 bank_minimum:best.str(),bank_minimum_decimal:best.num(),bank_minimum_row:bestRow,independent_warp_replays:physical,families};
const output=JSON.stringify(report,null,2)+"\n";
if(process.argv[5])fs.writeFileSync(process.argv[5],output);process.stdout.write(output);
