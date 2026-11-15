"use strict";
// Integer verification of a sparse, physically valid Qout closure witness.
// Edge completeness is unnecessary for an upper: every supplied edge must
// be a proved Qout inequality. A missing edge can only weaken the bound.
const {inspectPlans,fraction}=require("../interval_clock_grid/exact_certificate.cjs");
const {maximumFlow}=require("../interval_clock_grid/qout_primal_certificate.cjs");
function buildClosure(c){
 const n=c.n,W=BigInt(c.weight_denominator),R=2*n,C=4*n;
 if(!Number.isSafeInteger(n)||n<1||W<=0n||c.pair_law!=="fair_reflection"||c.center_deadline!==2||c.completion_horizon!==8||c.physical_step!=="1/"+R)throw Error("physical metadata");
 const stats=inspectPlans(n,c.paths,W),pressure=new Map();
 for(const [key,q] of stats.pressure){
  let [j,k]=key.split(",").map(Number);if(k===0)continue;
  const sign=k>0?1n:-1n;k=Math.abs(k);
  if(j>C){k-=j-C;j=C;}if(k<=0)continue;
  const point=j+","+k;pressure.set(point,(pressure.get(point)||0n)+sign*q);
 }
 const nodes=c.qout_nodes,index=new Map();
 if(!Array.isArray(nodes))throw Error("missing event nodes");
 for(let i=0;i<nodes.length;i++){
  const [j,k]=nodes[i];
  if(nodes[i].length!==2||!Number.isSafeInteger(j)||!Number.isSafeInteger(k)||j<0||j>C||k<1||k>R||(j+k)%2||index.has(j+","+k))throw Error("invalid event node");
  index.set(j+","+k,i);
 }
 const coeff=new Array(nodes.length).fill(0n);
 for(const [point,value] of pressure){if(value===0n)continue;const id=index.get(point);if(id===undefined)throw Error("missing charged event");coeff[id]+=value;}
 let positive=0n;for(const value of coeff)if(value>0n)positive+=value;
 const S=nodes.length,T=S+1,INF=positive+1n,arcs=[];
 for(let i=0;i<nodes.length;i++){if(coeff[i]>0n)arcs.push([S,i,coeff[i]]);else if(coeff[i]<0n)arcs.push([i,T,-coeff[i]]);}
 const seen=new Set();
 for(const edge of c.qout_order){
  if(edge.length!==2)throw Error("order edge arity");const [a,b]=edge;
  if(!Number.isSafeInteger(a)||!Number.isSafeInteger(b)||a<0||b<0||a>=nodes.length||b>=nodes.length||a===b||seen.has(a+","+b))throw Error("invalid order edge");
  seen.add(a+","+b);const [j,k]=nodes[a],[s,r]=nodes[b];
  const cone=r-k>=Math.abs(s-j);
  // Reach (min(C,j+R-k),R), then decrease endpoint time by stopping.
  const stopped=r===R&&s<=Math.min(C,j+R-k);
  if(!cone&&!stopped)throw Error("unjustified Qout edge");
  arcs.push([a,b,INF]);
 }
 return {n,W,stats,nodes,coeff,S,T,arcs,positive};
}
function verify(c){
 const g=buildClosure(c),balance=new Array(g.T+1).fill(0n),seen=new Set();
 for(const entry of c.closure_flow){
  if(entry.length!==2)throw Error("flow arity");const [i,text]=entry,f=BigInt(text);
  if(!Number.isSafeInteger(i)||i<0||i>=g.arcs.length||seen.has(i)||f<=0n||f>g.arcs[i][2])throw Error("invalid flow");
  seen.add(i);const [a,b]=g.arcs[i];balance[a]-=f;balance[b]+=f;
 }
 const flow=-balance[g.S];if(flow<0n||balance[g.T]!==flow||balance.slice(0,g.S).some(x=>x!==0n))throw Error("flow conservation");
 const side=new Set(c.closure_source_side);
 if(side.size!==c.closure_source_side.length||!side.has(g.S)||side.has(g.T))throw Error("cut terminals");
 for(const i of side)if(!Number.isSafeInteger(i)||i<0||i>g.T)throw Error("invalid cut node");
 let cut=0n;for(const [a,b,cap] of g.arcs)if(side.has(a)&&!side.has(b))cut+=cap;
 if(flow!==cut)throw Error("flow cut mismatch");
 const upper=fraction(g.stats.mass+g.positive-flow,4n*BigInt(g.n)*g.W);
 if(c.global_upper&&c.global_upper!==upper)throw Error("claimed upper mismatch");
 return {status:"PASS",scope:"Unrestricted physical Monster upper from individually checked Qout inequalities and integer flow/cut; no finite-bank lower claim",n:g.n,physical_calendar_plans:c.paths.length,closure_nodes:g.T+1,closure_arcs:g.arcs.length,exact_flow:String(flow),exact_cut:String(cut),global_upper:upper,endpoint_baseline:fraction(g.stats.mass,4n*BigInt(g.n)*g.W),closure_excess:fraction(g.positive-flow,4n*BigInt(g.n)*g.W)};
}
module.exports={buildClosure,verify};
if(require.main===module){
 const fs=require("node:fs"),zlib=require("node:zlib");
 function read(path){const b=fs.readFileSync(path);return JSON.parse(b[0]===31&&b[1]===139?zlib.gunzipSync(b):b);}
 try{
  if(process.argv[2]==="--solve"){
   const c=read(process.argv[3]),prefix=process.argv[4];if(!prefix)throw Error("--solve input output-prefix");
   const g=buildClosure(c),f=maximumFlow(g);c.closure_flow=f.entries;c.closure_source_side=f.source_side;
   c.global_upper=fraction(g.stats.mass+g.positive-f.flow,4n*BigInt(g.n)*g.W);
   const replay=verify(c);fs.writeFileSync(prefix+".sparse.json",JSON.stringify(c)+"\n");fs.writeFileSync(prefix+".replay.json",JSON.stringify(replay,null,2)+"\n");console.log(JSON.stringify(replay));
  }else console.log(JSON.stringify(verify(read(process.argv[2])),null,2));
 }catch(error){console.error(error.stack);process.exitCode=1;}
}
