#!/usr/bin/env node
/** Independent exact reconstruction after the 2026-11-11 executor outage.
 * Run: node exact_response_audit.mjs path/to/endpoint_joint_i1_field.json [report.json]
 * The computational body was executed in V8; no Lean compilation or CI was run.
 */
import fs from "node:fs";

function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a;}
class Rat{
 constructor(n,d=1n){if(n instanceof Rat){this.n=n.n;this.d=n.d;return;}if(typeof n==="string"){let p=n.split("/");if(p.length===2){n=BigInt(p[0]);d=BigInt(p[1]);}else {let [s,e]=n.toLowerCase().split("e");let neg=s[0]==="-";if(neg||s[0]==="+")s=s.slice(1);let parts=s.split(".");let f=parts[1]||"";n=BigInt(parts[0]+f)*(neg?-1n:1n);let power=f.length-Number(e||0);if(power>=0)d=10n**BigInt(power);else n*=10n**BigInt(-power);}}else n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
 a(q){q=Q(q);return new Rat(this.n*q.d+q.n*this.d,this.d*q.d);}
 s(q){q=Q(q);return new Rat(this.n*q.d-q.n*this.d,this.d*q.d);}
 m(q){q=Q(q);return new Rat(this.n*q.n,this.d*q.d);}
 dby(q){q=Q(q);return new Rat(this.n*q.d,this.d*q.n);}
 neg(){return new Rat(-this.n,this.d);}
 cmp(q){q=Q(q);let z=this.n*q.d-q.n*this.d;return z<0n?-1:z>0n?1:0;}
 eq(q){return this.cmp(q)===0;}
 num(){return Number(this.n)/Number(this.d);}
 str(){return String(this.n)+(this.d===1n?"":"/"+this.d);}
}
function Q(x){return x instanceof Rat?x:new Rat(typeof x==="number"?String(x):x);}
const ZERO=Q(0),ONE=Q(1);
function minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}
function maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}
function uniq(xs){let m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}
function bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){let m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}
function coord(x){let z=Q(x);if(z.cmp(0)<0)return coord(z.neg()).neg();const lim=4194304n;if(z.d<=lim)return z;let n=z.n,d=z.d,p0=0n,q0=1n,p1=1n,q1=0n;while(true){let a=n/d,q2=q0+a*q1;if(q2>lim)break;[p0,p1]=[p1,p0+a*p1];[q0,q1]=[q1,q2];[n,d]=[d,n-a*d];}
 let k=(lim-q0)/q1,b1=new Rat(p0+k*p1,q0+k*q1),b2=new Rat(p1,q1);return Math.abs(b1.num()-z.num())<Math.abs(b2.num()-z.num())?b1:b2;}
