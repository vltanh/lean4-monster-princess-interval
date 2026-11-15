"use strict";
const fs=require("node:fs");
const path=require("node:path");
const crypto=require("node:crypto");
const {buildGraph}=require("./grid_model.cjs");
const {verifyCertificate}=require("./exact_certificate.cjs");
const filename=process.argv[2]||path.join(__dirname,"grid_n1_certificate.json");
try{
 const data=fs.readFileSync(filename),certificate=JSON.parse(data);
 const report=verifyCertificate(certificate,buildGraph);
 report.certificate_sha256=crypto.createHash("sha256").update(data).digest("hex");
 process.stdout.write(JSON.stringify(report,null,2)+"\n");
}catch(error){process.stderr.write(error.stack+"\n");process.exitCode=1;}
