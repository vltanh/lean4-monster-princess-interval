# A complete counterexample to the wait-in-out response reduction

## Result and scope

For the symmetric six-row M1/M2 monster mixture below, the supremum over all
princess paths that **wait at their starting point, move inward at speed
one, then move outward at speed one and stay at the endpoint** is exactly

    2641/1600 = 1.650625.

An explicit admissible rational princess path obtains

    100559/60000 = 1.6759833333...,

which exceeds that restricted supremum by

    3043/120000 > 0.

Therefore that three-parameter response family is not sufficient for
arbitrary M1/M2 mixtures, even when finite bottom heights and independent
waiting times are allowed. This is stronger than the earlier exclusion of
a family with a common infinitesimal bottom and a prescribed departure
time.

This theorem does not determine the unrestricted interval game value. It
does not exclude a response-shape theorem with additional optimality
hypotheses on a specific monster law. It also does not assert that every
possible one-inward-phase path, allowing arbitrary motion before and after
that phase, belongs to the restricted family tested here.

## 1. The monster mixture

Use M1 and M2 as defined in `CHARACTERISTIC_RESPONSE.md`. Select a row with
its integer weight divided by 100, and then select the path or its
reflection with equal probability.

| Family | Start x | Pair-weight numerator |
|---|---:|---:|
| M1 | `-1` | 39 |
| M1 | `-1/2` | 5 |
| M1 | `5/8` | 16 |
| M2 | `-1/2` | 9 |
| M1 | `1/2` | 12 |
| M1 | `1/4` | 19 |

The numerators sum to 100. Each of the twelve actual monster paths is
1-Lipschitz and completes an endpoint-to-endpoint sweep by time four.

## 2. The complete restricted princess family

Its parameters are

    0<=b<=a<=1,   u>=a.

Here `a` is the initial height, `b` the bottom height, and `u` the constant
value of `t+p(t)` on the inward leg. In particular, `b` here is a path
height, not the M2 start cutoff from the characteristic-response note.

The vertices are

    (0,a), (u-a,a), (u-b,b), (u+1-2b,1),

followed by a constant tail at one. Zero-length pieces are omitted. An
equivalent formula valid for all t is

    p_{a,b,u}(t) = min(1, max(min(a,u-t), t-u+2b)).         (1)

This includes zero waiting time, zero inward distance, a zero bottom,
endpoint starts, and stationary limiting responses. Reflections give the
same expected payoff because the monster law is symmetric.

It suffices to take `u<=5`: for `u>=5`, the path waits at `a` throughout
`[0,4]`, and every monster has already captured it by time four. Thus the
parameter domain may be taken to be the compact polytope

    D={0<=b<=a<=1, a<=u<=5}.                             (2)

## 3. Inverse times and the finite arrangement

Write `A(c)=inf{t:t+p(t)>=c}` and
`B(c)=inf{t:t-p(t)>=c}`. Directly from the vertices,

    A(c) = 0                  if c<=a,
           c-a                if a<c<=u,
           (c+u-2b)/2         if u<c<=u+2-2b,
           c-1                otherwise;

    B(c) = 0                  if c<=-a,
           c+a                if -a<c<=u-2a,
           (c+u)/2            if u-2a<c<=u-2b,
           c+1                otherwise.               (3)

These are first-inverse formulas, so equality at a plateau selects its
left endpoint. For generic parameters `u!=1`, the M2 plateau endpoint at
level one agrees with `A(1)`. Its start cutoff is

    2a-1    if u>1,
    2b-u    if u<1.                                      (4)

The second formula uses `b<=a<=u<1`, which rules out an endpoint-tail branch
for `A(1)`. The exact nongeneric case `u=1` is handled by the boundary
argument below, rather than assigned the wrong cutoff.

Let X be the set of row starts in Section 1, and define the finite threshold
sets

    C_A = {1} union {-x,2-x : x in X},
    C_B = {1,3} union {-x,2-x : x in X}.

Every branch of the capture formulas and every facet of D belongs to the
following hyperplane arrangement. Extra planes outside D are harmless.

| Left-hand side | Right-hand sides |
|---|---|
| `a` | `0,1`, every `x,-x,(1+x)/2`, every element of `C_A`, and every element of `-C_B` |
| `b` | `0` |
| `b-a` | `0` |
| `u` | every element of `C_A`, and `5` |
| `u-a` | `0` |
| `u-2a` | every element of `C_B` |
| `u-2b` | every element of `C_B`, and every `c-2` for `c` in `C_A` |

To see completeness, (3) supplies all its threshold planes directly.
Initial capture classifications add `a=x,-x`. In (4), comparison with a
monster start adds `a=(1+x)/2` or `u-2b=-x`, already listed. The two formulas
in (4) are separated by the plane `u=1`. No other parameter comparisons
occur.

On each open full-dimensional cell inside D, every capture time is an
affine function of `(a,b,u)`. Hence the expected payoff is affine there.

## 4. Why limiting vertex values give the global supremum

There are two issues: boundaries with capture-time jumps, and covering
every side of every vertex.

### 4.1 A boundary cannot exceed all nearby generic responses

