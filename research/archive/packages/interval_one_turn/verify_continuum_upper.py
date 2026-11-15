#!/usr/bin/env python3
"""Independent rational residual repair of a continuum S/P_b P2 candidate.

Uses only the standard library. Reconstructs physical costs, geometry, and
Bernstein inequalities from a rounded law and P2 nodal values; auxiliary CDF
variables and saved optimizer residuals are ignored. Present scope: 0<b<2, with exact initial bonuses for r>=b.
"""
from __future__ import annotations
import argparse
from bisect import bisect_right
from decimal import Decimal, ROUND_HALF_EVEN
from fractions import Fraction as Q
from functools import lru_cache
import gzip
import hashlib
import json
from math import comb
from pathlib import Path
import time

TARGET = Q(291849329389899, 204800000000000)


def qbern(values):
    a,m,b=values
    return (a,2*m-(a+b)/2,b)


def round_integer(x, scale):
    return int((Decimal(str(x))*scale).to_integral_value(rounding=ROUND_HALF_EVEN))


class Replay:
    def __init__(self, data, digits=14):
        self.data=data
        self.n,self.m,self.d=map(int,(data['n'],data['r_bins'],data['density_n']))
        n=self.n
        assert n>0 and self.m>0 and self.d>0 and n%self.m==0 and self.m%self.d==0
        self.knots=tuple(map(Q,data['positive_knots_exact']))
        assert len(self.knots)==n+1 and self.knots[0]==0 and self.knots[-1]==1
        assert all(a<b for a,b in zip(self.knots,self.knots[1:]))
        self.bs=tuple(map(Q,data['b_levels_exact']))
        assert self.bs==tuple(sorted(set(self.bs))) and all(0<b<2 for b in self.bs)
        self.levels=tuple(sorted(set((Q(1),)+self.bs)))
        self.ranks={b:i+1 for i,b in enumerate(self.levels)}
        self.boundaries=[]
        for b in self.levels:
            ix=[i for i in range(0,2*n) if self.coord(i)==b]
            assert len(ix)==1
            self.boundaries.append(ix[0])
        self.edges=tuple(self.coord(-n+j*(n//self.d)) for j in range(2*self.d+1))
        self.rs=tuple(self.coord(j*(n//self.m)) for j in range(self.m+1))
        assert list(map(str,self.edges))==data['density_edges_exact']
        assert list(map(str,self.rs))==data['r_knots_exact']
        self.integer_input=data.get('format')=='one-turn-continuum-potential-v1'
        self.scale=int(data['rounding_scale']) if self.integer_input else 10**digits
        assert self.scale>0
        raw=(list(map(int,data['solution_integer_numerators'])) if self.integer_input
             else list(map(lambda x:round_integer(x,self.scale),data['solution'])))
        self.pi_offsets=[2+2*self.d*(i+1) for i in range(len(self.bs))]
        assert self.pi_offsets==data['pi_offsets']
        self.mass_end=2+2*self.d*(1+len(self.bs))
        if self.integer_input:assert all(z>=0 for z in raw[1:self.mass_end])
        self.masses=[max(0,z) for z in raw[1:self.mass_end]]
        self.removed_unsupported=0
        for b,offset in zip(self.bs,self.pi_offsets):
            begin,end=-min(b,Q(1)),min(b,2-b,Q(1))
            for j,(lo,hi) in enumerate(zip(self.edges,self.edges[1:])):
                assert not (lo<begin<hi or lo<end<hi)
                if lo<begin or hi>end:
                    if self.integer_input:assert self.masses[offset+j-1]==0
                    self.removed_unsupported+=self.masses[offset+j-1]
                    self.masses[offset+j-1]=0
        self.den=sum(self.masses)
        assert self.den>0
        if self.integer_input:assert self.den==int(data['normalizing_integer'])
        self.endpoint=self.masses[0]
        self.sigma=self.masses[1:1+2*self.d]
        self.pi={b:self.masses[offset-1:offset-1+2*self.d]
                 for b,offset in zip(self.bs,self.pi_offsets)}
        self.totals={b:sum(values) for b,values in self.pi.items()}
        self.family={None:self.sigma,**self.pi}
        self.prefix={family:[0] for family in self.family}
        for family,values in self.family.items():
            for z in values:self.prefix[family].append(self.prefix[family][-1]+z)
        self.primitive=[Q(0)]
        for mass,lo,hi in zip(self.sigma,self.edges,self.edges[1:]):
            self.primitive.append(self.primitive[-1]+mass*(1-(lo+hi)/2))
        self.raw_C=raw[0]
        self.triangles=[]
        nodes={}
        for i in range(3*n):
            for j in range(-n,2*n):
                a,b,c,d=(i,j),(i+1,j),(i,j+1),(i+1,j+1)
                cells=((a,b,d),(a,d,c)) if i-j in (0,2*n) else ((a,b,c),(d,c,b))
                for points in cells:
                    if not all(self.admissible(*p) for p in points):continue
                    physical=[(self.coord(u),self.coord(w)) for u,w in points]
                    assert all(0<=u-w<=2 and 0<=u+w<=4 for u,w in physical)
                    us=sum(u for u,w in physical);ws=sum(w for u,w in physical)
                    key=(sum(us>3*b for b in self.levels),sum(ws>3*b for b in self.levels))
                    local=tuple((2*u,2*w) for u,w in points)+tuple(
                        (points[a][0]+points[b][0],points[a][1]+points[b][1])
                        for a,b in ((0,1),(1,2),(2,0)))
                    nodes.setdefault(key,set()).update(local)
                    (u0,w0),(u1,w1),(u2,w2)=physical
                    det=(u1-u0)*(w2-w0)-(u2-u0)*(w1-w0)
                    assert det!=0
                    grads=(((w1-w2)/det,(u2-u1)/det),
                           ((w2-w0)/det,(u0-u2)/det),
                           ((w0-w1)/det,(u1-u0)/det))
                    derivs=[]
                    for k in range(3):
                        dirs=[]
                        for direction in (0,1):
                            g=[v[direction] for v in grads]
                            coeff=[(3 if v==k else -1)*g[v] for v in range(3)]
                            coeff.extend(4*((g[a] if b==k else 0)+(g[b] if a==k else 0))
                                         for a,b in ((0,1),(1,2),(2,0)))
                            dirs.append(tuple(coeff))
                        derivs.append(tuple(dirs))
                    self.triangles.append((key,points,physical,local,tuple(derivs)))
        assert len(self.triangles)==8*n*n
        self.keys=sorted(nodes)
        assert [list(k) for k in self.keys]==data['phase_keys']
        expected=[[list(p) for p in sorted(nodes[k])] for k in self.keys]
        assert expected==data['phase_nodes_doubled_grid']
        self.local={};total=0
        for key in self.keys:
            self.local[key]={p:total+j for j,p in enumerate(sorted(nodes[key]))}
            total+=len(nodes[key])
        self.per_r=total
        assert total==data['per_r']
        start=int(data['potential_start'])
        assert start>=self.mass_end and len(raw)==start+(self.m+1)*total
        self.pot=raw[start:]
        self.residual={'hjb':Q(0),'initial':Q(0)}
        self.terminal={key:Q(0) for key in self.keys}
        self.interfaces={}
        self.witness={}
        self.counts={name:0 for name in ('hjb','u_jump','w_transition','terminal','initial_cubic')}

    def freeze(self):
        return {'format':'one-turn-continuum-potential-v1',
                'n':self.n,'r_bins':self.m,'density_n':self.d,
                'b_levels_exact':list(map(str,self.bs)),
                'positive_knots_exact':list(map(str,self.knots)),
                'density_edges_exact':list(map(str,self.edges)),
                'r_knots_exact':list(map(str,self.rs)),
                'phase_keys':[list(k) for k in self.keys],
                'phase_nodes_doubled_grid':[[list(p) for p in sorted(self.local[k])] for k in self.keys],
                'pi_offsets':self.pi_offsets,'potential_start':self.mass_end,'per_r':self.per_r,
                'rounding_scale':str(self.scale),'normalizing_integer':str(self.den),
                'solution_integer_numerators':list(map(str,[self.raw_C]+self.masses+self.pot))}

    @lru_cache(None)
    def coord(self,i):
        n=self.n
        period=(i+n)//(2*n)
        reduced=i-2*n*period
        return 2*period+(self.knots[reduced] if reduced>=0 else -self.knots[-reduced])

    @lru_cache(None)
    def midpoint(self,i):
        return (self.coord(i//2)+self.coord((i+1)//2))/2

    def admissible(self,u,w):
        return 0<=u-w<=2*self.n and 0<=u+w<=4*self.n

    @lru_cache(None)
    def cdf(self,z,family=None):
        z=Q(z)
        if z<=-1:return Q(0)
        if z>=1:return Q(self.prefix[family][-1])
        j=bisect_right(self.edges,z)-1
        return self.prefix[family][j]+self.family[family][j]*(z-self.edges[j])/(self.edges[j+1]-self.edges[j])

    @lru_cache(None)
    def moment(self,z):
        z=Q(z)
        if z<=-1:return Q(0)
        if z>=1:return self.primitive[-1]
        j=bisect_right(self.edges,z)-1
        lo,hi=self.edges[j:j+2]
        return self.primitive[j]+self.sigma[j]*((z-z*z/2)-(lo-lo*lo/2))/(hi-lo)

    def value(self,ri,key,node):
        return self.pot[ri*self.per_r+self.local[key][node]]

    def cost(self,r,key,U,W):
        iu,iw=key
        z=(self.cdf(-U)+self.cdf(-W)+max(Q(0),self.cdf(2-U)-self.cdf(r))
           +self.cdf(2-W)-self.cdf(-r))
        er=self.ranks[Q(1)]
        z+=self.endpoint*((iu<er)+(iw<er))
        for b in self.bs:
            rank=self.ranks[b];M=self.totals[b]
            if iu<rank:z+=2*M-self.cdf(r,b)-self.cdf(-r,b)+self.cdf(-U,b)+self.cdf(-W,b)
            elif iw<rank:z+=M-self.cdf(-r,b)
        return z

    def terminal_cost(self,r,key,s):
        return self.moment(s)-self.moment(-r)+sum(
            (b-1)*(self.totals[b]-self.cdf(-r,b))
            for b in self.bs if key[1]<self.ranks[b])

    def record(self,kind,residual,witness):
        self.counts['initial_cubic' if kind=='initial' else kind]+=1
        if residual>self.residual[kind]:
            self.residual[kind]=residual;self.witness[kind]=witness

    def run(self,progress=False):
        n=self.n
        started=time.monotonic()
        for ri,r in enumerate(self.rs):
            costs={}
            for ti,(key,points,physical,local,derivs) in enumerate(self.triangles):
                yy=[self.value(ri,key,node) for node in local]
                for k,((u,w),(U,W)) in enumerate(zip(points,physical)):
                    ck=(key,u,w)
                    if ck not in costs:costs[ck]=self.cost(r,key,U,W)
                    g=costs[ck]
                    for direction in (0,1):
                        z=2*sum(c*y for c,y in zip(derivs[k][direction],yy))+g
                        self.record('hjb',z,[ri,ti,k,direction])
            for rank,(b,boundary) in enumerate(zip(self.levels,self.boundaries),1):
                for j in range(-n,2*n):
                    if not(self.admissible(boundary,j) and self.admissible(boundary,j+1)):continue
                    iw=sum(2*j+1>2*k for k in self.boundaries)
                    pre,post=(rank-1,iw),(rank,iw)
                    if pre not in self.local or post not in self.local:continue
                    vals=[]
                    for jj in (2*j,2*j+1,2*j+2):
                        node=(2*boundary,jj);W=self.midpoint(jj)
                        jump=(b+3-(b+W)/2)*self.cdf(-W,b) if b in self.pi else Q(0)
                        vals.append(jump+self.value(ri,post,node)-self.value(ri,pre,node))
                    residual=max(Q(0),*qbern(vals))
                    self.interfaces[(pre,post)]=max(self.interfaces.get((pre,post),Q(0)),residual)
                    self.counts['u_jump']+=3
                for i in range(3*n):
                    if not(self.admissible(i,boundary) and self.admissible(i+1,boundary)):continue
                    iu=sum(2*i+1>2*k for k in self.boundaries)
                    pre,post=(iu,rank-1),(iu,rank)
                    if pre not in self.local or post not in self.local:continue
                    vals=[Q(self.value(ri,post,(ii,2*boundary))-self.value(ri,pre,(ii,2*boundary)))
                          for ii in (2*i,2*i+1,2*i+2)]
                    residual=max(Q(0),*qbern(vals))
                    self.interfaces[(pre,post)]=max(self.interfaces.get((pre,post),Q(0)),residual)
                    self.counts['w_transition']+=3
            for j in range(n):
                key=(sum(4*n+2*j+1>2*k for k in self.boundaries),
                     sum(4*n-2*j-1>2*k for k in self.boundaries))
                vals=[self.terminal_cost(r,key,self.midpoint(s))-self.value(ri,key,(4*n+s,4*n-s))
                      for s in (2*j,2*j+1,2*j+2)]
                self.terminal[key]=max(self.terminal[key],*qbern(vals))
                self.counts['terminal']+=3
            if progress:print(json.dumps({'stage':'exact_radius','completed':ri+1,'total':len(self.rs),
                                          'seconds':time.monotonic()-started}),flush=True)
        refinement=n//self.m
        for j in range(n):
            initial_key=(sum(2*j+1>2*k for k in self.boundaries),0)
            bonus=sum((b+3)*self.totals[b] for b in self.bs if initial_key[0]>=self.ranks[b])
            ri=j//refinement
            lo,hi=self.rs[ri:ri+2]
            theta=((self.coord(j)-lo)/(hi-lo),(self.coord(j+1)-lo)/(hi-lo))
            nodes=[(2*j,-2*j),(2*j+1,-2*j-1),(2*j+2,-2*j-2)]
            left=qbern([Q(self.value(ri,initial_key,node)) for node in nodes])
            right=qbern([Q(self.value(ri+1,initial_key,node)) for node in nodes])
            for degree in range(4):
                z=Q(-2*self.raw_C)+bonus
                for k in range(3):
                    h=degree-k
                    if h in (0,1):
                        z+=Q(comb(2,k),comb(3,degree))*((1-theta[h])*left[k]+theta[h]*right[k])
                self.record('initial',z,[j,degree])
        beta={}
        for key in sorted(self.keys,key=lambda k:sum(k),reverse=True):
            beta[key]=max(Q(0),self.terminal[key],*(res+beta[post]
                          for (pre,post),res in self.interfaces.items() if pre==key))
        initial_keys={(sum(2*j+1>2*k for k in self.boundaries),0) for j in range(n)}
        beta_initial=max(beta[key] for key in initial_keys)
        repair=self.residual['hjb']+(beta_initial+self.residual['initial'])/2
        upper=(self.raw_C+repair)/self.den
        baseline=Q(self.endpoint)+sum(m*(2-(lo+hi)/2)
                     for m,lo,hi in zip(self.sigma,self.edges,self.edges[1:]))
        baseline+=sum((b+2)*self.totals[b] for b in self.bs)
        baseline/=self.den
        assert upper>=baseline, 'physical endpoint lower test exceeds repaired bound'
        return {'scope':'exact repaired continuum S/P_b all-Princess upper; 0<b<2 HJB theorem with initial bonuses',
                'upper':str(upper),'upper_decimal':float(upper),'frozen_benchmark':str(TARGET),
                'gap_above_frozen':str(upper-TARGET),'passes_counterexample_gate':upper<=TARGET,
                'raw_rounded_C':str(Q(self.raw_C,self.den)),
                'repair':str(repair/self.den),'endpoint_baseline':str(baseline),
                'rounding_scale':str(self.scale),'normalizing_integer':str(self.den),
                'removed_unsupported_raw_mass':str(self.removed_unsupported),
                'hjb_residual':str(self.residual['hjb']/self.den),
                'initial_residual':str(self.residual['initial']/self.den),
                'maximum_initial_phase_offset':str(beta_initial/self.den),
                'phase_offsets':{str(k):str(v/self.den) for k,v in beta.items()},
                'terminal_residuals':{str(k):str(v/self.den) for k,v in self.terminal.items()},
                'interface_residuals':{str(k):str(v/self.den) for k,v in self.interfaces.items()},
                'counts':self.counts,'worst_witnesses':self.witness,
                'law':{'endpoint_mass':str(Q(self.endpoint,self.den)),
                       'sigma_bin_masses':[str(Q(z,self.den)) for z in self.sigma],
                       'pi_bin_masses_by_level':{str(b):[str(Q(z,self.den)) for z in values]
                                                for b,values in self.pi.items()}},
                'seconds':time.monotonic()-started}



def self_test():
    from copy import deepcopy
    path=Path(__file__).with_name('continuum_endpoint_fixture.json.gz')
    data=json.loads(gzip.decompress(path.read_bytes()))
    report=Replay(data).run()
    assert report['upper']=='3/2' and report['repair']=='0'
    assert not report['passes_counterexample_gate']
    frozen=Replay(data).freeze()
    exact=Replay(frozen).run()
    assert exact['upper']==report['upper'] and exact['repair']=='0'
    bad_C=deepcopy(data)
    bad_C['solution'][0]=1
    corrected=Replay(bad_C).run()
    assert corrected['upper']=='3/2' and Q(corrected['initial_residual'])==1
    bad_node=deepcopy(data)
    bad_node['solution'][bad_node['potential_start']]+=1
    corrected=Replay(bad_node).run()
    assert Q(corrected['upper'])>=Q(3,2) and Q(corrected['repair'])>0
    malformed=[]
    negative_mass=deepcopy(frozen)
    negative_mass['solution_integer_numerators'][2]='-1'
    malformed.append(negative_mass)
    wrong_knots=deepcopy(data)
    wrong_knots['positive_knots_exact'][1]='0'
    malformed.append(wrong_knots)
    wrong_nodes=deepcopy(data)
    wrong_nodes['phase_nodes_doubled_grid'][0][-1]=wrong_nodes['phase_nodes_doubled_grid'][0][0]
    malformed.append(wrong_nodes)
    wrong_phase=deepcopy(data)
    wrong_phase['phase_keys'][0]=[0,1]
    malformed.append(wrong_phase)
    rejected=0
    for candidate in malformed:
        try:Replay(candidate)
        except (AssertionError,ValueError,KeyError):rejected+=1
        else:raise AssertionError('malformed geometry accepted')
    print(json.dumps({'endpoint_exact_upper':'3/2','endpoint_repair':'0',
                      'residual_repair_controls':2,'malformed_inputs_rejected':rejected,
                      'counterexample_gate':False}))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,nargs='?')
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--digits',type=int,default=14)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--freeze-output',type=Path,help='save canonical integer input; optional .gz suffix')
    parser.add_argument('--progress',action='store_true')
    parser.add_argument('--require-counterexample',action='store_true')
    args=parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.input is None:parser.error('input is required unless --self-test is selected')
    raw=args.input.read_bytes()
    data=json.loads(gzip.decompress(raw) if args.input.suffix=='.gz' else raw)
    replay=Replay(data,args.digits)
    if args.freeze_output:
        payload=json.dumps(replay.freeze(),separators=(',',':')).encode()
        if args.freeze_output.suffix=='.gz':payload=gzip.compress(payload,mtime=0)
        args.freeze_output.write_bytes(payload)
    report=replay.run(args.progress)
    report['input_sha256']=hashlib.sha256(raw).hexdigest()
    if args.output:args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    if args.require_counterexample and not report['passes_counterexample_gate']:
        raise SystemExit('Exact repaired upper remains above the frozen benchmark')


if __name__=='__main__':main()