function subP(a,b){return[a[0].s(b[0]),a[1].s(b[1])];}
function cross(a,b){return a[0].m(b[1]).s(a[1].m(b[0]));}
class ExactField{
 constructor(data){
 this.nodes=data.nodes.map(p=>p.map(coord));this.values=(data.rational_values||data.values).map(Q);
 this.grid=[0,1].map(k=>uniq(this.nodes.map(p=>p[k])));this.cells=new Map();this.strips=[new Map(),new Map()];this.triangles=[];
 this.initial=this.nodes.map((p,i)=>[p,this.values[i]]).filter(([p,v])=>p[0].eq(p[1].neg())).map(([p,v])=>[p[0],v]).sort((a,b)=>a[0].cmp(b[0]));this.initialKnots=this.initial.map(p=>p[0]);
 for(const inds of data.triangles){
 let ps=inds.map(i=>this.nodes[i]),[p,q,r]=ps,[e,f]=[subP(q,p),subP(r,p)],det=cross(e,f),[x,y,z]=inds.map(i=>this.values[i]);
 let ru=y.s(x).m(f[1]).s(z.s(x).m(e[1])).dby(det),rv=e[0].m(z.s(x)).s(f[0].m(y.s(x))).dby(det);
 if(ru.cmp(0)<0||rv.cmp(0)>0)throw Error("transport");
 let n=this.triangles.length;this.triangles.push({ps,cf:[ru,rv,x.s(ru.m(p[0])).s(rv.m(p[1]))],positive:det.cmp(0)>0});
 let ranges=[0,1].map(k=>[bisect(this.grid[k],minQ(...ps.map(p=>p[k])),false),bisect(this.grid[k],maxQ(...ps.map(p=>p[k])),false)]);
 for(let k=0;k<2;k++)for(let i=ranges[k][0];i<ranges[k][1];i++){if(!this.strips[k].has(i))this.strips[k].set(i,[]);this.strips[k].get(i).push(n);}
 for(let i=ranges[0][0];i<ranges[0][1];i++)for(let j=ranges[1][0];j<ranges[1][1];j++){let key=i+","+j;if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(n);}
 }
 this.rcache=new Map();this.icache=new Map();
 }
 initialValue(z){z=Q(z);let i=Math.max(0,Math.min(this.initial.length-2,bisect(this.initialKnots,z)-1));let[a,x]=this.initial[i],[b,y]=this.initial[i+1];return x.a(z.s(a).m(y.s(x)).dby(b.s(a)));}
 radial(u,v){u=Q(u);v=Q(v);if(v.cmp(1)>0)return ZERO;let key=u.str()+","+v.str();if(this.rcache.has(key))return this.rcache.get(key);let cell=[u,v].map((p,k)=>Math.max(0,Math.min(this.grid[k].length-2,bisect(this.grid[k],p)-1))),poss=new Set();
 for(let i of[cell[0],cell[0]-1])for(let j of[cell[1],cell[1]-1])for(let n of(this.cells.get(i+","+j)||[]))poss.add(n);
 for(let n of[...poss].sort((a,b)=>a-b)){let {ps,cf,positive}=this.triangles[n];let turns=ps.map((p,i)=>cross(subP(ps[(i+1)%3],p),subP([u,v],p)));if(turns.every(t=>positive?t.cmp(0)>=0:t.cmp(0)<=0)){let z=cf[0].m(u).a(cf[1].m(v)).a(cf[2]);this.rcache.set(key,z);return z;}}
 throw Error("no triangle "+key);
 }
 integral(fixed,left,right,axis,threshold=null){fixed=Q(fixed);left=Q(left);right=Q(right);if(threshold!==null)threshold=Q(threshold);if(right.cmp(left)<=0)return ZERO;
 let key=[fixed.str(),left.str(),right.str(),axis,threshold===null?"":threshold.str()].join(",");if(this.icache.has(key))return this.icache.get(key);
 if((axis===1&&fixed.cmp(1)>=0)||(axis===0&&left.cmp(1)>=0))return threshold===null?ZERO:maxQ(0,threshold).m(right.s(left));
 if(axis===0&&right.cmp(1)>0)return this.integral(fixed,left,ONE,axis,threshold).a(threshold===null?ZERO:maxQ(0,threshold).m(right.s(1)));
 let i=Math.max(0,Math.min(this.grid[axis].length-2,bisect(this.grid[axis],fixed)-1)),poss=new Set([...(this.strips[axis].get(i)||[]),...(this.strips[axis].get(i-1)||[])]),cuts=[left,right],other=1-axis;
 for(let n of poss){let {ps}=this.triangles[n];for(let k=0;k<3;k++){let a=ps[k],b=ps[(k+1)%3];if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(let x of[a,b])if(x[other].cmp(left)>0&&x[other].cmp(right)<0)cuts.push(x[other]);}else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&fixed.cmp(maxQ(a[axis],b[axis]))<=0){let v=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));if(v.cmp(left)>0&&v.cmp(right)<0)cuts.push(v);}}}
 cuts=uniq(cuts);let total=ZERO;
 for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],fa=axis===0?this.radial(fixed,a):this.radial(a,fixed),fb=axis===0?this.radial(fixed,b):this.radial(b,fixed);
 if(threshold!==null){fa=threshold.s(fa);fb=threshold.s(fb);if(fa.cmp(0)<=0&&fb.cmp(0)<=0)continue;if(fa.m(fb).cmp(0)<0){let w=b.s(a).m(fa.cmp(0)>0?fa.dby(fa.s(fb)):fb.dby(fb.s(fa)));total=total.a(w.m(maxQ(fa,fb)).dby(2));continue;}}
 total=total.a(b.s(a).m(fa.a(fb)).dby(2));}
 this.icache.set(key,total);return total;
 }
 negativeM1(a){a=Q(a);return this.integral(a,a.neg(),a,0).a(a.m(4)).a(8).s(a.a(3).m(2).m(this.initialValue(a))).s(this.integral(a,a,a.a(2),1)).dby(4);}
 positiveM1(a){a=Q(a);let A=this.initialValue(a);return Q(8).s(a.m(4)).a(Q(3).s(a).m(A)).s(this.integral(a.neg(),a,Q(2).s(a),1)).s(this.integral(Q(2).s(a),a.neg(),ONE,0,A)).dby(4);}
 fixedOne(a,positive){a=Q(a);let A=this.initialValue(a),v=positive?a.neg():a,I=this.integral(v,a,ONE,1),B=this.radial(ONE,v);
 return positive?Q(12).a(A.m(2)).s(Q(7).a(a).m(B)).s(I).s(this.integral(ONE,a.neg(),ONE,0,A)).dby(4):this.integral(a,a.neg(),a,0).a(12).s(A.m(4)).s(Q(7).s(a).m(B)).s(I).dby(4);
 }
 cdfSides(t,x){t=Q(t);x=Q(x);let r=this.radial(t.a(x.cmp(0)<0?x.neg():x),t.s(x.cmp(0)<0?x.neg():x));if(x.eq(0))return[ONE.s(r).dby(2),ONE.a(r).dby(2)];if(x.eq(1))return[ONE.a(r).dby(2),ONE];if(x.eq(-1))return[ZERO,ONE.s(r).dby(2)];let v=x.cmp(0)>0?ONE.a(r).dby(2):ONE.s(r).dby(2);return[v,v];}
 unitRoutePayoff(route){route=route.map(p=>p.map(Q));let[lower,upper]=this.cdfSides(...route[0]),cost=ZERO;
 for(let k=0;k<route.length-1;k++){let[start,x]=route[k],[end,y]=route[k+1];if(end.eq(start)){if(!x.eq(y))throw Error("bad duplicate");continue;}let vel=y.s(x).dby(end.s(start));if(!vel.eq(1)&&!vel.eq(-1))throw Error("not unit");let cuts=[start,end];if(x.m(y).cmp(0)<0)cuts.splice(1,0,start.s(vel.m(x)));let area=ZERO;
 for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],xa=x.a(vel.m(a.s(start))),xb=x.a(vel.m(b.s(start))),sign=xa.a(xb).cmp(0)>0?1:-1,ua=a.a(xa.m(sign)),va=a.s(xa.m(sign)),ub=b.a(xb.m(sign)),vb=b.s(xb.m(sign)),record=vel.eq(1)?upper:lower;
 if(vel.m(sign).eq(1)){let threshold=sign===1?record.m(2).s(1):ONE.s(record.m(2));area=area.a(this.integral(va,ua,ub,1).s(threshold.m(ub.s(ua))).a(this.integral(va,ua,ub,1,threshold)).dby(4));}
 else{let threshold=sign===-1?ONE.s(record.m(2)):record.m(2).s(1);area=area.a(this.integral(ua,va,vb,0,threshold).dby(4));}}
 let[strict,closed]=this.cdfSides(end,y);if(vel.eq(1)){let updated=maxQ(upper,closed);cost=cost.a(end.m(updated.s(upper))).s(area);upper=updated;}else{let updated=minQ(lower,strict);cost=cost.a(end.m(lower.s(updated))).s(area);lower=updated;}}
 if(!lower.eq(0)||!upper.eq(1))throw Error("incomplete");return cost;
 }
}

