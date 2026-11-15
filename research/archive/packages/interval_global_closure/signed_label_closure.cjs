"use strict";
/* Generic signed unary optimization on nondecreasing ordered labels. */
function createSignedLabelClosure(E) {
 const Q=E.Physical.Q,Z=new Q(0),ONE=new Q(1);
 function gcd(a,b){while(b){let r=a%b;a=b;b=r;}return a;}
 function maximize(input){
  const {labels,rowBounds,unaryValues}=input,mode=input.mode||"exact",R=rowBounds.length,L=labels.length;
  if(R!==unaryValues.length||!L)throw Error("shape mismatch");
  if(mode!=="exact"&&mode!=="float")throw Error("unknown arithmetic mode");
  const original=rowBounds.map(v=>v.slice()),bounds=original.map(v=>v.slice()),table=unaryValues.map((row,i)=>{
   let[lo,hi]=original[i];if(!Number.isInteger(lo)||!Number.isInteger(hi)||lo<0||lo>hi||hi>=L)throw Error("invalid row bounds");
   if(row.length===L)return row.map(x=>new Q(x));
   if(row.length===hi-lo+1){let a=Array(L).fill(null);for(let k=lo;k<=hi;k++)a[k]=new Q(row[k-lo]);return a;}
   throw Error("unary row length");
  });
  for(let i=1;i<R;i++)bounds[i][0]=Math.max(bounds[i][0],bounds[i-1][0]);
  for(let i=R-2;i>=0;i--)bounds[i][1]=Math.min(bounds[i][1],bounds[i+1][1]);
  for(let i=0;i<R;i++)if(bounds[i][0]>bounds[i][1])return{status:"infeasible",reason:"ordered bounds conflict",bounds};
  const offset=[],weights=[];let N=0,constant=Z;
  for(let i=0;i<R;i++){const[lo,hi]=bounds[i];offset.push(N);constant=constant.add(table[i][lo]);for(let k=lo+1;k<=hi;k++){weights.push(table[i][k].sub(table[i][k-1]));N++;}}
  const node=(i,k)=>offset[i]+k-bounds[i][0]-1,s=N,t=N+1,edges=[];
  for(let i=0;i<R;i++){
   const[lo,hi]=bounds[i];for(let k=lo+2;k<=hi;k++)edges.push([node(i,k),node(i,k-1)]);
   if(i+1<R)for(let k=lo+1;k<=hi;k++)if(k>bounds[i+1][0])edges.push([node(i,k),node(i+1,k)]);
  }
  let denominator=1n,graph,flow,positive=Z,inf;
  if(mode==="exact"){
   for(const q of weights)denominator=denominator/gcd(denominator,q.d)*q.d;
   const iw=weights.map(q=>q.n*(denominator/q.d));let abs=0n,pos=0n;for(const z of iw){abs+=z<0n?-z:z;if(z>0n)pos+=z;}inf=abs+1n;
   graph=new E.BigFlow.BigFlow(N+2);
   for(let i=0;i<N;i++)if(iw[i]>0n)graph.add(s,i,iw[i]);else if(iw[i]<0n)graph.add(i,t,-iw[i]);
   for(const[a,b]of edges)graph.add(a,b,inf);
   const capacities=graph.cap.slice();flow=graph.solve(s,t,inf);positive=new Q(pos,denominator);
   let cut=0n;for(let i=0;i<graph.n;i++)if(flow.reach[i])for(let e=graph.head[i];e!==-1;e=graph.next[e])if(!flow.reach[graph.to[e]])cut+=capacities[e];
   if(cut!==flow.flow)throw Error("integer cut-capacity replay failed");
   graph.initialCapacities=capacities;
  }else{
   const tol=input.tolerance??1e-12,ws=weights.map(q=>q.number());let abs=0,pos=0;for(const z of ws){abs+=Math.abs(z);if(z>0)pos+=z;}inf=1+abs;
   graph=new E.Cut.Flow(N+2,tol);
   for(let i=0;i<N;i++)if(ws[i]>0)graph.add(s,i,ws[i]);else if(ws[i]<0)graph.add(i,t,-ws[i]);
   for(const[a,b]of edges)graph.add(a,b,inf);
   flow=graph.solve(s,t,inf);positive=pos;
  }
  function read(mask,maximal=false){return bounds.map(([lo,hi],i)=>{let k=lo;while(k<hi&&(maximal?!mask[node(i,k+1)]:mask[node(i,k+1)]))k++;return k;});}
  const minimum=read(flow.reach),maximum=read(flow.sink,true);
  function score(xs){let q=Z;for(let i=0;i<R;i++){if(xs[i]<bounds[i][0]||xs[i]>bounds[i][1]||(i&&xs[i]<xs[i-1]))throw Error("illegal returned labels");q=q.add(table[i][xs[i]]);}return q;}
  const vmin=score(minimum),vmax=score(maximum);
  const value=mode==="exact"?constant.add(positive).sub(new Q(flow.flow,denominator)):constant.number()+positive-flow.flow;
  if(mode==="exact"&&(vmin.cmp(value)||vmax.cmp(value)))throw Error("exact witness score mismatch");
  return {status:"optimal",arithmetic:mode,value:mode==="exact"?value.toString():value,decimal:mode==="exact"?value.number():value,
   minimum_labels:minimum,maximum_labels:maximum,minimum_score:vmin.toString(),maximum_score:vmax.toString(),
   witness_error:mode==="exact"?0:Math.max(Math.abs(vmin.number()-value),Math.abs(vmax.number()-value)),
   bounds,threshold_nodes:N,implications:edges.length,graph_arcs:graph.to.length/2,
   ...(mode==="exact"?{denominator:String(denominator),flow:String(flow.flow),infinity:String(inf)}:{}),
   ...(input.retainGraph?{graph,flowResult:flow,source:s,sink:t,offset}:{} )};
 }
 return{maximize};
}
module.exports={createSignedLabelClosure};
