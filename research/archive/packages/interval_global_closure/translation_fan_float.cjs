/** Discovery-only double evaluation of fixed nonzero-width translation fans.
 * Endpoint flags and leg directions must come from the ACTUAL physical germ,
 * not from its collapsed coordinates.  Exact certification uses the germ
 * translation-fan scorer instead. */
module.exports=(function(){
function createFloatFanPath(vertices){
 const t=[],x=[];
 for(const [a,b]of vertices){
  if(!Number.isFinite(a)||!Number.isFinite(b)||a<0||b< -1-1e-12||b>1+1e-12)throw Error("invalid limiting path vertex");
  if(t.length&&a===t.at(-1)){if(Math.abs(b-x.at(-1))>1e-12)throw Error("noncontinuous collapsed path");continue;}
  if(t.length&&a<t.at(-1))throw Error("limiting path time order: "+JSON.stringify({previous:t.at(-1),current:a,vertices}));t.push(a);x.push(b);
 }
 if(!t.length||t[0]!==0)throw Error("path must start at0");
 const rate=t.slice(1).map((a,i)=>(x[i+1]-x[i])/(a-t[i])),atCache=new Map();
 function right(a,q){let l=0,r=a.length;while(l<r){const m=(l+r)>>1;if(a[m]<=q)l=m+1;else r=m;}return l-1;}
 function at(q){if(atCache.has(q))return atCache.get(q);const i=right(t,q),v=i+1===t.length?x[i]:x[i]+rate[i]*(q-t[i]);atCache.set(q,v);return v;}
 const tables=[0,1].map(h=>{
  const sign=2*h-1,seq=t.map((a,i)=>a-sign*x[i]),prefix=[0],inverseRate=[];
  for(let i=0;i+1<t.length;i++){
   let ds=seq[i+1]-seq[i];if(ds< -1e-11)throw Error("nonmonotone limiting characteristic");if(ds<0){seq[i+1]=seq[i];ds=0;}
   prefix.push(prefix.at(-1)+ds*(t[i]+t[i+1])/2);inverseRate.push(ds===0?null:(t[i+1]-t[i])/ds);
  }
  return{seq,prefix,inverseRate};
 });
 function primitive(h,q){
  const a=tables[h];if(q<=a.seq[0])return 0;const i=right(a.seq,q),dq=q-a.seq[i];
  if(i+1===t.length)return a.prefix[i]+t[i]*dq+dq*dq/2;
  if(a.inverseRate[i]===null)throw Error("flat inverse interval selected");
  return a.prefix[i]+t[i]*dq+dq*dq*a.inverseRate[i]/2;
 }
 function bandMoment(h,left,rightQ,end){
  if(rightQ<=left)return 0;const cap=end-(2*h-1)*at(end),cut=Math.min(rightQ,cap);
  let value=cut>left?primitive(h,cut)-primitive(h,left):0;
  if(rightQ>cap)value+=(rightQ-Math.max(left,cap))*end;
  if(value< -1e-9)throw Error("negative floating capture moment");return Math.max(0,value);
 }
 return{t,x,at,primitive,bandMoment};
}
function scoreFloatTranslationFan(path,monster,delta){
 if(!Number.isFinite(delta)||delta<=0)throw Error("finite positive fixed width required");
 const route=monster.route,flags=monster.endpoint_flags,directions=monster.directions;
 if(!flags||flags.length!==route.length||!directions||directions.length+1!==route.length)throw Error("actual endpoint flags and directions required");
 const clip=x=>Math.max(-delta,Math.min(delta,x));let total=0;
 for(const sign of [1,-1]){
  let L=clip(route[0][1]-sign*path.x[0]),H=L,moment=0;
  if(flags[0]===1)H=delta;if(flags[0]===-1)L=-delta;
  for(let k=0;k<directions.length;k++){
   if(L===-delta&&H===delta)break;
   const d=directions[k];if(d!==1&&d!==-1)throw Error("unit Monster required");
   const end=route[k+1][0],c=route[k][0]-d*route[k][1],r=route[k+1][1]-sign*path.at(end),h=(d*sign+1)>>1;
   let left,right;
   if(d===1){const next=flags[k+1]===1?delta:Math.max(H,clip(r));left=c+H;right=c+next;H=next;}
   else{const next=flags[k+1]===-1?-delta:Math.min(L,clip(r));left=c-L;right=c-next;L=next;}
   moment+=path.bandMoment(h,left,right,end);
  }
  if(L!==-delta||H!==delta)return Infinity;total+=moment/(2*delta);
 }
 return total/2;
}
function createFloatFanEvaluator(packet){
 const paths=packet.profiles.map(createFloatFanPath),rowToProfile=packet.rows.map(r=>r.profile);
 return{score:(row,monster,delta)=>scoreFloatTranslationFan(paths[rowToProfile[row]],typeof monster==="number"?packet.monsters[monster]:monster,delta),
  paths,rowToProfile,monsters:packet.monsters,rows:packet.rows};
}
return{createFloatFanPath,scoreFloatTranslationFan,createFloatFanEvaluator};
})();
