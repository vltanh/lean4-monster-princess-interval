"use strict";
/* Exact G2 Princess separation-cut screen for fixed route-bank Monster weights.
 * This is a safe REJECTION test, never a Monster upper certificate.
 *
 * node packages/interval_global_closure/g2_princess_cut_screen.cjs --baseline
 * node packages/interval_global_closure/g2_princess_cut_screen.cjs --inject 1/100
 * node packages/interval_global_closure/g2_princess_cut_screen.cjs --transfer 0 120 300000
 * node packages/interval_global_closure/g2_princess_cut_screen.cjs --weights candidate.json
 */
const fs=require("node:fs"),path=require("node:path");
const E=require("../interval_turn_density/atomic_survival_v8.cjs");
const Q=E.Physical.Q,Z=new Q(0),O=new Q(1);
const read=s=>JSON.parse(fs.readFileSync(path.join(__dirname,s),"utf8"));
const old=read("upper_dyadic_exact.json"),cuts=read("g2_near_active_princess_cuts.json");
if(!Array.isArray(cuts.rows)||cuts.rows.length<4||
   cuts.rows.some(r=>r.length!==old.atoms.length+1))
 throw Error("mismatched physical Princess cut bank");
const D=new Q(old.weight_denominator),n=old.atoms.length;
function weightsFor(args) {
 const base=old.atoms.map(a=>new Q(a.weight_numerator).div(D)).concat(Z);
 if(args[0]==="--baseline"||!args.length)return base;
 if(args[0]==="--inject"){
   const lam=new Q(args[1]||"1/100");
   if(lam.cmp(Z)<0||lam.cmp(O)>0)throw Error("invalid injection");
   return base.map((w,i)=>i<n?w.mul(O.sub(lam)):lam);
 }
 if(args[0]==="--transfer") {
   const from=Number(args[1]),to=Number(args[2]);
   const mass=new Q(args[3]).div(D);
   if(!Number.isInteger(from)||!Number.isInteger(to)||from<0||to<0||
      from>=n||to>=n||from===to)throw Error("invalid transfer indices");
   base[from]=base[from].sub(mass);base[to]=base[to].add(mass);
   return base;
 }
 if(args[0]==="--weights"){
   const data=JSON.parse(fs.readFileSync(args[1],"utf8"));
   if(!Array.isArray(data)||data.length!==n+1)throw Error("expected 281 rational weights");
   return data.map(x=>new Q(x));
 }
 throw Error("unknown argument format");
}
function score(weights){
 if(weights.length!==n+1)throw Error("wrong route count");
 let sum=Z;for(const v of weights){if(v.cmp(Z)<0)throw Error("negative mass");sum=sum.add(v);}
 if(sum.cmp(O)!==0)throw Error("not a probability law");
 const values=cuts.rows.map(r=>{
   let v=Z;for(let j=0;j<weights.length;j++)if(weights[j].cmp(Z)>0)
      v=v.add(weights[j].mul(new Q(r[j])));return v;
 });
 let worst=values[0],arg=0;
 for(let k=1;k<values.length;k++)if(values[k].cmp(worst)>0){worst=values[k];arg=k;}
 return {
   scope:"Certified LOWER bound on unrestricted Princess response to proposed Monster weights, not an upper bound or a saddle",
   routeCount:weights.length,
   physicalPrincessColumns:cuts.column_names,
   columnScores:values.map(v=>v.toString()),
   columnScoresDecimal:values.map(v=>v.number()),
   provenPrincessLowerBound:worst.toString(),
   lowerBoundDecimal:worst.number(),
   activeAdversarialColumn:cuts.column_names[arg],
   oldMonsterFullPrincessCeiling:old.value,
   strictRejection:worst.cmp(new Q(old.value))>0,
   captureChecksPinned:cuts.physical_first_contacts_checked
 };
}
const output=score(weightsFor(process.argv.slice(2)));
if(require.main===module)console.log(JSON.stringify(output,null,2));
module.exports={weightsFor,score};
