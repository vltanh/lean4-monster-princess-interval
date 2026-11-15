
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a;}
class Rat{
 constructor(n,d=1n){if(n instanceof Rat){this.n=n.n;this.d=n.d;return;}if(typeof n==="string"){let p=n.split("/");if(p.length===2){n=BigInt(p[0]);d=BigInt(p[1]);}else {let [s,e]=n.toLowerCase().split("e");let neg=s[0]==="-";if(neg||s[0]==="+")s=s.slice(1);let parts=s.split(".");let f=parts[1]||"";n=BigInt(parts[0]+f)*(neg?-1n:1n);let power=f.length-Number(e||0);if(power>=0)d=10n**BigInt(power);else n*=10n**BigInt(-power);}}else n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
 a(q){q=Q(q);return new Rat(this.n*q.d+q.n*this.d,this.d*q.d);}
 s(q){q=Q(q);return new Rat(this.n*q.d-q.n*this.d,this.d*q.d);}
 m(q){q=Q(q);return new Rat(this.n*q.n,this.d*q.d);}
 dby(q){q=Q(q);return new Rat(this.n*q.d,this.d*q.n);}
 neg(){return new Rat(-this.n,this.d);}
 cmp(q){q=Q(q);let z=this.n*q.d-q.n*this.d;return z<0n?-1:z>0n?1:0;}
 eq(q){return this.cmp(q)===0;}
 num(){return Number(this.n)/Number(this.d);}
 str(){return String(this.n)+(this.d===1n?"":"/"+this.d);}
}
function Q(x){return x instanceof Rat?x:new Rat(typeof x==="number"?String(x):x);}
const ZERO=Q(0),ONE=Q(1);
function minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}
function maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}
function uniq(xs){let m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}
function bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){let m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}

