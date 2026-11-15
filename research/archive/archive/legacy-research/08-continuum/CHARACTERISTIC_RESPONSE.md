# Exact characteristic response to the M1/M2 monster families

## Scope

This note gives an exact response functional for an arbitrary symmetric mixture of the two monster families already used in the project. It includes atoms, starting coincidences, and princess segments lying on a monster characteristic. These cases cannot be discarded when seeking an exact saddle certificate.

The result reduces the princess response to a monotone path problem in two characteristic coordinates. It does **not** prove that the unrestricted monster optimum belongs to these two families, or that one inward princess turn suffices. Those remain separate structural questions.

## 1. Paths and inverse conventions

For `-1<=x<=1`, use the paths

    M1(x;t) = x+t       until t=1-x,
              2-x-t   until t=3-x,
              -1      afterward;

    M2(x;t) = x+t       until t=(1-x)/2,
              1-t     until t=2,
              t-3     until t=4,
              1       afterward.

Their reflections are `-M1(x)` and `-M2(x)`. Let the princess be any 1-Lipschitz path `p(t)` in `[0,1]`, and put

    a = p(0),
    U(t) = t+p(t),
    V(t) = t-p(t).

Both `U` and `V` are continuous and nondecreasing, with

    U(0)=a,  V(0)=-a,
    U(t)+V(t)=2t,
    0<=U(t)-V(t)<=2.

Define the **first** inverse times

    A(c) = inf {t>=0 : U(t)>=c},
    B(c) = inf {t>=0 : V(t)>=c}.

Thus `A(c)=0` for `c<=a`, and `B(c)=0` for `c<=-a`. Since `U(t)>=t` and `V(t)>=t-1`, all the inverses used below are finite. At a plateau, the inverse selects its left endpoint.

There are two different times associated with the characteristic `U=1`:

    s = A(1),
    e = inf {t>=0 : U(t)>1}.

The second is the **right endpoint** of the possibly degenerate plateau at level one. Continuity gives `U(e)=1`, and

    0<=s<=e<=1.

Set

    b = 1-2e.

Then `-1<=b<=a`. Indeed, `p(e)=1-e`, and the speed bound from the initial point gives `1-e-a<=e`.

The distinction between `s` and `e` is essential. Replacing `e` by `s` can assign a very late capture to a path that actually meets the monster during its first turn.

## 2. Exact individual capture formulas

All formulas below are for first capture, not a later intersection.

### 2.1 The M1 pair

For the unreflected path,

    T(M1(x),p) = B(-x)     if x<a,
                  0        if x=a,
                  A(2-x)   if x>a.

For its reflection,

    T(-M1(x),p) = A(-x)    if x<-a,
                   0       if x=-a,
                   B(2-x)  if x>-a.

**Proof.** If `x<a`, the unreflected monster begins below the princess. Its first leg catches her when `t-p(t)=-x`. This happens by its arrival at `+1`, because the princess lies at or below that endpoint. If `x>a`, the monster's first leg starts above the princess and cannot be caught from behind by a speed-at-most-one path. Its descending leg meets her when `t+p(t)=2-x`. The endpoint bounds guarantee a meeting on that leg. Initial equality is capture at time zero. Reflecting the same argument gives the second formula. Monotonicity of `U,V` ensures that the first inverse selects the first encounter even when there is a plateau.

### 2.2 The M2 pair

For the unreflected path, the exact formula is

    T(M2(x),p) = B(3)      if x<b,
                  B(-x)    if b<=x<a,
                  0        if x=a,
                  A(1)     if x>a.

For its reflection,

    T(-M2(x),p) = A(-x)    if x<-a,
                   0       if x=-a,
                   B(1)    if x>-a.

**Proof of the unreflected formula.** Let `tau=(1-x)/2`, the monster's first turning time.

If `x<a`, the monster begins below the princess. It catches her on its first leg exactly when

    B(-x)<=tau.

By continuity and monotonicity of `V`, this is equivalent to

    V(tau)>=-x=2*tau-1,
    U(tau)<=1,
    tau<=e,
    x>=1-2e=b.

The non-strict inequality includes capture exactly at the turn. If the condition fails, the princess is strictly above the turn point. Thereafter `U(t)>1` prevents capture by the descending central leg `1-t`. The final ascending leg captures her at `B(3)`; since `p>=0`, that meeting lies between times three and four.

