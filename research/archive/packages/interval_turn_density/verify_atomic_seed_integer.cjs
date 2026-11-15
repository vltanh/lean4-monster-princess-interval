/* Exact replay audit. Core executed independently in V8; Node I/O wrapper unrun during executor outage. */
(function () {
"use strict";

function verifyIncumbent(E,c,seed){
 const {Physical,Rational,Integer,Cut,BigFlow,FaceOpt}=E,{Q}=Physical,z=new Q(0n),one=new Q(1n),two=new Q(2n);
 const key=raw=>{const a=raw.map(p=>p.map(q=>new Q(q))),out=[];for(const p of a){if(out.length&&p.every((q,j)=>q.cmp(out.at(-1)[j])===0))continue;while(out.length>1){const p0=out.at(-2),p1=out.at(-1);if(p0[0].cmp(p1[0])===0&&p1[0].cmp(p[0])===0||p0[1].cmp(p1[1])===0&&p1[1].cmp(p[1])===0)out.pop();else break;}out.push(p);}const s=JSON.stringify(out.map(p=>p.map(q=>q.toString()))),t=JSON.stringify(out.map(([u,v])=>[v.toString(),u.toString()]));return s<t?s:t;};
 const archived=new Map();for(const f of seed.families){const a=new Q(f.start);let p=f.kind===1?[[a,a.neg()],[two.sub(a),a.neg()],[two.sub(a),new Q(4n).sub(a)]]:[[a,a.neg()],[one,a.neg()],[one,new Q(3n)],[new Q(5n),new Q(3n)]];const k=key(p);archived.set(k,(archived.get(k)||0n)+BigInt(f.weight_numerator));}
 let total=0n,active=0;const supplied=new Map();
 for(const a of c.atoms){const w=BigInt(a.weight_numerator);if(w<0n)throw Error("negative weight");total+=w;const p=a.exact_light.map(x=>x.map(q=>new Q(q)));if(p[0][0].add(p[0][1]).cmp(z)!==0)throw Error("nonzero initial time");let left=false,right=false;
  for(let j=0;j<p.length;j++){const[u,v]=p[j],x=u.sub(v).div(two);if(u.add(v).cmp(z)<0||x.abs().cmp(one)>0)throw Error("illegal position");if(x.cmp(one)===0)right=true;if(x.cmp(one.neg())===0)left=true;if(j){const old=p[j-1];if(!((u.cmp(old[0])>0&&v.cmp(old[1])===0)||(v.cmp(old[1])>0&&u.cmp(old[0])===0)))throw Error("illegal unit leg");}}
  if(!left||!right)throw Error("route lacks endpoint sweep");if(w>0n){active++;const k=key(p);supplied.set(k,(supplied.get(k)||0n)+w);}
 }
 if(total!==BigInt(c.weight_denominator)||total!==BigInt(seed.weight_denominator)||supplied.size!==archived.size)throw Error("probability/source size");
 for(const[k,w]of archived)if(supplied.get(k)!==w)throw Error("incumbent differs from archived law");
 const model=new Rational.Model(c.atoms);
 if(JSON.stringify(model.v)!==JSON.stringify(c.vertices)||JSON.stringify(model.base)!==JSON.stringify(c.base_levels))throw Error("event geometry mismatch");
 const weights=c.atoms.map(a=>a.weight_numerator),verified=Integer.verifyIntegerFlow(Cut,Physical,BigFlow.BigFlow,model,weights,c.weight_denominator,c.flow_certificate);
 if(verified.exactValue!==c.expected_value)throw Error("response mismatch");
 const b=Integer.solveIntegerLaw(Cut,Physical,BigFlow.BigFlow,model,weights,c.weight_denominator,{buildOnly:true}),g=b.graph,fc=c.flow_certificate;
 if(fc.source!==b.source||fc.sink!==b.sink)throw Error("source/sink mismatch");
 const ids=new Set();for(const[id,vi]of fc.positiveFlows){if(!Number.isInteger(id)||!Number.isInteger(vi)||vi<0||vi>=fc.flowValues.length||ids.has(id))throw Error("bad/duplicate flow entry");ids.add(id);const f=BigInt(fc.flowValues[vi]);g.cap[2*id]-=f;g.cap[2*id+1]+=f;}
 function reachFrom(start,reverse){const seen=new Uint8Array(g.n),q=[start];seen[start]=1;for(let at=0;at<q.length;at++){const u=q[at];for(let e=g.head[u];e!==-1;e=g.next[e])if(g.cap[reverse?e^1:e]>0n&&!seen[g.to[e]]){seen[g.to[e]]=1;q.push(g.to[e]);}}return seen;}
 const reach=reachFrom(b.source,false),sink=reachFrom(b.sink,true),sourceSide=new Set(fc.sourceSide);if(sourceSide.size!==fc.sourceSide.length)throw Error("duplicate cut node");
 for(let i=0;i<g.n;i++)if(!!reach[i]!==sourceSide.has(i))throw Error("saved cut not exact residual reachable cut");
 const free=[],edges=[],forcedTrue=[],forcedFalse=[];for(let i=0;i<b.source;i++)if(!reach[i]&&!sink[i])free.push(i);const fs=new Set(free);
 for(const u of free)for(let e=g.head[u];e!==-1;e=g.next[e])if(g.cap[e]>0n&&fs.has(g.to[e]))edges.push([u,g.to[e]]);
 for(let i=0;i<model.N;i++){if(reach[i])forcedTrue.push(i);if(sink[i])forcedFalse.push(i);}
 const face=FaceOpt.compress(model,{face:{free,edges,forcedTrue,forcedFalse},value:new Q(c.expected_value).number()});
 if(face.count!==c.residual_face.count||JSON.stringify(face.nodeComp)!==JSON.stringify(c.residual_face.nodeComp)||JSON.stringify(face.edges)!==JSON.stringify(c.residual_face.edges))throw Error("residual SCC face mismatch");
 let labelsChecked=0;for(const labs of[c.minimum_labels,c.maximum_labels]){let value=z;for(let i=0;i<labs.length;i++)if(labs[i]<model.bounds[i][0]||labs[i]>model.bounds[i][1]||i&&labs[i]<labs[i-1])throw Error("illegal response labels");const row=model.rowExact(labs);for(let j=0;j<row.length;j++)if(BigInt(weights[j])>0n)value=value.add(row[j].mul(new Q(BigInt(weights[j]),BigInt(c.weight_denominator))));if(value.toString()!==c.expected_value)throw Error("exact response-row mismatch");labelsChecked++;}
 return{scope:"Independent replay for the archived 67-atom monster law; no saddle or exact game-value claim.",legalMonsterAtoms:c.atoms.length,positiveMassAtoms:active,archivedMassesMatched:archived.size,thresholdNodes:model.N,events:model.v.length,levels:model.base.length,...verified,sourceCutReconstructed:true,freeResidualNodes:free.length,residualSCCs:face.count,condensationEdges:face.edges.length,exactExtremalRows:labelsChecked};
}
const api={verifyIncumbent};
if(typeof module!=="undefined"&&module.exports){
 module.exports=api;
 if(require.main===module){
  const fs=require("node:fs"),path=require("node:path");
  const engine=require("./atomic_survival_v8.cjs");
  const cert=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"atomic_seed_integer_certificate.json"),"utf8"));
  const seed=JSON.parse(fs.readFileSync(process.argv[3]||path.join(__dirname,"../interval_refined_upper/strategy.json"),"utf8"));
  console.log(JSON.stringify(verifyIncumbent(engine,cert,seed),null,2));
 }
}
return api;
})()
