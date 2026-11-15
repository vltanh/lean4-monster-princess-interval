"use strict";
/* Exact response-supremum adapter for initial CENTER waits, followed by unit
 * legs. This is not an adapter for arbitrary interior waiting segments.
 * The virtual continuation starts at (w,w). On the dense class of strictly
 * positive radial princesses, its initial record is above=true, below=false.
 */
const E=require('./atomic_survival_v8.cjs'),Q=E.Physical.Q;
const zero=new Q(0n),two=new Q(2n),four=new Q(4n);
const qmin=(a,b)=>a.cmp(b)<=0?a:b,qmax=(a,b)=>a.cmp(b)>=0?a:b;
function atom(route,source='initial center wait'){
  const p=route.map(r=>r.map(x=>new Q(x)));
  if(p.length<3||p[0][0].n!==0n||p[0][1].n!==0n||p[1][1].n!==0n||p[1][0].cmp(zero)<=0)
    throw Error('expected nonzero initial center wait');
  const w=p[1][0];
  for(let k=1;k<p.length;k++){
    const dt=p[k][0].sub(p[k-1][0]),dx=p[k][1].sub(p[k-1][1]);
    if(dt.cmp(zero)<=0||p[k][1].abs().cmp(new Q(1n))>0||dx.abs().cmp(dt)>0)
      throw Error('illegal waiting route');
    if(k>1&&dx.abs().cmp(dt)!==0)throw Error('only initial center wait is supported');
  }
  return {kind:'initial_center_wait',wait:w.toString(),source,
          exact_physical:p.map(r=>r.map(String)),
          exact_light:p.slice(1).map(([t,x])=>[t.add(x).toString(),t.sub(x).toString()])};
}
function patch(m,atoms){
  const oldCapture=m.capture,oldCompile=m.compile,waitExact=new Array(atoms.length);
  const iswait=atoms.map(a=>a.kind==='initial_center_wait');
  const waitCapture=(r,labels)=>{
    let[u0,v0]=r[0];
    for(let k=1;k<r.length;k++){
      const[u1,v1]=r[k];
      if(u1.cmp(u0)>0){
        const p=labels[m.query.get(v0.toString())];
        if(p<m.gt(u1))return m.b(p).add(v0).div(two);
      }
      u0=u1;v0=v1;
    }
    throw Error('waiting continuation lacks endpoint capture');
  };
  m.rowExact=function(labels){return this.routes.map((r,j)=>{
    const cap=iswait[j]?waitCapture:(a,b)=>oldCapture.call(m,a,b);
    return cap(r[0],labels).add(cap(r[1],labels)).div(two);
  });};
  m.row=function(labels){return this.rowExact(labels).map(x=>x.number());};
  for(let j=0;j<atoms.length;j++)if(iswait[j]){
    const w=new Q(atoms[j].wait),r0=m.routes[j][0][0];
    if(r0[0].cmp(w)||r0[1].cmp(w))throw Error('wrong center-wait endpoint');
    const sums=new Map();
    const add=(bits,c)=>{
      if(c.n===0n)return;
      if(c.n<0n)throw Error('negative wait reward');
      const b=m.norm(true,bits);if(b===null)return;
      const key='+'+b.join(',');let id=m.defMap.get(key);
      if(id===undefined){id=m.defs.length;m.defMap.set(key,id);m.defs.push({pos:true,bits:b});}
      sums.set(id,(sums.get(id)||zero).add(c));
    };
    add([],w.mul(four));
    for(const r of m.routes[j]){
      let[u0,v0]=r[0],above=[];
      for(let k=1;k<r.length;k++){
        const[u1,v1]=r[k];
        if(u1.cmp(u0)>0){
          const idx=m.query.get(v0.toString());
          let old=qmax(zero,qmin(m.baseQ[0],u1).sub(u0));add(above,old);
          for(let l=1;l<m.baseQ.length;l++){
            const z=qmax(zero,qmin(m.baseQ[l],u1).sub(u0));
            if(z.cmp(old)>0)add(above.concat([[idx,3*l]]),z.sub(old));old=z;
          }
        }else add(above,v1.sub(v0));
        above.push([m.query.get(v1.toString()),m.gt(u1)]);u0=u1;v0=v1;
      }
    }
    waitExact[j]=Array.from(sums);
    m.units[j]=waitExact[j].map(([id,c])=>[id,c.number()]);
  }
  m.compile=function(j){
    if(!iswait[j])return oldCompile.call(this,j);
    this.lastExactUnits=waitExact[j];
    return waitExact[j].map(([id,c])=>[id,c.number()]);
  };
  m.waitSemantics='initial-center-wait; strictly-positive response-supremum continuation';
  return m;
}
function Model(atoms){return patch(new E.Rational.Model(atoms),atoms);}
function restore(shape,atoms){
  // Rebuild to keep the exact custom-row semantics. The deterministic source
  // assigns the same coordinates and reward ids; reject stale shapes.
  const m=Model(atoms);
  if(JSON.stringify(m.v)!==JSON.stringify(shape.v)||JSON.stringify(m.base)!==JSON.stringify(shape.base)||
     JSON.stringify(m.units)!==JSON.stringify(shape.units))throw Error('wait model source/shape mismatch');
  return m;
}
function sparseSolve(full,weights,retainFace=true){
  const indices=[],atoms=[],ws=[];
  for(let j=0;j<weights.length;j++)if(weights[j]>0){indices.push(j);atoms.push(full.atoms[j]);ws.push(weights[j]);}
  const m=Model(atoms),br=m.solve(ws,2e-13,retainFace);
  const labels=E.Rational.lift(m,br.labels,full),maxlabels=E.Rational.lift(m,br.maxlabels,full);
  const row=full.row(labels),rowmax=full.row(maxlabels),value=row.reduce((s,x,j)=>s+x*weights[j],0);
  if(Math.abs(value-br.value)>3e-9)throw Error('waiting sparse lift changed payoff');
  return{value,row,rowmax,labels,maxlabels,smallModel:m,smallResponse:br,indices};
}
function physical(atom){
  if(atom.exact_physical)return atom.exact_physical;
  return atom.exact_light.map(([u,v])=>[new Q(u).add(v).div(two).toString(),new Q(u).sub(v).div(two).toString()]);
}
function replacement(a){
  if(a.kind!=='initial_center_wait')throw Error('replacement requires center wait');
  const p=a.exact_physical.map(r=>r.map(x=>new Q(x))),w=new Q(a.wait);
  const sign=p[2][1].cmp(p[1][1]);if(!sign)throw Error('missing first unit direction');
  const raw=[[zero,w.mul(new Q(BigInt(-sign)))],...p.slice(1)],clean=[];
  for(const v of raw){
    while(clean.length>1){const a=clean.at(-2),b=clean.at(-1);
      if(b[1].sub(a[1]).mul(v[0].sub(b[0])).cmp(v[1].sub(b[1]).mul(b[0].sub(a[0])))!==0)break;
      clean.pop();
    }
    clean.push(v);
  }
  return{kind:'center_wait_unit_replacement',source:a.source,
         exact_physical:clean.map(r=>r.map(String)),
         exact_light:clean.map(([t,x])=>[t.add(x).toString(),t.sub(x).toString()])};
}
module.exports={atom,Model,restore,sparseSolve,physical,replacement};
