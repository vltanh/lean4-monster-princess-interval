/** Fixed physical tail, exact initial-start reduction. Discovery defaults to
 * same-limit substitutions; --all-initial releases the complete start family.
 * Raw paired cost is a rigorous lower bound on the ordered cost, so only raw
 * target violations need the more expensive ordered record evaluation.
 */
import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createHash} from "node:crypto";
import {createFrozenSeparator} from "./separate_frozen_law.mjs";
import unitModule from "./germ_unit_route_score.cjs";
const sha=s=>createHash("sha256").update(s).digest("hex");
const pause=()=>new Promise(resolve=>setImmediate(resolve));

export function compileFixedTails(worker,bank,{sameLimitOnly=true}={}){
 const {G,F,paths}=worker,Q=G.Q,ss=paths.flatMap(p=>[p.x[0],p.x[0].neg()]).concat([Q(-1),G.ONE]);
 ss.sort((a,b)=>a.cmp(b));const starts=ss.filter((x,j)=>!j||!x.eq(ss[j-1])),families=new Map();
 let skippedNoReversal=0,skippedIncompleteTail=0,unsupported=0;
 for(let j=0;j<bank.length;j++){
  let monster;try{monster=F.prepareMonster(bank[j]);}catch(e){unsupported++;continue;}
  let p=monster.path.vertices,left=false,right=false;
  for(let k=0;k<p.length;k++){left=left||p[k][1].eq(-1);right=right||p[k][1].eq(1);if(left&&right){p=p.slice(0,k+1);break;}}
  if(p.length<3){skippedNoReversal++;continue;}
  const d=p[1][1].cmp(p[0][1]);if(d!==-1&&d!==1)throw Error("nonunit first leg");
  const oriented=p.map(([t,x])=>[t,x.m(d)]),c=oriented[1][0].a(oriented[1][1]),tail=oriented.slice(2);
  if(!tail.some(([,x])=>x.eq(-1))||!tail.some(([,x])=>x.eq(1))) {skippedIncompleteTail++;continue;}
  if(!tail[0][0].a(tail[0][1]).eq(c))throw Error("first tail leg is not the opposite unit characteristic");
  const lower=[Q(-1),c.s(tail[0][0].m(2))].reduce((a,b)=>a.cmp(b)>0?a:b),
   upper=[G.ONE,c,Q(2).s(c)].reduce((a,b)=>a.cmp(b)<0?a:b);
  if(lower.cmp(upper)>0)throw Error("empty legal interval for an existing tail");
  const key=JSON.stringify([c.str(),tail.map(v=>v.map(x=>x.str()))]);
  let f=families.get(key);if(!f){f={id:sha(key).slice(0,20),c,tail,lower,upper,source_indices:[],initial_limits:new Set()};families.set(key,f);}
  f.source_indices.push(j);f.initial_limits.add(oriented[0][1].limit().str());
 }
 const candidates=new Map();
 for(const f of families.values()){
  const choices=starts.filter(b=>b.cmp(f.lower)>=0&&b.cmp(f.upper)<=0&&(!sameLimitOnly||f.initial_limits.has(b.limit().str()))).concat([f.lower,f.upper]);
  for(const b of choices){
   const route=[[G.ZERO,b],[f.c.s(b).dby(2),f.c.a(b).dby(2)],...f.tail],m=F.prepareMonster(route),key=JSON.stringify(m.route);
   if(!candidates.has(key))candidates.set(key,{id:"fixed-tail-start:"+sha(key).slice(0,20),family:f.id,start:b.str(),route:m.route,monster:m});
  }
 }
 return{candidates:[...candidates.values()],families:[...families.values()].map(f=>({id:f.id,c:f.c.str(),tail:f.tail.map(v=>v.map(x=>x.str())),lower:f.lower.str(),upper:f.upper.str(),
  source_indices:f.source_indices,initial_limits:[...f.initial_limits]})),
  counts:{supplied_atoms:bank.length,actual_initial_positions:starts.length,fixed_tail_families:families.size,candidates:candidates.size,
   skipped_no_reversal:skippedNoReversal,skipped_tail_without_both_endpoints:skippedIncompleteTail,unsupported_atoms:unsupported},
  sameLimitOnly};
}

