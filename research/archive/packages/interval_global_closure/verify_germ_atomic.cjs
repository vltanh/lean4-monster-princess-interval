/** Exact specialization replay against the original rational integer cut. */
module.exports = function verifyGermAtomic(E,G,A,fixtures){
 const Q=x=>G.Q(x).limit(),reports=[];let checks=0;
 for(const f of fixtures){
  const weights=f.nums.map(x=>G.Q(x).dby(f.den).str()),m=A.Model(f.atoms),lim=A.integerLimitCut(m,weights),specializations=[];
  for(const epsilon of f.specializations||["1/16","1/64","1/256"]){
   const atoms=f.atoms.map(a=>({exact_light:a.exact_light.map(p=>p.map(x=>G.Q(x).evaluate(epsilon).str()))}));
   const old=new E.Rational.Model(atoms);
   if(JSON.stringify(old.bounds)!==JSON.stringify(m.bounds)||JSON.stringify(old.defs)!==JSON.stringify(m.defs))throw Error("specialized topology");
   for(let j=0;j<atoms.length;j++){
    old.compile(j);const x=old.lastExactUnits,y=m.germUnits[j];if(x.length!==y.length)throw Error("reward count");
    for(let k=0;k<x.length;k++){if(x[k][0]!==y[k][0]||x[k][1].toString()!==y[k][1].g.evaluate(epsilon).str())throw Error("reward specialization");checks++;}
   }
   const exact=E.Integer.solveIntegerLaw(E.Cut,E.Physical,E.BigFlow.BigFlow,old,f.nums,f.den),v=Q(exact.exactValue),L=Q(lim.value);
   const error=lim.uniform_error_terms.reduce((a,x)=>a.a(G.Q(x).evaluate(epsilon)),Q(0));
   if(v.s(L).cmp(error)>0||L.s(v).cmp(error)>0)throw Error("uniform envelope");
   for(const labels of [lim.labels,lim.maximum_labels]){
    const x=old.rowExact(labels),y=m.rowExact(labels);
    for(let j=0;j<x.length;j++){if(x[j].toString()!==y[j].g.evaluate(epsilon).str())throw Error("capture specialization");checks++;}
   }
   specializations.push({epsilon,exact_response:exact.exactValue,error_bound:error.str()});checks++;
  }
  reports.push({name:f.name,limit:lim.value,zero_leading_rewards:lim.zero_leading_rewards,nodes:lim.graph_nodes,arcs:lim.graph_arcs,specializations});
 }
 return{scope:"Exact integer limiting cut compared with the original rational integer oracle after specialization; no equilibrium claim.",reports,checks,arithmetic:G.stats()};
};