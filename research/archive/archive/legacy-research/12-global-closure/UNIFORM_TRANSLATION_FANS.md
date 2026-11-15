# Uniform translation fans over frozen paths

This is a new continuous Princess family and an exact finite-route payoff
oracle. It is not an unrestricted response certificate or a matching game law.
The path and width of a row are immutable when a new Monster is added.

## Physical row and scope

Fix a legal 1-Lipschitz path `p` and a positive width `delta`. Choose `z`
uniformly from `[-delta,delta]`, use `clamp(p(t)+z,-1,1)`, and reflect with
probability one half. Clipping preserves legality. In a germ construction the
fixed width may itself be a specified positive rational function of epsilon;
the new Monster may use a smaller scale, but neither row datum is reselected.

The exact code accepts piecewise affine paths over Q(epsilon), constant tails,
and unit-speed Monster legs. Every comparison contributes to the common
positive specialization radius. An incomplete route is explicitly marked
incomplete. The floating companion applies only to a fixed nonzero limiting
width and is a discovery tool.

Translation generally destroys endpoint absorption: a base path eventually
equal to 1 leaves stationary paths at `1+z` for negative `z`. Old
endpoint-by-two formulas must therefore not be imported. The fan is stationary
after the latest base vertex, but this alone does not justify a fixed
completion horizon: an advantageous static search can visit interior mass
before returning for small remaining tails.

## General intervals and the outward radial version

The exact provider also accepts
`prepareInterval(p,lo,hi,{id,provenance})`, with `hi>lo`.
The original `prepare(p,delta)` remains a convenience for
`[-delta,delta]`. On the negative reflected copy the effective translation
window is `[-hi,-lo]`, not `[lo,hi]`. Each orientation is normalized by
`hi-lo`. The inverse moment formula below is unchanged.

For interior signed x, the pair marginal is

\[
 \frac12\left[
 \operatorname{clip}_{[0,1]}\frac{x-p(t)-lo}{hi-lo}
 +\operatorname{clip}_{[0,1]}\frac{x+p(t)+hi}{hi-lo}
 \right].
\]

Strict and closed endpoint traces retain the same clipping atoms. The exact
verifier covers positive, negative, shifted, symmetric and germ intervals.

For a nonnegative base path the outward choice `[0,delta]` keeps almost
every positive-copy path strictly above the center. It therefore preserves
avoided-center geometry that a symmetric translation can erase. Whenever
the base is at +1 the entire outward fan is at +1; if the base remains
absorbed there, the fan does also. An exact scan of the pinned349 base paths
found no negative vertex and only unit/wait slopes on all68,589 segments.

A safe general radial-density bound is
`2*sum(w_i/(hi_i-lo_i))`; for nonnegative outward fans it improves to
`sum(w_i/delta_i)`. In the uniform-profile comparison below, replace E by
`2*sum(w_i*eta_i/(hi_i-lo_i))` for arbitrary intervals. This reduces to the
stated symmetric formula. The outward ordered marginal admits sharper
bounds, but the conservative general bound is already sufficient for
uniform convergence.

## Exact capture moment

For an orientation `sigma`, symmetry of the translation interval lets us use
`clamp(sigma*p+z)` directly. The captured translation parameters form an interval
`[L,H]` within `[-delta,delta]`. Initially both records equal the clipped value
`m(0)-sigma*p(0)`. If the Monster starts at 1, set `H=delta`; if it starts at
-1, set `L=-delta`. These are clipping atoms caught at time zero.

On a unit leg of direction `d`, the relative value `m-sigma*p` is monotone.
A right leg enlarges the upper record, and a left leg decreases the lower
record. An actual endpoint hit fills the corresponding record to `delta` or
`-delta`. The word actual matters for germ routes: a turn at `1-epsilon` does
not capture the atom clipped to 1.

Put `c=t-d*m(t)`, which is constant on the leg, and

