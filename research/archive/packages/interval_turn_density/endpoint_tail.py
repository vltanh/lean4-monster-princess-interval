#!/usr/bin/env python3
"""Continuous endpoint densities from the audited logarithmic tail balance.

The convergent pantograph series removes every inverse-log error from the
dominant free-incoming condition.  The optional Volterra solve then enforces
the full a and c stationarity equations for the fixed leading-order front
maps d(eps)=4*sqrt(eps), eta(eps)=eps**2/16.

This is a boundary construction, not a coupled equilibrium certificate:
the full incoming equation and the lower-law corrections remain explicit
residuals.  No atom or piecewise-constant density is inserted at the endpoint.
"""

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.polynomial.laguerre import laggauss
from scipy.integrate import quad
from scipy.interpolate import CubicSpline


GAMMA=math.log(1.5)/math.log(4.)


def coefficients(count=24):
    values=[1.]
    for n in range(1,count):
        values.append(-12.*(GAMMA-n+1)*values[-1]/(4.**n-1.))
    return np.array(values)


COEFFICIENTS=coefficients()


def modulation(x,derivative=False,terms=None):
    """H(x), or H'(x), from its absolutely convergent series for x>0."""
    x=np.asarray(x,dtype=float)
    if np.any(x<=0):raise ValueError("The logarithmic coordinate must be positive")
    coeff=COEFFICIENTS if terms is None else COEFFICIENTS[:terms]
    result=np.zeros_like(x)
    for n,c in enumerate(coeff):
        result+=c*(GAMMA-n if derivative else 1.)*x**(-n)
    return x**(GAMMA-(1 if derivative else 0))*result


def series_remainder_bound(x,terms=12):
    """Geometric majorant for the omitted terms of H(x), x>=log(16)."""
    if x<math.log(16.):raise ValueError("Use the stated positive tail domain")
    coeff=coefficients(terms+2)
    first=abs(coeff[terms])*x**(GAMMA-terms)
    ratio=12.*(terms-GAMMA)/(4.**(terms+1)-1.)/x
    return first/(1-ratio)


@dataclass
class PowerLogTail:
    amplitude: float=1.
    endpoint_mass: float=1.
    quadrature_order: int=48

    def __post_init__(self):
        self.nodes,self.weights=laggauss(self.quadrature_order)

    @staticmethod
    def coordinate(eps):
        eps=np.asarray(eps,dtype=float)
        if np.any((eps<=0)|(eps>1)):
            raise ValueError("Use positive endpoint deficits no greater than one")
        return math.log(16.)-np.log(eps)

    def f(self,eps):
        eps=np.asarray(eps,dtype=float)
        return self.amplitude*eps**(-2/3)*modulation(self.coordinate(eps))

    def ell(self,eps):
        eps=np.asarray(eps,dtype=float)
        return self.amplitude/2*eps**(-1/6)*modulation(self.coordinate(eps))

    def primitive(self,eps,power=2/3,amplitude=None):
        """Integral from 0 to eps of amplitude*t^(-power)*H(log(16/t)).

        Analytically this is a convergent sum of upper incomplete-gamma
        functions.  Gauss-Laguerre evaluates its nonsingular scaled integral;
        verify() independently checks it with adaptive quadrature.
        """
        eps=np.asarray(eps,dtype=float)
        scalar=eps.ndim==0
        positive=np.maximum(eps,np.finfo(float).tiny)
        x=self.coordinate(positive)
        rate=1-power
        scale=self.amplitude if amplitude is None else amplitude
        total=modulation(x[...,None]+self.nodes/rate)@self.weights/rate
        result=np.where(eps>0,scale*positive**rate*total,0.)
        return float(result) if scalar else result

    def f_primitive(self,eps):return self.primitive(eps)

    def ell_primitive(self,eps):return self.primitive(eps,1/6,self.amplitude/2)

    def g_endpoint(self,eps):
        """Endpoint-limit c identity; VolterraTail adds moving-front terms."""
        eps=np.asarray(eps,dtype=float)
        return (self.endpoint_mass-eps*self.f(eps))/(8-eps)


