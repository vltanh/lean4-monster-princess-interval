"use strict";
// Independent exact pricing on the full two-credit planning DAG.
const {inspectUniformPrimal,uniformGeometry}=require("./uniform_certificate.cjs");
const {fraction}=require("./exact_certificate.cjs");
function buildPlanningGraph(n){
 const N=16*n,R=2*n,C=4*n,states=[null,null],index=new Map(),edges=[],outgoing=[[],[]];
 function node(s){
  const [j,k,qm,qp,em,ep,c,dir]=s,T=N-j;
  if(j<0||j>N||Math.abs(k)>R||(j+k)%2||qm<0||qp<0||qm>T||qp>T)return null;
  if(em&&qm||ep&&qp||k===-R&&!em||k===R&&!ep||k===0&&!c||!c&&j>=C)return null;
  const key=s.join(",");let id=index.get(key);if(id===undefined){id=states.length;index.set(key,id);states.push(s);outgoing.push([]);}return id;
 }
 function edge(u,v,event=null){if(v===null)return;outgoing[u].push(edges.length);edges.push([u,v,event]);}
 for(let k=-R;k<=R;k+=2)edge(0,node([0,k,0,0,+(k===-R),+(k===R),+(k===0),0]));
 for(let u=2;u<states.length;u++){
  const [j,k,qm,qp,em,ep,c,dir]=states[u];
  if(em&&ep){edge(u,1);continue;}
  if(dir===0){
   if(!em)edge(u,node([j,k,qm+1,qp,em,ep,c,0]),[2*j,2*k]);
   if(!ep)edge(u,node([j,k,qm,qp+1,em,ep,c,0]),[2*j,-2*k]);
   if(j<N)for(const d of [-1,1])if(Math.abs(k+d)<=R)edge(u,node([j,k,qm,qp,em,ep,c,d]));
  }else{
   if(!em)edge(u,node([j,k,qm+1,qp,em,ep,c,dir]),[2*j+1,2*k+dir]);
   if(!ep)edge(u,node([j,k,qm,qp+1,em,ep,c,dir]),[2*j+1,-2*k-dir]);
   if(j<N&&(em||qm>=1)&&(ep||qp>=1)){
    const kk=k+dir,mm=qm-+(!em),pp=qp-+(!ep);
    if(!(kk===-R&&!em&&mm!==0||kk===R&&!ep&&pp!==0))
     edge(u,node([j+1,kk,mm,pp,+(em||kk===-R),+(ep||kk===R),+(c||kk===0),0]));
   }
  }
 }
 const level=[-1,5*N+1,...states.slice(2).map(s=>4*s[0]+s[2]+s[3]+ +(s[7]!==0))];
 for(const [u,v] of edges)if(level[u]>=level[v])throw Error("planning cycle");
 const order=states.map((_,i)=>i).sort((a,b)=>level[a]-level[b]);
 return {states,edges,outgoing,order};
}
function verifyPlanning(c){
 const {n,W,primal}=inspectUniformPrimal(c),D=BigInt(c.discount_denominator),geometry=uniformGeometry(n),d=new Map();
 if(D<=0n)throw Error("discount denominator");
 for(const [t,x,a] of c.discounts){const z=BigInt(a),key=t+","+x;if(z<0n||d.has(key))throw Error("invalid discount");d.set(key,z);}
 if(d.size!==geometry.events.length)throw Error("incomplete type geometry");
 for(const z of geometry.events)if(!d.has(z.join(",")))throw Error("missing pressure type");
 for(const [p,q] of geometry.matches)if(d.get(geometry.events[p].join(","))+d.get(geometry.events[q].join(","))<D)throw Error("covering inequality");
 const g=buildPlanningGraph(n),tail=new Array(g.states.length).fill(null);tail[1]=0n;
 for(let oi=g.order.length-1;oi>=0;oi--){
  const u=g.order[oi];if(u===1)continue;
  for(const ei of g.outgoing[u]){
   const [,v,event]=g.edges[ei];if(tail[v]===null)continue;
   const cost=event?BigInt(1+ +(event[1]>0))*D-(event[1]===0?0n:d.get(event.join(","))):0n;
   const value=cost+tail[v];if(tail[u]===null||value<tail[u])tail[u]=value;
  }
 }
 if(tail[0]===null||primal*D!==tail[0]*W)throw Error("nonzero full planning primal-dual gap");
 const value=fraction(primal,4n*BigInt(n)*W);
 if(c.exact_value&&c.exact_value!==value)throw Error("claimed value");
 return {status:"PASS",model:"full_vertex_uniform_planning_DAG",n,nodes:g.states.length,arcs:g.edges.length,
  exact_scaled_primal:fraction(primal,W),exact_scaled_dual:fraction(tail[0],D),exact_value:value};
}
module.exports={buildPlanningGraph,verifyPlanning};
if(require.main===module){
 const fs=require("node:fs"),path=require("node:path"),file=process.argv[2]||path.join(__dirname,"uniform_n1_certificate.json");
 try{process.stdout.write(JSON.stringify(verifyPlanning(JSON.parse(fs.readFileSync(file))),null,2)+"\n");}
 catch(error){process.stderr.write(error.stack+"\n");process.exitCode=1;}
}
