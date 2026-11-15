#!/usr/bin/env python3
"""Exact algebra checks for CANDIDATE_DENSITIES.md; not an equilibrium test."""
from fractions import Fraction as Q


class Dual:
    """First-order rational automatic differentiation in a,u,c,y."""
    def __init__(self, value, gradient=(0, 0, 0, 0)):
        self.value = Q(value)
        self.gradient = tuple(map(Q, gradient))

    @staticmethod
    def cast(other):
        return other if isinstance(other, Dual) else Dual(other)

    def __add__(self, other):
        other = self.cast(other)
        return Dual(self.value + other.value,
                    tuple(x+y for x, y in zip(self.gradient, other.gradient)))

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, tuple(-x for x in self.gradient))

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        other = self.cast(other)
        return Dual(self.value * other.value,
                    tuple(x*other.value+self.value*y
                          for x, y in zip(self.gradient, other.gradient)))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.cast(other)
        return Dual(self.value/other.value,
                    tuple((x*other.value-self.value*y)/other.value**2
                          for x, y in zip(self.gradient, other.gradient)))

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        answer = Dual(1)
        for _ in range(n):
            answer *= self
        return answer


def poly(coefficients, x):
    return sum((c*x**i for i, c in enumerate(coefficients)), Dual(0))


def integral(coefficients, lo, hi, constant=1, linear=0):
    """Integral of (constant+linear*x) times a polynomial density."""
    result = Dual(0)
    for i, coefficient in enumerate(coefficients):
        result += coefficient*constant*(hi**(i+1)-lo**(i+1))/(i+1)
        result += coefficient*linear*(hi**(i+2)-lo**(i+2))/(i+2)
    return result


def evaluate(a0, u0, c0, y0, fs, gs, hs):
    parameters = []
    for i, z in enumerate((a0, u0, c0, y0)):
        parameters.append(Dual(z, tuple(int(i == j) for j in range(4))))
    a, u, c, y = parameters
    zero, one, w0 = Dual(0), Dual(1), Q(1, 7)
    k = -c if c0 < 0 else zero
    F = lambda z: integral(fs, zero, z)
    G = lambda z: integral(gs, zero, z)
    H = lambda z: integral(hs, zero, z)
    fb, gb, hb = lambda z: F(one)-F(z), lambda z: G(one)-G(z), lambda z: H(one)-H(z)
    f, g, h = lambda z: poly(fs, z), lambda z: poly(gs, z), lambda z: poly(hs, z)

    # Independently assemble the capture-time integrals in Section 3.
    j4 = w0*(5+c)
    j4 += integral(fs, zero, k, 8, -4)
    j4 += integral(fs, k, a, u+6, -3)
    j4 += integral(fs, a, one, 8+c, -3)
    j4 += 12*G(k)+integral(gs, k, a, u+4, -1)+(5+c)*gb(a)
    j4 += 4*H(a)+integral(hs, a, u, -a, 1)
    if c0 >= u0:
        j4 += 2*integral(hs, u, c, 0, 1)
    q = c if c0 > u0 else u
    j4 += integral(hs, q, one, c, 1)
    if c0 < 0:
        j4 += 8*H(one)
    else:
        r = c if c0 < u0 else u
        j4 += integral(hs, zero, r, u, 1)+8*hb(c)
        if c0 >= u0:
            j4 += 2*integral(hs, u, c, 0, 1)

    expected_a = (u-2-c)*f(a)+(u-1-a-c)*g(a)+4*h(a)-H(u)+H(a)
    if c0 < 0:
        expected_u = F(a)-F(-c)+G(a)-G(-c)-(a+c)*h(u)
        expected_c = w0+fb(a)+gb(a)+hb(u)-(2+c-u)*f(-c)-(8-c-u)*g(-c)
    else:
        r = c if c0 < u0 else u
        expected_u = F(a)+G(a)+H(r)-(a+r)*h(u)
        expected_c = w0+fb(a)+gb(a)+hb(q)-(8-c-q)*h(c)
    assert j4.gradient == (expected_a.value, expected_u.value,
                           expected_c.value, Q(0))

    lower = -y if y0 < 0 else zero
    correction = (y-c)*fb(a)-integral(fs, lower, k, 1, -1)
    k4 = j4+correction
    expected_ka = (u-2-y)*f(a)+(u-1-a-c)*g(a)+4*h(a)-H(u)+H(a)
    expected_kc = expected_c-fb(a)
    if c0 < 0:
        expected_kc += (1+c)*f(-c)
    expected_ky = fb(a)-(1+y)*f(-y) if y0 < 0 else fb(a)
    assert k4.gradient == (expected_ka.value, expected_u.value,
                           expected_kc.value, expected_ky.value)


def ode_check(a, f, w):
    h = w/(7-a)
    hp = w/(7-a)**2
    g = (w-(1-a)*f)/(7+a)
    A = (a+3)*(3*a+25)/((a+7)*(19-2*a-a*a))
    B = 2*(147-84*a-11*a*a)/((7-a)**2*(a+7)*(19-2*a-a*a))
    fp = A*f+B*w
    gp = (f-g-(1-a)*fp)/(7+a)
    assert (3-a)*fp+2*gp == 2*f+g-h+(4-2*a)*hp
    assert A == 1/(a+7)+4*(a+2)/(20-(a+1)**2)


def main():
    polynomial_sets = [
        ((1,), (2,), (3,)),
        ((1, 0, 1), (2, -1), (1, 2, 0, 1)),
        ((0, 1, 2), (1, 3, 1), (2, 0, 1)),
    ]
    checks = 0
    # Exercise every smooth branch, including c<a, a<c<u, c>u,
    # and negative c with either a negative or positive detour endpoint.
    # A representative exact check suffices; the identities are derived
    # symbolically in the note rather than inferred from this finite grid.
    parameter_sets = [
        (2, 6, 1, 3), (2, 6, 3, 5), (2, 6, 7, 8),
        (5, 7, 2, 8), (5, 7, 6, 8), (5, 7, -4, -2),
        (5, 7, -4, 2), (5, 7, -1, 8), (6, 7, -5, -1),
    ]
    for den in (8, 9, 11):
        for ai, ui, ci, yi in parameter_sets:
            for fs, gs, hs in polynomial_sets:
                evaluate(Q(ai, den), Q(ui, den), Q(ci, den),
                         Q(yi, den), fs, gs, hs)
                checks += 1
    for ai in range(1, 100):
        for f in (Q(0), Q(1, 7), Q(3, 5)):
            for w in (Q(1, 2), Q(7, 10)):
                ode_check(Q(ai, 100), f, w)

    # Exact counterexample to the negative-c two-choice suffix shortcut.
    a, c, y = Q(99, 100), Q(-99, 100), Q(-9, 10)
    tail = 11*(1-a)
    primitive = lambda x: x-x*x/2
    partial = (y-c)*tail-(primitive(-c)-primitive(-y))
    full = (1-c)*tail-primitive(-c)
    assert partial == Q(99, 20000) and full == Q(-5621, 20000)
    print(f"PASS: {checks} exact derivative cases for original and modified payoffs")
    print("PASS: 594 exact ODE and homogeneous-factor identities")
    print("PASS: negative-transition intermediate-detour counterexample")
    print("Scope: conditional algebra only; no equilibrium or new value bound")


if __name__ == '__main__':
    main()
