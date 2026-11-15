# Initial center waits in the global response cut

This extends the finite atomic response engine to a monster that waits at the
center for a specified time and then follows finitely many unit-speed legs.
It does not approximate a wait by increasingly many excursions. It is not an
extension to arbitrary waits away from the center.

## Response supremum and positivity

Let the monster law be a finite symmetric probability law, and use the existing
folding theorem to consider nonnegative princess paths. For any such legal
path `p`, set

\[
p_\delta(t)=(1-\delta)p(t)+\delta,\qquad 0<\delta<1.
\]

This path is legal, strictly positive, and converges uniformly to `p` on every
compact time interval. First contact with a fixed continuous monster path is
lower semicontinuous under this convergence: if `T<T(m,p)`, the continuous
nonzero difference on `[0,T]` has a positive minimum absolute value. Hence
`T(m,p_delta)>T` for sufficiently small `delta`. Fatou's inequality gives

\[
J_\nu(p)\le\liminf_{\delta\downarrow0}J_\nu(p_\delta).
\]

Therefore restricting the response **supremum** to strictly positive radial
paths loses no value. This is not a pointwise assertion about a lower princess
law that puts mass at the center. Waiting can capture that mass, and such
lower-law costs must still be evaluated by physical first contact.

## Exact continuation rule

Consider an atom that stays at zero until `w`, then follows a unit-speed route
`m` beginning at `(t,x)=(w,0)`. A strictly positive princess survives the whole
wait against both reflected copies. At the end of the wait it is above each
monster. Thus its paired cost has deterministic elapsed part `w`, followed by
only the **above-survival** contribution from the continuation.

In light coordinates, the continuation begins at `(U,V)=(w,w)`. The cut's
four-score compiler must:

1. add the unconditional constant `4w`;
2. initialize `above = true` for each reflected continuation;
3. omit the below-survival record entirely;
4. retain every subsequent physical endpoint/turn predicate.

In particular, the initial above record remains true on a limiting trace with
`P(w)=w`. That trace is approached through strictly positive paths; treating it
as an actual contact at time `w` would erase the waiting response.

Every remaining horizontal or vertical unit leg has the same positive AND
survival rewards as in the unit-route engine. Only its initial record changes.
The common-event realization and maximum-closure argument therefore apply to
a mixture of ordinary unit routes and these center-wait atoms. For an actual
physical response, use the same common epsilon for all atoms and retain the
strict positivity perturbation.

## Implementation and independent checks

`center_wait_survival.cjs` exports:

```javascript
atom(rationalTimePositionVertices, source)
Model(atoms)
restore(shape, atoms)
sparseSolve(model, weights, retainFace)
physical(atom)
```

The serialized wait atom retains its actual physical route, its wait time, and
the continuation light-coordinate vertices. It is explicitly labelled
`initial_center_wait`. The adapter never passes the diagonal wait segment to
the unit-leg compiler.

Run:

```bash
node verify_center_wait.cjs
```

The current verifier passes 896 exact rational reward/first-capture identities
and 147 independent physical segment-capture checks. It includes four waiting
geometries, the dyadic round-one waiting witness, and three ordinary route
atoms. An integer-capacity max-flow certificate for a mixed seven-atom fixture
gives exactly `22177/10240`; a single explicitly legal common-epsilon path has
the same numerical score. Random side-zero trace faces are checked with the
correct one-sided inequality: strictification may avoid an exact contact and
gain payoff. No assertion of attained lower-law equality is made for those
limiting faces.

## Scope of using a replacement prefix

Replacing an initial center wait by a suitable unit-speed trip to the center
can dominate the wait against strictly positive princess paths. That is useful
at the response-supremum level when the replacement route is in the permitted
monster library. It does not preserve the wait's cost against a supplied
lower-law CDF with center mass. The present adapter keeps actual wait atoms and
their physical scores distinct from their replacements and from small-lobe
approximations.
