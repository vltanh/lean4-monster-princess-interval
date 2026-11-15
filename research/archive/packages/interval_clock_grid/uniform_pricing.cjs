"use strict";
// Numerical discovery only. Every proposed optimum is replayed with BigInt.
function typeOrder(nodes){
 const order=[];
 for(let i=0;i<nodes.length;i++)for(let j=0;j<nodes.length;j++)
  if(i!==j&&nodes[j][1]>=nodes[i][1]+Math.abs(nodes[j][0]-nodes[i][0]))order.push([i,j]);
 return order;
}
function pricePhysical(g,discounts){
 const {n,N,R}=g,C=4*n,scale=1e10;
 function charge(t,x){if(x===0)return 1;const i=g.eventIndex.get(t+","+x);if(i===undefined)throw Error("missing type");return Math.round((1+ +(x>0)-discounts[i])*scale)/scale;}
 function key(s){return [s.start,s.k,s.em,s.ep,s.c,s.mm,s.mp].join(",");}
 let layer=new Map(),bestByStart=new Map(),count=0,maxLayer=0;
 for(let k=-R;k<=R;k+=2){const s={start:k,k,em:k===-R,ep:k===R,c:k===0,mm:Infinity,mp:Infinity,cost:0,prev:null,step:0};layer.set(key(s),s);}
 for(let j=0;j<=N;j++){
  const next=new Map();count+=layer.size;maxLayer=Math.max(maxLayer,layer.size);
  for(const s of layer.values()){
   if(s.em&&s.ep){const old=bestByStart.get(s.start);if(!old||s.cost<old.cost)bestByStart.set(s.start,s);continue;}
   if(j===N||!s.c&&j>=C)continue;
   const mm=s.em?Infinity:Math.min(s.mm,charge(2*j,2*s.k)),mp=s.ep?Infinity:Math.min(s.mp,charge(2*j,-2*s.k));
   for(const step of [-1,1]){
    const k=s.k+step;if(Math.abs(k)>R)continue;
    const c=s.c||k===0;if(!c&&j+1>=C)continue;
    const m=s.em?Infinity:Math.min(mm,charge(2*j+1,2*s.k+step));
    const p=s.ep?Infinity:Math.min(mp,charge(2*j+1,-2*s.k-step));
    const cost=s.cost+(s.em?0:m)+(s.ep?0:p),em=s.em||k===-R,ep=s.ep||k===R;
    const z={start:s.start,k,em,ep,c,mm:em?Infinity:m,mp:ep?Infinity:p,cost,prev:s,step},id=key(z),old=next.get(id);
    if(!old||cost<old.cost-1e-11)next.set(id,z);
   }
  }
  layer=next;
 }
 function decode(last){
  const moves=[];for(let a=last;a.prev;a=a.prev)moves.push(a.step);moves.reverse();
  const positions=[last.start];for(const step of moves)positions.push(positions.at(-1)+step);
  function calendar(sign,end){
   const atoms=new Map(),uniform=new Map();let best=Infinity,when=-1,kind=0;
   for(let j=0;j<end;j++){
    const a=charge(2*j,2*sign*positions[j]),b=charge(2*j+1,sign*(2*positions[j]+moves[j]));
    if(a<best-1e-11){best=a;when=j;kind=0;}if(b<best-1e-11){best=b;when=j;kind=1;}
    const counts=kind?uniform:atoms;counts.set(when,(counts.get(when)||0)+1);
   }
   return {atoms:Array.from(atoms),uniform:Array.from(uniform)};
  }
  const m=calendar(1,positions.indexOf(-R)),p=calendar(-1,positions.indexOf(R));
  return {start_grid:last.start,moves,minus_charges:m.atoms,minus_uniform:m.uniform,plus_charges:p.atoms,plus_uniform:p.uniform};
 }
 const choices=Array.from(bestByStart.values()).sort((a,b)=>a.cost-b.cost).map(s=>({value:s.cost,plan:decode(s)}));
 if(!choices.length)throw Error("no physical record path");
 return {value:choices[0].value,choices,record_states:count,max_layer:maxLayer};
}
function planColumn(g,plan){
 const positions=[plan.start_grid];for(const d of plan.moves)positions.push(positions.at(-1)+d);
 const counts=new Array(g.events.length).fill(0);let cost=0;
 for(const [prefix,sign] of [["minus",1],["plus",-1]]){
  for(const [j,a] of plan[prefix+"_charges"]||[]){const x=2*sign*positions[j];cost+=a*(1+ +(x>0));if(x)counts[g.eventIndex.get(2*j+","+x)]+=a;}
  for(const [j,a] of plan[prefix+"_uniform"]||[]){const x=sign*(2*positions[j]+plan.moves[j]);cost+=a*(1+ +(x>0));counts[g.eventIndex.get((2*j+1)+","+x)]+=a;}
 }
 return {plan,cost,counts};
}
module.exports={typeOrder,pricePhysical,planColumn};
