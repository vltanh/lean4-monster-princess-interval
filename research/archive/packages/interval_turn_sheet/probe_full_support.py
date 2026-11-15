#!/usr/bin/env python3
"""Inspect turn geometry on one fixed eighth-grid support.

The objective is numerical support discovery, not an exact value claim.
Endpoint-start paths with a premature reversal are omitted because the
direct sweep from the same endpoint captures every path no later.
"""
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'packages/interval_continuum_discovery'))
from direct_support import solve_support
from integer_geometry import clean,mirror


def main():
    n=8
    scale=4*n
    names=[]
    representatives=[]
    seen=set()
    for ix in range(-n,n+1):
        for ic in range(ix,2*n-ix+1):
            if abs(ix)==n and ic not in (ix,2*n-ix):
                continue
            x,c=4*ix,4*ic
            path=[[0,x],[(c-x)//2,(c+x)//2],
                  [c+scale,-scale],[c+3*scale,scale]]
            if c+x==2*scale:
                path=path[:-1]
            path=clean(path)
            if abs(ix)==n:
                path=[[0,x],[2*scale,-x]]
            key=min(tuple(map(tuple,path)),tuple(map(tuple,mirror(path))))
            if key in seen:
                continue
            seen.add(key)
            names.append([ix/n,ic/n])
            representatives.append(path)
    paths=[p for representative in representatives
           for p in (representative,mirror(representative))]
    result=solve_support(paths,scale)
    result['names']=names
    result['scope']='Floating fixed eighth-grid support geometry; not a game certificate.'
    Path(__file__).with_name('full_support.json').write_text(json.dumps(result)+'\n')
    print('ACTIVE',[(name,w) for name,w in zip(names,result['weights']) if w>1e-8],flush=True)


if __name__=='__main__':
    main()
