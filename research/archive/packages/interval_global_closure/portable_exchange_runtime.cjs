function createExchangeRuntime(Engine,FastGeometry){
const {Q}=Engine.Physical,zero=new Q(0n),two=new Q(2n);
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

function build(atoms,profilesCoordinates){
 const shape=makeShape(atoms,profilesCoordinates),model=Engine.Rational.restore(shape,atoms);
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

 model.separate=function(weights,{samples=0,seed=1}={}){
  const indices=[],ws=[];
  for(let j=0;j<weights.length;j++)if(weights[j]>0){indices.push(j);ws.push(weights[j]);}
  const fast=FastGeometry?FastGeometry.build(model,indices):null;
  const small=fast||new Engine.Rational.Model(indices.map(j=>atoms[j]));
  const br=small.solve(ws,2e-13,true),lift=fast?FastGeometry.lift:Engine.Rational.lift;
  const labels=lift(small,br.labels,model),maxlabels=lift(small,br.maxlabels,model);
  const row=model.row(labels),rowmax=model.row(maxlabels),value=row.reduce((s,x,j)=>s+x*weights[j],0),vmax=rowmax.reduce((s,x,j)=>s+x*weights[j],0);
  if(Math.abs(value-br.value)>3e-9||Math.abs(value-vmax)>3e-9)throw Error("separator/contact mismatch");
  const extras=Engine.Face.sampleFaceRows(small,br,samples,seed).map(p=>{const ls=lift(small,p.labels,model);return{labels:ls,row:model.row(ls)};});
  return{value,labels,maxlabels,row,rowmax,extras,active:indices.length,thresholdNodes:small.N,auxiliaryNodes:br.auxiliaryNodes,dualValue:br.dualValue};
 };
 return model;
}
function coordinates(model){return{v:model.v,base:model.base};}
return{build,coordinates};
}
const api={createExchangeRuntime};
if(typeof module==='object'&&module.exports)module.exports=api;
return api;