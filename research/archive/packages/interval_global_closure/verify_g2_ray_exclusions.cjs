"use strict";
/* Exact continuum exclusion of two attempted one-dimensional Monster
 * strategy updates using physical Princess cuts. This does not solve
 * the unrestricted game or exclude arbitrary new Monster supports.
 */
const fs=require("node:fs"),path=require("node:path");
const E=require("../interval_turn_density/atomic_survival_v8.cjs");
const Q=E.Physical.Q,Z=new Q(0),O=new Q(1);
const read=name=>JSON.parse(fs.readFileSync(path.join(__dirname,name),"utf8"));
const old=read("upper_dyadic_exact.json"),cuts=read("g2_near_active_princess_cuts.json"),
    best=read("../interval_common_warp/upper_warp_tight_exact.json"),
    inject=read("g2_m1_injection_witness.json");
if(cuts.rows.length!==4||cuts.rows.some(r=>r.length!==281))
 throw Error("expected four exact 281-route Princess cuts");
const Uold=new Q(old.value),Ubest=new Q(best.exact_value);
if(Ubest.cmp(Uold)>=0)throw Error("unexpected certified upper ordering");
// Monster weight reallocation from old atom 0 to old atom 120.
const a0=new Q(cuts.original_weighted_scores[0]),
      a3=new Q(cuts.original_weighted_scores[3]);
const slope0=new Q(cuts.rows[0][120]).sub(new Q(cuts.rows[0][0])),
      slope3=new Q(cuts.rows[3][120]).sub(new Q(cuts.rows[3][0]));
if(!(a0.cmp(a3)>0&&slope0.cmp(Z)<0&&slope3.cmp(Z)>0))
 throw Error("monotone exchange cut signs fail");
const delta=a0.sub(a3).div(slope3.sub(slope0)),
      validMax=new Q(old.atoms[0].weight_numerator,old.weight_denominator),
      minimumLowerBound=a0.add(slope0.mul(delta));
if(!(delta.cmp(Z)>0&&delta.cmp(validMax)<0&&minimumLowerBound.cmp(Ubest)>0))
 throw Error("uniform ray exclusion failed");
if(minimumLowerBound.cmp(a3.add(slope3.mul(delta)))!==0)
 throw Error("incorrect affine-cut crossing");
// For ANY 0<=x<=validMax, max(a0+slope0*x,a3+slope3*x)
// >= their intersection minimumLowerBound, by opposite monotonicities.
// No finite sampling is used to prove this continuum inequality.
const Ai=new Q(inject.oldLawScore),Bi=new Q(inject.addedRouteScore),
      lcrit=Uold.sub(Ai).div(Bi.sub(Ai));
if(!(Uold.cmp(Ai)>0&&Bi.cmp(Uold)>0&&
      lcrit.cmp(Z)>0&&lcrit.cmp(O)<0))
 throw Error("injection witness threshold invalid");
// The best *branch-wide* upper certificate is already BELOW the
// fixed physical Princess's baseline payoff. Because Bi>Ai,
// the full injection ray (including lambda=0) cannot beat it.
if(!(Ai.cmp(Ubest)>0&&Bi.cmp(Ai)>0))
 throw Error("full injection ray is not excluded against best upper");
const output={
 scope:"RIGOROUS CONTINUUM exclusions for two specified Monster weight-update rays; NOT a global equilibrium",
 fromAtom:0,toAtom:120,
 validTransferMass:["0",validMax.toString()],
 crossingTransfer:delta.toString(),
 crossingTransferDecimal:delta.number(),
 uniformPrincessResponseLowerBound:minimumLowerBound.toString(),
 uniformLowerDecimal:minimumLowerBound.number(),
 bestExistingGameUpper:Ubest.toString(),
 oldMonsterUpper:Uold.toString(),
 strictMargin:minimumLowerBound.sub(Ubest).toString(),
 strictMarginDecimal:minimumLowerBound.sub(Ubest).number(),
 transferRayExcludedAgainstBestUpper:true,
 addedMonsterInjectionThreshold:lcrit.toString(),
 injectionThresholdDecimal:lcrit.number(),
 injectionRayAboveThresholdExcludedAgainstOldUpper:true,
 fullInjectionRayExcludedAgainstBestUpper:true,
 fullInjectionRayLowerBound:Ai.toString(),
 fullInjectionRayLowerBoundDecimal:Ai.number(),
 fullInjectionMarginVsBest:Ai.sub(Ubest).toString()
};
if(require.main===module)console.log(JSON.stringify(output,null,2));
module.exports={verify:()=>output};
