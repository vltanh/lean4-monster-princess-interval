/* Standalone exact center-factorization fixtures; pure V8/CommonJS. */
const EXACT_SOURCE="\nfunction gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a;}\nclass Rat{\n constructor(n,d=1n){if(n instanceof Rat){this.n=n.n;this.d=n.d;return;}if(typeof n===\"string\"){let p=n.split(\"/\");if(p.length===2){n=BigInt(p[0]);d=BigInt(p[1]);}else {let [s,e]=n.toLowerCase().split(\"e\");let neg=s[0]===\"-\";if(neg||s[0]===\"+\")s=s.slice(1);let parts=s.split(\".\");let f=parts[1]||\"\";n=BigInt(parts[0]+f)*(neg?-1n:1n);let power=f.length-Number(e||0);if(power>=0)d=10n**BigInt(power);else n*=10n**BigInt(-power);}}else n=BigInt(n);d=BigInt(d);if(d===0n)throw Error(\"zero denominator\");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}\n a(q){q=Q(q);return new Rat(this.n*q.d+q.n*this.d,this.d*q.d);}\n s(q){q=Q(q);return new Rat(this.n*q.d-q.n*this.d,this.d*q.d);}\n m(q){q=Q(q);return new Rat(this.n*q.n,this.d*q.d);}\n dby(q){q=Q(q);return new Rat(this.n*q.d,this.d*q.n);}\n neg(){return new Rat(-this.n,this.d);}\n cmp(q){q=Q(q);let z=this.n*q.d-q.n*this.d;return z<0n?-1:z>0n?1:0;}\n eq(q){return this.cmp(q)===0;}\n num(){return Number(this.n)/Number(this.d);}\n str(){return String(this.n)+(this.d===1n?\"\":\"/\"+this.d);}\n}\nfunction Q(x){return x instanceof Rat?x:new Rat(typeof x===\"number\"?String(x):x);}\nconst ZERO=Q(0),ONE=Q(1);\nfunction minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}\nfunction maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}\nfunction uniq(xs){let m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}\nfunction bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){let m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}\nfunction coord(x){let z=Q(x);if(z.cmp(0)<0)return coord(z.neg()).neg();const lim=4194304n;if(z.d<=lim)return z;let n=z.n,d=z.d,p0=0n,q0=1n,p1=1n,q1=0n;while(true){let a=n/d,q2=q0+a*q1;if(q2>lim)break;[p0,p1]=[p1,p0+a*p1];[q0,q1]=[q1,q2];[n,d]=[d,n-a*d];}\n let k=(lim-q0)/q1,b1=new Rat(p0+k*p1,q0+k*q1),b2=new Rat(p1,q1);return Math.abs(b1.num()-z.num())<Math.abs(b2.num()-z.num())?b1:b2;}\nfunction subP(a,b){return[a[0].s(b[0]),a[1].s(b[1])];}\nfunction cross(a,b){return a[0].m(b[1]).s(a[1].m(b[0]));}\nclass ExactField{\n constructor(data){\n this.nodes=data.nodes.map(p=>p.map(coord));this.values=(data.rational_values||data.values).map(Q);\n this.grid=[0,1].map(k=>uniq(this.nodes.map(p=>p[k])));this.cells=new Map();this.strips=[new Map(),new Map()];this.triangles=[];\n this.initial=this.nodes.map((p,i)=>[p,this.values[i]]).filter(([p,v])=>p[0].eq(p[1].neg())).map(([p,v])=>[p[0],v]).sort((a,b)=>a[0].cmp(b[0]));this.initialKnots=this.initial.map(p=>p[0]);\n for(const inds of data.triangles){\n let ps=inds.map(i=>this.nodes[i]),[p,q,r]=ps,[e,f]=[subP(q,p),subP(r,p)],det=cross(e,f),[x,y,z]=inds.map(i=>this.values[i]);\n let ru=y.s(x).m(f[1]).s(z.s(x).m(e[1])).dby(det),rv=e[0].m(z.s(x)).s(f[0].m(y.s(x))).dby(det);\n if(ru.cmp(0)<0||rv.cmp(0)>0)throw Error(\"transport\");\n let n=this.triangles.length;this.triangles.push({ps,cf:[ru,rv,x.s(ru.m(p[0])).s(rv.m(p[1]))],positive:det.cmp(0)>0});\n let ranges=[0,1].map(k=>[bisect(this.grid[k],minQ(...ps.map(p=>p[k])),false),bisect(this.grid[k],maxQ(...ps.map(p=>p[k])),false)]);\n for(let k=0;k<2;k++)for(let i=ranges[k][0];i<ranges[k][1];i++){if(!this.strips[k].has(i))this.strips[k].set(i,[]);this.strips[k].get(i).push(n);}\n for(let i=ranges[0][0];i<ranges[0][1];i++)for(let j=ranges[1][0];j<ranges[1][1];j++){let key=i+\",\"+j;if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(n);}\n }\n this.rcache=new Map();this.icache=new Map();\n }\n initialValue(z){z=Q(z);let i=Math.max(0,Math.min(this.initial.length-2,bisect(this.initialKnots,z)-1));let[a,x]=this.initial[i],[b,y]=this.initial[i+1];return x.a(z.s(a).m(y.s(x)).dby(b.s(a)));}\n radial(u,v){u=Q(u);v=Q(v);if(v.cmp(1)>0)return ZERO;let key=u.str()+\",\"+v.str();if(this.rcache.has(key))return this.rcache.get(key);let cell=[u,v].map((p,k)=>Math.max(0,Math.min(this.grid[k].length-2,bisect(this.grid[k],p)-1))),poss=new Set();\n for(let i of[cell[0],cell[0]-1])for(let j of[cell[1],cell[1]-1])for(let n of(this.cells.get(i+\",\"+j)||[]))poss.add(n);\n for(let n of[...poss].sort((a,b)=>a-b)){let {ps,cf,positive}=this.triangles[n];let turns=ps.map((p,i)=>cross(subP(ps[(i+1)%3],p),subP([u,v],p)));if(turns.every(t=>positive?t.cmp(0)>=0:t.cmp(0)<=0)){let z=cf[0].m(u).a(cf[1].m(v)).a(cf[2]);this.rcache.set(key,z);return z;}}\n throw Error(\"no triangle \"+key);\n }\n integral(fixed,left,right,axis,threshold=null){fixed=Q(fixed);left=Q(left);right=Q(right);if(threshold!==null)threshold=Q(threshold);if(right.cmp(left)<=0)return ZERO;\n let key=[fixed.str(),left.str(),right.str(),axis,threshold===null?\"\":threshold.str()].join(\",\");if(this.icache.has(key))return this.icache.get(key);\n if((axis===1&&fixed.cmp(1)>=0)||(axis===0&&left.cmp(1)>=0))return threshold===null?ZERO:maxQ(0,threshold).m(right.s(left));\n if(axis===0&&right.cmp(1)>0)return this.integral(fixed,left,ONE,axis,threshold).a(threshold===null?ZERO:maxQ(0,threshold).m(right.s(1)));\n let i=Math.max(0,Math.min(this.grid[axis].length-2,bisect(this.grid[axis],fixed)-1)),poss=new Set([...(this.strips[axis].get(i)||[]),...(this.strips[axis].get(i-1)||[])]),cuts=[left,right],other=1-axis;\n for(let n of poss){let {ps}=this.triangles[n];for(let k=0;k<3;k++){let a=ps[k],b=ps[(k+1)%3];if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(let x of[a,b])if(x[other].cmp(left)>0&&x[other].cmp(right)<0)cuts.push(x[other]);}else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&fixed.cmp(maxQ(a[axis],b[axis]))<=0){let v=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));if(v.cmp(left)>0&&v.cmp(right)<0)cuts.push(v);}}}\n cuts=uniq(cuts);let total=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],fa=axis===0?this.radial(fixed,a):this.radial(a,fixed),fb=axis===0?this.radial(fixed,b):this.radial(b,fixed);\n if(threshold!==null){fa=threshold.s(fa);fb=threshold.s(fb);if(fa.cmp(0)<=0&&fb.cmp(0)<=0)continue;if(fa.m(fb).cmp(0)<0){let w=b.s(a).m(fa.cmp(0)>0?fa.dby(fa.s(fb)):fb.dby(fb.s(fa)));total=total.a(w.m(maxQ(fa,fb)).dby(2));continue;}}\n total=total.a(b.s(a).m(fa.a(fb)).dby(2));}\n this.icache.set(key,total);return total;\n }\n negativeM1(a){a=Q(a);return this.integral(a,a.neg(),a,0).a(a.m(4)).a(8).s(a.a(3).m(2).m(this.initialValue(a))).s(this.integral(a,a,a.a(2),1)).dby(4);}\n positiveM1(a){a=Q(a);let A=this.initialValue(a);return Q(8).s(a.m(4)).a(Q(3).s(a).m(A)).s(this.integral(a.neg(),a,Q(2).s(a),1)).s(this.integral(Q(2).s(a),a.neg(),ONE,0,A)).dby(4);}\n fixedOne(a,positive){a=Q(a);let A=this.initialValue(a),v=positive?a.neg():a,I=this.integral(v,a,ONE,1),B=this.radial(ONE,v);\n return positive?Q(12).a(A.m(2)).s(Q(7).a(a).m(B)).s(I).s(this.integral(ONE,a.neg(),ONE,0,A)).dby(4):this.integral(a,a.neg(),a,0).a(12).s(A.m(4)).s(Q(7).s(a).m(B)).s(I).dby(4);\n }\n cdfSides(t,x){t=Q(t);x=Q(x);let r=this.radial(t.a(x.cmp(0)<0?x.neg():x),t.s(x.cmp(0)<0?x.neg():x));if(x.eq(0))return[ONE.s(r).dby(2),ONE.a(r).dby(2)];if(x.eq(1))return[ONE.a(r).dby(2),ONE];if(x.eq(-1))return[ZERO,ONE.s(r).dby(2)];let v=x.cmp(0)>0?ONE.a(r).dby(2):ONE.s(r).dby(2);return[v,v];}\n unitRoutePayoff(route){route=route.map(p=>p.map(Q));let[lower,upper]=this.cdfSides(...route[0]),cost=ZERO;\n for(let k=0;k<route.length-1;k++){let[start,x]=route[k],[end,y]=route[k+1];if(end.eq(start)){if(!x.eq(y))throw Error(\"bad duplicate\");continue;}let vel=y.s(x).dby(end.s(start));if(!vel.eq(1)&&!vel.eq(-1))throw Error(\"not unit\");let cuts=[start,end];if(x.m(y).cmp(0)<0)cuts.splice(1,0,start.s(vel.m(x)));let area=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],xa=x.a(vel.m(a.s(start))),xb=x.a(vel.m(b.s(start))),sign=xa.a(xb).cmp(0)>0?1:-1,ua=a.a(xa.m(sign)),va=a.s(xa.m(sign)),ub=b.a(xb.m(sign)),vb=b.s(xb.m(sign)),record=vel.eq(1)?upper:lower;\n if(vel.m(sign).eq(1)){let threshold=sign===1?record.m(2).s(1):ONE.s(record.m(2));area=area.a(this.integral(va,ua,ub,1).s(threshold.m(ub.s(ua))).a(this.integral(va,ua,ub,1,threshold)).dby(4));}\n else{let threshold=sign===-1?ONE.s(record.m(2)):record.m(2).s(1);area=area.a(this.integral(ua,va,vb,0,threshold).dby(4));}}\n let[strict,closed]=this.cdfSides(end,y);if(vel.eq(1)){let updated=maxQ(upper,closed);cost=cost.a(end.m(updated.s(upper))).s(area);upper=updated;}else{let updated=minQ(lower,strict);cost=cost.a(end.m(lower.s(updated))).s(area);lower=updated;}}\n if(!lower.eq(0)||!upper.eq(1))throw Error(\"incomplete\");return cost;\n }\n}\nreturn {Rat,Q,ZERO,ONE,minQ,maxQ,uniq,bisect,ExactField};\n";

