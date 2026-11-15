#!/usr/bin/env python3
"""Exact initial-gap and law-specific cutoff diagnostics for a physical law.

This reuses only the Fraction chronological-path helpers in the boundary
kernel replay. It does not inspect or reprove the stored upper flow bound.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as Q
import gzip
import hashlib
import json
from pathlib import Path

from verify_boundary_layer_kernel import inspect_certificate,decode_route,contact


def inspect(source):
    report=inspect_certificate(source)
    raw=source.read_bytes()
    data=json.loads(gzip.decompress(raw) if raw[:2]==b'\x1f\x8b' else raw)
    step=Q(data['physical_step'])
    by_start=defaultdict(lambda:{'mass':0,'max_center':Q(0)})
    physical=set()
    for row in data['paths']:
        route=decode_route(row,step)
        radius=abs(route[0][1])
        center=contact(route,[(Q(0),Q(0))])
        by_start[radius]['mass']+=int(row['weight_numerator'])
        by_start[radius]['max_center']=max(center,by_start[radius]['max_center'])
        path=tuple(route)
        reflected=tuple((t,-x) for t,x in route)
        physical.add(min(path,reflected))
    knots=sorted(set(by_start)|{Q(0),Q(1)})
    profile=[]
    for left,right in zip(knots,knots[1:]):
        # The strict start inequality is constant on [left,right).
        cutoff=max((entry['max_center'] for start,entry in by_start.items()
                    if start>left),default=Q(0))
        if profile and profile[-1]['cutoff']==str(cutoff):
            profile[-1]['right']=str(right)
        else:
            profile.append({'left':str(left),'right':str(right),
                            'cutoff':str(cutoff),'interval':'[left,right)'})
    report.pop('cutoff_checks',None)
    report.update({
        'status':'PASS',
        'distinct_physical_pairs':len(physical),
        'initial_start_rows':[
            {'initial_absolute_position':str(a),'weight_numerator':str(row['mass']),
             'maximum_center_time':str(row['max_center'])}
            for a,row in sorted(by_start.items())],
        'law_specific_outward_cutoff':profile,
        'cutoff_at_one':'0',
        'cutoff_source_thresholds':len(knots),
        'upper_minus_boundary_limit_decimal':float(Q(report['upper_minus_boundary_limit'])),
        'stationary_endpoint_score_decimal':float(Q(report['stationary_endpoint_score'])),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    })
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--physical-certificate',type=Path,required=True)
    parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args()
    report=inspect(args.physical_certificate)
    args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items()
                     if key not in ('initial_start_rows','law_specific_outward_cutoff','exact_loop_scores')},indent=2))


if __name__=='__main__':main()
