// Unrestricted capture-order response to a finite ordered symmetric Princess law.
// Numeric discovery counterpart of packages/interval_uniform_reduction/exact_response.py.
// Never treat floating results as exact proof certificates.
function bleft(arr,z){let a=0,b=arr.length;while(a<b){let m=(a+b)>>>1;if(arr[m]<z)a=m+1;else b=m;}return a;}
function build(half_paths,half_weights,S){
 const paths=half_paths.slice().reverse().map(p=>p.map(([t,x])=>[t,-x])).concat(half_paths);
 const weights=half_weights.slice().reverse().concat(half_weights);
 return paths.map((v,i)=>{
   const t=v.map(z=>z[0]),x=v.map(z=>z[1]),s=[];
   for(let j=1;j<v.length;j++)s.push((x[j]-x[j-1])/(t[j]-t[j-1]));
   const seq=[t.map((t,j)=>t+x[j]),t.map((t,j)=>t-x[j])];
   return {t,x,s,seq,w:weights[i],at(z){const k=Math.max(0,bleft(t,z+1)-1);return k+1===t.length?x[k]:x[k]+s[k]*(z-t[k]);},
   hit(z,a,d){const q=z-d*a,arr=seq[(d+1)/2],k=bleft(arr,q);return k===arr.length?t.at(-1)+q-arr.at(-1):k===0?z:t[k-1]+(q-arr[k-1])/(1-d*s[k-1]);}};
 });
}

function warpMaker(knots,increments,S){
 if(!knots || !increments)return (z)=>z;
 const vals=[0];for(const d of increments)vals.push(vals.at(-1)+d);
 if(Math.abs(vals.at(-1)-1)>1e-7 || Math.abs(knots[0])>1e-10 || Math.abs(knots.at(-1)-1)>1e-10)throw Error("bad warp");
 function atUnit(z){
  let k=Math.floor((z+1)/2),r=z-2*k,sgn=r>=0?1:-1;
  let x=Math.abs(r);const j=Math.min(increments.length-1,Math.max(0,bleft(knots,x)-1));
  const ratio=(x-knots[j])/(knots[j+1]-knots[j]);
  return 2*k+sgn*(vals[j]+increments[j]*ratio);
 }
 return z=>S*atUnit(z/S);
}
function basisUnit(z,j,knots){
 let k=Math.floor((z+1)/2),r=z-2*k,sgn=r>=0?1:-1;
 let x=Math.abs(r),a=knots[j],b=knots[j+1];
 return 2*k+sgn*Math.min(1,Math.max(0,(x-a)/(b-a)));
}
function scoreRoute(half_paths,half_weights,S,route,knots){
 const ps=build(half_paths,half_weights,S),n=ps.length;
 const routeInt=route.map(([t,x])=>[t*S,x*S]);
 function at(q,t){
  const j=Math.max(0,bleft(q.map(z=>z[0]),t+1e-9)-1);
  if(j+1===q.length)return q[j][1];
  return q[j][1]+(t-q[j][0])*(q[j+1][1]-q[j][1])/(q[j+1][0]-q[j][0]);
 }
 const feats=knots.slice(1).map(()=>0), W=half_weights.reduce((a,b)=>a+b,0)*2;
 const encounters=[];
 for(const p of ps){
  const q=p.t.map((t,j)=>[t,p.x[j]]);
  const times=[...new Set(routeInt.map(z=>z[0]).concat(p.t))].sort((a,b)=>a-b);
  let hit=null;
  for(let j=0;j<times.length;j++){
   const t=times[j],d=at(routeInt,t)-p.at(t);
   if(Math.abs(d)<1e-7){hit=t;break;}
   if(j){
    const oldt=times[j-1],oldd=at(routeInt,oldt)-p.at(oldt);
    if(oldd*d<0){hit=oldt+(t-oldt)*Math.abs(oldd)/(Math.abs(oldd)+Math.abs(d));break;}
   }
  }
  if(hit===null)throw Error("uncaptured path");
  const x=p.at(hit),u=(hit+x)/S,v=(hit-x)/S;
  for(let j=0;j<feats.length;j++)feats[j]+=p.w*(basisUnit(u,j,knots)+basisUnit(v,j,knots))/(2*W);
  encounters.push([hit/S,x/S,p.w]);
 }
 return {feats,encounters};
}
function solve(half_paths,half_weights,S,opts={}){
 const ps=build(half_paths,half_weights,S),n=ps.length;
 const wtot=half_weights.reduce((a,b)=>a+b,0),factor=4*wtot*S;
 const psi=warpMaker(opts.warp_knots,opts.warp_increments,S);
 const twice=(t,x)=>psi(t+x)+psi(t-x);
 let best=0;
 for(const p of ps){const h=p.hit(0,-S,1);best+=p.w*twice(h,p.at(h));}
 let bestPath=[[0,-S],[2*S,S]],route=[],memo=new Map(),stats={nodes:0,leaves:0,dominated:0,bounded:0};
 const last=n-1,limit=opts.node_limit||1000000;
 let near=[], capture=[];
 function walk(l,r,anchor,t,x,cost){
   stats.nodes++;if(stats.nodes>limit)throw Error("node limit");
   while(l>0&&ps[l-1].at(t)===x){l--;cost+=ps[l].w*twice(t,x);}
   while(r+1<n&&ps[r+1].at(t)===x){r++;cost+=ps[r].w*twice(t,x);}
   if(l===0&&r===last){
     stats.leaves++;if(cost<best){best=cost;bestPath=route.map(z=>z.slice());}
     if(opts.record_leaves && near.length<1000)near.push({score:cost/factor,route:route.map(z=>[z[0]/S,z[1]/S])});
     return;
   }
   const key=l+":"+r+":"+anchor,vv=memo.get(key)||[];
   for(const [tt,cc] of vv)if(tt<=t&&cc<=cost){stats.dominated++;return;}
   memo.set(key,vv.filter(([tt,cc])=>!(t<=tt&&cost<=cc)).concat([[t,cost]]));
   let lb=cost;for(let j=0;j<l;j++){let h=ps[j].hit(t,x,-1);lb+=ps[j].w*twice(h,ps[j].at(h));}
   for(let j=r+1;j<n;j++){let h=ps[j].hit(t,x,1);lb+=ps[j].w*twice(h,ps[j].at(h));}
   if(lb>=best){stats.bounded++;return;}
   let choices=[];if(l>0)choices.push([ps[l-1].hit(t,x,-1),l-1,-1]);
   if(r+1<n)choices.push([ps[r+1].hit(t,x,1),r+1,1]);
   choices.sort((a,b)=>a[0]-b[0]||b[2]-a[2]);
   for(const [tt,j,d] of choices){
     const xx=x+d*(tt-t);route.push([tt,xx]);
     walk(Math.min(l,j),Math.max(r,j),j,tt,xx,cost+ps[j].w*twice(tt,xx));
     route.pop();
   }
 }
 for(let i=0;i<n;i++){
   if(ps[i].x[0]<0||(i>0&&ps[i].x[0]===ps[i-1].x[0]))continue;
   route=[[0,ps[i].x[0]]];walk(i,i,i,0,ps[i].x[0],0);
 }
 if(opts.capture_times){
   capture=ps.map(p=>({w:p.w,t:0}));
   // First hit along a given route via exact segment intersection; optional later.
 }
 return {score:best/factor,best_path:bestPath.map(([t,x])=>[t/S,x/S]),stats,near};
}
return {solve,build,warpMaker,basisUnit,scoreRoute};