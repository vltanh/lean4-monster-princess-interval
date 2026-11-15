const api=(function makeLateNegativeAudit(exactSource) {
  const X=Function(exactSource)(),{Q,ZERO,ONE,minQ,maxQ,uniq,bisect}=X;
  const originalBlob="5c45d042ee9948faebc03354c3e1e2ee3cbec1a5";
  function verify(data,reference,options={}) {
    const assert=(ok,message)=>{if(!ok)throw Error(message);};
    assert(JSON.stringify(data.nodes)===JSON.stringify(reference.nodes)&&JSON.stringify(data.triangles)===JSON.stringify(reference.triangles),"Changed reference geometry");
    assert(data.terminal_time===2,"Endpoint-by-two attachment");
    const f=new X.ExactField(data);
    assert(f.initial[0][0].eq(0)&&f.initial[0][1].eq(0)&&f.initial.at(-1)[0].eq(1)&&f.initial.at(-1)[1].eq(1),"Initial atom convention");
    assert(f.values.every(v=>v.cmp(0)>=0&&v.cmp(1)<=0),"CDF range");
    for(let j=0;j<f.nodes.length;j++)if(f.nodes[j][1].eq(1))assert(f.values[j].eq(0),"V=1 trace");
    for(const tr of f.triangles) {
      assert(uniq(tr.ps.map(p=>p[0])).length===2&&uniq(tr.ps.map(p=>p[1])).length===2,"Axis-aligned reference triangle");
      const lo=minQ(...tr.ps.map(p=>p[0])),hi=maxQ(...tr.ps.map(p=>p[0]));
      if(lo.cmp(1)<0){assert(hi.cmp(1)<=0,"Triangle crosses U=1");assert(!f.initialKnots.some(b=>lo.cmp(b)<0&&b.cmp(hi)<0),"Initial row regime");}
    }
    const columns=new Map(),acache=new Map(),ncache=new Map();
    const av=a=>{let k=a.str();if(!acache.has(k))acache.set(k,f.initialValue(a));return acache.get(k);};
    const nv=a=>{let k=a.str();if(!ncache.has(k))ncache.set(k,f.integral(a,a.neg(),a,0));return ncache.get(k);};
    function column(a) {
      const key=a.str();if(columns.has(key))return columns.get(key);
      const i=Math.max(0,Math.min(f.grid[1].length-2,bisect(f.grid[1],a)-1));
      const possible=new Set([...(f.strips[1].get(i)||[]),...(f.strips[1].get(i-1)||[])]);
      let cuts=[a,a.a(2)];
      for(const number of possible) {
        const ps=f.triangles[number].ps;
        for(let j=0;j<ps.length;j++) {
          const p=ps[j],q=ps[(j+1)%ps.length];
          if(p[1].eq(q[1])){if(p[1].eq(a))cuts.push(p[0],q[0]);}
          else if(minQ(p[1],q[1]).cmp(a)<=0&&a.cmp(maxQ(p[1],q[1]))<=0)
            cuts.push(p[0].a(a.s(p[1]).m(q[0].s(p[0])).dby(q[1].s(p[1]))));
        }
      }
      const xs=uniq(cuts.filter(u=>a.cmp(u)<=0&&u.cmp(a.a(2))<=0)),ys=xs.map(u=>f.radial(u,a)),prefix=[ZERO];
      for(let j=0;j+1<xs.length;j++)prefix.push(prefix.at(-1).a(xs[j+1].s(xs[j]).m(ys[j+1].a(ys[j])).dby(2)));
      function value(s){const j=Math.max(0,Math.min(xs.length-2,bisect(xs,s)-1));return ys[j].a(s.s(xs[j]).m(ys[j+1].s(ys[j])).dby(xs[j+1].s(xs[j])));}
      function primitive(s){assert(a.cmp(s)<=0&&s.cmp(a.a(2))<=0,"Column range");const j=Math.max(0,Math.min(xs.length-2,bisect(xs,s)-1));return prefix[j].a(s.s(xs[j]).m(ys[j].a(value(s))).dby(2));}
      const result={value,primitive};columns.set(key,result);return result;
    }
    function cost(s,a,endpoint=false) {
      const col=column(a),B=endpoint?ONE:col.value(s);
      return nv(a).a(s.m(4)).a(8).s(s.a(1).m(2).m(av(a))).s(s.a(6).s(a).m(B)).s(col.primitive(s)).dby(4);
    }
    const triangles=[],edgeMap=new Map();
    for(let number=0;number<f.triangles.length;number++) {
      const tr=f.triangles[number],ps=tr.ps;
      if(ps.some(p=>p[0].cmp(1)<0||p[1].cmp(0)<0))continue;
      assert(ps.every(p=>p[1].cmp(1)<=0)&&tr.cf[0].cmp(0)>=0,"Post-one triangle");
      triangles.push(number);
      for(let j=0;j<ps.length;j++) {
        let p=ps[j],q=ps[(j+1)%ps.length];if(p[1].eq(q[1]))continue;
        if(p[1].cmp(q[1])>0)[p,q]=[q,p];
        edgeMap.set(p.map(v=>v.str()).join(",")+";"+q.map(v=>v.str()).join(","),[p,q]);
      }
    }
    const edges=[...edgeMap.values()].sort((x,y)=>x[0][1].cmp(y[0][1])||x[1][1].cmp(y[1][1])||x[0][0].cmp(y[0][0])||x[1][0].cmp(y[1][0]));
    assert(triangles.length===3468&&edges.length===3502,"Whole geometry census");
    for(const[p,q]of edges)assert(!f.initialKnots.some(b=>p[1].cmp(b)<0&&b.cmp(q[1])<0),"Edge straddles initial knot");
    const physical=(a,s)=>[[ZERO,a.neg()],[s.a(a).dby(2),s.s(a).dby(2)],[s.a(1),Q(-1)],[s.a(3),ONE]];
    const report={scope:"Exact complete continuous late negative-M2 minimum for one supplied field; no unrestricted game-bound claim",field_blob:options.fieldBlob||originalBlob,triangles:triangles.length,edges:edges.length,tested_edges:0,quadratic_checks:0,endpoint_edges:0,stationary_candidates:0,minimizers:[]};
    let best=null;
    for(let index=0;index<edges.length;index++) {
      const[p,q]=edges[index],endpoint=p[0].s(p[1]).eq(2)&&q[0].s(q[1]).eq(2);
      if(endpoint)report.endpoint_edges++;
      const along=t=>p.map((x,j)=>x.a(q[j].s(x).m(t)));
      const value=t=>{const[s,a]=along(t);return cost(s,a,endpoint);};
      const y0=value(ZERO),ym=value(Q("1/2")),y1=value(ONE),qa=y1.s(ym.m(2)).a(y0).m(2),qb=y1.s(y0).s(qa);
      for(const t of[Q("1/3"),Q("2/3")]){assert(value(t).eq(y0.a(qb.m(t)).a(qa.m(t.m(t)))),"Quadratic edge identity "+index);report.quadratic_checks++;}
      const candidates=[[ZERO,y0],[ONE,y1]];
      if(qa.cmp(0)>0) {
        const t=qb.neg().dby(qa.m(2));
        if(t.cmp(0)>0&&t.cmp(1)<0){candidates.push([t,y0.s(qb.m(qb).dby(qa.m(4)))]);report.stationary_candidates++;}
      }
      const[t,z]=candidates.reduce((a,b)=>a[1].cmp(b[1])<0?a:b);
      if(!best||z.cmp(best.value)<0) {
        const[s,a]=along(t);best={s,a,value:z,endpoint};
        const row={value:z.str(),decimal:z.num(),absolute_start:a.str(),firstU:s.str(),endpoint,edge:index,edge_vertices:[p,q].map(v=>v.map(x=>x.str())),route:physical(a,s).map(v=>v.map(x=>x.str()))};
        report.minimum=row;report.minimizers.push(row);
      }
      report.tested_edges=index+1;
      if(options.progress&&(index+1)%500===0)options.progress(index+1);
    }
    assert(f.unitRoutePayoff(physical(best.a,best.s)).eq(best.value),"Independent physical capture");
    report.independent_physical_capture_check=true;
    report.cached_columns=columns.size;
    return report;
  }
  return{verify,originalBlob,create:makeLateNegativeAudit};
})("\nfunction gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a;}\nclass Rat{\n constructor(n,d=1n){if(n instanceof Rat){this.n=n.n;this.d=n.d;return;}if(typeof n===\"string\"){let p=n.split(\"/\");if(p.length===2){n=BigInt(p[0]);d=BigInt(p[1]);}else {let [s,e]=n.toLowerCase().split(\"e\");let neg=s[0]===\"-\";if(neg||s[0]===\"+\")s=s.slice(1);let parts=s.split(\".\");let f=parts[1]||\"\";n=BigInt(parts[0]+f)*(neg?-1n:1n);let power=f.length-Number(e||0);if(power>=0)d=10n**BigInt(power);else n*=10n**BigInt(-power);}}else n=BigInt(n);d=BigInt(d);if(d===0n)throw Error(\"zero denominator\");if(d<0n){n=-n;d=-d;}let g=gcd(n,d);this.n=n/g;this.d=d/g;}\n a(q){q=Q(q);return new Rat(this.n*q.d+q.n*this.d,this.d*q.d);}\n s(q){q=Q(q);return new Rat(this.n*q.d-q.n*this.d,this.d*q.d);}\n m(q){q=Q(q);return new Rat(this.n*q.n,this.d*q.d);}\n dby(q){q=Q(q);return new Rat(this.n*q.d,this.d*q.n);}\n neg(){return new Rat(-this.n,this.d);}\n cmp(q){q=Q(q);let z=this.n*q.d-q.n*this.d;return z<0n?-1:z>0n?1:0;}\n eq(q){return this.cmp(q)===0;}\n num(){return Number(this.n)/Number(this.d);}\n str(){return String(this.n)+(this.d===1n?\"\":\"/\"+this.d);}\n}\nfunction Q(x){return x instanceof Rat?x:new Rat(typeof x===\"number\"?String(x):x);}\nconst ZERO=Q(0),ONE=Q(1);\nfunction minQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)<0?a:b);}\nfunction maxQ(...xs){return xs.map(Q).reduce((a,b)=>a.cmp(b)>0?a:b);}\nfunction uniq(xs){let m=new Map(xs.map(Q).map(x=>[x.str(),x]));return [...m.values()].sort((a,b)=>a.cmp(b));}\nfunction bisect(xs,x,right=true){let a=0,b=xs.length;while(a<b){let m=(a+b)>>1,c=xs[m].cmp(x);if(c<0||(right&&c===0))a=m+1;else b=m;}return a;}\nfunction coord(x){let z=Q(x);if(z.cmp(0)<0)return coord(z.neg()).neg();const lim=4194304n;if(z.d<=lim)return z;let n=z.n,d=z.d,p0=0n,q0=1n,p1=1n,q1=0n;while(true){let a=n/d,q2=q0+a*q1;if(q2>lim)break;[p0,p1]=[p1,p0+a*p1];[q0,q1]=[q1,q2];[n,d]=[d,n-a*d];}\n let k=(lim-q0)/q1,b1=new Rat(p0+k*p1,q0+k*q1),b2=new Rat(p1,q1);return Math.abs(b1.num()-z.num())<Math.abs(b2.num()-z.num())?b1:b2;}\nfunction subP(a,b){return[a[0].s(b[0]),a[1].s(b[1])];}\nfunction cross(a,b){return a[0].m(b[1]).s(a[1].m(b[0]));}\nclass ExactField{\n constructor(data){\n this.nodes=data.nodes.map(p=>p.map(coord));this.values=(data.rational_values||data.values).map(Q);\n this.grid=[0,1].map(k=>uniq(this.nodes.map(p=>p[k])));this.cells=new Map();this.strips=[new Map(),new Map()];this.triangles=[];\n this.initial=this.nodes.map((p,i)=>[p,this.values[i]]).filter(([p,v])=>p[0].eq(p[1].neg())).map(([p,v])=>[p[0],v]).sort((a,b)=>a[0].cmp(b[0]));this.initialKnots=this.initial.map(p=>p[0]);\n for(const inds of data.triangles){\n let ps=inds.map(i=>this.nodes[i]),[p,q,r]=ps,[e,f]=[subP(q,p),subP(r,p)],det=cross(e,f),[x,y,z]=inds.map(i=>this.values[i]);\n let ru=y.s(x).m(f[1]).s(z.s(x).m(e[1])).dby(det),rv=e[0].m(z.s(x)).s(f[0].m(y.s(x))).dby(det);\n if(ru.cmp(0)<0||rv.cmp(0)>0)throw Error(\"transport\");\n let n=this.triangles.length;this.triangles.push({ps,cf:[ru,rv,x.s(ru.m(p[0])).s(rv.m(p[1]))],positive:det.cmp(0)>0});\n let ranges=[0,1].map(k=>[bisect(this.grid[k],minQ(...ps.map(p=>p[k])),false),bisect(this.grid[k],maxQ(...ps.map(p=>p[k])),false)]);\n for(let k=0;k<2;k++)for(let i=ranges[k][0];i<ranges[k][1];i++){if(!this.strips[k].has(i))this.strips[k].set(i,[]);this.strips[k].get(i).push(n);}\n for(let i=ranges[0][0];i<ranges[0][1];i++)for(let j=ranges[1][0];j<ranges[1][1];j++){let key=i+\",\"+j;if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(n);}\n }\n this.rcache=new Map();this.icache=new Map();\n }\n initialValue(z){z=Q(z);let i=Math.max(0,Math.min(this.initial.length-2,bisect(this.initialKnots,z)-1));let[a,x]=this.initial[i],[b,y]=this.initial[i+1];return x.a(z.s(a).m(y.s(x)).dby(b.s(a)));}\n radial(u,v){u=Q(u);v=Q(v);if(v.cmp(1)>0)return ZERO;let key=u.str()+\",\"+v.str();if(this.rcache.has(key))return this.rcache.get(key);let cell=[u,v].map((p,k)=>Math.max(0,Math.min(this.grid[k].length-2,bisect(this.grid[k],p)-1))),poss=new Set();\n for(let i of[cell[0],cell[0]-1])for(let j of[cell[1],cell[1]-1])for(let n of(this.cells.get(i+\",\"+j)||[]))poss.add(n);\n for(let n of[...poss].sort((a,b)=>a-b)){let {ps,cf,positive}=this.triangles[n];let turns=ps.map((p,i)=>cross(subP(ps[(i+1)%3],p),subP([u,v],p)));if(turns.every(t=>positive?t.cmp(0)>=0:t.cmp(0)<=0)){let z=cf[0].m(u).a(cf[1].m(v)).a(cf[2]);this.rcache.set(key,z);return z;}}\n throw Error(\"no triangle \"+key);\n }\n integral(fixed,left,right,axis,threshold=null){fixed=Q(fixed);left=Q(left);right=Q(right);if(threshold!==null)threshold=Q(threshold);if(right.cmp(left)<=0)return ZERO;\n let key=[fixed.str(),left.str(),right.str(),axis,threshold===null?\"\":threshold.str()].join(\",\");if(this.icache.has(key))return this.icache.get(key);\n if((axis===1&&fixed.cmp(1)>=0)||(axis===0&&left.cmp(1)>=0))return threshold===null?ZERO:maxQ(0,threshold).m(right.s(left));\n if(axis===0&&right.cmp(1)>0)return this.integral(fixed,left,ONE,axis,threshold).a(threshold===null?ZERO:maxQ(0,threshold).m(right.s(1)));\n let i=Math.max(0,Math.min(this.grid[axis].length-2,bisect(this.grid[axis],fixed)-1)),poss=new Set([...(this.strips[axis].get(i)||[]),...(this.strips[axis].get(i-1)||[])]),cuts=[left,right],other=1-axis;\n for(let n of poss){let {ps}=this.triangles[n];for(let k=0;k<3;k++){let a=ps[k],b=ps[(k+1)%3];if(a[axis].eq(b[axis])){if(a[axis].eq(fixed))for(let x of[a,b])if(x[other].cmp(left)>0&&x[other].cmp(right)<0)cuts.push(x[other]);}else if(minQ(a[axis],b[axis]).cmp(fixed)<=0&&fixed.cmp(maxQ(a[axis],b[axis]))<=0){let v=a[other].a(fixed.s(a[axis]).m(b[other].s(a[other])).dby(b[axis].s(a[axis])));if(v.cmp(left)>0&&v.cmp(right)<0)cuts.push(v);}}}\n cuts=uniq(cuts);let total=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],fa=axis===0?this.radial(fixed,a):this.radial(a,fixed),fb=axis===0?this.radial(fixed,b):this.radial(b,fixed);\n if(threshold!==null){fa=threshold.s(fa);fb=threshold.s(fb);if(fa.cmp(0)<=0&&fb.cmp(0)<=0)continue;if(fa.m(fb).cmp(0)<0){let w=b.s(a).m(fa.cmp(0)>0?fa.dby(fa.s(fb)):fb.dby(fb.s(fa)));total=total.a(w.m(maxQ(fa,fb)).dby(2));continue;}}\n total=total.a(b.s(a).m(fa.a(fb)).dby(2));}\n this.icache.set(key,total);return total;\n }\n negativeM1(a){a=Q(a);return this.integral(a,a.neg(),a,0).a(a.m(4)).a(8).s(a.a(3).m(2).m(this.initialValue(a))).s(this.integral(a,a,a.a(2),1)).dby(4);}\n positiveM1(a){a=Q(a);let A=this.initialValue(a);return Q(8).s(a.m(4)).a(Q(3).s(a).m(A)).s(this.integral(a.neg(),a,Q(2).s(a),1)).s(this.integral(Q(2).s(a),a.neg(),ONE,0,A)).dby(4);}\n fixedOne(a,positive){a=Q(a);let A=this.initialValue(a),v=positive?a.neg():a,I=this.integral(v,a,ONE,1),B=this.radial(ONE,v);\n return positive?Q(12).a(A.m(2)).s(Q(7).a(a).m(B)).s(I).s(this.integral(ONE,a.neg(),ONE,0,A)).dby(4):this.integral(a,a.neg(),a,0).a(12).s(A.m(4)).s(Q(7).s(a).m(B)).s(I).dby(4);\n }\n cdfSides(t,x){t=Q(t);x=Q(x);let r=this.radial(t.a(x.cmp(0)<0?x.neg():x),t.s(x.cmp(0)<0?x.neg():x));if(x.eq(0))return[ONE.s(r).dby(2),ONE.a(r).dby(2)];if(x.eq(1))return[ONE.a(r).dby(2),ONE];if(x.eq(-1))return[ZERO,ONE.s(r).dby(2)];let v=x.cmp(0)>0?ONE.a(r).dby(2):ONE.s(r).dby(2);return[v,v];}\n unitRoutePayoff(route){route=route.map(p=>p.map(Q));let[lower,upper]=this.cdfSides(...route[0]),cost=ZERO;\n for(let k=0;k<route.length-1;k++){let[start,x]=route[k],[end,y]=route[k+1];if(end.eq(start)){if(!x.eq(y))throw Error(\"bad duplicate\");continue;}let vel=y.s(x).dby(end.s(start));if(!vel.eq(1)&&!vel.eq(-1))throw Error(\"not unit\");let cuts=[start,end];if(x.m(y).cmp(0)<0)cuts.splice(1,0,start.s(vel.m(x)));let area=ZERO;\n for(let j=0;j<cuts.length-1;j++){let a=cuts[j],b=cuts[j+1],xa=x.a(vel.m(a.s(start))),xb=x.a(vel.m(b.s(start))),sign=xa.a(xb).cmp(0)>0?1:-1,ua=a.a(xa.m(sign)),va=a.s(xa.m(sign)),ub=b.a(xb.m(sign)),vb=b.s(xb.m(sign)),record=vel.eq(1)?upper:lower;\n if(vel.m(sign).eq(1)){let threshold=sign===1?record.m(2).s(1):ONE.s(record.m(2));area=area.a(this.integral(va,ua,ub,1).s(threshold.m(ub.s(ua))).a(this.integral(va,ua,ub,1,threshold)).dby(4));}\n else{let threshold=sign===-1?ONE.s(record.m(2)):record.m(2).s(1);area=area.a(this.integral(ua,va,vb,0,threshold).dby(4));}}\n let[strict,closed]=this.cdfSides(end,y);if(vel.eq(1)){let updated=maxQ(upper,closed);cost=cost.a(end.m(updated.s(upper))).s(area);upper=updated;}else{let updated=minQ(lower,strict);cost=cost.a(end.m(lower.s(updated))).s(area);lower=updated;}}\n if(!lower.eq(0)||!upper.eq(1))throw Error(\"incomplete\");return cost;\n }\n}\nreturn {Rat,Q,ZERO,ONE,minQ,maxQ,uniq,bisect,ExactField};\n\n");
if(typeof module!=="undefined")module.exports=api;

