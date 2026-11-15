/** Exact ordered common-quantile interval-fan costs and weight supergradients.
 * Every path/interval is fixed strategy data. A supplied unit Monster route
 * is scored completely; this module is not an unrestricted response search.
 */
module.exports=(function(){
function createOrderedFanTools(G,fanModule){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,T=fanModule.createTranslationFan(G),
  min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,
  unique=xs=>[...new Map(xs.map(Q).map(x=>[x.str(),x])).values()].sort((a,b)=>a.cmp(b));
 function prepareBasis(rows){
  return rows.map((r,i)=>T.prepareInterval(r.path,r.lower??r.lo,r.upper??r.hi,{id:r.id??i,provenance:r.provenance??null}));
 }
 function law(basis,weights){
  if(basis.length!==weights.length||!basis.length)throw Error("basis/weight dimensions");
  const raw=weights.map(Q);if(raw.some(w=>w.cmp(0)<0||!w.eq(Q(w.limit().str()))))throw Error("constant nonnegative weights required");
  const total=raw.reduce((a,b)=>a.a(b),Z);if(total.eq(0))throw Error("empty law");
  const w=raw.map(x=>x.dby(total)),active=w.map((x,i)=>x.eq(0)?-1:i).filter(i=>i>=0),R=basis.length;
  const dot=v=>active.reduce((s,i)=>s.a(w[i].m(v[i])),Z);
  function features(t,x,mode="interior"){
   return basis.map(row=>{const r=T.marginal(row,t,x);return mode==="strict"?r.strict:mode==="closed"?r.closed:x.eq(1)?r.strict:r.closed;});
  }
  function marginal(t,x,mode="interior"){t=Q(t);x=Q(x);return dot(features(t,x,mode));}
  function trace(a,b,d){
   const[t0,x0]=a,[t1,x1]=b;
   if(!x1.s(x0).eq(t1.s(t0).m(d)))throw Error("unit Monster leg required");
   const knots=[t0,t1];
   for(const i of active){const row=basis[i],p=row.path;
    const cuts=unique([t0,t1,...p.t.filter(t=>t.cmp(t0)>0&&t.cmp(t1)<0)]);
    for(let j=0;j+1<cuts.length;j++){
     const l=cuts[j],r=cuts[j+1],ml=x0.a(l.s(t0).m(d)),mr=x0.a(r.s(t0).m(d));
     knots.push(l,r);
     for(const sign of[1,-1]){
      const yl=ml.s(p.at(l).m(sign)),yr=mr.s(p.at(r).m(sign));
      if(yr.s(yl).m(d).cmp(0)<0)throw Error("nonmonotone fan characteristic");
      if(yr.eq(yl))continue;
      const lo=sign===1?row.lower:row.upper.neg(),hi=sign===1?row.upper:row.lower.neg();
      for(const q of[lo,hi])if(q.cmp(min(yl,yr))>0&&q.cmp(max(yl,yr))<0)
       knots.push(l.a(q.s(yl).m(r.s(l)).dby(yr.s(yl))));
     }
    }
   }
   const cuts=unique(knots),points=cuts.map(t=>({t,f:marginal(t,x0.a(t.s(t0).m(d)))}));
   for(let j=1;j<points.length;j++)if(points[j].f.s(points[j-1].f).m(d).cmp(0)<0)throw Error("nonmonotone assembled CDF");
   return points;
  }
  function featureIntegral(row,a,d,left,right){
   if(right.eq(left))return Z;
   const p=row.path,c=a[0].s(a[1].m(d));let ans=Z;
   for(const sign of[1,-1]){
    const lo=sign===1?row.lower:row.upper.neg(),hi=sign===1?row.upper:row.lower.neg(),
     l=d===1?c.a(lo):c.s(hi),r=d===1?c.a(hi):c.s(lo),h=(d*sign+1)>>1,
     moment=T.bandMoment(p,h,l,r,right).s(T.bandMoment(p,h,l,r,left));
    ans=ans.a(d===1?right.s(left).s(moment.dby(row.width)):moment.dby(row.width));
   }
   return ans.dby(2);
  }
  function positiveArea(a,b,h){
   if(a.cmp(0)>=0&&b.cmp(0)>=0)return a.a(b).m(h).dby(2);
   if(a.cmp(0)<=0&&b.cmp(0)<=0)return Z;
   return a.cmp(0)>0?h.m(a.m(a)).dby(a.s(b).m(2)):h.m(b.m(b)).dby(b.s(a).m(2));
  }
  function score(rawMonster,{gradient=false,requireComplete=true,details=false}={}){
   const m=rawMonster?.path?.v?rawMonster.path:rawMonster?.v?rawMonster:new G.PLPath(rawMonster.route??rawMonster);
   let lv=features(m.t[0],m.x[0],"strict"),hv=features(m.t[0],m.x[0],"closed"),L=dot(lv),H=dot(hv),cost=Z;
   const g=basis.map(()=>Z),legs=[];let pieces=0;
   for(let i=0;i<m.v.length;i++){
    const d=m.v[i].eq(1)?1:m.v[i].eq(-1)?-1:0;if(!d)throw Error("unit Monster required");
    const a=m.vertices[i],b=m.vertices[i+1],points=trace(a,b,d),duration=b[0].s(a[0]);
    let cut=b[0],found=false,part=Z;
    for(let j=0;j+1<points.length;j++){
     const l=points[j],r=points[j+1],dt=r.t.s(l.t),
      q0=d===1?l.f.s(H):L.s(l.f),q1=d===1?r.f.s(H):L.s(r.f);
     part=part.a(O.s(H).a(L).m(dt).s(positiveArea(q0,q1,dt)));pieces++;
     if(!found&&q1.cmp(0)>0){cut=q0.cmp(0)>=0?l.t:l.t.a(q0.neg().m(dt).dby(q1.s(q0)));found=true;}
    }
    cost=cost.a(part);
    if(gradient){const before=cut.s(a[0]);
     for(let j=0;j<R;j++){const I=featureIntegral(basis[j],a,d,cut,b[0]);
      g[j]=g[j].a(d===1?duration.m(O.a(lv[j])).s(before.m(hv[j])).s(I):duration.m(O.s(hv[j])).a(before.m(lv[j])).a(I));}
    }
    const endv=features(b[0],b[1],d===1?"closed":"strict"),end=dot(endv);
    if(d===1&&end.cmp(H)>0){H=end;hv=endv;}else if(d===-1&&end.cmp(L)<0){L=end;lv=endv;}
    if(details)legs.push({index:i,direction:d,activation:cut.str(),cost:part.str(),lower:L.str(),upper:H.str()});
   }
   const survivor=O.s(H).a(L),complete=survivor.eq(0);
   if(requireComplete&&!complete)throw Error("unfinished ordered capture");
   const euler=gradient?dot(g):null;if(gradient&&!euler.eq(cost))throw Error("exact homogeneous gradient identity");
   return{scope:"Exact supplied-route ordered fan cost; no unrestricted response claim",complete,exact_cost:cost.str(),limit:cost.limit().str(),
    survivor:survivor.str(),gradient:gradient?g.map(x=>x.str()):null,euler:euler?.str()??null,pieces,legs};
  }
  return{score,marginal,features,featureIntegral,trace,weights:w.map(x=>x.str()),basis};
 }
 return{prepareBasis,law,fan:T};
}
return{createOrderedFanTools};
})();