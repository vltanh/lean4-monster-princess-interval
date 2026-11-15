/** Exact uniform interval fans over a frozen physical Princess path.
 * A row chooses z uniformly in [lower,upper], clips p+z to [-1,1], then
 * reflects fairly. The path and interval are fixed, never query-dependent.
 * prepare(p,delta) retains the symmetric [-delta,delta] convenience API.
 */
module.exports=(function(){
function createTranslationFan(G){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,cache=new WeakMap(),stats={primitiveQueries:0,primitiveHits:0,bandQueries:0,bandHits:0,rows:0,scores:0};
 const min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b;
 function integralTable(p,h){
  let all=cache.get(p);if(!all){all=[null,null];cache.set(p,all);}if(all[h])return all[h];
  const seq=p.seq[h],prefix=[Z],inverseRate=[];
  for(let i=0;i+1<seq.length;i++){
   const ds=seq[i+1].s(seq[i]);if(ds.cmp(0)<0)throw Error("decreasing first-inverse characteristic");
   prefix.push(prefix.at(-1).a(ds.m(p.t[i].a(p.t[i+1])).dby(2)));
   inverseRate.push(ds.eq(0)?null:p.t[i+1].s(p.t[i]).dby(ds));
  }
  return all[h]={seq,prefix,inverseRate,primitive:new Map(),bands:new Map()};
 }
 function primitive(p,h,x){
  x=Q(x);const t=integralTable(p,h),key=x.str();stats.primitiveQueries++;
  if(t.primitive.has(key)){stats.primitiveHits++;return t.primitive.get(key);}
  const s=t.seq;let answer;
  if(x.cmp(s[0])<=0)answer=Z;
  else{
   let l=0,r=s.length;while(l<r){const m=(l+r)>>1;if(s[m].cmp(x)<=0)l=m+1;else r=m;}
   const i=l-1,dq=x.s(s[i]);
   if(i+1===s.length)answer=t.prefix[i].a(p.t[i].m(dq)).a(dq.m(dq).dby(2));
   else{
    const inv=t.inverseRate[i];if(inv===null)throw Error("flat inverse interval selected");
    answer=t.prefix[i].a(p.t[i].m(dq)).a(dq.m(dq).m(inv).dby(2));
   }
  }
  t.primitive.set(key,answer);return answer;
 }
 function bandMoment(p,h,left,right,end){
  left=Q(left);right=Q(right);end=Q(end);if(right.cmp(left)<0)throw Error("reversed inverse band");
  if(right.eq(left))return Z;
  const t=integralTable(p,h),key=[left,right,end].map(x=>x.str()).join("|");stats.bandQueries++;
  if(t.bands.has(key)){stats.bandHits++;return t.bands.get(key);}
  const cap=end.s(p.at(end).m(2*h-1)),cut=min(right,cap);let result=Z;
  if(cut.cmp(left)>0)result=primitive(p,h,cut).s(primitive(p,h,left));
  if(right.cmp(cap)>0)result=result.a(right.s(max(left,cap)).m(end));
  if(result.cmp(0)<0)throw Error("negative capture moment");t.bands.set(key,result);return result;
 }
 function prepareInterval(raw,lower,upper,{id=null,provenance=null}={}){
  const p=raw&&raw.seq&&raw.t?raw:new G.PLPath(raw),lo=Q(lower),hi=Q(upper),width=hi.s(lo);
  if(width.cmp(0)<=0)throw Error("translation interval must have strictly positive length");
  stats.rows++;return{path:p,lower:lo,upper:hi,width,delta:lo.eq(hi.neg())?hi:null,id,provenance,
   definition:"z uniform[lower,upper]; clamp(p(t)+z,-1,1); fair reflection; path and interval immutable"};
 }
 function prepare(raw,delta,options={}){const d=Q(delta);return prepareInterval(raw,d.neg(),d,options);}
 function marginal(row,time,position){
  const t=Q(time),x=Q(position),p=row.path.at(t),clip01=z=>max(Z,min(O,z));
  if(x.cmp(-1)<0)return{strict:Z,closed:Z};
  if(x.cmp(1)>0)return{strict:O,closed:O};
  const interior=clip01(x.s(p).s(row.lower).dby(row.width)).a(clip01(x.a(p).a(row.upper).dby(row.width))).dby(2);
  return{strict:x.eq(-1)?Z:interior,closed:x.eq(1)?O:interior};
 }
 function orientation(row,m,sign,{trace=false}={}){
  const p=row.path,low=sign===1?row.lower:row.upper.neg(),high=sign===1?row.upper:row.lower.neg(),clip=x=>max(low,min(high,x)),
   z0=m.x[0].s(p.x[0].m(sign));let L=clip(z0),H=L,moment=Z;
  if(m.x[0].eq(1))H=high;if(m.x[0].eq(-1))L=low;
  const initialMass=H.s(L).dby(row.width),records=[];
  for(let k=0;k<m.v.length;k++){
   if(L.eq(low)&&H.eq(high))break;
   const d=m.v[k].eq(1)?1:m.v[k].eq(-1)?-1:0;if(!d)throw Error("translation-fan scorer requires unit Monster legs");
   const end=m.t[k+1],c=m.t[k].s(m.x[k].m(d)),relative=m.x[k+1].s(p.at(end).m(sign)),h=(d*sign+1)>>1;
   let left,right,added;
   if(d===1){
    const next=m.x[k+1].eq(1)?high:max(H,clip(relative));added=next.s(H);left=c.a(H);right=c.a(next);H=next;
   }else{
    const next=m.x[k+1].eq(-1)?low:min(L,clip(relative));added=L.s(next);left=c.s(L);right=c.s(next);L=next;
   }
   if(added.cmp(0)<0)throw Error("captured translation interval shrank");
   if(added.eq(0))continue;
   const part=bandMoment(p,h,left,right,end);moment=moment.a(part);
   if(trace)records.push({leg:k,direction:d,mass:added.dby(row.width).str(),inverse_band:[left.str(),right.str()],end:end.str(),moment:part.str()});
  }
  return{complete:L.eq(low)&&H.eq(high),moment,cost:moment.dby(row.width),lower:L,upper:H,
   initial_mass:initialMass.str(),captured_mass:H.s(L).dby(row.width).str(),records};
 }
 function score(row,raw,{trace=false}={}){
  stats.scores++;const m=raw?.path?.v?raw.path:raw?.v?raw:new G.PLPath(raw?.route||raw),a=orientation(row,m,1,{trace}),b=orientation(row,m,-1,{trace}),
   value=a.cost.a(b.cost).dby(2),complete=a.complete&&b.complete;
  return{complete,exact_cost:value.str(),limit:complete?value.limit().str():null,decimal:complete?value.limit().num():null,
   delta:row.delta?.str()??null,interval:[row.lower.str(),row.upper.str()],width:row.width.str(),row_id:row.id,orientations:[a,b].map((r,i)=>({sign:i===0?1:-1,complete:r.complete,cost:r.cost.str(),
    initial_mass:r.initial_mass,captured_mass:r.captured_mass,lower:r.lower.str(),upper:r.upper.str(),records:r.records}))};
 }
 return{prepare,prepareInterval,score,orientation,primitive,bandMoment,marginal,stats:()=>({...stats})};
}
return{createTranslationFan};
})();
