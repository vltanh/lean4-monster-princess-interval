import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";
import fanModule from "./germ_translation_fan.cjs";
import separatorModule from "./fan_fixed_tail_separator.cjs";
import {physicalFanScore} from "./verify_translation_fan.mjs";

export function verifyFanFixedTailSeparator(){
 const E=createOracle(),G=germModule.createGermOracle(E),Q=G.Q,Z=G.ZERO,O=G.ONE,e=G.eps,T=fanModule.createTranslationFan(G),
  laws=[
   {name:"stationary_outward",rows:[{path:[[0,"1/2"]],lo:0,hi:"1/10",weight:1}]},
   {name:"moving_symmetric",rows:[{path:[[0,"1/4"],["1/2","3/4"],["5/4",0],["9/4",1]],lo:"-1/8",hi:"1/8",weight:1}]},
   {name:"two_outward_waves",rows:[{path:[[0,"1/4"],["1/2","3/4"],["5/4",0],["9/4",1]],lo:0,hi:"1/4",weight:"2/5"},{path:[[0,"3/4"],["3/4",0],["7/4",1]],lo:0,hi:"1/8",weight:"3/5"}]},
   {name:"subunit_asymmetric",rows:[{path:[[0,"-1/4"],[1,"1/4"],[2,"-1/4"],[4,"3/4"]],lo:"-1/4",hi:"1/8",weight:"3/7"},{path:[[0,"1/3"]],lo:"-1/2",hi:0,weight:"4/7"}]},
   {name:"endpoint_atom",rows:[{path:[[0,1]],lo:0,hi:"1/4",weight:1}]},
   {name:"germ_turns_and_width",rows:[{path:[[Z,Q("1/2").s(e)],[Q("1/2"),O.s(e)],[Q("3/2"),e.neg()],[Q("5/2"),O.s(e)]],lo:Z,hi:e.pow(2),weight:1}]}
  ],
  tails=[
   {name:"fixed_one",firstDirection:1,tail:[[2,-1],[4,1]]},
   {name:"fixed_three_quarters",firstDirection:1,tail:[["7/4",-1],["15/4",1]]},
   {name:"fixed_multi_turn",firstDirection:1,tail:[["1/2","1/4"],[1,"3/4"],["11/4",-1],["19/4",1]]},
   {name:"reflected_multi_turn",firstDirection:-1,tail:[["1/2","-1/4"],[1,"-3/4"],["11/4",1],["19/4",-1]]},
   {name:"germ_turn",firstDirection:1,tail:[[Q(2).a(e.pow(2)),-1],[Q(4).a(e.pow(2)),1]]}
  ];
 const fixtures=[];
 for(const law of laws)for(const ti of law.name==="germ_turns_and_width"?[0,2,4]:[0,1,2]){
  fixtures.push({law,tail:tails[ti]});
 }
 fixtures.push({law:laws[2],tail:tails[3]});
 let physicalChecks=0,pieces=0,polynomialChecks=0,stationaryChecks=0,closedChecks=0;const results=[];
 for(const fixture of fixtures){
  const{law,tail}=fixture,entries=law.rows.map((r,i)=>({id:law.name+":"+i,row:T.prepareInterval(r.path,r.lo,r.hi),weight:r.weight})),
   S=separatorModule.createFanFixedTailSeparator(G,T,entries,tail),result=S.separate({keepCells:true}),
   W=entries.reduce((a,b)=>a.a(Q(b.weight)),Z);
  function physical(start){const m=S.route(start);let cost=Z;for(const r of entries){const p=physicalFanScore(G,r.row.path,m,[r.row.lower,r.row.upper]);cost=cost.a(p.cost.m(Q(r.weight)).dby(W));pieces+=p.pieces;}physicalChecks++;return cost;}
  if(!physical(Q(result.start)).eq(Q(result.minimum)))throw Error("fixed-tail minimum physical witness mismatch");
  for(const cell of result.cells){
   const a=Q(cell.left),b=Q(cell.right),width=b.s(a),coef=cell.local_coefficients.map(Q),poly=u=>coef[0].a(coef[1].m(u)).a(coef[2].m(u.m(u)));
   for(const u of [Q("1/5"),Q("4/5")]){const c=physical(a.a(width.m(u)));if(!c.eq(poly(u)))throw Error("fixed-tail physical polynomial mismatch");polynomialChecks++;}
   for(const endpoint of [a,b]){if(physical(endpoint).cmp(Q(result.minimum))<0)throw Error("fixed-tail arrangement endpoint missed");closedChecks++;}
   if(cell.stationary_start!==null){if(!physical(Q(cell.stationary_start)).eq(S.score(Q(cell.stationary_start))))throw Error("stationary physical score mismatch");stationaryChecks++;}
  }
  results.push({law:law.name,tail:tail.name,minimum:result.minimum,start:result.start,physical_start:Q(result.start).m(tail.firstDirection).str(),domain:S.domain.map(x=>x.str()),cells:result.cell_count,stationary_candidates:result.stationary_candidates,polynomial_checks:result.polynomial_checks,route:result.route});
 }
 const a=results.find(r=>r.law==="two_outward_waves"&&r.tail==="fixed_multi_turn"),b=results.find(r=>r.tail==="reflected_multi_turn");
 if(a.minimum!==b.minimum||a.start!==b.start)throw Error("fair-reflection fixed-tail symmetry failed");
 return{scope:"Complete continuous initial-start arrangements for each supplied fixed unit tail of a raw fan mixture. Independent actual translated/clipped first-contact integrations verify every polynomial cell; this is not unrestricted Monster separation.",
  families:results,independent_physical_scores:physicalChecks,independent_affine_translation_pieces:pieces,independent_polynomial_checks:polynomialChecks,closed_endpoint_checks:closedChecks,stationary_witness_checks:stationaryChecks,arithmetic:G.stats()};
}
async function main(){const[out]=process.argv.slice(2);if(!out)throw Error("usage: node verify_fan_fixed_tail_separator.mjs REPORT.json");const r=verifyFanFixedTailSeparator();await fs.writeFile(out,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.families.length,"complete fixed tails",r.independent_physical_scores,"physical scores",r.independent_polynomial_checks,"polynomial checks");}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
