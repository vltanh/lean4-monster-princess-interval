#!/usr/bin/env python3
"""Diffuse the entire deadline corridor; integrate a fixed response exactly.

Each component is uniform in lambda in (0,1), with
p_lambda(t)=(1-lambda)L(t)+lambda U(t).  The envelopes and every log
coefficient are rational.  Decimal evaluations are discovery output, not
certified logarithm bounds or an unrestricted monster-response theorem.
"""
from __future__ import annotations
import argparse
from bisect import bisect_left
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_exact_reduction'))
from exact_oracles import position, tail_cone, envelope_knots, simplify, admissible, first_meeting
sys.path.insert(0,str(ROOT/'packages/interval_turn_density'))
from atom_survival_cut import light_route


@dataclass
class LogExpression:
    rational: Q=Q(0)
    logs: list | None=None

    def __post_init__(self):
        if self.logs is None:self.logs=[]

    def add(self,other,scale=Q(1)):
        self.rational+=scale*other.rational
        self.logs.extend((scale*c,r) for c,r in other.logs if scale*c and r!=1)
        return self

    def decimal(self,precision=60):
        with localcontext() as context:
            context.prec=precision
            def dec(q):return Decimal(q.numerator)/Decimal(q.denominator)
            return dec(self.rational)+sum((dec(c)*dec(r).ln() for c,r in self.logs),Decimal(0))

    def data(self):
        low,high=self.rational_bounds()
        return dict(rational=str(self.rational),logs=[[str(c),str(r)] for c,r in self.logs],
                    decimal=str(self.decimal()),rational_lower=str(low),rational_upper=str(high))

    def rational_bounds(self):
        """Elementary exact bounds: 1-1/r <= log(r) <= r-1."""
        low=high=self.rational
        for coefficient,ratio in self.logs:
            assert ratio>0
            a,b=1-1/ratio,ratio-1
            low+=coefficient*(a if coefficient>=0 else b)
            high+=coefficient*(b if coefficient>=0 else a)
        return low,high


def integral_ratio(a,b,A,B,C,D):
    """Integral_a^b (A*t+B)/(C*t+D), with positive denominator."""
    assert C*a+D>0 and C*b+D>0
    if not C:return LogExpression((A*(b*b-a*a)/2+B*(b-a))/D)
    return LogExpression(A*(b-a)/C,[((B*C-A*D)/(C*C),(C*b+D)/(C*a+D))])


def oriented_path(atom,reflection=False):
    return [((u+v)/2,(u-v)/2) for u,v in light_route(atom,reflection)]


