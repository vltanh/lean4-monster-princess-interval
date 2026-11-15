/* Exact affine-center chain energy audit; pure V8/CommonJS. */
const EXACT_SOURCE="\nfunction gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a;}\nclass Rat{\n constructor(n,d=1n){if(n instanceof Rat){this.n=n.n;this.d=n.d;return;}if(typeof n===\"string\"){let p=n.split(\"/\");if(p.length===2){n=BigInt(p[0]);d=BigInt(p[1]);}else {let [s,e]=n.toLowerCase().split(\"e\");let neg=s[0]===\"-\";if(neg||s[0]===\"+\")s=s.slice(1);let parts=s.split(\".\");let f=parts[1]||\"\";n=BigInt(parts[0]+f)*(neg?-1n:1n);let power=f.length-Number(e||0);if(power>=0)d=10n**BigInt(power);else n*=10n**BigInt(-power);}}else n=BigInt(n);d=BigInt(d);if(d===0n)throw Error(\"zero denominator\");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}\n a(q){q=Q(q);return new Rat(this.n*q.d+q.n*this.d,this.d*q.d);}\n s(q){q=Q(q);return new Rat(this.n*q.d-q.n*this.d,this.d*q.d);}\n m(q){q=Q(q);return new Rat(this.n*q.n,this.d*q.d);}\n dby(q){q=Q(q);return new Rat(this.n*q.d,this.d*q.n);}\n neg(){return new Rat(-this.n,this.d);}\n cmp(q){q=Q(q);let z=this.n*q.d-q.n*this.d;return z<0n?-1:z>0n?1:0;}\n eq(q){return this.cmp(q)===0;}\n num(){return Number(this.n)/Number(this.d);}\n str(){return String(this.n)+(this.d===1n?\"\":\"/\"+this.d);}\n}\nfunction Q(x){return x instanceof Rat?x:new Rat(typeof x===\"number\"?String(x):x);}\nconst ZERO=Q(0),ONE=Q(1);\nfunction minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}\nfunction maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}\nfunction uniq(xs){let m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}\nfunction bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){let m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}\nfunction coord(x){let z=Q(x);if(z.cmp(0)<0)return coord(z.neg()).neg();const lim=4194304n;if(z.d<=lim)return z;let n=z.n,d=z.d,p0=0n,q0=1n,p1=1n,q1=0n;while(true){let a=n/d,q2=q0+a*q1;if(q2>lim)break;[p0,p1]=[p1,p0+a*p1];[q0,q1]=[q1,q2];[n,d]=[d,n-a*d];}\n let k=(lim-q0)/q1,b1=new Rat(p0+k*p1,q0+k*q1),b2=new Rat(p1,q1);return Math.abs(b1.num()-z.num())<Math.abs(b2.num()-z.num())?b1:b2;}\nfunction subP(a,b){return[a[0].s(b[0]),a[1].s(b[1])];}\nfunction cross(a,b){return a[0].m(b[1]).s(a[1].m(b[0]));}\nclass ExactField{\n constructor(data){\n this.nodes=data.nodes.map(p=>p.map(coord));this.values=(data.rational_values||data.values).map(Q);\n this.grid=[0,1].map(k=>uniq(this.nodes.map(p=>p[k])));this.cells=new Map();this.strips=[new Map(),new Map()];this.triangles=[];\n this.initial=this.nodes.map((p,i)=>[p,this.values[i]]).filter(([p,v])=>p[0].eq(p[1].neg())).map(([p,v])=>[p[0],v]).sort((a,b)=>a[0].cmp(b[0]));this.initialKnots=this.initial.map(p=>p[0]);\n for(const inds of data.triangles){\n let ps=inds.map(i=>this.nodes[i]),[p,q,r]=ps,[e,f]=[subP(q,p),subP(r,p)],det=cross(e,f),[x,y,z]=inds.map(i=>this.values[i]);\n let ru=y.s(x).m(f[1]).s(z.s(x).m(e[1])).dby(det),rv=e[0].m(z.s(x)).s(f[0].m(y.s(x))).dby(det);\n if(ru.cmp(0)<0||rv.cmp(0)>0)throw Error(\"transport\");\n let n=this.triangles.length;this.triangles.push({ps,cf:[ru,rv,x.s(ru.m(p[0])).s(rv.m(p[1]))],positive:det.cmp(0)>0});\n let ranges=[0,1].map(k=>[bisect(this.grid[k],minQ(...ps.map(p=>p[k])),false),bisect(this.grid[k],maxQ(...ps.map(p=>p[k])),false)]);\n for(let k=0;k<2;k++)for(let i=ranges[k][0];i<ranges[k][1];i++){if(!this.strips[k].has(i))this.strips[k].set(i,[]);this.strips[k].get(i).push(n);}\n for(let i=ranges[0][0];i<ranges[0][1];i++)for(let j=ranges[1][0];j<ranges[1][1];j++){let key=i+\",\"+j;if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(n);}\n }\n this.rcache=new Map();this.icache=new Map();\n }\n initialValue(z){z=Q(z);let i=Math.max(0,Math.min(this.initial.length-2,bisect(this.initialKnots,z)-1));let[a,x]=this.initial[i],[b,y]=this.initial[i+1];return x.a(z.s(a).m(y.s(x)).dby(b.s(a)));}\n radial(u,v){u=Q(u);v=Q(v);if(v.cmp(1)>0)return ZERO;let key=u.str()+\",\"+v.str();if(this.rcache.has(key))return this.rcache.get(key);let cell=[u,v].map((p,k)=>Math.max(0,Math.min(this.grid[k].length-2,bisect(this.grid[k],p)-1))),poss=new Set();\n for(let i of[cell[0],cell[0]-1])for(let j of[cell[1],cell[1]-1])for(let n of(this.cells.get(i+\",\"+j)||[]))poss.add(n);\n for(let n of[...poss].sort((a,b)=>a-b)){let {ps,cf,positive}=this.triangles[n];let turns=ps.map((p,i)=>cross(subP(ps[(i+1)%3],p),subP([u,v],p)));if(turns.every(t=>positive?t.cmp(0)>=0:t.cmp(0)<=0)){let z=cf[0].m(u).a(cf[1].m(v)).a(cf[2]);this.rcache.set(key,z);return z;}}\n throw Error(\"no triangle \"+key);\n }\n integral(fixed,left,right,axis,threshold=null){fixed=Q(fixed);left=Q(left);right=Q(right);if(threshold!==null)threshold=Q(threshold);if(right.cmp(left)<=0)return ZERO;\n let key=[fixed.str(),left.str(),right.str(),axis,threshold===null?\"\":threshold.str()].join(\",\");if(this.icache.has(key))return this.icache.get(key);\n if((axis===1&&fixed.cmp(1)>=0)||(axis===0&&left.cmp(1)>=0))return threshold===null?ZERO:maxQ(0,threshold).m(right.s(left));\n if(axis===0&&right.cmp(1)>0)return this.integral(fixed,left,ONE,axis,threshold).a(threshold===null?ZERO:maxQ(0,threshold).m(right.s(1)));\n let i=Math.max(0,Math.min(this.grid[axis].length-2,bisect(this.grid[axis],fixed)-1)),poss=new Set([...(this.strips[axis].get(i)||[]),...(this.strips[axis].get(i-1)||[])]),cuts=[left,right],other=1-axis;\n for(let n of poss){let {ps}=this.triangles[n];for(let k=0;k<3;k++){let a=ps[k],b=ps[(k+1)%3];if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(let x of[a,b])if(x[other].cmp(left)>0&&x[other].cmp(right)<0)cuts.push(x[other]);}else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&fixed.cmp(maxQ(a[axis],b[axis]))<=0){let v=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));if(v.cmp(left)>0&&v.cmp(right)<0)cuts.push(v);}}}\n cuts=uniq(cuts);let total=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],fa=axis===0?this.radial(fixed,a):this.radial(a,fixed),fb=axis===0?this.radial(fixed,b):this.radial(b,fixed);\n if(threshold!==null){fa=threshold.s(fa);fb=threshold.s(fb);if(fa.cmp(0)<=0&&fb.cmp(0)<=0)continue;if(fa.m(fb).cmp(0)<0){let w=b.s(a).m(fa.cmp(0)>0?fa.dby(fa.s(fb)):fb.dby(fb.s(fa)));total=total.a(w.m(maxQ(fa,fb)).dby(2));continue;}}\n total=total.a(b.s(a).m(fa.a(fb)).dby(2));}\n this.icache.set(key,total);return total;\n }\n negativeM1(a){a=Q(a);return this.integral(a,a.neg(),a,0).a(a.m(4)).a(8).s(a.a(3).m(2).m(this.initialValue(a))).s(this.integral(a,a,a.a(2),1)).dby(4);}\n positiveM1(a){a=Q(a);let A=this.initialValue(a);return Q(8).s(a.m(4)).a(Q(3).s(a).m(A)).s(this.integral(a.neg(),a,Q(2).s(a),1)).s(this.integral(Q(2).s(a),a.neg(),ONE,0,A)).dby(4);}\n fixedOne(a,positive){a=Q(a);let A=this.initialValue(a),v=positive?a.neg():a,I=this.integral(v,a,ONE,1),B=this.radial(ONE,v);\n return positive?Q(12).a(A.m(2)).s(Q(7).a(a).m(B)).s(I).s(this.integral(ONE,a.neg(),ONE,0,A)).dby(4):this.integral(a,a.neg(),a,0).a(12).s(A.m(4)).s(Q(7).s(a).m(B)).s(I).dby(4);\n }\n cdfSides(t,x){t=Q(t);x=Q(x);let r=this.radial(t.a(x.cmp(0)<0?x.neg():x),t.s(x.cmp(0)<0?x.neg():x));if(x.eq(0))return[ONE.s(r).dby(2),ONE.a(r).dby(2)];if(x.eq(1))return[ONE.a(r).dby(2),ONE];if(x.eq(-1))return[ZERO,ONE.s(r).dby(2)];let v=x.cmp(0)>0?ONE.a(r).dby(2):ONE.s(r).dby(2);return[v,v];}\n unitRoutePayoff(route){route=route.map(p=>p.map(Q));let[lower,upper]=this.cdfSides(...route[0]),cost=ZERO;\n for(let k=0;k<route.length-1;k++){let[start,x]=route[k],[end,y]=route[k+1];if(end.eq(start)){if(!x.eq(y))throw Error(\"bad duplicate\");continue;}let vel=y.s(x).dby(end.s(start));if(!vel.eq(1)&&!vel.eq(-1))throw Error(\"not unit\");let cuts=[start,end];if(x.m(y).cmp(0)<0)cuts.splice(1,0,start.s(vel.m(x)));let area=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],xa=x.a(vel.m(a.s(start))),xb=x.a(vel.m(b.s(start))),sign=xa.a(xb).cmp(0)>0?1:-1,ua=a.a(xa.m(sign)),va=a.s(xa.m(sign)),ub=b.a(xb.m(sign)),vb=b.s(xb.m(sign)),record=vel.eq(1)?upper:lower;\n if(vel.m(sign).eq(1)){let threshold=sign===1?record.m(2).s(1):ONE.s(record.m(2));area=area.a(this.integral(va,ua,ub,1).s(threshold.m(ub.s(ua))).a(this.integral(va,ua,ub,1,threshold)).dby(4));}\n else{let threshold=sign===-1?ONE.s(record.m(2)):record.m(2).s(1);area=area.a(this.integral(ua,va,vb,0,threshold).dby(4));}}\n let[strict,closed]=this.cdfSides(end,y);if(vel.eq(1)){let updated=maxQ(upper,closed);cost=cost.a(end.m(updated.s(upper))).s(area);upper=updated;}else{let updated=minQ(lower,strict);cost=cost.a(end.m(lower.s(updated))).s(area);lower=updated;}}\n if(!lower.eq(0)||!upper.eq(1))throw Error(\"incomplete\");return cost;\n }\n}\nreturn {Rat,Q,ZERO,ONE,minQ,maxQ,uniq,bisect,ExactField};\n";

