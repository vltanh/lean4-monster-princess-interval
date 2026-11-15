/* Exact record-Bellman region audit, V8/CommonJS.
 * The supplied JSON contains affine Farkas identities, not a game bound.
 * Run: node verify_record_bellman_regions.cjs FIELD_JSON CERTIFICATE_JSON [--universe]
 * In a V8 tool isolate: const verifier=Function("return ("+source+")")();
 * verifier.verifyRegions(fieldData, certificate);
 * verifier.classifyPostGate(fieldData, certificate.complete_post_turn_sufficient_gate_classification);
 */
(function(){
const API=(function(){

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
return {Rat,Q,ZERO,ONE,minQ,maxQ,uniq,bisect,ExactField};

})();
const makeRegionProver=(function(){

function makeRegionProver(f,X){
 const {Q,ZERO,ONE}=X, zer=()=>Array.from({length:5},()=>ZERO);
 const cn=x=>{let a=zer();a[0]=Q(x);return a;};
 const variable=k=>{let a=zer();a[k+1]=ONE;return a;};
 const [U,V,w,s]=[0,1,2,3].map(variable);
 const add=(...fs)=>fs.reduce((a,b)=>a.map((q,i)=>q.a(b[i])),zer());
 const scale=(a,k)=>a.map(q=>q.m(k));
 const sub=(a,b)=>add(a,scale(b,-1));
 const ev=(a,p)=>a.slice(1).reduce((z,q,i)=>z.a(q.m(p[i])),a[0]);
 const cf=id=>f.triangles[id].cf;
 const field=(id,x,y)=>{const [a,b,c]=cf(id);return add(scale(x,a),scale(y,b),cn(c));};
 function solve(A,b,exact=false){
  const n=b.length,m=A.map((r,i)=>[...r,b[i]]);
  for(let k=0;k<n;k++){
   let p=k;
   if(exact){while(p<n&&m[p][k].eq(0))p++;if(p===n)return null;}
   else {for(let j=k+1;j<n;j++)if(Math.abs(m[j][k])>Math.abs(m[p][k]))p=j;if(Math.abs(m[p][k])<1e-13)return null;}
   [m[k],m[p]]=[m[p],m[k]];const div=m[k][k];
   for(let j=k;j<=n;j++)m[k][j]=exact?m[k][j].dby(div):m[k][j]/div;
   for(let i=0;i<n;i++)if(i!==k){const z=m[i][k];for(let j=k;j<=n;j++)m[i][j]=exact?m[i][j].s(z.m(m[k][j])):m[i][j]-z*m[k][j];}
  }
  return m.map(r=>r[n]);
 }
 function coord(x){const candidates=[...f.grid[0],...f.grid[1]];const q=candidates.find(q=>Math.abs(q.num()-x)<1e-14);return q||Q(String(x));}
 function prepare(ids,withDomain=true){
  const [ci,fi,ai,bi]=ids, M=field(ci,U,V),ell=field(fi,U,w),ca=cf(ai),cb=cf(bi);
  if(ca[1].cmp(0)>=0||cb[0].cmp(0)<=0)return null;
  const za=scale(sub(sub(ell,scale(s,ca[0])),cn(ca[2])),ONE.dby(ca[1]));
  const ub=scale(sub(sub(M,scale(w,cb[1])),cn(cb[2])),ONE.dby(cb[0]));
  const G=sub(scale(sub(add(s,za),add(U,w)),cf(fi)[0].dby(2)),scale(sub(add(ub,w),add(U,V)),cf(ci)[0].dby(2)));
  let constraints=[];
  function tri(id,x,y,label){const t=f.triangles[id],sg=t.positive?ONE:Q(-1);
   for(let j=0;j<3;j++){const a=t.ps[j],b=t.ps[(j+1)%3],du=b[0].s(a[0]),dv=b[1].s(a[1]);
    constraints.push({label:label+"_edge"+j,f:scale(sub(scale(sub(y,cn(a[1])),du),scale(sub(x,cn(a[0])),dv)),sg)});
   }
  }
  tri(ci,U,V,"current");tri(fi,U,w,"first");tri(ai,s,za,"alpha");tri(bi,ub,w,"beta");
  if(withDomain)for(const[label,form]of[
   ["U_ge_a0",sub(U,cn("255/256"))],["U_le_1",sub(cn(1),U)],["initial_domain",add(U,V)],
   ["inward_order",sub(w,V)],["positive_first_turn",sub(U,w)],["second_order",sub(s,U)],
   ["second_below_endpoint",sub(add(cn(2),w),s)],["high_rank",sub(M,cn(f.initialValue(Q("255/256"))))],
   ["rank_order",sub(M,ell)],["useful_second_turn",sub(s,ub)]
  ])constraints.push({label,f:form});
  const unique=new Map();
  for(const row of constraints){const v=row.f.find(q=>!q.eq(0));if(!v)continue;const abs=v.cmp(0)<0?v.neg():v;
   const key=row.f.map(q=>q.dby(abs).str()).join(",");if(!unique.has(key))unique.set(key,row);
  }
  return {ids,G,constraints:[...unique.values()],M,ell,za,ub};
 }
 function prove(seed,withDomain=true){
  const reg=prepare(seed.ids,withDomain);if(!reg)return {status:"unsupported_inverse",ids:seed.ids};
  const {G,constraints}=reg;
  const center=[seed.witness.U,seed.witness.V,seed.witness.w,seed.witness.s].map(coord);
  const scopes=[[seed.ids[0],0],[seed.ids[0],1],[seed.ids[1],1],[seed.ids[2],0]];
  const scales=scopes.map(([id,axis])=>{const a=f.triangles[id].ps.map(p=>p[axis]).sort((x,y)=>x.cmp(y));const width=a[2].s(a[0]);return width.eq(0)?Q("1/262144"):width;});
  const trans=a=>({b:ev(a,center).num(),a:a.slice(1).map((q,i)=>q.m(scales[i]).num())});
  const g=trans(G), rows=constraints.map(r=>{const t=trans(r.f),n=Math.max(...t.a.map(Math.abs),Math.abs(t.b),1e-100);return{b:t.b/n,a:t.a.map(q=>q/n)};});
  let best=[];
  for(let a=0;a<rows.length;a++)for(let b=a+1;b<rows.length;b++)for(let c=b+1;c<rows.length;c++)for(let d=c+1;d<rows.length;d++){
   const inds=[a,b,c,d],lam=solve([0,1,2,3].map(k=>inds.map(i=>rows[i].a[k])),g.a);
   if(!lam||lam.some(q=>q < -1e-10))continue;
   const bound=g.b-lam.reduce((z,q,k)=>z+q*rows[inds[k]].b,0);
   best.push({inds,bound});
  }
  best.sort((a,b)=>b.bound-a.bound);
  let exactBest=null;
  for(const candidate of best.slice(0,80)){
   const inds=candidate.inds,lambda=solve([0,1,2,3].map(k=>inds.map(i=>constraints[i].f[k+1])),G.slice(1),true);
   if(!lambda||lambda.some(q=>q.cmp(0)<0))continue;
   const bound=lambda.reduce((z,q,k)=>z.s(q.m(constraints[inds[k]].f[0])),G[0]);
   const lhs=add(cn(bound),...lambda.map((q,k)=>scale(constraints[inds[k]].f,q)));
   if(lhs.some((q,k)=>!q.eq(G[k])))throw Error("dual identity");
   exactBest={ids:seed.ids,domain:withDomain?"triangle_and_physical":"triangle_only",
    lower_bound:bound.str(),lower_bound_float:bound.num(),
    dual:inds.map((i,k)=>({constraint:constraints[i].label,multiplier:lambda[k].str()})),
    witness:center.map(q=>q.str()),witness_G:ev(G,center).str(),
    witness_inside:constraints.every(r=>ev(r.f,center).cmp(0)>=0),
    status:bound.cmp(0)>=0?"PASS":"NEGATIVE_DUAL_BOUND"};
   if(bound.cmp(0)>=0)return exactBest;
  }
  return exactBest||{status:"NO_EXACT_DUAL",ids:seed.ids,float_bound:best[0]?.bound};
 }
 return {prove,prepare,ev,solve};
}
return makeRegionProver;

})();
const polygonTools=(function(){

function polygonTools(X){
 const {Q,ZERO,ONE,minQ,maxQ,uniq}=X;
 const ev=(f,p)=>f[0].a(f[1].m(p[0])).a(f[2].m(p[1]));
 const same=(a,b)=>a[0].eq(b[0])&&a[1].eq(b[1]);
 function clean(ps){const ans=[];for(const p of ps)if(!ans.length||!same(p,ans[ans.length-1]))ans.push(p);if(ans.length>1&&same(ans[0],ans[ans.length-1]))ans.pop();return ans;}
 function clip(ps,form){if(ps.length===0)return[];if(ps.length===1)return ev(form,ps[0]).cmp(0)>=0?ps:[];
  const ans=[];
  for(let i=0;i<ps.length;i++){
   const a=ps[i],b=ps[(i+1)%ps.length],fa=ev(form,a),fb=ev(form,b);
   if(fa.cmp(0)>=0)ans.push(a);
   if(fa.cmp(0)*fb.cmp(0)<0){const t=fa.dby(fa.s(fb));ans.push(a.map((q,k)=>q.a(b[k].s(q).m(t))));}
  }
  return clean(ans);
 }
 function area(ps){if(ps.length<3)return ZERO;return ps.reduce((z,p,i)=>z.a(p[0].m(ps[(i+1)%ps.length][1]).s(p[1].m(ps[(i+1)%ps.length][0]))),ZERO);}
 function bounds(ps){return{umin:minQ(...ps.map(p=>p[0])),umax:maxQ(...ps.map(p=>p[0])),zmin:minQ(...ps.map(p=>p[1])),zmax:maxQ(...ps.map(p=>p[1]))};}
 function slice(ps,u){
  const vals=[];
  if(ps.length===1)return ps[0][0].eq(u)?[ps[0][1],ps[0][1]]:null;
  for(let i=0;i<ps.length;i++){
   const a=ps[i],b=ps[(i+1)%ps.length];
   if(a[0].eq(b[0])){if(a[0].eq(u))vals.push(a[1],b[1]);}
   else if(minQ(a[0],b[0]).cmp(u)<=0&&maxQ(a[0],b[0]).cmp(u)>=0)
    vals.push(a[1].a(u.s(a[0]).m(b[1].s(a[1])).dby(b[0].s(a[0]))));
  }
  return vals.length?[minQ(...vals),maxQ(...vals)]:null;
 }
 function affineFromEnds(u0,z0,u1,z1){const slope=z1.s(z0).dby(u1.s(u0));return[z0.s(slope.m(u0)),slope];}
 function fiberVertices(v,w){
  if(!v||!w||v[0].cmp(w[1])>0)return [];
  let ps=[[v[0],w[0]],[v[1],w[0]],[v[1],w[1]],[v[0],w[1]]];
  // Here the first coordinate is V, the second w.
  return clip(ps,[ZERO,Q(-1),ONE]);
 }
 function regionMin(cur,first,G,extraForm=null){
  const cb=bounds(cur),fb=bounds(first),lo=maxQ(cb.umin,fb.umin),hi=minQ(cb.umax,fb.umax);
  if(lo.cmp(hi)>0||cb.zmin.cmp(fb.zmax)>0)return null;
  let knots=uniq([lo,hi,...cur.map(p=>p[0]),...first.map(p=>p[0])].filter(q=>q.cmp(lo)>=0&&q.cmp(hi)<=0));
  let extra=[];
  for(let i=0;i<knots.length-1;i++){
   const a=knots[i],b=knots[i+1],va=slice(cur,a),vb=slice(cur,b),wa=slice(first,a),wb=slice(first,b);
   if(!va||!vb||!wa||!wb)continue;
   const lines=[affineFromEnds(a,va[0],b,vb[0]),affineFromEnds(a,va[1],b,vb[1]),affineFromEnds(a,wa[0],b,wb[0]),affineFromEnds(a,wa[1],b,wb[1])];
   for(let j=0;j<4;j++)for(let k=j+1;k<4;k++)if(!lines[j][1].eq(lines[k][1])){
    const x=lines[k][0].s(lines[j][0]).dby(lines[j][1].s(lines[k][1]));
    if(x.cmp(a)>0&&x.cmp(b)<0)extra.push(x);
   }
  }
  knots=uniq([...knots,...extra]);
  let best=null,vertices=0,extraMax=null;
  for(const u of knots){
   const poly=fiberVertices(slice(cur,u),slice(first,u));
   for(const [v,w]of poly){const val=G[0].a(G[1].m(u)).a(G[2].m(v)).a(G[3].m(w));vertices++;if(extraForm){const e=extraForm[0].a(extraForm[1].m(u)).a(extraForm[2].m(v)).a(extraForm[3].m(w));if(extraMax===null||e.cmp(extraMax)>0)extraMax=e;}if(!best||val.cmp(best.value)<0)best={point:[u,v,w],value:val};}
  }
  return best?{...best,vertices,knots:knots.length,extraMax}:null;
 }
 return{clip,clean,area,bounds,slice,regionMin,ev};
}
return polygonTools;

})();

function exactGeometry(f,X){
 const {Q,ZERO,ONE,minQ,maxQ,uniq,bisect}=X, cache=new Map();
 const cross=(a,b)=>a[0].m(b[1]).s(a[1].m(b[0]));
 const sub=(a,b)=>[a[0].s(b[0]),a[1].s(b[1])];
 function inside(id,point,dir=null){
  const t=f.triangles[id],sg=t.positive?ONE:Q(-1);
  for(let k=0;k<3;k++){
   const e=sub(t.ps[(k+1)%3],t.ps[k]),g=cross(e,sub(point,t.ps[k])).m(sg);
   if(g.cmp(0)<0)return false;
   if(dir&&g.eq(0)&&cross(e,dir).m(sg).cmp(0)<0)return false;
  }
  return true;
 }
 function directional(point,dir){
  const cell=point.map((p,k)=>Math.max(0,Math.min(f.grid[k].length-2,bisect(f.grid[k],p)-1))),poss=new Set();
  for(const i of[cell[0],cell[0]-1])for(const j of[cell[1],cell[1]-1])for(const n of f.cells.get(i+","+j)||[])poss.add(n);
  return [...poss].sort((a,b)=>a-b).filter(n=>inside(n,point,dir));
 }
 function line(axis,fixed){
  const key=axis+","+fixed.str();if(cache.has(key))return cache.get(key);
  const lo=axis===0?maxQ(fixed.neg(),fixed.s(2)):(fixed.cmp(0)<0?fixed.neg():fixed),hi=axis===0?minQ(fixed,1):fixed.a(2);
  const index=Math.max(0,Math.min(f.grid[axis].length-2,bisect(f.grid[axis],fixed)-1)),other=1-axis;
  const poss=new Set([...(f.strips[axis].get(index)||[]),...(f.strips[axis].get(index-1)||[])]);
  let cuts=[lo,hi];
  for(const n of poss){const ps=f.triangles[n].ps;for(let j=0;j<3;j++){
   const a=ps[j],b=ps[(j+1)%3];
   if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(const p of[a,b])if(p[other].cmp(lo)>0&&p[other].cmp(hi)<0)cuts.push(p[other]);}
   else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&maxQ(a[axis],b[axis]).cmp(fixed)>=0){
    const z=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));
    if(z.cmp(lo)>0&&z.cmp(hi)<0)cuts.push(z);
   }
  }}
  const ps=uniq(cuts).map(z=>[z,axis===0?f.radial(fixed,z):f.radial(z,fixed)]);
  cache.set(key,ps);return ps;
 }
 function alphaCoordinate(U,q){
  const ps=line(0,U);
  for(let j=0;j<ps.length-1;j++){
   const [a,ra]=ps[j],[b,rb]=ps[j+1];
   if(ra.cmp(q)<=0)return a;
   if(rb.cmp(q)<=0)return a.a(b.s(a).m(ra.s(q)).dby(ra.s(rb)));
  }
  return U;
 }
 function betaCoordinate(V,q){
  const ps=line(1,V);
  if(q.cmp(ps[0][1])<0)return ps[0][0];
  for(let j=0;j<ps.length-1;j++){
   const [a,ra]=ps[j],[b,rb]=ps[j+1];
   if(q.cmp(rb)<0)return a.a(b.s(a).m(q.s(ra)).dby(rb.s(ra)));
  }
  return V.a(2);
 }
 return {inside,directional,line,alphaCoordinate,betaCoordinate};
}


