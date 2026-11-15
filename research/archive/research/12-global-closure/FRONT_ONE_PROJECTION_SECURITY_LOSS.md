# Direct front-one completion can strictly lower Princess security

This is an exact counterexample to the assertion that completing every
Princess rank maximally outward at its first contact with `t+|x|=1`
always preserves security. The source law is symmetric, ordered,
sticky at the endpoints, and already absorbed at the endpoints by time
two. Its six deterministic target paths and their probabilities are
specified below.

The exact source and projected securities, with the Monster's initial
position free and all legal Monster paths allowed, are

\[
 S(\mu)=\frac{47}{40},\qquad
 S(P_1\mu)=\frac{469}{400},\qquad
 S(\mu)-S(P_1\mu)=\frac1{400}>0.
\tag{1}
\]

These numbers are below the game's certified lower bound. Thus (1)
does **not** disprove value-level sufficiency of the entire front-one
Princess class, or a preservation theorem with a sufficiently high
security hypothesis. It rules out a universal projection theorem and
shows that the late-center exception in the incoming-front argument
can cause a strict loss after optimizing over every free-start response.
Section 6 extends the strict-loss conclusion to some regular laws with
bounded interior density, without claiming exact securities or an
explicit smoothing threshold for those laws.

## 1. An ordered, completely specified source law

Choose one of three radial paths with probabilities

\[
                  (w_1,w_2,w_3)=\left(\frac1{10},
                                     \frac7{10},\frac15\right),
\tag{2}
\]

then choose an independent fair sign. Each radial path is the linear
interpolation of the following time-position vertices, followed by a
stationary endpoint suffix:

| Path | Vertices `(time,radius)` |
|---|---|
| `r_1` | `(0,1/20)`, `(21/20,1/20)`, `(2,1)` |
| `r_2` | `(0,4/5)`, `(13/20,3/20)`, `(17/20,3/20)`, `(17/10,1)` |
| `r_3` | `(0,19/20)`, `(1/20,19/20)`, `(1/10,1)` |

All speeds are in `{-1,0,1}`. One has `r_1<=r_2<=r_3` at every
time: it suffices to check the finite union of the displayed knots,
because each difference is affine between consecutive knots. All
three paths reach and stay at the positive endpoint by time two.

Their first contacts with `t+r=1` are respectively

\[
                 T_1=\frac{19}{20},\qquad
                 T_2=\frac{17}{20},\qquad T_3=\frac1{20}.
\tag{3}
\]

The second and third paths already move maximally outward from their
first front contacts. Therefore `P_1` changes only the first path:

\[
 P_1r_1:
 (0,1/20)\longrightarrow(19/20,1/20)
                   \longrightarrow(19/10,1),
\tag{4}
\]

again followed by its stationary endpoint suffix. Both laws are legal
symmetric ordered laws. Neither uses a center atom, but each has finitely
many initial positions and atomic interior marginals.

## 2. The same late-center route attains both values

Let the Monster start at `4/5`, move directly to the positive endpoint,
then sweep directly to the negative endpoint:

\[
 m:\quad (0,4/5)\longrightarrow(1/5,1)
                              \longrightarrow(11/5,-1).
\tag{5}
\]

Its first center time is `6/5>1`. Its exact first captures are:

| Target | Source capture | Projected capture |
|---|---:|---:|
| `+r_1` | `11/10` | `21/20` |
| `-r_1` | `11/5` | `11/5` |
| `+r_2` | `0` | `0` |
| `-r_2` | `11/5` | `11/5` |
| `+r_3` | `1/5` | `1/5` |
| `-r_3` | `11/5` | `11/5` |

For example, the descending Monster leg is `m(t)=6/5-t`. It meets
the source inner positive path `r_1(t)=t-1` at `t=11/10`. After
projection that Princess leg is `r_1(t)=t-9/10`, so the contact
advances to `21/20`. Its probability is `w_1/2=1/20`; this one
advance saves exactly `(1/20)(1/20)=1/400` for the Monster.

The three fair-pair costs of (5) are

\[
 \left(\frac{33}{20},\frac{11}{10},\frac65\right)
 \quad\hbox{and}\quad
 \left(\frac{13}{8},\frac{11}{10},\frac65\right),
\]

