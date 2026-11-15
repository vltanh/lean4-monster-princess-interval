"""A global survival/closure cut on a finite monster event arrangement.

There is no fixed initial position, U1 cutoff, or wave count. A monotone
light-coordinate graph U=P(V) crosses t=0 freely. One value is kept at
every monster vertex's V coordinate. Between those queries its limiting
fill is max(previous value,V,0), with a connector just BEFORE the next
query. A dense strict-speed class justifies one shared contact value.
Positive same-polarity AND rewards have an exact maximum-closure
reduction. Fraction inputs give exact arithmetic. Lexicographic labels
retain open contact chambers while ramp lengths use the base value.
"""
from bisect import bisect_left, bisect_right
from collections import deque
from dataclasses import dataclass
from fractions import Fraction as Q
import numpy as np
from monotone_cut import _Flow


def level_key(value):
    return tuple(value) if isinstance(value, (tuple, list)) else (value, 0)


def level_base(value):
    return level_key(value)[0]


def light_route(atom, reflection=False):
    kind, p = atom["kind"], atom["parameters"]
    if kind == "PATH":
        # A complete arbitrary unit-leg monster route, in light coordinates.
        # Flattening preserves the existing rational atom serialization.
        assert len(p) >= 4 and len(p) % 2 == 0
        points = list(zip(p[::2], p[1::2]))
        assert points[0][0] + points[0][1] == 0
        assert all(u+v >= 0 and -2 <= u-v <= 2 for u,v in points)
        walls = {u-v for u,v in points if u-v in (-2,2)}
        assert walls == {-2,2}, "A PATH atom must visit both endpoints"
    elif kind == "M1":
        x, = p
        points = [(x,-x),(2-x,-x),(2-x,4-x)]
    elif kind == "M2":
        x,s = p
        points = [(x,-x),(s,-x),(s,s+2),(s+4,s+2)]
    elif kind == "M3":
        x,s,t = p
        points = [(x,-x),(s,-x),(s,t),(t+2,t),(t+2,t+4)]
    else:
        assert kind == "I"
        z,v,s = p
        points = [(z,-z),(z,v),(s,v),(s,s+2),(s+4,s+2)]
    result = []
    for u,v in points:
        point = (v,u) if reflection else (u,v)
        if not result or point != result[-1]:
            result.append(point)
    for (u0,v0),(u1,v1) in zip(result,result[1:]):
        assert ((u1>u0 and v1==v0) or (v1>v0 and u1==u0)), (atom,result)
    return tuple(result)


@dataclass
class SurvivalResult:
    value: object
    minimum_values: tuple
    maximum_values: tuple
    labels: tuple
    maximum_labels: tuple
    threshold_nodes: int
    auxiliary_nodes: int
    reward_terms: int
    face: dict | None


