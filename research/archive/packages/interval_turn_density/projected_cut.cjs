"use strict";
const E=require('./atomic_survival_v8.cjs');
function project(full){
  const used=Array.from(new Set(full.defs.flatMap(d=>d.bits))).sort((a,b)=>a-b),ids=new Map(used.map((x,i)=>[x,i]));
  const rows=full.bounds.map(([lo,hi],i)=>{
    const row=[];for(let k=lo+1;k<=hi;k++){const id=ids.get(full.offset[i]+k-lo-1);if(id!==undefined)row.push([k,id]);}return row;
  }),lastRow=new Int32Array(full.L).fill(-1),lastNode=new Int32Array(full.L).fill(-1),edges=[];
  for(let i=0;i<rows.length;i++)for(let j=rows[i].length-1;j>=0;j--){
    const[k,n]=rows[i][j];let record=-1;
    for(let l=k;l<full.L;l++)if(lastRow[l]>record){edges.push([lastNode[l],n]);record=lastRow[l];if(record===i)break;}
    lastRow[k]=i;lastNode[k]=n;
  }
  return{N:used.length,defs:full.defs.map(d=>({pos:d.pos,bits:d.bits.map(b=>ids.get(b))})),units:full.units,
         threshold_hard:edges,projection:{original_N:full.N,old_nodes:used,row_thresholds:rows}};
}
function labelsFromProjection(p,full,bits,maximum=false){
  const rows=p.projection.row_thresholds,labels=[];let prev=0;
  if(maximum){
    let next=full.bounds.at(-1)[1];
    for(let i=rows.length-1;i>=0;i--){
      let k=Math.min(next,full.bounds[i][1]);
      for(const[t,n]of rows[i])if(!bits[n])k=Math.min(k,t-1);
      if(k<full.bounds[i][0])throw Error('maximal projection face is below physical bound');
      for(const[t,n]of rows[i])if(Boolean(bits[n])!==(k>=t))throw Error('maximal projection face fails a priced threshold');
      labels[i]=k;next=k;
    }
    return labels;
  }
  for(let i=0;i<rows.length;i++){
    let k=Math.max(prev,full.bounds[i][0]);
    for(const[t,n]of rows[i])if(bits[n])k=Math.max(k,t);
    if(k>full.bounds[i][1])throw Error('projected face exceeds a physical bound');
    for(const[t,n]of rows[i])if(Boolean(bits[n])!==(k>=t))throw Error('projected face fails a priced threshold');
    labels.push(k);prev=k;
  }
  return labels;
}
function solve(p,weights,full,tol=2e-13){
  const rw=new Float64Array(p.defs.length);
  for(let j=0;j<weights.length;j++)if(weights[j]>0)for(const[r,c]of p.units[j])rw[r]+=weights[j]*c;
  const lin=new Array(p.N).fill(0),hard=[];let constant=0;
  for(let r=0;r<rw.length;r++){
    const w=rw[r];if(!w)continue;const d=p.defs[r];
    if(!d.bits.length){constant+=w;continue;}
    if(d.bits.length===1){lin[d.bits[0]]+=d.pos?w:-w;if(!d.pos)constant+=w;}
    else{const a=lin.length;lin.push(d.pos?w:-w);if(!d.pos)constant+=w;
      for(const b of d.bits)hard.push(d.pos?[a,b]:[b,a]);}
  }
  const s=lin.length,t=s+1,inf=1+lin.reduce((s,x)=>s+Math.abs(x),0),g=new E.Cut.Flow(t+1,tol);let ceiling=constant;
  for(let i=0;i<lin.length;i++)if(lin[i]>=0){g.add(s,i,lin[i]);ceiling+=lin[i];}else g.add(i,t,-lin[i]);
  for(const[u,v]of hard)g.add(u,v,inf);
  for(const[u,v]of p.threshold_hard)g.add(u,v,inf);
  const flow=g.solve(s,t,inf),labels=labelsFromProjection(p,full,flow.reach),
        maxlabels=labelsFromProjection(p,full,Array.from(flow.sink,x=>!x),true);
  const row=full.row(labels),rowmax=full.row(maxlabels),value=row.reduce((a,x,j)=>a+x*weights[j],0),
        vmax=rowmax.reduce((a,x,j)=>a+x*weights[j],0),dualValue=(ceiling-flow.flow)/4;
  if(Math.abs(value-dualValue)>3e-8||Math.abs(value-vmax)>3e-8)throw Error('projection flow/direct-capture mismatch');
  return{value,dualValue,labels,maxlabels,row,rowmax,nodes:g.n,arcs:g.to.length/2};
}
module.exports={project,solve,labelsFromProjection};
