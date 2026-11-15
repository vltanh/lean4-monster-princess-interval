#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import {pathToFileURL} from "node:url";
import {createUpperWorker} from "./upper_oracle_worker.mjs";
export async function verifyUpperWorker(fixtures){
 const worker=await createUpperWorker();let checks=0;const cases=[];
 function check(x,msg){if(!x)throw Error(msg);checks++;}
 for(const f of fixtures){
  const r=await worker({atoms:f.atoms,weights:f.nums.map(x=>Number(x)/Number(f.den)),
   options:{exactCut:true,exactCollapsed:true,companionRows:true}});
  check(r.response.exact_value===f.result.value,"exact fixture response");
  check(r.rows.length>=2,"missing extremal physical rows");
  for(const row of r.rows){
   check(row.payoffs.length===f.atoms.length&&row.exact_payoffs.length===f.atoms.length,"full bank scoring dimensions");
   check(row.witness_validation.exact_equality,"physical recapture / own cut");
   check(row.witness_validation.maximizing_limit_witness,"not a maximizing witness");
   check(row.weighted_recapture.decimal<=r.response.value+1e-12,"physical row exceeds global cut");
   check(row.provenance.physical_rows_are_immutable===true,"missing frozen-path provenance");
  }
  cases.push({name:f.name,upper:r.response.exact_value,companion:r.collapsed_companion.response.value,
   physical_rows:r.rows.length,original_rows:r.rows.filter(x=>x.provenance.witness_law==="original-germ").length,
   companion_rows:r.rows.filter(x=>x.provenance.witness_law==="collapsed-ordinary").length});
 }
 const parserAtoms=[
  {kind:1,start:"-1"},{kind:2,start:"1/2"},
  {kind:"M1",parameters:["1/3"]},{kind:"M2",parameters:["1/2","1"]},
  {kind:"M3",parameters:["-1/8","7/8","1"]},
  {kind:"I",parameters:["3/4","-1/2","1"]},
  {kind:"I1",parameters:["3/4","-1/2"]},
  {kind:"E",parameters:["3/4","-1/2"]},
  {kind:"PATH",parameters:["-1","1","3","1"]},
  {route:[[0,0],[1,-1],[3,1]]}
 ];
 const parser=await worker({atoms:parserAtoms,weights:parserAtoms.map(()=>.1),
  options:{exactCut:true,exactCollapsed:true,profiles:[{profile:"minimum",fill:"avoided",strictMode:"clip"}]}});
 check(parser.complete,"ordinary format parser");
 check(parser.rows[0].payoffs.length===parserAtoms.length,"ordinary parser full row");
 check(parser.rows[0].witness_validation.exact_equality,"ordinary parser physical recapture");
 const endpoint=fixtures[0].atoms[0],g="germ:[[\"0\",\"0\",\"0\",\"0\",\"0\",\"1\"],[\"1\"]]",
  ng="germ:[[\"0\",\"0\",\"0\",\"0\",\"0\",\"-1\"],[\"1\"]]",
  two="germ:[[\"2\",\"0\",\"0\",\"0\",\"0\",\"1\"],[\"1\"]]",
  four="germ:[[\"4\",\"0\",\"0\",\"0\",\"0\",\"1\"],[\"1\"]]",
  attack={exact_light:[[g,ng],[g,two],[four,two]]},
  base=await worker({atoms:[endpoint],weights:[1],options:{collapsed:false}}),
  enlarged=await worker({atoms:[endpoint,attack],weights:[1,0],options:{collapsed:false}});
 check(base.response.value===enlarged.response.value,"zero-weight atom changed active response");
 check(base.rows.length===enlarged.rows.length,"inactive coordinate changed realized row count");
 for(let j=0;j<base.rows.length;j++){
  check(base.rows[j].id===enlarged.rows[j].id,"inactive atom changed physical row");
  check(base.rows[j].capture_germs[0]===enlarged.rows[j].capture_germs[0],"old physical payoff changed");
  check(enlarged.rows[j].payoffs.length===2,"new inactive atom not physically scored");
 }
 return{scope:"Native active-support worker, frozen physical witnesses, original-bank and companion separation.",
  exact_checks:checks,fixtures:cases,ordinary_formats:parserAtoms.length,
  parser_response:parser.response.exact_value,inactive_germ_geometry_test:{
   preserved_rows:base.rows.length,maximum_gap_order:enlarged.rows[0].provenance.scale.max_gap_order,
   full_bank_size:enlarged.bank_size,active_size:enlarged.active_indices.length}};
}
async function main(){
 const [input,output]=process.argv.slice(2);
 if(!input||!output)throw Error("usage: node verify_upper_oracle_worker.mjs GERM_FIXTURE_LABELS.json REPORT.json");
 const fixtures=JSON.parse(await fs.readFile(input,"utf8")),started=Date.now(),
  report=await verifyUpperWorker(fixtures);
 report.seconds=(Date.now()-started)/1000;
 await fs.writeFile(output,JSON.stringify(report,null,2)+"\n");console.log(JSON.stringify(report));
}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href)
 main().catch(e=>{console.error(e.stack||e);process.exitCode=1;});
