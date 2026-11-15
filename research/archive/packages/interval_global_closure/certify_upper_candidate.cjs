"use strict";
// Turn floating discovery weights into a different, explicit rational law,
// then solve and independently replay its unrestricted princess response.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const E=require('../interval_turn_density/atomic_survival_v8.cjs');
const {Q}=E.Physical,zero=new Q(0n),one=new Q(1n),two=new Q(2n);
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');

function validate(atoms,den){
  let total=0n;
  for(const a of atoms){
    const w=BigInt(a.weight_numerator);if(w<=0n)throw Error('nonpositive atom');total+=w;
    const route=a.exact_light.map(p=>p.map(x=>new Q(x)));
    if(route[0][0].add(route[0][1]).cmp(zero)!==0)throw Error('nonzero initial time');
    const walls=new Set();
    for(let i=0;i<route.length;i++){
      const[u,v]=route[i];if(u.add(v).cmp(zero)<0||u.sub(v).abs().cmp(two)>0)throw Error('illegal vertex');
      if(u.sub(v).abs().cmp(two)===0)walls.add(u.sub(v).toString());
      if(i){const[s,t]=route[i-1];if(!((u.cmp(s)>0&&v.cmp(t)===0)||(v.cmp(t)>0&&u.cmp(s)===0)))throw Error('non-unit leg');}
    }
    if(walls.size!==2)throw Error('incomplete endpoint sweep');
  }
  if(total!==BigInt(den))throw Error('probability normalization');
}

function verify(c){
  validate(c.atoms,c.weight_denominator);
  const model=new E.Rational.Model(c.atoms),weights=c.atoms.map(a=>a.weight_numerator);
  if(JSON.stringify(model.v)!==JSON.stringify(c.query_v)||JSON.stringify(model.base)!==JSON.stringify(c.base_levels))throw Error('changed event geometry');
  const result=E.Integer.verifyIntegerFlow(E.Cut,E.Physical,E.BigFlow.BigFlow,model,weights,c.weight_denominator,c.flow_certificate);
  if(result.exactValue!==c.value)throw Error('flow value');
  for(const labels of[c.minimum_labels,c.maximum_labels]){
    for(let i=0;i<labels.length;i++)if(labels[i]<model.bounds[i][0]||labels[i]>model.bounds[i][1]||(i&&labels[i]<labels[i-1]))throw Error('illegal response labels');
    let value=zero;const row=model.rowExact(labels);
    for(let j=0;j<row.length;j++)value=value.add(row[j].mul(new Q(BigInt(weights[j]),BigInt(c.weight_denominator))));
    if(value.toString()!==c.value)throw Error('exact response payoff');
  }
  return{scope:'Exact unrestricted princess response to the supplied normalized rational monster law; no equilibrium claim',
    positive_reflected_pairs:c.atoms.length,normalization_verified:true,physical_routes_verified:true,
    flow_replayed:true,extremal_responses_checked:2,...result};
}

function generate(source,bankfile,destination,denominator='10000000000'){
  const start=Date.now(),text=fs.readFileSync(source,'utf8'),data=JSON.parse(text),bank=JSON.parse(fs.readFileSync(bankfile,'utf8'));
  if(data.atoms.length!==bank.atoms.length)throw Error('bank size mismatch');
  const groups=new Map();
  for(let i=0;i<data.atoms.length;i++){
    if(JSON.stringify(data.atoms[i])!==JSON.stringify({kind:bank.atoms[i].kind,parameters:bank.atoms[i].parameters}))throw Error('bank atom mismatch');
    const w=data.weights[i];if(w<0||!Number.isFinite(w))throw Error('invalid discovery weight');if(!w)continue;
    let route=bank.atoms[i].exact_light;
    const a=JSON.stringify(route),b=JSON.stringify(route.map(([u,v])=>[v,u]));
    const key=a<b?a:b;if(b<a)route=route.map(([u,v])=>[v,u]);
    if(!groups.has(key))groups.set(key,{exact_light:route,weight:0,sources:[]});
    const g=groups.get(key);g.weight+=w;g.sources.push(i);
  }
  const items=[...groups.values()],sum=items.reduce((s,a)=>s+a.weight,0),den=Number(denominator);
  if(!Number.isSafeInteger(den)||Math.abs(sum-1)>1e-8)throw Error('rounding input');
  let assigned=0;
  for(const a of items){const ideal=a.weight/sum*den;a.integer=Math.floor(ideal);a.remainder=ideal-a.integer;assigned+=a.integer;}
  const order=items.map((_,i)=>i).sort((a,b)=>items[b].remainder-items[a].remainder||a-b);
  if(den-assigned>order.length)throw Error('rounding residual');
  for(let j=0;j<den-assigned;j++)items[order[j]].integer++;
  const atoms=items.filter(a=>a.integer>0).map(a=>({exact_light:a.exact_light,weight_numerator:String(a.integer),source_indices:a.sources}));
  validate(atoms,denominator);
  const model=new E.Rational.Model(atoms);
  console.error(JSON.stringify({event:'integer_model',atoms:atoms.length,queries:model.v.length,levels:model.base.length,threshold_nodes:model.N}));
  const answer=E.Integer.solveIntegerLaw(E.Cut,E.Physical,E.BigFlow.BigFlow,model,atoms.map(a=>a.weight_numerator),denominator);
  const c={scope:'Explicit rational reflected-pair monster strategy and exact unrestricted princess response certificate. This is an upper bound, not a saddle point.',
    source:path.basename(source),source_sha256:sha(text),weight_denominator:denominator,
    rounding:'Aggregate identical reflected physical pairs, then normalize and use largest remainders at the stated denominator.',
    atoms,value:answer.exactValue,decimal_value:answer.value,query_v:model.v,base_levels:model.base,
    minimum_labels:answer.labels,maximum_labels:answer.maxlabels,flow_certificate:answer.flowCertificate,
    network:answer.certificate};
  c.verification=verify(c);c.seconds=(Date.now()-start)/1000;
  fs.writeFileSync(destination,JSON.stringify(c)+'\n');
  const summary={value:c.value,decimal_value:c.decimal_value,atoms:atoms.length,network:c.network,
    verification:c.verification,seconds:c.seconds,certificate_sha256:sha(fs.readFileSync(destination))};
  fs.writeFileSync(destination.replace(/\.json$/,'.report.json'),JSON.stringify(summary,null,2)+'\n');
  console.log(JSON.stringify(summary,null,2));return c;
}

module.exports={verify,generate};
if(require.main===module){
  if(process.argv[2]==='--verify')console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));
  else generate(process.argv[2],process.argv[3],process.argv[4],process.argv[5]||'10000000000');
}
