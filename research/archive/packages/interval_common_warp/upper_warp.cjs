"use strict";
// Exact interval coefficients for common odd, two-periodic light-coordinate warps.
module.exports=(function(E,P){

const {Q}=E.Physical,zero=new Q(0n),one=new Q(1n),two=new Q(2n);
function floor(q){let z=q.n/q.d;if(q.n<0n&&q.n%q.d)z--;return z;}
function fold(q){q=new Q(q);const n=floor(q.div(two)),r=q.sub(new Q(2n*n));return r.cmp(one)<=0?{radius:r,sign:1,constant:Number(2n*n)}:{radius:two.sub(r),sign:-1,constant:Number(2n*n+2n)};}
function gcd(a,b){while(b){const c=a%b;a=b;b=c;}return a;}
function build(cert){
 const m=new E.Rational.Model(cert.atoms),den=BigInt(cert.weight_denominator),map=new Map([["0",zero],["1",one]]);
 for(const q of m.vQ.concat(m.baseQ)){const r=fold(q).radius;map.set(String(r),r);}
 const knots=Array.from(map.values()).sort((a,b)=>a.cmp(b)),ki=new Map(knots.map((q,i)=>[String(q),i]));
 m.defMap=new Map(m.defs.map((d,i)=>[(d.pos?"+":"-")+d.bits.join(","),i]));
 const ranges=new Map();let rawIntervals=0;
 function add(pos,bits,low,high,weight){
  if(high.cmp(low)<=0)return;const b=m.norm(pos,bits);if(b===null)return;
  const id=m.defMap.get((pos?"+":"-")+b.join(","));if(id===undefined)throw Error("reward structure changed");
  rawIntervals++;
  while(low.cmp(high)<0){
   const cut=new Q(floor(low)+1n),end=cut.cmp(high)<0?cut:high;
   const a=ki.get(String(fold(low).radius)),z=ki.get(String(fold(end).radius));
   if(a===undefined||z===undefined||a===z)throw Error("missing warp knot");
   const lo=Math.min(a,z),hi=Math.max(a,z),key=id+":"+lo+":"+hi;
   ranges.set(key,(ranges.get(key)||0n)+weight);low=end;
  }
 }
 for(let j=0;j<cert.atoms.length;j++){
  const w=BigInt(cert.atoms[j].weight_numerator);
  for(const route of m.routes[j]){
   let[u0,v0]=route[0],above=[[m.query.get(String(v0)),m.gt(u0)]],below=[[m.query.get(String(v0)),m.ge(u0)]];
   for(let k=1;k<route.length;k++){
    const[u1,v1]=route[k];
    if(u1.cmp(u0)>0){
     const idx=m.query.get(String(v0));let old=u0;
     if(m.baseQ[0].cmp(u0)>0){const end=m.baseQ[0].cmp(u1)<0?m.baseQ[0]:u1;add(true,above,u0,end,w);old=end;}
     for(let l=1;l<m.baseQ.length;l++){
      const end=m.baseQ[l].cmp(u1)<0?m.baseQ[l]:u1;
      if(end.cmp(old)>0){add(true,above.concat([[idx,3*l]]),old,end,w);old=end;}
     }
     add(false,below,u0,u1,w);
    }else{
     add(true,above,v0,v1,w);
     const left=m.query.get(String(v0)),right=m.query.get(String(v1)),th=m.ge(u0);
     for(let i=left;i<right;i++){const end=m.vQ[i+1].cmp(u0)<0?m.vQ[i+1]:u0;add(false,below.concat([[i,th]]),m.vQ[i],end,w);}
    }
    above.push([m.query.get(String(v1)),m.gt(u1)]);below.push([m.query.get(String(v1)),m.ge(u1)]);u0=u1;v0=v1;
   }
  }
 }
 let scale=1n;for(const q of knots)scale=scale/gcd(scale,q.d)*q.d;
 const expected=new Array(m.defs.length).fill(0n),actual=new Array(m.defs.length).fill(0n);
 for(let j=0;j<cert.atoms.length;j++){m.compile(j);const w=BigInt(cert.atoms[j].weight_numerator);for(const[id,c]of m.lastExactUnits){if(scale%c.d)throw Error("nonintegral coefficient scale");expected[id]+=w*c.n*(scale/c.d);}}
 const intervals=[];
 for(const[key,w]of ranges){const[id,lo,hi]=key.split(":").map(Number),length=knots[hi].sub(knots[lo]);actual[id]+=w*length.n*(scale/length.d);const num=Number(w);if(!Number.isSafeInteger(num))throw Error("weight range not safely represented");intervals.push([id,lo,hi,num]);}
 for(let i=0;i<actual.length;i++)if(actual[i]!==expected[i])throw Error("identity reward mismatch at "+i);
 const projection=P.project(m);delete projection.units;
 const full={v:m.v,base:m.base,bounds:m.bounds,offset:m.offset,N:m.N};
 return{scope:"Fixed probability law; common odd, 2-periodic monotone light-coordinate warp. All branch orders are retained.",
  atoms:cert.atoms,denominator:String(den),knots:knots.map(String),full,projection,intervals,
  audit:{reward_definitions:actual.length,raw_intervals:rawIntervals,aggregated_intervals:intervals.length,exact_identity_reward_checks:actual.length,threshold_nodes:m.N,projected_threshold_nodes:projection.N}};
}
function identity(data){const q=data.knots.map(x=>new Q(x));return q.slice(1).map((x,i)=>x.sub(q[i]).number());}
function restore(data){return E.Rational.restore(data.full,data.atoms);}
function capturePoint(m,route,labels){
 let[u,v]=route[0],p=labels[m.query.get(String(v))],ge=m.ge(u),gt=m.gt(u);
 if(p>=ge&&p<gt)return[u,v];const above=p>=gt;
 for(let k=1;k<route.length;k++){const[a,b]=route[k];
  if(a.cmp(u)>0&&above){p=labels[m.query.get(String(v))];if(p<m.gt(a))return[m.b(p),v];}
  else if(b.cmp(v)>0&&!above){const at=E.Cut.lower(labels,m.ge(u)),q=m.vQ[at],cross=u.cmp(q)<=0?u:q;if(cross.cmp(b)<=0)return[u,cross];}
  u=a;v=b;
 }throw Error("no capture point");
}
function features(data,labels){
 const m=restore(data),K=data.knots.length-1,index=new Map(data.knots.map((q,i)=>[q,i])),diff=new Array(K+1).fill(0);
 let constant=0;
 for(let j=0;j<data.atoms.length;j++){
  const w=Number(data.atoms[j].weight_numerator);
  for(const route of m.routes[j])for(const q of capturePoint(m,route,labels)){
   const f=fold(q),k=index.get(String(f.radius));if(k===undefined)throw Error("capture outside knots");
   constant+=w*f.constant;diff[0]+=w*f.sign;diff[k]-=w*f.sign;
  }
 }
 let running=constant;const numerators=[];
 for(let k=0;k<K;k++){running+=diff[k];if(!Number.isSafeInteger(running))throw Error("capture numerator not exact");numerators.push(running);}
 const divisor=4*Number(data.denominator);
 return{numerators,denominator:String(4n*BigInt(data.denominator)),values:numerators.map(x=>x/divisor)};
}
function rewardWeights(data,d){
 if(d.some(x=>x<0)||Math.abs(d.reduce((a,b)=>a+b,0)-1)>1e-9)throw Error("warp increments must be nonnegative and sum to one");
 const cum=[0];for(const x of d)cum.push(cum.at(-1)+x);
 const rw=new Float64Array(data.projection.defs.length),den=Number(data.denominator);
 for(const[id,lo,hi,n]of data.intervals)rw[id]+=(cum[hi]-cum[lo])*n/den;
 return rw;
}
function solve(data,d,tol=2e-13){
 const p=data.projection,rw=rewardWeights(data,d),lin=new Array(p.N).fill(0),hard=[];let constant=0;
 for(let i=0;i<rw.length;i++){
  const w=rw[i];if(!w)continue;const r=p.defs[i];if(!r.bits.length){constant+=w;continue;}
  if(r.bits.length===1){lin[r.bits[0]]+=r.pos?w:-w;if(!r.pos)constant+=w;}
  else{const a=lin.length;lin.push(r.pos?w:-w);if(!r.pos)constant+=w;for(const b of r.bits)hard.push(r.pos?[a,b]:[b,a]);}
 }
 const s=lin.length,t=s+1,g=new E.Cut.Flow(t+1,tol),inf=1+lin.reduce((a,b)=>a+Math.abs(b),0);let ceiling=constant;
 for(let i=0;i<lin.length;i++)if(lin[i]>0){g.add(s,i,lin[i]);ceiling+=lin[i];}else if(lin[i]<0)g.add(i,t,-lin[i]);
 for(const[a,b]of hard)g.add(a,b,inf);for(const[a,b]of p.threshold_hard)g.add(a,b,inf);
 const result=g.solve(s,t,inf),m=restore(data),labels=P.labelsFromProjection(p,m,result.reach),maxlabels=P.labelsFromProjection(p,m,Array.from(result.sink,x=>!x),true);
 const f=features(data,labels),fm=features(data,maxlabels),value=f.values.reduce((s,x,k)=>s+x*d[k],0),maxvalue=fm.values.reduce((s,x,k)=>s+x*d[k],0),dualValue=(ceiling-result.flow)/4;
 if(Math.abs(value-maxvalue)>3e-8||Math.abs(value-dualValue)>3e-8)throw Error("warped cut and capture features disagree");
 return{value,dualValue,labels,maxlabels,features:f,maximumFeatures:fm,nodes:g.n,arcs:g.to.length/2};
}
function warpedAtoms(data,d){ // exact rational increment strings
 const q=d.map(x=>new Q(x)),cum=[zero];for(const x of q)cum.push(cum.at(-1).add(x));
 if(cum.at(-1).cmp(one)!==0||q.some(x=>x.cmp(zero)<=0))throw Error("invalid exact warp");
 const index=new Map(data.knots.map((s,i)=>[s,i]));
 function warp(s){const f=fold(new Q(s)),k=index.get(String(f.radius));if(k===undefined)throw Error("unpriced warp coordinate");return new Q(BigInt(f.constant)).add(cum[k].mul(new Q(BigInt(f.sign))));}
 return data.atoms.map(a=>({...a,exact_light:a.exact_light.map(p=>p.map(x=>String(warp(x))))}));
}
return{build,identity,features,rewardWeights,solve,warpedAtoms,fold,capturePoint};

})(require("../interval_turn_density/atomic_survival_v8.cjs"),require("../interval_turn_density/projected_cut.cjs"));
