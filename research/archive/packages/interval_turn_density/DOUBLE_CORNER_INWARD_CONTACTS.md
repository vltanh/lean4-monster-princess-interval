# Singular double-corner inward law: exact contacts and response obstruction

This note audits a proposed singular support for the general inward
monster family. It gives exact capture identities and finite legal
princess variations. It does not construct a matching strategy or give
a new game-value bound.

## 1. The proposed curve and its closed capture kernel

Consider an ordered family of ordinary nonnegative princess paths with
strictly increasing initial and incoming characteristics `a(q), u(q)`
and strictly decreasing final characteristic `c(q)<0`. A path first
moves outward on `V=-a(q)`, then inward on `U=u(q)`, and finally outward
on `V=c(q)` to the endpoint. Assume `a(q)<u(q)<1` and `-a(q)<c(q)<0`.

For a curve parameter b, define t and sigma by

    c(t(b))=-a(b),       a(sigma(b))=u(b),
    b<sigma(b)<t(b),     S(b)=u(t(b)).                 (1)

The monster is `I(u(b),-a(b),S(b))`, reflected fairly. Thus its first
turn is the initial/incoming corner of princess b, and its second turn
is the incoming/outgoing corner of princess t(b).

Four times the symmetric capture expectation against princess q is

| Rank range | Four-score |
| --- | --- |
| `q<b` | `2+3S(b)+c(q)` |
| `b<=q<=sigma(b)` | `2+2S(b)+u(b)-a(q)` |
| `sigma(b)<q<=t(b)` | `2+2S(b)+u(q)-a(b)` |
| `q>t(b)` | `8+4S(b)` |

Every displayed equality is a first capture, including the initial
contact at `q=sigma(b)`. At `q=b`, the first turn captures the princess;
relative to the left trace, its four-score has the downward contact gap

    D1(b)=S(b)-u(b)+c(b)+a(b)>0.                       (2)

At `q=t(b)`, the second turn captures the princess; the right trace has
the upward gap `6+S(b)+a(b)`. These facts follow directly from the first
inverse capture formula in `FREE_SECOND_INWARD_CONTACTS.md`. In
particular, the contact dip in (2) is real and must be retained.

## 2. The first-turn dip does not cancel the final-turn kink

Give the curve a continuous parameter density `m(b)db`. Fix a princess
rank q and let

    b*=t^{-1}(q),     a=a(q), u=u(q), c0=c(q).

Suppose b* is interior to the curve support, `m(b*)>0`, and the maps
are differentiable with `a'(b*)>0`. From (1),

    S(b*)=u,        a(b*)=-c0,        u(b*)<a.         (3)

The final strict inequality is essential: the curve near b* remains in
the low-monster-start branch when c changes, so it is separated from
the first-turn contact near b=q.

Keep a and u fixed and vary c. Near b*, middle-leg capture occurs
exactly when

    b>=max(a^{-1}(-c), S^{-1}(u)).                    (4)

The unreflected four-score is `u-a(b)` on the captured side and
`2S(b)+6` on the missed side. Their gap at b* is

    D2=6+u-c0>0.

For c below c0, the first argument of the maximum in (4) moves; for c
above c0, the cutoff is fixed. Therefore the curve's total four-score
has the upward derivative jump

    F_c(c0+)-F_c(c0-)=D2*m(b*)/a'(b*)>0.              (5)

The separate first-turn contact at b=q does not move with c. All
remaining capture boundaries in this local configuration contribute
continuous derivatives. Thus a differentiable remaining monster score
cannot cancel (5). Both perturbed princess paths are legal, and

    F(c0+epsilon)+F(c0-epsilon)-2F(c0)
       =D2*m(b*)/a'(b*)*epsilon+o(epsilon)>0.          (6)

At least one of the two paths has a larger score. This excludes the
proposed ordinary incoming/outgoing attachment for the curve law under
the stated smoothness and positive-mass conditions. The fact that the
curve is singular in monster-start coordinates does not remove this
obstruction.

## 3. Varying the incoming level gives a second obstruction

There is also a useful independent variation. Keep a and c fixed and
vary u, assuming q is an interior support point with `u'(q)>0` and
`S'(b*)>0`. Near b=q, first-leg capture has cutoff

    b<=min(a^{-1}(a), u^{-1}(u)).                     (7)

For u below its current value this cutoff moves; above it the cutoff is
fixed. Its contribution to the upward derivative jump is
`D1(q)m(q)/u'(q)`. The second-turn cutoff (4), with c now fixed, adds
another upward contribution. In total,

    F_u(u+)-F_u(u-)
      =D1(q)m(q)/u'(q)+D2*m(b*)/S'(b*)>0.             (8)

The two contact boundaries reinforce each other. They do not supply
opposing kinks. The same finite midpoint argument gives an improving
legal incoming-level variation. This statement is conditional on
interior freedom to vary u and on differentiability of the rest of the
score; it does not exclude a different curved incoming field or an
explicit additional nonsmooth component.

## 4. Independent exact physical verification

Run `verify_double_corner_inward.py`. Its affine rational fixture uses

    a(q)=2/5+3q/5,        u(q)=43/100+57q/100,
    c(q)=-1/3-2q/3,
    sigma(b)=1/20+19b/20, t(b)=1/10+9b/10.

It satisfies (1), with strict separation throughout the tested support.
Three positive polynomial curve densities are tested at three distinct
princess ranks. The checker passes 1,631 exact rational checks:

* 35 closed rank-kernel contacts;
* 162 complete physical curve integrals over 1,398 independent affine
  capture cells;
* nine exact c derivative jumps and nine finite c midpoint gains;
* nine exact u derivative jumps and nine finite u midpoint gains.

The integration partition is built from physical segment endpoint and
line-intersection events. It evaluates actual first captures, without
using the rank kernel or the cutoff formulas to obtain the integrals.
One-sided derivatives are exact polynomial interpolation. The affine
fixtures verify the formulas; the local arguments in (4)-(8) allow
general differentiable front maps.
