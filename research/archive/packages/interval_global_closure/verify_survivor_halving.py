"""Exact regression for the global survivor-halving response recurrence.

The continuum theorem is proved in the companion note. This executable
compares one-target-at-a-time DP with capture-mass macro recurrence on
finite ordered moving-target fixtures. Its finite action sets are TEST
MODELS, not a finite discretization certificate for the full game.
All scores and contact times use fractions.Fraction.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
from itertools import permutations, product
import json

ZERO, ONE, TWO, FOUR = Q(0), Q(1), Q(2), Q(4)

@dataclass(frozen=True)
class Path:
    vertices: tuple[tuple[Q, Q], ...]

    def __post_init__(self):
        assert self.vertices and self.vertices[0][0] == 0
        assert all(-1 <= x <= 1 for _, x in self.vertices)
        assert all(b > a and abs(y-x) <= b-a
                   for (a,x),(b,y) in zip(self.vertices,self.vertices[1:]))

    def at(self, t: Q) -> Q:
        assert t >= 0
        for (a,x),(b,y) in zip(self.vertices,self.vertices[1:]):
            if a <= t <= b:
                return x+(y-x)*(t-a)/(b-a)
        return self.vertices[-1][1]

    def chase(self, t: Q, x: Q, direction: int) -> Q:
        """First exact contact with the unit ray from (t,x)."""
        assert direction in (-1,1)
        end = t+(1-x if direction == 1 else x+1)
        knots = sorted({t,end} | {s for s,_ in self.vertices if t < s < end})
        if x == self.at(t):
            return t
        for a,b in zip(knots,knots[1:]):
            da=x+direction*(a-t)-self.at(a)
            db=x+direction*(b-t)-self.at(b)
            if da == 0:
                return a
            if db == 0 or da*db < 0:
                return a+(b-a)*(-da)/(db-da)
        raise ValueError('Target is not ahead of selected ray')


def direct_hit(route: tuple[tuple[Q,Q],...], target: Path) -> Q:
    """Independent physical first-hit engine on a finite polygonal route."""
    for (t,x),(u,y) in zip(route,route[1:]):
        knots=sorted({t,u}|{s for s,_ in target.vertices if t < s < u})
        for a,b in zip(knots,knots[1:]):
            ma=x+(y-x)*(a-t)/(u-t)
            mb=x+(y-x)*(b-t)/(u-t)
            da,db=ma-target.at(a),mb-target.at(b)
            if da==0:
                return a
            if db==0 or da*db<0:
                return a+(b-a)*(-da)/(db-da)
    t,x=route[-1]
    if x==target.at(t):
        return t
    raise ValueError('Route has not captured this target')

State=tuple[Q,Q,tuple[int,...]]

class Model:
    def __init__(self, targets: tuple[Path,...], weights: tuple[Q,...]):
        assert len(targets)==len(weights)>0
        assert all(w>0 for w in weights) and sum(weights)==1
        self.targets,self.weights=targets,weights
        knots=sorted({t for p in targets for t,_ in p.vertices})
        for t in knots:
            xs=[p.at(t) for p in targets]
            assert xs==sorted(xs), 'The targets must be ordered throughout time'

    def mass(self, alive: tuple[int,...]) -> Q:
        return sum((self.weights[i] for i in alive),ZERO)

    def state(self,t:Q,x:Q,alive:tuple[int,...]|None=None)->State:
        if alive is None: alive=tuple(range(len(self.targets)))
        return (t,x,tuple(i for i in alive if self.targets[i].at(t)!=x))

    @lru_cache(None)
    def moves(self,z:State)->tuple[tuple[Q,State],...]:
        t,x,alive=z
        if not alive:return ()
        left=[i for i in alive if self.targets[i].at(t)<x]
        right=[i for i in alive if self.targets[i].at(t)>x]
        out=[]
        for direction,indices in [(-1,left),(1,right)]:
            if not indices:continue
            nxt=max(indices) if direction==-1 else min(indices)
            u=self.targets[nxt].chase(t,x,direction)
            y=x+direction*(u-t)
            zz=self.state(u,y,alive)
            assert len(zz[2])<len(alive)
            out.append((u-t,zz))
        return tuple(out)

    @lru_cache(None)
    def micro(self,z:State)->Q:
        if not z[2]:return ZERO
        mass=self.mass(z[2])
        return min(dt+self.mass(zz[2])/mass*self.micro(zz)
                   for dt,zz in self.moves(z))

    @lru_cache(None)
    def macro(self,z:State)->tuple[tuple[Q,Q,State],...]:
        """All canonical capture prefixes ending below half mass by time 4.

        Enumerates a finite TEST model. Does not claim to compute the
        continuum Bellman operator for arbitrary terminal functions.
        """
        if not z[2]:return ()
        mass0=self.mass(z[2]); start=z[0]; out=[]
        def visit(cur:State,cost:Q):
            mass=self.mass(cur[2])
            if mass<=mass0/2:
                out.append((cost,mass/mass0,cur))
            for dt,zz in self.moves(cur):
                if zz[0]-start<=4:
                    visit(zz,cost+mass/mass0*dt)
        visit(z,ZERO)
        assert out
        return tuple(out)

    @lru_cache(None)
    def iterate(self,z:State,n:int,upper:bool=False)->Q:
        if not z[2]:return ZERO
        if n==0:return TWO if upper else ZERO
        return min(c+beta*self.iterate(zz,n-1,upper)
                   for c,beta,zz in self.macro(z))

    @lru_cache(None)
    def optimal_route(self,z:State)->tuple[tuple[Q,Q],...]:
        if not z[2]:return ((z[0],z[1]),)
        mass=self.mass(z[2]); options=self.moves(z)
        dt,zz=min(options,key=lambda a:a[0]+self.mass(a[1][2])/mass*self.micro(a[1]))
        return ((z[0],z[1]),)+self.optimal_route(zz)

    def permutation_min(self,z:State)->Q:
        """Independent all-order chase and direct chronological score."""
        assert len(z[2])<=6
        mass=self.mass(z[2]); best=None
        for order in permutations(z[2]):
            t,x,_=z; route=[(t,x)]
            for i in order:
                try:
                    direct_hit(tuple(route),self.targets[i]);continue
                except ValueError:pass
                y=self.targets[i].at(t)
                if y==x:continue
                d=1 if y>x else -1
                u=self.targets[i].chase(t,x,d)
                x=x+d*(u-t);t=u;route.append((t,x))
            score=sum((self.weights[i]*(direct_hit(tuple(route),self.targets[i])-z[0])
                       for i in z[2]),ZERO)/mass
            best=score if best is None else min(best,score)
        assert best is not None
        return best


def static(x:Q)->Path:return Path(((ZERO,x),))

def drifting(x:Q,v:Q)->Path:
    if v==0:return static(x)
    endpoint=ONE if v>0 else -ONE
    finish=(endpoint-x)/v
    return static(x) if finish==0 else Path(((ZERO,x),(finish,endpoint)))

def inward_pair(a:Q)->tuple[Path,Path]:
    # Common-quantile, noncrossing realization; paths meet at time a.
    return (Path(((ZERO,-a),(a,ZERO),(a+1,-ONE))),
            Path(((ZERO,a),(a,ZERO),(a+1,ONE))))


def check_cdf_restart(model:Model,z:State)->int:
    """Check clipped-CDF posterior against explicit survivor path law."""
    t,x,alive=z
    if not alive:return 0
    # Every state used here has a captured contiguous index interval.
    missing=[i for i in range(len(model.targets)) if i not in alive]
    if not missing:return 0
    assert missing==list(range(min(missing),max(missing)+1))
    a=sum(model.weights[:min(missing)],ZERO)
    b=sum(model.weights[:max(missing)+1],ZERO)
    mass=model.mass(alive);assert mass==a+1-b
    checks=0
    for dt in [ZERO,Q(1,3),ONE,TWO]:
        vals={-ONE,-Q(1,2),ZERO,Q(1,2),ONE}
        vals|={p.at(t+dt) for p in model.targets}
        for y in vals:
            for closed in [False,True]:
                cmp=lambda v: v<=y if closed else v<y
                F=sum((w for p,w in zip(model.targets,model.weights) if cmp(p.at(t+dt))),ZERO)
                clipped=(min(F,a)+max(F-b,ZERO))/mass
                actual=sum((model.weights[i] for i in alive if cmp(model.targets[i].at(t+dt))),ZERO)/mass
                assert clipped==actual
                checks+=1
    return checks



def endpoint_tour(x:Q, first:int)->tuple[tuple[Q,Q],...]:
    route=[(ZERO,x)]
    t=abs(Q(first)-x)
    if t>0:route.append((t,Q(first)))
    route.append((t+2,Q(-first)))
    return tuple(route)


def check_universal_two_tour_bound()->int:
    count=0
    grid=[Q(k,4) for k in range(-4,5)]
    for xs in product(grid,repeat=3):
        if abs(xs[1]-xs[0])>1 or abs(xs[2]-xs[1])>1:continue
        p=Path(((ZERO,xs[0]),(ONE,xs[1]),(TWO,xs[2])))
        for x in [-ONE,-Q(1,2),ZERO,Q(1,2),ONE]:
            L=direct_hit(endpoint_tour(x,-1),p)
            R=direct_hit(endpoint_tour(x,1),p)
            assert L+R<=4
            count+=1
    return count


def main()->dict:
    result={'two_tour_pointwise_checks':check_universal_two_tour_bound(),'models':0,'initial_states':0,'iterative_brackets':0,
            'physical_routes':0,'all_order_oracles':0,'posterior_identities':0}
    datasets=[]
    for v in [Q(-1,2),ZERO,Q(1,2)]:
        for n in [3,4,5]:
            xs=tuple(-ONE+Q(2*i,n-1) for i in range(n))
            paths=tuple(drifting(x,v) for x in xs)
            for raw in [tuple([1]*n),tuple(2**min(i,n-1-i) for i in range(n)),tuple(range(1,n+1))]:
                weights=tuple(Q(w,sum(raw)) for w in raw)
                datasets.append(Model(paths,weights))
    for a in [Q(1,4),Q(1,2),Q(3,4),ONE]:
        datasets.append(Model(inward_pair(a),(Q(1,2),Q(1,2))))
    for model in datasets:
        result['models']+=1
        for x in [-ONE,-Q(1,4),ZERO,Q(1,3),ONE]:
            z=model.state(ZERO,x)
            if not z[2]:continue
            result['initial_states']+=1
            truth=model.micro(z);assert ZERO<=truth<=2
            assert model.permutation_min(z)==truth
            result['all_order_oracles']+=1
            route=model.optimal_route(z)
            physical=sum((model.weights[i]*direct_hit(route,model.targets[i]) for i in z[2]),ZERO)/model.mass(z[2])
            assert physical==truth
            result['physical_routes']+=1
            lo_prev=ZERO;hi_prev=TWO
            for n in range(7):
                lo=model.iterate(z,n);hi=model.iterate(z,n,True)
                assert lo_prev<=lo<=truth<=hi<=hi_prev
                assert hi-lo<=Q(2,2**n)
                lo_prev,hi_prev=lo,hi
                result['iterative_brackets']+=1
            assert lo==hi==truth  # These small finite models finish exactly.
            for _,_,zz in model.macro(z):
                result['posterior_identities']+=check_cdf_restart(model,zz)
    # Same time, position and survival mass; different rank tails.
    model=Model(tuple(static(x) for x in [-ONE,-Q(1,2),Q(1,2),ONE]),(Q(1,4),)*4)
    zA=model.state(TWO,ZERO,(0,3));zB=model.state(TWO,ZERO,(2,3))
    assert model.mass(zA[2])==model.mass(zB[2])==Q(1,2)
    assert model.micro(zA)==2 and model.micro(zB)==Q(3,4)
    result['memory_counterexample']={'same_time':2,'same_position':0,'same_survival':'1/2',
                                    'two_outer_tails_value':'2','right_tail_only_value':'3/4'}
    # The arbitrary half-survival mark need not correspond to a turn.
    # Fixed start -1, stationary targets -1,0,1: the Monster's optimal
    # route remains a single unit-speed segment through the time-1 mark.
    three=Model(tuple(static(x) for x in [-ONE,ZERO,ONE]),(Q(1,3),)*3)
    start=three.state(ZERO,-ONE)
    straight=((ZERO,-ONE),(ONE,ZERO),(TWO,ONE))
    physical_hits=tuple(direct_hit(straight,p) for p in three.targets)
    assert physical_hits==(ZERO,ONE,TWO)
    assert start[2]==(1,2)
    assert three.micro(start)==Q(3,2)
    # Initially there are two equal-mass conditional survivors; at time
    # one one is caught, but the control has no reversal or speed switch.
    assert three.mass(start[2])==Q(2,3)
    assert three.mass((2,))==Q(1,3)
    result['halving_is_not_a_turn']={'response':'3/2',
          'conditional_survival_at_time_1':'1/2',
          'optimal_motion':'single unit-speed rightward segment'}
    print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    report=main()
    Path_ = __import__('pathlib').Path
    Path_(__file__).with_suffix('.report.json').write_text(json.dumps(report,indent=2)+'\n')