function fixedRoute(x){x=Q(x);return[[ZERO,x],[ONE.s(x).dby(2),ONE.a(x).dby(2)],[Q(2),Q(-1)],[Q(4),ONE]];}
function earlyRoute(a,s){a=Q(a);s=Q(s);return[[ZERO,a.neg()],[s.a(a).dby(2),s.s(a).dby(2)],[s.a(1).dby(2),s.s(1).dby(2)],[Q(2),ONE],[Q(4),Q(-1)]];}
function negativeEarly(f,a,s){a=Q(a);s=Q(s);let A=f.initialValue(a),N=f.integral(a,a.neg(),a,0),B=f.radial(s,a),D=f.radial(ONE,s),I=f.integral(a,a,s,1),G=f.integral(s,s,ONE,1).s(A.m(ONE.s(s))).a(f.integral(s,s,ONE,1,A));return N.a(12).s(A.m(8)).a(s.a(a).s(4).m(B)).s(Q(7).s(s).m(maxQ(ZERO,D.s(A)))).s(I).s(G).dby(4);}
function auditFixed(f,pos){
 let knots=uniq([ZERO,ONE,...f.initialKnots,...f.grid.flat().filter(x=>x.cmp(0)>=0&&x.cmp(1)<=0)]);
 if(pos){let levels=uniq(f.grid[1].map(v=>f.radial(ONE,v)));let more=[];
  for(let i=0;i<f.initial.length-1;i++){let[a,x]=f.initial[i],[b,y]=f.initial[i+1];if(y.eq(x))continue;for(let r of levels)if(r.cmp(x)>0&&r.cmp(y)<0)more.push(a.a(r.s(x).m(b.s(a)).dby(y.s(x))));}
 knots=uniq([...knots,...more]);}
 let best=null,quadChecks=0,captureChecks=0;
 function offer(a,v){if(best===null||v.cmp(best.v)<0)best={a,v};}
 for(let i=0;i<knots.length-1;i++){let lo=knots[i],hi=knots[i+1],fun=a=>f.fixedOne(a,pos),f0=fun(lo),fm=fun(lo.a(hi).dby(2)),f1=fun(hi),qa=f1.s(fm.m(2)).a(f0).m(2),qb=f1.s(f0).s(qa),qc=f0;
 if(!fun(lo.m(3).a(hi).dby(4)).eq(qa.dby(16).a(qb.dby(4)).a(qc)))throw Error("not quadratic "+pos+" "+lo.str());quadChecks++;
 offer(lo,f0);offer(hi,f1);if(qa.cmp(0)>0){let y=qb.neg().dby(qa.m(2));if(y.cmp(0)>0&&y.cmp(1)<0){let a=lo.a(hi.s(lo).m(y)),v=qc.s(qb.m(qb).dby(qa.m(4)));if(!fun(a).eq(v))throw Error("vertex mismatch");offer(a,v);}}
 for(let j of[1,2]){let a=lo.a(hi.s(lo).m(j).dby(3));if(!f.unitRoutePayoff(fixedRoute(pos?a:a.neg())).eq(fun(a)))throw Error("physical mismatch");captureChecks++;}
 }
 if(!f.unitRoutePayoff(fixedRoute(pos?best.a:best.a.neg())).eq(best.v))throw Error("minimum physical mismatch");
 return{sign:pos?"positive":"negative",cells:knots.length-1,start:(pos?best.a:best.a.neg()).str(),absolute_start:best.a.str(),value:best.v.str(),decimal:best.v.num(),gap:best.v.s(f.positiveM1(ONE)).str(),gap_decimal:best.v.s(f.positiveM1(ONE)).num(),quadratic_checks:quadChecks,capture_checks:captureChecks};
}

