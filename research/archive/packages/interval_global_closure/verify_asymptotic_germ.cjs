/** Regression for objective-only asymptotic pruning. */
module.exports = function verifyAsymptotic(G,createAsymptoticSearch,fixtures){
 const S=createAsymptoticSearch(G),records=[];
 for(const fixture of fixtures)for(const mode of ["raw","sorted"]){
  const exact=new G.CaptureSearch(fixture.paths,fixture.weights,{mode,prune:false});
  const asym=new S(fixture.paths,fixture.weights,{mode});
  while(!exact.runSlice(10000,1000)){}
  while(!asym.runSlice(10000,1000)){}
  const e=exact.result(),r=asym.result(),v=G.Q(e.value);
  const lo=G.Q(r.asymptotic.lower_value),hi=G.Q(r.asymptotic.upper_value);
  if(!e.complete||!r.asymptotic.certified||lo.cmp(v)>0||v.cmp(hi)>0||
      !lo.limit().eq(v.limit())||!hi.limit().eq(v.limit()))throw Error("invalid sandwich: "+fixture.name);
  records.push({name:fixture.name,mode,limit:v.limit().str(),lower:lo.str(),upper:hi.str(),
   exact:v.str(),exact_nodes:e.stats.nodes,asymptotic_nodes:r.stats.nodes,
   exact_germ_optimum:r.exact_germ_optimum,pruned_bounds:asym.proofBounds()});
 }
 return{scope:"Completed limiting-response regression, not a full-game certificate",
  records,arithmetic:G.stats()};
};