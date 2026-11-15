/**
 * Exact unrestricted monster response to a finite rational polygonal princess law.
 * The core is also executed directly as a V8 function body in this checkpoint.
 * Default mode uses the stronger comonotone quantile coupling of the input law.
 * A stopped search supplies an attained attack, never an optimality certificate.
 */
function createOracle(){

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

return{Rat,Q,ZERO,ONE,PLPath,prepare,rawCapture,sortedCapture,CaptureSearch,compressRoute,explicitQuantiles};

}
export {createOracle};
async function main(){
  const fs=await import("node:fs/promises"),crypto=await import("node:crypto");
  const args=process.argv.slice(2),file=args[0];if(!file)throw Error("usage: node finite_quantile_response.mjs INPUT.json [--raw] [--nodes N] [--target FRACTION]");
  const text=await fs.readFile(file,"utf8"),input=JSON.parse(text),L=createOracle(),paths=[],weights=[];
  const add=(p,w,pair)=>{paths.push(p);weights.push(w);if(pair){paths.push(p.map(([t,x])=>[t,L.Q(x).neg().str()]));weights.push(w);}};
  if(input.paths_h){input.paths_h.forEach((p,i)=>add(p.map(([t,x])=>[L.Q(t).dby(input.S).str(),L.Q(x).dby(input.S).str()]),String(input.weights_h[i]),true));}
  else if(input.paths?.[0]?.path){const pair=String(input.pairing||"").includes("negative reflection");input.paths.forEach(p=>add(p.path,p.weight,pair));}
  else input.paths.forEach((p,i)=>add(p,input.weights[i],input.pairing==="symmetric_radial"));
  const arg=(key,def)=>{const i=args.indexOf(key);return i<0?def:args[i+1];};
  const options={mode:args.includes("--raw")?"raw":"sorted",nodeLimit:Number(arg("--nodes","1000000000"))};
  if(args.includes("--target"))options.target=arg("--target");
  const s=new L.CaptureSearch(paths,weights,options),start=Date.now();
  while(!s.runSlice(10000,1000))await new Promise(resolve=>setImmediate(resolve));
  const result=s.result();result.input_sha256=crypto.createHash("sha256").update(text).digest("hex");result.wall_ms=Date.now()-start;
  console.log(JSON.stringify(result,null,2));
}
if(typeof process!=="undefined"&&process.argv[1]){
 const {pathToFileURL}=await import("node:url");
 if(import.meta.url===pathToFileURL(process.argv[1]).href)await main();
}
