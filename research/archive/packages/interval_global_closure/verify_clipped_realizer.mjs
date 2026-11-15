import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import germModule from "./germ_response_v8.cjs";
import clippedModule from "./germ_clipped_realizer.cjs";
import avoidedModule from "./germ_avoided_realizer.cjs";
import unitModule from "./germ_unit_route_score.cjs";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";

export function verifyClippedRealizer(data,{bank=true}={}){
 const E=createOracle(),G=germModule.createGermOracle(E),R=clippedModule.createClippedRealizer(G),
  A=avoidedModule.createAvoidedRealizer(G),U=unitModule.createUnitRouteScorer(G),q=G.Q,toy=[];
 for(const tau of ["1/4","1/2","3/4"]){
  const t=q(tau),query=["-1",t.neg().str(),t.str(),t.a(2).str()],levels=["0",t.str(),t.a(2).str(),t.a(4).str()],labels=[1,3,6,9];
  const d=R.realize(query,levels,labels),p=d.path;
  if(d.traces.some(x=>!x.nonzeroPreserved))throw Error("toy nonzero side");
  const search=new G.CaptureSearch([p.json(),p.vertices.map(([t,x])=>[t.str(),x.neg().str()])],["1/2","1/2"],{mode:"sorted",nodeLimit:10000});
  while(!search.runSlice(1000,1000)){}const r=search.result();
  const expected=t.a(1).dby(2).s(G.eps.dby(2)).s(G.eps.pow(6).dby(2));
  if(!r.complete||!q(r.value).eq(expected))throw Error("clipped toy value");
  toy.push({tau,value:q(r.value).str(),limit:q(r.value).limit().str(),vertices:p.t.length,nodes:r.stats.nodes});
 }
 const rows=[];
 if(data){
  if(data.princess_mixture.length!==159||data.query_v.length!==408||data.atoms.length!==1086)throw Error("wrong checkpoint");
  const levels=data.event_labels.filter((_,j)=>j%3===0).map(x=>x[0]);
  const routes=data.atoms.map(a=>{
   if(a.kind!=="PATH")throw Error("nonpath atom");const r=[];
   for(let j=0;j<a.parameters.length;j+=2){const u=q(a.parameters[j]),v=q(a.parameters[j+1]);r.push([u.a(v).dby(2),u.s(v).dby(2)]);}
   return r;
  });
  for(const id of [0,85,79,158]){
   const labels=data.princess_mixture[id].labels,old=A.realize(data.query_v,levels,labels,{avoidIsolated:false}),alt=R.realize(data.query_v,levels,labels);
   if(alt.traces.some(x=>!x.nonzeroPreserved))throw Error("actual nonzero side");
   const prep=p=>G.prepare([p.json(),p.vertices.map(([t,x])=>[t.str(),x.neg().str()])],["1/2","1/2"]);
   let checks=0;
   if(bank){const p=prep(old.path),r=prep(alt.path);
    for(const m of routes){const a=U.score(p,m),b=U.score(r,m);if(!a.complete||!b.complete||!E.Q(a.limit).eq(b.limit))throw Error("fixed-bank limit changed");checks++;}
   }
   rows.push({row:id,vertices:alt.path.t.length,isolated_avoided:alt.changes.length,
    nonzero_side_checks:alt.traces.filter(x=>x.side).length,
    changed_zero_signatures:alt.traces.filter((x,j)=>!x.side&&(x.postSide!==old.traces[j].postSide||x.postLastSide!==old.traces[j].postSide)).length,
    fixed_bank_checks:checks});
  }
 }
 return{scope:"Distinct clipped unit/wait candidates. Fixed-bank agreement does not imply adaptive-response equivalence.",toy,rows,arithmetic:G.stats()};
}
async function main(){
 const args=process.argv.slice(2),bank=!args.includes("--skip-bank"),files=args.filter(x=>x!=="--skip-bank"),[input,output]=files;
 if(!input||!output)throw Error("usage: node verify_clipped_realizer.mjs CHECKPOINT.json REPORT.json [--skip-bank]");
 const r=verifyClippedRealizer(JSON.parse(await fs.readFile(input,"utf8")),{bank});
 await fs.writeFile(output,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.toy.length,"complete toy searches",r.rows.length,"actual controls",r.rows.reduce((n,x)=>n+x.fixed_bank_checks,0),"bank comparisons");
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
