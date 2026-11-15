/** Unrestricted atomic survival cut with monster coordinates in Q(epsilon).
 * Princess label sides use a subordinate infinitesimal delta.
 * Geometry is exact; discovery capacities are limits of positive germ rewards.
 */
module.exports = (function(){
function createGermAtomic(E,G){
 const smallConstants=new Map();
 class Coordinate{
  constructor(x){
   if(x instanceof Coordinate)return x;
   const g=G.Q(x);this._g=g;
   this.r=g.p.length===1&&g.q.length===1?g.p[0].dby(g.q[0]):null;
  }
  static rational(r){const out=Object.create(Coordinate.prototype);out.r=r;out._g=null;return out;}
  static of(x){
   if(x instanceof Coordinate)return x;
   if(typeof x==="number"&&Number.isInteger(x)||typeof x==="bigint"){
    const key=String(x);if(!smallConstants.has(key))smallConstants.set(key,new Coordinate(x));return smallConstants.get(key);
   }
   return new Coordinate(x);
  }
  get g(){if(this._g===null)this._g=G.Q(this.r);return this._g;}
  add(x){x=Coordinate.of(x);return this.r&&x.r?Coordinate.rational(this.r.a(x.r)):new Coordinate(this.g.a(x.g));}
  sub(x){x=Coordinate.of(x);return this.r&&x.r?Coordinate.rational(this.r.s(x.r)):new Coordinate(this.g.s(x.g));}
  mul(x){x=Coordinate.of(x);return this.r&&x.r?Coordinate.rational(this.r.m(x.r)):new Coordinate(this.g.m(x.g));}
  div(x){x=Coordinate.of(x);return this.r&&x.r?Coordinate.rational(this.r.dby(x.r)):new Coordinate(this.g.dby(x.g));}
  neg(){return this.r?Coordinate.rational(this.r.neg()):new Coordinate(this.g.neg());}
  abs(){return this.cmp(0)<0?this.neg():this;}
  cmp(x){x=Coordinate.of(x);return this.r&&x.r?this.r.cmp(x.r):this.g.cmp(x.g);}
  toString(){return this.r?this.r.str():this.g.str();}
  number(){return this.r?this.r.num():this.g.limit().num();}
 }
 const moduleSource="const Rational=(function(Cut,Physical){\n\nconst {Q}=Physical,zero=new Q(0n),two=new Q(2n);\nconst qmin=(a,b)=>a.cmp(b)<=0?a:b,qmax=(a,b)=>a.cmp(b)>=0?a:b;\nconst key=q=>q.toString();\nfunction search(a,x,strict){let l=0,r=a.length;while(l<r){const m=(l+r)>>1,c=a[m].cmp(x);if(c<0||strict&&c===0)l=m+1;else r=m;}return l;}\nfunction initialize(m,atoms){\n m.atoms=atoms;m.routes=atoms.map(a=>{const p=a.exact_light.map(r=>r.map(x=>new Q(x)));for(let j=0;j<p.length;j++){const[u,v]=p[j];if(u.add(v).cmp(zero)<0||u.sub(v).abs().cmp(two)>0)throw Error(\"nonphysical rational monster vertex\");if(j){const x=p[j-1];if(!((u.cmp(x[0])>0&&v.cmp(x[1])===0)||(v.cmp(x[1])>0&&u.cmp(x[0])===0)))throw Error(\"non-unit rational monster leg\");}}return[p,p.map(([u,v])=>[v,u])];});\n m.ge=function(x){x=new Q(x);const j=search(this.baseQ,x,false);return 3*j+(j<this.baseQ.length&&this.baseQ[j].cmp(x)===0?1:0);};\n m.gt=function(x){x=new Q(x);const j=search(this.baseQ,x,false);return 3*j+(j<this.baseQ.length&&this.baseQ[j].cmp(x)===0?2:0);};\n m.b=function(k){return this.baseQ[Math.floor(k/3)];};\n m.capture=function(route,labels){let[u0,v0]=route[0],p=labels[this.query.get(key(v0))],ge=this.ge(u0),gt=this.gt(u0);if(p>=ge&&p<gt)return u0.add(v0).div(two);const above=p>=gt;\n  for(let k=1;k<route.length;k++){const[u1,v1]=route[k];if(u1.cmp(u0)>0&&above){p=labels[this.query.get(key(v0))];if(p<this.gt(u1))return this.b(p).add(v0).div(two);}else if(v1.cmp(v0)>0&&!above){const at=Cut.lower(labels,this.ge(u0)),cross=qmin(u0,this.vQ[at]);if(cross.cmp(v1)<=0)return u0.add(cross).div(two);}u0=u1;v0=v1;}throw Error(\"rational missing capture\");};\n m.rowExact=function(labels){return this.routes.map(rr=>this.capture(rr[0],labels).add(this.capture(rr[1],labels)).div(two));};\n m.row=function(labels){return this.rowExact(labels).map(x=>x.number());};\n m.compile=function(j){\n  const sums=new Map();const add=(pos,bits,c)=>{if(c.cmp(zero)===0)return;if(c.cmp(zero)<0)throw Error(\"negative germ reward\");const q=this.norm(pos,bits);if(q===null)return;const kk=(pos?\"+\":\"-\")+q.join(\",\");let id=this.defMap.get(kk);if(id===undefined){id=this.defs.length;this.defMap.set(kk,id);this.defs.push({pos,bits:q});}const prior=sums.get(id)||zero;sums.set(id,prior.add(c));};\n  const bit=(u,v,pos)=>[this.query.get(key(v)),pos?this.gt(u):this.ge(u)];\n  for(const route of this.routes[j]){let[u0,v0]=route[0],above=[bit(u0,v0,true)],below=[bit(u0,v0,false)];\n   for(let k=1;k<route.length;k++){const[u1,v1]=route[k];if(u1.cmp(u0)>0){const idx=this.query.get(key(v0));let old=qmax(zero,qmin(this.baseQ[0],u1).sub(u0));add(true,above,old);\n    for(let l=1;l<this.baseQ.length;l++){const z=qmax(zero,qmin(this.baseQ[l],u1).sub(u0));if(z.cmp(old)>0)add(true,above.concat([[idx,3*l]]),z.sub(old));old=z;}add(false,below,u1.sub(u0));\n   }else{add(true,above,v1.sub(v0));const left=this.query.get(key(v0)),right=this.query.get(key(v1)),th=this.ge(u0);for(let i=left;i<right;i++)add(false,below.concat([[i,th]]),qmax(zero,qmin(this.vQ[i+1],u0).sub(this.vQ[i])));}\n   above.push(bit(u1,v1,true));below.push(bit(u1,v1,false));u0=u1;v0=v1;\n  }}this.lastExactUnits=Array.from(sums);return Array.from(sums,([id,c])=>[id,c.number()]);\n };\n}\nfunction Model(atoms,extraQueries=[],extraBases=[]){\n const m=Object.create(Cut.Model.prototype);initialize(m,atoms);const vv=new Map([[\"-1\",new Q(-1n)]]),bb=new Map([[\"0\",zero]]);\n for(const x of extraQueries){const q=new Q(x);if(q.cmp(-1)<0)throw Error(\"query below virtual origin\");vv.set(key(q),q);}\n for(const x of extraBases){const q=new Q(x);if(q.cmp(0)<0)throw Error(\"negative player level\");bb.set(key(q),q);}\n for(const rr of m.routes)for(const r of rr)for(const[u,v]of r){vv.set(key(v),v);if(u.cmp(zero)>=0)bb.set(key(u),u);}\n m.vQ=Array.from(vv.values()).sort((a,b)=>a.cmp(b));for(const v of m.vQ){const lo=qmax(v,zero),hi=v.add(two);bb.set(key(lo),lo);bb.set(key(hi),hi);}\n m.baseQ=Array.from(bb.values()).sort((a,b)=>a.cmp(b));m.v=m.vQ.map(key);m.base=m.baseQ.map(key);m.L=3*m.base.length;m.query=new Map(m.v.map((v,i)=>[v,i]));\n m.bounds=m.vQ.map(v=>[m.ge(qmax(v,zero)),m.ge(v.add(two))]);m.bounds[0]=[m.ge(zero),m.ge(zero)];const last=m.ge(m.vQ.at(-1).add(two));m.bounds[m.bounds.length-1]=[last,last];\n m.offset=[];let n=0;for(const[lo,hi]of m.bounds){m.offset.push(n);n+=hi-lo;}m.N=n;m.defs=[];m.defMap=new Map();m.units=[];m.germUnits=[];for(let j=0;j<atoms.length;j++){m.units.push(m.compile(j));m.germUnits.push(m.lastExactUnits.slice());}return m;\n}\nfunction pack(m){return{v:m.v,base:m.base,bounds:m.bounds,offset:m.offset,N:m.N,defs:m.defs,units:m.units};}\nfunction restore(shape,atoms){const m=Object.create(Cut.Model.prototype);initialize(m,atoms);Object.assign(m,shape);m.vQ=m.v.map(x=>new Q(x));m.baseQ=m.base.map(x=>new Q(x));m.L=m.base.length*3;m.query=new Map(m.v.map((v,i)=>[v,i]));return m;}\nfunction lift(small,labels,full){let out=[],j=0;for(let i=0;i<full.vQ.length;i++){const v=full.vQ[i];while(j+1<small.vQ.length&&small.vQ[j+1].cmp(v)<=0)j++;let b=small.b(labels[j]),side=labels[j]%3-1;if(small.vQ[j].cmp(v)!==0){if(v.cmp(zero)>=0&&b.cmp(v)<=0){b=v;side=1;}else if(b.cmp(zero)<0){b=zero;side=0;}}let k=full.ge(b)+side;if(i===0)k=full.bounds[i][0];if(i===full.v.length-1)k=full.bounds[i][1];if(k<full.bounds[i][0]||k>full.bounds[i][1]||i&&k<out[i-1])throw Error(\"rational lift illegal\");out.push(k);}return out;}\nfunction sparseSolve(full,weights,retainFace=true){\n const indices=[],atoms=[],ws=[];for(let j=0;j<weights.length;j++)if(weights[j]>0){indices.push(j);atoms.push(full.atoms[j]);ws.push(weights[j]);}const m=new Model(atoms),br=m.solve(ws,2e-13,retainFace),labels=lift(m,br.labels,full),maxlabels=lift(m,br.maxlabels,full),row=full.row(labels),rowmax=full.row(maxlabels),value=row.reduce((s,x,j)=>s+x*weights[j],0),vm=rowmax.reduce((s,x,j)=>s+x*weights[j],0);if(Math.abs(value-br.value)>3e-9||Math.abs(vm-br.value)>3e-9)throw Error(\"rational lift score changed\");return{value,row,rowmax,labels,maxlabels,smallModel:m,smallResponse:br,indices,thresholdNodes:m.N,auxiliaryNodes:br.auxiliaryNodes,rewards:br.rewards,dualValue:br.dualValue};\n}\nreturn{Model,pack,restore,lift,sparseSolve};\n\n})(Cut,Physical);";
 const R=Function("Cut","Physical",moduleSource+"\nreturn Rational;")(E.Cut,{Q:Coordinate});
 function canonical(x){const q=G.Q(x);return new G.Germ(q.p,q.q).str();}
 function normalizeAtoms(atoms){return atoms.map(a=>({...a,exact_light:a.exact_light.map(p=>p.map(canonical))}));}
 function auditRoutes(m,complete){
  for(const pair of m.routes)for(const route of pair){
   if(route[0][0].add(route[0][1]).cmp(0)!==0)throw Error("monster must start at time zero");
   let left=false,right=false;
   for(const[u,v]of route){u.g.limit();v.g.limit();const x=u.sub(v);if(x.cmp(-2)===0)left=true;if(x.cmp(2)===0)right=true;}
   if(complete&&(!left||!right))throw Error("append endpoint completion to each monster route");
  }
 }
 function auditGeometry(m){
  for(const row of [m.vQ,m.baseQ])for(let j=0;j<row.length;j++){
   row[j].g.limit();if(j&&row[j-1].cmp(row[j])>=0)throw Error("cached event order");
  }
  if(m.vQ[0].cmp(-1)!==0||m.baseQ[0].cmp(0)!==0)throw Error("cached virtual origin");
  const expected=m.vQ.map(v=>[m.ge(v.cmp(0)<0?0:v),m.ge(v.add(2))]);
  expected[0]=[m.ge(0),m.ge(0)];const last=m.ge(m.vQ.at(-1).add(2));expected[expected.length-1]=[last,last];
  if(JSON.stringify(expected)!==JSON.stringify(m.bounds))throw Error("cached physical bounds");
  let N=0;for(let j=0;j<m.bounds.length;j++){if(m.offset[j]!==N)throw Error("cached offsets");N+=m.bounds[j][1]-m.bounds[j][0];}
  if(N!==m.N)throw Error("cached node count");
  for(const pair of m.routes)for(const route of pair)for(const[u,v]of route){
   if(!m.query.has(v.toString()))throw Error("cached missing query");
   if(u.cmp(0)>=0&&m.ge(u)%3!==1)throw Error("cached missing monster level");
  }
 }
 function recompile(m){
  m.defs=[];m.defMap=new Map();m.units=[];m.germUnits=[];
  for(let j=0;j<m.atoms.length;j++){m.units.push(m.compile(j));m.germUnits.push(m.lastExactUnits.slice());}
  m.exactRewardsAudited=true;return m;
 }
 function Model(atoms,{complete=true,extraQueries=[],extraBases=[]}={}){
  const m=new R.Model(normalizeAtoms(atoms),extraQueries.map(canonical),extraBases.map(canonical));
  auditRoutes(m,complete);auditGeometry(m);m.exactRewardsAudited=true;
  m.geometryRadius=G.stats().radius;m.coordinateField="Q(epsilon), with subordinate label delta";
  return m;
 }
 function restore(shape,atoms,{complete=true,auditRewards=true}={}){
  const cache={v:shape.v.map(canonical),base:shape.base.map(canonical),
   bounds:shape.bounds,offset:shape.offset,N:shape.N,defs:shape.defs,units:shape.units};
  const m=R.restore(cache,normalizeAtoms(atoms));m.defMap=new Map(m.defs.map((d,i)=>[(d.pos?"+":"-")+d.bits.join(","),i]));
  m.germUnits=(shape.germ_units||[]).map(row=>row.map(([id,c])=>[id,new Coordinate(canonical(c))]));
  auditRoutes(m,complete);auditGeometry(m);m.exactRewardsAudited=false;
  if(auditRewards)recompile(m);
  m.geometryRadius=G.stats().radius;m.coordinateField="Q(epsilon), with subordinate label delta";return m;
 }
 function extend(shape,atoms,options={}){
  return Model(atoms,{...options,extraQueries:[...(shape.v||[]),...(options.extraQueries||[])],
   extraBases:[...(shape.base||[]),...(options.extraBases||[])]});
 }
 function lift(small,labels,full,{tail="minimal"}={}){
  for(const v of small.vQ)if(!full.query.has(v.toString()))throw Error("lift requires retained query universe");
  for(const b of small.baseQ)if(full.ge(b)%3!==1)throw Error("lift requires retained level universe");
  const out=R.lift(small,labels,full);
  if(tail==="absorb"){for(let i=0;i<full.vQ.length;i++)if(full.vQ[i].cmp(small.vQ.at(-1))>0)out[i]=full.ge(full.vQ[i].add(2));}
  else if(tail!=="minimal")throw Error("unknown lifted tail");
  return out;
 }
 function sparseSolve(full,weights,{tolerance=2e-13,retainFace=true}={}){
  if(weights.length!==full.atoms.length)throw Error("sparse weight dimensions");
  const indices=[],atoms=[],activeWeights=[];
  for(let j=0;j<weights.length;j++){
   if(!Number.isFinite(weights[j])||weights[j]<0)throw Error("invalid numerical probability");
   if(weights[j]>0){indices.push(j);atoms.push(full.atoms[j]);activeWeights.push(weights[j]);}
  }
  if(!atoms.length)throw Error("empty active law");
  const small=Model(atoms),response=small.solve(activeWeights,tolerance,retainFace);
  const labels=lift(small,response.labels,full),maximum=lift(small,response.maxlabels,full);
  const exact=full.rowExact(labels),exactMaximum=full.rowExact(maximum);
  const row=exact.map(x=>x.number()),rowmax=exactMaximum.map(x=>x.number());
  const value=row.reduce((a,x,j)=>a+x*weights[j],0),other=rowmax.reduce((a,x,j)=>a+x*weights[j],0);
  if(Math.abs(value-response.value)>3e-9||Math.abs(other-response.value)>3e-9)throw Error("sparse germ lift changed response");
  return{scope:"Floating limiting response discovery; integer replay required for certification",
   value,row,rowmax,rowGerms:exact.map(x=>x.toString()),rowmaxGerms:exactMaximum.map(x=>x.toString()),
   labels,maxlabels:maximum,smallModel:small,smallResponse:response,indices,
   thresholdNodes:small.N,auxiliaryNodes:response.auxiliaryNodes,rewards:response.rewards,dualValue:response.dualValue};
 }
 function pack(m){
  return{...R.pack(m),coordinate_field:m.coordinateField,geometry_radius:m.geometryRadius,
   germ_units:m.germUnits.map(row=>row.map(([id,c])=>[id,c.toString()]))};
 }
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const c=a%b;a=b;b=c;}return a;}
 function integerLimitCut(m,weights,{retainGraph=false}={}){
  if(!m.exactRewardsAudited)recompile(m);
  if(weights.length!==m.atoms.length)throw Error("weight dimensions");
  const wg=weights.map(G.Q);let total=G.ZERO;
  for(const w of wg){if(w.cmp(0)<0)throw Error("negative probability");total=total.a(w);}
  if(!total.eq(1))throw Error("probabilities must sum exactly to one");
  const rw=Array(m.defs.length).fill(null);
  for(let j=0;j<wg.length;j++)for(const[id,c]of m.germUnits[j]){
   const z=c.g.m(wg[j]);rw[id]=rw[id]===null?z:rw[id].a(z);
  }
  const zero=G.ZERO.limit(),limits=rw.map(x=>x===null?zero:x.limit());
  let D=1n;for(const x of limits){if(x.cmp(0)<0)throw Error("negative reward limit");D=D/gcd(D,x.d)*x.d;}
  const ints=limits.map(x=>x.n*(D/x.d)),lin=Array(m.N).fill(0n),hard=[];let constant=0n;
  for(let id=0;id<ints.length;id++){
   const w=ints[id];if(!w)continue;const{pos,bits}=m.defs[id];
   if(!bits.length){constant+=w;continue;}
   if(bits.length===1){lin[bits[0]]+=pos?w:-w;if(!pos)constant+=w;}
   else{const a=lin.length;lin.push(pos?w:-w);if(!pos)constant+=w;for(const b of bits)hard.push(pos?[a,b]:[b,a]);}
  }
  const s=lin.length,t=s+1,graph=new E.BigFlow.BigFlow(t+1);
  let inf=1n,ceiling=constant;for(const x of lin)inf+=x<0n?-x:x;
  for(let i=0;i<lin.length;i++)if(lin[i]>0n){graph.add(s,i,lin[i]);ceiling+=lin[i];}else if(lin[i]<0n)graph.add(i,t,-lin[i]);
  for(const[a,b]of hard)graph.add(a,b,inf);
  for(let i=0;i<m.v.length;i++){
   const[lo,hi]=m.bounds[i];for(let k=lo+2;k<=hi;k++)graph.add(m.node(i,k),m.node(i,k-1),inf);
  }
  for(let i=0;i+1<m.v.length;i++){
   const lo=Math.max(m.bounds[i][0],m.bounds[i+1][0]),hi=Math.min(m.bounds[i][1],m.bounds[i+1][1]);
   for(let k=lo+1;k<=hi;k++)graph.add(m.node(i,k),m.node(i+1,k),inf);
  }
  const flow=graph.solve(s,t,inf),labels=[],maximum=[];
  for(let i=0;i<m.v.length;i++){
   const[lo,hi]=m.bounds[i];let a=lo,b=lo;
   for(let k=lo+1;k<=hi;k++){const n=m.node(i,k);if(flow.reach[n])a++;if(!flow.sink[n])b++;}
   labels.push(a);maximum.push(b);
  }
  const value=G.Q((ceiling-flow.flow)+"/"+(4n*D)).limit();
  const row=m.rowExact(labels).map(x=>x.g),maxrow=m.rowExact(maximum).map(x=>x.g);
  const score=row.reduce((a,x,j)=>a.a(x.m(wg[j])),G.ZERO),maxscore=maxrow.reduce((a,x,j)=>a.a(x.m(wg[j])),G.ZERO);
  if(!score.limit().eq(value)||!maxscore.limit().eq(value))throw Error("integer limit cut/capture mismatch");
  const balances=Array(graph.n).fill(0n),positiveFlows=[],flowValues=[],flowMap=new Map(),sourceSide=[];
  let replayCut=0n;
  for(let arc=0;arc<graph.to.length;arc+=2){
   const from=graph.to[arc^1],to=graph.to[arc],capacity=graph.cap[arc]+graph.cap[arc^1],f=graph.cap[arc^1];
   if(f<0n||f>capacity)throw Error("integer capacity replay");
   balances[from]-=f;balances[to]+=f;
   if(flow.reach[from]&&!flow.reach[to])replayCut+=capacity;
   if(f>0n){const key=String(f);let id=flowMap.get(key);if(id===undefined){id=flowValues.length;flowMap.set(key,id);flowValues.push(key);}positiveFlows.push([arc/2,id]);}
  }
  for(let i=0;i<graph.n;i++){
   if(i!==s&&i!==t&&balances[i]!==0n)throw Error("integer conservation replay");
   if(flow.reach[i])sourceSide.push(i);
  }
  if(balances[s]!==-flow.flow||balances[t]!==flow.flow||replayCut!==flow.flow)throw Error("integer cut replay");
  const flowCertificate={flowValues,positiveFlows,sourceSide,source:s,sink:t};
  const errors=[];
  for(let id=0;id<rw.length;id++)if(rw[id]!==null){
   let z=rw[id].s(G.Q(limits[id].str()));if(z.cmp(0)<0)z=z.neg();
   if(!z.limit().eq(0))throw Error("nonvanishing coefficient error");
   if(!z.eq(0))errors.push(z.dby(4).str());
  }
  return{scope:"Exact limiting unrestricted response to this supplied finite germ Monster law",
   value:value.str(),decimal:value.num(),labels,maximum_labels:maximum,
   row:row.map(x=>x.str()),maximum_row:maxrow.map(x=>x.str()),
   witness_score:score.str(),maximum_witness_score:maxscore.str(),
   uniform_error_terms:errors,radius:G.stats().radius,
   zero_leading_rewards:limits.filter((x,i)=>x.eq(0)&&rw[i]!==null&&!rw[i].eq(0)).length,
   graph_nodes:graph.n,graph_arcs:graph.to.length/2,
   flowCertificate,
   flow:{value:String(flow.flow),denominator:String(D),ceiling:String(ceiling),phases:flow.phases,pushes:flow.pushes},
   ...(retainGraph?{graph,result:flow,source:s,sink:t}:{} )};
 }
 return{Model,pack,restore,extend,lift,recompile,sparseSolve,Coordinate,integerLimitCut,audit:{coefficient_sign_gate_changes:1,exact_germ_units_added:true,
  geometry_number_conversions:0,discovery_number_conversions:"reward limits and final row limits only",
  subordinate_scale:"delta is smaller than every positive compared epsilon-germ"}};
}
return{createGermAtomic};
})();