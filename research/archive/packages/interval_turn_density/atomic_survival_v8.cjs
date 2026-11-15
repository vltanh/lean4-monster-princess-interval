/* Dependency-free CommonJS wrapper for the interval finite-law response engine. */
module.exports = (() => {
/* Interval finite-law response engine. Rational geometry preserves all capture predicates. General cut capacities are numerical; Integer supplies replayable exact flow certificates. Exact master certifies its supplied dyadic payoff matrix. No runtime dependencies. */
const Cut=(()=>{

function lower(a,x){let l=0,r=a.length;while(l<r){let m=(l+r)>>1;if(a[m]<x)l=m+1;else r=m;}return l;}
function upper(a,x){let l=0,r=a.length;while(l<r){let m=(l+r)>>1;if(a[m]<=x)l=m+1;else r=m;}return l;}
class Flow {
 constructor(n,tol=1e-12){this.n=n;this.tol=tol;this.head=new Int32Array(n).fill(-1);this.to=[];this.next=[];this.cap=[];}
 add(u,v,c){if(c<0)throw Error("negative capacity");if(!c)return;let e=this.to.length;this.to.push(v,u);this.next.push(this.head[u],this.head[v]);this.cap.push(c,0);this.head[u]=e;this.head[v]=e+1;}
 solve(s,t,inf){
  const n=this.n,h=this.head,to=this.to,nx=this.next,cap=this.cap,tol=this.tol,L=new Int32Array(n),pt=new Int32Array(n),q=new Int32Array(n);
  let flow=0;
  const dfs=(u,f)=>{if(u===t)return f;for(let e=pt[u];e!==-1;pt[u]=e=nx[e])if(cap[e]>tol&&L[to[e]]===L[u]+1){const z=dfs(to[e],Math.min(f,cap[e]));if(z>tol){cap[e]-=z;cap[e^1]+=z;return z;}}return 0;};
  while(true){L.fill(-1);L[s]=0;let a=0,b=0;q[b++]=s;while(a<b){let u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e]>tol&&L[to[e]]<0){L[to[e]]=L[u]+1;q[b++]=to[e];}}
   if(L[t]<0)break;pt.set(h);while(true){let z=dfs(s,inf);if(z<=tol)break;flow+=z;}}
  const reach=new Uint8Array(n);let a=0,b=0;q[b++]=s;reach[s]=1;while(a<b){let u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e]>tol&&!reach[to[e]]){reach[to[e]]=1;q[b++]=to[e];}}
  const sink=new Uint8Array(n);a=0;b=0;q[b++]=t;sink[t]=1;while(a<b){let u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e^1]>tol&&!sink[to[e]]){sink[to[e]]=1;q[b++]=to[e];}}
  return {flow,reach,sink};
 }
}
function cleanLight(points){
 let out=[];for(const p of points){if(out.length&&p[0]===out[out.length-1][0]&&p[1]===out[out.length-1][1])continue;
 while(out.length>1){let a=out[out.length-2],b=out[out.length-1];if((a[0]===b[0]&&b[0]===p[0])||(a[1]===b[1]&&b[1]===p[1]))out.pop();else break;}
 out.push(p);}
 for(let j=1;j<out.length;j++){let a=out[j-1],b=out[j];if(!((b[0]>a[0]&&b[1]===a[1])||(b[1]>a[1]&&b[0]===a[0])))throw Error("non-unit route "+JSON.stringify(out));}
 return out;
}
function family(kind,p){
 let x,s,t,z,v,q;
 if(kind==="M1"){[x]=p;q=[[x,-x],[2-x,-x],[2-x,4-x]];}
 else if(kind==="M2"){[x,s]=p;q=[[x,-x],[s,-x],[s,s+2],[s+4,s+2]];}
 else if(kind==="M3"){[x,s,t]=p;q=[[x,-x],[s,-x],[s,t],[t+2,t],[t+2,t+4]];}
 else{[z,v,s]=p;q=[[z,-z],[z,v],[s,v],[s,s+2],[s+4,s+2]];}
 return {kind,parameters:p,light:cleanLight(q)};
}
class Model{
 constructor(atoms){
  this.atoms=atoms;this.routes=atoms.map(a=>[a.light,a.light.map(([u,v])=>[v,u])]);
  let vs=new Set([-1]),bs=new Set([0]);for(const rr of this.routes)for(const r of rr)for(const [u,v]of r){vs.add(v);if(u>=0)bs.add(u);}
  this.v=Array.from(vs).sort((a,b)=>a-b);this.end=this.v[this.v.length-1];bs.add(this.end+2);
  for(let v of this.v){bs.add(Math.max(v,0));bs.add(v+2);}
  this.base=Array.from(bs).sort((a,b)=>a-b);this.L=this.base.length*3;this.query=new Map(this.v.map((v,i)=>[v,i]));
  this.bounds=this.v.map(v=>[this.ge(Math.max(v,0)),this.ge(v+2)]);this.bounds[0]=[this.ge(0),this.ge(0)];let last=this.ge(this.end+2);this.bounds[this.v.length-1]=[last,last];
  this.offset=[];let n=0;for(const [lo,hi]of this.bounds){this.offset.push(n);n+=hi-lo;}this.N=n;
  this.defs=[];this.defMap=new Map();this.units=[];for(let j=0;j<atoms.length;j++)this.units.push(this.compile(j));
 }
 ge(u){let j=lower(this.base,u);return 3*j+(this.base[j]===u?1:0);}
 gt(u){let j=lower(this.base,u);return 3*j+(this.base[j]===u?2:0);}
 b(k){return this.base[Math.floor(k/3)];}
 node(i,k){let lo=this.bounds[i][0],hi=this.bounds[i][1];if(!(lo<k&&k<=hi))throw Error("forced node");return this.offset[i]+k-lo-1;}
 norm(pos,bits){
  let m=new Map();for(const [i,k]of bits){let[lo,hi]=this.bounds[i];if(pos){if(k<=lo)continue;if(k>hi)return null;m.set(i,Math.max(k,m.has(i)?m.get(i):k));}else{if(k<=lo)return null;if(k>hi)continue;m.set(i,Math.min(k,m.has(i)?m.get(i):k));}}
  let arr=Array.from(m).sort((a,b)=>a[0]-b[0]),out=[];
  if(pos){let high=-1;for(const x of arr)if(x[1]>high){out.push(this.node(...x));high=x[1];}}
  else{let low=this.L+1;for(let j=arr.length-1;j>=0;j--)if(arr[j][1]<low){out.push(this.node(...arr[j]));low=arr[j][1];}out.reverse();}
  return out;
 }
 compile(j){
  let sums=new Map();const add=(pos,bits,c)=>{if(!c)return;if(c<0)throw Error("negative reward");let q=this.norm(pos,bits);if(q===null)return;let key=(pos?"+":"-")+q.join(",");let id=this.defMap.get(key);if(id===undefined){id=this.defs.length;this.defMap.set(key,id);this.defs.push({pos,bits:q});}sums.set(id,(sums.get(id)||0)+c);};
  const bit=(u,v,pos)=>[this.query.get(v),pos?this.gt(u):this.ge(u)];
  for(const route of this.routes[j]){
   let[u0,v0]=route[0],above=[bit(u0,v0,true)],below=[bit(u0,v0,false)];
   for(let k=1;k<route.length;k++){
    let[u1,v1]=route[k];
    if(u1>u0){let idx=this.query.get(v0),old=Math.max(0,Math.min(this.b(0),u1)-u0);add(true,above,old);
     for(let l=1;l<this.L;l++){let z=Math.max(0,Math.min(this.b(l),u1)-u0);if(z>old)add(true,above.concat([[idx,l]]),z-old);old=z;}add(false,below,u1-u0);
    }else{add(true,above,v1-v0);let left=this.query.get(v0),right=this.query.get(v1),th=this.ge(u0);for(let i=left;i<right;i++)add(false,below.concat([[i,th]]),Math.max(0,Math.min(this.v[i+1],u0)-this.v[i]));}
    above.push(bit(u1,v1,true));below.push(bit(u1,v1,false));u0=u1;v0=v1;
   }
  }return Array.from(sums);
 }
 solve(weights,tol=1e-12,retainFace=false){
  let rw=new Float64Array(this.defs.length);for(let j=0;j<weights.length;j++)if(weights[j]>0)for(const[id,c]of this.units[j])rw[id]+=weights[j]*c;
  let lin=new Array(this.N).fill(0),hard=[],constant=0,terms=0;
  for(let id=0;id<rw.length;id++){let w=rw[id];if(!w)continue;terms++;let{pos,bits}=this.defs[id];if(!bits.length){constant+=w;continue;}if(bits.length===1){lin[bits[0]]+=pos?w:-w;if(!pos)constant+=w;}
   else{let a=lin.length;lin.push(pos?w:-w);if(!pos)constant+=w;for(let b of bits)hard.push(pos?[a,b]:[b,a]);}}
  let s=lin.length,t=s+1,g=new Flow(t+1,tol),inf=1+lin.reduce((z,x)=>z+Math.abs(x),0),ceiling=constant;
  for(let i=0;i<lin.length;i++)if(lin[i]>=0){g.add(s,i,lin[i]);ceiling+=lin[i];}else g.add(i,t,-lin[i]);
  for(const[a,b]of hard)g.add(a,b,inf);
  for(let i=0;i<this.v.length;i++){let[lo,hi]=this.bounds[i];for(let k=lo+2;k<=hi;k++)g.add(this.node(i,k),this.node(i,k-1),inf);}
  for(let i=0;i<this.v.length-1;i++){let lo=Math.max(this.bounds[i][0],this.bounds[i+1][0]),hi=Math.min(this.bounds[i][1],this.bounds[i+1][1]);for(let k=lo+1;k<=hi;k++)g.add(this.node(i,k),this.node(i+1,k),inf);}
  let result=g.solve(s,t,inf),labels=[],maxlabels=[];
  for(let i=0;i<this.v.length;i++){let[lo,hi]=this.bounds[i],a=lo,b=lo;for(let k=lo+1;k<=hi;k++){let n=this.node(i,k);if(result.reach[n])a++;if(!result.sink[n])b++;}labels.push(a);maxlabels.push(b);}
  for(let i=1;i<labels.length;i++)if(labels[i]<labels[i-1]||maxlabels[i]<maxlabels[i-1])throw Error("path order");
  let score=constant;for(let i=0;i<lin.length;i++)if(result.reach[i])score+=lin[i];
  let row=this.row(labels),rowmax=this.row(maxlabels),value=row.reduce((z,x,j)=>z+x*weights[j],0),vmax=rowmax.reduce((z,x,j)=>z+x*weights[j],0);
  if(Math.abs(value-score/4)>3e-8||Math.abs(value-vmax)>3e-8)throw Error("cut/contact mismatch "+[value,score/4,vmax]);
  let face=null;if(retainFace){let free=[],edges=[];for(let i=0;i<lin.length;i++)if(!result.reach[i]&&!result.sink[i])free.push(i);let set=new Set(free);for(let a of free)for(let e=g.head[a];e!==-1;e=g.next[e])if(g.cap[e]>tol&&set.has(g.to[e]))edges.push([a,g.to[e]]);face={free,edges,forcedTrue:[],forcedFalse:[]};for(let i=0;i<this.N;i++){if(result.reach[i])face.forcedTrue.push(i);if(result.sink[i])face.forcedFalse.push(i);}}
  return {value,row,rowmax,labels,maxlabels,thresholdNodes:this.N,auxiliaryNodes:lin.length-this.N,rewards:terms,dualValue:(ceiling-result.flow)/4,face};
 }
 capture(route,labels){
  let[u0,v0]=route[0],p=labels[this.query.get(v0)],ge=this.ge(u0),gt=this.gt(u0);if(p>=ge&&p<gt)return(u0+v0)/2;let above=p>=gt;
  for(let k=1;k<route.length;k++){let[u1,v1]=route[k];if(u1>u0&&above){p=labels[this.query.get(v0)];if(p<this.gt(u1))return(this.b(p)+v0)/2;}
   else if(v1>v0&&!above){let at=lower(labels,this.ge(u0));let cross=Math.min(u0,this.v[at]);if(cross<=v1)return(u0+cross)/2;}u0=u1;v0=v1;}
  throw Error("missing capture");
 }
 row(labels){return this.routes.map(r=>(this.capture(r[0],labels)+this.capture(r[1],labels))/2);}
}
return {Flow,Model,family,cleanLight,lower,upper};

})();
const Sparse=(()=>{

function restoreFull(A,shape,atoms){
 const m=Object.create(A.Model.prototype);Object.assign(m,shape,{atoms,routes:atoms.map(a=>[a.light,a.light.map(([u,v])=>[v,u])]),L:shape.base.length*3,query:new Map(shape.v.map((v,i)=>[v,i])),N:shape.offset.at(-1)+shape.bounds.at(-1)[1]-shape.bounds.at(-1)[0]});return m;
}
function liftLabels(small,labels,full){
 let out=[],j=0;for(let i=0;i<full.v.length;i++){
  const v=full.v[i];while(j+1<small.v.length&&small.v[j+1]<=v)j++;
  let b=small.b(labels[j]),side=labels[j]%3-1;
  if(small.v[j]!==v){if(v>=0&&b<=v){b=v;side=1;}else if(b<0){b=0;side=0;}}
  let k=full.ge(b)+side;
  if(i===0)k=full.bounds[i][0];if(i===full.v.length-1)k=full.bounds[i][1];
  if(k<full.bounds[i][0]||k>full.bounds[i][1])throw Error("lift outside physical strip");
  if(i&&k<out[i-1])throw Error("lift is not ordered");out.push(k);
 }
 return out;
}
function sparseSolve(A,full,weights,options={}){
 const indices=[],ws=[],atoms=[];for(let j=0;j<weights.length;j++)if(weights[j]>0){indices.push(j);ws.push(weights[j]);atoms.push(full.atoms[j]);}
 const model=new A.Model(atoms),br=model.solve(ws,options.tol||2e-13,options.retainFace!==false),labels=liftLabels(model,br.labels,full),maxlabels=liftLabels(model,br.maxlabels,full),row=full.row(labels),rowmax=full.row(maxlabels);
 const value=row.reduce((s,x,j)=>s+x*weights[j],0),vmax=rowmax.reduce((s,x,j)=>s+x*weights[j],0);
 if(Math.abs(value-br.value)>3e-9||Math.abs(vmax-br.value)>3e-9)throw Error("sparse lifting changes active payoff "+[value,vmax,br.value]);
 return {value,row,rowmax,labels,maxlabels,smallModel:model,smallResponse:br,indices,thresholdNodes:model.N,auxiliaryNodes:br.auxiliaryNodes,rewards:br.rewards,dualValue:br.dualValue};
}
return{restoreFull,liftLabels,sparseSolve};

})();
const Face=(()=>{

function sampleFaceRows(model,result,samples=64,seed=7271){
 const f=result.face;if(!f)return[];const n=model.N+result.auxiliaryNodes,adj=Array.from({length:n},()=>[]);
 for(const[a,b]of f.edges)adj[a].push(b);
 const cand=f.free.filter(x=>x<model.N),forced=f.forcedTrue,out=[];
 let rng=seed|0;const rnd=()=>{rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return(rng>>>0)/4294967296;};
 for(let s=0;s<samples;s++){
  let yes=new Uint8Array(n),q=[];for(const u of forced)yes[u]=1;
  let target=1<<(s%10);if(s>=samples-4)target=Math.max(1,Math.floor(cand.length*(s-(samples-5))/4));
  for(let k=0;k<target&&cand.length;k++){let u=cand[Math.floor(rnd()*cand.length)];if(!yes[u]){yes[u]=1;q.push(u);}}
  for(let k=0;k<q.length;k++)for(const v of adj[q[k]])if(!yes[v]){yes[v]=1;q.push(v);}
  let labels=[];for(let i=0;i<model.v.length;i++){let[lo,hi]=model.bounds[i],k=lo;for(let x=lo+1;x<=hi;x++)if(yes[model.node(i,x)])k++;labels.push(k);}
  let row=model.row(labels);out.push({row,labels});
 }return out;
}
return {sampleFaceRows};

})();
const Exact=(()=>{

function gcd(a,b){if(a<0n)a=-a;if(b<0n)b=-b;while(b){const r=a%b;a=b;b=r;}return a;}
function abs(a){return a<0n?-a:a;}
function floatRat(x){if(x===0)return[0n,0];const dv=new DataView(new ArrayBuffer(8));dv.setFloat64(0,x);const bits=dv.getBigUint64(0),sign=(bits>>63n)?-1n:1n,e=Number((bits>>52n)&2047n);let n=(bits&((1n<<52n)-1n))+(e?1n<<52n:0n),p=(e?e-1023:1-1023)-52;while(n&&!(n&1n)){n>>=1n;p++;}return[sign*n,p];}
function matrixIntegers(rows){const cache=new Map();let D=0;for(const row of rows)for(const x of row)if(!cache.has(x)){const r=floatRat(x);cache.set(x,r);D=Math.max(D,-r[1]);}const Q=1n<<BigInt(D);for(const[x,r]of cache)cache.set(x,r[0]<<BigInt(D+r[1]));return{A:rows.map(row=>row.map(x=>cache.get(x))),Q,D};}
function solveInteger(A,b){
 const n=A.length;if(!n)return{num:[],den:1n};const M=A.map((r,i)=>r.concat([b[i]]));let previous=1n;
 for(let k=0;k<n-1;k++){
  let p=k;for(let i=k+1;i<n;i++)if(abs(M[i][k])>abs(M[p][k]))p=i;if(M[p][k]===0n)throw Error("singular exact basis");
  if(p!==k){const t=M[p];M[p]=M[k];M[k]=t;}const pivot=M[k][k];
  for(let i=k+1;i<n;i++){const v=M[i][k];for(let j=k+1;j<=n;j++){const z=M[i][j]*pivot-v*M[k][j];if(z%previous!==0n)throw Error("Bareiss nonintegral");M[i][j]=z/previous;}M[i][k]=0n;}previous=pivot;
 }
 let den=M[n-1][n-1];if(!den)throw Error("singular exact basis");const num=new Array(n).fill(0n);
 for(let i=n-1;i>=0;i--){let z=den*M[i][n];for(let j=i+1;j<n;j++)z-=M[i][j]*num[j];if(z%M[i][i]!==0n)throw Error("nonintegral back substitution");num[i]=z/M[i][i];}
 if(den<0n){den=-den;for(let i=0;i<n;i++)num[i]=-num[i];}let g=den;for(const z of num)g=gcd(g,z);if(g>1n){den/=g;for(let i=0;i<n;i++)num[i]/=g;}return{num,den};
}
function ratioNumber(n,d){if(!n)return 0;const sign=n<0n?-1:1;if(n<0n)n=-n;const a=n.toString(),b=d.toString(),ka=Math.min(16,a.length),kb=Math.min(16,b.length);return sign*(Number(a.slice(0,ka))/Number(b.slice(0,kb)))*10**(a.length-ka-b.length+kb);}
function inspect(data,basis){
 const{A,Q}=data,m=A.length,n=A[0].length,C=basis.C,R=basis.R,k=C.length;if(R.length!==k)throw Error("nonsquare basis");
 const K=R.map(i=>C.map(j=>A[i][j])),KT=C.map((_,j)=>R.map((_,i)=>K[i][j])),x=solveInteger(K,new Array(k).fill(Q)),y=solveInteger(KT,new Array(k).fill(Q));
 const ps=new Array(m),ds=new Array(n);for(let i=0;i<m;i++){let z=Q*x.den;for(let l=0;l<k;l++)z-=A[i][C[l]]*x.num[l];ps[i]=z;}
 for(let j=0;j<n;j++){let z=-Q*y.den;for(let l=0;l<k;l++)z+=A[R[l]][j]*y.num[l];ds[j]=z;}
 for(let l=0;l<k;l++)if(ps[R[l]]!==0n||ds[C[l]]!==0n)throw Error("exact basis equations fail");
 const basicViol=[],dualViol=[],CS=new Set(C),RS=new Set(R);
 for(let l=0;l<k;l++){if(x.num[l]<0n)basicViol.push({id:C[l],kind:"original",index:l,num:Q*x.num[l]});if(y.num[l]<0n)dualViol.push({id:n+R[l],kind:"slack",index:l,num:Q*y.num[l]});}
 for(let i=0;i<m;i++)if(!RS.has(i)&&ps[i]<0n)basicViol.push({id:n+i,kind:"slack",index:i,num:ps[i]});
 for(let j=0;j<n;j++)if(!CS.has(j)&&ds[j]<0n)dualViol.push({id:j,kind:"original",index:j,num:ds[j]});
 basicViol.sort((a,b)=>a.id-b.id);dualViol.sort((a,b)=>a.id-b.id);
 return{K,KT,x,y,ps,ds,basicViol,dualViol,CS,RS,primal:basicViol.length===0,dual:dualViol.length===0};
}
function replaceBasis(basis,leave,enter,n){
 const C=basis.C.slice(),R=basis.R.slice(),lo=leave<n,eo=enter<n;
 if(lo&&eo)C[C.indexOf(leave)]=enter;
 else if(lo&&!eo){C.splice(C.indexOf(leave),1);R.splice(R.indexOf(enter-n),1);}
 else if(!lo&&eo){C.push(enter);R.push(leave-n);}
 else R[R.indexOf(enter-n)]=leave-n;
 return{C,R};
}
function repairStep(data,basis){
 const z=inspect(data,basis),{A,Q}=data,n=A[0].length,m=A.length,C=basis.C,R=basis.R,k=C.length;
 if(z.primal&&z.dual)return{basis,done:true,state:z};
 const mixed=!z.primal&&!z.dual;let leave,enter,mode;
 const doDual=z.dual||mixed&&z.basicViol[0].id<z.dualViol[0].id;
 if(doDual){
  const bad=mixed?z.basicViol[0]:z.basicViol.reduce((a,b)=>b.num<a.num?b:a);leave=bad.id;mode=mixed?"criss-cross-primal":"dual";
  let rhs;if(leave<n)rhs=C.map(j=>j===leave?Q:0n);else rhs=C.map(j=>-A[leave-n][j]);
  const lam=solveInteger(z.KT,rhs),candidates=[];
  for(let j=0;j<n;j++)if(!z.CS.has(j)){let d=(leave<n?0n:A[leave-n][j]*lam.den);for(let l=0;l<k;l++)d+=lam.num[l]*A[R[l]][j];if(d<0n)candidates.push({id:j,d:-d,cost:z.ds[j]});}
  for(let l=0;l<k;l++)if(lam.num[l]<0n)candidates.push({id:n+R[l],d:-Q*lam.num[l],cost:Q*z.y.num[l]});
  if(!candidates.length)throw Error("exact dual pivot infeasible");
  candidates.sort((a,b)=>mixed?a.id-b.id:(a.cost*b.d<b.cost*a.d?-1:a.cost*b.d>b.cost*a.d?1:a.id-b.id));enter=candidates[0].id;
 }else{
  const bad=mixed?z.dualViol[0]:z.dualViol.reduce((a,b)=>b.num<a.num?b:a);enter=bad.id;mode=mixed?"criss-cross-dual":"primal";
  const rhs=enter<n?R.map(i=>A[i][enter]):R.map(i=>i===enter-n?Q:0n),d=solveInteger(z.K,rhs),candidates=[];
  for(let l=0;l<k;l++)if(d.num[l]>0n)candidates.push({id:C[l],d:Q*d.num[l],b:Q*z.x.num[l]});
  for(let i=0;i<m;i++)if(!z.RS.has(i)){let v=enter<n?A[i][enter]*d.den:0n;for(let l=0;l<k;l++)v-=A[i][C[l]]*d.num[l];if(v>0n)candidates.push({id:n+i,d:v,b:z.ps[i]});}
  if(!candidates.length)throw Error("exact primal pivot unbounded");
  candidates.sort((a,b)=>mixed?a.id-b.id:(a.b*b.d<b.b*a.d?-1:a.b*b.d>b.b*a.d?1:a.id-b.id));leave=candidates[0].id;
 }
 return{basis:replaceBasis(basis,leave,enter,n),done:false,state:z,pivot:{leave,enter,mode}};
}
function summary(data,basis,z){
 const sx=z.x.num.reduce((a,b)=>a+b,0n),sy=z.y.num.reduce((a,b)=>a+b,0n),weights=new Array(data.A[0].length).fill(0),dual=new Array(data.A.length).fill(0);
 for(let l=0;l<basis.C.length;l++){weights[basis.C[l]]=ratioNumber(z.x.num[l],sx);dual[basis.R[l]]=ratioNumber(z.y.num[l],sy);}
 return{primal:z.primal,dual:z.dual,basicViolations:z.basicViol.length,dualViolations:z.dualViol.length,objective:ratioNumber(sx,z.x.den),dualObjective:ratioNumber(sy,z.y.den),gameValue:ratioNumber(z.x.den,sx),weights,responseDual:dual,k:basis.C.length,integerBits:data.D};
}
function serializeCertificate(data,basis,z){return{scope:"exact stored Float64 dyadic payoff matrix; physical rational recapture still separate",scalePower:data.D,basis,primalNumerators:z.x.num.map(String),primalDenominator:String(z.x.den),dualNumerators:z.y.num.map(String),dualDenominator:String(z.y.den),primalFeasible:z.primal,dualFeasible:z.dual};}
return{gcd,abs,floatRat,matrixIntegers,solveInteger,ratioNumber,inspect,replaceBasis,repairStep,summary,serializeCertificate};

})();
const Absorb=(()=>{

function lower(a,x){let l=0,r=a.length;while(l<r){let m=(l+r)>>1;if(a[m]<x)l=m+1;else r=m;}return l;}
function upper(a,x){let l=0,r=a.length;while(l<r){let m=(l+r)>>1;if(a[m]<=x)l=m+1;else r=m;}return l;}
class Flow {
 constructor(n,tol=1e-12){this.n=n;this.tol=tol;this.head=new Int32Array(n).fill(-1);this.to=[];this.next=[];this.cap=[];}
 add(u,v,c){if(c<0)throw Error("negative capacity");if(!c)return;let e=this.to.length;this.to.push(v,u);this.next.push(this.head[u],this.head[v]);this.cap.push(c,0);this.head[u]=e;this.head[v]=e+1;}
 solve(s,t,inf){
  const n=this.n,h=this.head,to=this.to,nx=this.next,cap=this.cap,tol=this.tol,L=new Int32Array(n),pt=new Int32Array(n),q=new Int32Array(n);
  let flow=0;
  const dfs=(u,f)=>{if(u===t)return f;for(let e=pt[u];e!==-1;pt[u]=e=nx[e])if(cap[e]>tol&&L[to[e]]===L[u]+1){const z=dfs(to[e],Math.min(f,cap[e]));if(z>tol){cap[e]-=z;cap[e^1]+=z;return z;}}return 0;};
  while(true){L.fill(-1);L[s]=0;let a=0,b=0;q[b++]=s;while(a<b){let u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e]>tol&&L[to[e]]<0){L[to[e]]=L[u]+1;q[b++]=to[e];}}
   if(L[t]<0)break;pt.set(h);while(true){let z=dfs(s,inf);if(z<=tol)break;flow+=z;}}
  const reach=new Uint8Array(n);let a=0,b=0;q[b++]=s;reach[s]=1;while(a<b){let u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e]>tol&&!reach[to[e]]){reach[to[e]]=1;q[b++]=to[e];}}
  const sink=new Uint8Array(n);a=0;b=0;q[b++]=t;sink[t]=1;while(a<b){let u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e^1]>tol&&!sink[to[e]]){sink[to[e]]=1;q[b++]=to[e];}}
  return {flow,reach,sink};
 }
}
function cleanLight(points){
 let out=[];for(const p of points){if(out.length&&p[0]===out[out.length-1][0]&&p[1]===out[out.length-1][1])continue;
 while(out.length>1){let a=out[out.length-2],b=out[out.length-1];if((a[0]===b[0]&&b[0]===p[0])||(a[1]===b[1]&&b[1]===p[1]))out.pop();else break;}
 out.push(p);}
 for(let j=1;j<out.length;j++){let a=out[j-1],b=out[j];if(!((b[0]>a[0]&&b[1]===a[1])||(b[1]>a[1]&&b[0]===a[0])))throw Error("non-unit route "+JSON.stringify(out));}
 return out;
}
function family(kind,p){
 let x,s,t,z,v,q;
 if(kind==="M1"){[x]=p;q=[[x,-x],[2-x,-x],[2-x,4-x]];}
 else if(kind==="M2"){[x,s]=p;q=[[x,-x],[s,-x],[s,s+2],[s+4,s+2]];}
 else if(kind==="M3"){[x,s,t]=p;q=[[x,-x],[s,-x],[s,t],[t+2,t],[t+2,t+4]];}
 else{[z,v,s]=p;q=[[z,-z],[z,v],[s,v],[s,s+2],[s+4,s+2]];}
 return {kind,parameters:p,light:cleanLight(q)};
}
class Model{
 constructor(atoms,absorb=null){this.absorb=absorb;
  this.atoms=atoms;this.routes=atoms.map(a=>[a.light,a.light.map(([u,v])=>[v,u])]);
  let vs=new Set([-1]),bs=new Set([0]);if(absorb!==null)vs.add(absorb);for(const rr of this.routes)for(const r of rr)for(const [u,v]of r){vs.add(v);if(u>=0)bs.add(u);}
  this.v=Array.from(vs).sort((a,b)=>a-b);this.end=this.v[this.v.length-1];bs.add(this.end+2);
  for(let v of this.v){bs.add(Math.max(v,0));bs.add(v+2);}
  this.base=Array.from(bs).sort((a,b)=>a-b);this.L=this.base.length*3;this.query=new Map(this.v.map((v,i)=>[v,i]));
  this.bounds=this.v.map(v=>[this.ge(Math.max(v,0)),this.ge(v+2)]);if(absorb!==null)for(let i=0;i<this.v.length;i++)if(this.v[i]>=absorb){const k=this.ge(this.v[i]+2);this.bounds[i]=[k,k];}this.bounds[0]=[this.ge(0),this.ge(0)];let last=this.ge(this.end+2);this.bounds[this.v.length-1]=[last,last];
  this.offset=[];let n=0;for(const [lo,hi]of this.bounds){this.offset.push(n);n+=hi-lo;}this.N=n;
  this.defs=[];this.defMap=new Map();this.units=[];for(let j=0;j<atoms.length;j++)this.units.push(this.compile(j));
 }
 ge(u){let j=lower(this.base,u);return 3*j+(this.base[j]===u?1:0);}
 gt(u){let j=lower(this.base,u);return 3*j+(this.base[j]===u?2:0);}
 b(k){return this.base[Math.floor(k/3)];}
 node(i,k){let lo=this.bounds[i][0],hi=this.bounds[i][1];if(!(lo<k&&k<=hi))throw Error("forced node");return this.offset[i]+k-lo-1;}
 norm(pos,bits){
  let m=new Map();for(const [i,k]of bits){let[lo,hi]=this.bounds[i];if(pos){if(k<=lo)continue;if(k>hi)return null;m.set(i,Math.max(k,m.has(i)?m.get(i):k));}else{if(k<=lo)return null;if(k>hi)continue;m.set(i,Math.min(k,m.has(i)?m.get(i):k));}}
  let arr=Array.from(m).sort((a,b)=>a[0]-b[0]),out=[];
  if(pos){let high=-1;for(const x of arr)if(x[1]>high){out.push(this.node(...x));high=x[1];}}
  else{let low=this.L+1;for(let j=arr.length-1;j>=0;j--)if(arr[j][1]<low){out.push(this.node(...arr[j]));low=arr[j][1];}out.reverse();}
  return out;
 }
 compile(j){
  let sums=new Map();const add=(pos,bits,c)=>{if(!c)return;if(c<0)throw Error("negative reward");let q=this.norm(pos,bits);if(q===null)return;let key=(pos?"+":"-")+q.join(",");let id=this.defMap.get(key);if(id===undefined){id=this.defs.length;this.defMap.set(key,id);this.defs.push({pos,bits:q});}sums.set(id,(sums.get(id)||0)+c);};
  const bit=(u,v,pos)=>[this.query.get(v),pos?this.gt(u):this.ge(u)];
  for(const route of this.routes[j]){
   let[u0,v0]=route[0],above=[bit(u0,v0,true)],below=[bit(u0,v0,false)];
   for(let k=1;k<route.length;k++){
    let[u1,v1]=route[k];
    if(u1>u0){let idx=this.query.get(v0),old=Math.max(0,Math.min(this.b(0),u1)-u0);add(true,above,old);
     for(let l=1;l<this.L;l++){let z=Math.max(0,Math.min(this.b(l),u1)-u0);if(z>old)add(true,above.concat([[idx,l]]),z-old);old=z;}add(false,below,u1-u0);
    }else{add(true,above,v1-v0);let left=this.query.get(v0),right=this.query.get(v1),th=this.ge(u0);for(let i=left;i<right;i++)add(false,below.concat([[i,th]]),Math.max(0,Math.min(this.v[i+1],u0-(this.absorb!==null&&this.v[i]>=this.absorb?2:0))-this.v[i]));}
    above.push(bit(u1,v1,true));below.push(bit(u1,v1,false));u0=u1;v0=v1;
   }
  }return Array.from(sums);
 }
 solve(weights,tol=1e-12,retainFace=false){
  let rw=new Float64Array(this.defs.length);for(let j=0;j<weights.length;j++)if(weights[j]>0)for(const[id,c]of this.units[j])rw[id]+=weights[j]*c;
  let lin=new Array(this.N).fill(0),hard=[],constant=0,terms=0;
  for(let id=0;id<rw.length;id++){let w=rw[id];if(!w)continue;terms++;let{pos,bits}=this.defs[id];if(!bits.length){constant+=w;continue;}if(bits.length===1){lin[bits[0]]+=pos?w:-w;if(!pos)constant+=w;}
   else{let a=lin.length;lin.push(pos?w:-w);if(!pos)constant+=w;for(let b of bits)hard.push(pos?[a,b]:[b,a]);}}
  let s=lin.length,t=s+1,g=new Flow(t+1,tol),inf=1+lin.reduce((z,x)=>z+Math.abs(x),0),ceiling=constant;
  for(let i=0;i<lin.length;i++)if(lin[i]>=0){g.add(s,i,lin[i]);ceiling+=lin[i];}else g.add(i,t,-lin[i]);
  for(const[a,b]of hard)g.add(a,b,inf);
  for(let i=0;i<this.v.length;i++){let[lo,hi]=this.bounds[i];for(let k=lo+2;k<=hi;k++)g.add(this.node(i,k),this.node(i,k-1),inf);}
  for(let i=0;i<this.v.length-1;i++){let lo=Math.max(this.bounds[i][0],this.bounds[i+1][0]),hi=Math.min(this.bounds[i][1],this.bounds[i+1][1]);for(let k=lo+1;k<=hi;k++)g.add(this.node(i,k),this.node(i+1,k),inf);}
  let result=g.solve(s,t,inf),labels=[],maxlabels=[];
  for(let i=0;i<this.v.length;i++){let[lo,hi]=this.bounds[i],a=lo,b=lo;for(let k=lo+1;k<=hi;k++){let n=this.node(i,k);if(result.reach[n])a++;if(!result.sink[n])b++;}labels.push(a);maxlabels.push(b);}
  for(let i=1;i<labels.length;i++)if(labels[i]<labels[i-1]||maxlabels[i]<maxlabels[i-1])throw Error("path order");
  let score=constant;for(let i=0;i<lin.length;i++)if(result.reach[i])score+=lin[i];
  let row=this.row(labels),rowmax=this.row(maxlabels),value=row.reduce((z,x,j)=>z+x*weights[j],0),vmax=rowmax.reduce((z,x,j)=>z+x*weights[j],0);
  if(Math.abs(value-score/4)>3e-8||Math.abs(value-vmax)>3e-8)throw Error("cut/contact mismatch "+[value,score/4,vmax]);
  let face=null;if(retainFace){let free=[],edges=[];for(let i=0;i<lin.length;i++)if(!result.reach[i]&&!result.sink[i])free.push(i);let set=new Set(free);for(let a of free)for(let e=g.head[a];e!==-1;e=g.next[e])if(g.cap[e]>tol&&set.has(g.to[e]))edges.push([a,g.to[e]]);face={free,edges,forcedTrue:[],forcedFalse:[]};for(let i=0;i<this.N;i++){if(result.reach[i])face.forcedTrue.push(i);if(result.sink[i])face.forcedFalse.push(i);}}
  return {value,row,rowmax,labels,maxlabels,thresholdNodes:this.N,auxiliaryNodes:lin.length-this.N,rewards:terms,dualValue:(ceiling-result.flow)/4,face};
 }
 capture(route,labels){
  let[u0,v0]=route[0],p=labels[this.query.get(v0)],ge=this.ge(u0),gt=this.gt(u0);if(p>=ge&&p<gt)return(u0+v0)/2;let above=p>=gt;
  for(let k=1;k<route.length;k++){let[u1,v1]=route[k];if(u1>u0&&above){p=labels[this.query.get(v0)];if(p<this.gt(u1))return(this.b(p)+v0)/2;}
   else if(v1>v0&&!above){let at=lower(labels,this.ge(u0));let limit=this.absorb===null?u0:Math.min(u0,Math.max(this.absorb,u0-2));let cross=Math.min(limit,this.v[at]);if(cross<=v1)return(u0+cross)/2;}u0=u1;v0=v1;}
  throw Error("missing capture");
 }
 row(labels){return this.routes.map(r=>(this.capture(r[0],labels)+this.capture(r[1],labels))/2);}
}
return {Flow,Model,family,cleanLight,lower,upper};

})();
const AbsorbCompare=(()=>{

function compare(A,AA,S,full,weights,ordinary){
 const ids=[],ws=[];for(let j=0;j<weights.length;j++)if(weights[j]>0){ids.push(j);ws.push(weights[j]);}
 const model=new AA.Model(ids.map(j=>full.atoms[j]),1),br=model.solve(ws,2e-13,true);
 function lift(labels){const out=S.liftLabels(model,labels,full);for(let i=0;i<full.v.length;i++)if(full.v[i]>=1)out[i]=full.ge(full.v[i]+2);return out;}
 const fixed=Object.create(AA.Model.prototype);Object.assign(fixed,full,{absorb:1});
 const labels=lift(br.labels),maxlabels=lift(br.maxlabels),row=fixed.row(labels),rowmax=fixed.row(maxlabels);
 const value=row.reduce((s,x,j)=>s+x*weights[j],0),vm=rowmax.reduce((s,x,j)=>s+x*weights[j],0);
 if(Math.abs(value-br.value)>3e-9||Math.abs(vm-br.value)>3e-9)throw Error("absorbing lift changed score");
 const unrestricted=ordinary?ordinary.value:S.sparseSolve(A,full,weights).value;
 return {unrestricted,absorbing:value,gap:unrestricted-value,row,rowmax,labels,maxlabels,indices:ids,smallFace:{v:model.v,base:model.base,bounds:model.bounds,offset:model.offset,N:model.N,face:br.face,labels:br.labels,maxlabels:br.maxlabels}};
}
return{compare};

})();
const Physical=(()=>{

function gcd(a,b){if(a<0n)a=-a;if(b<0n)b=-b;while(b){const r=a%b;a=b;b=r;}return a;}
class Q{
 constructor(n,d=1n){if(n instanceof Q)return n;if(typeof n==="number"){const r=Q.number(n);this.n=r.n;this.d=r.d;return;}if(typeof n==="string"&&n.includes("/")){const a=n.split("/");n=BigInt(a[0]);d=BigInt(a[1]);}else n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);this.n=n/g;this.d=d/g;}
 static number(x){if(x===0)return new Q(0n);const v=new DataView(new ArrayBuffer(8));v.setFloat64(0,x);const bits=v.getBigUint64(0),e=Number((bits>>52n)&2047n),sign=(bits>>63n)?-1n:1n,n=sign*((bits&((1n<<52n)-1n))+(e?1n<<52n:0n)),p=(e?e-1023:1-1023)-52;return p>=0?new Q(n<<BigInt(p)):new Q(n,1n<<BigInt(-p));}
 add(o){o=new Q(o);return new Q(this.n*o.d+o.n*this.d,this.d*o.d);}
 sub(o){o=new Q(o);return new Q(this.n*o.d-o.n*this.d,this.d*o.d);}
 mul(o){o=new Q(o);return new Q(this.n*o.n,this.d*o.d);}
 div(o){o=new Q(o);return new Q(this.n*o.d,this.d*o.n);}
 cmp(o){o=new Q(o);const x=this.n*o.d-o.n*this.d;return x<0n?-1:x>0n?1:0;}
 neg(){return new Q(-this.n,this.d);}
 abs(){return this.n<0n?this.neg():this;}
 toString(){return this.d===1n?String(this.n):this.n+"/"+this.d;}
 number(){return Number(this.n)/Number(this.d);}
}
const min=(...q)=>q.reduce((a,b)=>a.cmp(b)<=0?a:b),max=(...q)=>q.reduce((a,b)=>a.cmp(b)>=0?a:b);
function realize(vs,bases,labels,epsilon="1/1099511627776",strict=true){
 const zero=new Q(0n),one=new Q(1n),two=new Q(2n),three=new Q(3n),eps=new Q(epsilon),connector=eps.mul(eps),vv=vs.map(x=>new Q(x));
 const values=labels.map((k,i)=>{let x=new Q(bases[Math.floor(k/3)]).add(eps.mul(new Q(BigInt(k%3-1))));return min(max(x,vv[i],zero),vv[i].add(two));});
 let points=[[zero,new Q(-1n)]],clamps=0;
 function add(u,v){
  const last=points.at(-1);if(u.cmp(last[0])===0&&v.cmp(last[1])===0)return;
  if(u.cmp(last[0])<0||v.cmp(last[1])<0||u.sub(v).cmp(zero)<0||u.sub(v).cmp(two)>0)throw Error("illegal inverse connector");
  while(points.length>1){const a=points.at(-2),b=points.at(-1);if(b[0].sub(a[0]).mul(v.sub(b[1])).cmp(b[1].sub(a[1]).mul(u.sub(b[0])))!==0)break;points.pop();}
  points.push([u,v]);
 }
 for(let j=1;j<vv.length;j++){
  const v=vv[j],previous=values[j-1],target=values[j],delta=min(connector,v.sub(vv[j-1]).div(three)),before=v.sub(delta);
  add(previous,min(before,previous));if(before.cmp(previous)>0)add(before,before);add(min(target,before.add(two)),before);if(target.cmp(before.add(two))>0)add(target,target.sub(two));add(target,v);
 }
 let path=[];for(let j=1;j<points.length;j++){const a=points[j-1],b=points[j],t0=a[0].add(a[1]).div(two),t1=b[0].add(b[1]).div(two),x0=a[0].sub(a[1]).div(two),x1=b[0].sub(b[1]).div(two);if(t1.cmp(zero)<0)continue;if(!path.length){if(t0.cmp(zero)>0)throw Error("virtual curve skips time zero");const x=t0.cmp(zero)===0?x0:x0.add(x1.sub(x0).mul(t0.neg()).div(t1.sub(t0)));path.push([zero,x]);}if(t1.cmp(path.at(-1)[0])>0)path.push([t1,x1]);}
 const eta=strict?eps.mul(eps).mul(eps).mul(eps).mul(eps).mul(eps):zero,factor=one.sub(two.mul(eta));if(strict)path=path.map(([t,x])=>[t,factor.mul(x).add(eta)]);
 for(let j=1;j<path.length;j++){const[a,x]=path[j-1],[b,y]=path[j];if(x.cmp(zero)<0||x.cmp(one)>0||y.cmp(zero)<0||y.cmp(one)>0||b.cmp(a)<=0||y.sub(x).abs().cmp(b.sub(a))>0)throw Error("illegal realized physical path");}
 return{path:path.map(p=>p.map(String)),epsilon:eps.toString(),strictEta:eta.toString(),pointCount:path.length};
}
function capture(p,m){
 p=p.map(q=>q.map(x=>new Q(x)));m=m.map(q=>q.map(x=>new Q(x)));let i=0,j=0;
 const val=(r,k,t)=>k>=r.length-1?r.at(-1)[1]:r[k][1].add(r[k+1][1].sub(r[k][1]).mul(t.sub(r[k][0])).div(r[k+1][0].sub(r[k][0])));
 while(j<m.length-1){const lo=max(p[i][0],m[j][0]),hi=i<p.length-1?min(p[i+1][0],m[j+1][0]):m[j+1][0],d0=val(p,i,lo).sub(val(m,j,lo)),d1=val(p,i,hi).sub(val(m,j,hi));if(d0.n===0n)return lo;if(d0.cmp(new Q(0n))*d1.cmp(new Q(0n))<=0)return lo.add(hi.sub(lo).mul(d0).div(d0.sub(d1)));if(i<p.length-1&&p[i+1][0].cmp(hi)===0)i++;if(m[j+1][0].cmp(hi)===0)j++;}
 return null;
}
return {Q,realize,capture};

})();
const FaceOpt=(()=>{

function compress(model,result){
 const f=result.face,n=f.free.length,idMap=new Map(f.free.map((x,i)=>[x,i])),adj=Array.from({length:n},()=>[]),rev=Array.from({length:n},()=>[]);
 for(const[a,b]of f.edges){const u=idMap.get(a),v=idMap.get(b);adj[u].push(v);rev[v].push(u);}
 const seen=new Uint8Array(n),order=[];
 for(let i=0;i<n;i++)if(!seen[i]){const stack=[[i,0]];seen[i]=1;while(stack.length){const p=stack.at(-1),u=p[0];if(p[1]<adj[u].length){const v=adj[u][p[1]++];if(!seen[v]){seen[v]=1;stack.push([v,0]);}}else{order.push(u);stack.pop();}}}
 const comp=new Int32Array(n).fill(-1);let count=0;
 for(let k=order.length-1;k>=0;k--){const i=order[k];if(comp[i]>=0)continue;const stack=[i];comp[i]=count;while(stack.length){const u=stack.pop();for(const v of rev[u])if(comp[v]<0){comp[v]=count;stack.push(v);}}count++;}
 const nodeComp=new Int32Array(model.N).fill(-3);for(const u of f.forcedTrue)nodeComp[u]=-1;for(const u of f.forcedFalse)nodeComp[u]=-2;for(let i=0;i<n;i++)if(f.free[i]<model.N)nodeComp[f.free[i]]=comp[i];for(const c of nodeComp)if(c===-3)throw Error("unclassified face threshold");
 const es=new Set(),edges=[];for(let u=0;u<n;u++)for(const v of adj[u]){const a=comp[u],b=comp[v],k=a+","+b;if(a!==b&&!es.has(k)){es.add(k);edges.push([a,b]);}}
 return{count,nodeComp:Array.from(nodeComp),edges,primaryValue:result.value};
}
function optimize(Cut,model,face,weights,primaryWeights=null,tolerance=2e-13){
 const rw=new Float64Array(model.defs.length);for(let j=0;j<weights.length;j++)if(weights[j]>0)for(const[id,c]of model.units[j])rw[id]+=weights[j]*c;
 const terms=new Map();let constant=0;
 for(let id=0;id<rw.length;id++)if(rw[id]>0){const d=model.defs[id],bits=new Set();let dead=false;for(const node of d.bits){const c=face.nodeComp[node];if(d.pos&&c===-2||!d.pos&&c===-1){dead=true;break;}if(c>=0)bits.add(c);}if(dead)continue;const bs=Array.from(bits).sort((a,b)=>a-b);if(!bs.length){constant+=rw[id];continue;}const key=(d.pos?"+":"-")+bs.join(","),old=terms.get(key);if(old)old.w+=rw[id];else terms.set(key,{pos:d.pos,bits:bs,w:rw[id]});}
 const lin=new Array(face.count).fill(0),hard=face.edges.slice();for(const{pos,bits,w}of terms.values()){if(bits.length===1){lin[bits[0]]+=pos?w:-w;if(!pos)constant+=w;}else{const a=lin.length;lin.push(pos?w:-w);if(!pos)constant+=w;for(const b of bits)hard.push(pos?[a,b]:[b,a]);}}
 const s=lin.length,t=s+1,flow=new Cut.Flow(t+1,tolerance),inf=1+lin.reduce((a,b)=>a+Math.abs(b),0);for(let i=0;i<lin.length;i++)if(lin[i]>0)flow.add(s,i,lin[i]);else if(lin[i]<0)flow.add(i,t,-lin[i]);for(const[a,b]of hard)flow.add(a,b,inf);
 const f=flow.solve(s,t,inf),labels=[],maxlabels=[];
 for(let i=0;i<model.v.length;i++){const[lo,hi]=model.bounds[i];let a=lo,b=lo;for(let k=lo+1;k<=hi;k++){const c=face.nodeComp[model.node(i,k)];if(c===-1||c>=0&&f.reach[c])a++;if(c===-1||c>=0&&!f.sink[c])b++;}labels.push(a);maxlabels.push(b);}
 const row=model.row(labels),rowmax=model.row(maxlabels),value=row.reduce((s,x,j)=>s+x*weights[j],0),vmax=rowmax.reduce((s,x,j)=>s+x*weights[j],0);let cut=constant;for(let i=0;i<lin.length;i++)if(f.reach[i])cut+=lin[i];if(Math.abs(value-cut/4)>3e-8||Math.abs(value-vmax)>3e-8)throw Error("projected cut cost mismatch");
 const primary=primaryWeights?row.reduce((s,x,j)=>s+x*primaryWeights[j],0):null;if(primary!==null&&Math.abs(primary-face.primaryValue)>3e-8)throw Error("projected path leaves primary face");
 return{value,row,rowmax,labels,maxlabels,primary,components:face.count,nodes:lin.length};
}
return{compress,optimize};

})();
const BigFlow=(()=>{

class BigFlow{
 constructor(n){this.n=n;this.head=new Int32Array(n).fill(-1);this.to=[];this.next=[];this.cap=[];}
 add(u,v,c){if(c<0n)throw Error("negative integer capacity");if(!c)return;const e=this.to.length;this.to.push(v,u);this.next.push(this.head[u],this.head[v]);this.cap.push(c,0n);this.head[u]=e;this.head[v]=e+1;}
 solve(s,t,inf){
  const n=this.n,h=this.head,to=this.to,nx=this.next,cap=this.cap,L=new Int32Array(n),pt=new Int32Array(n),q=new Int32Array(n);let flow=0n,phases=0,pushes=0;
  const dfs=(u,f)=>{if(u===t)return f;for(let e=pt[u];e!==-1;pt[u]=e=nx[e])if(cap[e]>0n&&L[to[e]]===L[u]+1){const z=dfs(to[e],f<cap[e]?f:cap[e]);if(z>0n){cap[e]-=z;cap[e^1]+=z;return z;}}return 0n;};
  while(true){L.fill(-1);L[s]=0;let a=0,b=0;q[b++]=s;while(a<b){const u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e]>0n&&L[to[e]]<0){L[to[e]]=L[u]+1;q[b++]=to[e];}}if(L[t]<0)break;phases++;pt.set(h);while(true){const z=dfs(s,inf);if(z===0n)break;flow+=z;pushes++;}}
  const reach=new Uint8Array(n),sink=new Uint8Array(n);let a=0,b=0;q[b++]=s;reach[s]=1;while(a<b){const u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e]>0n&&!reach[to[e]]){reach[to[e]]=1;q[b++]=to[e];}}
  a=0;b=0;q[b++]=t;sink[t]=1;while(a<b){const u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e^1]>0n&&!sink[to[e]]){sink[to[e]]=1;q[b++]=to[e];}}
  return{flow,reach,sink,phases,pushes};
 }
}
return{BigFlow};

})();
const Integer=(()=>{

function solveIntegerLaw(Cut,Physical,BigFlow,model,weightNumerators,weightDenominator,options={}){
 const {Q}=Physical;function gcd(a,b){while(b){const t=a%b;a=b;b=t;}return a;}let scale=1n;for(const q of model.vQ.concat(model.baseQ))scale=scale/gcd(scale,q.d)*q.d;
 model.defMap=new Map(model.defs.map((d,i)=>[(d.pos?"+":"-")+d.bits.join(","),i]));
 const rw=new Array(model.defs.length).fill(0n);let totalWeight=0n;
 for(let j=0;j<weightNumerators.length;j++){const w=BigInt(weightNumerators[j]);totalWeight+=w;if(w>0n){model.compile(j);for(const[id,c]of model.lastExactUnits){if(scale%c.d!==0n)throw Error("reward denominator outside geometry scale");rw[id]+=w*c.n*(scale/c.d);}}}
 if(totalWeight!==BigInt(weightDenominator))throw Error("integer probability mass");
 const lin=new Array(model.N).fill(0n),hard=[];let constant=0n,terms=0;
 for(let id=0;id<rw.length;id++){const w=rw[id];if(w===0n)continue;terms++;const{pos,bits}=model.defs[id];if(!bits.length){constant+=w;continue;}if(bits.length===1){lin[bits[0]]+=pos?w:-w;if(!pos)constant+=w;}else{const a=lin.length;lin.push(pos?w:-w);if(!pos)constant+=w;for(const b of bits)hard.push(pos?[a,b]:[b,a]);}}
 const s=lin.length,t=s+1,g=new BigFlow(t+1),inf=1n+lin.reduce((a,b)=>a+(b<0n?-b:b),0n);let ceiling=constant;
 for(let i=0;i<lin.length;i++)if(lin[i]>0n){g.add(s,i,lin[i]);ceiling+=lin[i];}else if(lin[i]<0n)g.add(i,t,-lin[i]);
 for(const[a,b]of hard)g.add(a,b,inf);
 for(let i=0;i<model.v.length;i++){const[lo,hi]=model.bounds[i];for(let k=lo+2;k<=hi;k++)g.add(model.node(i,k),model.node(i,k-1),inf);}
 for(let i=0;i<model.v.length-1;i++){const lo=Math.max(model.bounds[i][0],model.bounds[i+1][0]),hi=Math.min(model.bounds[i][1],model.bounds[i+1][1]);for(let k=lo+1;k<=hi;k++)g.add(model.node(i,k),model.node(i+1,k),inf);}
 if(options.buildOnly)return{graph:g,source:s,sink:t,scale,lin,constant,ceiling,inf,weightDenominator:BigInt(weightDenominator)};
 const f=g.solve(s,t,inf),labels=[],maxlabels=[];
 for(let i=0;i<model.v.length;i++){const[lo,hi]=model.bounds[i];let a=lo,b=lo;for(let k=lo+1;k<=hi;k++){const n=model.node(i,k);if(f.reach[n])a++;if(!f.sink[n])b++;}labels.push(a);maxlabels.push(b);}
 let score=constant;for(let i=0;i<lin.length;i++)if(f.reach[i])score+=lin[i];if(score!==ceiling-f.flow)throw Error("exact max-flow/min-cut mismatch");
 const den=4n*scale*BigInt(weightDenominator),valueQ=new Q(score,den),row=model.rowExact(labels),rowmax=model.rowExact(maxlabels);let direct=new Q(0n),directMax=new Q(0n);for(let j=0;j<weightNumerators.length;j++)if(BigInt(weightNumerators[j])>0n){const w=new Q(BigInt(weightNumerators[j]),BigInt(weightDenominator));direct=direct.add(w.mul(row[j]));directMax=directMax.add(w.mul(rowmax[j]));}
 if(direct.cmp(valueQ)!==0||directMax.cmp(valueQ)!==0)throw Error("exact path/cut mismatch");
 const free=[],edges=[],forcedTrue=[],forcedFalse=[];
 for(let i=0;i<lin.length;i++)if(!f.reach[i]&&!f.sink[i])free.push(i);const fs=new Set(free);
 for(const a of free)for(let e=g.head[a];e!==-1;e=g.next[e])if(g.cap[e]>0n&&fs.has(g.to[e]))edges.push([a,g.to[e]]);
 for(let i=0;i<model.N;i++){if(f.reach[i])forcedTrue.push(i);if(f.sink[i])forcedFalse.push(i);}
 const flowValues=[],flowMap=new Map(),positiveFlows=[],sourceSide=[];const balances=new Array(g.n).fill(0n);let checkedCut=0n;for(let e=0;e<g.to.length;e+=2){const u=g.to[e^1],v=g.to[e],cap=g.cap[e]+g.cap[e^1],fl=g.cap[e^1];if(fl<0n||fl>cap)throw Error("exact flow capacity violation");balances[u]-=fl;balances[v]+=fl;if(f.reach[u]&&!f.reach[v])checkedCut+=cap;if(fl>0n){const key=String(fl);let id=flowMap.get(key);if(id===undefined){id=flowValues.length;flowMap.set(key,id);flowValues.push(key);}positiveFlows.push([e/2,id]);}}for(let i=0;i<g.n;i++){if(i!==s&&i!==t&&balances[i]!==0n)throw Error("exact flow conservation");if(f.reach[i])sourceSide.push(i);}if(balances[t]!==f.flow||balances[s]!==-f.flow||checkedCut!==f.flow)throw Error("exact flow/cut certificate failed");
 return{flowCertificate:{flowValues,positiveFlows,sourceSide,source:s,sink:t},value:valueQ.number(),exactValue:valueQ.toString(),labels,maxlabels,row:row.map(x=>x.number()),rowmax:rowmax.map(x=>x.number()),thresholdNodes:model.N,auxiliaryNodes:lin.length-model.N,rewards:terms,face:{free,edges,forcedTrue,forcedFalse},certificate:{scale:String(scale),weightDenominator:String(weightDenominator),maximumFlow:String(f.flow),cutCapacity:String(ceiling-score),totalRewardCeiling:String(ceiling),score:String(score),denominator:String(den),phases:f.phases,pushes:f.pushes,nodes:g.n,arcs:g.to.length/2}};
}

function verifyIntegerFlow(Cut,Physical,BigFlow,model,weightNumerators,weightDenominator,certificate){
 const b=solveIntegerLaw(Cut,Physical,BigFlow,model,weightNumerators,weightDenominator,{buildOnly:true}),g=b.graph,flows=new Map(certificate.positiveFlows.map(([id,v])=>[id,BigInt(certificate.flowValues[v])])),side=new Set(certificate.sourceSide),balance=new Array(g.n).fill(0n);let cut=0n;
 for(let e=0;e<g.to.length;e+=2){const u=g.to[e^1],v=g.to[e],cap=g.cap[e],f=flows.get(e/2)||0n;if(f<0n||f>cap)throw Error("certificate capacity violation");balance[u]-=f;balance[v]+=f;if(side.has(u)&&!side.has(v))cut+=cap;}
 for(const id of flows.keys())if(id<0||id>=g.to.length/2)throw Error("certificate nonexistent edge");
 for(let i=0;i<g.n;i++)if(i!==b.source&&i!==b.sink&&balance[i]!==0n)throw Error("certificate conservation violation");
 if(!side.has(b.source)||side.has(b.sink)||balance[b.source]!==-balance[b.sink]||cut!==balance[b.sink])throw Error("certificate max-flow/min-cut inequality");
 return{exactValue:new Physical.Q(b.ceiling-cut,4n*b.scale*b.weightDenominator).toString(),flow:String(cut),nodes:g.n,arcs:g.to.length/2,positiveFlows:flows.size};
}
return{solveIntegerLaw,verifyIntegerFlow};

})();
const Rational=(function(Cut,Physical){

const {Q}=Physical,zero=new Q(0n),two=new Q(2n);
const qmin=(a,b)=>a.cmp(b)<=0?a:b,qmax=(a,b)=>a.cmp(b)>=0?a:b;
const key=q=>q.toString();
function search(a,x,strict){let l=0,r=a.length;while(l<r){const m=(l+r)>>1,c=a[m].cmp(x);if(c<0||strict&&c===0)l=m+1;else r=m;}return l;}
function initialize(m,atoms){
 m.atoms=atoms;m.routes=atoms.map(a=>{const p=a.exact_light.map(r=>r.map(x=>new Q(x)));for(let j=0;j<p.length;j++){const[u,v]=p[j];if(u.add(v).cmp(zero)<0||u.sub(v).abs().cmp(two)>0)throw Error("nonphysical rational monster vertex");if(j){const x=p[j-1];if(!((u.cmp(x[0])>0&&v.cmp(x[1])===0)||(v.cmp(x[1])>0&&u.cmp(x[0])===0)))throw Error("non-unit rational monster leg");}}return[p,p.map(([u,v])=>[v,u])];});
 m.ge=function(x){x=new Q(x);const j=search(this.baseQ,x,false);return 3*j+(j<this.baseQ.length&&this.baseQ[j].cmp(x)===0?1:0);};
 m.gt=function(x){x=new Q(x);const j=search(this.baseQ,x,false);return 3*j+(j<this.baseQ.length&&this.baseQ[j].cmp(x)===0?2:0);};
 m.b=function(k){return this.baseQ[Math.floor(k/3)];};
 m.capture=function(route,labels){let[u0,v0]=route[0],p=labels[this.query.get(key(v0))],ge=this.ge(u0),gt=this.gt(u0);if(p>=ge&&p<gt)return u0.add(v0).div(two);const above=p>=gt;
  for(let k=1;k<route.length;k++){const[u1,v1]=route[k];if(u1.cmp(u0)>0&&above){p=labels[this.query.get(key(v0))];if(p<this.gt(u1))return this.b(p).add(v0).div(two);}else if(v1.cmp(v0)>0&&!above){const at=Cut.lower(labels,this.ge(u0)),cross=qmin(u0,this.vQ[at]);if(cross.cmp(v1)<=0)return u0.add(cross).div(two);}u0=u1;v0=v1;}throw Error("rational missing capture");};
 m.rowExact=function(labels){return this.routes.map(rr=>this.capture(rr[0],labels).add(this.capture(rr[1],labels)).div(two));};
 m.row=function(labels){return this.rowExact(labels).map(x=>x.number());};
 m.compile=function(j){
  const sums=new Map();const add=(pos,bits,c)=>{if(c.n===0n)return;if(c.n<0n)throw Error("negative rational reward");const q=this.norm(pos,bits);if(q===null)return;const kk=(pos?"+":"-")+q.join(",");let id=this.defMap.get(kk);if(id===undefined){id=this.defs.length;this.defMap.set(kk,id);this.defs.push({pos,bits:q});}const prior=sums.get(id)||zero;sums.set(id,prior.add(c));};
  const bit=(u,v,pos)=>[this.query.get(key(v)),pos?this.gt(u):this.ge(u)];
  for(const route of this.routes[j]){let[u0,v0]=route[0],above=[bit(u0,v0,true)],below=[bit(u0,v0,false)];
   for(let k=1;k<route.length;k++){const[u1,v1]=route[k];if(u1.cmp(u0)>0){const idx=this.query.get(key(v0));let old=qmax(zero,qmin(this.baseQ[0],u1).sub(u0));add(true,above,old);
    for(let l=1;l<this.baseQ.length;l++){const z=qmax(zero,qmin(this.baseQ[l],u1).sub(u0));if(z.cmp(old)>0)add(true,above.concat([[idx,3*l]]),z.sub(old));old=z;}add(false,below,u1.sub(u0));
   }else{add(true,above,v1.sub(v0));const left=this.query.get(key(v0)),right=this.query.get(key(v1)),th=this.ge(u0);for(let i=left;i<right;i++)add(false,below.concat([[i,th]]),qmax(zero,qmin(this.vQ[i+1],u0).sub(this.vQ[i])));}
   above.push(bit(u1,v1,true));below.push(bit(u1,v1,false));u0=u1;v0=v1;
  }}this.lastExactUnits=Array.from(sums);return Array.from(sums,([id,c])=>[id,c.number()]);
 };
}
function Model(atoms){
 const m=Object.create(Cut.Model.prototype);initialize(m,atoms);const vv=new Map([["-1",new Q(-1n)]]),bb=new Map([["0",zero]]);
 for(const rr of m.routes)for(const r of rr)for(const[u,v]of r){vv.set(key(v),v);if(u.cmp(zero)>=0)bb.set(key(u),u);}
 m.vQ=Array.from(vv.values()).sort((a,b)=>a.cmp(b));for(const v of m.vQ){const lo=qmax(v,zero),hi=v.add(two);bb.set(key(lo),lo);bb.set(key(hi),hi);}
 m.baseQ=Array.from(bb.values()).sort((a,b)=>a.cmp(b));m.v=m.vQ.map(key);m.base=m.baseQ.map(key);m.L=3*m.base.length;m.query=new Map(m.v.map((v,i)=>[v,i]));
 m.bounds=m.vQ.map(v=>[m.ge(qmax(v,zero)),m.ge(v.add(two))]);m.bounds[0]=[m.ge(zero),m.ge(zero)];const last=m.ge(m.vQ.at(-1).add(two));m.bounds[m.bounds.length-1]=[last,last];
 m.offset=[];let n=0;for(const[lo,hi]of m.bounds){m.offset.push(n);n+=hi-lo;}m.N=n;m.defs=[];m.defMap=new Map();m.units=[];for(let j=0;j<atoms.length;j++)m.units.push(m.compile(j));return m;
}
function pack(m){return{v:m.v,base:m.base,bounds:m.bounds,offset:m.offset,N:m.N,defs:m.defs,units:m.units};}
function restore(shape,atoms){const m=Object.create(Cut.Model.prototype);initialize(m,atoms);Object.assign(m,shape);m.vQ=m.v.map(x=>new Q(x));m.baseQ=m.base.map(x=>new Q(x));m.L=m.base.length*3;m.query=new Map(m.v.map((v,i)=>[v,i]));return m;}
function lift(small,labels,full){let out=[],j=0;for(let i=0;i<full.vQ.length;i++){const v=full.vQ[i];while(j+1<small.vQ.length&&small.vQ[j+1].cmp(v)<=0)j++;let b=small.b(labels[j]),side=labels[j]%3-1;if(small.vQ[j].cmp(v)!==0){if(v.cmp(zero)>=0&&b.cmp(v)<=0){b=v;side=1;}else if(b.cmp(zero)<0){b=zero;side=0;}}let k=full.ge(b)+side;if(i===0)k=full.bounds[i][0];if(i===full.v.length-1)k=full.bounds[i][1];if(k<full.bounds[i][0]||k>full.bounds[i][1]||i&&k<out[i-1])throw Error("rational lift illegal");out.push(k);}return out;}
function sparseSolve(full,weights,retainFace=true){
 const indices=[],atoms=[],ws=[];for(let j=0;j<weights.length;j++)if(weights[j]>0){indices.push(j);atoms.push(full.atoms[j]);ws.push(weights[j]);}const m=new Model(atoms),br=m.solve(ws,2e-13,retainFace),labels=lift(m,br.labels,full),maxlabels=lift(m,br.maxlabels,full),row=full.row(labels),rowmax=full.row(maxlabels),value=row.reduce((s,x,j)=>s+x*weights[j],0),vm=rowmax.reduce((s,x,j)=>s+x*weights[j],0);if(Math.abs(value-br.value)>3e-9||Math.abs(vm-br.value)>3e-9)throw Error("rational lift score changed");return{value,row,rowmax,labels,maxlabels,smallModel:m,smallResponse:br,indices,thresholdNodes:m.N,auxiliaryNodes:br.auxiliaryNodes,rewards:br.rewards,dualValue:br.dualValue};
}
return{Model,pack,restore,lift,sparseSolve};

})(Cut,Physical);
return {Cut,Sparse,Face,Exact,Absorb,AbsorbCompare,Physical,FaceOpt,BigFlow,Integer,Rational};

})();
