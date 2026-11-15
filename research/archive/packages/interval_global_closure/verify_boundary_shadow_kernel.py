#!/usr/bin/env python3
"""Exact first-contact checks for the outward/inward/outward boundary shadow.
The tests are finite regressions of explicit analytic kernels, not global values.
"""
from fractions import Fraction as Q
from collections import Counter
from pathlib import Path
import importlib.util,json,hashlib

KERNEL=Path(__file__).with_name('verify_boundary_layer_kernel.py')
if not KERNEL.exists():  # Optional discovery-workspace copy; canonical package uses its sibling.
 KERNEL=Path(__file__).resolve().parents[1]/'finite-reduction-checkout/packages/interval_global_closure/verify_boundary_layer_kernel.py'
spec=importlib.util.spec_from_file_location('boundary_physical',KERNEL)
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)

def shadow(e,h,eta):
 assert 0<eta<=e<=h<1
 return b.clean([(0,1-e),((e-eta)/2,1-(e+eta)/2),((h-eta)/2,1-(h+eta)/2),(h,1),(4,1)])

def direct(a):
 return b.clean([(0,1-a),(2-a,-1),(4-a,1),(4,1)])

def direct_loop(a,e,h):
 if a==e:return 1-a/2
 return 1+h/4-3*a/4 if a<e else 3-a

def direct_shadow(a,e,h,eta):
 if a==e:return 1-a/2,'initial'
 if a>e:return 3-a,'behind'
 if a>=eta:return 1+e/4-3*a/4,'early'
 return 1+h/4-3*a/4,'late'

def inward_shadow(a,z,e,h,eta):
 if a==e:return Q(1),'initial'
 if z<e:return 1+h/4,'front_before_start'
 if eta<=a<e:return 1+(e-a)/4,'initial_inward_hit'
 if a<eta:
  if h<=z:return 1+(h-a)/4,'late_initial_inward_hit'
  return 1+h/4,'final_front'
 assert a>e
 if z<=h:return 1+(z-eta)/4,'outward_hit'
 return Q(3),'escaped_front'

def main():
 grid=[Q(i,10)for i in range(10)]
 count=Counter();dcount=Counter();gain=Counter();sweeps=0
 E=b.monster(Q(0),Q(0))
 for h in grid[1:]:
  for e in grid[1:]:
   if e>h:continue
   for eta in grid[1:]:
    if eta>e:continue
    p=shadow(e,h,eta);old=b.princess(e,h)
    assert b.pair_score(E,p)==1+h/4;sweeps+=1
    for a in grid:
     m=direct(a);expected,case=direct_shadow(a,e,h,eta)
     actual=b.pair_score(m,p)
     assert actual==expected,(a,e,h,eta,actual,expected)
     assert b.pair_score(m,old)==direct_loop(a,e,h)
     dcount[case]+=1
     if a not in (eta,e):
      diff=-(h-e)/4 if eta<a<e else Q(0)
      assert actual-b.pair_score(m,old)==diff
      gain['direct']+=1
     for z in grid:
      if z<a:continue
      m=b.monster(a,z);expected,case=inward_shadow(a,z,e,h,eta)
      actual=b.pair_score(m,p)
      assert actual==expected,(a,z,e,h,eta,actual,expected)
      assert b.contact(m,[(t,-x)for t,x in p])==2
      count[case]+=1
      if a==z and a not in(e,h):
       diff=(e-eta)/4 if e<a<h else Q(0)
       assert actual-b.pair_score(m,old)==diff,(a,e,h,eta)
       gain['outward']+=1
 out={'status':'PASS','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'physical_evaluator_sha256':hashlib.sha256(KERNEL.read_bytes()).hexdigest(),
      'I_cases':sum(count.values()),'I_case_counts':dict(count),
      'D_cases':sum(dcount.values()),'D_case_counts':dict(dcount),
      'fast_sweeps':sweeps,'gain_checks':dict(gain),
      'scope':'Exact rational chronological intersections, including initial, first-turn and front ties; no global equilibrium assertion.'}
 outpath=Path(__file__).with_name('boundary_shadow_kernel_replay.json')
 outpath.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
