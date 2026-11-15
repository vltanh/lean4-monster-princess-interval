/** Shared exact geometry cache for already serialized rational-germ paths.
 * Every distinct vertex and edge is independently checked. Reflection is exact.
 */
module.exports = (function(){
function createCachedGermPaths(G){
 const Q=G.Q,Z=G.ZERO;
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){const c=a%b;a=b;b=c;}return a;}
 function integerWeights(values){
  const w=values.map(Q);let D=1n;
  for(const x of w){if(x.cmp(0)<0)throw Error("negative weight");D=D/gcd(D,x.d)*x.d;}
  let a=w.map(x=>x.n*(D/x.d)),g=a.reduce((p,q)=>gcd(p,q),0n);
  if(!g)throw Error("zero mass");return a.map(x=>x/g);
 }
 function hydrate(payload,{pair=true}={}){
  const coords=payload.coordinate_dictionary.map(Q),vertices=new Map(),edges=new Map(),positive=[];
  function vertex(index){
   const key=index.join(",");if(vertices.has(key))return vertices.get(key);
   const t=coords[index[0]],x=coords[index[1]];
   if(t.cmp(0)<0||x.cmp(-1)<0||x.cmp(1)>0)throw Error("illegal cached vertex");
   const o={p:[t,x],u:t.a(x),v:t.s(x)};vertices.set(key,o);return o;
  }
  function edge(a,b){
   const key=a.join(",")+";"+b.join(",");if(edges.has(key))return edges.get(key);
   const p=vertex(a).p,q=vertex(b).p,dt=q[0].s(p[0]);
   if(dt.cmp(0)<=0)throw Error("illegal cached time order");
   const v=q[1].s(p[1]).dby(dt);if(v.cmp(-1)<0||v.cmp(1)>0)throw Error("illegal cached speed");
   edges.set(key,v);return v;
  }
  for(const r of payload.paths){
   const vv=r.path.map(vertex),p=Object.create(G.PLPath.prototype);
   if(!vv.length||!vv[0].p[0].eq(0))throw Error("cached initial time");
   p.vertices=vv.map(x=>x.p);p.t=vv.map(x=>x.p[0]);p.x=vv.map(x=>x.p[1]);
   p.v=r.path.slice(1).map((x,j)=>edge(r.path[j],x));
   p.seq=[vv.map(x=>x.u),vv.map(x=>x.v)];p.inverseCache=[new Map(),new Map()];positive.push(p);
  }
  const ws=integerWeights(payload.paths.map(r=>r.weight)),paths=positive.slice(),weights=ws.slice();
  if(pair)for(let j=0;j<positive.length;j++){
   const p=positive[j],r=Object.create(G.PLPath.prototype);
   r.t=p.t;r.x=p.x.map(x=>x.neg());r.vertices=r.t.map((t,k)=>[t,r.x[k]]);
   r.v=p.v.map(x=>x.neg());r.seq=[p.seq[1],p.seq[0]];r.inverseCache=[new Map(),new Map()];
   paths.push(r);weights.push(ws[j]);
  }
  return{paths,weights,W:weights.reduce((a,b)=>a+b,0n),positive,
   audit:{unique_coordinates:coords.length,unique_vertices:vertices.size,unique_edges:edges.size,
    positive_paths:positive.length,signed_paths:paths.length,radius:G.stats().radius}};
 }
 return{hydrate,integerWeights};
}
return{createCachedGermPaths};
})();