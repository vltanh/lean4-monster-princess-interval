/** Reusable lower worker: immutable physical rows, complete M1 first,
 * then the unchanged all-capture-order search when the M1 test is nonviolating.
 * Output columns always include every supplied row, including zero-weight rows.
 */
import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createHash} from "node:crypto";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";
import frozenModule from "./germ_frozen_law_tools.cjs";
import cachedModule from "./germ_cached_paths.cjs";
import m1Module from "./germ_m1_separator.cjs";
import unitModule from "./germ_unit_route_score.cjs";
import asymptoticModule from "./asymptotic_germ_search.cjs";

const sha=s=>createHash("sha256").update(s).digest("hex");
const pause=()=>new Promise(resolve=>setImmediate(resolve));
function dictionaryOfRows(rows){
 const coordinate_dictionary=[],indices=new Map();
 const index=x=>{x=String(x);if(!indices.has(x)){indices.set(x,coordinate_dictionary.length);coordinate_dictionary.push(x);}return indices.get(x);};
 return{coordinate_dictionary,paths:rows.map((r,j)=>{const path=[];
  for(const v of r.path){const p=v.map(index),last=path.at(-1);if(last&&p[0]===last[0]&&p[1]===last[1])continue;path.push(p);}
  return{row:r.id??j,weight:"1",path};})};
}

