import {createMixedScorer} from "./mixed_cdf_payoff.mjs";
import fs from "node:fs/promises";
const L=createMixedScorer(),fixtures=JSON.parse(await fs.readFile(new URL("./snapshots/finite_quantile_response_inputs.json",import.meta.url),"utf8"));
const field=JSON.parse(await fs.readFile(process.argv[3]||new URL("./snapshots/endpoint_joint_i1_field.json",import.meta.url),"utf8"));
if(!process.argv[2])throw Error("usage: node verify_mixed_cdf_payoff.mjs MIXTURE.json [FIELD.json]");
const mix=JSON.parse(await fs.readFile(process.argv[2],"utf8")),expected=JSON.parse(await fs.readFile(new URL("./snapshots/mixed_cdf_round41_attack.json",import.meta.url),"utf8"));
let finiteChecks=0,fieldChecks=0;
for(const f of [...fixtures.archived.map(x=>x.data),...fixtures.arbitrary]){
 const s=new L.CaptureSearch(f.paths,f.weights,{mode:"sorted"});while(!s.runSlice()){}
 const result=s.result(),got=new L.MixedFieldScorer(null,0,f.paths,f.weights).score(result.route);
 if(!got.complete||!L.Q(got.value).eq(result.value))throw Error("pure-finite crosscheck");finiteChecks++;
}
const pure=new L.MixedFieldScorer(field,1);
for(const a0 of ["0","1/32","1/8","3/5","23/32","255/256","1"]){
 const a=L.Q(a0),routes=[
 [[0,a],[L.ONE.s(a),1],[L.Q(3).s(a),-1]],
 [[0,a.neg()],[L.ONE.a(a),1],[L.Q(3).a(a),-1]],
 [[0,a],[L.ONE.s(a).dby(2),L.ONE.a(a).dby(2)],[2,-1],[4,1]],
 [[0,a.neg()],[L.ONE.a(a).dby(2),L.ONE.s(a).dby(2)],[2,-1],[4,1]]
 ];
 for(const route of routes){const v=pure.score(route),w=pure.field.unitRoutePayoff(route);if(!v.complete||!L.Q(v.value).eq(w))throw Error("pure-field crosscheck");fieldChecks++;}
}
if(mix.continuous.length!==1)throw Error("continuous identity");
const paths=[],weights=[];let mass=L.Q(mix.continuous[0].weight);
for(const p of mix.paths){mass=mass.a(p.weight);paths.push(p.path,p.path.map(([t,x])=>[t,L.Q(x).neg().str()]));weights.push(p.weight,p.weight);}
if(!mass.eq(1))throw Error("mass normalization");
const scorer=new L.MixedFieldScorer(field,mix.continuous[0].weight,paths,weights),route=[[0,"3/5"],["2/5",1],["12/5",-1]],score=scorer.score(route),moment=scorer.positiveM1Moment("3/5");
const wanted=expected.routes.find(r=>r.name==="positiveM1_3_5").value;
if(!score.complete||!L.Q(score.value).eq(moment)||!moment.eq(wanted)||moment.cmp("7117/5000")>=0)throw Error("mixed M1 attack");
console.log(JSON.stringify({finiteChecks,fieldChecks,independentMixedMoment:true,exactThreshold:"7117/5000",attack:score},null,2));
