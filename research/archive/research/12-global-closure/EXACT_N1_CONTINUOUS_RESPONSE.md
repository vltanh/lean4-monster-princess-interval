# Exact continuous response to the n=1 full-width Princess field

## 1. Result and scope

Let `F` be the symmetric ordered Princess CDF in
`packages/interval_clock_grid/grid_n1_princess.json`, using full-width
common-threshold interpolation (`epsilon=1/2`) and its prescribed sticky,
outward-after-two continuation. This is a supplied test strategy, not an
asserted equilibrium of the unrestricted game.

The exact security of this Princess strategy, against every legal
Monster path and with the Monster's initial position free, is

\[
                         S(F)=\frac{39}{32}.
\tag{1}
\]

There is a stronger statewise conclusion. For a fixed initial Monster
position `x`, put `z=|x|`. Its exact best-response cost is

\[
 V_F(z)=
 \begin{cases}
 \displaystyle\frac{79}{64}+\frac z{32}-\frac{15z^2}{448},
       &0\le z\le\frac78,\\[4pt]
 \displaystyle\frac{37}{64}+\frac{49z}{32}-\frac{57z^2}{64},
       &\frac78\le z\le1.
 \end{cases}
\tag{2}
\]

For every `z`, the following physical path attains (2): start at `z`,
move right at unit speed until time `(1-z)/2` and position `(1+z)/2`,
move left at unit speed to `-1` at time `2`, then move right at unit speed
to `+1` at time `4`. Reflect the path for a negative initial position.
Zero-length legs may be removed. At `z=1`, the first sweep already
captures all ranks, so the last leg is immaterial.

Equation (1) is a complete continuous fixed-strategy response result.
It is not a new lower bound on the unrestricted game near its current
best bounds. Its purpose is to exercise the finite response reduction
with off-grid initial positions, off-grid record crossings, physical
boundary cells, and an independently checked continuous continuation.

## 2. The supplied field and an explicit attaining response

The radial nodal values before time two are, in coordinates
`(t,r)=(j,k)/2`,

| `(j,k)` | Radial CDF |
|---|---:|
| `(0,2)` | `1` |
| `(1,1)` | `7/8` |
| `(2,2)` | `1` |
| `(3,1)` | `0` |
| `(4,2)` | `1` |

The center radial value is zero. The signed initial CDF is
`F(0,x)=(1+x)/2` for `-1<=x<=1`. Endpoint interior traces and the
post-two field are the normalized ones specified by the source artifact.
The checker validates all these nodes and the legal field constructor;
it does not inherit an unverified numerical CDF.

For example, along the descending endpoint sweep `m(t)=1-t`,

\[
 F(t,1-t)=
 \begin{cases}
 1-t/8,&0\le t\le1/2,\\
 11/8-7t/8,&1/2\le t\le1,\\
 1/2,&1\le t\le3/2,\\
 2-t,&3/2\le t\le2.
 \end{cases}
\tag{3}
\]

This is nonincreasing. The initial upper record is already one, so its
capture cost is the integral of (3):

\[
              \frac{31}{64}+\frac{23}{64}
               +\frac{16}{64}+\frac8{64}=\frac{39}{32}.
\tag{4}
\]

For the three-leg family in Section 1, write
`T=(1-z)/2`, `L=(1+z)/2`, and `R'=(1-z)/16`. Its outward leg costs
`T-7T^2/16`; its remaining upper-survivor cost is `R'(4-T)`; its
remaining lower-survivor cost is

\[
             \int_T^2\min\{L,F(t,1-t)\}\,dt.
\tag{5}
\]

The first lower-record crossing is at `1-4z/7` for `z<=7/8`, and at
`4(1-z)` for `z>=7/8`. Integrating (5) gives exactly (2). This proves
attainability. The finite exhaustion below proves that no other legal
path improves it.

## 3. Normalization and the precenter domain

