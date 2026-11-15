# A sharp outward-time cutoff from the opposite half

This strengthens the existing exact-horizon reduction. It uses the already
proved reduction to symmetric ordered Princess laws: a fair, fixed sign
times a random nonnegative one-Lipschitz radius path. Capture includes
co-location, and all physical paths remain in `[-1,1]`.

Write `J(m,mu)` for expected capture time, `S(mu)=inf_m J(m,mu)` for
Princess security, and `V=sup_mu S(mu)` for the unrestricted value.
For a Monster path let `tau_0` be its first visit to zero, with infinity
allowed. All arguments below concern arbitrary legal paths, including
paths with infinitely many turns.

## 1. The parameterized forcing inequality

Fix a physical time `T>=0`. Replace every radial Princess path after `T`
by its maximally outward continuation:

\[
 R^T(t)=
 \begin{cases}R(t),&t\le T,\\
 \min\{1,R(T)+t-T\},&t\ge T.
 \end{cases}
\]

The transformed law `mu^T` is legal, symmetric, ordered, and absorbed by
time `T+1`.

**Monster paths with `tau_0<=T`.** At the first center visit, an uncaught
positive-side Princess is strictly above the Monster; an uncaught negative
Princess is strictly below. Otherwise continuity would already have forced
a contact. These strict orders persist until capture, so they hold at `T`
for every survivor. The new positive continuation is pointwise at least
the original one, and the new negative continuation is pointwise at most
the original one. A Monster cannot meet the new outer path before crossing
the original inner path. Thus, path by path,

\[
 \tau_0(m)\le T\quad\Longrightarrow\quad
 J(m,\mu^T)\ge J(m,\mu).
\tag{1}
\]

Already captured paths have exactly the same capture times. Zero-radius
atoms are included: any such path present at a center contact is already
captured and is not a survivor to which a strict order is assigned.

**Monster paths with `tau_0>T`.** Its sign is constant on `[0,T]`, and
`m(T)!=0`. Suppose that sign is positive. The entire fair negative half is
uncaptured. After `T`, a negative Princess at radius `r=R(T)` has position

\[
 -\min\{1,r+t-T\}.
\]

Until this path reaches `-1`, the speed constraint gives

\[
 m(t)-[-r-(t-T)]\ge m(T)+r>0.
\]

Hence it cannot be caught in the interior. Any capture must occur at
`-1`, and the Monster cannot arrive there before `T+1+m(T)`. Reflection
gives the same statement for a negative Monster. Therefore

\[
 \boxed{\quad
 \tau_0(m)>T\ \Longrightarrow\
 J(m,\mu^T)\ge\frac{T+1+|m(T)|}{2}
                    >\frac{T+1}{2}.\quad}
\tag{2}
\]

This also covers `R(T)=0`: its distance from the Monster is still strictly
positive. Combining (1) and (2) proves

\[
 \boxed{\quad S(\mu^T)\ge
        \min\{S(\mu),(T+1)/2\}.\quad}
\tag{3}
\]

The constant `(T+1)/2` is sharp under these hypotheses alone. Let both
reflected radii be `a>0` until `T`, then outward. A Monster starts at `a`,
holds there until `T`, then moves to `-1`. It captures the positive half
at time zero and the negative half at time `T+1+a`, so its expected time
is `(T+1+a)/2`, tending to the bound as `a` decreases to zero.

## 2. Exact choices of cutoff

If `U` is any certified unrestricted upper bound, every Princess law has
security at most `V<=U`. Consequently every

\[
 T\ge2U-1
\]

preserves security under outward forcing. The same statement holds
theoretically with `U=V`.

For the current exact upper

\[
 U=\frac{1140799301969009059644426513}
          {800000000000000000000000000}<\frac32,
\]

`T=2` is a convenient global cutoff. `T=15/8` is already sufficient,
because `(T+1)/2=23/16>U`; the rational choice `T=2U-1` also satisfies
the criterion exactly. No claim that `T=1` is sufficient follows from
this argument.

In particular, the unrestricted value is preserved by Princess laws
outward after time two and absorbed by time three. Thus the existing
analytic-exit potential hierarchy with **absorption horizon three** is
globally complete in its proved supremum sense.

## 3. Every optimal Monster law visits the center early

Assume the previously proved minimax equality and existence of an optimal
Monster law `nu`. The claim applies to every such law, without assuming a
finite support or a particular clock representation.

Choose symmetric ordered Princess laws `mu_n` with
`S(mu_n)>=V-epsilon_n`, where `epsilon_n` tends to zero. For fixed `T`,
put `A_T={tau_0>T}` and `p_T=nu(A_T)`. Applying (1) on the complement
and (2) on `A_T`, while using optimality of `nu` against the legal law
`mu_n^T`, gives

\[
 \begin{aligned}
 V&\ge J(\nu,\mu_n^T)\\
  &\ge(1-p_T)(V-\epsilon_n)
      +p_T\frac{T+1}{2}
      +\frac12\int_{A_T}|m(T)|\,d\nu(m).
 \end{aligned}
\]

Letting `n` tend to infinity yields the useful exact inequality

\[
 \int_{A_T}|m(T)|\,d\nu(m)
       \le (2V-T-1)\,p_T.
\tag{4}
\]

Taking `T=2V-1` makes the right side zero. The integrand is strictly
positive on `A_T`, so that set has zero measure. Therefore

