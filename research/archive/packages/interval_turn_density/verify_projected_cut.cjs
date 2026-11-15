"use strict";
const fs=require('fs'),path=require('path'),assert=require('assert');
const E=require('./atomic_survival_v8.cjs'),P=require('./projected_cut.cjs'),Q=E.Physical.Q;
const flag=process.argv.indexOf('--strategy');
const source=flag>=0?process.argv[flag+1]:path.join(__dirname,'../interval_refined_upper/strategy.json');
const seedData=JSON.parse(fs.readFileSync(source,'utf8'));
function family(kind,args){
  const q=args.map(x=>new Q(x));let p;
  if(kind==='M1'){const[x]=q;p=[[x,x.neg()],[new Q(2n).sub(x),x.neg()],[new Q(2n).sub(x),new Q(4n).sub(x)]];}
  else if(kind==='M2'){const[x,s]=q;p=[[x,x.neg()],[s,x.neg()],[s,s.add(2n)],[s.add(4n),s.add(2n)]];}
  else if(kind==='M3'){const[x,s,t]=q;p=[[x,x.neg()],[s,x.neg()],[s,t],[t.add(2n),t],[t.add(2n),t.add(4n)]];}
  else{const[a,v,s]=q;p=[[a,a.neg()],[a,v],[s,v],[s,s.add(2n)],[s.add(4n),s.add(2n)]];}
  return{kind,exact_light:p.map(r=>r.map(String))};
}
const atoms=seedData.families.map(a=>family(a.kind===1?'M1':'M2',a.kind===1?[a.start]:[a.start,'1']));
const extras=[family('M3',['-1/32','273/320','1']),family('I',['3/4','-11/16','31/32']),
              family('I',['15/16','-7/8','33/32']),family('M2',['-7/8','33/32'])];
const count=atoms.length;atoms.push(...extras);
const full=E.Rational.Model(atoms),projected=P.project(full),seed=atoms.map((_,j)=>j<count?seedData.families[j].weight_numerator/seedData.weight_denominator:0),
      mixed=seed.map((x,j)=>.8*x+(j>=count?.05:0)),single=atoms.map((_,j)=>j===count?1:0),
      early=seed.map((x,j)=>.5*x+(j===count+1?.5:0));
const fixtures=[['certified67',seed],['initial_inward_mixture',early],['four_family_mixture',mixed],['single_center_M3',single]],report=[];
for(const[name,w]of fixtures){
 const t=Date.now(),p=P.solve(projected,w,full),ordinary=E.Rational.sparseSolve(full,w,false);
 const error=Math.abs(p.value-ordinary.value);assert(error<3e-9);
 if(name==='certified67')assert(Math.abs(p.value-new Q(seedData.expected_upper).number())<3e-12);
 report.push({name,value:p.value,ordinary:ordinary.value,error,seconds:(Date.now()-t)/1000,nodes:p.nodes,arcs:p.arcs});
}
const out={scope:'Exact order projection; numerical cuts independently rescored by rational physical first capture.',
 oldThresholds:full.N,pricedThresholds:projected.N,projectedEdges:projected.threshold_hard.length,fixtures:report};
fs.writeFileSync('projected_cut_portable_verification.json',JSON.stringify(out,null,2));console.log(JSON.stringify(out,null,2));
