/** Exact dyadic enclosures of fixed history-selector fan upper planes.
 * Selector validity, rather than stationarity of a numerical gradient, proves
 * each plane. All original profile vertices are exact rational source data.
 */
module.exports=(function(){
const abs=x=>x<0n?-x:x,min=(a,b)=>a<b?a:b,max=(a,b)=>a>b?a:b;
const floorDiv=(a,b)=>{if(b<=0n)throw Error("positive divisor");return a>=0n?a/b:-((-a+b-1n)/b);};
const ceilDiv=(a,b)=>-floorDiv(-a,b);
function rational(s){const a=String(s).split("/");return{n:BigInt(a[0]),d:BigInt(a[1]??1)};}
function nearest(q,S){return q.n<0n?-nearest({n:-q.n,d:q.d},S):(2n*q.n*S+q.d)/(2n*q.d);}
function createSelectorVerifier({scalePower=44,widthDenominator=1024}={}){
 const S=1n<<BigInt(scalePower),W=S/BigInt(widthDenominator);if(W*BigInt(widthDenominator)!==S)throw Error("dyadic width");
 function profile(vertices){
  const raw=vertices.map(([t,x])=>[rational(t),rational(x)]),t=[],x=[];let dropped=0;
  if(raw[0][0].n!==0n)throw Error("profile time0");
  for(let j=0;j<raw.length;j++){
   const[a,b]=raw[j];if(a.d<=0n||b.d<=0n||a.n<0n||b.n<0n||b.n>b.d)throw Error("profile domain");
   if(j){const[c,d]=raw[j-1],dt=a.n*c.d-c.n*a.d,dx=abs(b.n*d.d-d.n*b.d);if(dt<0n||dx*a.d*c.d>dt*b.d*d.d)throw Error("nonlegal profile");}
   const u=nearest(a,S),v=nearest(b,S);
   if(t.length&&u===t.at(-1)){x[x.length-1]=v;dropped++;}
   else{t.push(u);x.push(v);}
  }
  // Verify the uniform enclosure at every breakpoint of either polyline.
  // Their difference is affine between those breakpoints, so this is global.
  let j=0,checks=0;
  for(const[a,b]of raw){
   while(j+1<t.length&&t[j+1]*a.d<=a.n*S)j++;
   let numerator,denominator;
   if(j+1===t.length){numerator=x[j];denominator=1n;}
   else{const dt=t[j+1]-t[j];numerator=x[j]*dt*a.d+(x[j+1]-x[j])*(a.n*S-t[j]*a.d);denominator=dt*a.d;}
   if(abs(numerator*b.d-b.n*S*denominator)>4n*denominator*b.d)throw Error("source-node approximation enclosure");
   checks++;
  }
  let k=0;
  for(let j=0;j<t.length;j++){
   const u=t[j];while(k+1<raw.length&&raw[k+1][0].n*S<=u*raw[k+1][0].d)k++;
   let numerator,denominator;
   if(k+1===raw.length){const q=raw[k][1];numerator=q.n*S;denominator=q.d;}
   else{const[ta,xa]=raw[k],[tb,xb]=raw[k+1],dt=tb.n*ta.d-ta.n*tb.d,off=u*ta.d-ta.n*S,dx=xb.n*xa.d-xa.n*xb.d;
    if(dt<=0n)throw Error("unresolved equal-time source nodes");
    numerator=xa.n*S*xb.d*dt+dx*off*tb.d;denominator=xb.d*xa.d*dt;}
   if(abs(numerator-x[j]*denominator)>4n*denominator)throw Error("rounded-node approximation enclosure");
   checks++;
  }
  return{t,x,source_vertices:raw.length,dropped,enclosure_checks:checks};
 }
 const right=(a,u)=>{let l=0,r=a.length;while(l<r){const j=(l+r)>>1;if(a[j]<=u)l=j+1;else r=j;}return l-1;};
 function position(p,u){
  const j=right(p.t,u);if(j<0)throw Error("negative evaluation time");
  if(j+1===p.t.length)return{lo:p.x[j],hi:p.x[j]};
  const den=p.t[j+1]-p.t[j],num=p.x[j]*den+(p.x[j+1]-p.x[j])*(u-p.t[j]);
  return{lo:floorDiv(num,den),hi:ceilDiv(num,den)};
 }
 const clamp=u=>max(0n,min(W,u));
 const capLo=u=>floorDiv(clamp(u)*S,W),capHi=u=>ceilDiv(clamp(u)*S,W);
 function feature(p,t,x){
  const z=position(p,t),r=abs(x),rlo=capLo(r-z.hi)+capLo(z.lo+W-2n*S+r),rhi=capHi(r-z.lo)+capHi(z.hi+W-2n*S+r);
  return x>=0n?{lo:floorDiv(S+rlo,2n),hi:ceilDiv(S+rhi,2n)}:{lo:floorDiv(S-rhi,2n),hi:ceilDiv(S-rlo,2n)};
 }
 function clipArea(u,v,dt){
  if(u>v){const z=u;u=v;v=z;}let numerator,denominator;
  if(u===v){numerator=dt*clamp(u);denominator=W;}
  else{const phi=z=>z<=0n?0n:z<W?z*z:2n*W*z-W*W;numerator=dt*(phi(v)-phi(u));denominator=2n*W*(v-u);}
  return{lo:floorDiv(numerator,denominator),hi:ceilDiv(numerator,denominator)};
 }
 function integral(p,a,d,l,r,stats){
  if(l===r)return{lo:0n,hi:0n};if(l>r)throw Error("integral order");
  const ts=[l,r],zero=a[0]-BigInt(d)*a[1];if(zero>l&&zero<r)ts.push(zero);
  for(let j=Math.max(0,right(p.t,l)+1);j<p.t.length&&p.t[j]<r;j++)ts.push(p.t[j]);
  ts.sort((a,b)=>a<b?-1:a>b?1:0);let lo=0n,hi=0n;
  for(let j=0;j+1<ts.length;j++){const u=ts[j],v=ts[j+1],dt=v-u;if(dt===0n)continue;
   const pu=position(p,u),pv=position(p,v),xu=a[1]+BigInt(d)*(u-a[0]),xv=a[1]+BigInt(d)*(v-a[0]),ru=abs(xu),rv=abs(xv),positive=xu+xv>=0n;
   const A=clipArea(ru-pu.hi,rv-pv.hi,dt),B=clipArea(ru-pu.lo,rv-pv.lo,dt),
    C=clipArea(pu.lo+W-2n*S+ru,pv.lo+W-2n*S+rv,dt),D=clipArea(pu.hi+W-2n*S+ru,pv.hi+W-2n*S+rv,dt);
   if(positive){lo+=floorDiv(dt+A.lo+C.lo,2n);hi+=ceilDiv(dt+B.hi+D.hi,2n);}
   else{lo+=floorDiv(dt-B.hi-D.hi,2n);hi+=ceilDiv(dt-A.lo-C.lo,2n);}
   if(stats)stats.integral_cells=(stats.integral_cells??0)+1;
  }
  return{lo,hi};
 }
 function ordinaryRoute(route){
  const vertices=[];let t=0n,previous=null;
  for(const pair of route){const x=max(-S,min(S,BigInt(Math.round(pair[1]*Number(S)))));if(previous!==null)t+=abs(x-previous);vertices.push([t,x]);previous=x;}
  return vertices;
 }
 function freezePlane(monster,entry){
  const route=ordinaryRoute(monster.route),selectors=entry.selectors.map(s=>{
   const a=route[s.leg],b=route[s.leg+1],offset=BigInt(Math.round((s.activation-monster.route[s.leg][0])*Number(S))),cut=max(a[0],min(b[0],a[0]+offset));
   return{leg:s.leg,cut:cut.toString(),lower_index:s.lower_index,upper_index:s.upper_index};
  });
  return{monster:entry.monster,route:route.map(p=>p.map(String)),selectors};
 }
 function upperCoefficient(p,frozen,stats){
  const route=frozen.route.map(pair=>pair.map(BigInt)),selectors=new Map(frozen.selectors.map(s=>[s.leg,s])),seenMinus=route.some(v=>v[1]===-S),seenPlus=route.some(v=>v[1]===S);
  if(route[0][0]!==0n||!seenMinus||!seenPlus||route.some(v=>v[1]<-S||v[1]>S))throw Error("incomplete or nonphysical route");
  let result=0n;
  for(let k=0;k+1<route.length;k++){
   const a=route[k],b=route[k+1],duration=b[0]-a[0];if(duration<0n||abs(b[1]-a[1])!==duration)throw Error("nonunit physical leg");
   if(duration===0n)continue;const d=b[1]>a[1]?1:-1,s=selectors.get(k);if(!s)throw Error("missing selector");
   if(s.lower_index<0||s.upper_index<0||s.lower_index>k||s.upper_index>k)throw Error("selector looks into future");
   const cut=BigInt(s.cut);if(cut<a[0]||cut>b[0])throw Error("illegal selector cut");
   const lv=feature(p,...route[s.lower_index]),hv=feature(p,...route[s.upper_index]),before=cut-a[0],I=integral(p,a,d,cut,b[0],stats);
   result+=d===1?ceilDiv(duration*(S+lv.hi),S)-floorDiv(before*hv.lo,S)-I.lo
    :ceilDiv(duration*(S-hv.lo),S)+ceilDiv(before*lv.hi,S)+I.hi;
  }
  // The original exact profile and rounded interpolant differ uniformly by
  // at most4/S. Each signed folded CDF differs by at most4/(S*delta).
  // A selector integrand contains two such CDF evaluations.
  const T=route.at(-1)[0],perturbation=ceilDiv(8n*T*S,S*W);
  return{upper:result+perturbation,rounded_upper:result,perturbation};
 }
 function certify(packet,discovery,{weightScalePower=36}={}){
  const profiles=packet.profile_exact_vertices.map(profile),ws=1n<<BigInt(weightScalePower),planes=discovery.map(e=>({...freezePlane(packet.monsters[e.monster],e),weight:BigInt(Math.round(e.weight*Number(ws))).toString()})).filter(p=>BigInt(p.weight)>0n),
   total=planes.reduce((s,p)=>s+BigInt(p.weight),0n),stats={profiles:profiles.length,planes:planes.length,source_vertices:profiles.reduce((s,p)=>s+p.source_vertices,0),rounded_vertices:profiles.reduce((s,p)=>s+p.t.length,0),coalesced_vertices:profiles.reduce((s,p)=>s+p.dropped,0),uniform_profile_enclosure_checks:profiles.reduce((s,p)=>s+p.enclosure_checks,0),integral_cells:0,coefficients:0},rows=[];
  if(total<=0n)throw Error("empty law");let maximum=-1n,maxIndex=-1;
  for(let i=0;i<profiles.length;i++){let weighted=0n;const coefficients=[];
   for(const p of planes){const c=upperCoefficient(profiles[i],p,stats);coefficients.push(c.upper.toString());weighted+=BigInt(p.weight)*c.upper;stats.coefficients++;}
   rows.push({profile:i,weighted_upper_numerator:weighted.toString(),coefficients});if(weighted>maximum){maximum=weighted;maxIndex=i;}
  }
  const denominator=total*S;
  return{scope:"Exact finite reflected-fan basis exclusion by arbitrary history selectors; not a game upper bound.",
   scale:S.toString(),scale_power:scalePower,width:"1/"+widthDenominator,weight_total:total.toString(),planes,rows,stats,
   upper_numerator:maximum.toString(),upper_denominator:denominator.toString(),maximizing_profile:maxIndex,
   upper_decimal:Number(maximum)/Number(denominator),
   certified_lower_bound:"36290299773897097/25600000000000000",
   strictly_below_certified_game_lower:maximum*25600000000000000n<36290299773897097n*denominator};
 }
 function replay(packet,certificate){
  if(certificate.scale!==S.toString()||certificate.width!=="1/"+widthDenominator)throw Error("certificate scale/width mismatch");
  const profiles=packet.profile_exact_vertices.map(profile),planes=certificate.planes,total=planes.reduce((s,p)=>{
   const w=BigInt(p.weight);if(w<=0n)throw Error("nonpositive plane weight");return s+w;},0n);
  if(total.toString()!==certificate.weight_total||certificate.rows.length!==profiles.length)throw Error("certificate dimensions");
  const stats={profiles:profiles.length,planes:planes.length,source_vertices:profiles.reduce((s,p)=>s+p.source_vertices,0),
   rounded_vertices:profiles.reduce((s,p)=>s+p.t.length,0),coalesced_vertices:profiles.reduce((s,p)=>s+p.dropped,0),
   uniform_profile_enclosure_checks:profiles.reduce((s,p)=>s+p.enclosure_checks,0),integral_cells:0,coefficients:0};
  let maximum=-1n,maxIndex=-1;
  for(let i=0;i<profiles.length;i++){
   const row=certificate.rows[i];if(row.profile!==i||row.coefficients.length!==planes.length)throw Error("coefficient dimensions");
   let weighted=0n;
   for(let j=0;j<planes.length;j++){const c=upperCoefficient(profiles[i],planes[j],stats);
    if(c.upper.toString()!==row.coefficients[j])throw Error("coefficient replay mismatch");weighted+=BigInt(planes[j].weight)*c.upper;stats.coefficients++;}
   if(weighted.toString()!==row.weighted_upper_numerator)throw Error("weighted row replay mismatch");
   if(weighted>maximum){maximum=weighted;maxIndex=i;}
  }
  const denominator=total*S;
  if(maximum.toString()!==certificate.upper_numerator||denominator.toString()!==certificate.upper_denominator||
   maxIndex!==certificate.maximizing_profile||JSON.stringify(stats)!==JSON.stringify(certificate.stats))throw Error("aggregate replay mismatch");
  if(!(maximum*25600000000000000n<36290299773897097n*denominator))throw Error("exclusion gap not established");
  return{scope:certificate.scope,complete:true,stats,upper_numerator:maximum.toString(),upper_denominator:denominator.toString(),
   upper_decimal:Number(maximum)/Number(denominator),maximizing_profile:maxIndex,strictly_below_certified_game_lower:true,
   no_numerical_solver_assumption:true,profile_error_bound:"4/"+S,selector_plane_error_bound:"8*T/(S*delta)"};
 }
 return{profile,position,feature,clipArea,integral,ordinaryRoute,freezePlane,upperCoefficient,certify,replay,S,W};
}
return{createSelectorVerifier};
})();