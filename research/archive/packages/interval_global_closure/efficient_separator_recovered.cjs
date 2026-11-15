"use strict";
// Persistent rational-geometry global princess separator for one fixed bank.
const fs=require('fs'),path=require('path'),readline=require('readline');
const Engine=require('../interval_turn_density/atomic_survival_v8.cjs');
const FastGeometry=require('./efficient_numeric_model.cjs');
const {Q}=Engine.Physical,zero=new Q(0n),two=new Q(2n);
const started=Date.now(),input=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const checkpoint=JSON.parse(fs.readFileSync(path.join(__dirname,'../interval_turn_density/atomic_search_checkpoint.json'),'utf8'));
const prior=JSON.parse(fs.readFileSync(path.join(__dirname,'global_minimax_enriched.json'),'utf8'));
function makeShape(atoms,extra){
  const vv=new Map([['-1',new Q(-1n)]]),bb=new Map([['0',zero]]);
  const put=(map,q)=>map.set(q.toString(),q);
  for(const atom of atoms)for(const row of (atom.event_light||atom.exact_light)){
    const u=new Q(row[0]),v=new Q(row[1]);put(vv,u);put(vv,v);
    if(u.cmp(zero)>=0)put(bb,u);if(v.cmp(zero)>=0)put(bb,v);
  }
  for(const e of extra){for(const v of e.v)put(vv,new Q(v));for(const b of e.base)put(bb,new Q(b));}
  const v=Array.from(vv.values()).sort((a,b)=>a.cmp(b));
  for(const x of v){put(bb,x.cmp(zero)>0?x:zero);put(bb,x.add(two));}
  const base=Array.from(bb.values()).sort((a,b)=>a.cmp(b));
  const lookup=new Map(base.map((x,j)=>[x.toString(),3*j+1]));
  const bounds=v.map(x=>[lookup.get((x.cmp(zero)>0?x:zero).toString()),lookup.get(x.add(two).toString())]);
  bounds[0]=[lookup.get('0'),lookup.get('0')];const last=bounds.at(-1)[1];bounds[bounds.length-1]=[last,last];
  const offset=[];let N=0;for(const[lo,hi]of bounds){offset.push(N);N+=hi-lo;}
  return {v:v.map(x=>x.toString()),base:base.map(x=>x.toString()),bounds,offset,N,defs:[],units:[]};
}
function bare(shape){return Engine.Rational.restore({...shape,defs:[],units:[]},[]);}
const priorShape={v:prior.query_v,base:prior.event_labels.filter((_,j)=>j%3===0).map(x=>x[0])};
const shape=makeShape(input.atoms,[checkpoint.modelCoordinates,priorShape,...(input.extra_profiles||[])]);
// Master columns remain exactly input.atoms. Additional event coordinates only
// permit old legal princess profiles to be lifted without resampling them.
const model=Engine.Rational.restore(shape,input.atoms);
// The full union needs query geometry and physical contact rows only. Its
// maximum-closure rewards are never compiled: each global cut builds just
// the positive-support model, and coarea completion is evaluated directly
// from its complete nested-profile mixture.
const old=bare(checkpoint.modelCoordinates),oldPrior=bare(priorShape);
// Contact predicates are compiled with exact rational comparisons. Only the
// final payoff arithmetic is floating, as required by the numerical master.
const baseNumbers=model.baseQ.map(q=>q.number()),vNumbers=model.vQ.map(q=>q.number());
function compileContact(route){
  const [u,v]=route[0],start={query:model.query.get(v.toString()),ge:model.ge(u),gt:model.gt(u),time:u.add(v).div(two).number()};
  const legs=[];
  for(let j=1;j<route.length;j++){
    const[u0,v0]=route[j-1],[u1,v1]=route[j];
    if(u1.cmp(u0)>0)legs.push({horizontal:true,query:model.query.get(v0.toString()),gt:model.gt(u1),v:v0.number()});
    else legs.push({horizontal:false,ge:model.ge(u0),right:model.query.get(v1.toString()),
      unconditional:u0.cmp(v1)<=0,u:u0.number()});
  }
  return{start,legs};
}
const contacts=model.routes.map(pair=>pair.map(compileContact));
function captureContact(compiled,labels){
  const s=compiled.start,p=labels[s.query];if(p>=s.ge&&p<s.gt)return s.time;
  const above=p>=s.gt;
  for(const leg of compiled.legs){
    if(leg.horizontal&&above){const k=labels[leg.query];if(k<leg.gt)return(baseNumbers[Math.floor(k/3)]+leg.v)/2;}
    else if(!leg.horizontal&&!above){
      const at=Engine.Cut.lower(labels,leg.ge);
      if(leg.unconditional||at<=leg.right)return(leg.u+Math.min(leg.u,vNumbers[at]))/2;
    }
  }
  throw Error('compiled contact missed a capture');
}
function fastRow(labels){return contacts.map(pair=>(captureContact(pair[0],labels)+captureContact(pair[1],labels))/2);}
const rationalRow=model.row.bind(model);let checkedRows=0;
model.row=function(labels){
  const answer=fastRow(labels);
  if(checkedRows++<16){const exact=rationalRow(labels);for(let j=0;j<answer.length;j++)
    if(Math.abs(answer[j]-exact[j])>2e-14)throw Error('compiled contact mismatch');}
  return answer;
};
// Cache exact active-support geometry across bundle trials. The small model
// retains its independent rational contact calculation.
const supportCache=new Map();
function sparseSolve(weights,retainFace=true,forceRational=false){
  const indices=[],atoms=[],ws=[];for(let j=0;j<weights.length;j++)if(weights[j]>0){indices.push(j);atoms.push(model.atoms[j]);ws.push(weights[j]);}
  const key=(forceRational?'Q:':'N:')+indices.join(',');let small=supportCache.get(key);
  if(!small){
    small=forceRational?null:FastGeometry.build(model,indices);
    if(small)small.exactNumericOrdering=true;else small=new Engine.Rational.Model(atoms);
    supportCache.set(key,small);if(supportCache.size>4)supportCache.delete(supportCache.keys().next().value);
  }
  const lift=small.exactNumericOrdering?FastGeometry.lift:Engine.Rational.lift;
  const br=small.solve(ws,2e-13,retainFace),labels=lift(small,br.labels,model),maxlabels=lift(small,br.maxlabels,model);
  const payoff=model.row(labels),payoffmax=model.row(maxlabels),value=payoff.reduce((sum,x,j)=>sum+x*weights[j],0),vm=payoffmax.reduce((sum,x,j)=>sum+x*weights[j],0);
  if(Math.abs(value-br.value)>3e-9||Math.abs(vm-br.value)>3e-9)throw Error('cached sparse rational lift score changed');
  return{value,row:payoff,rowmax:payoffmax,labels,maxlabels,smallModel:small,smallResponse:br,indices,thresholdNodes:small.N,dualValue:br.dualValue,lift};
}
function row(labels){
  for(let i=0;i<labels.length;i++)if(labels[i]<model.bounds[i][0]||labels[i]>model.bounds[i][1]||i&&labels[i]<labels[i-1])throw Error('illegal lifted labels');
  return {labels,row:model.row(labels)};
}
function uncross(profiles,weights,retain=0){
  const total=weights.reduce((a,b)=>a+b,0);weights=weights.map(x=>x/total);
  const probabilities=new Float64Array(model.N);
  for(let i=0;i<model.v.length;i++){
    const[lo,hi]=model.bounds[i],diff=new Float64Array(hi-lo+2);
    for(let j=0;j<profiles.length;j++){
      const k=profiles[j][i];if(k>lo){diff[0]+=weights[j];diff[k-lo]-=weights[j];}
    }
    let sum=0;for(let k=lo+1;k<=hi;k++){sum+=diff[k-lo-1];probabilities[model.node(i,k)]=Math.max(0,Math.min(1,sum));}
  }
  const raw=Array.from(new Set(probabilities)).sort((a,b)=>a-b),levels=[0];
  for(const p of raw)if(p-levels.at(-1)>1e-12)levels.push(p);
  if(1-levels.at(-1)<1e-12)levels[levels.length-1]=1;else levels.push(1);
  const pieces=[];
  for(let j=1;j<levels.length;j++)pieces.push({weight:levels[j]-levels[j-1],threshold:(levels[j]+levels[j-1])/2});
  pieces.sort((a,b)=>b.weight-a.weight);
  const responses=[],costs=new Float64Array(input.atoms.length);
  const keep=retain<0?pieces.length:Math.min(pieces.length,retain||0);
  for(let j=0;j<pieces.length;j++){
    const piece=pieces[j];
    const labels=[];
    for(let i=0;i<model.v.length;i++){
      let[lo,hi]=model.bounds[i];
      while(lo<hi){const middle=Math.floor((lo+hi+1)/2);
        if(probabilities[model.node(i,middle)]>=piece.threshold)lo=middle;else hi=middle-1;}
      labels.push(lo);
    }
    const response=row(labels);
    for(let k=0;k<costs.length;k++)costs[k]+=piece.weight*response.row[k];
    if(j<keep)responses.push({...response,weight:piece.weight});
  }
  return {minimum:Math.min(...costs),costs:Array.from(costs),components:pieces.length,responses};
}
process.stdout.write(JSON.stringify({ready:true,atoms:input.atoms.length,queries:model.v.length,
  labels:model.base.length*3,threshold_nodes:model.N,seconds:(Date.now()-started)/1000,
  v:model.v,event_labels:model.base.flatMap(b=>[-1,0,1].map(s=>[b,s]))})+'\n');
