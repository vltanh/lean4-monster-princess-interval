"use strict";
const {Q,makeStrategy,createEvaluator,buildProfile,verifyExtraction}=require("./extract_princess.cjs");
function verifySamples(certificate,strategy){
 const report=verifyExtraction(certificate,strategy),n=certificate.n;
 const p=buildProfile(certificate),ev=createEvaluator(strategy);
 let closure=0,nodes=0,symmetry=0,transport=0,outward=0;
 for(const [a,k,v] of p.nodes){
  let expected=0n;
  for(const [aa,kk,dd] of certificate.discounts)if(kk>0&&k>=kk+Math.abs(a-aa)){
   const raw=BigInt(dd),d=raw>p.D?p.D:raw,u=p.D-d;
   if(u>expected)expected=u;
  }
  if(BigInt(v)!==expected)throw Error("adjacent closure differs from full containment");
  closure++;
  const value=ev.rawTrace(new Q(BigInt(a),BigInt(2*n)),new Q(BigInt(k),BigInt(2*n)));
  if(value.cmp(new Q(p.D+BigInt(v),2n*p.D))!==0)throw Error("nodal interpolation");
  nodes++;
 }
 const B=8*n,step=new Q(1n,BigInt(B));
 for(let a=0;a<=3*B;a++)for(let k=-B;k<=B;k++){
  const t=new Q(BigInt(a),BigInt(B)),x=new Q(BigInt(k),BigInt(B));
  const value=ev.interiorTrace(t,x);
  if(value.add(ev.interiorTrace(t,new Q(BigInt(-k),BigInt(B)))).cmp(1)!==0)throw Error("reflection symmetry");
  symmetry++;
  if(k>-B){
   if(ev.interiorTrace(t.add(step),x.sub(step)).cmp(value)>0)throw Error("left transport");
   transport++;
  }
  if(k<B){
   if(ev.interiorTrace(t.add(step),x.add(step)).cmp(value)<0)throw Error("right transport");
   transport++;
  }
  if(a>=2*B&&k>=0&&k<B){
   if(ev.interiorTrace(t.add(step),x.add(step)).cmp(value)!==0)throw Error("outward characteristic");
   outward++;
  }
 }
 return {...report,checks:{closure,nodes,symmetry,transport,outward},
  scope:"The exact finite dual and regenerated extraction certify the stated guarantee. Sampled CDF checks are implementation regressions; the extraction proof establishes legality on the entire continuous strip."};
}
module.exports={verifySamples};
if(require.main===module){
 const fs=require("node:fs"),path=require("node:path");
 try{
  const certificate=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"grid_n2_certificate.json"),"utf8"));
  const strategy=process.argv[3]?JSON.parse(fs.readFileSync(process.argv[3],"utf8")):makeStrategy(certificate,"1/"+(2*certificate.n));
  process.stdout.write(JSON.stringify(verifySamples(certificate,strategy),null,2)+"\n");
 }catch(error){process.stderr.write(error.stack+"\n");process.exitCode=1;}
}
