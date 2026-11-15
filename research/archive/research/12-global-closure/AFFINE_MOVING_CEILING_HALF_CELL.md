# Affine moving-ceiling half-cell: a finite response bound

Research proof independently reviewed by the root, audit, and verification
agents, 2026-11-14.

Let

\[
 F(t,x)=c+at+bx,\qquad b\ge a\ge0,
\]

on the half-plane `x<=0`. Fix physical entry and exit states and duration,
and fix the incoming and outgoing scalar record intervals of an admissible
path. The spatial line `x=0` is an internal CDF interface. The application
is inside an affine half of a light square whose entry/exit coordinate box
intersected with `x<=0` lies inside the physical arena. This condition also
permits an affine physical boundary half-cell; actual endpoint resets are
accounted for separately in the global corollary.

**Claim.** There is a dominating replacement, preserving the physical
endpoints, duration, and both exit records, with at most

\[
 \boxed{13\text{ physical affine pieces}.}
 \tag{1}
\]

For `b>0`, the velocities are drawn from `-1,+1,0,-a/b`; the constant
`a=b=0` case is treated separately below. The proof does not apply an
unconstrained scalar speed-up across the moving ceiling. It first uses
the constrained earliest-arrival connectors below.

We prove the nondegenerate case `b>a>0` first, and put

\[
 \alpha=b+a,\qquad\beta=b-a,\qquad
 \kappa=1/\alpha+1/\beta.
\]

Translate time and scalar rank so the starting interface value is zero.
The half-plane constraint is then `Y<=at` for the absolute scalar rank
`Y=at+bx`. The initial scalar value need not be zero.

## 1. Earliest constrained monotone connectors

Suppose a scalar rank `r` is occupied at time `s`, with `r<=as`.

For a higher target `y>=r`, its earliest feasible arrival is

\[
 A_+(s;r,y)=\max\left(s+\frac{y-r}{\alpha},\frac ya\right).
 \tag{2}
\]

Move physically with velocity `+1` until either the target or the interface
is reached. In the latter case, hold at the interface until its scalar
value `at` reaches `y`. These movements attain (2). The two terms in the
maximum are necessary by the scalar speed bound and the ceiling.

For a lower target `y<=r`, the earliest arrival is

\[
 A_-(s;r,y)=s+\frac{r-y}{\beta},
 \tag{3}
\]

attained by physical velocity `-1`, which stays inside the half-plane.
Both arrival functions are nondecreasing in departure time `s`. The same
formulas apply to every intermediate rank along the connector.

An earlier feasible encounter with a given scalar rank can also be held
until an old encounter time: constant scalar rank has velocity `-a/b`,
which moves farther into the half-plane. This makes explicit why earlier
encounters do not destroy later feasibility.

## 2. Constrained first-visit normalization

For a finite polygonal path, use the usual expanding-record normalization:
remove turns that discover no new opposite record, retain the chronological
order of genuinely expanding record targets, and after the first global
record go directly to the other global record and then to the final rank.
Connect consecutive targets by (2) or (3).

Induction on the retained target sequence, using monotonicity in `s`, shows
that each retained target and each newly discovered intermediate rank is
visited no later than in the original path. Deleted nonrecord excursions
have no new target that needs to be retained. After the first global record,
only the other record side can still contain unvisited ranks, so the same
argument justifies direct travel there and then to the final rank.

Any remaining time is put in a final constant-scalar hold. If final rank
`f` is reached at time `s_f`, feasibility gives `f<=a*s_f`; it remains
feasible for all later times because `a>=0`. The physical final position is
the prescribed one at the original final time.

This normalization preserves both exit records and improves all new-level
first visits. Its only holds before the final scalar hold occur at the
interface. All other legs are physical unit-speed legs. It introduces no
additional nominated scalar record turns: an interface hold may subdivide
an upward connector, but creates no new nominated extremum.

