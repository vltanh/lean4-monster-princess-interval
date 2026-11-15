"""One final fixed-complexity negative-C1 test with moving analytic attacks."""
from pathlib import Path
import importlib.util,json,time
import numpy as np
from scipy.optimize import differential_evolution
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('fixed_wave',HERE/'five_leg_fixed_wave.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
original_moving=f.moving_routes

def special_route(law,mode=0):
 x=min(1.,law.incoming[0][0]);s=max(1.,law.incoming[0][-1])
 desired=-law.a[0] if mode==0 else min(-law.a[0],law.outgoing[0][-1])
 v=max(-x,s-2,min(x,desired))
 return f.clean([(0,x),((x+v)/2,(x-v)/2),((s+v)/2,(s-v)/2),(s+1,-1),(s+3,1)])

def moving(law):
 return original_moving(law)+[(f'analytic_first_wave_{mode}',special_route(law,mode)) for mode in [0,1]]
f.moving_routes=moving

def critical_oracle(law):
 results=[]
 ss=sorted(set([1.,max(1.,law.incoming[0][-1]),law.incoming[1][0],law.incoming[1][-1]]))
 for index,s in enumerate(ss):
  def route(z):
   x=z[0];low=max(-x,s-2);high=x;v=low+(high-low)*z[1]
   return f.clean([(0,x),((x+v)/2,(x-v)/2),((s+v)/2,(s-v)/2),(s+1,-1),(s+3,1)])
  opt=differential_evolution(lambda z:law.payoff(route(z)).value,[(0,1),(0,1)],seed=411+index,popsize=7,maxiter=30,tol=1e-8,polish=True)
  path=route(opt.x);results.append(dict(name=f'critical_U_two_turn_{s}',value=law.payoff(path).value,route=path))
  # Quantile-boundary faces can be much narrower than a generic search step.
  for initial in law.incoming[0]:
   x=min(1.,initial)
   for initial_a in law.a:
    v=max(-x,s-2,min(x,-initial_a))
    path=f.clean([(0,x),((x+v)/2,(x-v)/2),((s+v)/2,(s-v)/2),(s+1,-1),(s+3,1)])
    results.append(dict(name=f'critical_rank_face_U{s}',value=law.payoff(path).value,route=path))
  def one_turn(z):return f.via([z[0],(s+z[0])/2,-1,1])
  op=differential_evolution(lambda z:law.payoff(one_turn(z)).value,[(-1,min(s,2-s))],seed=511+index,popsize=7,maxiter=25,tol=1e-8,polish=True)
  path=one_turn(op.x);results.append(dict(name=f'critical_U_one_turn_{s}',value=law.payoff(path).value,route=path))
 results.sort(key=lambda row:row['value'])
 return results

def main():
 start=time.time();etas=[1/64,1/32,1/16,1/8,1/4,1/2]
 starts=sorted(set([i/8 for i in range(-8,9)]+[sign*(1-eta) for eta in etas for sign in [-1,1]]))
 cuts=[(f'M{kind}({x})',builder(x)) for kind,builder in [(1,f.m1),(2,f.m2)] for x in starts]
 cuts.extend((f'Q({eta})',f.shifted(eta)) for eta in etas)
 previous=json.load(open(HERE/'five_leg_fixed_wave.json'))
 for index,row in enumerate(previous['seed_results']+previous['history']):
  for response in row['responses'][:3]:cuts.append((f'prior_{index}_{response["name"]}',response['route']))
 seed=np.r_[[0,.6,.9,.999],[.6,.7,.96,.9995],[.6,.2,-.5,-.99],[.95,.8,.3,-.98],.08]
 seed=f.project(seed);initial=f.law_from(seed)
 print('INITIAL',f.law_data(initial),flush=True)
 print('INITIAL_ANALYTIC_ROUTES',[(i,initial.payoff(special_route(initial,i)).value) for i in [0,1]],flush=True)
 z,summary=f.optimize(seed,cuts,maxiter=100)
 law=f.law_from(z)
 print('FIT',time.time()-start,summary,flush=True)
 print('LAW',f.law_data(law),flush=True)
 responses=f.oracle(law,2150,deep=True)
 critical=critical_oracle(law)
 output=dict(scope='One bounded negative-outer-C1 structural test, not a game-value certificate.',
             epsilon=.001,q_knots=f.Q.tolist(),initial_law=f.law_data(initial),
             law=f.law_data(law),optimization=summary,responses=responses,
             critical_responses=critical,seconds=time.time()-start,
             analytic_routes=[dict(mode=i,value=law.payoff(special_route(law,i)).value,route=special_route(law,i)) for i in [0,1]])
 narrow=[]
 for eta in [.001,.0010005,.001001]:
  for name,builder in [('F',lambda e:f.m1(1-e)),('L',lambda e:f.m1(-1+e)),('Q',f.shifted)]:
   route=builder(eta);narrow.append(dict(name=f'{name}({eta})',route=route,value=law.payoff(route).value))
 output['narrow_wave_probes']=sorted(narrow,key=lambda row:row['value'])
 json.dump(output,open(HERE/'five_leg_negative_branch.json','w'),indent=2)
 for response in sorted(responses+critical,key=lambda row:row['value'])[:8]:print('RESPONSE',response,flush=True)
 print('DONE',time.time()-start,flush=True)
if __name__=='__main__':main()
