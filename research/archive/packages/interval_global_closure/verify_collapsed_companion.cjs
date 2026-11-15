/**
 * Exact regression checks for the separate collapsed ordinary upper law.
 * Dependencies are injected so the same verifier runs in Node or pure V8.
 */
module.exports = (function(){
function verifyCollapsedCompanion(E,G,A,C,fixtures){
 let checks=0;const rows=[],rejections=[];
 function assert(x,msg){if(!x)throw Error(msg);checks++;}
 function reject(name,f){let ok=false;try{f();}catch(e){ok=true;rejections.push({name,message:String(e.message||e)});}assert(ok,"accepted invalid case: "+name);}
 function path(light){return new G.PLPath(light.map(([u,v])=>{u=G.Q(u);v=G.Q(v);return[u.a(v).dby(2),u.s(v).dby(2)];}));}
 const fixedPrincess=[
  [[0,0]],[[0,1]],[[0,-1]],
  [[0,"1/3"],[1,"-2/3"],[2,"1/3"]],
  [[0,"-1/4"],["3/4","1/2"],["7/4","-1/2"]]
 ].map(p=>new G.PLPath(p));
 let uniformChecks=0,lscChecks=0;
 for(const f of fixtures){
  const original=JSON.stringify(f.atoms),weights=f.nums.map(x=>G.Q(x).dby(f.den)),
   result=C.companion(f.atoms,weights);
  assert(G.Q(result.response.value).cmp(f.result.value)<=0,"collapsed upper exceeds germ limit");
  assert(result.response.flow_replay.exactValue===result.response.value,"ordinary integer replay");
  assert(JSON.stringify(f.atoms)===original,"input atom geometry mutated");
  assert(result.law.route_audits.every(r=>r.limit_nonunit_segments===0),"unit inputs acquired nonunit limits");
  for(const atom of f.atoms){
   const r=C.collapseRoute(atom),old=path(atom.exact_light),now=path(r.exact_light);
   for(const p of fixedPrincess){
    const a=G.rawCapture(old,p),b=G.rawCapture(now,p);
    assert(a!==null&&b!==null,"complete endpoint path missed a Princess");
    assert(b.limit().cmp(a.limit())<=0,"fixed-Princess lower semicontinuity");
    lscChecks++;
   }
   const oldVertices=old.vertices,limitVertices=oldVertices.map(row=>row.map(x=>x.limit()));
   for(const epsilon of ["1/32","1/64","1/128"]){
    const e=G.Q(epsilon).limit(),special=oldVertices.map(row=>row.map(x=>x.evaluate(e))),
     sp=new G.PLPath(special);
    let dx=G.ZERO,dt=G.ZERO;
    for(let j=0;j<special.length;j++){
     let a=G.Q(special[j][0].s(limitVertices[j][0])),b=G.Q(special[j][1].s(limitVertices[j][1]));
     if(a.cmp(0)<0)a=a.neg();if(b.cmp(0)<0)b=b.neg();
     if(a.cmp(dt)>0)dt=a;if(b.cmp(dx)>0)dx=b;
    }
    const points=sp.t.concat(now.t).sort((a,b)=>a.cmp(b)),bound=dx.a(dt);
    for(const t of points){
     let error=sp.at(t).s(now.at(t));if(error.cmp(0)<0)error=error.neg();
     assert(error.cmp(bound)<=0,"uniform polygonal convergence estimate");
     uniformChecks++;
    }
   }
  }
  rows.push({name:f.name,germ_response:f.result.value,ordinary_response:result.response.value,
   input_atoms:f.atoms.length,ordinary_atoms:result.law.output_atom_count,
   collapsed_segments:result.law.route_audits.reduce((s,x)=>s+x.collapsed_zero_duration_segments,0),
   flow_replay:result.response.flow_replay});
 }
 const endpoint=fixtures[0].atoms[0],other=fixtures[4].atoms[1],
  zero=C.companion([endpoint,other],[G.ONE.s(G.eps),G.eps]);
 assert(zero.law.output_atom_count===1&&zero.law.dropped_zero_weights.length===1,"zero limiting weight not removed");
 assert(zero.response.value==="3/2","zero limiting atom changed ordinary response");
 const m=new A.Model([endpoint,other]),germZero=A.integerLimitCut(m,[G.ONE.s(G.eps),G.eps]);
 assert(germZero.value==="3/2","vanishing-probability germ changed limiting response");
 const reflect={exact_light:endpoint.exact_light.map(([u,v])=>[v,u])},
  merge=C.companion([endpoint,reflect],["1/3","2/3"]);
 assert(merge.law.output_atom_count===1&&merge.law.weight_numerators[0]==="1"&&merge.law.weight_denominator==="1","reflection merge lost probability");
 const duplicate={exact_light:[endpoint.exact_light[0],...endpoint.exact_light]};
 const duplicateResult=C.companion([duplicate],["1"]);
 assert(duplicateResult.law.route_audits[0].collapsed_zero_duration_segments===1,"duplicate equal-time vertex retained");
 assert(duplicateResult.response.value==="3/2","duplicate vertex changed ordinary response");
 const nonunit={route:[[0,0],[1,"1/2"],["3/2",1],["7/2",-1]]},
  nonunitLaw=C.collapseLaw([nonunit],["1"]);
 assert(!nonunitLaw.standard_atomic_supported&&nonunitLaw.route_audits[0].limit_nonunit_segments===1,"genuine nonunit limit not flagged");
 reject("nonunit ordinary response",()=>C.standardResponse(nonunitLaw));
 reject("negative probability",()=>C.collapseLaw([endpoint,other],[G.ONE.a(G.eps),G.eps.neg()]));
 reject("unnormalized probabilities",()=>C.collapseLaw([endpoint,other],["1/2","1/4"]));
 reject("instantaneous displacement",()=>C.collapseRoute({route:[[0,0],[0,G.eps],[2,-1],[4,1]]}));
 reject("missing endpoint completion",()=>C.collapseRoute({route:[[0,0],[1,1]]}));
 reject("nonzero initial time",()=>C.collapseRoute({route:[[G.eps,0],[2,-1],[4,1]]}));
 reject("diverging vertex time",()=>C.collapseRoute({route:[[0,0],[G.ONE.dby(G.eps),0],[G.ONE.dby(G.eps).a(1),1],[G.ONE.dby(G.eps).a(3),-1]]}));
 const varying=new G.PLPath([[0,G.eps]]),varyingNeg=new G.PLPath([[0,G.eps.neg()]]),
  originalM={route:[[0,G.eps],[G.ONE.a(G.eps),-1],[G.Q(3).a(G.eps),1]]},
  originalPath=new G.PLPath(originalM.route),collapsed=C.collapseRoute(originalM),collapsedPath=path(collapsed.exact_light),
  before=G.rawCapture(originalPath,varying).a(G.rawCapture(originalPath,varyingNeg)).dby(2),
  after=G.rawCapture(collapsedPath,varying).a(G.rawCapture(collapsedPath,varyingNeg)).dby(2);
 assert(before.eq(G.eps),"varying-Princess original cost");
 assert(after.eq(G.ONE.a(G.eps)),"varying-Princess collapsed cost");
 return{scope:"Collapsed companion comparison, ordinary flow replay, and geometry/semicontinuity regressions.",
  exact_checks:checks,fixtures:rows,uniform_convergence_checks:uniformChecks,
  fixed_princess_lsc_checks:lscChecks,zero_probability_germ_response:germZero.value,
  varying_princess_counterexample:{original:before.str(),collapsed:after.str(),original_limit:before.limit().str(),collapsed_limit:after.limit().str()},
  rejected_cases:rejections,arithmetic:G.stats()};
}
return{verifyCollapsedCompanion};
})();