"use strict";
const fs=require("node:fs"),os=require("node:os"),path=require("node:path"),zlib=require("node:zlib"),crypto=require("node:crypto"),assert=require("node:assert/strict");
const {verify}=require("./verify_bigint.cjs"),{verifyStrategy}=require("./verify_strategy.cjs");
const {makeStrategy}=require("../interval_clock_grid/extract_normalized_princess.cjs");
const sha=raw=>crypto.createHash("sha256").update(raw).digest("hex");
const folder=fs.mkdtempSync(path.join(os.tmpdir(),"compact-strategy-"));
try{
 const raw=Buffer.alloc(20),field={format:"qout-clock-grid-field-u32-zlib-v1",n:1,field_denominator:"17",normalized_profile:true,
  encoding:{count:5,integer_type:"uint32 little-endian",compression:"zlib",uncompressed_sha256:sha(raw)},
  pre_two_values_base64:zlib.deflateSync(raw).toString("base64"),minimum_units:"68"};
 const fieldPath=path.join(folder,"field.json"),strategyPath=path.join(folder,"strategy.json");
 const bytes=Buffer.from(JSON.stringify(field)+"\n");fs.writeFileSync(fieldPath,bytes);
 const report=verify(field);report.input_sha256=sha(bytes);
 const strategy=makeStrategy(bytes,report,"1/4");fs.writeFileSync(strategyPath,JSON.stringify(strategy));
 const checked=verifyStrategy(fieldPath,strategyPath);
 assert.equal(checked.guaranteed_security,"3/8");assert.equal(checked.pricing.global_lower,"1/2");
 let rejected=0;
 for(const mutation of [s=>s.guaranteed_security="1",s=>s.source_input_sha256="0".repeat(64),s=>s.verified_lower_units="69",s=>s.quantile_rule="changed",s=>s.interpolation_epsilon="0"]){
  const broken=structuredClone(strategy);mutation(broken);fs.writeFileSync(strategyPath,JSON.stringify(broken));
  assert.throws(()=>verifyStrategy(fieldPath,strategyPath));rejected++;
 }
 console.log(JSON.stringify({status:"PASS",exact_strategy_regenerations:1,corrupted_guarantee_source_target_rule_or_width_rejections:rejected,scope:"Integration of independent bank replay and existing exact strategy extraction; no new bound."},null,2));
}finally{fs.rmSync(folder,{recursive:true,force:true});}
