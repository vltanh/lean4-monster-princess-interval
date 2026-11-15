/** Independent direct first-leg segment replay for an inward-first M1 route. */
module.exports = function verifyFirstLeg(G,prepared,start="7/8"){
 const a=G.Q(start),T=a.a(1),final=a.a(3),gapCache=new Map(),rootCache=new Map();
 let mass=0n,cost=G.ZERO;const hits=[];
 function gap(t,x){const key=t.str()+"|"+x.str();if(!gapCache.has(key))gapCache.set(key,x.s(a.s(t)));return gapCache.get(key);}
 for(let j=0;j<prepared.paths.length;j++){
  const p=prepared.paths[j];if(p.x[0].cmp(a)>0)continue;
  const vertices=p.vertices.filter(v=>v[0].cmp(T)<=0);
  if(!vertices.at(-1)[0].eq(T))vertices.push([T,p.at(T)]);
  let previous=null,hit=null;
  for(const[t,x]of vertices){
   const f=gap(t,x);if(f.eq(0)){hit=t;break;}
   if(previous&&previous.f.cmp(0)<0&&f.cmp(0)>0){
    const key=previous.t.str()+"|"+previous.x.str()+";"+t.str()+"|"+x.str();
    if(!rootCache.has(key))rootCache.set(key,previous.t.a(t.s(previous.t).m(previous.f.neg()).dby(f.s(previous.f))));
    hit=rootCache.get(key);break;
   }
   previous={t,x,f};
  }
  if(hit===null||hit.cmp(T)>0)throw Error("unit first-leg capture missing");
  mass+=prepared.weights[j];cost=cost.a(hit.m(prepared.weights[j]));
  hits.push({path:j,time:hit.str(),mass:String(prepared.weights[j])});
 }
 const moment=cost.dby(prepared.W),M=G.Q(mass).dby(prepared.W);
 const ceiling=moment.a(G.ONE.s(M).m(final));
 return{start:a.str(),first_end:T.str(),final_end:final.str(),
  signed_paths:prepared.paths.length,captured_paths:hits.length,
  captured_mass:M.str(),first_moment:moment.str(),first_moment_limit:moment.limit().str(),
  ceiling:ceiling.str(),ceiling_limit:ceiling.limit().str(),
  ceiling_decimal:ceiling.limit().num(),individual_hits:hits,arithmetic:G.stats(),
  cache:{vertices:gapCache.size,intersection_segments:rootCache.size}};
};