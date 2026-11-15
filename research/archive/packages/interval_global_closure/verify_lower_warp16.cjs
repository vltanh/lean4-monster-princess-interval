#!/usr/bin/env node
'use strict';
/*
 Independent exact supplied-law NO-GO certificate:
 every odd, strictly increasing, 2-periodic light-coordinate warp with 16
 uniform knots applied to the archived 338 Princess paths is attacked by an
 explicit legal Monster mixture. This proves a restricted-family ceiling, NOT
 a full-game upper or a better lower bound.
*/
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'../..');
const api=(new Function(fs.readFileSync(path.join(__dirname,'common_warp_lower_bigint.cjs'),'utf8')))();
const L=JSON.parse(fs.readFileSync(path.join(ROOT,'packages/interval_uniform_reduction/princess_strategy.json'),'utf8'));
const C=JSON.parse(fs.readFileSync(path.join(__dirname,'common_warp_lower_16.cert.json'),'utf8'));
const assert=(p,s)=>{if(!p)throw Error(s);};
const frac=s=>s.split('/').map(BigInt);
const S=L.S, n=C.bin_count, h=S/n,denWeight=BigInt(C.monster_weight_denominator);
assert(S===C.S&&S%n===0&&n===16,"source or geometry mismatch");
let sum=0n;let D=null;const cols=Array(n).fill(0n);
for(let i=0;i<C.monster_routes.length;i++){
 const {name,vertices,weight_numerator}=C.monster_routes[i];
 const weight=BigInt(weight_numerator);assert(weight>0n,"nonpositive monster weight");
 sum+=weight;
 assert(vertices.length>=2&&vertices[0][0]===0,"bad Monster start");
 let hitMinus=false,hitPlus=false;
 for(const [t,x] of vertices){
   assert(Number.isSafeInteger(t)&&Number.isSafeInteger(x)&&Math.abs(x)<=S,"illegal vertex");
   if(x===-S)hitMinus=true;
   if(x===S)hitPlus=true;
 }
 assert(hitMinus&&hitPlus,"Monster route must visit both endpoints");
 for(let j=1;j<vertices.length;j++){
   const dt=vertices[j][0]-vertices[j-1][0], dx=vertices[j][1]-vertices[j-1][1];
   assert(dt>0&&Math.abs(dx)===dt,"Monster route has a non-unit segment");
 }
 const f=api.featuresInteger(L,vertices,n);
 if(D===null)D=f.den;
 assert(D===f.den && f.events.length===338,"wrong exact contact dimensions");
 for(let j=0;j<n;j++)cols[j]+=weight*f.sums[j];
}
assert(sum===denWeight,"Monster probabilities do not normalize");
const max=cols.reduce((a,b)=>a>b?a:b),den=D*denWeight;
const [upperN,upperD]=frac(C.exact_ceiling);
assert(max*upperD===upperN*den,"exact worst-bin ceiling mismatch");
const [origN,origD]=frac(C.original_lower);
const [gapN,gapD]=frac(C.exact_improvement_ceiling);
assert(gapN*den*origD===(max*origD-origN*den)*gapD,"exact gap mismatch");
assert(max*origD>origN*den,"original law is below the family ceiling");
assert((max*origD-origN*den)*1000000000n<7n*den*origD,"gap must be < 7e-9");
// The archived attaining Monster has exactly the original certified score.
const x=api.featuresInteger(L,L.attaining_monster,n);
const refNum=x.sums.reduce((a,b)=>a+b,0n),refDen=x.den*BigInt(n);
assert(refNum*origD===origN*refDen,"archived exact lower oracle reference mismatch");
console.log(JSON.stringify({
 status:"PASS",scope:C.scope,
 princess_paths:338,monster_routes:C.monster_routes.length,
 contact_checks:338*C.monster_routes.length,
 bin_count:n,ceiling:api.printRat(max,den),
 original_value:C.original_lower,
 ceiling_minus_original:api.printRat(max*origD-origN*den,den*origD),
 restricts:"Every warp with nonnegative piecewise-linear increments summing to 1",
 full_game_saddle:false
},null,2));