class SurvivalCut:
    def __init__(self, atoms, trace=0, lexicographic=False):
        assert not (trace and lexicographic)
        self.atoms,self.trace = tuple(atoms),trace
        self.lexicographic = lexicographic
        self.routes = tuple((light_route(a),light_route(a,True)) for a in atoms)
        vertices = [point for pair in self.routes for route in pair for point in route]
        self.v = tuple(sorted({-1}|{v for u,v in vertices}))
        assert self.v[0] == -1
        self.end = self.v[-1]
        levels = {0,self.end+2}|{u for u,v in vertices if u>=0}
        levels |= {max(0,v) for v in self.v}|{v+2 for v in self.v}
        if trace:
            levels |= {u+d*trace for u in tuple(levels) for d in (-1,1)
                       if 0<=u+d*trace<=self.end+2}
        self.levels = (tuple((u,side) for u in sorted(levels) for side in (-1,0,1))
                       if lexicographic else tuple(sorted(levels)))
        self.keys = tuple(level_key(value) for value in self.levels)
        self.bounds = [(bisect_left(self.keys,(max(0,v),0)),
                        bisect_right(self.keys,(v+2,0))-1) for v in self.v]
        initial = self.keys.index((0,0))
        self.bounds[0] = (initial,initial)
        last = self.keys.index((self.end+2,0))
        self.bounds[-1] = (last,last)
        self.query = {v:j for j,v in enumerate(self.v)}
        self._unit_rewards = [None]*len(atoms)

    def bit(self,u,v,positive):
        index = self.query[v]
        threshold = (bisect_right(self.keys,(u,0)) if positive
                     else bisect_left(self.keys,(u,0)))
        return index,threshold

    def normalize(self,positive,bits):
        merged = {}
        for i,k in bits:
            lo,hi = self.bounds[i]
            if positive:
                if k<=lo: continue
                if k>hi: return None
                merged[i] = max(k,merged.get(i,k))
            else:
                if k<=lo: return None
                if k>hi: continue
                merged[i] = min(k,merged.get(i,k))
        ordered = sorted(merged.items())
        if positive:
            result,highest = [],-1
            for i,k in ordered:
                if k>highest:
                    result.append((i,k))
                    highest=k
        else:
            result,lowest = [],len(self.levels)+1
            for i,k in reversed(ordered):
                if k<lowest:
                    result.append((i,k))
                    lowest=k
            result.reverse()
        return tuple(result)

    def unit_rewards(self,atom_index):
        cached = self._unit_rewards[atom_index]
        if cached is not None: return cached
        rewards = {}
        def add(positive,bits,weight):
            if not weight: return
            assert weight>0
            normal = self.normalize(positive,bits)
            if normal is not None:
                key = positive,normal
                rewards[key] = rewards.get(key,0)+weight
        for route in self.routes[atom_index]:
            u0,v0 = route[0]
            above = [self.bit(u0,v0,True)]
            below = [self.bit(u0,v0,False)]
            for (u0,v0),(u1,v1) in zip(route,route[1:]):
                if u1>u0:
                    length = u1-u0
                    index = self.query[v0]
                    ramp = [max(0,min(level_base(u),u1)-u0) for u in self.levels]
                    add(True,above,ramp[0])
                    for k in range(1,len(ramp)):
                        add(True,above+[(index,k)],ramp[k]-ramp[k-1])
                    add(False,below,length)
                else:
                    length = v1-v0
                    add(True,above,length)
                    left,right = self.query[v0],self.query[v1]
                    threshold = bisect_left(self.keys,(u0,0))
                    for j in range(left,right):
                        width = max(0,min(self.v[j+1],u0)-self.v[j])
                        add(False,below+[(j,threshold)],width)
                above.append(self.bit(u1,v1,True))
                below.append(self.bit(u1,v1,False))
        self._unit_rewards[atom_index]=rewards
        return rewards

    def rewards(self,weights):
        result={}
        for j,weight in enumerate(weights):
            assert weight>=0
            if weight:
                for key,value in self.unit_rewards(j).items():
                    result[key]=result.get(key,0)+weight*value
        return result

    def solve(self,weights,tolerance=0,retain_face=False):
        rewards=self.rewards(weights)
        nlevels,nvariables=len(self.levels),len(self.v)
        threshold_count=nvariables*(nlevels-1)
        linear=[0]*threshold_count
        hard,constant=[],0
        def node(i,k):
            assert 1<=k<nlevels
            return i*(nlevels-1)+k-1
        for (positive,bits),weight in rewards.items():
            if not bits:
                constant+=weight
                continue
            endpoints=[node(i,k) for i,k in bits]
            if len(bits)==1:
                if positive:
                    linear[endpoints[0]]+=weight
                else:
                    constant+=weight
                    linear[endpoints[0]]-=weight
            else:
                auxiliary=len(linear)
                linear.append(weight if positive else -weight)
                if positive:
                    hard.extend((auxiliary,end) for end in endpoints)
                else:
                    constant+=weight
                    hard.extend((end,auxiliary) for end in endpoints)
        auxiliary_count=len(linear)-threshold_count
        for i in range(nvariables):
            hard.extend((node(i,k),node(i,k-1)) for k in range(2,nlevels))
        for i in range(nvariables-1):
            hard.extend((node(i,k),node(i+1,k)) for k in range(1,nlevels))
        source,sink=len(linear),len(linear)+1
        graph=_Flow(len(linear)+2,tolerance=tolerance)
        infinity=1+sum(abs(value) for value in linear)
        upper=constant
        for j,value in enumerate(linear):
            if value>=0:
                graph.add(source,j,value)
                upper+=value
            else:
                graph.add(j,sink,-value)
        for left,right in hard:
            graph.add(left,right,infinity)
        for i,(lo,hi) in enumerate(self.bounds):
            if lo: graph.add(source,node(i,lo),infinity)
            if hi+1<nlevels: graph.add(node(i,hi+1),sink,infinity)
        flow,reachable=graph.solve(source,sink,infinity)
        reverse=[[] for _ in graph.graph]
        for left,edges in enumerate(graph.graph):
            for edge in edges:
                if edge.cap>tolerance:
                    reverse[edge.to].append(left)
        ancestors,queue={sink},deque([sink])
        while queue:
            for left in reverse[queue.popleft()]:
                if left not in ancestors:
                    ancestors.add(left)
                    queue.append(left)
        labels=tuple(sum(node(i,k) in reachable for k in range(1,nlevels))
                     for i in range(nvariables))
        maximum_labels=tuple(sum(node(i,k) not in ancestors for k in range(1,nlevels))
                             for i in range(nvariables))
        minimum_values=tuple(self.levels[k] for k in labels)
        maximum_values=tuple(self.levels[k] for k in maximum_labels)
        for label_vector in (labels,maximum_labels):
            assert all(lo<=label_vector[i]<=hi for i,(lo,hi) in enumerate(self.bounds))
            assert all(x<=y for x,y in zip(label_vector,label_vector[1:]))
        actual=constant+sum(linear[j] for j in range(len(linear)) if j in reachable)
        allowed=tolerance*max(1,len(graph.original))
        assert abs(actual-(upper-flow))<=allowed
        independent=sum(weight*self.atom_value(atom,minimum_values)
                        for atom,weight in zip(self.atoms,weights))
        independent_max=sum(weight*self.atom_value(atom,maximum_values)
                            for atom,weight in zip(self.atoms,weights))
        assert abs(actual/4-independent)<=allowed,(actual/4,independent)
        assert abs(actual/4-independent_max)<=allowed,(actual/4,independent_max)
        face=None
        if retain_face:
            free=[j for j in range(len(linear)) if j not in reachable and j not in ancestors]
            free_index={j:k for k,j in enumerate(free)}
            edges=sorted({(free_index[j],free_index[e.to])
                          for j in free for e in graph.graph[j]
                          if e.cap>tolerance and e.to in free_index})
            face=dict(scope="Residual closure face at supplied arithmetic/tolerance; physical limiting realization remains explicit.",
                      free_nodes=free,implications=edges,
                      threshold_node_count=threshold_count,
                      threshold_node_layout="node=i*(label_count-1)+k-1 for [P(V_i)>=level_k]",
                      label_count=nlevels,
                      forced_true_thresholds=[j for j in range(threshold_count) if j in reachable],
                      forced_false_thresholds=[j for j in range(threshold_count) if j in ancestors])
        return SurvivalResult(actual/4,minimum_values,maximum_values,labels,
                              maximum_labels,threshold_count,auxiliary_count,len(rewards),face)

    def p_value(self,v,values):
        j=bisect_left(self.v,v)
        if j<len(self.v) and self.v[j]==v:
            return values[j]
        if self.lexicographic:
            return max(level_key(values[j-1]),(v,0),(0,0))
        return max(values[j-1],v,0)

    def oriented_capture(self,route,values):
        u0,v0=route[0]
        initial=self.p_value(v0,values)
        if level_key(initial)==(u0,0):
            return (u0+v0)/2
        above=level_key(initial)>(u0,0)
        for (u0,v0),(u1,v1) in zip(route,route[1:]):
            if u1>u0 and above:
                crossing=self.p_value(v0,values)
                if level_key(crossing)<=(u1,0):
                    assert level_key(crossing)>=(u0,0)
                    return (level_base(crossing)+v0)/2
            elif v1>v0 and not above:
                at=bisect_left(tuple(level_key(value) for value in values),(u0,0))
                assert at<len(values)
                crossing=min(u0,self.v[at])
                if crossing<=v1:
                    assert crossing>=v0
                    return (u0+crossing)/2
        raise AssertionError(("No capture before completed endpoint sweeps",route,values))

    def atom_value(self,atom,values):
        return (self.oriented_capture(light_route(atom),values)
                +self.oriented_capture(light_route(atom,True),values))/2

    def row(self,atoms,values):
        return tuple(self.atom_value(atom,values) for atom in atoms)

    def realize(self,values,epsilon=Q(1,2**50),strict=True):
        vv=tuple(Q(v) for v in self.v)
        epsilon=Q(epsilon)
        if self.lexicographic:
            values=tuple(Q(level_base(p))+level_key(p)[1]*epsilon for p in values)
            connector=epsilon**2
        else:
            values=tuple(Q(p) for p in values)
            connector=epsilon
        points=[(Q(0),Q(-1))]
        def add(u,v):
            if (u,v)==points[-1]: return
            assert u>=points[-1][0] and v>=points[-1][1]
            assert 0<=u-v<=2
            points.append((u,v))
        for j in range(1,len(vv)):
            v,previous,target=vv[j],values[j-1],values[j]
            delta=min(connector,(v-vv[j-1])/3)
            before=v-delta
            add(previous,min(before,previous))
            if before>previous: add(before,before)
            add(min(target,before+2),before)
            if target>before+2: add(target,target-2)
            add(target,v)
        path=[]
        for (u0,v0),(u1,v1) in zip(points,points[1:]):
            t0,t1=(u0+v0)/2,(u1+v1)/2
            if t1<0: continue
            x0,x1=(u0-v0)/2,(u1-v1)/2
            if not path:
                if t0<=0:
                    x=x0+(x1-x0)*(-t0)/(t1-t0)
                    path.append((Q(0),x))
                else:
                    raise AssertionError("Virtual curve skipped time zero")
            if t1>path[-1][0]:
                path.append((t1,x1))
        if strict:
            eta=epsilon**6 if self.lexicographic else epsilon**3
            path=[(t,(1-2*eta)*x+eta) for t,x in path]
        for (t0,x0),(t1,x1) in zip(path,path[1:]):
            assert 0<=x0<=1 and 0<=x1<=1
            assert t1>t0 and abs(x1-x0)<=t1-t0
        return path
