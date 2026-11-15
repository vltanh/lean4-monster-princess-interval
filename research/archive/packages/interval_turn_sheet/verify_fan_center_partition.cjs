
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

function positiveArea(a,b,fa,fb){
 if(b.cmp(a)<=0||maxQ(fa,fb).cmp(0)<=0)return ZERO;
 if(minQ(fa,fb).cmp(0)>=0)return b.s(a).m(fa.a(fb)).dby(2);
 const f=maxQ(fa,fb),other=minQ(fa,fb);
 return b.s(a).m(f.m(f)).dby(f.s(other).m(2));
}
function positivePrimitive(q,c){return maxQ(0,Q(q).s(c)).m(maxQ(0,Q(q).s(c))).dby(2);}
function ceilQ(q){q=Q(q);if(q.cmp(0)<0)throw Error("negative ceiling");return(q.n+q.d-1n)/q.d;}
class Fan{
 constructor(rows,intervalDensity=false){
  this.rows=rows.map(r=>({w:Q(r.w),lo:Q(r.lo),hi:Q(r.hi),p:r.p.map(x=>x.map(Q))}));
  if(!intervalDensity&&!this.rows.reduce((s,r)=>s.a(r.w),ZERO).eq(1))throw Error("weights");
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
 route(route,n=0){
  route=route.map(p=>p.map(Q));n=Q(n);
  if(!route[0][1].eq(0))throw Error("fixture must start at center");
  let lower=ONE.s(n).dby(2),upper=ONE.a(n).dby(2),cost=ZERO,affinePieces=0;
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
function partition(rows,H,intervalDensity=false){
 const fan=new Fan(rows,intervalDensity);H=Q(H);let events=[ZERO,H];
 for(const row of fan.rows){
  for(const[t]of row.p)if(t.cmp(0)>0&&t.cmp(H)<0)events.push(t);
  const ends=uniq([ZERO,H,...row.p.map(x=>x[0]).filter(t=>t.cmp(0)>0&&t.cmp(H)<0)]);
  for(let j=0;j<ends.length-1;j++){
   const L=ends[j],R=ends[j+1],mid=L.a(R).dby(2),b=fan.base(row,mid);
   if(!b.slope.eq(0))for(const off of[row.lo,row.hi]){
    const root=mid.s(b.value.a(off).dby(b.slope));
    if(root.cmp(L)>0&&root.cmp(R)<0)events.push(root);
   }
  }
 }
 events=uniq(events);const blocks=[];let J=0n,edgeChecks=0,identityChecks=0;
 for(let j=0;j<events.length-1;j++){
  const L=events[j],R=events[j+1],mid=L.a(R).dby(2);let allowed=ONE,k=ZERO;const states=[];
  for(const row of fan.rows){
   const b=fan.base(row,mid),edges=[b.value.a(row.lo),b.value.a(row.hi)];
   if(b.slope.eq(0)){for(const edge of edges)if(!edge.eq(0))allowed=minQ(allowed,edge.cmp(0)<0?edge.neg().m(2):edge.m(2));}
   else for(const edge of edges){
    const root=mid.s(edge.dby(b.slope));if(root.cmp(L)>0&&root.cmp(R)<0)throw Error("unpartitioned moving crossing");edgeChecks++;
   }
   const lo=edges[0],hi=edges[1];
   let multiplicity=0;if(lo.cmp(0)<0&&hi.cmp(0)>0)multiplicity=2;
   else if((lo.eq(0)&&hi.cmp(0)>0)||(lo.cmp(0)<0&&hi.eq(0)))multiplicity=1;
   k=k.a(row.w.m(multiplicity).dby(row.hi.s(row.lo).m(2)));
   states.push({row,b,edges});
  }
  const count=ceilQ(R.s(L).dby(allowed)),step=R.s(L).dby(Q(count));J+=count;
  for(const {b,edges}of states)if(b.slope.eq(0))for(const edge of edges)if(!edge.eq(0)){
   if(step.cmp((edge.cmp(0)<0?edge.neg():edge).m(2))>0)throw Error("stationary margin");edgeChecks++;
  }
  if(step.cmp(1)>0)throw Error("endpoint cone margin");
  if(count>10000n)throw Error("fixture partition too large; use compact certificate mode for datasets");
  for(let h=0n;h<count;h++){
   const A=L.a(step.m(Q(h))),B=A.a(step);
   for(const [tf,ef]of[[0,1],["1/4","3/4"],[0,"1/2"],["1/2",1]]){
    const t=A.a(step.m(Q(tf))),e=A.a(step.m(Q(ef)));
    for(const sf of["1/4","1/2","3/4"]){
     const s=t.a(e.s(t).m(Q(sf))),rad=minQ(s.s(t),e.s(s));
     for(const rf of["0","1/2","1"]){
      const rr=rad.m(Q(rf)),got=fan.radial(s,rr),want=k.m(rr).m(2);
      if(!got.eq(want))throw Error("whole-cone fixture identity");identityChecks++;
     }
    }
   }
  }
  blocks.push({left:L.str(),right:R.str(),subintervals:String(count),step:step.str(),k:k.str()});
 }
 return{H:H.str(),J:String(J),balanced_productive_return_bound:String(2n*J-1n),conservative_physical_return_bound:String(2n*J),blocks,edge_checks:edgeChecks,cone_identity_checks:identityChecks};
}
function verifyMerge(){
 let algebra=0,pairing=0,physical=0,physicalPieces=0,worst=null;
 for(const ks of["1/4","1/2","1","2"])for(const ps of["1/20","1/10","1/5"])for(const mult of["1","3/2","2"]){
  const k=Q(ks),p=Q(ps),q=p.m(Q(mult)),N1=k.m(p),N2=k.m(q),N=k.m(p.a(q)),t=Q("1/7"),e=t.a(p).a(q),u=t.a(p);
  if(N.cmp(1)>0)continue;
  const Bt=z=>t.m(z).a(z.m(z).dby(k.m(4))),Bu=z=>u.m(z).a(z.m(z).dby(k.m(4)));
  for(const frac of["0","1/3","2/3","1"]){
   const n=N1.m(Q(frac)),bound=k.m(p).m(q).dby(2).neg().s(n.m(q)).a(n.m(n).dby(k.m(4)));
   if(bound.cmp(0)>=0)throw Error("strict merge bound");
   const local=Bt(N).s(Bt(N1)).s(Bu(N2)).a(Bu(n)).s(n.m(e));
   if(!local.eq(bound))throw Error("merge polynomial algebra");algebra++;
   for(const mode of[0,1,2,3,4]){
    const Be=z=>{
     if(mode===0)return e.m(z);
     if(mode===1)return e.a(1).m(z);
     if(mode===2)return e.m(z).a(z.m(z).dby(4));
     if(mode===3)return e.m(z).a(positivePrimitive(z,"1/3").dby(2));
     return e.m(z).a(z.m(z).dby(6)).a(positivePrimitive(z,"1/4").dby(3)).a(maxQ(0,z.s("3/4")).dby(3));
    };
    const pair=Be(N1).s(Be(n)).s(Be(N).s(Be(N2)));
    if(pair.cmp(n.m(e).neg())>0)throw Error("future inverse monotone pairing");
    const actual=Bt(N).s(Bt(N1)).s(Bu(N2)).a(Bu(n)).a(pair);
    if(actual.cmp(bound)>0)throw Error("kernel upper bound");pairing++;
   }
  }
 }
 for(const Rs of["1/4","1/2","3/4"])for(const pf of["1/4","1/2"])for(const qm of[1,2])for(const ts of["0","1/7"])for(const nf of["0","1/2","1"])for(const future of[0,1,2]){
  const R=Q(Rs),k=ONE.dby(R.m(2)),p=R.m(Q(pf)),q=p.m(qm),t=Q(ts),u=t.a(p),e=u.a(q),n=k.m(p).m(Q(nf));
  let vertices=[[ZERO,ZERO],[e,ZERO]];
  if(future===1)vertices.push([e.a(1),ONE],[e.a(2),ZERO]);
  if(future===2)vertices.push([e.a("1/3"),ZERO],[e.a("5/6"),Q("1/2")],[e.a("4/3"),ZERO]);
  const fan=new Fan([{w:1,lo:R.neg(),hi:R,p:vertices}]);
  const two=[[t,0],[t.a(p.dby(2)),p.dby(2)],[u,0],[u.a(q.dby(2)),q.dby(2).neg()],[e,0],[e.a(1),1],[e.a(3),-1]];
  const merged=[[t,0],[t.a(p.a(q).dby(2)),p.a(q).dby(2)],[e,0],[e.a(1),-1],[e.a(3),1]];
  const a=fan.route(two,n),b=fan.route(merged,n);
  const bound=k.m(p).m(q).dby(2).neg().s(n.m(q)).a(n.m(n).dby(k.m(4)));
  const diff=b.cost.s(a.cost).m(2);
  if(diff.cmp(bound)>0)throw Error("independent physical merge fixture");
  if(worst===null||diff.s(bound).cmp(worst)>0)worst=diff.s(bound);
  physical++;physicalPieces+=a.pieces+b.pieces;
 }
 return{polynomial_identities:algebra,arbitrary_future_inverse_pairings:pairing,independent_ordered_capture_routes:physical,affine_capture_pieces:physicalPieces,maximum_physical_difference_minus_bound:worst.str()};
}
function verifyCount(){
 let cases=0;
 for(let J=1;J<=5;J++){
  const points=Array.from({length:2*J+1},(_,i)=>Q(i).dby(2)),interior=points.length-2;
  for(let mask=0;mask<(1<<interior);mask++){
   let ts=[points[0],...points.slice(1,-1).filter((_,i)=>(mask>>i)&1),points[points.length-1]];
   let changed=true;
   while(changed){
    changed=false;
    for(let j=0;j<ts.length-2;j++){
     const same=Array.from({length:J},(_,k)=>k).some(k=>ts[j].cmp(k)>=0&&ts[j+2].cmp(k+1)<=0);
     if(same){ts.splice(j+1,1);changed=true;break;}
    }
   }
   const inside=[],cross=[];
   for(let j=0;j<ts.length-1;j++){
    const holders=Array.from({length:J},(_,k)=>k).filter(k=>ts[j].cmp(k)>=0&&ts[j+1].cmp(k+1)<=0);
    if(holders.length)inside.push(holders[0]);else cross.push(j);
   }
   if(inside.length>J||cross.length>J-1||ts.length-1>2*J-1)throw Error("partition crossing count");
   cases++;
  }
 }return{exhaustive_time_partition_chains:cases};
}

function foldedComponents(rows){
 let total=ZERO;const out=[];
 for(const r of rows){
  const w=Q(r.w),delta=Q(r.delta),p=r.p.map(v=>v.map(Q));
  if(delta.cmp(0)<=0||delta.cmp(1)>0||p.some(v=>v[1].cmp(0)<0||v[1].cmp(1)>0))throw Error("folded outward data");
  total=total.a(w);
  out.push({w,lo:ZERO,hi:delta,p});
  out.push({w,lo:delta.neg(),hi:ZERO,p:p.map(([t,x])=>[t,Q(2).s(x)])});
 }
 if(!total.eq(1))throw Error("folded weights");return out;
}
function verifyFolded(){
 const fixtures=[
  [{w:1,delta:"1/4",p:[[0,0],[1,1],[2,0]]}],
  [{w:"1/2",delta:"1/4",p:[[0,0],["1/2",0],["3/2",1],[2,"1/2"]]},{w:"1/2",delta:1,p:[[0,1],["1/2",1],["3/2",0],[2,0]]}]
 ];
 const partitions=fixtures.map(rows=>partition(foldedComponents(rows),2,true));
 let normalized=0,staticCapture=0,capturePieces=0;
 for(const pp of["0","1/2","3/4","1"])for(const dd of["1/4","1/2","1"]){
  const p=Q(pp),delta=Q(dd),fan=new Fan(foldedComponents([{w:1,delta,p:[[0,p],[2,p]]}]),true);
  for(const t of[0,1,2]){if(!fan.radial(Q(t),ONE).eq(1)||!fan.cdfInterior(Q(t),ONE).eq(1)||!fan.cdfInterior(Q(t),Q(-1)).eq(0))throw Error("folded normalization/no endpoint atom");normalized++;}
  const z=minQ(delta,ONE.s(p)),first=p.m(z).a(z.m(z).dby(2)),rest=Q(2).s(p).m(delta.s(z)).s(delta.m(delta).s(z.m(z)).dby(2)),mean=first.a(rest).dby(delta);
  const got=fan.route([[0,0],[1,1],[3,-1]]);if(!got.cost.eq(ONE.a(mean)))throw Error("folded static capture integral");staticCapture++;capturePieces+=got.pieces;
 }
 return{scope:"Reflected outward fans p_z=1-|1-p-z|, z in[0,delta], then fair reflection. The two interval components form a density representation, not a probability mixture of clipped rows.",partitions,normalization_and_endpoint_trace_checks:normalized,static_ordered_capture_checks:staticCapture,affine_capture_pieces:capturePieces};
}
function verify(){
 const fixtures=[
  [{w:1,lo:0,hi:"1/4",p:[[0,0],["1/2",0],[1,"1/2"],["3/2",0],[2,0]]}],
  [{w:1,lo:"-1/4",hi:"1/4",p:[[0,"1/4"],[1,"1/4"],["3/2","3/4"],[2,"1/4"]]}],
  [{w:"1/2",lo:"-1/8",hi:"3/8",p:[[0,0],["1/2","1/2"],[1,"1/2"],["3/2",0],[2,0]]},{w:"1/2",lo:"-1/2",hi:"-1/4",p:[[0,"1/4"],["1/2","1/4"],[1,"3/4"],["3/2","1/4"],[2,"1/4"]]}],
  [{w:"1/3",lo:0,hi:"1/8",p:[[0,0],[2,0]]},{w:"2/3",lo:"-1/3",hi:"1/3",p:[[0,"-1/2"],["1/2",0],[1,"1/2"],["3/2",0],[2,"-1/2"]]}]
 ];
 const partitions=fixtures.map(rows=>partition(rows,2));
 return{scope:"Exact stationary-cone merge and finite center-return partition for ordered fixed-interval bang-bang translation fans. It does not reduce arbitrary same-side prefixes before the first center. No game value or matching law is claimed.",
 merge:verifyMerge(),count:verifyCount(),partitions,folded_outward:verifyFolded(),
 conventions:{field:"ordered common-quantile realization of the symmetric marginal",intervals:"general fixed nondegenerate [lo,hi], including outward [0,delta]",endpoint:"clipping atoms retained by strict/closed traces; within-cell diamonds have duration <=1",future:"merge uses only monotonicity and beta_e>=e outside the cone",physical_count:"balanced renewal <=2J-1; conservative physical action realization <=2J before static completion"}};
}
const api={Rat,Q,Fan,partition,foldedComponents,verify};if(typeof module==="object"&&module.exports)module.exports=api;
if(typeof require==="function"&&require.main===module)console.log(JSON.stringify(verify(),null,2));
return api;
