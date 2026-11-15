"use strict";
const fs=require('fs'),assert=require('assert');
const E=require('./atomic_survival_v8.cjs'),W=require('./center_wait_survival.cjs'),Q=E.Physical.Q;
const zero=new Q(0n),one=new Q(1n),two=new Q(2n),four=new Q(4n);
function q(x){return new Q(x);}
function asatom(kind,p){const a=E.Cut.family(kind,p);a.exact_light=a.light.map(r=>r.map(x=>Q.number(x).toString()));return a;}
function reward(m,labels,j){
  m.compile(j);let ans=zero;
  for(const[id,c]of m.lastExactUnits){const d=m.defs[id],bits=d.bits;
    const used=bits.every(b=>{
      let i=0;while(i+1<m.offset.length&&m.offset[i+1]<=b)i++;
      const k=m.bounds[i][0]+1+b-m.offset[i];return d.pos?labels[i]>=k:labels[i]<k;
    });if(used)ans=ans.add(c);
  }
  return ans.div(four);
}
function randLabels(m,seed){
  let r=seed|0;const rnd=()=>{r^=r<<13;r^=r>>>17;r^=r<<5;return(r>>>0)/4294967296;};
  let prev=0;return m.bounds.map(([lo,hi])=>{const l=Math.max(lo,prev);let z=l+Math.floor(rnd()*(hi-l+1));prev=z;return z;});
}
const waits=[
 W.atom([['0','0'],['1/4','0'],['5/4','1'],['13/4','-1']]),
 W.atom([['0','0'],['1/4','0'],['3/4','-1/2'],['9/4','1'],['17/4','-1']]),
 W.atom([['0','0'],['1/2','0'],['3/4','1/4'],['5/4','-1/4'],['5/2','1'],['9/2','-1']]),
 W.atom([['0','0'],['59/256','0'],['215/512','97/512'],['1649/2048','-401/2048'],
         ['2049/1024','1'],['4097/1024','-1']],'dyadic round1 waiting attack')
];
const atoms=[asatom('M1',[1]),asatom('M1',[.5]),asatom('M2',[-.5,1]),...waits];
const m=W.Model(atoms);let exactReward=0,physicalChecks=0,maximumError=0;
for(let t=1;t<=128;t++){
  const labels=randLabels(m,7271*t);
  const row=m.rowExact(labels);
  for(let j=0;j<atoms.length;j++){assert(reward(m,labels,j).cmp(row[j])===0);exactReward++;}
  if(t<=20){
    const p=E.Physical.realize(m.v,m.base,labels,'1/1099511627776',true).path;
    for(let j=0;j<atoms.length;j++){
      const route=W.physical(atoms[j]),flip=route.map(([t,x])=>[t,q(x).neg().toString()]);
      const cap=E.Physical.capture(p,route).add(E.Physical.capture(p,flip)).div(two);
      const error=cap.sub(row[j]).number();
      // Dense strictification may avoid a side-zero contact and gain a finite
      // amount. It must not lose a nonvanishing amount against the declared
      // limiting face. The maximizing face below is checked in both directions.
      assert(error>=-1e-8);maximumError=Math.max(maximumError,Math.max(0,-error));physicalChecks++;
    }
  }
}
const ws=[35,15,10,10,10,10,10],den=100;
const br=m.solve(ws.map(x=>x/den),2e-13,true);
const exact=E.Integer.solveIntegerLaw(E.Cut,E.Physical,E.BigFlow.BigFlow,m,ws,den);
assert(Math.abs(br.value-exact.value)<1e-10);
const p=E.Physical.realize(m.v,m.base,exact.labels,'1/1208925819614629174706176',true).path;
let actual=zero;
for(let j=0;j<atoms.length;j++){
 const route=W.physical(atoms[j]),flip=route.map(([t,x])=>[t,q(x).neg().toString()]);
 actual=actual.add(E.Physical.capture(p,route).add(E.Physical.capture(p,flip)).mul(q(ws[j])).div(q(2*den)));physicalChecks++;
}
assert(Math.abs(actual.number()-exact.value)<1e-12);
const report={scope:'Initial-center-wait continuation compiler; exact rewards/cut and direct legal physical paths.',
 exactRewardChecks:exactReward,physicalChecks,maximumNegativePhysicalDeviation:maximumError,
 numerical:br.value,exact:exact.exactValue,physical:actual.number(),difference:actual.number()-exact.value,
 atoms,labels:exact.labels,physicalPath:p};
fs.writeFileSync('center_wait_verification.json',JSON.stringify(report,null,2));
console.log(JSON.stringify({...report,atoms:undefined,labels:undefined,physicalPath:undefined},null,2));
