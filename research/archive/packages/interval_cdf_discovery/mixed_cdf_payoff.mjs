/** Exact record scoring for a specified ordered mixture; no response search theorem for the continuous component. */
function createMixedScorer(){

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
 num(){const a=Number(this.n),b=Number(this.d);if(Number.isFinite(a)&&Number.isFinite(b))return a/b;const n=(this.n<0n?-this.n:this.n).toString(),d=this.d.toString();return (this.n<0n?-1:1)*Number(n.slice(0,16))/Number(d.slice(0,16))*10**(n.length-d.length-Math.min(n.length,16)+Math.min(d.length,16));}
 str(){return String(this.n)+(this.d===1n?"":"/"+this.d);}
}
function Q(x){return x instanceof Rat?x:new Rat(typeof x==="number"?String(x):x);}
const ZERO=Q(0),ONE=Q(1);
function minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}
function maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}
function uniq(xs){let m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}
function bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){let m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}
function coord(x){let z=Q(x);if(z.cmp(0)<0)return coord(z.neg()).neg();const lim=4194304n;if(z.d<=lim)return z;let n=z.n,d=z.d,p0=0n,q0=1n,p1=1n,q1=0n;while(true){let a=n/d,q2=q0+a*q1;if(q2>lim)break;[p0,p1]=[p1,p0+a*p1];[q0,q1]=[q1,q2];[n,d]=[d,n-a*d];}
 let k=(lim-q0)/q1,b1=new Rat(p0+k*p1,q0+k*q1),b2=new Rat(p1,q1);return Math.abs(b1.num()-z.num())<Math.abs(b2.num()-z.num())?b1:b2;}
