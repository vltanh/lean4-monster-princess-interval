import fs from "node:fs/promises";
import {resolve} from "node:path";
import {pathToFileURL} from "node:url";
import germModule from "./germ_response_v8.cjs";
import frozenModule from "./germ_frozen_law_tools.cjs";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";

function verifyFrozenLawTools(E,G,F,fixtures,upperFixtures,{dictionary=null,hydrate=null,reference=null}={}){
 let pure=0,actual=0,normalization=0;const checks=[],constantRoutes=[
 [[0,"1/4"],["1/4",0],["3/4","1/2"],["9/4",-1],["17/4",1]],
 [[0,0],["1/2","1/2"],["3/2","-1/2"],[3,1],[5,-1]]
 ];
 function compare(p,m){
  const r=F.pairScore(p,m,{fullCost:true});if(!r.complete)throw Error("incomplete pair");
  const neg=new G.PLPath(p.vertices.map(([t,x])=>[t,x.neg()])),
   a=G.rawCapture(m.path,p),b=G.rawCapture(m.path,neg);
  if(a===null||b===null||!a.eq(G.Q(r.plus))||!b.eq(G.Q(r.minus))||!a.a(b).dby(2).eq(G.Q(r.exact_cost)))throw Error("pair/physical segment mismatch");
  pure+=2;
 }
 for(const f of fixtures){
  const P=G.prepare(f.paths,f.weights),starts=P.paths.map(p=>p.x[0]).concat([G.Q(-1),G.Q(1)]);
  starts.sort((a,b)=>a.cmp(b));const ss=starts.filter((x,j)=>!j||!x.eq(starts[j-1])),monsters=[];
  for(const a of ss)for(const d of [-1,1]){
   const t=G.ONE.s(a.m(d)),path=[[G.ZERO,a]];if(t.cmp(0)>0)path.push([t,G.Q(d)]);path.push([t.a(2),G.Q(-d)]);
   monsters.push(F.prepareMonster(path));
  }
  for(const raw of constantRoutes)monsters.push(F.prepareMonster(raw));
  for(const p of P.paths)for(const m of monsters)compare(p,m);
  checks.push({name:f.name,paths:P.paths.length,monsters:monsters.length});
 }
 const constantPaths=[[[0,0],[1,1]],[[0,1]],[[0,"1/3"],[1,"-2/3"],[2,"1/3"]]];
 for(const raw of constantPaths)for(const route of constantRoutes.concat([[[0,1],[2,-1],[4,1]],[[0,-1],[2,1],[4,-1]]]))compare(F.preparePath(raw),F.prepareMonster(route));
 for(const f of upperFixtures){
  for(const a of f.atoms){
   const m=F.prepareMonster(a);
   for(const raw of constantPaths)compare(F.preparePath(raw),m);
  }
 }
 let full=null;
 if(dictionary){
  if(!hydrate||!reference)throw Error("actual verification dependencies");
  const P=hydrate(dictionary),m=F.prepareMonster(reference.best.route),n=P.positive.length;let mean=G.ZERO;
  for(let j=0;j<n;j++){
   const r=F.pairScore(P.positive[j],m,{fullCost:true});
   if(!r.complete||!G.Q(r.plus).eq(G.Q(reference.best_component_data.raw_times[j]))||!G.Q(r.minus).eq(G.Q(reference.best_component_data.raw_times[j+n])))throw Error("actual first-record component mismatch");
   actual+=2;mean=mean.a(G.Q(r.exact_cost).m(P.weights[j]));
  }
  if(!mean.dby(P.W/2n).eq(G.Q(reference.best.raw_cost)))throw Error("actual normalized pair mean");
  const selected=[0,79,85,158].map(j=>P.positive[j]),ms=[m,...constantRoutes.map(x=>F.prepareMonster(x)),F.prepareMonster(upperFixtures.at(-1).atoms.at(-1))];
  for(const p of selected)for(const monster of ms)compare(p,monster);
  const rows=selected.map((path,j)=>({id:[0,79,85,158][j],path,weight:["1/2","1/3","1/6","0"][j],provenance:"frozen-dictionary"})),
   old=selected.map(p=>JSON.stringify(p.json())),law=F.orderedLaw(rows),again=hydrate(law.dictionary());
  if(law.metadata.length!==3||law.metadata.some(x=>x.id===158))throw Error("zero weight/provenance");
  for(const t of ["0","1/2","1","2"])for(const rank of ["0","1/8","1/2","7/8","1"]){
   const x=law.quantile(t,rank),r=law.ranks(t,x),target=G.Q(rank).m(r.total);
   if(G.Q(r.strict).cmp(target)>0||G.Q(r.closed).cmp(target)<0)throw Error("strict/closed quantile normalization");
   let lo=0n,hi=0n;
   for(let j=0;j<again.paths.length;j++){const z=again.paths[j].at(G.Q(t)).cmp(x);if(z<0)lo+=again.weights[j];if(z<=0)hi+=again.weights[j];}
   if(lo*r.total!==r.strict*again.W||hi*r.total!==r.closed*again.W)throw Error("dictionary ordered-law mismatch");normalization++;
  }
  selected.forEach((p,j)=>{if(JSON.stringify(p.json())!==old[j])throw Error("frozen geometry mutated");});
  full={signed_component_matches:actual,ordered_quantile_checks:normalization,raw_m1_limit:mean.dby(P.W/2n).limit().str(),retained_ids:law.metadata.map(x=>x.id)};
 }
 return{scope:"Frozen physical rows; exact unit-Monster pure capture and normalized implicit ordered laws.",fixtures:checks,pure_segment_equalities:pure,actual:full,cache:F.stats(),arithmetic:G.stats()};
}

export function verifyFrozenRows(fixtures,upperFixtures,{dictionary=null,cachedModule=null,reference=null}={}){
 const E=createOracle(),G=germModule.createGermOracle(E),F=frozenModule.createFrozenLawTools(G),
  H=cachedModule?cachedModule.createCachedGermPaths(G):null;
 return verifyFrozenLawTools(E,G,F,fixtures,upperFixtures,{dictionary,hydrate:H?(d=>H.hydrate(d)):null,reference});
}
async function main(){
 const[fixturesFile,upperFile,output,dictionaryFile,referenceFile,hydratorFile]=process.argv.slice(2);
 if(!fixturesFile||!upperFile||!output)throw Error("usage: node verify_frozen_law_tools.mjs GERM_FIXTURES.json UPPER_FIXTURES.json REPORT.json [CLIPPED_DICTIONARY.json M1_REPORT.json SHARED_HYDRATOR.cjs]");
 const fixtures=JSON.parse(await fs.readFile(fixturesFile,"utf8")),upper=JSON.parse(await fs.readFile(upperFile,"utf8"));
 const dictionary=dictionaryFile?JSON.parse(await fs.readFile(dictionaryFile,"utf8")):null,
  reference=referenceFile?JSON.parse(await fs.readFile(referenceFile,"utf8")):null,
  cachedModule=hydratorFile?(await import(pathToFileURL(resolve(hydratorFile)).href)).default:null,
  r=verifyFrozenRows(fixtures,upper,{dictionary,cachedModule,reference});
 await fs.writeFile(output,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.pure_segment_equalities,"direct physical comparisons",r.actual?.signed_component_matches||0,"actual component checks");
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
