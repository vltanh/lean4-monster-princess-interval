"use strict";
// Independent dual pricing: physical paths and their two running historical minima.
// For a path with endpoint time K, a causal calendar prices as
// sum_{j=0}^{K-1} min_{0<=i<=j} c_i. No credit-queue graph is used.
const {fraction,inspectPrimal}=require("./exact_certificate.cjs");
function priceRecordDual(certificate){
 const {n,W,primal}=inspectPrimal(certificate),N=16*n,R=2*n,C=4*n,D=BigInt(certificate.discount_denominator);
 if(!Number.isSafeInteger(n)||n<1||D<=0n)throw Error("invalid grid parameters");
 const d=new Map();
 for(const [j,k,a] of certificate.discounts){
  if(!Number.isSafeInteger(j)||!Number.isSafeInteger(k)||k===0)throw Error("invalid pressure coordinate");
  const z=BigInt(a),key=j+","+k;if(z<0n||d.has(key))throw Error("invalid discount");d.set(key,z);
 }
 const events=certificate.discounts;
 let coneChecks=0;
 for(const [t,x,a] of events)if(x>0)for(const [s,y,b] of events)
  if(y<0&&-y>=x+Math.abs(t-s)){if(BigInt(a)+BigInt(b)<D)throw Error("cone dual violation");coneChecks++;}
 function charge(j,k){
  if(k===0)return D;
  const z=d.get(j+","+k);if(z===undefined)throw Error("missing reachable physical event "+j+","+k);
  return BigInt(1+ +(k>0))*D-z;
 }
 function key(s){return [s.k,s.em,s.ep,s.c,s.mm===null?"none":s.mm,s.mp===null?"none":s.mp].join(",");}
 let layer=new Map(),best=null,states=0,transitions=0,maxLayer=0;
 for(let k=-R;k<=R;k+=2){
  const s={k,em:k===-R,ep:k===R,c:k===0,mm:null,mp:null,cost:0n};
  layer.set(key(s),s);
 }
 for(let j=0;j<=N;j++){
  maxLayer=Math.max(maxLayer,layer.size);states+=layer.size;
  const next=new Map();
  for(const s of layer.values()){
   if(s.em&&s.ep){if(best===null||s.cost<best)best=s.cost;continue;}
   if(j===N||!s.c&&j>=C)continue;
   let mm=s.mm,mp=s.mp;
   if(!s.em){const z=charge(j,s.k);if(mm===null||z<mm)mm=z;}
   if(!s.ep){const z=charge(j,-s.k);if(mp===null||z<mp)mp=z;}
   const cost=s.cost+(s.em?0n:mm)+(s.ep?0n:mp);
   for(const step of [-1,1]){
    const k=s.k+step;if(Math.abs(k)>R)continue;
    const c=s.c||k===0;if(!c&&j+1>=C)continue;
    const em=s.em||k===-R,ep=s.ep||k===R;
    const z={k,em,ep,c,mm:em?null:mm,mp:ep?null:mp,cost},id=key(z),old=next.get(id);
    if(old===undefined||cost<old.cost)next.set(id,z);
    transitions++;
   }
  }
  layer=next;
 }
 if(best===null)throw Error("no complete physical path");
 if(primal*D!==best*W)throw Error("nonzero exact record primal-dual gap");
 const value=fraction(best,4n*BigInt(n)*D);
 if(certificate.exact_value&&value!==certificate.exact_value)throw Error("record dual differs from claimed optimum: "+value);
 return {status:"PASS",method:"physical-path running-minimum dual",n,exact_scaled_primal:fraction(primal,W),exact_scaled_dual:fraction(best,D),
  exact_value:value,physical_record_states:states,transitions,max_layer_states:maxLayer,cone_inequalities:coneChecks};
}
module.exports={priceRecordDual};
if(require.main===module){
 const fs=require("node:fs"),path=require("node:path");
 const filename=process.argv[2]||path.join(__dirname,"grid_n1_certificate.json");
 try{process.stdout.write(JSON.stringify(priceRecordDual(JSON.parse(fs.readFileSync(filename))),null,2)+"\n");}
 catch(error){process.stderr.write(error.stack+"\n");process.exitCode=1;}
}