function subP(a,b){return[a[0].s(b[0]),a[1].s(b[1])];}
function cross(a,b){return a[0].m(b[1]).s(a[1].m(b[0]));}
class ExactField{
 constructor(data){
 this.nodes=data.nodes.map(p=>p.map(coord));this.values=(data.rational_values||data.values).map(Q);
 this.grid=[0,1].map(k=>uniq(this.nodes.map(p=>p[k])));this.cells=new Map();this.strips=[new Map(),new Map()];this.triangles=[];
 this.initial=this.nodes.map((p,i)=>[p,this.values[i]]).filter(([p,v])=>p[0].eq(p[1].neg())).map(([p,v])=>[p[0],v]).sort((a,b)=>a[0].cmp(b[0]));this.initialKnots=this.initial.map(p=>p[0]);
 for(const inds of data.triangles){
 let ps=inds.map(i=>this.nodes[i]),[p,q,r]=ps,[e,f]=[subP(q,p),subP(r,p)],det=cross(e,f),[x,y,z]=inds.map(i=>this.values[i]);
 let ru=y.s(x).m(f[1]).s(z.s(x).m(e[1])).dby(det),rv=e[0].m(z.s(x)).s(f[0].m(y.s(x))).dby(det);
 if(ru.cmp(0)<0||rv.cmp(0)>0)throw Error("transport");
 let n=this.triangles.length;this.triangles.push({ps,cf:[ru,rv,x.s(ru.m(p[0])).s(rv.m(p[1]))],positive:det.cmp(0)>0});
 let ranges=[0,1].map(k=>[bisect(this.grid[k],minQ(...ps.map(p=>p[k])),false),bisect(this.grid[k],maxQ(...ps.map(p=>p[k])),false)]);
 for(let k=0;k<2;k++)for(let i=ranges[k][0];i<ranges[k][1];i++){if(!this.strips[k].has(i))this.strips[k].set(i,[]);this.strips[k].get(i).push(n);}
 for(let i=ranges[0][0];i<ranges[0][1];i++)for(let j=ranges[1][0];j<ranges[1][1];j++){let key=i+","+j;if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(n);}
 }
 this.rcache=new Map();this.icache=new Map();
 }
 initialValue(z){z=Q(z);let i=Math.max(0,Math.min(this.initial.length-2,bisect(this.initialKnots,z)-1));let[a,x]=this.initial[i],[b,y]=this.initial[i+1];return x.a(z.s(a).m(y.s(x)).dby(b.s(a)));}
 radial(u,v){u=Q(u);v=Q(v);if(v.cmp(1)>0)return ZERO;let key=u.str()+","+v.str();if(this.rcache.has(key))return this.rcache.get(key);let cell=[u,v].map((p,k)=>Math.max(0,Math.min(this.grid[k].length-2,bisect(this.grid[k],p)-1))),poss=new Set();
 for(let i of[cell[0],cell[0]-1])for(let j of[cell[1],cell[1]-1])for(let n of(this.cells.get(i+","+j)||[]))poss.add(n);
 for(let n of[...poss].sort((a,b)=>a-b)){let {ps,cf,positive}=this.triangles[n];let turns=ps.map((p,i)=>cross(subP(ps[(i+1)%3],p),subP([u,v],p)));if(turns.every(t=>positive?t.cmp(0)>=0:t.cmp(0)<=0)){let z=cf[0].m(u).a(cf[1].m(v)).a(cf[2]);this.rcache.set(key,z);return z;}}
 throw Error("no triangle "+key);
 }
 integral(fixed,left,right,axis,threshold=null){fixed=Q(fixed);left=Q(left);right=Q(right);if(threshold!==null)threshold=Q(threshold);if(right.cmp(left)<=0)return ZERO;
 let key=[fixed.str(),left.str(),right.str(),axis,threshold===null?"":threshold.str()].join(",");if(this.icache.has(key))return this.icache.get(key);
 if((axis===1&&fixed.cmp(1)>=0)||(axis===0&&left.cmp(1)>=0))return threshold===null?ZERO:maxQ(0,threshold).m(right.s(left));
 if(axis===0&&right.cmp(1)>0)return this.integral(fixed,left,ONE,axis,threshold).a(threshold===null?ZERO:maxQ(0,threshold).m(right.s(1)));
 let i=Math.max(0,Math.min(this.grid[axis].length-2,bisect(this.grid[axis],fixed)-1)),poss=new Set([...(this.strips[axis].get(i)||[]),...(this.strips[axis].get(i-1)||[])]),cuts=[left,right],other=1-axis;
 for(let n of poss){let {ps}=this.triangles[n];for(let k=0;k<3;k++){let a=ps[k],b=ps[(k+1)%3];if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(let x of[a,b])if(x[other].cmp(left)>0&&x[other].cmp(right)<0)cuts.push(x[other]);}else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&fixed.cmp(maxQ(a[axis],b[axis]))<=0){let v=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));if(v.cmp(left)>0&&v.cmp(right)<0)cuts.push(v);}}}
 cuts=uniq(cuts);let total=ZERO;
 for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],fa=axis===0?this.radial(fixed,a):this.radial(a,fixed),fb=axis===0?this.radial(fixed,b):this.radial(b,fixed);
 if(threshold!==null){fa=threshold.s(fa);fb=threshold.s(fb);if(fa.cmp(0)<=0&&fb.cmp(0)<=0)continue;if(fa.m(fb).cmp(0)<0){let w=b.s(a).m(fa.cmp(0)>0?fa.dby(fa.s(fb)):fb.dby(fb.s(fa)));total=total.a(w.m(maxQ(fa,fb)).dby(2));continue;}}
 total=total.a(b.s(a).m(fa.a(fb)).dby(2));}
 this.icache.set(key,total);return total;
 }
 negativeM1(a){a=Q(a);return this.integral(a,a.neg(),a,0).a(a.m(4)).a(8).s(a.a(3).m(2).m(this.initialValue(a))).s(this.integral(a,a,a.a(2),1)).dby(4);}
 positiveM1(a){a=Q(a);let A=this.initialValue(a);return Q(8).s(a.m(4)).a(Q(3).s(a).m(A)).s(this.integral(a.neg(),a,Q(2).s(a),1)).s(this.integral(Q(2).s(a),a.neg(),ONE,0,A)).dby(4);}
 fixedOne(a,positive){a=Q(a);let A=this.initialValue(a),v=positive?a.neg():a,I=this.integral(v,a,ONE,1),B=this.radial(ONE,v);
 return positive?Q(12).a(A.m(2)).s(Q(7).a(a).m(B)).s(I).s(this.integral(ONE,a.neg(),ONE,0,A)).dby(4):this.integral(a,a.neg(),a,0).a(12).s(A.m(4)).s(Q(7).s(a).m(B)).s(I).dby(4);
 }
 cdfSides(t,x){t=Q(t);x=Q(x);let r=this.radial(t.a(x.cmp(0)<0?x.neg():x),t.s(x.cmp(0)<0?x.neg():x));if(x.eq(0))return[ONE.s(r).dby(2),ONE.a(r).dby(2)];if(x.eq(1))return[ONE.a(r).dby(2),ONE];if(x.eq(-1))return[ZERO,ONE.s(r).dby(2)];let v=x.cmp(0)>0?ONE.a(r).dby(2):ONE.s(r).dby(2);return[v,v];}
 unitRoutePayoff(route){route=route.map(p=>p.map(Q));let[lower,upper]=this.cdfSides(...route[0]),cost=ZERO;
 for(let k=0;k<route.length-1;k++){let[start,x]=route[k],[end,y]=route[k+1];if(end.eq(start)){if(!x.eq(y))throw Error("bad duplicate");continue;}let vel=y.s(x).dby(end.s(start));if(!vel.eq(1)&&!vel.eq(-1))throw Error("not unit");let cuts=[start,end];if(x.m(y).cmp(0)<0)cuts.splice(1,0,start.s(vel.m(x)));let area=ZERO;
 for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],xa=x.a(vel.m(a.s(start))),xb=x.a(vel.m(b.s(start))),sign=xa.a(xb).cmp(0)>0?1:-1,ua=a.a(xa.m(sign)),va=a.s(xa.m(sign)),ub=b.a(xb.m(sign)),vb=b.s(xb.m(sign)),record=vel.eq(1)?upper:lower;
 if(vel.m(sign).eq(1)){let threshold=sign===1?record.m(2).s(1):ONE.s(record.m(2));area=area.a(this.integral(va,ua,ub,1).s(threshold.m(ub.s(ua))).a(this.integral(va,ua,ub,1,threshold)).dby(4));}
 else{let threshold=sign===-1?ONE.s(record.m(2)):record.m(2).s(1);area=area.a(this.integral(ua,va,vb,0,threshold).dby(4));}}
 let[strict,closed]=this.cdfSides(end,y);if(vel.eq(1)){let updated=maxQ(upper,closed);cost=cost.a(end.m(updated.s(upper))).s(area);upper=updated;}else{let updated=minQ(lower,strict);cost=cost.a(end.m(lower.s(updated))).s(area);lower=updated;}}
 if(!lower.eq(0)||!upper.eq(1))throw Error("incomplete");return cost;
 }
}
class PLPath {
  constructor(raw) {
    this.vertices=[];
    for(const [t0,x0] of raw){
      const t=Q(t0),x=Q(x0),p=this.vertices.at(-1);
      if(t.cmp(0)<0||x.cmp(-1)<0||x.cmp(1)>0)throw Error("inadmissible vertex");
      if(p&&t.eq(p[0])){if(!x.eq(p[1]))throw Error("inconsistent duplicate time");continue;}
      if(p&&t.cmp(p[0])<0)throw Error("time order");
      this.vertices.push([t,x]);
      while(this.vertices.length>=3){
        const n=this.vertices.length,[a,x1]=this.vertices[n-3],[b,x2]=this.vertices[n-2],[c,x3]=this.vertices[n-1];
        if(x2.s(x1).m(c.s(b)).eq(x3.s(x2).m(b.s(a))))this.vertices.splice(n-2,1);else break;
      }
    }
    if(!this.vertices.length||!this.vertices[0][0].eq(0))throw Error("initial time");
    this.t=this.vertices.map(p=>p[0]);this.x=this.vertices.map(p=>p[1]);this.v=[];
    for(let k=0;k+1<this.t.length;k++){
      const v=this.x[k+1].s(this.x[k]).dby(this.t[k+1].s(this.t[k]));
      if(v.cmp(-1)<0||v.cmp(1)>0)throw Error("speed bound");this.v.push(v);
    }
    this.seq=[this.vertices.map(([t,x])=>t.a(x)),this.vertices.map(([t,x])=>t.s(x))];
    this.inverseCache=[new Map(),new Map()];
  }
  at(t){t=Q(t);const k=bisect(this.t,t,true)-1;if(k<0)throw Error("negative time");return k+1===this.t.length?this.x[k]:this.x[k].a(this.v[k].m(t.s(this.t[k])));}
  hit(t,x,d){
    t=Q(t);x=Q(x);const y=this.at(t),sgn=y.cmp(x);if(!sgn)return t;if(sgn!==d)return null;
    const h=(d+1)>>1,q=t.s(x.m(d)),key=q.str(),old=this.inverseCache[h].get(key);if(old)return old;
    const seq=this.seq[h],k=bisect(seq,q,false);let ans;
    if(k===seq.length)ans=this.t.at(-1).a(q.s(seq.at(-1)));
    else if(k===0)throw Error("non-forward inverse");
    else{const den=ONE.s(this.v[k-1].m(d));if(den.cmp(0)<=0)throw Error("flat inverse");ans=this.t[k-1].a(q.s(seq[k-1]).dby(den));}
    if(ans.cmp(t)<0||ans.cmp(t.a(ONE.s(x.m(d))))>0)throw Error("ray hit outside reachable arena");
    this.inverseCache[h].set(key,ans);return ans;
  }
  json(){return this.vertices.map(p=>p.map(z=>z.str()));}
}
function integerWeights(weights){
  const qs=weights.map(Q);let D=1n;
  for(const q of qs){if(q.cmp(0)<=0)throw Error("positive weights required");D=D/gcd(D,q.d)*q.d;}
  let ws=qs.map(q=>q.n*(D/q.d)),g=ws.reduce((a,b)=>gcd(a,b));ws=ws.map(w=>w/g);return ws;
}
function prepare(raw,weights){
  if(raw.length!==weights.length||!raw.length)throw Error("input dimensions");
  const ws=integerWeights(weights),map=new Map();
  raw.forEach((p,i)=>{const path=new PLPath(p),key=JSON.stringify(path.json());if(map.has(key))map.get(key).w+=ws[i];else map.set(key,{p:path,w:ws[i]});});
  const entries=[...map.values()];return {paths:entries.map(e=>e.p),weights:entries.map(e=>e.w),W:entries.reduce((a,e)=>a+e.w,0n)};
}
function rawCapture(monster,princess){
  const ts=uniq([...monster.t,...princess.t]);let last=null;
  for(const t of ts){const f=monster.at(t).s(princess.at(t));if(f.eq(0))return t;if(last&&f.cmp(0)!==last[1].cmp(0))return last[0].a(t.s(last[0]).m(last[1]).dby(last[1].s(f)));last=[t,f];}
  return null;
}
function sortedCapture(paths,weights,monster){
  const H=monster.t.at(-1),events=[ZERO,H];
  for(const p of paths){
    const ts0=uniq([ZERO,H,...monster.t,...p.t].filter(t=>t.cmp(H)<=0));
    const diff=ts0.map(t=>p.at(t).s(monster.at(t)));
    for(let k=0;k<ts0.length;k++)if(diff[k].eq(0))events.push(ts0[k]);
    for(let k=0;k+1<ts0.length;k++){
      const a=ts0[k],b=ts0[k+1],fa=diff[k],fb=diff[k+1];
      if(fa.cmp(0)*fb.cmp(0)<0)events.push(a.a(b.s(a).m(fa).dby(fa.s(fb))));
    }
  }
  const ts=uniq(events),W=weights.reduce((a,b)=>a+b,0n);let lo=W,hi=0n,cost=ZERO,captures=[];
  for(const t of ts){
    const x=monster.at(t);let fl=0n,fh=0n;
    for(let j=0;j<paths.length;j++){const sg=paths[j].at(t).cmp(x);if(sg<0)fl+=weights[j];if(sg<=0)fh+=weights[j];}
    const initial=lo>hi,nl=initial?fl:(fl<lo?fl:lo),nh=initial?fh:(fh>hi?fh:hi),added=initial?fh-fl:(lo-nl)+(nh-hi);
    if(added){cost=cost.a(t.m(added));captures.push({time:t.str(),mass:String(added),lower:String(nl),upper:String(nh)});}
    lo=nl;hi=nh;
  }
  return{complete:lo===0n&&hi===W,cost,value:cost.dby(W),lower:lo,upper:hi,captures};
}
function compressRoute(route){
  const out=[];for(const p of route){out.push(p);while(out.length>=3){const n=out.length,[a,x]=out[n-3],[b,y]=out[n-2],[c,z]=out[n-1];if(y.s(x).m(c.s(b)).eq(z.s(y).m(b.s(a))))out.splice(n-2,1);else break;}}return out;
}
class CaptureSearch{
  constructor(raw,weights,options={}){
    const d=prepare(raw,weights);this.ps=d.paths;this.ws=d.weights;this.W=d.W;this.n=this.ps.length;this.options=options;this.mode=options.mode||"sorted";
    if(!["sorted","raw"].includes(this.mode))throw Error("mode");
    this.full=(1n<<BigInt(this.n))-1n;this.memo=new Map();this.stats={nodes:0,leaves:0,bounded:0,dominated:0,improvements:0};this.complete=false;this.stopReason=null;this.best=null;this.bestRoute=null;
    this.stack=[];let starts=new Map();
    this.ps.forEach((p,i)=>{const key=p.x[0].str();if(!starts.has(key))starts.set(key,{x:p.x[0],anchor:i});});
    for(const z of starts.values())this.stack.push({lo:this.W,hi:0n,mask:0n,t:ZERO,x:z.x,cost:ZERO,anchor:z.anchor,route:{p:[ZERO,z.x],prev:null}});
    const initial=options.incumbents||[];for(const r of [[[0,-1],[2,1]],[[0,1],[2,-1]],...initial])this.considerRoute(r);
    if(this.best===null)throw Error("no initial complete route");
    this.target=options.target===undefined?null:Q(options.target).m(this.W);
  }
  considerRoute(raw){
    const m=new PLPath(raw);let cost=ZERO;
    if(this.mode==="sorted"){const v=sortedCapture(this.ps,this.ws,m);if(!v.complete)return;cost=v.cost;}
    else{for(let j=0;j<this.n;j++){const t=rawCapture(m,this.ps[j]);if(t===null)return;cost=cost.a(t.m(this.ws[j]));}}
    if(this.best===null||cost.cmp(this.best)<0){this.best=cost;this.bestRoute=m.vertices;}
  }
  routeArray(link){let a=[];while(link){a.push(link.p);link=link.prev;}return compressRoute(a.reverse());}
  recordImprovement(cost,route){
    if(cost.cmp(this.best)<0){this.best=cost;this.bestRoute=this.routeArray(route);this.stats.improvements++;if(this.target&&cost.cmp(this.target)<0)this.stopReason="strict attack found";}
  }
  sortedEvents(state,side,positions){
    let c=0n;const events=[];
    for(let j=0;j<this.n;j++){
      const sg=positions[j].cmp(state.x);
      if(side<0&&sg<0){c+=this.ws[j];events.push({t:this.ps[j].hit(state.t,state.x,-1),w:this.ws[j],anchor:j});}
      if(side>0){if(sg<=0)c+=this.ws[j];else events.push({t:this.ps[j].hit(state.t,state.x,1),w:this.ws[j],anchor:j});}
    }
    events.sort((a,b)=>a.t.cmp(b.t));let lb=ZERO,next=null;
    for(let k=0;k<events.length;){
      const tm=events[k].t;let mass=0n,anchor=events[k].anchor;
      do{mass+=events[k].w;anchor=Math.min(anchor,events[k].anchor);k++;}while(k<events.length&&events[k].t.eq(tm));
      const after=side<0?c-mass:c+mass;
      const old=side<0?(c<state.lo?c:state.lo):(c>state.hi?c:state.hi);
      const newer=side<0?(after<state.lo?after:state.lo):(after>state.hi?after:state.hi);
      const gained=side<0?old-newer:newer-old;
      if(gained>0n){lb=lb.a(tm.m(gained));if(next===null)next={t:tm,anchor,d:side};}
      c=after;
    }
    return{lb,next};
  }
  step(){
    if(!this.stack.length){this.complete=true;return false;}
    if(this.stopReason)return false;
    const s=this.stack.pop();this.stats.nodes++;
    const pos=this.ps.map(p=>p.at(s.t));let anchor=s.anchor;
    if(this.mode==="sorted"){
      let fl=0n,fh=0n;
      for(let j=0;j<this.n;j++){const sg=pos[j].cmp(s.x);if(sg<0)fl+=this.ws[j];if(sg<=0)fh+=this.ws[j];if(!sg)anchor=Math.min(anchor,j);}
      const initial=s.lo>s.hi,nl=initial?fl:(fl<s.lo?fl:s.lo),nh=initial?fh:(fh>s.hi?fh:s.hi);
      s.cost=s.cost.a(s.t.m(initial?fh-fl:(s.lo-nl)+(nh-s.hi)));s.lo=nl;s.hi=nh;
      if(s.lo===0n&&s.hi===this.W){this.stats.leaves++;this.recordImprovement(s.cost,s.route);return true;}
    }else{
      for(let j=0;j<this.n;j++)if(pos[j].eq(s.x)){anchor=Math.min(anchor,j);const bit=1n<<BigInt(j);if(!(s.mask&bit)){s.mask|=bit;s.cost=s.cost.a(s.t.m(this.ws[j]));}}
      if(s.mask===this.full){this.stats.leaves++;this.recordImprovement(s.cost,s.route);return true;}
    }
    const key=this.mode==="sorted"?s.lo+"|"+s.hi+"|"+anchor:s.mask+"|"+anchor;
    if(this.options.prune!==false){
      const front=this.memo.get(key)||[];
      if(front.some(z=>z.t.cmp(s.t)<=0&&z.c.cmp(s.cost)<=0)){this.stats.dominated++;return true;}
      this.memo.set(key,[...front.filter(z=>!(s.t.cmp(z.t)<=0&&s.cost.cmp(z.c)<=0)),{t:s.t,c:s.cost}]);
    }
    let lb=s.cost,choices=[];
    if(this.mode==="sorted"){
      for(const d of [-1,1]){const v=this.sortedEvents(s,d,pos);lb=lb.a(v.lb);if(v.next)choices.push(v.next);}
    }else{
      let next=[null,null];
      for(let j=0;j<this.n;j++)if(!(s.mask&(1n<<BigInt(j)))){
        const d=pos[j].cmp(s.x),t=this.ps[j].hit(s.t,s.x,d),k=(d+1)>>1;
        lb=lb.a(t.m(this.ws[j]));if(next[k]===null||t.cmp(next[k].t)<0)next[k]={t,anchor:j,d};
      }
      choices=next.filter(Boolean);
    }
    if(this.options.prune!==false&&lb.cmp(this.best)>=0){this.stats.bounded++;return true;}
    choices.sort((a,b)=>b.t.cmp(a.t)||a.d-b.d);
    for(const c of choices){
      if(c.t.cmp(s.t)<=0)throw Error("non-new capture");
      const x=s.x.a(c.t.s(s.t).m(c.d));
      this.stack.push({lo:s.lo,hi:s.hi,mask:s.mask,t:c.t,x,cost:s.cost,anchor:c.anchor,route:{p:[c.t,x],prev:s.route}});
    }
    return true;
  }
  runSlice(maxNodes=10000,maxMillis=5000){
    const n=this.stats.nodes,start=Date.now();
    while(this.stats.nodes-n<maxNodes&&Date.now()-start<maxMillis&&this.step()){
      if(this.options.nodeLimit&&this.stats.nodes>=this.options.nodeLimit){this.stopReason="node limit";break;}
    }
    if(!this.stack.length&&!this.stopReason)this.complete=true;
    return this.complete||!!this.stopReason;
  }
  result(check=true){
    const m=new PLPath(this.bestRoute),direct=this.mode==="sorted"?sortedCapture(this.ps,this.ws,m):null;
    if(check&&direct&&(!direct.complete||!direct.cost.eq(this.best)))throw Error("independent record cost mismatch");
    if(check&&this.mode==="raw"){
      const cost=this.ps.reduce((acc,p,j)=>{const t=rawCapture(m,p);if(t===null)throw Error("missed target");return acc.a(t.m(this.ws[j]));},ZERO);
      if(!cost.eq(this.best))throw Error("independent segment cost mismatch");
    }
    return{mode:this.mode,complete:this.complete,stopReason:this.stopReason,paths:this.n,weightTotal:String(this.W),value:this.best.dby(this.W).str(),decimal:this.best.dby(this.W).num(),route:this.bestRoute.map(p=>p.map(q=>q.str())),stats:{...this.stats,memoKeys:this.memo.size,remaining:this.stack.length},captureRecords:direct?.captures};
  }
}

