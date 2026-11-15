/* Exact front-chain convex solution; see FRONT_CHAIN_QUADRATIC_SOLUTION.md. */
const api=(function makeFrontQP() {
 "use strict";
 const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a;};
 class F {
  constructor(n,d=1n){if(n instanceof F){this.n=n.n;this.d=n.d;return;}if(typeof n==="string"&&n.includes("/")){let p=n.split("/");n=BigInt(p[0]);d=BigInt(p[1]);}else n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
  a(v){v=q(v);return new F(this.n*v.d+v.n*this.d,this.d*v.d);}
  s(v){v=q(v);return new F(this.n*v.d-v.n*this.d,this.d*v.d);}
  m(v){v=q(v);return new F(this.n*v.n,this.d*v.d);}
  dby(v){v=q(v);return new F(this.n*v.d,this.d*v.n);}
  neg(){return new F(-this.n,this.d);}
  c(v){v=q(v);let x=this.n*v.d-v.n*this.d;return x<0n?-1:x>0n?1:0;}
  eq(v){return this.c(v)===0;}
  p(n){if(n<0)return new F(this.d,this.n).p(-n);return new F(this.n**BigInt(n),this.d**BigInt(n));}
  str(){return this.d===1n?String(this.n):this.n+"/"+this.d;}
  num(){return Number(this.n)/Number(this.d);}
 }
 const q=x=>x instanceof F?x:new F(x),z=q(0),one=q(1),sum=a=>a.reduce((s,x)=>s.a(x),z),pos=x=>x.c(0)>0?x:z,sq=x=>x.m(x);
 function constants(theta,k=one){
  theta=q(theta);k=q(k);const r=theta.dby(theta.a(1).p(2).m(2)),l=k.m(r),d=k.s(l),A=k.dby(8).s(l.dby(2)),C=l.dby(theta.m(4)),b=theta.m(3);
  return{theta,k,r,l,d,A,C,b,Hstar:b.dby(one.s(theta))};
 }
 function threshold(c,m){
  if(!m)return z;const {theta:t,b}=c;
  const f=j=>t.p(1-j).m(one.s(t.p(j))).m(one.s(t.p(j+1))).dby(one.s(t).p(2).m(one.a(t)));
  return b.dby(t).m(sum(Array.from({length:m},(_,j)=>f(j+1)))).dby(f(m+1));
 }
 function solve(c,m,H){
  H=q(H);const {theta:t,b,C}=c,cm=one.s(t.p(m)).dby(one.s(t).m(one.a(t.p(m+1)))),Pm=q(m).s(t.m(2).m(cm)).dby(one.s(t).p(2)),u=one.s(t.p(2*m)).dby(one.s(t.p(2*m+2))),v=Array.from({length:m},(_,j)=>t.p(m-j-1).m(one.s(t.p(2*j+2))).dby(one.s(t.p(2*m+2)))),p=Array.from({length:m},(_,j)=>one.s(t.p(j+1).a(t.p(m-j)).dby(one.a(t.p(m+1)))).dby(one.s(t).p(2))),lambda=b.m(cm).s(H).dby(Pm),h=v.map((x,j)=>b.m(x).s(lambda.m(p[j]))),energy=C.m(b.p(2).m(u).neg().a(b.m(cm).s(H).p(2).dby(Pm)));
  return{h,lambda,energy,cm,Pm,u};
 }
 function Q(c,h){return c.A.m(sum(h.map(sq))).s(c.l.dby(2).m(sum(h.slice(1).map((x,j)=>x.m(h[j]))))).s(c.l.m(3).dby(2).m(h.at(-1)));}
 function energy(c,h){
  let E=Q(c,h);
  for(let j=1;j+1<h.length;j++)E=E.s(pos(c.l.m(h[j-1]).s(c.d.m(h[j]))).p(2).dby(c.k.m(8)));
  if(h.length>1)E=E.s(pos(c.l.m(h.at(-2)).s(c.d.m(h.at(-1)))).dby(2));
  return E;
 }
 function primitiveCost(c,h){
  const H=sum(h),end=q(2),start=end.s(H),offset=q("1/8"),front=t=>c.d.m(t).a(offset),T=(t,n,terminal=false)=>t.m(n).a(terminal?pos(n.s(front(t))):pos(n.s(front(t))).p(2).dby(c.k.m(4)));
  let t=start,n=front(start),cost=z;
  for(let j=0;j<h.length;j++){
   let e=t.a(h[j]),N=front(t).a(c.k.m(h[j]));
   if(N.c(n)<0)throw Error("nonproductive primitive fixture");
   cost=cost.a(T(t,N).s(T(t,n)).a(T(e,N,j+1===h.length)).s(T(e,n,j+1===h.length)).dby(2));
   t=e;n=N;
  }
  cost=cost.a(end.a(2).m(one.s(n)));
  const waiting=c.d.m(end.p(2).s(start.p(2))).dby(2).a(end.a(2).m(one.s(front(end))));
  return cost.s(waiting);
 }
 function verify(options={}){
  const counts={riccati_identities:0,threshold_checks:0,kkt_coordinates:0,kkt_support:0,objective_checks:0,sorted_hinge_comparisons:0,primitive_chain_identities:0,geometric_limits:0};
  const assert=(yes,where)=>{if(!yes)throw Error(where);};
  let seed=548331;const random=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;};
  const examples=[];
  for(const tv of ["1/100","1/80","1/10","1/4","1/2","3/4"]){
   const c=constants(tv,q("1/8")),{theta:t,C,b,k,l,d,A,Hstar}=c;
   assert(C.m(one.a(t.p(2))).eq(A)&&C.m(t).eq(l.dby(4)),"Riccati coefficients");counts.riccati_identities+=2;
   let prior=z;
   for(let m=1;m<=10;m++){
    const hi=threshold(c,m),gap=b.m(t.p(m)).m(one.a(t)).m(q(m).m(one.s(t)).a(one.s(t.m(2))).a(t.p(m+2))).dby(one.s(t).m(one.s(t.p(m+1))).m(one.s(t.p(m+2))));
    assert(hi.c(prior)>0&&hi.c(Hstar)<0&&Hstar.s(hi).eq(gap),"threshold formula");counts.threshold_checks+=3;
    for(const f of [z,q("1/3"),q("2/3"),one]){
     const H=prior.a(hi.s(prior).m(f)),s=solve(c,m,H),h=s.h;
     assert(sum(h).eq(H)&&s.lambda.c(0)>=0&&s.lambda.s(t.m(h[0])).c(0)>=0,"support KKT");counts.kkt_support+=3;
     for(let j=0;j<m;j++){
      const lhs=one.a(t.p(2)).m(h[j]).s(t.m(j?h[j-1]:z)).s(t.m(j+1<m?h[j+1]:z)),rhs=(j+1===m?b:z).s(s.lambda);
      assert(lhs.eq(rhs),"stationary coordinate");
      assert(h[j].c(0)>=0&&(j===0||h[j].c(h[j-1])>=0),"nonnegative increasing active block");
      counts.kkt_coordinates+=2;
     }
     assert(Q(c,h).eq(s.energy),"objective formula");counts.objective_checks++;
     if(H.c(0)>0&&H.c(1)<=0&&h[0].c(0)>0){assert(primitiveCost(c,h).eq(s.energy),"independent primitive chain");counts.primitive_chain_identities++;}
    }
    const at=solve(c,m,hi);assert(at.lambda.eq(t.m(at.h[0])),"support entry threshold");counts.threshold_checks++;
    prior=hi;
   }
   for(let m=1;m<=7;m++)for(let trial=0;trial<35;trial++){
    let h=Array.from({length:m},()=>q(1+random(30)).dby(100)),sorted=[...h].sort((a,b)=>a.c(b)),M=sorted.at(-1);
    let down=z;for(let j=1;j<m;j++)down=down.a(pos(h[j-1].s(h[j])).p(2));
    const lower=l.dby(4).m(one.s(c.r.dby(2))).m(down).a(l.dby(2).m(q(2).s(M)).m(M.s(h.at(-1))));
    assert(energy(c,h).s(Q(c,sorted)).c(lower)>=0,"sorting/hinge bound");counts.sorted_hinge_comparisons++;
   }
   for(let m=1;m<=8;m++)for(let trial=0;trial<10;trial++){
    let h=[q(1)];
    for(let j=1;j<m;j++){
     // The first two factors exercise short productive returns; the others exercise long returns.
     const jcase=random(4),factor=jcase===0?c.r:jcase===1?c.r.m(one.a(one.dby(one.s(c.r)))).dby(2):jcase===2?one:q(2);
     h.push(h.at(-1).m(factor));
    }
    const scale=q("1/4").dby(sum(h));h=h.map(x=>x.m(scale));
    assert(primitiveCost(c,h).eq(energy(c,h)),"full endpoint primitive energy");counts.primitive_chain_identities++;
   }
   for(let m=1;m<=12;m++){
    const h=Array.from({length:m},(_,j)=>b.m(t.p(m-j-1)));
    assert(Q(c,h).a(C.m(b.p(2))).eq(C.m(b.p(2)).m(t.p(2*m))),"geometric residual");
    assert(sum(h).eq(Hstar.m(one.s(t.p(m)))),"geometric total");counts.geometric_limits+=2;
   }
   examples.push({theta:t.str(),ratio:c.r.str(),first_threshold:threshold(c,1).str(),accumulation_duration:Hstar.str(),limiting_excess:C.m(b.p(2)).neg().str()});
   if(options.progress)options.progress({theta:tv,counts:{...counts}});
  }
  return{scope:"Exact prescribed-terminal front-chain energy, sorting, all-count convex KKT formulas and affine rank-primitive capture moments. Exterior inverse branches and the complete unrestricted game remain separate.",checks:counts,total_checks:Object.values(counts).reduce((a,b)=>a+b,0),examples};
 }
 return{verify,constants,threshold,solve,Q,energy,primitiveCost,F,q};
})();
if(typeof module==='object'&&module.exports)module.exports=api;
if(typeof require==='function'&&require.main===module)console.log(JSON.stringify(api.verify(),null,2));
return api;
