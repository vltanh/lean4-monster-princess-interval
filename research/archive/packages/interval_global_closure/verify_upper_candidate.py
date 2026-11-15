#!/usr/bin/env python3
"""Independent Fraction response rows and an actual epsilon best response.

The integer flow replay is in certify_upper_candidate.cjs. This different
implementation checks the rational geometry and both extremal rows, then
intersects a legal physical princess with every monster in the mixture.
"""
from fractions import Fraction as Q
import argparse,json,sys,time
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'interval_turn_density'))
sys.path.insert(0,str(HERE.parent/'interval_exact_reduction'))
from atom_survival_cut import SurvivalCut
from exact_oracles import admissible,simplify,first_meeting


def run(source,dest,epsilon=Q(1,2**24)):
    started=time.time();c=json.loads(Path(source).read_text())
    atoms=[dict(kind='PATH',parameters=tuple(Q(x)for p in a['exact_light']for x in p))for a in c['atoms']]
    model=SurvivalCut(atoms,lexicographic=True)
    assert list(map(str,model.v))==c['query_v']
    assert [[str(a),b]for a,b in model.levels]==[[x,s]for x in c['base_levels']for s in [-1,0,1]]
    weights=[Q(int(a['weight_numerator']),int(c['weight_denominator']))for a in c['atoms']]
    assert sum(weights)==1 and min(weights)>0
    ceiling=Q(c['value'])
    for labels in [c['minimum_labels'],c['maximum_labels']]:
        values=[model.levels[j]for j in labels]
        assert sum(q*w for q,w in zip(model.row(atoms,values),weights))==ceiling
    values=[model.levels[j]for j in c['minimum_labels']]
    princess=simplify(model.realize(values,epsilon=epsilon,strict=True));assert admissible(princess)
    captures=[];payoff=Q(0)
    for item,weight in zip(c['atoms'],weights):
        uv=[tuple(map(Q,p))for p in item['exact_light']]
        positive=[((u+v)/2,(u-v)/2)for u,v in uv]
        negative=[(t,-x)for t,x in positive]
        assert admissible(positive)and admissible(negative)
        hits=[first_meeting(m,princess)for m in [positive,negative]]
        assert all(t is not None for t in hits)
        payoff+=weight*sum(hits)/2;captures.append(list(map(str,hits)))
    assert 0<=ceiling-payoff<=Q(1,10**6)
    report=dict(scope='Independent exact physical epsilon best response to the supplied monster law; not a princess minimax strategy.',
                source=Path(source).name,extremal_fraction_rows_checked=2,monster_pairs=len(atoms),
                epsilon=str(epsilon),response_ceiling=str(ceiling),actual_princess_payoff=str(payoff),
                exact_best_response_gap=str(ceiling-payoff),gap_decimal=float(ceiling-payoff),
                princess_route=[[str(t),str(x)]for t,x in princess],
                first_capture_times=captures,seconds=time.time()-started)
    Path(dest).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ['princess_route','first_capture_times']}),flush=True)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('output')
    args=p.parse_args();run(args.source,args.output)
