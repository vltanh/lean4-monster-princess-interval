#!/usr/bin/env python3
"""Fit full upper tail stationarity to corrected analytic lower front data.

The primary density is p=f+g.  For any p, a scalar retarded Volterra
equation determines ell, and the c equation then determines g exactly.
Only the free-u equation remains to fit.  This program uses a short
analytic power/pantograph basis, not step densities or endpoint atoms.

The lower front series is an asymptotic history, not an exact solution.
This is a local candidate construction and must not be read as a game
bound or an attachment/existence proof.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
from scipy.optimize import lsq_linear

from endpoint_tail import GAMMA,PowerLogTail,modulation


class FractionalFronts:
    """The audited lower-history correction, including all exponents <1."""
    def __init__(self,terms=36,corrected=True):
        self.corrected=corrected
        exponents=[.5];coeff=[4.];d=1.
        if corrected:
            for n in range(1,terms+1):
                e=(1-2.**(-n))/2
                d=-16.**e/(4*(1+e))*d
                exponents.append(.5+e);coeff.append(-4*(1+2*e)*d)
        self.exponents=np.array(exponents);self.coeff=np.array(coeff)

    def delta(self,eps,derivative=False):
        eps=np.asarray(eps,dtype=float)
        if derivative:
            return eps[...,None]**(self.exponents-1)@(self.coeff*self.exponents)+(88/125 if self.corrected else 0.)
        return eps[...,None]**self.exponents@self.coeff+(88/125*eps if self.corrected else 0.)

    def eta(self,eps):
        eps=np.asarray(eps,dtype=float)
        return eps**2/16*(1+np.sqrt(eps)/15 if self.corrected else 1.)

    def inverse_delta(self,value):
        value=np.asarray(value,dtype=float)
        loge=2*(np.log(value)-math.log(4.))
        for _ in range(12):
            e=np.exp(loge);d=self.delta(e)
            correction=np.log(d/value)/(e*self.delta(e,True)/d)
            loge-=correction
            if float(np.max(abs(correction)))<2e-14:break
        return np.exp(loge)


class PairDensity:
    """A linear combination eps^(-2/3+alpha) H(scale*log(16/eps))."""
    def __init__(self,terms,coefficients,scale_deficit):
        self.terms=list(terms);self.coefficients=np.asarray(coefficients,dtype=float)
        self.scale_deficit=scale_deficit
        self.base=PowerLogTail()

    def density(self,eps):
        e=np.asarray(eps,dtype=float);x=self.base.coordinate(e)
        result=np.zeros_like(e)
        for (alpha,scale),coefficient in zip(self.terms,self.coefficients):
            if coefficient:
                result+=coefficient*e**(-2/3)*(e/self.scale_deficit)**alpha*modulation(scale*x)/scale**GAMMA
        return result

    def primitive(self,eps):
        e=np.asarray(eps,dtype=float);x=self.base.coordinate(e)
        result=np.zeros_like(e)
        for (alpha,scale),coefficient in zip(self.terms,self.coefficients):
            if coefficient:
                rate=1/3+alpha
                integral=modulation(scale*(x[...,None]+self.base.nodes/rate))@self.base.weights/rate
                result+=coefficient*e**rate/self.scale_deficit**alpha/scale**GAMMA*integral
        return result

    def primitive_quad(self,eps):
        """Independent adaptive evaluation of the analytic primitive."""
        x=float(self.base.coordinate(eps));result=0.
        for (alpha,scale),coefficient in zip(self.terms,self.coefficients):
            if coefficient:
                rate=1/3+alpha
                integral=quad(lambda r:math.exp(-rate*r)*float(modulation(scale*(x+r))),
                    0,np.inf,epsabs=2e-12,epsrel=2e-12)[0]
                result+=coefficient*eps**rate/self.scale_deficit**alpha/scale**GAMMA*integral
        return result


class PairVolterra:
    """Linear exact Ka/Kc reduction for arbitrary supplied front maps.

    Let P be the primitive of p=f+g, Lambda the primitive of ell,
    r=delta^{-1}, and eta the incoming defect.  Then

      g(t)=[w0+P(r(t))+Lambda(eta(r(t)))
               -(t+eta(r(t)))p(t)]/(8-2t),
      ell(t)=[(delta(t)+eta(t))p(t)-t*g(t)
               +Lambda(t)-Lambda(eta(t))]/(8-2t).

    These are genuinely retarded equations: r(t),eta(t)<t in this tail.
    They are linear in p and w0 and have a small Volterra operator norm.
    """
    def __init__(self,pair,fronts,endpoint_mass,cutoff=1e-5,nodes=385,log_horizon=112.):
        self.pair=pair;self.fronts=fronts;self.endpoint_mass=endpoint_mass
        self.base=pair.base;self.cutoff=cutoff
        self.x=np.linspace(float(self.base.coordinate(cutoff)),log_horizon,nodes)
        self.eps=16*np.exp(-self.x)
        e=self.eps;d=fronts.delta(e);h=fronts.eta(e);r=fronts.inverse_delta(e);hr=fronts.eta(r)
        self.ell_ref=self.base.ell(e)
        p=pair.density(e);Pr=pair.primitive(r)
        self.ratio=(d+h)*p/(8*self.ell_ref)
        self.limit=sum(c for (alpha,scale),c in zip(pair.terms,pair.coefficients) if alpha==0)
        self.iterations=0
        for n in range(24):
            self._interpolant=CubicSpline(self.x,self.ratio)
            g=(endpoint_mass+Pr+self.ell_primitive(hr)-(e+hr)*p)/(8-2*e)
            updated=((d+h)*p-e*g+self.ell_primitive(e)-self.ell_primitive(h))/((8-2*e)*self.ell_ref)
            error=float(abs(updated-self.ratio).max())
            self.ratio=updated;self.iterations=n+1
            if error<1e-13:break
        self.iteration_error=error
        self._interpolant=CubicSpline(self.x,self.ratio)

    def ratio_at(self,x):
        x=np.asarray(x,dtype=float)
        return np.where(x>self.x[-1],self.limit,
            self._interpolant(np.clip(x,self.x[0],self.x[-1])))

    def ell(self,eps):
        return self.base.ell(eps)*self.ratio_at(self.base.coordinate(eps))

    def ell_primitive(self,eps):
        e=np.asarray(eps,dtype=float);x=self.base.coordinate(e)
        rate=5/6;xx=x[...,None]+self.base.nodes/rate
        integral=(modulation(xx)*self.ratio_at(xx))@self.base.weights/rate
        return .5*e**rate*integral

    def g(self,eps):
        e=np.asarray(eps,dtype=float);r=self.fronts.inverse_delta(e);hr=self.fronts.eta(r)
        return (self.endpoint_mass+self.pair.primitive(r)+self.ell_primitive(hr)
            -(e+hr)*self.pair.density(e))/(8-2*e)

    def f(self,eps):return self.pair.density(eps)-self.g(eps)

    def ku(self,eps):
        e=np.asarray(eps,dtype=float);d=self.fronts.delta(e);h=self.fronts.eta(e)
        return self.pair.primitive(d)-self.pair.primitive(e)-(d-e)*self.ell(h)

    def ell_primitive_quad(self,eps):
        x=float(self.base.coordinate(eps))
        integral=quad(lambda r:math.exp(-5*r/6)*float(modulation(x+r))*float(self.ratio_at(x+r)),
            0,np.inf,epsabs=2e-12,epsrel=2e-12)[0]
        return .5*eps**(5/6)*integral

    def independent_audit(self,probes):
        rows=[]
        for e in probes:
            d=float(self.fronts.delta(e));h=float(self.fronts.eta(e))
            pe=self.pair.primitive_quad(e);pd=self.pair.primitive_quad(d)
            le=self.ell_primitive_quad(e);lh=self.ell_primitive_quad(h)
            ka=-(d+h)*self.pair.density(e)+e*self.g(e)+(8-2*e)*self.ell(e)-le+lh
            ku=pd-pe-(d-e)*self.ell(h)
            rows.append(dict(epsilon=float(e),relative_ka=float(ka/((d+h)*self.pair.density(e))),
                relative_ku=float(ku/((d-e)*self.ell(h))),
                p_primitive_relative_difference=float(self.pair.primitive(d)/pd-1),
                ell_primitive_relative_difference=float(self.ell_primitive(e)/le-1)))
        return rows

    def audit(self,eps):
        e=np.asarray(eps,dtype=float);d=self.fronts.delta(e);h=self.fronts.eta(e)
        p=self.pair.density(e);g=self.g(e)
        ka=-(d+h)*p+e*g+(8-2*e)*self.ell(e)-self.ell_primitive(e)+self.ell_primitive(h)
        kc=self.endpoint_mass+self.pair.primitive(e)+self.ell_primitive(h)-(d+h)*self.pair.density(d)-(8-2*d)*self.g(d)
        ku=self.ku(e);scale=(d-e)*self.ell(h)
        ascale=(d+h)*p
        return [dict(epsilon=float(t),outgoing_defect=float(dd),incoming_defect=float(hh),
            ka=float(ra),kc=float(rc),ku=float(ru),relative_ka=float(ra/sa),relative_ku=float(ru/sc))
            for t,dd,hh,ra,rc,ru,sa,sc in zip(e,d,h,ka,kc,ku,ascale,scale)]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--cutoff",type=float,default=1e-5)
    ap.add_argument("--amplitude",type=float,default=.1)
    ap.add_argument("--endpoint-mass",type=float,default=.622)
    ap.add_argument("--leading-fronts",action="store_true")
    ap.add_argument("--output",default="endpoint_tail_fit.json")
    args=ap.parse_args()
    fronts=FractionalFronts(corrected=not args.leading_fronts)
    scale=float(fronts.delta(args.cutoff))
    terms=[(0.,1.),(1/3,2.),(.5,1.),(.75,1.),(.875,1.),(1.,1.),(1.25,1.),(1.5,1.)]
    probes=np.geomspace(args.cutoff,1e-16,80)
    reference=PowerLogTail(args.amplitude,args.endpoint_mass)
    denominator=fronts.delta(probes)*reference.ell(fronts.eta(probes))
    source=PairVolterra(PairDensity(terms,np.zeros(len(terms)),scale),fronts,args.endpoint_mass,args.cutoff)
    models=[]
    for j in range(len(terms)):
        coefficients=np.zeros(len(terms));coefficients[j]=1.
        models.append(PairVolterra(PairDensity(terms,coefficients,scale),fronts,0.,args.cutoff))
    columns=np.array([model.ku(probes)/denominator for model in models]).T
    rhs=-source.ku(probes)/denominator-args.amplitude*columns[:,0]
    # Finite analytic correction coefficients; fixing the leading amplitude
    # prevents the vacuous zero-density homogeneous solution.
    fit=lsq_linear(columns[:,1:],rhs,bounds=(-10.,10.),tol=1e-13,max_iter=300)
    coefficients=np.r_[args.amplitude,fit.x]
    result=PairVolterra(PairDensity(terms,coefficients,scale),fronts,args.endpoint_mass,args.cutoff)
    check=np.geomspace(args.cutoff*.987,1.031e-16,121)
    audit=result.audit(check)
    independent=result.independent_audit(np.geomspace(args.cutoff*.913,1.173e-16,8))
    density_check=np.geomspace(scale,1e-20,501)
    f=result.f(density_check);g=result.g(density_check)
    ell=result.ell(np.geomspace(args.cutoff,1e-20,501))
    output=dict(scope="Local analytic upper-tail candidate fitted to asymptotic lower front history; no global bound or matching-law claim.",
        corrected_fronts=not args.leading_fronts,cutoff=args.cutoff,scale_deficit=scale,
        incoming_history="eps^2/16*(1+sqrt(eps)/15)" if not args.leading_fronts else "eps^2/16",
        outgoing_particular_correction=88/125 if not args.leading_fronts else 0.,
        endpoint_mass=args.endpoint_mass,terms=terms,coefficients=coefficients.tolist(),
        fit_success=bool(fit.success),fit_message=fit.message,
        max_off_sample_relative_ku=max(abs(row['relative_ku'])for row in audit),
        max_off_sample_relative_ka=max(abs(row['relative_ka'])for row in audit),
        max_off_sample_ka=max(abs(row['ka'])for row in audit),
        max_off_sample_kc=max(abs(row['kc'])for row in audit),
        max_independent_relative_ka=max(abs(row['relative_ka'])for row in independent),
        max_independent_relative_ku=max(abs(row['relative_ku'])for row in independent),
        density_positive=bool(min(f)>0 and min(g)>0 and min(ell)>0),
        density_minima=dict(f=float(min(f)),g=float(min(g)),ell=float(min(ell))),
        f_monotone_on_probe=bool(np.all(np.diff(f)>=-1e-8)),
        ell_monotone_on_probe=bool(np.all(np.diff(ell)>=-1e-8)),
        volterra_iterations=result.iterations,volterra_iteration_error=result.iteration_error,
        independent_quadrature_audit=independent,
        residual_audit=audit)
    dest=Path(__file__).with_name(args.output);dest.write_text(json.dumps(output,indent=2))
    print(json.dumps({key:value for key,value in output.items()if key not in ['residual_audit','independent_quadrature_audit']},indent=2))
    print("OUTPUT",dest)


if __name__=="__main__":main()
