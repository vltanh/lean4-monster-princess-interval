#!/usr/bin/env node
import fs from "node:fs";
import {createRequire} from "node:module";
const require=createRequire(import.meta.url),E=require("./warp_exact_field_core.cjs"),{createWarpTools}=require("./warp_capture_features.cjs"),{createEarlyWarpAudit}=require("./warp_early_phase.cjs");
if(process.argv.length<4)throw Error("Supply FIELD SOLUTION [REPORT]");
const [field,solution]=process.argv.slice(2,4).map(p=>JSON.parse(fs.readFileSync(p,"utf8")));
const report=createEarlyWarpAudit(E,createWarpTools(E)).verify(field,solution),text=JSON.stringify(report,null,2)+"\n";
if(process.argv[4])fs.writeFileSync(process.argv[4],text);process.stdout.write(text);