\[
 \boxed{\quad \tau_0(m)\le2V-1
          \quad\text{for every optimal Monster law, almost surely}.\quad}
\tag{5}
\]

Equivalently, one may first use every `T>2V-1`, obtain `p_T=0` from its
uniform positive gap, and take a countable decreasing sequence of cutoffs.
No optimal Princess law or limiting interchange of capture functions is
needed for this argument.

## 4. Best responses complete by time six

Fix a Princess law outward after `T`, with security at most `(T+1)/2`.
It is endpoint absorbed by `T+1`. First restrict a Monster to its prefix
through `T+1` followed by a fastest endpoint tour, preserving the order
of its future first endpoint visits. This cannot increase capture times
of the surviving endpoint Princesses, and completes by `T+5`. That
bounded complete-endpoint path class is compact; expected capture is
lower semicontinuous, so an exact best response exists in it.

By the strict inequality in (2), a best response cannot have `tau_0>T`.
For a response with `tau_0<=T`, every Princess surviving at `T` lies
strictly above or below the Monster and then moves outward at unit speed.
No such survivor can subsequently be captured in the interior. All its
remaining captures are at the appropriate endpoint.

Replace the Monster suffix after `T` by a fastest tour in the order of
its future first endpoint visits. Each endpoint is reached no later than
in the original suffix. Starting at `x=m(T)`, the tour length is either
`3-x` or `3+x`, hence at most four. This proves an exact best response
exists with center visited by `T` and both endpoints completed by `T+4`.

For `T=2`, the completion horizon is **six**. To realize a global upper
law in this class, directly transform an existing optimal symmetric
Monster law `nu`. Section 3 gives center visitation by two almost surely.
Choose a common measurable fastest endpoint-tour rule after two,
preserving the order of endpoints still unvisited at two. An endpoint
already visited by two has no surviving corresponding Princess half:
that half was contacted between the center and endpoint visits. Thus
visit any remaining endpoint first; an already visited endpoint may be
visited afterward to finish the normalized tour. If both were visited,
all Princess paths have already been captured. The rule can be chosen
reflection-equivariantly (randomizing a completely symmetric tie), so the
transformed law `nu'` remains symmetric.

This single suffix transformation dominates simultaneously against every
outward-after-two law. For every symmetric ordered Princess law `mu`,

\[
 J(\nu',\mu)\le J(\nu',\mu^2)
        \le J(\nu,\mu^2)\le V.
\]

The first inequality is survivor-order domination because `nu'` visits
the center by two; the middle inequality is the endpoint-tail improvement;
the final inequality is global optimality of `nu`. Symmetrizing an
arbitrary Princess law does not change its payoff against symmetric
`nu'`, and common-quantile reordering only increases that payoff. Thus
`nu'` is a global optimal upper law supported on center-by-two,
completed-by-six paths, without a new restricted minimax argument.

As usual, normalize the continuation after the first endpoint to the
fastest sweep to the other endpoint. This pointwise improves every
capture payoff. Center visitation by two is preserved: if the first
center visit was after the first endpoint, the fastest sweep reaches
zero no later than the previous continuation. Thus the first endpoint
time `sigma` of the normalized optimal Monster is at most four.

## 5. The protected-turn full-matching horizon becomes eight

The previously proved protected-turn construction modifies each sampled
original path pair at most once. Its input may now be the normalized
optimal law with center visited by two and first endpoint `sigma<=4`.

For a boundary turn, orient the original first endpoint as `+1` and use
the established notation

\[
 a=\sigma-\eta,\qquad m(a)=1-\varepsilon,
 \qquad0<\varepsilon\le\eta\le\tfrac12.
\]

The modified path follows the original through `a`, moves to `-1`, then
sweeps to `+1`. Its first endpoint time is

\[
 T_{\rm new}=\sigma+2-\eta-\varepsilon\le\sigma+2,
\]

and its completion time is at most `sigma+4<=8`.

Center visitation by two is preserved. If the original center visit
`c` precedes `sigma`, the speed bound gives `sigma>=c+1`, so
`a>=sigma-1/2>c` and the old visit remains in the unchanged prefix.
If the original center visit follows its first endpoint, the normalized
sweep gives `c=sigma+1<=2`; the modified path reaches zero at
`sigma+1-eta-epsilon<=c`. Sweeps used by the separate front-completion
construction have their own explicit center visit at time one.

The protected negative tail invariant prevents a modified copy from being
turned again. The same finite-measure limiting argument therefore yields
an attained zero-deficiency optimal law supported on paths that visit
the center by two and complete both endpoints by **eight**.

This conclusion uses the protected-turn/full-matching theorem already
proved; it does not assert that arbitrary clock compression preserves the
protection label during the construction.

## 6. Distinguish the two horizon constants

The normalized zero-credit physical game now has completion horizon six.
The analytic-exit potential proof is a *statewise future-credit* problem
with arbitrary queue credits. With absorption horizon three it still
uses its established safe relative completion bound `3+4=7`, charged
mass at most fourteen, and Lipschitz constants `14L,4+14L,1,1`.
The new physical normalization alone does not replace that statewise
bound by six. The global completeness proof needs only that absorbed-by-
three fields are now value dense, which follows directly from (3) and
the existing radial-smoothing argument.
