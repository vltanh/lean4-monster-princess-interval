/** Exact finite quantile-family source from an ordered symmetric path certificate.
 * The supplied physical vertices are immutable. There is no germ re-realization.
 * Pair probabilities select a nonnegative path, then reflect with probability 1/2.
 */
module.exports = (function(){
function createCertifiedSeedSource(G,F){
 const Q=G.Q;
 function integer(x,name){if(!Number.isSafeInteger(x))throw Error(name+" must be a safe integer");return BigInt(x);}
 function prepare(data,{prefix="certified169",provenance=null}={}){
  const S=integer(data.S,"coordinate scale");if(S<=0n)throw Error("positive scale");
  if(!Array.isArray(data.paths_h)||data.paths_h.length!==data.weights_h.length)throw Error("seed dimensions");
  const total=data.weights_h.reduce((z,w)=>z+integer(w,"weight"),0n);
  if(total<=0n||total!==integer(data.weight_total,"weight total"))throw Error("seed normalization");
  const rows=data.paths_h.map((raw,i)=>{
   const weight=integer(data.weights_h[i],"weight");if(weight<=0n)throw Error("nonpositive seed weight");
   const vertices=raw.map(([t,x])=>[Q(integer(t,"time")).dby(S),Q(integer(x,"position")).dby(S)]),path=F.preparePath(vertices);
   if(path.x.some(x=>x.cmp(0)<0)||!path.x.at(-1).eq(1))throw Error("source is not nonnegative with endpoint tail");
   if(path.v.some(v=>!v.eq(-1)&&!v.eq(0)&&!v.eq(1)))throw Error("source has a nonunit nonwait leg");
   return{id:prefix+":"+i,path,weight:Q(weight).dby(total).str(),provenance:{source:provenance,index:i}};
  });
  let orderChecks=0;
  for(let i=1;i<rows.length;i++)for(const t of rows[i-1].path.t.concat(rows[i].path.t)){
   if(rows[i-1].path.at(t).cmp(rows[i].path.at(t))>0)throw Error("source paths are not ordered");orderChecks++;
  }
  const law=F.orderedLaw(rows),attaining=data.attaining_monster?.map(([t,x])=>[Q(integer(t,"monster time")).dby(S),Q(integer(x,"monster position")).dby(S)]);
  return{rows,law,attaining,declaredValue:Q(data.value),orderChecks,
   originalVertices:data.paths_h.reduce((z,p)=>z+p.length,0),vertices:rows.reduce((z,r)=>z+r.path.t.length,0),
   scale:S,weightTotal:total};
 }
 function column(seed,atom,{fullCost=false}={}){
  const m=atom.legs?atom:F.prepareMonster(atom),values=[],exactCosts=[],records=[];let mean=Q(0);
  for(let i=0;i<seed.rows.length;i++){
   const v=F.pairScore(seed.rows[i].path,m,{fullCost});if(!v.complete)throw Error("incomplete source/Monster capture");
   values.push(v.limit);if(fullCost)exactCosts.push(v.exact_cost);
   mean=mean.a(Q(fullCost?v.exact_cost:v.limit).m(seed.rows[i].weight));
   records.push([v.plus,v.minus]);
  }
  return{route:m.route,limits:values,exactCosts:fullCost?exactCosts:null,
   mean:mean.str(),meanLimit:mean.limit().str(),firstHits:records};
 }
 function bestResponse(seed,columns,weights){
  if(columns.length!==weights.length)throw Error("source-oracle dimensions");
  const ws=weights.map(Q);if(ws.some(w=>w.p.length!==1||w.q.length!==1||w.cmp(0)<0))throw Error("constant nonnegative Monster probabilities required");
  const sum=ws.reduce((a,b)=>a.a(b),Q(0));if(sum.cmp(0)<=0)throw Error("empty Monster law");
  const scores=seed.rows.map((_,i)=>columns.reduce((z,c,j)=>ws[j].eq(0)?z:z.a(Q(c.limits[i]).m(ws[j])),Q(0)).dby(sum));
  let best=scores[0];for(const s of scores)if(s.cmp(best)>0)best=s;
  const ids=scores.flatMap((s,i)=>s.eq(best)?[seed.rows[i].id]:[]);
  const sourceMean=scores.reduce((z,s,i)=>z.a(s.m(seed.rows[i].weight)),Q(0));
  return{value:best.str(),decimal:best.limit().num(),ids,scores:scores.map(s=>s.str()),
   sourceMean:sourceMean.str(),sourceMeanDecimal:sourceMean.limit().num(),
   scope:"Exact maximum over every quantile path of the supplied finite ordered source; not the unrestricted Princess maximum."};
 }
 return{prepare,column,bestResponse};
}
return{createCertifiedSeedSource};
})();
