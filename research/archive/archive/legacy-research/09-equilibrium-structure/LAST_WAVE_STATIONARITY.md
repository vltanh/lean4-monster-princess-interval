# Joint start and turn equations in a last-wave region

## 1. Region and notation

Consider a continuous ordered five-leg law with parameters
`a(q), A1(q), C1(q), A2(q), C2(q)` and equal reflection probabilities.
Assume the no-early-absorption peak inequalities, C2<=1, and first-wave
separation `inf A1>=sup C1`. There is no stationary endpoint component
in the formulas below; one can add its separately known payoff afterward.

Write

    A(z)=Pr(a<=z),  B1(z)=Pr(A1<=z),
    B2(s)=Pr(A2<=s),  D1(z)=Pr(C1>=z), D2(z)=Pr(C2>=z).

The monster starts at -z, moves right to

    ((s+z)/2,(s-z)/2),

then visits -1 at s+1 and +1 at s+3. Work in an open region satisfying

    0<z<min(1,inf A2),    1<s<2+z,
    d=D1(z) < Q=B2(s) < D2(z).                          (1)

The inequalities ensure that the early positive capture front is exactly
the last incoming CDF Q. Earlier positive captures still contribute to
the payoff and its start derivative; they cannot be discarded merely
because the final front is B2(s).

Set

    r=A(z),    b=B1(z).

One has b<=r. Assume the displayed CDFs are differentiable on the region;
for second derivatives assume the additional smoothness explicitly used.
CDFs that are constant outside their parameter range have derivative zero.
At a knot, atom, or changed capture ordering, the corresponding one-sided
comparison is needed instead of these smooth equations.

## 2. Exact payoff and the two moving prefix fronts

Let C(s,z) be the expected capture time against this symmetric law. Then

    4C(s,z)
      = 2(s+1)(1-r)
        + integral_0^b (z+C1(q)) dq
        + integral_b^r (z-a(q)) dq
        + integral_0^d (A1(q)+z) dq
        + integral_d^Q (A2(q)+z) dq
        + 2(s+3)(1-Q).                                (2)

### Negative princesses

Ranks with a<z are captured on the monster's first rightward leg at
the first inverse of U=z. For q<b that inverse lies on the first return
outward and is `(z+C1(q))/2`. For b<q<r it lies on the initial outward
leg and is `(z-a(q))/2`. The first-wave separation and z<inf A2 ensure
that neither a center wait nor the second wave changes these inverses.
Ranks with a>z are captured at the negative endpoint at time s+1.

### Positive princesses

For q<d, C1(q)>z, so the first incoming leg crosses V=z at
`(A1(q)+z)/2`. For d<q<Q, the first wave does not reach V=z and the
second incoming leg does, at `(A2(q)+z)/2`. The condition z<inf A2
places this encounter before any possible center wait of that wave.
The remaining ranks q>Q miss the first turn and are captured at s+3.
These classes prove (2), with null boundary ranks omitted.

Notice the two distinct moving fronts:

* b=B1(z) changes which negative ranks are caught before or after the
  first incoming characteristic;
* d=D1(z) changes which positive ranks are caught by the first or second
  incoming wave.

Both contribute to the start derivative.

## 3. Exact partial derivatives