respectively. Weighting by (2) gives the two quantities in (1).
This alone gives upper bounds on the two securities. The finite
exhaustion below proves the matching lower bounds against all
legal Monster paths.

## 3. Complete finite exhaustion for finitely many moving targets

The following reduction applies to any finite collection of legal
deterministic target paths `p_i` with positive weights. For this fixture
every target eventually stays at an endpoint, so all the required
contacts can be made in finite time.

For each permutation `i_1,...,i_N`, start the Monster at `p_{i_1}(0)`.
From its current state, pursue the next listed target at its earliest
reachable contact time. Record those planned contact times `s_i`,
and sum `sum_i w_i s_i`. A straight unit-speed pursuit realizes each
earliest contact in one spatial dimension; a zero-time contact requires
no movement.

**Finite-target exhaustion lemma.** The minimum of these planned sums
over all permutations equals the unrestricted free-start physical
capture value. Incidental earlier captures need not be subtracted
inside each planned sum.

To prove the lower-bound direction, take any finite-cost physical
Monster path and order the targets by their actual first capture times
`t_i`, breaking ties arbitrarily. For the first target, the greedy
construction has contact time zero. Inductively, suppose its previous
planned contact with target `i` is at `s_i<=t_i`. From that state it
can follow the legal target path `p_i` until time `t_i`, then follow
the original Monster to its next capture. This is an admissible route
to the next target by its original capture time. The greedy earliest
contact is therefore no later. All planned times for this order are
at most their physical counterparts. The minimum planned sum is
consequently at most the cost of every physical response.

Conversely, concatenate the straight earliest pursuits for any order.
This is a legal physical path. Every target is captured by its planned
time, and incidental captures can only improve the actual payoff.
Hence the physical infimum is at most every planned sum. The two
inequalities prove equality. Infinite-cost physical paths cannot
improve a finite-cost competitor and need no separate enumeration.

This also proves that it suffices to use a target's initial position
as the free start. It does not assert the corresponding restriction
for a law with a continuum of target paths.

## 4. Exact arithmetic replay

The standard-library script
`verify_front_one_projection_counterexample.py` enumerates all `6!=720`
orders for each law using Python `Fraction`. It validates legality,
radial order, fair weights, and the exact first-front completion before
pricing any route.

On a target segment `p(t)=v t+b`, earliest reachability from `(s,x)`
is found by solving the two rational light-cone equations

\[
                     p(t)-x=\pm(t-s).
\]

The sticky final segment guarantees a solution. No sampled time grid,
floating tolerance, branch pruning, or fitted lower bound is used.
As an independent attainment check, the script intersects (5) directly
with each affine target segment in chronological order; it does not
reuse the pursuit-cone routine for those first-hit times.

The exhaustive minima, grouped by the positive initial target, are:

| Initial position | Source | Projected |
|---|---:|---:|
| `1/20` | `43/32` | `43/32` |
| `4/5` | `47/40` | `469/400` |
| `19/20` | `501/400` | `13/10` |

Reflection supplies the identical three minima at negative starts.
The finite-target lemma makes this an exhaustive all-path calculation,
not just a comparison of the displayed routes.

Run from the repository root:

```bash
python packages/interval_global_closure/verify_front_one_projection_counterexample.py --output /tmp/front_one_projection_counterexample_replay.json
```

The receipt binds the checker source by SHA256, includes the complete
source and projected paths, lists both `720`-order minima and the
independently reconstructed capture times, and records the exact
security loss `1/400`.

## 5. Consequence for the front-one question

The incoming-front theorem already protects every fixed Monster path
whose first center visit is by time one. Route (5) lies outside that
protected class, and this example shows that optimizing over all free
starts does not automatically remove the loss.

Therefore a globally sufficient front-one Princess class cannot be
justified by claiming that the direct projection `P_1` preserves every
source security. A value-level proof would need an additional
optimality argument, a high-security hypothesis with an effective
threshold, or a different replacement of the Princess law.
The counterexample does not decide whether such a proof exists.

## 6. The loss persists for some bounded-density regular laws

