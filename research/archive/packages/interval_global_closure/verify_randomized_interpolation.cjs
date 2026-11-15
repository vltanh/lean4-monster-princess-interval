#!/usr/bin/env node
"use strict";
const result=(function runExtractionTests(){
 const abs=x=>x<0n?-x:x,gcd=(a,b)=>{a=abs(a);b=abs(b);while(b){let t=a%b;a=b;b=t;}return a;};
 const Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}let g=gcd(n,d);return[n/g,d/g];};
 const A=(x,y)=>Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1]),N=x=>[-x[0],x[1]],S=(x,y)=>A(x,N(y)),M=(x,y)=>Q(x[0]*y[0],x[1]*y[1]),D=(x,y)=>Q(x[0]*y[1],x[1]*y[0]);
 const C=(x,y)=>{let z=x[0]*y[1]-y[0]*x[1];return z<0n?-1:z>0n?1:0;},eq=(x,y)=>C(x,y)===0;
 const fl=x=>x[0]>=0n?x[0]/x[1]:-((-x[0]+x[1]-1n)/x[1]);
 const ab=x=>Q(abs(x[0]),x[1]),mn=(x,y)=>C(x,y)<0?x:y,mx=(x,y)=>C(x,y)>0?x:y;
 const zero=Q(0),one=Q(1),two=Q(2),half=Q(1,2),str=x=>`${x[0]}/${x[1]}`;
 let checks={map:0,physical:0,buffer:0,field:0,affine:0};let summaries=[];
 const assert=(p,why)=>{if(!p)throw new Error(why);};
 function cell(z,n){let q=M(z,Q(n)),k=fl(q),a=S(q,Q(k)),m=((k%(2n*BigInt(n)))+2n*BigInt(n))%(2n*BigInt(n));return{k,a,rep:m<BigInt(n)};}
 function T(z,Z,n){let {k,a,rep}=cell(z,n);if(eq(a,zero))return z;let th=rep?Z:S(one,Z),up=rep?C(a,th)>0:C(a,th)>=0;return Q(k+(up?1n:0n),BigInt(n));}
 function fn(t,x){let g=mx(zero,mn(one,S(M(two,ab(x)),ab(S(t,one)))));return A(half,M(C(x,zero)>=0?half:N(half),g));}
 function Fuv(u,v,n,L,R){
  const cu=cell(u,n),cv=cell(v,n);let cuts=[L,R];
  for(let z of [cu.rep?cu.a:S(one,cu.a),cv.rep?cv.a:S(one,cv.a)])if(C(z,L)>0&&C(z,R)<0)cuts.push(z);
  cuts.sort(C);let sum=zero;
  for(let i=0;i+1<cuts.length;i++){let z=D(A(cuts[i],cuts[i+1]),two),a=T(u,z,n),b=T(v,z,n);sum=A(sum,M(S(cuts[i+1],cuts[i]),fn(D(A(a,b),two),D(S(a,b),two))));}
  return D(sum,S(R,L));
 }
 function F(t,x,n,L,R){return Fuv(A(t,x),S(t,x),n,L,R);}
 function signature(u,v,n,L,R){const cu=cell(u,n),cv=cell(v,n);let rows=[["L",L],["R",R],["U",cu.rep?cu.a:S(one,cu.a)],["V",cv.rep?cv.a:S(one,cv.a)]];rows.sort((a,b)=>C(a[1],b[1])||a[0].localeCompare(b[0]));return `${cu.k},${cv.k}|${rows.map(x=>x[0]).join("")}`;}
 for(let n=1;n<=4;n++)for(let eps of [Q(1,2),Q(1,4),Q(1,8)]){
  const h=Q(1,n),L=S(half,eps),R=A(half,eps),Zs=[L,D(A(L,half),two),half,D(A(half,R),two),R];
  for(let Z of Zs){
   let bound=M(h,mx(Z,S(one,Z))),last=null;
   for(let j=-16*n;j<=24*n;j++){
    let z=Q(j,8*n),t=T(z,Z,n);
    assert(eq(T(N(z),Z,n),N(t)),"oddness");assert(eq(T(A(z,two),Z,n),A(t,two)),"period");
    assert(C(ab(S(t,z)),bound)<=0,"uniform displacement");if(last)assert(C(last,t)<=0,"monotonicity");last=t;
    if(j%8===0)assert(eq(t,z),"fixed grid");checks.map++;
   }
   for(let it=0;it<=8*n;it+=2)for(let ix=-4*n;ix<=4*n;ix+=2){
    let t=Q(it,4*n),x=Q(ix,4*n),u=T(A(t,x),Z,n),v=T(S(t,x),Z,n),tp=D(A(u,v),two),xp=D(S(u,v),two);
    assert(C(ab(xp),one)<=0&&C(tp,zero)>=0,"physical strip");assert(C(ab(S(tp,t)),bound)<=0,"time displacement");
    let ti=M(M(two,Q(n)),tp),xi=M(M(two,Q(n)),xp);assert(ti[1]===1n&&xi[1]===1n&&(ti[0]-xi[0])%2n===0n,"node parity");
    if(eq(x,zero))assert(eq(xp,zero)&&C(tp,two)<=0,"center deadline");
    if(eq(ab(x),one))assert(eq(xp,x)&&C(tp,two)<=0,"endpoint deadline");checks.physical++;
   }
  }
  let bL=M(h,mx(L,S(one,L))),bC=M(h,half),bR=M(h,mx(R,S(one,R)));
  let avg=D(A(M(S(half,L),D(A(bL,bC),two)),M(S(R,half),D(A(bC,bR),two))),S(R,L));
  let expected=M(h,A(half,D(eps,two)));assert(eq(avg,expected),"buffer expectation");checks.buffer++;
  const delta=Q(1,8*n);
  for(let it=0;it<=12*n;it+=2)for(let ix=-4*n;ix<=4*n;ix+=2){
   let t=Q(it,4*n),x=Q(ix,4*n),a=F(t,x,n,L,R);
   assert(eq(A(a,F(t,N(x),n,L,R)),one),"CDF symmetry");
   if(eq(x,zero))assert(eq(a,half),"center trace");
   if(C(A(x,delta),one)<=0)assert(C(F(A(t,delta),A(x,delta),n,L,R),a)>=0,"CDF right transport");
   if(C(S(x,delta),N(one))>=0)assert(C(F(A(t,delta),S(x,delta),n,L,R),a)<=0,"CDF left transport");
   let uu=M(A(t,x),Q(n)),vv=M(S(t,x),Q(n));
   if(uu[1]===1n&&vv[1]===1n)assert(eq(a,fn(t,x)),"nodal interpolation");checks.field++;
  }
  for(let i=0;i<2*n;i++)for(let j=0;j<2*n;j++)for(let aa of [1,3,5])for(let bb of [1,3,5]){
   let u=Q(8*i+aa,8*n),v=Q(8*j+bb,8*n),u2=A(u,Q(1,8*n)),v2=A(v,Q(1,8*n));
   if(C(ab(S(u,v)),two)>0||C(ab(S(u2,v2)),two)>0)continue;
   if(signature(u,v,n,L,R)!==signature(u2,v2,n,L,R))continue;
   let mid=Fuv(D(A(u,u2),two),D(A(v,v2),two),n,L,R),rhs=D(A(Fuv(u,v,n,L,R),Fuv(u2,v2,n,L,R)),two);
   assert(eq(mid,rhs),"P1 common threshold patch");checks.affine++;
  }
  summaries.push({n,epsilon:str(eps),expected_buffer:str(avg)});
 }
 return {scope:"Exact BigInt rational regression of the randomized interpolation construction; no optimal LP or game value evaluated.",checks,summaries};
})();
console.log(JSON.stringify(result,null,2));
