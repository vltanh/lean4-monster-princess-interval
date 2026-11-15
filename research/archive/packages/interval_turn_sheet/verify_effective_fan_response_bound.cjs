"use strict";
function verify(Q,createBoundTools){
 const B=createBoundTools(Q),Z=Q(0),abs=x=>Q(x).cmp(0)<0?Q(x).neg():Q(x),min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b;
 let width=0,degenerate=0,characteristic=0,scale=0,episodes=0,transfers=0,rejections=0;const examples=[];
 const cones=[
 ["0","1/4","3/2"],["0","2","1/7"],
 ["1/7","3/7","2"],["1/4","1/2","1/4"],["1/2","3/4","3"],
 ["1/4","2","1/2"],["-1/7","2","3/7"],["-1/4","1/4","1/2"],
 ["1/4","1/4","2"],["-1/4","2","1/4"],["0","0","1"],["0","2","0"],["0","0","0"]
 ];
 let seed=72639211;const rnd=n=>{seed=(1664525*seed+1013904223)>>>0;return(seed>>>8)%n;};
 for(const [alpha,bm,bp]of cones)for(let n=1;n<=17;n++)for(let z=0;z<8;z++){
  let t=Z,x=Z;const path=[[t,x]];for(let j=0;j<n;j++){const dt=Q(1+rnd(7)).div(8192);t=t.add(dt);x=x.add(dt.mul(rnd(2)?1:-1));path.push([t,x]);}
  const r=B.local(alpha,bm,bp,n),w=B.unitWidth(path,alpha,bm,bp);
  if(r.kind==="two_front"){if(w.width.cmp(r.kappa.mul(t))<0)throw Error("unit width failed");width++;
   const oldL=w.low.sub(Q(z).div(1000)),oldH=w.high.add(Q(7-z).div(1000));if(oldH.sub(oldL).cmp(r.kappa.mul(t))<0)throw Error("old band width failed");width++;
  }else{const direction=r.direction;if(direction==="upper"&&w.low.cmp(0)<0)throw Error("degenerate lower capture");if(direction==="lower"&&w.high.cmp(0)>0)throw Error("degenerate upper capture");if(direction==="none"&&!w.width.eq(0))throw Error("flat width");degenerate++;}
 }
 for(let j=0;j<240;j++){
  const a=Q(rnd(9)-4).div(16),b=Q(rnd(9)-4).div(16),T=Q(1),signs=[-1,1],cplusLo=b.sub(T).sub(Q(rnd(5)).div(16)),cplusHi=a.add(Q(rnd(5)).div(16)),cminusLo=a.sub(Q(rnd(5)).div(16)),cminusHi=b.add(T).add(Q(rnd(5)).div(16));
  for(let k=0;k<=24;k++){
   const t=Q(k).div(24),mx=min(Q(1),min(a.add(t),b.add(T.sub(t)))),mn=max(Q(-1),max(a.sub(t),b.sub(T.sub(t))));
   for(const x of[mx,mn]){
    if(x.sub(t).cmp(cplusLo)<0||x.sub(t).cmp(cplusHi)>0||x.add(t).cmp(cminusLo)<0||x.add(t).cmp(cminusHi)>0)throw Error("characteristic half-plane failed");characteristic+=4;
   }
  }
 }
 const data={horizon:"10",spatial_lipschitz:"4",time_slabs:8,characteristic_segments:27,stationary_positions:["-3/4","-1/4","0","1/3","3/4"],interfaces:cones.map((v,i)=>({id:i,alpha:v[0],beta_minus:v[1],beta_plus:v[2]}))},out=B.derive(data);examples.push(out);
 const H=Q(out.horizon),delta=Q(out.delta),G=Q(out.gamma_max),kap=Q(out.kappa_min),M=Q(out.spatial_lipschitz);
 for(const f of data.interfaces){
  const r=B.local(f.alpha,f.beta_minus,f.beta_plus);if(r.kind!=="two_front")continue;
  for(let j=1;j<=120;j++){
   const R=H.mul(j).div(120),d=min(delta.div(2),R.div(2)).div(r.gamma),ratio=R.div(d),rhs=r.gamma.mul(2).mul(max(R.div(delta),Q(1)));
   if(!ratio.eq(rhs)||ratio.cmp(G.mul(2).mul(max(H.div(delta),Q(1))))>0)throw Error("scale ratio");scale+=2;
   const exact=M.mul(2).mul(R).div(r.kappa.mul(d)),global=M.mul(4).mul(G).mul(max(H.div(delta),Q(1))).div(kap);
   if(exact.cmp(global)>0||B.ceil(exact)>BigInt(out.record_switch_bound))throw Error("episode bound");episodes+=2;
  }
 }
 const positions=out.stationary_positions.map(Q);
 for(let j=0;j<100;j++){let time=Z,last=rnd(positions.length),count=0;for(let k=0;k<25;k++){let next=rnd(positions.length);if(next===last)continue;const dt=abs(positions[next].sub(positions[last])).add(Q(rnd(3)).div(64));time=time.add(dt);last=next;count++;if(BigInt(count)>B.floor(time.div(delta)))throw Error("transfer charge");transfers++;}}
 for(const args of[[1,0,2],[1,2,0],[-1,0,2],[0,-1,0]]){let bad=false;try{B.local(...args);}catch(e){bad=true;}if(!bad)throw Error("invalid cone accepted");rejections++;}
 for(const input of[
 {...data,horizon:"-1"}, {...data,spatial_lipschitz:"1/8"}, {...data,time_slabs:0}, {...data,stationary_positions:[2]}
 ]){let bad=false;try{B.derive(input);}catch(e){bad=true;}if(!bad)throw Error("invalid bound input");rejections++;}
 const flat=B.derive({horizon:4,spatial_lipschitz:0,time_slabs:1,characteristic_segments:0,stationary_positions:[],interfaces:[{alpha:0,beta_minus:0,beta_plus:0}]});if(flat.record_switch_bound!=="0"||flat.piece_bound!=="88")throw Error("flat convention");examples.push(flat);
 return{pass:true,unit_width_checks:width,degenerate_one_front_checks:degenerate,characteristic_half_plane_checks:characteristic,scale_identity_checks:scale,episode_bound_checks:episodes,distinct_transfer_checks:transfers,invalid_input_rejections:rejections,examples,
  scope:"Exact fixtures check local inequalities and count arithmetic; the global finite-piece theorem is analytic."};
}
module.exports={verify};
if(typeof require!=="undefined"&&require.main===module){const {Q}=require("./affine_record_prefix.cjs"),B=require("./effective_fan_response_bound.cjs");process.stdout.write(JSON.stringify(verify(Q,B.createBoundTools),null,2)+"\n");}