const line=readline.createInterface({input:process.stdin,crlfDelay:Infinity});
line.on('line',text=>{
  try{
    const request=JSON.parse(text),begin=Date.now();
    if(request.operation==='seed'){
      const responses=[];
      for(const labels of checkpoint.archiveLabels)if(labels!==null)responses.push(row(Engine.Rational.lift(old,labels,model)));
      for(const item of prior.princess_mixture)responses.push(row(Engine.Rational.lift(oldPrior,item.labels,model)));
      for(const extra of(input.extra_profiles||[])){
        const oldExtra=bare(extra);
        for(const item of extra.profiles)responses.push(row(Engine.Rational.lift(oldExtra,item.labels,model)));
      }
      const seed=sparseSolve(input.seed_weights,false);
      responses.push({labels:seed.labels,row:seed.row},{labels:seed.maxlabels,row:seed.rowmax});
      process.stdout.write(JSON.stringify({responses,seed_value:seed.value,seed_labels:seed.labels,
        seconds:(Date.now()-begin)/1000})+'\n');
    }else if(request.operation==='uncross'){
      const result=uncross(request.profiles,request.weights,request.retain||0);
      process.stdout.write(JSON.stringify({...result,seconds:(Date.now()-begin)/1000})+'\n');
    }else if(request.operation==='rows'){
      process.stdout.write(JSON.stringify({responses:request.profiles.map(row),seconds:(Date.now()-begin)/1000})+'\n');
    }else if(request.operation==='separate'){
      const answer=sparseSolve(request.weights,true,request.rational||false);
      const responses=[{labels:answer.labels,row:answer.row},{labels:answer.maxlabels,row:answer.rowmax}];
      const samples=Engine.Face.sampleFaceRows(answer.smallModel,answer.smallResponse,request.samples||0,request.seed||1);
      for(const sample of samples)responses.push(row(answer.lift(answer.smallModel,sample.labels,model)));
      process.stdout.write(JSON.stringify({value:answer.value,dual_value:answer.dualValue,responses,
        active_atoms:answer.indices.length,threshold_nodes:answer.thresholdNodes,
        seconds:(Date.now()-begin)/1000})+'\n');
    }else throw Error('unknown operation');
  }catch(error){process.stdout.write(JSON.stringify({error:error.stack})+'\n');}
});
