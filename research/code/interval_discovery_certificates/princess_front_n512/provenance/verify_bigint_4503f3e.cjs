"use strict";
// Independent target-bound replay. Costs and all pursuit sums are BigInt.
// Compact uint32 nodal probabilities are decoded directly; no event/discount
// Map, beam, state cap, floating comparison, or attaining witness is used.
const fs=require("node:fs"),crypto=require("node:crypto"),zlib=require("node:zlib");
function sha(raw){return crypto.createHash("sha256").update(raw).digest("hex");}
function fraction(a,b){let x=a<0n?-a:a,y=b;while(y){const r=x%y;x=y;y=r;}return b/x===1n?String(a/x):String(a/x)+"/"+String(b/x);}

function decode(input){
 const n=input.n,D=BigInt(input.field_denominator);
 if(!Number.isSafeInteger(n)||n<1||n>10000||D<=0n||D>=2n**32n)throw Error("unsupported compact dimensions or denominator");
 if(input.format!=="qout-clock-grid-field-u32-zlib-v1"||input.normalized_profile!==true)throw Error("compact normalized field required");
 const count=(4*n+1)*n,e=input.encoding;
 if(e.count!==count||e.integer_type!=="uint32 little-endian"||e.compression!=="zlib")throw Error("compact encoding metadata");
 const text=input.pre_two_values_base64;
 if(typeof text!=="string"||text.length%4||!/^[A-Za-z0-9+/]*={0,2}$/.test(text))throw Error("invalid base64 field");
 const packed=Buffer.from(text,"base64");if(packed.toString("base64")!==text)throw Error("noncanonical base64 field");
 const raw=zlib.inflateSync(packed,{maxOutputLength:4*count});
 if(raw.length!==4*count||sha(raw)!==e.uncompressed_sha256)throw Error("compact field length or hash");
 const pre=new Uint32Array(count),Dn=Number(D),R=2*n,C=4*n,H=12*n;
 for(let i=0;i<count;i++){const value=raw.readUInt32LE(4*i);if(value>Dn)throw Error("nodal range");pre[i]=value;}
 function radial(j,k){if(k===0)return 0;if(j>C){k-=j-C;j=C;}return k<=0?0:pre[j*n+((k-1)>>1)];}
 let coneChecks=0,frontChecks=0,front=true;
 for(let j=0;j<=H;j++)for(let k=j%2;k<=R;k+=2){
  const value=radial(j,k);
  if(k<R)for(const step of [-1,1])if(j+step>=0&&j+step<=H){
   if(value>radial(j+step,k+1))throw Error("radial transport inequality");coneChecks++;
  }
  if(j+k>C){const d=(j+k-C)/2,foot=k-d;
   if(value!==(foot<=0?0:radial(j-d,foot)))front=false;frontChecks++;
  }
 }
 for(let j=0;j<C;j+=2)if(radial(j+2,R)>radial(j,R))throw Error("sticky endpoint identity");
 // Outward2 is the explicit decoder rule, checked independently in pricing
 // by the monotone direct pursuits below; no full-table expansion is needed.
 const unique=new Set([0,Dn,2*Dn]);
 for(const g of pre){unique.add(Dn+g);unique.add(Dn-g);}
 const numbers=Array.from(unique).sort((a,b)=>a-b),ids=new Map(numbers.map((v,i)=>[v,i]));
 const values=numbers.map(BigInt),positive=new Uint32Array(count),negative=new Uint32Array(count);
 for(let i=0;i<count;i++){positive[i]=ids.get(Dn+pre[i]);negative[i]=ids.get(Dn-pre[i]);}
 const center=ids.get(Dn),initial=ids.get(2*Dn);
 function charge(j,k){if(k===0)return center;const minus=k<0;k=Math.abs(k);if(j>C){k-=j-C;j=C;}if(k<=0)return center;
  return (minus?negative:positive)[j*n+((k-1)>>1)];}
 return {n,D,R,C,H,values,initial,charge,front,coneChecks,frontChecks,compactNodes:count};
}

