'use strict';
// Exact ALL-warp certificate checker; game-value matching remains OPEN.
function verifyAllWarp(L,B,C,api){
 const check=(p,s)=>{if(!p)throw Error(s)};
 const S=BigInt(L.S),W=2n*BigInt(L.weight_total),den=BigInt(C.weight_denominator);
 check(C.S===L.S&&B.S===L.S&&B.monster_routes.length===16&&C.weight_numerators.length===16,"source mismatch");
 check(L.paths_h.length===169&&L.weights_h.length===169,"Princess support");
 check(L.weights_h.reduce((a,b)=>a+b,0)===L.weight_total,"Princess normalization");
 for(const p of L.paths_h){check(p[0][0]===0,"Princess start");for(let j=0;j<p.length;j++){
  check(Math.abs(p[j][1])<=L.S,"Princess arena");
  if(j){const dt=p[j][0]-p[j-1][0],dx=p[j][1]-p[j-1][1];check(dt>0&&Math.abs(dx)<=dt,"Princess speed");}
 }}
 const changes=new Map();let base=0n,sum=0n,used=0,contacts=0;
 function folded(z){
  const period=2n*S;let k=(z+S)/period;
  if(z+S<0n&&(z+S)%period!==0n)k--;
  const r=z-2n*k*S;check(r>=-S&&r<S,"bad folded coordinate");
  return {k,r};
 }
 for(let i=0;i<16;i++){
  const lam=BigInt(C.weight_numerators[i]);check(lam>=0n,"negative weight");sum+=lam;
  if(!lam)continue;used++;
  const path=B.monster_routes[i].vertices;check(path.length>1&&path[0][0]===0,"Monster start");
  let left=false,right=false;
  for(let j=0;j<path.length;j++){
   const [t,x]=path[j];check(Number.isSafeInteger(t)&&Number.isSafeInteger(x)&&Math.abs(x)<=L.S,"Monster geometry");
   left ||= x===-L.S;right ||=x===L.S;
   if(j){const dt=t-path[j-1][0],dx=x-path[j-1][1];check(dt>0&&Math.abs(dx)===dt,"Monster speed");}
  }
  check(left&&right,"Monster must sweep both endpoints");
  const events=api.routeEvents(L,path);check(events.length===338,"first contact count");contacts+=events.length;
  for(const [U,V,w] of events)for(const z of [U,V]){
   const {k,r}=folded(z),sgn=r>0n?1n:r<0n?-1n:0n,rad=r<0n?-r:r;
   base+=lam*w*(2n*k+sgn);
   if(rad>0n&&rad<S){const key=rad.toString();changes.set(key,(changes.get(key)||0n)-lam*w*sgn);}
  }
 }
 check(sum===den&&used===C.positive_route_count,"Monster normalization");
 const cuts=[...changes].map(([k,v])=>[BigInt(k),v]).sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:0);
 check(cuts.length===C.source_contact_thresholds,"threshold count");
 let current=base,max=base,where=0n;
 for(const [s,d] of cuts){current+=d;if(current>max){max=current;where=s;}}
 const D=2n*W*den;
 const [wantN,wantD]=C.exact_worst_step.split("/").map(BigInt);
 check(max*wantD===wantN*D&&where.toString()===C.worst_step_right_of,"exact ceiling");
 const [upperN,upperD]=C.known_full_game_upper.split("/").map(BigInt);
 check(max*upperD<upperN*D,"not below known upper");
 const other=api.exactStepEnvelope(L,B.monster_routes.map(x=>x.vertices),C.weight_numerators);
 check(max*other.den===other.maximum*D&&other.events===cuts.length,"independent envelope");
 check(S%16n===0n,"sixteen-bin division");const h=S/16n;
 for(let j=0;j<16;j++){
  const lo=BigInt(j)*h,hi=lo+h;let area=base*h;
  for(const [s,d] of cuts){if(s<=lo)area+=d*h;else if(s<hi)area+=d*(hi-s);}
  let direct=0n;
  for(let i=0;i<16;i++){
   const lam=BigInt(C.weight_numerators[i]);
   if(lam)direct+=lam*api.featuresInteger(L,B.monster_routes[i].vertices,16).sums[j];
  }
  check(area===direct,"ramp/step bin "+j);
 }
 return {status:"PASS",scope:"all strictly increasing continuous odd period-two common coordinate warps",
   positive_monster_routes:used,princess_paths:338,first_contacts:contacts,breakpoints:cuts.length,
   independently_checked_bin_integrals:16,ceiling:api.printRat(max,D),worst_interval_after:where.toString(),
   below_existing_unrestricted_upper:true,full_game_solved:false};
}
if(typeof module!=="undefined")module.exports=verifyAllWarp;
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const fs=require("fs"),path=require("path"),crypto=require("crypto");
 const root=path.resolve(__dirname,"../..");
 const read=p=>fs.readFileSync(path.join(root,p));
 const C=JSON.parse(read("packages/interval_global_closure/common_warp_lower_all.cert.json").toString());
 const princess=read(C.princess_file),routes=read(C.monster_routes_file);
 const sha=b=>crypto.createHash("sha1").update("blob "+b.length).update(Buffer.from([0])).update(b).digest("hex");
 if(sha(princess)!==C.princess_blob_sha||sha(routes)!==C.monster_routes_blob_sha)throw Error("pinned Git blobs changed");
 const helper=read("packages/interval_global_closure/common_warp_lower_bigint.cjs").toString();
 console.log(JSON.stringify(verifyAllWarp(JSON.parse(princess),JSON.parse(routes),
  C,(new Function(helper))()),null,2));
}
