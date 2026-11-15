'use strict';
// Independent exact-contact and step-envelope verification for the all-warp
// 64th-grid certificate. This is a *restricted-family* result, NOT a game saddle.
function buildTightWarpRoutes(L,B,C){
 const S=L.S,routes=B.monster_routes.map(r=>r.vertices);
 if(C.extra_routes.start_grid_denominator!==64||C.extra_routes.start_grid_numerators_from!==32||
   C.extra_routes.start_grid_numerators_to!==64)throw Error('unexpected sweep definition');
 routes.push([[0,-S],[2*S,S],[4*S,-S]]);
 for(let k=32;k<=64;k++){
  const x=k*S/64;
  routes.push(x===S?[[0,S],[2*S,-S]]:[[0,x],[S-x,S],[3*S-x,-S]]);
 }
 return routes;
}
function verifyTightWarp(L,B,C,api){
 const assert=(p,s)=>{if(!p)throw Error(s);};
 const S=BigInt(L.S),W=BigInt(L.weight_total)*2n,den=BigInt(C.weights_denominator);
 const routes=buildTightWarpRoutes(L,B,C),nums=C.weight_numerators.map(BigInt);
 assert(L.S===C.scale&&L.S===B.S&&routes.length===50&&nums.length===50,'source/route dimensions');
 assert(L.paths_h.length===169&&L.weights_h.length===169&&L.weights_h.reduce((a,b)=>a+b,0)===L.weight_total,'source Princess law');
 for(const p of L.paths_h){
  assert(p[0][0]===0,'Princess initial time');
  for(let j=0;j<p.length;j++){
   const [t,x]=p[j];assert(Number.isSafeInteger(t)&&Number.isSafeInteger(x)&&Math.abs(x)<=L.S,'Princess arena');
   if(j){const [a,y]=p[j-1],dt=t-a,dx=x-y;assert(dt>0&&Math.abs(dx)<=dt&&(dx===0||Math.abs(dx)===dt),'Princess velocity');}
  }
 }
 const source=L.paths_h.slice().reverse().map(p=>p.map(([t,x])=>[t,-x])).concat(L.paths_h);
 const sw=L.weights_h.slice().reverse().concat(L.weights_h);
 function bleft(a,z){let l=0,r=a.length;while(l<r){let m=(l+r)>>1;if(a[m]<z)l=m+1;else r=m;}return l;}
 function bright(a,z){let l=0,r=a.length;while(l<r){let m=(l+r)>>1;if(a[m]<=z)l=m+1;else r=m;}return l;}
 const P=source.map(path=>{
  const ts=path.map(v=>v[0]),xs=path.map(v=>v[1]),plus=path.map(([t,x])=>t-x),minus=path.map(([t,x])=>t+x);
  const slopes=[];
  for(let j=0;j<ts.length-1;j++)slopes.push((xs[j+1]-xs[j])/(ts[j+1]-ts[j]));
  return {ts,xs,plus,minus,slopes,
   at(t){const j=Math.max(0,bright(ts,t)-1);return j===ts.length-1?xs[j]:xs[j]+slopes[j]*(t-ts[j]);},
   arrival(t,x,d){
    const q=t-d*x,seq=d===1?plus:minus,k=bleft(seq,q);
    if(k===seq.length)return 2*(ts[ts.length-1]+q-seq[seq.length-1]);
    if(k===0)return 2*t;
    const slope=slopes[k-1],speed=1-d*slope,numer=2*(q-seq[k-1]);
    assert(speed>0&&numer%speed===0,'noninteger doubled arrival');
    return 2*ts[k-1]+numer/speed;
   }
  };
 });
 function firstContact(mon,p){
  for(let j=1;j<mon.length;j++){
   const [a,x]=mon[j-1],[b,y]=mon[j],d=(y-x)/(b-a);
   assert(d===1||d===-1,'not a unit segment');
   const target=p.at(a),diff=target-x;
   if(diff===0)return [BigInt(a+x),BigInt(a-x)];
   if(diff*d<=0)continue; // A 1-Lipschitz target behind the ray cannot overtake it.
   const tw=p.arrival(a,x,d);
   if(tw<=2*b){
    assert(tw>=2*a,'arrival before segment start');
    const q=BigInt(a-d*x),T2=BigInt(tw);
    return d===1?[T2-q,q]:[q,T2-q];
   }
  }
  throw Error('uncaptured source path');
 }
 function fold(z){
  const period=2n*S;let k=(z+S)/period;if(z+S<0n&&(z+S)%period!==0n)k--;
  const r=z-2n*k*S;assert(r>=-S&&r<S,'fold error');return [k,r];
 }
 let sum=0n,base=0n,positive=0,contacts=0;
 const diffs=new Map();
 for(let i=0;i<routes.length;i++){
  const lam=nums[i];assert(lam>=0n,'negative route weight');sum+=lam;
  if(!lam)continue;positive++;
  const route=routes[i];assert(route.length>=2&&route[0][0]===0,'Monster start');
  let left=false,right=false;
  for(let j=0;j<route.length;j++){
   const [t,x]=route[j];assert(Number.isSafeInteger(t)&&Number.isSafeInteger(x)&&Math.abs(x)<=L.S,'Monster arena');
   left ||= x===-L.S;right ||= x===L.S;
   if(j){const [a,y]=route[j-1],dt=t-a,dx=x-y;assert(dt>0&&Math.abs(dx)===dt,'Monster speed');}
  }
  assert(left&&right,'route is not endpoint complete');
  const ext=api.routeEvents(L,route);assert(ext.length===P.length,'old contact evaluator count');
  for(let j=0;j<P.length;j++){
   const [U,V]=firstContact(route,P[j]);contacts++;
   assert(U===ext[j][0]&&V===ext[j][1]&&ext[j][2]===BigInt(sw[j]),'independent chronological first hit mismatch');
   for(const z of [U,V]){
    let [k,r]=fold(z),sgn=r>0n?1n:r<0n?-1n:0n,rad=r<0n?-r:r;
    base+=lam*BigInt(sw[j])*(2n*k+sgn);
    if(rad>0n&&rad<S){const key=rad.toString();diffs.set(key,(diffs.get(key)||0n)-lam*BigInt(sw[j])*sgn);}
   }
  }
 }
 assert(sum===den&&positive===C.nonzero_monster_routes&&contacts===C.source_contacts,'mixture normalization/contacts');
 const cuts=[...diffs].map(([key,d])=>[BigInt(key),d]).sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:0);
 assert(cuts.length===C.step_breakpoints,'exact breakpoint census');
 let cur=base,mx=base,where='0+';
 for(const [r,d] of cuts){cur+=d;if(cur>mx){mx=cur;where=r.toString();}}
 const totalDen=2n*W*den;
 assert(api.printRat(mx,totalDen)===C.exact_ceiling&&where===C.worst_step_right_of_scaled,'exact ceiling or witness');
 const same=api.exactStepEnvelope(L,routes,C.weight_numerators);
 assert(same.maximum*totalDen===mx*same.den&&same.events===cuts.length,'independent complete envelope');
 const [loN,loD]=C.original_lower.split('/').map(BigInt);
 const [oldN,oldD]=C.earlier_all_warp_ceiling.split('/').map(BigInt);
 assert(mx*oldD<oldN*totalDen,'ceiling not improved');
 assert(mx*loD>loN*totalDen,'below old certified response would be impossible');
 assert(api.printRat(mx*loD-loN*totalDen,totalDen*loD)===C.exact_ceiling_minus_original,'wrong old baseline gap');
 for(const n of [16,64]){
  assert(S%BigInt(n)===0n,'bin size');const h=S/BigInt(n);
  const coefficients=Array(n).fill(0n);
  for(let i=0;i<routes.length;i++)if(nums[i]){
   const f=api.featuresInteger(L,routes[i],n);
   for(let j=0;j<n;j++)coefficients[j]+=nums[i]*f.sums[j];
  }
  for(let j=0;j<n;j++){
   const a=BigInt(j)*h,b=a+h;let integral=base*h;
   for(const [s,d]of cuts){if(s<=a)integral+=d*h;else if(s<b)integral+=d*(b-s);}
   assert(integral===coefficients[j],'independent exact integral of step/ramp bin '+n+':'+j);
  }
 }
 return {status:'PASS',scope:'all continuous strictly increasing common light-coordinate warps of one archived Princess law',
   positive_monster_routes:positive,first_hit_checks:contacts,independent_hit_checks:contacts,
   discontinuity_thresholds:cuts.length,independent_step_ramp_integrals:16+64,
   exact_ceiling:api.printRat(mx,totalDen),worst_open_cell_starts_after_scaled:where,
   narrower_than_prior_all_warp:true,full_game_solved:false};
}
if(typeof module!=='undefined')module.exports={buildTightWarpRoutes,verifyTightWarp};
if(typeof require!=='undefined'&&typeof module!=='undefined'&&require.main===module){
 const fs=require('fs'),path=require('path'),crypto=require('crypto');
 const root=path.resolve(__dirname,'../..'),read=p=>fs.readFileSync(path.join(root,p));
 const C=JSON.parse(read('packages/interval_global_closure/common_warp_lower_all_tight.cert.json').toString());
 const pb=read(C.princess_file),rb=read(C.legacy_route_file);
 const sha=b=>crypto.createHash('sha1').update('blob '+b.length).update(Buffer.from([0])).update(b).digest('hex');
 if(sha(pb)!==C.princess_blob_sha||sha(rb)!==C.legacy_route_blob_sha)throw Error('source Git blob mismatch');
 const api=(new Function(read('packages/interval_global_closure/common_warp_lower_bigint.cjs').toString()))();
 console.log(JSON.stringify(verifyTightWarp(JSON.parse(pb),JSON.parse(rb),C,api),null,2));
}
