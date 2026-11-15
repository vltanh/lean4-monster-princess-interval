import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";

function verifyAvoidedCenterBounce(L,face=null,upper=null,sourceCertificate=null){
 const Q=L.Q,Z=Q(0),O=Q(1),reports=[];
 function assert(ok,msg){if(!ok)throw Error(msg);}
 function pairPath(tau,eps){
  tau=Q(tau);eps=Q(eps);
  assert(tau.cmp(0)>0&&tau.cmp(1)<0&&eps.cmp(0)>=0&&eps.cmp(1)<0,"fixture domain");
  const a=eps.a(O.s(eps).m(tau));
  return [[Z,a],[tau,eps],[tau.a(1),O]];
 }
 function reflected(p){return p.map(([t,x])=>[t,x.neg()]);}
 function completed(raw,weights,mode="raw"){
  const s=new L.CaptureSearch(raw,weights,{mode,nodeLimit:100000});
  while(!s.runSlice(10000,1000)){}
  const r=s.result();assert(r.complete,"incomplete exact response");return r;
 }
 for(const tau of ["1/8","1/2","7/8"]){
  for(const eps of ["1/2","1/8","1/64","1/1024","0"]){
   const p=pairPath(tau,eps),r=completed([reflected(p),p],["1/2","1/2"]);
   const expected=Q(eps).eq(0)?Q(tau).dby(2):O.a(p[0][1]).dby(2);
   assert(Q(r.value).eq(expected),"avoided-bounce exact value");
   reports.push({tau,epsilon:eps,value:r.value,nodes:r.stats.nodes,complete:true});
  }
 }
 const atomlessFixtures=[];
 for(const eps of ["1/8","1/32","1/128"]){
  const e=Q(eps),tau=Q("1/2"),delta=e.m(e).dby(16);
  const ts=[tau.s(delta),tau,tau.a(delta)],ps=ts.map(t=>pairPath(t,e));
  const raw=[...ps.map(reflected),...ps],weights=Array(6).fill("1/6");
  const r=completed(raw,weights);
  const amin=ps[0][0][1],amax=ps[2][0][1];
  assert(amin.cmp(ts[2])>0,"opposite-sign separation gate");
  const lower=O.a(amin).dby(2),upperBound=O.a(amax).dby(2).a(delta.dby(e));
  assert(Q(r.value).cmp(lower)>=0&&Q(r.value).cmp(upperBound)<=0,"jitter bounds");
  atomlessFixtures.push({epsilon:eps,delta:delta.str(),finiteFixtureValue:r.value,
    rigorousContinuousFamilyLower:lower.str(),rigorousContinuousFamilyUpper:upperBound.str(),nodes:r.stats.nodes});
 }
 const out={scope:"Exact finite fixtures plus stated analytic all-monster lemmas for the avoided-bounce family. No lower strategy for the full target game is claimed.",pair_fixtures:reports,jitter_fixtures:atomlessFixtures,all_searches_complete:true};
 if(face){
  const a=Q(face.limiting_profiles[1].initial);
  const monster=new L.PLPath([[Z,a],[a.a(1),Q(-1)],[a.a(3),O],[Q(8),O]]);
  const score=p=>{
   const plus=new L.PLPath(p),minus=new L.PLPath(p.map(([t,x])=>[t,Q(x).neg()]));
   const cp=L.rawCapture(monster,plus),cm=L.rawCapture(monster,minus);
   assert(cp!==null&&cm!==null,"face capture");
   return{positive:cp.str(),negative:cm.str(),value:cp.a(cm).dby(2).str(),decimal:cp.a(cm).dby(2).num()};
  };
  out.face_attack={scope:"Specified straight-left attack, independently intersected with each supplied physical path.",route:monster.json(),
   profiles:face.limiting_profiles.map(p=>({name:p.name,...score(p.path_through_two)})),
   epsilon_profile:score(face.absorbing_physical_response.path)};
  if(upper&&sourceCertificate){
   const levels=sourceCertificate.base_levels,queries=sourceCertificate.query_v;
   const label=k=>({U:levels[Math.floor(k/3)],side:k%3-1});
   const expected=[
    {v:"-1/2",min:{U:"0",side:0},max:{U:"1/2",side:-1}},
    {v:"-15/32",min:{U:"4823449/8388608",side:-1},max:{U:"4823449/8388608",side:-1}},
    {v:"1/2",min:{U:"5/8",side:-1},max:{U:"5/8",side:-1}}
   ];
   for(const row of expected){
    const j=queries.indexOf(row.v);assert(j>=0,"missing query");
    assert(JSON.stringify(label(upper.minimum_labels[j]))===JSON.stringify(row.min),"minimum face trace");
    assert(JSON.stringify(label(upper.maximum_labels[j]))===JSON.stringify(row.max),"maximum face trace");
   }
   const knots=upper.knots.map(Q),ds=upper.increment_numerators.map(x=>Q(x).dby(upper.increment_denominator));
   function psi(x){x=Q(x);let y=Z;for(let j=0;j<ds.length;j++){if(x.cmp(knots[j+1])>=0)y=y.a(ds[j]);else if(x.cmp(knots[j])>0){y=y.a(ds[j].m(x.s(knots[j])).dby(knots[j+1].s(knots[j])));break;}else break;}return y;}
   const A=psi("15/32"),X=psi("1/2"),T=psi("5/8"),bound=X.m(2).a(T).s(A).dby(4);
   assert(X.eq(a),"attack start warp");
   assert(bound.eq("578124999999997/2000000000000000"),"face bound");
   out.face_attack.uniform_trace_bound={scope:"Uniform limiting bound over all realizing residual-face controls, using the three priced traces and lattice extremality, not canonical-fill interpolation.",trace_checks:expected,A:A.str(),X:X.str(),T:T.str(),bound:bound.str(),decimal:bound.num()};
  }
 }
 return out;
}
export {verifyAvoidedCenterBounce};

async function main(){const args=process.argv.slice(2);const opt={};for(let j=0;j<args.length;j+=2){if(!args[j].startsWith("--")||args[j+1]===undefined)throw Error("usage: --output REPORT [--face FACE --upper UPPER --source SOURCE]");opt[args[j].slice(2)]=args[j+1];}const read=async k=>opt[k]?JSON.parse(await fs.readFile(opt[k],"utf8")):null;const [face,upper,source]=await Promise.all([read("face"),read("upper"),read("source")]);const out=verifyAvoidedCenterBounce(createOracle(),face,upper,source);if(!opt.output)throw Error("--output required");await fs.writeFile(opt.output,JSON.stringify(out,null,2)+"\n");console.log("PASS",out.pair_fixtures.length,"pair fixtures",out.jitter_fixtures.length,"jitter fixtures",out.face_attack?"and exact face attack":"");}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