function explicitQuantiles(raw,weights){
  const {paths,weights:ws,W}=prepare(raw,weights),ts0=uniq(paths.flatMap(p=>p.t)),events=[...ts0];
  for(let i=0;i<paths.length;i++)for(let j=0;j<i;j++)for(let k=0;k+1<ts0.length;k++){
    const a=ts0[k],b=ts0[k+1],f=paths[i].at(a).s(paths[j].at(a)),g=paths[i].at(b).s(paths[j].at(b));
    if(f.cmp(0)*g.cmp(0)<0)events.push(a.a(b.s(a).m(f).dby(f.s(g))));
  }
  const ts=uniq(events),rows=[],breaks=new Set(["0",String(W)]);
  for(const t of ts){
    const row=paths.map((p,i)=>({x:p.at(t),w:ws[i]})).sort((a,b)=>a.x.cmp(b.x));let c=0n;for(const z of row){c+=z.w;breaks.add(String(c));}rows.push(row);
  }
  for(let k=0;k+1<ts.length;k++){
    const t=ts[k].a(ts[k+1]).dby(2),row=paths.map((p,i)=>({x:p.at(t),w:ws[i]})).sort((a,b)=>a.x.cmp(b.x));let c=0n;for(const z of row){c+=z.w;breaks.add(String(c));}
  }
  const bs=[...breaks].map(BigInt).sort((a,b)=>a<b?-1:a>b?1:0),out=[],weightsOut=[];
  for(let j=0;j+1<bs.length;j++){
    const q2=bs[j]+bs[j+1],path=[];
    rows.forEach((row,k)=>{let c=0n,x=null;for(const z of row){c+=z.w;if(2n*c>=q2){x=z.x;break;}}path.push([ts[k],x]);});
    out.push(new PLPath(path).json());weightsOut.push(String(bs[j+1]-bs[j]));
  }
  return{paths:out,weights:weightsOut,originalPaths:paths.length,sortedPaths:out.length,arrangementTimes:ts.length};
}