class Corridor:
    def __init__(self,knots,weight=Q(1),targets=None,limiting=False):
        self.knots=[(Q(t),Q(l),Q(u)) for t,l,u in knots]
        self.weight=Q(weight)
        self.targets=[] if targets is None else targets
        self.limiting=limiting
        self.lower=[(t,l) for t,l,u in self.knots]
        self.upper=[(t,u) for t,l,u in self.knots]
        assert self.knots[0][0]==0
        assert admissible(self.lower) and admissible(self.upper)
        assert all(0<=l<=u<=1 and (limiting or l<u) for t,l,u in self.knots)

    def path(self,lam):
        lam=Q(lam)
        assert 0<lam<1
        result=simplify([(t,(1-lam)*l+lam*u) for t,l,u in self.knots])
        assert admissible(result)
        return result

    def reflected(self):
        # Kept as a separate fixed-response transformation, since the class
        # stores positive corridors only.
        raise NotImplementedError('Reflect the monster in payoff(), not the positive corridor')

    def payoff(self,monster,horizon=None):
        """Full expected capture if the supplied monster finishes both walls.

        Corridor paths remain constant after their last supplied time. Every
        segment CDF is fractional-linear; its derivative has constant sign.
        Exact crossings of old records determine the survival integral.
        """
        monster=[(Q(t),Q(x)) for t,x in monster]
        assert not self.limiting,'Use payoff_by_lambda for collapsed limiting envelopes'
        assert admissible(monster)
        horizon=max(monster[-1][0],self.knots[-1][0]) if horizon is None else Q(horizon)
        times=sorted({Q(0),horizon}|{t for t,x in monster if t<=horizon}
                     |{t for t,l,u in self.knots if t<=horizon})
        def clip(x):return min(Q(1),max(Q(0),x))
        def cdf(t):
            l,u=position(self.lower,t),position(self.upper,t)
            return clip((position(monster,t)-l)/(u-l))
        low=high=cdf(Q(0))
        result=LogExpression()
        for a,b in zip(times,times[1:]):
            la,lb=position(self.lower,a),position(self.lower,b)
            ua,ub=position(self.upper,a),position(self.upper,b)
            xa,xb=position(monster,a),position(monster,b)
            A=((xb-lb)-(xa-la))/(b-a); B=xa-la-A*a
            C=((ub-lb)-(ua-la))/(b-a); D=ua-la-C*a
            cuts={a,b}
            for value in (Q(0),low,high,Q(1)):
                if A-value*C:
                    t=(value*D-B)/(A-value*C)
                    if a<t<b:cuts.add(t)
            cuts=sorted(cuts)
            for left,right in zip(cuts,cuts[1:]):
                middle=(left+right)/2
                raw=(A*middle+B)/(C*middle+D)
                f=clip(raw)
                if f>high:
                    if f==1:integ=LogExpression(right-left)
                    else:integ=integral_ratio(left,right,A,B,C,D)
                    result.rational+=(1+low)*(right-left)
                    result.add(integ,-1)
                elif f<low:
                    if f==0:integ=LogExpression()
                    else:integ=integral_ratio(left,right,A,B,C,D)
                    result.rational+=(1-high)*(right-left)
                    result.add(integ)
                else:result.rational+=(1+low-high)*(right-left)
                fleft=clip((A*left+B)/(C*left+D))
                fright=clip((A*right+B)/(C*right+D))
                low=min(low,fleft,fright);high=max(high,fleft,fright)
        assert low==0 and high==1,('Monster has not captured all corridor ranks',low,high)
        return result

    def payoff_by_lambda(self,monster):
        """Independent first-intersection integral in the rank variable.

        Split lambda at every vertex contact. Within each resulting interval
        the first capture segment is fixed and capture time is fractional
        linear in lambda. This also handles collapsed limiting corridors.
        """
        monster=[(Q(t),Q(x)) for t,x in monster]
        assert admissible(monster)
        horizon=max(monster[-1][0],self.knots[-1][0])
        times=sorted({Q(0),horizon}|{t for t,x in monster}|{t for t,l,u in self.knots})
        # Difference monster-princess = intercept + coefficient*lambda.
        differences=[];cuts={Q(0),Q(1)}
        for t in times:
            l,u=position(self.lower,t),position(self.upper,t)
            intercept=position(monster,t)-l;coefficient=l-u
            differences.append((intercept,coefficient))
            if coefficient:
                rank=-intercept/coefficient
                if 0<rank<1:cuts.add(rank)
        result=LogExpression();cuts=sorted(cuts)
        for left,right in zip(cuts,cuts[1:]):
            rank=(left+right)/2
            found=False
            for k,t in enumerate(times):
                d0,c0=differences[k];at=d0+c0*rank
                if at==0:
                    # Either the entire open rank interval contacts at t, or
                    # a missing rank cut would have been required above.
                    assert d0==c0==0
                    result.rational+=t*(right-left);found=True;break
                if k+1==len(times):continue
                end=times[k+1];d1,c1=differences[k+1]
                if at*(d1+c1*rank)<0:
                    # t + (end-t)*(d0+c0*lambda)/
                    #                 ((d0-d1)+(c0-c1)*lambda).
                    C,D=c0-c1,d0-d1
                    A=t*C+(end-t)*c0;B=t*D+(end-t)*d0
                    if C*rank+D<0:A,B,C,D=-A,-B,-C,-D
                    result.add(integral_ratio(left,right,A,B,C,D))
                    found=True;break
            assert found,'Supplied monster does not capture every rank'
        return result

    def data(self):
        return dict(weight=str(self.weight),knots=[[str(t),str(l),str(u)] for t,l,u in self.knots],
                    targets=self.targets,limiting=self.limiting)


def profile_value(query_v,values,v):
    j=bisect_left(query_v,v)
    if j<len(query_v) and query_v[j]==v:return values[j]
    return max(values[j-1],(v,0),(Q(0),0))


def capture_target(route,query_v,values):
    """Independent direct limiting contact formula for one oriented route."""
    u,v=route[0]
    initial=profile_value(query_v,values,v)
    if initial==(u,0):return Q(0),None
    below=initial>(u,0)
    for (u0,v0),(u1,v1) in zip(route,route[1:]):
        if u1>u0 and below:
            crossing=profile_value(query_v,values,v0)
            if crossing<=(u1,0):return (crossing[0]+v0)/2,True
        elif v1>v0 and not below:
            k=bisect_left(values,(u0,0))
            assert k<len(values)
            crossing=min(u0,query_v[k])
            if crossing<=v1:return (u0+crossing)/2,False
    raise AssertionError('Missing capture target')