function solveLinear(matrix,rhs){
 const n=matrix.length,a=matrix.map((row,i)=>[...row.map(Q),Q(rhs[i])]);
 for(let col=0;col<n;col++){let pivot=col;while(pivot<n&&a[pivot][col].eq(0))pivot++;if(pivot===n)return null;[a[col],a[pivot]]=[a[pivot],a[col]];let z=a[col][col];for(let k=col;k<=n;k++)a[col][k]=a[col][k].dby(z);for(let i=0;i<n;i++)if(i!==col&&!a[i][col].eq(0)){let c=a[i][col];for(let k=col;k<=n;k++)a[i][k]=a[i][k].s(c.m(a[col][k]));}}
 return a.map(row=>row[n]);
}
function evaluateQuad(matrix,w){let total=ZERO;for(let i=0;i<w.length;i++)for(let j=0;j<w.length;j++)total=total.a(Q(matrix[i][j]).m(w[i]).m(w[j]));return total;}
function minQuad(input){
 const matrix=input.map(row=>row.map(Q)),n=matrix.length;let best=null,faces=0,singular=0,feasible=0;
 for(let mask=1;mask<(1<<n);mask++){let ids=[];for(let i=0;i<n;i++)if(mask&(1<<i))ids.push(i);let k=ids.length,a=ids.map(i=>[...ids.map(j=>matrix[i][j].m(2)),Q(-1)]);a.push([...ids.map(()=>ONE),ZERO]);let rhs=[...ids.map(()=>ZERO),ONE],sol=solveLinear(a,rhs);faces++;if(sol===null){singular++;continue;}if(sol.slice(0,k).some(w=>w.cmp(0)<0))continue;feasible++;let weights=Array(n).fill(ZERO);ids.forEach((i,j)=>weights[i]=sol[j]);let value=evaluateQuad(matrix,weights);if(!value.eq(sol[k].dby(2)))throw Error("stationary identity");if(best===null||value.cmp(best.value)<0)best={value,weights,support:ids};}
 if(best===null)throw Error("no vertex");return{...best,faces,singular,feasible};
}
function matrixFrom(vertices,fn){
 const vals=vertices.map(fn),n=vertices.length,m=Array.from({length:n},()=>Array(n).fill(ZERO));
 for(let i=0;i<n;i++){m[i][i]=vals[i];for(let j=0;j<i;j++)m[i][j]=m[j][i]=fn(vertices[i].map((x,k)=>Q(x).a(vertices[j][k]).dby(2))).m(2).s(vals[i].a(vals[j]).dby(2));}return m;
}

