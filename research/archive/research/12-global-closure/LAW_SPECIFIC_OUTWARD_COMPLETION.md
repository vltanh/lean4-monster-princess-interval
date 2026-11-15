# Outward completion relative to a supplied Monster law

This is a **fixed-opponent dominance theorem** and a diagnostic for the
retained certificates. It is not a global restriction on maximin Princess
strategies. In particular, improving against an optimal Monster law alone
does not preserve security against Monsters outside its support.

Let `r:[0,infinity)->[0,1]` be a legal radial Princess path, and use the
fair pair `+r,-r`. Let `m` be a legal Monster path. Coincidence, including
at time zero, counts as capture.

## 1. An initial interval protects outward completion

If `|m(0)|<=r(0)`, each still-uncaught reflected target stays on its
assigned outer side of the Monster. Indeed, a positive target starts
weakly above it and a negative target starts weakly below it. Equality
is already capture; changing that order later requires another contact.

For a time `T>=0`, define the maximal outward completion

\[
 r^T(t)=\begin{cases}
 r(t),&t\le T,\\
 \min\{1,r(T)+t-T\},&t\ge T.
 \end{cases}                                                \tag{1}
\]

This is legal and `r^T>=r` after `T`. If the positive target is
uncaught at `T`, then `m(T)<r(T)`. At any later first contact with
`+r^T`, the old positive target lies weakly below the new one.
Continuity therefore gives an old contact no later. The negative
target has the reflected argument. Targets caught before `T` have
unchanged prefixes.

Thus, when the Monster starts in the closed initial interval,

\[
 T(m,+r^T)\ge T(m,+r),\qquad
 T(m,-r^T)\ge T(m,-r).                                     \tag{2}
\]

The same conclusion holds for a Monster starting outside the interval
once its initially adjacent target has already been caught. The other
target started on the opposite outer side and has the preceding
order property throughout.

## 2. A path-dependent exact cutoff

For a supplied Monster path define

\[
 c_m(r)=\begin{cases}
 0,& |m(0)|\le r(0),\\
 T(m,+r),&m(0)>r(0),\\
 T(m,-r),&m(0)<-r(0).
 \end{cases}                                               \tag{3}
\]

For a Monster law `nu`, put

\[
                  T_\nu(r)=\mathop{\rm ess\,sup}_{m\sim\nu}c_m(r).
                                                               \tag{4}
\]

If this is infinite, leave the path unchanged. Otherwise replace it
by (1) with `T=T_nu(r)`. For almost every supported Monster, the
same-side target in (3) was caught by `T`, or the Monster started
inside the initial interval. Section 1 proves (2) for both targets.
For a finite law with positive weights, it holds separately for every
supported route.

This is an actual chronological capture comparison, not an assertion
about a sampled payoff table or a selected clock plane. In particular,
every all-clock lower target for the same fixed Monster bank is
preserved. An arbitrary slack clock plane need not keep its old value.

### Ordered radii remain ordered

If `r<=s` pointwise, then

\[
                          c_m(s)\le c_m(r)                 \tag{5}
\]

for every Monster. A Monster that starts inside the smaller initial
interval also starts inside the larger one. If it starts outside both,
it meets the outer same-side target no later than the inner target,
by continuity and their order. If it lies between the two initial
radii, the outer target's value in (3) is zero. Reflection covers
negative starts.

Consequently `T_nu(s)<=T_nu(r)`. The outer path starts its maximal
outward completion earlier. Before that time the original order
holds; between the two cutoff times the outer completion dominates
its old path; after the later cutoff both paths use the same
order-preserving outward evolution. Thus the completed paths remain
ordered.

Applied rank by rank, the construction gives another legal ordered
Princess law with no smaller payoff against `nu`. First-contact
times are Borel functions of the path pair. Moreover
`{r:T_nu(r)>a}={r:nu(c_m(r)>a)>0}` up to the usual rational-threshold
description, so the cutoff and completion maps are measurable.
Fubini handles null sets that depend on the Princess rank.