def build(data,delta=Q(1,4096),positive_wall=Q(0)):
    """Build uniform corridors using only positive-weight upper support."""
    assert positive_wall==0
    delta=Q(delta); assert delta>=0
    atoms=[dict(kind=a['kind'],parameters=tuple(map(Q,a['parameters']))) for a in data['monster_pairs']]
    routes=[light_route(a,r) for a in atoms for r in (False,True)]
    monsters=[oriented_path(a,r) for a in atoms for r in (False,True)]
    horizon=max(p[-1][0] for p in monsters)
    query_v=list(map(Q,data['query_v']))
    levels=[(Q(q),int(side)) for q,side in data['event_labels']]
    corridors=[]
    for component in data['princess_components']:
        values=[levels[k] for k in component['labels']]
        lows=[[(Q(0),Q(0)),(horizon,Q(0))]]
        ups=[[(Q(0),Q(1)),(horizon,Q(1))]]
        targets=[]
        for route,monster in zip(routes,monsters):
            target,below=capture_target(route,query_v,values)
            targets.append(dict(time=str(target),below=below))
            if target==0:continue
            curve=tail_cone(monster,max(Q(0),target-delta),horizon,-1 if below else 1)
            (lows if below else ups).append(curve)
        times=sorted(envelope_knots(lows,horizon)|envelope_knots(ups,horizon))
        knots=[(t,max(position(p,t) for p in lows),min(position(p,t) for p in ups)) for t in times]
        corridor=Corridor(knots,Q(component['weight']),targets,limiting=not delta)
        # Independent physical checks of representative ranks. The theorem
        # covers every lambda; these guards catch assembly/sign mistakes.
        for lam in ((Q(1,7),Q(1,2),Q(6,7)) if delta else ()):
            p=corridor.path(lam)
            for m,target in zip(monsters,targets):
                t=first_meeting(m,p)
                assert t is not None and t>=Q(target['time'])-delta
        corridors.append(corridor)
    assert sum(c.weight for c in corridors)==1
    return corridors


def mixture_payoff(corridors,monster,direct=False):
    reflected=[(t,-x) for t,x in monster]
    result=LogExpression()
    for corridor in corridors:
        method=corridor.payoff_by_lambda if direct or corridor.limiting else corridor.payoff
        result.add(method(monster),corridor.weight/2)
        result.add(method(reflected),corridor.weight/2)
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('--delta',default='1/4096')
    parser.add_argument('--output')
    parser.add_argument('--m1-grid',type=int,default=32)
    args=parser.parse_args()
    source=Path(args.source)
    data=json.loads(source.read_text())
    corridors=build(data,Q(args.delta))
    active=[]
    for a in data['monster_pairs']:
        atom=dict(kind=a['kind'],parameters=tuple(map(Q,a['parameters'])))
        payoff=mixture_payoff(corridors,oriented_path(atom))
        active.append(dict(kind=a['kind'],parameters=a['parameters'],payoff=payoff.data()))
    attacks=[]
    for k in range(-args.m1_grid,args.m1_grid+1):
        x=Q(k,args.m1_grid)
        payoff=mixture_payoff(corridors,oriented_path(dict(kind='M1',parameters=(x,))))
        attacks.append(dict(start=str(x),payoff=payoff.data()))
    best=min(attacks,key=lambda a:Decimal(a['payoff']['decimal']))
    out=dict(scope='Uniform deadline-corridor candidate; analytic supplied-monster responses only. '
             'No unrestricted lower guarantee or equilibrium is asserted.',source=source.name,
             delta=args.delta,bank_value=data['value'],corridors=[c.data() for c in corridors],
             active_monster_payoffs=active,m1_attacks=attacks,best_m1_attack=best)
    destination=Path(args.output) if args.output else source.with_suffix('.corridor.json')
    destination.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(components=len(corridors),initial_chambers=[
          [str(c.knots[0][1]),str(c.knots[0][2])] for c in corridors],
          active_min=min(a['payoff']['decimal'] for a in active),best_m1=best,output=str(destination)),indent=2))


if __name__=='__main__':main()