function assert(condition,message){if(!condition)throw Error(message);}
function negativeLift(f,p,branch){let[a,s,b]=p,A=f.initialValue(a);return f.integral(a,a.neg(),a,0).a(12).s(A.m(8)).a(s.a(a).s(4).m(f.radial(s,a))).s(f.integral(a,a,s,1)).s(Q(branch).m(Q(7).s(s)).m(f.radial(ONE,s).s(A))).s(f.integral(s,b,ONE,1)).a(ONE.s(b).m(A));}
function runAudit(data){
 const f=new ExactField(data),reference=f.positiveM1(ONE),families=[auditFixed(f,true),auditFixed(f,false)];
 let m3Checks=0;
 for(const av of["1/32","3/5","3/4"]){let a=Q(av);for(const sv of["13/16","273/320","7/8","1"]){let s=maxQ(a,Q(sv));assert(negativeEarly(f,a,s).eq(f.unitRoutePayoff(earlyRoute(a,s))),"M3 physical identity");m3Checks++;}}
 const fixtures=[
 {matrix:[[1,1,1],[1,1,1],[1,1,1]],min:"1"},
 {matrix:[[-1,-1],[-1,-1]],min:"-1"},
 {matrix:[[1,0,0],[0,2,0],[0,0,3]],min:"6/11"},
 {matrix:[[1,2],[2,1]],min:"1"},
 {matrix:[[2,-1,-1],[-1,2,-1],[-1,-1,2]],min:"0"},
 {matrix:[[1,-1,-1],[-1,1,-1],[-1,-1,1]],min:"-1/3"},
 {matrix:[[0,0,1],[0,0,1],[1,1,2]],min:"0"},
 {matrix:[["7/13"]],min:"7/13"}];
 for(let t of fixtures)assert(minQuad(t.matrix).value.eq(t.min),"quadratic fixture");
 const pm=matrixFrom([[0,0],[1,0],[0,1]],p=>Q(p[0]).s("1/3").m(Q(p[0]).s("1/3")).a(Q(p[1]).s("1/4").m(Q(p[1]).s("1/4")).m(2)));
 const pr=minQuad(pm);assert(pr.value.eq(0)&&pr.weights.map(x=>x.str()).join(",")==="5/12,1/3,1/4","independent polynomial");
 const vertices=[["0","13/16","13/16"],["1/16","7/8","7/8"],["0","7/8","7/8"],["0","13/16","7/8"]].map(p=>p.map(Q));
 let branchReports=[],polynomialChecks=0,captureChecks=0;
 for(let branch of[0,1]){
  const fn=p=>negativeLift(f,p,branch).s(reference.m(4)),matrix=matrixFrom(vertices,fn);
  for(let i=0;i<=5;i++)for(let j=0;j<=5-i;j++)for(let k=0;k<=5-i-j;k++){
   const l=5-i-j-k,w=[i,j,k,l].map(x=>Q(x).dby(5)),p=[0,1,2].map(k=>w.reduce((z,ww,i)=>z.a(ww.m(vertices[i][k])),ZERO));
   assert(evaluateQuad(matrix,w).eq(fn(p)),"whole-cell polynomial identity");polynomialChecks++;
   const physical=f.unitRoutePayoff(earlyRoute(p[0],p[1])),actual=negativeEarly(f,p[0],p[1]);
   assert(physical.eq(actual),"independent capture");assert(negativeLift(f,p,branch).dby(4).cmp(actual)>=0,"lift below actual");captureChecks+=2;
  }
  const answer=minQuad(matrix),point=[0,1,2].map(k=>answer.weights.reduce((z,w,i)=>z.a(w.m(vertices[i][k])),ZERO));
  const physical=f.unitRoutePayoff(earlyRoute(point[0],point[1]));
  if(branch===1){
   assert(physical.s(reference).m(4).eq(answer.value),"minimizing cutoff");
   assert(f.radial(point[2],point[1]).eq(f.initialValue(point[0])),"rank cutoff");
   assert(f.radial(ONE,point[1]).cmp(f.initialValue(point[0]))>=0,"hinge branch");
   assert(answer.weights.every(w=>w.cmp(0)>0),"interior stationary point");
  }
  branchReports.push({branch,matrix:matrix.map(row=>row.map(x=>x.str())),minimum_four_gap:answer.value.str(),gap_decimal:answer.value.num()/4,
    point:point.map(x=>x.str()),point_decimal:point.map(x=>x.num()),weights:answer.weights.map(x=>x.str()),cost_at_minimizer:physical.str(),cost_decimal:physical.num(),
    faces:answer.faces,singular:answer.singular});
 }
 const a=Q("1/32"),s=Q("273/320"),cost=negativeEarly(f,a,s);
 return{status:"PASS",scope:"Independent exact V8 reconstruction of continuous response failures on a supplied field; no unrestricted game bound or saddle certificate.",
  source:"endpoint_joint_i1_field.json",nodes:f.nodes.length,triangles:f.triangles.length,endpoint_reference:reference.str(),
  fixed_one:{families,quadratic_checks:families.reduce((n,x)=>n+x.quadratic_checks,0),physical_checks:families.reduce((n,x)=>n+x.capture_checks,0)},
  early_m3:{source_checks:m3Checks,witness:{a:a.str(),s:s.str(),cost:cost.str(),gap:cost.s(reference).str()},tetrahedron:vertices.map(p=>p.map(x=>x.str())),polynomial_checks:polynomialChecks,capture_checks:captureChecks,branches:branchReports},
  quadratic_fixtures:fixtures.length+1,general_i:runGeneralIAudit(f),center_i:runCenterIAudit(f)};
}

