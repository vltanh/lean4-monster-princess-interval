"""Exact exclusion of a three-parameter wait/inward/outward response class.

All calculations use integers and fractions.Fraction. The global maximum
is certified by the complete hyperplane arrangement described in the proof.
No numerical optimization, tolerances, or external packages are used.
"""

from fractions import Fraction as F
from functools import reduce
from itertools import combinations, product
from math import gcd


# Pair weights are these integers divided by 100; reflection is equiprobable.
ROWS = ((1,F(-1),39), (1,F(-1,2),5), (1,F(5,8),16),
        (2,F(-1,2),9), (1,F(1,2),12), (1,F(1,4),19))
NORMALS = ((1,0,0), (0,1,0), (-1,1,0), (0,0,1),
           (-1,0,1), (-2,0,1), (0,-2,1))


def dot(a, b):
    return sum(x*y for x,y in zip(a,b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def determinant(a, b, c):
    return dot(a, cross(b,c))


def generic_directions():
    """One exact interior vector in every full-dimensional normal cone.

    Coordinate sign constraints make each cone pointed. Every extreme ray
    is the intersection of two of its bounding planes. Summing all its
    feasible primitive rays gives a strict interior point exactly when its
    strict sign pattern is feasible. See the accompanying completeness proof.
    """
    rays = set()
    for a,b in combinations(NORMALS,2):
        r = cross(a,b)
        divisor = reduce(gcd, (abs(x) for x in r))
        if divisor:
            r = tuple(x//divisor for x in r)
            rays.add(r)
            rays.add(tuple(-x for x in r))
    directions = []
    for signs in product((-1,1),repeat=len(NORMALS)):
        signed = [tuple(s*x for x in n) for s,n in zip(signs,NORMALS)]
        feasible = [r for r in rays if all(dot(n,r)>=0 for n in signed)]
        d = tuple(sum(r[i] for r in feasible) for i in range(3))
        if all(dot(n,d)>0 for n in signed):
            directions.append(d)
    return directions


def arrangement_vertices():
    xs = [x for _,x,_ in ROWS]
    a_thresholds = {F(1)} | {-x for x in xs} | {2-x for x in xs}
    b_thresholds = {F(1),F(3)} | {-x for x in xs} | {2-x for x in xs}
    groups = [
        {F(0),F(1)} | set(xs) | {-x for x in xs}
        | {(1+x)/2 for x in xs} | a_thresholds
        | {-c for c in b_thresholds},
        {F(0)},
        {F(0)},
        a_thresholds | {F(5)},
        {F(0)},
        b_thresholds,
        b_thresholds | {c-2 for c in a_thresholds},
    ]
    vertices = set()
    for ids in combinations(range(len(NORMALS)),3):
        na,nb,nc = [NORMALS[i] for i in ids]
        det = determinant(na,nb,nc)
        if det == 0:
            continue
        ca,cb,cc = cross(nb,nc),cross(nc,na),cross(na,nb)
        for rhs in product(*(groups[i] for i in ids)):
            v = tuple((rhs[0]*ca[j]+rhs[1]*cb[j]+rhs[2]*cc[j])/det
                      for j in range(3))
            a,b,u = v
            if 0<=b<=a<=1 and a<=u<=5:
                vertices.add(v)
    return sorted(vertices)


def greater_equal(pair, constant):
    return pair[0]>constant or pair[0]==constant and pair[1]>=0


def greater(pair, constant):
    return pair[0]>constant or pair[0]==constant and pair[1]>0


def admissible_direction(vertex, direction):
    a,b,u = vertex
    da,db,du = direction
    # Strictly interior parameters vertex + epsilon*direction, epsilon>0.
    return all(greater(z,0) for z in (
        (a,da), (1-a,-da), (b,db), (a-b,da-db),
        (u-a,du-da), (5-u,-du)))


def objective_limit(vertex, direction):
    """Constant term of the exact affine objective as epsilon tends to zero.

    Each pair denotes c0+c1*epsilon. Comparisons use lexicographic order.
    Generic directions avoid all branch hyperplanes, including u=1.
    """
    a,b,u = vertex
    da,db,du = map(F,direction)

    def A(c):
        if greater_equal((a,da),c):
            return F(0),F(0)
        if greater_equal((u,du),c):
            return c-a,-da
        if greater_equal((u+2-2*b,du-2*db),c):
            return (c+u-2*b)/2,(du-2*db)/2
        return c-1,F(0)

    def B(c):
        if greater_equal((-a,-da),c):
            return F(0),F(0)
        if greater_equal((u-2*a,du-2*da),c):
            return c+a,da
        if greater_equal((u-2*b,du-2*db),c):
            return (c+u)/2,du/2
        return c+1,F(0)

    s,ds = A(F(1))
    cutoff = 1-2*s,-2*ds
    total = F(0)
    for family,x,weight in ROWS:
        if family == 1:
            unreflected = B(-x)[0] if greater((a,da),x) else A(2-x)[0]
            reflected = A(-x)[0] if greater((-a,-da),x) else B(2-x)[0]
        else:
            if greater(cutoff,x):
                unreflected = B(F(3))[0]
            elif greater((a,da),x):
                unreflected = B(-x)[0]
            else:
                unreflected = s
            reflected = A(-x)[0] if greater((-a,-da),x) else B(F(1))[0]
        total += weight*(unreflected+reflected)
    return total/(2*sum(weight for _,_,weight in ROWS))


def at(path, t):
    for (a,x),(b,y) in zip(path,path[1:]):
        if a<=t<=b:
            return x+(y-x)*(t-a)/(b-a)
    assert t>=path[-1][0]
    return path[-1][1]


def direct_capture(monster, princess):
    previous = None
    for t in sorted({t for t,_ in monster+princess}):
        difference = at(monster,t)-at(princess,t)
        if difference == 0:
            return t
        if previous is not None:
            old_t,old_difference = previous
            if difference*old_difference<0:
                return old_t+(t-old_t)*abs(old_difference)/(
                    abs(old_difference)+abs(difference))
        previous = t,difference
    raise AssertionError("The monster must capture by time four")


def direct_payoff(princess):
    assert princess[0][0] == 0 and princess[-1][0] == 4
    assert all(0<=x<=1 for _,x in princess)
    assert all(b>a and abs(y-x)<=b-a for (a,x),(b,y)
               in zip(princess,princess[1:]))
    total = F(0)
    captures = []
    for family,x,weight in ROWS:
        if family == 1:
            monster = [(F(0),x),(1-x,F(1)),(3-x,F(-1))]
        else:
            monster = [(F(0),x),((1-x)/2,(1+x)/2),
                       (F(2),F(-1)),(F(4),F(1))]
        pair = (direct_capture(monster,princess),
                direct_capture([(t,-y) for t,y in monster],princess))
        captures.append(pair)
        total += weight*sum(pair)
    return total/(2*sum(weight for _,_,weight in ROWS)),captures


def main():
    assert sum(weight for _,_,weight in ROWS) == 100
    vertices = arrangement_vertices()
    directions = generic_directions()
    assert len(vertices) == 369
    assert len(directions) == 32
    best = F(-1)
    checked = 0
    for vertex in vertices:
        for direction in directions:
            if not admissible_direction(vertex,direction):
                continue
            checked += 1
            best = max(best,objective_limit(vertex,direction))
    assert checked == 7392
    assert best == F(2641,1600)
    v = F(5,8),F(1,4),F(1)
    d = -1,-2,-5
    assert admissible_direction(v,d) and objective_limit(v,d)==best

    delta = F(1,1000)
    witness = [(F(0),F(1,4)-delta/3),
               (F(1,8),F(3,8)-delta/3),
               (F(1,2)-delta,2*delta/3),
               (F(15,16)-delta,F(7,16)+2*delta/3),
               (F(19,16)-delta,F(3,16)+2*delta/3),
               (2-2*delta,1-delta/3),
               (F(4),1-delta/3)]
    actual,captures = direct_payoff(witness)
    assert actual == F(100559,60000)
    assert actual-best == F(3043,120000)>0
    print(f"PASS: {len(vertices)} vertices, {len(directions)} cone directions,")
    print(f"      {checked} admissible exact cases, supremum {best}.")
    print(f"PASS: direct rational witness payoff {actual}.")
    print(f"PASS: wait-in-out class loses at least {actual-best}.")
    for (family,x,_),pair in zip(ROWS,captures):
        print(f"M{family}({x}): capture times {pair[0]}, {pair[1]}")


if __name__ == "__main__":
    main()
