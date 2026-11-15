"""Exact finite-control features for endpoint I plus arbitrary M1 atoms.

The attractive pair table is the exact integral of the continuum
coupling.  A finite cut optimizes these controls globally; it does not
by itself bound the error from restricting the continuum controls.
"""
from fractions import Fraction as Q
from functools import lru_cache

from verify_general_inward_adjoint import integrate
from verify_terminal_inward_c import split_integral


class PairedEndpoint:
    def __init__(self, density, a, c, pre_edges, post_edges,
                 pre_levels, post_levels, m1_atoms=()):
        self.density, self.a, self.c = density, a, c
        self.L = 2+c
        self.pre_edges, self.post_edges = tuple(pre_edges), tuple(post_edges)
        self.pre_levels = tuple(pre_levels)
        self.w_levels = tuple(sorted(-v for v in post_levels))
        self.m1_atoms = tuple(m1_atoms)
        assert self.pre_edges[0] == -a and self.pre_edges[-1] == c
        assert self.post_edges[0] == 1 and self.post_edges[-1] == self.L
        assert 2-a in self.post_edges
        assert all(2+v in self.post_edges for v in self.pre_edges)
        self.npre, self.npost = len(pre_edges)-1, len(post_edges)-1

    @lru_cache(None)
    def beta_tail(self, value):
        density, a = self.density, self.a
        low = (split_integral(lambda v: density.column(a, v),
                              max(value, -a), a, (Q(0),), density.degree+1)
               if value < a else Q(0))
        reflected = (split_integral(lambda b: density.column(Q(1), b-2),
                                    max(value, Q(1)), Q(3), (Q(2),), density.degree+1)
                     if value < 3 else Q(0))
        return low+reflected

    @lru_cache(None)
    def terminal_beta(self, value):
        return ((2+value-self.L)*self.beta_tail(value)
                +split_integral(self.beta_tail, value, Q(3),
                                (-self.a, Q(0), self.a, Q(1), Q(2)),
                                self.density.degree+2))

    def prefix_unary(self, value, level):
        d, a = self.density, self.a
        return (d.column(a, value)*level
                -integrate(lambda z: d.row_tail(z, value)
                           +(2-z)*d.density(z, value),
                           max(a, abs(value)), level, d.degree+1))

    def endpoint_constant(self):
        """The absolute four-score constant, independent of both controls.

        Keeping this term removes the need for a physical anchor path when
        the feature is used as a column in a density optimization.
        """
        d, a, c = self.density, self.a, self.c
        alpha = (split_integral(lambda z: (z+c)*d.row_tail(z, c),
                                a, Q(1), (c,), d.degree+2)
                 +split_integral(
                     lambda v: (2+v)*(d.column(Q(1), v)-d.column(a, v)),
                     Q(-1), c, (-a, Q(0), a), d.degree+2))
        beta = (split_integral(lambda v: v*d.column(a, v),
                               -a, a, (Q(0),), d.degree+2)
                +split_integral(lambda v: d.column(a, v),
                                max(c, -a), a, (Q(0),), d.degree+1)
                +split_integral(lambda v: (v+1)*d.column(Q(1), v-2),
                                Q(1), Q(3), (Q(2),), d.degree+2))
        return alpha+beta

    def suffix_column(self, u):
        return self.density.column(Q(1), u-2)

    def tables(self):
        d, a, c = self.density, self.a, self.c
        unaries, pairs, bounds = [], [], []
        for vl, vr in zip(self.pre_edges, self.pre_edges[1:]):
            unaries.append([split_integral(
                lambda v: self.prefix_unary(v, level), vl, vr,
                (Q(0), a), d.degree+2) for level in self.pre_levels])
            legal = [j for j, level in enumerate(self.pre_levels)
                     if max(a, vr) <= level < 1]
            bounds.append((min(legal), max(legal)))
        for ul, ur in zip(self.post_edges, self.post_edges[1:]):
            source = (integrate(self.suffix_column, ul, ur, d.degree+1)
                      if ur <= 2-a else Q(0))
            unaries.append([(ur-ul)*self.beta_tail(-w)-w*source
                            for w in self.w_levels])
            legal = [j for j, w in enumerate(self.w_levels) if c <= -w <= ul]
            bounds.append((min(legal), max(legal)))
        for j, w in enumerate(self.w_levels):
            unaries[-1][j] += self.terminal_beta(-w)
        for i, (vl, vr) in enumerate(zip(self.pre_edges, self.pre_edges[1:])):
            post = self.post_edges.index(2+vl)
            assert self.post_edges[post+1] == 2+vr
            table = []
            for level in self.pre_levels:
                column = integrate(lambda v: integrate(
                    lambda z: d.density(z, v), level, Q(1), d.degree),
                    vl, vr, d.degree)
                table.append([-w*column for w in self.w_levels])
            pairs.append((i, self.npre+post, table))

        constant = self.endpoint_constant()
        for parameter, mass in self.m1_atoms:
            constant += self.add_m1(unaries, parameter, mass)
        return unaries, pairs, bounds, constant

    def add_m1(self, unaries, parameter, mass):
        """One signed M1 pair, retaining both initial equalities."""
        a = self.a
        constant = Q(0)
        if parameter < a:
            constant += self.add_inverse(unaries, "beta", -parameter, mass)
        elif parameter > a:
            constant += self.add_inverse(unaries, "alpha", 2-parameter, mass)
        if parameter < -a:
            constant += self.add_inverse(unaries, "alpha", -parameter, mass)
        elif parameter > -a:
            constant += self.add_inverse(unaries, "beta", 2-parameter, mass)
        return constant

    def add_inverse(self, unaries, kind, threshold, mass):
        """Add exactly 2*mass times a first inverse, including atoms."""
        if kind == "alpha":
            if threshold <= self.a:
                return Q(0)
            if threshold < 1:
                for i, (vl, vr) in enumerate(zip(self.pre_edges, self.pre_edges[1:])):
                    for j, p in enumerate(self.pre_levels):
                        unaries[i][j] += mass*(vr-vl)*(p < threshold)
                return mass*(threshold-self.a)
            if threshold == 1:
                return mass*(1+self.c)
            index = next(i for i, (ul, ur) in enumerate(
                zip(self.post_edges, self.post_edges[1:])) if ul < threshold <= ur)
            for j, w in enumerate(self.w_levels):
                unaries[self.npre+index][j] -= mass*w
            return mass*threshold
        assert kind == "beta"
        if threshold <= -self.a:
            return Q(0)
        if threshold <= self.c:
            index = next(i for i, (vl, vr) in enumerate(
                zip(self.pre_edges, self.pre_edges[1:])) if vl < threshold <= vr)
            for j, p in enumerate(self.pre_levels):
                unaries[index][j] += mass*p
            return mass*threshold
        for i, (ul, ur) in enumerate(zip(self.post_edges, self.post_edges[1:])):
            for j, w in enumerate(self.w_levels):
                unaries[self.npre+i][j] += mass*(ur-ul)*(-w < threshold)
        for j, w in enumerate(self.w_levels):
            unaries[-1][j] += mass*(threshold+2-self.L)*(-w < threshold)
        return mass*(threshold+1)

    def path(self, labels):
        graph = [(self.a, -self.a)]
        for i, (vl, vr) in enumerate(zip(self.pre_edges, self.pre_edges[1:])):
            u = self.pre_levels[labels[i]]
            graph.extend([(u, vl), (u, vr)])
        graph.append((Q(1), self.c))
        for i, (ul, ur) in enumerate(zip(self.post_edges, self.post_edges[1:])):
            v = -self.w_levels[labels[self.npre+i]]
            graph.extend([(ul, v), (ur, v)])
        last_v = graph[-1][1]
        graph.append((2+last_v, last_v))
        vertices = [((u+v)/2, (u-v)/2) for u, v in graph]
        vertices.append((Q(10), Q(1)))
        clean = []
        for point in vertices:
            if not clean or point != clean[-1]:
                clean.append(point)
        for (t0, x0), (t1, x1) in zip(clean, clean[1:]):
            assert t1 > t0 and abs(x1-x0) <= t1-t0
            assert 0 <= x0 <= 1 and 0 <= x1 <= 1
        return clean

    def reward(self, labels, tables=None):
        unaries, pairs, bounds, constant = self.tables() if tables is None else tables
        return (constant+sum((row[labels[i]] for i, row in enumerate(unaries)), Q(0))
                +sum((table[labels[i]][labels[j]] for i, j, table in pairs), Q(0)))
