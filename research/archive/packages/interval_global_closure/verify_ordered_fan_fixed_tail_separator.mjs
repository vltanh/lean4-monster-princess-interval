import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";
import fanModule from "./germ_translation_fan.cjs";
import rawTailModule from "./fan_fixed_tail_separator.cjs";
import separatorModule from "./ordered_fan_fixed_tail_separator.cjs";
import orderedModule from "./ordered_fan_cost.cjs";
/** Independent ordered-quantile first-contact moment integration.
 * CDFs are computed directly from translated intervals, not through the
 * ordered provider. New rank bands are integrated against affine first-hit
 * inverses, rather than integrating survival or using inverse-band caches.
 */
export function physicalOrderedFanScore(G,entries,rawMonster){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,min=(a,b)=>a.cmp(b)<0?a:b,max=(a,b)=>a.cmp(b)>0?a:b,
  unique=xs=>[...new Map(xs.map(Q).map(x=>[x.str(),x])).values()].sort((a,b)=>a.cmp(b)),
  m=rawMonster?.v?rawMonster:new G.PLPath(rawMonster),W=entries.reduce((a,e)=>a.a(Q(e.weight??1)),Z);
 function cdf(t,x,mode="interior"){
  if(x.eq(-1)&&mode==="strict")return Z;if(x.eq(1)&&mode==="closed")return O;
  let ans=Z;
  for(const e of entries){const p=e.row.path,weight=Q(e.weight??1).dby(W);if(weight.eq(0))continue;
   for(const sign of[1,-1]){
    const lo=sign===1?e.row.lower:e.row.upper.neg(),hi=sign===1?e.row.upper:e.row.lower.neg(),
     y=x.s(p.at(t).m(sign)).s(lo).dby(hi.s(lo)),f=max(Z,min(O,y));
    ans=ans.a(weight.m(f).dby(2));
   }
  }return ans;
 }
 let L=cdf(m.t[0],m.x[0],"strict"),H=cdf(m.t[0],m.x[0],"closed"),moment=Z,pieces=0,jumps=0;
 for(let j=0;j<m.v.length;j++){
  const d=m.v[j].eq(1)?1:m.v[j].eq(-1)?-1:0;if(!d)throw Error("physical ordered fixture requires unit Monster");
  const start=m.t[j],end=m.t[j+1],x0=m.x[j],pos=t=>x0.a(t.s(start).m(d)),times=[start,end];
  for(const e of entries)if(Q(e.weight??1).cmp(0)>0){
   const p=e.row.path,base=unique([start,end,...p.t.filter(t=>t.cmp(start)>0&&t.cmp(end)<0)]);
   times.push(...base);
   for(let k=0;k+1<base.length;k++)for(const sign of[1,-1]){
    const a=base[k],b=base[k+1],ya=pos(a).s(p.at(a).m(sign)),yb=pos(b).s(p.at(b).m(sign));if(ya.eq(yb))continue;
    const lo=sign===1?e.row.lower:e.row.upper.neg(),hi=sign===1?e.row.upper:e.row.lower.neg();
    for(const z of[lo,hi])if(z.cmp(min(ya,yb))>0&&z.cmp(max(ya,yb))<0)times.push(a.a(b.s(a).m(z.s(ya)).dby(yb.s(ya))));
   }
  }
  const cuts=unique(times);
  for(let k=0;k+1<cuts.length;k++){
   const a=cuts[k],b=cuts[k+1],fa=cdf(a,pos(a)),fb=cdf(b,pos(b));
   if(fb.s(fa).m(d).cmp(0)<0)throw Error("nonmonotone physical CDF");
   if(d===1){
    if(fa.cmp(H)>0){moment=moment.a(a.m(fa.s(H)));H=fa;jumps++;}
    if(fb.cmp(H)>0){const lo=max(H,fa),hi=fb,t=a.a(b.s(a).m(lo.a(hi).dby(2).s(fa)).dby(fb.s(fa)));moment=moment.a(hi.s(lo).m(t));H=fb;}
   }else{
    if(fa.cmp(L)<0){moment=moment.a(a.m(L.s(fa)));L=fa;jumps++;}
    if(fb.cmp(L)<0){const lo=fb,hi=min(L,fa),t=a.a(b.s(a).m(lo.a(hi).dby(2).s(fa)).dby(fb.s(fa)));moment=moment.a(hi.s(lo).m(t));L=fb;}
   }pieces++;
  }
  const f=cdf(end,m.x[j+1],d===1?"closed":"strict");
  if(d===1&&f.cmp(H)>0){moment=moment.a(end.m(f.s(H)));H=f;jumps++;}
  if(d===-1&&f.cmp(L)<0){moment=moment.a(end.m(L.s(f)));L=f;jumps++;}
 }
 if(!H.s(L).eq(1))throw Error("physical ordered route incomplete");
 return{cost:moment,pieces,jumps};
}


