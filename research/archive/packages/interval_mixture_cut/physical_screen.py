"""Exact physical-marginal diagnostics and an explicit Princess-loop cut.

The loop value is a response lower for ONE supplied Monster law. It is
never a game-value lower or a bound on a family with variable probabilities.
"""
from collections import defaultdict
from fractions import Fraction as Q
import hashlib
import json

import numpy as np


def candidate_law(master, numerators, denominator=10**12):
    return {"n": master.n, "weight_denominator": str(denominator),
            "paths": [dict(c["plan"], weight_numerator=str(w))
                      for c, w in zip(master.columns, numerators) if w > 0]}


def analyze_physical_law(law):
    """Validate paths and aggregate reflected geometry, ignoring dead suffixes."""
    n, W = int(law["n"]), int(law["weight_denominator"])
    if n < 1 or W <= 0:
        raise ValueError("invalid physical law scale")
    R = 2*n
    masses = defaultdict(Q)
    baseline = endpoint_mass = Q(0)
    maximum_interior = None
    endpoint_sweeps = True
    total = 0
    for plan in law["paths"]:
        weight = int(plan["weight_numerator"])
        if weight <= 0:
            raise ValueError("nonpositive physical probability")
        total += weight
        probability = Q(weight, W)
        x = int(plan["start_grid"])
        if abs(x) > R:
            raise ValueError("physical start outside arena")
        first = {x: 0} if x in (-R, 0, R) else {}
        moves = plan["moves"]
        for j, direction in enumerate(moves, 1):
            if direction not in (-1, 1):
                raise ValueError("non-unit physical step")
            x += direction
            if abs(x) > R:
                raise ValueError("physical path outside arena")
            if x in (-R, 0, R) and x not in first:
                first[x] = j
        if not all(x in first for x in (-R, 0, R)) or first[0] > 4*n:
            raise ValueError("physical path misses an endpoint or center deadline")
        if max(first[-R], first[R]) > 16*n:
            raise ValueError("physical path exceeds certificate horizon")
        baseline += probability*Q(first[-R]+first[R], 4*n)
        start = int(plan["start_grid"])
        if abs(start) == R:
            endpoint_mass += probability
            direction = -1 if start > 0 else 1
            endpoint_sweeps &= moves[:4*n] == [direction]*(4*n)
        else:
            maximum_interior = max(maximum_interior or 0, abs(start))
        runs = []
        for direction in moves[:max(first[-R], first[R])]:
            if runs and runs[-1][0] == direction:
                runs[-1] = (direction, runs[-1][1]+1)
            else:
                runs.append((direction, 1))
        direct = start, tuple(runs)
        reflected = -start, tuple((-d, count) for d, count in runs)
        masses[min(direct, reflected)] += probability
    if total != W:
        raise ValueError("physical probabilities do not sum to one")
    gap = Q(1) if maximum_interior is None else 1-Q(maximum_interior, R)
    rows = [[start, list(runs), str(p)] for (start, runs), p in sorted(masses.items())]
    encoded = json.dumps([n, rows], separators=(",", ":")).encode()
    geometry = json.dumps([n, [row[:2] for row in rows]], separators=(",", ":")).encode()
    result = {
        "scope": "Exact diagnostics of this one physical law; no game-value lower or variable-mixture obstruction.",
        "reflected_physical_pairs": len(masses),
        "physical_marginals_sha256": hashlib.sha256(encoded).hexdigest(),
        "physical_geometry_sha256": hashlib.sha256(geometry).hexdigest(),
        "endpoint_baseline": str(baseline), "endpoint_sweep_mass": str(endpoint_mass),
        "initial_gap": str(gap), "endpoint_loop_supported": bool(endpoint_sweeps),
    }
    if endpoint_sweeps:
        result["endpoint_loop_supremum_lower"] = str(baseline+endpoint_mass*gap/4)
    return result, dict(masses)


def marginal_change(current, seed):
    keys = current.keys() | seed.keys()
    l1 = sum((abs(current.get(k, Q(0))-seed.get(k, Q(0))) for k in keys), Q(0))
    new_mass = sum((p for key, p in current.items() if key not in seed), Q(0))
    return {"physical_probability_l1_from_seed": str(l1),
            "physical_probability_total_variation_from_seed": str(l1/2),
            "new_physical_path_mass": str(new_mass),
            "new_physical_paths": sum(key not in seed for key in current),
            "only_calendars_changed": l1 == 0}


def endpoint_loop_field(master,h,epsilon):
    """Strict radial traces of one explicit, endpoint-stopped radial loop."""
    assert 0<epsilon<=h and epsilon+h<=2
    field=np.zeros(master.K,dtype=np.uint8)
    for j in range(4*master.n+1):
        time=Q(j,2*master.n)
        if time>=h:break
        radius=1-epsilon-time if time<=(h-epsilon)/2 else 1-h+time
        radial_units=2*master.n*radius
        # Strict traces preserve the cone inequality into endpoint arrival.
        first=radial_units.numerator//radial_units.denominator+1
        if (first+j)%2:first+=1
        for k in range(max(1,first),2*master.n+1,2):field[master.index[j,k]]=1
    if any(field[a]>field[b] for a,b in master.order):
        raise AssertionError("explicit loop field violates Qout transport")
    return field


def rectangle_field(master,a,b):
    if not 1<=a<=master.n or not 1-a<=b<=a:raise ValueError("invalid loop rectangle")
    epsilon=Q(2*master.n-2*a+1,2*master.n)
    h=Q(2*master.n-2*b+1,2*master.n)
    return endpoint_loop_field(master,h,epsilon)


