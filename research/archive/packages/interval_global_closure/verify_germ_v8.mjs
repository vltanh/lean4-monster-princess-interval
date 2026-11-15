import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import germModule from "./germ_response_v8.cjs";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";

export function verifyGermAdapter(inputs){
 const F=createOracle(),G=germModule.createGermOracle(F),q=G.Q;
 const guard=germModule.createGermOracle(F);
 if(guard.Q(1).s(guard.eps.m(1000)).eq(0))throw Error("equality identity failure");
 if(F.Q(guard.stats().radius).cmp("1/2000")>0)throw Error("equality radius guard");
 const hole=guard.eps.s("1/1000");
 if(!hole.dby(hole).eq(1)||F.Q(guard.stats().radius).cmp("1/2000")>0)throw Error("division guard");
 function finish(s){while(!s.runSlice(5000,1000)){}const r=s.result();if(!r.complete)throw Error("incomplete exact fixture");return r;}
 const reports=[];
 for(const f of inputs){
  const raw=f.paths.map(p=>p.map(r=>r.map(q)));
  for(const mode of ["raw","sorted"]){
   const s=finish(new G.CaptureSearch(raw,f.weights,{mode,nodeLimit:100000}));
   const u=finish(new G.CaptureSearch(raw,f.weights,{mode,prune:false,nodeLimit:100000}));
   if(!q(s.value).eq(q(u.value)))throw Error("pruned/unpruned germ mismatch");
   const epsilon=F.Q(G.stats().radius).dby(2);
   const physical=raw.map(p=>p.map(r=>r.map(x=>x.evaluate(epsilon).str())));
   const r=finish(new F.CaptureSearch(physical,f.weights,{mode,nodeLimit:100000}));
   if(!F.Q(r.value).eq(q(s.value).evaluate(epsilon).str()))throw Error("rational specialization mismatch");
   const route=s.route.map(p=>p.map(x=>q(x).evaluate(epsilon).str())),monster=new F.PLPath(route);
   let direct;
   if(mode==="raw")direct=physical.reduce((sum,p,j)=>{const t=F.rawCapture(monster,new F.PLPath(p));if(t===null)throw Error("missed specialized path");return sum.a(t.m(f.weights[j]));},F.ZERO);
   else{const d=F.prepare(physical,f.weights);const c=F.sortedCapture(d.paths,d.weights,monster);if(!c.complete)throw Error("incomplete specialized records");direct=c.value;}
   if(!direct.eq(r.value))throw Error("independent specialized capture mismatch");
   reports.push({name:f.name,mode,limit:q(s.value).limit().str(),nodes:s.stats.nodes,unpruned_nodes:u.stats.nodes,specialized_value:r.value,epsilon:epsilon.str()});
  }
 }
 return{scope:"Exact germ adapter regressions, not a game bound.",equality_and_division_radius_guard:true,fixtures:reports,arithmetic:G.stats(),unchanged_finite_core_blob:"51dbac43b59c3041abf831837dc58fde2a9294b2",reference_python_germ_blob:"99f6b3f384a71f155280d1c7aa240b65a112ddcb"};
}
async function main(){
 const[input,output]=process.argv.slice(2);if(!input||!output)throw Error("usage: node verify_germ_v8.mjs INPUTS.json REPORT.json");
 const report=verifyGermAdapter(JSON.parse(await fs.readFile(input,"utf8")));
 await fs.writeFile(output,JSON.stringify(report,null,2)+"\n");console.log("PASS",report.fixtures.length,"exact germ/rational fixtures");
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
