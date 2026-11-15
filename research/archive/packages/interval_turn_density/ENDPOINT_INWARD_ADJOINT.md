# Endpoint-second inward rows: exact upper adjoint

This family is different from a regular interior second-turn surface.
Its second turn is the positive endpoint, where the closed radial CDF
equals one. The interior cap and homogeneous coarea bounds do not remove
it. The identities below construct its linear score and variations;
they do not yet give a matched normalized law.

## 1. Physical route and closed first contacts

For `0<z<=1` and `-z<=v<z`, let `E(z,v)` follow

    (0,z), ((z+v)/2,(z-v)/2), (1+v,1), (3+v,-1).      (1)

Reflect fairly. This is `I(z,v,s)` on the endpoint face `s=2+v`.
The boundary v=-z is positive M1. The boundary v=z is excluded here
because a first contact with a waiting center atom needs its separate
closed correction.

For a nonnegative princess starting at a, use the actual first inverses
alpha(U), beta(V), and `psi(U)=2alpha(U)-U`.
The unreflected contact is exactly

    a<=z: alpha(z) if psi(z)<=v, otherwise alpha(2+v);
    a>z:  beta(v).                                   (2)

The reflected contact is `beta(2+v)`. In the second line of (2), middle
capture always occurs: the physical bound `phi(v)<=2+v` includes equality
at the endpoint. There is no missed-beta branch with a later sweep.
For a path absorbed at +1 by time two, `beta(2+v)=3+v`, since v>-1.
All initial and turn equalities in (2) are closed first captures.

Give the endpoint face a density `i(z,v) dz dv`. Its mass is simply the
integral of i over the physical triangle. For an arbitrary absorbed path,
four times its score is the integral of

    6+2v
       + [ z+psi(z) if a<=z and psi(z)<=v,
           2+v+psi(2+v) if a<=z and psi(z)>v,
           v+phi(v) if a>z ].                        (3)

Thus the first/last inverse distinction is retained even on this
singular second-turn face.

## 2. The general pre-one inverse price

Write

    T_z(V)=integral_V^z i(z,v)dv,
    j_a(V)=integral_|V|^a i(z,V)dz,

with empty integrals zero. At a regular negative prefix point U<1,
the endpoint-I contribution to the local inverse derivative is

    j_a(V)-T_U(V)-[2+psi(2+V)-U]i(U,V).              (4)

The coefficient is twice the time between the first inward turn and
the delayed alpha capture. It is nonnegative on a legal monotone path.
It must use the actual first inverse at `2+V`, including any post-one
motion. At the initial boundary U=z,V=-z it becomes
`2alpha(2-z)`, the coefficient in the independent active-f curvature
calculation.

No restriction `i(z,v)=0` above a pre-one outgoing cap follows here.
At the endpoint turn the closed second frontier is one, even if its
interior trace is below the monster's initial frontier. Replacing that
closed endpoint by its interior limit would delete this physical
capture and incorrectly recover the earlier cap.

## 3. Exact functional for a final pre-one incoming phase

For the rest of this section assume the princess's final incoming
motion ends at `(u,c)`, with `a<=u<1` and `-a<c<0`, and is followed by
the final outward leg to the endpoint. Let its prefix graph be
`U=phi(V)`, `-a<=V<=c`. Then

    psi(2+V)=c          whenever V<=c,

so (4) simplifies to

    j_a(V)-T_U(V)-(2+c-U)i(U,V).                     (5)

The complete four-score is

    F_E=C_E(a,c)+integral_-a^c q_E(a,c,V,phi(V))dV,

    q_E=(U-V-2)j_a(V)
          -integral_a^U[T_z(V)+(2+c-z)i(z,V)]dz,      (6)

where the explicit constant is

    C_E = integral_all (6+2v)i(z,v) dz dv
          +integral_(z<a) (2+2v)i(z,v) dz dv
          +integral_a^1 [
             integral_-z^c (2+v+c)i(z,v)dv
             +(z+c)T_z(c)] dz.                      (7)

This is a linear feature formula for any frozen prefix. It retains the
entire row tail T; no assumption that T is smaller than p or k is used.

Let `u0=phi(-a+)`. The initial-coordinate derivative is

    (F_E)_a
      =integral_-a^c [V+phi(V)]i(a,V)dV
         +integral_c^a 2(1+V)i(a,V)dV
         +q_E(a,c,-a,u0).                            (8)

