/** Exact QQ(epsilon) adapter for the unchanged finite_quantile_response.mjs core.
 * Source core:51dbac43b59c3041abf831837dc58fde2a9294b2.
 * Realization and branch radius follow germ_response.py:99f6b3f384a71f155280d1c7aa240b65a112ddcb.
 * A stopped search supplies an attack, never an all-monster lower certificate.
 */
module.exports = (function(){

function createGermArithmetic(E){
 const R=E.Q,rz=R(0),ro=R(1);let radius=R("1/4"),comparisons=0,maxDegree=0;
 const iszero=p=>p.length===1&&p[0].eq(0);
 const trim=p=>{p=p.slice();while(p.length>1&&p.at(-1).eq(0))p.pop();return p;};
 const add=(p,q)=>trim(Array.from({length:Math.max(p.length,q.length)},(_,j)=>(p[j]||rz).a(q[j]||rz)));
 const neg=p=>p.map(x=>x.neg());
 const sub=(p,q)=>add(p,neg(q));
 function mul(p,q){if(iszero(p)||iszero(q))return[rz];const z=Array(p.length+q.length-1).fill(rz);for(let i=0;i<p.length;i++)if(!p[i].eq(0))for(let j=0;j<q.length;j++)if(!q[j].eq(0))z[i+j]=z[i+j].a(p[i].m(q[j]));return trim(z);}
 const scale=(p,a)=>trim(p.map(x=>x.m(a)));
 function divmod(p,q){p=trim(p);q=trim(q);if(iszero(q))throw Error("zero polynomial divisor");const out=Array(Math.max(1,p.length-q.length+1)).fill(rz);while(!iszero(p)&&p.length>=q.length){const k=p.length-q.length,c=p.at(-1).dby(q.at(-1));out[k]=out[k].a(c);for(let j=0;j<q.length;j++)p[k+j]=p[k+j].s(c.m(q[j]));p=trim(p);}return[trim(out),p];}
 const monic=p=>iszero(p)?p:scale(p,ro.dby(p.at(-1)));
 function pgcd(p,q){p=trim(p);q=trim(q);if(iszero(q))return monic(p);if(p.length===1||q.length===1)return[ro];while(!iszero(q)){const r=divmod(p,q)[1];p=q;q=r;}return monic(p);}
 function psign(p){p=trim(p);if(iszero(p))return 0;maxDegree=Math.max(maxDegree,p.length-1);let j=0;while(p[j].eq(0))j++;const lead=p[j],rem=p.slice(j+1).reduce((s,a)=>s.a(a.cmp(0)<0?a.neg():a),rz);if(!rem.eq(0)){const b=(lead.cmp(0)<0?lead.neg():lead).dby(rem.m(2));if(b.cmp(radius)<0)radius=b;}return lead.cmp(0);}
 function decode(x){if(x instanceof Germ)return[x.p,x.q];if(typeof x==="string"&&x.startsWith("germ:")){const d=JSON.parse(x.slice(5));return[d[0].map(R),d[1].map(R)];}return[[R(x)],[ro]];}
 class Germ{
  constructor(p=0,q=null,raw=false){
   if(q===null){const d=decode(p);this.p=d[0];this.q=d[1];return;}
   p=trim(p.map(R));q=trim(q.map(R));if(iszero(q))throw Error("zero denominator");
   if(iszero(p)){this.p=[rz];this.q=[ro];return;}
   if(q.length===1){this.p=scale(p,ro.dby(q[0]));this.q=[ro];return;}
   const g=pgcd(p,q);if(g.length>1){p=divmod(p,g)[0];q=divmod(q,g)[0];}
   const f=ro.dby(q.at(-1));this.p=scale(p,f);this.q=scale(q,f);
  }
  a(x){x=Q(x);return new Germ(add(mul(this.p,x.q),mul(x.p,this.q)),mul(this.q,x.q));}
  s(x){return this.a(Q(x).neg());}
  neg(){return new Germ(neg(this.p),this.q);}
  m(x){x=Q(x);return new Germ(mul(this.p,x.p),mul(this.q,x.q));}
  dby(x){x=Q(x);if(iszero(x.p))throw Error("zero germ divisor");psign(x.p);psign(x.q);return new Germ(mul(this.p,x.q),mul(this.q,x.p));}
  pow(n){if(!Number.isInteger(n)||n<0)throw Error("integer power");let a=Q(1),b=this;while(n){if(n%2)a=a.m(b);n=Math.floor(n/2);if(n)b=b.m(b);}return a;}
  cmp(x){comparisons++;x=Q(x);return psign(sub(mul(this.p,x.q),mul(x.p,this.q)))*psign(mul(this.q,x.q));}
  eq(x){return this.cmp(x)===0;}
  limit(){if(iszero(this.p))return rz;let i=0,j=0;while(this.p[i].eq(0))i++;while(this.q[j].eq(0))j++;if(i<j)throw Error("infinite germ limit");return i>j?rz:this.p[i].dby(this.q[j]);}
  evaluate(e){e=R(e);const ev=p=>p.reduceRight((s,a)=>s.m(e).a(a),rz);return ev(this.p).dby(ev(this.q));}
  str(){return this.p.length===1&&this.q.length===1?this.p[0].dby(this.q[0]).str():"germ:"+JSON.stringify([this.p.map(x=>x.str()),this.q.map(x=>x.str())]);}
  num(){return this.limit().num();}
  get n(){if(this.p.length!==1||this.q.length!==1)throw Error("nonconstant weight");return this.p[0].dby(this.q[0]).n;}
  get d(){if(this.p.length!==1||this.q.length!==1)throw Error("nonconstant weight");return this.p[0].dby(this.q[0]).d;}
  data(){return{numerator:Object.fromEntries(this.p.map((x,j)=>[j,x.str()]).filter(x=>x[1]!=="0")),denominator:Object.fromEntries(this.q.map((x,j)=>[j,x.str()]).filter(x=>x[1]!=="0"))};}
 }
 function Q(x){return x instanceof Germ?x:new Germ(x);}
 const eps=new Germ([rz,ro],[ro]);
 return{Germ,Q,ZERO:Q(0),ONE:Q(1),eps,stats:()=>({radius:radius.str(),comparisons,maxDegree}),reset:()=>{radius=R("1/4");comparisons=0;maxDegree=0;},poly:{add,sub,mul,divmod,pgcd}};
}


function createGermOracle(E){
 const A=createGermArithmetic(E),{Q,ZERO,ONE}=A,Rat=A.Germ;
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const r=a%b;a=b;b=r;}return a;}
 function minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}
 function maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}
 function uniq(xs){const m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}
 function bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){const m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}
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


 function realize(queryV,baseLevels,indices){
  const vv=queryV.map(Q),values=indices.map(k=>Q(baseLevels[Math.floor(k/3)]).a(A.eps.m(k%3-1)));
  const points=[[ZERO,Q(-1)]],eps=A.eps;
  function add(u,v){u=Q(u);v=Q(v);const p=points.at(-1);if(u.eq(p[0])&&v.eq(p[1]))return;if(u.cmp(p[0])<0||v.cmp(p[1])<0||u.s(v).cmp(0)<0||u.s(v).cmp(2)>0)throw Error("illegal light germ");points.push([u,v]);}
  for(let j=1;j<vv.length;j++){
   const v=vv[j],prev=values[j-1],target=values[j],delta=minQ(eps.pow(2),v.s(vv[j-1]).dby(3)),before=v.s(delta);
   add(prev,minQ(before,prev));if(before.cmp(prev)>0)add(before,before);
   add(minQ(target,before.a(2)),before);if(target.cmp(before.a(2))>0)add(target,target.s(2));add(target,v);
  }
  const path=[];
  for(let j=0;j+1<points.length;j++){
   const[u0,v0]=points[j],[u1,v1]=points[j+1],t0=u0.a(v0).dby(2),t1=u1.a(v1).dby(2);
   if(t1.cmp(0)<0)continue;const x0=u0.s(v0).dby(2),x1=u1.s(v1).dby(2);
   if(!path.length){if(t0.cmp(0)>0)throw Error("missing initial crossing");path.push([ZERO,x0.a(x1.s(x0).m(t0.neg()).dby(t1.s(t0)))]);}
   if(t1.cmp(path.at(-1)[0])>0)path.push([t1,x1]);
  }
  const eta=eps.pow(6),shrink=ONE.s(eta.m(2));return new PLPath(path.map(([t,x])=>[t,x.m(shrink).a(eta)]));
 }
 return{...A,Rat,Q,ZERO,ONE,PLPath,prepare,rawCapture,sortedCapture,CaptureSearch,compressRoute,explicitQuantiles,realize};


}
return {createGermArithmetic,createGermOracle};
})();
