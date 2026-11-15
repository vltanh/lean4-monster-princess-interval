/* Exact last-crossing oracle over Q(sqrt(623060432741/655898601421)). */
const EXACT_SOURCE="\nfunction gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a;}\nclass BRat{\n constructor(n,d=1n){if(n instanceof BRat){this.n=n.n;this.d=n.d;return;}if(typeof n===\"string\"){let p=n.split(\"/\");if(p.length===2){n=BigInt(p[0]);d=BigInt(p[1]);}else {let [s,e]=n.toLowerCase().split(\"e\");let neg=s[0]===\"-\";if(neg||s[0]===\"+\")s=s.slice(1);let parts=s.split(\".\");let f=parts[1]||\"\";n=BigInt(parts[0]+f)*(neg?-1n:1n);let power=f.length-Number(e||0);if(power>=0)d=10n**BigInt(power);else n*=10n**BigInt(-power);}}else n=BigInt(n);d=BigInt(d);if(d===0n)throw Error(\"zero denominator\");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}\n a(q){q=BQ(q);return new BRat(this.n*q.d+q.n*this.d,this.d*q.d);}\n s(q){q=BQ(q);return new BRat(this.n*q.d-q.n*this.d,this.d*q.d);}\n m(q){q=BQ(q);return new BRat(this.n*q.n,this.d*q.d);}\n dby(q){q=BQ(q);return new BRat(this.n*q.d,this.d*q.n);}\n neg(){return new BRat(-this.n,this.d);}\n cmp(q){q=BQ(q);let z=this.n*q.d-q.n*this.d;return z<0n?-1:z>0n?1:0;}\n eq(q){return this.cmp(q)===0;}\n num(){return Number(this.n)/Number(this.d);}\n str(){return String(this.n)+(this.d===1n?\"\":\"/\"+this.d);}\n}\nfunction BQ(x){return x instanceof BRat?x:new BRat(typeof x===\"number\"?String(x):x);}\n\nconst RADICAND=BQ(\"623060432741/655898601421\");\nconst RZERO=BQ(0);\nfunction safeRationalNumber(x){const a=(x.n<0n?-x.n:x.n).toString(),b=x.d.toString(),aa=a.slice(0,16),bb=b.slice(0,16);return(x.n<0n?-1:1)*Number(aa)/Number(bb)*Math.pow(10,a.length-aa.length-b.length+bb.length);}\nclass Rat{\n constructor(x,d=1n){\n  if(x instanceof Rat){this.aa=x.aa;this.bb=x.bb;return;}\n  if(typeof x===\"string\"&&x.startsWith(\"A[\")&&x.endsWith(\"]\")){const [a,b]=x.slice(2,-1).split(\";\");this.aa=BQ(a);this.bb=BQ(b);return;}\n  this.aa=(d===1n?BQ(x):new BRat(x,d));this.bb=RZERO;\n }\n static from(a,b){const x=Object.create(Rat.prototype);x.aa=BQ(a);x.bb=BQ(b);return x;}\n get n(){if(!this.bb.eq(0))throw Error(\"irrational numerator requested\");return this.aa.n;}\n get d(){if(!this.bb.eq(0))throw Error(\"irrational denominator requested\");return this.aa.d;}\n a(x){x=Q(x);return Rat.from(this.aa.a(x.aa),this.bb.a(x.bb));}\n s(x){x=Q(x);return Rat.from(this.aa.s(x.aa),this.bb.s(x.bb));}\n neg(){return Rat.from(this.aa.neg(),this.bb.neg());}\n m(x){x=Q(x);if(this.bb.eq(0))return Rat.from(this.aa.m(x.aa),this.aa.m(x.bb));if(x.bb.eq(0))return Rat.from(this.aa.m(x.aa),this.bb.m(x.aa));return Rat.from(this.aa.m(x.aa).a(this.bb.m(x.bb).m(RADICAND)),this.aa.m(x.bb).a(this.bb.m(x.aa)));}\n dby(x){x=Q(x);if(x.bb.eq(0))return Rat.from(this.aa.dby(x.aa),this.bb.dby(x.aa));const norm=x.aa.m(x.aa).s(x.bb.m(x.bb).m(RADICAND));return Rat.from(this.aa.m(x.aa).s(this.bb.m(x.bb).m(RADICAND)).dby(norm),this.bb.m(x.aa).s(this.aa.m(x.bb)).dby(norm));}\n cmp(x){x=Q(x);const a=this.aa.s(x.aa),b=this.bb.s(x.bb),sa=a.cmp(0),sb=b.cmp(0);if(sb===0)return sa;if(sa===0)return sb;if(sa===sb)return sa;return sa*a.m(a).cmp(b.m(b).m(RADICAND));}\n eq(x){return this.cmp(x)===0;}\n num(){if(this.bb.eq(0))return safeRationalNumber(this.aa);const a=this.aa,b=this.bb,root=Math.sqrt(safeRationalNumber(RADICAND));if(a.cmp(0)*b.cmp(0)<0){const rat=a.m(a).s(b.m(b).m(RADICAND)).dby(a);return safeRationalNumber(rat)/(1-safeRationalNumber(b.dby(a))*root);}return safeRationalNumber(a)+safeRationalNumber(b)*root;}\n str(){return this.bb.eq(0)?this.aa.str():\"A[\"+this.aa.str()+\";\"+this.bb.str()+\"]\";}\n}\nfunction Q(x){return x instanceof Rat?x:new Rat(typeof x===\"number\"?String(x):x);}\nconst ZERO=Q(0),ONE=Q(1);\nfunction minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}\nfunction maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}\nfunction uniq(xs){let m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}\nfunction bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){let m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}\nfunction coord(x){let z=Q(x);if(z.cmp(0)<0)return coord(z.neg()).neg();const lim=4194304n;if(z.d<=lim)return z;let n=z.n,d=z.d,p0=0n,q0=1n,p1=1n,q1=0n;while(true){let a=n/d,q2=q0+a*q1;if(q2>lim)break;[p0,p1]=[p1,p0+a*p1];[q0,q1]=[q1,q2];[n,d]=[d,n-a*d];}\n let k=(lim-q0)/q1,b1=new Rat(p0+k*p1,q0+k*q1),b2=new Rat(p1,q1);return Math.abs(b1.num()-z.num())<Math.abs(b2.num()-z.num())?b1:b2;}\nfunction subP(a,b){return[a[0].s(b[0]),a[1].s(b[1])];}\nfunction cross(a,b){return a[0].m(b[1]).s(a[1].m(b[0]));}\nclass ExactField{\n constructor(data){\n this.nodes=data.nodes.map(p=>p.map(coord));this.values=(data.rational_values||data.values).map(Q);\n this.grid=[0,1].map(k=>uniq(this.nodes.map(p=>p[k])));this.cells=new Map();this.strips=[new Map(),new Map()];this.triangles=[];\n this.initial=this.nodes.map((p,i)=>[p,this.values[i]]).filter(([p,v])=>p[0].eq(p[1].neg())).map(([p,v])=>[p[0],v]).sort((a,b)=>a[0].cmp(b[0]));this.initialKnots=this.initial.map(p=>p[0]);\n for(const inds of data.triangles){\n let ps=inds.map(i=>this.nodes[i]),[p,q,r]=ps,[e,f]=[subP(q,p),subP(r,p)],det=cross(e,f),[x,y,z]=inds.map(i=>this.values[i]);\n let ru=y.s(x).m(f[1]).s(z.s(x).m(e[1])).dby(det),rv=e[0].m(z.s(x)).s(f[0].m(y.s(x))).dby(det);\n if(ru.cmp(0)<0||rv.cmp(0)>0)throw Error(\"transport\");\n let n=this.triangles.length;this.triangles.push({ps,cf:[ru,rv,x.s(ru.m(p[0])).s(rv.m(p[1]))],positive:det.cmp(0)>0});\n let ranges=[0,1].map(k=>[bisect(this.grid[k],minQ(...ps.map(p=>p[k])),false),bisect(this.grid[k],maxQ(...ps.map(p=>p[k])),false)]);\n for(let k=0;k<2;k++)for(let i=ranges[k][0];i<ranges[k][1];i++){if(!this.strips[k].has(i))this.strips[k].set(i,[]);this.strips[k].get(i).push(n);}\n for(let i=ranges[0][0];i<ranges[0][1];i++)for(let j=ranges[1][0];j<ranges[1][1];j++){let key=i+\",\"+j;if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(n);}\n }\n this.rcache=new Map();this.icache=new Map();\n }\n initialValue(z){z=Q(z);let i=Math.max(0,Math.min(this.initial.length-2,bisect(this.initialKnots,z)-1));let[a,x]=this.initial[i],[b,y]=this.initial[i+1];return x.a(z.s(a).m(y.s(x)).dby(b.s(a)));}\n radial(u,v){u=Q(u);v=Q(v);if(v.cmp(1)>0)return ZERO;let key=u.str()+\",\"+v.str();if(this.rcache.has(key))return this.rcache.get(key);let cell=[u,v].map((p,k)=>Math.max(0,Math.min(this.grid[k].length-2,bisect(this.grid[k],p)-1))),poss=new Set();\n for(let i of[cell[0],cell[0]-1])for(let j of[cell[1],cell[1]-1])for(let n of(this.cells.get(i+\",\"+j)||[]))poss.add(n);\n for(let n of[...poss].sort((a,b)=>a-b)){let {ps,cf,positive}=this.triangles[n];let turns=ps.map((p,i)=>cross(subP(ps[(i+1)%3],p),subP([u,v],p)));if(turns.every(t=>positive?t.cmp(0)>=0:t.cmp(0)<=0)){let z=cf[0].m(u).a(cf[1].m(v)).a(cf[2]);this.rcache.set(key,z);return z;}}\n throw Error(\"no triangle \"+key);\n }\n integral(fixed,left,right,axis,threshold=null){fixed=Q(fixed);left=Q(left);right=Q(right);if(threshold!==null)threshold=Q(threshold);if(right.cmp(left)<=0)return ZERO;\n let key=[fixed.str(),left.str(),right.str(),axis,threshold===null?\"\":threshold.str()].join(\",\");if(this.icache.has(key))return this.icache.get(key);\n if((axis===1&&fixed.cmp(1)>=0)||(axis===0&&left.cmp(1)>=0))return threshold===null?ZERO:maxQ(0,threshold).m(right.s(left));\n if(axis===0&&right.cmp(1)>0)return this.integral(fixed,left,ONE,axis,threshold).a(threshold===null?ZERO:maxQ(0,threshold).m(right.s(1)));\n let i=Math.max(0,Math.min(this.grid[axis].length-2,bisect(this.grid[axis],fixed)-1)),poss=new Set([...(this.strips[axis].get(i)||[]),...(this.strips[axis].get(i-1)||[])]),cuts=[left,right],other=1-axis;\n for(let n of poss){let {ps}=this.triangles[n];for(let k=0;k<3;k++){let a=ps[k],b=ps[(k+1)%3];if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(let x of[a,b])if(x[other].cmp(left)>0&&x[other].cmp(right)<0)cuts.push(x[other]);}else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&fixed.cmp(maxQ(a[axis],b[axis]))<=0){let v=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));if(v.cmp(left)>0&&v.cmp(right)<0)cuts.push(v);}}}\n cuts=uniq(cuts);let total=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],fa=axis===0?this.radial(fixed,a):this.radial(a,fixed),fb=axis===0?this.radial(fixed,b):this.radial(b,fixed);\n if(threshold!==null){fa=threshold.s(fa);fb=threshold.s(fb);if(fa.cmp(0)<=0&&fb.cmp(0)<=0)continue;if(fa.m(fb).cmp(0)<0){let w=b.s(a).m(fa.cmp(0)>0?fa.dby(fa.s(fb)):fb.dby(fb.s(fa)));total=total.a(w.m(maxQ(fa,fb)).dby(2));continue;}}\n total=total.a(b.s(a).m(fa.a(fb)).dby(2));}\n this.icache.set(key,total);return total;\n }\n negativeM1(a){a=Q(a);return this.integral(a,a.neg(),a,0).a(a.m(4)).a(8).s(a.a(3).m(2).m(this.initialValue(a))).s(this.integral(a,a,a.a(2),1)).dby(4);}\n positiveM1(a){a=Q(a);let A=this.initialValue(a);return Q(8).s(a.m(4)).a(Q(3).s(a).m(A)).s(this.integral(a.neg(),a,Q(2).s(a),1)).s(this.integral(Q(2).s(a),a.neg(),ONE,0,A)).dby(4);}\n fixedOne(a,positive){a=Q(a);let A=this.initialValue(a),v=positive?a.neg():a,I=this.integral(v,a,ONE,1),B=this.radial(ONE,v);\n return positive?Q(12).a(A.m(2)).s(Q(7).a(a).m(B)).s(I).s(this.integral(ONE,a.neg(),ONE,0,A)).dby(4):this.integral(a,a.neg(),a,0).a(12).s(A.m(4)).s(Q(7).s(a).m(B)).s(I).dby(4);\n }\n cdfSides(t,x){t=Q(t);x=Q(x);let r=this.radial(t.a(x.cmp(0)<0?x.neg():x),t.s(x.cmp(0)<0?x.neg():x));if(x.eq(0))return[ONE.s(r).dby(2),ONE.a(r).dby(2)];if(x.eq(1))return[ONE.a(r).dby(2),ONE];if(x.eq(-1))return[ZERO,ONE.s(r).dby(2)];let v=x.cmp(0)>0?ONE.a(r).dby(2):ONE.s(r).dby(2);return[v,v];}\n unitRoutePayoff(route){route=route.map(p=>p.map(Q));let[lower,upper]=this.cdfSides(...route[0]),cost=ZERO;\n for(let k=0;k<route.length-1;k++){let[start,x]=route[k],[end,y]=route[k+1];if(end.eq(start)){if(!x.eq(y))throw Error(\"bad duplicate\");continue;}let vel=y.s(x).dby(end.s(start));if(!vel.eq(1)&&!vel.eq(-1))throw Error(\"not unit\");let cuts=[start,end];if(x.m(y).cmp(0)<0)cuts.splice(1,0,start.s(vel.m(x)));let area=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],xa=x.a(vel.m(a.s(start))),xb=x.a(vel.m(b.s(start))),sign=xa.a(xb).cmp(0)>0?1:-1,ua=a.a(xa.m(sign)),va=a.s(xa.m(sign)),ub=b.a(xb.m(sign)),vb=b.s(xb.m(sign)),record=vel.eq(1)?upper:lower;\n if(vel.m(sign).eq(1)){let threshold=sign===1?record.m(2).s(1):ONE.s(record.m(2));area=area.a(this.integral(va,ua,ub,1).s(threshold.m(ub.s(ua))).a(this.integral(va,ua,ub,1,threshold)).dby(4));}\n else{let threshold=sign===-1?ONE.s(record.m(2)):record.m(2).s(1);area=area.a(this.integral(ua,va,vb,0,threshold).dby(4));}}\n let[strict,closed]=this.cdfSides(end,y);if(vel.eq(1)){let updated=maxQ(upper,closed);cost=cost.a(end.m(updated.s(upper))).s(area);upper=updated;}else{let updated=minQ(lower,strict);cost=cost.a(end.m(lower.s(updated))).s(area);lower=updated;}}\n if(!lower.eq(0)||!upper.eq(1))throw Error(\"incomplete\");return cost;\n }\n}\nreturn {Rat,Q,ZERO,ONE,minQ,maxQ,uniq,bisect,ExactField};\n";
function makeOracle(fieldData){
 const X=Function(EXACT_SOURCE)(),{Q,ZERO,ONE,minQ,maxQ,uniq,ExactField}=X;
 const f=new ExactField(fieldData),a=Q("7/8"),b=Q("15/16"),cap=Q("17/16"),zb=f.radial(b,b);
 const T=(t,n)=>t.m(n).a(f.integral(t,t,t.a(2),1,n).dby(2));
 const H=e=>f.integral(e,e,e.a(2),1);
 const valueAt=(t,n,e)=>{
  const N=f.radial(e,t);if(N.cmp(n)<0)return null;
  const I=f.integral(t,t,e,1),te=T(e,n);
  return e.m(4).a(8).s(e.a(6).s(t).m(N)).s(I).s(H(e)).s(te.m(2)).dby(4);
 };
 function minimize(t0,n0,check=true){
  const t=Q(t0),n=Q(n0);if(t.cmp(a)<0||t.cmp(b)>0||n.cmp(f.radial(t,t))<0||n.cmp(ONE)>0)throw Error("state outside domain");
  const cuts=[b,cap,Q(1)];
  function add(q){if(q.cmp(b)>=0&&q.cmp(cap)<=0)cuts.push(q);}
  function pointValue(tr,p){return tr.cf[0].m(p[0]).a(tr.cf[1].m(p[1])).a(tr.cf[2]);}
  for(const tr of f.triangles)if(tr.positive){
   let vmin=tr.ps[0][1],vmax=vmin;
   for(const p of tr.ps){vmin=minQ(vmin,p[1]);vmax=maxQ(vmax,p[1]);add(p[1]);}
   const inRank=vmax.cmp(b)>=0&&vmin.cmp(cap)<=0, inRow=vmin.cmp(t)<=0&&vmax.cmp(t)>=0;
   if(!inRank&&!inRow)continue;
   for(let j=0;j<3;j++){
    const p=tr.ps[j],q=tr.ps[(j+1)%3];
    if(inRow){
     if(p[1].eq(q[1])){if(p[1].eq(t)){add(p[0]);add(q[0]);}}
     else if(minQ(p[1],q[1]).cmp(t)<=0&&maxQ(p[1],q[1]).cmp(t)>=0)
      add(p[0].a(t.s(p[1]).m(q[0].s(p[0])).dby(q[1].s(p[1]))));
    }
    if(inRank){
     const vp=pointValue(tr,p),vq=pointValue(tr,q);
     if(!vp.eq(vq)&&minQ(vp,vq).cmp(n)<=0&&maxQ(vp,vq).cmp(n)>=0)
      add(p[1].a(n.s(vp).m(q[1].s(p[1])).dby(vq.s(vp))));
    }
   }
  }
  let cc=uniq(cuts);
  for(let j=0;j+1<cc.length;j++){
   const l=cc[j],r=cc[j+1],fl=f.radial(l,t).s(n),fr=f.radial(r,t).s(n);
   if(fl.m(fr).cmp(ZERO)<0)add(l.s(fl.m(r.s(l)).dby(fr.s(fl))));
  }
  cc=uniq(cuts);
  const tn=T(t,n);let best=null,intervals=0,quarters=0,identities=0,stationary=0;
  const accept=(e,W,label)=>{
   if(W===null)return;
   if(best===null||W.cmp(best.W)<0)best={e,W,label};
  };
  for(const e of cc)accept(e,valueAt(t,n,e),"boundary");
  for(let j=0;j+1<cc.length;j++){
   const l=cc[j],r=cc[j+1],h=r.s(l),mid=l.a(r).dby(2);
   if(f.radial(mid,t).cmp(n)<0)continue;
   const v0=valueAt(t,n,l),v1=valueAt(t,n,r),vm=valueAt(t,n,mid);
   if(v0===null||v1===null||vm===null)throw Error("useful interval split missing");
   const AA=v1.a(v0).s(vm.m(2)).m(2),BB=v1.s(v0).s(AA);intervals++;
   const poly=u=>v0.a(BB.m(u)).a(AA.m(u.m(u)));
   if(check){
    for(const u of [Q("1/4"),Q("3/4")]){
     const e=l.a(h.m(u)),actual=valueAt(t,n,e);
     if(!actual.eq(poly(u)))throw Error("quadratic arrangement failure");quarters++;
    }
    const N=f.radial(mid,t),direct=T(t,N).s(tn).a(T(mid,N).s(T(mid,n))).dby(2).a(mid.a(2).m(ONE.s(N))).a(tn.dby(2));
    if(!direct.eq(vm))throw Error("crossing kernel identity");identities++;
   }
   if(AA.cmp(ZERO)>0){
    const u=BB.neg().dby(AA.m(2));
    if(u.cmp(ZERO)>0&&u.cmp(ONE)<0){stationary++;accept(l.a(h.m(u)),poly(u),"stationary");}
   }
  }
  const endW=T(t,ONE).a(t.a(3).m(ONE.s(n))).dby(2);
  let waitV;
  if(n.cmp(zb)>=0)waitV=b.a(2).m(ONE.s(n));
  else{
   const d=Q("10184278599/976562500"),c=Q("-71289950193/7812500000");
   waitV=zb.s(n).m(zb.a(n).dby(2).s(c)).dby(d).a(b.a(2).m(ONE.s(zb)));
  }
  const waitW=waitV.a(tn.dby(2));
  const result={state:{t:t.str(),n:n.str()},cuts:cc.length,intervals,quadratic_quarter_checks:quarters,primitive_identity_checks:identities,stationary_candidates:stationary,
   crossing:best?{return:best.e.str(),W:best.W.str(),V:best.W.s(tn.dby(2)).str(),numerical_value:best.W.s(tn.dby(2)).num(),type:best.label}:null,
   endpoint:{W:endW.str(),V:endW.s(tn.dby(2)).str(),numerical_value:endW.s(tn.dby(2)).num()},
   wait_to_b:{W:waitW.str(),V:waitV.str(),numerical_value:waitV.num()}};
  return result;
 }
 return {minimize,field:f,T};
}

