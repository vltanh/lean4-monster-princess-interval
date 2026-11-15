/** Exact ordered-fan M1 separation. Moving second-ray CDF events and
 * initial-rank equalities refine the raw first-moment geometry.
 */
module.exports=(function(){
function createOrderedFanM1Separator(G,fanModule,orderedModule,rawM1Module,entries){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,
  OT=orderedModule.createOrderedFanTools(G,fanModule),T=OT.fan,
  raw=rawM1Module.createFanM1Separator(G,T,entries),law=OT.law(entries.map(e=>e.row),entries.map(e=>e.weight??1)),
  weights=law.weights.map(Q),active=entries.filter((_,i)=>weights[i].cmp(0)>0),cache=new Map();
 function score(a){a=Q(a);const key=a.str();if(cache.has(key))return cache.get(key);const value=Q(law.score(raw.route(a)).exact_cost);cache.set(key,value);return value;}
 function geometryCuts({verifyAffine=true,maxEvents=20000,maxPairTests=2000000,maxCells=200000}={}){
  const points=new Map(),groups=new Map(),add=a=>{a=Q(a);if(a.cmp(-1)>=0&&a.cmp(1)<=0)points.set(a.str(),a);};
  for(const a of raw.geometryCuts())add(a);
  function restrict(interval,s,b){
   if(interval===null)return null;let[l,r]=interval;
   if(s.eq(0))return b.cmp(0)<0?null:interval;
   const root=b.neg().dby(s);if(s.cmp(0)>0)l=max(l,root);else r=min(r,root);
   return l.cmp(r)<=0?[l,r]:null;
  }
  function event(s,b,from=null,to=null){
   let interval=[Q(-1),O];
   interval=restrict(interval,s.s(1),b.s(1));
   interval=restrict(interval,O.s(s),Q(3).s(b));
   if(from!==null)interval=restrict(interval,s,b.s(from));
   if(to!==null)interval=restrict(interval,s.neg(),Q(to).s(b));
   if(interval===null)return;
   const key=s.str()+"|"+b.str(),item={s,b,lo:interval[0],hi:interval[1]};
   if(!groups.has(key))groups.set(key,[]);groups.get(key).push(item);
  }
  event(O,O);event(O,Q(3));
  for(const{row}of active){
   const p=row.path;
   for(const t of p.t)event(Z,t);
   for(const sign of[1,-1]){
    const lo=sign===1?row.lower:row.upper.neg(),hi=sign===1?row.upper:row.lower.neg();
    for(let i=0;i<p.t.length;i++){
     const v=i<p.v.length?p.v[i]:Z,den=O.s(v.m(sign)),base=Q(2).a(p.x[i].s(v.m(p.t[i])).m(sign));
     for(const z of[lo,hi]){
      if(den.eq(0)){add(base.a(z).neg());continue;}
      event(O.dby(den),base.a(z).dby(den),p.t[i],i+1<p.t.length?p.t[i+1]:null);
     }
    }
   }
  }
  const events=[];
  for(const list of groups.values()){
   list.sort((a,b)=>a.lo.cmp(b.lo));let current=null;
   for(const e of list){if(current===null)current={...e};else if(e.lo.cmp(current.hi)<=0)current.hi=max(current.hi,e.hi);else{events.push(current);current={...e};}}
   if(current!==null)events.push(current);
  }
  if(events.length>maxEvents)throw Error("ordered M1 time-event cap exceeded");
  events.sort((a,b)=>a.lo.cmp(b.lo));
  for(const e of events){add(e.lo);add(e.hi);}
  let pairTests=0,timeCrossings=0;
  for(let i=0;i<events.length;i++)for(let j=i+1;j<events.length&&events[j].lo.cmp(events[i].hi)<=0;j++){
   const e=events[i],f=events[j];if(e.s.eq(f.s))continue;
   if(++pairTests>maxPairTests)throw Error("ordered M1 event-intersection cap exceeded");
   const a=f.b.s(e.b).dby(e.s.s(f.s)),l=max(e.lo,f.lo),r=min(e.hi,f.hi);
   if(a.cmp(l)>0&&a.cmp(r)<0){if(!points.has(a.str()))timeCrossings++;add(a);}
  }
  const base=[...points.values()].sort((a,b)=>a.cmp(b));
  if(base.length-1>maxCells)throw Error("ordered M1 geometric cell cap exceeded");
  let affineChecks=0,rankCuts=0;
  for(let j=0;j+1<base.length;j++){
   const left=base[j],width=base[j+1].s(left),a1=left.a(width.dby(3)),a2=left.a(width.m(2).dby(3)),am=left.a(width.dby(2)),
    M1=law.marginal(Z,a1,"closed"),M2=law.marginal(Z,a2,"closed"),Mm=verifyAffine?law.marginal(Z,am,"closed"):null;
   for(const e of events){
    if(am.cmp(e.lo)<=0||am.cmp(e.hi)>=0)continue;
    const gap=(a,M)=>{const t=e.s.m(a).a(e.b);return law.marginal(t,t.s(a).s(2),"interior").s(M);},
     f1=gap(a1,M1),f2=gap(a2,M2),slope=f2.s(f1).m(3),offset=f1.s(slope.dby(3));
    if(verifyAffine){if(!gap(am,Mm).eq(offset.a(slope.dby(2))))throw Error("missing ordered M1 CDF event topology");affineChecks++;}
    if(slope.eq(0))continue;
    const u=offset.neg().dby(slope);
    if(u.cmp(0)>0&&u.cmp(1)<0){const a=left.a(width.m(u));if(!points.has(a.str()))rankCuts++;add(a);}
   }
  }
  const cuts=[...points.values()].sort((a,b)=>a.cmp(b));
  if(cuts.length-1>maxCells)throw Error("ordered M1 refined cell cap exceeded");
  return{cuts,base_cells:base.length-1,time_events:events.length,pair_tests:pairTests,time_crossings:timeCrossings,rank_cuts:rankCuts,affine_checks:affineChecks};
 }
 function separate({verifyPolynomial=true,keepCells=false,maxCells=200000,maxEvents=20000,maxPairTests=2000000,onProgress=()=>{}}={}){
  const geometry=geometryCuts({maxCells,maxEvents,maxPairTests}),cuts=geometry.cuts;
  let best=null,bestStart=null,stationary=0,checks=0;const cells=[];
  function candidate(a){const value=score(a);if(best===null||value.cmp(best)<0){best=value;bestStart=a;}}
  for(const a of cuts)candidate(a);
  for(let j=0;j+1<cuts.length;j++){
   const a=cuts[j],width=cuts[j+1].s(a),at=u=>score(a.a(width.m(u))),
    f1=at(Q("1/4")),f2=at(Q("1/2")),f3=at(Q("3/4")),
    q2=f1.s(f2.m(2)).a(f3).m(8),q1=f3.s(f1).m(2).s(q2),q0=f2.s(q1.dby(2)).s(q2.dby(4)),
    polynomial=u=>q0.a(q1.m(u)).a(q2.m(u.m(u)));
   if(verifyPolynomial)for(const u of[Q("1/3"),Q("2/3")]){if(!polynomial(u).eq(at(u)))throw Error("missing ordered M1 hinge boundary");checks++;}
   let root=null;if(q2.cmp(0)>0){const u=q1.neg().dby(q2.m(2));if(u.cmp(0)>0&&u.cmp(1)<0){root=a.a(width.m(u));if(!score(root).eq(polynomial(u)))throw Error("ordered M1 stationary mismatch");candidate(root);stationary++;}}
   if(keepCells)cells.push({left:a.str(),right:cuts[j+1].str(),local_coefficients:[q0.str(),q1.str(),q2.str()],stationary_start:root?.str()??null});
   if(j%32===31)onProgress({cells:j+1,total:cuts.length-1});
  }
  return{scope:"Complete continuous M1 starts against the ordered common-quantile law of immutable interval fans; no other Monster family is certified.",
   complete:true,minimum:best.str(),limit:best.limit().str(),decimal:best.limit().num(),start:bestStart.str(),route:raw.route(bestStart).json(),
   cell_count:cuts.length-1,base_cell_count:geometry.base_cells,time_events:geometry.time_events,event_pair_tests:geometry.pair_tests,
   time_intersection_cuts:geometry.time_crossings,rank_refinement_cuts:geometry.rank_cuts,affine_event_checks:geometry.affine_checks,
   stationary_candidates:stationary,polynomial_checks:checks,score_queries:cache.size,cuts:cuts.map(x=>x.str()),cells:keepCells?cells:null,
   normalized_weights:law.weights,arithmetic:G.stats()};
 }
 return{score,route:raw.route,geometryCuts,separate,law};
}
return{createOrderedFanM1Separator};
})();