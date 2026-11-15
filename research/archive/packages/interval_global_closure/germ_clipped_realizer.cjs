/** Pointwise-clipped avoided connector: a separate legal unit/wait candidate.
 * Inspect traces[].nonzeroPreserved when auditTraces is enabled.
 * Fixed-bank agreement does not imply adaptive-response equivalence.
 */
module.exports = (function(){

function createClippedRealizer(G){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,e=G.eps;
 const min=(a,b)=>a.cmp(b)<=0?a:b;
 function realize(queryV,baseLevels,indices,{avoidIsolated=true,clip=true,auditTraces=true}={}){
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
  const eta=clip?e.pow(6):Z;
  const transformed=[];
  function pushClip(u,v){const t=u.a(v).dby(2),r=u.s(v).dby(2),p=r.cmp(eta)<0?eta:r.cmp(O.s(eta))>0?O.s(eta):r,z=[t.a(p),t.s(p)],old=transformed.at(-1);if(!old||!z[0].eq(old[0])||!z[1].eq(old[1]))transformed.push(z);}
  for(let j=0;j+1<points.length;j++){
   const[u0,v0]=points[j],[u1,v1]=points[j+1],r0=u0.s(v0).dby(2),r1=u1.s(v1).dby(2),a=[Z,O];
   if(!r0.eq(r1))for(const h of [eta,O.s(eta)]){const z=h.s(r0).dby(r1.s(r0));if(z.cmp(0)>0&&z.cmp(1)<0)a.push(z);}
   a.sort((x,y)=>x.cmp(y));for(const z of a)pushClip(u0.a(u1.s(u0).m(z)),v0.a(v1.s(v0).m(z)));
  }
  const traces=[];
  if(auditTraces)for(let j=0;j<vv.length;j++){
   const pre=trace(points,vv[j]);if(!pre.first.eq(values[j])||!pre.last.eq(values[j]))throw Error("pre-shrink query mismatch");
   const post=trace(transformed,vv[j]),sgn=post.first.cmp(bases[j]);
   const lastSide=post.last.cmp(bases[j]);
   traces.push({query:j,side:sides[j],postSide:sgn,postLastSide:lastSide,nonzeroPreserved:!sides[j]||(sgn===sides[j]&&lastSide===sides[j])});
  }
  const path=[];
  for(let j=0;j+1<transformed.length;j++){
   const[u0,v0]=transformed[j],[u1,v1]=transformed[j+1],t0=u0.a(v0).dby(2),t1=u1.a(v1).dby(2);
   if(t1.cmp(0)<0)continue;const x0=u0.s(v0).dby(2),x1=u1.s(v1).dby(2);
   if(!path.length){if(t0.cmp(0)>0)throw Error("missing initial crossing");path.push([Z,x0.a(x1.s(x0).m(t0.neg()).dby(t1.s(t0)))]);}
   if(t1.cmp(path.at(-1)[0])>0)path.push([t1,x1]);
  }
  const physical=new G.PLPath(path);if(physical.v.some(x=>!x.eq(-1)&&!x.eq(0)&&!x.eq(1)))throw Error("clipped path lost unit/wait structure");
  return{path:physical,changes,forcedCenterIntervals:forced,traces,points:points.length};
 }
 return{realize};
}
return {createClippedRealizer};

})();
