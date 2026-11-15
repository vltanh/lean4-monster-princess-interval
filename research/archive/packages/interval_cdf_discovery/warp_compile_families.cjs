
function compileWarpFamilies(E,W,A,field,warp,{verifyQuarter=true,onProgress=()=>{}}={}){
 const {Q,ZERO,ONE}=E,cache=new Map(),cells=[];let featureCalls=0,coefficientChecks=0,identityChecks=0;
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const r=a%b;a=b;b=r;}return a;}
 function compact(v){let d=1n;for(const x of v)d=d/gcd(d,x.d)*x.d;return{denominator:String(d),numerators:v.map(x=>String(x.n*(d/x.d)))};}
 function feature(family,positive,a){
  const key=family+"|"+positive+"|"+a.str();if(cache.has(key))return cache.get(key);
  const route=family==="m1"?A.m1Route(a,positive):A.fixedRoute(a,positive);
  const f=W.captureFeatures(field,warp,route);featureCalls++;
  const expected=family==="m1"?(positive?field.positiveM1(a):field.negativeM1(a)):field.fixedOne(a,positive);
  if(!f.identityCost.eq(expected))throw Error("identity feature mismatch "+key);identityChecks++;
  cache.set(key,f.coefficients);return f.coefficients;
 }
 for(const family of ["m1","fixed_one"])for(const positive of [false,true]){
  const cuts=family==="m1"?A.m1Cuts(field,positive):A.fixedCuts(field,positive);
  for(let j=0;j+1<cuts.length;j++){
   const left=cuts[j],right=cuts[j+1],c0=feature(family,positive,left),cm=feature(family,positive,left.a(right).dby(2)),c1=feature(family,positive,right);
   const qa=c0.map((x,i)=>c1[i].s(cm[i].m(2)).a(x).m(2)),qb=c0.map((x,i)=>c1[i].s(x).s(qa[i]));
   if(verifyQuarter){const actual=feature(family,positive,left.m(3).a(right).dby(4));for(let i=0;i<warp.n;i++){if(!actual[i].eq(c0[i].a(qb[i].dby(4)).a(qa[i].dby(16))))throw Error("basis quadratic mismatch "+family+"|"+positive+"|"+j+"|"+i);coefficientChecks++;}}
   cells.push({family,positive,interval:[left.str(),right.str()],constant:compact(c0),linear:compact(qb),quadratic:compact(qa)});
   if(cells.length%20===0)onProgress({cells:cells.length,featureCalls,coefficientChecks});
  }
 }
 return{scope:"Complete exact continuous-start M1 and fixed-U1 M2 warp quadratics on fixed reference geometry; coefficients linear in warp increments. Other monster families remain separate.",knots:warp.knots.map(x=>x.str()),cells,verification:{feature_calls:featureCalls,identity_checks:identityChecks,basis_quarter_checks:coefficientChecks}};
}
module.exports = {compileWarpFamilies};
