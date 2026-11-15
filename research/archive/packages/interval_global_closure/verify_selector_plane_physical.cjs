"use strict";
/* Independent exact physical audit of selector_plane_oracle.cjs.
 * The checker integrates signed pair CDFs by exact affine sign-measure lengths,
 * independently of the compiler's split-and-midpoint integrator.
 */
function auditSelector(A,P,packets){
 const Q=A.Q,Z=Q(0),half=Q("1/2");
 const cmp=(a,b)=>Q(a).cmp(Q(b)),add=(a,b)=>Q(a).a(Q(b)),sub=(a,b)=>Q(a).s(Q(b)),mul=(a,b)=>Q(a).m(Q(b)),div=(a,b)=>Q(a).dby(Q(b));
 function expand(packet){if(!packet.planes)return packet;let total=packet.planes.reduce((s,p)=>s.a(Q(p.weight??1)),Z),constant=Z,points=[],rays=[];for(const p of packet.planes){const w=Q(p.weight??1).dby(total),r=p.route.map(v=>v.map(Q));for(let j=0;j+1<r.length;j++){const dt=r[j+1][0].s(r[j][0]);if(dt.eq(0))continue;const sel=p.selectors.find(s=>s.leg===j),cut=Q(sel.cut),before=cut.s(r[j][0]),sgn=r[j+1][1].cmp(r[j][1]),l=r[sel.lower_index],h=r[sel.upper_index];constant=constant.a(w.m(dt));points.push({time:l[0].str(),position:l[1].str(),coefficient:w.m(sgn>0?dt:before).str(),trace:"strict"});points.push({time:h[0].str(),position:h[1].str(),coefficient:w.m(sgn>0?before:dt).neg().str(),trace:"closed"});rays.push({start_time:cut.str(),end_time:r[j+1][0].str(),start_position:r[j][1].a(cut.s(r[j][0]).m(sgn)).str(),direction:sgn,coefficient:w.m(-sgn).str(),trace:sgn>0?"closed":"strict"});}}return{constant:constant.str(),points,rays};}
 function independentScore(packet,path){packet=expand(packet);
  const v=path.map(p=>p.map(Q));
  function at(t){t=Q(t);for(let i=0;i+1<v.length;i++)if(t.cmp(v[i+1][0])<=0)return v[i][1].a(v[i+1][1].s(v[i][1]).m(t.s(v[i][0])).dby(v[i+1][0].s(v[i][0])));return v.at(-1)[1];}
  function atom(t,x,trace){t=Q(t);x=Q(x);const r=at(t);let n=0;for(const q of[r,r.neg()])if(q.cmp(x)<0||(q.eq(x)&&trace==="closed"))n++;return Q(n).dby(2);}
  let out=Q(packet.constant??0);
  for(const p of packet.points??[])out=out.a(Q(p.coefficient).m(atom(p.time,p.position,p.trace)));
  for(const r of packet.rays??[]){
   const t0=Q(r.start_time),t1=Q(r.end_time),x0=Q(r.start_position),dir=Q(r.direction),bs=[t0,t1];
   for(const [t]of v)if(t.cmp(t0)>0&&t.cmp(t1)<0)bs.push(t);
   bs.sort((a,b)=>a.cmp(b));
   let integral=Z;
   for(let k=0;k+1<bs.length;k++){
    const l=bs[k],h=bs[k+1];if(l.eq(h))continue;
    const xl=x0.a(dir.m(l.s(t0))),xh=x0.a(dir.m(h.s(t0))),pl=at(l),ph=at(h);
    for(const sign of[1,-1]){
     const dl=xl.s(pl.m(sign)),dh=xh.s(ph.m(sign));
     let duration=Z;
     if(dl.eq(dh)){if(dl.cmp(0)>0||(dl.eq(0)&&r.trace==="closed"))duration=h.s(l);}
     else if(dl.cmp(0)>=0&&dh.cmp(0)>=0)duration=h.s(l);
     else if(dl.cmp(0)<=0&&dh.cmp(0)<=0)duration=Z;
     else{const f=dl.neg().dby(dh.s(dl));duration=h.s(l).m(dl.cmp(0)>0?f:Q(1).s(f));}
     integral=integral.a(duration.dby(2));
    }
   }
   out=out.a(Q(r.coefficient).m(integral));
  }
  return out;
 }
 let rng=639835201;const rand=n=>{rng=(1664525*rng+1013904223)>>>0;return rng%n;};
 const diagnostics=[];let independent=0,upper=0,realizations=0,arbitraryLabels=0;
 function pairCost(route,path){const r=route.map(v=>v.map(Q)),p=path.map(v=>v.map(Q));function val(vertices,t){for(let j=0;j+1<vertices.length;j++)if(t.cmp(vertices[j+1][0])<=0)return vertices[j][1].a(vertices[j+1][1].s(vertices[j][1]).m(t.s(vertices[j][0])).dby(vertices[j+1][0].s(vertices[j][0])));return vertices.at(-1)[1];}const end=r.at(-1)[0],ts=[...new Map([...r.map(v=>v[0]),...p.map(v=>v[0]).filter(t=>t.cmp(end)<=0)].map(t=>[t.str(),t])).values()].sort((a,b)=>a.cmp(b));let total=Z;for(const sign of[1,-1]){let hit=null;for(let j=0;j+1<ts.length;j++){let a=ts[j],b=ts[j+1],da=val(r,a).s(val(p,a).m(sign)),db=val(r,b).s(val(p,b).m(sign));if(da.eq(0)){hit=a;break;}if(db.eq(0)||da.cmp(0)*db.cmp(0)<0){hit=a.a(b.s(a).m(da.neg()).dby(db.s(da)));break;}}if(hit===null)throw Error("complete endpoint tour missed Princess");total=total.a(hit.dby(2));}return total;}
 let selectorMajorants=0;
 const staticPaths=[];for(let j=0;j<=8;j++)staticPaths.push([[0,Q(j).dby(8).str()],[5,Q(j).dby(8).str()]]);
 for(let z=0;z<80;z++){let x=rand(9),p=[[0,Q(x).dby(8).str()]];for(let k=1;k<=40;k++){x=Math.max(0,Math.min(8,x+rand(3)-1));p.push([Q(k).dby(8).str(),Q(x).dby(8).str()]);}staticPaths.push(p);}
 for(let i=0;i<packets.length;i++){
  const packet=packets[i],r=P.solve(packet);let worst=Q(-100),bestGap=null;
  for(const path of staticPaths){const s=independentScore(packet,path),t=P.physicalScore(packet,path);if(!s.eq(t))throw Error("independent capture mismatch "+i+" "+s.str()+" "+t.str());independent++;if(packet.planes){let den=packet.planes.reduce((z,p)=>z.a(Q(p.weight??1)),Z),cost=packet.planes.reduce((z,p)=>z.a(Q(p.weight??1).m(pairCost(p.route,path))),Z).dby(den);if(s.cmp(cost)<0)throw Error("selector below physical capture");selectorMajorants++;}if(s.cmp(Q(r.value))>0)throw Error("sample exceeds compiler "+i);upper++;if(s.cmp(worst)>0)worst=s;}
  for(const label of[r.closure.minimum_labels,r.closure.maximum_labels])for(const tol of["1/16","1/100000"]){
   const out=P.realize(r.compiled,label,{tolerance:tol});const s=independentScore(packet,out.path);if(!s.eq(Q(out.physical_score)))throw Error("realized score mismatch");independent++;realizations++;
   const gap=Q(r.value).s(s);if(gap.cmp(0)<0)throw Error("actual realization exceeds claimed supremum");if(gap.cmp(Q(out.error_bound))>0)throw Error("physical error envelope");if(bestGap===null||gap.cmp(bestGap)<0)bestGap=gap;
  }
  for(let k=0;k<8;k++){const labels=[];for(let j=0;j<r.compiled.rows.length;j++){const b=r.closure.bounds[j],lo=Math.max(b[0],j?labels[j-1]:0),hi=b[1];labels.push(lo+rand(hi-lo+1));}const out=P.realize(r.compiled,labels,{tolerance:"1/10000"}),s=independentScore(packet,out.path),gap=Q(out.label_score).s(s);if(!s.eq(Q(out.physical_score))||gap.cmp(Q(out.error_bound))>0)throw Error("arbitrary face realization");independent++;arbitraryLabels++;}
  diagnostics.push({id:i,value:r.value,sampled:worst.str(),realized_gap:bestGap.str(),shape:r.compiled.statistics});
 }
 return{pass:true,packets:packets.length,independent_score_checks:independent,sampled_upper_checks:upper,realizations,arbitrary_labels:arbitraryLabels,selector_majorants:selectorMajorants,diagnostics};
}
module.exports={auditSelector};
if(typeof require!=="undefined"&&require.main===module){
 (async()=>{
  const fs=require("node:fs"),path=require("node:path");
  const E=require("../interval_turn_density/atomic_survival_v8.cjs");
  const {createOracle}=await import("../interval_cdf_discovery/finite_quantile_response.mjs");
  const A=createOracle(),S=require("./signed_label_closure.cjs").createSignedLabelClosure(E);
  const P=require("./selector_plane_oracle.cjs").createSelectorPlaneOracle(A,S);
  const packets=JSON.parse(fs.readFileSync(path.join(__dirname,"selector_plane_physical_inputs.json"),"utf8"));
  process.stdout.write(JSON.stringify(auditSelector(A,P,packets),null,2)+"\n");
 })().catch(e=>{console.error(e);process.exitCode=1;});
}
