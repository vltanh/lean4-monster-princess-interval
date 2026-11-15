
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a;}
class Rat{
 constructor(n,d=1n){if(n instanceof Rat){this.n=n.n;this.d=n.d;return;}if(typeof n==="string"){let p=n.split("/");if(p.length===2){n=BigInt(p[0]);d=BigInt(p[1]);}else {let [s,e]=n.toLowerCase().split("e");let neg=s[0]==="-";if(neg||s[0]==="+")s=s.slice(1);let parts=s.split(".");let f=parts[1]||"";n=BigInt(parts[0]+f)*(neg?-1n:1n);let power=f.length-Number(e||0);if(power>=0)d=10n**BigInt(power);else n*=10n**BigInt(-power);}}else n=BigInt(n);d=BigInt(d);if(d===0n)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}
 a(q){q=Q(q);return new Rat(this.n*q.d+q.n*this.d,this.d*q.d);}
 s(q){q=Q(q);return new Rat(this.n*q.d-q.n*this.d,this.d*q.d);}
 m(q){q=Q(q);return new Rat(this.n*q.n,this.d*q.d);}
 dby(q){q=Q(q);return new Rat(this.n*q.d,this.d*q.n);}
 neg(){return new Rat(-this.n,this.d);}
 cmp(q){q=Q(q);let z=this.n*q.d-q.n*this.d;return z<0n?-1:z>0n?1:0;}
 eq(q){return this.cmp(q)===0;}
 num(){return Number(this.n)/Number(this.d);}
 str(){return String(this.n)+(this.d===1n?"":"/"+this.d);}
}
function Q(x){return x instanceof Rat?x:new Rat(typeof x==="number"?String(x):x);}
const ZERO=Q(0),ONE=Q(1);
function minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}
function maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}
function uniq(xs){let m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}
function bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){let m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}

