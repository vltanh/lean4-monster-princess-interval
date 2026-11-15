/* Floating discovery helper only. Exact reports use separate BigInt scorers. */
"use strict";
module.exports=(function(){

function unique(a){a.sort((x,y)=>x-y);return a.filter((x,i)=>!i||x-a[i-1]>1e-12);}
function bs(a,x){let l=0,r=a.length;while(l<r){let m=(l+r)>>1;if(a[m]<=x)l=m+1;else r=m;}return l;}
class FloatField{
 constructor(data){
 this.nodes=data.nodes;this.values=data.values;this.grid=[0,1].map(k=>unique(data.nodes.map(p=>p[k])));this.cells=new Map();this.strips=[new Map(),new Map()];this.triangles=[];
 this.initial=this.nodes.map((p,i)=>[p,this.values[i]]).filter(([p,v])=>Math.abs(p[0]+p[1])<1e-13).map(([p,v])=>[p[0],v]).sort((a,b)=>a[0]-b[0]);this.initialKnots=this.initial.map(p=>p[0]);
 for(const inds of data.triangles){
  const ps=inds.map(i=>this.nodes[i]),[p,q,r]=ps,e=[q[0]-p[0],q[1]-p[1]],f=[r[0]-p[0],r[1]-p[1]],det=e[0]*f[1]-e[1]*f[0],[x,y,z]=inds.map(i=>this.values[i]),ru=((y-x)*f[1]-(z-x)*e[1])/det,rv=(e[0]*(z-x)-f[0]*(y-x))/det,n=this.triangles.length;
  this.triangles.push({ps,cf:[ru,rv,x-ru*p[0]-rv*p[1]],positive:det>0,scale:Math.abs(det)});
  const ranges=[0,1].map(k=>[bs(this.grid[k],Math.min(...ps.map(p=>p[k])))-1,bs(this.grid[k],Math.max(...ps.map(p=>p[k])))-1]);
  for(let k=0;k<2;k++)for(let i=ranges[k][0];i<ranges[k][1];i++){if(!this.strips[k].has(i))this.strips[k].set(i,[]);this.strips[k].get(i).push(n);}
  for(let i=ranges[0][0];i<ranges[0][1];i++)for(let j=ranges[1][0];j<ranges[1][1];j++){let key=i+","+j;if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(n);}
 }
 this.rcache=new Map();this.icache=new Map();this.calls=0;
 }
 initialValue(z){const i=Math.max(0,Math.min(this.initial.length-2,bs(this.initialKnots,z)-1)),[a,x]=this.initial[i],[b,y]=this.initial[i+1];return x+(z-a)*(y-x)/(b-a);}
 radial(u,v){
  if(v>1)return 0;const key=u+","+v;if(this.rcache.has(key))return this.rcache.get(key);
  const cell=[u,v].map((p,k)=>Math.max(0,Math.min(this.grid[k].length-2,bs(this.grid[k],p)-1))),poss=new Set();
  for(let i of[cell[0],cell[0]-1])for(let j of[cell[1],cell[1]-1])for(let n of(this.cells.get(i+","+j)||[]))poss.add(n);
  for(let n of[...poss].sort((a,b)=>a-b)){
   const {ps,cf,positive,scale}=this.triangles[n],turns=ps.map((p,i)=>{let q=ps[(i+1)%3];return(q[0]-p[0])*(v-p[1])-(q[1]-p[1])*(u-p[0]);});
   if(turns.every(t=>positive?t>=-scale*1e-8:t<=scale*1e-8)){
    const z=cf[0]*u+cf[1]*v+cf[2];this.rcache.set(key,z);return z;
   }
  }throw Error("no float triangle "+key);
 }
 integral(fixed,left,right,axis,threshold=null){
  if(right-left<=1e-14)return 0;const key=[fixed,left,right,axis,threshold===null?"":threshold].join(",");if(this.icache.has(key))return this.icache.get(key);
  if((axis===1&&fixed>=1)||(axis===0&&left>=1))return threshold===null?0:Math.max(0,threshold)*(right-left);
  if(axis===0&&right>1)return this.integral(fixed,left,1,axis,threshold)+(threshold===null?0:Math.max(0,threshold)*(right-1));
  const i=Math.max(0,Math.min(this.grid[axis].length-2,bs(this.grid[axis],fixed)-1)),poss=new Set([...(this.strips[axis].get(i)||[]),...(this.strips[axis].get(i-1)||[])]),cuts=[left,right],other=1-axis;
  for(const n of poss){const {ps}=this.triangles[n];for(let k=0;k<3;k++){const a=ps[k],b=ps[(k+1)%3];if(a[axis]===b[axis]){if(a[axis]===fixed)for(const x of[a,b])if(x[other]>left&&x[other]<right)cuts.push(x[other]);}else if(Math.min(a[axis],b[axis])<=fixed&&fixed<=Math.max(a[axis],b[axis])){const v=a[other]+(fixed-a[axis])*(b[other]-a[other])/(b[axis]-a[axis]);if(v>left&&v<right)cuts.push(v);}}}
  const cs=unique(cuts);let total=0;
  for(let j=0;j+1<cs.length;j++){const a=cs[j],b=cs[j+1];let fa=axis===0?this.radial(fixed,a):this.radial(a,fixed),fb=axis===0?this.radial(fixed,b):this.radial(b,fixed);
   if(threshold!==null){fa=threshold-fa;fb=threshold-fb;if(fa<=0&&fb<=0)continue;if(fa*fb<0){let w=(b-a)*(fa>0?fa/(fa-fb):fb/(fb-fa));total+=w*Math.max(fa,fb)/2;continue;}}
   total+=(b-a)*(fa+fb)/2;
  }
  this.icache.set(key,total);return total;
 }
 generalI(z,v,s){
  this.calls++;if(this.icache.size>200000){this.icache.clear();this.rcache.clear();}
  const A=this.initialValue(z),l=this.radial(z,v),B=Math.abs(s-v-2)<1e-12?1:this.radial(s,v),
  twoPs=2*s*l-this.integral(s,Math.max(-s,s-2),s,0,l),
  high=this.integral(v,z,s,1)-A*(s-z)+this.integral(v,z,s,1,A);
  return(this.integral(z,-z,z,0)-(z+v)*l-this.integral(z,v,z,0)+twoPs
   +2*(s+3)*(1-A)-(s+6-v)*Math.max(0,B-A)-high+2*s+2-this.integral(s,s,s+2,1))/4;
 }
}
return {FloatField};
})();