class VolterraTail:
    """Solve exact Ka=Kc=0 for given f and leading front maps.

    The two remaining unknown functions g and ell solve a retarded linear
    integral system.  The unknowns are normalized before interpolation, so
    the divergent endpoint density is represented analytically.  Numerical
    interpolation here is not an interval certificate.
    """

    def __init__(self,base,cutoff=1/64,log_horizon=96.,nodes=385,tolerance=2e-13):
        self.base=base;self.cutoff=cutoff
        xmin=float(base.coordinate(cutoff))
        self.x=np.linspace(xmin,log_horizon,nodes)
        self.eps=16*np.exp(-self.x)
        self.f_values=base.f(self.eps)
        self.ell_base=base.ell(self.eps)
        self.rg=np.full(nodes,-1/8.)
        self.rl=np.ones(nodes)
        self.iterations=0
        for iteration in range(40):
            self._update_interpolants()
            e=self.eps;h=e*e/16;hh=h*h/16;d=4*np.sqrt(e)
            numerator=(base.f_primitive(h)+self.g_primitive(h)+self.ell_primitive(hh)
                -(e+hh)*self.f_values+base.endpoint_mass*(e-hh)/8)
            rg=numerator/(8-e+hh)/(e*self.f_values)
            g=base.endpoint_mass/8+e*self.f_values*rg
            rl=((d+h)*self.f_values+(d+h-e)*g
                +self.ell_primitive(e)-self.ell_primitive(h))/((8-2*e)*self.ell_base)
            error=max(float(abs(rg-self.rg).max()),float(abs(rl-self.rl).max()))
            self.rg,self.rl=rg,rl
            self.iterations=iteration+1
            if error<tolerance:break
        self.iteration_error=error
        self._update_interpolants()

    def _update_interpolants(self):
        self._gs=CubicSpline(self.x,self.rg)
        self._ls=CubicSpline(self.x,self.rl)

    def _ratios(self,x,kind):
        x=np.asarray(x,dtype=float)
        fn=self._gs if kind=="g" else self._ls
        asymptote=-1/8 if kind=="g" else 1.
        return np.where(x>self.x[-1],asymptote,fn(np.clip(x,self.x[0],self.x[-1])))

    def f(self,eps):return self.base.f(eps)

    def ell(self,eps):
        return self.base.ell(eps)*self._ratios(self.base.coordinate(eps),"ell")

    def g(self,eps):
        eps=np.asarray(eps,dtype=float)
        return self.base.endpoint_mass/8+eps*self.f(eps)*self._ratios(self.base.coordinate(eps),"g")

    def _primitive(self,eps,rate,kind,amplitude):
        eps=np.asarray(eps,dtype=float)
        scalar=eps.ndim==0
        positive=np.maximum(eps,np.finfo(float).tiny)
        x=self.base.coordinate(positive)
        xx=x[...,None]+self.base.nodes/rate
        total=(modulation(xx)*self._ratios(xx,kind))@self.base.weights/rate
        result=np.where(eps>0,amplitude*positive**rate*total,0.)
        return float(result) if scalar else result

    def f_primitive(self,eps):return self.base.f_primitive(eps)

    def ell_primitive(self,eps):return self._primitive(eps,5/6,"ell",self.base.amplitude/2)

    def g_primitive(self,eps):
        return self.base.endpoint_mass*np.asarray(eps)/8+self._primitive(eps,4/3,"g",self.base.amplitude)

    def residuals(self,eps):
        e=float(eps);d=4*math.sqrt(e);h=e*e/16
        f,g,ell=self.f(e),self.g(e),self.ell(e)
        # Kc is evaluated at e; its g(d) value must lie inside the solved tail.
        ka=-(d+h)*f+(e-h-d)*g+(8-2*e)*ell-self.ell_primitive(e)+self.ell_primitive(h)
        ku=self.f_primitive(d)-self.f_primitive(e)+self.g_primitive(d)-self.g_primitive(e)-(d-e)*self.ell(h)
        kc=(self.base.endpoint_mass+self.f_primitive(e)+self.g_primitive(e)+self.ell_primitive(h)
            -(d+h)*self.f(d)-(8-d+h)*self.g(d))
        scale_a=(d+h)*f
        scale_u=(d-e)*self.ell(h)
        return dict(epsilon=e,incoming_defect=h,outgoing_defect=d,a=1-e,u=1-h,c=-1+d,
            ka=float(ka),ku=float(ku),kc=float(kc),
            relative_ka=float(ka/scale_a),relative_ku=float(ku/scale_u),
            scaled_kc=float(kc/self.base.endpoint_mass))


