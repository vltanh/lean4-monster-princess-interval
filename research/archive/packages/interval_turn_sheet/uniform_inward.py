#!/usr/bin/env python3
"""Exact upper features for an added uniform initial-inward monster law.

The density is i(a,v)=h(a) on -a<v<a.  Scores are FOUR times the
unnormalized expected capture time.  The graph feature is an upper
relaxation retaining first-touch jumps safely; see UNIFORM_INWARD_UPPER.md.
"""
from bisect import bisect_right


class UniformInward:
    def __init__(self, knots, heights):
        self.knots, self.heights = tuple(knots), tuple(heights)
        if len(knots) != len(heights)+1 or knots[0] != 0 or knots[-1] != 1:
            raise ValueError("Density knots must partition [0,1]")
        if not all(a < b for a, b in zip(knots, knots[1:])) or min(heights) < 0:
            raise ValueError("Expected increasing knots and nonnegative density")
        self.zero = knots[0]*0
        self.primitive = [self.zero]
        for a, b, h in zip(knots, knots[1:], heights):
            self.primitive.append(self.primitive[-1]+(b-a)*h)
        self.mass = sum(((b*b-a*a)*h for a,b,h in zip(knots,knots[1:],heights)), self.zero)

    def H(self, x):
        x = min(self.knots[-1], max(self.zero, x))
        i = min(len(self.heights)-1, max(0, bisect_right(self.knots, x)-1))
        return self.primitive[i]+(x-self.knots[i])*self.heights[i]

    def density(self, x):
        i = min(len(self.heights)-1, max(0, bisect_right(self.knots, x)-1))
        return self.heights[i]

    def mass_below(self, b):
        return sum(((min(b,r)**2-l*l)*h for l,r,h in
                    zip(self.knots,self.knots[1:],self.heights) if l < b), self.zero)

    def j(self, b, v):
        return max(self.zero, self.H(b)-self.H(abs(v)))

    def constant_four_score(self, b, c):
        below = self.mass_below(b)
        result = 4*self.mass+(1+c)*(self.mass-below)+8*below
        def primitive(a):
            return a*a*a/3-(1+c)*a*a/2+c*a
        for left, right, height in zip(self.knots,self.knots[1:],self.heights):
            lo = max(left, b, c)
            if lo < right:
                result += height*(primitive(right)-primitive(lo))
        return result

    def graph_integrand(self, b, c, v, u):
        return (self.j(b,v)*(v+u-8)
                -(1+c-2*v)*(self.H(u)-self.H(max(b,v))))

    def graph_gradient(self, b, c, v, u):
        return self.j(b,v)-(1+c-2*v)*self.density(u)

    def piece_four_score(self, b, c, vl, vr, ul, ur):
        if vl == vr:
            return self.zero
        slope = (ur-ul)/(vr-vl)
        intercept = ul-slope*vl
        cuts = {vl, vr}
        for point in [self.zero, b, -b, *self.knots, *[-x for x in self.knots]]:
            if vl < point < vr:
                cuts.add(point)
        if slope != 0:
            for level in self.knots:
                point = (level-intercept)/slope
                if vl < point < vr:
                    cuts.add(point)
        cuts = sorted(cuts)
        def value(v):
            return self.graph_integrand(b,c,v,slope*v+intercept)
        return sum(((r-l)*(value(l)+4*value((l+r)/2)+value(r))/6
                    for l,r in zip(cuts,cuts[1:])), self.zero)

    def graph_four_score(self, b, c, graph):
        """Graph vertices are (V,U); vertical jumps in U are allowed."""
        if graph[0][0] != -b or graph[-1][0] != c:
            raise ValueError("The inverse graph must run from V=-b to V=c")
        for (vl,ul),(vr,ur) in zip(graph,graph[1:]):
            if not (vl <= vr and ul <= ur and max(b,vl) <= ul <= 1
                    and max(b,vr) <= ur <= 1):
                raise ValueError("Illegal inverse graph")
        return self.constant_four_score(b,c)+sum((
            self.piece_four_score(b,c,vl,vr,ul,ur)
            for (vl,ul),(vr,ur) in zip(graph,graph[1:])), self.zero)


def graph_from_path(path):
    """Last-U=1 convention; keeps incoming U=1 plateaus in the graph."""
    b = path[0][1]
    graph = [(path[0][0]-b, path[0][0]+b)]
    c = None
    for (tl,pl),(tr,pr) in zip(path,path[1:]):
        ul, ur = tl+pl, tr+pr
        vl, vr = tl-pl, tr-pr
        if ul > 1:
            break
        if ur <= 1:
            point = (vr,ur)
            if point != graph[-1]:
                graph.append(point)
            if ur == 1:
                c = vr
            continue
        if ul == 1:
            c = vl
        else:
            fraction = (1-ul)/(ur-ul)
            c = vl+fraction*(vr-vl)
            graph.append((c,ul*0+1))
        break
    if c is None:
        raise ValueError("Princess path does not include the last U=1 event")
    return b, c, graph
