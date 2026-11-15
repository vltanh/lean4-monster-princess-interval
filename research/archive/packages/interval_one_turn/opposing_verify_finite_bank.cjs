'use strict';
// Rebuild the physical geometry and all reward rows. No saved LP matrix,
// floating solution, numerical optimizer, or precomputed reward units is read.
const fs=require('node:fs'),zlib=require('node:zlib'),path=require('node:path');
const input=process.argv[2]||path.join(__dirname,'opposing_complete8_witness.json.gz');
const engine=process.argv[3]||path.join(__dirname,'..','interval_turn_density');
const E=require(path.join(engine,'atomic_survival_v8.cjs')),P=require(path.join(engine,'projected_cut.cjs'));
const bytes=fs.readFileSync(input),w=JSON.parse((input.endsWith('.gz')?zlib.gunzipSync(bytes):bytes).toString('utf8'));
const {Q}=E.Physical,zero=new Q(0n),one=new Q(1n),two=new Q(2n),D=BigInt(w.threshold_denominator);
function assert(c,s){if(!c)throw Error(s);}
function gcd(a,b){while(b){const t=a%b;a=b;b=t;}return a;}
function rational(n,d){const g=gcd(n,d);return String(n/g)+'/'+String(d/g);}
function pairKey(route){const p=route.map(v=>v.map(x=>new Q(x).toString()));return [JSON.stringify(p),JSON.stringify(p.map(([u,v])=>[v,u]))].sort()[0];}
let latest=zero,lateCenter=0,interior=0,legs=0;const seenPairs=new Set();
for(const raw of w.atoms){
 const route=raw.map(v=>v.map(x=>new Q(x))),pair=pairKey(raw);assert(!seenPairs.has(pair),'duplicate reflected pair');seenPairs.add(pair);
 assert(route.length>=2,'short route');assert(route[0][0].add(route[0][1]).cmp(zero)===0,'nonzero starting time');
 const hit=new Set();let priorDirection=null,turns=0,center=null;
 for(let i=0;i<route.length;i++){
  const[u,v]=route[i],t=u.add(v).div(two),x=u.sub(v).div(two);
  assert(t.cmp(zero)>=0&&x.abs().cmp(one)<=0,'outside physical spacetime');
  if(i){
   const[a,b]=route[i-1],du=u.sub(a),dv=v.sub(b);
   assert((du.cmp(zero)>0&&dv.n===0n)||(dv.cmp(zero)>0&&du.n===0n),'non-unit-speed leg');
   const direction=du.cmp(zero)>0?1:-1;
   if(priorDirection!==null&&direction!==priorDirection){
    const previousX=a.sub(b).div(two);
    if(previousX.abs().cmp(one)<0){assert(hit.size===0,'interior reversal after first endpoint');turns++;}
   }
   priorDirection=direction;legs++;
   const oldX=a.sub(b).div(two);
   if(center===null&&oldX.cmp(zero)*x.cmp(zero)<=0)center=a.add(b).div(two).add(oldX.abs());
  }
  if(x.abs().cmp(one)===0)hit.add(x.toString());
 }
 assert(turns<=1,'more than one pre-endpoint interior turn');interior+=turns;
 assert(hit.has('-1')&&hit.has('1'),'route does not complete both endpoints');
 assert(route.at(-1)[0].sub(route.at(-1)[1]).abs().cmp(two)===0,'final point is not an endpoint');
 const last=route.at(-1)[0].add(route.at(-1)[1]).div(two);if(last.cmp(latest)>0)latest=last;
 assert(center!==null,'missing center crossing');if(center.cmp(two)>0)lateCenter++;
}
assert(w.atoms.length===w.expected.atoms,'atom count');
// Check complete n8 coverage by independently constructing canonical P(a,b),
// reducing zero/collinear legs and stopping when both endpoints have appeared.
function clean(raw){
 const p=[];for(const row of raw){const v=row.map(x=>new Q(x));if(p.length&&v[0].cmp(p.at(-1)[0])===0&&v[1].cmp(p.at(-1)[1])===0)continue;
  while(p.length>1&&((p.at(-2)[0].cmp(p.at(-1)[0])===0&&v[0].cmp(p.at(-1)[0])===0)||(p.at(-2)[1].cmp(p.at(-1)[1])===0&&v[1].cmp(p.at(-1)[1])===0)))p.pop();p.push(v);}
 const out=[],hit=new Set();for(const v of p){out.push(v.map(String));const x=v[0].sub(v[1]).div(two);if(x.abs().cmp(one)===0)hit.add(x.toString());if(hit.size===2)break;}return out;
}
const grid=new Set(),n=w.triangle.a_b_denominator;
for(let ai=-n;ai<=n;ai++)for(let bi=ai;bi<=2*n-ai;bi++){
 const a=new Q(BigInt(ai),BigInt(n)),b=new Q(BigInt(bi),BigInt(n));
 const route=Math.abs(ai)===n?[['-1','1'],['3','1']]:clean([[a,a.neg()],[b,a.neg()],[b,b.add(two)],[b.add(new Q(4n)),b.add(two)]]);
 const key=pairKey(route);grid.add(key);assert(seenPairs.has(key),'missing complete-grid route');
}
assert(grid.size===w.triangle.unique_reflected_pairs,'complete-grid count');assert(lateCenter===w.triangle.late_center_pairs,'late-center count');
const atoms=w.atoms.map(exact_light=>({exact_light})),model=new E.Rational.Model(atoms),p=P.project(model);
assert(model.N===w.expected.original_thresholds&&p.N===w.expected.projected_thresholds,'reconstructed threshold counts');
assert(p.defs.length===w.expected.rewards&&p.threshold_hard.length===w.expected.hard_order_edges,'reconstructed reward/order counts');
const x=w.threshold_numerators.map(z=>{assert(Number.isSafeInteger(z),'noninteger threshold numerator');return BigInt(z);});
assert(x.length===p.N&&x.every(z=>z>=0n&&z<=D),'threshold probability bounds');
for(const[u,v]of p.threshold_hard)assert(x[u]<=x[v],'hard order violation');
// Independently complete the projected marginals on every original threshold.
// This checks the nested-label coupling directly, beyond the saved edge count.
const active=new Array(model.L+1).fill(0n);let previous=null,completed=0;
for(let i=0;i<model.v.length;i++){
 for(const[k,id]of p.projection.row_thresholds[i])if(active[k]<x[id])active[k]=x[id];
 const row=new Array(model.L+1),[lo,hi]=model.bounds[i];let value=0n;
 for(let k=model.L;k>=0;k--){if(active[k]>value)value=active[k];row[k]=k<=lo?D:k>hi?0n:value;if(previous)assert(row[k]>=previous[k],'full inverse-CDF row order');completed++;}
 for(const[k,id]of p.projection.row_thresholds[i])assert(row[k]===x[id],'completion changes a priced marginal');
 for(let k=1;k<row.length;k++)assert(row[k]<=row[k-1],'within-row threshold order');previous=row;
}
let scale=1n;for(const q of model.vQ.concat(model.baseQ))scale=scale/gcd(scale,q.d)*q.d;
assert(String(scale)===w.expected.geometry_scale,'reconstructed rational geometry scale');
const reward=p.defs.map(d=>{if(!d.bits.length)return D;let z=d.pos?D:0n;for(const bit of d.bits)z=d.pos?(x[bit]<z?x[bit]:z):(x[bit]>z?x[bit]:z);return d.pos?z:D-z;});
let minimum=null,minimumIndex=-1,unitCount=0;
for(let i=0;i<atoms.length;i++){
 model.compile(i);let total=0n;
 for(const[id,c]of model.lastExactUnits){assert(c.n>=0n&&scale%c.d===0n,'nonintegral exact reward unit');total+=c.n*(scale/c.d)*reward[id];unitCount++;}
 if(minimum===null||total<minimum){minimum=total;minimumIndex=i;}
}
assert(model.defs.length===p.defs.length,'recompilation changes reward definitions');
const denominator=4n*scale*D,exactMinimum=rational(minimum,denominator);
assert(exactMinimum===w.expected.exact_minimum,'exact row minimum mismatch');
const [targetN,targetD]=w.expected.target.split('/').map(BigInt),marginN=minimum*targetD-targetN*denominator,marginD=denominator*targetD;
assert(marginN>0n,'does not strictly exclude target');
console.log(JSON.stringify({scope:'Finite specified Monster bank only; exact geometric/order/payoff replay. The physical interpretation uses the finite-event inverse-curve response theorem.',atoms:atoms.length,complete_triangle_pairs:grid.size,late_center_pairs:lateCenter,unit_speed_legs:legs,pre_endpoint_interior_turns:interior,completion_horizon:latest.toString(),projected_thresholds:p.N,original_thresholds:model.N,completed_cdf_entries:completed,hard_order_edges:p.threshold_hard.length,rewards:p.defs.length,exact_units_rebuilt:unitCount,quantile_components:new Set(['0',String(D),...x.map(String)]).size-1,exact_minimum:exactMinimum,minimum:Number(minimum)/Number(denominator),minimum_index:minimumIndex,target:w.expected.target,exact_margin:rational(marginN,marginD),strictly_above_target:true}));
