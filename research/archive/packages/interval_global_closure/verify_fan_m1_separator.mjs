import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";
import fanModule from "./germ_translation_fan.cjs";
import separatorModule from "./fan_m1_separator.cjs";
import {physicalFanScore} from "./verify_translation_fan.mjs";

export function verifyFanM1Separator(){
 const E=createOracle(),G=germModule.createGermOracle(E),Q=G.Q,Z=G.ZERO,O=G.ONE,e=G.eps,T=fanModule.createTranslationFan(G),
  models=[
   {name:"stationary_outward",rows:[{path:[[0,"1/2"]],lo:0,hi:"1/10",weight:1}]},
   {name:"moving_symmetric",rows:[{path:[[0,"1/4"],["1/2","3/4"],["5/4",0],["9/4",1]],lo:"-1/8",hi:"1/8",weight:1}]},
   {name:"two_outward_waves",rows:[{path:[[0,"1/4"],["1/2","3/4"],["5/4",0],["9/4",1]],lo:0,hi:"1/4",weight:"2/5"},{path:[[0,"3/4"],["3/4",0],["7/4",1]],lo:0,hi:"1/8",weight:"3/5"}]},
   {name:"asymmetric_negative_window",rows:[{path:[[0,"-1/4"],["1/2","1/4"],[1,"-1/4"],[2,"3/4"]],lo:"-1/4",hi:"1/8",weight:"3/7"},{path:[[0,"1/3"]],lo:"-1/2",hi:0,weight:"4/7"}]},
   {name:"germ_turns_and_width",rows:[{path:[[Z,Q("1/2").s(e)],[Q("1/2"),O.s(e)],[Q("3/2"),e.neg()],[Q("5/2"),O.s(e)]],lo:Z,hi:e.pow(2),weight:1}]},
   {name:"germ_endpoint_band",rows:[{path:[[Z,O.s(e)]],lo:Z,hi:e.m(2),weight:1}]},
   {name:"endpoint_atom_jump",rows:[{path:[[0,1]],lo:0,hi:"1/4",weight:1}]}
  ];
 let physicalChecks=0,pieces=0,quadraticChecks=0;const results=[];
 for(const model of models){
  const entries=model.rows.map((r,i)=>({id:model.name+":"+i,row:T.prepareInterval(r.path,r.lo,r.hi),weight:r.weight})),S=separatorModule.createFanM1Separator(G,T,entries),result=S.separate({keepCells:true});
  const W=entries.reduce((a,b)=>a.a(Q(b.weight)),Z);
  function physical(start){const m=S.route(start);let cost=Z;for(const r of entries){const p=physicalFanScore(G,r.row.path,m,[r.row.lower,r.row.upper]);cost=cost.a(p.cost.m(Q(r.weight)).dby(W));pieces+=p.pieces;}physicalChecks++;return cost;}
  if(!physical(Q(result.start)).eq(Q(result.minimum)))throw Error("fan M1 minimum physical witness mismatch");
  for(const cell of result.cells){
   const a=Q(cell.left),b=Q(cell.right),width=b.s(a),coef=cell.local_coefficients.map(Q),poly=u=>coef[0].a(coef[1].m(u)).a(coef[2].m(u.m(u)));
   for(const u of [Q("1/5"),Q("4/5")]){const c=physical(a.a(width.m(u)));if(!c.eq(poly(u)))throw Error("fan M1 physical polynomial mismatch");quadraticChecks++;}
   for(const endpoint of [a,b])if(physical(endpoint).cmp(Q(result.minimum))<0)throw Error("fan M1 arrangement endpoint missed");
  }
  if(model.name==="endpoint_atom_jump"){
   const last=result.cells.at(-1),atOne=physical(O),coef=last.local_coefficients.map(Q),leftLimit=coef.reduce((a,b)=>a.a(b),Z);
   if(!atOne.eq(1)||!leftLimit.eq(3))throw Error("initial endpoint atom closed trace lost");
  }
  results.push({name:model.name,minimum:result.minimum,start:result.start,cells:result.cell_count,stationary_candidates:result.stationary_candidates,polynomial_checks:result.polynomial_checks,route:result.route});
 }
 return{scope:"Complete raw-fan M1 arrangements, checked by independent continuous translated-path physical integration; no ordered-law violation is inferred from a raw violation.",
  models:results,independent_physical_scores:physicalChecks,independent_affine_translation_pieces:pieces,independent_polynomial_checks:quadraticChecks,arithmetic:G.stats()};
}
async function main(){const[out]=process.argv.slice(2);if(!out)throw Error("usage: node verify_fan_m1_separator.mjs REPORT.json");const r=verifyFanM1Separator();await fs.writeFile(out,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.models.length,"complete families",r.independent_physical_scores,"physical scores",r.independent_polynomial_checks,"polynomial checks");}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
