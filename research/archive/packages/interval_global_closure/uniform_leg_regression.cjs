#!/usr/bin/env node
"use strict";
/* Exact regression of the new uniform-leg pieces. No LP or game value is
 * computed. Uses only Node and BigInt rational arithmetic. */
function runUniformLegRegression() {
  const abs = x => x < 0n ? -x : x;
  const gcd = (a,b) => { a=abs(a); b=abs(b); while(b){const c=a%b;a=b;b=c;} return a; };
  const Q = (n,d=1n) => {n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return[n/g,d/g];};
  const add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
  const neg=a=>[-a[0],a[1]], sub=(a,b)=>add(a,neg(b));
  const mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]);
  const cmp=(a,b)=>{const d=a[0]*b[1]-b[0]*a[1];return d<0n?-1:d>0n?1:0;};
  const eq=(a,b)=>cmp(a,b)===0, min=(a,b)=>cmp(a,b)<0?a:b;
  const floor=a=>a[0]>=0n?a[0]/a[1]:-((-a[0]+a[1]-1n)/a[1]);
  const str=a=>a[1]===1n?String(a[0]):String(a[0])+"/"+String(a[1]);
  const Z=Q(0), O=Q(1), H=Q(1,2);
  const assert=(ok,why)=>{if(!ok)throw new Error(why);};
  let seed=74139;
  const next=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;};
  const checks={calendars:0,rounding_pieces:0,credit_samples:0,planning_arcs:0,
    matching_pairs:0,common_alpha_lifts:0,infeasible_pair_samples:0,
    endpoint_exclusions:0,pricing_cases:0,integer_calendars:0};
  const samples=[Z,Q(1,7),Q(1,3),H,Q(5,7),O];
  const saved=[];

  function creditCheck(a,b) {
    const k=a.length;
    let prefix=Z;
    for(let j=0;j<k;j++){
      const A=add(prefix,a[j]), B=add(A,b[j]);
      assert(cmp(B,Q(j+1))>=0,"left-limit causality");
      for(const s of samples){
        const actual=sub(add(A,mul(s,b[j])),add(Q(j),s));
        const affine=add(mul(sub(O,s),sub(A,Q(j))),mul(s,sub(B,Q(j+1))));
        assert(eq(actual,affine),"within-leg affine credit");
        assert(cmp(actual,Z)>=0,"within-leg nonnegative credit");
        assert(cmp(actual,sub(Q(k-j),s))<=0,"remaining-time credit bound");
        checks.credit_samples++;
      }
      prefix=B;
    }
    assert(eq(prefix,Q(k)),"calendar exact active mass");
  }

  function roundingCheck(a,b) {
    creditCheck(a,b);
    const k=a.length,C=[Z];
    let prefix=Z;
    for(let j=0;j<k;j++){prefix=add(prefix,a[j]);C.push(prefix);prefix=add(prefix,b[j]);C.push(prefix);}
    let cuts=[Z,O];
    for(const c of C){const f=sub(c,Q(floor(c)));if(cmp(f,Z)>0)cuts.push(sub(O,f));}
    cuts.sort(cmp);cuts=cuts.filter((q,i)=>i===0||!eq(q,cuts[i-1]));
    const mean=Array.from({length:2*k},()=>Z), pieces=[];
    for(let i=0;i+1<cuts.length;i++){
      const weight=sub(cuts[i+1],cuts[i]), z=mul(add(cuts[i+1],cuts[i]),H);
      const rounded=C.map(c=>floor(add(c,z)));
      const masses=rounded.slice(1).map((c,j)=>c-rounded[j]);
      assert(masses.every(c=>c>=0n),"rounded nonnegative increments");
      const aa=[],bb=[];
      for(let j=0;j<k;j++){aa.push(Q(masses[2*j]));bb.push(Q(masses[2*j+1]));}
      creditCheck(aa,bb);
      for(let j=0;j<2*k;j++)mean[j]=add(mean[j],mul(weight,Q(masses[j])));
      pieces.push({weight,masses});checks.rounding_pieces++;
    }
    for(let j=0;j<k;j++){
      assert(eq(mean[2*j],a[j]),"node marginal preserved");
      assert(eq(mean[2*j+1],b[j]),"uniform-leg marginal preserved");
    }
    checks.calendars++;
    saved.push(pieces[0].masses);
    return pieces;
  }

  roundingCheck([],[]);
  for(let k=1;k<=6;k++){
    roundingCheck(Array.from({length:k},()=>Z),Array.from({length:k},()=>O));
    roundingCheck(Array.from({length:k},(_,j)=>Q(j===0?k:0)),
                  Array.from({length:k},()=>Z));
    for(let trial=0;trial<18;trial++){
      const a=Array.from({length:k},()=>Z),b=Array.from({length:k},()=>Z);
      const den=[2,3,5,7][trial%4];
      for(let row=0;row<k;row++){
        const fraction=Q(next(den+1),den);
        for(const weight of [fraction,sub(O,fraction)]){
          const item=next(2*(row+1)), j=Math.floor(item/2), dest=item%2?b:a;
          dest[j]=add(dest[j],weight);
        }
      }
      roundingCheck(a,b);
    }
  }

  // Explicit terminal-node exclusion: exact total mass plus the last
  // left-limit inequality permits no mass at the active endpoint.
  for(let k=1;k<=6;k++){
    const terminal=Q(1,7), before=sub(Q(k),terminal);
    assert(cmp(before,Q(k))<0,"positive terminal atom must violate causality");
    checks.endpoint_exclusions++;
  }

  function planningPair(ca,cb) {
    const calendars=[ca,cb], ends=calendars.map(c=>c.length/2), N=Math.max(...ends);
    const q=[0n,0n];let phase=0,j=0;
    const rank=()=>4n*BigInt(j)+q[0]+q[1]+BigInt(phase);
    const arc=action=>{const before=rank();action();assert(rank()>before,"strict planning DAG rank");checks.planning_arcs++;};
    for(j=0;j<N;){
      for(let z=0;z<2;z++)if(j<ends[z])
        for(let i=0n;i<calendars[z][2*j];i++)arc(()=>q[z]++);
      const q0=q.slice();
      arc(()=>{phase=1;});
      for(let z=0;z<2;z++)if(j<ends[z])
        for(let i=0n;i<calendars[z][2*j+1];i++)arc(()=>q[z]++);
      for(let z=0;z<2;z++)if(j<ends[z]){
        assert(q[z]>=1n,"move guard");
        assert(q[z]<=BigInt(N-j),"planning queue upper bound");
        for(const s of samples){
          const real=add(Q(q0[z]),mul(s,Q(q[z]-q0[z]-1n)));
          assert(cmp(real,Z)>=0,"planning charge physical causality");
        }
      }
      arc(()=>{
        for(let z=0;z<2;z++)if(j<ends[z]){
          q[z]--;
          if(j+1===ends[z])assert(q[z]===0n,"own-endpoint zero queue");
        }
        j++;phase=0;
      });
    }
    assert(q[0]===0n&&q[1]===0n,"terminal queues");
  }
  for(let i=0;i<saved.length;i++)planningPair(saved[i],saved[(37*i+11)%saved.length]);

  // Exact cell matching. A type stores knot/band indices for U and V.
  // Physical knots are half-integers. Each odd index denotes its open band.
  const map=(index,alpha)=>mul(H,add(Q(Math.floor(index/2)),index%2===0?Z:alpha));
  const event=(type,alpha)=>({u:map(type.u,alpha),v:map(type.v,alpha)});
  const contains=(p,n)=>cmp(n.u,p.v)<=0&&cmp(p.u,n.v)<=0;
  const position=e=>mul(sub(e.u,e.v),H);
  const valid=(i,j)=>i+j>=0&&i+j<=8&&Math.abs(i-j)<=4;
  const types=[];
  for(let i=-2;i<=6;i++)for(let j=-2;j<=6;j++)if(valid(i,j)){
    types.push({u:2*i,v:2*j,node:true});
    if(valid(i+1,j))types.push({u:2*i+1,v:2*j,node:false});
    if(valid(i,j+1))types.push({u:2*i,v:2*j+1,node:false});
  }
  const positive=[],negative=[];
  for(const type of types){
    const x=position(event(type,H));
    for(const alpha of [Q(1,17),Q(1,5),H,Q(4,5),Q(16,17)]){
      const xx=position(event(type,alpha));
      assert(cmp(xx,Q(-1))>=0&&cmp(xx,O)<=0,"physical type stays in arena");
      assert(cmp(xx,Z)===cmp(x,Z),"open cell sign preserved");
      if(!type.node)assert(cmp(xx,Q(-1))>0&&cmp(xx,O)<0,"open leg excludes endpoints");
    }
    if(cmp(x,Z)>0)positive.push(type);
    if(cmp(x,Z)<0){
      if(eq(x,Q(-1))){assert(type.node,"negative endpoint is a knot");checks.endpoint_exclusions++;}
      else negative.push(type);
    }
  }
  for(const p of positive)for(const n of negative){
    const indexed=n.u<=p.v&&p.u<=n.v;
    assert(indexed===contains(event(p,H),event(n,H)),"midpoint/index criterion");
    checks.matching_pairs++;
    if(eq(position(event(p,H)),O)){
      assert(!indexed,"active negative pressure cannot contain arena endpoint source");
      checks.endpoint_exclusions++;
    }
    if(indexed){
      for(const alpha of [Q(1,17),Q(1,5),H,Q(4,5),Q(16,17)]){
        assert(contains(event(p,alpha),event(n,alpha)),"common-alpha coupling");
        checks.common_alpha_lifts++;
      }
    }else{
      for(const a of [Q(1,17),H,Q(16,17)])for(const b of [Q(1,17),H,Q(16,17)]){
        assert(!contains(event(p,a),event(n,b)),"infeasible types gained interior match");
        checks.infeasible_pair_samples++;
      }
    }
  }
  // Contact only at the excluded endpoint of an open band must not create
  // a matching edge. These endpoints are cell endpoints, not arena endpoints.
  const atomP={u:2,v:0,node:true},openN={u:1,v:2,node:false};
  assert(contains(event(atomP,H),event(openN,Z)),"contact boundary control");
  assert(!contains(event(atomP,H),event(openN,H)),"open lower endpoint excluded");
  const openP={u:3,v:0,node:false},atomN={u:0,v:2,node:true};
  assert(contains(event(openP,Z),event(atomN,H)),"second contact boundary control");
  assert(!contains(event(openP,H),event(atomN,H)),"open upper containment excluded");
  checks.endpoint_exclusions+=2;
  // Same-band admissibility requires a shared coordinate, not independence.
  const sameP={u:3,v:0,node:false},sameN={u:0,v:3,node:false};
  assert(contains(event(sameP,Q(3,4)),event(sameN,Q(3,4))),"diagonal same-band coupling");
  assert(!contains(event(sameP,Q(3,4)),event(sameN,Q(1,4))),"independent uniforms can fail");

  function integerCalendars(k) {
    if(k===0)return [[]];
    const result=[],a=Array(2*k).fill(0);
    function visit(i,left){
      if(i===a.length-1){
        a[i]=left;let s=0,ok=true;
        for(let j=0;j<k;j++){s+=a[2*j]+a[2*j+1];if(s<j+1)ok=false;}
        if(ok)result.push(a.slice());
        return;
      }
      for(let v=0;v<=left;v++){a[i]=v;visit(i+1,left-v);}
    }
    visit(0,k);return result;
  }
  const pricingWitnesses=[];
  for(let k=0;k<=5;k++){
    const calendars=integerCalendars(k);checks.integer_calendars+=calendars.length;
    for(let trial=0;trial<16;trial++){
      const prices=Array.from({length:2*k},()=>Q(next(29)-9,[1,2,3,5][trial%4]));
      let best=null;
      for(const calendar of calendars){
        let cost=Z;
        for(let i=0;i<calendar.length;i++)cost=add(cost,mul(Q(calendar[i]),prices[i]));
        if(best===null||cmp(cost,best)<0)best=cost;
      }
      let record=null,formula=Z;
      for(let j=0;j<k;j++){
        record=record===null?min(prices[2*j],prices[2*j+1]):
          min(record,min(prices[2*j],prices[2*j+1]));
        formula=add(formula,record);
      }
      assert(eq(best,formula),"exhaustive integer-calendar pricing");
      checks.pricing_cases++;
    }
  }
  for(let k=1;k<=5;k++){
    const node=Array(k).fill(Q(20)),leg=Array.from({length:k},(_,j)=>Q(k-j));
    const a=Array(k).fill(Z),b=Array(k).fill(O);
    creditCheck(a,b);
    let price=Z;for(const p of leg)price=add(price,p);
    const atomOnly=Q(20*k);
    assert(cmp(price,atomOnly)<0,"current uniform leg is essential");
    pricingWitnesses.push({steps:k,node_prices:node.map(str),leg_prices:leg.map(str),
      initial_credit:"0",uniform_calendar:Array(k).fill(1),price:str(price)});
  }
  return {scope:"Exact regression of uniform-leg calendar rounding, planning credit, type matching and current-leg pricing; no LP or game value evaluated.",
    status:"passed",checks,types:{total:types.length,positive:positive.length,active_negative:negative.length},
    pricing_witnesses:pricingWitnesses};
}
if (require.main === module) console.log(JSON.stringify(runUniformLegRegression(),null,2));
module.exports={runUniformLegRegression};

