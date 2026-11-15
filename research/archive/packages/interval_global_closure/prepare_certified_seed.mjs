import fs from "node:fs/promises";
import {resolve,join} from "node:path";
import {pathToFileURL} from "node:url";
import {createHash} from "node:crypto";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";
import frozenModule from "./germ_frozen_law_tools.cjs";
import sourceModule from "./certified_seed_source.cjs";

function sha(s){return createHash("sha256").update(s).digest("hex");}
function gitSha(s){const b=Buffer.from(s);return createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex");}
export async function prepareCertifiedSeed(sourcePath,bankPath,outputDir){
 const sourceText=await fs.readFile(sourcePath,"utf8"),bankText=await fs.readFile(bankPath,"utf8"),
  data=JSON.parse(sourceText),bank=JSON.parse(bankText),atoms=bank.atoms||bank,
  E=createOracle(),G=germModule.createGermOracle(E),F=frozenModule.createFrozenLawTools(G),S=sourceModule.createCertifiedSeedSource(G,F),
  provenance={path:"packages/interval_uniform_reduction/princess_strategy.json",sha256:sha(sourceText),git_blob_sha1:gitSha(sourceText)},
  seed=S.prepare(data,{provenance}),columns=[],ids=[];
 let directChecks=0;
 function direct(p,m,record){
  const neg=new G.PLPath(p.vertices.map(([t,x])=>[t,x.neg()])),a=G.rawCapture(m.path,p),b=G.rawCapture(m.path,neg);
  if(a===null||b===null||!a.eq(G.Q(record[0]))||!b.eq(G.Q(record[1])))throw Error("chronological direct-capture discrepancy");directChecks+=2;
 }
 const attaining=F.prepareMonster(seed.attaining),certificate=S.column(seed,attaining,{fullCost:true});
 if(!G.Q(certificate.mean).eq(seed.declaredValue))throw Error("archived attaining route changed value");
 seed.rows.forEach((r,i)=>direct(r.path,attaining,certificate.firstHits[i]));
 for(let j=0;j<atoms.length;j++){
  const m=F.prepareMonster(atoms[j]),c=S.column(seed,m,{fullCost:true});
  if(G.Q(c.mean).cmp(seed.declaredValue)<0)throw Error("Monster bank contradicts the archived unrestricted source guarantee");
  if(j%137===0)for(const i of [0,Math.floor(seed.rows.length/2),seed.rows.length-1])direct(seed.rows[i].path,m,c.firstHits[i]);
  columns.push(c);ids.push("old:"+j);
 }
 const a=G.Q("15/16").s(G.eps),attack=[[G.ZERO,a],[G.ONE.a(a),G.Q(-1)],[G.Q(3).a(a),G.ONE]],
  extra=S.column(seed,attack,{fullCost:true});
 seed.rows.forEach((r,i)=>direct(r.path,F.prepareMonster(attack),extra.firstHits[i]));
 if(G.Q(extra.mean).limit().cmp(seed.declaredValue.limit())<0)throw Error("germ attack contradicts source guarantee");
 columns.push(extra);ids.push("inward-M1:15/16-eps");
 const matrix=seed.rows.map((_,i)=>columns.map(c=>c.limits[i])),numeric=matrix.map(row=>row.map(x=>E.Q(x).num()));
 const oldWeights=bank.best?.weights||bank.weights;
 const oracle=oldWeights?S.bestResponse(seed,columns.slice(0,atoms.length),oldWeights):null;
 let min=0;for(let j=1;j<columns.length;j++)if(G.Q(columns[j].meanLimit).cmp(G.Q(columns[min].meanLimit))<0)min=j;
 const dictionary=seed.law.dictionary(),frozenRows={scope:"Immutable exact constant-germ Princess pairs from the supplied certified ordered source.",provenance,
  rows:seed.rows.map(r=>({id:r.id,weight:r.weight,path:r.path.json(),provenance:r.provenance}))};
 const report={scope:"Exact pure-pair payoff matrix and full quantile-family source oracle for a fixed certified finite law; no new equilibrium or improved unrestricted lower value claimed.",
  source:provenance,bank:{sha256:sha(bankText),git_blob_sha1:gitSha(bankText),old_atoms:atoms.length},
  counts:{positive_paths:seed.rows.length,signed_paths:2*seed.rows.length,columns:columns.length,source_vertices:seed.originalVertices,compressed_vertices:seed.vertices,
   adjacent_order_vertex_checks:seed.orderChecks,direct_segment_checks:directChecks},
  certified_value:data.value,certified_value_decimal:seed.declaredValue.limit().num(),attaining_route:certificate.route,attaining_rescore:certificate.mean,
  old_bank_and_extra_minimum:{id:ids[min],cost:columns[min].meanLimit,decimal:G.Q(columns[min].meanLimit).limit().num()},
  extra_attack:{id:ids.at(-1),route:extra.route,exact_source_cost:extra.mean,limit:extra.meanLimit,decimal:G.Q(extra.meanLimit).limit().num()},
  source_best_response_to_old_best_weights:oracle,cache:F.stats(),arithmetic:G.stats()};
 await fs.mkdir(outputDir,{recursive:true});
 const payload={scope:report.scope,source:provenance,row_ids:seed.rows.map(r=>r.id),column_ids:ids,
  exact_limits:matrix,decimals:numeric,source_weights:seed.rows.map(r=>r.weight),source_exact_costs:columns.map(c=>c.mean),source_limits:columns.map(c=>c.meanLimit),
  extra_monsters:[{id:ids.at(-1),route:extra.route}]};
 for(const[name,obj]of [["certified_seed_dictionary.json",dictionary],["certified_seed_rows.json",frozenRows],
  ["certified_seed_payoffs.json",payload],["certified_seed_report.json",report]])await fs.writeFile(join(outputDir,name),JSON.stringify(obj,null,2)+"\n");
 await fs.writeFile(join(outputDir,"princess_strategy.json"),sourceText);
 console.log(JSON.stringify({status:"PASS",paths:seed.rows.length,columns:columns.length,direct:directChecks,
  old_bank_minimum:report.old_bank_and_extra_minimum,extra:report.extra_attack,oracle:oracle?{value:oracle.value,ids:oracle.ids,sourceMean:oracle.sourceMean}:null,output:resolve(outputDir)}));
 return report;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 const[source,bank,out]=process.argv.slice(2);if(!source||!bank||!out)throw Error("usage: node prepare_certified_seed.mjs PRINCESS_STRATEGY.json BANK_CHECKPOINT.json OUTPUT_DIR");
 await prepareCertifiedSeed(source,bank,out);
}
