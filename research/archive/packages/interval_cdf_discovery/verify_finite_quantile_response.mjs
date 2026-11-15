import {createOracle} from "./finite_quantile_response.mjs";
import fs from "node:fs/promises";

function verifyOracle(L,inputs){
 let archivedRaw=0,archivedSorted=0,arbitrarySearch=0,arbitrarySorted=0,rayChecks=0;
 const finish=s=>{while(!s.runSlice(10000,1000)){}const r=s.result();if(!r.complete)throw Error("incomplete fixture");return r;};
 const eq=(a,b,msg)=>{if(!L.Q(a).eq(b))throw Error(msg+": "+a+" != "+b);};
 for(const f of inputs.archived){
   eq(finish(new L.CaptureSearch(f.data.paths,f.data.weights,{mode:"raw"})).value,f.exact_value,"archived raw");archivedRaw++;
   const q=L.explicitQuantiles(f.data.paths,f.data.weights),a=finish(new L.CaptureSearch(f.data.paths,f.data.weights,{mode:"sorted"})),b=finish(new L.CaptureSearch(q.paths,q.weights,{mode:"raw"}));
   eq(a.value,b.value,"implicit quantile");if(L.Q(a.value).cmp(f.exact_value)<0)throw Error("sorting decreased hiding");archivedSorted++;
 }
 const sixty=finish(new L.CaptureSearch(inputs.sixty.paths,inputs.sixty.weights,{mode:"raw"}));eq(sixty.value,"56305800187/40000000000","sixty path certificate");
 let seed=419109;const rand=n=>{seed=(1664525*seed+1013904223)>>>0;return seed%n;};
 function directRay(p,t,x,d){
   const sg=p.at(t).cmp(x);if(!sg)return t;if(sg!==d)return null;
   const wall=t.a(L.ONE.s(x.m(d))),ts=[t,...p.t.filter(z=>z.cmp(t)>0&&z.cmp(wall)<0),wall];
   for(let k=0;k+1<ts.length;k++){
     const a=ts[k],b=ts[k+1],fa=p.at(a).s(x.a(a.s(t).m(d))),fb=p.at(b).s(x.a(b.s(t).m(d)));
     if(fa.eq(0))return a;if(fa.cmp(0)*fb.cmp(0)<=0)return a.a(b.s(a).m(fa).dby(fa.s(fb)));
   }throw Error("direct ray missed");
 }
 for(const f of inputs.arbitrary){
   const a=finish(new L.CaptureSearch(f.paths,f.weights,{mode:"raw"})),b=finish(new L.CaptureSearch(f.paths,f.weights,{mode:"raw",prune:false}));
   eq(a.value,b.value,"pruning");eq(a.value,f.raw,"stored arbitrary raw");arbitrarySearch++;
   const q=L.explicitQuantiles(f.paths,f.weights),c=finish(new L.CaptureSearch(f.paths,f.weights,{mode:"sorted"})),d=finish(new L.CaptureSearch(q.paths,q.weights,{mode:"raw"}));
   eq(c.value,d.value,"arbitrary sorting");eq(c.value,f.sorted,"stored arbitrary sorted");arbitrarySorted++;
   for(const raw of f.paths){const p=new L.PLPath(raw);for(let k=0;k<8;k++){const t=L.Q(rand(9)).dby(8),x=L.Q(rand(17)-8).dby(8);for(const dir of [-1,1]){const v=p.hit(t,x,dir),w=directRay(p,t,x,dir);if(v===null?w!==null:w===null||!v.eq(w))throw Error("independent ray");rayChecks++;}}}
 }
 const ps=[[[0,0]]],ws=["4096"];for(const [x,w]of[["1/4",512],["1/2",64],["3/4",8],["1",1]]){ps.push([[0,x]],[[0,L.Q(x).neg().str()]]);ws.push(String(w),String(w));}
 const shell=finish(new L.CaptureSearch(ps,ws,{mode:"sorted"}));eq(shell.value,"381/2633","three interior turns");
 const p=[[[0,"-1/2"],[1,"1/2"],[2,"-1/2"]],[[0,"1/2"],[1,"-1/2"],[2,"1/2"]]],pd=L.prepare(p,[1,1]),m=new L.PLPath([[0,"1/4"],[2,"1/4"],["11/4",1],["19/4",-1]]);
 const raw=pd.paths.reduce((a,p)=>a.a(L.rawCapture(m,p)),L.ZERO).dby(2),sorted=L.sortedCapture(pd.paths,pd.weights,m);
 eq(raw,"1/2","crossing raw");eq(sorted.value,"9/4","crossing sorted");
 return{scope:"Exact finite rational polygonal laws, constant tails. No game-value or continuous-CDF certification.",archivedRaw,archivedSorted,arbitrarySearch,arbitrarySorted,rayChecks,sixty,shell,crossing:{raw:raw.str(),sorted:sorted.value.str()}};
}

const input=JSON.parse(await fs.readFile(new URL("./snapshots/finite_quantile_response_inputs.json",import.meta.url),"utf8"));
console.log(JSON.stringify(verifyOracle(createOracle(),input),null,2));
