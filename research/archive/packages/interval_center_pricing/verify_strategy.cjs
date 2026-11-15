"use strict";
// One independent bank replay followed by the unchanged exact extractor.
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto");
const {verify}=require("./verify_bigint.cjs");
const {readSource,makeStrategy,assertSameStrategy,createEvaluator}=require("../interval_clock_grid/extract_normalized_princess.cjs");
const sha=raw=>crypto.createHash("sha256").update(raw).digest("hex");

function verifyStrategy(fieldFile,strategyFile,options={}){
 const source=readSource(fieldFile),saved=readSource(strategyFile);
 // Bind the executing files before a possibly long search.
 const verifierSha=sha(fs.readFileSync(path.join(__dirname,"verify_bigint.cjs")));
 const extractorSha=sha(fs.readFileSync(path.join(__dirname,"../interval_clock_grid/extract_normalized_princess.cjs")));
 const wrapperSha=sha(fs.readFileSync(__filename));
 const pricing=verify(source.data,{...options,targetUnits:saved.data.verified_lower_units});
 pricing.input_sha256=source.input_sha256;
 pricing.verifier_source_sha256=verifierSha;
 const expected=makeStrategy(source.bytes,pricing,saved.data.interpolation_epsilon);
 assertSameStrategy(saved.data,expected);
 const evaluator=createEvaluator(saved.data);
 return {status:"PASS",scope:"Independent complete-bank BigInt target replay and exact regeneration of the saved continuous Princess law using the unchanged extractor. The fixed-law guarantee includes its positive interpolation-width allowance.",
   n:expected.n,input_sha256:source.input_sha256,strategy_sha256:saved.input_sha256,
   wrapper_source_sha256:wrapperSha,extractor_source_sha256:extractorSha,
   finite_dual_lower:expected.finite_dual_lower,interpolation_epsilon:expected.interpolation_epsilon,
   exact_transfer_loss:expected.exact_transfer_loss,guaranteed_security:expected.guaranteed_security,
   validation:evaluator.validation,pricing};
}

module.exports={verifyStrategy};
if(require.main===module){
 try{
  const args=process.argv.slice(2),[field,strategy]=args;
  if(!field||!strategy)throw Error("usage: node verify_strategy.cjs field.json strategy.json [--progress N]");
  const index=args.indexOf("--progress"),progress=index<0?0:Number(args[index+1]);
  if(!Number.isSafeInteger(progress)||progress<0)throw Error("invalid progress interval");
  process.stdout.write(JSON.stringify(verifyStrategy(field,strategy,{progress}),null,2)+"\n");
 }catch(error){process.stderr.write(error.stack+"\n");process.exitCode=1;}
}
