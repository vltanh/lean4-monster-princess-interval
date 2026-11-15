"use strict";
// Replace only the discovery optimizer. The original sparse physical,
// geometric-edge, and BigInt flow/cut verifier remains mandatory afterward.
const cp=require("node:child_process");
const LIMIT=(1n<<63n)-1n;

function verifyNetwork(g,f){
 const N=g.nodes.length+2;
 if(f.graph_nodes!==N||f.graph_arcs!==g.arcs.length)throw Error("native graph size mismatch");
 const flow=BigInt(f.flow),balance=new Array(N).fill(0n),used=new Set();
 if(flow<0n||flow>g.positive)throw Error("native flow bound");
 for(const entry of f.entries){
  if(!Array.isArray(entry)||entry.length!==2)throw Error("native flow entry shape");
  const [i,text]=entry,x=BigInt(text);
  if(!Number.isSafeInteger(i)||i<0||i>=g.arcs.length||used.has(i)||x<=0n||x>g.arcs[i][2])throw Error("native capacity violation");
  used.add(i);const [a,b]=g.arcs[i];balance[a]-=x;balance[b]+=x;
 }
 for(let i=0;i<N;i++)if(balance[i]!== (i===g.S?-flow:i===g.T?flow:0n))throw Error("native flow conservation");
 const side=new Set(f.source_side);
 if(side.size!==f.source_side.length||!side.has(g.S)||side.has(g.T))throw Error("native cut terminals");
 for(const i of side)if(!Number.isSafeInteger(i)||i<0||i>=N)throw Error("native cut node");
 let cut=0n;for(const [a,b,cap] of g.arcs)if(side.has(a)&&!side.has(b))cut+=cap;
 if(cut!==flow)throw Error("native flow/cut mismatch");
 return {flow,entries:f.entries,source_side:f.source_side};
}

function nativeMaximumFlow(g,binary=process.env.PRINCESS_MONSTER_FLOW_BINARY){
 if(!binary)throw Error("missing PRINCESS_MONSTER_FLOW_BINARY");
 const N=g.nodes.length+2,M=g.arcs.length;
 if(!Number.isSafeInteger(N)||N<2||N>5000000||!Number.isSafeInteger(M)||M>50000000||g.positive<0n||g.positive>=LIMIT)throw Error("native graph or capacity bound");
 let source=0n;
 const lines=[`PMFLOW1 ${N} ${M} ${g.S} ${g.T} ${g.positive}`];
 for(const edge of g.arcs){
  if(edge.length!==3)throw Error("native edge arity");
  const [a,b,cap]=edge;
  if(!Number.isSafeInteger(a)||!Number.isSafeInteger(b)||a<0||a>=N||b<0||b>=N||a===b||typeof cap!=="bigint"||cap<0n||cap>LIMIT)throw Error("native edge or capacity overflow");
  if(a===g.S)source+=cap;
  lines.push(`${a} ${b} ${cap}`);
 }
 if(source!==g.positive)throw Error("native source capacity mismatch");
 const result=cp.spawnSync(binary,[],{input:lines.join("\n")+"\n",encoding:"utf8",maxBuffer:512*1024*1024});
 if(result.error||result.status!==0)throw Error("native optimizer failed: "+(result.error||result.stderr));
 return verifyNetwork(g,JSON.parse(result.stdout));
}

module.exports={nativeMaximumFlow,verifyNetwork};
if(require.main===module){
 const optimizer=require("../interval_clock_grid/qout_primal_certificate.cjs");
 optimizer.maximumFlow=nativeMaximumFlow;
 require("../interval_mixture_cut/closure_server.cjs");
}
