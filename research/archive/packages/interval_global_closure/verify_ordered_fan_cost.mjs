import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";
import fanModule from "./germ_translation_fan.cjs";
import orderedModule from "./ordered_fan_cost.cjs";

export function verifyOrderedFans(){
 const E=createOracle(),G=germModule.createGermOracle(E),Q=G.Q,Z=G.ZERO,O=G.ONE,e=G.eps,
  OT=orderedModule.createOrderedFanTools(G,fanModule),T=OT.fan;
 const near=Q("1/4").a(e).s(e.pow(2)),
  profiles=[
   [[0,"1/2"]],
   [[0,"1/4"],["1/4","1/2"],["1/2","1/4"],[1,"3/4"]],
   [[0,0],["1/4","1/4"],["1/2",0],["3/2",1]],
   [[0,1]],
   [[0,Q("1/4").a(e)],[near,e.pow(2)],[near.a(O.s(e.pow(2))),1]]
  ],
  intervals=[[0,"1/8"],["-1/16","1/8"],[e.pow(2),e.pow(2).m(2)]],
  rows=profiles.flatMap((path,i)=>intervals.map(([lower,upper],j)=>({id:i+":"+j,path,lower,upper}))),
  basis=OT.prepareBasis(rows),
  monsters=[
   [[0,-1],[2,1]],[[0,0],[1,1],[3,-1]],[[0,"1/4"],["5/4",-1],["13/4",1]],
   [[0,"-1/4"],["5/4",1],["13/4",-1]],
   [[0,0],[O.s(e),O.s(e)],[Q(3).s(e.m(2)),-1],[Q(5).s(e.m(2)),1]],
   [[0,0],["1/4","1/4"],["1/2",0],["3/4","-1/4"],[1,0],[2,1],[4,-1]],
   [[0,"2/5"],["1/5","3/5"],["11/10","-3/10"],["12/5",1],["22/5",-1]]
  ].map(p=>new G.PLPath(p));
 let singleEqual=0,staticEqual=0,rawBounds=0,strictImprovements=0,superplanes=0,primitiveChecks=0,segments=0;
 const samples=[];
 const weightSets=[basis.map(()=>Q(1)),basis.map((_,i)=>Q((i%4)+1)),basis.map((_,i)=>Q(i%3===0?1:0))];
 for(const weights of weightSets){
  const sum=weights.reduce((a,b)=>a.a(b),Z),w=weights.map(x=>x.dby(sum)),law=OT.law(basis,w);
  for(const m of monsters){
   const result=law.score(m,{gradient:true}),cost=Q(result.exact_cost),g=result.gradient.map(Q);
   let raw=Z;for(let i=0;i<basis.length;i++)if(!w[i].eq(0))raw=raw.a(w[i].m(Q(T.score(basis[i],m).exact_cost)));
   if(cost.cmp(raw)<0)throw Error("ordering worsened physical mixture");
   rawBounds++;if(cost.cmp(raw)>0)strictImprovements++;segments+=result.pieces;
   for(const j of[0,4,8,12]){
    const v=w.map((x,i)=>x.m("3/4").a(i===j?Q("1/4"):Z)),
     other=Q(OT.law(basis,v).score(m).exact_cost),bound=v.reduce((s,x,i)=>s.a(x.m(g[i])),Z);
    if(other.cmp(bound)>0)throw Error("global concave superplane inequality");superplanes++;
   }
   samples.push({cost:cost.str(),raw:raw.str(),gradient_euler:result.euler,pieces:result.pieces});
  }
 }
 for(let i=0;i<basis.length;i++){
  const law=OT.law([basis[i]],[1]),row=basis[i];
  for(const m of monsters){
   const exact=Q(law.score(m,{gradient:true}).exact_cost),raw=Q(T.score(row,m).exact_cost);
   if(i%3===0||Math.floor(i/3)===0||Math.floor(i/3)===3){
    if(!exact.eq(raw))throw Error("known ordered physical family equality");singleEqual++;
   }
   for(let j=0;j<m.v.length;j++){
    const a=m.vertices[j],b=m.vertices[j+1],d=m.v[j].eq(1)?1:-1,
     left=a[0].a(b[0].s(a[0]).dby(3)),aa=[left,a[1].a(left.s(a[0]).m(d))],
     points=law.trace(aa,b,d);
    let area=Z;for(let k=0;k+1<points.length;k++)area=area.a(points[k].f.a(points[k+1].f).m(points[k+1].t.s(points[k].t)).dby(2));
    const inverse=law.featureIntegral(row,a,d,left,b[0]);
    if(!area.eq(inverse))throw Error("CDF area versus independent inverse band primitive");primitiveChecks++;
   }
  }
 }
 const statics=OT.prepareBasis([{path:[[0,"1/4"]],lower:"-1/8",upper:"1/8"},{path:[[0,1]],lower:"-1/4",upper:"1/8"},{path:[[0,e]],lower:e.neg().m(2),upper:e.m(2)}]),
  ws=[Q("1/3"),Q("1/2"),Q("1/6")],sl=OT.law(statics,ws);
 for(const m of monsters){const c=Q(sl.score(m,{gradient:true}).exact_cost),raw=statics.reduce((s,r,i)=>s.a(ws[i].m(Q(T.score(r,m).exact_cost))),Z);if(!c.eq(raw))throw Error("static raw equals quantile");staticEqual++;}
 if(!strictImprovements)throw Error("missing strict rearrangement fixture");
 return{scope:"Exact supplied-route ordered fan scoring and concave weight supergradients; no unrestricted response or game bound.",
  known_ordered_physical_equalities:singleEqual,static_mixture_equalities:staticEqual,
  raw_dominance_checks:rawBounds,strict_rearrangement_improvements:strictImprovements,
  weight_superplane_checks:superplanes,CDF_area_inverse_primitive_checks:primitiveChecks,
  mixed_trace_pieces:segments,samples,arithmetic:G.stats()};
}
async function main(){
 const[out]=process.argv.slice(2);if(!out)throw Error("usage: node verify_ordered_fan_cost.mjs REPORT.json");
 const r=verifyOrderedFans();await fs.writeFile(out,JSON.stringify(r,null,2)+"\n");
 console.log("PASS",r.raw_dominance_checks,r.weight_superplane_checks,r.CDF_area_inverse_primitive_checks);
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
