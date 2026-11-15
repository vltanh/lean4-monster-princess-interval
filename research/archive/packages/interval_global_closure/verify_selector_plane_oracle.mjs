import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import atomicModule from "../interval_turn_density/atomic_survival_v8.cjs";
import signedModule from "./signed_label_closure.cjs";
import selectorModule from "./selector_plane_oracle.cjs";
import independentModule from "../interval_finite_reduction_audit/verify_selector_compiler_independent.cjs";

export function verifySelectorPlaneOracle(A, closure, oracleModule, input, independentDP=null){
 const Q=A.Q,Z=Q(0),O=oracleModule.createSelectorPlaneOracle(A,closure),
  answer=O.solve(input.problem),C=answer.compiled,reference=Q(input.known_actual_capture_supremum),
  assert=(ok,msg)=>{if(!ok)throw Error(msg);},abs=q=>q.cmp(0)<0?q.neg():q,
  min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,
  unique=xs=>[...new Map(xs.map(x=>[x.str(),x])).values()].sort((a,b)=>a.cmp(b));
 assert(Q(answer.value).cmp(reference)>=0,"selector supremum below known actual capture supremum");
 const dp=independentDP?independentDP(C):null;
 if(dp)assert(Q(C.constant).a(Q(dp.value)).eq(Q(answer.value)),"independent full prefix-DP/flow mismatch");
 const prepared=O.prepare(input.route_packet);
 let captures=0,queryChecks=0,parallelChecks=0;const witnesses={};
 function capture(path){
  const p=[new A.PLPath(path),new A.PLPath(path.map(([t,x])=>[t,Q(x).neg().str()]))];let value=Z;const rows=[];
  for(const a of prepared.planes){
   const monster=new A.PLPath(a.route),times=p.map(row=>A.rawCapture(monster,row));
   assert(times.every(t=>t!==null),"completed Monster misses Princess");
   captures+=2;const paired=times[0].a(times[1]).dby(2);
   value=value.a(a.weight.m(paired));
   rows.push({id:a.id,weight:a.weight.str(),positive_time:times[0].str(),negative_time:times[1].str(),paired_cost:paired.str()});
  }return{cost:value,rows};
 }
 function inspection(chosen,actual){
  const vs=C.grid.v.map(Q),values=chosen.map(k=>Q(C.labels[k].base)),light=[];
  function put(v,u){const p=light.at(-1);if(p&&p[0].eq(v)&&p[1].eq(u))return;
   assert(!p||(v.cmp(p[0])>=0&&u.cmp(p[1])>=0),"nonmonotone nominal light path");light.push([v,u]);}
  for(let i=0;i+1<vs.length;i++){
   const a=vs[i],b=vs[i+1],c=values[2*i+1],f=v=>min(v.a(2),max(max(v,Z),c));
   put(a,values[2*i]);put(a,f(a));
   for(const v of unique([Z,c,c.s(2)].filter(v=>v.cmp(a)>0&&v.cmp(b)<0)))put(v,f(v));
   put(b,f(b));put(b,values[2*i+2]);
  }
  const physical=light.map(([v,u])=>[v.a(u).dby(2),u.s(v).dby(2)]),out=[];
  function add(t,x){if(out.length&&out.at(-1)[0].eq(t)){assert(out.at(-1)[1].eq(x),"nominal instantaneous position jump");return;}
   out.push([t,x]);while(out.length>=3){const[a,b,c]=out.slice(-3);if(b[1].s(a[1]).m(c[0].s(b[0])).eq(c[1].s(b[1]).m(b[0].s(a[0]))))out.splice(out.length-2,1);else break;}}
  for(let i=0;i<physical.length;i++){const[t,x]=physical[i];if(t.cmp(0)<0)continue;
   if(!out.length&&t.cmp(0)>0){const[a,p]=physical[i-1];add(Z,p.a(x.s(p).m(a.neg()).dby(t.s(a))));}add(t,x);}
  const path=out.map(v=>v.map(x=>x.str())),literalCapture=capture(path),p=new A.PLPath(actual.path);
  let margin=null,center=null,endpoint=null;const queryMargins=[];
  for(const term of C.source_terms.points){
   const t=Q(term.time),x=Q(term.position),r=p.at(t),gap=abs(r.s(abs(x)));
   assert(gap.cmp(0)>0,"actual path has a retained point contact");queryChecks++;
   margin=margin===null?gap:min(margin,gap);
   if(x.eq(0))center=center===null?r:min(center,r);
   if(abs(x).eq(1))endpoint=endpoint===null?gap:min(endpoint,gap);
   queryMargins.push({time:term.time,position:term.position,radius:r.str(),absolute_distance:gap.str()});
  }
  for(const ray of C.source_terms.rays){
   const l=Q(ray.start_time),r=Q(ray.end_time),x=Q(ray.start_position),d=ray.direction,
    cuts=unique([l,r,...p.t.filter(t=>t.cmp(l)>0&&t.cmp(r)<0)]);
   for(let j=0;j+1<cuts.length;j++)for(const sign of[1,-1]){
    const a=cuts[j],b=cuts[j+1],pa=p.at(a).m(sign),pb=p.at(b).m(sign);
    assert(!(pa.eq(x.a(a.s(l).m(d)))&&pb.eq(x.a(b.s(l).m(d)))),"positive-duration priced ray contact");parallelChecks++;
   }
  }
  queryMargins.sort((a,b)=>Q(a.absolute_distance).cmp(Q(b.absolute_distance)));
  return{
   scope:"The zero-scale polygon is inspection only. Its literal contact payoffs are separately evaluated and are not substituted for the actual query-avoiding witness.",
   actual_vertices:actual.path.length,nominal_vertices:path.length,nominal_path:path,
   nominal_path_decimal:path.map(v=>v.map(x=>Q(x).num())),
   actual_initial:actual.path[0][1],actual_initial_decimal:Q(actual.path[0][1]).num(),
   delta:actual.delta,bridge_width:actual.bridge_width,
   minimum_physical_query_distance:margin?.str()??null,minimum_physical_query_distance_decimal:margin?.num()??null,
   minimum_center_query_radius:center?.str()??null,minimum_endpoint_query_distance:endpoint?.str()??null,
   five_smallest_query_margins:queryMargins.slice(0,5),
   literal_nominal_selector_score:O.physicalScore(input.problem,path).str(),
   literal_nominal_capture_score:literalCapture.cost.str(),
   nominal_center_vertices:path.filter(v=>Q(v[1]).eq(0)).map(v=>v[0])
  };
 }
 for(const name of["minimum","maximum"]){
  const labels=answer.closure[name+"_labels"],r=O.realize(C,labels,{tolerance:input.realization_tolerance??"1/100000000"}),
   routeScore=O.physicalScore(input.route_packet,r.path),cap=capture(r.path);
  assert(routeScore.eq(Q(r.physical_score)),"original route selector score differs from flattened packet");
  assert(Q(r.label_score).eq(Q(answer.value)),"witness is not globally optimal");
  assert(Q(r.physical_score).cmp(Q(answer.value))<=0,"physical selector score exceeds global supremum");
  assert(Q(r.physical_score).cmp(Q(answer.value).s(Q(r.error_bound)))>=0,"explicit realization envelope fails");
  assert(cap.cost.cmp(Q(r.physical_score))<=0,"causal selector fails to majorize actual capture");
  assert(cap.cost.cmp(reference)<=0,"actual response exceeds independently certified reference supremum");
  witnesses[name]={...r,actual_capture:cap.cost.str(),actual_capture_decimal:cap.cost.num(),capture_rows:cap.rows};
 }
 const minimumInspection=inspection(answer.closure.minimum_labels,witnesses.minimum);
 return{
  scope:"Exact global supremum of one selector-type affine CDF plane, with actual rational approximating Princess witnesses. This is not a game equilibrium or a lower guarantee.",
  problem_sources:input.sources,source_counts:{points:input.problem.points.length,rays:input.problem.rays.length,monster_reflection_pairs:prepared.planes.length},
  compiled_statistics:C.statistics,grid:{v:C.grid.v,u:C.grid.u},constant:C.constant,
  closure:answer.closure,independent_prefix_dp:dp,global_selector_supremum:answer.value,global_selector_decimal:answer.decimal,
  known_actual_capture_supremum:reference.str(),known_actual_capture_decimal:reference.num(),
  selector_minus_actual_supremum:Q(answer.value).s(reference).str(),
  counts:{exact_chronological_captures:captures,strict_point_queries:queryChecks,priced_ray_subintervals:parallelChecks},
  witnesses,minimum_inspection:minimumInspection
 };
}
async function main(){
 const inputFile=process.argv[2]??new URL("./snapshots/selector_global_26_input.json",import.meta.url),
  input=JSON.parse(await fs.readFile(inputFile,"utf8")),A=createOracle(),S=signedModule.createSignedLabelClosure(atomicModule),
  result=verifySelectorPlaneOracle(A,S,selectorModule,input,independentModule.maximizeOrdinaryOrderedLabels),text=JSON.stringify(result,null,2)+"\n";
 if(process.argv[3])await fs.writeFile(process.argv[3],text);else process.stdout.write(text);
}
if(typeof process!=="undefined"&&process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
