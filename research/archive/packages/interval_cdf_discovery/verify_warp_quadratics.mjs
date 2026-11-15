#!/usr/bin/env node
import fs from "node:fs";
import {createRequire} from "node:module";
const require=createRequire(import.meta.url);
const E=require("./warp_exact_field_core.cjs");
const {createWarpTools}=require("./warp_capture_features.cjs");
const {createWarpFamilyAuditor}=require("./warp_family_audit.cjs");
const {compileWarpFamilies}=require("./warp_compile_families.cjs");
const {compileLateWarpEdges}=require("./warp_compile_late_edges.cjs");
const {createQuadraticWarpSeparator}=require("./warp_quadratic_separator.cjs");
const args=process.argv.slice(2),rebuild=args.includes("--rebuild"),paths=args.filter(x=>x!=="--rebuild");
if(paths.length<4)throw Error("Supply FIELD FOUR_TENSOR LATE_TENSOR SOLUTION [REPORT] [--rebuild]");
const [data,four,late,sol]=paths.slice(0,4).map(p=>JSON.parse(fs.readFileSync(p,"utf8")));
const W=createWarpTools(E),A=createWarpFamilyAuditor(E),S=createQuadraticWarpSeparator(E),f=new E.ExactField(data),warp=new W.WarpCoordinates(sol.knots),d=warp.validate(sol.increments);
for(const tensor of[four,late])if(JSON.stringify(tensor.knots)!==JSON.stringify(sol.knots))throw Error("knots");
if(rebuild){
 const rebuiltFour=compileWarpFamilies(E,W,A,f,warp),rebuiltLate=compileLateWarpEdges(E,W,f,warp);
 if(JSON.stringify(rebuiltFour.cells)!==JSON.stringify(four.cells))throw Error("four-family tensor mismatch");
 if(JSON.stringify(rebuiltLate.cells)!==JSON.stringify(late.cells))throw Error("late tensor mismatch");
}
const physical=W.remapExactField(f,warp,d),results=[];
for(const tensor of[four,late])for(const r of S.separate(S.decode(tensor),d).families){
 let route,reference;
 if(r.family==="late_negative_m2"){
  const c=tensor.cells[r.cell],p=c.vertices[0].map(E.Q),q=c.vertices[1].map(E.Q),[s,a]=p.map((x,j)=>x.a(q[j].s(x).m(r.parameter)));
  route=[[E.ZERO,a.neg()],[s.a(a).dby(2),s.s(a).dby(2)],[s.a(1),E.Q(-1)],[s.a(3),E.ONE]];
  reference={start:a.neg().str(),firstU:s.str()};
 }else{
  route=r.family==="m1"?A.m1Route(r.start,r.positive):A.fixedRoute(r.start,r.positive);
  reference={start:(r.positive?r.start:r.start.neg()).str(),firstU:r.family==="fixed_one"?"1":null};
 }
 const image=warp.route(route,d),actual=physical.unitRoutePayoff(image);
 if(!actual.eq(r.value))throw Error("independent physical capture "+r.family);
 const features=W.captureFeatures(f,warp,route).coefficients;
 if(features.some((x,i)=>!x.eq(r.coefficients[i])))throw Error("independent feature coefficients");
 results.push({family:r.family,positive:r.positive,cell:r.cell,parameter:r.parameter.str(),reference,minimum:r.value.str(),decimal:r.value.num(),route:image.map(p=>p.map(x=>x.str()))});
}
const report={scope:"Exact complete named-family minima on a strict common warp, not unrestricted lower feasibility.",rebuild,transport_triangles:physical.triangles.length,four_family_cells:four.cells.length,late_edges:late.cells.length,verification:[four.verification,late.verification],families:results};
const text=JSON.stringify(report,null,2)+"\n";if(paths[4])fs.writeFileSync(paths[4],text);process.stdout.write(text);
