# Initial curvature at an endpoint-inward contact

The endpoint coalescence identity gives a local curvature test without
assuming positive-M2 indifference or differentiating an exterior CDF
column. It concerns a fixed interior positive-M1 start. It is not an
endpoint asymptotic uniform in that start, and does not assert that the
inward equality region reaches the diagonal.

## 1. Assumptions and the finite comparison

Fix `0<b<1`. Near b, let the ordered positive princess paths be indexed
by their initial position xi. Suppose the initial law has a continuous
density `rho(b)>0`, no atom at b, and uniformly in xi near b,

    p_xi(t)=xi+t-kappa(xi)t^gamma+o(t^gamma),
    gamma>1,    kappa continuous,    kappa(b)>0.

All paths remain nonnegative and have speed at most one. The remainder
is uniform as `(xi,t)->(b,0)`. The lag `t+xi-p_xi(t)` is nondecreasing;
the first inverse therefore has the corresponding regular-variation
asymptotic. The density and kappa may be assumed locally Lipschitz to
make the uniform integrations below immediate.

Write `alpha_xi` and `beta_xi` for the first U and V inverses. Set

    D_b=lim_(xi downarrow b) 2 alpha_xi(2-b).

Ordering makes this one-sided limit exist. The physical endpoint bound
gives `D_b>=2(1-b)>0`; nonnegativity gives a finite upper bound. Its
definition deliberately retains the true post-one first inverse.

Compare positive M1 from b with the endpoint-inward route starting at
`a=b+delta`, first turning at `V=-b`, and then visiting +1 and -1. The
two routes coalesce at time `delta/2`. Only positive paths initially in
`(b,b+delta]` can have different capture times.

The initial position at their first-turn dividing rank is

    xi_0=b+kappa(b)(delta/2)^gamma+o(delta^gamma).

The paths from b to xi_0 miss the new inward prefix and are caught at
`alpha_xi(2-b)`. The remaining initial band is caught by that prefix by
time `delta/2`. In the original positive-M1 route the first capture is

    beta_xi(-b)=((xi-b)/kappa(b))^(1/gamma)(1+o(1)).

For sufficiently small delta this capture lies in the displayed initial
phase. The local inverse estimate is uniform under integration; one can
also sandwich the lag between `(kappa(b) +/- epsilon)t^gamma` before
letting epsilon tend to zero.

Integrating the three contributions proves

    4[CI_end(b+delta,-b)-Cf(b)]
      =rho(b)[D_b kappa(b) delta^gamma/2^gamma
             -2gamma kappa(b)^(-1/gamma)
                    delta^(1+1/gamma)/(gamma+1)]
       +o(delta^gamma+delta^(1+1/gamma)).             (1)

The newly captured upper part of the band contributes `O(delta^2)`.
This is smaller than the leading power in (1), because
`min(gamma,1+1/gamma)<=phi<2`, where `phi=(1+sqrt(5))/2`.
The other ranks cancel exactly by coalescence, so no off-diagonal
derivative hypothesis is needed.

## 2. Consequences and the activity gate

If `gamma>phi`, the negative term in (1) dominates. Hence a sufficiently
short endpoint-inward route is strictly cheaper than Cf(b). Such an
initial germ cannot face an active positive-M1 start in a saddle.

If `1<gamma<phi`, the leading difference is positive. The endpoint
comparison permits an inactive gap next to the diagonal.

If `gamma=phi`, nonnegativity of all sufficiently short comparisons
requires

    kappa(b)^phi >= 2^(phi+1)/(phi D_b).              (2)

If endpoint-inward equality occurs along a sequence `delta->0`, the
leading term must vanish. Then necessarily

    gamma=phi,
    kappa(b)^phi = 2^(phi+1)/(phi D_b).              (3)

Equality of leading terms does not determine the next sign. It does not
prove that an active patch exists.

These statements assume a unit initial tangent. A strictly slower
initial speed can instead create positive first-order endpoint slack.
Neither (1) nor the saved endpoint support permits imposing the golden
power where an inward equality region stays separated from the diagonal.
The constants and the valid local time interval can also vary with b;
no limit as `b->1` is taken here.

## 3. Independent physical fixture

Use the legal `PowerWave` family from `CURVED_INITIAL_POWER_PHASE.md`:
initial xi is uniform on `[1/5,2/5]`,

    p_xi(t)=xi+t-kappa t^gamma,    0<=t<=T0=1/32,
    u(xi)=xi+2T0-kappa T0^gamma,
    c(xi)=c0-xi,                 c0=9/10.

After this first phase the path moves inward to zero, waits until c(xi),
then moves outward to one. The checked parameters obey the speed bound
and the phase order. Fix `b=3/10` and
`delta<kappa T0^gamma`. Put `D=2+c0-2b`.

The exact four-cost difference is

    rho[ D kappa delta^gamma/2^gamma
         -2gamma kappa^(-1/gamma) delta^(1+1/gamma)/(gamma+1)
         +delta^2/2
         -kappa gamma delta^(gamma+1)/((gamma+1)2^gamma)
         -kappa^2 delta^(2gamma)/2^(2gamma+1) ].       (4)

For the newly caught initial band, substitute
`xi-b=delta-2t+kappa t^gamma`. For the missed band use
`2alpha_xi(2-b)=D-(xi-b)`. The original capture time is
`((xi-b)/kappa)^(1/gamma)`. These give (4) directly.

The verifier instead intersects both complete monster routes with the
actual curved/linear princess pieces, takes the first equality, and
integrates those physical capture times. It checks (4), both curvature
signs, the balanced golden coefficient, and the independent cancellation
outside the initial band:

```sh
python -B packages/interval_turn_sheet/verify_endpoint_curved_power.py --quick
```

The quick audit passes 42 comparisons at 45-digit precision. These are
independent numerical checks of an explicit analytic identity, not
rational or interval certificates. The exact coalescence and endpoint
field identities have separate Fraction checks in
`verify_endpoint_inward_comparison.py`.
