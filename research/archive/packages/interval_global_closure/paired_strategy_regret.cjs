"use strict";
// Exact cross-play and unilateral regrets for two supplied certified laws.
// This replays physical captures; it imports, rather than reruns, each
// archived unrestricted-response theorem/certificate.
function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const r=a%b;a=b;b=r;}return a;}
function frac(n,d=1n){n=BigInt(n);d=BigInt(d);if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d;}const g=gcd(n,d);return{n:n/g,d:d/g};}
function parse(s){const p=String(s).split("/");return frac(p[0],p[1]||1);}
function add(a,b){return frac(a.n*b.d+b.n*a.d,a.d*b.d);}
function sub(a,b){return frac(a.n*b.d-b.n*a.d,a.d*b.d);}
function times(a,b){return frac(a.n*b.n,a.d*b.d);}
function divide(a,b){return frac(a.n*b.d,a.d*b.n);}
function show(a){return a.d===1n?String(a.n):a.n+"/"+a.d;}
function decimalExpansion(a,n=30){let k=a.n,sign=k<0n?"-":"";if(k<0n)k=-k;const whole=k/a.d;let r=k%a.d,digits="";for(let i=0;i<n;i++){r*=10n;digits+=r/a.d;r%=a.d;}return sign+whole+"."+digits;}
function cmp(a,b){const d=a.n*b.d-b.n*a.d;return d<0n?-1:d>0n?1:0;}
function safe(n){const x=Number(n);if(!Number.isSafeInteger(x)||BigInt(x)!==n)throw Error("unsafe integer");return x;}
function scaled(q,D){if(D%q.d)throw Error("common scale");return safe(q.n*(D/q.d));}
function reflect(p){return p.map(([t,x])=>[t,-x]);}
function validate(p,D,unit=false){
 if(!p.length||p[0][0]!==0)throw Error("start");
 for(let i=0;i<p.length;i++){
  const[t,x]=p[i];if(!Number.isSafeInteger(t)||!Number.isSafeInteger(x)||t<0||Math.abs(x)>D)throw Error("vertex");
  if(i){const[a,y]=p[i-1];if(t<=a||![0,t-a,a-t].includes(x-y)||unit&&Math.abs(x-y)!==t-a)throw Error("speed");}
 }
 if(4*(p.at(-1)[0]+D)>Number.MAX_SAFE_INTEGER)throw Error("unsafe capture arithmetic");
}
function at(p,i,t){if(i+1===p.length)return p[i][1];const[a,x]=p[i],[b,y]=p[i+1];return x+(y-x)/(b-a)*(t-a);}
function hit2(m,p){
 let i=0,j=0,t=0;
 while(i+1<m.length){
  const end=Math.min(m[i+1][0],j+1<p.length?p[j+1][0]:Infinity);
  const mx=at(m,i,t),px=at(p,j,t),d=mx-px;
  if(d===0)return 2*t;
  const mv=(m[i+1][1]-m[i][1])/(m[i+1][0]-m[i][0]);
  const pv=j+1<p.length?(p[j+1][1]-p[j][1])/(p[j+1][0]-p[j][0]):0;
  const rate=mv-pv;
  if(rate){const h=2*t-2*d/rate;if(h>=2*t&&h<=2*end){if(!Number.isSafeInteger(h))throw Error("nonintegral doubled hit");return h;}}
  t=end;if(t===m[i+1][0])i++;if(j+1<p.length&&t===p[j+1][0])j++;
 }
 throw Error("uncaught target");
}
function independentHit2(m,p){
 // Independently merge endpoint times and detect zero/sign changes.
 const end=m.at(-1)[0],events=[...new Set([...m,...p].map(v=>v[0]).filter(t=>t<=end))].sort((a,b)=>a-b);
 let i=0,j=0,lastT=0,lastD=null;
 for(const t of events){
  while(i+1<m.length&&m[i+1][0]<t)i++;
  while(j+1<p.length&&p[j+1][0]<t)j++;
  const d=at(m,i,t)-at(p,j,t);
  if(d===0)return 2*t;
  if(lastD!==null&&Math.sign(d)!==Math.sign(lastD)){
   const num=2n*BigInt(t-lastT)*BigInt(Math.abs(lastD)),den=BigInt(Math.abs(lastD)+Math.abs(d));
   if(num%den)throw Error("doubled intersection scale");
   return safe(2n*BigInt(lastT)+num/den);
  }
  lastT=t;lastD=d;
 }
 throw Error("independent uncaught target");
}
function run(princess,monster){
 const S=BigInt(princess.S),half=frac(1,2),raw=[];
 let D=S;
 for(const atom of monster.atoms){
  const path=atom.exact_light.map(([u,v])=>{u=parse(u);v=parse(v);return[times(add(u,v),half),times(sub(u,v),half)];});
  for(const p of path)for(const q of p)D=D/gcd(D,q.d)*q.d;
  raw.push(path);
 }
 const dscale=safe(D),ps=princess.paths_h.map(p=>p.map(([t,x])=>[scaled(frac(t,S),D),scaled(frac(x,S),D)]));
 const ms=raw.map(p=>p.map(([t,x])=>[scaled(t,D),scaled(x,D)]));
 const ws=princess.weights_h.map(BigInt),wm=monster.atoms.map(a=>BigInt(a.weight_numerator)),W=ws.reduce((a,b)=>a+b,0n),M=BigInt(monster.weight_denominator);
 if(W!==BigInt(princess.weight_total)||wm.reduce((a,b)=>a+b,0n)!==M||ws.some(w=>w<=0n)||wm.some(w=>w<=0n))throw Error("weights");
 ps.forEach(p=>validate(p,dscale));ms.forEach(p=>{validate(p,dscale,true);if(!p.some(v=>v[1]===dscale)||!p.some(v=>v[1]===-dscale))throw Error("endpoint completion");});
 const ns=ps.map(reflect),rows=[];let numerator=0n,captures=0;
 for(let j=0;j<ms.length;j++){
  let row=0n;
  for(let i=0;i<ps.length;i++){
   const a=hit2(ms[j],ps[i]),b=hit2(ms[j],ns[i]);
   if(a!==independentHit2(ms[j],ps[i])||b!==independentHit2(ms[j],ns[i]))throw Error("independent capture mismatch");
   row+=ws[i]*BigInt(a+b);captures+=2;
  }
  numerator+=wm[j]*row;rows.push(show(frac(row,4n*W*D)));
 }
 const J=frac(numerator,4n*M*W*D),L=parse(princess.value),U=parse(monster.value);
 if(cmp(J,L)<0||cmp(J,U)>0)throw Error("cross play outside certified interval");
 const old=princess.attaining_monster.map(([t,x])=>[scaled(frac(t,S),D),scaled(frac(x,S),D)]);
 validate(old,dscale,true);let lowerReplay=0n;
 for(let i=0;i<ps.length;i++)for(const p of[ps[i],ns[i]]){
  const a=hit2(old,p);if(a!==independentHit2(old,p))throw Error("lower response capture");lowerReplay+=ws[i]*BigInt(a);
 }
 if(cmp(frac(lowerReplay,4n*W*D),L)!==0)throw Error("archived lower response payoff");
 const rM=sub(J,L),rP=sub(U,J),eps=cmp(rM,rP)>=0?rM:rP;
 return{scope:"Explicit approximate saddle pair using the archived unrestricted-response certificates. Cross payoffs and both direct-capture implementations are recomputed exactly; the global searches are imported, not rerun.",
 princess_law:"../interval_uniform_reduction/princess_strategy.json",monster_law:"upper_dyadic_exact.json",
 princess_paths:2*ps.length,monster_reflected_pairs:ms.length,coordinate_scale:String(D),
 direct_captures:captures,independent_captures:captures,archived_monster_response_captures:2*ps.length,
 lower_response:L.n+"/"+L.d,upper_response:U.n+"/"+U.d,cross_payoff:show(J),
 monster_improvement:show(rM),princess_improvement_supremum:show(rP),
 maximum_unilateral_improvement:show(eps),total_response_gap:show(sub(U,L)),
 decimal:{cross_payoff:Number(J.n)/Number(J.d),monster_improvement:Number(rM.n)/Number(rM.d),
 princess_improvement_supremum:Number(rP.n)/Number(rP.d),maximum_unilateral_improvement:Number(eps.n)/Number(eps.d)},
 decimal_expansions:{lower_response:decimalExpansion(L),upper_response:decimalExpansion(U),cross_payoff:decimalExpansion(J),monster_improvement:decimalExpansion(rM),princess_improvement_supremum:decimalExpansion(rP),maximum_unilateral_improvement:decimalExpansion(eps),total_response_gap:decimalExpansion(sub(U,L))},
 monster_pair_payoffs:rows};
}
module.exports={run,hit2,independentHit2};
if(require.main===module){
 const fs=require("node:fs"),path=require("node:path");
 const p=JSON.parse(fs.readFileSync(path.join(__dirname,"../interval_uniform_reduction/princess_strategy.json"),"utf8"));
 const m=JSON.parse(fs.readFileSync(path.join(__dirname,"upper_dyadic_exact.json"),"utf8"));
 const r=run(p,m),destination=process.argv[2]||path.join(__dirname,"paired_strategy_regret.json");
 fs.writeFileSync(destination,JSON.stringify(r,null,2)+"\n");
 const{monster_pair_payoffs,...summary}=r;console.log(JSON.stringify(summary,null,2));
}
