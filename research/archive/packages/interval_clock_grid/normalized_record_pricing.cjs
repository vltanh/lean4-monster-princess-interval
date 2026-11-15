"use strict";
// Exact dual pricing for the normalized physical bank. This is not an
// unrestricted-path dual extension: the bank-normalization theorem is required.
const {fraction,inspectPrimal}=require("./exact_certificate.cjs");
function expandNodalInput(input){
 if(!input.radial_nodes)return {...input,qout_verified:false};
 const n=input.n,D=BigInt(input.field_denominator),H=12*n,R=2*n,N=16*n,g=new Map();
 if(!Number.isSafeInteger(n)||n<1||D<=0n)throw Error("invalid nodal parameters");
 for(const [j,k,a] of input.radial_nodes){
  const value=BigInt(a),key=j+","+k;
  if(!Number.isSafeInteger(j)||!Number.isSafeInteger(k)||j<0||j>H||k<=0||k>R||(j+k)%2||value<0n||value>D||g.has(key))throw Error("invalid radial node");
  g.set(key,value);
 }
 let count=0;
 for(let j=0;j<=H;j++)for(let k=1;k<=R;k++)if((j+k)%2===0){
  const value=g.get(j+","+k);if(value===undefined)throw Error("missing radial node");count++;
  if(k<R)for(const step of [-1,1])if(j+step>=0&&j+step<=H){
   const upper=g.get((j+step)+","+(k+1));if(upper===undefined||value>upper)throw Error("nodal transport inequality");
  }
 }
 if(g.size!==count)throw Error("radial geometry");
 let qout=true;
 for(let j=0;j+2<=H;j+=2)if(g.get((j+2)+","+R)>g.get(j+","+R))qout=false;
 for(let j=4*n;j<=H;j++)for(let k=1;k<=R;k++)if((j+k)%2===0){
  const foot=k-j+4*n,expected=foot<=0?0n:g.get((4*n)+","+foot);
  if(g.get(j+","+k)!==expected)qout=false;
 }
 if(input.normalized_profile===true&&!qout)throw Error("claimed sticky/outward2 profile fails exact identities");
 const discounts=[];
 for(let j=0;j<N;j++)for(let k=-R+1;k<=R;k++)if(k&&(j+k)%2===0){
  const value=j>H?(qout&&k<0?0n:D):k>0?D-g.get(j+","+k):g.get(j+","+(-k));discounts.push([j,k,String(value)]);
 }
 return {...input,discount_denominator:String(D),discounts,input_mode:"radial nodal profile through time6",qout_verified:qout};
}
function verifyNormalizedDual(c,options={}){
 c=expandNodalInput(c);
 const n=c.n,D=BigInt(c.discount_denominator),N=16*n,R=2*n,C=4*n;
 if(!Number.isSafeInteger(n)||n<1||D<=0n)throw Error("invalid normalized grid");
 const target=options.targetUnits===undefined?null:BigInt(options.targetUnits);
 if(target!==null&&options.witness)throw Error("target-bound mode does not construct an attaining witness");
 const d=new Map();
 for(const [j,k,a] of c.discounts){
  if(!Number.isSafeInteger(j)||!Number.isSafeInteger(k)||j<0||j>=N||k<=-R||k>R||k===0||(j+k)%2)throw Error("invalid event coordinate");
  const z=BigInt(a),key=j+","+k;if(z<0n||d.has(key))throw Error("invalid covering discount");d.set(key,z);
 }
 const events=[];
 for(let j=0;j<N;j++)for(let k=-R+1;k<=R;k++)if(k&&(j+k)%2===0){const key=j+","+k;if(!d.has(key))throw Error("missing event "+key);events.push([j,k]);}
 if(d.size!==events.length)throw Error("unexpected event geometry");
 // Cone suffix minima: every larger containing interval is reached through
 // one of the two immediate radius-increasing neighbors. Complexity O(n^2).
 const cover=Array.from({length:R+1},()=>new Array(N).fill(null));
 for(let r=R-1;r>=1;r--)for(let j=0;j<N;j++)if((j+r)%2===0){
  let minimum=d.get(j+","+(-r));
  for(const t of [j-1,j+1])if(t>=0&&t<N){const a=cover[r+1][t];if(a!==null&&a<minimum)minimum=a;}
  cover[r][j]=minimum;
 }
 let coneChecks=0;
 for(const [j,k] of events)if(k>0){
  const minimum=cover[k][j];if(minimum!==null&&d.get(j+","+k)+minimum<D)throw Error("covering inequality");coneChecks++;
 }
 const raw=new Map();raw.set("center",D);
 for(const [j,k] of events)raw.set(j+","+k,BigInt(1+ +(k>0))*D-d.get(j+","+k));
 const values=Array.from(new Set(raw.values())).sort((a,b)=>a<b?-1:a>b?1:0),ids=new Map(values.map((a,i)=>[String(a),i])),INF=values.length,B=INF+1;
 const costs=new Map(Array.from(raw,([key,a])=>[key,ids.get(String(a))]));
 function charge(j,k){const id=costs.get(k===0?"center":j+","+k);if(id===undefined)throw Error("unpriced normalized event");return id;}
 // Independent pursuit relaxation. Each clock separately follows the fastest
 // route to its own endpoint. Transport makes its prices nonincreasing and no
 // larger than the same clock's prices along any actual continuation. Summing
 // the two independent lower costs is valid even though the pursuits differ.
 // After time 2, Qout makes both surviving running records constant.
 const pursuit=options.pursuit!==false&&c.qout_verified;
 let directIds=null,directSums=null;
 if(pursuit){
  directIds=Array.from({length:C+1},()=>new Int32Array(2*R+1).fill(-1));
  directSums=Array.from({length:C+1},()=>new Array(2*R+1).fill(0n));
  for(let j=0;j<=C;j++)for(let x=-R+1;x<=R;x++)if((j+x)%2===0)directIds[j][x+R]=charge(j,x);
  for(let j=C-1;j>=0;j--)for(let x=-R+1;x<=R;x++)if((j+x)%2===0){
   const id=directIds[j][x+R],next=directIds[j+1][x-1+R];
   if(next>=0&&next>id)throw Error("Qout direct-pursuit prices are not monotone");
   directSums[j][x+R]=values[id]+directSums[j+1][x-1+R];
  }
 }
 function directLower(j,x,record){
  const remaining=C-j,steps=Math.min(remaining,x+R);
  let lo=0,hi=steps;
  if(record!==INF)while(lo<hi){const m=(lo+hi)>>1;if(directIds[j+m][x-m+R]>record)lo=m+1;else hi=m;}
  const prefix=record===INF?directSums[j][x+R]:BigInt(lo)*values[record]+directSums[j+lo][x-lo+R];
  const rate=x+R<=remaining?0n:values[Math.min(record,directIds[C][x-remaining+R])];
  return [prefix,rate];
 }
 function pursuitLower(j,s){
  const remaining=C-j,reach=s.c?remaining:remaining-Math.abs(s.k);
  if(reach<0)return null;
  const low=s.c?Math.max(-R,s.k-reach):Math.max(-R,-reach),high=s.c?Math.min(R,s.k+reach):Math.min(R,reach);
  const [leftPrefix,a]=directLower(j,s.k,s.mm),[rightPrefix,b]=directLower(j,-s.k,s.mp);
  const leftTour=BigInt(R+low)*a+BigInt(3*R+low)*b;
  const rightTour=BigInt(3*R-high)*a+BigInt(R-high)*b;
  return s.cost+leftPrefix+rightPrefix+(leftTour<rightTour?leftTour:rightTour);
 }
 const numericKeys=(2*R+1)*2*B*B<=Number.MAX_SAFE_INTEGER;
 function stateKey(s){return numericKeys?(((s.k+R)*2+ +s.c)*B+s.mm)*B+s.mp:[s.k,+s.c,s.mm,s.mp].join(",");}
 function pareto(states){
  if(options.pareto===false)return states;
  const groups=new Map();
  for(const s of states.values()){const key=s.k+","+ +s.c;if(!groups.has(key))groups.set(key,[]);groups.get(key).push(s);}
  const keep=new Map();
  for(const group of groups.values()){
   group.sort((a,b)=>a.mm-b.mm||a.mp-b.mp||(a.cost<b.cost?-1:a.cost>b.cost?1:0));
   const ps=Array.from(new Set(group.map(s=>s.mp))).sort((a,b)=>a-b),rank=new Map(ps.map((p,i)=>[p,i+1])),tree=new Array(ps.length+1).fill(null);
   for(const s of group){
    const r=rank.get(s.mp);let best=null;
    for(let i=r;i>0;i-=i&-i)if(tree[i]!==null&&(best===null||tree[i]<best))best=tree[i];
    if(best!==null&&best<=s.cost)continue;
    keep.set(stateKey(s),s);
    for(let i=r;i<tree.length;i+=i&-i)if(tree[i]===null||s.cost<tree[i])tree[i]=s.cost;
   }
  }
  return keep;
 }
 const tails=new Map();
 function tail(j,k,first,center){
  const key=[j,k,first,+center].join(",");if(tails.has(key))return tails.get(key);
  let t=j,x=k,em=x===-R,ep=x===R,cc=center,mm=INF,mp=INF;
  const cm=[],cp=[],moves=[];
  for(const target of [first,-first])while(x!==target){
   if(!cc&&t>=C){tails.set(key,null);return null;}
   if(!em){mm=Math.min(mm,charge(t,x));cm.push(mm);}
   if(!ep){mp=Math.min(mp,charge(t,-x));cp.push(mp);}
   const step=target>x?1:-1;if(options.witness)moves.push(step);x+=step;t++;
   cc=cc||x===0;em=em||x===-R;ep=ep||x===R;
  }
  if(!cc||t>N)throw Error("illegal normalized suffix");
  function summary(a){const sum=[0n];for(const id of a)sum.push(sum.at(-1)+values[id]);return {a,sum};}
  const out={minus:summary(cm),plus:summary(cp),moves};tails.set(key,out);return out;
 }
 function evaluate(summary,record){
  const {a,sum}=summary;if(record===INF)return sum.at(-1);
  let lo=0,hi=a.length;while(lo<hi){const mid=(lo+hi)>>1;if(a[mid]>=record)lo=mid+1;else hi=mid;}
  return values[record]*BigInt(lo)+sum.at(-1)-sum[lo];
 }
 let layer=new Map(),best=null,bestState=null,bestTail=null,states=0,generated=0,maxLayer=0,pursuitPruned=0,centerPruned=0,terminalChecks=0;
 for(let k=-R;k<=R;k+=2){const s={k,c:k===0,mm:INF,mp:INF,cost:0n,prev:null,step:0,start:options.witness?k:0};layer.set(stateKey(s),s);}
 for(let j=0;j<=C;j++){
  layer=pareto(layer);states+=layer.size;maxLayer=Math.max(maxLayer,layer.size);const next=new Map();
  for(const s of layer.values()){
   if(!s.c&&C-j<Math.abs(s.k)){centerPruned++;continue;}
   const cutoff=target===null?best:target;
   if(pursuit&&cutoff!==null){const bound=pursuitLower(j,s);if(bound===null){centerPruned++;continue;}if(bound>=cutoff){pursuitPruned++;continue;}}
   const endpoint=Math.abs(s.k)===R;
   if(endpoint||j===C){
    if(!endpoint&&!s.c)continue;
    for(const first of endpoint?[s.k]:[-R,R]){
     const q=tail(j,s.k,first,s.c);if(q===null)continue;
     const value=s.cost+evaluate(q.minus,s.mm)+evaluate(q.plus,s.mp);
     terminalChecks++;
     if(target!==null&&value<target)throw Error("target lower bound fails: complete normalized path has units "+value+" < "+target);
     if(best===null||value<best){best=value;bestState=s;bestTail=q;}
    }
    continue;
   }
   const mm=Math.min(s.mm,charge(j,s.k)),mp=Math.min(s.mp,charge(j,-s.k)),cost=s.cost+values[mm]+values[mp];
   for(const step of [-1,1]){
    const k=s.k+step,cc=s.c||k===0;if(!cc&&j+1>=C)continue;
    const z={k,c:cc,mm,mp,cost,prev:options.witness?s:null,step:options.witness?step:0,start:options.witness?s.start:0},id=stateKey(z),old=next.get(id);
    if(!old||cost<old.cost)next.set(id,z);generated++;
   }
  }
  layer=next;
 }
 if(best===null&&target===null)throw Error("no normalized physical path");
 const certified=target===null?best:target;
 const value=fraction(certified,4n*BigInt(n)*D),lower=fraction(certified-2n*D,4n*BigInt(n)*D);
 const report={status:"PASS",scope:c.qout_verified?"full-bank profile dual via exact sticky/outward2 normalization; global lower via common quantization":"normalized physical bank dual; global lower uses exact bank normalization and common quantization",n,
  qout_verified:!!c.qout_verified,
  verification_mode:target===null?"exact minimum":"target lower bound",attainment_checked:target===null||best===target,
  verified_lower_units:String(certified),objective_denominator:String(4n*BigInt(n)*D),
  exact_scaled_dual:fraction(certified,D),normalized_bank_lower:value,global_lower:lower,record_states:states,generated_transitions:generated,max_layer_states:maxLayer,
  cached_suffixes:tails.size,covering_queries:coneChecks,covering_method:"quadratic cone suffix minima",pareto:options.pareto!==false,
  pursuit_pruning:!!pursuit,pursuit_pruned_states:pursuitPruned,center_unreachable_states:centerPruned,complete_path_checks:terminalChecks};
 if(c.minimum_units!==undefined&&BigInt(c.minimum_units)!==certified)throw Error("claimed native minimum differs");
 if(c.objective_denominator!==undefined&&BigInt(c.objective_denominator)!==4n*BigInt(n)*D)throw Error("claimed objective denominator");
 if(c.global_lower!==undefined&&c.global_lower!==lower)throw Error("claimed global lower");
 if(c.normalized_bank_dual_value!==undefined&&c.normalized_bank_dual_value!==value)throw Error("claimed normalized value");
 if(c.paths){
  const p=inspectPrimal(c);report.primal_global_upper=fraction(p.primal,4n*BigInt(n)*p.W);
  report.exact_primal_dual_equality=p.primal*D===certified*p.W;
  if(p.primal*D<certified*p.W)throw Error("normalized lower exceeds physical primal upper");
  if(c.exact_value&&c.exact_value!==report.primal_global_upper)throw Error("claimed primal value");
 }
 if(options.witness){
  const moves=[];for(let p=bestState;p.prev;p=p.prev)moves.push(p.step);moves.reverse();moves.push(...bestTail.moves);
  const positions=[bestState.start];for(const step of moves)positions.push(positions.at(-1)+step);
  function calendar(sign,end){const a=new Map();let current=INF,when=-1;for(let j=0;j<end;j++){const id=charge(j,sign*positions[j]);if(id<current){current=id;when=j;}a.set(when,(a.get(when)||0)+1);}return Array.from(a);}
  report.attaining_calendar={start_grid:bestState.start,moves,minus_charges:calendar(1,positions.indexOf(-R)),plus_charges:calendar(-1,positions.indexOf(R))};
 }
 return report;
}
module.exports={expandNodalInput,verifyNormalizedDual};
if(require.main===module){
 const fs=require("node:fs"),crypto=require("node:crypto"),{readField}=require("./qout_field_codec.cjs"),file=process.argv[2];
 if(!file)throw Error("usage: node normalized_record_pricing.cjs certificate.json [--no-pareto] [--no-pursuit] [--witness] [--target-bound]");
 try{const start=Date.now(),input=readField(file);if(process.argv.includes("--target-bound")&&input.minimum_units===undefined)throw Error("target-bound input must specify minimum_units");const report=verifyNormalizedDual(input,{pareto:!process.argv.includes("--no-pareto"),pursuit:!process.argv.includes("--no-pursuit"),witness:process.argv.includes("--witness"),targetUnits:process.argv.includes("--target-bound")?input.minimum_units:undefined});report.input_sha256=crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");report.elapsed_ms=Date.now()-start;process.stdout.write(JSON.stringify(report,null,2)+"\n");}
 catch(error){process.stderr.write(error.stack+"\n");process.exitCode=1;}
}
