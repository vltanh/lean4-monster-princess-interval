import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";
import fanModule from "./germ_translation_fan.cjs";

/** Independent physical integration.  The only shared operations with the
 * inverse-band engine are exact arithmetic, PL-path legality and chronological
 * segment intersection.  Each fan interval is integrated at its midpoint only
 * after all changes of the affine first-hit branch have been inserted. */
export function physicalFanScore(G,p,m,delta,{details=false}={}){
 const Q=G.Q,Z=G.ZERO,bounds=Array.isArray(delta)?delta.map(Q):[Q(delta).neg(),Q(delta)],H=m.t.at(-1),
  min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,
  clip=x=>max(Q(-1),min(Q(1),x)),uniq=xs=>{
   const out=[...new Map(xs.map(x=>[x.str(),x])).values()];out.sort((a,b)=>a.cmp(b));return out;};
 const times=uniq([Z,H,...p.t,...m.t].filter(t=>t.cmp(0)>=0&&t.cmp(H)<=0));
 let total=Z,count=0,clippingCrossings=0;const signs=[];
 for(const sign of [1,-1]){
  const lo=sign===1?bounds[0]:bounds[1].neg(),hi=sign===1?bounds[1]:bounds[0].neg();
  const cuts=uniq([lo,hi,...times.map(t=>m.at(t).s(p.at(t).m(sign)))].filter(z=>z.cmp(lo)>=0&&z.cmp(hi)<=0));
  let moment=Z;const pieces=[];
  for(let j=0;j+1<cuts.length;j++){
   const left=cuts[j],right=cuts[j+1],z=left.a(right).dby(2),vertices=[];
   for(let k=0;k+1<times.length;k++){
    const a=times[k],b=times[k+1],pa=p.at(a).m(sign).a(z),pb=p.at(b).m(sign).a(z),local=[a,b];
    if(!pa.eq(pb))for(const bound of [-1,1]){
     const q=Q(bound);if(q.cmp(min(pa,pb))>0&&q.cmp(max(pa,pb))<0){
      local.push(a.a(b.s(a).m(q.s(pa)).dby(pb.s(pa))));clippingCrossings++;
     }
    }
    for(const t of uniq(local))vertices.push([t,clip(p.at(t).m(sign).a(z))]);
   }
   if(!vertices.length)vertices.push([Z,clip(p.at(Z).m(sign).a(z))]);
   const translated=new G.PLPath(vertices),hit=G.rawCapture(m,translated);
   if(hit===null||hit.cmp(H)>0)throw Error("physical fan fixture not fully captured");
   moment=moment.a(right.s(left).m(hit));count++;
   if(details)pieces.push({left:left.str(),right:right.str(),midpoint:z.str(),hit:hit.str()});
  }
  const cost=moment.dby(hi.s(lo));total=total.a(cost);
  signs.push({sign,cost:cost.str(),pieces});
 }
 return{cost:total.dby(2),pieces:count,clipping_crossings:clippingCrossings,orientations:signs};
}

