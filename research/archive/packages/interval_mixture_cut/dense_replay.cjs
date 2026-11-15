"use strict";
// Independent full-grid reconstruction of an already rational sparse law.
// Physical probabilities and paths are copied exactly; no new rounding occurs.
const fs=require("node:fs"),crypto=require("node:crypto");
const Q=require("../interval_clock_grid/qout_primal_certificate.cjs");
const {fraction}=require("../interval_clock_grid/exact_certificate.cjs");
try{
 const input=process.argv[2],prefix=process.argv[3];
 if(!input||!prefix)throw Error("usage: dense_replay sparse.json output-prefix");
 const bytes=fs.readFileSync(input),source=JSON.parse(bytes);
 const certificate={scope:"Exact full-grid Qout replay of unchanged rational physical law.",
  n:source.n,pair_law:source.pair_law,center_deadline:source.center_deadline,
  completion_horizon:source.completion_horizon,physical_step:source.physical_step,
  weight_denominator:source.weight_denominator,paths:source.paths,
  sparse_source_sha256:crypto.createHash("sha256").update(bytes).digest("hex")};
 const graph=Q.buildClosure(certificate),flow=Q.maximumFlow(graph);
 certificate.closure_flow=flow.entries;certificate.closure_source_side=flow.source_side;
 certificate.global_upper=fraction(graph.stats.mass+graph.positive-flow.flow,4n*BigInt(graph.n)*graph.W);
 const replay=Q.verifyClosure(certificate);
 fs.writeFileSync(prefix+".physical.json",JSON.stringify(certificate)+"\n");
 fs.writeFileSync(prefix+".replay.json",JSON.stringify(replay,null,2)+"\n");
 console.log(JSON.stringify(replay));
}catch(error){console.error(error.stack);process.exitCode=1;}
