// Two-phase simplex, standard tableau; floating discovery only.
// maximize c.x subject to A.x <= b, x >= 0.
const LP_EPS=1e-9;
class LPSolver {
 constructor(A,b,c){
  this.m=b.length;this.n=c.length;
  const m=this.m,n=this.n;
  this.N=Array.from({length:n+1},(_,i)=>i);
  this.B=Array.from({length:m},(_,i)=>n+i);
  this.D=Array.from({length:m+2},()=>Array(n+2).fill(0));
  for(let i=0;i<m;i++){for(let j=0;j<n;j++)this.D[i][j]=A[i][j];this.D[i][n]=-1;this.D[i][n+1]=b[i];}
  for(let j=0;j<n;j++)this.D[m][j]=-c[j];
  this.N[n]=-1;this.D[m+1][n]=1;
 }
 pivot(r,s){
  const D=this.D,m=this.m,n=this.n,inv=1/D[r][s];
  for(let i=0;i<m+2;i++)if(i!==r)for(let j=0;j<n+2;j++)if(j!==s)D[i][j]-=D[r][j]*D[i][s]*inv;
  for(let j=0;j<n+2;j++)if(j!==s)D[r][j]*=inv;
  for(let i=0;i<m+2;i++)if(i!==r)D[i][s]*=-inv;
  D[r][s]=inv;
  [this.B[r],this.N[s]]=[this.N[s],this.B[r]];
 }
 simplex(phase){
  const m=this.m,n=this.n,D=this.D,B=this.B,N=this.N,x=phase===1?m+1:m;
  while(true){
   let s=-1;
   for(let j=0;j<=n;j++){
    if(phase===2&&N[j]===-1)continue;
    if(s===-1||D[x][j]<D[x][s]-LP_EPS||(Math.abs(D[x][j]-D[x][s])<=LP_EPS&&N[j]<N[s]))s=j;
   }
   if(D[x][s]>=-LP_EPS)return true;
   let r=-1;
   for(let i=0;i<m;i++){
    if(D[i][s]<=LP_EPS)continue;
    let val=D[i][n+1]/D[i][s];
    if(r===-1 || val<D[r][n+1]/D[r][s]-LP_EPS||(Math.abs(val-D[r][n+1]/D[r][s])<=LP_EPS&&B[i]<B[r]))r=i;
   }
   if(r===-1)return false;
   this.pivot(r,s);
  }
 }
 solve(){
  const m=this.m,n=this.n,D=this.D,B=this.B,N=this.N;
  let r=0;for(let i=1;i<m;i++)if(D[i][n+1]<D[r][n+1])r=i;
  if(D[r][n+1]<-LP_EPS){
   this.pivot(r,n);
   if(!this.simplex(1)||D[m+1][n+1]<-LP_EPS)return {status:"infeasible"};
   if(D[m+1][n+1]>LP_EPS)return {status:"infeasible"};
   for(let i=0;i<m;i++)if(B[i]===-1){
    let s=-1;for(let j=0;j<=n;j++)
      if(s===-1||D[i][j]<D[i][s]-LP_EPS||(Math.abs(D[i][j]-D[i][s])<=LP_EPS&&N[j]<N[s]))s=j;
    this.pivot(i,s);
   }
  }
  if(!this.simplex(2))return {status:"unbounded"};
  const x=Array(n).fill(0);
  for(let i=0;i<m;i++)if(B[i]<n)x[B[i]]=D[i][n+1];
  return {status:"optimal",objective:D[m][n+1],x};
 }
}
function maximizeMin(features,low,high){
 const n=features[0].length;
 const A=[],b=[],c=Array(n+1).fill(0);c[n]=1;
 const constant=features.map(row=>row.reduce((s,a)=>s+low*a,0));
 const mass=1-n*low;
 for(let j=0;j<n;j++){const row=Array(n+1).fill(0);row[j]=1;A.push(row);b.push(high-low);}
 // y = z-1 >= 0; linear constraints z <= feature . warp .
 for(let i=0;i<features.length;i++){
  const row=features[i].map(a=>-a).concat([1]);A.push(row);b.push(constant[i]-1);
 }
 // sum increments exactly 1 => sum x=mass
 A.push(Array(n).fill(1).concat([0]));b.push(mass);
 A.push(Array(n).fill(-1).concat([0]));b.push(-mass);
 const result=new LPSolver(A,b,c).solve();
 if(result.status!=="optimal")return result;
 const d=result.x.slice(0,n).map(x=>x+low);
 return {...result,d,value:1+result.x[n],residualSum:d.reduce((a,b)=>a+b,0)-1};
}
return {LPSolver,maximizeMin};