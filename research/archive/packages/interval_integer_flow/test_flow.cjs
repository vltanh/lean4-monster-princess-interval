"use strict";
const assert=require("node:assert/strict"),fs=require("node:fs"),zlib=require("node:zlib"),cp=require("node:child_process"),path=require("node:path");
const {maximumFlow}=require("../interval_clock_grid/qout_primal_certificate.cjs");
const sparse=require("../interval_sparse_upper/sparse_certificate.cjs");
const {nativeMaximumFlow,verifyNetwork}=require("./native_server.cjs");
const binary=process.argv[2];if(!binary)throw Error("pass native binary path");
let state=314159;
function next(){state=(Math.imul(state,1664525)+1013904223)>>>0;return state;}
function graph(N,arcs){const S=N-2,T=N-1;return {nodes:Array(N-2).fill(null),S,T,arcs,positive:arcs.filter(a=>a[0]===S).reduce((s,a)=>s+a[2],0n)};}
let randomChecks=0;
for(let trial=0;trial<100;trial++){
 const N=2+next()%12,arcs=[];
 for(let k=0;k<3*N;k++){
  const a=next()%N,b=next()%N;if(a===b)continue;
  const cap=BigInt(next()%1000)*(trial%3===0?10000000000000n:1n);
  arcs.push([a,b,cap]);
 }
 const g=graph(N,arcs),actual=nativeMaximumFlow(g,binary),expected=maximumFlow(g);
 assert.equal(actual.flow,expected.flow);
 randomChecks++;
}
const large=graph(4,[[2,0,1n<<60n],[0,1,(1n<<60n)-17n],[1,3,1n<<60n]]);
assert.equal(nativeMaximumFlow(large,binary).flow,(1n<<60n)-17n);
const N=20000,chain=[];for(let i=0;i<N-1;i++)chain.push([i===0?N-2:i-1,i===N-2?N-1:i,999999999999999n]);
assert.equal(nativeMaximumFlow(graph(N,chain),binary).flow,999999999999999n);
let rejected=0;
for(const input of ["PMFLOW1 2 1 0 1 1\n", "PMFLOW1 2 0 0 1 0\n0 1 1\n", "PMFLOW1 2 1 0 1 1\n0 1 -1\n", "PMFLOW1 2 1 0 1 9223372036854775808\n0 1 1\n"]){
 const p=cp.spawnSync(binary,[],{input,encoding:"utf8"});assert.notEqual(p.status,0);rejected++;
}
assert.throws(()=>nativeMaximumFlow(graph(2,[[0,1,1n<<63n]]),binary));rejected++;
const f=nativeMaximumFlow(large,binary);
assert.throws(()=>verifyNetwork(large,{...f,graph_nodes:4,graph_arcs:4}));rejected++;
assert.throws(()=>verifyNetwork(large,{...f,graph_nodes:4,graph_arcs:3,flow:String(f.flow-1n)}));rejected++;
const seed=path.join(__dirname,"../interval_fixed_marginal/seed_plain_n128.sparse.json.gz");
const c=JSON.parse(zlib.gunzipSync(fs.readFileSync(seed))),g=sparse.buildClosure(c);
const began=Date.now(),native=nativeMaximumFlow(g,binary);
c.closure_flow=native.entries;c.closure_source_side=native.source_side;
const replay=sparse.verify(c);assert.equal(replay.global_upper,"729770894042503/512000000000000");
const corrupted=JSON.parse(JSON.stringify(c));corrupted.closure_flow[0][1]=String(BigInt(corrupted.closure_flow[0][1])+1n);
assert.throws(()=>sparse.verify(corrupted));rejected++;
console.log(JSON.stringify({status:"PASS",random_integer_graphs:randomChecks,capacity_above_2_to_53:true,iterative_long_chain_nodes:N,
 rejected_bad_inputs_or_witnesses:rejected,retained_physical_seed_replay:replay,native_seed_seconds:(Date.now()-began)/1000}));
