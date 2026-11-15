/** Exact endpoint-reflected radial interval fans and their ordered law.
 * Row: p_z=1-|1-p-z|, z uniform[lower,upper] subset[0,1], then fair reflection.
 * All path/window data are immutable. No unrestricted response is claimed.
 */
module.exports=(function(){
function createReflectedFanTools(G){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,abs=a=>a.cmp(0)<0?a.neg():a,
  unique=xs=>[...new Map(xs.map(Q).map(x=>[x.str(),x])).values()].sort((a,b)=>a.cmp(b)),cache=new WeakMap();
 function prepareInterval(raw,lower,upper,{id=null,provenance=null}={}){
  const path=raw?.v?raw:new G.PLPath(raw),lo=Q(lower),hi=Q(upper);
  if(lo.cmp(0)<0||hi.cmp(1)>0||lo.cmp(hi)>=0)throw Error("reflected translation window must lie in[0,1]");
  if(path.x.some(x=>x.cmp(0)<0))throw Error("reflected radial base must be nonnegative");
  const row={path,lower:lo,upper:hi,width:hi.s(lo),id,provenance};cache.set(row,new Map());return row;
 }
 function prepareBasis(rows){return rows.map((r,i)=>prepareInterval(r.path,r.lower??r.lo??0,r.upper??r.hi??r.delta,{id:r.id??i,provenance:r.provenance??null}));}
 function marginal(row,t,x){
  t=Q(t);x=Q(x);if(x.cmp(-1)<0||x.cmp(1)>0)throw Error("CDF position outside arena");
  const p=row.path.at(t),u=abs(x),clip=a=>max(Z,min(O,a)),
   radial=clip(u.s(p).s(row.lower).dby(row.width)).a(clip(u.a(p).a(row.upper).s(2).dby(row.width))),
   f=x.cmp(0)>=0?O.a(radial).dby(2):O.s(radial).dby(2);
  return{strict:f,closed:f};
 }
 function rowTrace(row,a,b,d){
  const[t0,x0]=a.map(Q),[t1,x1]=b.map(Q);
  if(t1.cmp(t0)<0||!x1.s(x0).eq(t1.s(t0).m(d)))throw Error("unit reflected-fan ray required");
  const key=[t0.str(),x0.str(),t1.str(),x1.str(),d].join("|"),map=cache.get(row)??new Map();if(!cache.has(row))cache.set(row,map);
  if(map.has(key))return map.get(key);
  const p=row.path,base=[t0,t1,...p.t.filter(t=>t.cmp(t0)>0&&t.cmp(t1)<0)];
  if(x0.cmp(0)*x1.cmp(0)<0)base.push(t0.s(x0.dby(d)));
  const cuts=unique(base),knots=[...cuts],pos=t=>x0.a(t.s(t0).m(d));
  for(let j=0;j+1<cuts.length;j++){
   const l=cuts[j],r=cuts[j+1],pl=p.at(l),pr=p.at(r),xl=abs(pos(l)),xr=abs(pos(r)),
    el=[pl.a(row.lower),pl.a(row.upper),Q(2).s(pl).s(row.upper),Q(2).s(pl).s(row.lower)],
    er=[pr.a(row.lower),pr.a(row.upper),Q(2).s(pr).s(row.upper),Q(2).s(pr).s(row.lower)];
   for(let k=0;k<4;k++){const yl=xl.s(el[k]),yr=xr.s(er[k]);if(yl.cmp(0)*yr.cmp(0)<0)knots.push(l.a(r.s(l).m(yl.neg()).dby(yr.s(yl))));}
  }
  const result=unique(knots).map(t=>({t,f:marginal(row,t,pos(t)).closed}));
  for(let j=1;j<result.length;j++)if(result[j].f.s(result[j-1].f).m(d).cmp(0)<0)throw Error("reflected-fan transport failure");
  map.set(key,result);return result;
 }
 function featureIntegral(row,a,d,left,right){
  a=a.map(Q);left=Q(left);right=Q(right);if(right.eq(left))return Z;
  const p=t=>a[1].a(t.s(a[0]).m(d)),points=rowTrace(row,[left,p(left)],[right,p(right)],d);let out=Z;
  for(let j=0;j+1<points.length;j++)out=out.a(points[j+1].t.s(points[j].t).m(points[j].f.a(points[j+1].f)).dby(2));
  return out;
 }
 function monster(raw){return raw?.path?.v?raw.path:raw?.v?raw:new G.PLPath(raw.route??raw);}
 function historyPlane(basis,rawMonster,selectors){
  const m=monster(rawMonster),end=m.t.at(-1);
  if(!m.x.some(x=>x.eq(-1))||!m.x.some(x=>x.eq(1)))throw Error("history plane requires both endpoint visits");
  for(const d of m.v)if(!d.eq(1)&&!d.eq(-1))throw Error("unit Monster history required");
  const g=basis.map(()=>Z);let previous=Z;
  function integrateCurrent(row,left,right){
   const cuts=unique([left,right,...m.t.filter(t=>t.cmp(left)>0&&t.cmp(right)<0)]);let s=Z;
   for(let j=0;j+1<cuts.length;j++){
    const a=cuts[j],b=cuts[j+1],x=m.at(a),d=m.at(b).s(x).cmp(0);
    s=s.a(featureIntegral(row,[a,x],d,a,b));
   }return s;
  }
  for(const piece of selectors){
   const left=Q(piece.start),right=Q(piece.end);if(!left.eq(previous)||right.cmp(left)<0||right.cmp(end)>0)throw Error("history-selector partition");
   const duration=right.s(left);
   function value(row,which,mode){
    const s=piece[which];if(!s)throw Error("missing history selector");
    if(s.current===true)return integrateCurrent(row,left,right);
    const t=Q(s.time);if(t.cmp(0)<0||t.cmp(left)>0)throw Error("selector refers to future");
    return marginal(row,t,m.at(t))[mode].m(duration);
   }
   for(let i=0;i<basis.length;i++)g[i]=g[i].a(duration.s(value(basis[i],"upper","closed")).a(value(basis[i],"lower","strict")));
   previous=right;
  }
  if(!previous.eq(end))throw Error("history-selector horizon gap");
  return{scope:"Affine upper plane for every normalized ordered mixture on this fixed reflected-fan basis; selectors are checked only for causality, not optimality.",gradient:g.map(x=>x.str()),horizon:end.str(),pieces:selectors.length};
 }
 function law(basis,weights){
  if(!basis.length||basis.length!==weights.length)throw Error("reflected law dimensions");
  const raw=weights.map(Q);for(const w of raw){w.n;if(w.cmp(0)<0)throw Error("negative weight");}
  const total=raw.reduce((s,w)=>s.a(w),Z);if(total.eq(0))throw Error("empty reflected law");
  const w=raw.map(x=>x.dby(total)),active=w.map((x,i)=>x.eq(0)?-1:i).filter(i=>i>=0),dot=v=>active.reduce((s,i)=>s.a(w[i].m(v[i])),Z);
  function features(t,x,mode="closed"){return basis.map(row=>marginal(row,t,x)[mode==="strict"?"strict":"closed"]);}
  function F(t,x,mode="closed"){return dot(features(t,x,mode));}
  function trace(a,b,d){
   const knots=[];for(const i of active)knots.push(...rowTrace(basis[i],a,b,d).map(p=>p.t));
   return unique(knots).map(t=>({t,f:F(t,a[1].a(t.s(a[0]).m(d)))}));
  }
  function positiveArea(a,b,h){
   if(a.cmp(0)>=0&&b.cmp(0)>=0)return a.a(b).m(h).dby(2);
   if(a.cmp(0)<=0&&b.cmp(0)<=0)return Z;
   return a.cmp(0)>0?h.m(a.m(a)).dby(a.s(b).m(2)):h.m(b.m(b)).dby(b.s(a).m(2));
  }
  function score(rawMonster,{gradient=false,details=false,requireComplete=true,selectors=false}={}){
   const m=monster(rawMonster);let lv=features(m.t[0],m.x[0],"strict"),hv=features(m.t[0],m.x[0],"closed"),
    L=dot(lv),H=dot(hv),lt=m.t[0],ht=m.t[0],cost=Z,pieces=0;
   const g=basis.map(()=>Z),legs=[],history=[];
   for(let j=0;j<m.v.length;j++){
    const d=m.v[j].eq(1)?1:m.v[j].eq(-1)?-1:0;if(!d)throw Error("unit Monster required");
    const a=m.vertices[j],b=m.vertices[j+1],points=trace(a,b,d),duration=b[0].s(a[0]);let part=Z,cut=b[0],found=false;
    for(let k=0;k+1<points.length;k++){
     const l=points[k],r=points[k+1],dt=r.t.s(l.t),q0=d===1?l.f.s(H):L.s(l.f),q1=d===1?r.f.s(H):L.s(r.f);
     part=part.a(O.s(H).a(L).m(dt).s(positiveArea(q0,q1,dt)));pieces++;
     if(!found&&q1.cmp(0)>0){cut=q0.cmp(0)>=0?l.t:l.t.a(q0.neg().m(dt).dby(q1.s(q0)));found=true;}
    }cost=cost.a(part);
    if(gradient){const before=cut.s(a[0]);for(let i=0;i<basis.length;i++){
     const I=featureIntegral(basis[i],a,d,cut,b[0]);
     g[i]=g[i].a(d===1?duration.m(O.a(lv[i])).s(before.m(hv[i])).s(I):duration.m(O.s(hv[i])).a(before.m(lv[i])).a(I));
    }}
    if(selectors){
     if(cut.cmp(a[0])>0)history.push({start:a[0].str(),end:cut.str(),upper:{time:ht.str()},lower:{time:lt.str()}});
     if(cut.cmp(b[0])<0)history.push({start:cut.str(),end:b[0].str(),upper:d===1?{current:true}:{time:ht.str()},lower:d===-1?{current:true}:{time:lt.str()}});
    }
    const endv=features(b[0],b[1],d===1?"closed":"strict"),rank=dot(endv);
    if(d===1&&rank.cmp(H)>0){H=rank;hv=endv;ht=b[0];}else if(d===-1&&rank.cmp(L)<0){L=rank;lv=endv;lt=b[0];}
    if(details)legs.push({direction:d,activation:cut.str(),cost:part.str(),lower:L.str(),upper:H.str()});
   }
   const complete=O.s(H).a(L).eq(0);if(requireComplete&&!complete)throw Error("incomplete reflected-fan capture");
   const euler=gradient?dot(g):null;if(gradient&&!euler.eq(cost))throw Error("reflected gradient Euler identity");
   if(selectors&&gradient){const plane=historyPlane(basis,m,history);for(let i=0;i<g.length;i++)if(!Q(plane.gradient[i]).eq(g[i]))throw Error("selector gradient mismatch");}
   return{scope:"Exact supplied unit-route cost for the ordered reflected-fan law; no unrestricted response claim.",complete,exact_cost:cost.str(),limit:cost.limit().str(),gradient:gradient?g.map(x=>x.str()):null,euler:euler?.str()??null,pieces,legs:details?legs:null,selectors:selectors?history:null};
  }
  return{score,marginal:F,features,trace,featureIntegral,weights:w.map(x=>x.str()),basis};
 }
 return{prepareInterval,prepareBasis,marginal,rowTrace,featureIntegral,historyPlane,law};
}
return{createReflectedFanTools};
})();