export function verifyOrderedFanFixedTailSeparator(){
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
   S=separatorModule.createOrderedFanFixedTailSeparator(G,fanModule,orderedModule,rawTailModule,entries,tail),result=S.separate({keepCells:true}),
   W=entries.reduce((a,b)=>a.a(Q(b.weight)),Z);
  function physical(start){const p=physicalOrderedFanScore(G,entries,S.route(start));physicalChecks++;pieces+=p.pieces;return p.cost;}
  if(!physical(Q(result.start)).eq(Q(result.minimum)))throw Error("fixed-tail minimum physical witness mismatch");
  for(const cell of result.cells){
   const a=Q(cell.left),b=Q(cell.right),width=b.s(a),coef=cell.local_coefficients.map(Q),poly=u=>coef[0].a(coef[1].m(u)).a(coef[2].m(u.m(u)));
   for(const u of [Q("1/5"),Q("4/5")]){const c=physical(a.a(width.m(u)));if(!c.eq(poly(u)))throw Error("fixed-tail physical polynomial mismatch");polynomialChecks++;}
   for(const endpoint of [a,b]){if(physical(endpoint).cmp(Q(result.minimum))<0)throw Error("fixed-tail arrangement endpoint missed");closedChecks++;}
   if(cell.stationary_start!==null){if(!physical(Q(cell.stationary_start)).eq(S.score(Q(cell.stationary_start))))throw Error("stationary physical score mismatch");stationaryChecks++;}
  }
  results.push({law:law.name,tail:tail.name,minimum:result.minimum,start:result.start,physical_start:Q(result.start).m(tail.firstDirection).str(),domain:S.domain.map(x=>x.str()),cells:result.cell_count,stationary_candidates:result.stationary_candidates,polynomial_checks:result.polynomial_checks,rank_refinement_cuts:result.rank_refinement_cuts,base_cell_count:result.base_cell_count,route:result.route});
 }
 const a=results.find(r=>r.law==="two_outward_waves"&&r.tail==="fixed_multi_turn"),b=results.find(r=>r.tail==="reflected_multi_turn");
 if(a.minimum!==b.minimum||a.start!==b.start)throw Error("fair-reflection fixed-tail symmetry failed");
 return{scope:"Complete continuous initial-start arrangements for each supplied fixed unit tail of an ordered common-quantile fan mixture. Independent continuous rank-band first-contact moment integration verifies every polynomial cell; this is not unrestricted Monster separation.",
  families:results,independent_physical_scores:physicalChecks,independent_affine_CDF_pieces:pieces,independent_polynomial_checks:polynomialChecks,closed_endpoint_checks:closedChecks,stationary_witness_checks:stationaryChecks,arithmetic:G.stats()};
}
async function main(){const[out]=process.argv.slice(2);if(!out)throw Error("usage: node verify_ordered_fan_fixed_tail_separator.mjs REPORT.json");const r=verifyOrderedFanFixedTailSeparator();await fs.writeFile(out,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.families.length,"complete fixed tails",r.independent_physical_scores,"physical scores",r.independent_polynomial_checks,"polynomial checks");}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