function verifyRegions(data,certificate){
 const f=new API.ExactField(data),{Q,ZERO,ONE}=API;
 if(data.nodes.length!==3571||data.triangles.length!==6936)throw Error("wrong field dimensions");
 const P=makeRegionProver(f,API),geo=exactGeometry(f,API);
 let minimum=null;
 for(const r of certificate.regions){
  const reg=P.prepare(r.ids,r.domain==="triangle_and_physical"),bound=Q(r.lower_bound);
  if(bound.cmp(0)<0)throw Error("negative declared lower bound");
  let sum=Array.from({length:5},()=>ZERO);sum[0]=bound;
  for(const term of r.dual){
   const row=reg.constraints.find(q=>q.label===term.constraint),lambda=Q(term.multiplier);
   if(!row||lambda.cmp(0)<0)throw Error("bad dual term");
   sum=sum.map((q,k)=>q.a(lambda.m(row.f[k])));
  }
  if(sum.some((q,k)=>!q.eq(reg.G[k])))throw Error("Farkas identity failed");
  const witness=r.witness.map(Q);
  if(!reg.constraints.every(c=>P.ev(c.f,witness).cmp(0)>=0))throw Error("witness outside region");
  if(!P.ev(reg.G,witness).eq(Q(r.witness_G)))throw Error("witness G mismatch");
  const [u,v,w,s]=witness;
  if(!geo.inside(r.ids[0],[u,v],[ONE,ZERO])||!geo.inside(r.ids[1],[u,w],[ONE,ZERO]))throw Error("wrong incoming derivative trace");
  const ell=P.ev(reg.ell,witness),m=P.ev(reg.M,witness);
  const za=P.ev(reg.za,witness),ub=P.ev(reg.ub,witness);
  if(!geo.alphaCoordinate(s,ell).eq(za)||!geo.betaCoordinate(w,m).eq(ub))throw Error("inverse witness trace mismatch");
  if(minimum===null||bound.cmp(minimum)<0)minimum=bound;
 }
 const alphaIds=[...new Set(certificate.regions.map(r=>r.ids[2]))],betaIds=[...new Set(certificate.regions.map(r=>r.ids[3]))];
 const trace=[];
 for(const [kind,ids,dir,axis,sign]of[["alpha",alphaIds,[ZERO,Q(-1)],1,-1],["beta",betaIds,[ONE,ZERO],0,1]]){
  for(const id of ids){
   const t=f.triangles[id],points=[...t.ps,...t.ps.map((p,j)=>p.map((q,k)=>q.a(t.ps[(j+1)%3][k]).dby(2)))];
   for(let k=0;k<points.length;k++){
    const point=points[k],neighbors=geo.directional(point,dir),endpoint=point[0].s(point[1]).eq(2),initial=point[0].a(point[1]).eq(0);
    const okay=neighbors.some(n=>f.triangles[n].cf[axis].m(sign).cmp(0)>0)||endpoint||(kind==="alpha"&&initial);
    trace.push({kind,id,face:k,status:okay?"continuous_right_rank_limit":"JUMP_FACE"});
   }
  }
 }
 const jumps=trace.filter(r=>r.status==="JUMP_FACE");
 if(certificate.expected.regions!==certificate.regions.length||certificate.expected.inverse_face_checks!==trace.length||certificate.expected.inverse_jump_faces!==jumps.length)throw Error("coverage metadata mismatch");
 return {status:"PASS",scope:certificate.scope,regions:certificate.regions.length,
   exact_farkas_identities:certificate.regions.length,exact_physical_inverse_witnesses:2*certificate.regions.length,
   inverse_face_checks:trace.length,inverse_jump_faces:jumps.length,
   minimum_affine_lower_bound:minimum.str(),minimum_affine_lower_bound_float:minimum.num(),
   unresolved_jump_faces:jumps,
   global_bellman_gate_proved:false};
}


