import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";

function unique(G,values){const out=[...new Map(values.map(G.Q).map(x=>[x.str(),x])).values()];out.sort((a,b)=>a.cmp(b));return out;}
function routeFromPositions(G,positions){let t=G.ZERO;const p=positions.map(G.Q),out=[[t,p[0]]];for(let i=1;i<p.length;i++){const d=p[i].s(p[i-1]);t=t.a(d.cmp(0)<0?d.neg():d);out.push([t,p[i]]);}return new G.PLPath(out);}
function prepareMeasure(G,m){return{cells:m.cells.map(([a,b,f])=>[G.Q(a),G.Q(b),G.Q(f)]),atoms:m.atoms.map(([x,w])=>[G.Q(x),G.Q(w)])};}
function densityAt(G,m,x){let z=G.ZERO;for(const[a,b,f]of m.cells)if(x.cmp(a)>0&&x.cmp(b)<0)z=z.a(f);return z;}

/** Exact stationary record integral, independent of direct path intersections. */
export function stationaryRecordCost(G,measure,monster){
 let lo=monster.x[0],hi=lo,cost=G.ZERO;const min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b;
 function band(a,b,c,d,includeLeft,includeRight){
  let value=G.ZERO;for(const[l,r,f]of measure.cells){const u=max(a,l),v=min(b,r);if(v.cmp(u)>0)value=value.a(f.m(c.m(v.s(u)).a(v.m(v).s(u.m(u)).m(d).dby(2))));}
  for(const[x,w]of measure.atoms)if((includeLeft?x.cmp(a)>=0:x.cmp(a)>0)&&(includeRight?x.cmp(b)<=0:x.cmp(b)<0))value=value.a(w.m(c.a(x.m(d))));return value;
 }
 for(let k=0;k<monster.v.length;k++){
  const v=monster.v[k];if(!v.eq(1)&&!v.eq(-1))throw Error("stationary verifier expects unit legs");
  const x=monster.x[k+1],t=monster.t[k],start=monster.x[k];
  if(v.eq(1)&&x.cmp(hi)>0){cost=cost.a(band(hi,x,t.s(start),1,false,true));hi=x;}
  if(v.eq(-1)&&x.cmp(lo)<0){cost=cost.a(band(x,lo,t.a(start),-1,true,false));lo=x;}
 }
 return cost;
}

/** Independent exact spatial integration of direct chronological captures. */
export function stationaryPhysicalCost(G,measure,monster){
 let cost=G.ZERO,pieces=0,atoms=0;
 for(const[a,b,f]of measure.cells){
  const cuts=unique(G,[a,b,...monster.x.filter(x=>x.cmp(a)>0&&x.cmp(b)<0)]);
  for(let i=0;i+1<cuts.length;i++){
   const x=cuts[i].a(cuts[i+1]).dby(2),hit=G.rawCapture(monster,new G.PLPath([[0,x]]));
   if(hit===null)throw Error("stationary target missed");cost=cost.a(f.m(cuts[i+1].s(cuts[i])).m(hit));pieces++;
  }
 }
 for(const[x,w]of measure.atoms){const hit=G.rawCapture(monster,new G.PLPath([[0,x]]));if(hit===null)throw Error("stationary atom missed");cost=cost.a(w.m(hit));atoms++;}
 return{cost,pieces,atoms};
}

