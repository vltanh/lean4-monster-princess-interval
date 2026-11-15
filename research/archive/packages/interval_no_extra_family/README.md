# Exact response test for the inward-then-outward princess family

**This test did not exclude the candidate family or close the interval game.**
It establishes a response ceiling only for the pure paths

```text
p_(a,c)(t)=min(1,max(a-t,t-c,0)),
0<=a<=1,   -a<=c<=1,
```

and their reflections and arbitrary probability mixtures. The exact checked
ceiling is

```text
182103823/128000000 = 1.4226861171875.
```

This exceeds the existing unrestricted lower guarantee
`36290299773897097/25600000000000000`. Therefore the test does not decide
whether this two-parameter family can reach that guarantee. No matching
princess lower strategy is asserted.

## The finite certificate

`response_ceiling.json` specifies 25 symmetric monster pairs with rational
weights. Each displayed path is chosen with probability one half within its
pair; its reflection receives the other half. The pair types are:

* `M1(x)`: `(0,x) -> (1-x,1) -> (3-x,-1)`.
* `M2(x)`: `(0,x) -> ((1-x)/2,(1+x)/2) -> (2,-1) -> (4,1)`.
* `early_turn(s)`: `(0,0) -> (s/2,s/2) -> (s+1,-1) -> (s+3,1)`.

Only `s=7/8` and `s=15/16` occur in the last type. The discovery search also
included center waits, initial sweeps followed by center waits, and one or
two zero-return triangles. Its positive-weight return paths simplified to
the two ordinary single-turn paths above. Two successive returns did not
improve that fixed finite optimization.

The weights have denominator dividing one million. They were rounded from
the floating LP and then checked exactly; the certificate does not rely on
floating feasibility tolerances or on the LP solver's optimality claim.

Run:

```text
python -B packages/interval_no_extra_family/verify.py
```

The checker uses only Python's standard library and `Fraction`. It rebuilds
176 rational parameter chambers and checks 675 chamber-vertex limits. It
prints `EXCLUSION NOT ACHIEVED` because the result is above the requested
comparison threshold.

## Why finitely many checks cover every parameter pair

For a fixed path p_(a,c), define its first characteristic inverses

```text
A(z)=inf{t:t+p(t)>=z},    B(z)=inf{t:t-p(t)>=z}.
```

They have the exact formulas

```text
A(z)=0                                      if z<=a;
A(z)=z                                      if a<z<=c;
A(z)=(z+c)/2                                if z>a, c<z<=c+2;
A(z)=z-1                                    if z>a, z>c+2.

B(z)=0                                      if z<=-a;
B(z)=max(z,(z+a)/2)                          if -a<z<=c;
B(z)=z+1                                    if z>c.
```

First inverses, including the left endpoint of a plateau, are intended.
The exact M1/M2 capture formulas are the ones proved in
`research/08-continuum/CHARACTERISTIC_RESPONSE.md`; for this particular
princess family the M2 cutoff is `-c`, including the case `a=1`.

For an early-turn path with `0<s<1`, away from parameter equality lines,
the unreflected capture is `a/2` when `a<=s` and `c>=0`, and is `s+3`
otherwise. The reflected capture is B(s). This follows directly by
comparing the princess's incoming leg with the monster's first outward
leg; a missed princess remains above its middle descending leg.

Every resulting payoff is affine in a,c on a finite arrangement of vertical
and horizontal threshold lines. The checker includes every threshold used
by these formulas. It clips each rectangle to the legal triangle `c>=-a`,
and also splits at `c=a` to keep the central-wait regions explicit. A
nondegenerate chamber's vertex average is an interior point; that point
selects the correct affine formula, which is then evaluated at every vertex
of the chamber's closure. A weighted affine payoff is bounded by the
largest of those vertex values.

### Initial coincidences and boundary jumps

The checker evaluates chamber formulas at boundary vertices rather than
silently substituting a generic formula for the actual boundary capture.
This is safe for an **upper** response ceiling. The map `(a,c)->p_(a,c)`
is continuous in the uniform path topology. Against a fixed continuous
monster, first capture time is lower semicontinuous: a convergent sequence
of earlier captures would give an equally early limiting intersection.
Thus the actual boundary payoff is no greater than a limiting payoff from
an adjacent chamber. Initial coincidences and central coalescence can make
that boundary payoff strictly smaller. All monsters finish their endpoint
traversals by time four, so no unbounded-horizon issue occurs.

Consequently the checked affine extensions bound the actual payoff at every
point of the closed parameter triangle. Integrating this pointwise bound
also covers every randomized law supported on the specified family.

## Independently checked useful formulas

For the endpoint sweep pair, the generic payoff is `(5+c)/4` for `a<1,c<1`.
The exceptional endpoint and central coincidences only reduce it.

For `0<=x<=1`, the M2(x) pair has, away from initial coincidences and with
`c<1`, the formula

```text
(5+c)/4                 if a<x;
1+(a-x)/4               if a>x and c>=-x;
3                       if a>x and c<-x.
```

Uniformly averaging x on `[0,1]` gives

```text
(5+c)/4 - a(1+c)/4 + a^2/8                  if 0<=c<1;
(5-7c)/4 - a/4 + (a^2+c^2)/8                if c<0.
```

At `c=1` these displayed generic expressions are upper bounds, because
the actual B(1) capture occurs earlier. A monster waiting at zero until
time one and then sweeping both endpoints has paired payoff a when
`a<=c`, and 3 when `a>c`.

## Scope of limiting families

The parameter triangle already includes arbitrarily small positive bounce
radii through `a>c` with `a-c` tending to zero. Those paths are covered by
the exact arrangement. The certificate does **not** automatically cover
uniformly nearby paths with an extra initial outward segment or additional
incoming waves. Capture payoffs can jump at coincidences, so a separate
uniform transfer argument would be required for such an extension.

The `research/` scripts preserve the bounded numerical discovery and its
unsuccessful exclusion target. The exact checker and certificate are the
authoritative scoped result; there is no claim that their mixture is
optimal even within the tested monster collection.