function classifyPostGate(data,expected=null){
 const f=new API.ExactField(data),{Q,ZERO,ONE,minQ,maxQ}=API;
 const P=polygonTools(API),a0=Q("255/256"),cut=f.initialValue(a0);
 const incoming=[];
 for(let id=0;id<f.triangles.length;id++){
  const t=f.triangles[id];
  if(minQ(...t.ps.map(p=>p[0])).cmp(1)>=0||maxQ(...t.ps.map(p=>p[0])).cmp(a0)<=0)continue;
  const poly=P.clip(P.clip(t.ps,[a0.neg(),ONE,ZERO]),[ONE,Q(-1),ZERO]);
  if(poly.length)incoming.push({id,poly,cf:t.cf});
 }
 const current=[];
 for(const t of incoming){
  const poly=P.clip(t.poly,[t.cf[2].s(cut),t.cf[0],t.cf[1]]);
  if(poly.length)current.push({...t,poly});
 }
 const row=f.nodes.map((p,i)=>({p,val:f.values[i]})).filter(t=>t.p[0].eq(1)).sort((a,b)=>a.p[1].cmp(b.p[1]));
 const pieces=[];
 for(let i=0;i<row.length-1;i++){
  const a=row[i],b=row[i+1];if(a.val.eq(b.val))continue;
  const slope=b.val.s(a.val).dby(b.p[1].s(a.p[1])),intercept=a.val.s(slope.m(a.p[1]));
  pieces.push({index:i,lo:b.val,hi:a.val,slope,intercept});
 }
 const first=[];
 for(const t of incoming){
  if(t.cf[0].eq(0)){first.push({...t,piece:null});continue;}
  const vals=t.poly.map(p=>t.cf[0].m(p[0]).a(t.cf[1].m(p[1])).a(t.cf[2])),mn=minQ(...vals),mx=maxQ(...vals);
  for(const piece of pieces){
   if(mx.cmp(piece.lo)<0||mn.cmp(piece.hi)>0)continue;
   let poly=P.clip(t.poly,[t.cf[2].s(piece.lo),t.cf[0],t.cf[1]]);
   poly=P.clip(poly,[piece.hi.s(t.cf[2]),t.cf[0].neg(),t.cf[1].neg()]);
   if(poly.length)first.push({...t,poly,piece});
  }
 }
 for(const o of [...current,...first]){
  o.bounds=P.bounds(o.poly);o.nb=Object.fromEntries(Object.entries(o.bounds).map(([k,q])=>[k,q.num()]));
  const vals=o.poly.map(p=>o.cf[0].m(p[0]).a(o.cf[1].m(p[1])).a(o.cf[2]));
  o.rankMin=minQ(...vals);o.rankMax=maxQ(...vals);
 }
 let feasible=0,pass=0,needs=0,degenerate=0,checked=0,examples=[];
 for(const cur of current){
  const a=cur.cf[0],nb=cur.nb;
  for(const one of first){
   const fb=one.nb;
   // Disjointness and rank pruning are exact rational comparisons.
   if(cur.bounds.umin.cmp(one.bounds.umax)>0||one.bounds.umin.cmp(cur.bounds.umax)>0||cur.bounds.zmin.cmp(one.bounds.zmax)>0||one.rankMin.cmp(cur.rankMax)>0)continue;
   checked++;
   const [a1,b1,c1]=one.cf;let G;
   if(!one.piece)G=[a.neg(),a.dby(2),a.dby(2),a.neg()];
   else{
    const {slope,intercept}=one.piece;
    G=[a1.m(ONE.a(c1.s(intercept).dby(slope))).dby(2).s(a),
       a1.m(a1.dby(slope).s(1)).dby(2).a(a.dby(2)),
       a.dby(2),a1.m(b1.dby(slope).s(1)).dby(2).s(a)];
   }
   const gap=[cur.cf[2].s(c1),a.s(a1),cur.cf[1],b1.neg()];
   const result=P.regionMin(cur.poly,one.poly,G,gap);
   if(!result)continue;
   if(result.extraMax.cmp(0)<0)throw Error("transport rank order");
   if(result.extraMax.eq(0)){degenerate++;continue;}
   feasible++;
   if(result.value.cmp(0)>=0)pass++;
   else{
    needs++;
    if(examples.length<3)examples.push({current:cur.id,first:one.id,alpha1_piece:one.piece?.index??null,minimum:result.value.str(),point:result.point.map(q=>q.str())});
   }
  }
 }
 const result={scope:"Complete closed affine cover for the stronger sufficient s>=1 gate; failures are not attacks.",
  current_triangles:current.length,first_triangles:incoming.length,alpha1_rank_pieces:pieces.length,
  first_rank_variants:first.length,checked_pairs:checked,
  feasible_nondegenerate_closed_cells:feasible,proved_nonnegative_cells:pass,needs_comparator_cells:needs,
  identically_zero_lower_rank_gap_cells:degenerate,negative_gate_examples:examples,
  s_below_one:"not covered",global_bellman_gate_proved:false};
 if(expected)for(const k of["current_triangles","first_triangles","alpha1_rank_pieces","feasible_nondegenerate_closed_cells","proved_nonnegative_cells","needs_comparator_cells","identically_zero_lower_rank_gap_cells"])
  if(result[k]!==expected[k])throw Error("post-universe mismatch "+k);
 return result;
}

const exported={verifyRegions,classifyPostGate};
if(typeof module==="object"&&module.exports){
 module.exports=exported;
 if(typeof require==="function"&&require.main===module){
  const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
  const fieldPath=process.argv[2]||path.join(__dirname,"snapshots/endpoint_joint_i1_field.json");
  const certPath=process.argv[3]||path.join(__dirname,"snapshots/record_bellman_regions.json");
  const raw=fs.readFileSync(fieldPath),certificate=JSON.parse(fs.readFileSync(certPath,"utf8"));
  const hash=crypto.createHash("sha1").update(Buffer.from("blob "+raw.length+"\0")).update(raw).digest("hex");
  if(hash!==certificate.source.blob_sha)throw Error("source blob hash mismatch");
  const data=JSON.parse(raw.toString("utf8")),result={regions:verifyRegions(data,certificate)};
  if(process.argv.includes("--universe"))result.post_turn_cover=classifyPostGate(data,certificate.complete_post_turn_sufficient_gate_classification);
  console.log(JSON.stringify(result,null,2));
 }
}
return exported;
})()