function physicalMoment(alpha,bp,bm,xs,first=1){
 alpha=Q(alpha);bp=Q(bp);bm=Q(bm);xs=xs.map(Q);let t=ZERO,x=ZERO,L=ZERO,M=ZERO,cost=ZERO;
 const F=(t,x)=>alpha.m(t).a((x.cmp(0)>=0?bp:bm).m(x));
 let pieces=0;
 for(let i=0;i<xs.length;i++){
  const sign=(i%2===0?first:-first),nx=xs[i].m(sign),v=Q(sign),nt=t.a(nx.s(x).cmp(0)<0?nx.s(x).neg():nx.s(x));
  let cuts=[t,nt];if(x.m(nx).cmp(0)<0)cuts.push(t.s(x.dby(v)));cuts=uniq(cuts);
  const record=sign===1?M:L;let area=ZERO;
  for(let j=0;j<cuts.length-1;j++){
   const a=cuts[j],b=cuts[j+1],fa=F(a,x.a(v.m(a.s(t)))),fb=F(b,x.a(v.m(b.s(t))));
   let ga=sign===1?fa.s(record):record.s(fa),gb=sign===1?fb.s(record):record.s(fb);
   if(maxQ(ga,gb).cmp(0)>0){
    if(minQ(ga,gb).cmp(0)>=0)area=area.a(b.s(a).m(ga.a(gb)).dby(2));
    else {const z=maxQ(ga,gb);area=area.a(b.s(a).m(z.m(z)).dby(z.s(minQ(ga,gb)).m(2)));}
   }pieces++;
  }
  const end=F(nt,nx);
  if(sign===1){const z=maxQ(M,end);cost=cost.a(nt.m(z.s(M))).s(area);M=z;}
  else {const z=minQ(L,end);cost=cost.a(nt.m(L.s(z))).s(area);L=z;}
  t=nt;x=nx;
 }return{cost,t,x,L,M,pieces};
}
function formula(alpha,bp,bm,xs){
 alpha=Q(alpha);bp=Q(bp);bm=Q(bm);xs=xs.map(Q);
 let S=ZERO,prev=[ZERO,ZERO],M=ZERO,correction=ZERO,valid=true,positiveHinges=0,rank=[];
 for(let i=0;i<xs.length;i++){
  const sg=i%2===0?1:-1,b=sg===1?bp:bm,c=b.a(alpha.m(sg)),r=c.m(xs[i]).a(alpha.m(S).m(sg)),old=prev[i%2];
  if(r.cmp(old)<0||r.cmp(0)<0)valid=false;
  M=M.a(r.m(r).s(old.m(old)).dby(c.m(2))).a(b.m(S).m(r.s(old)).dby(c));
  if(sg===1){
   const g=maxQ(0,alpha.m(S).s(old));
   if(g.cmp(0)>0)positiveHinges++;
   correction=correction.a(ONE.dby(bp.a(alpha)).s(ONE.dby(bm.a(alpha))).m(g.m(g)).dby(2));
  }
  prev[i%2]=r;rank.push(r);S=S.a(xs[i].m(2));
 }return{cost:M.a(correction),uncorrected:M,correction,valid,positiveHinges,rank};
}
function noHingeRankMoment(alpha,bp,bm,plus,minus){
 alpha=Q(alpha);bp=Q(bp);bm=Q(bm);plus=plus.map(Q);minus=minus.map(Q);let S=ZERO,prev=[ZERO,ZERO],cost=ZERO;
 for(let j=0;j<plus.length+minus.length;j++){
  const sg=j%2===0?1:-1,b=sg===1?bp:bm,c=b.a(alpha.m(sg)),r=sg===1?plus[(j/2)|0]:minus[(j/2)|0],old=prev[j%2];
  cost=cost.a(r.m(r).s(old.m(old)).dby(c.m(2))).a(b.m(S).m(r.s(old)).dby(c));
  const x=r.s(alpha.m(S).m(sg)).dby(c);
  S=S.a(x.m(2));prev[j%2]=r;
 }return{cost,S};
}
function verifyAlgebra(){
 let capture=0,hinged=0,pieces=0,conditional=0;
 for(const al of["0","1/8","1/4"])for(const bps of["1/2","1","2"])for(const bms of["1/2","1","2"])for(let N=2;N<=6;N++){
  const alpha=Q(al),bp=Q(bps),bm=Q(bms);
  for(const growth of["3/2","2","3"]){
   const xs=[];let z=Q("1/100");for(let i=0;i<N;i++){xs.push(z);z=z.m(Q(growth));}
   const a=formula(alpha,bp,bm,xs);if(!a.valid)continue;
   const b=physicalMoment(alpha,bp,bm,xs);
   if(!a.cost.eq(b.cost))throw Error("interface capture correction");
   capture++;pieces+=b.pieces;if(a.positiveHinges)hinged++;
  }
 }
 for(const al of["1/16","1/8","1/4"])for(const bps of["1/2","1","2"])for(const bms of["1/2","1","2"])for(let m=2;m<=7;m++){
  const a=Q(al),bp=Q(bps),bm=Q(bms),cp=bp.a(a),cm=bm.s(a),km=bm.a(a).dby(cm),kp=bp.s(a).dby(cp),K=kp.m(km),A=km.m(2).dby(cp),C=bp.dby(cp).m(A);
  const plus=Array.from({length:m+1},(_,j)=>Q(j+1).dby(10)),minus=Array.from({length:m},(_,j)=>Q(j+1).dby(11));
  for(const mode of[0,1,2]){
   const zs=[ZERO,...Array.from({length:m-1},(_,j)=>Q(mode===0?1:mode===1?j+1:(j%2===0?1:-1)).dby(1000)),ZERO];
   const vs=Array.from({length:m},(_,j)=>zs[j+1].s(K.m(zs[j])));
   const pp=plus.map((r,j)=>j<m?r.a(vs[j]):r),pm=plus.map((r,j)=>j<m?r.s(vs[j]):r);
   const f0=noHingeRankMoment(a,bp,bm,plus,minus),fp=noHingeRankMoment(a,bp,bm,pp,minus),fm=noHingeRankMoment(a,bp,bm,pm,minus);
   if(!fp.S.eq(f0.S)||!fm.S.eq(f0.S))throw Error("fixed-time recurrence");
   const sec=fp.cost.a(fm.cost).s(f0.cost.m(2)).dby(2),sos=zs.slice(1).reduce((s,z,j)=>s.a(z.s(zs[j]).m(z.s(zs[j]))),ZERO).m(C).m(K.a(1)).dby(2).neg();
   if(!sec.eq(sos)||sos.cmp(0)>=0)throw Error("conditional parity concavity");
   conditional++;
  }
 }
 return{scope:"Independent initial two-density interface audit. The corrected physical moment is exact; conditional parity concavity is proved only for the no-crossover-hinge quadratic, not for the full hinged objective.",physical_moment_identities:capture,with_active_crossing_hinges:hinged,affine_capture_pieces:pieces,conditional_parity_sos_identities:conditional};
}
function positiveArea(a,b,fa,fb){
 if(b.cmp(a)<=0||maxQ(fa,fb).cmp(0)<=0)return ZERO;
 if(minQ(fa,fb).cmp(0)>=0)return b.s(a).m(fa.a(fb)).dby(2);
 const f=maxQ(fa,fb),other=minQ(fa,fb);
 return b.s(a).m(f.m(f)).dby(f.s(other).m(2));
}
function positivePrimitive(q,c){return maxQ(0,Q(q).s(c)).m(maxQ(0,Q(q).s(c))).dby(2);}
function ceilQ(q){q=Q(q);if(q.cmp(0)<0)throw Error("negative ceiling");return(q.n+q.d-1n)/q.d;}
class Fan{
 constructor(rows){
  this.rows=rows.map(r=>({w:Q(r.w),lo:Q(r.lo),hi:Q(r.hi),p:r.p.map(x=>x.map(Q))}));
  if(!this.rows.reduce((s,r)=>s.a(r.w),ZERO).eq(1))throw Error("weights");
  for(const r of this.rows){
   if(r.w.cmp(0)<0||r.hi.cmp(r.lo)<=0||!r.p[0][0].eq(0))throw Error("fan data");
   for(let i=0;i<r.p.length-1;i++){
    const dt=r.p[i+1][0].s(r.p[i][0]),dp=r.p[i+1][1].s(r.p[i][1]);
    if(dt.cmp(0)<=0||![-1,0,1].some(v=>dp.eq(dt.m(v))))throw Error("non-bang-bang base");
   }
  }
 }
 base(row,t){
  t=Q(t);const p=row.p;if(t.cmp(p[p.length-1][0])>=0)return{value:p[p.length-1][1],slope:ZERO};
  const i=Math.max(0,bisect(p.map(x=>x[0]),t)-1),v=p[i+1][1].s(p[i][1]).dby(p[i+1][0].s(p[i][0]));
  return{value:p[i][1].a(t.s(p[i][0]).m(v)),slope:v};
 }
 radial(t,r){
  t=Q(t);r=Q(r);if(r.cmp(0)<0||r.cmp(1)>0)throw Error("radius");
  return this.rows.reduce((s,row)=>{
   const p=this.base(row,t).value,lo=p.a(row.lo),hi=p.a(row.hi);
   return s.a(row.w.m(maxQ(0,minQ(r,hi).s(maxQ(r.neg(),lo)))).dby(row.hi.s(row.lo)));
  },ZERO);
 }
 cdfInterior(t,x){
  t=Q(t);x=Q(x);
  let d=ZERO;
  for(const row of this.rows){
   const p=this.base(row,t).value,a=p.a(row.lo),width=row.hi.s(row.lo);
   const F=z=>maxQ(0,minQ(1,z.s(a).dby(width)));
   d=d.a(row.w.m(F(x).s(F(x.neg()))));
  }return ONE.a(d).dby(2);
 }
 sides(t,x){
  t=Q(t);x=Q(x);const f=this.cdfInterior(t,x);
  if(x.eq(1))return[f,ONE];if(x.eq(-1))return[ZERO,f];return[f,f];
 }
 route(route,n=0,records=null){
  route=route.map(p=>p.map(Q));n=Q(n);
  if(!records&&!route[0][1].eq(0))throw Error("fixture must start at center");
  let lower=records?Q(records[0]):ONE.s(n).dby(2),upper=records?Q(records[1]):ONE.a(n).dby(2),cost=ZERO,affinePieces=0;
  for(let j=0;j<route.length-1;j++){
   const[t0,x0]=route[j],[t1,x1]=route[j+1],v=x1.s(x0).dby(t1.s(t0));
   if(!v.eq(1)&&!v.eq(-1))throw Error("unit fixture");
   let cuts=[t0,t1];
   for(const row of this.rows)for(const[t]of row.p)if(t.cmp(t0)>0&&t.cmp(t1)<0)cuts.push(t);
   cuts=uniq(cuts);const more=[];
   for(let k=0;k<cuts.length-1;k++){
    const a=cuts[k],b=cuts[k+1],mid=a.a(b).dby(2),xm=x0.a(v.m(mid.s(t0)));
    for(const row of this.rows){
     const bs=this.base(row,mid);
     for(const sg of [-1,1])for(const z of[row.lo,row.hi]){
      const value=xm.m(sg).s(bs.value).s(z),slope=v.m(sg).s(bs.slope);
      if(!slope.eq(0)){
       const root=mid.s(value.dby(slope));if(root.cmp(a)>0&&root.cmp(b)<0)more.push(root);
      }
     }
    }
   }
   cuts=uniq(cuts.concat(more));let area=ZERO;
   const record=v.eq(1)?upper:lower;
   for(let k=0;k<cuts.length-1;k++){
    const a=cuts[k],b=cuts[k+1],fa=this.cdfInterior(a,x0.a(v.m(a.s(t0)))),fb=this.cdfInterior(b,x0.a(v.m(b.s(t0))));
    if(v.eq(1)&&fb.cmp(fa)<0||v.eq(-1)&&fb.cmp(fa)>0)throw Error("transport on unit leg");
    area=area.a(v.eq(1)?positiveArea(a,b,fa.s(record),fb.s(record)):positiveArea(a,b,record.s(fa),record.s(fb)));affinePieces++;
   }
   const[strict,closed]=this.sides(t1,x1);
   if(v.eq(1)){const nu=maxQ(upper,closed);cost=cost.a(t1.m(nu.s(upper))).s(area);upper=nu;}
   else{const nl=minQ(lower,strict);cost=cost.a(t1.m(lower.s(nl))).s(area);lower=nl;}
  }
  if(!lower.eq(0)||!upper.eq(1))throw Error("incomplete physical fixture");
  return{cost,pieces:affinePieces};
 }
}

