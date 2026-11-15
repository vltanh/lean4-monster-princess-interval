"use strict";
function verifyAffineRecordPrefix(A){
 const Q=A.Q,Z=Q(0),rates=[["1/3","2/5"],["1","1"],["7/4","1/9"],["2/7","11/3"]],counts={closed_identities:0,physical_integrals:0,physical_segments:0,unit_legs:0,hessian_entries:0,budget_vertices:0,three_level_checks:0,polytope_comparisons:0};
 function eq(x,y,msg){if(!x.eq(y))throw Error(msg+": "+x.str()+" != "+y.str());}
 function le(x,y,msg){if(x.cmp(y)>0)throw Error(msg);}
 const h=Q("1/997");
 for(const [ps,ms] of rates)for(let n=2;n<=12;n++){
   const p=Q(ps),m=Q(ms),k=Q(1).div(p).add(Q(1).div(m)),xs=Array.from({length:n},(_,i)=>Q(Math.floor(i/2)+2+(i%2)));
   for(const [a,b] of [[0,0],["1/7","1/11"],[1,2]]){
     const d=A.directMoment(xs,p,m,a,b),c=A.closedMoment(xs,p,m,a,b);eq(d.moment,c.moment,"telescoping moment");eq(d.time,c.time,"travel identity");counts.closed_identities+=2;
     const phys=A.physicalMoment(xs,p,m,a,b);eq(d.moment,phys.moment,"physical first-capture integral");counts.physical_integrals++;counts.physical_segments+=phys.segments;
   }
   const phys=A.physicalPath(xs,p,m);for(let j=1;j<phys.path.length;j++){let dx=phys.path[j].x.sub(phys.path[j-1].x);if(dx.cmp(0)<0)dx=dx.neg();eq(dx,phys.path[j].t.sub(phys.path[j-1].t),"unit physical leg");counts.unit_legs++;}
   const f=A.closedMoment(xs,p,m).moment;
   for(let i=0;i<n-2;i++)for(let j=i;j<n-2;j++){
     let value;
     if(i===j){let xp=xs.slice(),xm=xs.slice();xp[i]=xp[i].add(h);xm[i]=xm[i].sub(h);value=A.closedMoment(xp,p,m).moment.add(A.closedMoment(xm,p,m).moment).sub(f.mul(2)).div(h.mul(h));}
     else {let total=Z;for(let si of [-1,1])for(let sj of [-1,1]){let x=xs.slice();x[i]=x[i].add(h.mul(si));x[j]=x[j].add(h.mul(sj));total=total.add(A.closedMoment(x,p,m).moment.mul(si*sj));}value=total.div(h.mul(h).mul(4));}
     eq(value,i===j?k.mul(-2):j===i+1?k.neg():Z,"exact Hessian");counts.hessian_entries++;
   }
 }
 for(let n=2;n<=12;n++)for(const [a,b] of [[0,0],["1/7","1/11"]])for(let kind=0;kind<5;kind++){
   const upper=Q(3),lower=Q(2),m=n-2,x=Array(m);
   for(let parity=0;parity<2;parity++){let inds=Array.from({length:m},(_,i)=>i).filter(i=>i%2===parity),lo=Q(parity?b:a),hi=parity?lower:upper;inds.forEach((i,j)=>x[i]=lo.add(hi.sub(lo).mul(Q(j+1).div(inds.length+1))));}
   x.push((n-2)%2?lower:upper,(n-1)%2?lower:upper);
   const current=x.slice(0,m).reduce((s,v)=>s.add(v),Z),budget=current.add(Q(kind).div(7)),vs=A.budgetVertices(n,upper,lower,budget,a,b);
   if(!vs.length)throw Error("empty feasible vertex set");
   for(let v of vs){counts.budget_vertices++;le(v.slice(0,m).reduce((s,q)=>s.add(q),Z),budget,"budget vertex feasibility");if(A.productiveCount(v,a,b)>3)throw Error("more than three productive levels");counts.three_level_checks++;}
   for(const [p,q]of rates){const f=A.closedMoment(x,p,q,a,b).moment;let best=vs.map(v=>A.closedMoment(v,p,q,a,b).moment).reduce((u,v)=>u.cmp(v)<=0?u:v);le(best,f,"vertex does not dominate feasible interior");counts.polytope_comparisons++;}
 }
 return {status:"PASS",scope:"Exact affine-cell moment, physical capture integration, fixed-budget chain vertices. No two-cell or global-prefix assertion.",counts};
}
module.exports={verifyAffineRecordPrefix};

if(typeof require!=="undefined"&&require.main===module){const A=require("./affine_record_prefix.cjs");console.log(JSON.stringify(verifyAffineRecordPrefix(A),null,2));}
