/** Global selector-type signed-CDF plane compiler.
 * Coordinates and coefficients are ordinary exact rationals. Completed unit
 * Monster routes stand for fair reflection pairs. Output is a signed ordered-
 * label problem, not a raw-capture game or a finite Princess basis.
 */
module.exports=(function(){
function createSelectorPlaneOracle(A,closure){
 const Q=A.Q,Z=Q(0),O=Q(1),min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,abs=a=>a.cmp(0)<0?a.neg():a,
  unique=xs=>[...new Map(xs.map(Q).map(x=>[x.str(),x])).values()].sort((a,b)=>a.cmp(b));
 function ordinary(x){const q=Q(x);q.n;q.d;return q;}
 function prepare(packet){
  if(!packet.planes?.length)throw Error("selector planes required");
  const total=packet.planes.reduce((s,p)=>{const w=ordinary(p.weight??1);if(w.cmp(0)<0)throw Error("negative plane weight");return s.a(w);},Z);
  if(total.eq(0))throw Error("empty selector law");
  const planes=[];let horizon=Z;
  for(const p of packet.planes){
   const weight=ordinary(p.weight??1).dby(total);if(weight.eq(0))continue;
   const route=p.route.map(v=>v.map(ordinary));
   if(!route.length||!route[0][0].eq(0)||!route.some(v=>v[1].eq(-1))||!route.some(v=>v[1].eq(1)))throw Error("completed unit route required");
   for(let j=0;j<route.length;j++){
    if(route[j][0].cmp(0)<0||route[j][1].cmp(-1)<0||route[j][1].cmp(1)>0)throw Error("route domain");
    if(j){const dt=route[j][0].s(route[j-1][0]),dx=route[j][1].s(route[j-1][1]);if(dt.cmp(0)<0||!abs(dx).eq(dt))throw Error("route is not unit");}
   }
   const selectors=new Map();
   for(const s of p.selectors){
    if(!Number.isInteger(s.leg)||s.leg<0||s.leg+1>=route.length)throw Error("selector leg");
    if(!Number.isInteger(s.lower_index)||!Number.isInteger(s.upper_index)||s.lower_index<0||s.upper_index<0||s.lower_index>s.leg||s.upper_index>s.leg)throw Error("selector is not causal");
    const cut=ordinary(s.cut);if(cut.cmp(route[s.leg][0])<0||cut.cmp(route[s.leg+1][0])>0)throw Error("selector cut");
    if(selectors.has(s.leg))throw Error("duplicate selector leg");
    selectors.set(s.leg,{...s,cut});
   }
   for(let j=0;j+1<route.length;j++)if(!route[j][0].eq(route[j+1][0])&&!selectors.has(j))throw Error("missing selector leg");
   horizon=max(horizon,route.at(-1)[0]);planes.push({id:p.id??planes.length,weight,route,selectors});
  }
  return{planes,horizon};
 }
 function compile(packet,{maxGridPoints=5000,maxTableEntries=3000000}={}){
  const prepared=packet.planes?prepare(packet):null,pointMap=new Map(),horizontalMap=new Map(),verticalMap=new Map(),cdfPoints=[],cdfRays=[];
  let sourceConstant=prepared?Z:ordinary(packet.constant??0),constant=sourceConstant,inputH=prepared?.horizon??Z;
  function merge(map,key,term){
   if(term.coefficient.eq(0))return;
   if(map.has(key))map.get(key).coefficient=map.get(key).coefficient.a(term.coefficient);else map.set(key,term);
  }
  function point(t,x,coefficient,mode){
   if(coefficient.eq(0))return;
   if(!["strict","closed"].includes(mode)||t.cmp(0)<0||x.cmp(-1)<0||x.cmp(1)>0)throw Error("CDF point domain");
   inputH=max(inputH,t);cdfPoints.push({time:t.str(),position:x.str(),coefficient:coefficient.str(),trace:mode});
   if((mode==="closed"&&coefficient.cmp(0)>0)||(mode==="strict"&&coefficient.cmp(0)<0))throw Error("non-selector contact sign");
   const sign=x.cmp(0)>=0?1:-1,r=abs(x),v=t.s(r),u=t.a(r);
   if(sign===1)constant=constant.a(coefficient);
   merge(pointMap,v.str()+"|"+u.str(),{v,u,coefficient:coefficient.m(-sign).dby(2)});
  }
  function ray(a,b,d,left,right,coefficient,mode){
   if(left.eq(right)||coefficient.eq(0))return;
   if(!["strict","closed"].includes(mode)||left.cmp(0)<0||right.cmp(left)<0||(d!==1&&d!==-1))throw Error("CDF ray domain");
   const xa=a[1].a(left.s(a[0]).m(d)),xb=a[1].a(right.s(a[0]).m(d));
   if(xa.cmp(-1)<0||xa.cmp(1)>0||xb.cmp(-1)<0||xb.cmp(1)>0)throw Error("CDF ray outside arena");
   inputH=max(inputH,right);cdfRays.push({start_time:left.str(),end_time:right.str(),start_position:xa.str(),direction:d,coefficient:coefficient.str(),trace:mode});
   if((mode==="closed"&&coefficient.cmp(0)>0)||(mode==="strict"&&coefficient.cmp(0)<0))throw Error("non-selector ray sign");
   const pos=t=>a[1].a(t.s(a[0]).m(d)),times=[left,right],zero=a[0].s(a[1].m(d));
   if(zero.cmp(left)>0&&zero.cmp(right)<0)times.push(zero);
   const cuts=unique(times);
   for(let j=0;j+1<cuts.length;j++){
    const l=cuts[j],r=cuts[j+1],sign=pos(l.a(r).dby(2)).cmp(0)>=0?1:-1,
     ul=l.a(abs(pos(l))),ur=r.a(abs(pos(r))),vl=l.s(abs(pos(l))),vr=r.s(abs(pos(r))),c=coefficient.m(-sign).dby(4);
    if(sign===1)constant=constant.a(coefficient.m(r.s(l)));
    if(sign*d===1)merge(horizontalMap,vl.str()+"|"+ul.str()+"|"+ur.str(),{v:vl,left:ul,right:ur,coefficient:c});
    else merge(verticalMap,ul.str()+"|"+vl.str()+"|"+vr.str(),{u:ul,left:vl,right:vr,coefficient:c});
   }
  }
  if(prepared)for(const p of prepared.planes)for(let j=0;j+1<p.route.length;j++){
   const a=p.route[j],b=p.route[j+1],duration=b[0].s(a[0]);if(duration.eq(0))continue;
   const d=b[1].s(a[1]).cmp(0),s=p.selectors.get(j),before=s.cut.s(a[0]),low=p.route[s.lower_index],high=p.route[s.upper_index];
   constant=constant.a(p.weight.m(duration));sourceConstant=sourceConstant.a(p.weight.m(duration));
   if(d===1){point(low[0],low[1],p.weight.m(duration),"strict");point(high[0],high[1],p.weight.m(before).neg(),"closed");ray(a,b,d,s.cut,b[0],p.weight.neg(),"closed");}
   else{point(high[0],high[1],p.weight.m(duration).neg(),"closed");point(low[0],low[1],p.weight.m(before),"strict");ray(a,b,d,s.cut,b[0],p.weight,"strict");}
  }
  if(!prepared){
   for(const p of packet.points??[])point(ordinary(p.time),ordinary(p.position),ordinary(p.coefficient),p.trace);
   for(const r of packet.rays??[]){
    const left=ordinary(r.start_time),right=ordinary(r.end_time),x=ordinary(r.start_position),d=r.direction;
    ray([left,x],[right,x.a(right.s(left).m(d))],d,left,right,ordinary(r.coefficient),r.trace);
   }
  }
  const points=[...pointMap.values()].filter(x=>!x.coefficient.eq(0)),horizontal=[...horizontalMap.values()].filter(x=>!x.coefficient.eq(0)),vertical=[...verticalMap.values()].filter(x=>!x.coefficient.eq(0)),
   V=new Map(),U=new Map(),queue=[],H=inputH,Umax=H.a(2);
  function addV(x){x=Q(x);if(x.cmp(-1)<0||x.cmp(H)>0||V.has(x.str()))return;V.set(x.str(),x);queue.push(["v",x]);}
  function addU(x){x=Q(x);if(x.cmp(0)<0||x.cmp(Umax)>0||U.has(x.str()))return;U.set(x.str(),x);queue.push(["u",x]);}
  addV(-1);addV(0);addV(H);addU(0);
  for(const t of pointMap.values()){addV(t.v);addU(t.u);}
  for(const t of horizontalMap.values()){addV(t.v);addU(t.left);addU(t.right);}
  for(const t of verticalMap.values()){addU(t.u);addV(t.left);addV(t.right);}
  for(let k=0;k<queue.length;k++){
   if(V.size+U.size>maxGridPoints)throw Error("selector shift-closure grid cap exceeded");
   const[type,x]=queue[k];if(type==="v"){addU(max(Z,x));addU(x.a(2));}else{addV(x);addV(x.s(2));}
  }
  const vs=[...V.values()].sort((a,b)=>a.cmp(b)),us=[...U.values()].sort((a,b)=>a.cmp(b)),labels=[],labelMap=new Map();
  function label(u,side){const index=labels.length;labels.push({base:u.str(),side});labelMap.set(u.str()+"|"+side,index);}
  for(const u of us){if(u.eq(0))label(u,0);else label(u,-1);label(u,1);}
  const index=(u,side)=>{const k=labelMap.get(u.str()+"|"+side);if(k===undefined)throw Error("physical bound absent from shift closure");return k;},
   above=(lab,u)=>{const c=Q(lab.base).cmp(u);return c>0||(c===0&&lab.side===1);},
   clamp=(x,l,h)=>max(l,min(h,x)),rowBounds=[],unaryValues=[],rows=[];let entries=0,verticalCellNorm=Z;
  function query(v){
   const bound=v.eq(-1)?[index(Z,0),index(Z,0)]:[index(max(v,Z),1),index(v.a(2),-1)],values=[];
   for(let k=bound[0];k<=bound[1];k++){const lab=labels[k],base=Q(lab.base);let value=Z;
    for(const t of points)if(t.v.eq(v)&&above(lab,t.u))value=value.a(t.coefficient);
    for(const t of horizontal)if(t.v.eq(v))value=value.a(t.coefficient.m(clamp(base,t.left,t.right).s(t.left)));
    values.push(value.str());
   }rowBounds.push(bound);unaryValues.push(values);rows.push({type:"query",v:v.str()});entries+=values.length;
  }
  function fill(l,r){
   const bound=[index(max(l,Z),1),index(r.a(2),-1)],values=[],active=vertical.filter(t=>t.left.cmp(l)<=0&&t.right.cmp(r)>=0);
   for(const t of active)verticalCellNorm=verticalCellNorm.a(abs(t.coefficient));
   for(let k=bound[0];k<=bound[1];k++){let value=Z;for(const t of active)if(above(labels[k],t.u))value=value.a(t.coefficient.m(r.s(l)));values.push(value.str());}
   rowBounds.push(bound);unaryValues.push(values);rows.push({type:"fill",left:l.str(),right:r.str()});entries+=values.length;
  }
  for(let i=0;i<vs.length;i++){query(vs[i]);if(i+1<vs.length)fill(vs[i],vs[i+1]);if(entries>maxTableEntries)throw Error("selector unary table cap exceeded");}
  const serialize=t=>Object.fromEntries(Object.entries(t).map(([k,v])=>[k,v?.str?v.str():v]));
  return{scope:"Finite signed-label representation of the global supremum of this selector-type plane over symmetric legal Princess marginals.",constant:constant.str(),horizon:H.str(),
   labels,rowBounds,unaryValues,rows,grid:{v:vs.map(x=>x.str()),u:us.map(x=>x.str())},
   terms:{points:points.map(serialize),horizontal:horizontal.map(serialize),vertical:vertical.map(serialize)},
   horizontal_norm:horizontal.reduce((s,t)=>s.a(abs(t.coefficient)),Z).str(),vertical_cell_norm:verticalCellNorm.str(),
   source_terms:{constant:sourceConstant.str(),points:cdfPoints,rays:cdfRays},contact_queries:[...pointMap.values()].map(t=>({u:t.u.str(),v:t.v.str()})),
   normalized_planes:prepared?prepared.planes.map(p=>({id:p.id,weight:p.weight.str(),route:p.route.map(v=>v.map(x=>x.str())),selectors:[...p.selectors.values()].map(s=>({...s,cut:s.cut.str()}))})):null,
   statistics:{query_rows:vs.length,fill_rows:vs.length-1,labels:labels.length,unary_entries:entries,point_terms:points.length,horizontal_terms:horizontal.length,vertical_terms:vertical.length}};
 }
 function solve(packet,options={}){
  const compiled=compile(packet,options),answer=closure.maximize({...compiled,mode:options.mode??"exact"});
  if(answer.status!=="optimal")throw Error("physical selector grid unexpectedly infeasible");
  if(answer.arithmetic!=="exact")return{compiled,closure:answer,scope:"Floating selector discovery only",value:Q(compiled.constant).num()+answer.value};
  const value=Q(compiled.constant).a(Q(answer.value));
  return{compiled,closure:answer,value:value.str(),decimal:value.num(),scope:"Exact global SUPREMUM of the supplied selector-type plane; actual approximating paths require realization."};
 }
 function physicalScore(packet,path){
  const prepared=packet.planes?prepare(packet):null,vertices=path.map(v=>v.map(ordinary));
  if(!vertices.length||!vertices[0][0].eq(0))throw Error("physical Princess must start at time0");
  for(let i=0;i<vertices.length;i++){
   const[t,x]=vertices[i];if(t.cmp(0)<0||x.cmp(0)<0||x.cmp(1)>0)throw Error("radial Princess domain");
   if(i){const dt=t.s(vertices[i-1][0]);if(dt.cmp(0)<=0||abs(x.s(vertices[i-1][1])).cmp(dt)>0)throw Error("radial Princess speed");}
  }
  function position(t){
   let l=0,r=vertices.length;while(l<r){const k=(l+r)>>1;if(vertices[k][0].cmp(t)<=0)l=k+1;else r=k;}
   const j=l-1;if(j<0)throw Error("negative Princess time");if(j+1===vertices.length)return vertices[j][1];
   const[a,x]=vertices[j],[b,y]=vertices[j+1];return x.a(y.s(x).m(t.s(a)).dby(b.s(a)));
  }
  function F(t,x,mode){const p=position(t);let value=Z;for(const sign of[1,-1]){const c=p.m(sign).cmp(x);if(c<0||(c===0&&mode==="closed"))value=value.a(Q("1/2"));}return value;}
  function integral(a,d,left,right,mode){
   if(left.eq(right))return Z;const pos=t=>a[1].a(t.s(a[0]).m(d)),base=unique([left,right,...vertices.map(v=>v[0]).filter(t=>t.cmp(left)>0&&t.cmp(right)<0)]),times=[...base];
   for(let j=0;j+1<base.length;j++)for(const sign of[1,-1]){
    const l=base[j],r=base[j+1],dl=pos(l).s(position(l).m(sign)),dr=pos(r).s(position(r).m(sign));
    if(dl.cmp(0)*dr.cmp(0)<0)times.push(l.a(r.s(l).m(dl.neg()).dby(dr.s(dl))));
   }
   const cuts=unique(times);let value=Z;for(let j=0;j+1<cuts.length;j++){const t=cuts[j].a(cuts[j+1]).dby(2);value=value.a(cuts[j+1].s(cuts[j]).m(F(t,pos(t),mode)));}return value;
  }
  let value=prepared?Z:ordinary(packet.constant??0);
  if(!prepared){
   for(const p of packet.points??[])value=value.a(ordinary(p.coefficient).m(F(ordinary(p.time),ordinary(p.position),p.trace)));
   for(const r of packet.rays??[]){
    const left=ordinary(r.start_time),right=ordinary(r.end_time),x=ordinary(r.start_position);
    value=value.a(ordinary(r.coefficient).m(integral([left,x],r.direction,left,right,r.trace)));
   }
  }
  if(prepared)for(const p of prepared.planes)for(let j=0;j+1<p.route.length;j++){
   const a=p.route[j],b=p.route[j+1],duration=b[0].s(a[0]);if(duration.eq(0))continue;
   const s=p.selectors.get(j),d=b[1].s(a[1]).cmp(0),before=s.cut.s(a[0]),lv=p.route[s.lower_index],hv=p.route[s.upper_index];
   let part=duration;
   if(d===1)part=part.a(duration.m(F(lv[0],lv[1],"strict"))).s(before.m(F(hv[0],hv[1],"closed"))).s(integral(a,d,s.cut,b[0],"closed"));
   else part=part.s(duration.m(F(hv[0],hv[1],"closed"))).a(before.m(F(lv[0],lv[1],"strict"))).a(integral(a,d,s.cut,b[0],"strict"));
   value=value.a(p.weight.m(part));
  }
  return value;
 }
 function realize(compiled,chosen,{tolerance="1/100000000",delta:nullDelta=null}={}){
  if(chosen.length!==compiled.rows.length)throw Error("selector label witness dimensions");
  const tol=ordinary(tolerance);if(tol.cmp(0)<=0)throw Error("positive realization tolerance");
  for(let i=0;i<chosen.length;i++)if(!Number.isInteger(chosen[i])||chosen[i]<compiled.rowBounds[i][0]||chosen[i]>compiled.rowBounds[i][1]||(i&&chosen[i]<chosen[i-1]))throw Error("illegal label witness");
  const vs=compiled.grid.v.map(Q),us=compiled.grid.u.map(Q),Hn=Q(compiled.horizontal_norm),Vn=Q(compiled.vertical_cell_norm);let gap=O;
  for(const list of[vs,us])for(let i=0;i+1<list.length;i++)gap=min(gap,list[i+1].s(list[i]));
  const ceiling=min(Q("1/8"),gap.dby(8)),delta=nullDelta===null?min(ceiling,tol.dby(Hn.a(Vn.m(2)).a(1).m(2))):ordinary(nullDelta);
  if(delta.cmp(0)<=0||delta.cmp(Q("1/4"))>=0||delta.cmp(gap.dby(4))>=0)throw Error("realization scale does not fit query grid");
  const eta=delta.m(delta),values=chosen.map(k=>{const l=compiled.labels[k];return Q(l.base).a(delta.m(l.side));}),light=[];
  function put(v,u){
   if(u.cmp(max(v,Z))<0||u.cmp(v.a(2))>0)throw Error("realized light point outside cone");
   const previous=light.at(-1);if(previous&&v.eq(previous[0])){if(!u.eq(previous[1]))throw Error("discontinuous query interpolation");return;}
   if(previous&&(v.cmp(previous[0])<0||u.cmp(previous[1])<0))throw Error("nonmonotone realized P");light.push([v,u]);
  }
  for(let i=0;i+1<vs.length;i++){
   const a=vs[i],b=vs[i+1],left=values[2*i],c=values[2*i+1],right=values[2*i+2],lo=a.a(eta),hi=b.s(eta),
    f=v=>min(v.a(2),max(max(v,Z),c));
   if(lo.cmp(hi)>=0)throw Error("overlapping realization bridges");
   put(a,left);put(lo,f(lo));
   for(const v of unique([Z,c,c.s(2)].filter(v=>v.cmp(lo)>0&&v.cmp(hi)<0)))put(v,f(v));
   put(hi,f(hi));put(b,right);
  }
  const physical=light.map(([v,u])=>[u.a(v).dby(2),u.s(v).dby(2)]),out=[];
  function vertex(t,x){
   out.push([t,x]);while(out.length>=3){const n=out.length,[a,p]=out[n-3],[b,q]=out[n-2],[c,r]=out[n-1];if(q.s(p).m(c.s(b)).eq(r.s(q).m(b.s(a))))out.splice(n-2,1);else break;}
  }
  for(let i=0;i<physical.length;i++){
   const[t,x]=physical[i];if(t.cmp(0)<0)continue;
   if(!out.length&&t.cmp(0)>0){if(!i)throw Error("missing virtual initial segment");const[a,p]=physical[i-1];vertex(Z,p.a(x.s(p).m(a.neg()).dby(t.s(a))));}
   vertex(t,x);
  }
  if(!out.length||!out[0][0].eq(0)||out.at(-1)[0].cmp(Q(compiled.horizon))<0)throw Error("realized physical horizon");
  let contactChecks=0;
  for(const q of compiled.contact_queries){
   const v=Q(q.v),u=Q(q.u);let j=0;while(j+1<light.length&&light[j+1][0].cmp(v)<=0)j++;
   const value=light[j][0].eq(v)?light[j][1]:light[j][1].a(light[j+1][1].s(light[j][1]).m(v.s(light[j][0])).dby(light[j+1][0].s(light[j][0])));
   if(value.eq(u))throw Error("realized path hits a retained adverse point contact");contactChecks++;
  }
  const path=out.map(v=>v.map(x=>x.str())),packet=compiled.source_terms,score=physicalScore(packet,path),error=delta.m(Hn).a(eta.m(Vn).m(2));
  let gridScore=Q(compiled.constant);
  for(let i=0;i<chosen.length;i++)gridScore=gridScore.a(Q(compiled.unaryValues[i][chosen[i]-compiled.rowBounds[i][0]]));
  if(score.cmp(gridScore.s(error))<0)throw Error("selector realization missed its proved error envelope");
  return{scope:"Actual immutable rational radial Princess path realizing the selected label plane up to the explicit objective error; fair reflection is understood.",
   path,light:light.map(v=>v.map(x=>x.str())),delta:delta.str(),bridge_width:eta.str(),error_bound:error.str(),
   label_score:gridScore.str(),physical_score:score.str(),gap:gridScore.s(score).str(),vertices:path.length,point_contact_checks:contactChecks,positive_initial:Q(path[0][1]).cmp(0)>0};
 }

 return{prepare,compile,solve,physicalScore,realize};
}
return{createSelectorPlaneOracle};
})();