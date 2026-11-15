import fs from "node:fs/promises";
import {createHash} from "node:crypto";
import {pathToFileURL} from "node:url";
import {createFrozenSeparator} from "./separate_frozen_law.mjs";
import fanModule from "./germ_translation_fan.cjs";

const sha=s=>createHash("sha256").update(s).digest("hex");
const pause=()=>new Promise(resolve=>setImmediate(resolve));
export async function trialTranslationFans(rows,master,oldMaster,seed,{onProgress=()=>{}}={}){
 const worker=createFrozenSeparator(rows),{G,F,paths,ids}=worker,Q=G.Q,Z=G.ZERO,O=G.ONE,e=G.eps,
  T=fanModule.createTranslationFan(G),index=new Map(ids.map((id,i)=>[id,i]));
 const vectors={current:master.princess_weights.map(String),clipped159:rows.map(()=>"0"),certified169:rows.map(()=>"0")};
 oldMaster.princess_mixture.forEach((r,i)=>{const j=index.get("clipped159:"+i);if(j===undefined)throw Error("missing old frozen row");vectors.clipped159[j]=String(r.weight);});
 seed.weights_h.forEach((w,i)=>{const j=index.get("certified169:"+i);if(j===undefined)throw Error("missing certified row");vectors.certified169[j]=String(w);});
 const weights=Object.fromEntries(Object.entries(vectors).map(([name,v])=>{const a=v.map(Q),sum=a.reduce((x,y)=>x.a(y),Z);if(sum.cmp(0)<=0)throw Error("zero mixture");return[name,a.map(x=>x.dby(sum))];}));
 const inward=a=>[[Z,a],[O.a(a),Q(-1)],[Q(3).a(a),O]],
  positiveM2=(a,s=O)=>[[Z,a],[s.s(a).dby(2),s.a(a).dby(2)],[s.a(1),Q(-1)],[s.a(3),O]],
  negativeM2=(a,s)=>positiveM2(a.neg(),s),
  first=Q("15/16").s(e),second=Q("3/16").s(e),
  fixed=[
   {id:"m1-inward-15/16-eps",route:inward(first)},
   {id:"m1-inward-7/8",route:inward(Q("7/8"))},
   {id:"m1-inward-119/128",route:inward(Q("119/128"))},
   {id:"m1-inward-29/32+eps2",route:inward(Q("29/32").a(e.pow(2)))},
   {id:"m2-positive-3/16-eps-U1",route:positiveM2(second)},
   {id:"m2-negative-3/5-U65/64",route:negativeM2(Q("3/5"),Q("65/64"))},
  ];
 const mixtures=Object.entries(weights),serial=r=>r.map(v=>v.map(x=>Q(x).str())),baseline=[];
 // Preserve a literal column for every frozen row, including zero-weight rows.
 const used=rows.map(()=>true),rawCosts=new Map();
 for(const c of fixed){
  const m=F.prepareMonster(c.route),sum=Object.fromEntries(mixtures.map(([name])=>[name,Z])),pure=[];
  for(let i=0;i<rows.length;i++){
   if(!used[i]){pure.push(null);continue;}
   const s=F.pairScore(paths[i],m,{fullCost:true});if(!s.complete)throw Error("baseline incomplete");const cost=Q(s.exact_cost);pure.push(s.exact_cost);
   for(const[name,w]of mixtures)if(!w[i].eq(0))sum[name]=sum[name].a(cost.m(w[i]));
  }
  rawCosts.set(c.id,pure);baseline.push({id:c.id,route:serial(c.route),mixtures:Object.fromEntries(Object.entries(sum).map(([name,v])=>[name,{exact_cost:v.str(),limit:v.limit().str(),decimal:v.limit().num()}]))});
 }
 const widths=[{id:"constant-1/256",value:Q("1/256")},{id:"constant-1/64",value:Q("1/64")},
  {id:"eps2",value:e.pow(2)},{id:"eps8",value:e.pow(8)}],experiments=[];
 const started=Date.now();
 for(const width of widths){
  const delta=width.value,fanRows=paths.map((p,i)=>T.prepare(p,delta,{id:ids[i]+"/uniform-fan/"+width.id,provenance:{base_row_id:ids[i],base_provenance:rows[i].provenance??null,width:delta.str()}})),
   routes=fixed.concat([
    {id:"edge-m1-15/16-eps+delta",route:inward(first.a(delta)),adaptive:true},
    {id:"edge-m1-7/8+delta",route:inward(Q("7/8").a(delta)),adaptive:true},
    {id:"edge-m2-3/16-eps-delta-U1",route:positiveM2(second.s(delta)),adaptive:true},
   ]),scores=[];
  for(let k=0;k<routes.length;k++){
   const c=routes[k],m=F.prepareMonster(c.route),sum=Object.fromEntries(mixtures.map(([name])=>[name,Z])),pure=[];
   for(let i=0;i<rows.length;i++){
    if(!used[i]){pure.push(null);continue;}
    const s=T.score(fanRows[i],m);if(!s.complete)throw Error("fan row incomplete");const cost=Q(s.exact_cost);pure.push(s.exact_cost);
    for(const[name,w]of mixtures)if(!w[i].eq(0))sum[name]=sum[name].a(cost.m(w[i]));
    if(i%32===31){await onProgress({stage:"fan-components",width:width.id,monster:c.id,row:i+1,total:rows.length,seconds:(Date.now()-started)/1000});await pause();}
   }
   scores.push({id:c.id,adaptive_fan_edge:!!c.adaptive,route:serial(c.route),mixtures:Object.fromEntries(Object.entries(sum).map(([name,v])=>[name,{exact_cost:v.str(),limit:v.limit().str(),decimal:v.limit().num()}])),pure_exact_costs:pure});
   await onProgress({stage:"fan-route-complete",width:width.id,monster:c.id,scores:Object.fromEntries(Object.entries(sum).map(([name,v])=>[name,v.limit().num()])),seconds:(Date.now()-started)/1000});await pause();
  }
  experiments.push({width_id:width.id,delta:delta.str(),scores});
 }
 return{scope:"Exact selected-response trial for immutable uniform translation-fan rows. Mixture values are raw physical-law payoffs; no comonotone improvement or all-Monster bound is asserted.",
  fixed_row_policy:"Each base path and delta are frozen. Fan-edge Monster columns are separately scored against that same fan.",
  rows:rows.length,row_ids:ids,mixtures:Object.fromEntries(mixtures.map(([name,w])=>[name,{positive_rows:w.filter(x=>!x.eq(0)).length,weights:w.map(x=>x.str())}])),
  baseline,experiments,hydration:worker.hydration,cache:T.stats(),arithmetic:G.stats(),seconds:(Date.now()-started)/1000};
}
async function main(){
 const[rowsFile,masterFile,oldFile,seedFile,out]=process.argv.slice(2);if(!out)throw Error("usage: node trial_translation_fans.mjs ROWS MASTER OLD_MASTER SEED OUT.json");
 const texts=await Promise.all([rowsFile,masterFile,oldFile,seedFile].map(p=>fs.readFile(p,"utf8"))),data=texts.map(JSON.parse),
  r=await trialTranslationFans(...data,{onProgress:async p=>{console.error(JSON.stringify(p));await fs.writeFile(out+".progress.json",JSON.stringify(p)+"\n");}});
 r.inputs=[rowsFile,masterFile,oldFile,seedFile].map((path,i)=>({path,sha256:sha(texts[i])}));
 await fs.writeFile(out,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.experiments.length,"fixed fan widths,",r.rows,"frozen rows,",r.seconds,"seconds");
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
