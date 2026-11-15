"use strict";
const {buildGraph,price,column,decode}=require("./grid_model.cjs");
const {solveColumns}=require("./small_lp.cjs");
const {certifyNumerical}=require("./exact_certificate.cjs");
function planRoute(g,start,moves,minus,plus){
 let e=g.outgoing[0].find(e=>g.states[g.edges[e][1]][1]===start),u=g.edges[e][1];const route=[e];
 for(let j=0;j<moves.length;j++){
  for(const [kind,counts] of [[1,minus],[2,plus]])for(let k=0;k<(counts[j]||0);k++){
   e=g.outgoing[u].find(e=>g.edges[e][2]===kind);if(e===undefined)throw Error("illegal seed charge");
   route.push(e);u=g.edges[e][1];
  }
  e=g.outgoing[u].find(e=>g.edges[e][2]===3&&g.states[g.edges[e][1]][1]-g.states[u][1]===moves[j]);if(e===undefined)throw Error("illegal seed move");
  route.push(e);u=g.edges[e][1];
 }
 e=g.outgoing[u].find(e=>g.edges[e][2]===4);if(e===undefined)throw Error("illegal seed terminal");route.push(e);return route;
}
async function solveGrid(n,options={}){
 const g=buildGraph(n),columns=[],seen=new Set(),history=[];
 const maxIterations=options.maxIterations??200;
 function add(route){
  const col=column(g,route),key=col.cost+":"+col.counts.join(",");
  if(seen.has(key))return false;
  seen.add(key);columns.push(col);return true;
 }
 const sweepMinus={};for(let j=0;j<4*n;j++)sweepMinus[j]=1;
 add(planRoute(g,2*n,new Array(4*n).fill(-1),sweepMinus,{}));
 add(planRoute(g,0,[...new Array(n).fill(1),...new Array(3*n).fill(-1),...new Array(4*n).fill(1)],
  {[0]:3*n,[3*n]:n},{[0]:n,[n]:7*n}));
 for(let it=0;it<maxIterations;it++){
  const result=solveColumns(g,columns),priced=price(g,result.discounts);
  const report={it,columns:columns.length,upper:result.minimum/(4*n),priced:priced.value/(4*n),
   gap:(result.minimum-priced.value)/(4*n),pivots:result.pivots};
  history.push(report);
  const numerical={n,model:{nodes:g.states.length,flow_arcs:g.edges.length,pressure_nodes:g.events.length,matching_edges:g.matches.length},
   columns:columns.length,result,priced_value:priced.value,history,
   paths:columns.map((col,i)=>({weight:result.x[i],...decode(g,col.route)})).filter(p=>p.weight>1e-9)};
  if(options.onIteration)await options.onIteration(report,numerical);
  if(result.minimum-priced.value<=1e-8){
   const exact=certifyNumerical(numerical,()=>g);
   return {numerical,...exact};
  }
  let added=add(priced.route);
  // Also price every possible initial position with the same optimal suffix labels.
  for(const first of g.outgoing[0]){
   let u=g.edges[first][1];
   if(!Number.isFinite(priced.dist[u])||priced.dist[u]>=result.minimum-1e-8)continue;
   const route=[first];
   while(u!==1){
    const e=priced.choice[u];if(e<0)throw Error("broken start-price route");
    route.push(e);u=g.edges[e][1];
   }
   added=add(route)||added;
  }
  if(!added)throw Error("pricing stalled before an exact certificate");
 }
 throw Error("column generation iteration limit");
}
module.exports={solveGrid};
if(require.main===module){
 const fs=require("node:fs"),path=require("node:path");
 const n=Number(process.argv[2]||1),prefix=process.argv[3]||path.join(__dirname,"grid_n"+n);
 (async()=>{
  const out=await solveGrid(n,{onIteration:async(report,numerical)=>{
   process.stderr.write(JSON.stringify(report)+"\n");
   fs.writeFileSync(prefix+"_checkpoint.json",JSON.stringify(numerical,null,2)+"\n");
  }});
  fs.writeFileSync(prefix+"_certificate.json",JSON.stringify(out.certificate,null,2)+"\n");
  fs.writeFileSync(prefix+"_replay.json",JSON.stringify(out.replay,null,2)+"\n");
  process.stdout.write(JSON.stringify(out.replay,null,2)+"\n");
 })().catch(error=>{process.stderr.write(error.stack+"\n");process.exitCode=1;});
}