function verify(options={}){
 const X=Function(EXACT_SOURCE)(),{Q,ZERO,ONE,minQ,maxQ}=X;
 let checks={order:0,legality:0,repaired_upper_tail:0,earliest_unmatched:0,full_cost_comparison:0,lagging_sign_pair_comparison:0,balanced_renewal_kernel:0};
 let cases={productive_triangle:0,capped_triangle:0,productive_wait:0,no_upper_tail:0,empty_band:0};
 const examples=[];
 const assert=(b,m)=>{if(!b)throw Error(m);};
 const sum=xs=>xs.reduce((a,b)=>a.a(b),ZERO);
 function pos(path,t){for(let j=0;j<path.length-1;j++){const [a,x]=path[j],[b,y]=path[j+1];if(a.cmp(t)<=0&&t.cmp(b)<=0)return x.a(t.s(a).m(y.s(x)).dby(b.s(a)));}throw Error("position outside path");}
 function first(path,monster,sign){
  let best=null;
  for(let j=0;j<path.length-1;j++){
   const [a,x]=path[j],[b,y]=path[j+1],pv=y.s(x).m(sign).dby(b.s(a)),pi=x.m(sign).s(pv.m(a));
   for(let k=0;k<monster.length-1;k++){
    const [c,z]=monster[k],[d,w]=monster[k+1];if(d.eq(c)){assert(z.eq(w),"duplicate time");continue;}
    const left=maxQ(a,c),right=minQ(b,d);if(right.cmp(left)<0)continue;
    const mv=w.s(z).dby(d.s(c)),mi=z.s(mv.m(c)),slope=pv.s(mv),intercept=pi.s(mi);
    if(slope.eq(0)){if(intercept.eq(0)&&(best===null||left.cmp(best)<0))best=left;}
    else{const root=intercept.neg().dby(slope);if(left.cmp(root)<=0&&root.cmp(right)<=0&&(best===null||root.cmp(best)<0))best=root;}
   }
  }
  if(monster.length===1){const [t,x]=monster[0];if(pos(path,t).m(sign).eq(x))best=t;}
  return best;
 }
 function tidy(route){const out=[];for(const p0 of route){const p=p0.map(Q);if(out.length&&p[0].eq(out[out.length-1][0]))assert(p[1].eq(out[out.length-1][1]),"tidy duplicate");else out.push(p);}return out;}
 function legal(route){return route.every(p=>p[1].cmp(-1)>=0&&p[1].cmp(1)<=0)&&route.slice(1).every((p,j)=>p[0].cmp(route[j][0])>0&&p[1].s(route[j][1]).m(p[1].s(route[j][1]).cmp(0)<0?-1:1).cmp(p[0].s(route[j][0]))<=0);}
 function tent(t,e,sign=1){
  return e.s(t).cmp(2)<=0?tidy([[t,ZERO],[t.a(e).dby(2),e.s(t).m(sign).dby(2)],[e,ZERO]]):tidy([[t,ZERO],[t.a(1),Q(sign)],[e.s(1),Q(sign)],[e,ZERO]]);
 }
 const sweep=(t,sign=1)=>[[t,ZERO],[t.a(1),Q(sign)],[t.a(3),Q(-sign)]];
 function fixtures(){
  const low=[
   [[0,"1/10"],["1/2",0],[1,"1/10"],["19/10",1],[16,1]],
   [[0,"1/5"],["1/2",0],[1,"1/5"],["9/5",1],[16,1]],
   [[0,"3/10"],["1/2",0],[1,"3/10"],["17/10",1],[16,1]]
  ];
  const weights=["1/10","1/5","1/5","1/4","1/4"];
  const out=[
   {paths:[...low,[[0,"3/5"],["2/5",1],[16,1]],[[0,1],[16,1]]],weights},
   {paths:[...low,[[0,1],["3/2",1],["8/5","9/10"],["17/10",1],[16,1]],[[0,1],[16,1]]],weights}
  ];
  const ts=[0,"1/4","1/2","3/4",1,"5/4","3/2",2,16],rows=[
   [0,2,4,7,11,16],[0,1,2,4,8,14],[0,2,4,6,9,15],[0,1,2,4,7,12],
   [0,1,3,5,8,13],[5,6,8,10,13,18],[10,11,13,15,18,20],[20,20,20,20,20,20],[20,20,20,20,20,20]
  ];
  out.push({paths:Array.from({length:6},(_,j)=>ts.map((t,k)=>[Q(t),Q(rows[k][j]).dby(20)])),weights:[1,2,3,4,5,6].map(j=>Q(j).dby(21))});
  return out.map(o=>({paths:o.paths.map(p=>p.map(q=>q.map(Q))),weights:o.weights.map(Q)}));
 }
 function routes(start){
  const templates=[
   [],[["wait","1/4",0],["triangle","1/2",1],["wait","1/4",0],["triangle","3/4",-1]],
   [["triangle","1/4",1],["triangle","1/3",-1],["triangle","1/2",1]],
   [["wait","5/4",0],["triangle","1/4",-1]],[["wait","9/4",0]],
   [["triangle","1/5",-1],["wait","4/5",0],["triangle","7/8",1]],
   [["wait","1/8",0],["wait","3/8",0],["triangle","1/2",-1]]
  ],out=[];
  for(const template of templates)for(const endsign of[-1,1]){
   const route=[[start,ZERO]],actions=[];let t=start;
   for(const [kind,length,sign]of[...template,["triangle",2,endsign]]){
    const e=t.a(length),action=kind==="wait"?[[t,ZERO],[e,ZERO]]:tent(t,e,sign);
    route.push(...action.slice(1));actions.push({kind,start:t,end:e,sign,route:action,endIndex:route.length-1});t=e;
   }
   route.push([t.a(1),Q(-endsign)]);out.push({route:tidy(route),actions});
  }
  return out;
 }
 const laws=fixtures();
 for(let lawId=0;lawId<laws.length;lawId++){
  const {paths,weights}=laws[lawId],cache=new Map();
  function hits(route){
   const key=route.map(p=>p.map(q=>q.str()).join(",")).join(";");
   if(!cache.has(key))cache.set(key,{plus:paths.map(p=>first(p,route,1)),minus:paths.map(p=>first(p,route,-1))});
   return cache.get(key);
  }
  function cost(route,plus,minus){
   const ht=hits(route);let total=ZERO;
   for(const [side,low]of[["plus",plus],["minus",minus]])for(let j=low;j<paths.length;j++){assert(ht[side][j]!==null,"incomplete");total=total.a(weights[j].m(ht[side][j]).dby(2));}
   return total;
  }
  function repair(route,actions,n){
   const t=route[0][0];if(n===0)return{route,info:{kind:"empty_band"}};
   if(n===paths.length)return{route:sweep(t),info:{kind:"no_upper_tail"}};
   for(const act of actions){
    const ah=hits(act.route),upper=[...ah.plus.slice(n),...ah.minus.slice(n)].filter(x=>x!==null);if(!upper.length)continue;
    if(act.kind==="triangle"){
     const e=act.end,newRoute=tent(t,e).concat(route.slice(act.endIndex+1).map(([s,x])=>[s,x.m(act.sign)]));
     return{route:tidy(newRoute),info:{kind:"productive_triangle",capped:e.s(t).cmp(2)>0}};
    }
    const tau=minQ(...upper),beta=hits(sweep(t)).plus[n-1],chi=beta.m(2).s(t);
    assert(t.cmp(chi)<=0&&chi.cmp(minQ(t.a(2),tau))<=0,"balancing return");
    return{route:tidy(tent(t,chi).concat([[tau,ZERO]],route.filter(p=>p[0].cmp(tau)>0))),info:{kind:"productive_wait",chi:chi.str(),tau:tau.str()}};
   }
   throw Error("no productive action");
  }
  assert(sum(weights).eq(1),"weights");
  for(const time of X.uniq(paths.flatMap(p=>p.map(q=>q[0])))){const rs=paths.map(p=>pos(p,time));assert(rs.slice(1).every((v,j)=>v.cmp(rs[j])>=0),"path order");checks.order++;}
  for(const p of paths){assert(legal(p)&&pos(p,Q(2)).eq(1),"path legality");checks.legality++;}
  for(const t of[0,"1/8","3/8","3/4",1].map(Q)){
   const z=paths.filter(p=>pos(p,t).eq(0)).length;
   for(const {route,actions}of routes(t)){
    assert(legal(route),"monster legality");
    for(let n=z;n<=paths.length;n++){
     const made=repair(route,actions,n),nr=made.route,info=made.info;
     assert(legal(nr)&&nr[0][0].eq(t)&&nr[0][1].eq(0),"repair legality");checks.legality++;cases[info.kind]++;if(info.capped)cases.capped_triangle++;
     const before=cost(route,n,n),after=cost(nr,n,n);assert(after.cmp(before)<=0,"upper-tail comparison");checks.repaired_upper_tail++;
     const earliest=hits(sweep(t)).plus,newHits=hits(nr).plus;
     for(let r=z;r<=n;r++){
      for(let j=r;j<n;j++){assert(newHits[j]!==null&&newHits[j].eq(earliest[j]),"earliest unmatched");checks.earliest_unmatched++;}
      const extra=sum(weights.slice(r,n).map((w,j)=>w.m(earliest[j+r]).dby(2))),actual=cost(nr,r,n);
      assert(actual.eq(after.a(extra))&&actual.cmp(before.a(extra))<=0,"full decomposition");checks.full_cost_comparison++;
     }
     if(info.kind==="productive_wait"&&examples.length<3)examples.push({law:lawId,t:t.str(),n,...info});
    }
   }
   for(const e of["1/4","3/4","5/4",2].map(d=>t.a(d))){
    const positiveTent=tent(t,e),th=hits(positiveTent),rho=th.plus.filter(x=>x!==null).length,ze=paths.filter(p=>pos(p,e).eq(0)).length;
    const bt=hits(sweep(t)).plus,be=hits(sweep(e)).plus;
    for(let n=z;n<=paths.length;n++){
     const N=Math.max(n,rho),r1=Math.max(n,ze);let immediate=ZERO;
     for(const side of["plus","minus"])for(let j=n;j<paths.length;j++)if(th[side][j]!==null)immediate=immediate.a(weights[j].m(th[side][j]).dby(2));
     const imbalance=sum(weights.slice(r1,N).map((w,j)=>w.m(be[j+r1]).dby(2))),kernel=sum(weights.slice(n,N).map((w,j)=>w.m(bt[j+n].a(be[j+n])).dby(2)));
     assert(immediate.a(imbalance).eq(kernel),"renewal kernel");checks.balanced_renewal_kernel++;
     for(let r=z;r<=n;r++)for(const {route:future}of routes(e).slice(0,4)){
      const leading=tidy(tent(t,e,-1).concat(future.slice(1))),flip=rho>n?-1:1,lagging=tidy(positiveTent.concat(future.slice(1).map(([s,x])=>[s,x.m(flip)])));
      assert(cost(lagging,r,n).cmp(cost(leading,r,n))<=0,"lagging sign");checks.lagging_sign_pair_comparison++;
     }
    }
   }
  }
  if(options.progress)options.progress({law:lawId+1,checks:{...checks},cases:{...cases}});
 }
 return{scope:"Exact physical finite-route repair, renewal kernel, and sign comparisons; not an optimized game value",checks,total_recorded_checks:Object.values(checks).reduce((a,b)=>a+b,0),repair_case_counts:cases,productive_wait_examples:examples};
}
const api={verify};
if(typeof module==="object"&&module.exports)module.exports=api;
if(typeof require==="function"&&require.main===module)console.log(JSON.stringify(verify(),null,2));
return api;