If `x>a`, the initial monster is above the princess and its initial rightward leg cannot meet her. At its turn,

    U(tau) <= a+2*tau = a+1-x < 1.

It therefore catches the princess on the descending central leg at the first time `U=1`, namely `A(1)`. The equality `x=a` is an initial capture.

**Proof of the reflected formula.** If `x<-a`, the reflected monster starts above the princess and moves left. The first meeting is `A(-x)`, which is no later than time `-x` because `p>=0`; this is before its first turn. If `x>-a`, the reflected monster starts below the princess and its initial leftward leg cannot meet her. Its middle rightward leg is `t-1`, meeting the princess at `B(1)` between times one and two. Initial equality is again a separate zero-time branch.

### 2.3 Two boundary effects that must be retained

**A plateau changes the cutoff.** Let the princess wait at `1/2` until time `1/2`, move left at speed one until reaching zero at time one, and remain there. Then

    s=1/2,  e=1,  b=-1.

Against `M2(-1/4)`, capture occurs at time `5/8`, during the plateau `U=1`. A formula using `1-2s=0` as the cutoff would instead assign `B(3)=3`, which is incorrect.

**At the cutoff, use the early branch.** At `x=b<a`, capture is `B(-b)<=e`. It need not equal `s` or `e` if the plateau degenerates and `V` has an earlier flat segment. For example, let `p` wait at `1/4` until time `1/4`, then move right at speed one. Here `s=e=1/2`, `b=0`, but `B(0)=1/4`: `M2(0)` captures the princess before its turn.

For an atomless monster start distribution, a single cutoff value has zero mass. For finite supports or a proposed continuum law with atoms, this equality case changes the payoff and must be handled exactly.

## 3. Exact response functional for arbitrary start measures

Let `mu_1,mu_2` be finite nonnegative Borel measures on `[-1,1]`, with combined total mass one. The monster first chooses its family and parameter according to these measures, then chooses the displayed path or its reflection with equal probability.

The pairwise formulas give the following exact identity, including all point masses:

    2J(p) =
      integral_{[-1,a)}   B(-x)   dmu_1(x)
    + integral_{(a,1]}    A(2-x)  dmu_1(x)
    + integral_{[-1,-a)}  A(-x)   dmu_1(x)
    + integral_{(-a,1]}   B(2-x)  dmu_1(x)

    + mu_2([-1,b)) * B(3)
    + integral_{[b,a)}    B(-x)   dmu_2(x)
    + mu_2((a,1]) * A(1)
    + integral_{[-1,-a)}  A(-x)   dmu_2(x)
    + mu_2((-a,1]) * B(1).

Here `J(p)` is the expected capture time. Empty intervals contribute zero, and the initial-equality branches contribute zero automatically through their omission from the respective integrals.

The restriction `p>=0` is sufficient when maximizing against a symmetric
monster distribution. Here is a direct proof that does not require the
general quantile-coupling theorem. Put `q=abs(p)` and fix a reflected monster
pair `m,-m`. The earlier of the two capture times is the first time
`abs(p)=abs(m)`, so it is identical for p and q. Call this time t1. If the
contact is at zero, both monsters capture both paths then. Otherwise rename
the monster so that `m(t1)=q(t1)>0`, and put `sigma=sign(p(t1))`. The first
original capture is against `sigma*m`. At t1, the difference between p and
the other monster `-sigma*m` has sign sigma. At the later capture time t2
for q, one has `-m(t2)=q(t2)`, so this difference becomes
`p(t2)-sigma*q(t2)`, which has the opposite weak sign. By continuity, the
other original capture occurs by t2. If t2 is infinite the comparison is
automatic. Thus

    T(m,p)+T(-m,p) <= T(m,abs(p))+T(-m,abs(p)).

The absolute-value path remains 1-Lipschitz. Integrating this pairwise
inequality proves the claim for every symmetric monster law. This is a
reduction of the **princess response to a symmetric monster law**, not an
a priori restriction on both players.

## 4. A separable monotone-path formulation

For fixed `a` and `e` (hence fixed `b`), define threshold measures `alpha` and `beta` by assigning the terms in the preceding formula to their inverse type:

