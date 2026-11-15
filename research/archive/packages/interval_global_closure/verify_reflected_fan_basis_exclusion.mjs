#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import zlib from "node:zlib";
import crypto from "node:crypto";
import {createRequire} from "node:module";
import {fileURLToPath} from "node:url";
const require=createRequire(import.meta.url),here=path.dirname(fileURLToPath(import.meta.url));
const certificate=JSON.parse(fs.readFileSync(path.join(here,"snapshots/reflected_fan_basis_exclusion.json"),"utf8"));
const raw=zlib.gunzipSync(Buffer.from(fs.readFileSync(path.join(here,certificate.source_packet.path),"utf8"),"base64"));
if(crypto.createHash("sha256").update(raw).digest("hex")!==certificate.source_packet.uncompressed_sha256)throw Error("source packet identity");
const packet=JSON.parse(raw),start=Date.now();
const result=require("./fan_selector_upper_bound.cjs").createSelectorVerifier().replay(packet,certificate);
result.execution={engine:"Exact BigInt rational Node replay",elapsed_ms:Date.now()-start};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify(result,null,2));
