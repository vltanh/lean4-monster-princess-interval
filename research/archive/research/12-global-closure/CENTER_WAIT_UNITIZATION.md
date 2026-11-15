# Replacing every center wait in a symmetric upper law

A center wait, including an intermediate wait, can be replaced by closed
unit-speed excursions without increasing a symmetric monster law's
unrestricted princess-response supremum. This lets the unit-leg upper
oracle use information from the physical response search's waiting rows.
The original waiting rows remain necessary attacks against a specified
lower law with center atoms.

## Replacement and exact coalescence

Suppose a monster route is constant at zero on `[s,s+d]`. For `0<d<=2`,
replace that interval by the triangle with vertices

```
(s,0), (s+d/2,d/2), (s+d,0).
```

For `d>2`, concatenate triangles of duration two and one final triangle
of duration at most two. Each stays in the arena and has speed exactly
one. Outside the original waiting intervals the route is unchanged at
every time. In particular every old segment endpoint and the final route
time are preserved. The construction applies independently to every
center wait, including waits between arbitrary earlier and later legs.

Transform one representative `m` of each reflected pair and pair the
result `m'` with `-m'`. Equivalently, the reflected input `-m` uses
negative excursions. Applying positive excursions independently to both
orientations would not be the reflected-pair construction.

## Global upper comparison

Let `p(t)>0` be any legal princess path. The old monster cannot capture
`p` during a center wait, including at either end of that wait. At every
other time the old and new monsters coincide. Therefore the old first
contact, if finite, is still a contact for the new route, while the new
excursions may add earlier contacts:

```
T(m',p)<=T(m,p),       T(-m',p)<=T(-m,p).             (1)
```

This argument uses the complete unchanged prefix and suffix; it does not
assume that the wait is initial. It also applies to a law with any number
of independently replaced reflected components, leaving the other
components unchanged.

For completeness, the existing strict-positive supremum argument from
`research/10-turn-density/INITIAL_CENTER_WAIT_RESPONSE.md` is recalled.
The universal folding comparison reduces the princess supremum against
a symmetric monster law to nonnegative legal paths. For such a path set
`p_epsilon=(1-epsilon)*p+epsilon`. This stays in `[epsilon,1]`, is legal,
and converges uniformly to `p`. First capture is lower semicontinuous:

```
T(m,p)<=liminf_(epsilon->0) T(m,p_epsilon).
```

Otherwise a convergent sequence of contacts strictly before `T(m,p)`
would give an earlier exact contact by continuity. Fatou's lemma then
shows that the supremum over strictly positive paths equals the full
princess-response supremum for each symmetric monster law.

Apply this equality to both the old and the transformed law and integrate
(1) over their reflected components. The result is

```
sup_p E_(nu_unit) T(m,p) <= sup_p E_nu T(m,p).        (2)
```

Thus the transformed unit-only columns can be priced and certified by the
existing exact upper oracle. This theorem supplies a comparison of global
upper suprema. A transformed column's payoff against a particular lower
field must be recomputed; its old lower-law payoff is not transferable.

## Why the original lower attacks must be retained

Let the original monster wait at zero until `1/2`, then visit `+1` and
`-1`. Let the princess start at `1/4`, move left to zero by time `1/4`,
then stay there. The original reflected monster pair captures at mean
time `1/4`. Replacing the wait by a unit triangle gives capture times
`1/8` and `1/2`, with mean `5/16`. The replacement worsens this particular
attack. Its upper guarantee is nevertheless no worse by (2), because
the unrestricted princess supremum can be taken over paths that avoid
zero strictly.

## Implementation and executed checks

`continuous_response_waits.unitize_center_waits(route,direction=1)` accepts
exact Fraction or rational-string vertices and returns Fraction vertices.
It rejects non-unit moving legs and stationary segments away from zero.
The caller transforms a reflected-pair representative once. The optional
direction parameter makes reflection compatibility explicit.

The converter preserves the original route and original lower payoff as
provenance, without assigning that payoff to the new unit route:

```
python packages/interval_global_closure/continuous_response_waits.py REPORT \
  --output UNIT_REPORT
```

`verify_center_wait_unitization.py` checks initial waits, intermediate
waits, two waits in one route, and a wait longer than two. It uses the
independent exact `first_meeting` routine for both orientations and retains
the center-contact counterexample above. The executed report is
`center_wait_unitization_verification.json`. The finite checks validate
the implementation; the unrestricted comparison follows from (1)–(2).