function positiveAffineArea(fa,fb,length){
 if(fa.cmp(0)<=0&&fb.cmp(0)<=0)return ZERO;
 if(fa.cmp(0)>=0&&fb.cmp(0)>=0)return length.m(fa.a(fb)).dby(2);
 const p=maxQ(fa,fb);return length.m(p).m(p).dby(p.s(minQ(fa,fb))).dby(2);
}
class MixedFieldScorer{
 constructor(fieldData,lambda,raw=[],weights=[]){
  this.lambda=Q(lambda);if(this.lambda.cmp(0)<0||this.lambda.cmp(1)>0)throw Error("mixture mass");
  this.field=this.lambda.eq(0)?null:new ExactField(fieldData);
  if(raw.length){const f=prepare(raw,weights);this.ps=f.paths;this.ws=f.weights;this.W=f.W;}else{if(!this.lambda.eq(1))throw Error("missing finite part");this.ps=[];this.ws=[];this.W=1n;}
  this.finiteMass=ONE.s(this.lambda);this.cache=new Map();
 }
 sides(t,x){
  t=Q(t);x=Q(x);const key=t.str()+"|"+x.str();if(this.cache.has(key))return this.cache.get(key);
  let low=ZERO,high=ZERO;
  if(this.field){const r=this.field.cdfSides(t,x);low=r[0].m(this.lambda);high=r[1].m(this.lambda);}
  if(!this.finiteMass.eq(0)){
   let a=0n,b=0n;for(let j=0;j<this.ps.length;j++){const sg=this.ps[j].at(t).cmp(x);if(sg<0)a+=this.ws[j];if(sg<=0)b+=this.ws[j];}
   low=low.a(new Rat(a,this.W).m(this.finiteMass));high=high.a(new Rat(b,this.W).m(this.finiteMass));
  }
  if(low.cmp(0)<0||high.cmp(1)>0||low.cmp(high)>0)throw Error("CDF trace range");
  const result=[low,high];this.cache.set(key,result);return result;
 }
 fieldCuts(a,x,b,y){
  if(!this.field)return[];
  const sign=x.a(y).cmp(0)<0?-1:1;
  const p=[a.a(x.m(sign)),a.s(x.m(sign))],q=[b.a(y.m(sign)),b.s(y.m(sign))],d=subP(q,p),out=[];
  if(p[1].cmp(1)>=0)return out;
  if(q[1].cmp(1)>0&&!d[1].eq(0))out.push(a.a(b.s(a).m(ONE.s(p[1])).dby(d[1])));
  let poss=new Set();
  if(d[0].eq(0)||d[1].eq(0)){
   const axis=d[0].eq(0)?0:1,fixed=p[axis],i=Math.max(0,Math.min(this.field.grid[axis].length-2,bisect(this.field.grid[axis],fixed)-1));
   for(const n of [...(this.field.strips[axis].get(i)||[]),...(this.field.strips[axis].get(i-1)||[])])poss.add(n);
  }else{
   const ranges=[0,1].map(k=>[Math.max(0,bisect(this.field.grid[k],p[k],false)-1),Math.min(this.field.grid[k].length-2,bisect(this.field.grid[k],q[k],true))]);
   for(let i=ranges[0][0];i<=ranges[0][1];i++)for(let j=ranges[1][0];j<=ranges[1][1];j++)for(const n of this.field.cells.get(i+","+j)||[])poss.add(n);
  }
  for(const n of poss){
   const ps=this.field.triangles[n].ps;
   for(let k=0;k<3;k++){
    const r=ps[k],s=ps[(k+1)%3],e=subP(s,r),rp=subP(r,p),det=cross(d,e);
    if(!det.eq(0)){
     const t=cross(rp,e).dby(det),u=cross(rp,d).dby(det);
     if(t.cmp(0)>0&&t.cmp(1)<0&&u.cmp(0)>=0&&u.cmp(1)<=0)out.push(a.a(b.s(a).m(t)));
    }else if(cross(rp,d).eq(0)){
     const axis=d[0].eq(0)?1:0;for(const z of [r,s]){const t=z[axis].s(p[axis]).dby(d[axis]);if(t.cmp(0)>0&&t.cmp(1)<0)out.push(a.a(b.s(a).m(t)));}
    }
   }
  }
  return out;
 }
 legCuts(a,x,b,y){
  const vel=y.s(x).dby(b.s(a)),base=[a,b];
  if(x.cmp(0)*y.cmp(0)<0)base.push(a.s(x.dby(vel)));
  const centerCuts=uniq(base),cuts=[...centerCuts];
  for(let k=0;k+1<centerCuts.length;k++){
   const c=centerCuts[k],d=centerCuts[k+1],xc=x.a(vel.m(c.s(a))),xd=x.a(vel.m(d.s(a)));
   cuts.push(...this.fieldCuts(c,xc,d,xd));
  }
  if(!this.finiteMass.eq(0))for(const p of this.ps){
   const ts=uniq([a,b,...p.t.filter(t=>t.cmp(a)>0&&t.cmp(b)<0)]);
   cuts.push(...ts);
   const ds=ts.map(t=>p.at(t).s(x.a(vel.m(t.s(a)))));
   for(let k=0;k+1<ts.length;k++)if(ds[k].cmp(0)*ds[k+1].cmp(0)<0)cuts.push(ts[k].a(ts[k+1].s(ts[k]).m(ds[k]).dby(ds[k].s(ds[k+1]))));
  }
  return uniq(cuts);
 }

