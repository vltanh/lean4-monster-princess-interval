// Numerical attack discovery; exact final scores use mixed_cdf_payoff.mjs.
// Node CLI wrapper reconstructed during executor outage; the body was executed in V8.
import {createMixedScorer} from "./mixed_cdf_payoff.mjs";
import floatFieldDiscovery from "./float_field_discovery.cjs";
const {FloatField}=floatFieldDiscovery;
function createMixedDiscovery(){

/* Numerical discovery only. Full-law claims require createMixedScorer().MixedFieldScorer.score. */

const D=(()=>{
function bis(a,x,left=false){let l=0,r=a.length;while(l<r){const m=(l+r)>>1;if(a[m]<x||(!left&&a[m]===x))l=m+1;else r=m;}return l;}
function asNumber(z){if(typeof z==="number")return z;const p=String(z).split("/"),a=p[0],b=p[1]||"1";const aa=Number(a),bb=Number(b);if(Number.isFinite(aa)&&Number.isFinite(bb))return aa/bb;const neg=a[0]==="-",n=neg?a.slice(1):a;return(neg?-1:1)*Number(n.slice(0,16))/Number(b.slice(0,16))*10**(n.length-b.length-Math.min(n.length,16)+Math.min(b.length,16));}
class NPath{
 constructor(raw){this.t=raw.map(p=>asNumber(p[0]));this.x=raw.map(p=>asNumber(p[1]));this.v=this.t.slice(1).map((t,i)=>(this.x[i+1]-this.x[i])/(t-this.t[i]));this.seq=[this.t.map((t,i)=>t+this.x[i]),this.t.map((t,i)=>t-this.x[i])];}
 at(t){const k=Math.max(0,bis(this.t,t)-1);return k+1===this.t.length?this.x[k]:this.x[k]+this.v[k]*(t-this.t[k]);}
 hit(t,x,d){
  if(Math.abs(this.at(t)-x)<2e-11)return t;const q=t-d*x,seq=this.seq[(d+1)>>1],k=bis(seq,q,true);
  let ans;if(k===seq.length)ans=this.t.at(-1)+q-seq.at(-1);else if(!k)ans=t;else{const den=1-d*this.v[k-1];ans=den<1e-13?this.t[k]:this.t[k-1]+(q-seq[k-1])/den;}
  return Math.max(t,ans);
 }
}
function sampleQuantiles(field,data,n=64,steps=256){
 const lambda=asNumber(data.continuous[0].weight),finite=data.paths.map(p=>({p:new NPath(p.path),w:asNumber(p.weight)})),radial=Array.from({length:n},()=>[]);
 for(let k=0;k<=steps;k++){
  const t=2*k/steps,rows=finite.map(({p,w})=>({x:p.at(t),w})).sort((a,b)=>a.x-b.x);let cum=0;for(const row of rows){cum+=row.w;row.cum=cum;}
  function cdf(r){if(r>=1)return 1;const j=bis(rows.map(x=>x.x),r)-1;return lambda*Math.max(0,Math.min(1,field.radial(t+r,t-r)))+(j<0?0:rows[j].cum);}
  let previous=0;
  for(let j=0;j<n;j++){
   const q=(j+.5)/n;let lo=previous,hi=1;
   if(cdf(0)>=q)lo=hi=0;else for(let it=0;it<43;it++){const m=(lo+hi)/2;if(cdf(m)>=q)hi=m;else lo=m;}
   let x=(lo+hi)/2;if(k){const old=radial[j].at(-1)[1],dt=2/steps;x=Math.max(old-dt,Math.min(old+dt,x));}x=Math.max(previous,Math.min(1,Math.max(0,x)));radial[j].push([t,x]);previous=x;
  }
  field.rcache.clear();
 }
 const signed=[...radial].reverse().map(p=>p.map(([t,x])=>[t,-x])).concat(radial);return{radial,signed,rankCount:n,timeSteps:steps};
}
function shorten(route){const out=[];for(const p of route){out.push(p);while(out.length>=3){const n=out.length,d1=Math.sign(out[n-2][1]-out[n-3][1]),d2=Math.sign(out[n-1][1]-out[n-2][1]);if(d1===d2)out.splice(n-2,1);else break;}}return out;}
function orderedSearch(raw,nodeLimit=500000){
 const ps=raw.map(p=>new NPath(p)),n=ps.length,memo=new Map(),stack=[],stats={nodes:0,bounded:0,dominated:0,leaves:0},improvements=[];
 let best=ps.reduce((s,p)=>s+p.hit(0,-1,1),0),bestRoute=[[0,-1],[2,1]];
 for(let i=0;i<n;i++)if(ps[i].x[0]>=-1e-13&&(!i||Math.abs(ps[i].x[0]-ps[i-1].x[0])>1e-12))stack.push({l:i,r:i,anchor:i,t:0,x:ps[i].x[0],cost:0,route:[[0,ps[i].x[0]]]});
 while(stack.length&&stats.nodes<nodeLimit){
  const s=stack.pop();stats.nodes++;
  while(s.l>0&&Math.abs(ps[s.l-1].at(s.t)-s.x)<2e-10){s.l--;s.cost+=s.t;}
  while(s.r+1<n&&Math.abs(ps[s.r+1].at(s.t)-s.x)<2e-10){s.r++;s.cost+=s.t;}
  if(s.l===0&&s.r===n-1){stats.leaves++;if(s.cost<best-1e-12){best=s.cost;bestRoute=shorten(s.route);improvements.push({cost:best/n,route:bestRoute});}continue;}
  const key=s.l+","+s.r+","+s.anchor,front=memo.get(key)||[];
  if(front.some(z=>z.t<=s.t+1e-12&&z.c<=s.cost+1e-12)){stats.dominated++;continue;}
  memo.set(key,front.filter(z=>!(s.t<=z.t+1e-12&&s.cost<=z.c+1e-12)).concat([{t:s.t,c:s.cost}]));
  let lb=s.cost;for(let j=0;j<s.l;j++)lb+=ps[j].hit(s.t,s.x,-1);for(let j=s.r+1;j<n;j++)lb+=ps[j].hit(s.t,s.x,1);
  if(lb>=best-1e-12){stats.bounded++;continue;}
  const choices=[];if(s.l>0)choices.push({j:s.l-1,d:-1,t:ps[s.l-1].hit(s.t,s.x,-1)});if(s.r+1<n)choices.push({j:s.r+1,d:1,t:ps[s.r+1].hit(s.t,s.x,1)});
  choices.sort((a,b)=>b.t-a.t||a.d-b.d);
  for(const c of choices){if(c.t<=s.t+1e-13)continue;const x=s.x+c.d*(c.t-s.t);stack.push({l:Math.min(s.l,c.j),r:Math.max(s.r,c.j),anchor:c.j,t:c.t,x,cost:s.cost+c.t,route:s.route.concat([[c.t,x]])});}
 }
 return{scope:"Numerical discovery on interpolated quantiles only; no lower certificate",cost:best/n,route:bestRoute,improvements,stats:{...stats,remaining:stack.length,memoKeys:memo.size},exhausted:!stack.length};
}

function uniqF(a){a.sort((x,y)=>x-y);return a.filter((x,i)=>!i||x-a[i-1]>2e-12);}
function posArea(a,b,len){if(a<=0&&b<=0)return 0;if(a>=0&&b>=0)return len*(a+b)/2;const p=Math.max(a,b);return len*p*p/(p-Math.min(a,b))/2;}
class FloatMixed{
 constructor(field,data){this.field=field;this.lambda=asNumber(data.continuous[0].weight);this.paths=[];for(const p of data.paths){const path=new NPath(p.path),w=asNumber(p.weight)/2;this.paths.push({p:path,w},{p:new NPath(p.path.map(([t,x])=>[t,-asNumber(x)])),w});}}
 sides(t,x){
  const r=this.field.radial(t+Math.abs(x),t-Math.abs(x));let lo,hi;
  if(Math.abs(x)<1e-12){lo=(1-r)/2;hi=(1+r)/2;}
  else if(x>=1-1e-13){lo=(1+r)/2;hi=1;}
  else if(x<=-1+1e-13){lo=0;hi=(1-r)/2;}
  else lo=hi=x>0?(1+r)/2:(1-r)/2;
  lo*=this.lambda;hi*=this.lambda;
  for(const {p,w}of this.paths){const y=p.at(t);if(y<x-1e-12)lo+=w;if(y<=x+1e-12)hi+=w;}
  return[Math.max(0,Math.min(1,lo)),Math.max(0,Math.min(1,hi))];
 }
 fieldCuts(a,x,b,y){
  const sign=x+y<0?-1:1,p=[a+sign*x,a-sign*x],q=[b+sign*y,b-sign*y],du=q[0]-p[0],dv=q[1]-p[1],out=[];
  if(p[1]>=1-1e-13)return out;if(q[1]>1&&dv>0)out.push(a+(b-a)*(1-p[1])/dv);
  const axis=Math.abs(du)<1e-10?0:1,fixed=p[axis],other=1-axis;
  const grid=this.field.grid[axis],i=Math.max(0,Math.min(grid.length-2,bis(grid,fixed)-1)),poss=new Set([...(this.field.strips[axis].get(i)||[]),...(this.field.strips[axis].get(i-1)||[])]);
  const vl=p[other],vr=q[other];for(const n of poss){const ps=this.field.triangles[n].ps;for(let k=0;k<3;k++){const l=ps[k],r=ps[(k+1)%3];if(l[axis]===r[axis]){if(Math.abs(l[axis]-fixed)<1e-13)for(const z of[l[other],r[other]])if(z>vl+1e-13&&z<vr-1e-13)out.push(a+(b-a)*(z-vl)/(vr-vl));}else if(Math.min(l[axis],r[axis])<=fixed&&fixed<=Math.max(l[axis],r[axis])){const z=l[other]+(fixed-l[axis])*(r[other]-l[other])/(r[axis]-l[axis]);if(z>vl+1e-13&&z<vr-1e-13)out.push(a+(b-a)*(z-vl)/(vr-vl));}}}
  return out;
 }
 score(route){
  let[lo,hi]=this.sides(...route[0]),cost=0;const update=(a,b)=>{lo=Math.min(lo,a);hi=Math.max(hi,b);};
  for(let k=0;k+1<route.length;k++){
   const[t,x]=route[k],[end,y]=route[k+1],len=end-t;if(len<1e-13)continue;const v=(y-x)/len;if(Math.abs(Math.abs(v)-1)>1e-8)throw Error("unit legs only");
   const bas=[t,end];if(x*y<0)bas.push(t-x/v);const split=uniqF(bas),cuts=[...split];
   for(let j=0;j+1<split.length;j++){const a=split[j],b=split[j+1];cuts.push(...this.fieldCuts(a,x+v*(a-t),b,x+v*(b-t)));}
   for(const {p}of this.paths){const rel=p.at(t)-x;if(Math.abs(rel)<1e-12||Math.sign(rel)===Math.sign(v)){const tt=p.hit(t,x,Math.sign(v));if(tt>t+1e-13&&tt<end-1e-13)cuts.push(tt);}}
   const cs=uniqF(cuts);
   for(let j=0;j+1<cs.length;j++){
    const a=cs[j],b=cs[j+1],w=b-a;update(...this.sides(a,x+v*(a-t)));
    const f=this.sides(a+w/3,x+v*(a+w/3-t)),g=this.sides(a+2*w/3,x+v*(a+2*w/3-t)),fa=f.map((z,i)=>2*z-g[i]),fb=g.map((z,i)=>2*z-f[i]);update(...fa);
    const area=w*(1-hi+lo)-posArea(fa[1]-hi,fb[1]-hi,w)-posArea(lo-fa[0],lo-fb[0],w);cost+=Math.max(0,area);update(...fb);update(...this.sides(b,x+v*(b-t)));
   }
  }
  if(lo>1e-7||hi<1-1e-7)return Infinity;
  if(this.field.rcache.size>100000)this.field.rcache.clear();
  return cost;
 }
}
function routeFromPositions(xs){let t=0,out=[[0,xs[0]]];for(let i=1;i<xs.length;i++){if(Math.abs(xs[i]-xs[i-1])<1e-13)continue;t+=Math.abs(xs[i]-xs[i-1]);out.push([t,xs[i]]);}return shorten(out);}

class HybridMixed extends FloatMixed{
 constructor(field,data,core){super(field,data);this.Q=core.Q;this.exactPaths=[];for(const p of data.paths){const w=asNumber(p.weight)/2;this.exactPaths.push({p:new core.PLPath(p.path),w},{p:new core.PLPath(p.path.map(([t,x])=>[t,core.Q(x).neg().str()])),w});}}
 fieldSides(t,x){
  const r=this.field.radial(t+Math.abs(x),t-Math.abs(x));if(Math.abs(x)<1e-14)return[(1-r)/2,(1+r)/2];
  if(x>=1-1e-14)return[(1+r)/2,1];if(x<=-1+1e-14)return[0,(1-r)/2];return x>0?[(1+r)/2,(1+r)/2]:[(1-r)/2,(1-r)/2];
 }
 scoreExactRoute(raw){
  const rr=raw.map(p=>p.map(this.Q)),route=rr.map(p=>p.map(q=>q.num()));
  let fl=0,fh=0;for(const {p,w}of this.exactPaths){const c=p.at(rr[0][0]).cmp(rr[0][1]);if(c<0)fl+=w;if(c<=0)fh+=w;}
  const side=this.fieldSides(...route[0]);let lo=this.lambda*side[0]+fl,hi=this.lambda*side[1]+fh,cost=0;
  const update=(a,b)=>{lo=Math.min(lo,a);hi=Math.max(hi,b);};
  for(let k=0;k+1<route.length;k++){
   const[t,x]=route[k],[end,y]=route[k+1],len=end-t;if(len<1e-15)continue;
   const d=rr[k+1][1].s(rr[k][1]).cmp(0);
   if(d===0&&rr[k][1].eq(0)){
    const cuts=uniqF([t,end,...this.field.grid[0].filter(z=>z>t&&z<end),...this.field.grid[1].filter(z=>z>t&&z<end)]);
    let fl=0,fh=0;for(const{p,w}of this.exactPaths){const s=p.at(rr[k][0]).cmp(0);if(s<0)fl+=w;if(s<=0)fh+=w;}
    for(let j=0;j+1<cuts.length;j++){const a=cuts[j],b=cuts[j+1],w=b-a,aa=this.fieldSides(a,0);update(this.lambda*aa[0]+fl,this.lambda*aa[1]+fh);const f=this.fieldSides(a+w/3,0),g=this.fieldSides(a+2*w/3,0),fa=f.map((z,i)=>this.lambda*(2*z-g[i])+(i?fh:fl)),fb=g.map((z,i)=>this.lambda*(2*z-f[i])+(i?fh:fl));update(...fa);cost+=Math.max(0,w*(1-hi+lo)-posArea(fa[1]-hi,fb[1]-hi,w)-posArea(lo-fa[0],lo-fb[0],w));update(...fb);}
    continue;
   }
   if(!rr[k+1][1].s(rr[k][1]).m(d).eq(rr[k+1][0].s(rr[k][0])))throw Error("exact unit leg needed");
   const point0=this.fieldSides(t,x);fl=0;fh=0;const events=[];
   for(const{p,w}of this.exactPaths){const c=p.at(rr[k][0]).cmp(rr[k][1]);if(c<0)fl+=w;if(c<=0)fh+=w;if(c===d){const hit=p.hit(rr[k][0],rr[k][1],d);if(hit&&hit.cmp(rr[k+1][0])<=0)events.push({t:hit.num(),delta:d*w});}}
   update(this.lambda*point0[0]+fl,this.lambda*point0[1]+fh);
   let fp=d===1?fh:fl;const bas=[t,end];if(x*y<0)bas.push(t-x/d);const base=uniqF(bas);
   for(let j=0;j+1<base.length;j++)for(const tt of this.fieldCuts(base[j],x+d*(base[j]-t),base[j+1],x+d*(base[j+1]-t)))events.push({t:tt,delta:0});
   for(const tt of base)events.push({t:tt,delta:0});
   events.sort((a,b)=>a.t-b.t);const es=[];for(const e of events){if(es.length&&Math.abs(e.t-es.at(-1).t)<2e-14)es.at(-1).delta+=e.delta;else es.push({...e});}
   if(es[0].t<t-1e-12||es.at(-1).t>end+1e-12)throw Error("event range");
   for(let j=0;j+1<es.length;j++){
    const a=es[j].t,b=es[j+1].t,w=b-a;fp+=es[j].delta;const aa=this.fieldSides(a,x+d*(a-t));update(this.lambda*aa[0]+fp,this.lambda*aa[1]+fp);
    if(w>0){
     const f=this.fieldSides(a+w/3,x+d*(a+w/3-t)),g=this.fieldSides(a+2*w/3,x+d*(a+2*w/3-t)),fa=f.map((z,i)=>this.lambda*(2*z-g[i])+fp),fb=g.map((z,i)=>this.lambda*(2*z-f[i])+fp);update(...fa);
     cost+=Math.max(0,w*(1-hi+lo)-posArea(fa[1]-hi,fb[1]-hi,w)-posArea(lo-fa[0],lo-fb[0],w));update(...fb);
    }
    const nextfp=fp+es[j+1].delta,bb=this.fieldSides(b,x+d*(b-t));update(this.lambda*bb[0]+Math.min(fp,nextfp),this.lambda*bb[1]+Math.max(fp,nextfp));
   }
  }
  if(this.field.rcache.size>100000)this.field.rcache.clear();
  return{cost,complete:lo<1e-9&&hi>1-1e-9,lo,hi};
 }
 rationalPositions(xs,digits=12){let t=this.Q(0),r=[[t,this.Q(xs[0].toFixed(digits))]];for(let i=1;i<xs.length;i++){const x=this.Q(xs[i].toFixed(digits)),last=r.at(-1)[1],dx=x.s(last),sign=dx.cmp(0);if(!sign)continue;t=t.a(dx.m(sign));r.push([t,x]);}return r.map(p=>p.map(x=>x.str()));}
}
return{NPath,sampleQuantiles,orderedSearch,asNumber,FloatMixed,HybridMixed,routeFromPositions};
})();
const O=(()=>{
function charRoute(p,core,dir=1){
 const a=core.Q(p[0].toFixed(12)),q=p.slice(1).map(x=>core.Q(x.toFixed(12))),r=[[core.Q(0),a]];let U=a,V=a.neg(),d=dir;
 for(const v of q){if(d===1)U=v;else V=v;r.push([U.a(V).dby(2),U.s(V).dby(2)]);d=-d;}
 const z=q.at(-1);r.push([z.a(1),core.Q(d)],[z.a(3),core.Q(-d)]);return r.map(p=>p.map(x=>x.str()));
}
function nelder(fn,seed,scales,maxEval=350){
 const n=seed.length;let evals=0;const ev=p=>({p,f:fn(p),id:evals++});let simplex=[ev(seed.slice()),...scales.map((s,i)=>ev(seed.map((x,j)=>x+(i===j?s:0))))],history=[];
 while(evals<maxEval){
 simplex.sort((a,b)=>a.f-b.f);history.push({evals,f:simplex[0].f,p:simplex[0].p});const center=Array(n).fill(0);for(let i=0;i<n;i++)for(let j=0;j<n;j++)center[j]+=simplex[i].p[j]/n;
 const w=simplex[n],ref=ev(center.map((x,j)=>2*x-w.p[j]));
 if(ref.f<simplex[0].f){const ex=ev(center.map((x,j)=>3*x-2*w.p[j]));simplex[n]=ex.f<ref.f?ex:ref;}
 else if(ref.f<simplex[n-1].f)simplex[n]=ref;
 else{const outside=ref.f<w.f,co=ev(center.map((x,j)=>x+.5*((outside?ref:w).p[j]-x)));if(co.f<(outside?ref:w).f)simplex[n]=co;else for(let i=1;i<=n;i++)simplex[i]=ev(simplex[i].p.map((x,j)=>(x+simplex[0].p[j])/2));}
 if(simplex.every(s=>s.p.every((x,j)=>Math.abs(x-simplex[0].p[j])<2e-10)))break;
 }
 simplex.sort((a,b)=>a.f-b.f);return{...simplex[0],evals,history};
}
return{charRoute,nelder};
})();
function make(fieldData,mix,core){
 const field=new FloatField(fieldData),hybrid=new D.HybridMixed(field,mix,core);
 return {
  sample:(n=48,steps=256)=>D.sampleQuantiles(field,mix,n,steps),
  search:(sample,nodes=600000)=>D.orderedSearch(sample.signed,nodes),
  score:route=>hybrid.scoreExactRoute(route),
  rationalPositions:(xs,digits=12)=>hybrid.rationalPositions(xs,digits),
  charRoute:(p,dir=1)=>O.charRoute(p,core,dir),
  nelder:O.nelder
 };
}
return {make,FloatField,scope:"Exact finite-contact predicates with floating affine-field integration, for attack discovery only."};

}
export {createMixedDiscovery};
async function main(){
 const fs=await import("node:fs/promises"),crypto=await import("node:crypto"),args=process.argv.slice(2);
 if(args.length<2)throw Error("usage: node discover_mixed_response.mjs FIELD.json MIXTURE.json [--search]");
 const texts=await Promise.all(args.slice(0,2).map(p=>fs.readFile(p,"utf8"))),[field,mix]=texts.map(JSON.parse),core=createMixedScorer(),d=createMixedDiscovery().make(field,mix,core);
 const paths=[],weights=[];let total=core.Q(mix.continuous[0].weight);for(const p of mix.paths){total=total.a(p.weight);paths.push(p.path,p.path.map(([t,x])=>[t,core.Q(x).neg().str()]));weights.push(p.weight,p.weight);}if(!total.eq(1))throw Error("mass one");
 const scorer=new core.MixedFieldScorer(field,mix.continuous[0].weight,paths,weights),routes=[{"name":"late_negative_M2","route":[["0","434153572919/500000000000"],["950718151079/1000000000000","-82411005241/1000000000000"],["12707057227/6250000000","1"],["25207057227/6250000000","-1"]]},{"name":"center_wait_two_excursions","route":[["0","0"],["3/20","0"],["69/160","9/32"],["2197/2560","-373/2560"],["513/256","1"],["1025/256","-1"]]},{"name":"five_interior_turns","route":[["0","0"],["1/40","-1/40"],["3/40","1/40"],["1/8","-1/40"],["69/160","9/32"],["2197/2560","-373/2560"],["513/256","1"],["1025/256","-1"]]}];
 let search=null;if(args.includes("--search")){const sample=d.sample(48,256);search=d.search(sample,600000);const xs=search.route.map(p=>p[1]);if(xs.at(-1)!==1)xs.push(1);xs.push(-1);routes.push({name:"discovered_capture_order",route:d.rationalPositions(xs)});}
 const results=routes.map(row=>({...row,discovery:d.score(row.route),exact:scorer.score(row.route)}));
 console.log(JSON.stringify({scope:"Exact scores of specific routes; neither quantile search nor floating discovery certifies the unrestricted game.",input_sha256:texts.map(t=>crypto.createHash("sha256").update(t).digest("hex")),search,results},null,2));
}
if(typeof process!=="undefined"&&process.argv[1]){const {pathToFileURL}=await import("node:url");if(import.meta.url===pathToFileURL(process.argv[1]).href)await main();}
