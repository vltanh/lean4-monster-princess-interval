"""Fraction regression of global radial pressure matching and clock backlog.

Finite tests check the algebra and finite max-flow/closure theorem, not
infinite-dimensional Strassen, full-game minimax, or a matching equilibrium.
"""
from fractions import Fraction as Q
from collections import deque
from itertools import product
from random import Random

Z, O, TWO = Q(0), Q(1), Q(2)


def below(z, w):
    t, u, _ = z
    s, v, _ = w
    return v >= u + abs(s-t)


def maxmatch(pos, neg):
    """Exact rational bipartite max flow on the closed time-radius cone."""
    a, b = len(pos), len(neg)
    n, src, sink = a+b+2, a+b, a+b+1
    c = [[Z for _ in range(n)] for _ in range(n)]
    for i, (_, _, w) in enumerate(pos):
        c[src][i] += w
    for j, (_, _, w) in enumerate(neg):
        c[a+j][sink] += w
    total = sum((w for _,_,w in pos), Z)
    for i, z in enumerate(pos):
        for j, w in enumerate(neg):
            if below(z, w):
                c[i][a+j] = total
    flow = Z
    while True:
        prev = {src: -1}
        queue = deque([src])
        while queue and sink not in prev:
            u = queue.popleft()
            for v in range(n):
                if v not in prev and c[u][v] > 0:
                    prev[v] = u
                    queue.append(v)
        if sink not in prev:
            break
        v, gain = sink, None
        while v != src:
            u = prev[v]
            gain = c[u][v] if gain is None else min(gain, c[u][v])
            v = u
        v = sink
        while v != src:
            u = prev[v]
            c[u][v] -= gain
            c[v][u] += gain
            v = u
        flow += gain
    return flow


def brute_closure(pos, neg):
    """Independent exact maximum-weight upper set on ALL supplied atoms."""
    points = pos + neg
    n = len(points)
    assert n <= 9
    best, chosen = Z, 0
    for mask in range(1 << n):
        if any((mask >> i) & 1 and not ((mask >> j) & 1)
               and below(points[i], points[j])
               for i in range(n) for j in range(n)):
            continue
        weight = sum((points[i][2] * (1 if i < len(pos) else -1)
                      for i in range(n) if (mask >> i) & 1), Z)
        if weight > best:
            best, chosen = weight, mask
    return best, chosen


def physical_phi(radius, x):
    return int(x > radius) + int(x > -radius)


def radial_witness(pos, neg, center, mask):
    """McShane threshold from excluded atoms, then outward germ shift."""
    points = pos + neg
    excluded = [point for i, point in enumerate(points)
                if not ((mask >> i) & 1)]
    def base(t):
        return max(Z, min(O, max((u - abs(t-s) for s,u,_ in excluded),
                                  default=Z)))
    gaps = [u-base(t) for i,(t,u,w) in enumerate(points)
            if (mask >> i) & 1]
    assert all(g > 0 for g in gaps)
    epsilon = min([Q(1,10)] + [g/2 for g in gaps])
    def r(t):
        return min(O, base(t)+epsilon)
    assert all((u>r(t)) == bool((mask >> i) & 1)
               for i,(t,u,w) in enumerate(points))
    alpha = ([(t,u,w) for t,u,w in pos] +
             [(t,-u,w) for t,u,w in neg] +
             [(t,Z,w) for t,w in center])
    M = sum((w for t,x,w in alpha), Z)
    payoff = sum((w*physical_phi(r(t),x) for t,x,w in alpha), Z)
    return M, payoff


def random_matching_tests():
    random = Random(14712)
    times = [Q(i,4) for i in range(9)]
    posradii = [Q(i,4) for i in range(1,5)]
    negradii = [Q(i,4) for i in range(1,4)]
    for _ in range(200):
        pos = [(random.choice(times), random.choice(posradii),
                Q(random.randint(1,6),8)) for _ in range(random.randint(1,4))]
        neg = [(random.choice(times), random.choice(negradii),
                Q(random.randint(1,6),8)) for _ in range(random.randint(1,4))]
        center = [(random.choice(times), Q(random.randint(1,4),8))]
        matched = maxmatch(pos,neg)
        deficiency, mask = brute_closure(pos,neg)
        assert deficiency == sum((w for t,u,w in pos),Z)-matched
        M, payoff = radial_witness(pos,neg,center,mask)
        assert payoff == M+deficiency
    return 200


