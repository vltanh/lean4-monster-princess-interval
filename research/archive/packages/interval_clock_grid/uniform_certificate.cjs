"use strict";
// Exact atom/open-leg type capacities and independent current-leg record pricing.
const {fraction}=require("./exact_certificate.cjs");
function uniformGeometry(n){
 if(!Number.isSafeInteger(n)||n<1)throw Error("invalid grid");
 const N=16*n,R=2*n,events=[],matches=[];
 for(let j=0;j<N;j++){
  for(let k=-R+1;k<=R;k++)if(k!==0&&(j+k)%2===0)events.push([2*j,2*k]);
  for(let k=-2*R+1;k<2*R;k+=2)events.push([2*j+1,k]);
 }
 events.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 const eventIndex=new Map(events.map((z,i)=>[z.join(","),i]));
 for(let p=0;p<events.length;p++)if(events[p][1]>0)
  for(let q=0;q<events.length;q++)if(events[q][1]<0&&-events[q][1]>=events[p][1]+Math.abs(events[q][0]-events[p][0]))matches.push([p,q]);
 return {n,N,R,events,eventIndex,matches};
}
function inspectUniformPlans(n,plans,W){
 const N=16*n,R=2*n,pressure=new Map();let probability=0n,mass=0n;
 function add(t,x,q){const key=t+","+x;pressure.set(key,(pressure.get(key)||0n)+q);mass+=q;}
 for(const p of plans){
  const w=BigInt(p.weight_numerator);if(w<=0n)throw Error("nonpositive plan weight");probability+=w;
  if(!Number.isSafeInteger(p.start_grid)||p.start_grid%2||Math.abs(p.start_grid)>R)throw Error("invalid initial position");
  const positions=[p.start_grid];
  for(const d of p.moves){if(d!==1&&d!==-1)throw Error("non-unit move");const x=positions.at(-1)+d;if(Math.abs(x)>R)throw Error("outside arena");positions.push(x);}
  if(p.moves.length>N)throw Error("completion horizon");
  const km=positions.indexOf(-R),kp=positions.indexOf(R),center=positions.indexOf(0);
  if(km<0||kp<0||center<0||center>4*n)throw Error("visit deadline");
  for(const [prefix,end,sign] of [["minus",km,1],["plus",kp,-1]]){
   const a=new Array(end).fill(0),b=new Array(end).fill(0);
   for(const [kind,target] of [["_charges",a],["_uniform",b]])for(const [j,c] of p[prefix+kind]||[]){
    if(!Number.isSafeInteger(j)||!Number.isSafeInteger(c)||c<=0||j<0||j>=end)throw Error("invalid active calendar item");target[j]+=c;
   }
   let cumulative=0;
   for(let j=0;j<end;j++){
    cumulative+=a[j]+b[j];if(cumulative<j+1)throw Error("uniform calendar left-limit prefix");
    if(a[j])add(2*j,2*sign*positions[j],w*BigInt(a[j]));
    if(b[j])add(2*j+1,sign*(2*positions[j]+p.moves[j]),w*BigInt(b[j]));
   }
   if(cumulative!==end)throw Error("active clock mass");
  }
 }
 if(probability!==W)throw Error("probability normalization");return {pressure,mass};
}
function inspectUniformPrimal(c){
 const n=c.n,W=BigInt(c.weight_denominator);
 if(!Number.isSafeInteger(n)||n<1||W<=0n||c.clock_types!=="vertex_and_uniform_leg"||c.completion_horizon!==8||c.center_deadline!==2||c.physical_step!=="1/"+(2*n)||c.pressure_step!=="1/"+(4*n)||c.objective_scale!=="1/"+(4*n))throw Error("uniform model metadata");
 const stats=inspectUniformPlans(n,c.paths,W),used=new Map();let matched=0n;
 for(const [t,x,s,y,a] of c.matching){
  const q=BigInt(a);if(q<=0n||![t,x,s,y].every(Number.isSafeInteger)||x<=0||y>=0||-y<x+Math.abs(t-s))throw Error("invalid band containment");
  for(const key of [t+","+x,s+","+y])used.set(key,(used.get(key)||0n)+q);matched+=q;
 }
 for(const [key,q] of used)if(q>(stats.pressure.get(key)||0n))throw Error("matching type capacity");
 let positive=0n;for(const [key,q] of stats.pressure)if(Number(key.split(",")[1])>0)positive+=q;
 return {n,W,stats,matched,positive,primal:stats.mass+positive-matched};
}
function verifyUniform(c){
 const {n,W,stats,matched,positive,primal}=inspectUniformPrimal(c),g=uniformGeometry(n),D=BigInt(c.discount_denominator);
 if(D<=0n)throw Error("discount denominator");
 const d=new Map();for(const [t,x,a] of c.discounts){const z=BigInt(a),key=t+","+x;if(z<0n||d.has(key))throw Error("invalid type discount");d.set(key,z);}
 if(d.size!==g.events.length)throw Error("incomplete type geometry");
 for(const z of g.events)if(!d.has(z.join(",")))throw Error("missing type");
 for(const [p,q] of g.matches)if(d.get(g.events[p].join(","))+d.get(g.events[q].join(","))<D)throw Error("type covering inequality");
 function charge(t,x){if(x===0)return D;const a=d.get(t+","+x);if(a===undefined)throw Error("missing price");return BigInt(1+ +(x>0))*D-a;}
 function key(s){return [s.k,s.em,s.ep,s.c,s.mm===null?"none":s.mm,s.mp===null?"none":s.mp].join(",");}
 let layer=new Map(),best=null,count=0,transitions=0,maxLayer=0;
 for(let k=-g.R;k<=g.R;k+=2){const s={k,em:k===-g.R,ep:k===g.R,c:k===0,mm:null,mp:null,cost:0n};layer.set(key(s),s);}
 for(let j=0;j<=g.N;j++){
  const next=new Map();count+=layer.size;maxLayer=Math.max(maxLayer,layer.size);
  for(const s of layer.values()){
   if(s.em&&s.ep){if(best===null||s.cost<best)best=s.cost;continue;}
   if(j===g.N||!s.c&&j>=4*n)continue;
   let mm=s.mm,mp=s.mp;
   if(!s.em){const a=charge(2*j,2*s.k);if(mm===null||a<mm)mm=a;}
   if(!s.ep){const a=charge(2*j,-2*s.k);if(mp===null||a<mp)mp=a;}
   for(const step of [-1,1]){
    const k=s.k+step;if(Math.abs(k)>g.R)continue;
    const cc=s.c||k===0;if(!cc&&j+1>=4*n)continue;
    let m=mm,p=mp;
    if(!s.em){const a=charge(2*j+1,2*s.k+step);if(a<m)m=a;}
    if(!s.ep){const a=charge(2*j+1,-2*s.k-step);if(a<p)p=a;}
    const cost=s.cost+(s.em?0n:m)+(s.ep?0n:p),em=s.em||k===-g.R,ep=s.ep||k===g.R;
    const z={k,em,ep,c:cc,mm:em?null:m,mp:ep?null:p,cost},id=key(z),old=next.get(id);
    if(!old||cost<old.cost)next.set(id,z);transitions++;
   }
  }
  layer=next;
 }
 if(best===null||primal*D!==best*W)throw Error("nonzero uniform primal-dual gap");
 const value=fraction(primal,4n*BigInt(n)*W),lower=fraction(primal-2n*W,4n*BigInt(n)*W);
 if(c.exact_value&&c.exact_value!==value||c.global_lower&&c.global_lower!==lower)throw Error("claimed value");
 return {status:"PASS",model:"vertex_and_uniform_leg",n,physical_calendar_plans:c.paths.length,pressure_types:g.events.length,matching_edges:g.matches.length,
  physical_record_states:count,transitions,max_layer_states:maxLayer,exact_scaled_primal:fraction(primal,W),exact_scaled_dual:fraction(best,D),
  exact_value:value,global_lower:lower,enclosure_width:fraction(1n,2n*BigInt(n)),baseline:fraction(stats.mass,4n*BigInt(n)*W),deficiency:fraction(positive-matched,4n*BigInt(n)*W)};
}
module.exports={uniformGeometry,inspectUniformPlans,inspectUniformPrimal,verifyUniform};
if(require.main===module){
 const fs=require("node:fs"),path=require("node:path");
 const file=process.argv[2]||path.join(__dirname,"uniform_n1_certificate.json");
 try{process.stdout.write(JSON.stringify(verifyUniform(JSON.parse(fs.readFileSync(file))),null,2)+"\n");}
 catch(error){process.stderr.write(error.stack+"\n");process.exitCode=1;}
}
