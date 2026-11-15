import fs from "node:fs/promises";
import {resolve} from "node:path";
import {pathToFileURL} from "node:url";
import germModule from "./germ_response_v8.cjs";
import m1Module from "./germ_m1_separator.cjs";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";

export function auditM1Germs(dictionary,cachedModule,{reference=null}={}){
 const E=createOracle(),G=germModule.createGermOracle(E),H=cachedModule.createCachedGermPaths(G),
  M=m1Module.createM1Separator(G),P=H.hydrate(dictionary),ss=M.starts(P),rows=[];
 for(const a of ss)for(const d of [-1,1]){
  const r=M.score(P,a,d,{components:true});let plane=G.ZERO;
  for(let j=0;j<P.paths.length;j++)plane=plane.a(G.Q(r.supergradient[j]).m(P.weights[j]));
  if(!plane.dby(P.W).eq(G.Q(r.exact_cost)))throw Error("weight plane not supporting");
  if(reference){
   const old=reference.rows.find(x=>x.direction===d&&G.Q(x.start).eq(a));
   if(!old||!G.Q(old.exact_cost).eq(G.Q(r.exact_cost)))throw Error("record-reference mismatch");
  }
  rows.push(r);
 }
 const summary=M.summarize(rows),best=summary.best;
 const compact=rows.map(({component_raw_times,supergradient,ceiling_coefficients,...r})=>r);
 return{scope:"Complete M1 family only; not an all-monster lower certificate.",initial_positions:ss.map(x=>x.str()),
  rows:compact,...summary,best:compact[summary.best_index],
  best_component_data:{raw_times:best.component_raw_times,supergradient:best.supergradient,ceiling_coefficients:best.ceiling_coefficients},
  record_equalities:reference?rows.length:0,supporting_plane_equalities:rows.length,hydration:P.audit,arithmetic:G.stats()};
}
async function main(){
 const[input,output,hydratorFile,referenceFile]=process.argv.slice(2);
 if(!input||!output||!hydratorFile)throw Error("usage: node audit_m1_germs.mjs CLIPPED_DICTIONARY.json REPORT.json SHARED_HYDRATOR.cjs [RECORD_REPORT.json]");
 const dictionary=JSON.parse(await fs.readFile(input,"utf8")),
  cached=(await import(pathToFileURL(resolve(hydratorFile)).href)).default,
  reference=referenceFile?JSON.parse(await fs.readFile(referenceFile,"utf8")):null,
  r=auditM1Germs(dictionary,cached,{reference});
 await fs.writeFile(output,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.candidate_routes,"complete-family routes; minimum",r.minimum_limit);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