The cutoffs are nonincreasing in rank. This does **not** assert that
the actual last inward turn times are nonincreasing: a path might
already have stopped turning before its assigned cutoff. Nor does it
make the construction a universal Princess class independent of `nu`.

## 3. A cutoff depending only on initial radius

Let `tau_0(m)` be the Monster's first center time. A same-side target
in (3) must be captured by that time. Hence the simpler sufficient
cutoff is

\[
 H_\nu(a)=\mathop{\rm ess\,sup}
   \{\tau_0(m): |m(0)|>a\},\qquad \sup\varnothing=0.       \tag{6}
\]

It is nonincreasing in `a`, and

\[
                         T_\nu(r)\le H_\nu(r(0)).          \tag{7}
\]

Forcing each ordered rank outward after (6) therefore has the same
fixed-law dominance and order-preservation properties. The strict
inequality in (6) is intentional: an initial equality has already
captured the adjacent target at time zero.

## 4. Exact implications for the retained n64 Monster certificate

The fixed input is
`packages/interval_clock_grid/upper_n64_physical.json.gz`, with fair
reflection and total integer pair weight `10^12`. It has 703 distinct
physical pairs. Its largest interior initial absolute position is
`63/64`; its only endpoint-start pair is the fastest sweep pair, whose
probability is

\[
                         q=\frac{630441926044}{10^{12}}.
\]

Direct inspection of every route gives the following exact function:

\[
 H_\nu(a)=\begin{cases}
 23/16,&0\le a<9/16,\\
 2-(\lfloor64a\rfloor+1)/64,&9/16\le a<63/64,\\
 1,&63/64\le a<1,\\
 0,&a=1.
 \end{cases}                                               \tag{8}
\]

In particular, against this law all Princess ranks can be outward by
`23/16`, and all ranks initially at least `63/64` can be outward by
one. The current n256 profile has

\[
 G(0,63/64)=\frac{16974237}{20000000}.
\]

Thus the top `3025763/20000000 = 0.15128815` of its conditional radial
mass admits this earlier cutoff against the n64 law. This statement
does not modify the saved n256 strategy or its unrestricted guarantee.

For an initial radius at least `63/64` but below one, the stronger
cutoff (4) is just first contact with the fast incoming sweep
`m(t)=1-t`. Every resulting departure lies on the single front

\[
                         t+r=1.                           \tag{9}
\]

After that departure it moves outward at unit speed and is absorbed
at the endpoint at twice the departure time. For the **full-width
interpolation** of the current n256 nodal profile, representative
exact fast-sweep contact times are

| Conditional radial rank | Contact time | Approximate endpoint absorption time after completion |
|---:|---:|---:|
| `9/10` | `8975837/58066816` | `0.309155474` |
| `19/20` | `952361/12997120` | `0.146549543` |
| `39/40` | `594209/16682112` | `0.071239061` |

These times explain why late oscillations of those ranks are fixed-bank
slack. They do not justify applying the completion to a global lower
certificate without a new unrestricted response analysis. The full-width
view here is also distinct from the saved explicit strategy's narrow
interpolation width `1/512`.

## 5. The endpoint-gap obstruction

The complete boundary calculation is in
`BOUNDARY_LAYER_KERNEL_AND_GAP.md`. For this retained n64 law, it proves the
fixed-law lower bound `M+q/256` and the exact diagnostic

\[
 U-(M+q/256)=\frac{5567}{256000000000000}.
\]

That note also gives the full two-parameter initial-inward contact
kernel, including initial and turn co-location, and shows why repairs
confined strictly inside the old initial gap leave the same obstruction.
The standalone `verify_boundary_layer_kernel.py` independently replays
all 736 supplied calendar plans, the exact cutoff profile (8), and the
boundary-loop payoffs using chronological rational intersections.

This diagnostic concerns the retained n64 Monster law. Neither the outward
completion nor the boundary calculation changes the saved Princess
strategy's unrestricted security guarantee.
