#!/usr/bin/env node
/** Exact fixed-mesh response-cell geometry audit. No payoff solve.
 * Python port response_cells.py was not run during the executor outage.
 */
import {readFileSync,writeFileSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';

function auditResponseGeometry(data) {
 const D=1310720n;
 const r=x=>{let a=BigInt(Math.round(x*Number(D)));if(Math.abs(Number(a)/Number(D)-x)>1e-14)throw Error("coordinate");return a};
 const grid=data.base.map(r),n=grid.length-1;
 const nodes=data.nodes.map(p=>p.map(r));
 const ug=[...new Set(nodes.map(p=>p[0].toString()))].map(BigInt).sort((a,b)=>a<b?-1:a>b?1:0);
 const vg=[...new Set(nodes.map(p=>p[1].toString()))].map(BigInt).sort((a,b)=>a<b?-1:a>b?1:0);
 const ui=new Map(ug.map((x,i)=>[x.toString(),i])),vi=new Map(vg.map((x,i)=>[x.toString(),i]));
 const tris=data.triangles.map(t=>t.map(i=>nodes[i]));
 const cells=new Map;
 const cross=(p,q,r)=>(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0]);
 for(let k=0;k<tris.length;k++){
   let t=tris[k],us=t.map(p=>p[0]),vs=t.map(p=>p[1]);
   let imin=ui.get(us.reduce((a,b)=>a<b?a:b).toString()),imax=ui.get(us.reduce((a,b)=>a>b?a:b).toString());
   let jmin=vi.get(vs.reduce((a,b)=>a<b?a:b).toString()),jmax=vi.get(vs.reduce((a,b)=>a>b?a:b).toString());
   for(let i=imin;i<imax;i++)for(let j=jmin;j<jmax;j++){let key=i+","+j;if(!cells.has(key))cells.set(key,[]);cells.get(key).push(k)}
 }
 function bin(g,sum,m){let l=0,h=g.length;while(l<h){let k=(l+h)>>1;if(g[k]*m<=sum)l=k+1;else h=k}return Math.max(0,Math.min(g.length-2,l-1))}
 const checked=new Set;let projections=0,initialPrimitiveIntervalChecks=0;
 function sameInitialInterval(points){
   const aa=points.map(p=>p[0]),lo=aa.reduce((a,b)=>a<b?a:b),hi=aa.reduce((a,b)=>a>b?a:b);
   const i=bin(grid,lo,1n);if(lo<grid[i]||hi>grid[i+1])throw Error("initial primitive knot crossed");
   initialPrimitiveIntervalChecks++;
 }
 if(ug.filter(x=>x<=D).map(String).join()!==grid.map(String).join())throw Error("preone U grid");
 if(vg.filter(x=>x>=0n).map(String).join()!==grid.map(String).join())throw Error("positive V grid");
 if(vg.filter(x=>x<=0n).map(String).join()!==grid.map(x=>-x).reverse().map(String).join())throw Error("negative V grid");
 function commonTriangle(points){
   const key=points.map(p=>p.map(String).join(",")).sort().join(";");
   if(checked.has(key))return;
   const m=BigInt(points.length),su=points.reduce((a,p)=>a+p[0],0n),sv=points.reduce((a,p)=>a+p[1],0n);
   const i=bin(ug,su,m),j=bin(vg,sv,m);let found=false;
   for(let ii of[i,i-1])for(let jj of[j,j-1])for(let k of cells.get(ii+","+jj)||[]){
     const t=tris[k],sgn=cross(t[0],t[1],t[2]);
     if(points.every(p=>[0,1,2].every(z=>cross(t[z],t[(z+1)%3],p)*sgn>=0n)))found=true;
   }
   if(!found)throw Error("no common field triangle "+key);
   checked.add(key);projections++;
 }
 const sub=(a,b)=>a.map((x,i)=>x-b[i]);
 const det3=(a,b,c)=>a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]);
 function det(t){let z=det3(sub(t[1],t[0]),sub(t[2],t[0]),sub(t[3],t[0]));return z<0n?-z:z}
 const perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
 let negativeCount=0,negativeDet=0n;
 for(let a=0;a<n;a++)for(let s=a;s<n;s++)for(let b=s;b<n;b++)for(const p of perms){
   let pos=[];p.forEach((z,i)=>pos[z]=i);
   if(a===s&&pos[0]>pos[1]||s===b&&pos[1]>pos[2])continue;
   let bins=[a,s,b],z=[0,0,0],t=[z.slice()];
   for(let k=2;k>=0;k--){z=z.slice();z[p[k]]=1;t.push(z)}
   t=t.map(v=>v.map((z,k)=>grid[bins[k]+z]));
   if(t.some(([a,s,b])=>a<0n||a>s||s>b||b>D))throw Error("negative domain");
   sameInitialInterval(t);
   let vol=det(t);if(vol===0n)throw Error("zero tetra");
   commonTriangle(t.map(([a,s,b])=>[s,a]));
   commonTriangle(t.map(([a,s,b])=>[b,s]));
   negativeDet+=vol;negativeCount++;
 }
 function fibers(i){
   let rows=[],s0=grid[i],s1=grid[i+1],bid=0;
   rows.push({bin:bid++,side:"negative",ends:[[-s0,-s0],[-s1,-s0]],name:"edge"});
   let cuts=grid.slice(0,i+1).map(x=>-x).reverse().concat(grid.slice(1,i+1));
   for(let j=0;j<cuts.length-1;j++){
     let lo=cuts[j],hi=cuts[j+1],side=hi<=0n?"negative":"positive";
     rows.push({bin:bid,side,ends:[[lo,lo],[lo,hi]],name:"lower"});
     rows.push({bin:bid,side,ends:[[lo,hi],[hi,hi]],name:"upper"});bid++;
   }
   rows.push({bin:bid,side:"positive",ends:[[s0,s0],[s0,s1]],name:"edge"});
   return rows;
 }
 let positiveCount=0,positiveDet=0n;
 function acceptPositive(t){
   t=t.map(([s,v,c])=>[-v,s,c]);
   if(t.some(([a,s,c])=>a<0n||a>s||s>D||c< -a||c>s))throw Error("positive domain");
   sameInitialInterval(t);
   let vol=det(t);if(!vol)throw Error("zero positive tetra");
   commonTriangle(t.map(([a,s,c])=>[s,-a]));
   commonTriangle(t.map(([a,s,c])=>[s,c]));
   positiveCount++;positiveDet+=vol;
 }
 for(let i=0;i<n;i++){
   let rows=fibers(i),ss=[grid[i],grid[i+1]];
   for(const f of rows.filter(x=>x.side==="negative"))for(const g of rows){
     if(g.bin<f.bin)continue;
     if(f===g){
       let collapse=f.ends[0][0]===f.ends[0][1]?0:1,base=1-collapse;
       let apex=[ss[collapse],f.ends[collapse][0],f.ends[collapse][0]];
       let [lo,hi]=f.ends[base];
       acceptPositive([apex,[ss[base],lo,lo],[ss[base],lo,hi],[ss[base],hi,hi]]);
       continue;
     }
     if(f.bin===g.bin&&!f.ends.every((z,e)=>z[1]<=g.ends[e][0]))continue;
     const endpoint=e=>{
       let [a,b]=f.ends[e],[c,d]=g.ends[e];
       return [...new Map([[a,c],[b,c],[b,d],[a,d]].map(z=>[z.map(String).join(","),[ss[e],...z]])).values()];
     };
     let left=endpoint(0),right=endpoint(1);
     if(left.length+right.length===4)acceptPositive(left.concat(right));
     else if(left.length===1&&right.length===4){
       acceptPositive([left[0],right[0],right[1],right[2]]);
       acceptPositive([left[0],right[0],right[2],right[3]]);
     }else if(right.length===1&&left.length===4){
       acceptPositive([right[0],left[0],left[1],left[2]]);
       acceptPositive([right[0],left[0],left[2],left[3]]);
     }else throw Error("unexpected fiber "+[left.length,right.length]);
   }
 }
 let m1Count=0,m1Area=0n,m2Count=0,m2Area=0n,centerCount=0,centerArea=0n;
 const area=t=>{let z=cross(t[0],t[1],t[2]);return z<0n?-z:z};
 for(const t of tris)if(t.every(([u,v])=>u>=D&&u<=2n*D)){
   const q=t.map(([u,v])=>[2n*D-u,v]);sameInitialInterval(q);m1Count++;m1Area+=area(q);
 }
 for(const t of tris)if(t.every(([u,v])=>0n<=v&&v<=u&&u<=D)){
   const q=t.map(([u,v])=>[v,u]);sameInitialInterval(q);centerCount++;centerArea+=area(q);
 }
 function acceptM2(t){
   if(t.some(([a,c])=>a<0n||a>D||c< -a||c>D))throw Error("m2 domain");
   sameInitialInterval(t);m2Count++;m2Area+=area(t);
 }
 function rect(a,b,c,d){acceptM2([[a,c],[b,c],[b,d]]);acceptM2([[a,c],[b,d],[a,d]])}
 for(let j=0;j<n;j++){
   const a=grid[j],b=grid[j+1];
   for(let k=0;k<j;k++)rect(a,b,-grid[k+1],-grid[k]);
   acceptM2([[a,-a],[b,-b],[b,-a]]);
   for(let k=0;k<n;k++)rect(a,b,grid[k],grid[k+1]);
 }
 for(let i=0;i<n;i++){sameInitialInterval([[grid[i]],[grid[i+1]]]);sameInitialInterval([[grid[i]],[grid[i+1]]]);}
 if(negativeCount!==n**3||positiveCount!==3*n**3||m1Count!==3*n*n||m2Count!==3*n*n||centerCount!==n*n)throw Error("counts");
 if(negativeDet!==D**3n||positiveDet!==3n*D**3n||m1Area!==3n*D**2n||m2Area!==3n*D**2n||centerArea!==D**2n)throw Error("volumes");
 return {n,negativeM3Tetrahedra:negativeCount,positiveM3Tetrahedra:positiveCount,
   positiveM1Triangles:m1Count,positiveM2Triangles:m2Count,centerFixedOneTriangles:centerCount,
   exactProjectedTriangleChecks:projections,initialPrimitiveIntervalChecks,
   negativeM1Intervals:n,negativeM2Intervals:n,
   exactVolumes:{negativeM3:"1/6",positiveM3:"1/2",positiveM1:"3/2",positiveM2:"3/2",centerFixedOne:"1/2"},
   scope:"Geometric coverage and common-triangle checks only; no new payoff solve."};
}
export {auditResponseGeometry};
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 const here=dirname(fileURLToPath(import.meta.url));
 let field=resolve(here,'snapshots/endpoint_joint_i1_field.json'),output=null;
 for(let i=2;i<process.argv.length;i++){
   if(process.argv[i]==='--field')field=resolve(process.argv[++i]);
   else if(process.argv[i]==='--output')output=resolve(process.argv[++i]);
   else throw Error('Unknown argument '+process.argv[i]);
 }
 const result=auditResponseGeometry(JSON.parse(readFileSync(field,'utf8')));
 result.input=field;
 result.scope='Exact geometry coverage/common-triangle/primitive-knot checks; no payoff solve or unrestricted certificate.';
 if(output)writeFileSync(output,JSON.stringify(result,null,2)+'\n');
 process.stdout.write(JSON.stringify(result,null,2)+'\n');
}