If at most one exit record is new, direct constrained travel to that record
and then to the endpoint already gives at most two unit-speed legs, one
interface hold, and one final scalar hold. Hence only the case of two new
records can have unbounded initial word length.

## 3. Ordinary turn polytopes outside interface contacts

Split a normalized path at its first and last interface contacts, if any.
Call the pieces outside those contacts its exterior prefix and suffix.
They have no interface holds in their open time intervals. After removing
nonrecord turns by Section 2 when necessary, each is an ordinary fastest
expanding-record tour, with at most a final constant-scalar hold. Such a
removal either reduces its nominated turn count or produces a new interface
contact; it cannot increase the number of nominated turns outside contacts.

Consider one such boundary-free exterior piece, with fixed physical
endpoints, times, and incoming and outgoing records. If both exit records
are new, shift its initial scalar value to zero and denote the global
records by `-B,H`, the final scalar value by `f`, and the genuinely partial
turn magnitudes by `z_1,...,z_m`. Fix the order of the two global records.

All fastest-leg arrival times and scalar vertex values are affine in the
`z_i`. Impose:

* the two bounded monotone-chain inequalities;
* the ordinary duration inequality;
* the moving-ceiling inequality at every physical leg vertex;
* the moving-ceiling inequality at the start of the final scalar hold.

These are linear inequalities, so they define a nonempty bounded rational
polytope when the field and endpoint data are rational. The last rationality
qualification is irrelevant for the geometric proof.

On a maximal-speed physical leg, position is affine, so checking the
ceiling at the vertices is sufficient. The final constant-scalar hold
moves farther left, so checking its start is sufficient. No hidden
interior-in-time ceiling inequality is omitted.

The exact first-visit objective has quadratic part

\[
 -\kappa\left(\sum_i z_i^2+
                 \sum_{i=1}^{m-1}z_i z_{i+1}\right),
\]

and is jointly concave, as in the ordinary four-leg theorem. A minimizing
vertex of this constrained polytope therefore exists.

### Endpoint and final-hold rows

The physical initial and terminal states are fixed, so their own ceiling
inequalities are constant rows. They do not restrict a perturbation of
partial turns.

The start time of the final scalar hold is the full fastest tour duration:

\[
 s_f=\kappa\left(H+B+\sum_i z_i\right)+C,
\]

where `C=-f/beta` or `C=f/alpha` according to the fixed last-global-record
order. Its ceiling row is consequently a lower bound on the same sum
`sum z_i` that occurs in the duration upper bound. It does not introduce
an independent partial-sum equality.

If a global record vertex coincides with the fixed terminal point, its
arrival time is this same full-tour duration, after deleting the zero
terminal travel. Thus its ceiling row is again parallel to the sum row.
Vertices coinciding with the initial point have zero adjacent travel and
are removed as nonexpanding turns before the vertex count.

## 4. A vertex either gives four legs or creates a new interface contact

Group equal-valued partial turns within each monotone chain into maximal
free blocks, exactly as in the four-leg proof. If there is no active
ceiling row at a genuinely interior physical turn, all non-sum ceiling
rows have slack. A sufficiently small two-sided block perturbation
preserves them.

If the sum is unconstrained locally, one free block gives such a
perturbation. If either the duration upper bound or final-hold lower bound
is active, two free blocks can be shifted in opposite amounts weighted by
their sizes, preserving the sum. The same works if both parallel bounds
are active. Therefore a vertex without a new interior interface contact
has at most one free block.

Remove nonexpanding turns using Section 2. There remains at most one
genuinely partial turn, the two global records, and final travel: at most
four unit-speed legs, possibly interface holds inserted in the upward
connectors, and a final scalar hold. If the removal introduces interface
contacts, every inserted interface hold lies between the new first and
last contacts and is absorbed by the next middle replacement. Each exterior
portion of this bounded word has at most four unit-speed legs and the final
scalar hold, hence at most five pieces.

