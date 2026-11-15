"""Unary additions to the attractive endpoint paired-control functional.

All values are FOUR times the unnormalized reflected-pair expected time.
Fixed-second I1 uses the joint one-sided U=1 convention described in
ENDPOINT_PAIRED_RESPONSE.md.  For an exact physical check, keep the first
post level equal to c and all pre levels strictly below one.

Late M2 atoms use closed early capture, including a turn at an endpoint.
The code also integrates arbitrary signed piecewise-polynomial M1
densities exactly.  No monotonicity of any density is required.
"""
from fractions import Fraction as Q

from endpoint_paired_controls import PairedEndpoint
from verify_general_inward_adjoint import integrate, integration_weights
from verify_terminal_inward_c import split_integral


class ExtendedPairedEndpoint(PairedEndpoint):
    def __init__(self, *args, fixed_inward=(), late_m2_atoms=(),
                 fixed_m2_atoms=(), early_m2_atoms=(), early_m3_atoms=(),
                 m1_polynomials=(), m2_polynomials=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fixed_inward = tuple(fixed_inward)
        self.late_m2_atoms = tuple(late_m2_atoms)
        self.fixed_m2_atoms = tuple(fixed_m2_atoms)
        self.early_m2_atoms = tuple(early_m2_atoms)
        self.early_m3_atoms = tuple(early_m3_atoms)
        # (left, right, coefficients), in increasing powers of signed x.
        self.m1_polynomials = tuple(m1_polynomials)
        # (turn, left, right, coefficients), with turn>=1 fixed.
        self.m2_polynomials = tuple(m2_polynomials)

    def tables(self):
        unaries, pairs, bounds, constant = super().tables()
        for density in self.fixed_inward:
            constant += self.add_fixed_inward(unaries, density)
        for x, s, mass in self.late_m2_atoms:
            constant += self.add_late_m2(unaries, x, s, mass)
        for x, mass in self.fixed_m2_atoms:
            constant += self.add_fixed_m2(unaries, x, mass)
        for x, s, mass in self.early_m2_atoms:
            constant += self.add_early_m2(unaries, pairs, x, s, mass)
        for x, s, mass in self.early_m3_atoms:
            constant += self.add_early_m3(unaries, pairs, x, s, mass)
        for left, right, coefficients in self.m1_polynomials:
            constant += self.add_m1_polynomial(unaries, left, right, coefficients)
        for s, left, right, coefficients in self.m2_polynomials:
            constant += self.add_m2_polynomial(unaries, pairs, s, left, right, coefficients)
        return unaries, pairs, bounds, constant

    def add_fixed_inward(self, unaries, d):
        """A polynomial density on 0<z<1, -z<v<z, with second U=1."""
        a, c = self.a, self.c
        below = integrate(d.row_mass, Q(0), a, d.degree+2)
        constant = ((1+c)*(d.mass-below)+8*below
                    +split_integral(lambda z: (z-1)*d.row_tail(z, c),
                                    a, Q(1), (c,), d.degree+2))
        # The reflected beta(1) is exact and is not replaced by two.
        constant += self.add_inverse(unaries, "beta", Q(1), d.mass)
        for index, (vl, vr) in enumerate(zip(self.pre_edges, self.pre_edges[1:])):
            for j, level in enumerate(self.pre_levels):
                def local(v):
                    return ((v+level-8)*d.column(a, v)
                            -integrate(lambda z: d.row_tail(z, v)
                                       +(1+c-z-v)*d.density(z, v),
                                       max(a, abs(v)), level, d.degree+1))
                unaries[index][j] += split_integral(
                    local, vl, vr, (-a, Q(0), a), d.degree+2)
        return constant

    def add_late_m2(self, unaries, x, s, mass):
        """M2(x,s), with 1<s<=2-x and |x|<=s, including closed faces."""
        assert -1 <= x <= 1 and 1 < s <= 2-x and abs(x) <= s
        a = self.a
        constant = Q(0)
        if x < a:
            constant += self.add_early_or_final(unaries, -x, s, mass)
        elif x > a:
            constant += self.add_inverse(unaries, "alpha", s, mass)
        if x < -a:
            constant += self.add_inverse(unaries, "alpha", -x, mass)
        elif x > -a:
            constant += self.add_inverse(unaries, "beta", s, mass)
        return constant

    def add_fixed_m2(self, unaries, x, mass):
        """The U=1 turn line, with last-cutoff c and closed start faces."""
        assert -1 <= x <= 1
        constant = Q(0)
        if x < self.a:
            constant += (self.add_inverse(unaries, "beta", -x, mass)
                         if -x <= self.c else 8*mass)
        elif x > self.a:
            constant += mass*(1+self.c)
        if x < -self.a:
            constant += self.add_inverse(unaries, "alpha", -x, mass)
        elif x > -self.a:
            constant += self.add_inverse(unaries, "beta", Q(1), mass)
        return constant

    def add_prefix_switch(self, unaries, pairs, v, s, after, mass):
        """Early beta(v) at P(v)<=s; otherwise beta(after), after>c.

        The missed indicator increases with P and every beta(after)
        unary increases with W=-Z.  Their product is attractive.
        """
        assert v > -self.a and s <= 1 and after > self.c
        if v > self.c:
            return self.add_inverse(unaries, "beta", after, mass)
        index = next(i for i, (vl, vr) in enumerate(
            zip(self.pre_edges, self.pre_edges[1:])) if vl < v <= vr)
        beta_rows = [[Q(0)]*len(row) for row in unaries]
        beta_constant = self.add_inverse(beta_rows, "beta", after, Q(1))
        missed = [p > s for p in self.pre_levels]
        for j, p in enumerate(self.pre_levels):
            unaries[index][j] += mass*(beta_constant if missed[j] else v+p)
        assert not any(any(row) for row in beta_rows[:self.npre])
        for post, row in enumerate(beta_rows[self.npre:], self.npre):
            if any(row):
                pairs.append((index, post, [
                    [mass*miss*value for value in row] for miss in missed]))
        return Q(0)

    def add_early_m2(self, unaries, pairs, x, s, mass):
        """Center-reaching M2: |x|<=s<1, with exact missed beta(s+2)."""
        assert abs(x) <= s < 1
        constant = Q(0)
        if x < self.a:
            constant += self.add_prefix_switch(unaries, pairs, -x, s, s+2, mass)
        elif x > self.a:
            constant += self.add_inverse(unaries, "alpha", s, mass)
        if x < -self.a:
            constant += self.add_inverse(unaries, "alpha", -x, mass)
        elif x > -self.a:
            constant += self.add_inverse(unaries, "beta", s, mass)
        return constant

    def add_early_m3(self, unaries, pairs, x, s, mass):
        """M3(x,s,1): |x|<=s<1; the second turn has V=1.

        Same-half negative first turns s<|x| are NOT put through this
        formula: after reflection they are the separate fixed I1 family.
        """
        assert abs(x) <= s < 1
        constant = Q(0)
        if x < self.a:
            constant += self.add_prefix_switch(unaries, pairs, -x, s, Q(1), mass)
        elif x > self.a:
            constant += self.add_inverse(unaries, "alpha", s, mass)
        if x < -self.a:
            constant += self.add_inverse(unaries, "alpha", -x, mass)
        elif x > -self.a:
            constant += (self.add_inverse(unaries, "beta", s, mass)
                         if s <= self.c else 8*mass)
        return constant

    def add_early_or_final(self, unaries, v, s, mass):
        """2*mass*[beta(v) if phi(v)<=s, otherwise s+3]."""
        assert v > -self.a and s <= v+2
        if v <= self.c:
            return self.add_inverse(unaries, "beta", v, mass)
        constant = mass*(v+1)
        for i, (ul, ur) in enumerate(zip(self.post_edges, self.post_edges[1:])):
            length = max(Q(0), min(s, ur)-ul)
            if length:
                for j, w in enumerate(self.w_levels):
                    unaries[self.npre+i][j] += mass*length*(-w < v)
        if s > self.L:
            for j, w in enumerate(self.w_levels):
                unaries[-1][j] += mass*(s-self.L)*(-w < v)
        # At s=v+2 the monster turns at +1, and every physical phi(v)
        # is <=s.  The closed endpoint jump therefore has zero weight.
        if s < v+2:
            if s < self.L:
                # The EARLY test uses the LAST V on U=s, hence the
                # right cell when s is a control-cell boundary.
                i = next(i for i, (ul, ur) in enumerate(
                    zip(self.post_edges, self.post_edges[1:])) if ul <= s < ur)
                row = unaries[self.npre+i]
            else:
                row = unaries[-1]
            for j, w in enumerate(self.w_levels):
                row[j] += mass*(s+6-v)*(-w < v)
        return constant

    def add_m1_polynomial(self, unaries, left, right, coefficients):
        """Integrate signed M1 atom features over an exact arrangement."""
        assert -1 <= left <= right <= 1
        cuts = {left, right, Q(0), self.a, -self.a}
        cuts.update(-v for v in self.pre_edges)
        cuts.update(-u for u in self.pre_levels)
        for w in self.w_levels:
            cuts.update((w, 2+w))
        cuts.update(2-u for u in self.post_edges)
        cuts = sorted(x for x in cuts if left <= x <= right)
        constant = Q(0)
        nodes, weights = integration_weights(len(coefficients)+1)
        for lo, hi in zip(cuts, cuts[1:]):
            for t, weight in zip(nodes, weights):
                x = lo+(hi-lo)*t
                density = sum((c*x**k for k, c in enumerate(coefficients)), Q(0))
                constant += self.add_m1(unaries, x, (hi-lo)*weight*density)
        return constant

    def add_m2_polynomial(self, unaries, pairs, s, left, right, coefficients):
        """A signed start polynomial on a center-reaching turn line."""
        assert 0 <= s <= 3 and max(-1, -s) <= left <= right <= min(1, s, 2-s)
        cuts = {left, right, Q(0), self.a, -self.a, -self.c}
        cuts.update(-v for v in self.pre_edges)
        cuts.update(-u for u in self.pre_levels)
        cuts.update(self.w_levels)
        cuts = sorted(x for x in cuts if left <= x <= right)
        constant = Q(0)
        nodes, weights = integration_weights(len(coefficients)+1)
        for lo, hi in zip(cuts, cuts[1:]):
            for t, weight in zip(nodes, weights):
                x = lo+(hi-lo)*t
                density = sum((c*x**k for k, c in enumerate(coefficients)), Q(0))
                mass = (hi-lo)*weight*density
                if s < 1:
                    constant += self.add_early_m2(unaries, pairs, x, s, mass)
                elif s == 1:
                    constant += self.add_fixed_m2(unaries, x, mass)
                else:
                    constant += self.add_late_m2(unaries, x, s, mass)
        return constant

    @property
    def total_mass(self):
        return (self.density.mass
                +sum((mass for _, mass in self.m1_atoms), Q(0))
                +sum((mass for _, mass in self.fixed_m2_atoms), Q(0))
                +sum((mass for _, _, mass in self.early_m2_atoms), Q(0))
                +sum((mass for _, _, mass in self.early_m3_atoms), Q(0))
                +sum((d.mass for d in self.fixed_inward), Q(0))
                +sum((mass for _, _, mass in self.late_m2_atoms), Q(0))
                +sum((sum((c*(right**(k+1)-left**(k+1))/Q(k+1)
                           for k, c in enumerate(coefficients)), Q(0))
                      for left, right, coefficients in self.m1_polynomials), Q(0))
                +sum((sum((c*(right**(k+1)-left**(k+1))/Q(k+1)
                           for k, c in enumerate(coefficients)), Q(0))
                      for s, left, right, coefficients in self.m2_polynomials), Q(0)))
