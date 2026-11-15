#!/usr/bin/env python3
"""All-monster lower certificate using nonuniform light-coordinate cells.

CDF evaluations and record probabilities are rounded with exact rationals.
The C++ dynamic program only performs integer operations, including downward
rounded concave record interpolation. No number-of-turns hypothesis occurs.
"""
from pathlib import Path
from fractions import Fraction as Q
from functools import lru_cache
from math import lcm
import argparse,hashlib,json,subprocess,sys,time

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'interval_cdf_discovery'))
from continuum_field import ExtendedExactField
from audit_snapshot import coordinate


def floorq(q):return q.numerator//q.denominator


def prepare(source,bins,den,refine,work):
    assert bins>0 and den>0 and den%bins==0 and refine>0
    data=json.loads(Path(source).read_text());field=ExtendedExactField(data)
    horizon=Q(str(data.get('terminal_time',2)))
    assert horizon==field.terminal_time
    base=sorted(set(x for p in field.nodes for x in p)|{Q(-1),Q(0),horizon+1})
    axis=sorted(set(a+(b-a)*Q(j,refine) for a,b in zip(base,base[1:]) for j in range(refine))|{base[-1]})
    axis=[x for x in axis if -1<=x<=horizon+1]
    coord_den=lcm(*(x.denominator for x in axis));time_den=2*coord_den
    assert den*time_den*(horizon+4)<2**64,'Integer certificate would overflow uint64'
    @lru_cache(None)
    def sides(u,v):
        t,x=(u+v)/2,(u-v)/2
        if x < -1:return Q(0),Q(0)
        if x > 1:return Q(1),Q(1)
        return field.cdf_sides(max(Q(0),min(horizon,t)),x)
    cells=[];index={}
    for i,(u0,u1) in enumerate(zip(axis,axis[1:])):
        for j,(v0,v1) in enumerate(zip(axis,axis[1:])):
            if max(u0,v0-2,-v1,Q(-1))>min(u1,2*horizon-v0,v1+2,horizon+1):continue
            initlo=max(u0,-v1,Q(-1));inithi=min(u1,-v0,Q(1))
            termlo=max(u0,2*horizon-v1,horizon-1);termhi=min(u1,2*horizon-v0,horizon+1)
            terminal=termlo<=termhi
            a=floorq(den*sides(u0,v1)[0]);b=floorq(den*(1-sides(u1,v0)[1]))
            assert 0<=a and 0<=b and a+b<=den
            c=dict(i=i,j=j,time=int(time_den*max(Q(0),(u0+v0)/2)),a=a,b=b,
                   initial=initlo<=inithi,terminal=terminal,
                   bounds=[[str(u0),str(v0)],[str(u1),str(v1)]])
            if terminal:
                xmin,xmax=termlo-horizon,termhi-horizon
                c['tail']=[int(time_den*z)for z in (horizon+1+xmin,horizon+3+xmin,
                                                   horizon+3-xmax,horizon+1-xmax)]
            else:c['tail']=[0]*4
            index[i,j]=len(cells);cells.append(c)
    for c in cells:
        c['right']=index.get((c['i']+1,c['j']),-1)
        c['up']=index.get((c['i'],c['j']+1),-1)
        assert c['terminal'] or max(c['right'],c['up'])>=0
    inp=work/'input.txt'
    with inp.open('w')as out:
        out.write(f'{len(cells)} {bins} {den} {time_den}\n')
        for c in cells:
            out.write(' '.join(map(str,[c['right'],c['up'],c['time'],c['a'],c['b'],
                                          int(c['terminal']),int(c['initial']),*c['tail']]))+'\n')
    meta=dict(field_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),
              input_sha256=hashlib.sha256(inp.read_bytes()).hexdigest(),
              exact_cdf_queries=sides.cache_info().misses,axis_size=len(axis),
              refinement=refine,terminal_time=str(horizon))
    (work/'geometry.json').write_text(json.dumps(dict(cells=cells,metadata=meta)))
    print(json.dumps(dict(event='exact_graph_prepared',cells=len(cells),**meta)),flush=True)
    return inp,cells,meta