function interfaceFan(){
 return new Fan([
  {w:"1/4",lo:"-1/4",hi:"1/4",p:[[0,"1/2"],["1/2",0],[1,0]]},
  {w:"1/4",lo:"-1/4",hi:"1/4",p:[[0,"1/2"],[1,"1/2"]]},
  {w:"3/8",lo:"-1/8",hi:0,p:[[0,"1/2"],[1,"1/2"]]},
  {w:"1/8",lo:0,hi:"1/8",p:[[0,1],[1,1]]}
 ]);
}
function verifyCurvature(){
 const a=Q("1/4"),bp=Q("1/2"),bm=Q(2),m=24,K=Q("3/7"),eps=Q("1/85070591730234615865843651857942052864");
 let x=Q("1/9007199254740992"),xs=[];
 for(let j=0;j<49;j++){xs.push(x);x=x.m(2);}
 const baseline=formula(a,bp,bm,xs),plus=baseline.rank.filter((_,i)=>i%2===0),minus=baseline.rank.filter((_,i)=>i%2===1);
 const zs=Array.from({length:m+1},(_,j)=>Q(Math.min(j,m-j)).m(eps)),vs=Array.from({length:m},(_,j)=>zs[j+1].s(K.m(zs[j])));
 function recover(p){
  let S=ZERO,out=[];
  for(let i=0;i<49;i++){
   const sg=i%2===0?1:-1,b=sg===1?bp:bm,c=b.a(a.m(sg)),r=sg===1?p[(i/2)|0]:minus[(i/2)|0],x=r.s(a.m(S).m(sg)).dby(c);
   if(x.cmp(0)<=0)throw Error("negative physical extremum");out.push(x);S=S.a(x.m(2));
  }return out;
 }
 const xp=recover(plus.map((r,j)=>j<m?r.a(vs[j]):r)),xm=recover(plus.map((r,j)=>j<m?r.s(vs[j]):r));
 const f0=physicalMoment(a,bp,bm,xs),fp=physicalMoment(a,bp,bm,xp),fm=physicalMoment(a,bp,bm,xm);
 for(const f of[fp,fm])if(!f.t.eq(f0.t)||!f.x.eq(f0.x)||!f.L.eq(f0.L)||!f.M.eq(f0.M))throw Error("fixed-exit witness");
 for(const x of[xs,xp,xm]){const f=formula(a,bp,bm,x);if(!f.valid||f.positiveHinges!==24)throw Error("hinge witness gate");}
 const curvature=fp.cost.a(fm.cost).s(f0.cost.m(2)).dby(eps.m(eps).m(2));
 if(!curvature.eq("1504/441")||curvature.cmp(0)<=0)throw Error("positive curvature witness");
 const fan=interfaceFan();let realization=0;
 function completeRoute(xx){
  let t=ZERO,relative=ZERO;const route=[[t,Q("1/2")]];
  for(let i=0;i<xx.length;i++){
   const next=xx[i].m(i%2===0?1:-1),dist=next.s(relative);t=t.a(dist.cmp(0)<0?dist.neg():dist);relative=next;route.push([t,Q("1/2").a(relative)]);
  }
  const position=Q("1/2").a(relative);route.push([t.a(position).a(1),Q(-1)],[t.a(position).a(3),ONE]);return route;
 }
 const q0=Q("13/16"),full0=fan.route(completeRoute(xs),0,[q0,q0]),fullp=fan.route(completeRoute(xp),0,[q0,q0]),fullm=fan.route(completeRoute(xm),0,[q0,q0]);
 const fullCurvature=fullp.cost.a(fullm.cost).s(full0.cost.m(2)).dby(eps.m(eps).m(2));
 if(!fullCurvature.eq(curvature))throw Error("complete fan curvature witness");
 for(const t of["0","1/16","1/8"])for(const y of["-1/32","-1/64","0","1/64","1/32"]){
  const Y=Q(y),want=Q("13/16").a(a.m(Q(t))).a((Y.cmp(0)<0?bm:bp).m(Y));
  if(!fan.cdfInterior(Q(t),Q("1/2").a(Y)).eq(want))throw Error("fan realization of local field");realization++;
 }
 return{alpha:a.str(),beta_plus:bp.str(),beta_minus:bm.str(),legs:49,internal_positive_records:24,
 amplitudes:"x_j=2^(j-1)/2^53, j=1..49",epsilon:eps.str(),
 variation:"z_j=min(j,24-j)*epsilon; v_j=z_j-(3/7)z_(j-1), j=1..24; vary positive ranks by +/-v, fix negative and final positive ranks",
 exit_time:f0.t.str(),exit_position_relative:f0.x.str(),record_lower_relative:f0.L.str(),record_upper_relative:f0.M.str(),
 normalized_second_difference:curvature.str(),physical_piece_checks:f0.pieces+fp.pieces+fm.pieces,
 fan_realization_checks:realization,complete_fan_capture_curvature:fullCurvature.str(),complete_fan_affine_capture_pieces:full0.pieces+fullp.pieces+fullm.pieces,scope:"Counterexample to conditional parity concavity of the FULL hinged moment, not to a finite-prefix theorem."};
}
function verifyHingeDeletion(){
 const fan=interfaceFan(),q0=Q("13/16"),x0=Q("1/2"),a=Q("1/4"),B=Q(2),b=Q("1/2"),C=B.s(a),D=B.a(a),P=b.a(a);
 let routes=0,pieces=0,algebra=0,worst=null;
 for(const ps of["1/256","1/128","1/64"])for(const qm of["1/2","1","2","3"]){
  const p=Q(ps),q=p.m(Q(qm)),T=p.a(q),peak=P.m(p).dby(2),rold=C.m(q).dby(2).s(a.m(p)),rnew=C.m(T).dby(2),extra=rnew.s(rold);
  if(rold.cmp(0)<0||a.m(T).cmp(peak)<0||B.dby(C).a("1/2").m(T).cmp("1/8")>0)continue;
  if(!extra.eq(D.m(p).dby(2)))throw Error("extra lower band");
  const bound=B.m(T).m(p).dby(2).m(P.dby(D).s(D.dby(C)));
  if(bound.cmp(0)>=0)throw Error("strict deletion sign");
  const upper=B.m(T).m(peak).dby(D).a(peak.m(peak).dby(2).m(ONE.dby(D).s(ONE.dby(P))));
  const ignoredOldLower=upper.s(B.m(T).dby(C).m(extra));
  if(ignoredOldLower.cmp(bound)>0)throw Error("deletion bound algebra");algebra++;
  for(const up of["0","1/2","1"])for(const low of["0","1/2","1"]){
   const records=[q0.s(rold.m(Q(low))),q0.a(peak.m(Q(up)))];
   const old=[[0,x0],[p.dby(2),x0.a(p.dby(2))],[p,x0],[p.a(q.dby(2)),x0.s(q.dby(2))],[T,x0],[T.a("3/2"),-1],[T.a("7/2"),1]];
   const merged=[[0,x0],[T.dby(2),x0.s(T.dby(2))],[T,x0],[T.a("3/2"),-1],[T.a("7/2"),1]];
   const f=fan.route(old,0,records),g=fan.route(merged,0,records),diff=g.cost.s(f.cost);
   if(diff.cmp(bound)>0)throw Error("independent full-fan hinge deletion");
   const slack=diff.s(bound);if(worst===null||slack.cmp(worst)>0)worst=slack;
   routes++;pieces+=f.pieces+g.pieces;
  }
 }
 return{full_fan_capture_comparisons:routes,affine_capture_pieces:pieces,band_and_bound_identities:algebra,
 maximum_actual_difference_minus_bound:worst.str(),scope:"Two maximal interface tents with flow-overtaken upper peak, including arbitrary old records; future affine persistence is checked explicitly."};
}
function verify(){return{scope:"Exact local two-density initial-prefix identities, a failed-concavity witness, and a conditional hinge deletion. The general finite pre-first-center theorem remains open.",algebra:verifyAlgebra(),curvature:verifyCurvature(),deletion:verifyHingeDeletion()};}
const api={verify,verifyAlgebra,verifyCurvature,verifyHingeDeletion};if(typeof module==="object"&&module.exports)module.exports=api;
if(typeof require==="function"&&require.main===module)console.log(JSON.stringify(verify(),null,2));
return api;
