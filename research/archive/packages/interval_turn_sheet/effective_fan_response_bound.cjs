"use strict";
/* Exact constants for the fixed-fan finite-response theorem.
 * This module checks supplied arrangement constants. It does not construct
 * the arrangement or certify a game value.
 */
function createBoundTools(Q){
 const Z=Q(0),O=Q(1),HALF=Q("1/2"),NUNIT=17;
 const abs=x=>Q(x).cmp(0)<0?Q(x).neg():Q(x);
 const min=(a,b)=>Q(a).cmp(Q(b))<=0?Q(a):Q(b);
 const max=(a,b)=>Q(a).cmp(Q(b))>=0?Q(a):Q(b);
 const floor=q=>{q=Q(q);if(q.cmp(0)<0)throw Error("nonnegative floor only");return q.n/q.d;};
 const ceil=q=>{q=Q(q);if(q.cmp(0)<0)throw Error("nonnegative ceil only");return(q.n+q.d-1n)/q.d;};
 function local(alpha,betaMinus,betaPlus,n=NUNIT){
  alpha=Q(alpha);betaMinus=Q(betaMinus);betaPlus=Q(betaPlus);
  if(!Number.isInteger(n)||n<1)throw Error("positive unit count required");
  if(betaMinus.cmp(abs(alpha))<0||betaPlus.cmp(abs(alpha))<0)throw Error("transport cone");
  const reflected=alpha.cmp(0)<0;if(reflected){alpha=alpha.neg();[betaMinus,betaPlus]=[betaPlus,betaMinus];}
  if(alpha.eq(0)){
   if(betaMinus.eq(0)||betaPlus.eq(0))return{kind:"one_front",reflected,direction:betaMinus.eq(0)?(betaPlus.eq(0)?"none":"upper"):"lower"};
   return{kind:"two_front",reflected,gamma:Q("3/2"),kappa:min(betaMinus,betaPlus).div(n)};
  }
  const C=betaMinus.sub(alpha);
  if(C.eq(0))return{kind:"one_front",reflected,direction:reflected?"lower":"upper"};
  return{kind:"two_front",reflected,gamma:betaMinus.div(C).add(HALF),kappa:alpha.mul(C).div(alpha.mul(n).add(C))};
 }
 function derive(input){
  const H=Q(input.horizon),M=Q(input.spatial_lipschitz),S=input.time_slabs,E=input.characteristic_segments;
  if(H.cmp(0)<0||M.cmp(0)<0||!Number.isSafeInteger(S)||S<1||!Number.isSafeInteger(E)||E<0)throw Error("invalid global constants");
  const positions=[...new Map([-1,1,...(input.stationary_positions??[])].map(Q).map(x=>[x.str(),x])).values()].sort((a,b)=>a.cmp(b));
  if(positions.some(x=>x.cmp(-1)<0||x.cmp(1)>0))throw Error("stationary position outside arena");
  let delta=Q(2);for(let j=0;j+1<positions.length;j++)delta=min(delta,positions[j+1].sub(positions[j]));
  const cones=[];let Gamma=Z,kappa=null;
  for(const f of input.interfaces??[]){
   const bm=Q(f.beta_minus),bp=Q(f.beta_plus);if(bm.cmp(M)>0||bp.cmp(M)>0)throw Error("density bound below interface density");
   const r=local(f.alpha,bm,bp);if(r.kind==="two_front"){Gamma=max(Gamma,r.gamma);kappa=kappa===null?r.kappa:min(kappa,r.kappa);}
   cones.push({id:f.id??cones.length,...r,...(r.kind==="two_front"?{gamma:r.gamma.str(),kappa:r.kappa.str()}:{} )});
  }
  const ratio=max(H.div(delta),O),K=kappa===null?0n:ceil(M.mul(4).mul(Gamma).mul(ratio).div(kappa));
  const coarse=BigInt(S)+2n*BigInt(E)+1n,transfers=floor(H.div(delta)),bound=coarse*(40n+3n*K)+3n*transfers+2n;
  return{scope:"Computable fixed-law piece bound, conditional on the supplied complete fan arrangement and the proved local reductions.",
   horizon:H.str(),spatial_lipschitz:M.str(),delta:delta.str(),time_slabs:S,characteristic_segments:E,coarse_intervals:String(coarse),
   gamma_max:kappa===null?null:Gamma.str(),kappa_min:kappa?.str()??null,record_switch_bound:String(K),distinct_stationary_transfers:String(transfers),
   piece_bound:String(bound),unit_source_pieces:NUNIT,interfaces:cones,stationary_positions:positions.map(x=>x.str())};
 }
 function unitWidth(vertices,alpha,betaMinus,betaPlus){
  vertices=vertices.map(p=>p.map(Q));alpha=Q(alpha);betaMinus=Q(betaMinus);betaPlus=Q(betaPlus);
  if(betaMinus.cmp(abs(alpha))<0||betaPlus.cmp(abs(alpha))<0)throw Error("transport cone");
  if(!vertices.length||!vertices[0][0].eq(0)||!vertices[0][1].eq(0))throw Error("relative source must be(0,0)");
  let low=Z,high=Z;
  for(let j=0;j<vertices.length;j++){
   const[t,x]=vertices[j];if(j){const dt=t.sub(vertices[j-1][0]),dx=x.sub(vertices[j-1][1]);if(dt.cmp(0)<=0||!abs(dx).eq(dt))throw Error("unit path required");}
   const y=alpha.mul(t).add((x.cmp(0)<0?betaMinus:betaPlus).mul(x));low=min(low,y);high=max(high,y);
  }
  return{width:high.sub(low),low,high,duration:vertices.at(-1)[0],pieces:vertices.length-1};
 }
 return{local,derive,unitWidth,floor,ceil};
}
module.exports={createBoundTools};
