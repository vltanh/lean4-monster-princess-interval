/** Exact stationary-tail dynamic program for a bounded step density plus atoms.
 * The proof allowing arbitrary finite/infinite histories is
 * STATIC_TAIL_BOUNDARY_REDUCTION.md. No claim is made about an earlier moving phase.
 */
module.exports=(function(){
function createStaticTailDP(G){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b;
 function unique(values){const out=[...new Map(values.map(Q).map(x=>[x.str(),x])).values()];out.sort((a,b)=>a.cmp(b));return out;}
 function compile(raw,extra=[]){
  const cells=(raw.cells||[]).map(([a,b,f])=>[Q(a),Q(b),Q(f)]),atoms=(raw.atoms||[]).map(([x,w])=>[Q(x),Q(w)]);
  for(const[a,b,f]of cells)if(a.cmp(-1)<0||b.cmp(1)>0||a.cmp(b)>0||f.cmp(0)<0)throw Error("invalid stationary density cell");
  for(const[x,w]of atoms)if(x.cmp(-1)<0||x.cmp(1)>0||w.cmp(0)<0)throw Error("invalid stationary atom");
  const D=unique([Q(-1),O,...extra,...cells.flatMap(([a,b])=>[a,b]),...atoms.map(([x])=>x)]),K=D.length,
   beta=[],atomMass=D.map(()=>Z),strict=[],closed=[];
  for(let i=0;i+1<K;i++){const mid=D[i].a(D[i+1]).dby(2);let f=Z;for(const[a,b,v]of cells)if(mid.cmp(a)>0&&mid.cmp(b)<0)f=f.a(v);beta.push(f);}
  for(const[x,w]of atoms){const i=D.findIndex(y=>y.eq(x));atomMass[i]=atomMass[i].a(w);}
  let total=Z;
  for(let i=0;i<K;i++){strict.push(total);total=total.a(atomMass[i]);closed.push(total);if(i+1<K)total=total.a(beta[i].m(D[i+1].s(D[i])));}
  return{D,K,beta,atomMass,strict,closed,total,cells,atoms};
 }
 function removeRankBand(raw,lower,upper){
  const m=compile(raw),lo=Q(lower),hi=Q(upper);if(lo.cmp(0)<0||hi.cmp(lo)<0||hi.cmp(m.total)>0)throw Error("invalid captured rank band");
  const cells=[],atoms=[];
  function retained(a,b){const out=[],l=min(b,lo),r=max(a,hi);if(l.cmp(a)>0)out.push([a,l]);if(b.cmp(r)>0)out.push([r,b]);return out;}
  for(let i=0;i<m.K;i++){
   let w=Z;for(const[a,b]of retained(m.strict[i],m.closed[i]))w=w.a(b.s(a));if(w.cmp(0)>0)atoms.push([m.D[i].str(),w.str()]);
   if(i+1<m.K&&m.beta[i].cmp(0)>0)for(const[a,b]of retained(m.closed[i],m.strict[i+1])){
    const left=m.D[i].a(a.s(m.closed[i]).dby(m.beta[i])),right=m.D[i].a(b.s(m.closed[i]).dby(m.beta[i]));
    cells.push([left.str(),right.str(),m.beta[i].str()]);
   }
  }
  const out={cells,atoms},mass=compile(out).total;if(!mass.eq(m.total.s(hi.s(lo))))throw Error("rank-band mass conservation");
  return{...out,mass:mass.str(),captured_rank_band:[lo.str(),hi.str()]};
 }
 function fromFans(rows,{normalize=true}={}){
  const cells=[],atoms=[];let sum=Z;
  const data=rows.map(r=>{const weight=Q(r.weight??1),lo=Q(r.lower),hi=Q(r.upper),p=Q(r.tail_position);
   if(weight.cmp(0)<0||hi.cmp(lo)<=0||p.cmp(-1)<0||p.cmp(1)>0)throw Error("invalid stationary fan component");sum=sum.a(weight);return{weight,lo,hi,p};});
  if(sum.cmp(0)<=0)throw Error("zero stationary fan law");
  for(const r of data){const w=normalize?r.weight.dby(sum):r.weight,span=r.hi.s(r.lo),density=w.dby(span.m(2));
   for(const sign of [1,-1]){
    const a=sign===1?r.p.a(r.lo):r.p.neg().s(r.hi),b=sign===1?r.p.a(r.hi):r.p.neg().s(r.lo),
     left=max(Q(-1),a),right=min(O,b);
    if(right.cmp(left)>0)cells.push([left.str(),right.str(),density.str()]);
    const atLeft=min(b,Q(-1)).s(a),atRight=b.s(max(a,O));
    if(atLeft.cmp(0)>0)atoms.push(["-1",atLeft.m(density).str()]);
    if(atRight.cmp(0)>0)atoms.push(["1",atRight.m(density).str()]);
   }
  }
  const result={cells,atoms},mass=compile(result).total;if(!mass.eq(normalize?O:sum))throw Error("stationary fan mass");
  return{...result,mass:mass.str()};
 }
 function solve(raw,start,{absoluteTime=0,completeEndpoints=true,maxPoints=2048}={}){
  const x=Q(start),h=Q(absoluteTime);if(x.cmp(-1)<0||x.cmp(1)>0||h.cmp(0)<0)throw Error("invalid stationary starting state");
  const m=compile(raw,[x]),{D,K,beta,strict,closed,total}=m;if(K>maxPoints)throw Error("stationary DP point limit: "+K);
  const s=D.findIndex(y=>y.eq(x)),table=new Map();let states=0,candidates=0;
  const key=(l,r)=>l*K+r;
  for(let width=K-1;width>=0;width--)for(let l=Math.max(0,s-width);l<=Math.min(s,K-1-width);l++){
   const r=l+width,M=strict[l].a(total.s(closed[r])),values=[],choices=[];
   for(const side of [0,1]){
    states++;if(M.eq(0)){values.push(Z);choices.push(null);continue;}
    const position=side===0?D[l]:D[r];let best=null,choice=null;
    if(l>0){
     const delta=D[l].s(D[l-1]),edge=M.m(position.s(D[l-1])).s(beta[l-1].m(delta.m(delta)).dby(2)),
      future=table.get(key(l-1,r))[0],value=edge.a(future);candidates++;
     if(edge.cmp(0)<0)throw Error("negative stationary edge cost");best=value;choice=-1;
    }
    if(r+1<K){
     const delta=D[r+1].s(D[r]),edge=M.m(D[r+1].s(position)).s(beta[r].m(delta.m(delta)).dby(2)),
      future=table.get(key(l,r+1))[1],value=edge.a(future);candidates++;
     if(edge.cmp(0)<0)throw Error("negative stationary edge cost");if(best===null||value.cmp(best)<0){best=value;choice=1;}
    }
    if(best===null)throw Error("positive residual mass after full arena");values.push(best);choices.push(choice);
   }
   values.choices=choices;table.set(key(l,r),values);
  }
  let l=s,r=s,side=0,time=Z,position=x;const vertices=[[Z,x]],expansions=[];
  while(true){
   const state=table.get(key(l,r)),choice=state.choices[side];if(choice===null)break;
   const next=choice===-1?D[l-1]:D[r+1],dist=next.s(position);time=time.a(dist.cmp(0)<0?dist.neg():dist);vertices.push([time,next]);
   if(choice===-1){l--;side=0;}else{r++;side=1;}position=next;expansions.push({left:l,right:r,direction:choice});
  }
  if(completeEndpoints){
   let left=vertices.some(v=>v[1].eq(-1)),right=vertices.some(v=>v[1].eq(1));
   const targets=[];
   if(!left&&!right){if(position.cmp(0)<=0)targets.push(Q(-1),O);else targets.push(O,Q(-1));}
   else if(!left)targets.push(Q(-1));else if(!right)targets.push(O);
   for(const next of targets){const d=next.s(position);time=time.a(d.cmp(0)<0?d.neg():d);vertices.push([time,next]);position=next;}
  }
  const route=new G.PLPath(vertices),value=table.get(key(s,s))[0];
  if(route.t.at(-1).cmp(2*(K+1))>0)throw Error("stationary finite-horizon bound");
  return{scope:"Exact unrestricted stationary-tail optimum under the static boundary theorem; no claim about the preceding moving phase.",
   relative_cost:value.str(),absolute_moment:value.a(h.m(total)).str(),remaining_mass:total.str(),
   relative_route:route.json(),absolute_route:route.vertices.map(([t,y])=>[t.a(h).str(),y.str()]),
   boundary_points:D.map(y=>y.str()),density:beta.map(y=>y.str()),atoms:m.atomMass.map(y=>y.str()),
   state_count:states,candidate_count:candidates,expansions,completion_horizon:h.a(2*(K+1)).str()};
 }
 return{compile,removeRankBand,fromFans,solve};
}
return{createStaticTailDP};
})();
