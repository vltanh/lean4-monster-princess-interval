/** Cached compilation of the audited query connector.
 * The path geometry is identical to germ_avoided_realizer for affine/raw modes.
 * Clipping is a separately labelled legal candidate, with unit/wait velocities.
 */
module.exports = (function(){
function createCachedConnector(G){
 const Q=G.Q,Z=G.ZERO,O=G.ONE,e=G.eps,eta=e.pow(6),shrink=O.s(eta.m(2));
 const min=(a,b)=>a.cmp(b)<=0?a:b,max=(a,b)=>a.cmp(b)>=0?a:b;
 function compile(queryV,baseLevels,rows,{avoidIsolated=true,transform="affine"}={}){
  if(!["affine","raw","clip"].includes(transform))throw Error("unknown transform");
  const vv=queryV.map(Q),bases=baseLevels.map(Q),values=[];
  for(const b of bases)for(const side of [-1,0,1])values.push(b.a(e.m(side)));
  const vertices=new Map(),blocks=new Map(),edgeDirections=new Map(),converted=new Map(),clipEdges=new Map();
  let isolatedChanges=0,forcedIntervals=0;
  function vertex(u,v){
   const key=u.str()+"|"+v.str();if(vertices.has(key))return vertices.get(key);
   if(u.s(v).cmp(0)<0||u.s(v).cmp(2)>0)throw Error("light strip");
   const p={u,v,t:u.a(v).dby(2),x:u.s(v).dby(2),key};vertices.set(key,p);return p;
  }
  function direction(a,b){
   const key=a.key+";"+b.key;if(edgeDirections.has(key))return edgeDirections.get(key);
   const du=b.u.s(a.u),dv=b.v.s(a.v);
   if(du.cmp(0)<0||dv.cmp(0)<0)throw Error("light order");
   let d;if(du.eq(0))d=-1;else if(dv.eq(0))d=1;else if(du.eq(dv))d=0;else throw Error("non-axis connector");
   edgeDirections.set(key,d);return d;
  }
  function block(j,l,r){
   const key=j+","+l+","+r;if(blocks.has(key))return blocks.get(key);
   const v=vv[j],prev=values[l],target=values[r],points=[vertex(prev,vv[j-1])];
   let before=v.s(min(e.pow(2),v.s(vv[j-1]).dby(3)));
   const isolated=bases[Math.floor(l/3)].eq(v)&&bases[Math.floor(r/3)].cmp(v)>0;
   if(avoidIsolated&&isolated){before=min(before,prev.s(e));if(before.cmp(vv[j-1])<=0)throw Error("connector crosses query");isolatedChanges++;}
   else if(bases[Math.floor(l/3)].cmp(v)<0)forcedIntervals++;
   function add(u,w){const p=vertex(u,w),a=points.at(-1);if(a.key!==p.key){direction(a,p);points.push(p);}}
   add(prev,min(before,prev));if(before.cmp(prev)>0)add(before,before);
   add(min(target,before.a(2)),before);if(target.cmp(before.a(2))>0)add(target,target.s(2));add(target,v);
   blocks.set(key,points);return points;
  }
  const coordinate_dictionary=[],coordMap=new Map(),put=x=>{const s=x.str();if(coordMap.has(s))return coordMap.get(s);const i=coordinate_dictionary.length;coordinate_dictionary.push(s);coordMap.set(s,i);return i;};
  function affinePoint(p){
   if(converted.has(p.key))return converted.get(p.key);
   const o=[p.t,transform==="affine"?p.x.m(shrink).a(eta):p.x];converted.set(p.key,o);return o;
  }
  const clip=x=>min(O.s(eta),max(eta,x));
  function clipSegment(a,b){
   const key=a.map(x=>x.str()).join("|")+";"+b.map(x=>x.str()).join("|");if(clipEdges.has(key))return clipEdges.get(key);
   const d=b[1].cmp(a[1]),out=[];
   if(d)for(const h of [eta,O.s(eta)]){
    if((h.cmp(a[1])>0&&h.cmp(b[1])<0)||(h.cmp(a[1])<0&&h.cmp(b[1])>0))out.push([a[0].a(h.s(a[1]).m(d)),h]);
   }
   out.sort((p,q)=>p[0].cmp(q[0]));out.push([b[0],clip(b[1])]);clipEdges.set(key,out);return out;
  }
  const output=[];
  for(let row=0;row<rows.length;row++){
   const indices=rows[row].labels,light=[vertex(Z,Q(-1))],dirs=[];
   function addLight(p){const a=light.at(-1);if(p.key===a.key)return;const d=direction(a,p);
    if(dirs.length&&dirs.at(-1)===d){light.pop();dirs.pop();}
    light.push(p);dirs.push(d);
   }
   for(let j=1;j<vv.length;j++){const b=block(j,indices[j-1],indices[j]);if(light.at(-1).key!==b[0].key)throw Error("query attachment");for(const p of b.slice(1))addLight(p);}
   let raw=[];
   for(let j=0;j+1<light.length;j++){
    const a=light[j],b=light[j+1];if(b.t.cmp(0)<0)continue;
    if(!raw.length){if(a.t.cmp(0)>0)throw Error("initial crossing");let x=a.x.s(a.t.m(dirs[j]));if(transform==="affine")x=x.m(shrink).a(eta);raw.push([Z,x]);}
    if(b.t.cmp(raw.at(-1)[0])>0)raw.push(affinePoint(b));
   }
   if(transform==="clip"){
    const clipped=[[raw[0][0],clip(raw[0][1])]],cd=[];
    function add(p){const last=clipped.at(-1);if(p[0].eq(last[0])){if(!p[1].eq(last[1]))throw Error("clip duplicate");return;}
     const d=p[1].cmp(last[1]);if(cd.length&&cd.at(-1)===d){clipped.pop();cd.pop();}
     clipped.push(p);cd.push(d);
    }
    for(let j=0;j+1<raw.length;j++)for(const p of clipSegment(raw[j],raw[j+1]))add(p);
    raw=clipped;
   }
   output.push({row:rows[row].row??row,weight:String(rows[row].weight),initial_limit:raw[0][1].limit().str(),path:raw.map(p=>p.map(put))});
  }
  return{scope:"Exact cached "+(avoidIsolated?"avoided":"default")+" connector; "+transform+" transform. No lower guarantee.",
   coordinate_dictionary,paths:output,audit:{rows:output.length,unique_light_vertices:vertices.size,
    unique_blocks:blocks.size,unique_edges:edgeDirections.size,isolatedChanges,forcedIntervals,
    unique_clip_edges:clipEdges.size,radius:G.stats().radius},options:{avoidIsolated,transform}};
 }
 return{compile};
}
return{createCachedConnector};
})();