export function verifyStaticTailTurns(){
 const E=createOracle(),G=germModule.createGermOracle(E),Q=G.Q,Z=G.ZERO,e=G.eps,
  knots=[-1,"-3/4","-1/2","-1/4",0,"1/4","1/2","3/4",1],
  measures=[
   {name:"uniform",cells:[[-1,1,"1/2"]],atoms:[]},
   {name:"asymmetric_steps_and_atoms",cells:knots.slice(1).map((b,i)=>[knots[i],b,["1/7","2/9","3/8","0","5/11","1/3","2/5","1/13"][i]]),atoms:[["-1","1/19"],["-5/8","1/23"],[0,"1/29"],["3/8","1/17"],["5/8","1/31"],[1,"1/37"]]},
   {name:"overlapping_fan_intervals",cells:[["-7/8","3/8","2/5"],["-1/4","3/4","1/3"],["1/2",1,"1/7"]],atoms:[[-1,"1/8"],["-1/2","1/11"],["1/2","1/9"],[1,"1/6"]]},
   {name:"atomic_only",cells:[],atoms:[[-1,"1/101"],["-3/4","1/7"],["-1/2","2/9"],["1/2","2/9"],["3/4","1/7"],[1,"1/101"]]},
  ],geometries=[
   [0,"-1/8","1/8","-1/4","-3/4","7/8"],
   ["-1/5","-2/5","1/5","-3/5","-4/5","9/10"],
   ["1/5","-1/5","1/3","-2/5","-4/5","19/20"],
  ];
 let physical=0,pieces=0,atomChecks=0,curvatures=0,atomTraces=0,collisions=0;const examples=[];
 const check=(m,p)=>{const direct=stationaryPhysicalCost(G,m,p),record=stationaryRecordCost(G,m,p);if(!direct.cost.eq(record))throw Error("stationary record/physical mismatch");physical++;pieces+=direct.pieces;atomChecks+=direct.atoms;return record;};
 for(const raw of measures){
  const m=prepareMeasure(G,raw);
  for(const geometry of geometries)for(const sign of [1,-1]){
   const [start,oldLeft,oldRight,previousLeft,nextLeft,nextRight]=geometry.map(Q),positions=y=>[start,oldLeft,oldRight,previousLeft,y,nextLeft,nextRight,Q(-1),Q(1)].map(x=>x.m(sign)),
    route=y=>routeFromPositions(G,positions(y)),
    breaks=unique(G,[oldRight,nextRight,...m.cells.flatMap(([a,b])=>[a.m(sign),b.m(sign)]),...m.atoms.map(([x])=>x.m(sign))].filter(x=>x.cmp(oldRight)>=0&&x.cmp(nextRight)<=0));
   for(let j=0;j+1<breaks.length;j++){
    const a=breaks[j],b=breaks[j+1],mid=a.a(b).dby(2),h=b.s(a).dby(4),beta=densityAt(G,m,mid.m(sign)),
     cm=check(m,route(mid.s(h))),c0=check(m,route(mid)),cp=check(m,route(mid.a(h))),second=cm.a(cp).s(c0.m(2)).dby(h.m(h));
    if(!second.eq(beta.m(-4)))throw Error("static turning curvature mismatch");curvatures++;
    // Closed endpoint values include any atom reached exactly there.
    const ca=check(m,route(a)),cb=check(m,route(b));if(ca.cmp(c0)>0&&cb.cmp(c0)>0)throw Error("turn cannot be pushed to a cell boundary");
   }
   for(const[x,w]of m.atoms){const a=x.m(sign);if(a.cmp(oldRight)<=0||a.cmp(nextRight)>=0)continue;
    const at=check(m,route(a)),below=check(m,route(a.s(e))).limit(),above=check(m,route(a.a(e))).limit(),jump=w.m(a.s(nextLeft)).m(2);
    if(!G.Q(below.str()).s(at).eq(jump)||!G.Q(above.str()).eq(at))throw Error("closed atom turn trace mismatch");atomTraces++;
   }
   const lower=positions(oldRight),lowerDeleted=lower.filter((_,i)=>i!==3&&i!==4),upper=positions(nextRight),upperDeleted=upper.filter((_,i)=>i!==5&&i!==6),
    cl=check(m,routeFromPositions(G,lower)),dl=check(m,routeFromPositions(G,lowerDeleted)),cu=check(m,routeFromPositions(G,upper)),du=check(m,routeFromPositions(G,upperDeleted));
   if(dl.cmp(cl)>0||du.cmp(cu)>0)throw Error("colliding unproductive excursion cannot be deleted");collisions+=2;
  }
  examples.push({measure:raw.name});
 }
 // Static does not by itself mean that the direct endpoint tour is optimal.
 const a=Q("99/100"),tiny=Q("1/1000000"),m=prepareMeasure(G,{cells:[],atoms:[[a.neg(),Q("499999/1000000")],[a,Q("499999/1000000")],[-1,tiny],[1,tiny]]}),
  detour=routeFromPositions(G,[0,a.neg(),1,-1]),direct=routeFromPositions(G,[0,-1,1]),cd=check(m,detour),ce=check(m,direct);
 if(!cd.eq(Q("495001/250000"))||!ce.eq(Q("99500001/50000000"))||cd.cmp(ce)>=0)throw Error("stationary nontrivial route fixture");
 return{scope:"Exact static piecewise-constant-density turning-point identities and atom/collision boundaries; the finite/infinite-history reduction is stated separately in the proof note.",
  exact_second_derivative_checks:curvatures,closed_atom_trace_checks:atomTraces,collision_deletion_checks:collisions,
  independent_physical_route_comparisons:physical,independent_affine_spatial_pieces:pieces,independent_atom_captures:atomChecks,measures:examples,
  stationary_countercheck:{start:"0",interior_turn:a.neg().str(),detour_cost:cd.str(),direct_endpoint_cost:ce.str(),detour_completion:detour.t.at(-1).str()},arithmetic:G.stats()};
}
async function main(){const[out]=process.argv.slice(2);if(!out)throw Error("usage: node verify_static_tail_turns.mjs REPORT.json");const r=verifyStaticTailTurns();await fs.writeFile(out,JSON.stringify(r,null,2)+"\n");console.log("PASS",JSON.stringify(r));}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
