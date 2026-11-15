'use strict';
function createSharedArea(field){
 const B=field.nodes[0][0].aa.constructor,q=x=>x instanceof B?x:new B(x),z=q(0),one=q(1),two=q(2);
 const min=(a,b)=>a.cmp(b)<=0?a:b,max=(a,b)=>a.cmp(b)>=0?a:b;
 const tr=field.triangles.filter(t=>t.ps.some(p=>p[0].cmp(1)<=0)).map(t=>({p:t.ps.map(p=>p.map(x=>{if(x.bb.n!==0n)throw Error('nonrational field');return x.aa;})),c:t.cf.map(x=>x.aa)}));
 function uniq(xs){xs.sort((a,b)=>a.cmp(b));return xs.filter((x,i)=>!i||!x.eq(xs[i-1]));}
 function trace(fixed,lo,hi,axis){fixed=q(fixed);lo=q(lo);hi=q(hi);if(lo.eq(hi))return[];const seg=[],xs=[lo,hi],op=1-axis;
  for(const t of tr){let hit=[];for(let j=0;j<3;j++){const p=t.p[j],r=t.p[(j+1)%3];if(p[axis].eq(fixed))hit.push(p[op]);if(!p[axis].eq(r[axis])&&fixed.cmp(min(p[axis],r[axis]))>=0&&fixed.cmp(max(p[axis],r[axis]))<=0)hit.push(p[op].a(fixed.s(p[axis]).m(r[op].s(p[op])).dby(r[axis].s(p[axis]))));}if(hit.length<2)continue;hit=uniq(hit);let l=max(lo,hit[0]),h=min(hi,hit.at(-1));if(l.cmp(h)>=0)continue;let m=t.c[op],b=t.c[axis].m(fixed).a(t.c[2]);seg.push({lo:l,hi:h,m,b});xs.push(l,h);}
  let cuts=uniq(xs),out=[];for(let i=0;i+1<cuts.length;i++){let l=cuts[i],h=cuts[i+1],mid=l.a(h).dby(two),s=seg.find(s=>s.lo.cmp(mid)<=0&&s.hi.cmp(mid)>=0);if(!s)throw Error('line missing');let last=out.at(-1);if(last&&last.hi.eq(l)&&last.m.eq(s.m)&&last.b.eq(s.b))last.hi=h;else out.push({lo:l,hi:h,m:s.m,b:s.b});}return out;
 }
 const cache=new Map();
 function traces(l,h,H){const key=[l,h,H].map(x=>x.str()).join(',');if(cache.has(key))return cache.get(key);let F=trace(h.neg(),h,H,1),G=trace(l,l.neg(),l,0);
  if(!F.length)throw Error('empty F');if(h.cmp(l)>0)F.unshift({lo:l,hi:h,m:z,b:F[0].m.m(h).a(F[0].b)});
  let init=G.length?G[0].m.m(l.neg()).a(G[0].b):z;if(h.cmp(l)>0)G.unshift({lo:h.neg(),hi:l.neg(),m:z,b:init});G.push({lo:l,hi:H,m:z,b:z});G=G.filter(p=>p.lo.cmp(p.hi)<0);const v={F,G};cache.set(key,v);return v;
 }
 function cap(F,n){let out=[];for(const p of F){let fl=p.m.m(p.lo).a(p.b),fh=p.m.m(p.hi).a(p.b);if(fl.cmp(n)>=0)out.push({...p,m:z,b:n});else if(fh.cmp(n)<=0)out.push(p);else{if(p.m.cmp(z)<=0)throw Error('nonmonotone F');const cut=n.s(p.b).dby(p.m);out.push({...p,hi:cut});out.push({...p,lo:cut,m:z,b:n});}}return out;}
 function candidates(l,h,n,H){const raw=traces(l,h,H),F=cap(raw.F,n),G=raw.G,C=[];function add(lo,hi,m,b,kind){lo=max(z,lo);hi=min(H,hi);if(lo.cmp(hi)<0)C.push({lo,hi,m,b,kind});}
  for(const p of F)for(const u of[p.lo,p.hi]){const fv=p.m.m(u).a(p.b);for(const g of G){let lo=max(h.neg(),g.lo),hi=min(u,min(H,g.hi));add(u.a(lo).dby(two),u.a(hi).dby(two),g.m.m(-2),fv.a(g.m.m(u)).s(g.b),'U');}}
  for(const g of G)for(const v of[g.lo,g.hi]){const gv=g.m.m(v).a(g.b);for(const p of F){let lo=max(l,max(v,p.lo)),hi=min(H,p.hi);add(lo.a(v).dby(two),hi.a(v).dby(two),p.m.m(two),p.b.s(p.m.m(v)).s(gv),'V');}}
  for(const p of F)for(const g of G){const lo=max(l,max(p.lo,g.lo)),hi=min(H,min(p.hi,g.hi));add(lo,hi,p.m.s(g.m),p.b.s(g.b),'diagonal');}
  let dedup=new Map();for(const c of C){let key=[c.m,c.b,c.lo,c.hi].map(x=>x.str()).join('|');if(!dedup.has(key))dedup.set(key,c);}return[...dedup.values()];
 }
 function upperEnvelope(C,H){let env=[{lo:z,hi:H,m:z,b:z,id:-1}];for(let id=0;id<C.length;id++){let c=C[id],next=[];for(const e of env){let lo=max(e.lo,c.lo),hi=min(e.hi,c.hi);if(lo.cmp(hi)>=0){next.push(e);continue;}if(e.lo.cmp(lo)<0)next.push({...e,hi:lo});let cuts=[lo,hi],dm=c.m.s(e.m),db=c.b.s(e.b);if(dm.cmp(z)!==0){const cross=db.neg().dby(dm);if(cross.cmp(lo)>0&&cross.cmp(hi)<0)cuts.push(cross);}cuts.sort((a,b)=>a.cmp(b));for(let j=0;j+1<cuts.length;j++){let a=cuts[j],b=cuts[j+1],mid=a.a(b).dby(two),win=dm.m(mid).a(db).cmp(z)>0?{...c,id}:e;next.push({...win,lo:a,hi:b});}if(e.hi.cmp(hi)>0)next.push({...e,lo:hi});}
   env=[];for(const p of next){let e=env.at(-1);if(e&&e.hi.eq(p.lo)&&e.m.eq(p.m)&&e.b.eq(p.b))e.hi=p.hi;else env.push(p);}
  }return env;
 }
 function verifyEnvelope(C,E,H){let count=0;if(!E[0].lo.eq(z)||!E.at(-1).hi.eq(H))throw Error('envelope coverage');for(let j=0;j<E.length;j++){let e=E[j];if(j&&!E[j-1].hi.eq(e.lo))throw Error('envelope gap');for(const s of[e.lo,e.hi])if(e.m.m(s).a(e.b).cmp(z)<0)throw Error('negative envelope');if(e.id>=0){const c=C[e.id];if(!e.m.eq(c.m)||!e.b.eq(c.b))throw Error('invalid winner');}for(const c of C){const lo=max(e.lo,c.lo),hi=min(e.hi,c.hi);if(lo.cmp(hi)>=0)continue;for(const s of[lo,hi]){count++;if(e.m.s(c.m).m(s).a(e.b.s(c.b)).cmp(z)<0)throw Error('envelope not upper');}}}return count;}
 function areaBox(low,high,rank,Horizon=1,{verify=true}={}){const l=q(low),h=q(high),n=q(rank),H=q(Horizon);if(l.cmp(z)<0||h.cmp(l)<0||h.cmp(H)>0||n.cmp(z)<0||n.cmp(one)>0)throw Error('invalid box');const C=candidates(l,h,n,H),E=upperEnvelope(C,H);let area=z;for(const e of E)area=area.a(e.m.m(e.hi.m(e.hi).s(e.lo.m(e.lo))).dby(two)).a(e.b.m(e.hi.s(e.lo)));let checks=verify?verifyEnvelope(C,E,H):0;return{moment:H.m(n).s(area),area,candidates:C.length,segments:E.length,checks,envelope:E};}
 return{q,trace,areaBox,traces,candidates,upperEnvelope,verifyEnvelope};
}
module.exports = {createSharedArea};
