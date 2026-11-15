#!/usr/bin/env python3
"""Compute the whole-bank benefit of common-quantile uncrossing."""
import argparse,json
from pathlib import Path
from efficient_master import Separator
import numpy as np
from scipy.optimize import linprog

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('--retain',type=int,default=0)
    parser.add_argument('--test-master',action='store_true')
    args=parser.parse_args();directory=Path(__file__).parent
    data=json.loads((directory/args.source).read_text())
    sep=Separator(directory/'efficient_bank.json')
    assert data['query_v']==sep.ready['v'] and data['event_labels']==sep.ready['event_labels']
    try:
        result=sep.call(operation='uncross',profiles=[r['labels'] for r in data['princess_mixture']],
            weights=[r['weight'] for r in data['princess_mixture']],retain=args.retain)
        result.update(source=args.source,original_master=data['master_value'],
            source_mixture=data['princess_mixture'],query_v=data['query_v'],event_labels=data['event_labels'],
            scope='Floating common-quantile improvement against every member of the fixed909monster bank; not unrestricted lower guarantee.')
        if args.test_master:
            old=sep.call(operation='rows',profiles=[r['labels'] for r in data['princess_mixture']])['responses']
            rows=old+result['responses'];matrix=np.asarray([r['row'] for r in rows])
            answer=linprog(np.r_[np.zeros(len(rows)),-1.],
                A_ub=np.c_[-matrix.T,np.ones(matrix.shape[1])],b_ub=np.zeros(matrix.shape[1]),
                A_eq=np.array([[1.]*len(rows)+[0.]]),b_eq=[1.],
                bounds=[(0.,None)]*len(rows)+[(None,None)],method='highs')
            assert answer.success,answer.message
            result['augmented_master']=-float(answer.fun)
            result['augmented_mixture']=[dict(labels=rows[i]['labels'],weight=float(p))
                for i,p in enumerate(answer.x[:-1]) if p>1e-11]
        target=directory/'efficient_uncross_probe.json';target.write_text(json.dumps(result,indent=2)+'\n')
        print({k:v for k,v in result.items() if k not in('costs','responses','augmented_mixture')})
    finally:sep.close()