export function createFrozenSeparator(rows){
 if(!Array.isArray(rows)||!rows.length)throw Error("nonempty frozen row array required");
 const ids=rows.map((r,i)=>r.id??i);if(new Set(ids).size!==ids.length)throw Error("duplicate frozen row identity");
 const E=createOracle(),G=germModule.createGermOracle(E),F=frozenModule.createFrozenLawTools(G),
  H=cachedModule.createCachedGermPaths(G),hydrated=H.hydrate(dictionaryOfRows(rows)),
  paths=hydrated.positive,U=unitModule.createUnitRouteScorer(G),M=m1Module.createM1Separator(G,U);

 function canonical(raw){
  let p=F.prepareMonster(raw).route;
  const start=G.Q(p[0][1]);
  if(start.cmp(0)<0||(start.eq(0)&&p.length>1&&G.Q(p[1][1]).cmp(0)>0))p=p.map(([t,x])=>[t,G.Q(x).neg().str()]);
  return F.prepareMonster(p).route;
 }
 function collapse(raw){return canonical(raw.map(p=>p.map(x=>G.Q(x).limit().str())));}
 function completeRoute(raw){
  const p=[];let left=false,right=false;
  for(const v of raw){const q=v.map(G.Q);p.push(q);left=left||q[1].eq(-1);right=right||q[1].eq(1);if(left&&right)return canonical(p);}
  let[t,x]=p.at(-1);
  // Stop at the first visit to both endpoints. This covers every possible
  // Princess, including zero-weight rows, without appending a redundant tour.
  if(!left){t=t.a(x.a(1));p.push([t,G.Q(-1)]);x=G.Q(-1);left=true;}
  if(!right){t=t.a(G.ONE.s(x));p.push([t,G.ONE]);}
  return canonical(p);
 }
 function fullSearch(P,incumbent,target,options,objective){
  // This is precisely CaptureSearch's constructor state, reusing validated
  // paths and inverse caches instead of re-parsing all immutable vertices.
  const Search=objective==="limit"?asymptoticModule.createAsymptoticSearch(G):G.CaptureSearch,
   s=Object.create(Search.prototype);
  Object.assign(s,{ps:P.paths,ws:P.weights,W:P.W,n:P.paths.length,options,mode:"sorted",
   full:(1n<<BigInt(P.paths.length))-1n,memo:new Map(),
   stats:{nodes:0,leaves:0,bounded:0,dominated:0,improvements:0},complete:false,stopReason:null,
   best:G.Q(incumbent.exact_cost).m(P.W),bestRoute:incumbent.route.map(p=>p.map(G.Q)),stack:[],
   target:target===null?null:G.Q(target).m(P.W)});
  if(objective==="limit"){s.asymptoticBounds=[];s.proofMode="exact geometry with limit-only objective pruning";}
  const starts=new Map();P.paths.forEach((p,i)=>{const key=p.x[0].str();if(!starts.has(key))starts.set(key,{x:p.x[0],anchor:i});});
  for(const z of starts.values())s.stack.push({lo:P.W,hi:0n,mask:0n,t:G.ZERO,x:z.x,cost:G.ZERO,anchor:z.anchor,route:{p:[G.ZERO,z.x],prev:null}});
  return s;
 }

 async function separate(weights,{target=null,top=8,allInitialColumns=false,search=true,objective="germ",nodeLimit=20000,maxSearchMs=60000,onProgress=()=>{}}={}){
  if(objective!=="germ"&&objective!=="limit")throw Error("objective must be germ or limit");
  if(weights.length!==rows.length)throw Error("weight count differs from frozen rows");
  const weighted=rows.map((r,j)=>({id:ids[j],path:paths[j],weight:String(weights[j]),provenance:r.provenance??null})),
   law=F.orderedLaw(weighted),P=law.prepared,startTime=Date.now(),initial=M.starts(P),scores=[];
  let scan=0;
  for(const a of initial)for(const d of [-1,1]){
   scores.push(M.score(P,a,d));scan++;
   if(scan%16===0){await onProgress({stage:"m1",done:scan,total:2*initial.length,seconds:(Date.now()-startTime)/1000});await pause();}
  }
  const summary=M.summarize(scores),best=summary.best,minimumLimit=G.Q(summary.minimum_limit),
   targetQ=target===null?null:G.Q(target),violating=targetQ===null||minimumLimit.cmp(targetQ)<0,
   sorted=[...scores].sort((a,b)=>G.Q(a.limit).cmp(G.Q(b.limit))||G.Q(a.exact_cost).cmp(G.Q(b.exact_cost))),
   candidates=new Map();
  function add(route,kind,from=null){
   const p=canonical(route),key=JSON.stringify(p);if(candidates.has(key))return;
   candidates.set(key,{id:kind+":"+sha(key).slice(0,20),kind,from,route:p});
  }
  let selected=0;const seen=new Set();
  for(const r of sorted){
   const p=canonical(r.route),key=JSON.stringify(p);if(seen.has(key))continue;seen.add(key);
   if(selected>=top)break;
   if(targetQ!==null&&G.Q(r.limit).cmp(targetQ)>=0&&selected>0)break;
   add(p,"m1-germ");selected++;
  }
  let universalStarts=null;
  if(allInitialColumns){
   const a=paths.flatMap(p=>[p.x[0],p.x[0].neg()]).concat([G.Q(-1),G.ONE]);a.sort((x,y)=>x.cmp(y));
   universalStarts=a.filter((x,j)=>!j||!x.eq(a[j-1]));
   for(const x of universalStarts)for(const d of [-1,1])add(M.route(x,d),"m1-initial-universe");
  }
  let searchResult=null;
  if(search&&!violating){
   const s=fullSearch(P,best,target,{nodeLimit,prune:true},objective),started=Date.now();
   while(!s.runSlice(50,500)){
    await onProgress({stage:"capture-order",...s.stats,remaining:s.stack.length,seconds:(Date.now()-started)/1000});
    if(Date.now()-started>=maxSearchMs){s.stopReason="time budget";break;}await pause();
   }
   const route=completeRoute(s.bestRoute),direct=U.score(P,route,{fullCost:true});
   if(!direct.complete||!G.Q(direct.value??direct.exact_cost??direct.cost).eq(s.best.dby(P.W)))throw Error("capture-order independent unit-record mismatch");
   searchResult={complete:s.complete,stopReason:s.stopReason,stats:{...s.stats,memoKeys:s.memo.size,remaining:s.stack.length},
    value:s.best.dby(P.W).str(),limit:s.best.dby(P.W).limit().str(),route,objective,exact_germ_optimum:objective==="germ"&&s.complete,
    seconds:(Date.now()-started)/1000};
   if(objective==="limit"){
    searchResult.proof_mode=s.proofMode;
    searchResult.asymptotic={certified:s.complete&&!s.stopReason,pruned_bound_count:s.asymptoticBounds.length};
    if(searchResult.asymptotic.certified){
     let lower=s.best;for(const b of s.asymptoticBounds)if(b.cmp(lower)<0)lower=b;
     if(lower.limit().cmp(s.best.limit())!==0)throw Error("prepared asymptotic sandwich mismatch");
     searchResult.asymptotic.lower_value=lower.dby(P.W).str();searchResult.asymptotic.upper_value=s.best.dby(P.W).str();
     searchResult.asymptotic.limit=s.best.dby(P.W).limit().str();searchResult.exact_germ_optimum=lower.eq(s.best);
    }
   }
   add(route,"capture-order-germ");
  }
  // Collapsing is a separate physical Monster law. It never replaces a germ
  // attack, and is rescored against the same frozen Princess rows.
  for(const c of [...candidates.values()]){const p=collapse(c.route);if(JSON.stringify(p)!==JSON.stringify(c.route))add(p,"collapsed-companion",c.id);}
  const columns=[];
  for(const c of candidates.values()){
   const m=F.prepareMonster(c.route),v=[];let raw=G.ZERO;
   for(let j=0;j<rows.length;j++){
    const r=F.pairScore(paths[j],m,{fullCost:true});if(!r.complete)throw Error("new column misses a frozen row");v.push(r);
    raw=raw.a(G.Q(r.exact_cost).m(String(weights[j])));
   }
   const total=weights.reduce((z,w)=>z.a(G.Q(String(w))),G.ZERO);raw=raw.dby(total);
   let ordered;
   if(c.kind.startsWith("m1")||c.kind==="collapsed-companion"&&m.route.length<=3){
    const a=G.Q(m.route[0][1]),d=G.Q(m.route[1][1]).cmp(a);ordered=M.score(P,a,d).exact_cost;
   }else{const r=U.score(P,m.route,{fullCost:true});if(!r.complete)throw Error("ordered column incomplete");ordered=G.Q(r.value??r.exact_cost??r.cost).str();}
   if(G.Q(ordered).cmp(raw)<0)throw Error("ordered law is worse than raw mixture");
   const exact_light=m.route.map(([t,x])=>[G.Q(t).a(G.Q(x)).str(),G.Q(t).s(G.Q(x)).str()]);
   columns.push({...c,atom:{kind:"PATH",parameters:exact_light.flat()},exact_light,ordered_cost:ordered,ordered_limit:G.Q(ordered).limit().str(),ordered_decimal:G.Q(ordered).limit().num(),
    raw_cost:raw.str(),raw_limit:raw.limit().str(),limits:v.map(r=>r.limit),exact_costs:v.map(r=>r.exact_cost)});
   if(columns.length%8===0){await onProgress({stage:"new-columns",done:columns.length,total:candidates.size,seconds:(Date.now()-startTime)/1000});await pause();}
  }
  return{report:{scope:"Complete all-start M1 separation of the normalized implicit comonotone law. Full all-Monster certification is claimed only if capture_order.complete is true; returned finite attacks are independently scored physical unit routes.",
   target,weight_policy:"Each supplied decimal/string is interpreted as an exact constant rational, then normalized. No thresholding, re-realization, or path mutation.",
   frozen_rows:rows.length,active_rows:law.metadata.length,normalized_pair_weights:law.metadata.map(r=>({id:r.id,weight:r.pair_weight})),
   initial_positions:initial.map(x=>x.str()),m1:{...summary,rows:scores,violates_target:violating},capture_order:searchResult,
   universal_m1:universalStarts?{scope:"Complete M1 column universe for every probability vector on ALL frozen input rows; exact reflection deduplication uses each row's signed-pair convention.",
    initial_positions:universalStarts.map(x=>x.str()),oriented_candidates:2*universalStarts.length,includes_zero_weight_rows:true,
    distinct_columns_with_collapsed_companions:columns.length}:null,
   candidates:columns.map(({limits,exact_costs,...c})=>c),hydration:hydrated.audit,cache:F.stats(),arithmetic:G.stats(),seconds:(Date.now()-startTime)/1000},
   columns:{scope:"Literal pure-pair columns on every immutable input row; ordered-law score is separately tagged and must not be substituted for the raw matrix average.",
    row_ids:ids,monsters:columns.map(({limits,exact_costs,...c})=>c),
    exact_limits:rows.map((_,i)=>columns.map(c=>c.limits[i])),exact_costs:rows.map((_,i)=>columns.map(c=>c.exact_costs[i])),
    decimals:rows.map((_,i)=>columns.map(c=>G.Q(c.limits[i]).limit().num()))}};
 }
 return{separate,G,F,paths,ids,hydration:hydrated.audit};
}

