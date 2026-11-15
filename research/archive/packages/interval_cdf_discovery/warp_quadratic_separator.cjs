
function createQuadraticWarpSeparator(E){
 const {Q,ZERO}=E;
 function vector(v){return v.numerators.map(n=>Q(n).dby(v.denominator));}
 function dot(v,d){return v.reduce((s,x,i)=>s.a(x.m(d[i])),ZERO);}
 function decode(data){return data.cells.map(c=>({...c,constant:vector(c.constant),linear:vector(c.linear),quadratic:vector(c.quadratic)}));}
 function separate(cells,increments){
  const d=increments.map(Q),byFamily=new Map(),all=[];
  for(let index=0;index<cells.length;index++){
   const c=cells[index],p=dot(c.constant,d),b=dot(c.linear,d),a=dot(c.quadratic,d);
   const candidates=[[ZERO,p],[Q(1),p.a(b).a(a)]];
   if(a.cmp(0)>0){const t=b.neg().dby(a.m(2));if(t.cmp(0)>0&&t.cmp(1)<0)candidates.push([t,p.s(b.m(b).dby(a.m(4)))]);}
   let best=candidates[0];for(const v of candidates)if(v[1].cmp(best[1])<0)best=v;
   const [l,r]=c.interval.map(Q),t=best[0],start=l.a(r.s(l).m(t));
   const row={cell:index,family:c.family,positive:c.positive,parameter:t,start,value:best[1],
    coefficients:c.constant.map((x,i)=>x.a(c.linear[i].m(t)).a(c.quadratic[i].m(t.m(t))))};
   all.push(row);const key=c.family+"|"+c.positive;if(!byFamily.has(key)||row.value.cmp(byFamily.get(key).value)<0)byFamily.set(key,row);
  }
  return{families:[...byFamily.values()],cells:all};
 }
 return{decode,separate};
}
module.exports = {createQuadraticWarpSeparator};
