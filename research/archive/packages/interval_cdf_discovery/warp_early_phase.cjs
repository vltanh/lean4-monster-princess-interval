
function createEarlyWarpAudit(E,W){
 const {Q,ZERO,ONE}=E;
 function verify(data,solution){
  const original=new E.ExactField(data),warp=new W.WarpCoordinates(solution.knots),d=warp.validate(solution.increments),field=W.remapExactField(original,warp,d);
  const M2=(a,s)=>[[ZERO,a],[s.s(a).dby(2),s.a(a).dby(2)],[s.a(1),Q(-1)],[s.a(3),ONE]];
  const M3=(a,s,t)=>[[ZERO,a],[s.s(a).dby(2),s.a(a).dby(2)],[s.a(t).dby(2),s.s(t).dby(2)],[t.a(1),ONE],[t.a(3),Q(-1)]];
  function cost(a,s){const aa=warp.value(a,d),ss=warp.value(s,d),A=original.initialValue(a),B=original.radial(s,a.neg());return ss.m(4).a(8).a(ss.m(2).m(A)).s(ss.a(6).a(aa).m(B)).s(field.integral(aa.neg(),aa,ss,1)).s(field.integral(ss,aa.neg(),ss,0,A)).s(field.integral(ss,ss,ss.a(2),1)).dby(4);}
  const attacks=[];let physicalChecks=0,basisChecks=0;
  for(const[a,s,t]of [["1/8","15/16",null],["1/8","31/32",null],["1/8","63/64",null],["1/8","7/8","1"]]){
   const route=t?M3(Q(a),Q(s),Q(t)):M2(Q(a),Q(s)),image=warp.route(route,d),feature=W.captureFeatures(original,warp,route),actual=field.unitRoutePayoff(image),predicted=W.dot(feature.coefficients,d);
   if(!actual.eq(predicted))throw Error("independent capture identity");physicalChecks++;
   if(!t&&!actual.eq(cost(Q(a),Q(s))))throw Error("M2 moment identity");
   attacks.push({family:t?"positive_M3":"positive_M2",reference:{a,s,t},route:image.map(p=>p.map(x=>x.str())),cost:actual.str(),decimal:actual.num(),reference_cost:feature.identityCost.str()});basisChecks+=warp.n;
  }
  const a=Q("1/8"),s=Q("15/16"),h=Q("1/1073741824"),derivatives={};
  for(const axis of["a","s"]){
   const values=[-3,-2,-1,0,1,2,3].map(k=>axis==="a"?cost(a.a(h.m(k)),s):cost(a,s.a(h.m(k))));
   if(!values[0].s(values[1].m(3)).a(values[2].m(3)).s(values[3]).eq(0)||!values[3].s(values[4].m(3)).a(values[5].m(3)).s(values[6]).eq(0))throw Error("one-sided quadratic");
   const left=values[3].m(3).s(values[2].m(4)).a(values[1]).dby(h.m(2)),right=values[3].m(-3).a(values[4].m(4)).s(values[5]).dby(h.m(2));
   derivatives[axis]={left:left.str(),right:right.str(),left_decimal:left.num(),right_decimal:right.num()};
  }
  const A=original.initialValue(a),B=original.radial(s,a.neg()),Z=original.radial(s,s),ps=warp.value(s,d),H=field.integral(ps,ps,ps.a(2),1);
  if(A.cmp(Z)>=0)throw Error("F=0 branch lost");if(!H.eq(Z.m(2)))throw Error("flat beta-row moment lost");
  return{scope:"Exact rejection of the five-family warp by specified early routes; no unrestricted lower or saddle claim.",transport_triangles:field.triangles.length,physical_checks:physicalChecks,feature_score_checks:physicalChecks,feature_coefficients_evaluated:basisChecks,attacks,source:{A:A.str(),B:B.str(),Z:Z.str(),H:H.str(),F_is_zero:true,flat_beta_moment:true},one_sided_derivatives:derivatives};
 }
 return{verify};
}
module.exports={createEarlyWarpAudit};
