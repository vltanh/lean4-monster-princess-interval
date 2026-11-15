// Exact BigInt certificate for the full common-warp family of a specified ordered Princess law.
// Every source Princess leg is unit/zero velocity and every supplied Monster leg is unit speed.
function gcd(a,b){while(b){let c=a%b;a=b;b=c;}return a<0n?-a:a;}
function bleft(xs,z){let l=0,r=xs.length;while(l<r){let m=(l+r)>>1;if(xs[m]<z)l=m+1;else r=m;}return l;}
function at(path,t){
 const k=Math.max(0,bleft(path.map(p=>p[0]),t+1)-1);
 if(k+1===path.length)return path[k][1];
 return path[k][1]+(path[k+1][1]-path[k][1])/(path[k+1][0]-path[k][0])*(t-path[k][0]);
}
function exactFirstHit(mon,prin){
 const ends=[...new Set(mon.map(p=>p[0]).concat(prin.map(p=>p[0])))].sort((a,b)=>a-b);
 for(let i=0;i<ends.length;i++){
   const t=ends[i];
   if(t>mon.at(-1)[0])break;
   const M=at(mon,t),P=at(prin,t),diff=M-P;
   if(diff===0)return {U:BigInt(t+M),V:BigInt(t-M),timeDen:1n,tNumer:BigInt(t)};
   if(i+1===ends.length)break;
   const e=ends[i+1];
   if(e>mon.at(-1)[0])continue;
   const eDiff=at(mon,e)-at(prin,e);
   if((diff>0&&eDiff<0)||(diff<0&&eDiff>0)){
     const ad=Math.abs(diff),bd=Math.abs(eDiff),den=BigInt(ad+bd);
     const tNumer=BigInt(t)*den+BigInt(e-t)*BigInt(ad);
     const twodelta=2n*(tNumer-BigInt(t)*den);
     if(twodelta%den!==0n)throw Error("noninteger capture characteristic");
     const shift=twodelta/den, Mu=BigInt(t+M),Mv=BigInt(t-M);
     const j=Math.max(0,bleft(mon.map(p=>p[0]),t+1)-1);
     if(j+1===mon.length)throw Error("nonunit final leg");
     const dt=mon[j+1][0]-mon[j][0],dx=mon[j+1][1]-mon[j][1];
     if(Math.abs(dx)!==dt)throw Error("not unit Monster leg");
     return dx>0?{U:Mu+shift,V:Mv,timeDen:den,tNumer}:{U:Mu,V:Mv+shift,timeDen:den,tNumer};
   }
 }
 throw Error("no first hit");
}
function qDiv(a,b){let q=a/b;if(a%b<0n)q-=1n;return q;}
function fold(z,S){
 const K=qDiv(z+S,2n*S);
 const r=z-2n*K*S;
 return {K,r,z:r<0n?-r:r,sign:r<0n?-1n:1n};
}
function basisScaled(z,j,S,h){
 const a=fold(z,S),lo=BigInt(j)*h;
 const ramp=a.z<=lo?0n:a.z>=lo+h?h:a.z-lo;
 return 2n*a.K*h+a.sign*ramp;
}
function signedPaths(L){
 const raw=[...L.paths_h].reverse().map(p=>p.map(([t,x])=>[t,-x])).concat(L.paths_h);
 const weights=L.weights_h.slice().reverse().concat(L.weights_h);
 return {raw,weights};
}
function routeEvents(L,route){
 const {raw,weights}=signedPaths(L);
 const out=[];
 for(let i=0;i<raw.length;i++){
   const c=exactFirstHit(route,raw[i]);
   out.push([c.U,c.V,BigInt(weights[i])]);
 }
 return out;
}
function featuresInteger(L,route,bins=16){
 if(L.S%bins!==0)throw Error("grid does not divide scale");
 const events=routeEvents(L,route);
 const S=BigInt(L.S),h=S/BigInt(bins),den=2n*BigInt(L.weight_total*2)*h;
 const sums=Array(bins).fill(0n);
 for(const [U,V,w] of events){
   for(let j=0;j<bins;j++)sums[j]+=w*(basisScaled(U,j,S,h)+basisScaled(V,j,S,h));
 }
 return {sums,den,events};
}
function printRat(p,q){
 if(q<0n){p=-p;q=-q;}
 const g=gcd(p,q);return (p/g).toString()+"/"+(q/g).toString();
}
function exactStepEnvelope(L,routes,numerators){
 const W=BigInt(L.weight_total)*2n, S=BigInt(L.S);
 let total=0n;
 const events=new Map();
 for(let i=0;i<routes.length;i++){
  const lam=BigInt(numerators[i]);
  if(lam===0n)continue;
  for(const [U,V,w] of routeEvents(L,routes[i])){
   for(const z of [U,V]){
    const {K,r,sign,z:absz}=fold(z,S);
    total+=lam*w*(2n*K+(absz>0n?sign:0n));
    if(absz>0n && absz<S){
      const key=absz.toString();
      events.set(key,(events.get(key)||0n)-lam*w*sign);
    }
   }
  }
 }
 let maximum=total,where="0+";
 for(const [key,delta] of [...events.entries()].sort((a,b)=>BigInt(a[0])<BigInt(b[0])?-1:1)){
   total+=delta;
   if(total>maximum){maximum=total;where=key;}
 }
 const den=2n*W*numerators.reduce((s,x)=>s+BigInt(x),0n);
 return {maximum,den,where,events:events.size,fraction:printRat(maximum,den),decimal:Number(maximum)/Number(den)};
}
return {featuresInteger,routeEvents,exactStepEnvelope,printRat};
