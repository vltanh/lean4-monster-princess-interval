"use strict";
// Exact, lossless storage of a Qout profile. This module decodes data only;
// isotonicity, endpoint conditions, and the claimed lower require a verifier.
const fs=require("node:fs"),zlib=require("node:zlib"),crypto=require("node:crypto");

function expandField(data){
 if(data.format!=="qout-clock-grid-field-u32-zlib-v1")return data;
 const n=data.n;if(!Number.isSafeInteger(n)||n<1||n>10000||data.normalized_profile!==true)throw Error("invalid compact Qout dimensions");
 const count=(4*n+1)*n;
 if(data.encoding?.count!==count||data.encoding.integer_type!=="uint32 little-endian"||data.encoding.compression!=="zlib")throw Error("invalid compact field encoding");
 const raw=zlib.inflateSync(Buffer.from(data.pre_two_values_base64,"base64"),{maxOutputLength:4*count});
 if(raw.length!==4*count||crypto.createHash("sha256").update(raw).digest("hex")!==data.encoding.uncompressed_sha256)throw Error("compact field checksum mismatch");
 const radial_nodes=[];
 for(let j=0;j<=12*n;j++)for(let k=1;k<=2*n;k++)if((j+k)%2===0){
  const time=Math.min(j,4*n),foot=k-Math.max(0,j-4*n);
  const a=foot<=0?0:raw.readUInt32LE(4*(time*n+Math.floor((foot-1)/2)));
  radial_nodes.push([j,k,String(a)]);
 }
 return {...data,radial_nodes};
}
function readField(filename){
 let bytes=fs.readFileSync(filename);
 if(filename.endsWith(".gz"))bytes=zlib.gunzipSync(bytes);
 return expandField(JSON.parse(bytes.toString("utf8")));
}
module.exports={expandField,readField};
