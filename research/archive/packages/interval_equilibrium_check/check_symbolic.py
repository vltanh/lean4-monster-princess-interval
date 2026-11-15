from fractions import Fraction as Q
from pathlib import Path
import json
import affine as af
from affine import A
ROOT=Path(__file__).resolve().parent
D=json.load(open(ROOT/'certificate.json'));ms=[af.simplify([(A(t),A(x)) for t,x in p]) for p in D['paths']]
qs=list(map(Q,D['duals']));ps=[]
for r,a in zip(D['deadlines'],D['initials']):ps.append(af.witness(ms,list(map(Q,r)),Q(a)))
m=af.simplify([(A(0),A(Q(-15,16))),(A(Q(31,16)),A(1)),(A(Q(63,16)),A(-1))])
# This completion only helps; the simple straight portion already captures all of the displayed witnesses.
value=A(0);caps=[]
for q,p in zip(qs,ps):
    times=[af.meeting(m,p),af.meeting(m,[(t,-x) for t,x in p])];assert all(t is not None for t in times)
    value+=(times[0]+times[1])*(q/2);caps.append([t.data() for t in times])
v=Q(D['value']);assert value<A(v)-Q(1,2)
result=dict(payoff=value.data(),valid_epsilon_radius=str(af.RADIUS),monster=[[t.data(),x.data()] for t,x in m],princess_paths=[[[t.data(),x.data()] for t,x in p] for p in ps],captures=caps)
import sys
if '--check' in sys.argv:
    assert result==json.load(open(ROOT/'dual_family.json'))
else:
    json.dump(result,open(ROOT/'dual_family.json','w'),indent=2)
print('Symbolic counterexample payoff:',value)
print('Valid for 0 < epsilon <',af.RADIUS)
print('Limit =',float(value.a),'against the proposed dual family, not a full-game bound.')
