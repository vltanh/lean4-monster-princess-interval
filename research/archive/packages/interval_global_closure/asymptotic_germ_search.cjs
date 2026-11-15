/** Limit-only objective pruning around the exact QQ(epsilon) capture-order search.
 * Geometry, contacts, arrival-time comparisons, and Pareto dominance are unchanged.
 * A stopped search is an attack only. Completion certifies the limiting response,
 * with a finite uniform germ sandwich, not necessarily the full germ optimum.
 */
module.exports = (function(){
function createAsymptoticSearch(G){
 const needle="if(this.options.prune!==false&&lb.cmp(this.best)>=0){this.stats.bounded++;return true;}";
 const original=G.CaptureSearch.prototype.step.toString();
 if(original.split(needle).length!==2)throw Error("unrecognized objective pruning gate");
 const replacement="if(this.options.prune!==false&&lb.limit().cmp(this.best.limit())>=0){this.asymptoticBounds.push(lb);this.stats.bounded++;return true;}";
 const patched=original.replace(needle,replacement);
 const step=Function("return function "+patched)();
 class AsymptoticCaptureSearch extends G.CaptureSearch{
  constructor(raw,weights,options={}){
   super(raw,weights,options);
   this.asymptoticBounds=[];
   this.proofMode="exact geometry with limit-only objective pruning";
  }
  result(check=true){
   const out=super.result(check),finished=this.complete&&!this.stopReason;
   out.proof_mode=this.proofMode;
   out.exact_germ_optimum=false;
   out.asymptotic={certified:finished,pruned_bound_count:this.asymptoticBounds.length};
   if(finished){
    let lower=this.best;
    for(const b of this.asymptoticBounds)if(b.cmp(lower)<0)lower=b;
    const normalizedLower=lower.dby(this.W),normalizedUpper=this.best.dby(this.W);
    if(normalizedLower.limit().cmp(normalizedUpper.limit())!==0)throw Error("limit sandwich mismatch");
    out.asymptotic.lower_value=normalizedLower.str();
    out.asymptotic.upper_value=normalizedUpper.str();
    out.asymptotic.limit=normalizedUpper.limit().str();
    out.asymptotic.limit_decimal=normalizedUpper.limit().num();
    out.exact_germ_optimum=normalizedLower.eq(normalizedUpper);
   }
   out.uniform_comparison_radius=G.stats().radius;
   return out;
  }
  proofBounds(){
   return this.asymptoticBounds.map(b=>b.dby(this.W).str());
  }
 }
 AsymptoticCaptureSearch.prototype.step=step;
 AsymptoticCaptureSearch.audit={original_step:original,patched_step:patched,
  changed_gate_count:1,source_core:"51dbac43b59c3041abf831837dc58fde2a9294b2",
  source_germ:"b7e9accdfa1471a6dc4b348e582abbcc9059172b"};
 return AsymptoticCaptureSearch;
}
return {createAsymptoticSearch};
})();