def value(path, t):
    for (a,x),(b,y) in zip(path,path[1:]):
        if a<=t<=b:
            return x+(y-x)*(t-a)/(b-a)
    assert t==path[-1][0]
    return path[-1][1]


def eta_data(tau,kind):
    if kind == 'identity': return [], [(Z,tau,O)]
    if kind == 'frozen': return [(Z,tau)], []
    if kind == 'half': return [], [(Z,tau/2,TWO)]
    if kind == 'plateau': return [(tau/2,tau/2)], [(Z,tau/2,O)]
    if kind == 'lag': return [(Z,tau/2)], [(Z,tau/2,O)]
    raise AssertionError(kind)


def kappa(u,atoms,segs):
    return (sum((w for a,w in atoms if a<=u),Z)
            +sum((d*max(Z,min(u,b)-a) for a,b,d in segs),Z)-u)


def eta_integral(path,atoms,segs,A,B,C):
    answer = sum((w*(A*t+B*value(path,t)+C) for t,w in atoms),Z)
    for a,b,d in segs:
        knots = sorted({a,b}|{t for t,x in path if a<t<b})
        for u,v in zip(knots,knots[1:]):
            answer += d*(v-u)*(A*(u+v)/2+B*(value(path,u)+value(path,v))/2+C)
    return answer


def queue_integral(path,tau,atoms,segs,A,B,C):
    chronological = sum(((v-u)*(A*(u+v)/2+B*(x+y)/2+C)
                         for (u,x),(v,y) in zip(path,path[1:])),Z)
    knots = sorted({Z,tau}|{t for t,x in path}|
                   {t for t,w in atoms}|
                   {a for a,b,d in segs}|
                   {b for a,b,d in segs})
    correction = Z
    for u,v in zip(knots,knots[1:]):
        if u==v:continue
        midpoint=(u+v)/2
        slope=(value(path,v)-value(path,u))/(v-u)
        correction += (v-u)*kappa(midpoint,atoms,segs)*(A+B*slope)
    return chronological-correction


def clock_tests():
    paths = [
        [(Z,O),(O,Z),(Q(3),-O)],
        [(Z,Z),(O,O),(Q(3),-O)],
        [(Z,Q(1,2)),(Q(1,2),O),(Q(3,2),Z),(Q(5,2),-O)],
    ]
    n=0
    for path in paths:
        tau=path[-1][0]
        for kind in ['identity','frozen','half','plateau','lag']:
            atoms,segs=eta_data(tau,kind)
            assert sum((w for a,w in atoms),Z) + sum(((b-a)*d for a,b,d in segs),Z)==tau
            for u in [Z,tau/4,tau/2,3*tau/4,tau]:
                assert Z<=kappa(u,atoms,segs)<=tau-u
            for A,B,C in product([-2,-1,0,1,3],repeat=3):
                left=eta_integral(path,atoms,segs,Q(A),Q(B),Q(C))
                right=queue_integral(path,tau,atoms,segs,Q(A),Q(B),Q(C))
                assert left==right,(path,kind,A,B,C,left,right)
                if A>=abs(B):
                    chronological=sum(((v-u)*(Q(A)*(u+v)/2 + Q(B)*(x+y)/2+Q(C))
                                      for (u,x),(v,y) in zip(path,path[1:])),Z)
                    assert left<=chronological
                n+=1
    return n


def sweep_tests():
    def integrate(r,breaks):
        cuts=sorted(set(breaks))
        return sum(((v-u)*Q(1,2)*physical_phi(r((u+v)/2),O-(u+v)/2)
                    for u,v in zip(cuts,cuts[1:])),Z)
    r0=lambda t:abs(O-t)
    assert integrate(r0,[Z,O,TWO])==Q(1,2)
    for n in range(1,28):
        eps=Q(1,2**n)
        r=lambda t:abs(min(-O+eps+t,O))
        breaks=[Z,O-eps,O-eps/2,O,TWO-eps,TWO]
        assert integrate(r,breaks)==Q(3,2)-eps/4
    return 27


if __name__=='__main__':
    print('PASS: atomic matching/upper-set/radius tests =',random_matching_tests())
    print('PASS: physical causal-clock/backlog Fraction identities =',clock_tests())
    print('PASS: two-sweep singular contact-germ families =',sweep_tests())