function verify(input,options={}){
 const began=Date.now(),f=decode(input),{n,D,R,C,H,values,initial,charge}=f;
 const target=BigInt(options.targetUnits??input.minimum_units??input.certified_bank_lower_units??(()=>{throw Error("target units required");})());
 if(target<0n)throw Error("negative target");
 if(options.front===true&&!f.front)throw Error("incoming-front-two identities required");
 const useFront=options.front!==false&&f.front,pursuit=options.pursuit!==false,B=values.length;
 const numeric=(2*R+1)*2*B*B<=Number.MAX_SAFE_INTEGER,pairNumeric=B*B<=Number.MAX_SAFE_INTEGER;
 function key(s){return numeric?(((s.k+R)*2+ +s.c)*B+s.mm)*B+s.mp:[s.k,+s.c,s.mm,s.mp].join(",");}
 function pair(s){return pairNumeric?s.mm*B+s.mp:s.mm+","+s.mp;}
 function put(map,s){const k=key(s),old=map.get(k);if(!old||s.cost<old.cost)map.set(k,s);}
 const paths=[];
 // Each characteristic is the independent fastest pursuit of the left
 // endpoint. This checks monotonicity and stores arbitrary-precision sums.
 for(let u=-R;u<=C+R;u+=2){
  const first=Math.max(0,u-R),a=[],sum=[0n];
  for(let j=first;j<u+R;j++){
   const id=charge(j,u-j);if(a.length&&id>a.at(-1))throw Error("nonmonotone independent pursuit");
   a.push(id);sum.push(sum.at(-1)+values[id]);
  }
  paths.push({first,a:Int32Array.from(a),sum});
 }
 function directCost(j,x,record,through){
  const p=paths[(j+x+R)/2],begin=j-p.first,end=Math.min(through,j+x+R)-p.first;
  let lo=begin,hi=end;while(lo<hi){const m=(lo+hi)>>1;if(p.a[m]>record)lo=m+1;else hi=m;}
  return BigInt(lo-begin)*values[record]+p.sum[end]-p.sum[lo];
 }
 function lower(j,s){
  const duration=C-j,reach=s.c?duration:duration-Math.abs(s.k);if(reach<0)return null;
  const prefix=directCost(j,s.k,s.mm,C)+directCost(j,-s.k,s.mp,C);
  const a=s.k+R<=duration?0n:values[Math.min(s.mm,charge(C,s.k-duration))];
  const b=R-s.k<=duration?0n:values[Math.min(s.mp,charge(C,-s.k-duration))];
  const low=s.c?Math.max(-R,s.k-duration):Math.max(-R,-reach);
  const high=s.c?Math.min(R,s.k+duration):Math.min(R,reach);
  const left=BigInt(R+low)*a+BigInt(3*R+low)*b;
  const right=BigInt(3*R-high)*a+BigInt(R-high)*b;
  return s.cost+prefix+(left<right?left:right);
 }
 let retained=0,generated=0,dominated=0,maxLayer=0,boundPruned=0,centerPruned=0,returns=0,jumpedSteps=0,terminals=0,frontTerminals=0,attained=false;
 function check(value){terminals++;if(value<target)throw Error("target lower fails: complete physical path units "+value+" < "+target);if(value===target)attained=true;}
 function terminal(j,s){
  if(Math.abs(s.k)===R){
   if(!s.c&&j+R>C)return;
   check(s.cost+(s.k===R?directCost(j,s.k,s.mm,H):directCost(j,-s.k,s.mp,H)));return;
  }
  if(!s.c)return;
  const a=values[Math.min(s.mm,charge(j,s.k))],b=values[Math.min(s.mp,charge(j,-s.k))];
  check(s.cost+BigInt(R+s.k)*a+BigInt(3*R+s.k)*b);
  check(s.cost+BigInt(3*R-s.k)*a+BigInt(R-s.k)*b);
 }
 function pareto(states){
  if(options.pareto===false)return states;
  const groups=new Map();for(const s of states.values()){const id=2*(s.k+R)+ +s.c;if(!groups.has(id))groups.set(id,[]);groups.get(id).push(s);}
  const kept=new Map();
  for(const group of groups.values()){
   group.sort((a,b)=>a.mm-b.mm||a.mp-b.mp||(a.cost<b.cost?-1:a.cost>b.cost?1:0));
   const ps=Array.from(new Set(group.map(s=>s.mp))).sort((a,b)=>a-b),rank=new Map(ps.map((p,i)=>[p,i+1])),tree=new Array(ps.length+1).fill(null);
   for(const s of group){const r=rank.get(s.mp);let best=null;
    for(let i=r;i;i-=i&-i)if(tree[i]!==null&&(best===null||tree[i]<best))best=tree[i];
    if(best!==null&&best<=s.cost){dominated++;continue;}
    kept.set(key(s),s);for(let i=r;i<tree.length;i+=i&-i)if(tree[i]===null||s.cost<tree[i])tree[i]=s.cost;
   }
  }
  return kept;
 }
 let layer=new Map();const pending=Array.from({length:C+1},()=>new Map());
 for(let k=0;k<=R;k+=2)put(layer,{k,c:k===0,mm:initial,mp:initial,cost:0n});
 for(let j=0;j<=C;j++){
  for(const s of pending[j].values())put(layer,s);pending[j].clear();
  layer=pareto(layer);retained+=layer.size;maxLayer=Math.max(maxLayer,layer.size);
  const next=new Map();
  for(const s of layer.values()){
   if(Math.abs(s.k)===R){terminal(j,s);continue;}
   if(j===C||(useFront&&s.c&&j+Math.abs(s.k)>=C)){if(j<C)frontTerminals++;terminal(j,s);continue;}
   if(!s.c&&Math.abs(s.k)>C-j){centerPruned++;continue;}
   if(pursuit){const bound=lower(j,s);if(bound===null){centerPruned++;continue;}if(bound>=target){boundPruned++;continue;}}
   const mm=Math.min(s.mm,charge(j,s.k)),mp=Math.min(s.mp,charge(j,-s.k)),rate=values[mm]+values[mp];
   let steps;
   if(!s.c)steps=[-1,1];
   else if(s.k===0)steps=[mm<=mp?1:-1];
   else{
    const outward=s.k>0?1:-1;steps=[outward];
    if(s.k>0?mp<=mm:mm<=mp){
     const duration=Math.min(Math.abs(s.k),C-j),t=j+duration,k=s.k-outward*duration;
     const z={k,c:true,mm,mp,cost:s.cost+BigInt(duration)*rate};returns++;jumpedSteps+=duration;generated++;
     if(t===C)terminal(t,z);
     else if(pursuit&&lower(t,z)>=target)boundPruned++;
     else{const id=pair(z),old=pending[t].get(id);if(!old||z.cost<old.cost)pending[t].set(id,z);}
    }
   }
   for(const step of steps){const k=s.k+step,c=s.c||k===0;if(!c&&j+1>=C)continue;
    put(next,{k,c,mm,mp,cost:s.cost+rate});generated++;
   }
  }
  layer=next;
  if(options.progress&&j%options.progress===0)process.stderr.write(JSON.stringify({event:"bigint_progress",time_index:j,total_ticks:C,retained_states:retained,generated_transitions:generated,next_states:layer.size,elapsed_ms:Date.now()-began})+"\n");
 }
 const scale=4n*BigInt(n)*D,value=fraction(target,scale),global=fraction(target-2n*D,scale);
 if(input.objective_denominator!==undefined&&BigInt(input.objective_denominator)!==scale)throw Error("claimed denominator mismatch");
 if(input.minimum_units!==undefined&&options.targetUnits===undefined&&BigInt(input.minimum_units)!==target)throw Error("claimed target mismatch");
 if(input.global_lower!==undefined&&options.targetUnits===undefined&&input.global_lower!==global)throw Error("claimed global lower mismatch");
 if(input.normalized_bank_dual_value!==undefined&&options.targetUnits===undefined&&input.normalized_bank_dual_value!==value)throw Error("claimed native value mismatch");
 return {status:"PASS",scope:"Independent BigInt target lower on the complete normalized physical bank using proved center normal forms; game lower uses the existing transfer. No exact-minimum or same-CDF security assertion.",n,
  verification_mode:"target lower bound",attainment_checked:attained,verified_lower_units:String(target),objective_denominator:String(scale),normalized_bank_lower:value,global_lower:global,
  compact_nodes:f.compactNodes,validated_radial_cone_inequalities:f.coneChecks,qout_verified:true,sticky_verified:true,incoming_front_verified:f.front,center_policy:useFront?4:3,
  record_ids:values.length,record_states:retained,generated_transitions:generated,dominated_states:dominated,max_layer_states:maxLayer,pursuit_pruning:pursuit,pursuit_pruned_states:boundPruned,
  center_unreachable_states:centerPruned,deterministic_return_jumps:returns,jumped_unit_steps:jumpedSteps,complete_path_checks:terminals,front_terminal_checks:frontTerminals,
  pareto:options.pareto!==false,cost_arithmetic:"BigInt throughout",elapsed_ms:Date.now()-began,
  peak_resident_kib:process.resourceUsage().maxRSS,final_heap_bytes:process.memoryUsage().heapUsed};
}

module.exports={decode,verify};
if(require.main===module){
 try{
  const args=process.argv.slice(2),file=args[0];if(!file)throw Error("usage: node verify_bigint.cjs field.json [--target-units N] [--front] [--no-front] [--no-pareto] [--no-pursuit] [--progress N]");
  function option(name){const i=args.indexOf(name);return i<0?undefined:args[i+1];}
  const raw=fs.readFileSync(file),data=JSON.parse(raw[0]===31&&raw[1]===139?zlib.gunzipSync(raw):raw);
  const report=verify(data,{targetUnits:option("--target-units"),front:args.includes("--front")?true:args.includes("--no-front")?false:undefined,
    pareto:!args.includes("--no-pareto"),pursuit:!args.includes("--no-pursuit"),progress:Number(option("--progress")??0)});
  report.input_sha256=sha(raw);report.verifier_source_sha256=sha(fs.readFileSync(__filename));
  process.stdout.write(JSON.stringify(report,null,2)+"\n");
 }catch(error){process.stderr.write(error.stack+"\n");process.exitCode=1;}
}
