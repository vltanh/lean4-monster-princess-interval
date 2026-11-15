/**
 * Separate ordinary upper companion of a finite bounded-coordinate germ law.
 * Collapse is exact; it does not preserve payoffs against varying Princesses.
 */
module.exports = (function(){
function createCollapsedCompanion(E,G){
 const Q=G.Q,Z=G.ZERO,O=G.ONE;
 function gcd(a,b){while(b){const t=a%b;a=b;b=t;}return a<0n?-a:a;}
 function physical(points){return points.map(([u,v])=>[u.a(v).dby(2),u.s(v).dby(2)]);}
 function readLight(atom){
  if(atom&&Array.isArray(atom.exact_light))return atom.exact_light.map(r=>r.map(Q));
  const p=atom&&atom.exact_path||atom&&atom.route||atom;
  if(!Array.isArray(p))throw Error("atom requires exact_light or physical route");
  return p.map(([t,x])=>{t=Q(t);x=Q(x);return[t.a(x),t.s(x)];});
 }
 function collapseRoute(atom,{complete=true,mergeCollinear=true}={}){
  const input=readLight(atom);
  if(!input.length)throw Error("empty Monster route");
  if(!input[0][0].a(input[0][1]).eq(0))throw Error("Monster must start at time zero");
  let inputLeft=false,inputRight=false,inputNonunit=0;
  for(let j=0;j<input.length;j++){
   const[u,v]=input[j],t=u.a(v),x=u.s(v);
   if(t.cmp(0)<0||x.cmp(-2)<0||x.cmp(2)>0)throw Error("nonphysical Monster vertex");
   u.limit();v.limit();
   if(x.eq(-2))inputLeft=true;if(x.eq(2))inputRight=true;
   if(j){
    const du=u.s(input[j-1][0]),dv=v.s(input[j-1][1]);
    if(du.cmp(0)<0||dv.cmp(0)<0)throw Error("illegal Monster speed or time order");
    if(du.cmp(0)>0&&dv.cmp(0)>0)inputNonunit++;
   }
  }
  if(complete&&(!inputLeft||!inputRight))throw Error("original Monster route lacks endpoint completion");
  const limits=input.map(r=>r.map(x=>x.limit())),out=[],sourceVertices=[];
  let zeroDuration=0,collinear=0;
  for(let j=0;j<limits.length;j++){
   const p=limits[j],last=out.at(-1);
   if(last&&p[0].eq(last[0])&&p[1].eq(last[1])){zeroDuration++;continue;}
   if(last){
    const du=p[0].s(last[0]),dv=p[1].s(last[1]);
    if(du.cmp(0)<0||dv.cmp(0)<0)throw Error("limiting light coordinates are not monotone");
    if(du.a(dv).eq(0))throw Error("distinct equal-time limiting vertices");
   }
   if(mergeCollinear)while(out.length>=2){
    const a=out[out.length-2],b=out[out.length-1],
     u1=b[0].s(a[0]),v1=b[1].s(a[1]),u2=p[0].s(b[0]),v2=p[1].s(b[1]);
    if(!u1.m(v2).eq(v1.m(u2)))break;
    out.pop();sourceVertices.pop();collinear++;
   }
   out.push(p);sourceVertices.push(j);
  }
  let left=false,right=false,nonunit=0;
  for(let j=0;j<out.length;j++){
   const[u,v]=out[j],x=u.s(v);
   if(x.eq(-2))left=true;if(x.eq(2))right=true;
   if(j&&!u.eq(out[j-1][0])&&!v.eq(out[j-1][1]))nonunit++;
  }
  if(complete&&(!left||!right))throw Error("endpoint completion lost under collapse");
  if(!inputNonunit&&nonunit)throw Error("unit legs acquired a nonunit limit");
  return{
   exact_light:out.map(r=>r.map(x=>x.str())),
   exact_path:physical(out).map(r=>r.map(x=>x.str())),
   audit:{input_vertices:input.length,output_vertices:out.length,
    collapsed_zero_duration_segments:zeroDuration,removed_collinear_vertices:collinear,
    input_nonunit_segments:inputNonunit,limit_nonunit_segments:nonunit,
    source_vertices:sourceVertices,complete:left&&right,
    limiting_horizon:physical(out).at(-1)[0].str(),
    standard_atomic_supported:left&&right&&nonunit===0},
   radius:G.stats().radius
  };
 }
 function collapseLaw(atoms,weights,{complete=true,mergeReflections=true,mergeCollinear=true}={}){
  if(!Array.isArray(atoms)||!atoms.length||weights.length!==atoms.length)throw Error("law dimensions");
  const ws=weights.map(Q);let total=Z;
  for(const w of ws){if(w.cmp(0)<0)throw Error("negative eventual probability");total=total.a(w);}
  if(!total.eq(1))throw Error("probabilities must sum exactly to one");
  const groups=[],byKey=new Map(),zeroWeights=[],routeAudits=[];
  for(let j=0;j<atoms.length;j++){
   const w=ws[j].limit();
   if(ws[j].eq(0)){zeroWeights.push({index:j,reason:"identically zero"});continue;}
   const r=collapseRoute(atoms[j],{complete,mergeCollinear});routeAudits.push({index:j,...r.audit});
   if(w.eq(0)){zeroWeights.push({index:j,reason:"positive germ with zero limit"});continue;}
   let light=r.exact_light,flipped=false,key=JSON.stringify(light);
   if(mergeReflections){
    const reflect=light.map(([u,v])=>[v,u]),other=JSON.stringify(reflect);
    if(other<key){light=reflect;key=other;flipped=true;}
   }
   let id=byKey.get(key);
   if(id===undefined){id=groups.length;byKey.set(key,id);groups.push({exact_light:light,weight:w,source_indices:[],reflected_indices:[],audit:r.audit});}
   else groups[id].weight=groups[id].weight.a(w);
   groups[id].source_indices.push(j);if(flipped)groups[id].reflected_indices.push(j);
  }
  if(!groups.length)throw Error("empty limiting probability law");
  let D=1n;for(const g of groups)D=D/gcd(D,g.weight.d)*g.weight.d;
  const nums=groups.map(g=>g.weight.n*(D/g.weight.d));
  if(nums.reduce((a,b)=>a+b,0n)!==D)throw Error("limiting probability mass");
  let common=D;for(const n of nums)common=gcd(common,n);D/=common;
  const ordinaryAtoms=groups.map(g=>({exact_light:g.exact_light,source_indices:g.source_indices,reflected_indices:g.reflected_indices})),
   ordinaryWeights=groups.map(g=>g.weight.str());
  return{
   scope:"Separate ordinary collapsed companion; no varying-Princess payoff equivalence is asserted.",
   atoms:ordinaryAtoms,weights:ordinaryWeights,
   weight_numerators:nums.map(n=>String(n/common)),weight_denominator:String(D),
   input_atom_count:atoms.length,output_atom_count:groups.length,
   dropped_zero_weights:zeroWeights,route_audits:routeAudits,
   standard_atomic_supported:groups.every(g=>g.audit.standard_atomic_supported),
   relation:"U(companion) <= liminf U(original germ law)",
   radius:G.stats().radius
  };
 }
 function standardResponse(law,{exact=true,verifyFlow=true,retainModel=false,tolerance=2e-13,retainFace=true}={}){
  if(!law.standard_atomic_supported)throw Error("collapsed law is legal, but the standard atomic engine requires complete unit-leg routes; a genuinely nonunit limit is not silently replaced");
  const model=new E.Rational.Model(law.atoms);
  if(exact){
   const result=E.Integer.solveIntegerLaw(E.Cut,E.Physical,E.BigFlow.BigFlow,model,law.weight_numerators,law.weight_denominator),
    replay=verifyFlow?E.Integer.verifyIntegerFlow(E.Cut,E.Physical,E.BigFlow.BigFlow,model,law.weight_numerators,law.weight_denominator,result.flowCertificate):null;
   if(replay&&replay.exactValue!==result.exactValue)throw Error("ordinary companion certificate replay mismatch");
   return{scope:"Exact unrestricted response of the separate ordinary collapsed law.",
    exact:true,value:result.exactValue,decimal:result.value,result,flow_replay:replay,
    ...(retainModel?{model}:{})};
  }
  const weights=law.weights.map(w=>Q(w).limit().num()),result=model.solve(weights,tolerance,retainFace);
  return{scope:"Numerical response of the separate ordinary collapsed law; no flow certificate.",
   exact:false,value:result.value,result,...(retainModel?{model}:{})};
 }
 function companion(atoms,weights,options={}){
  const law=collapseLaw(atoms,weights,options),response=standardResponse(law,options);
  return{law,response};
 }
 return{readLight,collapseRoute,collapseLaw,standardResponse,companion};
}
return{createCollapsedCompanion};
})();