class EndpointLoopSeparator:
    """Separate ALL n(n+1) nonempty one-turn loop fields in O(n^2).

    At light indices u=(j+k)/2, v=(k-j)/2, strict loop fields are exactly
    {u>=a,v>=b}, 1<=a<=n and 1-a<=b<=a. The short h<1 subfamily has b>=1.
    The supplied shifted representatives have odd
    initial positions and endpoint times in physical grid units; equality
    and open endpoint traces are therefore handled explicitly.
    """
    def __init__(self,master):
        self.master=master
        self.shift=master.n-1
        chosen=[(i,(j+k)//2,(k-j)//2+self.shift) for i,(j,k) in enumerate(master.nodes) if (k-j)//2>=1-master.n]
        self.indices=np.asarray([p[0] for p in chosen],dtype=np.int64)
        self.u=np.asarray([p[1] for p in chosen],dtype=np.int64)
        self.v=np.asarray([p[2] for p in chosen],dtype=np.int64)
        self.checked_columns=0

    def clock_units(self,cuts,numerators):
        cuts.sync_columns();master=self.master
        if len(numerators)!=len(master.columns) or any(w<0 for w in numerators):raise ValueError("loop weights")
        for column in master.columns[self.checked_columns:]:
            if sum(abs(int(v)) for v in column["coeff"].values())>int(column["mass"]):
                raise ValueError("clock pressure exceeds its total mass")
        self.checked_columns=len(master.columns)
        mass=sum(int(c["mass"])*int(w) for c,w in zip(master.columns,numerators))
        if mass<0 or 2*mass>np.iinfo(np.int64).max:
            raise ValueError("exact loop suffix-sum capacity exceeds int64")
        pressure=cuts.matrix.T@np.asarray(numerators,dtype=np.int64)
        grid=np.zeros((3*master.n+2,2*master.n+2),dtype=np.int64)
        grid[self.u,self.v]=pressure[self.indices]
        suffix=np.cumsum(np.cumsum(grid[::-1,::-1],axis=0,dtype=np.int64),axis=1,dtype=np.int64)[::-1,::-1]
        return mass,suffix

    def maximize(self,cuts,numerators,denominator):
        if sum(numerators)!=denominator or denominator<=0:raise ValueError("loop probability normalization")
        mass,suffix=self.clock_units(cuts,numerators)
        best=None;choice=None
        for a in range(self.master.n,0,-1):
            b=a-int(np.argmax(suffix[a,1-a+self.shift:a+1+self.shift][::-1]));value=int(suffix[a,b+self.shift])
            if best is None or value>best:best,choice=value,(a,b)
        a,b=choice
        return {"a":a,"b":b,"clock_plane_value":str(Q(mass+best,4*self.master.n*denominator)),
            "h":str(Q(2*self.master.n-2*b+1,2*self.master.n)),
            "epsilon":str(Q(2*self.master.n-2*a+1,2*self.master.n)),
            "rectangles_separated":self.master.n*(self.master.n+1),
            "scope":"Exact maximum over all one-turn endpoint-loop nodal clock fields for this calendar mixture; not an all-Princess physical response calculation."}


def rectangle_loop_payoff(law,a,b):
    """Actual first contacts of the selected shifted loop, in half-grid ticks."""
    n,W=int(law["n"]),int(law["weight_denominator"]);R=2*n
    if not 1<=a<=n or not 1-a<=b<=a:raise ValueError("invalid physical loop parameters")
    initial,turn,arrival=2*a-1,a-b,2*n-2*b+1
    numerator=0
    for p in law["paths"]:
        positions=[int(p["start_grid"])]
        if positions[0]%2:raise ValueError("shifted loop scorer requires the supported even-start lattice")
        for direction in p["moves"]:positions.append(positions[-1]+direction)
        pair=0
        for sign in (-1,1):
            old=positions[0]-sign*initial;contact=None
            for j in range(min(arrival,len(positions)-1)):
                radius=initial-(j+1) if j+1<=turn else R-arrival+j+1
                new=positions[j+1]-sign*radius
                if old==0:contact=2*j;break
                if new==0:contact=2*(j+1);break
                if old*new<0:
                    if abs(old)+abs(new)!=2:raise AssertionError("non-half-grid loop contact")
                    contact=2*j+1;break
                old=new
            if contact is None:
                endpoint=positions.index(sign*R)
                if endpoint<=arrival:raise AssertionError("missed an earlier loop contact")
                contact=2*endpoint
            pair+=contact
        numerator+=int(p["weight_numerator"])*pair
    return Q(numerator,8*n*W)


def loop_cut(master, diagnostic, target):
    """Return a feasible binary Qout field and a strict actual-response witness.

    When the exact fixed-law floor exceeds target, choose 0<epsilon<h<gap.
    The radial Princess starts at 1-epsilon, moves inward to time
    (h-epsilon)/2, then moves outward to its endpoint at time h.
    """
    if not diagnostic["endpoint_loop_supported"]:
        return None
    baseline = Q(diagnostic["endpoint_baseline"])
    mass = Q(diagnostic["endpoint_sweep_mass"])
    gap = Q(diagnostic["initial_gap"])
    floor = Q(diagnostic["endpoint_loop_supremum_lower"])
    if floor <= target:
        return None
    if baseline >= target or mass == 0:
        h = gap/2
    else:
        h = (gap+4*(target-baseline)/mass)/2
    epsilon = h/2
    witness = baseline+mass*h/4
    assert 0 < epsilon < h < gap and witness > target
    field=endpoint_loop_field(master,h,epsilon)
    return field, {
        "h": str(h), "epsilon": str(epsilon),
        "actual_physical_loop_payoff": str(witness),
        "fixed_law_loop_supremum_lower": str(floor),
        "threshold": str(target),
        "scope": "Actual payoff of one explicit reflected Princess loop against this proposed physical law. The field cut is feasible in Qout; this is not a game lower.",
    }