export function verifyTranslationFan(fixtures=[]){
 const E=createOracle(),G=germModule.createGermOracle(E),T=fanModule.createTranslationFan(G),Q=G.Q,e=G.eps,Z=G.ZERO,O=G.ONE,
  paths=[
   {name:"center_stationary",path:[[0,0]]},
   {name:"interior_stationary",path:[[0,"1/2"]]},
   {name:"near_endpoint_stationary",path:[[0,O.s(e)]]},
   {name:"endpoint_stationary",path:[[0,1]]},
   {name:"outgoing_and_clipped",path:[[0,"1/4"],["3/4",1]]},
   {name:"isolated_center_bounce",path:[[0,"3/4"],["3/4",0],["7/4",1]]},
   {name:"two_waves",path:[[0,"1/4"],["1/4",0],["3/4","1/2"],["5/4",0],["9/4",1]]},
  ];
 for(const f of fixtures)for(let j=0;j<f.paths.length;j++)paths.push({name:f.name+":"+j,path:f.paths[j]});
 const a=Q("3/16").s(e),g=e.pow(2),j=e.pow(3),
  routes=[
   {name:"right_sweep",path:[[0,0],[1,1],[3,-1]]},
   {name:"left_sweep",path:[[0,0],[1,-1],[3,1]]},
   {name:"initial_right_clipping_atom",path:[[0,1],[2,-1],[4,1]]},
   {name:"initial_left_clipping_atom",path:[[0,-1],[2,1],[4,-1]]},
   {name:"interior_start",path:[[0,"1/2"],["3/2",-1],["7/2",1]]},
   {name:"two_turns",path:[[0,"1/4"],["1/4",0],["3/4","1/2"],["9/4",-1],["17/4",1]]},
   {name:"germ_positive_m2",path:[[Z,a],[O.s(a).dby(2),O.a(a).dby(2)],[2,-1],[4,1]]},
   {name:"nested_early_inward",path:[[Z,O.s(g)],[j.dby(2),O.s(g).s(j.dby(2))],[g.a(j.dby(2)),O.s(j.dby(2))],[Q(2).a(g),-1],[Q(4).a(g),1]]},
  ].map(r=>({...r,path:new G.PLPath(r.path)}));
 const widths=[Q("1/10"),Q("1/2"),Q(2),e.dby(3),e.pow(2),[Z,Q("1/10")],[Q("-1/2"),Z],[Q("1/4"),Q("3/4")],[e.pow(3),e.pow(2)]],checks=[];
 let equalities=0,pieces=0,clipping=0,marginals=0;
 for(const data of paths){
  const p=new G.PLPath(data.path);let local=0;
  for(const delta of widths){
   const bounds=Array.isArray(delta)?delta:[delta.neg(),delta];
   const row=T.prepareInterval(p,bounds[0],bounds[1],{id:data.name,provenance:"exact fixture"});
   for(const m of routes){
    const actual=T.score(row,m.path,{trace:true}),physical=physicalFanScore(G,p,m.path,delta);
    if(!actual.complete||!Q(actual.exact_cost).eq(physical.cost))throw Error("fan moment mismatch: "+JSON.stringify({path:data.name,interval:bounds.map(x=>x.str()),monster:m.name,actual,physical:physical.cost.str()}));
    equalities++;local++;pieces+=physical.pieces;clipping+=physical.clipping_crossings;
   }
   for(const time of [Q(0),Q("3/4"),Q(2)])for(const x of [Q(-1),Q("-1/2"),Z,Q("1/2"),O]){
    let strict=Z,closed=Z;
    for(const sign of [1,-1]){
     const center=p.at(time).m(sign),lo=sign===1?bounds[0]:bounds[1].neg(),hi=sign===1?bounds[1]:bounds[0].neg(),cut=x.s(center),breaks=[lo,hi];
     if(cut.cmp(lo)>0&&cut.cmp(hi)<0)breaks.splice(1,0,cut);
     for(let k=0;k+1<breaks.length;k++){
      const z=breaks[k].a(breaks[k+1]).dby(2),v=center.a(z),clipped=v.cmp(-1)<0?Q(-1):v.cmp(1)>0?O:v,
       mass=breaks[k+1].s(breaks[k]).dby(row.width.m(2)),cmp=clipped.cmp(x);
      if(cmp<0)strict=strict.a(mass);if(cmp<=0)closed=closed.a(mass);
     }
    }
    const actual=T.marginal(row,time,x);if(!actual.strict.eq(strict)||!actual.closed.eq(closed))throw Error("fan marginal mismatch");marginals++;
   }
  }
  checks.push({path:data.name,comparisons:local});
 }
 // A fixed atom-start attack improves after translation, but moving the
 // Monster start to the upper edge recovers an early capture.  These are two
 // different exact physical rows/columns, not a continuity assertion.
 const delta=Q("1/64"),p=new G.PLPath([[0,"1/2"]]),row=T.prepare(p,delta,{id:"stationary-edge-test"}),
  fixed=new G.PLPath([[0,"1/2"],["3/2",-1],["7/2",1]]),b=Q("1/2").a(delta),
  adaptive=new G.PLPath([[Z,b],[O.a(b),-1],[Q(3).a(b),1]]),
  fixedScore=T.score(row,fixed),adaptiveScore=T.score(row,adaptive);
 if(!Q(fixedScore.exact_cost).eq(Q("5/4").a(delta.dby(4)))||!Q(adaptiveScore.exact_cost).eq(b))throw Error("stationary fan-edge identity");
 const outward=T.prepareInterval(p,Z,delta,{id:"outward-stationary-edge-test"}),outFixed=T.score(outward,fixed),outEdge=T.score(outward,adaptive);
 if(!Q(outFixed.exact_cost).eq(Q(2).a(delta.dby(2)))||!Q(outEdge.exact_cost).eq(b))throw Error("outward stationary fan-edge identity");
 return{scope:"Exact uniform interval translation fans against supplied unit Monsters only; continuous z integration is exact, with no quadrature or full-response claim.",
  outward_edge_example:{interval:["0",delta.str()],fixed_monster_cost:outFixed.exact_cost,edge_monster_cost:outEdge.exact_cost},
  exact_fan_equalities:equalities,independent_midpoint_pieces:pieces,independent_clipping_crossings:clipping,exact_strict_closed_marginal_checks:marginals,
  fixture_checks:checks,adaptive_edge_example:{delta:delta.str(),fixed_monster_cost:fixedScore.exact_cost,edge_monster_cost:adaptiveScore.exact_cost},
  cache:T.stats(),arithmetic:G.stats()};
}

async function main(){
 const[input,output]=process.argv.slice(2);if(!output)throw Error("usage: node verify_translation_fan.mjs FIXTURES.json REPORT.json");
 const r=verifyTranslationFan(JSON.parse(await fs.readFile(input,"utf8")));await fs.writeFile(output,JSON.stringify(r,null,2)+"\n");
 console.log("PASS",r.exact_fan_equalities,"exact fan scores;",r.independent_midpoint_pieces,"independent affine pieces;",r.independent_clipping_crossings,"clipping crossings");
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
