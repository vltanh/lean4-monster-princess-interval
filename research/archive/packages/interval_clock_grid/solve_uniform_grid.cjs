// Numerical discovery uses adjacent nodal transport inequalities and physical-record pricing.
// Exact rational reconstruction and the independent BigInt record verifier are mandatory.
"use strict";
const {SmallLP}=require("./small_lp.cjs");
const {integerMatching,fraction}=require("./exact_certificate.cjs");
const {inspectUniformPlans:inspectPlans,uniformGeometry:geometry,verifyUniform:priceRecordDual}=require("./uniform_certificate.cjs");
const {typeOrder,pricePhysical,planColumn}=require("./uniform_pricing.cjs");


function solveNodalColumns(g,columns){
 const nodes=g.events.filter(z=>z[1]>0),loc=new Map(nodes.map((z,i)=>[z.join(","),i])),order=typeOrder(nodes);
 const size=nodes.length+1,offset=nodes.length+order.length,rows=offset+columns.length;
 const A=Array.from({length:rows},()=>new Float64Array(size)),b=new Float64Array(rows),c=new Float64Array(size);
 c[size-1]=1;
 for(let i=0;i<nodes.length;i++){A[i][i]=1;b[i]=1;}
 for(let i=0;i<order.length;i++){const [u,v]=order[i];A[nodes.length+i][u]=1;A[nodes.length+i][v]=-1;}
 for(let i=0;i<columns.length;i++){
  const row=A[offset+i],col=columns[i];row[size-1]=1;b[offset+i]=col.cost;
  for(let e=0;e<g.events.length;e++)if(col.counts[e]){
   const [t,x]=g.events[e],v=loc.get(t+","+Math.abs(x));
   row[v]+=(x>0?-1:1)*col.counts[e];
   if(x>0)b[offset+i]-=col.counts[e];
  }
 }
 const raw=new SmallLP(A,b,c).solve();if(raw.status!=="optimal")throw Error("nodal LP "+raw.status);
 let violation=0,reduced=0;
 for(let i=0;i<rows;i++){let s=0;for(let j=0;j<size;j++)s+=A[i][j]*raw.x[j];violation=Math.max(violation,s-b[i]);}
 for(let j=0;j<size;j++){let s=0;for(let i=0;i<rows;i++)s+=A[i][j]*raw.dual[i];reduced=Math.min(reduced,s-c[j]);}
 if(violation>1e-7||reduced< -1e-7||Math.min(...raw.x)< -1e-7||Math.min(...raw.dual)< -1e-7)throw Error("nodal LP residual");
 const profile=raw.x.slice(0,nodes.length),discounts=g.events.map(([t,x])=>{
  const v=profile[loc.get(t+","+Math.abs(x))];return x>0?1-v:v;
 });
 return {...raw,x:raw.dual.slice(offset),minimum:raw.value,discounts,nodal_nodes:nodes,nodal_values:profile,
  nodal_order:order,nodal_dual:raw.dual,violation,reduced};
}

async function solveUniformGrid(n,options={}){
 const g=geometry(n),columns=[],seen=new Set(),history=[];
 function add(plan){
  const col=planColumn(g,plan),key=col.cost+":"+col.counts.join(",");
  if(seen.has(key))return false;seen.add(key);columns.push(col);return true;
 }
 add({start_grid:2*n,moves:new Array(4*n).fill(-1),minus_charges:Array.from({length:4*n},(_,j)=>[j,1]),plus_charges:[]});
 add({start_grid:0,moves:[...new Array(n).fill(1),...new Array(3*n).fill(-1),...new Array(4*n).fill(1)],
  minus_charges:[[0,3*n],[3*n,n]],plus_charges:[[0,n],[n,7*n]]});
 for(let it=0;it<(options.maxIterations??200);it++){
  const result=solveNodalColumns(g,columns),priced=pricePhysical(g,result.discounts);
  const report={it,columns:columns.length,upper:result.minimum/(4*n),priced:priced.value/(4*n),
   gap:(result.minimum-priced.value)/(4*n),pivots:result.pivots,record_states:priced.record_states,max_layer:priced.max_layer};
  history.push(report);
  const numerical={n,model:{pressure_nodes:g.events.length,matching_edges:g.matches.length},columns:columns.length,column_plans:columns.map(c=>c.plan),result,priced_value:priced.value,history,
   paths:columns.map((col,i)=>({weight:result.x[i],...col.plan})).filter(p=>p.weight>1e-9)};
  if(options.onIteration)await options.onIteration(report,numerical);
  if(result.minimum-priced.value<=1e-8)return {numerical,...certifyNodal(numerical,g)};
  let added=false;
  for(const choice of priced.choices)if(choice.value<result.minimum-1e-8)added=add(choice.plan)||added;
  if(!added)throw Error("record pricing stalled");
 }
 throw Error("record column iteration limit");
}
module.exports={geometry,pricePhysical,planColumn,certifyNodal,solveUniformGrid};

function bigGcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const r=a%b;a=b;b=r;}return a;}
function rat(a,b=1n){if(b===0n)throw Error("zero rational denominator");if(b<0n){a=-a;b=-b;}const g=bigGcd(a,b);return {a:a/g,b:b/g};}
function addRat(x,y){return rat(x.a*y.b+y.a*x.b,x.b*y.b);}
function mulRat(x,y){return rat(x.a*y.a,x.b*y.b);}
function subRat(x,y){return rat(x.a*y.b-y.a*x.b,x.b*y.b);}
function exactSystem(rows,rhs,variables){
 const basis=[],selected=[];
 for(let ri=0;ri<rows.length;ri++){
  const v=rows[ri].map(Number);
  for(const b of basis){const a=v[b.p];if(a!==0)for(let j=b.p;j<variables;j++)v[j]-=a*b.v[j];}
  let p=0;while(p<variables&&Math.abs(v[p])<1e-9)p++;
  if(p===variables)continue;
  const a=v[p];for(let j=p;j<variables;j++)v[j]/=a;
  basis.push({p,v});basis.sort((a,b)=>a.p-b.p);selected.push(ri);
  if(selected.length===variables)break;
 }
 if(selected.length<variables)throw Error("equation rank "+selected.length+"/"+variables);
 const A=selected.map(i=>[...rows[i].map(BigInt),BigInt(rhs[i])]);
 let old=1n;
 for(let k=0;k<variables-1;k++){
  let p=k;while(p<variables&&A[p][k]===0n)p++;if(p===variables)throw Error("exact rank deficiency");
  if(p!==k)[A[p],A[k]]=[A[k],A[p]];
  const pivot=A[k][k];
  for(let i=k+1;i<variables;i++){
   for(let j=k+1;j<=variables;j++){
    const z=A[i][j]*pivot-A[i][k]*A[k][j];if(z%old!==0n)throw Error("Bareiss division");
    A[i][j]=z/old;
   }
   A[i][k]=0n;
  }
  old=pivot;
 }
 const x=new Array(variables);
 for(let i=variables-1;i>=0;i--){
  let z=rat(A[i][variables]);
  for(let j=i+1;j<variables;j++)z=subRat(z,mulRat(rat(A[i][j]),x[j]));
  x[i]=mulRat(z,rat(1n,A[i][i]));
 }
 for(let i=0;i<rows.length;i++){
  let z=rat(0n);for(let j=0;j<variables;j++)if(rows[i][j])z=addRat(z,mulRat(rat(BigInt(rows[i][j])),x[j]));
  if(z.a!==BigInt(rhs[i])*z.b)throw Error("inconsistent exact active equations at "+i);
 }
 return x;
}
function denominatorVector(x){
 let D=1n;for(const r of x)D=D/bigGcd(D,r.b)*r.b;
 return {denominator:D,numerators:x.map(r=>r.a*(D/r.b))};
}

