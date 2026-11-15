# Exact initial-start reduction for a fixed opposite characteristic and tail

Let the Monster's first leg have unit direction \(d\in\{-1,1\}\). Orient
space by \(y=dx\), put \(b=da\), and retain the opposite characteristic
\(c=t+dx\) at its first reversal. Its next fixed vertex is
\((t_2,y_2)\), with \(t_2+y_2=c\); every later vertex remains fixed.
The variable first turn is

\[
(t_1,y_1)=((c-b)/2,(c+b)/2).
\]

Assume the retained tail is legal and contains both endpoints. The full
admissible initial interval is

\[
\max(-1,c-2t_2)\le b\le\min(1,c,2-c).
\]

The lower bound ensures the first descending leg does not pass its next
fixed vertex; the upper bounds impose initial legality, nonnegative first
turn time, and \(y_1\le1\). The remaining condition \(y_1\ge-1\) follows
from \(y_1\ge y_2\ge-1\). Zero-length first or second legs are allowed and
use their physical closed-contact trace.

## Pointwise monotonicity inside an initial-support gap

For \(0\le t\le t_2\), the oriented Monster is exactly

\[
m_b(t)=\min(b+t,c-t).
\]

Take \(b_1<b_2\) with no Princess initial position in
\([b_1,b_2)\). An initially ahead Princess starts at or above \(b_2\).
The second Monster is pointwise higher before \(t_2\), and identical
afterwards, so continuity makes its first capture no later. Equality at
\(b_2\) gives capture at time zero.

An initially behind Princess starts strictly below \(b_1\). By the unit
speed bound, it cannot meet either outward branch \(b+t\). Before the later
first turn, the common descending line \(c-t\) is also above
\(b_1+t\), hence above that Princess. Its first possible capture is
therefore on the same descending line or the identical later tail, at the
same time under both Monsters.

Consequently every individual capture time, and hence every expected cost,
is nonincreasing as \(b\) advances through an open initial-support gap to
its right endpoint. This assertion must not be extended through the left
endpoint atom: leaving exact initial contact may increase its capture time.

If the initial support is finite, the infimum over the entire legal initial
interval is attained among its upper boundary and all initial support atoms
in the interval. Including both legal boundaries is harmless. The statement
holds for any coupling of the Princess paths. In particular it holds for
their common-quantile coupling, whose initial marginal has the same support.

## Germ and family scope

For a fixed finite rational-germ law, apply the argument pointwise at every
sufficiently small positive parameter. All support/boundary comparisons are
eventually fixed, so a common explicit sign radius makes the same finite
candidate list valid uniformly. The competing initial start may be an
arbitrary real function of the parameter; it need not itself be a rational
germ. Distinct actual initial germs with equal limits remain distinct.

This reduces a continuous initial-start parameter for each supplied tail.
It does not restrict the possible tail or certify all Monster paths.
The default implementation tests only support germs whose limits agree with
at least one old start for that tail, plus the legal boundaries. That mode is
an explicitly restricted discovery subset. `--all-initial` releases the
complete initial family for every supplied tail.

## Exact screening and first result

The raw paired payoff is a lower bound on the common-quantile payoff.
Accordingly a raw limiting cost at least the target safely excludes an
ordered-law attack. Every remaining candidate is scored using the exact
unit-route rank records. Returned columns are then scored against every
frozen pure row, including zero-weight rows.

On the pinned 332-row `round003` input, 1,443 old bank routes give 345 legal
completed tail families. The same-limit/boundary mode produces 2,363
candidates. Exact raw screening discards 2,286 at target 1.4192365094;
all 77 remaining candidates are ordered-law attacks. The strongest returned
route is

\[
(0,3/16-\epsilon),\quad
(13/32+\epsilon/2,19/32-\epsilon/2),\quad
(2,-1),\quad(4,1).
\]

Its first outward characteristic is exactly \(U=1\). Its limiting ordered
and raw cost agree:

\[
\frac{57919504145512204712631367442479}
     {41215599999999996741371017200000}
=1.4052811106841148\ldots.
\]

This is a rejection of the named mixture. It is not a game bound. The
discovery changes initial contacts while retaining existing tail geometry;
it introduces no path mesh.

## Replay

```sh
node packages/interval_global_closure/fixed_tail_start_separator.mjs \
  ROWS.json MASTER.json BANK.json OUTPREFIX --target TARGET

node packages/interval_global_closure/verify_fixed_tail_starts.mjs \
  inputs/germ_v8_fixture_inputs.json reports/fixed_tail_starts.json
```

The verifier uses chronological segment intersections independently of the
first-inverse scorer. It checks both pointwise and ordered monotonicity,
ordinary and nested-germ turn characteristics, multiple-turn tails,
legality boundaries, and an exact initial-atom counterexample to extending
the gap monotonicity through an atom.
