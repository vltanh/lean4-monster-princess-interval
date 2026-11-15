"use strict";
/* Exact local record moments. This module proves no game-value claim. */
class Rational {
  constructor(n,d=1n) {
    if(n instanceof Rational){this.n=n.n;this.d=n.d;return;}
    if(typeof n==="string"){let p=n.split("/");if(p.length===2){n=BigInt(p[0]);d=BigInt(p[1]);}
      else {let [s,e="0"]=n.toLowerCase().split("e"),sgn=1n;if(s[0]==="-"){sgn=-1n;s=s.slice(1);}else if(s[0]==="+")s=s.slice(1);let [a,b=""]=s.split(".");n=sgn*BigInt(a+b);let k=b.length-Number(e);if(k>=0)d=10n**BigInt(k);else n*=10n**BigInt(-k);}}
    else n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}
    let a=n<0n?-n:n,b=d;while(b){let r=a%b;a=b;b=r;}this.n=n/a;this.d=d/a;
  }
  add(x){x=Q(x);return new Rational(this.n*x.d+x.n*this.d,this.d*x.d);}
  sub(x){x=Q(x);return new Rational(this.n*x.d-x.n*this.d,this.d*x.d);}
  mul(x){x=Q(x);return new Rational(this.n*x.n,this.d*x.d);}
  div(x){x=Q(x);return new Rational(this.n*x.d,this.d*x.n);}
  neg(){return new Rational(-this.n,this.d);}
  cmp(x){x=Q(x);let z=this.n*x.d-x.n*this.d;return z<0n?-1:z>0n?1:0;}
  eq(x){return this.cmp(x)===0;}
  str(){return this.n.toString()+(this.d===1n?"":"/"+this.d);}
}
function Q(x){return x instanceof Rational?x:new Rational(typeof x==="number"?String(x):x);}
const Z=Q(0),O=Q(1),TWO=Q(2);
function sum(xs){return xs.reduce((s,x)=>s.add(x),Z);}
function speed(i,cp,cm){return i%2===0?cp:cm;}
function validate(xs,cp,cm,upper0=0,lower0=0){
  cp=Q(cp);cm=Q(cm);xs=xs.map(Q);upper0=Q(upper0);lower0=Q(lower0);
  if(cp.cmp(0)<=0||cm.cmp(0)<=0||upper0.cmp(0)<0||lower0.cmp(0)<0)throw Error("invalid speeds/band");
  for(let i=0;i<xs.length;i++){let old=i>=2?xs[i-2]:i%2?lower0:upper0;if(xs[i].cmp(old)<0)throw Error("record order");}
  return {xs,cp,cm,upper0,lower0};
}
function directMoment(xs,cp,cm,upper0=0,lower0=0){
  let v=validate(xs,cp,cm,upper0,lower0);({xs,cp,cm,upper0,lower0}=v);
  let time=Z,moment=Z;
  for(let i=0;i<xs.length;i++){
    const c=speed(i,cp,cm),prev=i?xs[i-1]:Z,old=i>=2?xs[i-2]:i%2?lower0:upper0,dx=xs[i].sub(old);
    moment=moment.add(dx.mul(time)).add(xs[i].mul(xs[i]).sub(old.mul(old)).div(2).add(prev.mul(dx)).div(c));
    time=time.add(xs[i].add(prev).div(c));
  }
  return {moment,time};
}
function closedMoment(xs,cp,cm,upper0=0,lower0=0){
  let v=validate(xs,cp,cm,upper0,lower0);({xs,cp,cm,upper0,lower0}=v);
  const n=xs.length;if(n<2)return directMoment(xs,cp,cm,upper0,lower0);
  let xn=xs[n-1],xp=xs[n-2],k=O.div(cp).add(O.div(cm)),S=xn.add(xp).mul(sum(xs.slice(0,n-2))).add(xn.mul(xp));
  for(let i=0;i<n-2;i++)S=S.sub(xs[i].mul(xs[i])).sub(xs[i].mul(xs[i+1]));
  let moment=xn.mul(xn).div(TWO.mul(speed(n-1,cp,cm))).add(xp.mul(xp).div(TWO.mul(speed(n-2,cp,cm)))).add(k.mul(S));
  moment=moment.sub(upper0.mul(upper0).div(TWO.mul(cp))).sub(lower0.mul(lower0).div(TWO.mul(cm))).sub(lower0.mul(k).mul(xs[0]));
  let time=xn.div(speed(n-1,cp,cm)).add(k.mul(sum(xs.slice(0,n-1))));
  return {moment,time};
}
function physicalPath(xs,cp,cm){
  const v=validate(xs,cp,cm);({xs,cp,cm}=v);const beta=cp.add(cm).div(2),alpha=cp.sub(cm).div(2);
  let t=Z,y=Z,out=[{t:Z,x:Z,y:Z}];
  for(let i=0;i<xs.length;i++){let yy=i%2?xs[i].neg():xs[i],dt=yy.sub(y);if(dt.cmp(0)<0)dt=dt.neg();dt=dt.div(speed(i,cp,cm));t=t.add(dt);y=yy;out.push({t,x:y.sub(alpha.mul(t)).div(beta),y});}
  return {alpha,beta,path:out};
}
/* Independent chronological first-segment integration in physical coordinates. */
function physicalMoment(xs,cp,cm,upper0=0,lower0=0){
  const {alpha,beta,path}=physicalPath(xs,cp,cm),a=Q(upper0),b=Q(lower0);
  let cuts=[a,b.neg(),...path.map(p=>p.y)],uniq=new Map(cuts.map(x=>[x.str(),x]));cuts=[...uniq.values()].sort((x,y)=>x.cmp(y));
  let moment=Z,intervals=0,segments=0;
  for(let j=0;j+1<cuts.length;j++){
    const lo=cuts[j],hi=cuts[j+1],mid=lo.add(hi).div(2);if(mid.cmp(b.neg())>=0&&mid.cmp(a)<=0)continue;
    let found=null;
    for(let i=0;i+1<path.length;i++){
      segments++;const p=path[i],r=path[i+1],q0=alpha.mul(p.t).add(beta.mul(p.x)),q1=alpha.mul(r.t).add(beta.mul(r.x));
      if(q0.eq(q1))continue;const low=q0.cmp(q1)<0?q0:q1,high=q0.cmp(q1)<0?q1:q0;
      if(mid.cmp(low)>=0&&mid.cmp(high)<=0){let slope=r.t.sub(p.t).div(q1.sub(q0)),constant=p.t.sub(slope.mul(q0));found=constant.mul(hi.sub(lo)).add(slope.mul(hi.mul(hi).sub(lo.mul(lo))).div(2));break;}
    }
    if(found===null)throw Error("uncaptured rank interval");moment=moment.add(found);intervals++;
  }
  return {moment,intervals,segments};
}
function chainVertices(length,lo,hi){
  lo=Q(lo);hi=Q(hi);let out=[];for(let j=0;j<=length;j++)out.push(Array.from({length},(_,i)=>i<j?lo:hi));return out;
}
function budgetVertices(n,upper,lower,budget,upper0=0,lower0=0){
  if(n<2)throw Error("at least two final records");upper=Q(upper);lower=Q(lower);budget=Q(budget);upper0=Q(upper0);lower0=Q(lower0);
  const m=n-2,odd=Array.from({length:m},(_,i)=>i).filter(i=>i%2===0),even=Array.from({length:m},(_,i)=>i).filter(i=>i%2===1);
  const vp=chainVertices(odd.length,upper0,upper),vm=chainVertices(even.length,lower0,lower);
  function join(p,q){let x=Array(m);odd.forEach((i,j)=>x[i]=p[j]);even.forEach((i,j)=>x[i]=q[j]);x.push((n-2)%2?lower:upper,(n-1)%2?lower:upper);return x;}
  const all=[],keys=new Set();function put(x){let z=sum(x.slice(0,m));if(z.cmp(budget)>0)return;let key=x.map(q=>q.str()).join(",");if(!keys.has(key)){keys.add(key);all.push(x);}}
  function edge(x,y){let sx=sum(x.slice(0,m)),sy=sum(y.slice(0,m));if(sx.eq(sy))return;if((sx.cmp(budget)<0&&sy.cmp(budget)>0)||(sy.cmp(budget)<0&&sx.cmp(budget)>0)){let f=budget.sub(sx).div(sy.sub(sx));put(x.map((v,i)=>v.add(y[i].sub(v).mul(f))));}}
  for(let p of vp)for(let q of vm)put(join(p,q));
  for(let q of vm)for(let i=0;i<vp.length;i++)for(let j=i+1;j<vp.length;j++)edge(join(vp[i],q),join(vp[j],q));
  for(let p of vp)for(let i=0;i<vm.length;i++)for(let j=i+1;j<vm.length;j++)edge(join(p,vm[i]),join(p,vm[j]));
  return all;
}
function productiveCount(xs,upper0=0,lower0=0){let old=[Q(upper0),Q(lower0)],n=0;xs.map(Q).forEach((x,i)=>{if(x.cmp(old[i%2])>0){n++;old[i%2]=x;}});return n;}
function reducedRecordPath(xs,upper0=0,lower0=0){
  let old=[Q(upper0),Q(lower0)],out=[];xs.map(Q).forEach((x,i)=>{if(x.cmp(old[i%2])>0){out.push({sign:i%2?-1:1,rank:x});old[i%2]=x;}});return out;
}
module.exports={Rational,Q,directMoment,closedMoment,physicalPath,physicalMoment,budgetVertices,productiveCount,reducedRecordPath};
