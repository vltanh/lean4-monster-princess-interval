'use strict';
function createTwoExtrema(field, sharedModule){
 // The shared envelope accepts either the audited quadratic-field runtime
 // (with rational coefficients) or a plain exact-rational field adapter.
 if(!field.nodes[0][0].aa){
  const original=field,Base=field.nodes[0][0].constructor;
  class Wrap{constructor(x){this.aa=new Base(x instanceof Wrap?x.aa:x);this.bb={n:0n};}cmp(x){return this.aa.cmp(x instanceof Wrap?x.aa:x);}num(){return this.aa.num();}str(){return this.aa.str();}}
  field={nodes:original.nodes.map(p=>p.map(x=>new Wrap(x))),triangles:original.triangles.map(tr=>({...tr,ps:tr.ps.map(p=>p.map(x=>new Wrap(x))),cf:tr.cf.map(x=>new Wrap(x))})),initialValue:x=>new Wrap(original.initialValue(x instanceof Wrap?x.aa:x))};
 }
 const S=sharedModule.createSharedArea(field),q=S.q,z=q(0),one=q(1),two=q(2),min=(a,b)=>a.cmp(b)<=0?a:b,max=(a,b)=>a.cmp(b)>=0?a:b;
 const tr=field.triangles.filter(t=>t.ps.some(p=>p[0].cmp(1)<=0)).map(t=>({p:t.ps.map(p=>p.map(x=>x.aa)),c:t.cf.map(x=>x.aa)}));
 function value(c,p){return c[0].m(p[0]).a(c[1].m(p[1])).a(c[2]);}
 function clip(poly,c){if(!poly.length)return[];let out=[];for(let j=0;j<poly.length;j++){const p=poly[j],r=poly[(j+1)%poly.length],vp=value(c,p),vr=value(c,r),ip=vp.cmp(z)>=0,ir=vr.cmp(z)>=0;if(ip)out.push(p);if(ip!==ir){const x=vp.dby(vp.s(vr));out.push([p[0].a(x.m(r[0].s(p[0]))),p[1].a(x.m(r[1].s(p[1])))]);}}let clean=[];for(const p of out)if(!clean.length||!p[0].eq(clean.at(-1)[0])||!p[1].eq(clean.at(-1)[1]))clean.push(p);if(clean.length>1&&clean[0][0].eq(clean.at(-1)[0])&&clean[0][1].eq(clean.at(-1)[1]))clean.pop();return clean;}
 function restrict(poly,conds){for(const c of conds){poly=clip(poly,c);if(!poly.length)break;}return poly;}
 function capTrace(F,n){const out=[];for(const p of F){const fl=p.m.m(p.lo).a(p.b),fh=p.m.m(p.hi).a(p.b);if(fl.cmp(n)>=0)out.push({...p,m:z,b:n});else if(fh.cmp(n)<=0)out.push(p);else{const cut=n.s(p.b).dby(p.m);out.push({...p,hi:cut},{...p,lo:cut,m:z,b:n});}}return out;}
 function clampTrace(F,A,n){const out=[];for(const p of capTrace(F,n)){const fl=p.m.m(p.lo).a(p.b),fh=p.m.m(p.hi).a(p.b);if(fh.cmp(A)<=0)out.push({...p,m:z,b:A});else if(fl.cmp(A)>=0)out.push(p);else{const cut=A.s(p.b).dby(p.m);out.push({...p,hi:cut,m:z,b:A},{...p,lo:cut});}}return out;}
 function envelope(initial,arrival,rank,{verify=true}={}){
  const a=q(initial),t=q(arrival),n=q(rank),aq=new field.nodes[0][0].constructor(a.str()),A=field.initialValue(aq).aa;if(a.cmp(z)<0||a.cmp(t)>0||t.cmp(one)>=0||n.cmp(A)<0||n.cmp(one)>0)throw Error('two-extrema domain');
  const G=S.trace(a,a.neg(),a,0),F=capTrace(S.trace(a.neg(),a,t,1),n),C=[],counts={left_polygons:0,right_polygons:0,center_segments:0};
  function add(lo,hi,m,b,family){lo=max(z,lo);hi=min(t,hi);if(lo.cmp(hi)<0)C.push({lo,hi,m,b,kind:family});}
  function polygon(poly,cf,family){if(!poly.length)return;for(const p of poly){const time=p[0].a(p[1]).dby(two),r=value(cf,p);add(time,t,z,r,family+'-vertex');}if(poly.length<2)return;for(let j=0;j<poly.length;j++){const p=poly[j],r=poly[(j+1)%poly.length],s0=p[0].a(p[1]).dby(two),s1=r[0].a(r[1]).dby(two);if(s0.eq(s1))continue;const v0=value(cf,p),v1=value(cf,r),m=v1.s(v0).dby(s1.s(s0)),b=v0.s(m.m(s0));add(min(s0,s1),max(s0,s1),m,b,family+'-edge');}}
  const dom=[[one,z,a.neg()],[one.neg(),z,t],[z,one,a]];
  for(const T of tr){let umin=T.p.reduce((x,p)=>min(x,p[0]),T.p[0][0]),umax=T.p.reduce((x,p)=>max(x,p[0]),T.p[0][0]),vmin=T.p.reduce((x,p)=>min(x,p[1]),T.p[0][1]),vmax=T.p.reduce((x,p)=>max(x,p[1]),T.p[0][1]);if(umax.cmp(a)<0||umin.cmp(t)>0||vmax.cmp(a.neg())<0)continue;
   let base=restrict(T.p,dom);if(!base.length)continue;
   if(vmin.cmp(a)<=0){let lp=clip(base,[z,one.neg(),a]);for(const g of G){if(g.hi.cmp(vmin)<0||g.lo.cmp(vmax)>0)continue;let p=restrict(lp,[[z,one,g.lo.neg()],[z,one.neg(),g.hi]]);if(!p.length)continue;
    const cases=[{cond:[[T.c[0].neg(),T.c[1].neg(),A.s(T.c[2])]],m:[z,z,A]},{cond:[[T.c[0],T.c[1],T.c[2].s(A)],[T.c[0].neg(),T.c[1].neg(),n.s(T.c[2])]],m:T.c},{cond:[[T.c[0],T.c[1],T.c[2].s(n)]],m:[z,z,n]}];
    for(const c of cases){const P=restrict(p,c.cond);if(!P.length)continue;counts.left_polygons++;polygon(P,[c.m[0],c.m[1].s(g.m),c.m[2].s(g.b)],'left');}
   }}
   for(const fp of F){if(fp.hi.cmp(umin)<0||fp.lo.cmp(umax)>0)continue;const p=restrict(base,[[one,z,fp.lo.neg()],[one.neg(),z,fp.hi]]);if(!p.length)continue;
    let P=clip(p,[T.c[0].neg(),T.c[1].neg(),A.s(T.c[2])]);if(P.length){counts.right_polygons++;polygon(P,[fp.m.s(T.c[0]),T.c[1].neg(),fp.b.s(T.c[2])],'right');}
    P=clip(p,[T.c[0],T.c[1],T.c[2].s(A)]);if(P.length){counts.right_polygons++;polygon(P,[fp.m,z,fp.b.s(A)],'right');}
   }
  }
  // A first inward leg may meet the center. Its strict lower rank is zero.
  for(const p of clampTrace(S.trace(a,a,t,1),A,n)){counts.center_segments++;polygon([[p.lo,a],[p.hi,a]],[p.m,z,p.b],'left-center');}
  // Likewise for a right-first path which has already returned to center.
  for(const p of F){counts.center_segments++;polygon([[p.lo,p.lo],[p.hi,p.hi]],[p.m,z,p.b],'right-center');}
  let dd=new Map();for(const c of C){const key=[c.lo,c.hi,c.m,c.b].map(x=>x.str()).join('|');if(!dd.has(key))dd.set(key,c);}const candidates=[...dd.values()],E=S.upperEnvelope(candidates,t);let area=z;for(const e of E)area=area.a(e.m.m(e.hi.m(e.hi).s(e.lo.m(e.lo))).dby(two)).a(e.b.m(e.hi.s(e.lo)));const checks=verify?S.verifyEnvelope(candidates,E,t):0;
  return{initial:a,arrival:t,rank:n,initial_rank:A,moment:t.m(n).s(area),area,envelope:E,candidates:candidates.length,checks,counts};
 }
 return{envelope,q,clip,restrict};
}
module.exports = {createTwoExtrema};
