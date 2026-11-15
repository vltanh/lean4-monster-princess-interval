# A finite last wave can resist turn variation

## 1. What the example decides

A finite final incoming wave need not be vulnerable to a change of the
monster's turning characteristic. This note constructs a strictly ordered
five-leg princess law for which a whole interval of last-wave turns is
globally minimizing at one fixed start. A second version has a unique
strict interior minimum instead.

The comparison includes the endpoint-turn boundary, where an endpoint
capture atom can otherwise invalidate a generic interior formula. It is
global over the last-wave turn range `1<=s<=2+z`, with the fixed start
`-z=-1/2`.

This does **not** construct an unrestricted equilibrium. Other starting
points and earlier-turn families remain available. Its consequence is
precise: no theorem can exclude all finite-wave candidates merely by
claiming that their last incoming wave always admits an improving change
of the turn characteristic. Joint start/turn stationarity and the other
response families still have to be checked.

## 2. Exact princess parameters

Let q be uniform on [0,1], and choose the sign of the princess path fairly.
Use the usual ordered five-leg construction with

    a(q)=11/20+q/4,
    A1(q)=17/20+q/10,
    C1(q)=1/10-3q/20,
    C2(q)=9/10-3q/10.

Define A2 as the quantile inverse of the following continuous strictly
increasing CDF B2 on `[11/10,19/10]`. Put

    s0=27/20,  K0=13467/250,  d=11033/12250,
    gamma in {0,1},  K_gamma=K0-9 gamma/400.

Then

    B2(s)=0                                      for s<=11/10,
          8(s-11/10)                             for 11/10<=s<=6/5,
          2-[K_gamma+gamma(s-s0)^2]/(s+11/2)^2   for 6/5<=s<=3/2,
          d+(1217/4900)(s-3/2)                   for 3/2<=s<=19/10,
          1                                      for s>=19/10.       (1)

The formulas agree at every join: B2 is 4/5 at 6/5 and d at 3/2.
The last affine piece reaches one exactly at 19/10.

On the middle piece, writing `H=137/20`,

    B2'(s)
      = 2[K_gamma-gamma H(s-s0)]/(s+11/2)^3 > 0.        (2)

For gamma=1, the numerator bracket is at least 26409/500; for gamma=0
it is K0. Thus A2 is continuous and strictly increasing. It is affine
on the first and last quantile pieces and algebraic on the middle one.

All admissibility and order conditions hold:

* a and A1 increase strictly, C1 and C2 decrease strictly;
* `a<=A1<A2` and `-a<=C1<C2<=1`;
* `max(a+A1)=7/4<2`;
* `max(A2-C1)=39/20<2`;
* `inf A1>sup C1` and `inf A2>sup C2`.

There is no early endpoint absorption or positive-mass center atom. Every
path reaches its final endpoint by time 19/10. Hence this is an ordinary
finite-wave law, with no limiting characteristic or vanishing margin.

## 3. The exact fixed-start turn comparison

Fix z=1/2. Let M(s,-z) start at -z, move right to

    ((s+z)/2,(s-z)/2),

then visit -1 at time s+1 and +1 at time s+3. Consider
`1<=s<=2+z=5/2`.

Every initial a is greater than z, so A(z)=0. Also every C1 is below z
and every C2 is above z. Therefore the early positive capture front is
exactly

    R(s,z)=B2(s).                                      (3)

The free-turn identity gives

    C_s(s,z)=(2-B2(s))/2-(s+11/2)B2'(s)/4.              (4)

At the endpoint-turn boundary s=5/2, all positive ranks have already been
captured: B2 has reached one at s=19/10. Thus there is no missing endpoint
jump in extending this comparison to the closed range.

Substituting (1) into (4) yields

    C_s=1                                  for 1<s<11/10,
    C_s=-28/5-6s                           for 11/10<s<6/5,
    C_s=gamma(s-s0)/[2(s+11/2)]             for 6/5<s<3/2,
    C_s>0                                  for 3/2<s<19/10,
    C_s=1/2                                for 19/10<s<5/2.   (5)

On the penultimate interval the derivative decreases linearly, and its
minimum at 19/10 is exactly `3971/98000>0`.

The initial increase contributes 1/10, while the following sharp decrease
contributes -5/4. Consequently

    C(6/5,z)=C(1,z)-23/20.

Since C(1,z)=3, this is 37/20. Thus the later minimum is strictly below
every turn before the incoming layer; the signs in (5) settle all turns
afterward as well.

For gamma=0, every s in `[6/5,3/2]` is a global minimizer over the closed
range `[1,5/2]`, with payoff 37/20.

For gamma=1, the unique global minimizer is the strict interior point
s=s0=27/20. On the middle interval,

    C_ss(s,z)=137/[40(s+11/2)^2]>0.

Its exact payoff is

    77/40-(137/40) log(137/134).

The payoff itself is not offered as a game bound; its role is to verify
an exact structural counterexample.

## 4. Implication for equilibrium discovery

The inverse-cube density required by free-turn stationarity is compatible
with a perfectly admissible finite final wave. A slightly steeper density
can also give a strict local minimum. Thus concentrating the last wave
into a narrow affine layer is a removable defect of that layer, not a
general proof that infinitely many waves are necessary.

The example deliberately does not solve the start-stationarity equation.
For a genuine equilibrium, the start and turn front equations in
`LAST_WAVE_STATIONARITY.md` must hold together, and all other monster
families must satisfy the lower inequality. Whether an unrestricted
optimal law can have finitely many waves remains unresolved by this
counterexample.
