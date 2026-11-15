"use strict";
function createInterfaceExcursionTools(A) {
 const Q=A.Q,Z=Q(0),O=Q(1);
 const min=(a,b)=>a.cmp(b)<=0?a:b,max=(a,b)=>a.cmp(b)>=0?a:b;
 function scalarPath(raw){return raw.map(p=>p.map(Q));}
 function validate(raw,side=-1) {
   const p=scalarPath(raw);if(p.length<2||!p[0][0].eq(0)||!p[0][1].eq(0)||!p[p.length-1][1].eq(0))throw Error("interface endpoints");
   for(let i=0;i<p.length;i++){if(p[i][1].mul(side).cmp(0)<0)throw Error("wrong side");if(i){let dt=p[i][0].sub(p[i-1][0]),dx=p[i][1].sub(p[i-1][1]);if(dx.cmp(0)<0)dx=dx.neg();if(dt.cmp(0)<=0||dx.cmp(dt)>0)throw Error("illegal leg");}}
   return p;
 }
 function moment(raw,alpha,beta,lo,hi,oldLower=0,oldUpper=0) {
   const path=scalarPath(raw);alpha=Q(alpha);beta=Q(beta);lo=Q(lo);hi=Q(hi);oldLower=Q(oldLower);oldUpper=Q(oldUpper);
   const qs=path.map(([t,x])=>alpha.mul(t).add(beta.mul(x)));
   let cuts=[lo,hi,oldLower.neg(),oldUpper,...qs].filter(q=>q.cmp(lo)>=0&&q.cmp(hi)<=0),u=new Map(cuts.map(q=>[q.str(),q]));cuts=[...u.values()].sort((x,y)=>x.cmp(y));
   let value=Z,intervals=0,segments=0;
   for(let j=0;j+1<cuts.length;j++){
     const l=cuts[j],h=cuts[j+1],m=l.add(h).div(2);if(m.cmp(oldLower.neg())>=0&&m.cmp(oldUpper)<=0)continue;
     let found=null;
     for(let i=0;i+1<path.length;i++){segments++;const q0=qs[i],q1=qs[i+1];if(q0.eq(q1))continue;if(m.cmp(min(q0,q1))<0||m.cmp(max(q0,q1))>0)continue;
       const slope=path[i+1][0].sub(path[i][0]).div(q1.sub(q0)),constant=path[i][0].sub(slope.mul(q0));
       found=constant.mul(h.sub(l)).add(slope.mul(h.mul(h).sub(l.mul(l))).div(2));break;
     }
     if(found===null)throw Error("uncaptured interval "+l.str()+","+h.str());value=value.add(found);intervals++;
   }
   return {value,intervals,segments};
 }
 function bounds(alpha,B,T,L){
   alpha=Q(alpha);B=Q(B);T=Q(T);L=Q(L);const C=B.sub(alpha),D=B.add(alpha);
   if(alpha.cmp(0)<0||C.cmp(0)<=0||T.cmp(0)<=0)throw Error("invalid affine flux");
   const Lmax=C.mul(T).div(2);if(L.cmp(0)<0||L.cmp(Lmax)>0)throw Error("invalid final lower record");
   const r=L.div(Lmax),d=O.sub(r),hstar=alpha.mul(C.mul(T).sub(L.mul(2))).div(D),hc=alpha.mul(T).mul(r),peak=max(Z,B.mul(r).mul(2).sub(C));
   const upperLower=alpha.mul(T.mul(T)).div(2).add(alpha.mul(B).mul(T.mul(T)).mul(peak.mul(peak)).div(D.mul(D).mul(D).mul(2)));
   const upperTent=alpha.mul(T.mul(T)).div(2).add(alpha.mul(B).mul(T.mul(T)).div(D.mul(2)));
   const credit=B.mul(T).mul(Lmax.sub(L)).div(C);
   const bound=credit.add(upperLower).sub(upperTent),margin=B.mul(C).mul(T).mul(Lmax.sub(L)).div(D.mul(D));
   return {C,D,Lmax,r,hstar,hc,upperLower,upperTent,credit,bound,margin,horizon:B.div(C).add(Q("1/2")).mul(T)};
 }
 function compare(raw,alpha,B,oldLower=0,oldUpper=0){
   const p=validate(raw),T=p[p.length-1][0];alpha=Q(alpha);B=Q(B);oldLower=Q(oldLower);oldUpper=Q(oldUpper);
   let L=Z;for(const [t,x]of p)L=max(L,alpha.mul(t).add(B.mul(x)).neg());
   if(L.cmp(oldLower)<=0)throw Error("excursion must create a lower record");
   const b=bounds(alpha,B,T,L),H=b.horizon;
   const old=[...p,[H,T.sub(H)]],big=[[Z,Z],[T.div(2),T.div(2).neg()],[T,Z],[H,T.sub(H)]];
   const a=moment(old,alpha,B,b.Lmax.neg(),alpha.mul(T),oldLower,oldUpper),c=moment(big,alpha,B,b.Lmax.neg(),alpha.mul(T),oldLower,oldUpper);
   if(a.value.sub(c.value).cmp(b.margin)<0)throw Error("tent domination failure");
   return {difference:a.value.sub(c.value),bound:b.bound,margin:b.margin,L,T,old:a,new:c};
 }
 return {Q,validate,moment,bounds,compare};
}
module.exports={createInterfaceExcursionTools};
