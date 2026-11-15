"use strict";
function createHalfCellBridgeTools(A){
 const Q=A.Q,Z=Q(0);
 function earliestLeft(t,x,q,alpha,B){
  t=Q(t);x=Q(x);q=Q(q);alpha=Q(alpha);B=Q(B);
  if(x.cmp(0)>0||alpha.cmp(0)<0||B.cmp(alpha)<=0)throw Error("left-half domain");
  const q0=alpha.mul(t).add(B.mul(x)),C=B.sub(alpha),D=B.add(alpha),p=[[t,x]];
  if(q.eq(q0))return {time:t,x,path:p,boundaryWait:false};
  if(q.cmp(q0)<0){const dt=q0.sub(q).div(C);return {time:t.add(dt),x:x.sub(dt),path:[...p,[t.add(dt),x.sub(dt)]],boundaryWait:false};}
  const unit=t.add(q.sub(q0).div(D)),edge=t.sub(x);
  if(unit.cmp(edge)<=0){return {time:unit,x:x.add(unit.sub(t)),path:[...p,[unit,x.add(unit.sub(t))]],boundaryWait:false};}
  if(alpha.eq(0))throw Error("unreachable positive rank in static left half");
  const end=q.div(alpha);if(end.cmp(edge)<0)throw Error("bad boundary ordering");
  if(edge.cmp(t)>0)p.push([edge,Z]);if(end.cmp(edge)>0)p.push([end,Z]);
  return {time:end,x:Z,path:p,boundaryWait:true};
 }
 function accelerate(raw,alpha,B){
  const p=raw.map(v=>v.map(Q));alpha=Q(alpha);B=Q(B);
  if(!p[0][0].eq(0)||!p[0][1].eq(0))throw Error("interface entry");
  let t=Q(0),x=Q(0),out=[[t,x]],arrivals=[],contacts=[];
  for(let i=1;i<p.length;i++){
   const q=alpha.mul(p[i][0]).add(B.mul(p[i][1])),z=earliestLeft(t,x,q,alpha,B);
   if(z.time.cmp(p[i][0])>0)throw Error("earliest travel delayed target");
   for(const v of z.path.slice(1)){if(v[0].cmp(out[out.length-1][0])<=0)continue;out.push(v);if(v[1].eq(0))contacts.push(v[0]);}
   t=z.time;x=z.x;arrivals.push(t);
  }
  const end=p[p.length-1],qe=alpha.mul(end[0]).add(B.mul(end[1]));
  if(t.cmp(end[0])<0){out.push([end[0],qe.sub(alpha.mul(end[0])).div(B)]);}
  if(!out[out.length-1][1].eq(end[1]))throw Error("exit mismatch");
  return {path:out,arrivals,contacts};
 }
 function rightBridge(T,x){
  T=Q(T);x=Q(x);if(x.cmp(0)<0||x.cmp(T)>0)throw Error("right endpoint");
  const turn=T.add(x).div(2);let p=[[Z,Z]];if(turn.cmp(0)>0)p.push([turn,turn]);if(turn.cmp(T)<0)p.push([T,x]);return p;
 }
 function firstHit(raw,q,alpha,B){
  const p=raw.map(v=>v.map(Q));q=Q(q);alpha=Q(alpha);B=Q(B);
  for(let i=0;i<p.length;i++){
   const q0=alpha.mul(p[i][0]).add(B.mul(p[i][1]));if(q0.eq(q))return p[i][0];if(i+1===p.length)break;
   const q1=alpha.mul(p[i+1][0]).add(B.mul(p[i+1][1]));
   if((q0.cmp(q)<0&&q1.cmp(q)>0)||(q1.cmp(q)<0&&q0.cmp(q)>0))
    return p[i][0].add(p[i+1][0].sub(p[i][0]).mul(q.sub(q0)).div(q1.sub(q0)));
  }
  return null;
 }
 return {Q,earliestLeft,accelerate,rightBridge,firstHit};
}
module.exports={createHalfCellBridgeTools};