* `alpha` receives the pushforward of `mu_1` on `(a,1]` under `x -> 2-x`, the pushforwards of `mu_1` and `mu_2` on `[-1,-a)` under `x -> -x`, and an atom of mass `mu_2((a,1])` at threshold one.
* `beta` receives the pushforward of `mu_1` on `[-1,a)` under `x -> -x`, the pushforward of `mu_1` on `(-a,1]` under `x -> 2-x`, the pushforward of `mu_2` on `[b,a)` under `x -> -x`, an atom of mass `mu_2((-a,1])` at threshold one, and an atom of mass `mu_2([-1,b))` at threshold three.

Then

    2J(p) = integral A(c) dalpha(c) + integral B(c) dbeta(c).

The first-inverse convention has the exact layer-cake representation

    A(c) = integral_0^infinity 1_{U(t)<c} dt,
    B(c) = integral_0^infinity 1_{V(t)<c} dt.

Consequently, by Tonelli's theorem,

    2J(p) = integral_0^4 [alpha((U(t),infinity))
                         + beta((V(t),infinity))] dt.       (1)

The interval tails are **open at the current characteristic value**. Replacing them with closed tails would incorrectly treat atoms lying on a capture characteristic as survivors. The upper integration limit is four because every monster in these two families has completed an endpoint-to-endpoint traversal by then.

Conversely, any pair of continuous nondecreasing functions `U,V` satisfying

    U+V=2t,  0<=U-V<=2,  (U(0),V(0))=(a,-a)

defines a 1-Lipschitz path `p=(U-V)/2` in `[0,1]`. For `t_2>=t_1`, nonnegative increments of both coordinates summing to `2(t_2-t_1)` imply `|p(t_2)-p(t_1)|<=t_2-t_1`. Thus (1) is an exact characteristic-path formulation.

When `e` is fixed as a parameter, its defining condition must also be retained:

    U(e)=1,
    U(t)<=1 for t<=e,
    U(t)>1 for t>e.

Merely requiring `U(e)=1` admits paths with a longer plateau and assigns them the wrong M2 cutoff. The strict post-`e` condition is one reason an optimal response may be approached rather than attained.

## 5. An exact local exchange identity

Write

    f(u)=alpha((u,infinity)),
    g(v)=beta((v,infinity)).

Consider a rectangle `[u_0,u_1] x [v_0,v_1]` lying within the strip `0<=u-v<=2`. Compare two characteristic paths with the same entrance and exit:

1. increase `U` from `u_0` to `u_1`, then increase `V` from `v_0` to `v_1`;
2. increase `V` first, then `U`.

Each coordinate is increased at rate two while the other is held fixed. These are speed-one princess legs. Assume the exchange preserves the parameter `e`; for example, the rectangle can lie wholly on one side of `U=1`.

Put `Delta_u=u_1-u_0` and `Delta_v=v_1-v_0`. Direct integration of (1) gives

    J(U-then-V) - J(V-then-U)
      = ( Delta_u * beta((v_0,v_1])
          - Delta_v * alpha((u_0,u_1]) ) / 4.              (2)

This identity is exact for atomic measures as well as continuous densities. Thus a local exchange favors processing the `U` interval first precisely when the mean `beta` mass density on the corresponding `V` interval exceeds the mean `alpha` mass density on the `U` interval.

The linked measures `alpha,beta` depend on the proposed monster law and on `a,e`. An actual one-inward-turn or wait-in-out reduction must prove enough ordering inequalities of the form (2), with the strip boundaries and the `U=1` transition included, to eliminate every other path shape. No such inequality follows merely from the definitions of M1 and M2.

## 6. What this supplies, and the remaining theorem

This representation removes unrestricted princess path coordinates from individual capture equations. For a proposed exact monster density, its response can be studied as a separable monotone-path control problem with two continuous initial/frozen parameters, `a` and `e`, and explicit treatment of atoms.

It does not yet reduce that control problem to a finite list of princess shapes. It also does not prove an unrestricted monster lower inequality. To use it in a complete saddle proof, one would still need to:

1. derive a candidate start measure and a globally sufficient response-shape or dual-potential argument for (1);
2. find a matching princess law whose guarantee holds against **all** monsters, including families beyond M1/M2;
3. verify any proposed support atoms using the exact branches in Section 2, rather than limiting formulas valid only away from plateaus and coincidences.

The nested stationary-shell counterexamples in `../07-structural-audit/CAPTURE_ORDER.md` show why a universal two-turn claim about best monster responses cannot replace step 2.
