# Initial prefix compression: an exact bound and a front-contact obstruction

This note records a concrete test of an attempted Monster simplification.
It does not disprove a finite optimal support family or claim that the
tested bank row is an exact best response.

## 1. A rigorous suffix-advance estimate

Let a symmetric regular signed CDF be `F`, and let a Monster path complete
its endpoint tour by `H`. Suppose its prefix `[0,tau]` contains no endpoint.
Set

\[
 W=\max_{0\le s\le\tau}F(s,m(s))-
       \min_{0\le s\le\tau}F(s,m(s)).
\]

Delete that prefix, start at `m(tau)` at time zero, and advance the entire
remaining physical path by `tau`. Let

\[
 \omega=\sup_{\tau\le s\le H}
       |F(s-\tau,m(s))-F(s,m(s))|,
\]

using the interior endpoint traces and the same separate endpoint resets
as the exact capture-record formula. If `C_old,C_new` are the actual
expected capture costs, then

\[
 \boxed{C_{\rm new}-C_{\rm old}
       \le-\tau+HW+2(H-\tau)\omega.}                     \tag{1}
\]

Indeed, the original prefix has surviving total record at least `1-W`
throughout, hence cost at least `tau(1-W)`. At its end, the two deficits
between the current CDF and the two old records sum to `W`. On the shifted
suffix, each new running minimum can exceed its corresponding old
minimum by at most that initial deficit plus `omega`. The sum of the
positive increases is therefore at most `W+2omega`, including the interval
after one clock has deactivated. Integrating for at most `H-tau` proves
(1). Both endpoint clocks deactivate at the corresponding shifted
endpoint times, so no endpoint mass is lost from this comparison.

For a returning prefix, its spatial diameter is at most `tau/2`. If the
local spatial and temporal CDF moduli are bounded by `rho` and `M`, then
`W<=rho*tau/2+M*tau`. This controls the *prefix* term. It does not control
the future temporal error `omega`; a later sharp record front can make
that error first order in `tau` with a large coefficient.

## 2. A retained physical route makes the future term material

Use the full-width (`epsilon=1/2`) interpretation of the projected n256
field, file SHA256

`a8e1d84d67e66e08d6d1eeb02f18c6e5121108cb4368ededd9db2e792a97189e`.

Here `epsilon` is dimensionless: this diagnostic reuses the nodal profile
with a different interpolation from the saved explicit Princess strategy,
whose `epsilon=1/512`; the costs below do not evaluate that saved strategy.

The actual unit-speed route is

\[
 (0,0)\to(3/32,3/32)\to(9/32,-3/32)
 \to(11/16,5/16)\to(2,-1)\to(4,1).
\]

It occurs with weight numerator `4737615` over `10^12` in the retained
n128 physical law. Its exact cost on this supplied field is

\[
 C_{\rm old}=\frac{465765360170948783}{327273369600000000}
             \approx1.4231691406490434.
\]

Deleting and advancing its first returning prefix of length `3/16`
**raises** cost by approximately `0.22219977664574286`; deleting `3/8`
raises it by approximately `0.40424001024939404`.

This is not only a long-prefix effect. For removed prefix lengths
`1/256,1/1024,1/4096,1/16384`, the exact differences divided by the
removed length are respectively approximately

`12.8895792905,12.8927637089,12.8935598135,12.8937588396`.

The final interior peak is on `U=1`. Advancing the suffix moves it to
`U=1-tau`, losing a substantial set of record captures at that front.
Thus local initial density and velocity alone cannot justify this
particular compression, even for arbitrarily short removed prefixes.

## 3. Preserving the later front changes the conclusion

Instead replace the first two opposite triangles by the single negative
triangle

\[
          (0,0)\to(3/16,-3/16)\to(3/8,0),
\]

then keep the entire old suffix from time `3/8` unchanged. This preserves
the later `U=1` contact. The new exact whole cost is

\[
 \frac{18215933931}{12800000000},
\]

which is below the old cost by

\[
 \frac{16135326468791}{327273369600000000}
       \approx0.00004930228966845642.
\]

However, the new prefix itself costs *more* by
`70273929/51200000000`. The old center records at `3/8` are

\[
 \left(\frac{8841627}{20000000},
             \frac{47355271}{100000000}\right),
\]

whereas the compressed prefix leaves

\[
 \left(\frac{88095047}{200000000},\frac12\right).
\]

Their total is larger by `993647/40000000`. Thus the usual sufficient
comparison for **every** symmetric increasing concave continuation does
not apply. The gain uses the actual continuation's unequal sensitivity
to the two records. Expanding the positive triangle instead, with the
same unchanged suffix, raises cost by about `0.0927527091284759`.

The exact rational values and additional row checks are saved in
`early_return_prefix_deletion.json`. They were computed by chronological
affine-interval integration using `Field` from
`build_endpoint_tail_charts.py` and `integrate_path` from
`replay_center_renewal_paths.py`; no grid response search or approximate
capture evaluator is used. This is a fixed-field diagnostic. A global
turn reduction still needs a condition on the central phase or on the
actual continuation sensitivities.