async function main(){
 const args=process.argv.slice(2),[rowsPath,weightsPath,prefix]=args;
 if(!rowsPath||!weightsPath||!prefix)throw Error("usage: node separate_frozen_law.mjs FROZEN_ROWS.json MASTER.json OUTPREFIX [--target VALUE] [--top 8] [--all-initial-columns] [--no-search] [--limit-objective] [--nodes 20000] [--milliseconds 60000]");
 const arg=(name,fallback)=>{const i=args.indexOf(name);return i<0?fallback:args[i+1];},
  rowsText=await fs.readFile(rowsPath,"utf8"),weightsText=await fs.readFile(weightsPath,"utf8"),rows=JSON.parse(rowsText),master=JSON.parse(weightsText),
  weights=master.princess_weights||master.weights||master,target=arg("--target",master.report?.packing_value===undefined?null:String(master.report.packing_value)),
  worker=createFrozenSeparator(rows);
 console.error(JSON.stringify({stage:"hydrated",rows:rows.length,hydration:worker.hydration}));
 const out=await worker.separate(weights,{target,top:Number(arg("--top","8")),allInitialColumns:args.includes("--all-initial-columns"),search:!args.includes("--no-search"),objective:args.includes("--limit-objective")?"limit":"germ",
  nodeLimit:Number(arg("--nodes","20000")),maxSearchMs:Number(arg("--milliseconds","60000")),
  onProgress:async p=>{console.error(JSON.stringify(p));await fs.writeFile(prefix+".progress.json",JSON.stringify(p)+"\n");}});
 out.report.inputs={rows_sha256:sha(rowsText),weights_sha256:sha(weightsText)};
 await fs.writeFile(prefix+".report.json",JSON.stringify(out.report,null,2)+"\n");
 await fs.writeFile(prefix+".columns.json",JSON.stringify(out.columns,null,2)+"\n");
 console.log(JSON.stringify({status:"PASS",active:out.report.active_rows,m1_routes:out.report.m1.candidate_routes,
  minimum_limit:out.report.m1.minimum_limit,minimum_decimal:worker.G.Q(out.report.m1.minimum_limit).limit().num(),
  violates_target:out.report.m1.violates_target,columns:out.columns.monsters.length,capture_order:out.report.capture_order,
  output_prefix:prefix,seconds:out.report.seconds}));
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