if(typeof require!=="undefined"&&require.main===module){
 const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),args=process.argv.slice(2);
 const arg=(name,fallback)=>{const i=args.indexOf(name);return i<0?fallback:args[i+1];};
 const referencePath=path.join(__dirname,"snapshots","endpoint_joint_i1_field.json"),referenceRaw=fs.readFileSync(referencePath);
 const hash=raw=>crypto.createHash("sha1").update(Buffer.from("blob "+raw.length+"\0")).update(raw).digest("hex");
 if(hash(referenceRaw)!==api.originalBlob)throw Error("Changed reference geometry file");
 const fieldPath=arg("--field",referencePath),raw=fs.readFileSync(fieldPath),report=api.verify(JSON.parse(raw),JSON.parse(referenceRaw),{fieldBlob:hash(raw)});
 const expected=arg("--expected",null),output=arg("--report",null);
 if(expected&&JSON.stringify(report)!==JSON.stringify(JSON.parse(fs.readFileSync(expected,"utf8"))))throw Error("Exact report mismatch");
 if(output)fs.writeFileSync(output,JSON.stringify(report,null,2)+"\n");
 console.log(JSON.stringify({triangles:report.triangles,edges:report.edges,minimum:report.minimum,independent_physical_capture_check:report.independent_physical_capture_check}));
}
return api;
