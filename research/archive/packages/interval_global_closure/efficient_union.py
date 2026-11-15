"""Make one physical-route union bank for global strategy exchange.

All columns from every supplied bank remain, modulo exact reflection and
redundant-unit-leg equivalence.  No source LP multipliers are reinterpreted as
probabilities: the incumbent law supplies the initial normalized weights.
"""
from __future__ import annotations
import argparse,json
from fractions import Fraction as Q
from pathlib import Path


def canonical(route):
    cleaned=[];walls=set()
    for u,v in [(Q(a),Q(b)) for a,b in route]:
        if cleaned and cleaned[-1]==(u,v):continue
        while len(cleaned)>1 and ((cleaned[-2][0]==cleaned[-1][0]==u)
              or(cleaned[-2][1]==cleaned[-1][1]==v)):
            cleaned.pop()
        cleaned.append((u,v))
        if u-v in(-2,2):walls.add(u-v)
        if len(walls)==2:break
    assert len(walls)==2
    reflected=[(v,u) for u,v in cleaned]
    cleaned=min(cleaned,reflected)
    return tuple(tuple(map(str,p)) for p in cleaned)


def main():
    p=argparse.ArgumentParser();p.add_argument('--incumbent',required=True)
    p.add_argument('--bank',action='append',required=True)
    p.add_argument('--profiles',action='append',default=[])
    p.add_argument('--attacks',action='append',default=[],help='Decoded physical unit-route attacks to add in full.')
    p.add_argument('--omit-center-waits',action='store_true',
        help='Explicitly record and omit center-wait attacks unsupported by the current unit-only upper oracle.')
    p.add_argument('--unitize-center-waits',action='store_true',
        help='Replace center waits by closed unit excursions, which dominate them for global upper-law optimization.')
    p.add_argument('--output',default='efficient_union_bank.json')
    args=p.parse_args();directory=Path(__file__).parent
    incumbent=json.loads((directory/args.incumbent).read_text())
    assert not(args.omit_center_waits and args.unitize_center_waits)
    groups={};weights=[];sources=[];omitted=[];replacements=[]
    for bank_index,filename in enumerate(args.bank):
        data=json.loads((directory/filename).read_text())
        if bank_index==0:assert len(data['atoms'])==len(incumbent['weights'])
        for j,a in enumerate(data['atoms']):
            key=canonical(a['exact_light'])
            if key not in groups:
                groups[key]=len(groups);weights.append(0.);sources.append([])
            i=groups[key]
            sources[i].append(dict(bank=filename,index=j,kind=a.get('kind'),parameters=a.get('parameters')))
            if bank_index==0:weights[i]+=incumbent['weights'][j]
    for filename in args.attacks:
        data=json.loads((directory/filename).read_text())
        for j,item in enumerate(data['attacks']):
            physical=[tuple(map(Q,p)) for p in item['route']]
            assert physical[0][0]==0
            waits=False
            for(a,x),(b,y)in zip(physical,physical[1:]):
                assert b>a and abs(y-x)<=b-a
                if abs(y-x)!=b-a:
                    assert x==y==0, 'Nonunit motion other than a center wait needs a separate oracle.'
                    waits=True
            if waits:
                if args.unitize_center_waits:
                    from continuous_response_waits import unitize_center_waits
                    physical=unitize_center_waits(physical)
                    replacements.append(dict(source=filename,index=j,original_route=item['route'],
                        unit_route=[[str(t),str(x)] for t,x in physical],
                        scope='Global upper-law dominance only; the old lower-CDF attack payoff is not transferred.'))
                else:
                    assert args.omit_center_waits, 'Center wait encountered: explicitly unitize or omit it.'
                    omitted.append(dict(source=filename,index=j,reason='Center wait is not supported by the current unit-only upper oracle.',route=item['route']))
                    continue
            key=canonical([(t+x,t-x) for t,x in physical])
            if key not in groups:
                groups[key]=len(groups);weights.append(0.);sources.append([])
            sources[groups[key]].append(dict(bank=filename,index=j,
                kind='unitized_center_wait' if waits else 'physical_node_attack'))
    atoms=[]
    for route,i in groups.items():
        atoms.append(dict(kind='PATH',parameters=sum((list(p) for p in route),[]),
            exact_light=[list(p) for p in route],light=[[float(Q(u)),float(Q(v))] for u,v in route],
            sources=sources[i]))
    extra=[]
    for filename in [args.incumbent]+args.profiles:
        data=json.loads((directory/filename).read_text())
        profiles=data.get('princess_mixture')
        if profiles is None:
            profiles=[dict(labels=data[key],weight=0.) for key in ('minimum_labels','maximum_labels') if key in data]
        extra.append(dict(source=filename,v=data['query_v'],
            base=[p[0] for j,p in enumerate(data['event_labels']) if j%3==0],
            profiles=profiles))
    payload=dict(scope='Exact physical union of supplied complete unit-route banks; fair reflected pairs.',
        atoms=atoms,seed_weights=weights,extra_profiles=extra,
        source_banks=args.bank,source_attacks=args.attacks,incumbent=args.incumbent,
        omitted_center_wait_attacks=omitted,center_wait_replacements=replacements)
    assert abs(sum(weights)-1)<1e-8
    (directory/args.output).write_text(json.dumps(payload,separators=(',',':'))+'\n')
    print(dict(pairs=len(atoms),source_banks=args.bank,seed_upper=incumbent['global_response'],
        extra_profiles=sum(len(e['profiles']) for e in extra),omitted_center_waits=len(omitted),
        unitized_center_waits=len(replacements)))


if __name__=='__main__':main()
