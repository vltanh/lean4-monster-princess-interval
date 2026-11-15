"use strict";
// Exact graph and flow proposal for rebuild_projected_upper.py.
// Its independent Python physical replay remains mandatory. The formal
// row/cut agreement below is not an actual finite-width Princess witness.
const fs=require('node:fs');
const E=require('../interval_turn_density/atomic_survival_v8.cjs');
const P=require('../interval_turn_density/projected_cut.cjs');
const native=require('../interval_integer_flow/native_server.cjs');
const Q=E.Physical.Q;
function gcd(a,b){while(b){const r=a%b;a=b;b=r;}return a;}
function solve(atoms,denominator,binary){
 if(BigInt(denominator)<=0n||atoms.some(a=>BigInt(a.weight_numerator)<0n))throw Error('invalid probability law');
 const started=Date.now(),model=new E.Rational.Model(atoms),p=P.project(model);
 let scale=1n;for(const q of model.vQ.concat(model.baseQ))scale=scale/gcd(scale,q.d)*q.d;
 const rw=new Array(p.defs.length).fill(0n);let mass=0n;
 for(let j=0;j<atoms.length;j++){
  const w=BigInt(atoms[j].weight_numerator);mass+=w;model.compile(j);
  for(const[id,c]of model.lastExactUnits){if(scale%c.d)throw Error('denominator');rw[id]+=w*c.n*(scale/c.d);}
 }
 if(mass!==BigInt(denominator))throw Error('mass');
 const lin=new Array(p.N).fill(0n),hard=p.threshold_hard.slice();let constant=0n;
 for(let id=0;id<rw.length;id++){
  const w=rw[id];if(!w)continue;const d=p.defs[id];
  if(!d.bits.length){constant+=w;continue;}
  if(d.bits.length===1){lin[d.bits[0]]+=d.pos?w:-w;if(!d.pos)constant+=w;}
  else{const a=lin.length;lin.push(d.pos?w:-w);if(!d.pos)constant+=w;for(const b of d.bits)hard.push(d.pos?[a,b]:[b,a]);}
 }
 const S=lin.length,T=S+1,arcs=[];let positive=0n;
 const inf=1n+lin.reduce((s,x)=>s+(x<0n?-x:x),0n);
 for(let i=0;i<lin.length;i++)if(lin[i]>0n){arcs.push([S,i,lin[i]]);positive+=lin[i];}else if(lin[i]<0n)arcs.push([i,T,-lin[i]]);
 for(const[a,b]of hard)arcs.push([a,b,inf]);
 const g={nodes:new Array(lin.length),S,T,arcs,positive};
 console.error(JSON.stringify({stage:'graph',pairs:atoms.length,nodes:T+1,arcs:arcs.length,scale:String(scale),seconds:(Date.now()-started)/1000}));
 const flow=native.nativeMaximumFlow(g,binary),reach=new Uint8Array(T+1);for(const i of flow.source_side)reach[i]=1;
 const labels=P.labelsFromProjection(p,model,reach),row=model.rowExact(labels);
 let direct=new Q(0n);for(let j=0;j<atoms.length;j++)direct=direct.add(row[j].mul(new Q(BigInt(atoms[j].weight_numerator),BigInt(denominator))));
 const exact=new Q(constant+positive-flow.flow,4n*scale*BigInt(denominator));if(exact.cmp(direct))throw Error('exact physical row/cut mismatch');
 return {format:'one-turn-projected-upper-v1',exact_value:String(exact),value:exact.number(),weights_denominator:String(denominator),atoms,
  projection:{N:p.N,threshold_hard:p.threshold_hard,projection:{old_nodes:p.projection.old_nodes}},
  graph:{nodes:T+1,arcs:arcs.map(([a,b,c])=>[a,b,String(c)]),source:S,sink:T,constant:String(constant),positive:String(positive),scale:String(scale)},
  flow:{value:String(flow.flow),entries:flow.entries,source_side:flow.source_side},seconds:(Date.now()-started)/1000};
}
module.exports={solve};
if(require.main===module){
 const d=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
 const out=solve(d.atoms,d.weights_denominator||d.weight_denominator,process.argv[4]||process.env.PRINCESS_MONSTER_FLOW_BINARY);
 fs.writeFileSync(process.argv[3],JSON.stringify(out));
 console.log(JSON.stringify({exact_value:out.exact_value,value:out.value,pairs:out.atoms.length,graph_nodes:out.graph.nodes,graph_arcs:out.graph.arcs.length,seconds:out.seconds}));
}
