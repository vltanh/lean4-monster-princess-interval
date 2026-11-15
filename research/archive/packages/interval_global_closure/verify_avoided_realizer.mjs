import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import germModule from "./germ_response_v8.cjs";
import avoidedModule from "./germ_avoided_realizer.cjs";
import unitModule from "./germ_unit_route_score.cjs";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";

export function verifyAvoidedRealizer(data,{bank=true}={}){
 const E=createOracle(),G=germModule.createGermOracle(E),R=avoidedModule.createAvoidedRealizer(G),U=unitModule.createUnitRouteScorer(G),q=G.Q;
 const toy=[];
 for(const tau of ["1/4","1/2","3/4"]){
  const t=q(tau),query=["-1",t.neg().str(),t.str(),t.a(2).str()],levels=["0",t.str(),t.a(2).str(),t.a(4).str()],indices=[1,3,6,9],row={tau};
  for(const avoid of [false,true]){
   const d=R.realize(query,levels,indices,{avoidIsolated:avoid}),p=d.path;
   const paths=[p.json(),p.vertices.map(([t,x])=>[t.str(),x.neg().str()])],s=new G.CaptureSearch(paths,["1/2","1/2"],{mode:"sorted",nodeLimit:10000});
   while(!s.runSlice(1000,1000)){}const r=s.result();if(!r.complete)throw Error("incomplete toy");
   const expected=avoid?t.a(1).dby(2):t.dby(2);
   if(!q(r.value).limit().eq(expected.limit()))throw Error("wrong toy limit");
   row[avoid?"avoided":"minimum_fill"]={limit:q(r.value).limit().str(),value:q(r.value).data(),vertices:p.t.length,changes:d.changes.length,traces:d.traces,nodes:r.stats.nodes};
  }
  toy.push(row);
 }
 const out={scope:"Two microscopic realizations of identical priced labels. Toy searches are complete all-monster results; actual-bank comparisons are fixed-route checks only.",toy};
 if(data){
  if(data.princess_mixture.length!==159||data.query_v.length!==408||data.atoms.length!==1086)throw Error("wrong checkpoint dimensions");
  const levels=data.event_labels.filter((_,j)=>j%3===0).map(x=>x[0]);
  for(let j=0;j<data.event_labels.length;j++)if(data.event_labels[j][0]!==levels[Math.floor(j/3)]||data.event_labels[j][1]!==j%3-1)throw Error("event label encoding");
  const routes=data.atoms.map(a=>{if(a.kind!=="PATH")throw Error("non-PATH atom");const r=[];for(let j=0;j<a.parameters.length;j+=2){const u=q(a.parameters[j]),v=q(a.parameters[j+1]);r.push([u.a(v).dby(2),u.s(v).dby(2)]);}return r;});
  const rows=[];
  for(const id of [0,79,158,85]){
   const source=data.princess_mixture[id],old=R.realize(data.query_v,levels,source.labels,{avoidIsolated:false}),alt=R.realize(data.query_v,levels,source.labels,{avoidIsolated:true});
   if(JSON.stringify(old.path.json())!==JSON.stringify(G.realize(data.query_v,levels,source.labels).json()))throw Error("baseline realizer mismatch");
   if(old.traces.some((x,k)=>x.postSide!==alt.traces[k].postSide))throw Error("post-label signature changed");
   for(const c of alt.changes)if(q(c.gap).dby(G.eps).limit().cmp(1)<0)throw Error("gap below epsilon");
   const row={row:id,old_vertices:old.path.t.length,new_vertices:alt.path.t.length,isolated_avoided:alt.changes.length,forced_intervals:alt.forcedCenterIntervals.length,pre_query_trace_pairs:old.traces.length+alt.traces.length,post_nonzero_label_checks:old.traces.filter(x=>x.side).length+alt.traces.filter(x=>x.side).length,post_signature_comparisons:old.traces.length,zero_label_sides:alt.traces.filter(x=>!x.side).map(x=>({query:x.query,side:x.postSide}))};
   if(bank){
    const prepare=p=>G.prepare([p.json(),p.vertices.map(([t,x])=>[t.str(),x.neg().str()])],["1/2","1/2"]),pold=prepare(old.path),palt=prepare(alt.path);
    for(const route of routes){const a=U.score(pold,route),b=U.score(palt,route);if(!a.complete||!b.complete||!E.Q(a.limit).eq(b.limit))throw Error("fixed-bank limiting payoff changed");}
    row.exact_fixed_bank_limit_comparisons=routes.length;
   }
   rows.push(row);
  }
  out.actual_checkpoint_blob="6cac47a4b2227fa1469bb463d35ed37ffb3af1b6";out.actual_rows=rows;
 }
 out.arithmetic=G.stats();return out;
}
async function main(){
 const args=process.argv.slice(2),noBank=args.includes("--skip-bank"),files=args.filter(x=>x!=="--skip-bank");
 const[input,output]=files;if(!input||!output)throw Error("usage: node verify_avoided_realizer.mjs FULL_CHECKPOINT.json REPORT.json [--skip-bank]");
 const result=verifyAvoidedRealizer(JSON.parse(await fs.readFile(input,"utf8")),{bank:!noBank});
 await fs.writeFile(output,JSON.stringify(result,null,2)+"\n");console.log("PASS",result.toy.length*2,"complete toy searches",result.actual_rows.length,"actual controls",noBank?"trace checks":"and all1086 fixed-bank comparisons per control");
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
