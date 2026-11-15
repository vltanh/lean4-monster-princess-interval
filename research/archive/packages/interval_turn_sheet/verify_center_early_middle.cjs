const RUNTIME="\nfunction gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a;}\nclass Rat{\n constructor(n,d=1n){if(n instanceof Rat){this.n=n.n;this.d=n.d;return;}if(typeof n===\"string\"){let p=n.split(\"/\");if(p.length===2){n=BigInt(p[0]);d=BigInt(p[1]);}else {let [s,e]=n.toLowerCase().split(\"e\");let neg=s[0]===\"-\";if(neg||s[0]===\"+\")s=s.slice(1);let parts=s.split(\".\");let f=parts[1]||\"\";n=BigInt(parts[0]+f)*(neg?-1n:1n);let power=f.length-Number(e||0);if(power>=0)d=10n**BigInt(power);else n*=10n**BigInt(-power);}}else n=BigInt(n);d=BigInt(d);if(d===0n)throw Error(\"zero denominator\");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}\n a(q){q=Q(q);return new Rat(this.n*q.d+q.n*this.d,this.d*q.d);}\n s(q){q=Q(q);return new Rat(this.n*q.d-q.n*this.d,this.d*q.d);}\n m(q){q=Q(q);return new Rat(this.n*q.n,this.d*q.d);}\n dby(q){q=Q(q);return new Rat(this.n*q.d,this.d*q.n);}\n neg(){return new Rat(-this.n,this.d);}\n cmp(q){q=Q(q);let z=this.n*q.d-q.n*this.d;return z<0n?-1:z>0n?1:0;}\n eq(q){return this.cmp(q)===0;}\n num(){return Number(this.n)/Number(this.d);}\n str(){return String(this.n)+(this.d===1n?\"\":\"/\"+this.d);}\n}\nfunction Q(x){return x instanceof Rat?x:new Rat(typeof x===\"number\"?String(x):x);}\nconst ZERO=Q(0),ONE=Q(1);\nfunction minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}\nfunction maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}\nfunction uniq(xs){let m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}\nfunction bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){let m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}\nfunction coord(x){let z=Q(x);if(z.cmp(0)<0)return coord(z.neg()).neg();const lim=4194304n;if(z.d<=lim)return z;let n=z.n,d=z.d,p0=0n,q0=1n,p1=1n,q1=0n;while(true){let a=n/d,q2=q0+a*q1;if(q2>lim)break;[p0,p1]=[p1,p0+a*p1];[q0,q1]=[q1,q2];[n,d]=[d,n-a*d];}\n let k=(lim-q0)/q1,b1=new Rat(p0+k*p1,q0+k*q1),b2=new Rat(p1,q1);return Math.abs(b1.num()-z.num())<Math.abs(b2.num()-z.num())?b1:b2;}\nfunction subP(a,b){return[a[0].s(b[0]),a[1].s(b[1])];}\nfunction cross(a,b){return a[0].m(b[1]).s(a[1].m(b[0]));}\nclass ExactField{\n constructor(data){\n this.nodes=data.nodes.map(p=>p.map(coord));this.values=(data.rational_values||data.values).map(Q);\n this.grid=[0,1].map(k=>uniq(this.nodes.map(p=>p[k])));this.cells=new Map();this.strips=[new Map(),new Map()];this.triangles=[];\n this.initial=this.nodes.map((p,i)=>[p,this.values[i]]).filter(([p,v])=>p[0].eq(p[1].neg())).map(([p,v])=>[p[0],v]).sort((a,b)=>a[0].cmp(b[0]));this.initialKnots=this.initial.map(p=>p[0]);\n for(const inds of data.triangles){\n let ps=inds.map(i=>this.nodes[i]),[p,q,r]=ps,[e,f]=[subP(q,p),subP(r,p)],det=cross(e,f),[x,y,z]=inds.map(i=>this.values[i]);\n let ru=y.s(x).m(f[1]).s(z.s(x).m(e[1])).dby(det),rv=e[0].m(z.s(x)).s(f[0].m(y.s(x))).dby(det);\n if(ru.cmp(0)<0||rv.cmp(0)>0)throw Error(\"transport\");\n let n=this.triangles.length;this.triangles.push({ps,cf:[ru,rv,x.s(ru.m(p[0])).s(rv.m(p[1]))],positive:det.cmp(0)>0});\n let ranges=[0,1].map(k=>[bisect(this.grid[k],minQ(...ps.map(p=>p[k])),false),bisect(this.grid[k],maxQ(...ps.map(p=>p[k])),false)]);\n for(let k=0;k<2;k++)for(let i=ranges[k][0];i<ranges[k][1];i++){if(!this.strips[k].has(i))this.strips[k].set(i,[]);this.strips[k].get(i).push(n);}\n for(let i=ranges[0][0];i<ranges[0][1];i++)for(let j=ranges[1][0];j<ranges[1][1];j++){let key=i+\",\"+j;if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(n);}\n }\n this.rcache=new Map();this.icache=new Map();\n }\n initialValue(z){z=Q(z);let i=Math.max(0,Math.min(this.initial.length-2,bisect(this.initialKnots,z)-1));let[a,x]=this.initial[i],[b,y]=this.initial[i+1];return x.a(z.s(a).m(y.s(x)).dby(b.s(a)));}\n radial(u,v){u=Q(u);v=Q(v);if(v.cmp(1)>0)return ZERO;let key=u.str()+\",\"+v.str();if(this.rcache.has(key))return this.rcache.get(key);let cell=[u,v].map((p,k)=>Math.max(0,Math.min(this.grid[k].length-2,bisect(this.grid[k],p)-1))),poss=new Set();\n for(let i of[cell[0],cell[0]-1])for(let j of[cell[1],cell[1]-1])for(let n of(this.cells.get(i+\",\"+j)||[]))poss.add(n);\n for(let n of[...poss].sort((a,b)=>a-b)){let {ps,cf,positive}=this.triangles[n];let turns=ps.map((p,i)=>cross(subP(ps[(i+1)%3],p),subP([u,v],p)));if(turns.every(t=>positive?t.cmp(0)>=0:t.cmp(0)<=0)){let z=cf[0].m(u).a(cf[1].m(v)).a(cf[2]);this.rcache.set(key,z);return z;}}\n throw Error(\"no triangle \"+key);\n }\n integral(fixed,left,right,axis,threshold=null){fixed=Q(fixed);left=Q(left);right=Q(right);if(threshold!==null)threshold=Q(threshold);if(right.cmp(left)<=0)return ZERO;\n let key=[fixed.str(),left.str(),right.str(),axis,threshold===null?\"\":threshold.str()].join(\",\");if(this.icache.has(key))return this.icache.get(key);\n if((axis===1&&fixed.cmp(1)>=0)||(axis===0&&left.cmp(1)>=0))return threshold===null?ZERO:maxQ(0,threshold).m(right.s(left));\n if(axis===0&&right.cmp(1)>0)return this.integral(fixed,left,ONE,axis,threshold).a(threshold===null?ZERO:maxQ(0,threshold).m(right.s(1)));\n let i=Math.max(0,Math.min(this.grid[axis].length-2,bisect(this.grid[axis],fixed)-1)),poss=new Set([...(this.strips[axis].get(i)||[]),...(this.strips[axis].get(i-1)||[])]),cuts=[left,right],other=1-axis;\n for(let n of poss){let {ps}=this.triangles[n];for(let k=0;k<3;k++){let a=ps[k],b=ps[(k+1)%3];if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(let x of[a,b])if(x[other].cmp(left)>0&&x[other].cmp(right)<0)cuts.push(x[other]);}else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&fixed.cmp(maxQ(a[axis],b[axis]))<=0){let v=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));if(v.cmp(left)>0&&v.cmp(right)<0)cuts.push(v);}}}\n cuts=uniq(cuts);let total=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],fa=axis===0?this.radial(fixed,a):this.radial(a,fixed),fb=axis===0?this.radial(fixed,b):this.radial(b,fixed);\n if(threshold!==null){fa=threshold.s(fa);fb=threshold.s(fb);if(fa.cmp(0)<=0&&fb.cmp(0)<=0)continue;if(fa.m(fb).cmp(0)<0){let w=b.s(a).m(fa.cmp(0)>0?fa.dby(fa.s(fb)):fb.dby(fb.s(fa)));total=total.a(w.m(maxQ(fa,fb)).dby(2));continue;}}\n total=total.a(b.s(a).m(fa.a(fb)).dby(2));}\n this.icache.set(key,total);return total;\n }\n negativeM1(a){a=Q(a);return this.integral(a,a.neg(),a,0).a(a.m(4)).a(8).s(a.a(3).m(2).m(this.initialValue(a))).s(this.integral(a,a,a.a(2),1)).dby(4);}\n positiveM1(a){a=Q(a);let A=this.initialValue(a);return Q(8).s(a.m(4)).a(Q(3).s(a).m(A)).s(this.integral(a.neg(),a,Q(2).s(a),1)).s(this.integral(Q(2).s(a),a.neg(),ONE,0,A)).dby(4);}\n fixedOne(a,positive){a=Q(a);let A=this.initialValue(a),v=positive?a.neg():a,I=this.integral(v,a,ONE,1),B=this.radial(ONE,v);\n return positive?Q(12).a(A.m(2)).s(Q(7).a(a).m(B)).s(I).s(this.integral(ONE,a.neg(),ONE,0,A)).dby(4):this.integral(a,a.neg(),a,0).a(12).s(A.m(4)).s(Q(7).s(a).m(B)).s(I).dby(4);\n }\n cdfSides(t,x){t=Q(t);x=Q(x);let r=this.radial(t.a(x.cmp(0)<0?x.neg():x),t.s(x.cmp(0)<0?x.neg():x));if(x.eq(0))return[ONE.s(r).dby(2),ONE.a(r).dby(2)];if(x.eq(1))return[ONE.a(r).dby(2),ONE];if(x.eq(-1))return[ZERO,ONE.s(r).dby(2)];let v=x.cmp(0)>0?ONE.a(r).dby(2):ONE.s(r).dby(2);return[v,v];}\n unitRoutePayoff(route){route=route.map(p=>p.map(Q));let[lower,upper]=this.cdfSides(...route[0]),cost=ZERO;\n for(let k=0;k<route.length-1;k++){let[start,x]=route[k],[end,y]=route[k+1];if(end.eq(start)){if(!x.eq(y))throw Error(\"bad duplicate\");continue;}let vel=y.s(x).dby(end.s(start));if(!vel.eq(1)&&!vel.eq(-1))throw Error(\"not unit\");let cuts=[start,end];if(x.m(y).cmp(0)<0)cuts.splice(1,0,start.s(vel.m(x)));let area=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],xa=x.a(vel.m(a.s(start))),xb=x.a(vel.m(b.s(start))),sign=xa.a(xb).cmp(0)>0?1:-1,ua=a.a(xa.m(sign)),va=a.s(xa.m(sign)),ub=b.a(xb.m(sign)),vb=b.s(xb.m(sign)),record=vel.eq(1)?upper:lower;\n if(vel.m(sign).eq(1)){let threshold=sign===1?record.m(2).s(1):ONE.s(record.m(2));area=area.a(this.integral(va,ua,ub,1).s(threshold.m(ub.s(ua))).a(this.integral(va,ua,ub,1,threshold)).dby(4));}\n else{let threshold=sign===-1?ONE.s(record.m(2)):record.m(2).s(1);area=area.a(this.integral(ua,va,vb,0,threshold).dby(4));}}\n let[strict,closed]=this.cdfSides(end,y);if(vel.eq(1)){let updated=maxQ(upper,closed);cost=cost.a(end.m(updated.s(upper))).s(area);upper=updated;}else{let updated=minQ(lower,strict);cost=cost.a(end.m(lower.s(updated))).s(area);lower=updated;}}\n if(!lower.eq(0)||!upper.eq(1))throw Error(\"incomplete\");return cost;\n }\n}\nreturn {Rat,Q,ZERO,ONE,minQ,maxQ,uniq,bisect,ExactField};\n";

