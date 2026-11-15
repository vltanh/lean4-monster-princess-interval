#!/usr/bin/env python3
"""Extract exact midpoint quantile paths from a complete rational CDF field.

All triangle intersections, path vertices, legality and ordering checks are
rational. Input coordinates follow the repository's exact mesh convention.
The finite law is paired by reflection and is an approximation of the
specified continuum law, not of the unrestricted equilibrium.
"""
from __future__ import annotations
import argparse
from bisect import bisect_right
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_cdf_discovery'))
from audit_snapshot import coordinate


def simplify(vertices):
    result=[]
    for t,x in vertices:
        if result and t==result[-1][0]:
            assert x==result[-1][1],('two quantile positions at one time',t,x,result[-1][1])
            continue
        result.append((t,x))
        while len(result)>=3:
            (a,x),(b,y),(c,z)=result[-3:]
            if (y-x)*(c-b)==(z-y)*(b-a):result.pop(-2)
            else:break
    return result


class Field:
    def __init__(self,data):
        self.data=data
        self.nodes=[tuple(map(coordinate,p))for p in data['nodes']]
        self.values=[Q(x)for x in data['rational_values']] if 'rational_values'in data else [Q(str(x))for x in data['values']]
        self.triangles=[tuple(t)for t in data['triangles']]
        self.ranges=[]
        assert all(0<=r<=1 for r in self.values)
        self.initial=sorted((u,self.values[i])for i,(u,v)in enumerate(self.nodes)if u==-v)
        assert self.initial[0]==(0,0) and self.initial[-1]==(1,1)
        self.terminal=Q(data['terminal_time'])
        self.vmax=coordinate(data.get('domain_max_v',1))
        assert self.terminal==self.vmax+1
        assert all(self.values[i]==0 for i,(u,v)in enumerate(self.nodes)if v==self.vmax)
        for inds in self.triangles:
            (u,v),(a,b),(c,d)=[self.nodes[i]for i in inds]
            r,s,t=[self.values[i]for i in inds]
            det=(a-u)*(d-v)-(c-u)*(b-v)
            ru=((s-r)*(d-v)-(t-r)*(b-v))/det
            rv=((a-u)*(t-r)-(c-u)*(s-r))/det
            assert ru>=0 and rv<=0,('transport',inds,ru,rv)
            self.ranges.append((min(r,s,t),max(r,s,t)))
        # A field's partition is part of its definition. Require precisely the
        # established complete mesh rather than silently accepting missing cells.
        from continuum_field import ExtendedFieldMesh
        mesh=ExtendedFieldMesh(data['base'],vmax=self.vmax)
        assert len(mesh.nodes)==len(self.nodes)
        assert [tuple(map(coordinate,p))for p in mesh.nodes]==self.nodes
        assert [tuple(map(int,t))for t in mesh.triangles]==self.triangles

    def quantile(self,q):
        q=Q(q)
        assert 0<q<1 and q not in self.values,('rank lies on nodal value; choose another midpoint mesh',q)
        points=set()
        for inds,(lo,hi)in zip(self.triangles,self.ranges):
            if not lo<q<hi:continue
            crossing=[]
            for j in range(3):
                i,k=inds[j],inds[(j+1)%3]
                a,b=self.values[i],self.values[k]
                if min(a,b)<q<max(a,b):
                    lam=(q-a)/(b-a)
                    u,v=[x+lam*(y-x)for x,y in zip(self.nodes[i],self.nodes[k])]
                    crossing.append(((u+v)/2,(u-v)/2))
            assert len(crossing)==2
            points.update(crossing)
        # The initial and endpoint faces may surround a constant-boundary gap
        # (e.g. a temporary center atom). Ordered level-set segments then join
        # through that same boundary at speed zero.
        if not any(t==0 for t,x in points):
            for (a,r),(b,s)in zip(self.initial,self.initial[1:]):
                if r<q<s:
                    points.add((Q(0),a+(b-a)*(q-r)/(s-r)))
                    break
        points.add((self.terminal,Q(1)))
        path=simplify(sorted(points))
        assert path[0][0]==0
        assert all(0<=x<=1 and 0<=t<=self.terminal for t,x in path)
        assert all(b>a and abs(y-x)<=b-a for(a,x),(b,y)in zip(path,path[1:]))
        return path


def position(path,t):
    k=bisect_right([p[0]for p in path],t)-1
    if k+1==len(path):return path[-1][1]
    a,x=path[k];b,y=path[k+1]
    return x+(y-x)*(t-a)/(b-a)


def extract(source,radial_count,phase=Q(1,2)):
    raw=Path(source).read_bytes();data=json.loads(raw)
    assert radial_count>=1
    phase=Q(phase);assert 0<phase<1
    field=Field(data);positive=[]
    for i in range(radial_count):positive.append(field.quantile((i+phase)/radial_count))
    paths=[[(t,-x)for t,x in p]for p in positive[::-1]]+positive
    for p,q in zip(paths,paths[1:]):
        assert all(position(p,t)<=position(q,t)for t in sorted(set(t for t,x in p+q))), 'quantile order'
    return dict(scope='Exact equally spaced radial quantiles of this legal endpoint-absorbed ordered CDF; no game-value claim.',
                input=Path(source).name,input_sha256=hashlib.sha256(raw).hexdigest(),
                radial_count=radial_count,total_count=len(paths),rank_phase=str(phase),terminal_time=str(field.terminal),
                response_horizon=str(field.terminal+4),
                uniform_payoff_error=str((field.terminal+4)*max(phase,1-phase)/radial_count),
                paths=[[[str(t),str(x)]for t,x in p]for p in paths],
                weights=[str(Q(1,len(paths)))]*len(paths),
                validation=dict(nodes=len(field.nodes),triangles=len(field.triangles),
                                cone='exact pass',complete_mesh='exact pass',
                                vertices=sum(len(p)for p in paths),ordered='exact pass'))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('field');parser.add_argument('--radial-count',type=int,default=16)
    parser.add_argument('--phase',default='1/2')
    parser.add_argument('--output',required=True);args=parser.parse_args();started=time.time()
    data=extract(args.field,args.radial_count,Q(args.phase));data['seconds']=time.time()-started
    output=Path(args.output);output.write_text(json.dumps(data,indent=2)+'\n')
    text=[str(data['total_count'])+' '+data['terminal_time']]
    for weight,path in zip(data['weights'],data['paths']):
        text.append(weight+' '+str(len(path)))
        text.extend(t+' '+x for t,x in path)
    output.with_suffix('.txt').write_text('\n'.join(text)+'\n')
    print(json.dumps({k:v for k,v in data.items()if k not in ('paths','weights')},indent=2))


if __name__=='__main__':main()