Otherwise, an additional active ceiling row is a physical interface
contact at an interior nominated turn. In an exterior prefix it moves
the first contact strictly earlier; in an exterior suffix it moves the
last contact strictly later. At least one of the old exterior nominated
turns is thereby transferred into the middle rather than remaining a
genuinely interior turn of that exterior piece.

This is the termination measure: the number of nominated scalar turn
vertices in the exterior under consideration, excluding its physical
endpoints. It decreases whenever an interior cap row forces another
iteration. Endpoint and final-arrival rows were treated separately above;
they cannot be counted as a decrease without actually moving a contact.

If a new contact occurs only at the start of the final scalar hold, its
row was parallel to the sum row, so the four-leg conclusion already holds.
Likewise, interface holds introduced while deleting nonexpanding turns do
not obstruct termination: at least one old turn has been deleted, or the
word already has the bounded four-leg form.

## 5. Compress the middle without changing its exit records

The whole piece between first and last interface contacts lies in `x<=0`.
Section 1 of `MOVING_KINK_RETURN_COMPRESSION.md` replaces it by an immediate
negative triangle followed by an interface hold, preserving both exit
records and not increasing cost. It uses at most three physical pieces.

After a prefix vertex creates an earlier first contact, apply this
replacement on the enlarged middle. The prefix optimization had preserved
records at the old first contact; the middle replacement preserves records
at its own endpoint, so the fixed later suffix remains valid. The new
exterior prefix has fewer nominated interior turns unless it was already
in the bounded form.

Finish all prefix reductions first. Then perform the corresponding suffix
reductions. A later last contact enlarges the middle but leaves the already
bounded prefix unchanged. The suffix optimization preserves the final
records; the middle replacement preserves the records entering the new
shorter suffix. Thus the complete original exit records remain unchanged
throughout the procedure.

Any interface subdivisions introduced while re-normalizing a bounded
nominated word lie in the middle after splitting at the new first and last
contacts. Each exterior contains at most the four unit-speed legs of that
word, together with its possible final scalar hold. There are therefore at
most five pieces before the first contact, three between first and last
contacts, and five after the last contact, proving (1).
If there are no contacts, the vertex argument either already supplies the
five-piece bound or creates the first contacts and starts this procedure.
If first and last contacts coincide, the middle has zero duration.

## 6. Arbitrary paths, degenerate coefficients, and physical containment

For an arbitrary Lipschitz path, polygonal interpolation through entry,
exit, and times attaining the two scalar extrema preserves the half-plane
and derivative bounds. Running records and integrated cost converge
uniformly. Apply the finite-word result and pass to a subsequence in the
compact duration parameter space for at most thirteen pieces from the
fixed velocity set. This preserves physical endpoints and both exit
records, and passes the cost comparison to the limit.

For `a=0`, the ceiling is a constant scalar bound. A scalar tour preserving
the actual attained global records stays beneath it, and the ordinary
four-leg proof applies. Cases with old records outside the actually
visited range use the direct one-new-record or no-new-record construction.

For `b=a>0`, the scalar field is nondecreasing along every legal physical
path. Only an upper record can be new. Its earliest feasible visit is
given by (2), and a final constant-scalar leg has physical velocity `-1`.
The direct construction is bounded and feasible. When `a=b=0`, the field
is constant and a feasible two-run physical path suffices.

Every replacement has speed at most one and retains the physical endpoint
states and times. Its light coordinates remain in their coordinatewise
entry/exit box. Intersecting this box with the established half-plane
constraint keeps the path inside the original half-square and, under the
stated intersection containment, inside the physical arena. No scalar
field is extended outside that legal half-square.

## Independent review

Both peer reviewers and the root independently checked the constrained
first-visit normalization, the classification of endpoint and final-hold
rows, the strictly decreasing exterior-turn count, the record-preserving
middle composition, the thirteen-piece count, and the degenerate cases.
The proof is now frozen after those reviews.
