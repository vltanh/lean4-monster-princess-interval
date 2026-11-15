/** Alternative microscopic connector for isolated limiting center bounces.
 * Non-isolated center-wait intervals are left explicit. The original realizer is unchanged.
 */
module.exports = (function(){

function createAvoidedRealizer(G){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,e=G.eps;
 const min=(a,b)=>a.cmp(b)<=0?a:b;
 function realize(queryV,baseLevels,indices,{avoidIsolated=true,shrink=true,auditTraces=true}={}){
  const vv=queryV.map(Q),bases=indices.map(k=>Q(baseLevels[Math.floor(k/3)])),
   sides=indices.map(k=>k%3-1),values=bases.map((b,j)=>b.a(e.m(sides[j]))),
   points=[[Z,Q(-1)]],changes=[],forced=[];
  function add(u,v){u=Q(u);v=Q(v);const p=points.at(-1);
   if(u.eq(p[0])&&v.eq(p[1]))return;
   if(u.cmp(p[0])<0||v.cmp(p[1])<0||u.s(v).cmp(0)<0||u.s(v).cmp(2)>0)throw Error("illegal light germ");
   points.push([u,v]);
  }
  for(let j=1;j<vv.length;j++){
   const v=vv[j],prev=values[j-1],target=values[j],
    delta=min(e.pow(2),v.s(vv[j-1]).dby(3));
   let before=v.s(delta);
   const isolated=bases[j-1].eq(v)&&bases[j].cmp(v)>0;
   if(avoidIsolated&&isolated){
    const candidate=min(before,prev.s(e));
    if(candidate.cmp(vv[j-1])<=0)throw Error("isolated connector crosses previous query");
    changes.push({query:j,V:v.str(),previousSide:sides[j-1],oldBefore:before.str(),before:candidate.str(),gap:prev.s(candidate).str()});
    before=candidate;
   }else if(bases[j-1].cmp(v)<0)forced.push({query:j,from:bases[j-1].str(),to:v.str()});
   add(prev,min(before,prev));if(before.cmp(prev)>0)add(before,before);
   add(min(target,before.a(2)),before);if(target.cmp(before.a(2))>0)add(target,target.s(2));add(target,v);
  }
  function trace(ps,v){
   let lo=0,hi=ps.length;
   while(lo<hi){const m=(lo+hi)>>1;if(ps[m][1].cmp(v)<0)lo=m+1;else hi=m;}
   if(lo<ps.length&&ps[lo][1].eq(v)){
    let end=lo;while(end+1<ps.length&&ps[end+1][1].eq(v))end++;
    return{first:ps[lo][0],last:ps[end][0]};
   }
   if(lo===0)throw Error("query below virtual graph");
   if(lo===ps.length){const[u,w]=ps.at(-1),z=v.a(u.s(w));return{first:z,last:z};}
   const[a,b]=ps[lo-1],[c,d]=ps[lo],z=a.a(c.s(a).m(v.s(b)).dby(d.s(b)));return{first:z,last:z};
  }
  const eta=shrink?e.pow(6):Z;
  const transformed=points.map(([u,v])=>{const h=eta.m(O.s(u).a(v));return[u.a(h),v.s(h)];});
  const traces=[];
  if(auditTraces)for(let j=0;j<vv.length;j++){
   const pre=trace(points,vv[j]);if(!pre.first.eq(values[j])||!pre.last.eq(values[j]))throw Error("pre-shrink query mismatch");
   const post=trace(transformed,vv[j]),sgn=post.first.cmp(bases[j]);
   if(!post.first.eq(post.last))throw Error("strict-shrink query ambiguity");
   if(sides[j]&&sgn!==sides[j])throw Error("nonzero query side changed");
   traces.push({query:j,side:sides[j],postSide:sgn});
  }
  const path=[];
  for(let j=0;j+1<transformed.length;j++){
   const[u0,v0]=transformed[j],[u1,v1]=transformed[j+1],t0=u0.a(v0).dby(2),t1=u1.a(v1).dby(2);
   if(t1.cmp(0)<0)continue;const x0=u0.s(v0).dby(2),x1=u1.s(v1).dby(2);
   if(!path.length){if(t0.cmp(0)>0)throw Error("missing initial crossing");path.push([Z,x0.a(x1.s(x0).m(t0.neg()).dby(t1.s(t0)))]);}
   if(t1.cmp(path.at(-1)[0])>0)path.push([t1,x1]);
  }
  return{path:new G.PLPath(path),changes,forcedCenterIntervals:forced,traces,points:points.length};
 }
 return{realize};
}
return {createAvoidedRealizer};

})();
