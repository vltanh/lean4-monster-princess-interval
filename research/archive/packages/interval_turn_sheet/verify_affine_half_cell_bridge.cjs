"use strict";
function verifyHalfCellBridge(A,M){
 const Q=A.Q,E=M.createHalfCellBridgeTools(A),Z=Q(0),checks={earliest_target_cases:0,physical_legs:0,old_path_arrivals:0,first_contact_comparisons:0,right_bridge_bounds:0};
 function le(a,b,msg){if(a.cmp(b)>0)throw Error(msg);}
 function legal(p){for(let i=0;i<p.length;i++){if(p[i][1].cmp(0)>0)throw Error("left cell escape");if(i){let dt=p[i][0].sub(p[i-1][0]),dx=p[i][1].sub(p[i-1][1]);if(dx.cmp(0)<0)dx=dx.neg();le(dx,dt,"speed");checks.physical_legs++;}}}
 const rates=[["1/8","1/4"],["1/4","1/2"],["1/4","1"],["1/4","2"],["3/4","1"],["0","1"]];
 for(const[a,b]of rates)for(const t of [0,"1/4","1/2"])for(const x of [0,"-1/16","-1/4"]){
  const alpha=Q(a),B=Q(b),q0=alpha.mul(Q(t)).add(B.mul(Q(x)));
  for(const d of ["-1/3","-1/17",0,"1/19","1/2"]){const q=q0.add(Q(d));if(alpha.eq(0)&&q.cmp(0)>0)continue;const r=E.earliestLeft(t,x,q,alpha,B);legal(r.path);if(!alpha.mul(r.time).add(B.mul(r.x)).eq(q))throw Error("wrong rank");checks.earliest_target_cases++;}
 }
 const templates=[
 [[0,0],["1/4","-1/4"],["1/2","-1/8"],["3/4","-3/16"],[1,"-1/8"]],
 [[0,0],["1/8","-1/32"],["1/4","-1/16"],["3/8","-3/16"],["1/2","-1/16"],["3/4","-1/4"],[1,0]],
 [[0,0],["1/4",0],["1/2","-1/8"],["3/4","-1/8"],[1,"-1/16"]],
 [[0,0],["1/8","-1/8"],["1/4",0],["1/2","-1/4"],["3/4",0],[1,"-1/4"]]
 ].map(p=>p.map(v=>v.map(Q)));
 for(const[a,b]of rates)for(const p of templates){
  const alpha=Q(a),B=Q(b),r=E.accelerate(p,alpha,B);legal(r.path);for(let i=0;i<r.arrivals.length;i++){le(r.arrivals[i],p[i+1][0],"arrival");checks.old_path_arrivals++;}
  let cuts=new Map([...p,...r.path].map(([t,x])=>{let q=alpha.mul(t).add(B.mul(x));return[q.str(),q];})),qs=[...cuts.values()].sort((x,y)=>x.cmp(y)),test=qs.slice();for(let i=0;i+1<qs.length;i++)test.push(qs[i].add(qs[i+1]).div(2));
  for(const q of test){const old=E.firstHit(p,q,alpha,B);if(old===null)continue;const now=E.firstHit(r.path,q,alpha,B);if(now===null)throw Error("lost rank");le(now,old,"capture delayed");checks.first_contact_comparisons++;}
 }
 for(const xe of [0,"1/8","1/2",1])for(const f of ["0","1/4","1/2","3/4",1]){
  const x=Q(xe),z=Q(f),p=templates[0].map(([t,v])=>[t,v.neg().mul(Q(1).sub(x)).mul(z).add(t.mul(x))]),bridge=E.rightBridge(1,x);
  /* A convex combination of a right loop and the endpoint line is nonnegative and legal; use a loop with zero endpoint. */
  const loop=templates[3].map(([t,v])=>[t,v.neg()]);loop[loop.length-1][1]=Z;
  const path=loop.map(([t,v])=>[t,v.mul(Q(1).sub(x)).mul(z).add(t.mul(x))]);
  function interp(p,t){for(let i=0;i+1<p.length;i++)if(t.cmp(p[i+1][0])<=0)return p[i][1].add(p[i+1][1].sub(p[i][1]).mul(t.sub(p[i][0])).div(p[i+1][0].sub(p[i][0])));return p[p.length-1][1];}
  for(const t of [...path.map(v=>v[0]),...bridge.map(v=>v[0])]){le(interp(path,t),interp(bridge,t),"maximal right bridge");checks.right_bridge_bounds++;}
 }
 return {status:"PASS",scope:"Constrained earliest travel and pointwise final bridge; local finite-piece theorem also uses the affine Hessian and separately verified interface-return theorem.",checks};
}
module.exports={verifyHalfCellBridge};
if(typeof require!=="undefined"&&require.main===module){const A=require("./affine_record_prefix.cjs"),M=require("./affine_half_cell_bridge.cjs");console.log(JSON.stringify(verifyHalfCellBridge(A,M),null,2));}
