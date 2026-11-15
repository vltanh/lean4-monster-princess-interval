"use strict";
// Fast discovery model with the same exact event ordering as Rational.Model.
// All comparisons are between members of one prechecked coordinate universe.
// Only reward lengths and flow capacities use floating arithmetic. Exact
// certificates continue to use the separate Rational/Integer implementation.
const E=require('../interval_turn_density/atomic_survival_v8.cjs');
const {Q}=E.Physical,zero=new Q(0n),two=new Q(2n);

function prepare(full){
  if(full.numericGeometry)return full.numericGeometry;
  const universe=new Map();
  for(const q of [...full.vQ,...full.baseQ])universe.set(q.toString(),q);
  const ordered=[...universe.values()].sort((a,b)=>a.cmp(b));
  let previous=-Infinity;
  for(const q of ordered){const value=q.number();
    if(!(value>previous))return null;previous=value;}
  const value=new Map(ordered.map(q=>[q.toString(),q.number()]));
  const baseIndex=new Map(full.base.map((s,j)=>[s,j]));
  const bounds=full.vQ.map(v=>[baseIndex.get((v.cmp(zero)>0?v:zero).toString()),baseIndex.get(v.add(two).toString())]);
  const routes=full.routes.map(pair=>pair.map(route=>route.map(([u,v])=>[
    full.query.get(u.toString()),full.query.get(v.toString())])));
  const g={value,baseIndex,bounds,routes};full.numericGeometry=g;return g;
}

function build(full,indices){
  const g=prepare(full);if(!g)return null;
  const queries=new Set([full.query.get('-1')]),bases=new Set([g.baseIndex.get('0')]);
  for(const j of indices)for(const route of g.routes[j])for(const[u,v]of route){
    queries.add(v);if(full.vQ[u].cmp(zero)>=0)bases.add(g.baseIndex.get(full.v[u]));
  }
  const qi=[...queries].sort((a,b)=>a-b);
  for(const i of qi)for(const b of g.bounds[i])bases.add(b);
  const bi=[...bases].sort((a,b)=>a-b),baseLocal=new Map(bi.map((b,j)=>[b,j]));
  const m=Object.create(E.Cut.Model.prototype);
  m.atoms=indices.map(j=>full.atoms[j]);
  m.routes=indices.map(j=>g.routes[j].map(route=>route.map(([u,v])=>[
    g.value.get(full.v[u]),g.value.get(full.v[v])])));
  m.v=qi.map(i=>g.value.get(full.v[i]));m.base=bi.map(i=>g.value.get(full.base[i]));
  m.vQ=qi.map(i=>full.vQ[i]);m.baseQ=bi.map(i=>full.baseQ[i]);
  m.query=new Map(m.v.map((v,j)=>[v,j]));m.L=3*m.base.length;
  m.bounds=qi.map(i=>g.bounds[i].map(b=>3*baseLocal.get(b)+1));
  const first=3*baseLocal.get(g.baseIndex.get('0'))+1;m.bounds[0]=[first,first];
  const last=m.bounds.at(-1)[1];m.bounds[m.bounds.length-1]=[last,last];
  m.offset=[];let n=0;for(const[lo,hi]of m.bounds){m.offset.push(n);n+=hi-lo;}m.N=n;
  m.defs=[];m.defMap=new Map();m.units=[];
  for(let j=0;j<indices.length;j++)m.units.push(m.compile(j));
  return m;
}

function lift(small,labels,full){
  // The lift uses rational coordinates, including physical-bound equality.
  const view={vQ:small.vQ,v:small.vQ.map(q=>q.toString()),b:k=>small.baseQ[Math.floor(k/3)]};
  return E.Rational.lift(view,labels,full);
}

module.exports={prepare,build,lift};
