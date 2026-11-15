"use strict";
/* Exact physical first-contact replay of the G2 near-active Princess witness.
 *
 * This certifies a SINGLE Princess path that defeats an attempted Monster
 * mixture. It does not establish the mixed Monster's exact optimum, and it
 * is not a new unrestricted game bound.
 */
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const E=require("../interval_turn_density/atomic_survival_v8.cjs");
const Q=E.Physical.Q,half=new Q("1/2"),zero=new Q(0);
const read=name=>fs.readFileSync(path.join(__dirname,name),"utf8");
const monsterText=read("upper_dyadic_exact.json");
const hash=crypto.createHash("sha1").update("blob "+Buffer.byteLength(monsterText)+"\0").update(monsterText).digest("hex");
if(hash!=="188b8b43fad7c69cafb42195d69d045cb44e8f23")
  throw Error("source Monster law blob changed");
const baseline=JSON.parse(monsterText);
const witness=JSON.parse(read("g2_m1_injection_witness.json"));
if(witness.base_law!=="upper_dyadic_exact.json")throw Error("source mismatch");
const atoms=baseline.atoms.concat([{exact_light:witness.new_route_exact_light}]);
const model=new E.Rational.Model(atoms);
const realize=E.Physical.realize(model.v,model.base,witness.labels,witness.epsilon,true);
if(realize.pointCount!==witness.realization_vertices)throw Error("unexpected Princess vertex count");
const princess=realize.path;
let old=zero,added=null,captureChecks=0,wsum=0n;
const den=new Q(baseline.weight_denominator),two=new Q(2);
for(let i=0;i<atoms.length;i++){
  const item=atoms[i],light=item.exact_light.map(pair=>pair.map(q=>new Q(q)));
  const plus=light.map(([u,v])=>[u.add(v).div(two),u.sub(v).div(two)]);
  const minus=plus.map(([t,x])=>[t,x.neg()]);
  const tp=E.Physical.capture(princess,plus),tm=E.Physical.capture(princess,minus);
  if(tp===null||tm===null)throw Error("incomplete endpoint capture");
  captureChecks+=2;
  const score=tp.add(tm).div(two);
  if(i<baseline.atoms.length){
    const w=BigInt(item.weight_numerator);
    if(w<=0n)throw Error("nonpositive original weight");
    wsum+=w;old=old.add(score.mul(new Q(w).div(den)));
  }else added=score;
}
if(wsum!==BigInt(baseline.weight_denominator))throw Error("normalization");
const mixed=old.mul(new Q(witness.old_mass_fraction))
               .add(added.mul(new Q(witness.new_mass_fraction)));
if(old.toString()!==witness.oldLawScore)throw Error("old law score changed");
if(added.toString()!==witness.addedRouteScore)throw Error("added Monster score changed");
if(mixed.toString()!==witness.mixedScore)throw Error("mixed score changed");
const U=new Q(baseline.value),lamcrit=U.sub(old).div(added.sub(old));
if(!(U.cmp(old)>0&&added.cmp(U)>0&&mixed.cmp(U)>0))
  throw Error("strict directional separation failed");
const output={
 scope:"Verified exact physical witness; NOT a full Monster upper certificate",
 baseValue:U.toString(),oldPrincessScore:old.toString(),
 addedMonsterScore:added.toString(),mixedPrincessScore:mixed.toString(),
 exactExclusionThreshold:lamcrit.toString(),
 thresholdDecimal:lamcrit.number(),mixedScoreDecimal:mixed.number(),
 strictWorsening:true,captureChecks,princessVertices:princess.length
};
console.log(JSON.stringify(output,null,2));
module.exports={verify:()=>output};