def verify(base):
    maximum_ode=0.;maximum_integral=0.;maximum_primitive=0.
    for x in [math.log(16.),4.,8.,16.,32.,64.,128.]:
        ode=12*modulation(x,derivative=True)-modulation(x)+1.5*modulation(x/4)
        maximum_ode=max(maximum_ode,abs(float(ode)))
        integral=quad(lambda r:.5*math.exp(-r/3)*float(modulation(x/4+r)),0,np.inf,
                      epsabs=3e-12,epsrel=3e-12)[0]
        maximum_integral=max(maximum_integral,abs(integral/float(modulation(x))-1))
    for e in [1/64,1e-5,1e-12,1e-30]:
        x=float(base.coordinate(e))
        reference=base.amplitude*e**(1/3)*quad(
            lambda r:math.exp(-r/3)*float(modulation(x+r)),0,np.inf,
            epsabs=2e-12,epsrel=2e-12)[0]
        maximum_primitive=max(maximum_primitive,abs(base.f_primitive(e)/reference-1))
        d=4*math.sqrt(e);h=e*e/16
        maximum_integral=max(maximum_integral,abs(base.f_primitive(d)/(d*base.ell(h))-1))
    assert maximum_ode<2e-12
    assert maximum_integral<2e-11
    assert maximum_primitive<2e-11
    assert float(modulation(math.log(16.)))>0
    return dict(max_pantograph_absolute_residual=maximum_ode,
        max_integral_identity_relative_residual=maximum_integral,
        max_independent_primitive_relative_residual=maximum_primitive,
        series_remainder_bound_at_log16_12_terms=series_remainder_bound(math.log(16.)))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--amplitude",type=float,default=.1)
    parser.add_argument("--endpoint-mass",type=float,default=.622)
    parser.add_argument("--cutoff",type=float,default=1/64)
    parser.add_argument("--output",default="endpoint_tail_diagnostic.json")
    args=parser.parse_args()
    base=PowerLogTail(args.amplitude,args.endpoint_mass)
    checked=verify(base)
    solved=VolterraTail(base,cutoff=args.cutoff)
    # Ensure d(eps) stays in the solved domain.  These are tail probes, not
    # added density bins or a claimed global value calculation.
    initial=args.cutoff**2/16
    probes=[initial*10.**(-j) for j in range(13)]
    rows=[solved.residuals(e) for e in probes]
    output=dict(scope="Analytic endpoint boundary model; full Ka and Kc solved numerically for fixed leading front maps; Ku and lower-front corrections remain.",
        gamma=GAMMA,coefficients=COEFFICIENTS[:12].tolist(),amplitude=args.amplitude,
        endpoint_mass=args.endpoint_mass,cutoff=args.cutoff,verification=checked,
        volterra_iterations=solved.iterations,volterra_iteration_error=solved.iteration_error,
        tail_f_mass=base.f_primitive(args.cutoff),tail_g_mass=float(solved.g_primitive(args.cutoff)),
        tail_ell_mass=solved.ell_primitive(args.cutoff),
        density_positive=bool(np.all(solved.g(solved.eps)>0) and np.all(solved.ell(solved.eps)>0)),
        stationarity=rows)
    dest=Path(__file__).with_name(args.output)
    dest.write_text(json.dumps(output,indent=2))
    print(json.dumps({key:output[key] for key in ("gamma","verification","volterra_iterations",
        "volterra_iteration_error","tail_f_mass","tail_g_mass","tail_ell_mass","density_positive")},indent=2))
    for row in rows:print("STATIONARITY",json.dumps(row))
    print("OUTPUT",dest)


if __name__=="__main__":main()
