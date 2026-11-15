"use strict";
/* Rebuild all G2 Princess cuts from actual legal physical trajectories
 * and exact chronological first contacts (BigInt rational arithmetic).
 * The minimax value remains unknown; this verifies only lower cuts.
 */
const fs=require("node:fs"),path=require("node:path");
const E=require("../interval_turn_density/atomic_survival_v8.cjs");
const Q=E.Physical.Q,Z=new Q(0),TWO=new Q(2),read=n=>JSON.parse(fs.readFileSync(path.join(__dirname,n),"utf8"));
const base=read("upper_dyadic_exact.json"),
      bank=read("g2_near_active_princess_cuts.json"),
      witness1=read("g2_m1_injection_witness.json"),
      witness3=read("g2_sweep_reweight_witness.json"),
      witness4=read("g2_balanced_shift_witness.json"),
      response=read("upper_dyadic_princess_response.json");
const extended=base.atoms.concat([{exact_light:bank.appended_monster_exact_light}]);
const bigModel=new E.Rational.Model(extended),oldModel=new E.Rational.Model(base.atoms);
const paths=[
 E.Physical.realize(bigModel.v,bigModel.base,witness1.labels,witness1.epsilon,true).path,
 response.princess_route,
 E.Physical.realize(oldModel.v,oldModel.base,witness3.labels,witness3.epsilon,true).path,
 E.Physical.realize(oldModel.v,oldModel.base,witness4.labels,witness4.epsilon,true).path
];
for(let k=0;k<paths.length;k++)if(paths[k].length<2)throw Error("empty Princess route");
if(bank.rows.length!==paths.length)throw Error("Princess column count");
let checks=0,oldScores=[];
const den=new Q(base.weight_denominator);
for(let k=0;k<paths.length;k++){
 let oldScore=Z;
 for(let j=0;j<extended.length;j++){
   const light=extended[j].exact_light.map(pair=>pair.map(q=>new Q(q)));
   const plus=light.map(([u,v])=>[u.add(v).div(TWO),u.sub(v).div(TWO)]);
   const minus=plus.map(([t,x])=>[t,x.neg()]);
   const a=E.Physical.capture(paths[k],plus),b=E.Physical.capture(paths[k],minus);
   if(a===null||b===null)throw Error("uncaught Princess path");
   const q=a.add(b).div(TWO);
   if(q.toString()!==bank.rows[k][j])throw Error("changed cut "+k+" "+j);
   checks+=2;
   if(j<base.atoms.length)oldScore=oldScore.add(q.mul(new Q(base.atoms[j].weight_numerator).div(den)));
 }
 if(oldScore.toString()!==bank.original_weighted_scores[k])throw Error("weighted Princess payoff mismatch");
 oldScores.push(oldScore);
}
if(checks!==bank.physical_first_contacts_checked||checks!==2248)throw Error("wrong audit count");
function transferScore(column,destination,numerator){
 const delta=new Q(numerator).div(den);
 return oldScores[column].add(delta.mul(
       new Q(bank.rows[column][destination]).sub(new Q(bank.rows[column][0]))));
}
if(transferScore(2,120,witness3.move_exact_numerator).toString()!==witness3.reweighted_score)
 throw Error("third column shifted score");
if(transferScore(3,120,witness4.moved_mass_numerator).toString()!==witness4.shifted_score)
 throw Error("fourth column shifted score");
if(oldScores[0].toString()!==witness1.oldLawScore)throw Error("first column source mismatch");
if(oldScores[1].toString()!==response.actual_princess_payoff)throw Error("second column source mismatch");
const report={
 scope:"Four exact global Princess separation cuts independently recomputed from physical routes",
 princessColumns:paths.length,monsterPairs:extended.length,
 chronologicalFirstContacts:checks,allExactScoresMatched:true,
 oldPayoffs:oldScores.map(q=>q.toString())
};
if(require.main===module)console.log(JSON.stringify(report,null,2));
module.exports={verify:()=>report};
