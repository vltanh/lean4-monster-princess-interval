
function createWarpTools(E) {
 const {Q,ZERO,ONE,minQ,maxQ,uniq,bisect}=E;
 const TWO=Q(2);
 function dot(a,b){return a.reduce((s,x,i)=>s.a(x.m(b[i])),ZERO);}
 function pointAt(a,x,vel,t){return[t,x.a(vel.m(t.s(a)))];}
 class WarpCoordinates {
  constructor(knots) {
   this.knots=knots.map(Q);
   if(this.knots.length<2||!this.knots[0].eq(0)||!this.knots.at(-1).eq(1))throw Error("warp endpoints");
   for(let i=1;i<this.knots.length;i++)if(this.knots[i].cmp(this.knots[i-1])<=0)throw Error("warp knots");
   this.n=this.knots.length-1;
   this.identity=this.knots.slice(1).map((x,i)=>x.s(this.knots[i]));
   this.cache=new Map();
  }
  basis(value) {
   const v=Q(value),key=v.str();if(this.cache.has(key))return this.cache.get(key);
   const den=2n*v.d;let k=v.n/den;if(v.n<0n&&v.n%den!==0n)k--;
   const r=v.s(Q(2n*k));let z=r,sign=1,c=Q(2n*k);
   if(r.cmp(1)>0){z=TWO.s(r);sign=-1;c=c.a(2);}
   const out=this.knots.slice(1).map((hi,i)=>{
    const lo=this.knots[i],h=z.cmp(lo)<=0?ZERO:z.cmp(hi)>=0?ONE:z.s(lo).dby(hi.s(lo));
    return c.a(h.m(sign));
   });
   this.cache.set(key,out);return out;
  }
  validate(increments,{strict=true}={}) {
   const d=increments.map(Q);if(d.length!==this.n||!d.reduce((s,x)=>s.a(x),ZERO).eq(1))throw Error("warp normalization");
   if(d.some(x=>strict?x.cmp(0)<=0:x.cmp(0)<0))throw Error("warp monotonicity");return d;
  }
  value(v,d){return dot(this.basis(v),d);}
  time(t,x){const u=this.basis(Q(t).a(x)),v=this.basis(Q(t).s(x));return u.map((q,i)=>q.a(v[i]).dby(2));}
  route(raw,increments){const d=this.validate(increments);return raw.map(p=>{
   const t=Q(p[0]),x=Q(p[1]),u=this.value(t.a(x),d),v=this.value(t.s(x),d);
   return[u.a(v).dby(2),u.s(v).dby(2)];
  });}
  interiorKnots(a,b){
   a=Q(a);b=Q(b);if(b.cmp(a)<=0)return[];
   const lo=Math.floor(a.num()/2)-1,hi=Math.ceil(b.num()/2)+1,out=[];
   for(let k=lo;k<=hi;k++)for(const z of this.knots)for(const v of[z.a(2*k),TWO.s(z).a(2*k)])if(v.cmp(a)>0&&v.cmp(b)<0)out.push(v);
   return uniq(out);
  }
 }
 function sides(field,t,x,interiorSign=null){
  const u=t.a(x.cmp(0)<0?x.neg():x),v=t.s(x.cmp(0)<0?x.neg():x);
  const r=v.cmp(1)>=0?ZERO:field.radial(u,v);
  if(interiorSign!==null){const z=interiorSign>0?ONE.a(r).dby(2):ONE.s(r).dby(2);return[z,z];}
  if(x.eq(0))return[ONE.s(r).dby(2),ONE.a(r).dby(2)];
  if(x.eq(1))return[ONE.a(r).dby(2),ONE];
  if(x.eq(-1))return[ZERO,ONE.s(r).dby(2)];
  const z=x.cmp(0)>0?ONE.a(r).dby(2):ONE.s(r).dby(2);return[z,z];
 }
 function cuts(field,warp,a,x,b,y) {
  const dt=b.s(a),vel=y.s(x).dby(dt),out=[a,b];
  if(x.m(y).cmp(0)<0)out.push(a.s(x.dby(vel)));
  const outer=uniq(out);
  for(let j=0;j+1<outer.length;j++){
   const t=outer[j],s=outer[j+1],xx=x.a(vel.m(t.s(a))),yy=x.a(vel.m(s.s(a)));
   const center=xx.eq(0)&&yy.eq(0),sign=xx.a(yy).cmp(0)<0?-1:1;
   const p=[t.a(xx.m(sign)),t.s(xx.m(sign))],q=[s.a(yy.m(sign)),s.s(yy.m(sign))];
   for(let axis=0;axis<2;axis++)if(q[axis].cmp(p[axis])>0){
    for(const v of warp.interiorKnots(p[axis],q[axis]))out.push(t.a(s.s(t).m(v.s(p[axis])).dby(q[axis].s(p[axis]))));
   }
   if(center){for(const grid of field.grid)for(const v of grid)if(v.cmp(t)>0&&v.cmp(s)<0)out.push(v);continue;}
   if(p[1].cmp(1)>=0)continue;
   const axis=p[0].eq(q[0])?0:1,other=1-axis,fixed=p[axis],low=p[other],high=q[other];
   if(q[1].cmp(1)>0&&q[1].cmp(p[1])>0)out.push(t.a(s.s(t).m(ONE.s(p[1])).dby(q[1].s(p[1]))));
   const i=Math.max(0,Math.min(field.grid[axis].length-2,bisect(field.grid[axis],fixed)-1));
   const poss=new Set([...(field.strips[axis].get(i)||[]),...(field.strips[axis].get(i-1)||[])]);
   for(const ti of poss){const ps=field.triangles[ti].ps;for(let z=0;z<3;z++){
    const aa=ps[z],bb=ps[(z+1)%3];let found=[];
    if(aa[axis].eq(bb[axis])){if(aa[axis].eq(fixed))found=[aa[other],bb[other]];}
    else if(minQ(aa[axis],bb[axis]).cmp(fixed)<=0&&fixed.cmp(maxQ(aa[axis],bb[axis]))<=0)
     found=[aa[other].a(fixed.s(aa[axis]).m(bb[other].s(aa[other])).dby(bb[axis].s(aa[axis])))];
    for(const v of found)if(v.cmp(low)>0&&v.cmp(high)<0)out.push(t.a(s.s(t).m(v.s(low)).dby(high.s(low))));
   }}
  }
  return uniq(out);
 }
 function captureFeatures(field,warp,raw,{requireComplete=true}={}) {
  const route=raw.map(p=>p.map(Q));if(!route.length||!route[0][0].eq(0))throw Error("initial time");
  let [l,h]=sides(field,...route[0]);const co=Array.from({length:warp.n},()=>ZERO);
  let mass=ZERO,pieces=0,jumps=0;
  function add(m,tv){if(m.cmp(0)<=0)return;mass=mass.a(m);for(let j=0;j<co.length;j++)co[j]=co[j].a(m.m(tv[j]));}
  function update(t,x,ss=null){
   const [a,b]=ss||sides(field,t,x),nl=minQ(l,a),nh=maxQ(h,b),m=l.s(nl).a(nh.s(h));
   if(m.cmp(0)>0){add(m,warp.time(t,x));jumps++;}
   l=nl;h=nh;
  }
  for(let k=0;k+1<route.length;k++){
   const[a,x]=route[k],[b,y]=route[k+1];if(b.eq(a)){if(!x.eq(y))throw Error("zero leg");continue;}
   if(b.cmp(a)<0||x.cmp(-1)<0||x.cmp(1)>0||y.cmp(-1)<0||y.cmp(1)>0)throw Error("route geometry");
   const vel=y.s(x).dby(b.s(a)),wait=x.eq(0)&&y.eq(0);
   if(!wait&&!vel.eq(1)&&!vel.eq(-1))throw Error("only unit legs and center waits");
   const ts=cuts(field,warp,a,x,b,y);
   for(let j=0;j+1<ts.length;j++){
    const t=ts[j],s=ts[j+1],[,xx]=pointAt(a,x,vel,t),[,yy]=pointAt(a,x,vel,s),sign=xx.a(yy).cmp(0)<0?-1:1;
    update(t,xx);
    const fa=wait?sides(field,t,xx):sides(field,t,xx,sign),fb=wait?sides(field,s,yy):sides(field,s,yy,sign);
    update(t,xx,fa);
    const ta=warp.time(t,xx),tb=warp.time(s,yy);
    function continuous(start,end,record,increasing){
     const delta=increasing?end.s(start):start.s(end);
     if(delta.cmp(0)<=0)return record;
     const m=increasing?end.s(record):record.s(end);
     if(m.cmp(0)<=0)return record;
     const lambda=increasing?record.s(start).dby(delta):start.s(record).dby(delta);
     if(lambda.cmp(0)<0||lambda.cmp(1)>0)throw Error("record crossing");
     const first=ta.map((q,i)=>q.a(tb[i].s(q).m(lambda))),mean=first.map((q,i)=>q.a(tb[i]).dby(2));
     add(m,mean);return end;
    }
    h=continuous(fa[1],fb[1],h,true);l=continuous(fa[0],fb[0],l,false);
    update(s,yy);pieces++;
   }
  }
  const complete=l.eq(0)&&h.eq(1);
  if(requireComplete&&!complete)throw Error("incomplete route");
  return{coefficients:co,identityCost:dot(co,warp.identity),capturedAfterTimeZero:mass,complete,lower:l,upper:h,pieces,jumps};
 }
 function remapExactField(field,warp,increments) {
  const d=warp.validate(increments),oldIndex=new Map(field.nodes.map((p,i)=>[p,i]));
  const out=Object.create(Object.getPrototypeOf(field));
  out.nodes=field.nodes.map(p=>p.map(v=>warp.value(v,d)));out.values=field.values.slice();
  out.grid=[0,1].map(k=>uniq(out.nodes.map(p=>p[k])));out.cells=new Map();out.strips=[new Map(),new Map()];out.triangles=[];
  out.initial=out.nodes.map((p,i)=>[p,out.values[i]]).filter(([p])=>p[0].eq(p[1].neg())).map(([p,v])=>[p[0],v]).sort((a,b)=>a[0].cmp(b[0]));
  out.initialKnots=out.initial.map(p=>p[0]);out.rcache=new Map();out.icache=new Map();
  for(const tr of field.triangles){
   const ids=tr.ps.map(p=>oldIndex.get(p));if(ids.some(i=>i===undefined))throw Error("triangle identity");
   const ps=ids.map(i=>out.nodes[i]),[p,q,r]=ps,e=[q[0].s(p[0]),q[1].s(p[1])],f=[r[0].s(p[0]),r[1].s(p[1])],det=e[0].m(f[1]).s(e[1].m(f[0])),[x,y,z]=ids.map(i=>out.values[i]);
   const ru=y.s(x).m(f[1]).s(z.s(x).m(e[1])).dby(det),rv=e[0].m(z.s(x)).s(f[0].m(y.s(x))).dby(det);
   if(ru.cmp(0)<0||rv.cmp(0)>0)throw Error("warped transport");
   const ti=out.triangles.length;out.triangles.push({ps,cf:[ru,rv,x.s(ru.m(p[0])).s(rv.m(p[1]))],positive:det.cmp(0)>0});
   const ranges=[0,1].map(k=>[bisect(out.grid[k],minQ(...ps.map(p=>p[k])),false),bisect(out.grid[k],maxQ(...ps.map(p=>p[k])),false)]);
   for(let k=0;k<2;k++)for(let i=ranges[k][0];i<ranges[k][1];i++){if(!out.strips[k].has(i))out.strips[k].set(i,[]);out.strips[k].get(i).push(ti);}
   for(let i=ranges[0][0];i<ranges[0][1];i++)for(let j=ranges[1][0];j<ranges[1][1];j++){const key=i+","+j;if(!out.cells.has(key))out.cells.set(key,[]);out.cells.get(key).push(ti);}
  }
  return out;
 }
 return{WarpCoordinates,captureFeatures,remapExactField,dot};
}
module.exports = {createWarpTools};
