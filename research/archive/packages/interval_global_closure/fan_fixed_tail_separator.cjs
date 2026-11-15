/** Exact continuous initial-start arrangement for a fixed completed unit tail.
 * Fair reflection permits an oriented first leg +1. This is RAW fan scoring.
 */
module.exports=(function(){
function createFanFixedTailSeparator(G,T,entries,family){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,
  direction=family.firstDirection??1;if(direction!==1&&direction!==-1)throw Error("unit initial direction");
 const originalTail=family.tail.map(v=>v.map(Q)),tail=originalTail.map(([t,x])=>[t,x.m(direction)]);
 if(!tail.length||tail[0][0].cmp(0)<0)throw Error("fixed tail required");
 for(let j=0;j<tail.length;j++){
  if(tail[j][1].cmp(-1)<0||tail[j][1].cmp(1)>0)throw Error("illegal fixed tail position");
  if(j){const dt=tail[j][0].s(tail[j-1][0]),dx=tail[j][1].s(tail[j-1][1]);if(dt.cmp(0)<=0||!dx.m(dx).eq(dt.m(dt)))throw Error("nonunit fixed tail");}
 }
 if(!tail.some(v=>v[1].eq(-1))||!tail.some(v=>v[1].eq(1)))throw Error("fixed tail must retain both endpoint visits");
 const c=tail[0][0].a(tail[0][1]),left=max(Q(-1),c.s(tail[0][0].m(2))),right=min(O,min(c,Q(2).s(c)));
 if(left.cmp(right)>0)throw Error("empty initial-start domain");
 let total=Z;const data=entries.map((e,i)=>{const weight=Q(e.weight??1);if(weight.cmp(0)<0)throw Error("negative fan weight");weight.n;total=total.a(weight);return{row:e.row,weight,id:e.id??i};});
 if(total.cmp(0)<=0)throw Error("zero fan law");
 const rows=data.filter(e=>e.weight.cmp(0)>0).map(e=>({...e,weight:e.weight.dby(total)})),cache=new Map();
 function route(b){b=Q(b);if(b.cmp(left)<0||b.cmp(right)>0)throw Error("initial start outside fixed-tail domain");return new G.PLPath([[Z,b.m(direction)],[c.s(b).dby(2),c.a(b).dby(2).m(direction)],...originalTail]);}
 function score(b){b=Q(b);const key=b.str();if(cache.has(key))return cache.get(key);const m=route(b);let value=Z;
  for(const e of rows){const a=T.orientation(e.row,m,1),n=T.orientation(e.row,m,-1);if(!a.complete||!n.complete)throw Error("incomplete fixed-tail fan score");value=value.a(a.cost.a(n.cost).dby(2).m(e.weight));}cache.set(key,value);return value;}
 function geometryCuts(){
  const points=new Map(),add=b=>{b=Q(b);if(b.cmp(left)>=0&&b.cmp(right)<=0)points.set(b.str(),b);};add(left);add(right);
  for(const{row}of rows)for(const sign of [1,-1]){
   const p=row.path,lo=sign===1?row.lower:row.upper.neg(),hi=sign===1?row.upper:row.lower.neg(),p0=p.x[0].m(sign),targets=[lo,hi],
    firstSeq=p.seq[(sign+1)>>1];
   for(let j=0;j<tail.length;j++){
    const [end,x]=tail[j],d=j===0?-1:tail[j][1].s(tail[j-1][1]).cmp(0),constant=end.s(x.m(d)),seq=p.seq[(d*sign+1)>>1];
    targets.push(x.s(p.at(end).m(sign)));for(const q of seq)targets.push(q.s(constant).m(d));
   }
   for(const target of targets)add(target.a(p0));
   for(const q of firstSeq){add(lo.s(q));add(hi.s(q));}
   for(let i=0;i<p.t.length;i++){
    const upper=min(right,c.s(p.t[i].m(2))),lower=i+1<p.t.length?max(left,c.s(p.t[i+1].m(2))):left;
    add(c.s(p.t[i].m(2)));if(lower.cmp(upper)>0)continue;
    const v=i<p.v.length?p.v[i]:Z,alpha=O.a(v.m(sign)).dby(2),offset=c.m(O.s(v.m(sign))).dby(2).s(p.x[i].m(sign)).a(v.m(p.t[i]).m(sign));
    if(!alpha.eq(0))for(const target of targets){const b=target.s(offset).dby(alpha);if(b.cmp(lower)>=0&&b.cmp(upper)<=0)add(b);}
    const slope=alpha.s(1);if(!slope.eq(0))for(const q of firstSeq){const b=q.s(offset).dby(slope);if(b.cmp(lower)>=0&&b.cmp(upper)<=0)add(b);}
   }
  }
  return[...points.values()].sort((a,b)=>a.cmp(b));
 }
 function separate({verifyPolynomial=true,keepCells=false,maxCells=200000,onProgress=()=>{}}={}){
  const cuts=geometryCuts();if(cuts.length-1>maxCells)throw Error("fan fixed-tail arrangement exceeds cell cap");let best=null,bestStart=null,stationary=0,checks=0;const cells=[];
  function candidate(a){const c=score(a);if(best===null||c.cmp(best)<0){best=c;bestStart=a;}}
  for(const a of cuts)candidate(a);
  for(let j=0;j+1<cuts.length;j++){
   const a=cuts[j],b=cuts[j+1],width=b.s(a),at=u=>score(a.a(width.m(u))),
    f1=at(Q("1/4")),f2=at(Q("1/2")),f3=at(Q("3/4")),
    q2=f1.s(f2.m(2)).a(f3).m(8),q1=f3.s(f1).m(2).s(q2),q0=f2.s(q1.dby(2)).s(q2.dby(4)),
    polynomial=u=>q0.a(q1.m(u)).a(q2.m(u.m(u)));
   if(verifyPolynomial)for(const u of [Q("1/3"),Q("2/3")]){if(!polynomial(u).eq(at(u)))throw Error("missing fan fixed-tail arrangement boundary");checks++;}
   let root=null;if(q2.cmp(0)>0){const u=q1.neg().dby(q2.m(2));if(u.cmp(0)>0&&u.cmp(1)<0){root=a.a(width.m(u));const c=score(root);if(!c.eq(polynomial(u)))throw Error("fixed-tail stationary polynomial mismatch");candidate(root);stationary++;}}
   if(keepCells)cells.push({left:a.str(),right:b.str(),local_coefficients:[q0.str(),q1.str(),q2.str()],stationary_start:root?.str()??null});
   if(j%32===31)onProgress({cells:j+1,total:cuts.length-1});
  }
  return{scope:"Complete continuous initial-start family for the supplied fixed tail for this RAW immutable fan mixture. A violating raw route must be rescored before claiming an attack on its ordered quantile coupling. Nonviolating raw family inequalities also hold after ordering.",
   complete:true,minimum:best.str(),limit:best.limit().str(),decimal:best.limit().num(),start:bestStart.str(),physical_start:bestStart.m(direction).str(),first_direction:direction,domain:[left.str(),right.str()],route:route(bestStart).json(),
   cell_count:cuts.length-1,stationary_candidates:stationary,polynomial_checks:checks,score_queries:cache.size,
   cuts:cuts.map(x=>x.str()),cells:keepCells?cells:null,normalized_weights:rows.map(e=>({id:e.id,weight:e.weight.str()})),arithmetic:G.stats()};
 }
 return{score,route,geometryCuts,separate,domain:[left,right],orientedCharacteristic:c,firstDirection:direction};
}
return{createFanFixedTailSeparator};
})();