function generalICost(f,z,v,s){
 z=Q(z);v=Q(v);s=Q(s);
 const A=f.initialValue(z),l=f.radial(z,v),B=s.s(v).eq(2)?ONE:f.radial(s,v);
 const twoPs=s.m(2).m(l).s(f.integral(s,maxQ(s.neg(),s.s(2)),s,0,l));
 const high=f.integral(v,z,s,1).s(A.m(s.s(z))).a(f.integral(v,z,s,1,A));
 return f.integral(z,z.neg(),z,0).s(z.a(v).m(l)).s(f.integral(z,v,z,0)).a(twoPs)
  .a(s.a(3).m(2).m(ONE.s(A))).s(s.a(6).s(v).m(maxQ(0,B.s(A)))).s(high)
  .a(s.m(2)).a(2).s(f.integral(s,s,s.a(2),1)).dby(4);
}
function generalIRoute(z,v,s){z=Q(z);v=Q(v);s=Q(s);return[[ZERO,z],[z.a(v).dby(2),z.s(v).dby(2)],[s.a(v).dby(2),s.s(v).dby(2)],[s.a(1),Q(-1)],[s.a(3),ONE]];}
function characteristicRoots(f,fixed,left,right,axis,level){
 let cuts=[left,right],other=1-axis;
 for(let {ps} of f.triangles){
  if(minQ(...ps.map(p=>p[axis])).cmp(fixed)>0||maxQ(...ps.map(p=>p[axis])).cmp(fixed)<0)continue;
  for(let i=0;i<3;i++){let a=ps[i],b=ps[(i+1)%3];if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(let p of[a,b])if(p[other].cmp(left)>0&&p[other].cmp(right)<0)cuts.push(p[other]);}
   else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&maxQ(a[axis],b[axis]).cmp(fixed)>=0){let x=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));if(x.cmp(left)>0&&x.cmp(right)<0)cuts.push(x);}
  }
 }
 cuts=uniq(cuts);let roots=[left,right],at=x=>axis===0?f.radial(fixed,x):f.radial(x,fixed);
 for(let i=0;i<cuts.length-1;i++){let a=cuts[i],b=cuts[i+1],fa=at(a).s(level),fb=at(b).s(level);if(fa.eq(0))roots.push(a);if(fb.eq(0))roots.push(b);if(fa.m(fb).cmp(0)<0)roots.push(a.a(b.s(a).m(fa).dby(fa.s(fb))));}
 return uniq(roots);
}
function generalILift(f,z,v,s,b,c,branch){
 let A=f.initialValue(z),l=f.radial(z,v),B=s.s(v).eq(2)?ONE:f.radial(s,v);
 return f.integral(z,z.neg(),z,0).a(s.m(4)).a(8).a(s.a(c).s(z).s(v).m(l)).s(s.a(b).a(6).m(A))
  .s(Q(branch).m(s.a(6).s(v)).m(B.s(A))).s(f.integral(z,v,z,0)).a(f.integral(s,c,s,0))
  .s(f.integral(v,b,s,1)).s(f.integral(s,s,s.a(2),1));
}
function runGeneralIAudit(f){
 let physicalChecks=0,liftChecks=0,endpointChecks=0,postOneChecks=0;
 for(let zz of["1/8","1/4","9/16","13/16","15/16","1"]){let z=Q(zz);
  for(let rr of["0","1/4","1/2","3/4"]){let v=z.neg().a(z.m(2).m(Q(rr)));
   for(let tt of["0","1/4","1/2","3/4","1"]){let s=z.a(v.a(2).s(z).m(Q(tt))),cost=generalICost(f,z,v,s);
    assert(cost.eq(f.unitRoutePayoff(generalIRoute(z,v,s))),"general I physical identity");physicalChecks++;
    if(s.s(v).eq(2))endpointChecks++;if(s.cmp(1)>0)postOneChecks++;
    if(rr==="1/4"&&tt!=="0"){
     let bs=characteristicRoots(f,v,z,s,1,f.initialValue(z)),cs=characteristicRoots(f,s,v,minQ(s,ONE),0,f.radial(z,v)),best=null;
     for(let b of bs)for(let c of cs)for(let j of[0,1]){let value=generalILift(f,z,v,s,b,c,j);if(best===null||value.cmp(best)<0)best=value;}
     assert(best.eq(cost.m(4)),"general I minimum of lifts");liftChecks++;
    }
   }
  }
 }
 return{scope:"Interior first turn -z<=v<z; endpoint second turns use closed B=1. No center-turn extension is asserted.",
  physical_checks:physicalChecks,cutoff_lift_checks:liftChecks,endpoint_second_turn_checks:endpointChecks,post_one_second_turn_checks:postOneChecks};
}