function absQ(q){q=Q(q);return q.cmp(0)<0?q.neg():q;}
function position(path,t){t=Q(t);let j=bisect(path.map(v=>v[0]),t)-1;if(j<0)throw Error("negative time");if(j+1===path.length)return path[j][1];let[a,x]=path[j],[b,y]=path[j+1];return x.a(y.s(x).m(t.s(a)).dby(b.s(a)));}
function pairCDF(p,x,strict){let count=0;for(let y of[p,p.neg()])if(y.cmp(x)<0||(!strict&&y.eq(x)))count++;return Q(count).dby(2);}
function rayData(path,start,end,x,d){
 const pos=t=>x.a(t.s(start).m(d)),base=uniq([start,end,...path.map(v=>v[0]).filter(t=>t.cmp(start)>0&&t.cmp(end)<0)]),cuts=[...base];
 for(let i=0;i<base.length-1;i++)for(let sign of[1,-1]){let a=base[i],b=base[i+1],fa=pos(a).s(position(path,a).m(sign)),fb=pos(b).s(position(path,b).m(sign));if(fa.cmp(0)*fb.cmp(0)<0)cuts.push(a.s(fa.m(b.s(a)).dby(fb.s(fa))));}
 return{pos,cuts:uniq(cuts)};
}
function rayIntegral(path,start,end,x,d,strict){
 let{pos,cuts}=rayData(path,start,end,x,d),value=ZERO;
 for(let j=0;j<cuts.length-1;j++){let t=cuts[j].a(cuts[j+1]).dby(2);value=value.a(cuts[j+1].s(cuts[j]).m(pairCDF(position(path,t),pos(t),strict)));}
 return{value,pieces:cuts.length-1};
}
function scoreFlat(packet,path){
 path=path.map(v=>v.map(Q));let value=Q(packet.constant||0),points=0,pieces=0;
 for(let p of packet.points||[]){value=value.a(Q(p.coefficient).m(pairCDF(position(path,Q(p.time)),Q(p.position),p.trace==="strict")));points++;}
 for(let r of packet.rays||[]){let f=rayIntegral(path,Q(r.start_time),Q(r.end_time),Q(r.start_position),r.direction,r.trace==="strict");value=value.a(Q(r.coefficient).m(f.value));pieces+=f.pieces;}
 return{value,points,pieces};
}
function scoreOriginal(packet,path){
 path=path.map(v=>v.map(Q));let total=packet.planes.reduce((s,p)=>s.a(Q(p.weight??1)),ZERO),value=ZERO;
 for(let p of packet.planes){let route=p.route.map(v=>v.map(Q)),v=ZERO;
  for(let j=0;j<route.length-1;j++){
   let[a,x]=route[j],[b,y]=route[j+1],s=p.selectors.find(s=>s.leg===j),d=y.s(x).cmp(0),dt=b.s(a),before=Q(s.cut).s(a),low=route[s.lower_index],high=route[s.upper_index];
   let fl=pairCDF(position(path,low[0]),low[1],true),fh=pairCDF(position(path,high[0]),high[1],false),cut=Q(s.cut),cx=x.a(cut.s(a).m(d)),integ=rayIntegral(path,cut,b,cx,d,d===-1).value;
   let leg=d===1?dt.m(ONE.a(fl)).s(before.m(fh)).s(integ):dt.m(ONE.s(fh)).a(before.m(fl)).a(integ);v=v.a(leg);
  }value=value.a(Q(p.weight??1).m(v).dby(total));
 }return value;
}
function firstCapture(route,path,sign){
 const knots=uniq([...route.map(z=>z[0]),...path.map(z=>z[0]).filter(t=>t.cmp(route.at(-1)[0])<=0)]);
 for(let i=0;i<knots.length;i++){
  let a=knots[i],fa=position(route,a).s(position(path,a).m(sign));if(fa.eq(0))return a;
  if(i+1<knots.length){let b=knots[i+1],fb=position(route,b).s(position(path,b).m(sign));if(fa.cmp(0)*fb.cmp(0)<0)return a.s(fa.m(b.s(a)).dby(fb.s(fa)));}
 }throw Error("completed route did not capture pair");
}
function actualRouteCost(packet,path){
 path=path.map(v=>v.map(Q));let total=packet.planes.reduce((s,p)=>s.a(Q(p.weight??1)),ZERO),value=ZERO;
 for(let p of packet.planes){let r=p.route.map(v=>v.map(Q)),c=firstCapture(r,path,1).a(firstCapture(r,path,-1)).dby(2);value=value.a(c.m(Q(p.weight??1)).dby(total));}return value;
}
function tightSelectors(route,path){
 route=route.map(v=>v.map(Q));path=path.map(v=>v.map(Q));let selectors=[];
 for(let j=0;j<route.length-1;j++){
  let low=0,high=0,fl=null,fh=null;
  for(let i=0;i<=j;i++){
   let l=pairCDF(position(path,route[i][0]),route[i][1],true),h=pairCDF(position(path,route[i][0]),route[i][1],false);
   if(fl===null||l.cmp(fl)<0){fl=l;low=i;}if(fh===null||h.cmp(fh)>0){fh=h;high=i;}
  }
  let[a,x]=route[j],[b,y]=route[j+1],d=y.s(x).cmp(0),{pos,cuts}=rayData(path,a,b,x,d),cut=b;
  for(let i=0;i<cuts.length;i++){
   let t=cuts[i],z=pairCDF(position(path,t),pos(t),d===-1),productive=d===1?z.cmp(fh)>0:z.cmp(fl)<0;
   if(productive){cut=t;break;}
   if(i+1<cuts.length){let mid=t.a(cuts[i+1]).dby(2),v=pairCDF(position(path,mid),pos(mid),d===-1);if(d===1?v.cmp(fh)>0:v.cmp(fl)<0){cut=t;break;}}
  }
  selectors.push({leg:j,lower_index:low,upper_index:high,cut:cut.str()});
 }return selectors;
}
function independentDP(input){
 let previous=null,parents=[];
 for(let i=0;i<input.rowBounds.length;i++){
  let[lo,hi]=input.rowBounds[i],cur=Array(input.labels.length).fill(null),back=Array(input.labels.length).fill(-1),best=null,bk=-1;
  for(let k=0;k<input.labels.length;k++){
   if(previous&&previous[k]!==null&&(best===null||previous[k].cmp(best)>0)){best=previous[k];bk=k;}
   if(k<lo||k>hi)continue;let row=input.unaryValues[i],u=Q(row[row.length===input.labels.length?k:k-lo]);
   if(!previous){cur[k]=u;back[k]=-1;}else if(best!==null){cur[k]=best.a(u);back[k]=bk;}
  }parents.push(back);previous=cur;
 }
 let value=null,k0=-1;for(let k=0;k<previous.length;k++)if(previous[k]!==null&&(value===null||previous[k].cmp(value)>0)){value=previous[k];k0=k;}
 if(value===null)return{status:"infeasible"};let chosen=Array(parents.length);
 for(let i=parents.length-1;i>=0;i--){chosen[i]=k0;k0=parents[i][k0];}
 return{status:"optimal",arithmetic:"exact",value:value.str(),minimum_labels:chosen};
}
function verify(compilerSource){
 const factory=Function("module",compilerSource+";return module.exports;")({exports:{}}),G=factory.createSelectorPlaneOracle({Q},{maximize:independentDP});
 const routes=[
 [[0,0],[1,1],[3,-1]],
 [[0,"1/4"],["1/4","1/2"],["7/4",-1],["15/4",1]],
 [[0,"-1/2"],["1/4","-1/4"],[1,-1],[3,1]],
 [[0,"3/4"],["1/2","1/4"],["5/4",1],["13/4",-1]],
 [[0,"1/8"],["1/4","3/8"],["3/4","-1/8"],["3/2","5/8"],["25/8",-1],["41/8",1]]
 ];
 let games=[],physicalPieces=0,pointChecks=0,tight=0;
 for(let n=0;n<8;n++){
  const packet={planes:[routes[n%5],routes[(n+2)%5]].map((route,j)=>({id:"p"+j,weight:j?"2/5":"1/3",route,selectors:route.slice(0,-1).map((a,k)=>{
   let b=route[k+1],f=Q(["0","1/3","1/2","1"][n%4]);return{leg:k,lower_index:Math.floor(k/2),upper_index:k,cut:Q(a[0]).a(Q(b[0]).s(a[0]).m(f)).str()};
  })}))};
  const sol=G.solve(packet),r=G.realize(sol.compiled,sol.closure.minimum_labels,{tolerance:"1/100000"}),s=scoreFlat(sol.compiled.source_terms,r.path),orig=scoreOriginal(packet,r.path),actual=actualRouteCost(packet,r.path);
  if(!s.value.eq(r.physical_score)||!orig.eq(s.value))throw Error("literal selector-plane compilation mismatch");
  if(actual.cmp(orig)>0)throw Error("selector plane below physical capture");
  if(s.value.cmp(Q(sol.value).s(Q(r.error_bound)))<0||s.value.cmp(Q(sol.value))>0)throw Error("supremum error envelope");
  pointChecks+=s.points;physicalPieces+=s.pieces;
  for(const route of routes){
   const tp={planes:[{weight:1,route,selectors:tightSelectors(route,r.path)}]},tc=G.compile(tp),p=scoreFlat(tc.source_terms,r.path).value,c=actualRouteCost(tp,r.path);
   if(!p.eq(c)||!scoreOriginal(tp,r.path).eq(c))throw Error("tight history selector does not equal first capture");tight++;
  }
  games.push({id:n,value:sol.value,physical:r.physical_score,gap:r.gap,vertices:r.vertices,unary_entries:sol.compiled.statistics.unary_entries});
 }
 const cancel={constant:0,points:[],rays:[]};
 for(let[time,position]of[["0","0"],["1/2","0"],["1/2","1"],["1/2","-1"],["1/2","1/2"]])for(let trace of["strict","closed"])cancel.points.push({time,position,coefficient:trace==="strict"?"1":"-1",trace});
 for(let[start_time,end_time,start_position,direction]of[["0","1","1/2",-1],["1/4","7/4","-3/4",1]])for(let trace of["strict","closed"])cancel.rays.push({start_time,end_time,start_position,direction,coefficient:trace==="strict"?"1":"-1",trace});
 const sol=G.solve(cancel),r=G.realize(sol.compiled,sol.closure.minimum_labels,{tolerance:"1/10000"}),s=scoreFlat(sol.compiled.source_terms,r.path);
 if(!Q(sol.value).eq(0)||!s.value.eq(0)||!Q(r.error_bound).eq(0))throw Error("cancelled contact geometry not preserved");
 return{scope:"Independent ordinary rational end-to-end selector-plane audit. Ordered labels are optimized by a separate prefix-max DP; physical first captures and signed-CDF integrals are independent of compiler scoring.",
 selector_games:games,source_point_checks:pointChecks,physical_ray_pieces:physicalPieces,tight_selector_first_capture_identities:tight,
 cancellation:{value:sol.value,physical:r.physical_score,error_bound:r.error_bound,retained_point_queries:r.point_contact_checks}};
}
const api={verify,maximizeOrdinaryOrderedLabels:independentDP};if(typeof module==="object"&&module.exports)module.exports=api;
if(typeof require==="function"&&typeof module==="object"&&require.main===module){
 const fs=require("fs"),path=require("path"),source=fs.readFileSync(path.join(__dirname,"../interval_global_closure/selector_plane_oracle.cjs"),"utf8");
 console.log(JSON.stringify(verify(source),null,2));
}
return api;