 radialIntegral(fixed,left,right,axis,strict=false,threshold=null){
  fixed=Q(fixed);left=Q(left);right=Q(right);if(right.cmp(left)<=0)return ZERO;if(threshold!==null)threshold=Q(threshold);
  const u0=axis===0?fixed:left,v0=axis===0?left:fixed,u1=axis===0?fixed:right,v1=axis===0?right:fixed;
  const a=u0.a(v0).dby(2),b=u1.a(v1).dby(2),x=u0.s(v0).dby(2),y=u1.s(v1).dby(2),vel=y.s(x).dby(b.s(a)),cuts=this.legCuts(a,x,b,y);let total=ZERO;
  for(let k=0;k+1<cuts.length;k++){
   const c=cuts[k],d=cuts[k+1],len=d.s(c),t1=c.a(len.dby(3)),t2=c.a(len.m(2).dby(3));
   const r1=this.sides(t1,x.a(vel.m(t1.s(a))))[strict?0:1].m(2).s(1),r2=this.sides(t2,x.a(vel.m(t2.s(a))))[strict?0:1].m(2).s(1);
   const ra=r1.m(2).s(r2),rb=r2.m(2).s(r1),width=len.m(2);
   total=total.a(threshold===null?width.m(ra.a(rb)).dby(2):positiveAffineArea(threshold.s(ra),threshold.s(rb),width));
  }
  return total;
 }
 positiveM1Moment(a){
  a=Q(a);if(a.cmp(0)<=0||a.cmp(1)>=0)throw Error("moment fixture uses interior start");
  const initial=this.sides(ZERO,a);if(!initial[0].eq(initial[1]))throw Error("initial atom needs a separate moment term");
  const A=initial[1].m(2).s(1),s=Q(2).s(a);
  const I=this.radialIntegral(a.neg(),a,s,1,false),F=this.radialIntegral(s,a.neg(),s,0,true,A),H=this.radialIntegral(s,s,s.a(2),1,false);
  return Q(8).s(a.m(4)).a(s.m(2).m(A)).s(I).s(F).s(H).dby(4);
 }
 score(raw,{checkAffine=true}={}){
  const monster=new PLPath(raw),route=monster.vertices;
  let [lower,upper]=this.sides(...route[0]),cost=ZERO,intervals=0,atomUpdates=0;
  const update=(l,h)=>{const nl=minQ(lower,l),nh=maxQ(upper,h);if(!nl.eq(lower)||!nh.eq(upper))atomUpdates++;lower=nl;upper=nh;};
  for(let k=0;k+1<route.length;k++){
   const [t,x]=route[k],[end,y]=route[k+1],vel=y.s(x).dby(end.s(t)),cuts=this.legCuts(t,x,end,y);
   for(let j=0;j+1<cuts.length;j++){
    const a=cuts[j],b=cuts[j+1],len=b.s(a),t1=a.a(len.dby(3)),t2=a.a(len.m(2).dby(3)),x1=x.a(vel.m(t1.s(t))),x2=x.a(vel.m(t2.s(t)));
    update(...this.sides(a,x.a(vel.m(a.s(t)))));
    const f1=this.sides(t1,x1),f2=this.sides(t2,x2),fa=f1.map((z,i)=>z.m(2).s(f2[i])),fb=f2.map((z,i)=>z.m(2).s(f1[i]));
    if(checkAffine){
     const tm=a.a(b).dby(2),mid=this.sides(tm,x.a(vel.m(tm.s(t))));
     if(!mid.every((z,i)=>z.m(2).eq(f1[i].a(f2[i]))))throw Error("missed CDF affine boundary");
    }
    if(fa[0].cmp(0)<0||fb[0].cmp(0)<0||fa[1].cmp(1)>0||fb[1].cmp(1)>0)throw Error("bad extrapolated CDF");
    update(...fa);
    const baseline=len.m(ONE.s(upper).a(lower)),up=positiveAffineArea(fa[1].s(upper),fb[1].s(upper),len),down=positiveAffineArea(lower.s(fa[0]),lower.s(fb[0]),len),area=baseline.s(up).s(down);
    if(area.cmp(0)<0)throw Error("negative survival area");
    cost=cost.a(area);update(...fb);update(...this.sides(b,x.a(vel.m(b.s(t)))));intervals++;
   }
  }
  return{value:cost.str(),decimal:cost.num(),complete:lower.eq(0)&&upper.eq(1),lower:lower.str(),upper:upper.str(),horizon:route.at(-1)[0].str(),intervals,atomUpdates};
 }
}
return{Rat,Q,ZERO,ONE,ExactField,PLPath,prepare,rawCapture,CaptureSearch,sortedCapture,MixedFieldScorer,positiveAffineArea};

}
export {createMixedScorer};
async function main(){
 const fs=await import("node:fs/promises"),crypto=await import("node:crypto"),args=process.argv.slice(2);if(args.length<3)throw Error("usage: node mixed_cdf_payoff.mjs FIELD.json MIXTURE.json ROUTE.json");
 const texts=await Promise.all(args.slice(0,3).map(p=>fs.readFile(p,"utf8"))),[field,mix,routeInput]=texts.map(JSON.parse),L=createMixedScorer();
 if(mix.continuous.length!==1)throw Error("one identified continuous component required");
 const paths=[],weights=[];let total=L.Q(mix.continuous[0].weight);
 for(const p of mix.paths){total=total.a(p.weight);paths.push(p.path,p.path.map(([t,x])=>[t,L.Q(x).neg().str()]));weights.push(p.weight,p.weight);}
 if(!total.eq(1))throw Error("mixture weights do not sum to one");
 const scorer=new L.MixedFieldScorer(field,mix.continuous[0].weight,paths,weights),result=scorer.score(routeInput.route||routeInput);
 result.scope="Exact payoff of the supplied route against the ordered full marginal mixture; not an all-monster lower certificate.";
 result.input_sha256=texts.map(t=>crypto.createHash("sha256").update(t).digest("hex"));console.log(JSON.stringify(result,null,2));
}
if(typeof process!=="undefined"&&process.argv[1]){const {pathToFileURL}=await import("node:url");if(import.meta.url===pathToFileURL(process.argv[1]).href)await main();}