function centerICost(f,z,s){
 const A=f.initialValue(z),Z=f.radial(z,z),B=s.s(z).eq(2)?ONE:f.radial(s,z);
 const first=f.integral(z,z,s,1).s(A.m(s.s(z))).a(f.integral(z,z,s,1,A));
 const last=f.integral(s,s,s.a(2),1).s(Z.m(2)).a(f.integral(s,s,s.a(2),1,Z));
 return f.integral(z,z.neg(),z,0).a(s.m(4)).a(8).s(s.m(2).a(2).s(z.m(2)).m(Z)).s(s.m(2).a(6).m(A))
  .s(s.a(6).s(z).m(maxQ(0,B.s(A)))).s(first).s(last).dby(4);
}
function centerILift(f,z,s,b,d,branch){
 const A=f.initialValue(z),Z=f.radial(z,z),B=s.s(z).eq(2)?ONE:f.radial(s,z);
 return f.integral(z,z.neg(),z,0).a(s.m(4)).a(8).a(z.m(2).s(s).s(d).m(Z)).s(s.a(b).a(6).m(A))
  .s(Q(branch).m(s.a(6).s(z)).m(B.s(A))).s(f.integral(z,b,s,1)).s(f.integral(s,d,s.a(2),1));
}
function runCenterIAudit(f){
 let checks=0,liftChecks=0;
 for(let zz of["0","1/8","1/4","9/16","13/16","15/16","1"]){let z=Q(zz);
  for(let tt of["0","1/4","1/2","3/4","1"]){let s=z.a(Q(2).m(Q(tt))),a=centerICost(f,z,s);
   assert(a.eq(f.unitRoutePayoff(generalIRoute(z,z,s))),"center first-turn capture");checks++;
  }
  const s=ONE,bs=characteristicRoots(f,z,z,s,1,f.initialValue(z)),d=Q(3);let best=null;
  for(let b of bs)for(let j of[0,1]){let x=centerILift(f,z,s,b,d,j);if(best===null||x.cmp(best)<0)best=x;}
  assert(best.eq(centerICost(f,z,s).m(4)),"center fixed-one lift");liftChecks++;
 }
 return {scope:"Continuous interior field, correct closed center and endpoint capture; first-turn center face checked separately.",
  physical_checks:checks,fixed_second_one_lift_checks:liftChecks};
}

if(!process.argv[2])throw Error("Supply a field JSON path");
const report=runAudit(JSON.parse(fs.readFileSync(process.argv[2],"utf8")));
const output=JSON.stringify(report,null,2)+"\n";
if(process.argv[3])fs.writeFileSync(process.argv[3],output);
process.stdout.write(output);