function verifyCone(fieldData){
 const X=Function(RUNTIME)(),{Q,ZERO,ONE,minQ,maxQ}=X,f=new X.ExactField(fieldData),hfield=Q("1/2"),lambda=Q("3521265547/12500000000");
 let triangles=0,crossings=0;
 for(const tr of f.triangles)if(tr.positive){
  const us=tr.ps.map(p=>p[0]),vs=tr.ps.map(p=>p[1]),lo=minQ(...us),hi=maxQ(...us),vl=minQ(...vs),vh=maxQ(...vs);
  if(lo.cmp(hfield)<0&&hi.cmp(hfield)>0&&vh.cmp(0)>0)crossings++;
  if(tr.ps.every(([U,V])=>U.cmp(hfield)<=0&&V.cmp(0)>=0)){
   triangles++;if(!tr.cf[0].eq(lambda)||!tr.cf[1].eq(0)||!tr.cf[2].eq(0))throw Error("constant cone coefficient");
  }
 }
 if(crossings)throw Error("unresolved cone boundary cell");
 const betaIntegral=(lam,t,q0,q1)=>{
  const center=lam.m(t),cut=maxQ(q0,minQ(q1,center));
  let ans=t.m(cut.s(q0));
  if(cut.cmp(q1)<0)ans=ans.a(t.m(q1.s(cut)).dby(2)).a(q1.m(q1).s(cut.m(cut)).dby(lam.m(4)));
  return ans;
 };
 let moments=0,frontComparisons=0,stationaryChecks=0;
 for(const ls of ["1/8","1/3","1/2","1"])for(const hs of ["1/4","1/2","3/4"])for(const ts of ["1/4","1/2"]){
  const lam=Q(ls),h=Q(hs),t=h.m(Q(ts)),z=lam.m(t);
  for(const ns of ["0","1/3","2/3","1"]){
   const n=z.a(lam.m(h.s(t)).m(Q(ns))),earliest=n.dby(lam);
   for(const es of ["0","1/2","1"]){
    const e=earliest.a(h.s(earliest).m(Q(es))),N=lam.m(e);
    const primitive=betaIntegral(lam,t,ZERO,N).s(e.m(n)).dby(2);
    const formula=lam.m(e.s(t).m(e.s(t))).dby(8).s(e.m(n.s(z)).dby(2));
    if(!primitive.eq(formula))throw Error("off-front action primitive");moments++;
    const frontTriangle=betaIntegral(lam,t,z,N).a(e.m(N.s(z))).dby(2);
    const wait=N.m(N).s(z.m(z)).dby(lam.m(2));
    if(!frontTriangle.s(wait).eq(lam.m(e.s(t).m(e.s(t))).dby(8)))throw Error("front triangle vs wait");frontComparisons++;
   }
   const y=n.s(z),estar=n.m(2).dby(lam).s(t);
   if(estar.cmp(h)<=0){
    const value=lam.m(estar.s(t).m(estar.s(t))).dby(8).s(estar.m(y).dby(2));
    const reduced=t.m(n).s(n.m(n).dby(lam)).dby(2);
    if(!value.eq(reduced))throw Error("constant boundary stationary identity");stationaryChecks++;
   }
  }
 }
 return {scope:"Exact local primitive identities and saved-field constant-cone gate for the parameter-level attachment theorem. The outside continuation is an explicit unresolved input, not a constant.",field_blob:"5c45d042ee9948faebc03354c3e1e2ee3cbec1a5",field_cone:{h:hfield.str(),lambda:lambda.str(),triangles,boundary_crossings:crossings,center_rank_at_h:lambda.m(hfield).str()},primitive_checks:{offfront_actions:moments,front_triangle_wait:frontComparisons,constant_boundary_stationarity:stationaryChecks}};
}

