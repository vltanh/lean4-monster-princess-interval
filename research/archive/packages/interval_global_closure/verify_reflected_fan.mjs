import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";
import reflectedModule from "./reflected_fan_cost.cjs";

export function reflectedPhysicalHelpers(G){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,abs=a=>a.cmp(0)<0?a.neg():a,
  unique=xs=>[...new Map(xs.map(Q).map(x=>[x.str(),x])).values()].sort((a,b)=>a.cmp(b));
 const fold=x=>O.s(abs(O.s(x)));
 function radial(row,t,x){
  const p=row.path.at(t),cuts=unique([row.lower,row.upper,x.s(p),Q(2).s(x).s(p),O.s(p)].filter(z=>z.cmp(row.lower)>=0&&z.cmp(row.upper)<=0));
  let mass=Z;for(let k=0;k+1<cuts.length;k++)if(fold(p.a(cuts[k].a(cuts[k+1]).dby(2))).cmp(x)<=0)mass=mass.a(cuts[k+1].s(cuts[k]));
  return mass.dby(row.width);
 }
 function signed(row,t,x){const r=radial(row,t,abs(x));return x.cmp(0)>=0?O.a(r).dby(2):O.s(r).dby(2);}
 function pathFor(row,q,H,kind,sign){
  const p=row.path,times=unique([Z,H,...p.t.filter(t=>t.cmp(H)>0?false:t.cmp(0)>0)]),out=[];
  function values(t){
   const x=p.at(t);
   if(kind==="raw")return[x.a(q),Q(2).s(x).s(q)];
   return[x.a(row.lower).a(row.width.m(q)),Q(2).s(x).s(row.upper).a(row.width.m(q)),O.s(row.width.dby(2)).a(row.width.m(q).dby(2))];
  }
  for(let k=0;k+1<times.length;k++){
   const a=times[k],b=times[k+1],va=values(a),vb=values(b),local=[a,b];
   for(let i=0;i<va.length;i++)for(let j=i+1;j<va.length;j++){
    const da=va[i].s(va[j]),db=vb[i].s(vb[j]);if(da.cmp(0)*db.cmp(0)<0)local.push(a.a(b.s(a).m(da.neg()).dby(db.s(da))));
   }
   for(const t of unique(local)){const v=values(t).reduce(min);out.push([t,v.m(sign)]);}
  }
  if(!out.length)out.push([Z,values(Z).reduce(min).m(sign)]);
  return new G.PLPath(out);
 }
 function rayTimes(row,m,j){
  const a=m.t[j],b=m.t[j+1],base=[a,b,...row.path.t.filter(t=>t.cmp(a)>0&&t.cmp(b)<0)];
  if(m.x[j].cmp(0)*m.x[j+1].cmp(0)<0)base.push(a.s(m.x[j].dby(m.v[j])));
  const cuts=unique(base),out=[...cuts];
  for(let k=0;k+1<cuts.length;k++){
   const l=cuts[k],r=cuts[k+1],xl=abs(m.at(l)),xr=abs(m.at(r)),pl=row.path.at(l),pr=row.path.at(r),
    el=[pl.a(row.lower),pl.a(row.upper),Q(2).s(pl).s(row.upper),Q(2).s(pl).s(row.lower)],
    er=[pr.a(row.lower),pr.a(row.upper),Q(2).s(pr).s(row.upper),Q(2).s(pr).s(row.lower)];
   for(let z=0;z<4;z++){const dl=xl.s(el[z]),dr=xr.s(er[z]);if(dl.cmp(0)*dr.cmp(0)<0)out.push(l.a(r.s(l).m(dl.neg()).dby(dr.s(dl))));}
  }return unique(out);
 }
 function rawScore(row,m){
  const H=m.t.at(-1),times=unique([Z,H,...row.path.t,...m.t].filter(t=>t.cmp(0)>=0&&t.cmp(H)<=0)),breaks=[row.lower,row.upper];
  for(let j=0;j<m.v.length;j++)if(m.x[j].cmp(0)*m.x[j+1].cmp(0)<0)times.push(m.t[j].s(m.x[j].dby(m.v[j])));
  for(const t of unique(times)){
   const p=row.path.at(t),x=abs(m.at(t));breaks.push(x.s(p),Q(2).s(x).s(p),O.s(p));
  }
  const cuts=unique(breaks.filter(z=>z.cmp(row.lower)>=0&&z.cmp(row.upper)<=0));let moment=Z,captures=0,linearity=0;
  for(let k=0;k+1<cuts.length;k++){
   const a=cuts[k],b=cuts[k+1],w=b.s(a);
   for(const sign of[1,-1]){
    const hit=u=>{captures++;const t=G.rawCapture(m,pathFor(row,a.a(w.m(u)),H,"raw",sign));if(t===null)throw Error("uncaptured raw reflected path");return t;},
     mid=hit(Q("1/2")),quarter=hit(Q("1/4")),three=hit(Q("3/4"));
    if(!quarter.a(three).dby(2).eq(mid))throw Error("raw reflected translation branch missing");linearity++;
    moment=moment.a(w.m(mid).dby(row.width.m(2)));
   }
  }return{cost:moment,captures,linearity,pieces:cuts.length-1};
 }
 function orderedSingle(row,m){
  const H=m.t.at(-1),values=[Z,O];
  for(let j=0;j<m.v.length;j++)for(const t of rayTimes(row,m,j))values.push(radial(row,t,abs(m.at(t))));
  const cuts=unique(values);let moment=Z,captures=0,linearity=0;
  for(let k=0;k+1<cuts.length;k++){
   const a=cuts[k],b=cuts[k+1],w=b.s(a);
   for(const sign of[1,-1]){
    const hit=u=>{captures++;const t=G.rawCapture(m,pathFor(row,a.a(w.m(u)),H,"ordered",sign));if(t===null)throw Error("uncaptured ordered reflected quantile");return t;},
     mid=hit(Q("1/2")),quarter=hit(Q("1/4")),three=hit(Q("3/4"));
    if(!quarter.a(three).dby(2).eq(mid))throw Error("ordered reflected quantile branch missing");linearity++;
    moment=moment.a(w.m(mid).dby(2));
   }
  }return{cost:moment,captures,linearity,pieces:cuts.length-1};
 }
 function orderedMixture(rows,weights,m){
  const W=weights.map(Q).reduce((a,b)=>a.a(b),Z),w=weights.map(x=>Q(x).dby(W)),cdf=(t,x)=>rows.reduce((s,r,i)=>s.a(signed(r,t,x).m(w[i])),Z);
  let L=cdf(m.t[0],m.x[0]),H=L,cost=Z,pieces=0;
  for(let j=0;j<m.v.length;j++){
   const d=m.v[j].eq(1)?1:m.v[j].eq(-1)?-1:0;if(!d)throw Error("unit physical mixture route");
   const times=unique(rows.flatMap(r=>rayTimes(r,m,j)));
   for(let k=0;k+1<times.length;k++){
    const a=times[k],b=times[k+1],fa=cdf(a,m.at(a)),fb=cdf(b,m.at(b));
    if(fb.s(fa).m(d).cmp(0)<0)throw Error("independent reflected CDF transport");
    if(d===1&&fb.cmp(H)>0){const l=max(H,fa),h=fb,t=a.a(b.s(a).m(l.a(h).dby(2).s(fa)).dby(fb.s(fa)));cost=cost.a(h.s(l).m(t));H=fb;}
    if(d===-1&&fb.cmp(L)<0){const l=fb,h=min(L,fa),t=a.a(b.s(a).m(l.a(h).dby(2).s(fa)).dby(fb.s(fa)));cost=cost.a(h.s(l).m(t));L=fb;}
    pieces++;
   }
  }
  if(!H.s(L).eq(1))throw Error("physical reflected mixture not complete");
  return{cost,pieces};
 }
 return{radial,signed,pathFor,rayTimes,rawScore,orderedSingle,orderedMixture};
}

