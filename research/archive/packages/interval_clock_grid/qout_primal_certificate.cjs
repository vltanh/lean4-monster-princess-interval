"use strict";
// Physical Monster upper certificate via the law-specific Princess normalization.
// The closure graph includes transport, sticky endpoint order and outward2 substitution.
const {inspectPlans,fraction}=require("./exact_certificate.cjs");
function buildClosure(c){
 const n=c.n,W=BigInt(c.weight_denominator),R=2*n,C=4*n;
 if(!Number.isSafeInteger(n)||n<1||W<=0n||c.pair_law!=="fair_reflection"||c.center_deadline!==2||c.completion_horizon!==8||c.physical_step!=="1/"+(2*n))throw Error("physical closure metadata");
 const stats=inspectPlans(n,c.paths,W),nodes=[],index=new Map();
 for(let j=0;j<=C;j++)for(let k=1;k<=R;k++)if((j+k)%2===0){index.set(j+","+k,nodes.length);nodes.push([j,k]);}
 const coeff=new Array(nodes.length).fill(0n);
 for(const [key,q] of stats.pressure){
  let [j,k]=key.split(",").map(Number);if(k===0)continue;
  const sign=k>0?1n:-1n;k=Math.abs(k);
  if(j>C){k-=j-C;j=C;}if(k<=0)continue;
  const id=index.get(j+","+k);if(id===undefined)throw Error("invalid outward footpoint");coeff[id]+=sign*q;
 }
 let positive=0n;for(const a of coeff)if(a>0n)positive+=a;
 const S=nodes.length,T=S+1,INF=positive+1n,arcs=[];
 for(let i=0;i<nodes.length;i++){if(coeff[i]>0n)arcs.push([S,i,coeff[i]]);else if(coeff[i]<0n)arcs.push([i,T,-coeff[i]]);}
 for(let i=0;i<nodes.length;i++){
  const [j,k]=nodes[i];
  if(k<R)for(const step of [-1,1])if(j+step>=0&&j+step<=C)arcs.push([i,index.get((j+step)+","+(k+1)),INF]);
 }
 for(let j=0;j<C;j+=2)arcs.push([index.get((j+2)+","+R),index.get(j+","+R),INF]);
 return {n,W,stats,nodes,coeff,S,T,arcs,positive};
}
function maximumFlow(g){
 const size=g.nodes.length+2,adj=Array.from({length:size},()=>[]),forward=[];
 for(const [u,v,cap] of g.arcs){const a={v,cap,rev:adj[v].length},b={v:u,cap:0n,rev:adj[u].length};adj[u].push(a);adj[v].push(b);forward.push(a);}
 let flow=0n;
 for(;;){
  const level=new Int32Array(size).fill(-1),queue=[g.S];level[g.S]=0;
  for(let h=0;h<queue.length;h++){const u=queue[h];for(const e of adj[u])if(e.cap>0n&&level[e.v]<0){level[e.v]=level[u]+1;queue.push(e.v);}}
  if(level[g.T]<0)break;
  const next=new Int32Array(size);
  function dfs(u,f){
   if(u===g.T)return f;
   for(;next[u]<adj[u].length;next[u]++){
    const e=adj[u][next[u]];if(e.cap>0n&&level[e.v]===level[u]+1){const a=dfs(e.v,f<e.cap?f:e.cap);if(a>0n){e.cap-=a;adj[e.v][e.rev].cap+=a;return a;}}
   }
   return 0n;
  }
  for(;;){const a=dfs(g.S,g.positive+1n);if(a===0n)break;flow+=a;}
 }
 const reached=new Uint8Array(size),queue=[g.S];reached[g.S]=1;
 for(let h=0;h<queue.length;h++)for(const e of adj[queue[h]])if(e.cap>0n&&!reached[e.v]){reached[e.v]=1;queue.push(e.v);}
 return {flow,entries:forward.map((e,i)=>[i,String(g.arcs[i][2]-e.cap)]).filter(a=>a[1]!=="0"),source_side:queue.sort((a,b)=>a-b)};
}
function verifyClosure(c){
 const g=buildClosure(c),balance=new Array(g.nodes.length+2).fill(0n),used=new Set();
 for(const [i,a] of c.closure_flow){
  const f=BigInt(a);if(!Number.isSafeInteger(i)||i<0||i>=g.arcs.length||used.has(i)||f<=0n||f>g.arcs[i][2])throw Error("invalid closure flow");used.add(i);
  const [u,v]=g.arcs[i];balance[u]-=f;balance[v]+=f;
 }
 const flow=-balance[g.S];if(flow<0n||balance[g.T]!==flow)throw Error("flow terminals");
 for(let i=0;i<g.nodes.length;i++)if(balance[i]!==0n)throw Error("flow conservation");
 const side=new Set(c.closure_source_side);
 if(side.size!==c.closure_source_side.length||!side.has(g.S)||side.has(g.T))throw Error("cut terminals");
 for(const i of side)if(!Number.isSafeInteger(i)||i<0||i>g.T)throw Error("cut node");
 let cut=0n;for(const [u,v,cap] of g.arcs)if(side.has(u)&&!side.has(v))cut+=cap;
 if(flow!==cut)throw Error("nonzero exact closure flow/cut gap");
 const units=g.stats.mass+g.positive-flow,upper=fraction(units,4n*BigInt(g.n)*g.W);
 if(c.global_upper&&c.global_upper!==upper)throw Error("claimed upper mismatch");
 const unique=new Set(c.paths.map(p=>JSON.stringify([p.start_grid,p.moves])));
 return {status:"PASS",scope:"global physical Monster upper via centered-law Princess normalization and exact Qout closure",n:g.n,
  physical_calendar_plans:c.paths.length,distinct_physical_pairs:unique.size,closure_nodes:g.nodes.length+2,closure_arcs:g.arcs.length,
  positive_flow_entries:c.closure_flow.length,exact_flow:String(flow),exact_cut:String(cut),global_upper:upper,
  endpoint_baseline:fraction(g.stats.mass,4n*BigInt(g.n)*g.W),closure_excess:fraction(g.positive-flow,4n*BigInt(g.n)*g.W)};
}
function fromCheckpoint(checkpoint,denominator=1000000000000n){
 if(checkpoint.columns.length!==checkpoint.weights.length)throw Error("checkpoint support size");
 const positive=checkpoint.weights.map((w,i)=>({w:Math.max(0,w),i})).filter(a=>a.w>0),total=positive.reduce((s,a)=>s+a.w,0);
 if(!(total>0)||denominator>BigInt(Number.MAX_SAFE_INTEGER))throw Error("rounding input");
 const rounded=positive.map(a=>{const x=a.w/total*Number(denominator),q=Math.floor(x);return {...a,q:BigInt(q),fraction:x-q};});
 let remainder=denominator-rounded.reduce((s,a)=>s+a.q,0n);
 rounded.sort((a,b)=>b.fraction-a.fraction||a.i-b.i);
 if(remainder<0n||remainder>BigInt(rounded.length))throw Error("rounding remainder");
 for(let i=0;i<Number(remainder);i++)rounded[i].q++;
 const paths=rounded.filter(a=>a.q>0n).sort((a,b)=>a.i-b.i).map(a=>({weight_numerator:String(a.q),...checkpoint.columns[a.i].plan}));
 const n=checkpoint.n,c={scope:"Exact physical Monster upper. Princess normalization to sticky/outward2 is used for this fixed centered law; this is not an unrestricted-pressure matching witness.",
  n,pair_law:"fair_reflection",center_deadline:2,completion_horizon:8,physical_step:"1/"+(2*n),weight_denominator:String(denominator),paths};
 const g=buildClosure(c),f=maximumFlow(g);c.closure_flow=f.entries;c.closure_source_side=f.source_side;
 c.global_upper=fraction(g.stats.mass+g.positive-f.flow,4n*BigInt(n)*denominator);
 return {certificate:c,replay:verifyClosure(c)};
}
module.exports={buildClosure,maximumFlow,verifyClosure,fromCheckpoint};
if(require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto"),zlib=require("node:zlib");
 function parse(bytes){return JSON.parse(bytes[0]===31&&bytes[1]===139?zlib.gunzipSync(bytes):bytes);}
 try{
  if(process.argv[2]==="--make"){
   const input=process.argv[3],prefix=process.argv[4];if(!input||!prefix)throw Error("--make checkpoint.json output_prefix");
   const bytes=fs.readFileSync(input),out=fromCheckpoint(parse(bytes));out.certificate.discovery_checkpoint_sha256=crypto.createHash("sha256").update(bytes).digest("hex");
   fs.writeFileSync(prefix+".physical.json",JSON.stringify(out.certificate,null,2)+"\n");fs.writeFileSync(prefix+".replay.json",JSON.stringify(out.replay,null,2)+"\n");console.log(JSON.stringify(out.replay,null,2));
  }else console.log(JSON.stringify(verifyClosure(parse(fs.readFileSync(process.argv[2]))),null,2));
 }catch(error){console.error(error.stack);process.exitCode=1;}
}
