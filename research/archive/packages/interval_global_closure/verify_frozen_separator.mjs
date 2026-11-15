import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createFrozenSeparator} from "./separate_frozen_law.mjs";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";
import asymptoticModule from "./asymptotic_germ_search.cjs";

export async function verifyFrozenSeparator(fixtures){
 const checks=[];let pure=0,searches=0,asymptoticSearches=0;
 for(const f of fixtures){
  const rows=f.paths.map((path,i)=>({id:f.name+":"+i,path,provenance:"exact-fixture"})),
   w=createFrozenSeparator(rows),out=await w.separate(f.weights,{target:"0",top:2,allInitialColumns:true,search:true,nodeLimit:100000,maxSearchMs:30000}),
   G=germModule.createGermOracle(createOracle()),positive=f.paths.map(p=>new G.PLPath(p)),
   negative=positive.map(p=>new G.PLPath(p.vertices.map(([t,x])=>[t,x.neg()]))),
   all=positive.concat(negative),weights=f.weights.concat(f.weights),s=new G.CaptureSearch(all.map(p=>p.json()),weights,{mode:"sorted",nodeLimit:100000});
  while(!s.runSlice(1000,1000))await new Promise(resolve=>setImmediate(resolve));
  const r=s.result();if(!r.complete||!out.report.capture_order?.complete||!G.Q(r.value).eq(G.Q(out.report.capture_order.value)))throw Error("prepared constructor differs from original CaptureSearch");searches++;
  const ao=await w.separate(f.weights,{target:"0",top:1,search:true,objective:"limit",nodeLimit:100000,maxSearchMs:30000}),
   AS=asymptoticModule.createAsymptoticSearch(G),as=new AS(all.map(p=>p.json()),weights,{mode:"sorted",nodeLimit:100000});
  while(!as.runSlice(1000,1000))await new Promise(resolve=>setImmediate(resolve));
  const ar=as.result();if(!ar.asymptotic.certified||!ao.report.capture_order.asymptotic.certified||
   !G.Q(ar.asymptotic.limit).eq(G.Q(ao.report.capture_order.limit)))throw Error("prepared limit-pruned constructor mismatch");asymptoticSearches++;
  for(let j=0;j<out.columns.monsters.length;j++){
   const c=out.columns.monsters[j],m=new G.PLPath(c.route);
   for(let i=0;i<rows.length;i++){
    const a=G.rawCapture(m,positive[i]),b=G.rawCapture(m,negative[i]);
    if(a===null||b===null||!a.a(b).dby(2).eq(G.Q(out.columns.exact_costs[i][j])))throw Error("universal-column direct capture mismatch");pure+=2;
   }
  }
  // Removing all but one weight must not remove the other rows' initial
  // germs from the universal column family.
  const zero=f.weights.map((_,i)=>i===0?"1":"0"),z=await w.separate(zero,{target:"10",top:1,allInitialColumns:true,search:false});
  if(JSON.stringify(z.report.universal_m1.initial_positions)!==JSON.stringify(out.report.universal_m1.initial_positions))throw Error("zero-weight initial support omitted");
  checks.push({name:f.name,search_value:r.value,search_nodes:r.stats.nodes,
   universal_starts:out.report.universal_m1.initial_positions.length,columns:out.columns.monsters.length,
   zero_weight_universe_preserved:true,asymptotic_value:ar.asymptotic.limit,asymptotic_nodes:ar.stats.nodes,radius:w.G.stats().radius});
 }
 return{scope:"Prepared-path search initialization is compared with the original constructor; every universal M1/companion column is checked by direct segment capture, including zero-weight row support.",
  fixtures:checks,complete_search_equalities:searches,complete_asymptotic_search_equalities:asymptoticSearches,direct_signed_captures:pure};
}
async function main(){const[input,output]=process.argv.slice(2);if(!input||!output)throw Error("usage: node verify_frozen_separator.mjs FIXTURES.json REPORT.json");
 const r=await verifyFrozenSeparator(JSON.parse(await fs.readFile(input,"utf8")));await fs.writeFile(output,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.complete_search_equalities,"complete search equalities",r.complete_asymptotic_search_equalities,"limit-search equalities",r.direct_signed_captures,"direct signed captures");}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
