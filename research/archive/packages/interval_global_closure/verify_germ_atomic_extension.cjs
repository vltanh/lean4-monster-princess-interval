/** Retained-universe and cache replay tests for the germ atomic cut. */
module.exports = function verifyGermExtension(E,G,A,fixtures){
 const checks=[];
 for(const f of fixtures){
  const m=A.Model(f.atoms),weights=f.nums.map(n=>G.Q(n).dby(f.den).str()),r=A.integerLimitCut(m,weights);
  const x=G.Q("1/3").a(G.eps.pow(5));
  const extra={exact_light:[[x,x.neg()],[G.Q(2).s(x),x.neg()],[G.Q(2).s(x),G.Q(4).s(x)]].map(p=>p.map(z=>z.str()))};
  const full=A.extend(A.pack(m),[...f.atoms,extra],{extraQueries:[G.Q("3/5").a(G.eps.pow(7)).str()],extraBases:[G.Q("4/5").s(G.eps.pow(6)).str()]});
  for(const tail of ["minimal","absorb"])for(const labels of [r.labels,r.maximum_labels]){
   const lifted=A.lift(m,labels,full,{tail}),old=m.rowExact(labels),now=full.rowExact(lifted);
   for(let j=0;j<old.length;j++){if(old[j].cmp(now[j])!==0)throw Error("lift changed old capture");checks.push({fixture:f.name,check:"old row",tail,atom:j});}
  }
  const restored=A.restore(A.pack(full),full.atoms),saved=A.pack(full),again=A.pack(restored);
  for(const key of ["v","base","bounds","offset","N","defs","units","germ_units"])
   if(JSON.stringify(saved[key])!==JSON.stringify(again[key]))throw Error("cache physical rebuild");
  const ww=[...weights.map(w=>G.Q(w).m("3/4").str()),"1/4"],a=A.integerLimitCut(full,ww),b=A.integerLimitCut(restored,ww);
  if(a.value!==b.value)throw Error("restored cut");
  checks.push({fixture:f.name,check:"restore",value:a.value});
 }
 return{checks,arithmetic:G.stats()};
};