function verify(fieldData){
 const oracle=makeOracle(fieldData),f=oracle.field;
 // The oracle's rational class is deliberately reused throughout this audit.
 const a=f.triangles[721].ps.find(p=>p[0].eq(p[1]))[0].constructor;
 const Q=v=>v instanceof a?v:new a(v),ZERO=Q(0),ONE=Q(1);
 const left=Q("7/8"),b=Q("15/16"),cap=Q("17/16"),cf=f.triangles[721].cf,zb=f.radial(b,b);
 let futureVertices=0,futureMax=ZERO,rowVertices=0,rowFailures=0,flatTriangles=0,flatFailures=0,modelVertices=0,modelMin=null,lineCross=0;
 const nonflat=[],v1=new Map();
 for(let i=0;i<f.triangles.length;i++){
  const tr=f.triangles[i];if(!tr.positive)continue;
  let u0=tr.ps[0][0],u1=u0,v0=tr.ps[0][1],vmax=v0;
  for(const p of tr.ps){if(p[0].cmp(u0)<0)u0=p[0];if(p[0].cmp(u1)>0)u1=p[0];if(p[1].cmp(v0)<0)v0=p[1];if(p[1].cmp(vmax)>0)vmax=p[1];}
  if((u0.cmp(cap)<0&&u1.cmp(cap)>0)||(v0.cmp(left)<0&&vmax.cmp(left)>0)||(v0.cmp(b)<0&&vmax.cmp(b)>0))lineCross++;
  if(u0.cmp(cap)>=0&&v0.cmp(left)>=0&&vmax.cmp(b)<=0){flatTriangles++;if(!tr.cf[0].eq(ZERO))flatFailures++;}
  if(u0.cmp(b)>=0&&vmax.cmp(left)>0&&v0.cmp(b)<0&&tr.cf[0].cmp(ZERO)>0)
   nonflat.push({triangle:i,ps:tr.ps.map(p=>p.map(q=>q.str())),ru:tr.cf[0].str(),rv:tr.cf[1].str(),c:tr.cf[2].str()});
  for(const p of tr.ps){
   const actual=tr.cf[0].m(p[0]).a(tr.cf[1].m(p[1])).a(tr.cf[2]);
   if(p[1].eq(ONE))v1.set(p[0].str(),actual);
   if(p[1].cmp(b)>=0){
    futureVertices++;if(actual.cmp(futureMax)>0)futureMax=actual;
    if(p[1].eq(b)){rowVertices++;if(!actual.eq(zb))rowFailures++;}
   }
   if(v0.cmp(left)>=0&&vmax.cmp(b)<=0){
    const gap=cf[0].m(p[0]).a(cf[1].m(p[1])).a(cf[2]).s(actual);modelVertices++;
    if(modelMin===null||gap.cmp(modelMin)<0)modelMin=gap;
   }
  }
 }
 const endpointModel=cf[0].a(cf[1]).m(left).a(cf[2]).a(cf[0].m(2));
 if(futureMax.cmp(zb)>0||rowFailures||flatFailures||lineCross||modelMin.cmp(ZERO)<0||endpointModel.cmp(ONE)<0||[...v1.values()].some(x=>!x.eq(ZERO)))throw Error("crossing field gate failed");
 const states=[["57/64","10184278599/62500000000"],["57/64","3/5"],["57/64","13/20"],["57/64","7/10"],["29/32","3/5"],["59/64","3/5"]];
 const queries=states.map(([t,n])=>oracle.minimize(t,n,true));
 return {scope:"Exact saved-field crossing gates and fixed-state continuum crossing minima. This is not a globally optimized center value or a game bound.",
  field_blob:"5c45d042ee9948faebc03354c3e1e2ee3cbec1a5",
  gates:{a:left.str(),b:b.str(),cap:cap.str(),z_b:zb.str(),future_vertices:futureVertices,future_max:futureMax.str(),row_b_vertices:rowVertices,row_b_failures:rowFailures,
   flat_triangles:flatTriangles,nonzero_flat_u_slopes:flatFailures,grid_line_crossings:lineCross,model_vertices:modelVertices,minimum_affine_model_gap:modelMin.str(),minimum_closed_endpoint_model:endpointModel.str(),outgoing_v1_nodes:v1.size,outgoing_v1_atom:false},
  incoming_exterior_pieces:nonflat,
  aggregate:{queries:queries.length,quadratic_intervals:queries.reduce((s,q)=>s+q.intervals,0),quarter_checks:queries.reduce((s,q)=>s+q.quadratic_quarter_checks,0),primitive_identities:queries.reduce((s,q)=>s+q.primitive_identity_checks,0),stationary_candidates:queries.reduce((s,q)=>s+q.stationary_candidates,0)},queries};
}
const api={makeOracle,verify};

if(typeof module==="object"&&module.exports)module.exports=api;
if(typeof require==="function"&&require.main===module){
 const fs=require("fs"),path=require("path");
 const input=process.argv[2]||path.join(__dirname,"../interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json");
 console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));
}
return api;
