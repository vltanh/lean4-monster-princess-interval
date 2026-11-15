# A strict inward attack excludes an ordinary initial tail

## Result

An endpoint construction with an ordinary initial outward run cannot be a
matching lower strategy wherever positive-start `M2(a,1)` is active and the
initial princess distribution has positive density. The obstruction is an
explicit finite capture improvement, not a numerical residual or an
asymptotic conjecture. It applies even if the later incoming and outgoing
fronts solve their cost equations exactly.

Consequently the ordinary high-rank replacement discussed in
`TERMINAL_SOURCE_FIXED_POINT.md` is only a conditional equation solver.
It cannot close the unrestricted game in that form. The initial path must
change, or the positive-M2 activity must end. A curved initial path with a
unit tangent is not excluded: the argument needs a positive-length unit
outward run, not merely instantaneous velocity one.

## 1. Routes and the local ordinary-wave assumptions

Let the positive princess paths be ordered by their initial position `b`,
with initial CDF `A`. Reflect the whole law fairly. In an initial-position
neighborhood of a point `0<a<1`, suppose each path begins by running outward
at unit speed, turns onto the incoming characteristic `U=u(b)`, and first
crosses `V=-a` on that incoming leg. The usual ordinary formula is

    p_b(t)=min(1,max(min(b+t,u(b)-t),t-c(b),0)),

with increasing `u`, decreasing `c`, and strict local inequalities

    a<u(a)<1,          c(a)>-a.

These inequalities ensure a genuine initial outward run and an incoming
crossing before the final outward turn. Assume the functions are continuous
at the ranks in question, that `A({a})=0`, and that `A` gives positive mass to every
sufficiently short interval immediately above `a`. Initial atoms require
their separate first-contact bookkeeping; this theorem does not replace
them by density values.

Write `g(a)=M2(a,1)` for the reflected pair that starts at `a`, moves right
along `V=-a` to `U=1`, then visits `-1` at time two and `+1` at time four.
Let `Cg(a)` be its expected capture time.

The initial-inward route `I(z,v)` has vertices

    (0,z), ((z+v)/2,(z-v)/2), ((1+v)/2,(1-v)/2),
    (2,-1), (4,1),                 -z<=v<z.

It initially moves left, turns right along `V=v`, reaches `U=1`, and then
performs the same final sweeps. Denote its reflected-pair cost by `CI(z,v)`.
In particular `I(a,-a)=g(a)`.

## 2. The finite improvement

Choose `delta>0` sufficiently small that

    a+delta<min(u(a),1),        c(a+delta)>-a.

Compare `g(a)` with `I(a+delta,-a)`. They join at time `delta/2`, at
position `a+delta/2`, and coincide thereafter. On the reflected side they
remain in the negative half-interval before that join, so their captures
of nonnegative princesses are identical.

On the unreflected side, the new first inward segment captures precisely
the newly enclosed initial-position band `a<b<a+delta`. For these ranks,
the old and new first captures are respectively

    old: (u(b)-a)/2,       new: (a+delta-b)/2.

The strict local inequalities guarantee both capture descriptions. Lower
ranks remain behind both prefixes until the common continuation; higher
ranks remain ahead until that continuation. Order therefore makes every
other capture unchanged.

Including the fair reflection gives the exact identity

    4[CI(a+delta,-a)-Cg(a)]
       = integral_(a,a+delta] [2a+delta-b-u(b)] dA(b).       (1)

The integrand is at most `a+delta-u(a)<0`. Thus

    CI(a+delta,-a)<Cg(a).                                  (2)

This proves a strict response improvement against the supplied lower law.
It requires no indifference equation and no limiting exchange of path
laws. In particular, if the lower law is claimed to guarantee `c` and
`Cg(a)=c`, (2) contradicts that guarantee.

The nonatomic assumption at the old start matters. If there is an atom
there, the original route captures it at time zero while the shifted
route captures it at `delta/2`. In the displayed local ordinary setting,
the four-score difference then has the extra term `delta A({a})`; it
cannot be omitted when claiming strict improvement.

## 3. Directional form and the missing initial phase

If `A` has density `rho(a)>0`, dividing (1) by `delta` gives

    4 partial_z CI(a,-a)=-(u(a)-a)rho(a).                   (3)

Differentiating `CI(a,-a)=Cg(a)` along the diagonal then gives the
one-sided turn derivative

    4 partial_v CI(a,-a+)
       =-4 Cg'(a)-(u(a)-a)rho(a).                         (4)

If `Cg` is constant on an ordinary branch, (4) is strictly negative.
Moving the first inward-turn characteristic just above `-a` also defeats
the proposed active value, even while holding the monster's start fixed.

The relevant discontinuity is a first-contact discontinuity in rank:

    beta_(A(a))(-a)=0,
    lim_(q downarrow A(a), q>A(a)) beta_q(-a)=(u(a)-a)/2.

Replacing the second expression by zero loses the entire obstruction.
For an immediately curved initial path the right limit can be zero;
the finite attack then changes other early captures at the same order and
the ordinary-wave calculation is unavailable. A viable endpoint solution
therefore needs its actual initial characteristic field, including its
attachment to the diagonal, rather than only an adjusted incoming front.

## 4. Exact audit

`packages/interval_turn_sheet/verify_initial_inward_cdf.py` compares the
full inward-route CDF identity with independent capture-record integration.
It separately checks (1) and (4) on rational ordinary laws. The derivative
fixtures are piecewise quadratic and give the same rational derivatives
at two stencil widths; the finite improvements in (1) use exact rank
integrals and are strictly negative.

The verifier also retains time-zero and incoming-characteristic atoms,
including a fixture where substituting a closed initial row for its strict
trace changes the answer by `3/8`. These are tests of the identities and
the exclusion. They do not supply a replacement equilibrium or change the
repository's claimed game bounds.
