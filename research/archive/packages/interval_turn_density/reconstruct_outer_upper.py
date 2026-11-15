#!/usr/bin/env python3
"""Reconstruct Ka/Kc upper densities on an actual supplied outer lower branch.

The source lower continuation is an experiment, not an exact lower law.
This diagnostic changes ell and g through the exact Volterra equations;
it does not retain an incompatible outer ell plateau.
"""
import argparse,json,math,sys
from pathlib import Path
import numpy as np
from scipy.interpolate import PchipInterpolator,PPoly
from scipy.optimize import brentq
from endpoint_tail import PowerLogTail
from fit_endpoint_tail import PairVolterra
from splice_endpoint_tail import TailFamily,Splice

class FrozenHistory:
    def __init__(self,data):
        self.data=data;self.p=np.array(data['powers']);self.w=np.array(data['w_coefficients'])
        self.blocks=[(b['hi'],{k:PPoly(np.array(b[k]),np.array(b['log_nodes']))for k in ['w','v']})for b in data['blocks']]
    def at(self,e,kind,der=0):
        if e<=self.data['delta']*(1+6e-8):
            if kind=='v':
                return e*e/16+(e**2.5/240 if self.data['particular']else 0.)
            coef=self.w*self.p if der else self.w
            return float(np.dot(coef,e**(self.p-der)))
        for hi,functions in self.blocks:
            if e<=hi*(1+6e-8):
                f=functions[kind];x=math.log(e)
                return float(f(x,1)/e if der else f(x))
        raise ValueError('Frozen history exhausted')


class JoinedFronts:
    def __init__(self,history,rows):
        self.history=history;self.rows=rows
        self.edge=rows[0]['x'];self.hi=rows[-1]['x']
        x=np.array([r['x']for r in rows])
        self.ds=PchipInterpolator(x,[1+r['c_high']for r in rows])
        self.hs=PchipInterpolator(x,[r['state'][0]for r in rows])

    def scalar(self,e,kind,derivative=False):
        if e<self.edge:return self.history.at(float(e),'w'if kind=='delta'else'v',int(derivative))
        fn=self.ds if kind=='delta'else self.hs
        return float(fn(e,int(derivative)))

    def delta(self,e,derivative=False):
        return np.vectorize(lambda t:self.scalar(t,'delta',derivative),otypes=[float])(e)

    def eta(self,e):return np.vectorize(lambda t:self.scalar(t,'eta'),otypes=[float])(e)

    def inverse_delta(self,values):
        def one(value):
            guess=(value/4)**2
            lo=math.log(max(1e-300,guess/20));hi=math.log(min(self.hi,guess*20))
            if self.scalar(math.exp(hi),'delta')<value:hi=math.log(self.hi)
            return math.exp(brentq(lambda l:self.scalar(math.exp(l),'delta')-value,lo,hi,xtol=2e-12))
        return np.vectorize(one,otypes=[float])(values)


class GlobalPair:
    def __init__(self,splice):
        self.splice=splice;self.base=PowerLogTail()
        self.terms=[(0.,1.)];self.coefficients=[splice.B]
    def density(self,e):return np.vectorize(lambda t:self.splice.density('p',float(t)),otypes=[float])(e)
    def primitive(self,e):return np.vectorize(lambda t:self.splice.primitive('P',float(t)),otypes=[float])(e)


class OuterVolterra(PairVolterra):
    def __init__(self,pair,fronts,w0):
        self.pair=pair;self.fronts=fronts;self.endpoint_mass=w0;self.base=pair.base
        self.cutoff=fronts.hi
        eps=np.r_[np.geomspace(1e-44,fronts.edge,420),[r['x']for r in fronts.rows]]
        self.x=np.unique(np.sort(self.base.coordinate(eps)));self.eps=16*np.exp(-self.x)
        e=self.eps;d=fronts.delta(e);h=fronts.eta(e);r=fronts.inverse_delta(e);hr=fronts.eta(r)
        self.ell_ref=self.base.ell(e);p=pair.density(e);Pr=pair.primitive(r)
        self.ratio=(d+h)*p/(8*self.ell_ref);self.limit=float(pair.coefficients[0])
        for n in range(24):
            self._interpolant=PchipInterpolator(self.x,self.ratio)
            g=(w0+Pr+self.ell_primitive(hr)-(e+hr)*p)/(8-2*e)
            updated=((d+h)*p-e*g+self.ell_primitive(e)-self.ell_primitive(h))/((8-2*e)*self.ell_ref)
            error=float(abs(updated-self.ratio).max());self.ratio=updated
            if error<2e-13:break
        self.iterations=n+1;self.iteration_error=error
        self._interpolant=PchipInterpolator(self.x,self.ratio)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',default='outer_lower_input.json')
    args=ap.parse_args()
    here=Path(__file__).resolve().parent
    data=json.loads((here/args.input).read_text())
    history=FrozenHistory(data);fronts=JoinedFronts(history,data['rows'])
    seed=json.loads((here/'split_edge_affine_discovery.json').read_text())
    splice_data=json.loads((here/'endpoint_tail_splice.json').read_text())['matches'][1]
    family=TailFamily();law=Splice(seed,family,splice_data['amplitude'],splice_data['ell_cutoff_deficit'])
    result=OuterVolterra(GlobalPair(law),fronts,seed['endpoint_mass'])
    rows=[]
    for low in data['rows'][::12]+data['rows'][-1:]:
        e=low['x'];h=float(fronts.eta(e));d=float(fronts.delta(e))
        expected=(law.primitive('P',d)-law.primitive('P',e))/(d-e)
        rows.append(dict(a=1-e,c=d-1,incoming_defect=h,
            ell_at_initial=float(result.ell(e)),seed_ell_at_initial=law.base_density('ell',e),
            ell_at_incoming=float(result.ell(h)),required_ell_by_Ku=expected,
            upper_Ku4=float(result.ku(e)),
            f_initial=float(result.f(e)),g_initial=float(result.g(e)),
            low_C=low['C'],low_initial=low['a_low']))
    probes=np.geomspace(fronts.hi,1e-20,600)
    values=result.ell(probes)
    out=dict(scope='Exact Ka/Kc Volterra reconstruction on a supplied numerical lower continuation; Ku and global law constraints remain diagnostics.',
        source_lower=args.input,
        amplitude=law.B,endpoint_mass=seed['endpoint_mass'],initial_range=[1-fronts.hi,1-fronts.edge],
        terminal_k_seed_at_15_16=float(seed['densities']['k'][8]),
        minimum_reconstructed_ell=float(min(values)),
        ell_nondecreasing_on_probe=bool(np.all(np.diff(values)>=-1e-9)),
        maximum_ell_decrease_on_probe=float(max(0.,-min(np.diff(values)))),
        ku_max_absolute=max(abs(r['upper_Ku4'])for r in rows),
        iterations=result.iterations,iteration_error=result.iteration_error,rows=rows)
    dest=here/'outer_upper_reconstruction.json';dest.write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items()if k!='rows'},indent=2))
    print('ENTRY',json.dumps(rows[0]));print('EXIT',json.dumps(rows[-1]));print('OUTPUT',dest)

if __name__=='__main__':main()
