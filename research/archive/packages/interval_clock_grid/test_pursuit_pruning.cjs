"use strict";
// Deterministic legal nodal fields built from actual stopped radial paths.
// Compare the pursuit verifier with the same exact oracle with pursuit disabled.
const {verifyNormalizedDual}=require("./normalized_record_pricing.cjs");
function fixture(n,seed){
 const R=2*n,C=4*n,H=12*n,weights=[37,113,251,599],paths=[];
 let random=seed>>>0;
 function bit(){random^=random<<13;random^=random>>>17;random^=random<<5;return random>>>0;}
 for(let a=0;a<weights.length;a++){
  const p=[bit()%(R+1)];
  for(let j=0;j<H;j++){
   const x=p[j];
   p.push(x===R?R:j>=C?x+1:x===0?1:x+(bit()%2?1:-1));
  }
  paths.push(p);
 }
 const radial_nodes=[];
 for(let j=0;j<=H;j++)for(let k=1;k<=R;k++)if((j+k)%2===0){
  let g=0;for(let a=0;a<paths.length;a++)if(paths[a][j]<k)g+=weights[a];
  radial_nodes.push([j,k,String(g)]);
 }
 return {n,field_denominator:"1000",normalized_profile:true,radial_nodes};
}
function test(){
 const cases=[];let rejected=0;
 for(const n of [1,2,3,4,6])for(const seed of [101,2027,65537,314159]){
  const c=fixture(n,seed),plain=verifyNormalizedDual(c,{pursuit:false}),pruned=verifyNormalizedDual(c),target=verifyNormalizedDual(c,{targetUnits:BigInt(plain.verified_lower_units)});
  if(!plain.qout_verified||plain.verified_lower_units!==pruned.verified_lower_units||plain.verified_lower_units!==target.verified_lower_units)throw Error("pursuit mismatch");
  let failed=false;
  try{verifyNormalizedDual(c,{targetUnits:BigInt(plain.verified_lower_units)+1n});}
  catch(error){if(!/target lower bound fails: complete normalized path/.test(error.message))throw error;failed=true;}
  if(!failed)throw Error("incorrect target accepted");rejected++;
  cases.push({n,seed,minimum_units:plain.verified_lower_units,unpruned_states:plain.record_states,pruned_states:pruned.record_states,target_states:target.record_states,target_pursuit_pruned:target.pursuit_pruned_states});
 }
 return {status:"PASS",scope:"Exact pursuit/no-pursuit comparison on deterministic legal Qout fields, plus one-unit false-target rejection",cases:cases.length,incorrect_targets_rejected:rejected,results:cases};
}
module.exports={fixture,test};
if(require.main===module)console.log(JSON.stringify(test(),null,2));