\[
 \phi(t)=t-d\sigma p(t),\qquad q=c+dz.
\]

The first contact of a newly added translation parameter is the generalized
first inverse of `phi` at `q`, capped at the leg end. The cap accounts for a
translation whose clipped path is first met at the endpoint even though the
unclipped characteristic has not reached `q`. The change of variable has
absolute Jacobian one.

At the base vertices `(t_i,p_i)`, write `s_i=t_i-d*sigma*p_i`.
The characteristic is nondecreasing. On a strictly increasing cell its
inverse is affine, and its integral is a trapezoid:

\[
 P_{i+1}-P_i=(s_{i+1}-s_i)(t_i+t_{i+1})/2.
\]

Flat characteristic cells have zero q-length. A right-sided binary search
selects the inverse branch after such a flat; the value at the single
boundary q does not affect the integral. Beyond the last base vertex, the
constant tail gives inverse slope one. For a new band `[q0,q1]` and end time
`T`, the code integrates the inverse up to `phi(T)` and adds `T` times the
remaining q-length. Sum all new bands, divide by `2*delta`, then average the
two orientations.

`germ_translation_fan.cjs` caches both inverse antiderivatives and capped band
moments. It also exposes the exact strict and closed marginal CDF.

## Independent physical check

`verify_translation_fan.mjs` does not use those inverse primitives. It merges
the physical Princess and Monster vertex times and inserts every relative
value `m(t)-sigma*p(t)` as a translation breakpoint. Between consecutive
breakpoints the first-contact time is affine in z. At its midpoint it builds
the actual translated-and-clipped path, including crossings of both clipping
levels, and invokes chronological segment intersection. Multiplying that
first-contact time by the interval length integrates the affine branch
exactly; this is not numerical quadrature.

The preserved replay passes 2,088 exact fan scores on 7,666 independent affine
translation pieces, with 1,181 clipping crossings. The fixtures include
rational-function speeds, isolated bounces, initial overlap, widths larger
than the arena, vanishing widths, and nested germ Monster turns. The 3,915 separate
strict/closed marginal checks retain endpoint atoms.

A small exact countercheck prevents overinterpreting spreading. For the
stationary path `p=1/2` and width `1/64`, the Monster starting at `1/2` and
sweeping left then right costs `321/256`. Moving its initial position to the
upper fan edge `33/64` reduces that cost to `33/64`. A fixed old contact attack
can improve while a new adaptive attack remains strong. For the outward
interval [0,1/64], the same fixed start costs257/128 while the upper-edge
start still costs33/64.

## Exact CDF construction and unrestricted-response route

For interior signed position x, one orientation has marginal

\[
 F_i(t,x)=\operatorname{clip}_{[0,1]}
     \frac{x-p_i(t)+\delta_i}{2\delta_i}.
\]

Average the reflected expression. At -1 the strict CDF is zero; at 1 the
closed CDF is one. The other endpoint traces use the interior formula. These
are the only marginal atoms. Finite fan mixtures therefore have a finite
piecewise affine marginal field on the arrangement of the base time knots
and the lines `p_i(t)+/-delta_i`.

The comonotone quantile coupling of these marginals is a legal symmetric
strategy and improves every Monster payoff over the raw mixture. It is a
separate construction: the pure-row matrix averages in the trial are raw
physical fan payoffs, not ordered-law payoffs. Along a supplied unit Monster
leg the CDF is monotone. Splitting at band crossings makes the ordered score
an exact integral of affine positive-part functions against prior lower and
upper records. Thus finite-route separation and concave weight optimization
need no quantile sampling.

This finite arrangement alone does not prove a finite unrestricted response
algorithm. Arbitrarily many pre-center turns and initial accumulating center
returns still need a Bellman argument. There is, however, no center atom:
`Z(t)=0`. A safe radial density bound is

\[
 C=\sum_i w_i/\delta_i.
\]

