"use strict";
function verifyInterfaceEpoch(A){
 const Q=A.Q,Z=Q(0),counts={scale_identities:0,cone_margins:0,opposing_trace_bounds:0,productive_duration_implications:0};
 const min=(a,b)=>a.cmp(b)<=0?a:b,max=(a,b)=>a.cmp(b)>=0?a:b;
 function le(a,b,msg){if(a.cmp(b)>0)throw Error(msg);}
 const rates=[["1/8","1/4"],["1/4","1/2"],["1/4","1"],["1/4","2"],["3/4","1"],["1","3"]];
 for(const[a,b]of rates)for(const rs of ["1/64","1/7","1/2","1","3"])for(const ds of ["1/128","1/8","1","4"]){
   const alpha=Q(a),B=Q(b),C=B.sub(alpha),gamma=B.div(C).add(Q("1/2")),R=Q(rs),Delta=Q(ds),H=Q(4),h=min(Delta,R.div(2)),d=h.div(gamma);
   const ratio=R.div(d),rhs=gamma.mul(max(R.div(Delta),Q(2)));
   if(ratio.cmp(rhs))throw Error("scale cancellation");le(ratio,gamma.mul(max(H.div(Delta),Q(2))),"global-horizon replacement");counts.scale_identities+=2;
   le(h,Delta,"stationary-neighbor margin");le(h.mul(2),R,"approaching-characteristic margin");le(d.mul(gamma),h,"persistence");counts.cone_margins+=3;
   for(const frac of ["1/8","1/3","1/2","3/4"]){
     const u=d,q=R.sub(d).mul(Q(frac));if(q.cmp(0)<=0)continue;
     const lower=alpha.mul(u).sub(C.mul(q).div(2));
     const templates=[
      [[Z,Z],[q.div(2),q.div(2).neg()],[q,Z]],
      [[Z,Z],[q.div(4),q.div(4).neg()],[q.mul(3).div(4),q.div(4).neg()],[q,Z]],
      [[Z,Z],[q.div(4),q.div(4).neg()],[q.div(2),Z],[q.mul(3).div(4),q.div(4).neg()],[q,Z]]
     ];
     for(const p of templates){let trace=Z;for(const[t,x]of p){let f=alpha.mul(u.add(t)).add(B.mul(x));if(f.cmp(trace)<0)trace=f;le(lower,f,"opposing CDF envelope");counts.opposing_trace_bounds++;}
      if(trace.cmp(0)<0){le(alpha.mul(d).mul(2).div(C),q,"productive duration");counts.productive_duration_implications++;}
     }
   }
 }
 return{status:"PASS",scope:"Fixed-interface epoch and scale cancellation only; no global atlas-count theorem.",counts};
}
module.exports={verifyInterfaceEpoch};
if(typeof require!=="undefined"&&require.main===module){const A=require("./affine_record_prefix.cjs");console.log(JSON.stringify(verifyInterfaceEpoch(A),null,2));}
