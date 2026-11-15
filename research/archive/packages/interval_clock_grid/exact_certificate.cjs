"use strict";
// All certificate acceptance arithmetic is integer or BigInt.
// Floating reconstruction only proposes a witness; verifyCertificate accepts it exactly.

function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const c=a%b;a=b;b=c;}return a;}
function fraction(a,b){if(b<=0n)throw Error("nonpositive denominator");const d=gcd(a,b);return String(a/d)+(b/d===1n?"":"/"+String(b/d));}
function commonDenominator(values,limit=1000000){
 for(let d=1;d<=limit;d++)if(values.every(x=>Math.abs(x*d-Math.round(x*d))<1e-7))return {denominator:BigInt(d),numerators:values.map(x=>BigInt(Math.round(x*d)))};
 throw Error("simple rational reconstruction failed");
}
function inspectPlans(n,plans,denominator){
 const N=16*n,R=2*n,pressure=new Map();let probability=0n,mass=0n;
 function add(j,k,q){const key=j+","+k;pressure.set(key,(pressure.get(key)||0n)+q);mass+=q;}
 for(const plan of plans){
  const w=BigInt(plan.weight_numerator);if(w<=0n)throw Error("nonpositive plan weight");probability+=w;
  const k0=plan.start_grid;if(!Number.isSafeInteger(k0)||k0%2||Math.abs(k0)>R)throw Error("initial point");
  const positions=[k0];for(const d of plan.moves){if(d!==1&&d!==-1)throw Error("non-unit move");const k=positions.at(-1)+d;if(Math.abs(k)>R)throw Error("leaves arena");positions.push(k);}
  if(plan.moves.length>N)throw Error("horizon");
  const km=positions.indexOf(-R),kp=positions.indexOf(R),center=positions.indexOf(0);
  if(km<0||kp<0||center<0||center>4*n)throw Error("visit deadline");
  for(const [key,end,sign] of [["minus_charges",km,1],["plus_charges",kp,-1]]){
   const b=new Array(end).fill(0);
   for(const [j,a] of plan[key]){if(!Number.isSafeInteger(j)||!Number.isSafeInteger(a)||a<=0||j<0||j>=end)throw Error("invalid selected clock time");b[j]+=a;}
   let cumulative=0;
   for(let j=0;j<end;j++){cumulative+=b[j];if(cumulative<j+1)throw Error("left-limit causal prefix");if(b[j])add(j,sign*positions[j],w*BigInt(b[j]));}
   if(cumulative!==end)throw Error("wrong active clock mass");
  }
 }
 if(probability!==denominator)throw Error("probability normalization");
 return {pressure,mass};
}
function integerMatching(g,pressure){
 const count=g.events.length,S=count,T=count+1,adj=Array.from({length:count+2},()=>[]),links=[];
 function edge(u,v,cap){const a={v,cap,rev:adj[v].length},b={v:u,cap:0n,rev:adj[u].length};adj[u].push(a);adj[v].push(b);return a;}
 let positive=0n;
 for(let i=0;i<count;i++){
  const p=pressure.get(g.events[i].join(","))||0n;
  if(g.events[i][1]>0){edge(S,i,p);positive+=p;}else edge(i,T,p);
 }
 for(const [p,q] of g.matches)links.push([p,q,edge(p,q,positive+1n)]);
 let flow=0n;
 for(;;){
  const level=new Int32Array(count+2).fill(-1),queue=[S];level[S]=0;
  for(let h=0;h<queue.length;h++){const u=queue[h];for(const e of adj[u])if(e.cap>0n&&level[e.v]<0){level[e.v]=level[u]+1;queue.push(e.v);}}
  if(level[T]<0)break;
  const next=new Int32Array(count+2);
  function dfs(u,f){if(u===T)return f;for(;next[u]<adj[u].length;next[u]++){const e=adj[u][next[u]];if(e.cap>0n&&level[e.v]===level[u]+1){const z=dfs(e.v,f<e.cap?f:e.cap);if(z>0n){e.cap-=z;adj[e.v][e.rev].cap+=z;return z;}}}return 0n;}
  for(;;){const z=dfs(S,positive+1n);if(z===0n)break;flow+=z;}
 }
 return {flow,positive,matching:links.map(([p,q,e])=>[...g.events[p],...g.events[q],String(adj[q][e.rev].cap)]).filter(x=>x[4]!=="0")};
}
function inspectPrimal(certificate){
 const n=certificate.n;
 if(!Number.isSafeInteger(n)||n<1||certificate.completion_horizon!==8||certificate.center_deadline!==2||certificate.physical_step!=='1/'+(2*n)||certificate.objective_scale!=='1/'+(4*n))throw Error('invalid model metadata');
 const W=BigInt(certificate.weight_denominator);
 if(W<=0n)throw Error("invalid weight denominator");
 const stats=inspectPlans(n,certificate.paths,W),used=new Map();let matched=0n;
 for(const [t,x,s,y,amount] of certificate.matching){
  const q=BigInt(amount);if(q<=0n||!Number.isSafeInteger(t)||!Number.isSafeInteger(x)||!Number.isSafeInteger(s)||!Number.isSafeInteger(y)||x<=0||y>=0||-y<x+Math.abs(s-t))throw Error("invalid cone match");
  for(const key of [t+","+x,s+","+y])used.set(key,(used.get(key)||0n)+q);matched+=q;
 }
 for(const [key,q] of used)if(q>(stats.pressure.get(key)||0n))throw Error("matching capacity");
 let positive=0n;for(const [key,q] of stats.pressure)if(Number(key.split(",")[1])>0)positive+=q;
 const primal=stats.mass+positive-matched;
 return {n,W,stats,matched,positive,primal};
}
function verifyCertificate(certificate,graphBuilder){
 const {n,W,stats,matched,positive,primal}=inspectPrimal(certificate),g=graphBuilder(n),D=BigInt(certificate.discount_denominator);
 if(D<=0n)throw Error("invalid discount denominator");
 const discounts=new Map();
 for(const [t,x,a] of certificate.discounts){
  const q=BigInt(a),key=t+","+x;if(q<0n||discounts.has(key))throw Error("invalid discount");discounts.set(key,q);
 }
 if(discounts.size!==g.events.length)throw Error("incomplete discount geometry");
 const d=g.events.map(z=>{const q=discounts.get(z.join(","));if(q===undefined)throw Error("missing event discount");return q;});
 for(const [p,q] of g.matches)if(d[p]+d[q]<D)throw Error("matching dual inequality");
 const tail=new Array(g.states.length).fill(null),next=new Array(g.states.length).fill(-1);tail[1]=0n;
 for(let oi=g.order.length-1;oi>=0;oi--){
  const u=g.order[oi];if(u===1)continue;
  for(const e of g.outgoing[u]){
   const v=g.edges[e][1];if(tail[v]===null)continue;
   const cost=BigInt(g.base[e])*D-(g.eventIds[e]<0?0n:d[g.eventIds[e]]),value=cost+tail[v];
   if(tail[u]===null||value<tail[u]){tail[u]=value;next[u]=e;}
  }
 }
 if(tail[0]===null)throw Error("no complete physical calendar");
 if(primal*D!==tail[0]*W)throw Error("nonzero exact primal-dual gap: "+fraction(primal,W)+" vs "+fraction(tail[0],D));
 const value=fraction(primal,4n*BigInt(n)*W),lower=fraction(primal-2n*W,4n*BigInt(n)*W);
 if(certificate.exact_value&&certificate.exact_value!==value)throw Error("claimed value mismatch");
 if(certificate.global_lower&&certificate.global_lower!==lower)throw Error("claimed lower mismatch");
 return {status:"PASS",n,nodes:g.states.length,flow_arcs:g.edges.length,pressure_nodes:g.events.length,matching_edges:g.matches.length,
  physical_calendar_plans:certificate.paths.length,positive_matching_entries:certificate.matching.length,
  exact_scaled_primal:fraction(primal,W),exact_scaled_dual:fraction(tail[0],D),exact_value:value,global_lower:lower,
  enclosure_width:fraction(1n,2n*BigInt(n)),baseline:fraction(stats.mass,4n*BigInt(n)*W),deficiency:fraction(positive-matched,4n*BigInt(n)*W)};
}
function certifyNumerical(numerical,graphBuilder){
 const g=graphBuilder(numerical.n),small=numerical.paths.filter(p=>p.weight>1e-9),w=commonDenominator(small.map(p=>p.weight));
 if(w.numerators.reduce((a,b)=>a+b,0n)!==w.denominator)throw Error("reconstructed probability mass");
 const plans=small.map((p,i)=>({weight_numerator:String(w.numerators[i]),start_grid:p.start_grid,moves:p.moves,minus_charges:p.minus_charges,plus_charges:p.plus_charges}));
 const stats=inspectPlans(g.n,plans,w.denominator),match=integerMatching(g,stats.pressure);
 const discount=commonDenominator(numerical.result.discounts.map(x=>Math.max(0,x)));
 const certificate={scope:"Exact primal and dual certificate for the complete polynomial clock-grid LP. Global enclosure uses the effective common-quantization theorem.",
  n:g.n,completion_horizon:8,center_deadline:2,physical_step:"1/"+(2*g.n),objective_scale:"1/"+(4*g.n),
  weight_denominator:String(w.denominator),paths:plans,matching:match.matching,
  discount_denominator:String(discount.denominator),discounts:g.events.map((z,i)=>[...z,String(discount.numerators[i])]),
  exact_value:fraction(stats.mass+match.positive-match.flow,4n*BigInt(g.n)*w.denominator),
  global_lower:fraction(stats.mass+match.positive-match.flow-2n*w.denominator,4n*BigInt(g.n)*w.denominator)};
 const replay=verifyCertificate(certificate,graphBuilder);return {certificate,replay};
}

module.exports={gcd,fraction,commonDenominator,inspectPlans,integerMatching,inspectPrimal,verifyCertificate,certifyNumerical};