export function verifyReflectedFans(){
 const E=createOracle(),G=germModule.createGermOracle(E),Q=G.Q,Z=G.ZERO,O=G.ONE,e=G.eps,T=reflectedModule.createReflectedFanTools(G),P=reflectedPhysicalHelpers(G),
  rows=[
   {id:"static_low",path:[[0,"1/4"]],lower:0,upper:"1/8"},
   {id:"static_partial_fold",path:[[0,"7/8"]],lower:0,upper:"1/4"},
   {id:"endpoint_avoiding",path:[[0,1]],lower:"1/8",upper:"1/2"},
   {id:"multiple_waves",path:[[0,"1/4"],["3/4",1],["7/4",0],["11/4",1]],lower:0,upper:"1/3"},
   {id:"subunit_waves",path:[[0,"1/2"],[1,1],["5/2","1/4"],[3,"3/4"]],lower:"1/8",upper:"1/2"},
   {id:"germ_window",path:[[0,"1/4"],["3/4",1],["7/4",0],["11/4",1]],lower:e.pow(3),upper:e.pow(2)},
   {id:"germ_base_and_window",path:[[Z,O],[O,e.pow(2)],[Q(2),O]],lower:0,upper:e.pow(2)}
  ],basis=T.prepareBasis(rows),a=Q("3/16").s(e),
  monsters=[
   {id:"center_sweep",path:[[0,0],[1,1],[3,-1]]},
   {id:"initial_endpoint",path:[[0,1],[2,-1],[4,1]]},
   {id:"interior_inward",path:[[0,"1/2"],["3/2",-1],["7/2",1]]},
   {id:"germ_positive_m2",path:[[Z,a],[O.s(a).dby(2),O.a(a).dby(2)],[2,-1],[4,1]]},
   {id:"three_direction_changes",path:[[0,"1/4"],["1/4","1/2"],["5/4","-1/2"],["11/4",1],["19/4",-1]]},
   {id:"near_endpoint_turn",path:[[Z,Z],[O.s(e),O.s(e)],[Q(3).s(e.m(2)),-1],[Q(5).s(e.m(2)),1]]}
  ].map(m=>({...m,path:new G.PLPath(m.path)}));
 let marginalChecks=0,orderedChecks=0,rawChecks=0,strictImprovements=0,directCaptures=0,linearityChecks=0,featureChecks=0,mixtureChecks=0,superplanes=0,causalPlanes=0,selectorEqualities=0;
 const cases=[];
 for(let i=0;i<basis.length;i++){
  const row=basis[i],law=T.law([row],[1]);let local=0;
  for(const t of[Q(0),Q("1/2"),O,Q(2),Q(4)])for(const x of[Q(-1),Q("-3/4"),Q("-1/4"),Z,Q("1/4"),Q("3/4"),O]){
   const expected=P.signed(row,t,x),actual=T.marginal(row,t,x);
   if(!actual.strict.eq(expected)||!actual.closed.eq(expected))throw Error("reflected CDF physical mismatch");marginalChecks++;
  }
  for(const m of monsters){
   const got=law.score(m.path,{gradient:true,selectors:true}),ordered=P.orderedSingle(row,m.path),raw=P.rawScore(row,m.path);
   if(!Q(got.exact_cost).eq(ordered.cost))throw Error("direct ordered reflected quantile capture mismatch: "+row.id+"/"+m.id);
   if(raw.cost.cmp(ordered.cost)>0)throw Error("rearrangement decreased reflected payoff");
   if(raw.cost.cmp(ordered.cost)<0)strictImprovements++;
   orderedChecks++;rawChecks++;directCaptures+=ordered.captures+raw.captures;linearityChecks+=ordered.linearity+raw.linearity;local++;
   const plane=T.historyPlane([row],m.path,got.selectors);if(!Q(plane.gradient[0]).eq(Q(got.exact_cost)))throw Error("active history plane mismatch");selectorEqualities++;
   for(let j=0;j<m.path.v.length;j++){
    const times=P.rayTimes(row,m.path,j);let physical=Z;for(let k=0;k+1<times.length;k++)physical=physical.a(times[k+1].s(times[k]).m(P.signed(row,times[k],m.path.at(times[k])).a(P.signed(row,times[k+1],m.path.at(times[k+1])))).dby(2));
    const actual=T.featureIntegral(row,m.path.vertices[j],m.path.v[j].eq(1)?1:-1,m.path.t[j],m.path.t[j+1]);
    if(!actual.eq(physical))throw Error("reflected component primitive mismatch");featureChecks++;
   }
  }
  cases.push({row:row.id,supplied_routes:local});
 }
 const mixed=[basis[3],basis[4],basis[2]],weights=[["2/5","2/5","1/5"],["1/7","2/7","4/7"],[1,0,0],[0,1,0]];
 for(const m of monsters.slice(0,5)){
  const scores=weights.map(w=>T.law(mixed,w).score(m.path,{gradient:true,selectors:true}));
  for(let i=0;i<weights.length;i++){
   const physical=P.orderedMixture(mixed,weights[i],m.path);if(!physical.cost.eq(Q(scores[i].exact_cost)))throw Error("independent reflected mixture moment mismatch");mixtureChecks++;
   const plane=T.historyPlane(mixed,m.path,scores[i].selectors);for(let k=0;k<mixed.length;k++){if(!Q(plane.gradient[k]).eq(Q(scores[i].gradient[k])))throw Error("mixed active history coefficient mismatch");selectorEqualities++;}
   for(let j=0;j<weights.length;j++){
    const W=weights[j].map(Q).reduce((a,b)=>a.a(b),Z),bound=plane.gradient.reduce((s,x,k)=>s.a(Q(x).m(Q(weights[j][k])).dby(W)),Z);
    if(Q(scores[j].exact_cost).cmp(bound)>0)throw Error("reflected weight superplane violation");superplanes++;
   }
  }
  const arbitrary=[];
  for(let j=0;j<m.path.v.length;j++){
   const left=m.path.t[j],right=m.path.t[j+1],mid=left.a(right).dby(2),d=m.path.v[j].eq(1)?1:-1;
   arbitrary.push({start:left.str(),end:mid.str(),upper:{time:"0"},lower:{time:"0"}},
    {start:mid.str(),end:right.str(),upper:d===1?{current:true}:{time:"0"},lower:d===-1?{current:true}:{time:"0"}});
  }
  const plane=T.historyPlane(mixed,m.path,arbitrary);
  for(let j=0;j<weights.length;j++){
   const W=weights[j].map(Q).reduce((a,b)=>a.a(b),Z),bound=plane.gradient.reduce((s,x,k)=>s.a(Q(x).m(Q(weights[j][k])).dby(W)),Z);
   if(Q(scores[j].exact_cost).cmp(bound)>0)throw Error("causal nonactive history plane violation");causalPlanes++;
  }
 }
 let rejected=0;
 for(const bad of[
  ()=>T.prepareBasis([{path:[[0,"-1/10"]],delta:"1/4"}]),
  ()=>T.prepareBasis([{path:[[0,"1/2"]],lower:0,upper:2}]),
  ()=>T.historyPlane([basis[0]],monsters[0].path,[{start:0,end:3,upper:{time:1},lower:{time:0}}])
 ]){try{bad();}catch{rejected++;}}
 if(rejected!==3)throw Error("invalid reflected input not rejected");
 return{scope:"Exact reflected-fan marginal, ordered supplied-route cost, weight supergradients and causal history upper planes. No basis-optimality or unrestricted-response claim.",
  cases,physical_marginal_checks:marginalChecks,direct_single_ordered_scores:orderedChecks,direct_raw_scores:rawChecks,strict_rearrangement_improvements:strictImprovements,
  direct_segment_capture_checks:directCaptures,affine_capture_branch_checks:linearityChecks,component_feature_integral_checks:featureChecks,
  independent_mixed_rank_moments:mixtureChecks,weight_superplane_checks:superplanes,causal_nonactive_planes:causalPlanes,history_coefficient_equalities:selectorEqualities,
  invalid_inputs_rejected:rejected,arithmetic:G.stats()};
}
async function main(){const[out]=process.argv.slice(2);if(!out)throw Error("usage: node verify_reflected_fan.mjs REPORT.json");const r=verifyReflectedFans();await fs.writeFile(out,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.direct_single_ordered_scores,"direct ordered",r.direct_segment_capture_checks,"physical captures",r.weight_superplane_checks,"superplanes");}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
