module.exports = (function(){

function createUnitRouteScorer(G){
 const Q=G.Q,Z=G.ZERO;
 function score(prepared,raw,{fullCost=false}={}){
  const {paths,weights,W}=prepared,m=new G.PLPath(raw);let lo=W,hi=0n,events=[],traceTests=0;
  function record(t,nl,nh){const initial=lo>hi,added=initial?nh-nl:lo-nl+nh-hi;if(added<0n)throw Error("negative capture mass");if(added)events.push({time:t,mass:added});lo=nl;hi=nh;}
  function point(t,x){
   let fl=0n,fh=0n;for(let j=0;j<paths.length;j++){const sg=paths[j].at(t).cmp(x);traceTests++;if(sg<0)fl+=weights[j];if(sg<=0)fh+=weights[j];}
   record(t,lo>hi?fl:(fl<lo?fl:lo),lo>hi?fh:(fh>hi?fh:hi));return{fl,fh};
  }
  for(let k=0;k+1<m.t.length;k++){
   const t=m.t[k],x=m.x[k],end=m.t[k+1],d=m.v[k].eq(1)?1:m.v[k].eq(-1)?-1:0;
   if(!d)throw Error("unit route required");const {fl,fh}=point(t,x);let rank=d>0?fh:fl;
   const hits=[];for(let j=0;j<paths.length;j++){
    const sg=paths[j].at(t).cmp(x);traceTests++;if(sg!==d)continue;
    const hit=paths[j].hit(t,x,d);if(hit!==null&&hit.cmp(end)<=0)hits.push({time:hit,mass:weights[j]});
   }
   hits.sort((a,b)=>a.time.cmp(b.time));
   for(let j=0;j<hits.length;){
    const time=hits[j].time;let mass=0n;do{mass+=hits[j++].mass;}while(j<hits.length&&hits[j].time.eq(time));
    rank+=BigInt(d)*mass;
    record(time,d<0&&rank<lo?rank:lo,d>0&&rank>hi?rank:hi);
   }
  }
  point(m.t.at(-1),m.x.at(-1));
  const zeroRat=typeof Z.limit==="function"?Z.limit():Z;
  const limitTime=t=>typeof t.limit==="function"?t.limit():t;
  let limiting=zeroRat;
  for(const z of events)limiting=limiting.a(limitTime(z.time).m(z.mass));
  let cost=null;if(fullCost){cost=Z;for(const z of events)cost=cost.a(z.time.m(z.mass));cost=cost.dby(W);}
  return{complete:lo===0n&&hi===W,lower:lo,upper:hi,limit:limiting.dby(W).str(),cost,
   events:events.map(z=>({time:z.time.str(),mass:String(z.mass)})),traceTests};
 }
 return{score};
}
return {createUnitRouteScorer};

})();
