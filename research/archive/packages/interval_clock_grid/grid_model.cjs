"use strict";
// Complete physical path / two-credit DAG. No geometric reachability pruning.
// Grid units: time and position = 1/(2n); initial positions = 1/n.
// States are [time,position,minusCredit,plusCredit,minusVisited,plusVisited,centerVisited].
// Charge units have physical mass 1/(4n), after fair reflection of each path.

function buildGraph(n){
 if(!Number.isSafeInteger(n)||n<1)throw Error('n must be a positive integer');
 const N=16*n,R=2*n,C=4*n,states=[null,null],index=new Map(),edges=[],outgoing=[[],[]];
 function admissible(s){
  const [j,k,qm,qp,em,ep,c]=s,T=N-j;
  if(j<0||j>N||k< -R||k>R||(j+k)%2||qm<0||qp<0||qm>T||qp>T)return false;
  if(em&&qm||ep&&qp||k===-R&&!em||k===R&&!ep||k===0&&!c)return false;
  if(!c&&j>=C)return false;
  return true;
 }
 function node(s){if(!admissible(s))return null;const key=s.join(",");let id=index.get(key);if(id===undefined){id=states.length;index.set(key,id);states.push(s);outgoing.push([]);}return id;}
 function edge(u,v,kind,event=null){if(v===null)return;outgoing[u].push(edges.length);edges.push([u,v,kind,event]);}
 for(let k=-R;k<=R;k+=2)edge(0,node([0,k,0,0,+(k===-R),+(k===R),+(k===0)]),0);
 for(let u=2;u<states.length;u++){
  const [j,k,qm,qp,em,ep,c]=states[u];
  if(em&&ep){edge(u,1,4);continue;}
  if(!em)edge(u,node([j,k,qm+1,qp,em,ep,c]),1,[j,k]);
  if(!ep)edge(u,node([j,k,qm,qp+1,em,ep,c]),2,[j,-k]);
  if(j<N&&(em||qm>=1)&&(ep||qp>=1))for(const d of [-1,1]){
   const kk=k+d;if(kk< -R||kk>R)continue;
   const mm=qm-+(!em),pp=qp-+(!ep);
   if(kk===-R&&!em&&mm!==0||kk===R&&!ep&&pp!==0)continue;
   edge(u,node([j+1,kk,mm,pp,+(em||kk===-R),+(ep||kk===R),+(c||kk===0)]),3);
  }
 }
 const lev=[-1,5*N+1,...states.slice(2).map(s=>3*s[0]+s[2]+s[3])],order=states.map((_,i)=>i).sort((a,b)=>lev[a]-lev[b]);
 for(const [u,v] of edges)if(lev[v]<=lev[u])throw Error("cycle");
 const all=new Map();for(const e of edges)if(e[3]&&e[3][1])all.set(e[3].join(","),e[3]);
 const events=Array.from(all.values()).sort((a,b)=>a[0]-b[0]||a[1]-b[1]),eventIndex=new Map(events.map((z,i)=>[z.join(","),i]));
 const eventIds=edges.map(e=>e[3]&&e[3][1]?eventIndex.get(e[3].join(",")):-1);
 const base=edges.map(e=>e[3]?1+ +(e[3][1]>0):0),matches=[];
 for(let i=0;i<events.length;i++)if(events[i][1]>0)for(let j=0;j<events.length;j++)if(events[j][1]<0&&-events[j][1]>=events[i][1]+Math.abs(events[j][0]-events[i][0]))matches.push([i,j]);
 return {n,N,R,states,edges,outgoing,order,events,eventIds,base,matches};
}
function price(g,discount){
 const dist=new Array(g.states.length).fill(Infinity),choice=new Array(g.states.length).fill(-1);dist[1]=0;
 for(let oi=g.order.length-1;oi>=0;oi--){const u=g.order[oi];if(u===1)continue;for(const e of g.outgoing[u]){
  const v=g.edges[e][1],cost=g.base[e]-(g.eventIds[e]<0?0:discount[g.eventIds[e]]),z=cost+dist[v];
  if(z<dist[u]-1e-12){dist[u]=z;choice[u]=e;}
 }}
 if(!Number.isFinite(dist[0]))throw Error("no terminal path");
 const route=[];let u=0;while(u!==1){const e=choice[u];if(e<0)throw Error("broken route");route.push(e);u=g.edges[e][1];}
 return {value:dist[0],route,dist,choice};
}
function column(g,route){
 const counts=new Array(g.events.length).fill(0);let cost=0;
 for(const e of route){cost+=g.base[e];if(g.eventIds[e]>=0)counts[g.eventIds[e]]++;}
 return {route,cost,counts};
}
function decode(g,route){
 let u=0,start=null;const moves=[],minus=new Map(),plus=new Map();
 for(const e of route){
  const [from,to,kind]=g.edges[e];if(from!==u)throw Error("disconnected route");
  if(kind===0)start=g.states[to][1];
  else if(kind===1||kind===2){const a=kind===1?minus:plus,j=g.states[u][0];a.set(j,(a.get(j)||0)+1);}
  else if(kind===3)moves.push(g.states[to][1]-g.states[u][1]);
  u=to;
 }
 if(u!==1||start===null)throw Error("incomplete route");
 return {start_grid:start,moves,minus_charges:Array.from(minus),plus_charges:Array.from(plus)};
}

module.exports={buildGraph,price,column,decode};
