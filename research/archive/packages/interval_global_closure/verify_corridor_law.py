#!/usr/bin/env python3
"""Exact whole-law exclusion and independent corridor-integration checks."""
from decimal import Decimal
from fractions import Fraction as Q
import json
from pathlib import Path

from corridor_law import (Corridor, LogExpression, build, mixture_payoff,
                         oriented_path, position, first_meeting)


def initial_left_mass(corridors,x):
    total=Q(0)
    for c in corridors:
        _,l,u=c.knots[0]
        assert l<u
        positive=min(Q(1),max(Q(0),(x-l)/(u-l)))
        negative=min(Q(1),max(Q(0),(x+u)/(u-l)))
        total+=c.weight*(positive+negative)/2
    return total


def verify():
    here=Path(__file__).resolve().parent
    data=json.loads((here/'global_minimax_grid4_exact.json').read_text())
    delta=Q(1,4096);start=Q(-15,16)
    monster=oriented_path(dict(kind='M1',parameters=(start,)))
    first_endpoint=1-start
    corridors=build(data,delta)
    limit_corridors=build(data,Q(0))
    value=Q(data['value'])

    # Exact original deadline equalities on each positive-weight upper atom.
    for j in range(len(data['monster_pairs'])):
        target=sum(c.weight*(Q(c.targets[2*j]['time'])+Q(c.targets[2*j+1]['time']))/2
                   for c in corridors)
        assert target==value

    # An independent integral with a known nontrivial logarithm.
    fixture=Corridor([(0,0,Q(1,2)),(1,0,1),(3,0,1)])
    route=[(0,Q(1,4)),(Q(3,4),1),(Q(11,4),-1)]
    expected=LogExpression(Q(1,4),[(Q(3,2),Q(3,2))])
    for expression in (fixture.payoff(route),fixture.payoff_by_lambda(route)):
        assert abs(expression.decimal()-expected.decimal())<Decimal('1e-50')

    physical=mixture_payoff(corridors,monster)
    independent=mixture_payoff(corridors,monster,direct=True)
    assert abs(physical.decimal()-independent.decimal())<Decimal('1e-45')
    limiting=mixture_payoff(limit_corridors,monster,direct=True)
    left=initial_left_mass(corridors,start)
    assert left==initial_left_mass(limit_corridors,start)==Q(1214049,19087564)
    upper=physical.rational_bounds()[1]
    limit_upper=limiting.rational_bounds()[1]
    assert upper==Q(38988395686171360146464288935247,37526228444123945289355351818240)
    assert limit_upper==Q(30459425896751,29347816802304)
    assert upper+2*left<Q(7,6)<value
    assert limit_upper+2*left==Q(34192713983279,29347816802304)<Q(7,6)

    # Dominated-convergence gate for the first unit-speed sweep. Degenerate
    # limiting corridors must not coincide with the monster for an interval.
    collapsed_segments=0
    for c in limit_corridors:
        times=sorted({Q(0),first_endpoint}|{t for t,l,u in c.knots if 0<t<first_endpoint})
        for a,b in zip(times,times[1:]):
            la,ua=position(c.lower,a),position(c.upper,a)
            lb,ub=position(c.lower,b),position(c.upper,b)
            if la==ua and lb==ub:
                collapsed_segments+=1
                for sign in (-1,1):
                    assert not(sign*position(monster,a)==la and sign*position(monster,b)==lb)

    # Direct physical point captures at midpoint ranks, independently of both
    # integration implementations. Quantile discrepancy is at most H/n.
    n=64;sample=Q(0)
    for c in corridors:
        for k in range(n):
            rank=Q(2*k+1,2*n)
            p=c.path(rank)
            for sign in (-1,1):
                t=first_meeting(monster,[(s,sign*x) for s,x in p])
                assert t is not None
                sample+=c.weight*t/(2*n)
    error=abs(Decimal(sample.numerator)/Decimal(sample.denominator)-physical.decimal())
    discrepancy=Q(monster[-1][0],n)
    assert error<Decimal(discrepancy.numerator)/Decimal(discrepancy.denominator)

    report=dict(scope='Excludes this exact uniform-deadline-corridor family and every '
                'coupling of its marginals, including ordered quantiles; no universal '
                'corridor or finite-support impossibility theorem is asserted.',
                source='global_minimax_grid4_exact.json',components=len(corridors),
                delta=str(delta),bank_value=str(value),active_deadline_lower=str(value-delta),
                attacker_start=str(start),initial_left_mass=str(left),
                physical_fixed_delta=physical.data(),physical_limiting=limiting.data(),
                any_coupling_fixed_delta_upper=str(upper+2*left),
                any_coupling_limiting_upper=str(limit_upper+2*left),
                comparison='both exact coupling upper bounds are less than 7/6',
                collapsed_first_leg_segments_checked=collapsed_segments,
                independent_midpoint_captures=2*n*len(corridors),
                independent_integrators_agree_to_decimal_places=45,
                integration_method='finite exact rational coefficients and log arguments; '
                'final exclusion uses only rational bounds 1-1/r <= log(r) <= r-1')
    target=here/'uniform_corridor_exclusion.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('components','bank_value','active_deadline_lower',
          'attacker_start','initial_left_mass','any_coupling_fixed_delta_upper',
          'any_coupling_limiting_upper','independent_midpoint_captures',
          'collapsed_first_leg_segments_checked')},indent=2))
    print('PASS: analytic corridor integration and exact whole-family exclusion')


if __name__=='__main__':verify()
