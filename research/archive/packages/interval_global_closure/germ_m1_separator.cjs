/** Complete M1 separation for a finite physical law, including QQ(epsilon) germs.
 * Every start is dominated by a finite initial-support start for the same
 * endpoint-sweep orientation. Ordered costs use first-inverse marginal moments.
 */
module.exports = (function(){
function createM1Separator(G,unitScorer=null){
 const Q=G.Q,Z=G.ZERO;
 function starts(prepared){
  const a=prepared.paths.map(p=>p.x[0]).concat([Q(-1),Q(1)]);
  a.sort((x,y)=>x.cmp(y));return a.filter((x,j)=>!j||!x.eq(a[j-1]));
 }
 function route(a,d){
  a=Q(a);if(d!==-1&&d!==1)throw Error("direction must be +1 or -1");
  if(a.cmp(-1)<0||a.cmp(1)>0)throw Error("illegal start");
  const t=Q(1).s(a.m(d)),p=[[Z,a]];
  if(t.cmp(0)>0)p.push([t,Q(d)]);p.push([t.a(2),Q(-d)]);return p;
 }
 function inverse(p,h,target){
  const q=Q(target),seq=p.seq[h],key=q.str(),old=p.inverseCache[h].get(key);
  if(old)return old;
  if(q.cmp(seq[0])<0)throw Error("inverse before initial value");
  let l=0,r=seq.length;
  while(l<r){const m=(l+r)>>1;if(seq[m].cmp(q)<0)l=m+1;else r=m;}
  let ans;
  if(l===0)ans=Z;
  else if(l===seq.length)ans=p.t.at(-1).a(q.s(seq.at(-1)));
  else{
   const rate=Q(1).s(p.v[l-1].m(2*h-1));
   if(rate.cmp(0)<=0)throw Error("flat first-inverse crossing");
   ans=p.t[l-1].a(q.s(seq[l-1]).dby(rate));
  }
  p.inverseCache[h].set(key,ans);return ans;
 }
 function score(prepared,a,d,{components=false}={}){
  a=Q(a);const path=route(a,d),{paths,weights,W}=prepared,T=Q(1).s(a.m(d)),
   firstH=(d+1)>>1,secondH=1-firstH,secondTarget=T.a(1);
  let captured=0n,first=Z,raw=Z;const items=[],rawTimes=[];
  for(let j=0;j<paths.length;j++){
   const p=paths[j],w=weights[j],sg=p.x[0].cmp(a),onFirst=sg*d>=0;
   const alpha=onFirst?inverse(p,firstH,a.m(-d)):Z,beta=inverse(p,secondH,secondTarget);
   if(beta.cmp(T)<0||beta.cmp(T.a(2))>0)throw Error("second capture outside endpoint leg");
   if(onFirst){captured+=w;first=first.a(alpha.m(w));}
   const actual=onFirst?alpha:beta;raw=raw.a(actual.m(w));rawTimes.push(actual);
   items.push({time:beta,mass:w,index:j,onFirst,alpha});
  }
  const remaining=W-captured;let left=remaining,tail=Z,theta=T.a(2);
  items.sort((x,y)=>y.time.cmp(x.time));
  for(const it of items){
   if(left===0n)break;const take=left<it.mass?left:it.mass;
   tail=tail.a(it.time.m(take));left-=take;theta=it.time;
  }
  if(left!==0n)throw Error("incomplete rank tail");
  const cost=first.a(tail).dby(W),rawCost=raw.dby(W),ceiling=first.a(T.a(2).m(remaining)).dby(W);
  if(rawCost.cmp(cost)>0||cost.cmp(ceiling)>0)throw Error("M1 coupling inequalities failed");
  const result={start:a.str(),direction:d,route:path.map(p=>p.map(x=>x.str())),exact_cost:cost.str(),limit:cost.limit().str(),
   raw_cost:rawCost.str(),raw_limit:rawCost.limit().str(),captured_mass:Q(captured).dby(W).str(),
   first_moment:first.dby(W).str(),prefix_ceiling:ceiling.str(),prefix_ceiling_limit:ceiling.limit().str(),cutoff:theta.str()};
  if(components){
   const gradient=Array(paths.length),ceilingCoefficients=Array(paths.length);
   for(const it of items){
    const extra=it.time.cmp(theta)>0?it.time.s(theta):Z;
    gradient[it.index]=(it.onFirst?it.alpha:theta).a(extra).str();
    ceilingCoefficients[it.index]=(it.onFirst?it.alpha:T.a(2)).str();
   }
   result.component_raw_times=rawTimes.map(x=>x.str());result.supergradient=gradient;result.ceiling_coefficients=ceilingCoefficients;
  }
  return result;
 }
 function recordScore(prepared,a,d){
  if(!unitScorer)throw Error("no independent record scorer supplied");
  const r=unitScorer.score(prepared,route(a,d),{fullCost:true});
  if(!r.complete)throw Error("endpoint sweep failed to capture all ranks");return r;
 }
 function summarize(rows){
  if(!rows.length)throw Error("empty scan");let best=0,limitBest=0;
  for(let j=1;j<rows.length;j++){
   if(Q(rows[j].exact_cost).cmp(Q(rows[best].exact_cost))<0)best=j;
   if(Q(rows[j].limit).cmp(Q(rows[limitBest].limit))<0)limitBest=j;
  }
  return{best_index:best,minimum_germ:rows[best].exact_cost,minimum_limit:rows[limitBest].limit,best:rows[best],
   candidate_routes:rows.length,complete_family:"both endpoint-M1 orientations"};
 }
 function separate(prepared,options={}){
  const ss=starts(prepared),rows=[];for(const a of ss)for(const d of [-1,1])rows.push(score(prepared,a,d,options));
  return{initial_positions:ss.map(x=>x.str()),rows,...summarize(rows),arithmetic:G.stats()};
 }
 return{starts,route,inverse,score,recordScore,summarize,separate};
}
return{createM1Separator};
})();