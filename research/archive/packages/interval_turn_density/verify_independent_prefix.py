"""Independent complete-feature audit of the I-only negative optimizer."""
import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad

from localized_independent_prefix import negative_blocks
from independent_inward_oracle import frozen_features
from m3_attached_oracle import attached_prefix, M3_LEFT, M3_RIGHT, M3_TURN
from m3_early_oracle import cumulative
from localized_inward_features import localized_inward_feature
from localized_ramp_basis import D


def affine_value(params,candidate,baseline,old,eta,knots):
    """Independent quadrature of the full negative score, including M3.

    Production frozen rows deliberately accept only constant negative
    blocks.  This integrates their defining pointwise generators directly
    on affine competitors instead of misusing that API for curved pieces.
    """
    a,u,c,y = params
    n = len(knots)-1
    p = old[1:1+n]+old[1+n:1+2*n]
    k = old[1+2*n:1+3*n]
    def at(x,values):
        return values[min(n-1,max(0,np.searchsorted(knots,x,side='right')-1))]
    def K(x):
        return sum(max(0.,min(x,knots[j+1])-knots[j])*k[j] for j in range(n))
    generators = []
    for j in range(n):
        lo,hi = max(M3_LEFT,knots[j]),min(M3_RIGHT,knots[j+1])
        if hi > lo:
            generators.append((M3_TURN,lo,hi,at(M3_TURN,k)-p[j]))
    for j in range(1,n):
        if knots[j] > M3_TURN+1e-13:
            generators.append((knots[j],M3_LEFT,M3_RIGHT,k[j]-k[j-1]))
    def local(v,U):
        result = at(-v,p)*(U-u)-K(U)+K(u)
        for r,lo,hi,weight in generators:
            change = 0.
            if lo < -v < hi:
                change += max(0.,U-r)-max(0.,u-r)
            change -= cumulative(r,max(lo,a),hi,U,1)-cumulative(r,max(lo,a),hi,u,1)
            result += weight*change
        return result/4.
    total = baseline
    for lo,hi,slope,intercept in candidate:
        cuts = [lo,hi]
        cuts.extend(-z for z in knots if lo < -z < hi)
        cuts.extend(-z for z in (M3_LEFT,M3_RIGHT) if lo < -z < hi)
        if slope:
            cuts.extend((z-intercept)/slope for z in knots if lo < (z-intercept)/slope < hi)
        cuts = sorted(set(cuts))
        for l,r in zip(cuts,cuts[1:]):
            part,error = quad(lambda v:local(v,slope*v+intercept),l,r,epsabs=2e-13,epsrel=2e-13)
            assert error < 2e-11, error
            total += part
    constant = np.array([[-a,min(c,0.),0.,u]])
    total += eta*(localized_inward_feature(D,a,c,candidate)
                  -localized_inward_feature(D,a,c,constant))/4.
    return total


def main():
    data = json.loads(Path(__file__).with_name('negative_prefix_discovery.json').read_text())
    knots = np.asarray(data['knots'])
    profile = np.asarray(data['affine_profile'])
    old = np.r_[data['endpoint_mass'], *(data['densities'][x] for x in ('f','g','k','ell'))]
    left, right, s0 = data['left'], data['right'], data['turn']
    rng = np.random.default_rng(650492)
    comparisons = 0
    largest = 0.
    for i in range(48):
        a = rng.uniform(.875, .999) if i % 2 else rng.uniform(.001, .875)
        u = rng.uniform(a, 1.)
        c = rng.uniform(-a, .99); y = rng.uniform(max(c,0.), .999)
        eta = (.005, .1, 1., 10.)[i % 4]
        params = np.array([a,u,c,y])
        variables = np.r_[old,eta]
        positive, npiece = attached_prefix(params,knots,old,left,right,s0)
        negative, nn = negative_blocks(params,knots,old,eta)
        def value(candidate):
            full = np.vstack((candidate,positive[:npiece]))
            return frozen_features(params,full,len(full),knots,profile,left,right,s0)@variables
        best = value(negative[:nn])
        baseline = value(np.array([[-a,min(c,0.),0.,u]]))
        for trial in range(80):
            n = 1+trial % 6
            cuts = np.r_[-a,np.sort(rng.uniform(-a,min(c,0.),n-1)),min(c,0.)]
            levels = np.sort(rng.uniform(a,u,n+1))
            if trial < 8:
                slopes = np.diff(levels)/np.diff(cuts)
                intercepts = levels[:-1]-slopes*cuts[:-1]
            else:
                slopes = np.zeros(n)
                intercepts = levels[:-1]
            candidate = np.c_[cuts[:-1],cuts[1:],slopes,intercepts]
            actual = (affine_value(params,candidate,baseline,old,eta,knots)
                      if trial < 8 else value(candidate))
            largest = max(largest,actual-best)
            assert actual <= best+5e-12, (params,eta,best,actual,negative[:nn],candidate)
            comparisons += 1
    print('PASS:',comparisons,'independent complete-feature comparisons, including curved monotone inverse competitors')
    print('Largest sampled improvement over the analytic I-only prefix optimum:',largest)
    print('Scope: floating arithmetic audit of the proved finite arrangement; no equilibrium claim')


if __name__ == '__main__':
    main()
