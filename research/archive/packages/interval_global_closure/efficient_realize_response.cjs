"use strict";
// Export actual legal epsilon responses to a finite Monster law. Rational
// segment-intersection recapture checks their payoff, independently of cuts.
const fs=require('node:fs'),E=require('../interval_turn_density/atomic_survival_v8.cjs');
const {Q}=E.Physical,two=new Q(2n),prefix=process.argv[2];let epsilon=process.argv[3]||'1/18446744073709551616';
const response=JSON.parse(fs.readFileSync(prefix+'.response.json','utf8'));
const bank=JSON.parse(fs.readFileSync(prefix+'.bank.json','utf8'));
const law=JSON.parse(fs.readFileSync(prefix+'.law.json','utf8'));
const bases=response.event_labels.filter((_,j)=>j%3===0).map(x=>x[0]),paths=[];
for(const key of ['minimum_labels','maximum_labels']){
  const realization=E.Physical.realize(response.query_v,bases,response[key],epsilon,true);
  let payoff=0,maxCapture=0,tail3=0;
  for(let j=0;j<bank.atoms.length;j++)for(const reflect of[false,true]){
    const monster=bank.atoms[j].exact_light.map(([a,b])=>{const u=new Q(a),v=new Q(b);
      return[u.add(v).div(two).toString(),(reflect?v.sub(u):u.sub(v)).div(two).toString()];});
    const capture=E.Physical.capture(realization.path,monster);
    if(capture===null)throw Error('complete sweep missed response');
    const time=capture.number();payoff+=law.weights[j]*time/2;maxCapture=Math.max(maxCapture,time);
    if(time>3)tail3+=law.weights[j]/2;
  }
  paths.push({source_profile:key,weight:0.5,route:realization.path,epsilon,
    strictEta:realization.strictEta,payoff_against_source_law:payoff,max_capture:maxCapture,mass_capture_after3:tail3});
}
const output={scope:'Two legal folded Princess paths, each symmetrized by fair reflection when used as a law. Rational contact checks; numerical source weights.',
  source:prefix+'.law.json',global_response_supremum:response.value,paths};
fs.writeFileSync(prefix+'.princess_paths.json',JSON.stringify(output)+'\n');
console.log(JSON.stringify(paths.map(({route,...rest})=>({...rest,vertices:route.length})),null,2));
