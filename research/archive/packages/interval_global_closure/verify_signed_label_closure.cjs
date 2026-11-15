"use strict";
function verifySignedLabelClosure(E,M){
 const Q=E.Physical.Q,S=M.createSignedLabelClosure(E),counts={games:0,feasible_assignments:0,exact_values:0,extremal_faces:0,float_replays:0,infeasible_bounds:0};
 let seed=1941;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
 for(let test=0;test<180;test++){
   const L=2+rnd(5),R=1+rnd(6),labels=Array.from({length:L},(_,i)=>[i,0]),rowBounds=[],unaryValues=[];
   for(let i=0;i<R;i++){let lo=rnd(L),hi=lo+rnd(L-lo);if(test%3===0){lo=0;hi=L-1;}rowBounds.push([lo,hi]);unaryValues.push(Array.from({length:L},()=>new Q(BigInt(rnd(17)-8),BigInt(1+rnd(7))).toString()));}
   const input={labels,rowBounds,unaryValues},result=S.maximize(input),best={value:null,min:null,max:null};
   function visit(xs){let i=xs.length;if(i===R){counts.feasible_assignments++;let q=new Q(0);for(let j=0;j<R;j++)q=q.add(new Q(unaryValues[j][xs[j]]));if(best.value===null||q.cmp(best.value)>0){best.value=q;best.min=xs.slice();best.max=xs.slice();}else if(!q.cmp(best.value)){best.min=xs.map((x,j)=>Math.min(x,best.min[j]));best.max=xs.map((x,j)=>Math.max(x,best.max[j]));}return;}
    for(let k=Math.max(rowBounds[i][0],i?xs[i-1]:0);k<=rowBounds[i][1];k++)visit([...xs,k]);
   }
   visit([]);counts.games++;
   if(best.value===null){if(result.status!=="infeasible")throw Error("missed infeasibility");counts.infeasible_bounds++;continue;}
   if(result.status!=="optimal"||new Q(result.value).cmp(best.value))throw Error("wrong exact optimum");counts.exact_values++;
   if(JSON.stringify(result.minimum_labels)!==JSON.stringify(best.min)||JSON.stringify(result.maximum_labels)!==JSON.stringify(best.max))throw Error("wrong optimal lattice extremum");counts.extremal_faces+=2;
   const short={...input,unaryValues:unaryValues.map((r,i)=>r.slice(rowBounds[i][0],rowBounds[i][1]+1))},sr=S.maximize(short);
   if(sr.value!==result.value)throw Error("bounded unary encoding mismatch");counts.exact_values++;
   if(test%5===0){let f=S.maximize({...input,mode:"float",tolerance:1e-13});if(Math.abs(f.decimal-best.value.number())>1e-10||f.witness_error>1e-10)throw Error("float replay mismatch");counts.float_replays++;}
 }
 const zero=S.maximize({labels:[0,1,2],rowBounds:[[0,2],[0,2],[0,2]],unaryValues:[[0,0,0],[0,0,0],[0,0,0]]});
 if(zero.minimum_labels.some(x=>x!==0)||zero.maximum_labels.some(x=>x!==2))throw Error("flat face");
 return{status:"PASS",scope:"Generic signed unary order-label closure only; no physical response theorem is assumed.",counts};
}
module.exports={verifySignedLabelClosure};

if(typeof require!=="undefined"&&require.main===module){const E=require("../interval_turn_density/atomic_survival_v8.cjs"),M=require("./signed_label_closure.cjs");console.log(JSON.stringify(verifySignedLabelClosure(E,M),null,2));}