def compress(route):
    out=[]
    for p in route:
        if out and p==out[-1]:continue
        if out and p[0]==out[-1][0]:
            assert p[1]==out[-1][1];continue
        while len(out)>=2:
            a,b=out[-2:]
            if (b[1]-a[1])*(p[0]-b[0])!=(p[1]-b[1])*(b[0]-a[0]):break
            out.pop()
        out.append(p)
    return out


def legal_route(cells,ids,horizon):
    centers=[]
    for i in ids:
        (u0,v0),(u1,v1)=[tuple(map(Q,p))for p in cells[i]['bounds']]
        u,v=(u0+u1)/2,(v0+v1)/2
        centers.append(((u+v)/2,(u-v)/2))
    # The centers make unit legs. Clip the 1-Lipschitz spatial curve to the
    # arena, and retain its nonnegative-time portion, including wall waits.
    if centers[0][0]>0:centers.insert(0,(Q(0),centers[0][1]))
    if centers[-1][0]<horizon:centers.append((horizon,centers[-1][1]))
    route=[]
    for (t,x),(s,y)in zip(centers,centers[1:]):
        assert t<s and abs(y-x)<=s-t
        lo,hi=max(Q(0),t),min(horizon,s)
        if lo>hi:continue
        cuts={lo,hi}
        if x!=y:
            for wall in [Q(-1),Q(1)]:
                z=t+(wall-x)*(s-t)/(y-x)
                if lo<z<hi:cuts.add(z)
        for z in sorted(cuts):
            w=x+(z-t)*(y-x)/(s-t)
            route.append((z,max(Q(-1),min(Q(1),w))))
    route=compress(route)
    assert route and route[0][0]==0 and route[-1][0]==horizon
    return route


def rescore(source,cells,result):
    from joint_cdf_field import RouteFunctional
    from continuum_field import ExtendedFieldMesh
    import numpy as np
    data=json.loads(Path(source).read_text());horizon=Q(str(data.get('terminal_time',2)))
    mesh=ExtendedFieldMesh(base=data['base'],vmax=data.get('domain_max_v',1));values=np.asarray(data['values'])
    route=legal_route(cells,result['cell_route'],horizon);t,x=route[-1];choices=[]
    for side in [-1,1]:
        full=compress(route+[(t+abs(side-x),Q(side)),(t+abs(side-x)+2,Q(-side))])
        score,_=RouteFunctional(mesh,full).value_gradient(values)
        choices.append(dict(cost=score,route=[[str(t),str(x)]for t,x in full]))
    return min(choices,key=lambda q:q['cost'])


def main():
    p=argparse.ArgumentParser();p.add_argument('field');p.add_argument('--bins',type=int,default=64)
    p.add_argument('--denominator',type=int,default=2**24);p.add_argument('--refine',type=int,default=1)
    p.add_argument('--work',required=True);p.add_argument('--out',required=True);p.add_argument('--reuse',action='store_true')
    args=p.parse_args();started=time.time();work=Path(args.work);work.mkdir(parents=True,exist_ok=True)
    if args.reuse:
        old=json.loads((work/'geometry.json').read_text());cells,meta=old['cells'],old['metadata'];inp=work/'input.txt'
        assert meta['field_sha256']==hashlib.sha256(Path(args.field).read_bytes()).hexdigest()
    else:inp,cells,meta=prepare(args.field,args.bins,args.denominator,args.refine,work)
    binary=work/'light_bellman_bin'
    subprocess.run(['c++','-O3','-std=c++17',str(HERE/'light_bellman.cpp'),'-o',str(binary)],check=True)
    raw=work/'result.json';subprocess.run([str(binary),str(inp),str(raw)],check=True)
    result=json.loads(raw.read_text());result.update(meta)
    result.update(scope='Exact-integer unrestricted-monster Bellman lower certificate for one supplied ordered CDF; no turn cutoff',
                  field=str(args.field),lower_bound=str(Q(result['bound_numerator'],result['bound_denominator'])))
    result['lower_bound_decimal']=float(Q(result['lower_bound']))
    result['legal_monster_response']=rescore(args.field,cells,result)
    result['seconds']=time.time()-started
    Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='cell_route'}),flush=True)


if __name__=='__main__':main()
