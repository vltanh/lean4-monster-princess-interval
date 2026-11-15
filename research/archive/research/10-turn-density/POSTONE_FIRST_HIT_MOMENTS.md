# First-hit moments with unrestricted post-one high-rank motion

This note retains the actual first crossing of `U=1`. It does not identify
that crossing with the final outgoing leg. In particular, it applies when
an ordered princess path has additional motion at `U>1`, or when its last
outgoing characteristic has a different rank trace.

## 1. Exact positive-M1 identity

Let the nonnegative paths be `p_q`, with the usual symmetric reflection,
and suppose `p_q(t)=1` for `t>=2`. Define the first inverses

    alpha_q(u)=inf{t>=0:t+p_q(t)>=u},
    beta_q(v)=inf{t>=0:t-p_q(t)>=v}.

These are first contacts, including a contact at time zero and the start
of a coincident characteristic. Set `b_q=p_q(0)`. For `0<x<1`, put
`z=1-x` and use the strict initial distribution

    A_<(z)=Pr(b_q<z),       r_ge(x)=Pr(b_q>=1-x).

The positive M1 route starts at z, visits `+1`, then visits `-1`. Its
capture time against the positive copy is `alpha_q(1+x)` when `b_q<z`,
and `beta_q(-1+x)` when `b_q>=z`. The latter convention retains an
initial atom at z, whose capture time is zero. The reflected copy is
captured at `beta_q(1+x)=2+x`.

The endpoint route starts at `+1` and sweeps left. Its reflected-pair
four-cost is

    V4_end=2 integral alpha_q(1)dq+2 integral beta_q(1)dq.       (1)

Define the complete post-one first-inverse source

    Q_all(x)=integral[2alpha_q(1+x)-2alpha_q(1)-x]dq>=0,         (2)

and the possible `V=1` contact correction

    H1=2 integral[2-beta_q(1)]dq>=0.                            (3)

The inequality in (2) follows from the speed bound on `U=t+p(t)`.
Endpoint absorption by time two gives `beta_q(1+x)=2+x`; no assumption
about earlier endpoint absorption is required.

Directly partitioning the positive initial ranks proves

    4[Cf(1-x)-C_end]
      =3x+Q_all(x)+H1
        -2 integral_(b_q>=1-x)
                [alpha_q(1+x)-beta_q(-1+x)]dq.                 (4)

The bracket is nonnegative: a princess initially to the right of z is
captured by the initial rightward leg no later than the right-endpoint
visit at time x, while `alpha_q(1+x)>=x`. Formula (4) retains all
post-one high-rank flux in `Q_all`. It makes no low/high source split.
When `beta_q(1)=2` almost surely, `H1=0`.

If

    c1(q)=2alpha_q(1)-1,

then (1) is `V4_end=5+integral c1-H1`. The final outgoing
characteristic `c2(q)` can differ from `c1(q)`. Substituting c2 into this
endpoint moment would be an error for a path with later motion.

## 2. A necessary high-rank first-hit moment

Put

    M(x)=integral_(b_q>=1-x) alpha_q(1)dq.

The initially lower ranks contribute at least `x A_<(1-x)` to the
four-cost difference, because their two alpha contacts are separated by
at least `x/2`. The highest initial ranks contribute at least `-2M(x)`,
and the reflected copies contribute `2x+H1`. Hence

    4[Cf(1-x)-C_end]
       >= x[2+A_<(1-x)]-2M(x)+H1.                              (5)

An active positive-M1 route no more expensive than the endpoint route
therefore requires

    M(x)>=[x(2+A_<(1-x))+H1]/2.                                (6)

This statement has no pre-one incoming, final-turn-count, or ordinary-wave
assumption. Initial atoms are included by the strict/closed partition
above. If `r_ge(x)~D sqrt(x)` and `H1=0`, the average first `U=1` contact
among those highest initial ranks must be at least asymptotically
`3sqrt(x)/(2D)`. A uniformly `O(x)` contact time cannot supply this
moment.

For example, suppose each of these highest paths stays at or above its
initial position until first reaching `U=1`. Then `alpha_q(1)<=1-b_q<=x`.
Equation (5) gives the particularly simple strict comparison

    4[Cf(1-x)-C_end]>=3x A_<(1-x)+H1.                            (7)

Thus an entire highest-rank initial phase that first crosses `U=1` while
moving monotonically outward cannot coexist with positive-M1 activity
there when `A_<(1-x)>0`. A curved initial arc is included in this
conclusion. More generally, `alpha_q(1)<=C(1-b_q)` implies the lower bound
`x[3-(1+2C)r_ge(x)]+H1`, which is positive near the endpoint if there is
no initial endpoint atom.

This does **not** exclude post-one motion after an earlier inward
excursion. Such a path can have a first `U=1` contact much later than its
initial distance from the endpoint.

## 3. Ordering a long post-one phase

For a fixed negative characteristic V, the first rank inverse
`phi_q(V)=2beta_q(V)-V` is nondecreasing in q. Consequently, if one rank
`q0<1` has `phi_q0(V)>1`, every higher rank has U excess at least
`phi_q0(V)-1`. A highest-rank post-one phase cannot occupy a common
nonzero V interval while its U excess tends to zero throughout that
interval.

A long final phase is still possible. Its limiting rank contour must
instead separate from `U=1`, or the interval occupied by the near-one
part of the phase must shrink. For example, contours may approach the
endpoint edge `U=V+2`. An initial endpoint rank has zero mass in a
continuous initial law, so a discontinuity of final hitting times in that
rank limit is not by itself excluded. These ordering facts do not provide
a bound on `Q_all'` without further flux and coverage conditions.

## 4. Verification and scope

Run

```sh
python -B packages/interval_turn_sheet/verify_postone_first_hit_moments.py
```

The verifier intersects polygonal monster and princess paths directly and
compares them with the first-inverse identities. Its additional fixtures
include ordinary first peaks beyond `U=1`, a curved initial outward arc,
later post-one motion after an earlier inward excursion, initial atoms,
and a `V=1` contact atom. The source and moment gate are exact identities
and necessary conditions. They do not specify the complete high-rank
phase, a matching upper law, or the unrestricted game value.
