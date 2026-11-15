import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";
import dpModule from "./static_tail_dp.cjs";
import fanModule from "./germ_translation_fan.cjs";
import {stationaryPhysicalCost} from "./verify_static_tail_turns.mjs";

export function verifyStaticTailDP(){
 const E=createOracle(),G=germModule.createGermOracle(E),Q=G.Q,Z=G.ZERO,O=G.ONE,e=G.eps,
  DP=dpModule.createStaticTailDP(G),F=fanModule.createTranslationFan(G),
  fanInputs=[
   [{tail_position:"1",lower:"-1/4",upper:"1/8",weight:"2/3"},{tail_position:"1/4",lower:"0",upper:"1/2",weight:"1/3"}],
   [{tail_position:O.s(e).str(),lower:"0",upper:e.m(2).str(),weight:"1"}]
  ],
  measures=[
   {name:"uniform",cells:[[-1,1,"1/2"]],atoms:[]},
   {name:"asymmetric_steps",cells:[[-1,"-1/3","1/5"],["-1/3","1/4","2/3"],["1/4",1,"1/7"]],atoms:[[-1,"1/11"],["1/4","1/13"],[1,"1/17"]]},
   {name:"pure_atoms",cells:[],atoms:[[-1,"1/10"],["-3/5","3/10"],["1/5","2/5"],[1,"1/5"]]},
   {name:"germ_center_band",cells:[[e.neg().str(),e.str(),O.dby(e.m(2)).str()]],atoms:[[-1,"1/7"],[1,"1/9"]]},
   ...fanInputs.map((f,i)=>({name:"fan_tail:"+i,...DP.fromFans(f)}))
  ],starts=[Q(0),Q("-3/7"),Q("3/5"),e.dby(2)];
 let exhaustiveRoutes=0,physicalPieces=0,physicalAtoms=0,cdfChecks=0,rankChecks=0;const cases=[];
 function prepared(raw){return{cells:raw.cells.map(c=>c.map(Q)),atoms:raw.atoms.map(c=>c.map(Q))};}
 function physical(raw,route){const p=stationaryPhysicalCost(G,prepared(raw),new G.PLPath(route));physicalPieces+=p.pieces;physicalAtoms+=p.atoms;return p.cost;}
 function cdf(raw,x,closed){let value=Z;for(const[a0,b0,f0]of raw.cells){const a=Q(a0),b=Q(b0),f=Q(f0),end=x.cmp(b)<0?x:b;if(end.cmp(a)>0)value=value.a(end.s(a).m(f));}
  for(const[y0,w0]of raw.atoms){const cmp=Q(y0).cmp(x);if(cmp<0||closed&&cmp===0)value=value.a(Q(w0));}return value;}
 for(const measure of measures)for(const start of starts){
  const answer=DP.solve(measure,start,{absoluteTime:"3/7"}),m=DP.compile(measure,[start]),D=m.D,s=D.findIndex(x=>x.eq(start));let best=null,routeCount=0;
  function visit(l,r,t,x,vertices){
   if(l===0&&r+1===D.length){const v=physical(measure,vertices);if(best===null||v.cmp(best)<0)best=v;routeCount++;return;}
   if(l>0){const y=D[l-1],dt=x.s(y);visit(l-1,r,t.a(dt),y,vertices.concat([[t.a(dt),y]]));}
   if(r+1<D.length){const y=D[r+1],dt=y.s(x);visit(l,r+1,t.a(dt),y,vertices.concat([[t.a(dt),y]]));}
  }
  visit(s,s,Z,start,[[Z,start]]);exhaustiveRoutes+=routeCount;
  const actual=physical(measure,answer.relative_route);
  if(!Q(answer.relative_cost).eq(best)||!actual.eq(best))throw Error("stationary DP differs from exhaustive physical boundary routes");
  if(!Q(answer.absolute_moment).eq(best.a(m.total.m("3/7"))))throw Error("stationary absolute time shift");
  cases.push({measure:measure.name,start:start.str(),cost:answer.relative_cost,boundaries:D.length,states:answer.state_count,exhaustive_routes:routeCount,route:answer.relative_route});
 }
 for(const input of fanInputs){
  const m=DP.fromFans(input),full=DP.compile(m),rows=input.map(r=>F.prepareInterval([[0,r.tail_position]],r.lower,r.upper)),ws=input.map(r=>Q(r.weight)),W=ws.reduce((a,b)=>a.a(b),Z),
   points=full.D.concat(full.D.slice(1).map((x,i)=>x.a(full.D[i]).dby(2)));
  for(const x of points)for(const closed of [false,true]){
   let expected=Z;rows.forEach((r,i)=>{expected=expected.a(F.marginal(r,0,x)[closed?"closed":"strict"].m(ws[i]).dby(W));});
   if(!cdf(m,x,closed).eq(expected))throw Error("fan-to-static marginal mismatch");cdfChecks++;
  }
  for(const[a,b]of [[0,"1/3"],["1/5","4/5"],["1/2","1/2"]]){
   const lo=Q(a).m(full.total),hi=Q(b).m(full.total),cut=DP.removeRankBand(m,lo,hi),cm=DP.compile(cut),
    qs=[...full.D,...cm.D,...cm.D.slice(1).map((x,i)=>x.a(cm.D[i]).dby(2))];
   for(const x of qs)for(const closed of [false,true]){
    const original=cdf(m,x,closed),expected=(original.cmp(lo)<0?original:lo).a(original.cmp(hi)>0?original.s(hi):Z);
    if(!cdf(cut,x,closed).eq(expected))throw Error("ordered rank-band survivor CDF mismatch");rankChecks++;
   }
   const answer=DP.solve(cut,0);if(!physical(cut,answer.relative_route).eq(Q(answer.relative_cost)))throw Error("survivor DP witness mismatch");
  }
 }
 return{scope:"Exact stationary-tail DP with independent exhaustive physical boundary-route verification; fan marginal and ordered survivor-band adapters are checked separately.",
  cases,exhaustive_boundary_routes:exhaustiveRoutes,independent_affine_spatial_pieces:physicalPieces,independent_atom_captures:physicalAtoms,
  fan_marginal_checks:cdfChecks,ordered_rank_survivor_checks:rankChecks,arithmetic:G.stats()};
}
async function main(){const[out]=process.argv.slice(2);if(!out)throw Error("usage: node verify_static_tail_dp.mjs REPORT.json");
 const r=verifyStaticTailDP();await fs.writeFile(out,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.cases.length,"states",r.exhaustive_boundary_routes,"exhaustive physical routes",r.fan_marginal_checks,"fan marginals",r.ordered_rank_survivor_checks,"survivor traces");}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