The preceding exact computation concerns six deterministic targets.
There is also an analytic existence extension showing that its strict
loss is not solely an artifact of atomic interior marginals.

For `0<delta<1/20`, independently sample `Z` uniformly on `[0,1]`
after selecting a radial component, and replace that radial path by

\[
       r_{i,\delta,Z}(t)=\min\{1,r_i(t)+\delta Z\}.
\tag{6}
\]

Retain the component weights (2) and a fair sign, and call this law
`mu_delta`. Each path is legal and sticky. For this particular fixture,
the three radial bands retain their order until absorption at one;
within a band, `Z` orders the paths. Every path is at its endpoint
by time two. The interior marginals have densities bounded by
`1/(2delta)` in signed spatial coordinates. Their CDF is jointly
continuous in the interior, with no center atom; physical endpoint
atoms remain permitted. Thus these are regular ordered laws of the
type used in the incoming-front completion theorem.

### A common compact Monster class

The displayed route (5) has source cost

\[
              J(m,\mu_\delta)=\frac{47}{40}
                                           +\frac{3\delta}{40}
                                  <\frac32.
\tag{7}
\]

This explicit competitor, rather than an assumed security theorem,
justifies discarding routes whose first center visit is after time two.
Such a route has kept one strict sign through time two. The opposite
fair half is uncaught and is already at its endpoint; that endpoint
cannot be reached before `3+|m(2)|`. Its cost is consequently greater
than `3/2`.

For a remaining route, retain its prefix through time two. All targets
are now stationary endpoints. Replace its suffix by a direct visit to
the two endpoints in the old order of their next visits; if only one
endpoint has uncaught mass, visit that endpoint first. This catches
every survivor no later. Unnecessary zero-cost visits can be appended
so that both endpoints are visited after time two and by time six.
The total tour length from any current position is at most four.

It follows that every source law `mu_delta`, and also `mu_0=mu`, has
the same security when Monsters are restricted to the common class
`K` of 1-Lipschitz paths on `[0,6]` which visit the center by time two
and visit both endpoints during `[2,6]`. This class is compact: the
speed and position bounds give equicontinuity, and all three hitting
requirements are closed under uniform convergence. All six-target
and smoothed-law captures in this class occur by time six.

Couple the source laws with the same component, sign, and `Z`.
Their target paths converge uniformly to the atomic source as
`delta` tends to zero. Along a sequence realizing the lower limit
of their securities, choose near-minimizing Monsters in `K` and
pass to a uniformly convergent subsequence. Joint lower
semicontinuity of physical first capture, followed by Fatou's lemma,
gives

\[
 \frac{47}{40}=S(\mu)
       \le J(m_*,\mu)
       \le\liminf_{\delta\downarrow0}S(\mu_\delta).
\tag{8}
\]

This is a lower-limit statement for the source security. No continuity
or attained value for a continuum of initial ranks is inferred from
the finite-target enumeration.

### A projected attack with a strictly lower limit

Write `z=delta Z`. Against route (5), the source middle positive target
is captured at `z/2`, the source inner positive target at `11/10-z/2`,
the outer positive target at `1/5`, and all three negative targets at
`11/5`. Averaging these first hits gives (7).

Under front-one completion, the inner positive target is instead
captured at `21/20-z`. The middle positive target is still captured
at `z/2`, before its front contact; the other four captures remain
unchanged. Therefore

\[
 S(P_1\mu_\delta)
 \le J(m,P_1\mu_\delta)
        =\frac{469}{400}+\frac{\delta}{16}.
\tag{9}
\]

The limits in (8)--(9) are separated by `1/400`. Hence, for every
sufficiently small positive `delta`,

\[
                       S(P_1\mu_\delta)<S(\mu_\delta).
\tag{10}
\]

The permitted security-loss threshold for `delta` is existential;
this argument does not provide a numerical threshold or exact values
of either smoothed security. The checker and receipt in Section 4
certify only the original six-target computation. The compactness
argument supplies this regularity corollary analytically.

These regular counterexamples still have low security, as (7) shows.
They refute universal direct-projection preservation even within the
regular class, but do not refute front-one sufficiency at the game
value or a theorem restricted to sufficiently high-security laws.
