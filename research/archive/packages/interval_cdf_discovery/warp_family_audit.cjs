
function createWarpFamilyAuditor(E) {
 const {Q,ZERO,ONE,minQ,maxQ,uniq}=E;
 function baseCuts(f){return uniq([ZERO,ONE,...f.initialKnots,...f.grid.flat().filter(x=>x.cmp(0)>=0&&x.cmp(1)<=0)]);}
 function m1Cuts(f,positive){
  let knots=baseCuts(f);if(!positive)return knots;
  for(const x of f.grid[0])if(x.cmp(1)>=0&&x.cmp(2)<=0)knots.push(Q(2).s(x));
  for(const tr of f.triangles){const {ps,cf}=tr;
   const lo=minQ(...ps.map(p=>p[0])),hi=maxQ(...ps.map(p=>p[0]));
   if(lo.cmp(1)<0||hi.cmp(2)>0)continue;
   if(f.initialKnots.some(x=>Q(2).s(x).cmp(lo)>0&&Q(2).s(x).cmp(hi)<0))throw Error("M1 geometry split missing");
   const gaps=ps.map(([u,v])=>f.initialValue(Q(2).s(u)).s(cf[0].m(u)).s(cf[1].m(v)).s(cf[2]));
   for(let i=0;i<3;i++){const j=(i+1)%3;if(gaps[i].m(gaps[j]).cmp(0)<0){const u=ps[i][0].s(gaps[i].m(ps[j][0].s(ps[i][0])).dby(gaps[j].s(gaps[i])));knots.push(Q(2).s(u));}}
  }
  return uniq(knots);
 }
 function fixedCuts(f,positive){
  let cuts=baseCuts(f);if(!positive)return cuts;
  const levels=uniq(f.grid[1].filter(v=>v.cmp(-1)>=0&&v.cmp(1)<=0).map(v=>f.radial(ONE,v)));
  for(let i=0;i+1<f.initial.length;i++){const[a,x]=f.initial[i],[b,y]=f.initial[i+1];if(x.eq(y))continue;
   for(const r of levels)if(r.cmp(x)>0&&r.cmp(y)<0)cuts.push(a.a(r.s(x).m(b.s(a)).dby(y.s(x))));
  }
  return uniq(cuts);
 }
 function m1Route(a,positive){const x=positive?a:a.neg();return[[ZERO,x],[ONE.s(x),ONE],[Q(3).s(x),Q(-1)]];}
 function fixedRoute(a,positive){const x=positive?a:a.neg();return[[ZERO,x],[ONE.s(x).dby(2),ONE.a(x).dby(2)],[Q(2),Q(-1)],[Q(4),ONE]];}
 function minimum(f,family,positive,{physical=true}={}){
  const cuts=family==="m1"?m1Cuts(f,positive):fixedCuts(f,positive);
  const fun=family==="m1"?(positive?a=>f.positiveM1(a):a=>f.negativeM1(a)):a=>f.fixedOne(a,positive);
  let best=null,polynomial=0,captures=0,stationary=0;const cellResults=[];
  for(let j=0;j+1<cuts.length;j++){
   const left=cuts[j],right=cuts[j+1],f0=fun(left),fm=fun(left.a(right).dby(2)),f1=fun(right);
   const qa=f1.s(fm.m(2)).a(f0).m(2),qb=f1.s(f0).s(qa);
   for(const t of [Q("1/4"),Q("3/4")]){const actual=fun(left.a(right.s(left).m(t))),pred=f0.a(qb.m(t)).a(qa.m(t.m(t)));if(!actual.eq(pred))throw Error("quadratic mismatch "+family+" "+positive+" "+j);polynomial++;}
   const candidates=[[left,f0],[right,f1]];
   if(qa.cmp(0)>0){const t=qb.neg().dby(qa.m(2));if(t.cmp(0)>0&&t.cmp(1)<0){const a=left.a(right.s(left).m(t)),value=f0.s(qb.m(qb).dby(qa.m(4)));if(!fun(a).eq(value))throw Error("stationary mismatch");candidates.push([a,value]);stationary++;}}
   let cb=null;for(const x of candidates){if(cb===null||x[1].cmp(cb[1])<0)cb=x;if(best===null||x[1].cmp(best[1])<0)best=x;}
   cellResults.push({interval:[left.str(),right.str()],point:cb[0].str(),value:cb[1].str()});
   if(physical){const a=left.m(2).a(right).dby(3),route=family==="m1"?m1Route(a,positive):fixedRoute(a,positive);const v=f.unitRoutePayoff(route);if(!v.eq(fun(a)))throw Error("physical mismatch "+family+" "+positive+" "+j);captures++;}
  }
  const a=best[0],route=family==="m1"?m1Route(a,positive):fixedRoute(a,positive);
  if(!f.unitRoutePayoff(route).eq(best[1]))throw Error("winner physical mismatch");captures++;
  return{family,positive,cells:cuts.length-1,polynomial_checks:polynomial,capture_checks:captures,stationary_points:stationary,point:a.str(),start:(positive?a:a.neg()).str(),minimum:best[1].str(),decimal:best[1].num(),route:route.map(p=>p.map(x=>x.str())),cell_minima:cellResults};
 }
 return{baseCuts,m1Cuts,fixedCuts,m1Route,fixedRoute,minimum};
}
module.exports = {createWarpFamilyAuditor};
