
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

/* Independent signed-CDF selector realization checks; no optimizer is used. */
function absQ(x){x=Q(x);return x.cmp(0)<0?x.neg():x;}
function assert(c,msg){if(!c)throw Error(msg);}
function ramp(x,a,b){return maxQ(0,minQ(Q(b).s(a),Q(x).s(a)));}
function valueAt(points,t){t=Q(t);let j=bisect(points.map(p=>p[0]),t)-1;if(j<0)return points[0][1];if(j>=points.length-1)return points[points.length-1][1];let[a,x]=points[j],[b,y]=points[j+1];return x.a(y.s(x).m(t.s(a)).dby(b.s(a)));}
function labelLevels(delta){
 const out=[{u:ZERO,side:0,value:ZERO}];
 for(let j=0;j<=8;j++){let u=Q(j).dby(2);if(j)out.push({u,side:-1,value:u.s(delta)});out.push({u,side:1,value:u.a(delta)});}
 return out;
}
function labelIndex(labels,u,side){let k=labels.findIndex(p=>p.u.eq(u)&&p.side===side);assert(k>=0,"missing label");return k;}
function makeRows(V,labels){
 let rows=[{kind:"query",i:0,lo:0,hi:0}];
 for(let i=0;i<V.length-1;i++){
  rows.push({kind:"fill",i,lo:labelIndex(labels,maxQ(V[i],0),1),hi:labelIndex(labels,V[i+1].a(2),-1)});
  rows.push({kind:"query",i:i+1,lo:labelIndex(labels,maxQ(V[i+1],0),1),hi:labelIndex(labels,V[i+1].a(2),-1)});
 }
 for(let j=1;j<rows.length;j++)rows[j].lo=Math.max(rows[j].lo,rows[j-1].lo);
 for(let j=rows.length-2;j>=0;j--)rows[j].hi=Math.min(rows[j].hi,rows[j+1].hi);
 return rows;
}
function realize(V,labels,chosen,eta){
 let q=[],c=[];for(let j=0;j<chosen.length;j++){if(j%2===0)q.push(labels[chosen[j]].value);else c.push(labels[chosen[j]].value);}
 const P=[[V[0],q[0]]],clip=(v,z)=>minQ(v.a(2),maxQ(v,0,z));
 for(let i=0;i<c.length;i++){
  const a=V[i],b=V[i+1],aa=a.a(eta),bb=b.s(eta),cuts=uniq([aa,bb,...[ZERO,c[i],c[i].s(2)].filter(v=>v.cmp(aa)>0&&v.cmp(bb)<0)]);
  for(const v of cuts)P.push([v,clip(v,c[i])]);P.push([b,q[i+1]]);
 }
 let checks=0;for(let j=0;j<P.length;j++){
  let[v,u]=P[j];assert(u.cmp(maxQ(v,0))>=0&&u.cmp(v.a(2))<=0,"physical cone");
  if(j){assert(v.cmp(P[j-1][0])>0,"V order");assert(u.cmp(P[j-1][1])>=0,"P monotonicity");}
  checks++;
 }
 const raw=P.map(([v,u])=>[u.a(v).dby(2),u.s(v).dby(2)]),p=[];
 for(let j=0;j<raw.length-1;j++){
  let[t,x]=raw[j],[s,y]=raw[j+1];
  if(t.cmp(0)<=0&&s.cmp(0)>=0){p.push([ZERO,x.a(y.s(x).m(t.neg()).dby(s.s(t)))]);break;}
 }
 for(const z of raw)if(z[0].cmp(0)>0)p.push(z);
 assert(p.length&&p[0][0].eq(0),"initial trimming");
 for(let j=0;j<p.length;j++){assert(p[j][1].cmp(0)>=0&&p[j][1].cmp(1)<=0,"radial arena");if(j)assert(absQ(p[j][1].s(p[j-1][1])).cmp(p[j][0].s(p[j-1][0]))<=0,"physical speed");checks++;}
 return{P,p,q,c,checks};
}
function indicatorIntegral(P,u,a,b){
 u=Q(u);a=Q(a);b=Q(b);let cuts=uniq([a,b,...P.map(p=>p[0]).filter(v=>v.cmp(a)>0&&v.cmp(b)<0)]),sum=ZERO;
 for(let j=0;j<cuts.length-1;j++){
  const l=cuts[j],r=cuts[j+1],v0=valueAt(P,l).s(u),v1=valueAt(P,r).s(u),d=r.s(l);
  if(v0.cmp(0)>=0&&v1.cmp(0)>=0){if(v0.cmp(0)||v1.cmp(0))sum=sum.a(d);}
  else if(v0.cmp(0)<=0&&v1.cmp(0)<=0){}
  else {const zero=l.s(v0.m(d).dby(v1.s(v0)));sum=sum.a(v0.cmp(0)>0?zero.s(l):r.s(zero));}
 }
 return sum;
}
function physicalIndicatorIntegral(p,u,a,b){
 // Direct physical pair evaluation along the inward characteristic U=u.
 const vs=[Q(a),Q(b)];
 for(const[t]of p){const v=t.m(2).s(u);if(v.cmp(a)>0&&v.cmp(b)<0)vs.push(v);}
 const base=uniq(vs);let sum=ZERO,checks=0;
 for(let j=0;j<base.length-1;j++){
  let l=base[j],r=base[j+1];
  const f=v=>{let time=Q(u).a(v).dby(2),radius=Q(u).s(v).dby(2);return valueAt(p,time).s(radius);};
  let A=f(l),B=f(r),length=r.s(l);
  if(A.cmp(0)>=0&&B.cmp(0)>=0){if(A.cmp(0)||B.cmp(0))sum=sum.a(length);}
  else if(A.cmp(0)<=0&&B.cmp(0)<=0){}
  else{let z=l.s(A.m(length).dby(B.s(A)));sum=sum.a(A.cmp(0)>0?z.s(l):r.s(z));}
  checks++;
 }
 return{sum,checks};
}
function physicalHorizontalIntegral(p,v,a,b){
 const vs=[Q(a),Q(b)];for(const[t]of p){const u=t.m(2).s(v);if(u.cmp(a)>0&&u.cmp(b)<0)vs.push(u);}
 const base=uniq(vs);let sum=ZERO,checks=0;
 for(let j=0;j<base.length-1;j++){
  let l=base[j],r=base[j+1],f=u=>valueAt(p,Q(u).a(v).dby(2)).s(Q(u).s(v).dby(2));
  let A=f(l),B=f(r),length=r.s(l);
  if(A.cmp(0)>=0&&B.cmp(0)>=0){if(A.cmp(0)||B.cmp(0))sum=sum.a(length);}
  else if(A.cmp(0)<=0&&B.cmp(0)<=0){}
  else{let z=l.s(A.m(length).dby(B.s(A)));sum=sum.a(A.cmp(0)>0?z.s(l):r.s(z));}
  checks++;
 }return{sum,checks};
}
function pairCDF(p,x,strict=false){p=Q(p);x=Q(x);let c=0;for(const v of[p,p.neg()])if(v.cmp(x)<0||(!strict&&v.eq(x)))c++;return Q(c).dby(2);}
function pointValue(p,x,a,b){return Q(b).m(pairCDF(p,x,true)).s(Q(a).m(pairCDF(p,x,false)));}
function verify(){
 let contacts=0,physicalQueries=0,rayChecks=0,coneChecks=0,fillChecks=0,horizontalChecks=0,orderedAssignments=0,horizontalPhysical=0;
 for(const x of["-1","-1/2","0","1/2","1"])for(const a of["0","1/3","1","2"])for(const b of["0","1/5","1","3"]){
  let r=absQ(x),exact=pointValue(r,x,a,b);
  if(r.cmp(0)>0){let lo=r.s(Q("1/100"));assert(exact.cmp(pointValue(lo,x,a,b))<=0,"contact below-side obstruction");contacts++;}
  if(r.cmp(1)<0){let hi=r.a(Q("1/100"));assert(exact.cmp(pointValue(hi,x,a,b))<=0,"contact above-side obstruction");contacts++;}
 }
 const V=Array.from({length:7},(_,i)=>Q(i-2).dby(2)),delta=Q("1/128"),eta=delta.m(delta),labels=labelLevels(delta),rows=makeRows(V,labels),U=Array.from({length:9},(_,i)=>Q(i).dby(2));
 let state=1831565813;
 const rand=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n;};
 for(let sample=0;sample<84;sample++){
  let prev=0,chosen=rows.map(row=>{let lo=Math.max(row.lo,prev),k=lo+rand(row.hi-lo+1);prev=k;return k;});
  const r=realize(V,labels,chosen,eta);coneChecks+=r.checks;orderedAssignments++;
  for(let i=0;i<V.length;i++)for(const u of U){
   if(u.cmp(absQ(V[i]))<0||u.cmp(V[i].a(2))>0)continue;
   const t=u.a(V[i]).dby(2),x=u.s(V[i]).dby(2),p=valueAt(r.p,t),above=r.q[i].cmp(u)>0;
   assert(p.cmp(x)!==0,"unintended priced point contact");assert((p.cmp(x)>0)===above,"physical inverse indicator");
   for(const sign of[1,-1]){let xx=x.m(sign),cdf=pairCDF(p,xx);let via=sign>0?ONE.s(Q(above?1:0).dby(2)):Q(above?1:0).dby(2);assert(cdf.eq(via),"fair reflected signed CDF");physicalQueries++;}
  }
  for(let i=0;i<V.length-1;i++){
   const a=V[i],b=V[i+1],cLabel=labels[chosen[2*i+1]],weights=U.map((_,j)=>Q(((sample+3*i+5*j)%9)-4).dby(j+1));let actual=ZERO,ideal=ZERO,abs=ZERO;
   for(let j=0;j<U.length;j++){
    const bit=cLabel.u.cmp(U[j])>0||(cLabel.u.eq(U[j])&&cLabel.side>0);
    actual=actual.a(weights[j].m(indicatorIntegral(r.P,U[j],a,b)));ideal=ideal.a(weights[j].m(bit?b.s(a):ZERO));abs=abs.a(absQ(weights[j]));
    for(const f of["1/4","1/2","3/4"]){let v=a.a(eta).a(b.s(a).s(eta.m(2)).m(Q(f))),got=valueAt(r.P,v).cmp(U[j])>0;assert(got===bit,"clipped fill changed priced threshold");fillChecks++;}
    // Physical segment comparison only on the actual characteristic portion.
    let va=maxQ(a,U[j].neg(),U[j].s(2)),vb=minQ(b,U[j]);
    if(vb.cmp(va)>0){let got=physicalIndicatorIntegral(r.p,U[j],va,vb);assert(got.sum.eq(indicatorIntegral(r.P,U[j],va,vb)),"vertical physical ray");rayChecks+=got.checks;}
   }
   assert(absQ(actual.s(ideal)).cmp(eta.m(2).m(abs))<=0,"vertical bridge error bound");fillChecks++;
  }
  for(let i=0;i<V.length;i++)for(let j=0;j<U.length-1;j++){
   const actual=ramp(r.q[i],U[j],U[j+1]),ideal=ramp(labels[chosen[2*i]].u,U[j],U[j+1]);
   assert(absQ(actual.s(ideal)).cmp(delta)<=0,"horizontal error bound");horizontalChecks++;
   let ua=maxQ(U[j],absQ(V[i])),ub=minQ(U[j+1],V[i].a(2));
   if(ub.cmp(ua)>0){const got=physicalHorizontalIntegral(r.p,V[i],ua,ub);assert(got.sum.eq(ramp(r.q[i],ua,ub)),"horizontal physical ray");horizontalPhysical+=got.checks;}
  }
 }
 return{scope:"Independent exact ingredients for the history-selector physical realization; no optimization or all-field claim is inferred from fixtures.",
 contact_side_inequalities:contacts,ordered_label_assignments:orderedAssignments,physical_cone_and_speed_checks:coneChecks,
 signed_physical_point_checks:physicalQueries,clipped_fill_and_error_checks:fillChecks,horizontal_ramp_error_checks:horizontalChecks,
 independent_physical_vertical_ray_pieces:rayChecks,independent_physical_horizontal_ray_pieces:horizontalPhysical,delta:delta.str(),eta:eta.str()};
}
const api={verify};if(typeof module==="object"&&module.exports)module.exports=api;
if(typeof require==="function"&&require.main===module)console.log(JSON.stringify(verify(),null,2));
return api;
