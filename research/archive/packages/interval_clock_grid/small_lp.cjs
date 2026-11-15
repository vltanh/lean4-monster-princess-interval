"use strict";
// Numerical discovery only. No result is certified by this simplex implementation.

class SmallLP{
 constructor(A,b,c,eps=1e-9){
  this.m=b.length;this.n=c.length;this.eps=eps;this.pivots=0;
  const m=this.m,n=this.n;this.B=new Int32Array(m);this.N=new Int32Array(n+1);
  this.D=Array.from({length:m+2},()=>new Float64Array(n+2));
  for(let i=0;i<m;i++){for(let j=0;j<n;j++)this.D[i][j]=A[i][j];this.B[i]=n+i;this.D[i][n]=-1;this.D[i][n+1]=b[i];}
  for(let j=0;j<n;j++){this.N[j]=j;this.D[m][j]=-c[j];}
  this.N[n]=-1;this.D[m+1][n]=1;
 }
 pivot(r,s){
  const D=this.D,m=this.m,n=this.n,inv=1/D[r][s],row=D[r];
  for(let i=0;i<m+2;i++)if(i!==r){
   const di=D[i],f=di[s]*inv;
   if(f!==0)for(let j=0;j<n+2;j++)if(j!==s)di[j]-=row[j]*f;
  }
  for(let j=0;j<n+2;j++)if(j!==s)row[j]*=inv;
  for(let i=0;i<m+2;i++)if(i!==r)D[i][s]*=-inv;
  row[s]=inv;const t=this.B[r];this.B[r]=this.N[s];this.N[s]=t;
  if(++this.pivots>200000)throw Error("simplex pivot limit");
 }
 simplex(phase){
  const m=this.m,n=this.n,D=this.D,E=this.eps,x=phase===1?m+1:m;
  for(;;){
   let s=-1;
   for(let j=0;j<=n;j++){
    if(phase===2&&this.N[j]===-1)continue;
    if(s<0||D[x][j]<D[x][s]-E||Math.abs(D[x][j]-D[x][s])<=E&&this.N[j]<this.N[s])s=j;
   }
   if(s<0||D[x][s]>=-E)return true;
   let r=-1;
   for(let i=0;i<m;i++)if(D[i][s]>E){
    if(r<0){r=i;continue;}
    const a=D[i][n+1]/D[i][s],b=D[r][n+1]/D[r][s];
    if(a<b-E||Math.abs(a-b)<=E&&this.B[i]<this.B[r])r=i;
   }
   if(r<0)return false;
   this.pivot(r,s);
  }
 }
 solve(){
  const m=this.m,n=this.n,D=this.D,E=this.eps;let r=0;
  for(let i=1;i<m;i++)if(D[i][n+1]<D[r][n+1])r=i;
  if(m&&D[r][n+1]<-E){
   this.pivot(r,n);
   if(!this.simplex(1)||D[m+1][n+1]<-E||Math.abs(D[m+1][n+1])>E)return {status:"infeasible"};
   for(let i=0;i<m;i++)if(this.B[i]===-1){
    let s=-1;for(let j=0;j<=n;j++)if(Math.abs(D[i][j])>E&&(s<0||D[i][j]<D[i][s]-E||Math.abs(D[i][j]-D[i][s])<=E&&this.N[j]<this.N[s]))s=j;
    if(s>=0)this.pivot(i,s);
   }
  }
  if(!this.simplex(2))return {status:"unbounded"};
  const x=new Array(n).fill(0),dual=new Array(m).fill(0);
  for(let i=0;i<m;i++)if(this.B[i]>=0&&this.B[i]<n)x[this.B[i]]=D[i][n+1];
  for(let j=0;j<=n;j++)if(this.N[j]>=n&&this.N[j]<n+m)dual[this.N[j]-n]=D[m][j];
  return {status:"optimal",value:D[m][n+1],x,dual,pivots:this.pivots};
 }
}
function solveColumns(g,columns){
 const k=columns.length,m=g.events.length,vars=k+g.matches.length;
 const A=Array.from({length:m+2},()=>new Float64Array(vars)),b=new Float64Array(m+2),c=new Float64Array(vars);
 for(let j=0;j<k;j++){const p=columns[j];c[j]=-p.cost;for(let i=0;i<m;i++)A[i][j]=-p.counts[i];A[m][j]=1;A[m+1][j]=-1;}
 for(let i=0;i<g.matches.length;i++){const [u,v]=g.matches[i];A[u][k+i]=1;A[v][k+i]=1;c[k+i]=1;}
 b[m]=1;b[m+1]=-1;
 const r=new SmallLP(A,b,c).solve();if(r.status!=="optimal")throw Error("LP "+r.status);
 let violation=0;for(let i=0;i<A.length;i++){let s=0;for(let j=0;j<vars;j++)s+=A[i][j]*r.x[j];violation=Math.max(violation,s-b[i]);}
 let reduced=0;for(let j=0;j<vars;j++){let s=0;for(let i=0;i<A.length;i++)s+=A[i][j]*r.dual[i];reduced=Math.min(reduced,s-c[j]);}
 if(violation>1e-7||reduced< -1e-7||Math.min(...r.x)< -1e-7||Math.min(...r.dual)< -1e-7)throw Error("LP residual");
 return {...r,minimum:-r.value,discounts:r.dual.slice(0,m),violation,reduced};
}

module.exports={SmallLP,solveColumns};
