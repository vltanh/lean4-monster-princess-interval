import fs from "node:fs/promises";
import {pathToFileURL} from "node:url";
import germModule from "./germ_response_v8.cjs";
import generalizedModule from "./germ_generalized_realizer.cjs";
import clippedModule from "./germ_clipped_realizer.cjs";
import {createOracle} from "../interval_cdf_discovery/finite_quantile_response.mjs";

export function verifyGeneralizedRealizer(fixtures,{checkpoint=null}={}){
 const E=createOracle(),G=germModule.createGermOracle(E),R=generalizedModule.createGeneralizedRealizer(G),q=G.Q,e=G.eps;
 const synthetic=[
  {name:"constant_bounce",v:["-1","-1/2","1/2","5/2"],b:["0","1/2","5/2","9/2"],labels:[1,3,6,9],power:1},
  {name:"epsilon2_query_gap",v:["-1","-1/2","1/2",q("1/2").a(e.pow(2)).str(),q("5/2").a(e.pow(2)).str()],b:["0","1/2",q("1/2").a(e.pow(2)).str(),q("5/2").a(e.pow(2)).str(),q("9/2").a(e.pow(2)).str()],labels:[1,3,6,9,12],power:3},
  {name:"equal_limit_not_equal_germ",v:["-1","-1/2","1/2","5/2"],b:["0",q("1/2").s(e.pow(2)).str(),"5/2","9/2"],labels:[1,3,6,9],power:3},
  {name:"rational_function_gap",v:["-1","-1/2","1/2",q("1/2").a(e.pow(2).dby(e.a(1))).str(),q("5/2").a(e.pow(2).dby(e.a(1))).str()],b:["0","1/2",q("1/2").a(e.pow(2).dby(e.a(1))).str(),q("5/2").a(e.pow(2).dby(e.a(1))).str(),q("9/2").a(e.pow(2).dby(e.a(1))).str()],labels:[1,3,6,9,12],power:3}
 ];
 const geometry=[];
 for(const f of synthetic)for(const fill of ["late","early","avoided","common-wave"])for(const strictMode of ["none","affine","clip"]){
  const d=R.realize(f.v,f.b,f.labels,{fill,strictMode});
  if(d.scale.power!==f.power)throw Error("wrong subordinate order");
  if(f.name==="equal_limit_not_equal_germ"&&d.changes.some(x=>x.query===2))throw Error("equal limit collapsed");
  if(strictMode==="clip"&&f.name!=="rational_function_gap"&&d.path.vertices.some(p=>p.some(x=>x.q.length!==1)))throw Error("polynomial closure");
  geometry.push({name:f.name,fill,strictMode,power:d.scale.power,vertices:d.path.t.length,avoided:d.changes.length,zeroChanges:d.zeroChanges.length});
 }
 const captures=[];
 for(const f of fixtures)for(const labelName of ["labels","maximum_labels"])for(const strictMode of ["affine","clip"]){
  const d=R.realize(f.query_v,f.base_levels,f[labelName],{fill:"avoided",strictMode}),p=d.path,
   neg=new G.PLPath(p.vertices.map(([t,x])=>[t,x.neg()]));
  let value=G.ZERO;
  const atomScores=f.atoms.map((a,j)=>{
   const m=new G.PLPath(a.exact_light.map(([uu,vv])=>{const u=q(uu),v=q(vv);return[u.a(v).dby(2),u.s(v).dby(2)];})),
    left=G.rawCapture(m,p),right=G.rawCapture(m,neg);
   if(left===null||right===null)throw Error("incomplete physical capture");
   const c=left.a(right).dby(2);value=value.a(c.m(q(f.nums[j]).dby(f.den)));return c.str();
  });
  if(!value.limit().eq(q(f.result.value).limit()))throw Error("cut/physical limit mismatch");
  captures.push({name:f.name,labelName,strictMode,power:d.scale.power,vertices:p.t.length,score:value.str(),limit:value.limit().str(),atom_scores:atomScores,zeroChanges:d.zeroChanges.length,polynomial:p.vertices.every(p=>p.every(x=>x.q.length===1))});
 }
 const compatibility=[];
 if(checkpoint){
  const C=clippedModule.createClippedRealizer(G),levels=checkpoint.event_labels.filter((_,j)=>j%3===0).map(x=>x[0]),
   scale=R.chooseScale(checkpoint.query_v,levels);
  for(const row of [0,79,85,158]){
   const labels=checkpoint.princess_mixture[row].labels,
    a=C.realize(checkpoint.query_v,levels,labels),
    b=R.realize(checkpoint.query_v,levels,labels,{scale,fill:"avoided",strictMode:"clip"});
   if(JSON.stringify(a.path.json())!==JSON.stringify(b.path.json()))throw Error("constant-geometry compatibility");
   compatibility.push({row,vertices:b.path.t.length,power:scale.power});
  }
 }
 return{scope:"Legal subordinate realizations and independently recaptured upper-germ witnesses; no lower feasibility assertion.",
  geometry,captures,compatibility,arithmetic:G.stats()};
}
async function main(){
 const[fixtures,output,checkpoint]=process.argv.slice(2);
 if(!fixtures||!output)throw Error("usage: node verify_generalized_realizer.mjs germ_atomic_fixture_labels.json REPORT.json [efficient_checkpoint.json]");
 const d=JSON.parse(await fs.readFile(fixtures,"utf8")),p=checkpoint?JSON.parse(await fs.readFile(checkpoint,"utf8")):null,
  r=verifyGeneralizedRealizer(d,{checkpoint:p});
 await fs.writeFile(output,JSON.stringify(r,null,2)+"\n");console.log("PASS",r.geometry.length,"geometry cases",r.captures.length,"physical recaptures",r.compatibility.length,"compatibility cases");
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
