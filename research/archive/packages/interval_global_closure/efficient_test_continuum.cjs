"use strict";
// Global numerical princess separation for a rational finite route law.
const fs=require('node:fs'),E=require('../interval_turn_density/atomic_survival_v8.cjs');
const prefix=process.argv[2],start=Date.now();
const bank=JSON.parse(fs.readFileSync(prefix+'.bank.json','utf8'));
const law=JSON.parse(fs.readFileSync(prefix+'.law.json','utf8'));
const model=new E.Rational.Model(bank.atoms);
console.error(JSON.stringify({event:'model',pairs:bank.atoms.length,queries:model.v.length,
  levels:model.base.length,threshold_nodes:model.N,seconds:(Date.now()-start)/1000}));
const answer=model.solve(law.weights,2e-13,{face:true});
const output={scope:'Numerical unrestricted princess response to a legal normalized rational finite monster law',
  source:prefix+'.law.json',value:answer.value,dual_value:answer.dualValue,
  query_v:model.v,event_labels:model.base.flatMap(b=>[-1,0,1].map(s=>[b,s])),
  minimum_labels:answer.labels,maximum_labels:answer.maxlabels,
  seconds:(Date.now()-start)/1000};
fs.writeFileSync(prefix+'.response.json',JSON.stringify(output)+'\n');
console.log(JSON.stringify({value:answer.value,dual_value:answer.dualValue,
  seconds:output.seconds,pairs:bank.atoms.length,queries:model.v.length,threshold_nodes:model.N}));