Rank q is at radius at least `q/C`. A productive center tent above positive
record n therefore lasts at least `2*n/C`; on a bounded horizon, forward
accumulation after the first positive-record return is impossible. An initial
growing chain at record zero is not excluded. Away from the finitely many
fan-edge/center intersections, the local center cell has the stationary
form `R(t,r)=C_j*r`. These facts are possible inputs to a complete center and
first-prefix potential, not an assertion that those potentials are solved.

## Uniform comparison of nearby base profiles

For a fixed Monster, the same translation-record interval description works
without a unit-leg restriction: use the running minimum and maximum of
`m-sigma*p`, with the same endpoint forcing. If two base profiles differ
uniformly by at most `eta`, each unforced record differs by at most `eta`.
Consequently the probability of capture by any time differs by at most
`eta/delta`. For mixtures set

\[
 E=\sum_i w_i\|p_i-\widetilde p_i\|_\infty/\delta_i.
\]

For a common bounded horizon T the raw fan payoffs differ by at most `T*E`,
uniformly over all Monster paths completed by T. The ordered construction has
the same bound: its signed marginal CDFs differ by at most `E/2`, and their
running lower and upper records give capture-probability error at most E.

There is also a safe unrestricted-value comparison without any asserted
optimal completion horizon. The Monster can always achieve expected time at
most 3 by choosing a nearest endpoint and then the other endpoint. Take a
nearly optimal Monster and replace its continuation after T by an endpoint
tour of length at most 4. Markov's inequality bounds the added expected time
by `12/T`, up to the vanishing near-optimality error. Both laws now face the
same route completed by `T+4`, so their unrestricted values differ by at most

\[
 12/T+(T+4)E.
\]

For `E>0`, choosing `T=sqrt(12/E)` gives
`2*sqrt(12*E)+4*E`. Thus fixed positive fan widths allow uniformly converging
base germ profiles to be replaced by their collapsed profiles as NEW actual
fan rows, with convergent unrestricted values. The argument does not collapse
the Monster or discard its exact endpoint flags. Widths tending to zero do
not give this conclusion unless the displayed E also tends to zero.

## Pinned 349-row trial

The exact trial fixes the archived 349 physical rows and their recorded
constant weights, together with the original clipped159 weights and the
certified169 source weights. It evaluates four widths against six named old
M1/M2 attacks and three separately tagged fan-edge starts. Every pure-row
cost is retained. The common specialization radius is
`1/320000000000000000`; maximum encountered degree is 20.

For the current repaired mixture, width `1/256` raises the tested positive M2
at start `3/16-epsilon`, first U=1, from about 1.41937141 to 1.48704505. The
tested inward M1 at `29/32+epsilon^2` becomes 1.42156524, while the late
negative M2 at start magnitude 3/5 and first U=65/64 becomes 1.42084537.
Increasing the width to `1/64` lowers the latter to 1.41390807. The old159
mixture remains rejected: its inward M1 at 119/128 costs 1.29219763 at width
1/256. These are selected-response diagnostics, not lower bounds.

## Floating packet and endpoint convention

`export_translation_fan_float.mjs` collapses only the Princess profiles, with
exact collinearity removal, and retains each Monster leg direction and its
actual endpoint-hit flag. Zero-duration limiting Monster legs are retained
when they carry such a flag. Correctly rounded rational-to-double conversion
avoids reversing two nearby limiting vertex times through independent
numerator/denominator rounding.

`translation_fan_float.cjs` uses those profiles and flags to score any fixed
positive numeric width. It must not infer a hit from a limiting coordinate
equal to an endpoint. A regression turns at `1-epsilon`, then sweeps left and
right against a clipped endpoint fan: falsely treating the first limiting
turn as an endpoint hit lowers the limiting cost by exactly one. The packet
is crosschecked against all retained exact trial entries at constant widths;
final candidate checks must use the exact scorer again.
