/**
 * Independent chronological segment-intersection audit of frozen germ pairs.
 * No inverse query or running-rank capture routine is used by directHit.
 */
module.exports = (function(){
function verifyFrozenPairIndependent(G,F,R,fixtures,upperFixtures,{dictionary=null,hydrate=null}={}){
 const Q=G.Q,Z=G.ZERO,O=G.ONE;
 let comparisons=0,realizations=0,actualComparisons=0;
 const cases=[],componentRows=[];
 function directHit(monster,princess,sign=1){
  let j=0;
  for(let i=0;i+1<monster.t.length;i++){
   let t=monster.t[i],end=monster.t[i+1];
   while(j+1<princess.t.length&&princess.t[j+1].cmp(t)<=0)j++;
   while(t.cmp(end)<0){
    const pe=j+1<princess.t.length?princess.t[j+1]:end;
    const next=pe.cmp(end)<0?pe:end;
    const pv=j<princess.v.length?princess.v[j]:Z;
    const px=princess.x[j].a(pv.m(t.s(princess.t[j]))).m(sign);
    const mx=monster.x[i].a(monster.v[i].m(t.s(monster.t[i])));
    const gap=px.s(mx),sgn=gap.cmp(0);
    if(!sgn)return t;
    const rate=pv.m(sign).s(monster.v[i]);
    if(!rate.eq(0)){
     const h=gap.neg().dby(rate);
     if(h.cmp(0)>=0&&h.cmp(next.s(t))<=0)return t.a(h);
    }
    t=next;
    if(j+1<princess.t.length&&princess.t[j+1].cmp(t)<=0)j++;
   }
  }
  const t=monster.t.at(-1),x=princess.at(t).m(sign);
  return x.eq(monster.x.at(-1))?t:null;
 }
 function check(p,m,{actual=false}={}){
  const score=F.pairScore(p,m,{fullCost:true}),raw=[];
  for(const sign of [1,-1]){
   const t=directHit(m.path,p,sign),s=sign===1?score.plus:score.minus;
   if((t===null)!==(s===null)||t!==null&&!t.eq(Q(s)))throw Error("frozen scorer / chronological intersection mismatch");
   raw.push(t);comparisons++;if(actual)actualComparisons++;
  }
  if(raw.every(x=>x!==null)){
   const c=raw[0].a(raw[1]).dby(2);
   if(!c.eq(Q(score.exact_cost))||!c.limit().eq(Q(score.limit).limit()))throw Error("pair mean mismatch");
   return c;
  }
  return null;
 }
 function M1(a,d){
  a=Q(a);const end=O.s(a.m(d)),p=[[Z,a]];
  if(end.cmp(0)>0)p.push([end,Q(d)]);
  p.push([end.a(2),Q(-d)]);
  return F.prepareMonster(p);
 }
 const specialRoutes=[
 [[0,"1/4"],["1/4",0],["3/4","1/2"],["9/4",-1],["17/4",1]],
 [[0,0],["1/2","1/2"],["3/2","-1/2"],[3,1],[5,-1]]
 ];
 for(const f of fixtures){
  const P=G.prepare(f.paths,f.weights),all=P.paths.map(p=>p.x[0]).concat([Q(-1),Q(1)]).sort((a,b)=>a.cmp(b)),
   starts=all.filter((x,j)=>!j||!x.eq(all[j-1])),ms=[];
  for(const x of starts)for(const d of [-1,1])ms.push(M1(x,d));
  for(const route of specialRoutes)ms.push(F.prepareMonster(route));
  const before=comparisons;
  for(const p of P.paths)for(const m of ms)check(p,m);
  cases.push({name:f.name,paths:P.paths.length,monsters:ms.length,signed_comparisons:comparisons-before});
 }
 for(const f of upperFixtures){
  const scale=R.chooseScale(f.query_v,f.base_levels),ms=f.atoms.map(a=>F.prepareMonster(a));
  ms.push(M1(Q("15/16").s(G.eps),-1));
  const before=comparisons;
  for(const lab of [f.labels,f.maximum_labels])for(const strictMode of ["clip","affine"]){
   const p=R.realize(f.query_v,f.base_levels,lab,{scale,fill:"avoided",strictMode,auditTraces:true}).path;
   for(const m of ms)check(p,m);
   const weights=f.nums.map(x=>Q(x).dby(f.den));
   let score=Z;for(let j=0;j<f.atoms.length;j++)score=score.a(Q(F.pairScore(p,ms[j],{fullCost:true}).exact_cost).m(weights[j]));
   if(!score.limit().eq(Q(f.result.value).limit()))throw Error("physical maximizing limit differs from upper cut");
   realizations++;
  }
  cases.push({name:"upper_"+f.name,signed_comparisons:comparisons-before,scale_K:scale.K});
 }
 let actual=null;
 if(dictionary){
  if(!hydrate)throw Error("hydrate is required for dictionary");
  const P=hydrate(dictionary),routes=[M1(Q("15/16").s(G.eps),-1),M1("7/8",-1)],means=[];
  for(const m of routes){
   let mean=Z;
   for(let j=0;j<P.positive.length;j++){
    const p=P.positive[j],before=JSON.stringify(p.json()),value=check(p,m,{actual:true});
    if(value===null)throw Error("complete unit Monster did not capture");
    if(JSON.stringify(p.json())!==before)throw Error("physical row changed");
    mean=mean.a(value.m(P.weights[j]));
   }
   mean=mean.dby(P.W/2n);means.push({route:m.route,raw_pair_cost:mean.str(),limit:mean.limit().str()});
  }
  actual={positive_paths:P.positive.length,signed_comparisons:actualComparisons,routes:means};
 }
 return{scope:"Independent chronological segment intersections; immutable physical Princess germs.",
  signed_capture_equalities:comparisons,upper_maximizer_realizations:realizations,cases,actual,
  cache:F.stats(),arithmetic:G.stats()};
}
return{verifyFrozenPairIndependent};
})();