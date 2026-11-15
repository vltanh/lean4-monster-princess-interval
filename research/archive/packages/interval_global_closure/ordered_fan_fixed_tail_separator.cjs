/** Exact ordered-fan continuous initial-start separation for one fixed unit tail.
 * The only moving record ranks after the first turn are initial F and turn F.
 * Fixed-ray CDF levels refine the geometric quadratic cells.
 */
module.exports=(function(){
function createOrderedFanFixedTailSeparator(G,fanModule,orderedModule,rawTailModule,entries,family){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,
  OT=orderedModule.createOrderedFanTools(G,fanModule),T=OT.fan,
  raw=rawTailModule.createFanFixedTailSeparator(G,T,entries,family),
  law=OT.law(entries.map(e=>e.row),entries.map(e=>e.weight??1)),weights=law.weights.map(Q),
  active=entries.filter((_,i)=>weights[i].cmp(0)>0),[left,right]=raw.domain,c=raw.orientedCharacteristic,
  tail=family.tail.map(v=>[Q(v[0]),Q(v[1]).m(raw.firstDirection)]),cache=new Map();
 const unique=xs=>[...new Map(xs.map(Q).map(x=>[x.str(),x])).values()].sort((a,b)=>a.cmp(b));
 function bisect(xs,x,strict=false){let l=0,h=xs.length;while(l<h){const m=(l+h)>>1,q=xs[m].cmp(x);if(q<0||(!strict&&q===0))l=m+1;else h=m;}return l;}
 function initialRank(b){return law.marginal(Z,b,"strict");}
 function turnRank(b){return law.marginal(c.s(b).dby(2),c.a(b).dby(2),"closed");}
 function score(b){b=Q(b);const key=b.str();if(cache.has(key))return cache.get(key);const value=Q(law.score(raw.route(b)).exact_cost);cache.set(key,value);return value;}
 function geometricCuts(){
  const points=new Map(),add=b=>{b=Q(b);if(b.cmp(left)>=0&&b.cmp(right)<=0)points.set(b.str(),b);};add(left);add(right);
  for(const{row}of active)for(const sign of[1,-1]){
   const p=row.path,lo=sign===1?row.lower:row.upper.neg(),hi=sign===1?row.upper:row.lower.neg();
   for(const q of p.seq[(sign+1)>>1]){add(lo.s(q));add(hi.s(q));}
   for(let i=0;i<p.t.length;i++){
    add(c.s(p.t[i].m(2)));
    const upper=min(right,c.s(p.t[i].m(2))),lower=i+1<p.t.length?max(left,c.s(p.t[i+1].m(2))):left;
    if(lower.cmp(upper)>0)continue;
    const v=i<p.v.length?p.v[i]:Z,slope=O.a(v.m(sign)).dby(2),
     offset=c.m(O.s(v.m(sign))).dby(2).s(p.x[i].m(sign)).a(v.m(p.t[i]).m(sign));
    if(slope.eq(0))continue;
    for(const z of[lo,hi]){const b=z.s(offset).dby(slope);if(b.cmp(lower)>=0&&b.cmp(upper)<=0)add(b);}
   }
  }
  return[...points.values()].sort((a,b)=>a.cmp(b));
 }
 function criticalRanks(){
  const values=[Z,O],begin=max(Z,c.s(1));
  if(begin.cmp(tail[0][0])<0)for(const p of law.trace([begin,c.s(begin)],tail[0],-1))values.push(p.f);
  for(let j=0;j<tail.length;j++){
   const a=tail[j];values.push(law.marginal(a[0],a[1],"strict"),law.marginal(a[0],a[1],"closed"));
   if(j+1<tail.length){const b=tail[j+1],d=b[1].s(a[1]).cmp(0);for(const p of law.trace(a,b,d))values.push(p.f);}
  }
  return unique(values);
 }
 function geometryCuts({verifyAffine=true}={}){
  const base=geometricCuts(),targets=criticalRanks(),points=new Map(base.map(x=>[x.str(),x]));let affineChecks=0,rankCuts=0;
  for(let j=0;j+1<base.length;j++){
   const a=base[j],width=base[j+1].s(a);
   for(const f of[initialRank,turnRank]){
    const f1=f(a.a(width.dby(3))),f2=f(a.a(width.m(2).dby(3))),slope=f2.s(f1).m(3),offset=f1.s(slope.dby(3));
    if(slope.cmp(0)<0)throw Error("nonmonotone first-leg ordered rank");
    if(verifyAffine){if(!f(a.a(width.dby(2))).eq(offset.a(slope.dby(2))))throw Error("missing ordered rank geometry boundary");affineChecks++;}
    if(slope.eq(0))continue;
    for(let k=bisect(targets,offset);k<targets.length&&targets[k].cmp(offset.a(slope))<0;k++){
     const u=targets[k].s(offset).dby(slope);if(u.cmp(0)<=0||u.cmp(1)>=0)continue;
     const b=a.a(width.m(u));if(!points.has(b.str()))rankCuts++;points.set(b.str(),b);
    }
   }
  }
  return{cuts:[...points.values()].sort((a,b)=>a.cmp(b)),base_cells:Math.max(0,base.length-1),critical_rank_count:targets.length,rank_cuts:rankCuts,affine_checks:affineChecks};
 }
 function separate({verifyPolynomial=true,keepCells=false,maxCells=200000,onProgress=()=>{}}={}){
  const geometry=geometryCuts(),cuts=geometry.cuts;if(cuts.length-1>maxCells)throw Error("ordered fixed-tail arrangement exceeds cell cap");
  let best=null,bestStart=null,stationary=0,checks=0;const cells=[];
  function candidate(b){const cost=score(b);if(best===null||cost.cmp(best)<0){best=cost;bestStart=b;}}
  for(const b of cuts)candidate(b);
  for(let j=0;j+1<cuts.length;j++){
   const a=cuts[j],width=cuts[j+1].s(a),at=u=>score(a.a(width.m(u))),
    f1=at(Q("1/4")),f2=at(Q("1/2")),f3=at(Q("3/4")),
    q2=f1.s(f2.m(2)).a(f3).m(8),q1=f3.s(f1).m(2).s(q2),q0=f2.s(q1.dby(2)).s(q2.dby(4)),
    polynomial=u=>q0.a(q1.m(u)).a(q2.m(u.m(u)));
   if(verifyPolynomial)for(const u of[Q("1/3"),Q("2/3")]){if(!polynomial(u).eq(at(u)))throw Error("missing ordered fixed-tail hinge boundary");checks++;}
   let root=null;if(q2.cmp(0)>0){const u=q1.neg().dby(q2.m(2));if(u.cmp(0)>0&&u.cmp(1)<0){root=a.a(width.m(u));if(!score(root).eq(polynomial(u)))throw Error("ordered stationary polynomial mismatch");candidate(root);stationary++;}}
   if(keepCells)cells.push({left:a.str(),right:cuts[j+1].str(),local_coefficients:[q0.str(),q1.str(),q2.str()],stationary_start:root?.str()??null});
   if(j%32===31)onProgress({cells:j+1,total:cuts.length-1});
  }
  return{scope:"Complete continuous starts for this fixed completed unit tail against the ordered common-quantile law of immutable interval fans; no separation of other tails.",
   complete:true,minimum:best.str(),limit:best.limit().str(),decimal:best.limit().num(),start:bestStart.str(),physical_start:bestStart.m(raw.firstDirection).str(),
   first_direction:raw.firstDirection,domain:[left.str(),right.str()],route:raw.route(bestStart).json(),
   cell_count:cuts.length-1,base_cell_count:geometry.base_cells,critical_rank_count:geometry.critical_rank_count,rank_refinement_cuts:geometry.rank_cuts,
   affine_rank_checks:geometry.affine_checks,stationary_candidates:stationary,polynomial_checks:checks,score_queries:cache.size,
   cuts:cuts.map(x=>x.str()),cells:keepCells?cells:null,normalized_weights:law.weights,arithmetic:G.stats()};
 }
 return{score,route:raw.route,geometricCuts,criticalRanks,geometryCuts,separate,law,domain:raw.domain,firstDirection:raw.firstDirection};
}
return{createOrderedFanFixedTailSeparator};
})();