Write `L` for the running lower CDF record and `R=1-H` for the running
upper-survivor record, with actual endpoint capture resets. The remaining
capture-time integral is the integral of `L+R`. Before a first center
visit from a nonnegative start,

\[
               \frac12\le L\le F(t,x),\qquad
               0\le R\le1-F(t,x).
\tag{6}
\]

A path that has not visited the center by time two costs strictly more
than `3/2`: the opposite fair half is uncaught and, after outward forcing,
cannot be captured before the opposite endpoint, whose time is greater
than three. The explicit attaining family in Section 2 costs at most
`149/120<3/2` for every fixed initial position: the first polynomial in
(2) has its maximum at `z=7/15`, and the second decreases on its stated
interval. Thus late-center paths cannot improve even with the initial
position fixed. The center-by-two reduction applies to both (1) and (2).
It is not assumed for arbitrary intermediate states.

Before the first center visit, use light coordinates

\[
                         U=t+x,\qquad W=t-x.
\]

They are nondecreasing for every legal Monster path. A positive-side path
that will reach the center by two satisfies `U<=2`. It remains in the
quadrilateral with vertices

\[
                   (0,0),\ (1,-1),\ (2,0),\ (2,2).
\]

Stop the precenter calculation at its first center visit, its first
positive endpoint visit, or the line `U=2`. On `U=2`, reaching the center
by two forces a direct unit-speed left suffix. First endpoint visits are
followed by the exact direct opposite sweep. These are exact
continuations for this normalized field.

The quadrilateral has the following six affine pieces; this is the full
precenter geometry, including its physical boundary:

| Cell | Vertices in `(U,W)` | Signed CDF `F` |
|---|---|---|
| A | `(0,0),(1,-1),(1,0)` | `1/2+7U/16-W/16` |
| B | `(0,0),(1,0),(1,1)` | `1/2+7U/16-7W/16` |
| C | `(1,-1),(1,0),(2,0)` | `7/8+U/16-W/16` |
| D | `(1,0),(1,1),(2,0)` | `7/8+U/16-7W/16` |
| E | `(1,1),(2,0),(2,1)` | `1-W/2` |
| F | `(1,1),(2,1),(2,2)` | `1/2` |

These formulas follow directly from full-width common-threshold
interpolation of the five nodes. The generator additionally checks them
at every triangle vertex, edge midpoint, and barycenter against the
independent raw-field evaluator. Every start, turn, and exit used by the
algebraic generator is constrained to its actual triangle. This last
condition is essential: an affine extension outside its cell is not the
same Princess strategy.

## 4. Complete local path classes

For a fixed entry and exit in A, D, or E, their coordinatewise box lies
inside the same affine cell. The two-run affine-cell theorem, applied
with the entire fixed optimal later continuation, permits one of the two
orders `U then W` or `W then U`. Its hypotheses hold because the exact
future response cost is a concave, nondecreasing function of the two
incoming survivor records. Each fixed physical continuation has that
property, and an infimum of such functions retains it.

There is a small center-boundary issue for B and F. Their positive halves
have a center diagonal, but the full centered square has the same affine
field. Apply the two-run theorem on this full square. If its selected
replacement reaches the center early, stop at that first center contact
and replace the whole remaining path by the exact center value. This
cannot increase cost. Such an early contact is reached by the initial
unit-left leg and is already one of the center exits enumerated below.
Consequently the generator may enforce `x>=0` on its retained two-run
pieces without excluding a best response. F is constant, so the same
argument also covers its zero-slope case without any division by zero.

Cell C has the physical endpoint boundary `x=1`. Here
`F=7/8+x/8` is stationary and strictly increasing in position. Use the
four-leg affine record-preserving theorem: every segment can be replaced
by at most four alternating unit-speed legs and a final constant-field
hold, with the same entry, exit, duration, and both exit records, and no
greater cost. The scalar record range is attained by the old legal path,
so preserving it keeps the replacement below `x=1`. The other two cell
edges are coordinate bounds and are preserved by monotone light
coordinates. A constant-field hold here is a stationary physical hold.

