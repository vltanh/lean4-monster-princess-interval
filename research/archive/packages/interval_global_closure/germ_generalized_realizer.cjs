/** Legal light-graph realization over QQ(epsilon), with a subordinate label scale.
 * Side labels use epsilon^K, connectors epsilon^(K+1), and the floor epsilon^(K+5).
 * K is chosen from the entire model; clipped polynomial degrees grow additively.
 * Fill and strictification choices are explicit candidate data, not equivalences
 * of adaptive responses. Zero-side traces after strictification are reported.
 */
module.exports = (function(){
function createGeneralizedRealizer(G){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,e=G.eps;
 const min=(a,b)=>a.cmp(b)<=0?a:b;
 function valuation(x){
  x=Q(x);const i=x.p.findIndex(c=>c.n!==0n),j=x.q.findIndex(c=>c.n!==0n);
  return i<0?Infinity:i-j;
 }
 function chooseScale(queryV,baseLevels,{extraGeometry=[],power=null}={}){
  const vv=queryV.map(Q),bb=baseLevels.map(Q);
  const pool=[Q(-1),Z,O,Q(2),...bb,...vv,...vv.map(v=>v.neg()),...vv.map(v=>v.a(2)),...extraGeometry.map(Q)];
  for(const x of pool)x.limit();
  pool.sort((a,b)=>a.cmp(b));const unique=pool.filter((x,j)=>!j||!x.eq(pool[j-1]));
  const gaps=unique.slice(1).map((x,j)=>x.s(unique[j]));
  let order=0;for(const g of gaps){if(g.cmp(0)<=0)throw Error("nonpositive geometry gap");order=Math.max(order,valuation(g));}
  const K=power===null?Math.max(1,order+1):Number(power);
  if(!Number.isSafeInteger(K)||K<1||K<=order)throw Error("subordinate power does not dominate the geometry");
  const delta=e.pow(K);
  for(const g of gaps)if(g.cmp(delta.m(8))<=0)throw Error("geometry gap does not dominate label shifts");
  return{power:K,delta:delta.str(),connector:e.pow(K+1).str(),floor:e.pow(K+5).str(),max_gap_order:order,distinct_geometry:unique.length,gap_count:gaps.length,radius:G.stats().radius};
 }
 function realize(queryV,baseLevels,indices,options={}){
  const {fill="avoided",strictMode="affine",auditTraces=true,waveOffset=4}=options;
  if(!["late","early","avoided","common-wave"].includes(fill))throw Error("unknown fill choice");
  if(!["none","affine","clip"].includes(strictMode))throw Error("unknown strictification");
  if(!Number.isSafeInteger(waveOffset)||waveOffset<2)throw Error("wave offset must be an integer >=2");
  const scale=options.scale||chooseScale(queryV,baseLevels,options);
  const delta=Q(scale.delta),connector=e.pow(scale.power+1),floor=e.pow(scale.power+5),vv=queryV.map(Q),allBases=baseLevels.map(Q);
  if(vv.length!==indices.length||vv.length<2)throw Error("query dimensions");
  if(!delta.eq(e.pow(scale.power)))throw Error("invalid subordinate scale");
  const bases=indices.map(k=>{
   if(!Number.isSafeInteger(k)||k<0||Math.floor(k/3)>=allBases.length)throw Error("invalid label");
   return allBases[Math.floor(k/3)];
  }),sides=indices.map(k=>k%3-1),values=bases.map((b,j)=>b.a(delta.m(sides[j])));
  if(!vv[0].eq(-1)||!values[0].eq(0))throw Error("virtual initial query must be (U,V)=(0,-1)");
  for(let j=0;j<vv.length;j++){
   if(values[j].cmp(0)<0||values[j].s(vv[j]).cmp(0)<0||values[j].s(vv[j]).cmp(2)>0)throw Error("label violates the physical strip");
   if(j&&(vv[j].cmp(vv[j-1])<=0||values[j].cmp(values[j-1])<0))throw Error("nonmonotone query profile");
  }
  const points=[[Z,Q(-1)]],intervals=[],changes=[];
  function add(u,v){
   u=Q(u);v=Q(v);const p=points.at(-1);
   if(u.eq(p[0])&&v.eq(p[1]))return;
   if(u.cmp(p[0])<0||v.cmp(p[1])<0||u.s(v).cmp(0)<0||u.s(v).cmp(2)>0)throw Error("illegal light graph");
   points.push([u,v]);
  }
  for(let j=1;j<vv.length;j++){
   const v=vv[j],prevV=vv[j-1],prev=values[j-1],target=values[j],
    margin=min(connector,v.s(prevV).dby(3));
   let before=fill==="early"?prevV.a(margin):v.s(margin),reason=fill==="early"?"early-maximal":"late-minimal";
   const exactIsolated=bases[j-1].eq(v)&&bases[j].cmp(v)>0;
   if(exactIsolated&&(fill==="avoided"||fill==="common-wave")){
    before=min(before,fill==="common-wave"?v.s(delta.m(waveOffset)):prev.s(delta));
    reason=fill==="common-wave"?"common-wave-offset":"isolated-avoidance";
    if(before.cmp(prevV)<=0)throw Error("avoided connector crosses previous query");
    changes.push({query:j,V:v.str(),previousSide:sides[j-1],before:before.str(),incoming:prev.str(),gap:prev.s(before).str(),reason});
   }
   if(before.cmp(prevV)<=0||before.cmp(v)>=0)throw Error("connector not inside query interval");
   const center=before.cmp(prev)>0;
   intervals.push({query:j,reason,before:before.str(),exactIsolated,merelyEqualLimit:!bases[j-1].eq(v)&&bases[j-1].limit().eq(v.limit()),centerWait:center?{from:prev.str(),to:before.str()}:null});
   add(prev,min(before,prev));if(center)add(before,before);
   add(min(target,before.a(2)),before);
   if(target.cmp(before.a(2))>0)add(target,target.s(2));
   add(target,v);
  }
  function trace(ps,v){
   let lo=0,hi=ps.length;
   while(lo<hi){const m=(lo+hi)>>1;if(ps[m][1].cmp(v)<0)lo=m+1;else hi=m;}
   if(lo<ps.length&&ps[lo][1].eq(v)){
    let end=lo;while(end+1<ps.length&&ps[end+1][1].eq(v))end++;
    return{first:ps[lo][0],last:ps[end][0]};
   }
   if(lo===0)throw Error("query before virtual graph");
   if(lo===ps.length){const[u,w]=ps.at(-1),z=v.a(u.s(w));return{first:z,last:z};}
   const[a,b]=ps[lo-1],[c,d]=ps[lo],z=a.a(c.s(a).m(v.s(b)).dby(d.s(b)));
   return{first:z,last:z};
  }
  const eta=strictMode==="none"?Z:floor;
  let transformed;
  if(strictMode==="affine")transformed=points.map(([u,v])=>{const h=eta.m(O.s(u).a(v));return[u.a(h),v.s(h)];});
  else if(strictMode==="none")transformed=points;
  else{
   transformed=[];
   function push(u,v){
    const t=u.a(v).dby(2),r=u.s(v).dby(2),p=r.cmp(eta)<0?eta:r.cmp(O.s(eta))>0?O.s(eta):r,z=[t.a(p),t.s(p)],old=transformed.at(-1);
    if(!old||!z[0].eq(old[0])||!z[1].eq(old[1]))transformed.push(z);
   }
   for(let j=0;j+1<points.length;j++){
    const[u0,v0]=points[j],[u1,v1]=points[j+1],r0=u0.s(v0).dby(2),r1=u1.s(v1).dby(2),cuts=[];
    if(!r0.eq(r1))for(const h of [eta,O.s(eta)]){
     if((h.cmp(r0)>0&&h.cmp(r1)<0)||(h.cmp(r0)<0&&h.cmp(r1)>0))cuts.push(h);
    }
    cuts.sort((a,b)=>r1.cmp(r0)>0?a.cmp(b):b.cmp(a));push(u0,v0);
    for(const h of cuts){
     if(u0.eq(u1))push(u0,u0.s(h.m(2)));
     else if(v0.eq(v1))push(v0.a(h.m(2)),v0);
     else throw Error("nonunit raw clipping edge");
    }
    push(u1,v1);
   }
  }
  const traces=[],nonzeroFailures=[],zeroChanges=[];
  if(auditTraces)for(let j=0;j<vv.length;j++){
   const pre=trace(points,vv[j]);if(!pre.first.eq(values[j])||!pre.last.eq(values[j]))throw Error("raw query trace mismatch");
   const post=trace(transformed,vv[j]),first=post.first.cmp(bases[j]),last=post.last.cmp(bases[j]);
   const row={query:j,side:sides[j],postFirst:first,postLast:last};
   traces.push(row);
   if(sides[j]&&(first!==sides[j]||last!==sides[j]))nonzeroFailures.push(row);
   if(!sides[j]&&(first!==0||last!==0))zeroChanges.push(row);
  }
  if(nonzeroFailures.length)throw Error("nonzero label side changed");
  const path=[];
  for(let j=0;j+1<transformed.length;j++){
   const[u0,v0]=transformed[j],[u1,v1]=transformed[j+1],t0=u0.a(v0).dby(2),t1=u1.a(v1).dby(2);
   if(t1.cmp(0)<0)continue;
   const x0=u0.s(v0).dby(2),x1=u1.s(v1).dby(2);
   if(!path.length){
    if(t0.cmp(0)>0)throw Error("missing time-zero crossing");
    path.push([Z,x0.a(x1.s(x0).m(t0.neg()).dby(t1.s(t0)))]);
   }
   if(t1.cmp(path.at(-1)[0])>0)path.push([t1,x1]);
  }
  const physical=new G.PLPath(path);
  if(strictMode!=="affine"&&physical.v.some(v=>!v.eq(-1)&&!v.eq(0)&&!v.eq(1)))throw Error("unit/wait property failed");
  return{path:physical,scale,fill,strictMode,intervals,changes,traces,zeroChanges,rawLight:points.map(p=>p.map(x=>x.str())),radius:G.stats().radius};
 }
 return{valuation,chooseScale,realize};
}
return{createGeneralizedRealizer};
})();