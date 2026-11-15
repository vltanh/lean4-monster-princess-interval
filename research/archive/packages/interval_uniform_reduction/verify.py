"""Run the exact certificates. This does not certify the unrestricted game value."""
import json,time
from pathlib import Path
from fractions import Fraction
from exact_response import solve,capture
from finite_grid import verify as verify_grid
from check_rejected_dual import verify as verify_rejection
ROOT=Path(__file__).resolve().parent

def main():
    d=json.loads((ROOT/'princess_strategy.json').read_text())
    hs=d['paths_h'];ws=d['weights_h'];S=d['S']
    raw=[[[t,-x]for t,x in p]for p in hs[::-1]]+hs;ww=ws[::-1]+ws
    start=time.time();v,m,stats=solve(raw,ww,S)
    assert v==Fraction(d['value'])
    for route in(m,d['attaining_monster']):
        assert all(abs(y-x)==b-a for(a,x),(b,y)in zip(route,route[1:]))
        value=sum(w*capture(route,p)for w,p in zip(ww,raw))/(sum(ww)*S)
        assert value==v
    print('PASS: all-monster response to the supplied',len(raw),'hider paths:',v)
    print('Exact search statistics:',stats)
    verify_grid(str(ROOT/'grid_case.json'))
    verify_rejection()
    print('Seconds:',time.time()-start)
    print('SCOPE: exact response certificate plus an exact finite-grid saddle. No full-game saddle is claimed.')
if __name__=='__main__':main()