Define the nonnegative prefix correction

    E(z)
      =[a(b)+C1(b)] B1'(z)
       +[A2(d)-A1(d)] (-D1'(z)).                       (3)

It is nonnegative because C1>=-a, A2>=A1, B1'>=0, and D1'<=0.
Direct differentiation of (2) gives

    4 C_s
      =2(2-A(z)-B2(s))-(6+s-z)B2'(s),                 (4)

    4 C_z
      =-2(s+1)A'(z)+A(z)+B2(s)+E(z).                 (5)

For example, differentiating the two negative-rank integrals gives

    A(z)+[a(B1(z))+C1(B1(z))]B1'(z).

The moving boundary at a=z contributes zero from its initial-outward
formula. Differentiating the two positive-rank integrals gives

    B2(s)+[A2(D1(z))-A1(D1(z))](-D1'(z)).

Dropping this second boundary term would give an incorrect C_z even
though the final radial front is just B2(s).

With global first-wave separation, the two summands in E generally occur
in different z regions: B1' can be nonzero only in the A1 range, while
-D1' can be nonzero only in the disjoint C1 range. In the gap
`sup C1<z<inf A1`, both vanish and E=0.

## 4. Necessary equations for an interior minimizing support curve

Suppose, as an additional support hypothesis, a differentiable curve
`s=s(z)` consists of interior monster minima against the same law. Then
both partial derivatives must vanish:

    (6+s-z)B2'(s)=2(2-A(z)-B2(s)),                     (6)

    2(s+1)A'(z)=A(z)+B2(s)+E(z).                       (7)

These are necessary equilibrium support equations, not assertions that
such a curve exists or that it controls all monsters.

Write `b2=B2'` and `W=6+s-z`. Differentiating (7) along the curve gives
the coupled front equation

    [b2(s)-2A'(z)]s'(z)
      =2(s+1)A''(z)-A'(z)-E'(z).                      (8)

Differentiating (6) gives the second compatibility equation

    [3b2(s)+W b2'(s)]s'(z)=b2(s)-2A'(z).               (9)

The correction E contains the earlier last-wave characteristic A2(d),
where d=D1(z)<B2(s). Thus (8) couples the current last-wave front to a
strictly earlier quantile of that same incoming wave; it is not an ODE
for B2 alone unless the first-wave correction is independently known.

The Hessian formulas are

    4 C_ss =-3b2-W b2',
    4 C_sz =b2-2A',
    4 C_zz =-2(s+1)A''+A'+E'.                         (10)

An isolated interior minimum requires this Hessian to be positive
semidefinite. A smooth continuum of indifferent minima additionally has
the support tangent in its nullspace, which is expressed by (8)-(9).
Where the denominators are nonzero, these imply

    [b2-2A']^2
      =[3b2+W b2'] [2(s+1)A''-A'-E'].                 (11)

This compatibility is a consequence of the support hypothesis, not a
global sufficiency condition.

## 5. Two structural consequences

### No interior start in a density gap

If A'(z)=0 while `A(z)+B2(s)+E(z)>0`, equation (5) gives C_z>0.
Moving the starting point toward the center (decreasing z) improves the
monster payoff as long as the open regime persists. Such a point cannot
be an interior optimum. The finite-wave counterexample in
`FINITE_LAST_WAVE_COUNTEREXAMPLE.md` deliberately concerns fixed-start
turn optimality; this test explains why it does not by itself give an
unrestricted equilibrium.

### A high-rank minimizing turn curve must increase

At a stationary point with `T=A(z)+B2(s)>=1`, equations (6)-(7) give

    b2-2A' = 2(2-T)/W-(T+E)/(s+1)<0.                  (12)

Indeed E>=0, and `s+z<4` follows from s<2+z and z<1. Hence
`W>2(s+1)`, so `2/W<1/(s+1)`. The right side of (12) is strictly
negative already at T=1,E=0 and decreases as T or E increases.

At a twice differentiable local minimum, the nonzero mixed derivative
then forces C_ss>0: a positive-semidefinite Hessian with C_ss=0 would
have zero mixed derivative. On a minimizing support curve,

    s'(z)=-C_sz/C_ss>0.                                (13)

Thus, in this regime, larger distance of the start from the center must
correspond to a later turning characteristic. The fixed-time-one curve
Q, given by s=2-z, cannot be a smooth minimizing support segment there.
This does not exclude an isolated Q atom or a Q segment in the low-rank
regime T<1.

The equations permit finite last waves with decreasing incoming density.
They do not prove that infinitely many waves are necessary, nor do they
construct a finite-wave equilibrium. They identify the additional coupled
conditions that a candidate must satisfy before that question can be
decided.
