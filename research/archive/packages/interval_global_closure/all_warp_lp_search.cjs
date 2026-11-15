'use strict';
// Discovery-only double oracle for *all* monotone common-coordinate warps.
// Every exported route is physical; finalize with verify_lower_warp_all.cjs.
function makeAllWarpGame(L,api,routes){
 const S=BigInt(L.S),W=2n*BigInt(L.weight_total),cuts=new Set(['0']),data=[];
 function fold(z){let k=(z+S)/(2n*S);if(z+S<0n&&(z+S)%(2n*S)!==0n)k--;return [k,z-2n*k*S];}
 for(const route of routes){
  let init=0n,delta=new Map();
  for(const [U,V,w] of api.routeEvents(L,route))for(const z of [U,V]){
   let [k,r]=fold(z),sgn=r>0n?1n:r<0n?-1n:0n,rad=r<0n?-r:r;
   init+=w*(2n*k+sgn);
   if(rad>0n&&rad<S){const key=rad.toString();cuts.add(key);delta.set(key,(delta.get(key)||0n)-w*sgn);}
  }
  data.push({init,delta});
 }
 const xs=[...cuts].map(BigInt).sort((a,b)=>a<b?-1:a>b?1:0);
 const A=data.map(d=>{let cur=d.init;return xs.map((x,j)=>{if(j)cur+=d.delta.get(x.toString())||0n;return Number(cur)/Number(2n*W);});});
 return {xs:xs.map(Number),A,rows:routes.length,columns:xs.length};
}
class WarpSimplex{
 constructor(A,b,c){
  this.m=b.length;this.n=c.length;
  let m=this.m,n=this.n;this.D=Array.from({length:m+2},()=>Array(n+2).fill(0));this.B=Array(m);this.N=Array(n+1);
  for(let i=0;i<m;i++){for(let j=0;j<n;j++)this.D[i][j]=A[i][j];this.B[i]=n+i;this.D[i][n]=-1;this.D[i][n+1]=b[i];}
  for(let j=0;j<n;j++){this.N[j]=j;this.D[m][j]=-c[j];}this.N[n]=-1;this.D[m+1][n]=1;
 }
 pivot(r,s){
  const m=this.m,n=this.n,D=this.D,inv=1/D[r][s];
  for(let i=0;i<m+2;i++)if(i!==r)for(let j=0;j<n+2;j++)if(j!==s)D[i][j]-=D[r][j]*D[i][s]*inv;
  for(let j=0;j<n+2;j++)if(j!==s)D[r][j]*=inv;
  for(let i=0;i<m+2;i++)if(i!==r)D[i][s]*=-inv;
  D[r][s]=inv;[this.B[r],this.N[s]]=[this.N[s],this.B[r]];
 }
 simplex(phase){
  const m=this.m,n=this.n,D=this.D,B=this.B,N=this.N,x=phase===1?m+1:m;
  for(let it=0;it<150000;it++){
   let s=-1;
   for(let j=0;j<=n;j++){
    if(phase===2&&N[j]===-1)continue;
    if(s<0||D[x][j]<D[x][s]-1e-10||(Math.abs(D[x][j]-D[x][s])<=1e-10&&N[j]<N[s]))s=j;
   }
   if(D[x][s]>=-1e-10)return true;
   let r=-1;
   for(let i=0;i<m;i++)if(D[i][s]>1e-10&&(r<0||D[i][n+1]/D[i][s]<D[r][n+1]/D[r][s]-1e-10||(Math.abs(D[i][n+1]/D[i][s]-D[r][n+1]/D[r][s])<1e-10&&B[i]<B[r])))r=i;
   if(r<0)return false;this.pivot(r,s);
  }
  throw Error('simplex iteration cap');
 }
 solve(){
  let m=this.m,n=this.n,D=this.D,B=this.B,N=this.N,r=0;
  for(let i=1;i<m;i++)if(D[i][n+1]<D[r][n+1])r=i;
  if(D[r][n+1]<-1e-10){
   this.pivot(r,n);
   if(!this.simplex(1)||D[m+1][n+1]<-1e-10)throw Error('infeasible');
   if(D[m+1][n+1]>1e-10)throw Error('phase I mismatch');
   let rr=B.indexOf(-1);
   if(rr>=0){let s=0;for(let j=1;j<=n;j++)if(D[rr][j]<D[rr][s]-1e-10||(Math.abs(D[rr][j]-D[rr][s])<=1e-10&&N[j]<N[s]))s=j;this.pivot(rr,s);}
  }
  if(!this.simplex(2))throw Error('unbounded');
  let out=Array(n).fill(0);for(let i=0;i<m;i++)if(B[i]<n)out[B[i]]=D[i][n+1];
  return {v:D[m][n+1],x:out};
 }
}
function optimizeAllWarpBank(game){
 const A=game.A,m=A.length,J=game.xs.length;
 const dualC=Array(J).fill(0).concat(1),dualA=A.map(row=>row.map(x=>-x).concat(1)),dualB=Array(m).fill(0);
 dualA.push(Array(J).fill(1).concat(0));dualB.push(1);
 dualA.push(Array(J).fill(-1).concat(0));dualB.push(-1);
 const dual=new WarpSimplex(dualA,dualB,dualC).solve();
 const primalC=Array(m).fill(0).concat(-1),primalA=Array.from({length:J},(_,j)=>A.map(row=>row[j]).concat(-1)),primalB=Array(J).fill(0);
 primalA.push(Array(m).fill(1).concat(0));primalB.push(1);
 primalA.push(Array(m).fill(-1).concat(0));primalB.push(-1);
 const primal=new WarpSimplex(primalA,primalB,primalC).solve();
 const probs=primal.x.slice(0,m),sum=probs.reduce((a,b)=>a+b,0);
 if(probs.some(x=>!Number.isFinite(x)||x< -1e-8)||Math.abs(sum-1)>1e-7)
  throw Error('discovery LP numerical instability: infeasible Monster mixture');
 const q=dual.x.slice(0,J).map((w,j)=>({cut:game.xs[j],w})).filter(o=>o.w>1e-11);
 const ceiling=Math.max(...game.xs.map((x,j)=>probs.reduce((s,w,i)=>s+w*A[i][j],0)));
 if(!Number.isFinite(ceiling)||Math.abs(ceiling-dual.v)>1e-7)
  throw Error('discovery LP numerical instability: nonmatching primal/dual');
 return {ceiling,primal:-primal.v,dual:dual.v,weights:probs,q};
}
function warpedResponse(L,api,routes,dual,maxNodes=100000){
 const S=L.S,W=2*L.weight_total;
 const cuts=dual.map(x=>x.cut),cprob=[],prob=dual.map(x=>x.w);
 let acc=0;for(const w of prob){acc+=w;cprob.push(acc);}
 const bisectleft=(a,v)=>{let i=0,j=a.length;while(i<j){let k=(i+j)>>1;if(a[k]<v)i=k+1;else j=k;}return i;};
 const bisectright=(a,v)=>{let i=0,j=a.length;while(i<j){let k=(i+j)>>1;if(a[k]<=v)i=k+1;else j=k;}return i;};
 const g=z=>{let k=Math.floor((z+S)/(2*S)),r=z-2*k*S,rad=Math.abs(r);if(!rad)return 2*k;
  let j=bisectleft(cuts,rad);return 2*k+Math.sign(r)*(j?cprob[j-1]:0);};
 const timed=(t,x)=>(g(t+x)+g(t-x))/2;
 const source=L.paths_h.slice().reverse().map(p=>p.map(([t,x])=>[t,-x])).concat(L.paths_h);
 const weights=L.weights_h.slice().reverse().concat(L.weights_h);
 const P=source.map((p,i)=>{
  const t=p.map(a=>a[0]),x=p.map(a=>a[1]),s=[],plus=p.map(([t,x])=>t-x),minus=p.map(([t,x])=>t+x);
  for(let j=0;j<t.length-1;j++)s.push((x[j+1]-x[j])/(t[j+1]-t[j]));
  return {t,x,s,plus,minus,w:weights[i],
   at(T){let j=bisectright(t,T)-1;return j>=t.length-1?x[x.length-1]:x[j]+s[j]*(T-t[j]);},
   hit(T,X,d){let seq=d===1?plus:minus,Q=T-d*X,j=bisectleft(seq,Q);
    if(j===seq.length)return t[t.length-1]+Q-seq[seq.length-1];
    if(j===0)return T;
    let den=1-d*s[j-1],num=Q-seq[j-1];
    if(den<=0||num%den!==0)throw Error('non-integral pursuit at '+j+': '+den+', '+num);
    return t[j-1]+num/den;
   }};
 });
 let best=Infinity,bestRoute=routes[0],firstBest;
 for(const route of routes){
  let val=0;for(const [U,V,w] of api.routeEvents(L,route))val+=Number(w)*(g(Number(U))+g(Number(V)))/2;
  if(val<best){best=val;bestRoute=route;}
 }
 firstBest=best;
 const memo=new Map(),stats={nodes:0,leaves:0,dominated:0,bounded:0,initial_starts:0};
 let running=[];
 function walk(l,r,anchor,t,x,cost){
  if(++stats.nodes>maxNodes)return;
  while(l>0&&P[l-1].at(t)===x){l--;cost+=P[l].w*timed(t,x);}
  while(r+1<P.length&&P[r+1].at(t)===x){r++;cost+=P[r].w*timed(t,x);}
  if(l===0&&r===P.length-1){stats.leaves++;if(cost<best-1e-6){best=cost;bestRoute=running.map(a=>a.slice());}return;}
  const key=l+','+r+','+anchor,old=memo.get(key)||[];
  if(old.some(z=>z[0]<=t&&z[1]<=cost+1e-6)){stats.dominated++;return;}
  memo.set(key,old.filter(z=>!(t<=z[0]&&cost<=z[1]+1e-6)).concat([[t,cost]]));
  let lb=cost;
  for(let j=0;j<l;j++){let nt=P[j].hit(t,x,-1);lb+=P[j].w*timed(nt,x-(nt-t));}
  for(let j=r+1;j<P.length;j++){let nt=P[j].hit(t,x,1);lb+=P[j].w*timed(nt,x+(nt-t));}
  if(lb>=best-1e-6){stats.bounded++;return;}
  const choices=[];
  if(l>0)choices.push([P[l-1].hit(t,x,-1),l-1,-1]);
  if(r+1<P.length)choices.push([P[r+1].hit(t,x,1),r+1,1]);
  choices.sort((a,b)=>a[0]-b[0]||b[2]-a[2]);
  for(const [nt,j,d]of choices){
   let nx=x+d*(nt-t);if(nt<t||Math.abs(nx)>S)throw Error('illegal new capture');
   running.push([nt,nx]);walk(Math.min(l,j),Math.max(r,j),j,nt,nx,cost+P[j].w*timed(nt,nx));running.pop();
   if(stats.nodes>maxNodes)break;
  }
 }
 for(let i=0;i<P.length&&stats.nodes<=maxNodes;i++){
  if(P[i].x[0]<0||(i>0&&P[i].x[0]===P[i-1].x[0]))continue;
  stats.initial_starts++;running=[[0,P[i].x[0]]];walk(i,i,i,0,P[i].x[0],0);
 }
 // Retain all first-hit events and append an endpoint tour only after last capture.
 let route=bestRoute.map(x=>x.slice());
 let visitedL=route.some(p=>p[1]===-S),visitedR=route.some(p=>p[1]===S);
 if(!visitedL&&!visitedR){let [t,x]=route[route.length-1],end=x>=0?S:-S;route.push([t+Math.abs(end-x),end]);}
 if(!visitedL){let [t,x]=route[route.length-1];route.push([t+Math.abs(-S-x),-S]);}
 if(!visitedR){let [t,x]=route[route.length-1];route.push([t+Math.abs(S-x),S]);}
 // Delete all equal-slope intermediate vertices.
 let compressed=[];for(const v of route){
  compressed.push(v);while(compressed.length>=3){
   let k=compressed.length,a=compressed[k-3],b=compressed[k-2],c=compressed[k-1];
   if((b[1]-a[1])*(c[0]-b[0])!==(c[1]-b[1])*(b[0]-a[0]))break;
   compressed.splice(k-2,1);
  }
 }
 return {first: firstBest/W,best:best/W,gain:(firstBest-best)/W,route:compressed,stats};
}
return {makeAllWarpGame,optimizeAllWarpBank,warpedResponse};