The final term is the initial outward-connector correction; it vanishes
when u0=a. A large unweighted row tail can have a much smaller weighted
contribution in the second integral. It cannot simply be discarded.

For the final-characteristic derivative, define the missed-row mass

    Q_c=integral_u^1 M(z)dz
           +integral_a^u integral_-z^psi(z)i(z,v)dv dz,
    M(z)=integral_-z^z i(z,v)dv.

Then

    (F_E)_c=Q_c
        +integral_u^1(2+c-z)i(z,c)dz
        -(2+c-u)j_a(c).                             (9)

The negative edge coefficient is now `2+c-u`, rather than the large
interior-second-turn coefficient `u+6-c`. The endpoint contact is what
changes this coefficient. The positive first-turn edge in (9) is also
retained; interior plateau deletion does not remove it.

In terminal deficit coordinates `eta=1-U`, `d=1+c`, the local price in
(5) is `T+(d+eta)i`. The previously studied fixed-second price had
`T+(d+eta-y)i`, with y=1+V. They are different operators.

## 4. The inhomogeneous post-one alpha source

The second threshold lies on `U=2+v`. Its alpha pushforward therefore
comes from the physical endpoint line `v=U-2`, and is

    Q_E,a^psi(U)=integral_(z>=a, z>=|U-2|)
          1_{U-2<psi(z)} i(z,U-2)dz.                 (10)

On the negative-V tail, if `a<=2-U`, every physical start in this
column is above a and misses the first inward leg. Therefore

    Q_E,a^psi(U)=integral_(2-U)^1 i(z,U-2)dz.          (11)

Outside that capacity the restricted first-miss formula (10) must be
used. This source is a boundary measure at first V=U-2. It is not a
regular interior H density, so the homogeneous causal estimate for an
interior surface does not bound it away.

Equivalently, let `phi^+(v)` be the last U on the outgoing
characteristic V=v, or the right limit of the first beta inverse. Then

    Q_E,a^psi(U)=integral_(phi^+(U-2))^1
                                      i(z,U-2)dz.   (12)

At regular levels phi^+ equals phi. At an initial or final outgoing
plateau they differ: using the first phi would incorrectly count exact
first-turn captures as misses. Formula (10) is the primary convention
when the law has a threshold atom.

If the first U=1 crossing of a two-wave path is at c1, then
`psi(z)<=c1` for z<=1. Thus the missed-second source in (10) vanishes
above `U=2+c1`. It can nevertheless extend beyond the positive-M1
source limit `2-a` whenever c1>-a. This is the additional alpha price
which a genuine curved first wave can supply to a later incoming wave.

## 5. A limited pre-one boundary consequence

Equation (9) does not mean the endpoint family automatically replaces
the positive-M2 boundary mass. Let `j_total(c)=integral_|c|^1i(z,c)dz`.
Then `0<=Q_c<=mu_E{z>a}`, and the positive edge in (9) is at most
`(2+c-u)j_total(c)`. If the baseline p,k are integrable and

    (1+c)[p(-c)+j_total(c)] ->0,

the endpoint-I c derivative tends to zero on a final pre-one terminal
branch. Its old endpoint balance again gives g(-c)->w0/8. Even without
that pointwise limit, setting g identically zero throughout such a
terminal interval would force a nonintegrable column lower bound of
order `1/(1+c)`, provided the other c terms have the displayed signs.

This conclusion is confined to the final pre-one branch. On a true
two-wave path, endpoint M1 is already captured at the first U=1
crossing, and its final-turn stationarity is different. The large row
tail and the source (10) also remain in the initial and incoming
equations; this section does not exclude their use in a matched law.

## 6. Independent exact verification

`verify_endpoint_inward_adjoint.py` passes 1,198 exact rational checks:

* 112 closed first-contact identities, including initial equality and
  the positive-M1 boundary v=-z;
* nine complete two-dimensional physical score integrals over 1,023
  independently partitioned capture triangles;
* 18 exact initial-coordinate derivatives, 18 final-characteristic
  derivatives, and 18 local inverse derivatives.

The payoff reference computes actual first segment intersections.
The functional and derivatives are checked independently using
polynomial integration and exact differentiation. The fixtures include
curved prefixes and an initial outward connector. They verify the
endpoint score and its price signs, not equilibrium complementarity.