Formula (1) makes the path depend continuously, uniformly on `[0,4]`, on
its parameters. First capture time against a fixed continuous monster,
truncated at four, is lower semicontinuous under that convergence. Indeed,
if capture has not occurred by a time r strictly below the limiting capture
time, the absolute separation has a positive minimum on `[0,r]`; all
sufficiently close paths also survive through r.

The finite weighted payoff is therefore lower semicontinuous. At any
boundary parameter, its value is no larger than the lower limit along a
generic interior sequence approaching that parameter. Consequently the
supremum over D equals the supremum over its open full-dimensional
arrangement cells.

This is why it is legitimate to compute one-sided generic limits next to
`u=1`, initial coincidences, and other capture discontinuities. It is not
legitimate to use a generic capture formula as the actual value at the
boundary itself.

Each cell has a bounded polyhedral closure. An affine function takes its
maximum on that closure at a vertex. Every such vertex is an intersection
of three linearly independent planes in the arrangement. The verifier
enumerates all those intersections that belong to D, using exact rational
Cramer's rule, obtaining **369 distinct vertices**.

### 4.2 A complete finite set of approach directions

The arrangement has only seven normal types, in `(a,b,u)` coordinates:

    (1,0,0), (0,1,0), (-1,1,0), (0,0,1),
    (-1,0,1), (-2,0,1), (0,-2,1).                        (5)

For each of the `2^7` assignments of signs to these normals, consider the
closed homogeneous cone obtained by making every signed dot product
nonnegative. The coordinate sign constraints make every such cone pointed.
Every extreme ray of a nonzero pointed polyhedral cone in three dimensions
is the intersection of two independent bounding planes. Thus its possible
rays are exactly among the two orientations of the cross products of pairs
of normals in (5).

The verifier collects every feasible primitive integer ray of each cone
and sums them. This sum has every signed dot product strictly positive if
and only if the cone is full-dimensional. In one direction this is
immediate. In the other direction, a full-dimensional pointed polyhedral
cone is generated by its extreme rays, and no nonzero defining normal
vanishes on all those rays. Their sum is therefore strictly inside every
defining half-space.

This gives one exact interior vector for every feasible generic direction
sign pattern: **32 vectors** in total. At any arrangement vertex, a local
full-dimensional cell specifies signs only for the planes passing through
that vertex. A generic direction into that cell belongs to one of the
global normal cones just enumerated; the chosen representative has the
same signs on every active plane. Thus these 32 vectors cover every local
cell next to every vertex.

Discard directions that fail to enter the strict interior of D. For each
remaining pair `(v,d)`, substitute

    (a,b,u) = v + epsilon*d,    epsilon -> 0+,

into (3) and the individual capture formulas. Every quantity is affine in
epsilon. Lexicographic comparison of its constant and linear coefficients
selects the exact branch for all sufficiently small positive epsilon.

There are **7392 admissible vertex-direction pairs**. All are evaluated
using `fractions.Fraction`. The largest constant term is

    2641/1600.

It is approached, for example, along

    a=5/8-epsilon,
    b=1/4-2epsilon,
    u=1-5epsilon.

The ray lies in the strict interior of D for sufficiently small positive
epsilon. Its branch is included in the enumeration and its limiting payoff
is the displayed maximum. This proves both inequalities for the exact
restricted supremum.

## 5. A rational princess that exceeds that supremum

Set `delta=1/1000`. Use the following vertices, then remain at the last
height:

| Time | Position |
|---|---|
| `0` | `1/4-delta/3` |
| `1/8` | `3/8-delta/3` |
| `1/2-delta` | `2delta/3` |
| `15/16-delta` | `7/16+2delta/3` |
| `19/16-delta` | `3/16+2delta/3` |
| `2-2delta` | `1-delta/3` |
| `4` | `1-delta/3` |

Its successive nonconstant slopes are `+1,-1,+1,-1,+1`. All heights are
strictly between zero and one, so this is an admissible princess path. It
has two separate inward legs.

An independent exact piecewise-linear intersection calculation gives:

| Monster row | Unreflected capture | Reflected capture |
|---|---:|---:|
| `M1(-1)` | `5999/3000` | `899/1200` |
| `M1(-1/2)` | `703/750` | `599/1200` |
| `M1(5/8)` | `89/75` | `1781/750` |
| `M2(-1/2)` | `11999/3000` | `599/1200` |
| `M1(1/2)` | `1499/1200` | `7499/3000` |
| `M1(1/4)` | `1649/1200` | `8249/3000` |

Multiplying these pairs by the weights in Section 1 and dividing by 200
gives exactly `100559/60000`. Therefore the unrestricted princess response
is at least that value, and strictly greater than the entire wait-in-out
family's supremum by `3043/120000`.

## 6. Reproduction and consequence for the continuum approach

Run

    python packages/interval_wait_in_out_exclusion/verify.py

from the repository root. The verifier constructs the arrangement and its
direction cones afresh, checks all 7392 cases, checks the maximizing
approach direction, independently intersects the displayed witness with
all twelve monster paths, and checks the strict rational gap. It uses only
Python's standard library.

The exact characteristic and potential formulations in the companion
notes remain valid. This counterexample explains why a proposed continuum
solution cannot replace their general monotone-path optimization by the
three-parameter wait-in-out family without an additional theorem about the
specific candidate monster law.
