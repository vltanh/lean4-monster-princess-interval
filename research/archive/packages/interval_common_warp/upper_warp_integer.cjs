"use strict";
// Integer certificates; probability and warp-increment denominators are kept explicit.
module.exports=(function(){

function build(data,candidate,BigFlow){
 const inc=candidate.increment_numerators.map(BigInt),den=BigInt(candidate.increment_denominator),sum=inc.reduce((a,b)=>a+b,0n);
 if(sum!==den||inc.some(x=>x<=0n))throw Error("strict rational warp required");
 const cum=[0n];for(const x of inc)cum.push(cum[cum.length-1]+x);
 const p=data.projection,rw=new Array(p.defs.length).fill(0n);
 for(const[id,lo,hi,n]of data.intervals){if(!Number.isSafeInteger(n)||n<0)throw Error("invalid interval coefficient");rw[id]+=(cum[hi]-cum[lo])*BigInt(n);}
 const lin=new Array(p.N).fill(0n),hard=[];let constant=0n;
 for(let i=0;i<rw.length;i++){
  const w=rw[i];if(w===0n)continue;const r=p.defs[i];
  if(!r.bits.length){constant+=w;continue;}
  if(r.bits.length===1){lin[r.bits[0]]+=r.pos?w:-w;if(!r.pos)constant+=w;}
  else{const a=lin.length;lin.push(r.pos?w:-w);if(!r.pos)constant+=w;for(const b of r.bits)hard.push(r.pos?[a,b]:[b,a]);}
 }
 const source=lin.length,sink=source+1,g=new BigFlow(sink+1),inf=1n+lin.reduce((a,b)=>a+(b<0n?-b:b),0n);let ceiling=constant;
 for(let i=0;i<lin.length;i++)if(lin[i]>0n){g.add(source,i,lin[i]);ceiling+=lin[i];}else if(lin[i]<0n)g.add(i,sink,-lin[i]);
 for(const[a,b]of hard)g.add(a,b,inf);for(const[a,b]of p.threshold_hard)g.add(a,b,inf);
 return{g,source,sink,inf,ceiling,constant,lin,denominator:4n*BigInt(data.denominator)*den};
}
async function maxflow(b,progress){
 const g=b.g,n=g.n,h=g.head,to=g.to,nx=g.next,cap=g.cap,s=b.source,t=b.sink,inf=b.inf,L=new Int32Array(n),pt=new Int32Array(n),q=new Int32Array(n);
 let flow=0n,phases=0,pushes=0,last=Date.now();
 function dfs(u,f){if(u===t)return f;for(let e=pt[u];e!==-1;pt[u]=e=nx[e])if(cap[e]>0n&&L[to[e]]===L[u]+1){const z=dfs(to[e],f<cap[e]?f:cap[e]);if(z>0n){cap[e]-=z;cap[e^1]+=z;return z;}}return 0n;}
 while(true){L.fill(-1);L[s]=0;let a=0,z=0;q[z++]=s;while(a<z){const u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e]>0n&&L[to[e]]<0){L[to[e]]=L[u]+1;q[z++]=to[e];}}
  if(L[t]<0)break;phases++;pt.set(h);while(true){const v=dfs(s,inf);if(v===0n)break;flow+=v;pushes++;}
  if(progress&&Date.now()-last>15000){last=Date.now();await progress({phases,pushes,flow:String(flow)});}
 }
 const reach=new Uint8Array(n),sinkReach=new Uint8Array(n);let a=0,z=0;q[z++]=s;reach[s]=1;
 while(a<z){const u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e]>0n&&!reach[to[e]]){reach[to[e]]=1;q[z++]=to[e];}}
 a=0;z=0;q[z++]=t;sinkReach[t]=1;while(a<z){const u=q[a++];for(let e=h[u];e!==-1;e=nx[e])if(cap[e^1]>0n&&!sinkReach[to[e]]){sinkReach[to[e]]=1;q[z++]=to[e];}}
 return{flow,phases,pushes,reach,sinkReach};
}
function certificate(b,f){
 const g=b.g,values=[],map=new Map(),positive=[],side=[],balance=new Array(g.n).fill(0n);let cut=0n;
 for(let e=0;e<g.to.length;e+=2){const u=g.to[e^1],v=g.to[e],cap=g.cap[e]+g.cap[e^1],flow=g.cap[e^1];if(flow<0n||flow>cap)throw Error("capacity");
  balance[u]-=flow;balance[v]+=flow;if(f.reach[u]&&!f.reach[v])cut+=cap;
  if(flow>0n){const key=String(flow);let id=map.get(key);if(id===undefined){id=values.length;map.set(key,id);values.push(key);}positive.push([e/2,id]);}}
 for(let i=0;i<g.n;i++){if(i!==b.source&&i!==b.sink&&balance[i]!==0n)throw Error("conservation");if(f.reach[i])side.push(i);}
 if(balance[b.sink]!==f.flow||balance[b.source]!==-f.flow||cut!==f.flow)throw Error("cut");
 return{flowValues:values,positiveFlows:positive,sourceSide:side,source:b.source,sink:b.sink,flow:String(f.flow),ceiling:String(b.ceiling),denominator:String(b.denominator),nodes:g.n,arcs:g.to.length/2,phases:f.phases,pushes:f.pushes};
}
function verify(data,candidate,cert,BigFlow,Q){
 const b=build(data,candidate,BigFlow),g=b.g,flows=new Map(cert.positiveFlows.map(([e,i])=>[e,BigInt(cert.flowValues[i])])),side=new Set(cert.sourceSide),balance=new Array(g.n).fill(0n);let cut=0n;
 if(cert.source!==b.source||cert.sink!==b.sink||!side.has(b.source)||side.has(b.sink))throw Error("terminals");
 for(const[e,f]of flows)if(!Number.isInteger(e)||e<0||e>=g.to.length/2||f<=0n)throw Error("flow index");
 for(let e=0;e<g.to.length;e+=2){const u=g.to[e^1],v=g.to[e],f=flows.get(e/2)||0n,c=g.cap[e];if(f<0n||f>c)throw Error("capacity");balance[u]-=f;balance[v]+=f;if(side.has(u)&&!side.has(v))cut+=c;}
 for(let i=0;i<g.n;i++)if(i!==b.source&&i!==b.sink&&balance[i]!==0n)throw Error("conservation");
 if(balance[b.source]!==-cut||balance[b.sink]!==cut)throw Error("flow/cut mismatch");
 return{value:new Q(b.ceiling-cut,b.denominator).toString(),decimal:new Q(b.ceiling-cut,b.denominator).number(),nodes:g.n,arcs:g.to.length/2,positiveFlows:flows.size};
}
return{build,maxflow,certificate,verify};

})();