function certifyNodal(numerical,g){
 const z=numerical.result,nodes=z.nodal_nodes,order=z.nodal_order,values=z.nodal_values;
 const K=nodes.length,offset=K+order.length,loc=new Map(nodes.map((a,i)=>[a.join(","),i]));
 const columns=numerical.column_plans.map(p=>planColumn(g,p));
 const rowVectors=[],rowBounds=[];
 for(let i=0;i<K;i++){const a=new Array(K+1).fill(0);a[i]=1;rowVectors.push(a);rowBounds.push(1);}
 for(const [u,v] of order){const a=new Array(K+1).fill(0);a[u]=1;a[v]=-1;rowVectors.push(a);rowBounds.push(0);}
 for(const col of columns){
  const a=new Array(K+1).fill(0);a[K]=1;let b=col.cost;
  for(let e=0;e<g.events.length;e++)if(col.counts[e]){
   const [t,x]=g.events[e],i=loc.get(t+","+Math.abs(x));
   a[i]+=(x>0?-1:1)*col.counts[e];if(x>0)b-=col.counts[e];
  }
  rowVectors.push(a);rowBounds.push(b);
 }
 // Reconstruct the positive dual support from exact active stationarity equations.
 const support=z.nodal_dual.map((a,i)=>[a,i]).filter(a=>a[0]>1e-9).map(a=>a[1]);
 const dualRows=[],dualRhs=[];
 for(let j=0;j<=K;j++){
  const a=support.map(i=>rowVectors[i][j]),target=j===K?1:0;
  const residue=a.reduce((s,b,k)=>s+b*z.nodal_dual[support[k]],-target);
  if(Math.abs(residue)<1e-8){dualRows.push(a);dualRhs.push(target);}
 }
 const dy=exactSystem(dualRows,dualRhs,support.length),dualMap=new Map(support.map((i,j)=>[i,dy[j]]));
 const w=columns.map((_,i)=>dualMap.get(offset+i)||rat(0n)),wv=denominatorVector(w);
 if(wv.numerators.some(a=>a<0n)||wv.numerators.reduce((a,b)=>a+b,0n)!==wv.denominator)throw Error("exact nodal weights");
 // Reconstruct the primal profile after contracting every tight transport edge.
 const parent=Array.from({length:K},(_,i)=>i);
 function root(i){while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i];}return i;}
 for(const [a,b] of order)if(Math.abs(values[a]-values[b])<1e-8)parent[root(a)]=root(b);
 const group=new Map();for(let i=0;i<K;i++){const r=root(i);if(!group.has(r))group.set(r,[]);group.get(r).push(i);}
 const unknown=[...group.keys()].filter(r=>values[group.get(r)[0]]>1e-8&&values[group.get(r)[0]]<1-1e-8);
 const uloc=new Map(unknown.map((r,i)=>[r,i])),profileRows=[],profileRhs=[];
 for(let i=0;i<columns.length;i++){
  const a=rowVectors[offset+i],b=rowBounds[offset+i],residue=a.slice(0,K).reduce((s,c,j)=>s+c*values[j],z.minimum-b);
  if(Math.abs(residue)>=1e-8)continue;
  const row=new Array(unknown.length+1).fill(0);row[unknown.length]=1;let rhs=b;
  for(let j=0;j<K;j++)if(a[j]){
   const r=root(j);if(uloc.has(r))row[uloc.get(r)]+=a[j];else rhs-=a[j]*Math.round(values[j]);
  }
  profileRows.push(row);profileRhs.push(rhs);
 }
 const ps=exactSystem(profileRows,profileRhs,unknown.length+1);
 const profile=nodes.map((_,i)=>uloc.has(root(i))?ps[uloc.get(root(i))]:rat(BigInt(Math.round(values[i]))));
 const pv=denominatorVector(profile),D=pv.denominator;
 if(pv.numerators.some(a=>a<0n||a>D))throw Error("exact nodal range");
 for(const [a,b] of order)if(pv.numerators[a]>pv.numerators[b])throw Error("exact nodal order");
 const plans=[];
 for(let i=0;i<columns.length;i++)if(wv.numerators[i]>0n)plans.push({weight_numerator:String(wv.numerators[i]),...columns[i].plan});
 const stats=inspectPlans(g.n,plans,wv.denominator),match=integerMatching(g,stats.pressure);
 const cert={scope:"Exact primal and independent physical-record dual certificate for the complete vertex-plus-uniform-leg clock-grid LP, reconstructed from the exact type-order master.",
  n:g.n,clock_types:"vertex_and_uniform_leg",completion_horizon:8,center_deadline:2,physical_step:"1/"+(2*g.n),pressure_step:"1/"+(4*g.n),objective_scale:"1/"+(4*g.n),
  weight_denominator:String(wv.denominator),paths:plans,matching:match.matching,
  discount_denominator:String(D),discounts:g.events.map(([t,x])=>[t,x,String(x>0?D-pv.numerators[loc.get(t+","+x)]:pv.numerators[loc.get(t+","+(-x))])]),
  exact_value:fraction(stats.mass+match.positive-match.flow,4n*BigInt(g.n)*wv.denominator),
  global_lower:fraction(stats.mass+match.positive-match.flow-2n*wv.denominator,4n*BigInt(g.n)*wv.denominator)};
 const v=ps.at(-1);
 if((stats.mass+match.positive-match.flow)*v.b!==v.a*wv.denominator)throw Error("exact restricted-master duality gap");
 return {certificate:cert,replay:priceRecordDual(cert),reconstruction:{positive_dual_variables:support.length,free_profile_components:unknown.length}};
}

if(require.main===module){
 const fs=require("node:fs"),path=require("node:path");
 const n=Number(process.argv[2]||4),prefix=process.argv[3]||path.join(__dirname,"uniform_n"+n);
 (async()=>{
  const out=await solveUniformGrid(n,{onIteration:async(report,numerical)=>{
   process.stderr.write(JSON.stringify(report)+"\n");
   fs.writeFileSync(prefix+"_checkpoint.json",JSON.stringify(numerical,null,2)+"\n");
  }});
  fs.writeFileSync(prefix+"_certificate.json",JSON.stringify(out.certificate,null,2)+"\n");
  fs.writeFileSync(prefix+"_record_replay.json",JSON.stringify(out.replay,null,2)+"\n");
  process.stdout.write(JSON.stringify({...out.replay,reconstruction:out.reconstruction},null,2)+"\n");
 })().catch(error=>{process.stderr.write(error.stack+"\n");process.exitCode=1;});
}