function verifyMiddle(fieldData){
 const X=Function(RUNTIME)(),{Q,ZERO,minQ,maxQ}=X,f=new X.ExactField(fieldData),h=Q("1/2"),a=Q("7/8"),H=f.radial(h,h);
 const clip=(ps,co)=>{
  const ev=p=>co[0].a(co[1].m(p[0])).a(co[2].m(p[1])),out=[];
  for(let j=0;j<ps.length;j++){
   const p=ps[j],q=ps[(j+1)%ps.length],fp=ev(p),fq=ev(q),ip=fp.cmp(0)>=0,iq=fq.cmp(0)>=0;
   if(ip)out.push(p);if(ip!==iq){const z=fp.dby(fp.s(fq));out.push(p.map((v,i)=>v.a(q[i].s(v).m(z))));}
  }return out;
 };
 let clipped=0,active=0,centerMax=ZERO,best=null;const thresholdVertices=[];
 for(let i=0;i<f.triangles.length;i++){
  const tr=f.triangles[i];if(!tr.positive)continue;
  for(const p of tr.ps)if(p[0].eq(p[1])&&p[0].cmp(h)>=0&&p[0].cmp(a)<=0)centerMax=maxQ(centerMax,f.radial(...p));
  let ps=clip(tr.ps,[a,Q(-1),ZERO]);ps=clip(ps,[h.neg(),ZERO,Q(1)]);if(!ps.length)continue;clipped++;
  const value=p=>tr.cf[0].m(p[0]).a(tr.cf[1].m(p[1])).a(tr.cf[2]);
  if(maxQ(...ps.map(value)).cmp(H)<=0)continue;active++;
  ps=clip(ps,[tr.cf[2].s(H),tr.cf[0],tr.cf[1]]);
  for(const p of ps){
   const gap=p[0].s(p[1]),rank=value(p);thresholdVertices.push({gap,rank});
   if(best===null||gap.cmp(best.gap)<0)best={gap,point:p,rank,triangle:i,cf:tr.cf};
  }
 }
 if(centerMax.cmp(H)>0||best.gap.cmp(0)<=0)throw Error("middle delay gate");
 const minRanks=thresholdVertices.filter(x=>x.gap.eq(best.gap)).map(x=>x.rank),strict=minRanks.every(x=>x.eq(H));
 const quotient=a.s(h).dby(best.gap),K=quotient.n/quotient.d;
 if(Q(K).m(best.gap).cmp(a.s(h))>0||Q(K+1n).m(best.gap).cmp(a.s(h))<=0)throw Error("integer duration count");
 return {scope:"Whole-middle-cone productive-duration certificate, using the universal past-center frontier H.",domain:[h.str(),a.str()],H:H.str(),maximum_center_rank:centerMax.str(),clipped_triangles:clipped,active_triangles:active,threshold_vertices:thresholdVertices.length,
  minimum_duration:best.gap.str(),minimum_numeric:best.gap.num(),strict_above_threshold:strict,maximum_productive_returns:Number(K),
  witness:{point:best.point.map(x=>x.str()),rank:best.rank.str(),triangle:best.triangle,coefficients:best.cf.map(x=>x.str())}};
}
function verify(fieldData){return {scope:"Exact early-cone and middle-duration gates for a finite center-renewal attachment. The outside low-record continuation and initial prefixes remain explicit dependencies.",cone:verifyCone(fieldData),middle:verifyMiddle(fieldData)};}
const api={verify,verifyCone,verifyMiddle};if(typeof module==="object"&&module.exports)module.exports=api;
if(typeof require==="function"&&require.main===module){const fs=require("fs");console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2));}
return api;