export async function separateFixedTails(rows,weights,bank,{target,top=12,sameLimitOnly=true,maximumRaw=1000000,planOnly=false,onProgress=()=>{}}={}){
 if(target===undefined)throw Error("target required for safe raw-cost screen");
 const worker=createFrozenSeparator(rows),{G,F,paths,ids}=worker,Q=G.Q,U=unitModule.createUnitRouteScorer(G),
  weighted=rows.map((r,j)=>({id:ids[j],path:paths[j],weight:String(weights[j]),provenance:r.provenance})),law=F.orderedLaw(weighted),P=law.prepared,
  plan=compileFixedTails(worker,bank,{sameLimitOnly}),started=Date.now();
 if(planOnly)return{report:{scope:"Exact geometry planning only.",counts:plan.counts,families:plan.families,same_limit_only:sameLimitOnly,arithmetic:G.stats()}};
 const targetRat=Q(target).limit();
 // Repeated tail vertices share time queries. This only caches evaluations;
 // the serialized physical paths and all exact branch decisions are unchanged.
 for(const p of P.paths){const original=p.at,cache=new Map();p.at=function(t){t=Q(t);const key=t.str();let x=cache.get(key);if(x===undefined){x=original.call(this,t);cache.set(key,x);}return x;};}
 const rawViolations=[];let rawTested=0,rawPruned=0,rawMinimum=null;
 for(const c of plan.candidates){
  if(rawTested>=maximumRaw)break;let cost=G.ZERO.limit();
  for(let j=0;j<P.positive.length;j++){
   const a=F.capture(P.positive[j],c.monster,1),b=F.capture(P.positive[j],c.monster,-1);
   if(a===null||b===null)throw Error("fixed completed tail misses a path");
   cost=cost.a(a.limit().a(b.limit()).m(P.pairWeights[j]));
  }
  cost=cost.dby(2n*P.pairTotal);rawTested++;c.raw=cost.str();
  if(rawMinimum===null||cost.cmp(Q(rawMinimum).limit())<0)rawMinimum=c.raw;
  if(cost.cmp(targetRat)<0)rawViolations.push(c);else rawPruned++;
  if(rawTested%32===0){await onProgress({stage:"fixed-tail-raw",tested:rawTested,total:plan.candidates.length,violations:rawViolations.length,seconds:(Date.now()-started)/1000});await pause();}
 }
 rawViolations.sort((a,b)=>Q(a.raw).cmp(Q(b.raw)));
 const ordered=[],attacks=[];
 for(const c of rawViolations){
  const score=U.score(P,c.route);if(!score.complete)throw Error("fixed tail incomplete for ordered law");
  c.ordered=score.limit;c.decimal=Q(c.ordered).limit().num();ordered.push(c);
  if(Q(c.ordered).cmp(Q(target))<0)attacks.push(c);
  if(ordered.length%16===0){await onProgress({stage:"fixed-tail-ordered",tested:ordered.length,total:rawViolations.length,attacks:attacks.length,
   minimum:Math.min(...ordered.map(x=>x.decimal)),seconds:(Date.now()-started)/1000});await pause();}
 }
 attacks.sort((a,b)=>Q(a.ordered).cmp(Q(b.ordered))||a.id.localeCompare(b.id));
 const selected=attacks.slice(0,top),columns=[];
 for(const c of selected){
  const full=U.score(P,c.route,{fullCost:true}),records=paths.map(p=>F.pairScore(p,c.monster,{fullCost:true}));
  if(records.some(r=>!r.complete))throw Error("selected tail misses a zero-weight row");
  const exact_light=c.route.map(([t,x])=>[Q(t).a(Q(x)).str(),Q(t).s(Q(x)).str()]);
  columns.push({id:c.id,family:c.family,start:c.start,route:c.route,atom:{kind:"PATH",parameters:exact_light.flat()},exact_light,
   ordered_cost:full.cost.str(),ordered_limit:full.limit,ordered_decimal:c.decimal,raw_limit:c.raw,
   limits:records.map(r=>r.limit),costs:records.map(r=>r.exact_cost)});
 }
 return{report:{scope:"Fixed-tail initial-start family only. Same-limit mode is a discovery subset, not complete separation of all tail starts or all Monster paths. Raw-cost pruning is safe because common-quantile coupling cannot reduce a Monster payoff.",
  target,counts:{...plan.counts,active_rows:law.metadata.length,raw_tested:rawTested,raw_nonviolating:rawPruned,ordered_tested:ordered.length,ordered_attacks:attacks.length},
  same_limit_only:sameLimitOnly,complete_candidate_pool:rawTested===plan.candidates.length,
  complete_supplied_tail_start_families:!sameLimitOnly&&rawTested===plan.candidates.length,
  families:plan.families,raw_minimum:rawMinimum,
  ordered_results:ordered.map(({monster,...c})=>c),candidates:columns.map(({limits,costs,...c})=>c),
  hydration:worker.hydration,cache:F.stats(),arithmetic:G.stats(),seconds:(Date.now()-started)/1000},
  columns:{scope:"Literal exact pure-pair columns, independently scored on every supplied frozen row; ordered costs are separate.",row_ids:ids,
   monsters:columns.map(({limits,costs,...c})=>c),exact_limits:rows.map((_,i)=>columns.map(c=>c.limits[i])),
   exact_costs:rows.map((_,i)=>columns.map(c=>c.costs[i])),decimals:rows.map((_,i)=>columns.map(c=>Q(c.limits[i]).limit().num()))}};
}

