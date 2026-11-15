
function compileLateWarpEdges(E,W,field,warp,{verifyQuarter=true,onProgress=()=>{}}={}){
 const {Q,ZERO,ONE,minQ,maxQ,uniq,bisect}=E,n=warp.n;
 const columns=new Map(),ncache=new Map(),acache=new Map();let coefficientChecks=0;
 function zero(){return Array(n).fill(ZERO);}
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const r=a%b;a=b;b=r;}return a;}
 function compact(v){let d=1n;for(const x of v)d=d/gcd(d,x.d)*x.d;return{denominator:String(d),numerators:v.map(x=>String(x.n*(d/x.d)))};}
 function cuts(fixed,left,right,axis){
  const i=Math.max(0,Math.min(field.grid[axis].length-2,bisect(field.grid[axis],fixed)-1)),poss=new Set([...(field.strips[axis].get(i)||[]),...(field.strips[axis].get(i-1)||[])]),out=[left,right,...warp.interiorKnots(left,right)],other=1-axis;
  for(const index of poss){const ps=field.triangles[index].ps;for(let j=0;j<3;j++){
   const a=ps[j],b=ps[(j+1)%3];if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(const p of[a,b])if(p[other].cmp(left)>0&&p[other].cmp(right)<0)out.push(p[other]);}
   else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&fixed.cmp(maxQ(a[axis],b[axis]))<=0){
    const t=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));if(t.cmp(left)>0&&t.cmp(right)<0)out.push(t);
   }
  }}
  return uniq(out);
 }
 function area(left,right,fl,fr){const bl=warp.basis(left),br=warp.basis(right),mean=fl.a(fr).dby(2);return bl.map((x,i)=>br[i].s(x).m(mean));}
 function Nv(a){
  const key=a.str();if(ncache.has(key))return ncache.get(key);const xs=cuts(a,a.neg(),a,0),ys=xs.map(v=>field.radial(a,v)),out=zero();
  for(let i=0;i+1<xs.length;i++){const v=area(xs[i],xs[i+1],ys[i],ys[i+1]);for(let j=0;j<n;j++)out[j]=out[j].a(v[j]);}
  ncache.set(key,out);return out;
 }
 function column(a){
  const key=a.str();if(columns.has(key))return columns.get(key);
  const xs=cuts(a,a,a.a(2),1),ys=xs.map(u=>field.radial(u,a)),prefix=[zero()];
  for(let i=0;i+1<xs.length;i++){const v=area(xs[i],xs[i+1],ys[i],ys[i+1]);prefix.push(v.map((x,j)=>prefix[i][j].a(x)));}
  function query(s){const j=Math.max(0,Math.min(xs.length-2,bisect(xs,s)-1)),b=ys[j].a(s.s(xs[j]).m(ys[j+1].s(ys[j])).dby(xs[j+1].s(xs[j]))),v=area(xs[j],s,ys[j],b);return{B:b,I:v.map((x,k)=>prefix[j][k].a(x))};}
  const result={query};columns.set(key,result);return result;
 }
 function feature(s,a,endpoint){
  const key=a.str();if(!acache.has(key))acache.set(key,field.initialValue(a));const A=acache.get(key),c=column(a).query(s),B=endpoint?ONE:c.B,N=Nv(a),bu=warp.basis(s),ba=warp.basis(a),cu=Q(4).s(A.m(2)).s(B),constant=Q(8).s(A.m(2)).s(B.m(6));
  return N.map((x,i)=>x.a(cu.m(bu[i])).a(B.m(ba[i])).a(constant).s(c.I[i]).dby(4));
 }
 const edgeMap=new Map();let triangles=0;
 for(const tr of field.triangles){const ps=tr.ps;if(ps.some(p=>p[0].cmp(1)<0||p[1].cmp(0)<0))continue;triangles++;
  for(let j=0;j<3;j++){let p=ps[j],q=ps[(j+1)%3];if(p[1].eq(q[1]))continue;if(p[1].cmp(q[1])>0)[p,q]=[q,p];edgeMap.set(p.map(x=>x.str()).join(",")+";"+q.map(x=>x.str()).join(","),[p,q]);}
 }
 const edges=[...edgeMap.values()].sort((x,y)=>x[0][1].cmp(y[0][1])||x[1][1].cmp(y[1][1])||x[0][0].cmp(y[0][0])||x[1][0].cmp(y[1][0]));
 if(triangles!==3468||edges.length!==3502)throw Error("whole late geometry census");const cells=[];
 for(let index=0;index<edges.length;index++){
  const[p,q]=edges[index],endpoint=p[0].s(p[1]).eq(2)&&q[0].s(q[1]).eq(2),point=t=>p.map((x,j)=>x.a(q[j].s(x).m(t))),f=t=>feature(...point(t),endpoint),c0=f(ZERO),cm=f(Q("1/2")),c1=f(ONE);
  const qa=c0.map((x,j)=>c1[j].s(cm[j].m(2)).a(x).m(2)),qb=c0.map((x,j)=>c1[j].s(x).s(qa[j]));
  if(verifyQuarter){const actual=f(Q("1/4"));for(let j=0;j<n;j++){if(!actual[j].eq(c0[j].a(qb[j].dby(4)).a(qa[j].dby(16))))throw Error("late basis quadratic "+index+" "+j);coefficientChecks++;}}
  cells.push({family:"late_negative_m2",positive:false,edge:index,vertices:[p,q].map(p=>p.map(x=>x.str())),endpoint,interval:["0","1"],constant:compact(c0),linear:compact(qb),quadratic:compact(qa)});
  if((index+1)%500===0)onProgress({edges:index+1,cachedColumns:columns.size,coefficientChecks});
 }
 return{scope:"Exact complete continuous late-negative M2 warp quadratics on all fixed reference fiber-boundary edges; no unrestricted game guarantee.",knots:warp.knots.map(x=>x.str()),cells,verification:{triangles,edges:edges.length,basis_quarter_checks:coefficientChecks,cached_columns:columns.size}};
}
module.exports = {compileLateWarpEdges};
