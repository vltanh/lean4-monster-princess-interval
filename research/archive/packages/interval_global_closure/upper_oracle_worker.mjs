#!/usr/bin/env node
/** Active-support upper separation and NEW frozen physical responses.
 * Existing physical master rows are never accepted or re-realized here.
 */
import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import {createRequire} from "node:module";
import {pathToFileURL,fileURLToPath} from "node:url";
import readline from "node:readline";
const require=createRequire(import.meta.url);
const HERE=path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_DEPS={
 atomic:path.resolve(HERE,"../interval_turn_density/atomic_survival_v8.cjs"),
 germAtomic:path.join(HERE,"germ_atomic_survival.cjs"),
 germ:path.join(HERE,"germ_response_v8.cjs"),
 realizer:path.join(HERE,"germ_generalized_realizer.cjs"),
 frozen:path.join(HERE,"germ_frozen_law_tools.cjs"),
 exact:path.resolve(HERE,"../interval_cdf_discovery/finite_quantile_response.mjs"),
 collapsed:path.join(HERE,"collapsed_companion.cjs")
};
const hash=x=>crypto.createHash("sha256").update(typeof x==="string"?x:JSON.stringify(x)).digest("hex");
export async function createUpperWorker(dependencies={}){
 const deps={...DEFAULT_DEPS,...dependencies},E=require(deps.atomic),
  Exact=await import(pathToFileURL(deps.exact).href),
  GM=require(deps.germ),AM=require(deps.germAtomic),
  RM=require(deps.realizer),FM=require(deps.frozen),CM=require(deps.collapsed);
 return async function solveUpper(input,options={}){
  const started=Date.now(),opts={...input.options,...options},
   G=GM.createGermOracle(Exact.createOracle()),A=AM.createGermAtomic(E,G),
   R=RM.createGeneralizedRealizer(G),F=FM.createFrozenLawTools(G),C=CM.createCollapsedCompanion(E,G),
   Q=G.Q,Z=G.ZERO,O=G.ONE;
  const log=opts.progress?x=>console.error("[upper-worker] "+x):()=>{};
  function clean(points){
   const out=[];
   for(const point of points){
    const p=point.map(Q),last=out.at(-1);
    if(last&&p[0].eq(last[0])&&p[1].eq(last[1]))continue;
    while(out.length>1){
     const a=out[out.length-2],b=out.at(-1);
     if(a[0].eq(b[0])&&b[0].eq(p[0])||a[1].eq(b[1])&&b[1].eq(p[1]))out.pop();else break;
    }
    out.push(p);
   }
   return out.map(row=>row.map(x=>x.str()));
  }
  function normalizeAtom(atom,index){
   let points;
   if(atom.exact_light)points=atom.exact_light;
   else if(atom.exact_path||atom.route||Array.isArray(atom)){
    const pp=atom.exact_path||atom.route||atom;
    points=pp.map(([t,x])=>{t=Q(t);x=Q(x);return[t.a(x),t.s(x)];});
   }else if(atom.kind==="PATH"&&atom.parameters){
    if(atom.parameters.length%2)throw Error("odd PATH parameter count");
    points=[];for(let j=0;j<atom.parameters.length;j+=2)points.push([atom.parameters[j],atom.parameters[j+1]]);
   }else if(atom.light)points=atom.light;
   else{
    const kind=atom.kind===1?"M1":atom.kind===2?"M2":atom.kind,
     ps=(atom.parameters||[]).map(Q),a=ps[0]??Q(atom.start??atom.a??atom.z);
    if(kind==="M1")points=[[a,a.neg()],[Q(2).s(a),a.neg()],[Q(2).s(a),Q(4).s(a)]];
    else if(kind==="M2"){
     const s=ps[1]??Q(atom.turn??atom.s??1);
     points=[[a,a.neg()],[s,a.neg()],[s,s.a(2)],[s.a(4),s.a(2)]];
    }else if(kind==="M3"){
     const s=ps[1]??Q(atom.first_turn??atom.s),t=ps[2]??Q(atom.second_turn??atom.t);
     points=[[a,a.neg()],[s,a.neg()],[s,t],[t.a(2),t],[t.a(2),t.a(4)]];
    }else if(["I","I1","E","INWARD"].includes(kind)){
     const v=ps[1]??Q(atom.v),s=kind==="E"?v.a(2):kind==="I1"?O:ps[2]??Q(atom.s);
     points=[[a,a.neg()],[a,v],[s,v],[s,s.a(2)],[s.a(4),s.a(2)]];
    }else throw Error("unsupported Monster format at "+index+": "+String(atom.kind));
   }
   return{exact_light:clean(points),source_index:index,source_id:atom.id??index};
  }
  const inputAtoms=input.atoms||input.bank?.atoms||input.bank,
   rawWeights=input.weights||input.monster_weights;
  if(!Array.isArray(inputAtoms)||!Array.isArray(rawWeights)||inputAtoms.length!==rawWeights.length)throw Error("atoms/weights dimensions");
  const parsed=rawWeights.map((x,j)=>{
   if(typeof x==="number"&&!Number.isFinite(x))throw Error("nonfinite weight "+j);
   const q=Q(x);if(q.p.length!==1||q.q.length!==1)throw Error("worker probabilities must be constants");
   if(q.cmp(0)<0)throw Error("negative probability "+j);
   return q;
  });
  let weightTotal=Z;for(const w of parsed)weightTotal=weightTotal.a(w);
  if(weightTotal.cmp(0)<=0)throw Error("empty probability law");
  const weightError=Math.abs(weightTotal.num()-1);
  if(weightError>(opts.normalizationTolerance??1e-8)&&!opts.allowRenormalization)throw Error("weights are not numerically normalized");
  const exactWeights=parsed.map(w=>w.dby(weightTotal)),numericWeights=exactWeights.map(w=>w.num()),
   activeIndices=exactWeights.map((w,j)=>w.cmp(0)>0?j:-1).filter(j=>j>=0),
   atoms=inputAtoms.map(normalizeAtom),activeAtoms=activeIndices.map(j=>atoms[j]),
   activeExact=activeIndices.map(j=>exactWeights[j]),activeNumeric=activeIndices.map(j=>numericWeights[j]);
  const lawHash=hash({atoms,weights:exactWeights.map(x=>x.str())});
  log("compiling "+activeAtoms.length+" positive atoms out of "+atoms.length);
  const model=new A.Model(activeAtoms),compiled=Date.now();
  let cut,exactCut=null;
  if(opts.exactCut){
   exactCut=A.integerLimitCut(model,activeExact);
   cut={value:exactCut.decimal,dualValue:exactCut.decimal,labels:exactCut.labels,maxlabels:exactCut.maximum_labels,
    thresholdNodes:model.N,auxiliaryNodes:exactCut.graph_nodes-model.N-2,rewards:model.defs.length};
  }else cut=model.solve(activeNumeric,opts.tolerance??2e-13,!!opts.retainFace);
  const solved=Date.now(),queryV=model.vQ.map(x=>x.toString()),baseLevels=model.baseQ.map(x=>x.toString()),
   profiles=opts.profiles||[
    {profile:"minimum",fill:"avoided",strictMode:"clip"},
    {profile:"maximum",fill:"avoided",strictMode:"clip"},
    {profile:"minimum",fill:"common-wave",strictMode:"clip"},
    {profile:"maximum",fill:"common-wave",strictMode:"clip"}
   ],monsters=atoms.map(a=>F.prepareMonster(a)),rows=[],seen=new Map(),duplicates=[],
   contexts=[{kind:"original-germ",model,cut,queryV,baseLevels,weights:activeExact,
    monsters:activeIndices.map(j=>monsters[j]),lawHash}];
  const companionStart=Date.now();let companion=null;
  if(opts.collapsed!==false||opts.companionRows){
   const law=C.collapseLaw(activeAtoms,activeExact);
   for(const atom of law.atoms)atom.source_full_indices=atom.source_indices.map(j=>activeIndices[j]);
   const response=C.standardResponse(law,{exact:!!opts.exactCollapsed,verifyFlow:true,
     retainFace:!!opts.retainFace,retainModel:!!opts.companionRows});
   if(opts.companionRows){
    const cm=response.model,cc=response.result;
    contexts.push({kind:"collapsed-ordinary",model:cm,cut:cc,
     queryV:cm.vQ.map(x=>x.toString()),baseLevels:cm.baseQ.map(x=>x.toString()),
     weights:law.weights.map(Q),monsters:law.atoms.map(a=>F.prepareMonster(a)),
     lawHash:hash({atoms:law.atoms,weights:law.weights})});
    delete response.model;
   }
   companion={law,response};log("separate collapsed response "+response.value);
  }
  const companionSeconds=(Date.now()-companionStart)/1000,rowsStarted=Date.now();
  function compressPhysical(p){
   const out=[p.vertices[0]];
   for(let j=0;j<p.v.length;j++){
    if(j&&p.v[j].eq(p.v[j-1]))out[out.length-1]=p.vertices[j+1];
    else out.push(p.vertices[j+1]);
   }
   if(out.length>1&&out.at(-1)[1].eq(out.at(-2)[1]))out.pop();
   return F.preparePath(out);
  }
  for(const context of contexts){
   const scale=R.chooseScale(context.queryV,context.baseLevels);
   for(const spec of profiles){
    const labels=spec.profile==="minimum"?context.cut.labels:spec.profile==="maximum"?context.cut.maxlabels:null;
    if(!labels)throw Error("unknown cut profile");
    const optsR={scale,fill:spec.fill||"avoided",strictMode:spec.strictMode||"clip",auditTraces:true};
    if(spec.waveOffset!==undefined)optsR.waveOffset=spec.waveOffset;
    const realization=R.realize(context.queryV,context.baseLevels,labels,optsR),p=compressPhysical(realization.path),
     vertices=p.json(),id="physical_"+hash(vertices),existing=seen.get(id);
    if(existing!==undefined){duplicates.push({witness_law:context.kind,spec,row:rows[existing].id});continue;}
    const rowStarted=Date.now();
    let weighted=Z,weightedLimit=G.ZERO.limit(),abstractLimit=G.ZERO.limit();
    const abstract=context.model.rowExact(labels),payoffs=[],exactPayoffs=[],captureGerms=[],activeHits=[];
    for(let j=0;j<monsters.length;j++){
     const c=F.pairScore(p,monsters[j],{fullCost:true});
     if(!c.complete)throw Error("complete Monster failed to capture row "+id+" atom "+j);
     payoffs.push(c.decimal);exactPayoffs.push(c.limit);
     if(opts.includeCaptureGerms!==false)captureGerms.push(c.exact_cost);
     if(exactWeights[j].cmp(0)>0){
      weighted=weighted.a(Q(c.exact_cost).m(exactWeights[j]));
      weightedLimit=weightedLimit.a(Q(c.limit).limit().m(exactWeights[j].limit()));
      activeHits.push({atom:j,plus:c.plus,minus:c.minus});
     }
    }
    let witnessWeighted=context.kind==="original-germ"?weighted:Z;
    if(context.kind!=="original-germ")for(let j=0;j<context.monsters.length;j++){
     const c=F.pairScore(p,context.monsters[j],{fullCost:true});
     if(!c.complete)throw Error("companion did not capture its witness");
     witnessWeighted=witnessWeighted.a(Q(c.exact_cost).m(context.weights[j]));
    }
    for(let j=0;j<context.weights.length;j++)abstractLimit=abstractLimit.a(Q(abstract[j].toString()).limit().m(context.weights[j].limit()));
    if(!weighted.limit().eq(weightedLimit))throw Error("full-germ/limit weighted recapture mismatch");
    const witnessLimit=witnessWeighted.limit(),delta=witnessLimit.s(abstractLimit),
     numericDelta=witnessLimit.num()-context.cut.value,allowed=opts.recaptureTolerance??3e-8;
    if(delta.num()>allowed||numericDelta>allowed||(spec.fill!=="early"&&(Math.abs(delta.num())>allowed||Math.abs(numericDelta)>allowed)))
     throw Error("physical response/own cut disagreement: "+delta.str()+" / "+numericDelta);
    if(weightedLimit.num()>cut.value+allowed)throw Error("legal companion witness exceeds original unrestricted cut");
    const validation={law:context.kind,exact_germ:witnessWeighted.str(),exact_limit:witnessLimit.str(),
     decimal:witnessLimit.num(),abstract_profile_limit:abstractLimit.str(),difference:delta.str(),
     exact_equality:delta.eq(0),numeric_cut_difference:numericDelta,
     maximizing_limit_witness:Math.abs(delta.num())<=allowed};
    const row={
     id,path:vertices,provenance:{source:"new active-support upper cut",original_law_hash:lawHash,
      witness_law:context.kind,witness_law_hash:context.lawHash,...spec,scale,
      query_universe:"witness-law positive Monster support only",physical_rows_are_immutable:true},
     payoffs,exact_payoffs:exactPayoffs,
     ...(opts.includeCaptureGerms!==false?{capture_germs:captureGerms}:{}),
     active_first_capture:activeHits,
     weighted_recapture:{score_scope:"original full bank",exact_germ:weighted.str(),
      exact_limit:weightedLimit.str(),decimal:weightedLimit.num(),
      ...(context.kind==="original-germ"?{abstract_profile_limit:abstractLimit.str(),
       difference:delta.str(),exact_equality:delta.eq(0),numeric_cut_difference:numericDelta,
       maximizing_limit_witness:validation.maximizing_limit_witness}:{})},
     witness_validation:validation,
     realization:{raw_vertices:realization.path.vertices.length,compressed_vertices:vertices.length,
      zero_side_changes:realization.zeroChanges,isolated_changes:realization.changes},
     seconds:(Date.now()-rowStarted)/1000
    };
    rows.push(row);seen.set(id,rows.length-1);
    log(context.kind+" "+spec.profile+"/"+spec.fill+" path "+vertices.length+" vertices; original-bank score "+weightedLimit.num());
   }
  }
  return{
   scope:opts.exactCut?"Exact limiting unrestricted upper response; separately frozen physical witnesses.":"Numerical unrestricted limiting upper separation; frozen physical witness payoffs are exact.",
   complete:true,law_hash:lawHash,bank_size:atoms.length,active_indices:activeIndices,
   normalization:{input_sum:weightTotal.str(),normalization_applied:!weightTotal.eq(1),
    normalized_exact_weights:exactWeights.map(w=>w.str()),no_positive_weight_was_clipped:true},
   response:{value:cut.value,dual_value:cut.dualValue,exact_value:exactCut?.value??null,
    query_v:queryV,base_levels:baseLevels,minimum_labels:cut.labels,maximum_labels:cut.maxlabels,
    threshold_nodes:model.N,auxiliary_nodes:cut.auxiliaryNodes,rewards:cut.rewards,
    numerical_tolerance:opts.exactCut?null:opts.tolerance??2e-13,
    ...(opts.retainFace?{face:cut.face}:{}),...(exactCut?{integer_certificate:exactCut}:{})},
   rows,duplicate_realizations:duplicates,collapsed_companion:companion,
   arithmetic:G.stats(),capture_cache:F.stats(),
   seconds:{compile:(compiled-started)/1000,cut:(solved-compiled)/1000,
    realize_and_score:(Date.now()-rowsStarted)/1000,collapsed:companionSeconds,total:(Date.now()-started)/1000},
   dependencies:deps
  };
 };
}
export async function solveUpper(input,options={}){
 const worker=await createUpperWorker(options.dependencies||input.dependencies||{});
 return worker(input,options);
}
async function readInput(file){
 const data=JSON.parse(await fs.readFile(file,"utf8")),base=path.dirname(path.resolve(file));
 if(data.bank_file){const bank=JSON.parse(await fs.readFile(path.resolve(base,data.bank_file),"utf8"));data.atoms=Array.isArray(bank)?bank:bank.atoms;}
 if(data.weights_file){const w=JSON.parse(await fs.readFile(path.resolve(base,data.weights_file),"utf8"));data.weights=Array.isArray(w)?w:w.monster_weights||w.weights;}
 return data;
}
export async function runCli(){
 const args=process.argv.slice(2);
 if(args[0]==="--jsonl"){
  const worker=await createUpperWorker();
  for await(const line of readline.createInterface({input:process.stdin,crlfDelay:Infinity})){
   if(!line.trim())continue;
   try{const request=JSON.parse(line);console.log(JSON.stringify(await (request.dependencies?solveUpper(request):worker(request))));}
   catch(e){console.log(JSON.stringify({complete:false,error:String(e.stack||e)}));}
  }
  return;
 }
 if(args.length!==2)throw Error("usage: node upper_oracle_worker.mjs INPUT.json OUTPUT.json (or --jsonl)");
 const input=await readInput(args[0]),output=await solveUpper(input,{progress:true});
 await fs.writeFile(args[1],JSON.stringify(output)+"\n");
 console.log(JSON.stringify({output:args[1],response:output.response.value,
  collapsed:output.collapsed_companion?.response.value,physical_rows:output.rows.length,seconds:output.seconds}));
}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href)
 runCli().catch(e=>{console.error(e.stack||e);process.exitCode=1;});
