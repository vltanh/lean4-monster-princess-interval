#!/usr/bin/env node
"use strict";
/* Exact regression of common left-floor clock atomization on unit grid legs. */
function run() {
  const abs=x=>x<0n?-x:x;
  const gcd=(a,b)=>{a=abs(a);b=abs(b);while(b){const c=a%b;a=b;b=c;}return a;};
  const Q=(n,d=1n)=>{n=BigInt(n);d=BigInt(d);if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return[n/g,d/g];};
  const add=(a,b)=>Q(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),neg=a=>[-a[0],a[1]],sub=(a,b)=>add(a,neg(b));
  const mul=(a,b)=>Q(a[0]*b[0],a[1]*b[1]),cmp=(a,b)=>{const c=a[0]*b[1]-b[0]*a[1];return c<0n?-1:c>0n?1:0;};
  const eq=(a,b)=>cmp(a,b)===0,floor=a=>a[0]>=0n?a[0]/a[1]:-((-a[0]+a[1]-1n)/a[1]);
  const Z=Q(0),O=Q(1),H=Q(1,2),h=H,dt=Q(1,4);
  const assert=(ok,why)=>{if(!ok)throw new Error(why);};
  const T=z=>mul(h,Q(floor(mul(Q(2),z))));
  const xy=(u,v)=>({t:mul(add(u,v),H),x:mul(sub(u,v),H),u,v});
  const original=(t,x)=>xy(add(t,x),sub(t,x));
  const mapped=p=>xy(T(p.u),T(p.v));
  const contains=(p,n)=>cmp(n.u,p.v)<=0&&cmp(p.u,n.v)<=0;
  const checks={selected_events:0,earlier_vertex:0,scoring_causality:0,reflections:0,
    own_endpoint_exclusions:0,type_pairs:0,matched_event_pairs:0,
    target_center_forces_source_center:0,deficiency_tests:0};
  let seed=82017;
  const next=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;};
  const alphas=[Q(1,5),H,Q(4,5)];
  const paths=[];
  for(let trial=0;trial<60;trial++){
    let k=[-2,0,2,4][trial%4], path=[k];
    for(let j=0;j<12&&k!==-4;j++){
      const d=k===4?-1:next(2)?1:-1;k+=d;path.push(k);
    }
    while(k>-4){k--;path.push(k);}
    paths.push(path);
  }
  for(const path of paths){
    const K=path.length-1;
    for(let j=0;j<K;j++){
      for(const alpha of [Z,...alphas]){
        const t=mul(dt,add(Q(j),alpha));
        const x=mul(dt,add(Q(path[j]),mul(alpha,Q(path[j+1]-path[j]))));
        const p=original(t,x),p2=mapped(p);
        const left=original(mul(dt,Q(j)),mul(dt,Q(path[j])));
        assert(eq(p2.t,left.t)&&eq(p2.x,left.x),"selected event maps to same leg's left vertex");
        assert(cmp(p2.t,p.t)<=0,"selected time moves earlier");
        assert(!eq(p2.x,Q(-1)),"active clock cannot acquire own endpoint atom");
        assert(cmp(p2.x,Z)===cmp(p.x,Z)||eq(p2.x,Z),"sign can only collapse to center");
        checks.selected_events++;checks.earlier_vertex++;checks.own_endpoint_exclusions++;
        const reflected=mapped(original(t,neg(x)));
        assert(eq(reflected.t,p2.t)&&eq(reflected.x,neg(p2.x)),"same floor respects reflection by coordinate swap");
        checks.reflections++;
        for(let row=j;row<K;row++)for(const beta of alphas){
          const score=mul(dt,add(Q(row),beta));
          if(cmp(t,score)<=0){
            assert(cmp(p2.t,score)<=0,"unchanged scoring time remains causal");
            checks.scoring_causality++;
          }
        }
      }
    }
  }
  const coordinate=(index,alpha)=>mul(h,add(Q(Math.floor(index/2)),index%2===0?Z:alpha));
  const event=(type,alpha)=>xy(coordinate(type.u,alpha),coordinate(type.v,alpha));
  const valid=(i,j)=>i+j>=0&&i+j<=16&&Math.abs(i-j)<=4;
  const types=[];
  for(let i=-2;i<=10;i++)for(let j=-2;j<=10;j++)if(valid(i,j)){
    types.push({u:2*i,v:2*j,node:true});
    if(valid(i+1,j))types.push({u:2*i+1,v:2*j,node:false});
    if(valid(i,j+1))types.push({u:2*i,v:2*j+1,node:false});
  }
  const positive=[],negative=[];
  for(const type of types){
    const left=event(type,Z),middle=event(type,H);
    // Nodes at the own endpoint and legs DEPARTING it cannot be scored by
    // this active clock. Incoming legs ending there remain admissible.
    if(eq(left.x,Q(-1))){checks.own_endpoint_exclusions++;continue;}
    if(cmp(middle.x,Z)>0)positive.push(type);
    if(cmp(middle.x,Z)<0)negative.push(type);
  }
  let sourceMass=Array(positive.length).fill(0n),targetMass=Array(negative.length).fill(0n);
  const matching=[];
  for(let i=0;i<positive.length;i++)for(let j=0;j<negative.length;j++){
    const p=positive[i],n=negative[j];
    checks.type_pairs++;
    for(const a of alphas)for(const b of alphas){
      const pe=event(p,a),ne=event(n,b);
      if(!contains(pe,ne))continue;
      const pp=mapped(pe),nn=mapped(ne);
      assert(contains(pp,nn),"common left floor preserves matching containment");
      assert(cmp(pp.x,Z)>=0&&cmp(nn.x,Z)<=0,"matching signs never reverse");
      if(eq(nn.x,Z)){
        assert(eq(pp.x,Z),"collapsed negative target forces collapsed positive source");
        checks.target_center_forces_source_center++;
      }
      checks.matched_event_pairs++;
    }
    // One common alpha realizes every indexed feasible matching type pair.
    if(contains(event(p,H),event(n,H))){
      const mass=BigInt(1+(i+3*j)%5);
      sourceMass[i]+=mass;targetMass[j]+=mass;matching.push([i,j,mass]);
    }
  }
  for(let trial=0;trial<12;trial++){
    const p=sourceMass.map((mass,i)=>mass+BigInt(1+(trial+2*i)%7));
    let oldPositive=p.reduce((a,b)=>a+b,0n),oldMatching=0n,newMatching=0n,newPositive=0n;
    for(let i=0;i<p.length;i++)if(cmp(mapped(event(positive[i],H)).x,Z)>0)newPositive+=p[i];
    for(const [i,j,mass] of matching){
      oldMatching+=mass;
      const pp=mapped(event(positive[i],H)),nn=mapped(event(negative[j],H));
      if(cmp(pp.x,Z)>0){
        assert(cmp(nn.x,Z)<0,"surviving matched source retains negative capacity");
        newMatching+=mass;
      }
    }
    const lostPositive=oldPositive-newPositive,discarded=oldMatching-newMatching;
    assert(discarded<=lostPositive,"lost match mass is bounded by lost positive pressure");
    assert(newPositive-newMatching<=oldPositive-oldMatching,"deficiency does not increase");
    checks.deficiency_tests++;
  }
  return {scope:"Exact finite regression of left-floor atomization; no LP/game value computed.",
    status:"passed",checks,physical_paths:paths.length,
    selected_type_counts:{positive:positive.length,active_negative:negative.length},
    conclusion_tested:"Earlier selection on the same physical path, unchanged scoring causality, no new own-endpoint atoms, preserved matching, and nonincreasing deficiency."};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={run};

