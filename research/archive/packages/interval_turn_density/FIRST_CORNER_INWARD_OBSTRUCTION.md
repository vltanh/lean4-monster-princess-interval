# A first-turn corner graph still fails with diffuse second turns

The singular double-corner law was excluded in
`DOUBLE_CORNER_INWARD_CONTACTS.md`. Spreading only its second turn does
not repair the first-corner obstruction. The statement here permits a
two-dimensional physical monster law, but assumes an ordinary initial
outward leg followed by a constant-U incoming leg in the proposed lower
path. It does not exclude a curved incoming transition.

## 1. Physical support and pure-path variation

Let `a(b),u(b)` be differentiable increasing fronts with
`0<a(b)<u(b)<1`. Place a nonnegative density `m(b,s) db ds` on

    I(u(b),-a(b),s),       u(b)<s<=1.                 (1)

The first turn is the initial/incoming corner of princess b, while the
second turn is free and diffuse. Consider the ordinary princess q with

    a=a(q), u=u(q), -a<c<0,

and allow u to vary with a,c fixed. This remains a legal path in a
neighborhood of its current u. Suppose q is interior to the curve
parameter support, `u'(q)>0`, and the density is sufficiently regular
locally for one-sided differentiation and dominated convergence. Bounded
continuous densities are sufficient. There is no mass on `s=u(b)` in
(1); that degenerate route is negative M1 and has a different contact
limit.

For b near q the monster start `u(b)` is strictly above the princess
initial a. Its first inward leg captures exactly when both

    a>=a(b),                 u>=u(b).

Thus the moving first-capture cutoff is

    b<=min(a^{-1}(a),u^{-1}(u)).                      (2)

For a fixed nondegenerate second turn s above u, the missed first leg
instead captures on `U=s`, after the princess's incoming segment. The
four-score difference between the missed and captured branches is

    s-u+c+a>0                                       (3)

at b=q. Its reflected capture is unchanged. The cutoff moves on the
lower-u side and stays fixed on the higher-u side.

## 2. Exact upward incoming-level jump

Integrating (3) over the second turns gives

    F_u(u+)-F_u(u-)
       =1/u'(q) * integral_u^1
             [s-u+c+a] m(q,s) ds.                   (4)

This is strictly positive whenever the conditional row has positive
nondegenerate mass. The second-turn capture boundaries are now diffuse
and contribute continuous derivatives. The triangular sliver adjacent
to `s=u(b)` contributes only o(epsilon) to the finite midpoint
difference; it does not cancel (4).

If the remaining monster score is differentiable in this variation,

    F(u+epsilon)+F(u-epsilon)-2F(u)
       =epsilon/u'(q) * integral_u^1
             [s-u+c+a]m(q,s)ds+o(epsilon)>0.         (5)

At least one perturbed princess has a strictly larger payoff. Hence the
ordinary initial/incoming corner cannot be an upper best response for
the law (1) under these hypotheses. Positive-M2 boundary mass is not
used: setting g to zero does not remove this obstruction.

This does not prove that every initial unit-speed run is impossible
when g has slack. A unit-speed run followed by a genuinely curved
incoming transition need not have the minimum cutoff (2). A spread in
monster first-turn support, zero conditional row mass, or an additional
opposing nonsmooth score also requires a separate analysis. The claim
is specifically about the ordinary +1/-1 corner with the first-turn
graph (1).

## 3. Independent exact physical checks

`verify_first_corner_inward.py` uses the rational fronts from the
double-corner verifier, but integrates the full second-turn interval
`u(b)<s<1`. It uses three positive polynomial densities and two
princess ranks. It passes 3,312 exact rational checks:

* 66 complete two-dimensional physical integrals, partitioned into
  3,234 independent capture triangles;
* six exact one-sided incoming-level derivative jumps;
* six strict finite incoming-level midpoint gains.

The reference evaluates actual first segment intersections on a
partition built from physical endpoint and line-intersection events.
Neither (2) nor (4) is used to compute the integrated scores. Exact
polynomial differentiation then checks (4). These fixtures verify the
identity and its sign; they are not a numerical strategy fit.
