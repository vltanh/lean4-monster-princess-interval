/* Portable revised packing simplex for discovery; independently inspect payoff residuals. */
function solvePackingRevised(A,b,c,options={}){
 const m=A.length,n=c.length,cols=Array.from({length:n},(_,j)=>Float64Array.from(A,row=>row[j]));
 const tol=options.tolerance||1e-10,feasTol=options.feasibilityTolerance||1e-11,maxPivots=options.maxPivots||10000;
 if(b.length!==m||A.some(r=>r.length!==n))throw Error("shape");
 if(!options.basis&&b.some(x=>x<0))throw Error("packing requires a feasible initial basis");
 let B=options.basis?options.basis.slice():Array.from({length:m},(_,i)=>n+i);
 let inverse=Array.from({length:m},(_,i)=>Float64Array.from({length:m},(_,j)=>i===j?1:0)),xb=Float64Array.from(b),refactors=0;
 const column=j=>j<n?cols[j]:Float64Array.from({length:m},(_,i)=>i===j-n?1:0);
 const cost=j=>j<n?c[j]:0;
 function refactor(){
  const work=Array.from({length:m},(_,i)=>{const r=new Float64Array(2*m);for(let j=0;j<m;j++)r[j]=B[j]<n?A[i][B[j]]:(B[j]-n===i?1:0);r[m+i]=1;return r;});
  for(let k=0;k<m;k++){
   let p=k;for(let i=k+1;i<m;i++)if(Math.abs(work[i][k])>Math.abs(work[p][k]))p=i;
   if(Math.abs(work[p][k])<1e-14)throw Error("singular basis");
   [work[p],work[k]]=[work[k],work[p]];const row=work[k],d=row[k];
   for(let j=k;j<2*m;j++)row[j]/=d;
   for(let i=0;i<m;i++)if(i!==k){const z=work[i][k];if(z===0)continue;work[i][k]=0;for(let j=k+1;j<2*m;j++)work[i][j]-=z*row[j];}
  }
  inverse=work.map(r=>r.slice(m));xb=Float64Array.from(inverse,row=>{let z=0;for(let i=0;i<m;i++)z+=row[i]*b[i];return z;});refactors++;
 }
 if(options.basis)refactor();
 if(Math.min(...xb)<-10*feasTol)throw Error("infeasible starting basis");
 let pivots=0,minPivot=Infinity,done=false,duals=new Float64Array(m),lastRef=-1;
 for(;pivots<maxPivots;pivots++){
  if(pivots&&pivots%40===0){refactor();lastRef=pivots;}
  const basic=new Uint8Array(n+m);for(const j of B)basic[j]=1;
  duals.fill(0);for(let i=0;i<m;i++){const z=cost(B[i]);if(z)for(let k=0;k<m;k++)duals[k]+=z*inverse[i][k];}
  let enter=-1,rcBest=tol;
  for(let j=0;j<n;j++)if(!basic[j]){let rc=c[j],col=cols[j];for(let k=0;k<m;k++)rc-=duals[k]*col[k];if(rc>rcBest){rcBest=rc;enter=j;}}
  for(let k=0;k<m;k++)if(!basic[n+k]&&-duals[k]>rcBest){rcBest=-duals[k];enter=n+k;}
  if(enter<0){if(lastRef!==pivots){refactor();lastRef=pivots;pivots--;continue;}done=true;break;}
  const col=column(enter),d=Float64Array.from(inverse,row=>{let z=0;for(let k=0;k<m;k++)z+=row[k]*col[k];return z;});
  let relaxed=Infinity;
  for(let i=0;i<m;i++)if(d[i]>1e-12)relaxed=Math.min(relaxed,(Math.max(0,xb[i])+feasTol)/d[i]);
  let leave=-1,largest=0;
  for(let i=0;i<m;i++)if(d[i]>1e-12&&xb[i]/d[i]<=relaxed&&d[i]>largest){leave=i;largest=d[i];}
  if(leave<0)throw Error("unbounded packing");
  const pivot=d[leave];minPivot=Math.min(minPivot,Math.abs(pivot));
  const newRow=inverse[leave];for(let k=0;k<m;k++)newRow[k]/=pivot;
  const step=xb[leave]/pivot;
  for(let i=0;i<m;i++)if(i!==leave){const z=d[i];for(let k=0;k<m;k++)inverse[i][k]-=z*newRow[k];xb[i]-=z*step;}
  xb[leave]=step;B[leave]=enter;
  if(options.progress&&pivots%100===0)options.progress({pivots,refactors,rc:rcBest,minBasic:Math.min(...xb)});
 }
 refactor();
 const x=Array(n).fill(0);for(let i=0;i<m;i++)if(B[i]<n)x[B[i]]=xb[i];
 duals.fill(0);for(let i=0;i<m;i++){const z=cost(B[i]);if(z)for(let k=0;k<m;k++)duals[k]+=z*inverse[i][k];}
 const y=Array.from(duals),dot=(a,b)=>a.reduce((s,z,j)=>s+z*b[j],0);
 return{status:done?"optimal":"pivot limit",x,y,basis:B,pivots,refactors,minPivot,objective:dot(c,x),dualObjective:dot(b,y),
 primalViolation:Math.max(0,-Math.min(...x),...A.map((row,i)=>dot(row,x)-b[i])),
 dualViolation:Math.max(0,-Math.min(...y),...cols.map((col,j)=>c[j]-dot(Array.from(col),y)))};
}
const api={solvePackingRevised};
if(typeof module==='object'&&module.exports)module.exports=api;
return api;