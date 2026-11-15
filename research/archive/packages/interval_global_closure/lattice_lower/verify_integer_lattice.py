#!/usr/bin/env python3
"""Prepare/replay the integer lattice value-lower verifier.

Native regression on 2026-11-13 compared all 27,666 sampled entries in six
legal rational fields at refinements 1, 2, 3 against independent Fraction
barycentric evaluation. Two complete native wrapper fixtures also passed.
See test_native_sampler.py and native_sampler_replay.json. No improved
unrestricted game lower bound has been produced by this implementation.
The fixed field is validated exactly; NumPy only performs bounded integer
barycentric arithmetic. This file is self-contained apart from NumPy/g++.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
from math import gcd,lcm
from pathlib import Path
import struct
import subprocess
import time
import numpy as np

class ExactField:
    def __init__(self,path):
        data=json.loads(Path(path).read_text())
        assert data['mesh_kind']=='light' and data.get('center_aligned',False)
        self.h=Q(str(data['step']));self.last=Q(str(data.get('mesh_horizon',5)))
        assert Q(str(data.get('outward_horizon',-1)))==2
        assert Q(str(data.get('absorption_horizon',3)))==3 and self.last>=5
        assert (1/self.h).denominator==1 and (2*self.last/self.h).denominator==1
        self.H=int(1/self.h);self.low=-self.H;self.high=int((self.last+1)/self.h)
        points=[(i,j) for i in range(self.low,self.high+1)
                for j in range(self.low,self.high+1)
                if 0<=i+j<=2*self.last/self.h and abs(i-j)<=2*self.H]
        self.points=sorted(points,key=lambda p:(p[0]+p[1],p[0]-p[1]))
        self.values=list(map(Q,data['signed_cdf_nodal']))
        assert len(self.values)==len(self.points)
        self.lookup=dict(zip(self.points,self.values));self.cells={}
        for (i,j),f in self.lookup.items():
            assert 0<=f<=1 and f+self.lookup[j,i]==1
            if i==j or (i+j)*self.h/2>=3:assert f==Q(1,2)
        self.triangles=[]
        for i in range(self.low,self.high):
            for j in range(self.low,self.high):
                corners=[(i,j),(i+1,j),(i,j+1),(i+1,j+1)]
                inside=[p for p in corners if p in self.lookup]
                if len(inside)<3:continue
                if len(inside)==3:local=[inside]
                elif i==j:local=[[corners[0],corners[1],corners[3]],
                                 [corners[0],corners[2],corners[3]]]
                else:local=[[corners[0],corners[1],corners[2]],
                            [corners[1],corners[2],corners[3]]]
                self.cells[i,j]=local
                for tri in local:
                    (i0,j0),(i1,j1),(i2,j2)=tri
                    f0,f1,f2=[self.lookup[p] for p in tri]
                    det=(i1-i0)*(j2-j0)-(i2-i0)*(j1-j0)
                    bu=((f1-f0)*(j2-j0)-(f2-f0)*(j1-j0))/det
                    bv=((i1-i0)*(f2-f0)-(i2-i0)*(f1-f0))/det
                    assert bu>=0 and bv<=0
                    if min((a+b)*self.h/2 for a,b in tri)>=2:
                        if min(a-b for a,b in tri)>=0:assert bu==0
                        if max(a-b for a,b in tri)<=0:assert bv==0
                    self.triangles.append(tri)
    def value(self,t,x):
        if t>=3:return Q(1,2)
        u=(t+x)/self.h;v=(t-x)/self.h
        i=u.numerator//u.denominator;j=v.numerator//v.denominator
        for ii,jj in [(i,j)]+[(i+a,j+b) for a in (-1,0,1) for b in (-1,0,1)]:
            for tri in self.cells.get((ii,jj),[]):
                (i0,j0),(i1,j1),(i2,j2)=tri
                det=(i1-i0)*(j2-j0)-(i2-i0)*(j1-j0)
                a=((u-i0)*(j2-j0)-(i2-i0)*(v-j0))/det
                b=((i1-i0)*(v-j0)-(u-i0)*(j1-j0))/det
                if min(a,b,1-a-b)>=0:
                    return (1-a-b)*self.lookup[tri[0]]+a*self.lookup[tri[1]]+b*self.lookup[tri[2]]
        raise AssertionError(('outside mesh',t,x))

def exact_sample(field,refinement):
    assert isinstance(refinement,int) and refinement>=1
    B=2*field.H*refinement;denweight=2*refinement
    original_den=1
    for f in field.values:original_den=lcm(original_den,f.denominator)
    D=original_den*denweight
    assert D%2==0 and 32*D*B<(2**64-1)//2 and D<2**62
    low,high=field.low,field.high
    grid=np.full((high-low+3,)*2,-1,dtype=np.int64)
    for (i,j),f in zip(field.points,field.values):
        scaled=f*original_den;assert scaled.denominator==1
        grid[i-low,j-low]=int(scaled)
    nt=6*B+1;nx=2*B+1;result=np.full((nt,nx),D//2,dtype=np.int64)
    positions=np.arange(-B,B+1,dtype=np.int64)[None,:]
    for start in range(0,3*B,64):
        times=np.arange(start,min(3*B,start+64),dtype=np.int64)[:,None]
        uu=times+positions;vv=times-positions
        i=uu//denweight;j=vv//denweight;a=uu%denweight;b=vv%denweight
        ii=i-low;jj=j-low
        f00=grid[ii,jj];f10=grid[ii+1,jj];f01=grid[ii,jj+1];f11=grid[ii+1,jj+1]
        missing10=f10<0;missing01=f01<0
        main=(i==j)|missing10|missing01
        first=np.where(main,a>=b,a+b<=denweight)
        first=np.where(missing10,False,np.where(missing01,True,first))
        first=np.where(f00<0,False,np.where(f11<0,True,first))
        w00=np.where(main,np.where(first,denweight-a,denweight-b),np.where(first,denweight-a-b,0))
        w10=np.where(main,np.where(first,a-b,0),np.where(first,a,denweight-b))
        w01=np.where(main,np.where(first,0,b-a),np.where(first,b,denweight-a))
        w11=np.where(main,np.where(first,b,a),np.where(first,0,a+b-denweight))
        total=np.zeros_like(f00)
        for weight,value in ((w00,f00),(w10,f10),(w01,f01),(w11,f11)):
            assert np.all(weight>=0) and not np.any((value<0)&(weight!=0))
            total+=weight*np.maximum(value,0)
        assert np.all(w00+w10+w01+w11==denweight)
        assert np.all((0<=total)&(total<=D))
        result[start:start+len(times)]=total
    common=gcd(int(np.gcd.reduce(result.reshape(-1))),D)
    if common>1:result//=common;D//=common
    assert D%2==0
    return B,D,result

def prepare(fieldpath,output,refinement=1):
    field=ExactField(fieldpath);B,D,values=exact_sample(field,refinement)
    probes=[]
    for n in sorted({0,1,B//3,B,2*B-1,2*B,3*B-1,3*B,6*B}):
        for j in sorted({-B,-B+1,-B//2,-1,0,1,B//2,B-1,B}):
            actual=Q(int(values[n,j+B]),D);expected=field.value(Q(n,B),Q(j,B))
            assert actual==expected,(n,j,actual,expected);probes.append((n,j))
    binary=Path(output).with_suffix('.input.bin')
    header=struct.pack('<IIIIQ',1,B,6*B+1,2*B+1,D)
    data=values.astype('<u8',copy=False).tobytes()
    binary.write_bytes(header+data)
    return binary,{'B':B,'n':B//2,'cdf_denominator':D,'refinement':refinement,
                   'sampled_values':int(values.size),'exact_sampling_spot_checks':len(probes),
                   'sampled_table_sha256':hashlib.sha256(header+data).hexdigest()}

def verify(fieldpath,output,refinement=1,keep_input=False,quiet=False):
    began=time.monotonic();fieldpath=Path(fieldpath);output=Path(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    binary,metadata=prepare(fieldpath,output,refinement)
    source=Path(__file__).with_suffix('.cpp');exe=source.with_suffix('')
    if not exe.exists() or exe.stat().st_mtime<source.stat().st_mtime:
        subprocess.run(['g++','-O3','-std=c++17',str(source),'-o',str(exe)],check=True)
    raw=output.with_suffix('.raw.json')
    subprocess.run([str(exe),str(binary),str(raw)],check=True,
                   stderr=subprocess.DEVNULL if quiet else None)
    result=json.loads(raw.read_text());result.update(metadata)
    lattice=Q(result['rounded_minimum_units'],result['cost_scale'])
    penalty=Q(1,result['B']);lower=lattice-penalty
    result.update({'scope':'Exact rounded-cost lower for center-by2 lattice Monsters; the global game-value lower uses the quantitative finite upper reduction. This is not a continuous-security claim for the supplied field.',
                   'field':str(fieldpath),'field_sha256':hashlib.sha256(fieldpath.read_bytes()).hexdigest(),
                   'verifier_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                   'lattice_lower':str(lattice),'lattice_lower_decimal':float(lattice),
                   'quantization_penalty':str(penalty),'global_value_lower':str(lower),
                   'global_value_lower_decimal':float(lower),'seconds':time.monotonic()-began})
    output.write_text(json.dumps(result,indent=2)+'\n')
    if not keep_input:binary.unlink()
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('field',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--refinement',type=int,default=1)
    parser.add_argument('--keep-input',action='store_true');args=parser.parse_args()
    answer=verify(args.field,args.output,args.refinement,args.keep_input)
    print(json.dumps({k:v for k,v in answer.items() if k!='layer_states'}),flush=True)
