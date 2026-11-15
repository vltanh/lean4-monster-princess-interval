/** Frozen physical-pair scoring and normalized implicit comonotone laws.
 * No path is re-realized from labels here. A new realization must receive a
 * new row identity. Inverse caches may grow; physical vertices are unchanged.
 */
module.exports = (function(){
function createFrozenLawTools(G){
 const counters={inverseQueries:0,inverseHits:0,constantComputations:0,germComputations:0,pairScores:0};
 const Q=G.Q,Z=G.ZERO,O=G.ONE,constants=new WeakMap(),limitCache=new WeakMap(),reflections=new WeakMap();
 function constant(x){return x.p.length===1&&x.q.length===1;}
 function limit(x){let r=limitCache.get(x);if(!r){r=x.limit();limitCache.set(x,r);}return r;}
 function cmp(a,b){return constant(a)&&constant(b)?limit(a).cmp(limit(b)):a.cmp(b);}
 function preparePath(raw){
  if(raw&&Array.isArray(raw.t)&&Array.isArray(raw.seq)&&raw.inverseCache)return raw;
  return new G.PLPath(raw);
 }
 function constantPath(p){
  if(constants.has(p))return constants.get(p);
  if(!p.t.every(constant)||!p.x.every(constant)){constants.set(p,null);return null;}
  const r={t:p.t.map(limit),v:p.v.map(limit),seq:p.seq.map(a=>a.map(limit))};constants.set(p,r);return r;
 }
 function inverse(p,h,q,key=q.str()){
  counters.inverseQueries++;const old=p.inverseCache[h].get(key);if(old){counters.inverseHits++;return old;}
  const c=constant(q)?constantPath(p):null;
  if(c){
   counters.constantComputations++;const target=limit(q),seq=c.seq[h],one=limit(O);if(target.cmp(seq[0])<0)throw Error("inverse precedes initial value");
   let l=0,r=seq.length;while(l<r){const m=(l+r)>>1;if(seq[m].cmp(target)<0)l=m+1;else r=m;}
   let t;
   if(l===0)t=limit(Z);
   else if(l===seq.length)t=c.t.at(-1).a(target.s(seq.at(-1)));
   else{const rate=one.s(c.v[l-1].m(2*h-1));if(rate.cmp(0)<=0)throw Error("flat constant inverse");t=c.t[l-1].a(target.s(seq[l-1]).dby(rate));}
   const ans=Q(t.str());p.inverseCache[h].set(key,ans);return ans;
  }
  counters.germComputations++;const seq=p.seq[h];if(cmp(q,seq[0])<0)throw Error("inverse precedes initial value");
  let l=0,r=seq.length;while(l<r){const m=(l+r)>>1;if(cmp(seq[m],q)<0)l=m+1;else r=m;}
  let ans;
  if(l===0)ans=Z;
  else if(l===seq.length)ans=p.t.at(-1).a(q.s(seq.at(-1)));
  else{const rate=O.s(p.v[l-1].m(2*h-1));if(cmp(rate,Z)<=0)throw Error("flat inverse");ans=p.t[l-1].a(q.s(seq[l-1]).dby(rate));}
  p.inverseCache[h].set(key,ans);return ans;
 }
 function prepareMonster(raw){
  let points=raw;
  if(raw&&raw.exact_light)points=raw.exact_light.map(([a,b])=>{const u=Q(a),v=Q(b);return[u.a(v).dby(2),u.s(v).dby(2)];});
  else if(raw&&raw.kind==="PATH"&&raw.parameters){
   points=[];for(let j=0;j<raw.parameters.length;j+=2){const u=Q(raw.parameters[j]),v=Q(raw.parameters[j+1]);points.push([u.a(v).dby(2),u.s(v).dby(2)]);}
  }else if(raw&&raw.route)points=raw.route;
  const p=preparePath(points),legs={1:[], "-1":[]};
  for(let j=0;j<p.v.length;j++){
   const d=p.v[j].eq(1)?1:p.v[j].eq(-1)?-1:0;
   if(!d)throw Error("pure scorer requires unit Monster legs");
   const target=p.t[j].s(p.x[j].m(d));legs[d].push({start:p.t[j],end:p.t[j+1],target,key:target.str(),direction:d});
  }
  return{path:p,initial:p.x[0],legs,route:p.json()};
 }
 function capture(path,monster,sign=1){
  const p=preparePath(path),m=monster.legs?monster:prepareMonster(monster);
  if(sign!==1&&sign!==-1)throw Error("reflection sign");
  const x=sign===1?p.x[0]:p.x[0].neg(),d=cmp(x,m.initial);
  if(!d)return Z;
  for(const leg of m.legs[d]){
   const h=(d*sign+1)>>1,t=inverse(p,h,leg.target,leg.key);
   if(cmp(t,leg.start)<0)throw Error("closing inverse precedes the leg");
   if(cmp(t,leg.end)<=0)return t;
  }
  return null;
 }
 function pairScore(path,monster,{fullCost=false}={}){
  counters.pairScores++;const p=preparePath(path),m=monster.legs?monster:prepareMonster(monster),plus=capture(p,m,1),minus=capture(p,m,-1);
  if(plus===null||minus===null)return{complete:false,plus:plus===null?null:plus.str(),minus:minus===null?null:minus.str()};
  const score=limit(plus).a(limit(minus)).dby(2);
  return{complete:true,plus:plus.str(),minus:minus.str(),limit:score.str(),decimal:score.num(),
   exact_cost:fullCost?plus.a(minus).dby(2).str():null};
 }
 function reflection(p){
  let r=reflections.get(p);if(r)return r;
  r=Object.create(G.PLPath.prototype);r.t=p.t;r.x=p.x.map(x=>x.neg());r.vertices=r.t.map((t,j)=>[t,r.x[j]]);
  r.v=p.v.map(v=>v.neg());r.seq=[p.seq[1],p.seq[0]];r.inverseCache=[p.inverseCache[1],p.inverseCache[0]];
  reflections.set(p,r);return r;
 }
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const c=a%b;a=b;b=c;}return a;}
 function orderedLaw(rows){
  const active=[];let denominator=1n;
  for(let j=0;j<rows.length;j++){
   const row=rows[j],w=Q(row.weight);
   if(!constant(w))throw Error("probability weights must be exact constants");
   const r=limit(w);if(r.cmp(0)<0)throw Error("negative probability");if(r.eq(0))continue;
   const p=preparePath(row.path);denominator=denominator/gcd(denominator,r.d)*r.d;
   active.push({id:row.id===undefined?j:row.id,path:p,weight:r,provenance:row.provenance??null});
  }
  if(!active.length)throw Error("empty law");
  let ws=active.map(r=>r.weight.n*(denominator/r.weight.d)),g=ws.reduce((a,b)=>gcd(a,b),0n);
  ws=ws.map(w=>w/g);const pairTotal=ws.reduce((a,b)=>a+b,0n),positive=active.map(x=>x.path),
   paths=positive.concat(positive.map(reflection)),weights=ws.concat(ws),W=2n*pairTotal,
   metadata=active.map((x,j)=>({id:x.id,pair_weight:Q(ws[j]).dby(pairTotal).str(),provenance:x.provenance}));
  const prepared={paths,weights,W,positive,pairWeights:ws,pairTotal,metadata};
  function ranks(t,x){
   t=Q(t);x=Q(x);let strict=0n,closed=0n;
   for(let j=0;j<paths.length;j++){const s=cmp(paths[j].at(t),x);if(s<0)strict+=weights[j];if(s<=0)closed+=weights[j];}
   return{strict,closed,total:W};
  }
  function quantile(t,rank){
   t=Q(t);rank=Q(rank);if(rank.cmp(0)<0||rank.cmp(1)>0)throw Error("rank outside [0,1]");
   const values=paths.map((p,j)=>({x:p.at(t),w:weights[j]})).sort((a,b)=>cmp(a.x,b.x));
   let mass=0n;for(const z of values){mass+=z.w;if(Q(mass).cmp(rank.m(W))>=0)return z.x;}
   throw Error("quantile normalization");
  }
  function dictionary(){
   const coordinates=[],index=new Map();
   function coordinate(x){const s=x.str();if(!index.has(s)){index.set(s,coordinates.length);coordinates.push(s);}return index.get(s);}
   return{scope:"Frozen physical rows with normalized pair weights; ordering is implicit through common quantiles.",
    coordinate_dictionary:coordinates,
    paths:positive.map((p,j)=>({row:metadata[j].id,weight:metadata[j].pair_weight,provenance:metadata[j].provenance,
     path:p.vertices.map(v=>v.map(coordinate))}))};
  }
  return{prepared,ranks,quantile,dictionary,metadata};
 }
 return{preparePath,prepareMonster,inverse,capture,pairScore,orderedLaw,stats:()=>({...counters})};
}
return{createFrozenLawTools};
})();