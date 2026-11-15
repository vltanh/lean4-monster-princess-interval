import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";
import germModule from "./germ_response_v8.cjs";

export function verifyFixedTailStarts(fixtures){
 const G=germModule.createGermOracle(createOracle()),Q=G.Q,checks=[];let individual=0,ordered=0,endpoint=0;
 const max=(a,b)=>a.cmp(b)>0?a:b,min=(a,b)=>a.cmp(b)<0?a:b;
 const families=[Q("3/4"),Q(1).a(G.eps.pow(2)),Q("-1/4").a(G.eps)].map(c=>({c,tail:[[c.a(1),Q(-1)],[c.a(3),Q(1)]]}));
 families.push({c:Q("3/4"),tail:[[Q("3/4"),Q(0)],[Q("5/4"),Q("1/2")],[Q("11/4"),Q(-1)],[Q("19/4"),Q(1)]]});
 function route(f,b){return new G.PLPath([[G.ZERO,b],[f.c.s(b).dby(2),f.c.a(b).dby(2)],...f.tail]);}
 for(const f of fixtures){
  const pp=f.paths.map(p=>new G.PLPath(p)),paths=pp.concat(pp.map(p=>new G.PLPath(p.vertices.map(([t,x])=>[t,x.neg()])))),
   weights=f.weights.concat(f.weights),P=G.prepare(paths.map(p=>p.json()),weights);let gaps=0;
  for(const family of families){
   const L=max(Q(-1),family.c.s(family.tail[0][0].m(2))),H=min(G.ONE,min(family.c,Q(2).s(family.c))),
    starts=paths.map(p=>p.x[0]).filter(x=>x.cmp(L)>=0&&x.cmp(H)<=0).concat([L,H]);
   starts.sort((a,b)=>a.cmp(b));const s=starts.filter((x,j)=>!j||!x.eq(starts[j-1]));
   for(let j=0;j+1<s.length;j++){
    const span=s[j+1].s(s[j]),a=s[j].a(span.dby(3)),b=s[j].a(span.m(2).dby(3)),c=s[j+1],ra=route(family,a),rb=route(family,b),rc=route(family,c);
    for(const p of paths){
     const ta=G.rawCapture(ra,p),tb=G.rawCapture(rb,p),tc=G.rawCapture(rc,p);
     if(ta===null||tb===null||tc===null||tb.cmp(ta)>0||tc.cmp(tb)>0)throw Error("fixed-tail gap monotonicity failed");individual+=2;
     if(p.x[0].cmp(a)<0&&!tb.eq(ta))throw Error("behind-start capture was not unchanged");
    }
    const ca=G.sortedCapture(P.paths,P.weights,ra),cb=G.sortedCapture(P.paths,P.weights,rb),cc=G.sortedCapture(P.paths,P.weights,rc);
    if(!ca.complete||!cb.complete||!cc.complete||cb.value.cmp(ca.value)>0||cc.value.cmp(cb.value)>0)throw Error("ordered-gap monotonicity failed");ordered+=2;gaps++;
   }
   for(const b of [L,H]){const m=route(family,b);if(!m.x.some(x=>x.eq(-1))||!m.x.some(x=>x.eq(1)))throw Error("legal boundary lost completion");endpoint++;}
  }
  checks.push({name:f.name,gaps});
 }
 // Exact initial atoms are essential: leaving one toward the right can
 // increase its capture from zero to a positive common-tail time.
 const stationary=new G.PLPath([[0,0]]),f={c:Q("1/2"),tail:[[Q("3/2"),Q(-1)],[Q("7/2"),Q(1)]]},
  at=G.rawCapture(route(f,G.ZERO),stationary),after=G.rawCapture(route(f,G.eps),stationary);
 if(!at.eq(0)||!after.eq("1/2"))throw Error("initial-atom lower-trace fixture");
 return{scope:"Direct chronological segment checks of the fixed-tail start-gap theorem, ordered-law checks, legality boundaries, and the essential exact initial-atom trace.",
  fixtures:checks,pointwise_capture_inequalities:individual,ordered_capture_inequalities:ordered,legal_boundary_routes:endpoint,
  atom_trace:{at:at.str(),right:after.str()},arithmetic:G.stats()};
}
async function main(){const[input,output]=process.argv.slice(2);if(!input||!output)throw Error("usage: node verify_fixed_tail_starts.mjs FIXTURES.json REPORT.json");
 const r=verifyFixedTailStarts(JSON.parse(await fs.readFile(input,"utf8")));await fs.writeFile(output,JSON.stringify(r,null,2)+"\n");
 console.log("PASS",r.pointwise_capture_inequalities,"pointwise inequalities",r.ordered_capture_inequalities,"ordered inequalities",r.legal_boundary_routes,"boundary routes");}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
