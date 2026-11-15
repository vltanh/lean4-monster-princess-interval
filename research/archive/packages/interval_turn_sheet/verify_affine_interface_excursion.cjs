"use strict";
function verifyInterfaceExcursion(A,M){
 const E=M.createInterfaceExcursionTools(A),Q=A.Q,Z=Q(0);
 let checks={algebraic_bounds:0,capture_order_traces:0,arbitrary_excursions:0,old_record_cases:0,physical_integrals:0,physical_segment_inspections:0,nonproductive_wait_checks:0,right_tent_checks:0};
 function ge(a,b,label){if(a.cmp(b)<0)throw Error(label+": "+a.str()+" < "+b.str());}
 const rates=[["0","1"],["1/8","1/4"],["1/4","1/2"],["1/4","1"],["1/4","2"],["3/4","1"],["3/4","2"],["1","3"]];
 for(const [al,be]of rates)for(let j=0;j<=64;j++){
   const a=Q(al),B=Q(be),T=Q("7/5"),L=B.sub(a).mul(T).mul(j).div(128),b=E.bounds(a,B,T,L);
   ge(b.bound,b.margin,"integrated capture-order lower bound");checks.algebraic_bounds++;
   if(a.cmp(0)>0)for(const h of [Z,b.hstar,b.hc,a.mul(T),b.hstar.add(b.hc).div(2)]){
     let early=h.div(a),after=h.div(b.D).add(B.mul(L).mul(2).div(b.C.mul(b.D))),lower=h.cmp(b.hstar)<=0?early:(early.cmp(after)>=0?early:after),tent=h.add(B.mul(T)).div(b.D);
     ge(tent,lower,"rankwise upper deficit has correct sign");checks.capture_order_traces++;
   }
 }
 function triangle(start,duration){return [[start,0],[Q(start).add(Q(duration).div(2)),Q(duration).div(2).neg()],[Q(start).add(duration),0]].map(p=>p.map(Q));}
 function joined(durations,wait=0){let t=Q(wait),p=[[Z,Z]];if(t.cmp(0)>0)p.push([t,Z]);for(const d of durations){const tri=triangle(t,d);p.push(...tri.slice(1));t=t.add(d);}if(t.cmp(1)<0)p.push([Q(1),Z]);return p;}
 let paths=[
 joined([1]),joined(["1/2"]),joined(["1/2"],"1/2"),joined(["1/2"],"1/4"),joined(["1/4","3/4"]),joined(["1/3","1/3","1/3"]),joined(["1/8","1/8","1/4","1/2"]),
 [["0","0"],["1/8","-1/8"],["1/4","-1/16"],["3/8","-3/16"],["1/2","-1/8"],["3/4","-1/4"],["1","0"]].map(p=>p.map(Q)),
 [["0","0"],["1/4","-1/4"],["3/4","-1/4"],["1","0"]].map(p=>p.map(Q))
 ];
 function interp(p,t){for(let i=0;i+1<p.length;i++)if(t.cmp(p[i+1][0])<=0)return p[i][1].add(p[i+1][1].sub(p[i][1]).mul(t.sub(p[i][0])).div(p[i+1][0].sub(p[i][0])));throw Error("interpolation domain");}
 const p0=paths[0],p1=paths[7];
 for(const f of ["1/5","1/2","4/5"]){let grid=new Map([...p0,...p1].map(p=>[p[0].str(),p[0]])),ts=[...grid.values()].sort((a,b)=>a.cmp(b)),z=Q(f);paths.push(ts.map(t=>[t,interp(p0,t).mul(z).add(interp(p1,t).mul(Q(1).sub(z)))]));}
 for(const [al,be]of rates)for(const path of paths){
   E.validate(path);const a=Q(al),B=Q(be);let L=Z;for(const[t,x]of path){let q=a.mul(t).add(B.mul(x)).neg();if(q.cmp(L)>0)L=q;}if(L.cmp(0)<=0)continue;checks.arbitrary_excursions++;
   for(const oldL of [Z,L.div(3),L.mul(2).div(3)])for(const oldH of [Z,a.div(3),a.mul(2).div(3),a.mul(2)]){
     const r=E.compare(path,a,B,oldL,oldH);ge(r.difference,r.margin,"full physical changed-rank comparison");checks.old_record_cases++;checks.physical_integrals+=2;checks.physical_segment_inspections+=r.old.segments+r.new.segments;
   }
   if(a.cmp(0)>0){const upper=E.moment(path,a,B,Z,a,L,Z),wait=E.moment([[Z,Z],[Q(1),Z]],a,B,Z,a,L,Z);ge(upper.value,wait.value,"nonproductive-lower excursion versus interface wait");checks.nonproductive_wait_checks++;}
 }
 /* The positive maximal tent is a pointwise upper envelope on each common PL cell. */
 for(const path of paths){let pos=path.map(([t,x])=>[t,x.neg()]),cuts=new Map([...pos.map(p=>p[0]),Q("1/2")].map(t=>[t.str(),t]));for(const t of cuts.values()){let tent=t.cmp("1/2")<=0?t:Q(1).sub(t);ge(tent,interp(pos,t),"right tent envelope");checks.right_tent_checks++;}}
 return {status:"PASS",scope:"Arbitrary confined-left excursion dominance with a fixed continuation and explicit affine future persistence; no global finite-prefix assertion.",checks};
}
module.exports={verifyInterfaceExcursion};
if(typeof require!=="undefined"&&require.main===module){const A=require("./affine_record_prefix.cjs"),M=require("./affine_interface_excursion.cjs");console.log(JSON.stringify(verifyInterfaceExcursion(A,M),null,2));}
