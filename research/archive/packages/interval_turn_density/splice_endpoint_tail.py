#!/usr/bin/env python3
"""Actual seed-density splice and full high-negative-c stationarity audit.

This evaluates the unchanged outer primitives together with the analytic
tail; it is not another local tail refinement or a complete response bound.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq,least_squares
from endpoint_tail import PowerLogTail
from fit_endpoint_tail import FractionalFronts,PairDensity,PairVolterra


class TailFamily:
    def __init__(self):
        self.fronts=FractionalFronts();self.T=1e-5
        self.scale=float(self.fronts.delta(self.T))
        self.terms=[(0.,1.),(1/3,2.),(.5,1.),(.75,1.),(.875,1.),(1.,1.),(1.25,1.),(1.5,1.)]
        probes=np.geomspace(self.T,1e-16,80)
        denom=self.fronts.delta(probes)*PowerLogTail().ell(self.fronts.eta(probes))
        models=[]
        for j in range(len(self.terms)):
            c=np.zeros(len(self.terms));c[j]=1
            models.append(PairVolterra(PairDensity(self.terms,c,self.scale),self.fronts,0.,self.T))
        source=PairVolterra(PairDensity(self.terms,np.zeros(len(self.terms)),self.scale),self.fronts,1.,self.T)
        cols=np.array([m.ku(probes)/denom for m in models]).T
        self.coef_B=np.r_[1.,np.linalg.lstsq(cols[:,1:],-cols[:,0],rcond=1e-12)[0]]
        self.coef_w=np.r_[0.,np.linalg.lstsq(cols[:,1:],-source.ku(probes)/denom,rcond=1e-12)[0]]
        self.Bmodel=PairVolterra(PairDensity(self.terms,self.coef_B,self.scale),self.fronts,0.,self.T)
        self.Wmodel=PairVolterra(PairDensity(self.terms,self.coef_w,self.scale),self.fronts,1.,self.T)

    def get(self,what,e,B,w):
        if what=='p':return B*self.Bmodel.pair.density(e)+w*self.Wmodel.pair.density(e)
        if what=='P':return B*self.Bmodel.pair.primitive(e)+w*self.Wmodel.pair.primitive(e)
        if what=='L':return B*self.Bmodel.ell_primitive(e)+w*self.Wmodel.ell_primitive(e)
        return B*getattr(self.Bmodel,what)(e)+w*getattr(self.Wmodel,what)(e)


class Splice:
    def __init__(self,seed,family,B,T):
        self.knots=np.array(seed['knots']);self.dens={k:np.array(v)for k,v in seed['densities'].items()}
        self.dens['p']=self.dens['f']+self.dens['g']
        self.family=family;self.B=B;self.T=T;self.cut=float(family.fronts.delta(T));self.w=seed['endpoint_mass']
        self.norm=self.w+sum(self.base_integral(k,0.,1.)for k in ['p','k'])
        self.norm+=float(family.get('P',self.cut,B,self.w))-self.base_integral('p',0,self.cut)
        self.norm+=float(family.get('L',T,B,self.w))-self.base_integral('ell',0,T)

    def base_density(self,kind,e):
        j=max(0,min(len(self.knots)-2,np.searchsorted(self.knots,1-e,side='right')-1))
        return float(self.dens[kind][j])

    def base_integral(self,kind,lo,hi):
        return sum(float(h)*max(0.,min(hi,1-self.knots[j])-max(lo,1-self.knots[j+1]))
                   for j,h in enumerate(self.dens[kind]))

    def density(self,kind,e):
        cutoff=self.T if kind=='ell' else self.cut
        if e<=cutoff:return float(self.family.get(kind,e,self.B,self.w))
        return self.base_density(kind,e)

    def primitive(self,kind,e):
        if e==0:return 0.
        cutoff=self.T if kind=='L' else self.cut
        base='ell'if kind=='L'else'p'
        return float(self.family.get(kind,min(e,cutoff),self.B,self.w))+self.base_integral(base,cutoff,e)

    def best_h(self,e,d):
        if d<=e*(1+1e-12):return e
        mean=(self.primitive('P',d)-self.primitive('P',e))/(d-e)
        if mean<=self.density('ell',e):return e
        if mean>self.density('ell',self.T):
            return math.exp(brentq(lambda l:math.log(self.density('ell',math.exp(l)))-math.log(mean),
                                   math.log(1e-200),math.log(self.T),xtol=2e-12))
        for j,h in enumerate(self.dens['ell']):
            if h>=mean and self.knots[j]>1-e:return 1-self.knots[j]
        return self.T

    def residuals(self,e,d,h=None):
        if h is None:h=self.best_h(e,d)
        f,g=self.density('f',e),self.density('g',e)
        ka=-(d+h)*f+(e-h-d)*g+(8-2*e)*self.density('ell',e)-self.primitive('L',e)+self.primitive('L',h)
        ku=self.primitive('P',d)-self.primitive('P',e)-(d-e)*self.density('ell',h)
        kc=self.w+self.primitive('P',e)+self.primitive('L',h)-(d+h)*self.density('f',d)-(8-d+h)*self.density('g',d)
        return dict(a=1-e,c=-1+d,initial_defect=e,incoming_defect=h,
            Ka4=float(ka/self.norm),Ku4=float(ku/self.norm),Kc4=float(kc/self.norm),
            f_a=f/self.norm,g_a=g/self.norm,ell_a=self.density('ell',e)/self.norm,
            ell_u=self.density('ell',h)/self.norm)

    def c_stationary(self,e):
        knots=sorted(set([e,1.,self.cut]+[1-x for x in self.knots if e<1-x<1]))
        out=[]
        for lo,hi in zip(knots,knots[1:]):
            a=lo+max(1e-13,(hi-lo)*1e-8);b=hi-max(1e-13,(hi-lo)*1e-8)
            if b<=a:continue
            fa=self.residuals(e,a)['Kc4'];fb=self.residuals(e,b)['Kc4']
            if fa>0>fb:
                root=brentq(lambda d:self.residuals(e,d)['Kc4'],a,b,xtol=2e-12)
                out.append(dict(kind='smooth local c maximum',**self.residuals(e,root)))
        for d in knots[1:-1]:
            gap=min(1e-9,(d-e)/100,(1-d)/100)
            if gap>0 and self.residuals(e,d-gap)['Kc4']>=0>=self.residuals(e,d+gap)['Kc4']:
                out.append(dict(kind='density-knot c maximum',**self.residuals(e,d)))
        return out


def main():
    here=Path(__file__).resolve().parent
    seed=json.loads((here/'split_edge_affine_discovery.json').read_text());family=TailFamily();w=seed['endpoint_mass']
    placeholder=Splice(seed,family,.055,1e-5)
    matches=[]
    for kind in ['p','f']:
        target=placeholder.dens[kind][-1];targetell=placeholder.dens['ell'][-1]
        def fun(v):
            B,T=v[0],math.exp(v[1]);cut=float(family.fronts.delta(T))
            return [float(family.get(kind,cut,B,w))/target-1,
                    float(family.get('ell',T,B,w))/targetell-1]
        solved=least_squares(fun,[.053,math.log(8e-6)],bounds=([.001,math.log(1e-9)],[1.,math.log(1e-5)]),
                             xtol=1e-13,ftol=1e-13,gtol=1e-13)
        B,T=float(solved.x[0]),math.exp(solved.x[1]);law=Splice(seed,family,B,T)
        d=law.cut
        item=dict(match=kind,amplitude=B,ell_cutoff_deficit=T,fg_cutoff_deficit=d,
            matching_residual=fun(solved.x),normalization_before_rescaling=law.norm,
            endpoint_mass_after_rescaling=w/law.norm,
            f_join_jump=law.density('f',d)-law.base_density('f',d),
            p_join_jump=law.density('p',d)-law.base_density('p',d),
            g_tail_positive=bool(np.all(family.get('g',np.geomspace(d,1e-30,100),B,w)>0)))
        W=w+law.primitive('P',1.)
        cap=math.exp(brentq(lambda l:2*law.density('ell',math.exp(l))-law.primitive('L',math.exp(l))-W,
                           math.log(1e-100),math.log(T)))
        item['cmax_deficit']=cap
        item['branches']={str(a):law.c_stationary(1-a)for a in [.985,.99,.991696693624,.995,.999,.99999,.999999]}
        item['lower_agent_entry']=law.residuals(1-.991696693624,1-.585131232)
        matches.append(item)
        print('MATCH',json.dumps(item),flush=True)
    output=dict(scope='Actual seed-primitive splice and high-negative-c response diagnostics; no full response bound.',
        coefficient_B=family.coef_B.tolist(),coefficient_w0=family.coef_w.tolist(),matches=matches)
    dest=here/'endpoint_tail_splice.json';dest.write_text(json.dumps(output,indent=2));print('OUTPUT',dest)

if __name__=='__main__':main()
