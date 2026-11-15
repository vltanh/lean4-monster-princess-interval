import fs from "node:fs/promises";
import {createHash} from "node:crypto";
import {pathToFileURL} from "node:url";
import {createFrozenSeparator} from "./separate_frozen_law.mjs";
import exactModule from "./germ_translation_fan.cjs";
import floatModule from "./translation_fan_float.cjs";

const sha=s=>createHash("sha256").update(s).digest("hex");
// Dividing two separately rounded huge BigInts can reverse nearby rationals.
// Round the rational itself to a 53-bit significand, with ties to even.
export function rationalDouble(r){
 let n=r.n,d=r.d;if(n===0n)return 0;const sign=n<0n?-1:1;if(n<0n)n=-n;
 let e=n.toString(2).length-d.toString(2).length;
 if(e>=0?(n<(d<<BigInt(e))):((n<<BigInt(-e))<d))e--;
 const shift=52-e,num=shift>=0?n<<BigInt(shift):n,den=shift>=0?d:d<<BigInt(-shift);
 let q=num/den;const rem=num%den;if(2n*rem>den||2n*rem===den&&(q&1n))q++;
 return sign*Number(q)*2**(e-52);
}
export function limitingProfile(p){
 const out=[];
 for(const vertex of p.vertices){
  const [t,x]=vertex.map(q=>q.limit()),last=out.at(-1);
  if(last&&last[0].eq(t)){if(!last[1].eq(x))throw Error("discontinuous collapsed Princess");continue;}
  out.push([t,x]);
  while(out.length>=3){const n=out.length,[a,u]=out[n-3],[b,v]=out[n-2],[c,w]=out[n-1];
   if(v.s(u).m(c.s(b)).eq(w.s(v).m(b.s(a))))out.splice(n-2,1);else break;
  }
 }
 return{exact:out.map(v=>v.map(q=>q.str())),numeric:out.map(v=>v.map(rationalDouble))};
}
export function limitingMonster(F,raw,id=null){
 const p=F.prepareMonster(raw).path;
 const directions=p.v.map(v=>{if(v.eq(1))return 1;if(v.eq(-1))return -1;throw Error("nonunit Monster in floating fan bank");});
 return{id,route:p.vertices.map(v=>v.map(q=>rationalDouble(q.limit()))),directions,
  endpoint_flags:p.x.map(x=>x.eq(1)?1:x.eq(-1)?-1:0),
  actual_route_sha256:sha(JSON.stringify(p.json()))};
}
export function exportFloatFans(rows,bank,{trial=null}={}){
 const worker=createFrozenSeparator(rows),{G,F,paths}=worker,profiles=[],profileIndex=new Map(),profileExact=[],
  rowData=rows.map((r,i)=>{const p=limitingProfile(paths[i]),key=JSON.stringify(p.exact);let index=profileIndex.get(key);
   if(index===undefined){index=profiles.length;profileIndex.set(key,index);profiles.push(p.numeric);profileExact.push(p.exact);}
   return{id:r.id,profile:index,base_path_sha256:sha(JSON.stringify(paths[i].json())),provenance:r.provenance??null};}),
  monsters=bank.map((m,i)=>limitingMonster(F,m,m.id??i)),packet={
   scope:"Double discovery evaluator for fixed positive rational fan widths. Princess profiles are exact collapsed limits; Monster endpoint flags and directions are retained from actual physical germs. This is not an exact payoff certificate.",
   width_policy:"delta must be a fixed nonzero real number, not a vanishing germ. Every chosen fan remains an immutable row.",
   rows:rowData,profiles,profile_exact_vertices:profileExact,monsters},V=floatModule.createFloatFanEvaluator(packet),T=exactModule.createTranslationFan(G);
 let checks=0,maxError=0,worst=null;
 if(trial){
  if(JSON.stringify(trial.row_ids)!==JSON.stringify(rows.map(r=>r.id)))throw Error("trial row identity mismatch");
  for(const experiment of trial.experiments){const d=G.Q(experiment.delta);if(!d.eq(G.Q(d.limit().str()))||d.cmp(0)<=0)continue;
   const delta=d.limit().num();
   for(const score of experiment.scores){const m=limitingMonster(F,score.route,score.id);
    for(let i=0;i<rows.length;i++){const actual=V.score(i,m,delta),expected=G.Q(score.pure_exact_costs[i]).limit().num(),err=Math.abs(actual-expected);checks++;
     if(err>maxError){maxError=err;worst={row:rows[i].id,width:experiment.width_id,monster:score.id,actual,expected,error:err};}
     if(err>5e-10)throw Error("floating fan crosscheck failed: "+JSON.stringify(worst));
    }
   }
  }
 }
 // A limiting turn at +1 is NOT an endpoint hit if its germ stays inside.
 // The clipped Princess endpoint atom then survives until the final sweep.
 const e=G.eps,Q=G.Q,p=new G.PLPath([[0,1]]),near=[[0,0],[G.ONE.s(e),G.ONE.s(e)],[Q(3).s(e.m(2)),-1],[Q(5).s(e.m(2)),1]],
  m=limitingMonster(F,near,"endpoint-flag-fixture"),delta=Q("1/64"),row=T.prepare(p,delta),exact=T.score(row,near),
  fp=floatModule.createFloatFanPath(limitingProfile(p).numeric),correct=floatModule.scoreFloatTranslationFan(fp,m,delta.limit().num()),
  naive={...m,endpoint_flags:m.route.map(v=>v[1]===1?1:v[1]===-1?-1:0)},wrong=floatModule.scoreFloatTranslationFan(fp,naive,delta.limit().num());
 if(Math.abs(correct-Q(exact.exact_cost).limit().num())>1e-12||Math.abs(correct-wrong-1)>1e-12)throw Error("endpoint flag regression");
 packet.verification={exact_trial_comparisons:checks,max_absolute_error:maxError,worst,
  endpoint_flag_fixture:{actual_germ_route:F.prepareMonster(near).route,exact_limit:exact.limit,retained_flag_score:correct,naive_collapsed_endpoint_score:wrong,difference:correct-wrong},
  distinct_profiles:profiles.length,original_rows:rows.length,profile_vertices:profiles.reduce((s,p)=>s+p.length,0),monster_count:monsters.length,arithmetic:G.stats()};
 return packet;
}
async function main(){
 const[rowsFile,bankFile,out,trialFile]=process.argv.slice(2);if(!out)throw Error("usage: node export_translation_fan_float.mjs ROWS BANK OUTPUT.json [EXACT_TRIAL.json]");
 const rt=await fs.readFile(rowsFile,"utf8"),bt=await fs.readFile(bankFile,"utf8"),trial=trialFile?JSON.parse(await fs.readFile(trialFile,"utf8")):null,
  p=exportFloatFans(JSON.parse(rt),JSON.parse(bt),{trial});p.inputs={rows_sha256:sha(rt),bank_sha256:sha(bt)};
 await fs.writeFile(out,JSON.stringify(p,null,2)+"\n");console.log(JSON.stringify(p.verification));
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href)await main();
