"use strict";
const E=require("../interval_turn_density/atomic_survival_v8.cjs");
const W=require("./upper_warp.cjs");
const I=require("./upper_warp_integer.cjs");
const api=(function(E,W,I){

const Q=E.Physical.Q;
function verifyUpperWarp(sourceCertificate,candidate,options={}){
 const data=W.build(sourceCertificate);
 if(JSON.stringify(candidate.knots)!==JSON.stringify(data.knots))throw Error("warp knot mismatch");
 if(candidate.increment_numerators.length!==data.knots.length-1)throw Error("warp dimension");
 const dn=BigInt(candidate.increment_denominator),d=candidate.increment_numerators.map(n=>new Q(BigInt(n),dn));
 if(d.some(x=>x.n<=0n)||d.reduce((s,x)=>s.add(x),new Q(0n)).cmp(new Q(1n))!==0)throw Error("non-strict warp");
 const atoms=W.warpedAtoms(data,d.map(String));let mass=0n,vertices=0,legs=0;
 for(let j=0;j<atoms.length;j++){
  const atom=atoms[j],supplied=candidate.atoms[j];
  if(!supplied||atom.weight_numerator!==supplied.weight_numerator||JSON.stringify(atom.exact_light)!==JSON.stringify(supplied.exact_light))throw Error("physical law mismatch");
  mass+=BigInt(atom.weight_numerator);const p=atom.exact_light.map(x=>x.map(q=>new Q(q)));
  if(p[0][0].add(p[0][1]).n!==0n)throw Error("initial time");
  for(const[u,v]of p){if(u.sub(v).abs().cmp(new Q(2n))>0)throw Error("strip");vertices++;}
  for(let i=1;i<p.length;i++){const du=p[i][0].sub(p[i-1][0]),dv=p[i][1].sub(p[i-1][1]);if(du.n<0n||dv.n<0n||(du.n===0n)===(dv.n===0n))throw Error("unit leg");legs++;}
 }
 if(mass!==BigInt(data.denominator)||atoms.length!==candidate.atoms.length)throw Error("probability law");
 const replay=I.verify(data,candidate,candidate.flow_certificate,E.BigFlow.BigFlow,Q),value=new Q(replay.value);
 if(value.cmp(new Q(candidate.exact_value))!==0)throw Error("reported value");
 const featureRows=[W.features(data,candidate.minimum_labels),W.features(data,candidate.maximum_labels)];
 for(const f of featureRows){let n=0n;for(let k=0;k<d.length;k++)n+=BigInt(f.numerators[k])*BigInt(candidate.increment_numerators[k]);
  if(new Q(n,4n*BigInt(data.denominator)*dn).cmp(value)!==0)throw Error("capture-coordinate row");}
 const report={...replay,atoms:atoms.length,vertices,unit_legs:legs,weight_numerator:String(mass),weight_denominator:data.denominator,exact_capture_rows:2,increment_count:d.length,strict:true};
 if(options.physical!==false){
  const cum=[new Q(0n)];for(const x of d)cum.push(cum[cum.length-1].add(x));
  const index=new Map(data.knots.map((x,i)=>[x,i]));
  function warp(x){const f=W.fold(new Q(x)),i=index.get(String(f.radius));if(i===undefined)throw Error("missing coordinate");return new Q(BigInt(f.constant)).add(cum[i].mul(new Q(BigInt(f.sign))));}
  const vs=data.full.v.map(x=>String(warp(x))),base=data.full.base.map(x=>String(warp(x))),path=E.Physical.realize(vs,base,candidate.minimum_labels,"1/281474976710656",true);
  let payoff=new Q(0n),captures=0;const two=new Q(2n);
  for(const atom of atoms){let sum=new Q(0n);for(const reflect of[false,true]){const route=atom.exact_light.map(p=>{const u=new Q(p[reflect?1:0]),v=new Q(p[reflect?0:1]);return[String(u.add(v).div(two)),String(u.sub(v).div(two))];}),t=E.Physical.capture(path.path,route);if(t===null)throw Error("uncaught");sum=sum.add(t);captures++;}
   payoff=payoff.add(sum.mul(new Q(BigInt(atom.weight_numerator),2n*BigInt(data.denominator))));}
  const gap=value.sub(payoff);if(gap.n<0n||gap.cmp(new Q("1/10000000000"))>0)throw Error("physical approximation");
  report.physical_captures=captures;report.physical_vertices=path.pointCount;report.physical_epsilon=path.epsilon;report.physical_payoff=String(payoff);report.physical_gap=String(gap);report.physical_gap_decimal=gap.number();
 }
 return report;
}
return{verifyUpperWarp};

})(E,W,I);
module.exports=api;
if(require.main===module){
 const fs=require("fs"),path=require("path");
 const source=JSON.parse(fs.readFileSync(path.join(__dirname,"../interval_global_closure/upper_dyadic_exact.json"),"utf8"));
 const candidate=JSON.parse(fs.readFileSync(path.join(__dirname,"upper_warp_exact.json"),"utf8"));
 console.log(JSON.stringify(api.verifyUpperWarp(source,candidate),null,2));
}