function verify(fieldData){
 const {Q,ZERO,ONE,maxQ,ExactField}=Function(EXACT_SOURCE)();
 const f=new ExactField(fieldData), b=Q("15/16");
 const tr=f.triangles[721],k=tr.cf[0],l=tr.cf[1].neg(),d=k.s(l),c=tr.cf[2],r=l.dby(k),A=k.dby(8).s(l.dby(2));
 if(!k.eq(Q("655898601421/62500000000"))||!l.eq(Q("820954217/12500000000")))throw Error("wrong field/cell");
 const z=t=>d.m(t).a(c),T=(t,q)=>t.m(q).a(f.integral(t,t,t.a(2),1,q).dby(2)),sq=x=>x.m(x),pos=x=>maxQ(ZERO,x);
 let checks=0;const traces=[];
 for(const a0 of ["1/128","1/64","3/128"]){
  const a=Q(a0), short=r.m(a), mids=short.a(l.m(a).dby(d)).dby(2);
  for(const hs of [[a],[a,short],[a,mids],[a,a],[a,mids,a],[a,a,short],[a,mids,a,short],[a,short,short.m(r)]]){
   const total=hs.reduce((s,h)=>s.a(h),ZERO),start=b.s(total);if(start.cmp(Q("7/8"))<0)continue;
   let time=start,n=z(start),cost=ZERO;
   for(const h of hs){
    const e=time.a(h),N=z(time).a(k.m(h));if(N.cmp(n)<0)throw Error("nonproductive");
    cost=cost.a(T(time,N).s(T(time,n)).a(T(e,N).s(T(e,n))).dby(2));time=e;n=N;
   }
   cost=cost.a(b.a(2).m(ONE.s(n)));
   const baseline=d.m(sq(b).s(sq(start))).dby(2).a(b.a(2).m(ONE.s(z(b))));
   let energy=A.m(hs.reduce((s,h)=>s.a(sq(h)),ZERO)).s(l.m(3).m(hs.at(-1)).dby(2));
   for(let j=1;j<hs.length;j++){
    energy=energy.s(l.m(hs[j-1]).m(hs[j]).dby(2));
    const gap=pos(l.m(hs[j-1]).s(d.m(hs[j])));
    energy=energy.s(j===hs.length-1?gap.dby(2):sq(gap).dby(k.m(8)));
   }
   if(!cost.s(baseline).eq(energy))throw Error("terminal energy mismatch");
   checks++;traces.push({lengths:hs.map(h=>h.str()),energy:energy.str()});
  }
 }
 const resetChecks=[];
 for(const w0 of ["1/2","3/4","7/8"]){
  const w=Q(w0),theta=ONE.s(w).dby(ONE.a(w)),rr=ONE.s(sq(w)).dby(8),kk=Q(2),ll=kk.m(rr),dd=kk.s(ll),cc=ZERO,t0=Q("1/20"),yy=Q("1/100");
  const zz=t=>dd.m(t).a(cc),TT=(t,q)=>t.m(q).a(sq(pos(q.s(zz(t)))).dby(kk.m(4)));
  const first=yy.dby(kk), short=rr.m(first), hc=first.a(yy.dby(dd)).dby(2);
  for(const hs of [[first],[hc],[first,short],[hc,first],[first,short,first],[first,first,short]]){
   let time=t0,n=zz(t0).a(yy),cost=ZERO;
   for(const h of hs){
    const e=time.a(h),N=zz(time).a(kk.m(h));if(N.cmp(n)<0)throw Error("reset nonproductive");
    cost=cost.a(TT(time,N).s(TT(time,n)).a(TT(e,N).s(TT(e,n))).dby(2));time=e;n=N;
   }
   const tau=time.a(ll.m(hs.at(-1)).dby(dd));
   const baseline=n.a(zz(t0).a(yy)).s(cc.m(2)).m(n.s(zz(t0).a(yy))).dby(dd.m(2));
   const AA=kk.dby(8).s(ll.dby(2)),beta=sq(ll).m(ONE.dby(dd.m(2)).s(ONE.dby(kk.m(8))));
   let E=AA.m(hs.reduce((s,h)=>s.a(sq(h)),ZERO)).s(yy.m(hs[0]).dby(2)).a(sq(yy).m(ONE.dby(dd.m(2)).s(ONE.dby(kk.m(8))))).s(beta.m(sq(hs.at(-1))));
   for(let j=0;j<hs.length;j++){
    if(j)E=E.s(ll.m(hs[j-1]).m(hs[j]).dby(2));
    E=E.s(sq(pos((j?ll.m(hs[j-1]):yy).s(dd.m(hs[j])))).dby(kk.m(8)));
   }
   if(!cost.s(baseline).eq(E))throw Error("reset energy mismatch");
   const B=Q(2).dby(sq(ONE.a(w))),kap=B.dby(kk).a(ONE.dby(kk.m(8))).s(ONE.dby(dd.m(2)));
   if(E.a(kap.m(sq(yy))).cmp(ZERO)<0)throw Error("reset lower bound");
   checks++;resetChecks.push({w:w.str(),tau:tau.str(),energy:E.str()});
  }
 }
 const report={checks,actual_field_terminal_chains:traces.length,analytic_nonfront_resets:resetChecks.length,
 scope:"Exact energy identities including all interior and final short-return hinges; complete actual-field T primitives used for terminal cases.",
 field_blob:"5c45d042ee9948faebc03354c3e1e2ee3cbec1a5",traces,resetChecks};
 const zb=f.radial(b,b);let futureMax=ZERO,vertices=0,rowVertices=0,rowFailures=0,crossing=0;
 for(const cell of f.triangles)if(cell.positive){
  let vl=cell.ps[0][1],vh=vl;
  for(const p of cell.ps){if(p[1].cmp(vl)<0)vl=p[1];if(p[1].cmp(vh)>0)vh=p[1];
   if(p[1].cmp(b)>=0){const value=cell.cf[0].m(p[0]).a(cell.cf[1].m(p[1])).a(cell.cf[2]);if(value.cmp(futureMax)>0)futureMax=value;vertices++;
    if(p[1].eq(b)){rowVertices++;if(!value.eq(zb))rowFailures++;}
   }
  }
  if(vl.cmp(b)<0&&vh.cmp(b)>0)crossing++;
 }
 if(futureMax.cmp(zb)>0||rowFailures||crossing)throw Error("terminal affine gate");
 report.terminal_gate={b:b.str(),z:zb.str(),future_vertex_max:futureMax.str(),vertex_checks:vertices,row_b_vertex_checks:rowVertices,row_failures:rowFailures,triangles_crossing_b:crossing};
 const start=Q("57/64"),firstReturn=Q("229/256"),initial=z(start),rank=f.radial(firstReturn,start);
 const toB=(u,q)=>{const N=maxQ(q,f.radial(b,u));return T(u,N).s(T(u,q)).a(T(b,N).s(T(b,q))).dby(2).a(b.a(2).m(ONE.s(N)));};
 const firstCost=T(start,rank).s(T(start,initial)).a(T(firstReturn,rank).s(T(firstReturn,initial))).dby(2);
 const twoCost=firstCost.a(toB(firstReturn,rank)),oneCost=toB(start,initial),difference=twoCost.s(oneCost);
 if(!difference.eq(Q("-819651265201/16384000000000000")))throw Error("crossing counterexample");
 report.one_crossing_counterexample={scope:"Exact within-cell violation of the one-crossing potential, not a game-value claim",field_blob:report.field_blob,triangle:721,k:k.str(),l:l.str(),d:d.str(),c:c.str(),t:start.str(),e:firstReturn.str(),b:b.str(),n:initial.str(),N:rank.str(),one_crossing_cost:oneCost.str(),two_return_cost:twoCost.str(),cost_difference:difference.str(),four_cost_difference:difference.m(4).str(),numerical_difference:difference.num()};
 return report;
}
const api={verify};
if(typeof module==="object"&&module.exports)module.exports=api;
if(typeof require==="function"&&require.main===module){
 const fs=require("fs"),path=require("path");
 const input=process.argv[2]||path.join(__dirname,"../interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json");
 console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(input,"utf8"))),null,2));
}
return api;
