# Final-characteristic price for a pre-one inward phase

This note concerns a branch whose **final** incoming motion ends at
`U=u<1`, followed by its final outward leg `V=c<0`. This is a branch
assumption, not a theorem that all optimal paths have this form. In
particular, a second incoming phase above `U=1` is outside the conclusion.

## 1. Exact three-part derivative

Let the princess have initial a, an arbitrary monotone prefix inverse
`U=phi(V)` ending at `(u,c)`, and then move outward to the endpoint.
Write `psi(z)=2 alpha(z)-z` for its **first** inverse. The endpoint
variation extends or truncates the prefix and changes its final
outgoing characteristic. Assume the relevant moving boundaries have
regular conditional densities; exact boundary atoms are addressed
separately below.

An inward monster has initial z, first turn V=v, and second turn U=s,
with `0<z<=s<=1`, `-z<=v<z`. Let its law be `mu`, with density
`i(z,v,s)` when writing the edge integrals. A measure supported on a
surface uses the corresponding conditional measure at v=c instead.

Let `D_I` be the c derivative of four times the inward component's
expected capture time. It has the exact form

    D_I = Q_c + E_plus - E_minus,                    (1)

where the nonnegative mass term is

    Q_c = mu{z>u}
          +mu{a<z<=u<s, v<psi(z)},                   (2)

and

    E_plus  = integral_(s>z>u) (s-z)i(z,c,s) dz ds,
    E_minus = integral_(z<a, s>u)
                          (2s+6-c-u)i(z,c,s) dz ds.  (3)

The physical domain is implicit. The first term in (2) has s>=z>u.
The two sets in (2) are disjoint, and therefore

    0<=Q_c<=mu{z>a, s>u}<=mu{z>a}.                    (4)

To see (1), a monster starting above u catches the princess on an alpha
threshold after its final turn, whether its first inward leg succeeds
or misses. Increasing c contributes one unit of four-score per such
row. For `a<z<=u`, only a row which misses the first leg and has s>u
contributes this unit; missing uses `v<psi(z)` with the first inverse.
The positive edge in (3) is the change from capture at alpha(z) to
capture at alpha(s). The negative edge is the change from the late
endpoint sweep to middle-leg capture as v=c is crossed. The reflected
contact is independent of c for this negative final characteristic.

These signs are important. The inward component does not consist only
of the negative column price, and the positive first-turn edge cannot
be discarded without a support argument.

## 2. What active-support deletion removes

Suppose an ordered lower family has atomless, strictly ordered final
outgoing characteristics. For its rank q with final characteristic c,
let u be its outgoing onset. Then

    R(S,c)=q=R(1,c)       for u<=S<=1.                (5)

The finite plateau-deletion theorem in
`research/10-turn-density/INWARD_TURN_DOMINANCE.md` applies directly:
if an inward monster with first V=c has second S>u, reducing S within
this plateau changes no captured frontier and strictly reduces its
expected capture time. Such a row cannot be active. No sign assumption
on a center-source derivative is needed.

This removes the strict negative edge `E_minus`. It also removes
`E_plus`: there z>u, and hence

    R(S,c)=q<=A(z).

The outward excursion captures no new rank above the initial frontier;
collapsing it is dominated by the direct negative-M1 route. Thus, when
there is no conditional contact atom at S=u,

    D_I=Q_c,           0<=D_I<=mu{z>a}.               (6)

For a finite genuine inward law supported at z<1, the right side tends
to zero as a tends to one. No assumption excluding a second-turn atom
at s=1 is needed for this bound. The degenerate endpoint row z=s=1 is
direct endpoint M1 and must be accounted for in the endpoint mass.

Equation (5) is not valid merely from transport. It uses the final
outgoing leg and the absence of a final-characteristic atom. Before
that outgoing onset one only has `R(S,c)<=A(S)`, and the stronger future
row bound `R(1,c)<=A(S)` need not hold.

## 3. Conditional endpoint consequence

For the signed-M1/M2 baseline, write p=f+g and let k denote its
pre-one alpha marginal, excluding the separately counted inward law.
Let w0 be the endpoint-M1 atom. In a terminal region where other compact
attachments contribute no c derivative, the exact free-boundary
stationarity equation is

    (6-2c)g(-c)
      =w0+Pbar(a)+Kbar(u)-(2+c-u)p(-c)+D_I.           (7)

Here `Pbar(a)=integral_a^1 p` and `Kbar(u)=integral_u^1 k`.
Equation (7) requires an interior final-characteristic variation. It
does not apply to a path constrained to c=-a or to an unexamined atom at
the first `U=1` contact.

If a,u tend to one, c tends to minus one, p and k are integrable, the
support deletion of Section 2 holds, and

    (2+c-u)p(-c) -> 0,                               (8)

then (4), (6), and (7) imply

    g(-c) -> w0/8.                                  (9)

For example, (8) holds for a regular integrable power tail or an
eventually nondecreasing integrable p: legality gives
`1-u<=1-a<=1+c`, and hence `2+c-u<=2(1+c)`.

Thus simply deleting the positive-M2 boundary mass does not close this
regular **pre-one final-incoming** class. A post-one incoming phase
changes (7): the endpoint-M1 capture can already have occurred at the
first crossing, and the post-one alpha density includes `f(2-U)`.
Neither (7) nor (9) is asserted for that different branch.

## 4. Contact atoms are a separate condition

The strict inequalities in (3) deliberately exclude a conditional atom
at S=u. First inverses at an incoming plateau cannot be replaced by its
last inverse. If a positive contact component follows a decreasing
outgoing-onset graph `S=S_out(v)`, it creates the upward c kink already
proved in `FREE_SECOND_INWARD_CONTACTS.md`. The singular first-turn
corner does not cancel it; see `DOUBLE_CORNER_INWARD_CONTACTS.md`.

An active contact has `R(S,c)>A(z)`, so its initial z is strictly below
the princess initial a. It therefore lies in the low-start branch,
separated from an initial equality contact. For a regular contact
column on a decreasing onset, a differentiable remaining score cannot
cancel the positive kink. A locally increasing or singular oscillatory
outgoing onset, a final-characteristic atom, or an explicitly opposing
nonsmooth contribution requires a different trace analysis. Those
possibilities are not discarded by (6)-(9).

## 5. Physical identity checks

`verify_terminal_inward_c.py` passes 7,104 exact checks: 48 one-sided
derivatives, 312 complete physical slice integrals over 6,732 independent
capture triangles, and 12 nonnegative edge-free mass identities.

The fixed second-turn slices test the linear measure identity, including
both edge signs. The fixtures have ordinary and curved initial prefixes,
a genuinely curved incoming endpoint whose u changes with c, second
turns on both sides of u, and first-turn intervals that either include
or avoid c. Support deletion itself uses the separate exact finite
comparison theorem; the fixtures are not an assertion that the supplied
slices form an active equilibrium law.