The generator enumerates both initial directions, all four alternating
legs with zero durations allowed, and every record-crossing pattern. It
imposes the cell and arena inequalities on every turn and exit. Thus it
includes every needed C replacement and no physically illegal path.
Every leg duration is at most one because the entire cell has time span
at most one.

The cited two-run and four-leg theorems include arbitrary Lipschitz paths,
not only finite words. Monotonicity of `U,W` means each cell is visited
only once, except harmless movement on shared faces. Closed-face branches
may duplicate a path, which is harmless. Actual center and endpoint exits
have their separate exact continuations. As in the center calculation,
a nominal closed branch that touches an endpoint earlier can only
overestimate its actual capture cost, never create a spurious lower
cost; the actual first-contact branch is included.

## 5. Exact terminal data and the directed edge calculation

Each edge is parameterized by `z`; its envelope variables are `(z,L,R)`.
The initial edge uses the same letter `z` as the initial position.
Intermediate precenter envelopes are **center-by-two constrained
continuations**. The center and endpoint exits have the separately proved
exact unrestricted continuations. In particular, the forced deadline
suffix is not asserted to be unrestricted optimal from every abstract
incoming record state; the preceding fixed-start comparison is what
licenses this constraint for the full initial problem.

| Edge | `(U,W)` | Parameter interval |
|---|---|---|
| center | `(z,z)` | `[0,2]` |
| endpoint | `(z,z-2)` | `[1,2]` |
| deadline | `(2,z)` | `[0,2]` |
| flat entry | `(z,1)` | `[1,2]` |
| time one | `(z,2-z)` | `[1,2]` |
| D left | `(1,z)` | `[0,1]` |
| D bottom | `(z,0)` | `[1,2]` |
| B bottom | `(z,0)` | `[0,1]` |
| C left | `(1,z)` | `[-1,0]` |
| initial | `(z,-z)` | `[0,1]` |

The center data are the complete depth-five n1 envelope from
`EXACT_CENTER_ENVELOPE_N1.md`, restricted to `L=1/2`. The first-endpoint
data are the independently constructed exact tail charts `B(z-1,L)`.
The endpoint trace in this time interval equals one, hence `R=0` there.

On the deadline edge, the forced left motion reaches the center at time
two, where the optimal tour costs `1/2+3R`. For `z<=1`, its prefix cost is

\[
 (L+R)\frac{1-z}{2}-\frac{(L-1/2)^2}{2}
                         +\frac{1/2+R}{2}.
\tag{7}
\]

For `z>=1`, `L=1/2` and the prefix cost is
`(L+R)(2-z)/2`. Thus all three terminal edge envelopes are exact.

Compute the remaining edges backwards in this order:

| Entry edge | Cell | All possible next edges |
|---|---|---|
| flat entry | F | center, deadline |
| time one | E | flat entry, deadline |
| D left | D | time one |
| D bottom | D | time one |
| B bottom | B | center, D left |
| C left | C | D bottom, endpoint |
| initial | A | C left, B bottom |

This is the complete successor list because `U,W` are nondecreasing and
the only other sides are entry sides. Shared vertices may be assigned to
either adjacent branch. Backward induction, Section 4, and the exact
terminal data therefore give the true center-by-two constrained envelope on every
precenter entry edge.
In particular, this is a completeness argument for all legal paths, not
an inference from the paths reconstructed at sample states.

## 6. Finite rational calculation and sound pruning

On a unit leg of duration `d`, precisely one CDF record can decrease. Let
its old value be `r`, its final field threshold be `p`, and its positive
constant decrease rate be `a`. There are two closed linear cases:

\[
 \begin{array}{ll}
 r\le p:&\text{cost }d(L+R),\quad\text{record unchanged},\\
 r\ge p:&\text{cost }d(L+R)-(r-p)^2/(2a),\quad\text{record becomes }p.
 \end{array}
\tag{8}
\]

