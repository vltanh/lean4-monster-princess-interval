/* Exact rational affine-cell center-renewal fixtures.
   Pure V8 / CommonJS. This is a local verification component, not a game value. */
const EXACT_SOURCE="\nfunction gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a;}\nclass Rat{\n constructor(n,d=1n){if(n instanceof Rat){this.n=n.n;this.d=n.d;return;}if(typeof n===\"string\"){let p=n.split(\"/\");if(p.length===2){n=BigInt(p[0]);d=BigInt(p[1]);}else {let [s,e]=n.toLowerCase().split(\"e\");let neg=s[0]===\"-\";if(neg||s[0]===\"+\")s=s.slice(1);let parts=s.split(\".\");let f=parts[1]||\"\";n=BigInt(parts[0]+f)*(neg?-1n:1n);let power=f.length-Number(e||0);if(power>=0)d=10n**BigInt(power);else n*=10n**BigInt(-power);}}else n=BigInt(n);d=BigInt(d);if(d===0n)throw Error(\"zero denominator\");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}\n a(q){q=Q(q);return new Rat(this.n*q.d+q.n*this.d,this.d*q.d);}\n s(q){q=Q(q);return new Rat(this.n*q.d-q.n*this.d,this.d*q.d);}\n m(q){q=Q(q);return new Rat(this.n*q.n,this.d*q.d);}\n dby(q){q=Q(q);return new Rat(this.n*q.d,this.d*q.n);}\n neg(){return new Rat(-this.n,this.d);}\n cmp(q){q=Q(q);let z=this.n*q.d-q.n*this.d;return z<0n?-1:z>0n?1:0;}\n eq(q){return this.cmp(q)===0;}\n num(){return Number(this.n)/Number(this.d);}\n str(){return String(this.n)+(this.d===1n?\"\":\"/\"+this.d);}\n}\nfunction Q(x){return x instanceof Rat?x:new Rat(typeof x===\"number\"?String(x):x);}\nconst ZERO=Q(0),ONE=Q(1);\nfunction minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}\nfunction maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}\nfunction uniq(xs){let m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}\nfunction bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){let m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}\nfunction coord(x){let z=Q(x);if(z.cmp(0)<0)return coord(z.neg()).neg();const lim=4194304n;if(z.d<=lim)return z;let n=z.n,d=z.d,p0=0n,q0=1n,p1=1n,q1=0n;while(true){let a=n/d,q2=q0+a*q1;if(q2>lim)break;[p0,p1]=[p1,p0+a*p1];[q0,q1]=[q1,q2];[n,d]=[d,n-a*d];}\n let k=(lim-q0)/q1,b1=new Rat(p0+k*p1,q0+k*q1),b2=new Rat(p1,q1);return Math.abs(b1.num()-z.num())<Math.abs(b2.num()-z.num())?b1:b2;}\nfunction subP(a,b){return[a[0].s(b[0]),a[1].s(b[1])];}\nfunction cross(a,b){return a[0].m(b[1]).s(a[1].m(b[0]));}\nclass ExactField{\n constructor(data){\n this.nodes=data.nodes.map(p=>p.map(coord));this.values=(data.rational_values||data.values).map(Q);\n this.grid=[0,1].map(k=>uniq(this.nodes.map(p=>p[k])));this.cells=new Map();this.strips=[new Map(),new Map()];this.triangles=[];\n this.initial=this.nodes.map((p,i)=>[p,this.values[i]]).filter(([p,v])=>p[0].eq(p[1].neg())).map(([p,v])=>[p[0],v]).sort((a,b)=>a[0].cmp(b[0]));this.initialKnots=this.initial.map(p=>p[0]);\n for(const inds of data.triangles){\n let ps=inds.map(i=>this.nodes[i]),[p,q,r]=ps,[e,f]=[subP(q,p),subP(r,p)],det=cross(e,f),[x,y,z]=inds.map(i=>this.values[i]);\n let ru=y.s(x).m(f[1]).s(z.s(x).m(e[1])).dby(det),rv=e[0].m(z.s(x)).s(f[0].m(y.s(x))).dby(det);\n if(ru.cmp(0)<0||rv.cmp(0)>0)throw Error(\"transport\");\n let n=this.triangles.length;this.triangles.push({ps,cf:[ru,rv,x.s(ru.m(p[0])).s(rv.m(p[1]))],positive:det.cmp(0)>0});\n let ranges=[0,1].map(k=>[bisect(this.grid[k],minQ(...ps.map(p=>p[k])),false),bisect(this.grid[k],maxQ(...ps.map(p=>p[k])),false)]);\n for(let k=0;k<2;k++)for(let i=ranges[k][0];i<ranges[k][1];i++){if(!this.strips[k].has(i))this.strips[k].set(i,[]);this.strips[k].get(i).push(n);}\n for(let i=ranges[0][0];i<ranges[0][1];i++)for(let j=ranges[1][0];j<ranges[1][1];j++){let key=i+\",\"+j;if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(n);}\n }\n this.rcache=new Map();this.icache=new Map();\n }\n initialValue(z){z=Q(z);let i=Math.max(0,Math.min(this.initial.length-2,bisect(this.initialKnots,z)-1));let[a,x]=this.initial[i],[b,y]=this.initial[i+1];return x.a(z.s(a).m(y.s(x)).dby(b.s(a)));}\n radial(u,v){u=Q(u);v=Q(v);if(v.cmp(1)>0)return ZERO;let key=u.str()+\",\"+v.str();if(this.rcache.has(key))return this.rcache.get(key);let cell=[u,v].map((p,k)=>Math.max(0,Math.min(this.grid[k].length-2,bisect(this.grid[k],p)-1))),poss=new Set();\n for(let i of[cell[0],cell[0]-1])for(let j of[cell[1],cell[1]-1])for(let n of(this.cells.get(i+\",\"+j)||[]))poss.add(n);\n for(let n of[...poss].sort((a,b)=>a-b)){let {ps,cf,positive}=this.triangles[n];let turns=ps.map((p,i)=>cross(subP(ps[(i+1)%3],p),subP([u,v],p)));if(turns.every(t=>positive?t.cmp(0)>=0:t.cmp(0)<=0)){let z=cf[0].m(u).a(cf[1].m(v)).a(cf[2]);this.rcache.set(key,z);return z;}}\n throw Error(\"no triangle \"+key);\n }\n integral(fixed,left,right,axis,threshold=null){fixed=Q(fixed);left=Q(left);right=Q(right);if(threshold!==null)threshold=Q(threshold);if(right.cmp(left)<=0)return ZERO;\n let key=[fixed.str(),left.str(),right.str(),axis,threshold===null?\"\":threshold.str()].join(\",\");if(this.icache.has(key))return this.icache.get(key);\n if((axis===1&&fixed.cmp(1)>=0)||(axis===0&&left.cmp(1)>=0))return threshold===null?ZERO:maxQ(0,threshold).m(right.s(left));\n if(axis===0&&right.cmp(1)>0)return this.integral(fixed,left,ONE,axis,threshold).a(threshold===null?ZERO:maxQ(0,threshold).m(right.s(1)));\n let i=Math.max(0,Math.min(this.grid[axis].length-2,bisect(this.grid[axis],fixed)-1)),poss=new Set([...(this.strips[axis].get(i)||[]),...(this.strips[axis].get(i-1)||[])]),cuts=[left,right],other=1-axis;\n for(let n of poss){let {ps}=this.triangles[n];for(let k=0;k<3;k++){let a=ps[k],b=ps[(k+1)%3];if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(let x of[a,b])if(x[other].cmp(left)>0&&x[other].cmp(right)<0)cuts.push(x[other]);}else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&fixed.cmp(maxQ(a[axis],b[axis]))<=0){let v=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));if(v.cmp(left)>0&&v.cmp(right)<0)cuts.push(v);}}}\n cuts=uniq(cuts);let total=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],fa=axis===0?this.radial(fixed,a):this.radial(a,fixed),fb=axis===0?this.radial(fixed,b):this.radial(b,fixed);\n if(threshold!==null){fa=threshold.s(fa);fb=threshold.s(fb);if(fa.cmp(0)<=0&&fb.cmp(0)<=0)continue;if(fa.m(fb).cmp(0)<0){let w=b.s(a).m(fa.cmp(0)>0?fa.dby(fa.s(fb)):fb.dby(fb.s(fa)));total=total.a(w.m(maxQ(fa,fb)).dby(2));continue;}}\n total=total.a(b.s(a).m(fa.a(fb)).dby(2));}\n this.icache.set(key,total);return total;\n }\n negativeM1(a){a=Q(a);return this.integral(a,a.neg(),a,0).a(a.m(4)).a(8).s(a.a(3).m(2).m(this.initialValue(a))).s(this.integral(a,a,a.a(2),1)).dby(4);}\n positiveM1(a){a=Q(a);let A=this.initialValue(a);return Q(8).s(a.m(4)).a(Q(3).s(a).m(A)).s(this.integral(a.neg(),a,Q(2).s(a),1)).s(this.integral(Q(2).s(a),a.neg(),ONE,0,A)).dby(4);}\n fixedOne(a,positive){a=Q(a);let A=this.initialValue(a),v=positive?a.neg():a,I=this.integral(v,a,ONE,1),B=this.radial(ONE,v);\n return positive?Q(12).a(A.m(2)).s(Q(7).a(a).m(B)).s(I).s(this.integral(ONE,a.neg(),ONE,0,A)).dby(4):this.integral(a,a.neg(),a,0).a(12).s(A.m(4)).s(Q(7).s(a).m(B)).s(I).dby(4);\n }\n cdfSides(t,x){t=Q(t);x=Q(x);let r=this.radial(t.a(x.cmp(0)<0?x.neg():x),t.s(x.cmp(0)<0?x.neg():x));if(x.eq(0))return[ONE.s(r).dby(2),ONE.a(r).dby(2)];if(x.eq(1))return[ONE.a(r).dby(2),ONE];if(x.eq(-1))return[ZERO,ONE.s(r).dby(2)];let v=x.cmp(0)>0?ONE.a(r).dby(2):ONE.s(r).dby(2);return[v,v];}\n unitRoutePayoff(route){route=route.map(p=>p.map(Q));let[lower,upper]=this.cdfSides(...route[0]),cost=ZERO;\n for(let k=0;k<route.length-1;k++){let[start,x]=route[k],[end,y]=route[k+1];if(end.eq(start)){if(!x.eq(y))throw Error(\"bad duplicate\");continue;}let vel=y.s(x).dby(end.s(start));if(!vel.eq(1)&&!vel.eq(-1))throw Error(\"not unit\");let cuts=[start,end];if(x.m(y).cmp(0)<0)cuts.splice(1,0,start.s(vel.m(x)));let area=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],xa=x.a(vel.m(a.s(start))),xb=x.a(vel.m(b.s(start))),sign=xa.a(xb).cmp(0)>0?1:-1,ua=a.a(xa.m(sign)),va=a.s(xa.m(sign)),ub=b.a(xb.m(sign)),vb=b.s(xb.m(sign)),record=vel.eq(1)?upper:lower;\n if(vel.m(sign).eq(1)){let threshold=sign===1?record.m(2).s(1):ONE.s(record.m(2));area=area.a(this.integral(va,ua,ub,1).s(threshold.m(ub.s(ua))).a(this.integral(va,ua,ub,1,threshold)).dby(4));}\n else{let threshold=sign===-1?ONE.s(record.m(2)):record.m(2).s(1);area=area.a(this.integral(ua,va,vb,0,threshold).dby(4));}}\n let[strict,closed]=this.cdfSides(end,y);if(vel.eq(1)){let updated=maxQ(upper,closed);cost=cost.a(end.m(updated.s(upper))).s(area);upper=updated;}else{let updated=minQ(lower,strict);cost=cost.a(end.m(lower.s(updated))).s(area);lower=updated;}}\n if(!lower.eq(0)||!upper.eq(1))throw Error(\"incomplete\");return cost;\n }\n}\nreturn {Rat,Q,ZERO,ONE,minQ,maxQ,uniq,bisect,ExactField};\n";
const {Q,ZERO,ONE,minQ,maxQ,uniq}=Function(EXACT_SOURCE)();
function assert(x,s){if(!x)throw Error(s);}
const sq=x=>x.m(x), pos=x=>maxQ(x,ZERO);
function verify(){
 const count={parameters:0,riccati:0,triangle_identities:0,triangle_nonnegative:0,
 wait_identities:0,wait_nonnegative:0,physical_intersections:0,
 primitive_integrals:0,slope_and_concavity:0,equality_chain:0,truncation_residual:0};
 const examples=[];
 for(const w0 of ["1","7/8","3/4","1/2","1/4","1/8"])
 for(const k0 of ["2","5/2","3"])
 for(const c0 of ["0","1/20"])
 for(const t0 of ["1/100","1/25"])
 for(const y0 of ["1/200","1/100"]){
  const w=Q(w0), k=Q(k0), c=Q(c0), t=Q(t0), y=Q(y0);
  const r=ONE.s(sq(w)).dby(8), l=k.m(r), d=k.s(l), B=Q(2).dby(sq(ONE.a(w)));
  const b=B.dby(k), aa=b.a(ONE.dby(k.m(8))), theta=Q(4).m(r).m(B);
  const gamma=Q(4).dby(k.m(w).m(ONE.a(w))), end=t.a(gamma.m(y));
  const z=u=>d.m(u).a(c), beta=(u,q)=>u.a(pos(q.s(z(u))).dby(k.m(2)));
  const T=(u,q)=>u.m(q).a(sq(pos(q.s(z(u)))).dby(k.m(4)));
  const C=Q(3);
  const W=(u,q)=>{const yy=q.s(z(u));return C.a(c.m(u).dby(2)).s(u.m(yy).dby(2)).s(b.m(sq(yy)));};
  const V=(u,q)=>W(u,q).s(T(u,q).dby(2));
  const n=z(t).a(y), A=Q(4).m(B).m(ONE.s(r)).s(Q(3).a(r).dby(2));
  count.parameters++;
  assert(B.m(8).m(Q("1/4").s(r).s(B.m(2).m(sq(r)))).eq(ONE),"Riccati");count.riccati++;
  assert(theta.eq(ONE.s(w).dby(ONE.a(w)))&&theta.cmp(ONE)<0,"geometric factor");count.riccati++;
  assert(A.cmp(ZERO)>0&&b.cmp(ZERO)>0&&B.cmp(Q("1/8"))>=0,"shape");count.slope_and_concavity++;
  assert(end.cmp(ONE)<0&&z(end).cmp(ONE)<0,"local physical range");
  const yy=y.dby(k);
  const hs=uniq([ZERO,yy.dby(4),yy.dby(2),yy,yy.dby(ONE.s(r)),
   yy.a(yy.dby(ONE.s(r))).dby(2),yy.m(B).m(4),yy.m(B).m(8)]);
  function p(q,s){
   if(s.cmp(ONE)<=0)return pos(q.s(c).s(d.m(s))).dby(k.a(l));
   return minQ(s.s(ONE),ONE);
  }
  function direct(q,sign,h){
   const e=t.a(h), center=pos(q.s(c)).dby(d);
   const ps=uniq([ZERO,center,ONE,Q(2),Q(6)]).map(u=>[u,p(q,u).m(sign)]);
   const ms=h.eq(ZERO)?[[t,ZERO]]:[[t,ZERO],[t.a(h.dby(2)),h.dby(2)],[e,ZERO]];
   if(h.eq(ZERO))return p(q,t).eq(ZERO)?t:null;
   let best=null;
   for(let i=0;i+1<ps.length;i++)for(let j=0;j+1<ms.length;j++){
    const [pa,pb]=[ps[i],ps[i+1]], [ma,mb]=[ms[j],ms[j+1]];
    const lo=maxQ(pa[0],ma[0]),hi=minQ(pb[0],mb[0]);if(lo.cmp(hi)>0)continue;
    const lerp=(a,b,u)=>a[1].a(b[1].s(a[1]).m(u.s(a[0])).dby(b[0].s(a[0])));
    const fl=lerp(ma,mb,lo).s(lerp(pa,pb,lo)), fh=lerp(ma,mb,hi).s(lerp(pa,pb,hi));
    let hit=null;
    if(fl.eq(ZERO))hit=lo;else if(fh.eq(ZERO))hit=hi;
    else if(fl.cmp(ZERO)*fh.cmp(ZERO)<0)hit=lo.s(fl.m(hi.s(lo)).dby(fh.s(fl)));
    if(hit!==null&&(best===null||hit.cmp(best)<0))best=hit;
   }return best;
  }
  for(const h of hs){
   const e=t.a(h), rho=z(t).a(k.m(h)), N=maxQ(n,rho), productive=rho.cmp(n)>=0;
   assert(e.cmp(ONE)<0&&rho.cmp(ONE)<0,"fixture range");
   const raw=W(e,N).m(2).a(T(t,N)).s(T(e,n)).s(W(t,n).m(2));
   let closed;
   if(productive){const A0=Q("1/4").s(r).s(B.m(2).m(sq(r)));closed=k.m(A0).m(sq(h)).s(y.m(h)).a(b.m(2).m(sq(y))).s(sq(pos(y.s(d.m(h)))).dby(k.m(4)));}
   else closed=A.m(h).m(y.s(d.m(h).dby(2)));
   assert(raw.eq(closed),"triangle identity");count.triangle_identities++;
   assert(raw.cmp(ZERO)>=0,"triangle sign");count.triangle_nonnegative++;
   if(productive&&h.cmp(y.dby(d))>=0){
    assert(raw.eq(k.m(sq(h.s(B.m(4).m(y).dby(k)))).dby(B.m(8))),"square");count.triangle_identities++;
   }
   const NW=maxQ(n,z(e));
   const wc=NW.s(n).m(NW.a(n).dby(2).s(c)).dby(d);
   const wr=wc.a(V(e,NW)).s(V(t,n));
   const wclosed=h.cmp(y.dby(d))<=0?
    A.dby(2).m(h).m(y.s(d.m(h).dby(2))):
    sq(y).m(aa.s(ONE.dby(d.m(2))));
   assert(wr.eq(wclosed),"wait identity");count.wait_identities++;
   assert(wr.cmp(ZERO)>=0,"wait sign");count.wait_nonnegative++;
   for(const q of uniq([ZERO,z(t),n,rho,z(e),Q("1/4"),Q("1/2"),ONE])){
    if(q.cmp(ZERO)<0||q.cmp(ONE)>0)continue;
    for(const sign of [1,-1]){
     const actual=direct(q,sign,h);
     const expected=q.cmp(z(t))<=0?t:
      sign===1?(q.cmp(rho)<=0?beta(t,q):null):(q.cmp(z(e))<=0?e:null);
     assert((actual===null&&expected===null)||(actual!==null&&expected!==null&&actual.eq(expected)),"physical intersection");
     count.physical_intersections++;
    }
   }
   for(const q of [n,N]){
    const breaks=uniq([ZERO,minQ(z(t),q),q]);let integral=ZERO;
    for(let j=0;j+1<breaks.length;j++){
     const a=breaks[j],bb=breaks[j+1];integral=integral.a(bb.s(a).m(beta(t,a).a(beta(t,bb))).dby(2));
    }
    assert(integral.eq(T(t,q)),"rank primitive");count.primitive_integrals++;
   }
  }
  let u=t, rank=n, gap=y, spent=ZERO;
  const initial=V(t,n), waitCoef=aa.s(ONE.dby(d.m(2)));
  for(let j=0;j<12;j++){
   const h=B.m(4).m(gap).dby(k), e=u.a(h), next=z(u).a(k.m(h));
   const action=T(u,next).s(T(u,rank)).a(T(e,next)).s(T(e,rank)).dby(2);
   spent=spent.a(action);
   assert(spent.a(V(e,next)).eq(initial),"chain telescoping");count.equality_chain++;
   const nextGap=next.s(z(e));
   assert(nextGap.eq(theta.m(gap))&&e.a(gamma.m(nextGap)).eq(end),"chain recurrence");count.equality_chain++;
   assert(e.a(pos(next.s(z(e))).dby(k)).cmp(end)<=0,"inverse stays in wedge");count.equality_chain++;
   const front=z(end), waitCost=front.s(next).m(front.a(next).dby(2).s(c)).dby(d);
   const trunc=spent.a(waitCost).a(V(end,front)).s(initial);
   assert(trunc.eq(waitCoef.m(sq(nextGap))),"finite-truncation residual");count.truncation_residual++;
   u=e;rank=next;gap=nextGap;
  }
  if(examples.length<6&&k0==="2"&&c0==="0"&&t0==="1/100"&&y0==="1/200")
   examples.push({w:w.str(),ratio:r.str(),B:B.str(),theta:theta.str(),limit_time:end.str()});
 }
 return {scope:"Exact local affine-cell renewal algebra and direct rational capture intersections. Crossing actions, front equality, and global attachment remain assumptions.",checks:count,total_checks:Object.values(count).reduce((a,b)=>a+b,0),examples};
}
const api={verify};
if(typeof module==="object"&&module.exports)module.exports=api;
if(typeof require==="function"&&require.main===module)console.log(JSON.stringify(verify(),null,2));
return api;
