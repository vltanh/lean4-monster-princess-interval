import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import germModule from "./germ_response_v8.cjs";
import m1Module from "./germ_m1_separator.cjs";
import unitModule from "./germ_unit_route_score.cjs";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";

export function verifyM1Separator(fixtures){
 const E=createOracle(),G=germModule.createGermOracle(E),U=unitModule.createUnitRouteScorer(G),M=m1Module.createM1Separator(G,U),cases=[];
 let records=0,rawSegments=0,gaps=0,planes=0;
 for(const f of fixtures){
  const P=G.prepare(f.paths,f.weights),ss=M.starts(P),rows=[];
  for(const a of ss)for(const d of [-1,1]){
   const r=M.score(P,a,d,{components:true}),v=M.recordScore(P,a,d);
   if(!G.Q(r.exact_cost).eq(v.cost))throw Error("inverse/record mismatch");records++;
   const monster=new G.PLPath(M.route(a,d));let raw=G.ZERO;
   for(let j=0;j<P.paths.length;j++){
    const t=G.rawCapture(monster,P.paths[j]);if(t===null)throw Error("raw incomplete");
    raw=raw.a(t.m(P.weights[j]));
   }
   if(!raw.dby(P.W).eq(G.Q(r.raw_cost)))throw Error("raw first-inverse/segment mismatch");rawSegments++;
   for(const shift of [1,2]){
    const ws=P.paths.map((_,j)=>BigInt(1+(j+shift)%P.paths.length)),W=ws.reduce((a,b)=>a+b,0n),
     altered={paths:P.paths,weights:ws,W},s=M.score(altered,a,d);
    let plane=G.ZERO;for(let j=0;j<ws.length;j++)plane=plane.a(G.Q(r.supergradient[j]).m(ws[j]));
    if(plane.dby(W).cmp(G.Q(s.exact_cost))<0)throw Error("concave weight plane invalid");planes++;
   }
   rows.push(r);
  }
  for(let j=0;j+1<ss.length;j++){
   const a=ss[j].a(ss[j+1]).dby(2);
   for(const d of [-1,1]){
    const boundary=d<0?ss[j]:ss[j+1],b=M.score(P,boundary,d),r=M.score(P,a,d);
    if(G.Q(b.exact_cost).cmp(G.Q(r.exact_cost))>0||G.Q(b.raw_cost).cmp(G.Q(r.raw_cost))>0)throw Error("initial-gap dominance failed");gaps++;
   }
  }
  const summary=M.summarize(rows);cases.push({name:f.name,initial_positions:ss.length,candidate_routes:rows.length,minimum_germ:summary.minimum_germ,minimum_limit:summary.minimum_limit});
 }
 return{scope:"Complete-family reduction fixtures, exact moments, physical segments, and concave weight planes.",
  cases,record_equalities:records,raw_segment_equalities:rawSegments,gap_dominance_checks:gaps,weight_plane_checks:planes,arithmetic:G.stats()};
}
async function main(){
 const[input,output]=process.argv.slice(2);
 if(!input||!output)throw Error("usage: node verify_m1_germs.mjs germ_v8_fixture_inputs.json REPORT.json");
 const r=verifyM1Separator(JSON.parse(await fs.readFile(input,"utf8")));
 await fs.writeFile(output,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.cases.length,"fixtures",r.record_equalities,"record and segment equalities",r.gap_dominance_checks,"gap checks",r.weight_plane_checks,"weight planes");
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