Zero rates are treated as constant records. Thus each finite record word
has a rational quadratic cost and rational linear feasibility conditions.
An ordinary cell has one free exit parameter. The C cell has its exit
parameter and the first three leg durations; the fourth duration is
fixed by displacement, and the remaining duration is a stationary hold.
Successively applying `eliminate_quadratic_interval.py` eliminates those
four scalar choices exactly. Boundary choices and, for a positive
quadratic coefficient, the stationary choice exhaust every compact
one-dimensional fiber.

The generator uses only exact Fraction/integer arithmetic. An interval
propagation filter discards a candidate only after proving a linear
constraint impossible on its enclosing box. Its final three-dimensional
domains are bounded by their edge interval and the record constraints.
Their exact vertices, including lower-dimensional domains, are therefore
complete. The inherited center-envelope pruning removes a piece only if
its whole polytope is contained in that of a competing piece and every
quadratic polar coefficient of the cost difference on its vertices is
nonnegative. Those are sufficient exact inequalities over the entire
domain. No sampled dominance or floating tolerance is used.

The resulting retained counts are:

| Edge | Retained quadratic pieces |
|---|---:|
| center | 5 |
| endpoint | 3 |
| deadline | 2 |
| flat entry | 1 |
| time one | 1 |
| D left | 1 |
| D bottom | 4 |
| B bottom | 5 |
| C left | 13 |
| initial | 28 |

For the initial edge substitute
`(z,L,R)=(z,(1+z)/2,(1-z)/2)`. Eighteen saved candidates meet this initial
curve. Exact one-variable quadratic minimization proves their minimum
is `39/32`. The independent replay goes further: 29 exact full-interval
comparisons show every eligible candidate lies above the appropriate
polynomial in (2), while one feasible candidate equals each polynomial
throughout its entire displayed interval. This proves (2) without a
sampling argument.

## 7. Portable certificate and independent replay

The implementation files are intended to live beside the existing
`record_bellman` modules:

- `exact_n1_precenter.py`: source binding, complete backward generation,
  exact elimination/pruning, and deterministic regeneration.
- `replay_n1_precenter.py`: independent initial-curve exhaustion and
  chronological integration against the raw common-threshold field.
- `n1_precenter_complete.json.gz`: retained envelopes, exact route
  provenance, and hashes of every generated candidate/pruning history.
- `n1_precenter_replay.json`: independent replay receipt.
- `n1_precenter_regeneration_replay.json`: complete regeneration receipt.

The generator binds decompressed SHA256 values for the actual Princess
field, center charts, endpoint charts, and center envelope. These are
input identity checks. Their semantic validity comes from regenerating
the two chart files from the actual field and regenerating the complete
center envelope, as already specified in the center certificate.

After those prerequisites, regenerate and compare the entire precenter
calculation with:

```sh
python exact_n1_precenter.py \
  --field ../../interval_clock_grid/grid_n1_princess.json \
  --center center_envelope_n1_exact.json.gz \
  --center-charts center_excursion_n1_fullwidth.json.gz \
  --tail endpoint_tail_n1_fullwidth.json \
  --output n1_precenter_complete.json.gz --complete --verify

python replay_n1_precenter.py \
  n1_precenter_complete.json.gz center_envelope_n1_exact.json.gz \
  ../../interval_clock_grid/grid_n1_princess.json n1_precenter_replay.json
```

The physical replay reconstructs minimizing paths using saved affine
decisions. It splits their raw-field integrals at all characteristic,
threshold-order, record, and time-two seams, and applies actual endpoint
resets. It checks 67 initial positions, including every exact initial
quadratic endpoint/stationary minimum and a rational mesh, and 97 edge
states chosen from every retained-domain vertex and barycenter. The
simple three-leg attaining family is integrated independently as well.
These route checks verify the cost/physical interpretation; the
normal-form proof, exhaustive successor graph, and complete exact
regeneration supply coverage over the continuum.

No conclusion about an exact global equilibrium follows from this test
field. It is an operational, exact fixed-field instance of the proved
finite continuous-response reduction.
