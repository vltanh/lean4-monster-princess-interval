"use strict";
// Construct a rational P1 Princess law from a verified finite clock-grid dual.
// The guarantee is justified by CONSTRUCTIVE_PRINCESS_GRID_DUAL.md.
// A saved strategy's claimed guarantee is checked by verifyExtraction against
// the original complete primal/dual certificate, not trusted as input.
const {priceRecordDual}=require("./record_pricing.cjs");
const {gcd}=require("./exact_certificate.cjs");

class Q {
 constructor(a,b=1n){
  a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero denominator");
  if(b<0n){a=-a;b=-b;}const d=gcd(a,b);this.a=a/d;this.b=b/d;
 }
 static of(x){if(x instanceof Q)return x;const p=String(x).split("/");if(p.length>2)throw Error("bad fraction");return new Q(p[0],p[1]||1);}
 add(x){x=Q.of(x);return new Q(this.a*x.b+x.a*this.b,this.b*x.b);}
 sub(x){x=Q.of(x);return new Q(this.a*x.b-x.a*this.b,this.b*x.b);}
 mul(x){x=Q.of(x);return new Q(this.a*x.a,this.b*x.b);}
 div(x){x=Q.of(x);return new Q(this.a*x.b,this.b*x.a);}
 cmp(x){x=Q.of(x);const a=this.a*x.b-x.a*this.b;return a<0n?-1:a>0n?1:0;}
 floor(){let q=this.a/this.b;if(this.a<0n&&this.a%this.b)q--;return q;}
 toString(){return String(this.a)+(this.b===1n?"":"/"+this.b);}
 toJSON(){return this.toString();}
}
const minQ=(a,b)=>Q.of(a).cmp(b)<=0?Q.of(a):Q.of(b);
const ZERO=new Q(0n),ONE=new Q(1n),HALF=new Q(1n,2n);
function buildProfile(certificate){
 const n=certificate.n,N=16*n,R=2*n,D=BigInt(certificate.discount_denominator);
 if(!Number.isSafeInteger(n)||n<1||D<=0n)throw Error("bad grid");
 const seed=new Map(),discount=new Map();
 for(const [a,k,s] of certificate.discounts){
  const raw=BigInt(s),d=raw>D?D:raw;
  if(raw<0n)throw Error("negative covering discount");
  discount.set(a+","+k,d);
  if(k>0)seed.set(a+","+k,D-d);
 }
 const g=new Map(),nodes=[];
 for(let k=0;k<=R;k++)for(let a=k%2;a<=N;a+=2){
  let v=seed.get(a+","+k)||0n;
  if(k===0)v=0n;
  else for(const aa of [a-1,a+1])if(aa>=0&&aa<=N){
   const parent=g.get(aa+","+(k-1))||0n;if(parent>v)v=parent;
  }
  if(v<0n||v>D)throw Error("profile range");
  g.set(a+","+k,v);nodes.push([a,k,String(v)]);
 }
 for(const [a,k,s] of certificate.discounts){
  const d=discount.get(a+","+k),v=g.get(a+","+Math.abs(k));
  if(v===undefined)throw Error("discount outside lattice");
  if(k>0&&v<D-d||k<0&&v>d)throw Error("profile does not dominate covering dual");
 }
 return {n,N,R,D,g,nodes};
}
function makeStrategy(certificate,epsilon){
 const replay=priceRecordDual(certificate),e=Q.of(epsilon);
 if(e.cmp(0)<=0||e.cmp(HALF)>0)throw Error("epsilon must lie in (0,1/2]");
 const p=buildProfile(certificate),loss=ONE.add(e).div(2*p.n);
 return {
  format:"clock-grid-princess-p1-v1",
  scope:"Legal symmetric ordered Princess law, stopped at its first endpoint and forced outward after time 2. The guarantee follows from the verified finite dual and randomized common-coordinate interpolation.",
  n:p.n,interpolation_epsilon:e.toString(),cdf_denominator:String(p.D),
  radial_nodal:p.nodes,cell_orientation:"k modulo 2n is positive for 0 <= k < n, negative otherwise",
  quantile_rule:"Choose u uniformly in [0,1), use inf {r in [0,1] : radialCDF(t,r) > u}, and choose an independent fair sign.",
  outward_time:2,absorption_time:3,finite_value:replay.exact_value,
  exact_transfer_loss:loss.toString(),
  guaranteed_security:Q.of(replay.exact_value).sub(loss).toString()
 };
}
function createEvaluator(strategy){
 if(strategy.format!=="clock-grid-princess-p1-v1"||strategy.outward_time!==2||strategy.absorption_time!==3)throw Error("bad strategy format");
 const n=strategy.n,N=16*n,R=2*n,D=BigInt(strategy.cdf_denominator),e=Q.of(strategy.interpolation_epsilon);
 if(!Number.isSafeInteger(n)||n<1||D<=0n||e.cmp(0)<=0||e.cmp(HALF)>0)throw Error("bad strategy parameters");
 const g=new Map();
 for(const [a,k,s] of strategy.radial_nodal){
  if(!Number.isSafeInteger(a)||!Number.isSafeInteger(k)||a<0||a>N||k<0||k>R||(a+k)%2)throw Error("invalid radial node");
  const key=a+","+k,v=BigInt(s);
  if(v<0n||v>D||k===0&&v!==0n||g.has(key))throw Error("invalid radial value");
  g.set(key,v);
 }
 let count=0;
 for(let k=0;k<=R;k++)for(let a=k%2;a<=N;a+=2){
  count++;const v=g.get(a+","+k);if(v===undefined)throw Error("missing radial node");
  if(k)for(const aa of [a-1,a+1])if(aa>=0&&aa<=N&&g.get(aa+","+(k-1))>v)throw Error("nonisotone field");
 }
 if(count!==g.size)throw Error("extra radial nodes");
 const A=HALF.sub(e),B=HALF.add(e),width=e.mul(2),prefix=[];
 for(let j=0;j<=2*n;j++){
  const v=new Q(g.get((2*j)+","+R),D);
  prefix.push(j?minQ(prefix[j-1],v):v);
 }
 function coordinate(z){
  const q=Q.of(z).mul(n),cell=q.floor(),alpha=q.sub(new Q(cell));
  const mod=Number((cell%BigInt(2*n)+BigInt(2*n))%BigInt(2*n));
  return {cell:Number(cell),alpha,plus:mod<n,threshold:mod<n?alpha:ONE.sub(alpha)};
 }
 function rawTrace(t,x){
  t=Q.of(t);x=Q.of(x);
  if(t.cmp(0)<0||t.cmp(8)>0||x.cmp(-1)<0||x.cmp(1)>0)throw Error("outside raw strip");
  const u=coordinate(t.add(x)),w=coordinate(t.sub(x)),cuts=[A,B];
  for(const c of [u,w])if(c.alpha.cmp(0)!==0&&c.threshold.cmp(A)>0&&c.threshold.cmp(B)<0)cuts.push(c.threshold);
  cuts.sort((a,b)=>a.cmp(b));
  let answer=ZERO;
  function rounded(c,z){
   if(c.alpha.cmp(0)===0)return c.cell;
   return c.cell+ +(c.plus?z.cmp(c.alpha)<0:z.cmp(ONE.sub(c.alpha))>0);
  }
  for(let i=0;i+1<cuts.length;i++){
   const length=cuts[i+1].sub(cuts[i]);if(length.cmp(0)===0)continue;
   const z=cuts[i+1].add(cuts[i]).div(2),U=rounded(u,z),W=rounded(w,z),a=U+W,k=U-W;
   const v=g.get(a+","+Math.abs(k));if(v===undefined)throw Error("rounded node outside lattice");
   const f=new Q(D+(k>=0?v:-v),2n*D);
   answer=answer.add(length.div(width).mul(f));
  }
  return answer;
 }
 function rawRadial(t,r){return rawTrace(t,r).mul(2).sub(1);}
 function stoppedRadial(t,r){
  const j=Number(Q.of(t).mul(n).floor());
  return minQ(rawRadial(t,r),minQ(prefix[j],rawRadial(t,1)));
 }
 function radialCDF(t,r){
  t=Q.of(t);r=Q.of(r);
  if(t.cmp(0)<0)throw Error("negative time");
  if(r.cmp(0)<0)return ZERO;if(r.cmp(1)>=0)return ONE;
  if(t.cmp(2)<=0)return stoppedRadial(t,r);
  const radius=r.sub(t.sub(2));if(radius.cmp(0)<0)return ZERO;
  return stoppedRadial(new Q(2n),radius);
 }
 function interiorTrace(t,x){
  t=Q.of(t);x=Q.of(x);
  if(t.cmp(0)<0||x.cmp(-1)<0||x.cmp(1)>0)throw Error("outside physical strip");
  if(x.cmp(0)===0)return HALF;
  const positive=x.cmp(0)>0,r=positive?x:ZERO.sub(x);
  let value;
  if(t.cmp(2)<=0)value=stoppedRadial(t,r);
  else {
   const radius=r.sub(t.sub(2));
   value=radius.cmp(0)<0?ZERO:stoppedRadial(new Q(2n),radius);
  }
  return ONE.add(positive?value:ZERO.sub(value)).div(2);
 }
 function strictCDF(t,x){
  x=Q.of(x);if(x.cmp(-1)<=0)return ZERO;if(x.cmp(1)>0)return ONE;
  return interiorTrace(t,x);
 }
 return {rawTrace,radialCDF,interiorTrace,strictCDF,node_count:count};
}
function verifyExtraction(certificate,strategy){
 const expected=makeStrategy(certificate,strategy.interpolation_epsilon);
 if(JSON.stringify(expected)!==JSON.stringify(strategy))throw Error("strategy differs from exact extraction");
 const evaluator=createEvaluator(strategy);
 return {status:"PASS",n:strategy.n,radial_nodes:evaluator.node_count,
  finite_value:strategy.finite_value,epsilon:strategy.interpolation_epsilon,
  exact_transfer_loss:strategy.exact_transfer_loss,guaranteed_security:strategy.guaranteed_security};
}
module.exports={Q,buildProfile,makeStrategy,createEvaluator,verifyExtraction};
if(require.main===module){
 const fs=require("node:fs");
 try{
  if(!process.argv[2])throw Error("usage: node extract_princess.cjs certificate.json epsilon [output.json]");
  const certificate=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
  const strategy=makeStrategy(certificate,process.argv[3]||"1/2");
  const report=verifyExtraction(certificate,strategy);
  if(process.argv[4])fs.writeFileSync(process.argv[4],JSON.stringify(strategy,null,2)+"\n");
  process.stdout.write(JSON.stringify(report,null,2)+"\n");
 }catch(error){process.stderr.write(error.stack+"\n");process.exitCode=1;}
}
