/** Complete continuous-start M1 separation for a fixed raw mixture of
 * uniform interval fans. Breakpoints are exact inverse/endpoint/initial
 * arrangement boundaries; no start sampling defines the family.
 */
module.exports=(function(){
function createFanM1Separator(G,T,entries){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,
  source=entries.map((e,i)=>({row:e.row,weight:Q(e.weight??1),id:e.id??i}));
 let total=Z;for(const e of source){if(e.weight.cmp(0)<0)throw Error("negative fan weight");e.weight.n;total=total.a(e.weight);}
 if(total.cmp(0)<=0)throw Error("zero fan mixture");
 const rows=source.filter(e=>e.weight.cmp(0)>0).map(e=>({...e,weight:e.weight.dby(total)})),cache=new Map();
 function route(a){a=Q(a);if(a.cmp(-1)<0||a.cmp(1)>0)throw Error("M1 start outside arena");return new G.PLPath([[Z,a],[O.a(a),Q(-1)],[Q(3).a(a),O]]);}
 function score(a){a=Q(a);const key=a.str();if(cache.has(key))return cache.get(key);const m=route(a);let cost=Z;
  for(const e of rows){const p=T.orientation(e.row,m,1),n=T.orientation(e.row,m,-1);if(!p.complete||!n.complete)throw Error("fan M1 did not complete");cost=cost.a(p.cost.a(n.cost).dby(2).m(e.weight));}
  cache.set(key,cost);return cost;
 }
 function geometryCuts(){
  const points=new Map(),add=a=>{a=Q(a);if(a.cmp(-1)>=0&&a.cmp(1)<=0)points.set(a.str(),a);};add(-1);add(1);
  for(const{row}of rows)for(const sign of [1,-1]){
   const p=row.path,lo=sign===1?row.lower:row.upper.neg(),hi=sign===1?row.upper:row.lower.neg(),p0=p.x[0].m(sign);
   add(p0.a(lo));add(p0.a(hi));
   const data=[
    {k:Q(1),nu:-sign,qs:[[Q(1),lo.neg()],[Q(1),hi.neg()],[Z,p0]]},
    {k:Q(3),nu:sign,qs:[[Q(1),Q(2).a(lo)],[Q(1),Q(2).a(hi)],[Q(2),Q(2).s(p0)]]}
   ];
   for(const d of data){
    const seq=p.seq[(d.nu+1)>>1];
    for(const[s,b]of d.qs)if(!s.eq(0))for(const q of seq)add(q.s(b).dby(s));
    for(let i=0;i<p.t.length;i++){
     const left=max(Q(-1),p.t[i].s(d.k)),right=i+1<p.t.length?min(O,p.t[i+1].s(d.k)):O;
     add(p.t[i].s(d.k));if(left.cmp(right)>0)continue;
     const v=i<p.v.length?p.v[i]:Z,
      cs=O.s(v.m(d.nu)),cb=d.k.s(p.x[i].a(v.m(d.k.s(p.t[i]))).m(d.nu));
     for(const[s,b]of d.qs){const den=s.s(cs);if(den.eq(0))continue;const a=cb.s(b).dby(den);if(a.cmp(left)>=0&&a.cmp(right)<=0)add(a);}
    }
   }
  }
  return[...points.values()].sort((a,b)=>a.cmp(b));
 }
 function separate({verifyPolynomial=true,keepCells=false,maxCells=200000,onProgress=()=>{}}={}){
  const cuts=geometryCuts();if(cuts.length-1>maxCells)throw Error("fan M1 arrangement exceeds cell cap");let best=null,bestStart=null,stationary=0,checks=0;const cells=[];
  function candidate(a){const c=score(a);if(best===null||c.cmp(best)<0){best=c;bestStart=a;}}
  for(const a of cuts)candidate(a);
  for(let j=0;j+1<cuts.length;j++){
   const a=cuts[j],b=cuts[j+1],width=b.s(a),at=u=>score(a.a(width.m(u))),
    f1=at(Q("1/4")),f2=at(Q("1/2")),f3=at(Q("3/4")),
    q2=f1.s(f2.m(2)).a(f3).m(8),q1=f3.s(f1).m(2).s(q2),q0=f2.s(q1.dby(2)).s(q2.dby(4)),
    polynomial=u=>q0.a(q1.m(u)).a(q2.m(u.m(u)));
   if(verifyPolynomial)for(const u of [Q("1/3"),Q("2/3")]){if(!polynomial(u).eq(at(u)))throw Error("missing fan M1 arrangement boundary");checks++;}
   let root=null;if(q2.cmp(0)>0){const u=q1.neg().dby(q2.m(2));if(u.cmp(0)>0&&u.cmp(1)<0){root=a.a(width.m(u));const c=score(root);if(!c.eq(polynomial(u)))throw Error("M1 stationary polynomial mismatch");candidate(root);stationary++;}}
   if(keepCells)cells.push({left:a.str(),right:b.str(),local_coefficients:[q0.str(),q1.str(),q2.str()],stationary_start:root?.str()??null});
   if(j%32===31)onProgress({cells:j+1,total:cuts.length-1});
  }
  return{scope:"Complete continuous initial-start M1 family for this RAW immutable fan mixture. A violating raw route must be rescored before claiming an attack on its ordered quantile coupling. Nonviolating raw M1 inequalities also hold after ordering.",
   complete:true,minimum:best.str(),limit:best.limit().str(),decimal:best.limit().num(),start:bestStart.str(),route:route(bestStart).json(),
   cell_count:cuts.length-1,stationary_candidates:stationary,polynomial_checks:checks,score_queries:cache.size,
   cuts:cuts.map(x=>x.str()),cells:keepCells?cells:null,normalized_weights:rows.map(e=>({id:e.id,weight:e.weight.str()})),arithmetic:G.stats()};
 }
 return{score,route,geometryCuts,separate};
}
return{createFanM1Separator};
})();