async function main(){
 const args=process.argv.slice(2),[rowsPath,masterPath,bankPath,prefix]=args;
 if(!prefix)throw Error("usage: node fixed_tail_start_separator.mjs ROWS.json MASTER.json BANK.json OUTPREFIX [--all-initial] [--plan] [--top 12] [--maximum-raw N] [--target V]");
 const opt=(k,v)=>{const i=args.indexOf(k);return i<0?v:args[i+1];},
  rowText=await fs.readFile(rowsPath,"utf8"),masterText=await fs.readFile(masterPath,"utf8"),bankText=await fs.readFile(bankPath,"utf8"),
  rows=JSON.parse(rowText),master=JSON.parse(masterText),b=JSON.parse(bankText),weights=master.princess_weights||master.weights||master,
  target=opt("--target",String(master.report?.packing_value)),
  out=await separateFixedTails(rows,weights,b.atoms||b,{target,top:Number(opt("--top","12")),sameLimitOnly:!args.includes("--all-initial"),
   maximumRaw:Number(opt("--maximum-raw","1000000")),planOnly:args.includes("--plan"),
   onProgress:async x=>{console.error(JSON.stringify(x));await fs.writeFile(prefix+".progress.json",JSON.stringify(x)+"\n");}});
 out.report.inputs={rows_sha256:sha(rowText),master_sha256:sha(masterText),bank_sha256:sha(bankText)};
 await fs.writeFile(prefix+".report.json",JSON.stringify(out.report,null,2)+"\n");
 if(out.columns)await fs.writeFile(prefix+".columns.json",JSON.stringify(out.columns,null,2)+"\n");
 console.log(JSON.stringify({status:"PASS",...out.report.counts,columns:out.columns?.monsters.length,minimum:out.columns?.monsters[0]?.ordered_limit,
  minimum_decimal:out.columns?.monsters[0]?.ordered_decimal,output_prefix:prefix,seconds:out.report.seconds}));
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
